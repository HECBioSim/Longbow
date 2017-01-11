# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of the
# HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the UK
# biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# Longbow is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""A module containing methods for processing application command-lines.

The applications module contains methods for processing the aspect of jobs
which relate to external applications (such as an MD package). The following
methods can be found within this module:

testapp(jobs)
    This method will make an attempt to check that the application executables
    required to run a job/s is present on the specified host/s. This method is
    capable of using the module system.

processjobs(jobs)
    This method will process information that is given as an intended target to
    be passed on to the executable at run time. It will check that required
    parameters (provided the respective plug-in is configured correctly) have
    been supplied, and that all files and their dependencies (again provided
    that the respective plug-in is configured for this) exist on disk.
"""

import logging
import os

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.shellwrappers as shellwrappers
import Longbow.apps as apps


LOG = logging.getLogger("Longbow.corelibs.applications")


def testapp(jobs):
    """A method to test that executables and their modules are launchable.

    This method will make an attempt to check that the application executables
    required to run a job/s is present on the specified host/s. This method is
    capable of using the module system.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    checked = {}

    LOG.info("Testing the executables defined for each job.")

    for job in jobs:

        # If we haven't checked this resource then it is likely not in the dict
        if jobs[job]["resource"] not in checked:

            checked[jobs[job]["resource"]] = []

        # Now check if we have tested this exec already.
        if jobs[job]["executable"] not in checked[jobs[job]["resource"]]:

            # If not then add it to the list now.
            checked[jobs[job]["resource"]].extend([jobs[job]["executable"]])

            LOG.info("Checking executable '%s' on '%s'",
                     jobs[job]["executable"], jobs[job]["resource"])

            cmd = []

            if jobs[job]["modules"] is "":

                LOG.debug("Checking without modules.")

            else:
                LOG.debug("Checking with modules.")

                for module in jobs[job]["modules"].split(","):

                    module = module.replace(" ", "")
                    cmd.extend(["module load " + module + "\n"])

            cmd.extend(["which " + jobs[job]["executable"]])

            try:

                shellwrappers.sendtossh(jobs[job], cmd)
                LOG.info("Executable check - passed.")

            except exceptions.SSHError:

                LOG.error("Executable check - failed.")
                raise


