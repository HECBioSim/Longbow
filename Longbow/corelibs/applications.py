# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of
# the HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the
# UK biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Longbow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""
The applications module contains methods for processing the aspect of jobs
which relate to external applications (such as an MD package). The following
methods can be found within this module:

testapp()
    This method will make an attempt to check that the application executables
    required to run a job/s is present on the specified host/s. This method is
    capable of using the module system.

processjobs()
    This method will process information that is given as an intended target to
    be passed on to the executable at run time. It will check that required
    parameters (provided the respective plug-in is configured correctly) have
    been supplied, and that all files and their dependencies (again provided
    that the respective plug-in is configured for this) exist on disk.
"""

import logging
import os
from random import randint

# Depending on how longbow is installed/utilised the import will be slightly
# different, this should handle both cases.
try:

    EX = __import__("corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("corelibs.shellwrappers", fromlist=[''])
    APPS = __import__("plugins.apps", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("Longbow.corelibs.shellwrappers", fromlist=[''])
    APPS = __import__("Longbow.plugins.apps", fromlist=[''])

LOGGER = logging.getLogger("Longbow")


def testapp(hosts, jobs):

    """
    This method will make an attempt to check that the application executables
    required to run a job/s is present on the specified host/s. This method is
    capable of using the module system.

    Required arguments are:

    hosts (dictionary) - The Longbow hosts data structure, see configuration.py
                         for more information about the format of this
                         structure.

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    checked = {}

    LOGGER.info("Testing the executables defined for each job.")

    for job in jobs:

        resource = jobs[job]["resource"]
        executable = jobs[job]["executable"]

        # If we haven't checked this resource then it is likely not in the dict
        if resource not in checked:

            checked[resource] = []

        # Now check if we have tested this exec already.
        if executable not in checked[resource]:

            # If not then add it to the list now.
            checked[resource].extend([executable])

            LOGGER.info(
                "Checking executable '{0}' on '{1}'"
                .format(executable, resource))

            cmd = []

            if jobs[job]["modules"] is "":

                LOGGER.debug("Checking without modules.")

            else:
                LOGGER.debug("Checking with modules.")

                for module in jobs[job]["modules"].split(","):

                    module = module.replace(" ", "")
                    cmd.extend(["module load " + module + "\n"])

            cmd.extend(["which " + executable])

            try:

                SHELLWRAPPERS.sendtossh(hosts[resource], cmd)
                LOGGER.info("Executable check - passed.")

            except EX.SSHError:

                LOGGER.error("Executable check - failed.")
                raise


