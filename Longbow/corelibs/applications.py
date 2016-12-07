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
        if (jobs[job]["executable"] not in checked[jobs[job]["resource"]] and
                (jobs[job]["nochecks"] is False or
                 jobs[job]["nochecks"] == "false")):

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

        # Process the command-line.
        foundflags = _proccommandline(jobs[job], filelist)

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
            "In job '{0}' there are missing flags on the command line '{1}'. "
            "See user documentation for plug-in '{2}'"
            .format(job["jobname"], flags, app))


def _proccommandline(job, filelist):
    """Command-line processor.

    This method selects which type of command-line we have.

    """
    # Initialisation.
    args = job["executableargs"]
    appplugins = getattr(apps, "PLUGINEXECS")
    app = appplugins[job["executable"]]
    foundflags = []
    substitution = {}

    # Detect command-line parameter substitutions.
    try:

        substitution = getattr(apps, app.lower()).detectsubstitutions(args)

    except AttributeError:

        pass

    try:

        # Determine the command-line type and call the processor method. Start
        # with command-lines of the type exec < input.file.
        if args[0] == "<":

            # Command-line type exec < input.file
            _proccommandlinetype1(job, filelist, foundflags, substitution)

        elif len(args) == 1 and args[0] != "<":

            # Command-line type exec input.file
            _proccommandlinetype4(job, filelist, foundflags, substitution)

        elif "-" in args[0]:

            # Command-line type exec -i file -c file
            _proccommandlinetype2(job, filelist, foundflags, substitution)

        elif "-" not in args[0] and "-" in args[1]:

            # Command-line type exec subexec -i file -c file
            _proccommandlinetype3(job, filelist, foundflags, substitution)

        else:

            raise ValueError

    except (IndexError, ValueError):

        raise exceptions.RequiredinputError(
            "In job '{0}', the command-line arguments for the application "
            "could not be understood. Check the documentation for more "
            "information on how to format command-lines."
            .format(job["jobname"]))

    return foundflags


def _proccommandlinetype1(job, filelist, foundflags, substitution):
    """Processor forcommand-line type 'exec < input.file > output.file'."""
    args = list(job["executableargs"])
    initargs = list(job["executableargs"])

    # Check the length of the command line.
    if len(args) > 1:

        # Mark the flag as found
        foundflags.append("<")

        # Process files and parameters.
        _procfiles(job, args[1], initargs, filelist, substitution)

    # Looks like the command line is too short to contain the input file.
    else:

        raise exceptions.RequiredinputError(
            "In job '{0}' it appears that the input file is missing, check "
            "your command line is of the form longbow [longbow args] "
            "executable '<' [executable args]".format(job["jobname"]))


def _proccommandlinetype2(job, filelist, foundflags, substitution):
    """Processor for command-line type 'exec --input file1 -file file2'."""
    args = list(job["executableargs"])
    initargs = list(job["executableargs"])

    # Run through each one.
    for arg in args:

        # If we have a flag (starting with '-') and it is in the list of
        # required flags.
        if arg[0] == "-":

            # Mark the flag as found
            foundflags.append(arg)

        # Otherwise it could just be a file or a parameter.
        else:

            # Process files and parameters.
            _procfiles(job, arg, initargs, filelist, substitution)


def _proccommandlinetype3(job, filelist, foundflags, substitution):
    """Processor command-line type 'exec subexec --file1 v1 -file2 p2'."""
    args = list(job["executableargs"])
    initargs = list(job["executableargs"])

    # Run through each one.
    for arg in args[1:]:

        # If we have a flag (starting with '-') and it is in the list of
        # required flags.
        if arg[0] == "-":

            # Mark the flag as found
            foundflags.append(arg)

        # Otherwise it could just be a file or a parameter.
        else:

            # Process files and parameters.
            _procfiles(job, arg, initargs, filelist, substitution)


def _proccommandlinetype4(job, filelist, foundflags, substitution):
    """Processor for command-line type 'exec input.file'."""
    args = list(job["executableargs"])
    initargs = list(job["executableargs"])

    # Lets make sure that we actually have something to load.
    if len(args) > 0:

        # Mark the flag as found
        foundflags.append("<")

        # Process files and parameters.
        _procfiles(job, args[0], initargs, filelist, substitution)

    # Looks like the command-line is too short to contain the input file so
    # raise an exception.
    else:

        raise exceptions.RequiredinputError(
            "In job '{0}' it appears that the input file is missing, check "
            "your command line is of the form: longbow [longbow args] "
            "executable '<' [executable args]".format(job["jobname"]))


def _procfiles(job, arg, initargs, filelist, substitution):
    """Processor for finding flags and files."""
    # Initialisation.
    appplugins = getattr(apps, "PLUGINEXECS")
    app = appplugins[job["executable"]]

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

            # Search input file for any file dependencies.
            try:

                getattr(apps, app.lower()).file_parser(
                    fileitem, job["localworkdir"], filelist, substitution)

            except AttributeError:

                if fileitem not in filelist:

                    filelist.append(fileitem)


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