def processjobs(jobs):
    """A method to process the application portion of the command-line.

    This method will process information that is given as an intended target to
    be passed on to the executable at run time. It will check that required
    parameters (provided the respective plug-in is configured correctly) have
    been supplied, and that all files and their dependencies (again provided
    that the respective plug-in is configured for this) exist on disk.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    LOG.info("Processing job/s and detecting files that require upload.")

    # Process each job.
    for job in jobs:

        filelist = []
        appplugins = getattr(apps, "PLUGINEXECS")
        app = appplugins[jobs[job]["executable"]]
        foundflags = []
        substitution = {}

        LOG.debug("Command-line arguments for job '%s' are '%s'",
                  job, " ".join(jobs[job]["executableargs"]))

        # Check for any files that are located outside the work directory or
        # absolute paths.
        for arg in jobs[job]["executableargs"]:

            if arg.count(os.path.pardir) > 0 or os.path.isabs(arg):

                raise exceptions.RequiredinputError(
                    "In job '{0}' input files are being provided with absolute"
                    " paths or from directories above localworkdir. This is "
                    "not supported".format(job))

        # If we have multiple jobs.
        if len(jobs) > 1:

            # Add the job name to the path.
            jobs[job]["localworkdir"] = os.path.join(
                jobs[job]["localworkdir"], job)

        # Check that the directory exists.
        if os.path.isdir(jobs[job]["localworkdir"]) is False:

            # If not, this is bad.
            raise exceptions.DirectorynotfoundError(
                "The local job directory '{0}' cannot be found for job '{1}'"
                .format(jobs[job]["localworkdir"], job))

        # Detect command-line parameter substitutions.
        try:

            substitution = getattr(
                apps, app.lower()).detectsubstitutions(
                    list(jobs[job]["executableargs"]))

        except AttributeError:

            pass

        # Process the command-line.
        foundflags = _proccommandline(jobs[job], filelist, foundflags,
                                      substitution)

        # Validate if all required flags are present.
        _flagvalidator(jobs[job], foundflags)

        # Setup the rysnc upload masks.
        if jobs[job]["upload-include"] != "":

            jobs[job]["upload-include"] = jobs[job]["upload-include"] + ", "

        jobs[job]["upload-include"] = (jobs[job]["upload-include"] +
                                       ", ".join(filelist))

        jobs[job]["upload-exclude"] = "*"

        # Replace the input command line with the execution command line.
        jobs[job]["executableargs"] = (jobs[job]["executable"] + " " +
                                       " ".join(jobs[job]["executableargs"]))

        LOG.info("For job '%s' - execution string: %s",
                 job, jobs[job]["executableargs"])

    LOG.info("Processing jobs - complete.")


def _flagvalidator(job, foundflags):
    """Validate that required command-line flags are provided."""
    # Initialisation.
    appplugins = getattr(apps, "PLUGINEXECS")
    app = appplugins[job["executable"]]
    execdata = getattr(apps, app.lower()).EXECDATA[job["executable"]]

    # Final check for if any required flags are missing.
    flags = list(set(execdata["requiredfiles"]) - set(foundflags))

    # If there are any missing still then tell the user.
    if len(flags) > 0:

        # Firstly is this due to it being an either type flag?
        for flag in flags:

            if "||" in flag:

                tmpflags = flag.split(" || ")
                tmpflag = list(set(tmpflags).intersection(set(foundflags)))

                if len(tmpflag) > 0:

                    flags.remove(flag)

    # If there are any missing still then tell the user.
    if len(flags) > 0:

        raise exceptions.RequiredinputError(
            "In job '{0}' either there is a flag and/or file missing on the "
            "command line '{1}'. See user documentation for plug-in '{2}'"
            .format(job["jobname"], flags, app))


def _markfoundfiles(arg, initargs, foundflags):
    """Method to mark file flags as found."""
    try:

        pos = initargs.index(arg) - 1

    except ValueError:

        pos = initargs.index("../" + arg) - 1

    # In cases where there is a single input file as the first parameter. This
    # should cover cases such as:
    # exec input.file
    # exec input.file > output.file
    if arg == initargs[0]:

        foundflags.append("<")

    # All other cases should pretty much be formats like:
    # exec -flag file -flag file -flag file
    elif len(initargs) > 1 and initargs[pos] not in foundflags:

        foundflags.append(initargs[pos])

    return foundflags


def _proccommandline(job, filelist, foundflags, substitution):
    """Command-line processor.

    This method selects which type of command-line we have.

    """
    # Initialisation.
    appplugins = getattr(apps, "PLUGINEXECS")
    app = appplugins[job["executable"]]
    args = list(job["executableargs"])
    subexecs = getattr(
        apps, app.lower()).EXECDATA[job["executable"]]["subexecutables"]

    try:

        for arg in args:

            if (arg != "<" and arg != ">" and arg[0] != "-" and
                    arg not in subexecs):

                foundflags = _procfiles(job, arg, filelist, foundflags,
                                        substitution)

    except (IndexError, ValueError):

        raise exceptions.RequiredinputError(
            "In job '{0}', the command-line arguments for the application "
            "could not be understood. Check the documentation for more "
            "information on how to format command-lines."
            .format(job["jobname"]))

    return foundflags


def _procfiles(job, arg, filelist, foundflags, substitution):
    """Processor for finding flags and files."""
    # Initialisation.
    appplugins = getattr(apps, "PLUGINEXECS")
    app = appplugins[job["executable"]]
    initargs = list(job["executableargs"])

    # Check for as many files as there are replicates (default of 1).
    for rep in range(1, int(job["replicates"]) + 1):

        fileitem = ""

        # If we do only have a single job then file path should be.
        if int(job["replicates"]) == 1:

            fileitem = _procfilessinglejob(app, arg, job["localworkdir"])

        # Otherwise we have a replicate job so check these.
        else:

            # Add the repX dir
            if ("rep" + str(rep)) not in filelist:

                filelist.append("rep" + str(rep))

            fileitem = _procfilesreplicatejobs(
                app, arg, job["localworkdir"], initargs, rep)

            job["executableargs"] = initargs

        # If we have a valid file
        if os.path.isfile(os.path.join(job["localworkdir"], fileitem)):

            _markfoundfiles(arg, initargs, foundflags)

            # Search input file for any file dependencies.
            try:

                getattr(apps, app.lower()).file_parser(
                    fileitem, job["localworkdir"], filelist, substitution)

            except AttributeError:

                if fileitem not in filelist:

                    filelist.append(fileitem)

    return foundflags


def _procfilessinglejob(app, arg, cwd):
    """Processor for single jobs."""
    fileitem = ""

    if os.path.isfile(os.path.join(cwd, arg)):

        fileitem = arg

    # Hook for checking plugin specific file naming scenarios eg (gromacs
    # -deffnm test) actually referring to test.tpr
    else:

        try:

            fileitem, _ = getattr(
                apps, app.lower()).defaultfilename(cwd, arg, "")

        except AttributeError:

            pass

    return fileitem


def _procfilesreplicatejobs(app, arg, cwd, initargs, rep):
    """Processor for replicate jobs."""
    fileitem = ""
    tmpitem = ""

    # We should check that the replicate directory structure exists.
    if os.path.isdir(os.path.join(cwd, "rep" + str(rep))) is False:

        os.mkdir(os.path.join(cwd, "rep" + str(rep)))

    # If we have a replicate job then we should check if the file resides
    # within ./rep{i} or if it is a global (common to each replicate) file.
    if os.path.isfile(os.path.join(cwd, "rep" + str(rep), arg)):

        fileitem = os.path.join("rep" + str(rep), arg)

    # Otherwise do we have a file in cwd
    elif os.path.isfile(os.path.join(cwd, arg)):

        fileitem = arg

        # Also update the command line to reflect a global file.
        if arg in initargs:

            initargs[initargs.index(arg)] = os.path.join("../", arg)

    # Hook for checking plugin specific file naming scenarios
    # eg (gromacs -deffnm test) actually referring to test.tpr
    else:

        try:

            tmpitem, _ = getattr(apps, app.lower()).defaultfilename(
                cwd, os.path.join("rep" + str(rep), arg), "")

        except AttributeError:

            pass

        # If we have a positive check then file found in rep$i directories.
        if tmpitem is not "":

            fileitem = tmpitem

        # Otherwise check for global one.
        else:

            try:

                fileitem, initargs = getattr(
                    apps, app.lower()).defaultfilename(cwd, arg, initargs)

            except AttributeError:

                pass

    return fileitem