def processjobs(jobs):

    """
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

    LOGGER.info("Processing job/s and detecting files that require upload.")

    # Get dictionary of executables and their required flags from plug-ins.
    tmp = getattr(APPS, "DEFMODULES")

    # Process each job.
    for job in jobs:

        # Initialise some basic parameters.
        executable = jobs[job]["executable"]
        app = tmp[executable]
        args = jobs[job]["executableargs"]
        filelist = []

        # Append a hash to the job directory to avoid directory clashes.
        destdir = job + ''.join(["%s" % randint(0, 9) for _ in range(0, 5)])

        jobs[job]["destdir"] = os.path.join(jobs[job]["destdir"], destdir)

        LOGGER.debug("Job '{0}' will be run in the '{1}' directory on the "
                     "remote resource.".format(job, jobs[job]["destdir"]))

        LOGGER.debug("Command-line arguments for job '{0}'are '{1}'"
                     .format(job, args))

        # Check for any files that are located outside the work directory or
        # absolute paths.
        for item in args:

            if item.count(os.path.pardir) > 0 or os.path.isabs(item):

                raise EX.RequiredinputError(
                    "In job '{0}' input files are being provided with "
                    "absolute paths or from directories above localworkdir. "
                    "This is not supported".format(job))

        # Base path to local job directory.
        cwd = jobs[job]["localworkdir"]

        # If we have multiple jobs.
        if len(jobs) > 1:

            # Add the job name to the path.
            cwd = os.path.join(cwd, job)
            jobs[job]["localworkdir"] = cwd

        # Check that the directory exists.
        if os.path.isdir(cwd) is False:

            # If not, this is bad.
            raise EX.DirectorynotfoundError(
                "The local job directory '{0}' cannot be found for job '{1}'"
                .format(cwd, job))

        # Detect command line substitutions. Make a copy of the commandline
        # arguments as text enforcing substitutions will be removed for most
        # of the code
        initargs = list(args)
        substte = {}

        try:

            substte = getattr(APPS, app.lower()).sub_dict(args)

        except AttributeError:

            pass

        # Process the command line arguments, detecting any missing flags,
        # files or dependencies within the files.

        # Get required flags.
        req_flags = getattr(APPS, "EXECFLAGS")[executable]
        found_flags = []

        # Start with the case where the command line would be provided like
        # exec < input.file or exec input.file.
        if "?" in req_flags:

            # Check if the first item is the "<".
            if args[0] is "<":

                # Check the length of the command line.
                if len(args) > 1:

                    # If 'replicates' == 1 then we will only check one file,
                    # else we will proceed to check files in all replicates.
                    for i in range(1, int(jobs[job]["replicates"]) + 1):

                        # If we do only have a single job then file path should
                        # be
                        if int(jobs[job]["replicates"]) == 1:

                            # For this type of job the file should be at [1].
                            fileitem = args[1]

                        # Otherwise we have a replicate job so we should amend
                        # the paths.
                        else:

                            # We should check that the replicate directory
                            # structure exists. If it doesn't then create it.
                            if os.path.isdir(os.path.join(
                                    cwd, "rep" + str(i))) is False:

                                os.mkdir(os.path.join(cwd, "rep" + str(i)))

                            # Add the repX dir to the file list as rsync will
                            # not create them.
                            if ("rep" + str(i)) not in filelist:

                                filelist.append("rep" + str(i))

                            # If we have a replicate job then we should check
                            # if the file resides within ./rep{i} or if it is
                            # a global (common to each replicate) file.
                            if os.path.isfile(
                                    os.path.join(
                                        cwd, "rep" + str(i), args[1])):

                                fileitem = os.path.join("rep" + str(i),
                                                        args[1])

                            # Otherwise do we have a file in cwd
                            elif os.path.isfile(os.path.join(cwd, args[1])):

                                fileitem = args[1]

                                # Also update the command line to reflect a
                                # global file.
                                if args[1] in initargs:

                                    initargs[initargs.index(args[1])] = \
                                        os.path.join("../", args[1])

                        # If the next argument along is a valid file.
                        if os.path.isfile(os.path.join(cwd, fileitem)):

                            # Then mark the flag as found.
                            found_flags.append("?")

                            # Search input file for any file dependencies that
                            # don't exist.
                            try:

                                getattr(
                                    APPS, app.lower()).file_parser(
                                        fileitem, cwd, filelist, substte)

                            except AttributeError:

                                if fileitem not in filelist:
                                    filelist.append(fileitem)

                # Looks like the command line is too short to contain the
                # input file so raise an exception.
                else:

                    raise EX.RequiredinputError(
                        "In job '{0}' it appears that the input file is "
                        "missing, check your command line is of the form "
                        "longbow [longbow args] executable '<' "
                        "[executable args]".format(job))

            # Some programs are run with the format "executable input.file"
            elif args[0] is not "<":

                # Lets make sure that we actually have something to load.
                if len(args) > 0:

                    # If 'replicates' == 1 then we will only check one file,
                    # else we will proceed to check files in all replicates.
                    for i in range(1, int(jobs[job]["replicates"]) + 1):

                        # If we do only have a single job then file path should
                        # be
                        if int(jobs[job]["replicates"]) == 1:

                            # For this type of job the file should be at [0].
                            fileitem = args[0]

                        # Otherwise we have a replicate job so we should amend
                        # the paths.
                        else:

                            # We should check that the replicate directory
                            # structure exists.
                            if os.path.isdir(os.path.join(
                                    cwd, "rep" + str(i))) is False:

                                os.mkdir(os.path.join(cwd, "rep" + str(i)))

                            # Add the repX dir to the file list as rsync will
                            # not create them.
                            if ("rep" + str(i)) not in filelist:

                                filelist.append("rep" + str(i))

                            # If we have a replicate job then we should check
                            # if the file resides within ./rep{i} or if it is
                            # a global (common to each replicate) file.
                            if os.path.isfile(
                                    os.path.join(
                                        cwd, "rep" + str(i), args[0])):

                                fileitem = os.path.join("rep" + str(i),
                                                        args[0])

                            # Otherwise do we have a file in cwd
                            elif os.path.isfile(os.path.join(cwd, args[0])):

                                fileitem = args[0]

                                # Also update the command line to reflect a
                                # global file.
                                if args[0] in initargs:

                                    initargs[initargs.index(args[0])] = \
                                        os.path.join("../", args[0])

                        # If we have something to load then check that it is a
                        # valid file
                        if os.path.isfile(os.path.join(cwd, fileitem)):

                            # Then mark the flag as found.
                            found_flags.append("?")

                            # Search input file for any file dependencies that
                            # don't exist.
                            try:

                                getattr(
                                    APPS, app.lower()).file_parser(
                                        fileitem, cwd, filelist, substte)

                            except AttributeError:

                                if fileitem not in filelist:

                                    filelist.append(fileitem)

                # Looks like the command line is too short to contain the
                # input file so raise an exception.
                else:

                    raise EX.RequiredinputError(
                        "In job '{0}' it appears that the input file "
                        "is missing, check your command line is of "
                        "the form: "
                        "longbow [longbow args] executable '<' "
                        "[executable args]".format(job))

        # Otherwise we have a more conventional command line of the form:
        # exec -a arg1 -b arg2 --foo bar
        else:

            # Run through each one.
            for item in args:

                fileitem = ""

                # If we have a flag (starting with '-') and it is in the list
                # of required flags.
                if item[0] is "-" and item in req_flags:

                    # Mark the flag as found
                    found_flags.append(item)

                # If we have a flag that is not in the list of required flags.
                elif item[0] is "-" and item not in req_flags:

                    # Check then if this flag belongs to a case where it is
                    # either one or the other flag has to be provided (ie ones
                    # listed as -foo || bar) such as gromacs -s or -deffnm)
                    for flag in req_flags:

                        # If it is the special case
                        if "||" in flag:

                            # Split them into separate args.
                            flags = flag.split(" || ")

                            # Now check if flag is present
                            if item in flags:

                                # Mark it as found if it hasn't been already.
                                if flag not in found_flags:
                                    found_flags.append(flag)

                # Otherwise it could just be a file or a parameter.
                else:

                    # If 'replicates' == 1 then we will only check one file,
                    # else we will proceed to check files in all replicates.
                    for i in range(1, int(jobs[job]["replicates"]) + 1):

                        tmpitem = ""

                        # If we do only have a single job then file path should
                        # be
                        if int(jobs[job]["replicates"]) == 1:

                            if os.path.isfile(os.path.join(cwd, item)):

                                fileitem = item

                            # Hook for checking plugin specific file naming
                            # scenarios (eg. gromacs -deffnm test actually
                            # referring to test.tpr).
                            else:

                                try:

                                    fileitem = getattr(
                                        APPS, app.lower()).defaultfilename(
                                            cwd, item)

                                except AttributeError:

                                    pass

                        # Otherwise we have a replicate job so we should amend
                        # the paths.
                        else:

                            # We should check that the replicate directory
                            # structure exists.
                            if os.path.isdir(os.path.join(
                                    cwd, "rep" + str(i))) is False:

                                os.mkdir(os.path.join(cwd, "rep" + str(i)))

                            # Add the repX dir to the file list as rsync will
                            # not create them.
                            if ("rep" + str(i)) not in filelist:

                                filelist.append("rep" + str(i))

                            # If we have a replicate job then we should check
                            # if the file resides within ./rep{i} or if it is
                            # a global (common to each replicate) file.
                            if os.path.isfile(
                                    os.path.join(cwd, "rep" + str(i), item)):

                                # Set the file path
                                fileitem = os.path.join("rep" + str(i), item)

                            # Otherwise do we have a file here.
                            elif os.path.isfile(os.path.join(cwd, item)):

                                # If we do then set file path.
                                fileitem = item

                                # Also update the command line to reflect a
                                # global file.
                                if item in initargs:

                                    initargs[initargs.index(item)] = \
                                        os.path.join("../", item)

                            # Hook for checking plugin specific file naming
                            # scenarios (eg. gromacs -deffnm test actually
                            # referring to test.tpr).
                            else:

                                try:

                                    tmpitem = getattr(
                                        APPS, app.lower()).defaultfilename(
                                            cwd, os.path.join(
                                                "rep" + str(i) + item))

                                except AttributeError:

                                    pass

                                # If we have a positive check then file found
                                # in rep$i directories.
                                if tmpitem is not "":

                                    fileitem = tmpitem

                                # Otherwise check for global one.
                                else:

                                    try:

                                        fileitem = getattr(
                                            APPS, app.lower()).defaultfilename(
                                                cwd, item)

                                        # Also update the command line to
                                        # reflect a global file.
                                        if item in initargs:

                                            initargs[initargs.index(item)] = \
                                                os.path.join("../", item)

                                    except AttributeError:

                                        pass

                        # Check if there are any dependencies inside the file
                        # otherwise if this is not supported then just append
                        # for upload.
                        if os.path.isfile(os.path.join(cwd, fileitem)):

                            # Search input file for any file dependencies
                            # that don't exist.
                            try:

                                getattr(
                                    APPS, app.lower()).file_parser(
                                        fileitem, cwd, filelist, substte)

                            except AttributeError:

                                if fileitem not in filelist:

                                    filelist.append(fileitem)

            # Final check for if any required flags are missing.
            flags = list(set(req_flags) - set(found_flags))

            # If there are any missing still then tell the user.
            if len(flags) is not 0:

                raise EX.RequiredinputError(
                    "In job '{0}' there are missing flags on the command line "
                    "'{1}'. See user documentation for plug-in '{2}'".format(
                        job, flags, getattr(APPS, "DEFMODULES")[executable]))

        # Setup the rysnc upload masks.
        if jobs[job]["upload-include"] is "":

            jobs[job]["upload-include"] = (", ".join(filelist))

        else:

            jobs[job]["upload-include"] = (
                jobs[job]["upload-include"] + ", " + ", ".join(filelist))

        jobs[job]["upload-exclude"] = "*"

        # Replace the input command line with the execution command line.
        # initargs is a copy of the original args before text enforcing
        # substitutions was removed
        jobs[job]["executableargs"] = executable + " " + " ".join(initargs)

        LOGGER.info("For job '{0}' - execution string: {1}".format(
            job, jobs[job]["executableargs"]))

    LOGGER.info("Processing jobs - complete.")
