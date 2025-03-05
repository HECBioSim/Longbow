# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council and
# The University of Nottingham
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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

import longbow.exceptions as exceptions
import longbow.shellwrappers as shellwrappers
import longbow.apps as apps


LOG = logging.getLogger("longbow.applications")


def checkapp(jobs):
    """Test that executables and their modules are launchable.

    This method will make an attempt to check that the application executable
    required to run a job or many jobs is present on the specified host. This
    method is capable of using the module system using some pre-configured
    either using user specified modules supplied in configuration files, or by
    using internal defaults. Users of codes that we are not supporting out of
    the box, will either have to specify the modules explicitly within
    configuration files.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    checked = {}

    LOG.info("Testing the executables defined for each job.")

    for job in [a for a in jobs if "lbowconf" not in a]:

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

            if jobs[job]["modules"] == "":

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

                raise exceptions.ExecutableError("Executable check - failed.")


def processjobs(jobs):
    """Process the application portion of the command-line.

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
    for job in [a for a in jobs if "lbowconf" not in a]:

        filelist = []
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
        if len([a for a in jobs if "lbowconf" not in a]) > 1:

            # Add the job name to the path.
            jobs[job]["localworkdir"] = os.path.join(
                jobs[job]["localworkdir"], job)

        # Check that the directory exists.
        if os.path.isdir(jobs[job]["localworkdir"]) is False:

            # If not, this is bad.
            raise exceptions.DirectorynotfoundError(
                "The local job directory '{0}' cannot be found for job '{1}'"
                .format(jobs[job]["localworkdir"], job))

        # Here we want to support generic executable launching. To do this
        # we will switch off all checking and testing and simply upload all
        # files in the job directory.
        try:

            appplugins = getattr(apps, "PLUGINEXECS")
            app = appplugins[os.path.basename(jobs[job]["executable"])]

        except KeyError:

            LOG.info("The software you are using is unsupported by a plugin. "
                     "Longbow will attempt to submit, but will assume you are"
                     "supplying modules manually or have used a absolute path"
                     "to your executable. If you think this is in error, "
                     "please open a ticket on github.")

            jobs[job]["upload-include"] = ""
            jobs[job]["upload-exclude"] = "*.log"

            # Replace the input command line with the execution command line.
            jobs[job]["executableargs"] = (
                jobs[job]["executable"] + " " +
                " ".join(jobs[job]["executableargs"]))

            LOG.info("For job '%s' - execution string: %s",
                     job, jobs[job]["executableargs"])

            LOG.info("Processing jobs - complete.")

            return

        # Hook to determine command-line parameter substitutions.
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

        # Some programs are too complex to do file detection, such as
        # chemshell.
        try:

            substitution = getattr(apps,
                                   app.lower()).rsyncuploadhook(jobs, job)

        except AttributeError:

            # Setup the rysnc upload masks.
            if jobs[job]["upload-include"] != "":

                jobs[job]["upload-include"] = (
                    jobs[job]["upload-include"] + ", ")

            jobs[job]["upload-include"] = (
                jobs[job]["upload-include"] + ", ".join(filelist))

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
    executable = os.path.basename(job["executable"])
    app = appplugins[executable]
    execdata = getattr(apps, app.lower()).EXECDATA[executable]

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
            "In job '{0}' the following arguments '{1}' to the application "
            "'{2}' are either missing or they require an input file to be "
            "specified, which has been found to be missing. Please check your "
            "command-line and filenames.".format(job["jobname"], flags, app))


def _markfoundfiles(arg, initargs, foundflags):
    """Mark file flags as found."""
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

    # Other cases should pretty much be formats like:
    # exec -flag file -flag file -flag file
    elif (len(initargs) > 1 and initargs[pos][0] == "-"
          and initargs[pos] not in foundflags):

        foundflags.append(initargs[pos])

    # Or cases like exec -flag file -flag file inputfile > outputfile
    elif (len(initargs) > 1 and initargs[pos][0] != "-"
          and initargs[pos] not in foundflags):

        foundflags.append("<")

    return foundflags


def _proccommandline(job, filelist, foundflags, substitution):
    """Command-line processor.

    This method selects which type of command-line we have.

    """
    # Initialisation.
    appplugins = getattr(apps, "PLUGINEXECS")
    executable = os.path.basename(job["executable"])
    app = appplugins[executable]
    args = list(job["executableargs"])
    subexe = getattr(apps, app.lower()).EXECDATA[executable]["subexecutables"]

    try:

        for arg in args:

            if (arg != "<" and arg != ">" and arg[0] != "-" and
                    arg[0] != "+" and arg not in subexe):

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
    executable = os.path.basename(job["executable"])
    app = appplugins[executable]
    initargs = list(job["executableargs"])

    # Check for as many files as there are replicates (default of 1).
    for rep in range(1, int(job["replicates"]) + 1):

        fileitem = ""

        # If we do only have a single job then file path should be.
        if int(job["replicates"]) == 1:

            fileitem = _procfilessinglejob(app, arg, job["localworkdir"])

        # Otherwise we have a replicate job so check these.
        else:

            repx = str(job["replicate-naming"]) + str(rep)

            # Add the repx dir
            if (repx) not in filelist:

                filelist.append(repx)

            fileitem = _procfilesreplicatejobs(
                app, arg, job["localworkdir"], initargs, repx)

            job["executableargs"] = initargs

        # If we have a valid file
        if os.path.isfile(os.path.join(job["localworkdir"], fileitem)):

            _markfoundfiles(arg, initargs, foundflags)

            # Hook to search input file for any file dependencies.
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


def _procfilesreplicatejobs(app, arg, cwd, initargs, repx):
    """Processor for replicate jobs."""
    fileitem = ""
    tmpitem = ""

    # We should check that the replicate directory structure exists.
    if os.path.isdir(os.path.join(cwd, repx)) is False:

        os.mkdir(os.path.join(cwd, repx))

    # If we have a replicate job then we should check if the file resides
    # within ./rep{i} or if it is a global (common to each replicate) file.
    if os.path.isfile(os.path.join(cwd, repx, arg)):

        fileitem = os.path.join(repx, arg)

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
                cwd, os.path.join(repx, arg), "")

        except AttributeError:

            pass

        # If we have a positive check then file found in rep$i directories.
        if tmpitem != "":

            fileitem = tmpitem

        # Otherwise check for global one.
        else:

            try:

                fileitem, initargs = getattr(
                    apps, app.lower()).defaultfilename(cwd, arg, initargs)

            except AttributeError:

                pass

    return fileitem
