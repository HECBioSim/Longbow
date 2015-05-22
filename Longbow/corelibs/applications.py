# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of
# the HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the
# UK biomolecular simulation community on resources such as Archer.
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

"""The application module provides methods for testing whether the requested
application executable is present on the remote machine and for processing the
command line arguments of the job in a code specific manner."""

import logging
import os

try:
    import Longbow.corelibs.exceptions as ex
except ImportError:
    import corelibs.exceptions as ex

try:
    import Longbow.corelibs.shellwrappers as shellwrappers
except ImportError:
    import corelibs.shellwrappers as shellwrappers

try:
    import Longbow.plugins.apps as apps
except ImportError:
    import plugins.apps as apps


LOGGER = logging.getLogger("Longbow")


def testapp(hosts, jobs):

    """Test whether the application executable is reachable. This method
    does support testing for modules."""

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
                "Checking executable '%s' on '%s'", executable, resource)

            cmd = []
            if jobs[job]["modules"] is "":
                LOGGER.debug("Checking without modules.")

            else:
                LOGGER.debug("Checking with modules.")

                for module in jobs[job]["modules"].split(","):
                    module.replace(" ", "")
                    cmd.extend(["module load " + module + "\n"])

            cmd.extend(["which " + executable])

            try:
                shellwrappers.sendtossh(hosts[resource], cmd)
                LOGGER.info("Executable check - passed.")

            except ex.SSHError:
                LOGGER.error("Executable check - failed.")
                raise


def processjobs(jobs):

    """Process the jobs command line, this method will extract information
    from the command line and construct a list of files to be staged."""

    LOGGER.info("Processing job/s and detecting files that require upload.")

    # Get dictionary of executables and their required flags from plug-ins.
    tmp = getattr(apps, "DEFMODULES")

    # Process each job.
    for job in jobs:

        # Initialise some basic parameters.
        executable = jobs[job]["executable"]
        app = tmp[executable]

        # Process the command line into a list.
        args = jobs[job]["commandline"].split()

        LOGGER.debug("Commandline arguments for job '%s': %s", job, args)

        # Check for any files that are located outside the work directory or
        # absolute paths.
        for item in args:

            if item.count(os.path.pardir) > 0 or os.path.isabs(item):

                raise ex.RequiredinputError(
                    "In job %s input files are being provided with absolute "
                    "paths or from directories above localworkdir. This is "
                    "not supported" % job)

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
            raise ex.DirectorynotfoundError(
                "The local job directory '%s' " % cwd + "cannot be found for "
                "job '%s'" % job)

        # Detect command line substitutions
        substte = {}

        try:
            substte = getattr(apps, app.lower()).sub_dict(args)

        except AttributeError:
            pass

        # Process the command line arguments, detecting any missing flags,
        # files or dependencies within the files.

        # Get required flags.
        req_flags = getattr(apps, "EXECFLAGS")[executable]
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
                    for i in range(1, jobs[job]["replicates"] + 1):

                        filepath = ""

                        # If we do only have a single job then file path should
                        # be
                        if jobs[job]["replicates"] == 1:

                            # For this type of job the file should be at [1].
                            filepath = os.path.join(cwd, args[1])

                        # Otherwise we have a replicate job so we should amend
                        # the paths.
                        else:

                            # We should check that the replicate directory
                            # structure exists.
                            if os.path.isdir(os.path.join(
                                    cwd, "rep" + str(i))) is False:

                                raise ex.RequiredinputError(
                                    "In job '%s' a replicate style job has "
                                    "been detected, but the directory '%s' "
                                    "cannot be found" %
                                    (job, os.path.join(cwd, "rep" + str(i))))

                            # If we have a replicate job then we should check
                            # if the file resides within ./rep{i} or if it is
                            # a global (common to each replicate) file.
                            if os.path.isfile(
                                    os.path.join(
                                        cwd, "rep" + str(i), args[1])):

                                # Set the file path
                                filepath = os.path.join(
                                    cwd, "rep" + str(i), args[1])

                            # Otherwise do we have a file here.
                            elif os.path.isfile(os.path.join(cwd, args[1])):

                                # If we do then set file path.
                                filepath = os.path.join(cwd, args[1])

                                # Also update the command line to reflect a
                                # global file.
                                args[args[1]] = os.path.join("../", args[1])

                        # If the next argument along is a valid file.
                        if os.path.isfile(filepath):

                            # Then mark the flag as found.
                            found_flags.append("?")

                            # FAO Gareth
                            # Search input file for any file dependencies that
                            # don't exist.
                            # try:
                            #    getattr(apps, app.lower()).file_parser(
                            #        filepath, cwd, substte)

                            # except AttributeError:
                            #     pass

                            # Maybe modify the file parser to return the
                            # ex.RequiredinputError if a file is referenced but
                            # not found. Then we can do something like this as
                            # long as the error message is raised in the parser
                            # except ex.RequiredinputError:
                            #     raise

                        # If it is not valid then raise an exception.
                        else:

                            raise ex.RequiredinputError(
                                "In job '%s' it appears that the input file "
                                "is missing, check your command line is of "
                                "the form: "
                                "longbow <longbow args> app '<' <app args>" %
                                job)

                # Looks like the command line is too short to contain the
                # input file so raise an exception.
                else:

                    raise ex.RequiredinputError(
                        "In job '%s' it appears that the input file is missing"
                        ", check your command line is of the form "
                        "longbow <longbow args> app '<' <app args>" % job)

            # Some programs are run with the format "executable input.file"
            elif args[0] is not "<":

                # Lets make sure that we actually have something to load.
                if len(args) > 0:

                    # If 'replicates' == 1 then we will only check one file,
                    # else we will proceed to check files in all replicates.
                    for i in range(1, jobs[job]["replicates"] + 1):

                        filepath = ""

                        # If we do only have a single job then file path should
                        # be
                        if jobs[job]["replicates"] == 1:

                            # For this type of job the file should be at [0].
                            filepath = os.path.join(cwd, args[0])

                        # Otherwise we have a replicate job so we should amend
                        # the paths.
                        else:

                            # We should check that the replicate directory
                            # structure exists.
                            if os.path.isdir(os.path.join(
                                    cwd, "rep" + str(i))) is False:

                                raise ex.RequiredinputError(
                                    "In job '%s' a replicate style job has "
                                    "been detected, but the directory '%s' "
                                    "cannot be found" %
                                    (job, os.path.join(cwd, "rep" + str(i))))

                            # If we have a replicate job then we should check
                            # if the file resides within ./rep{i} or if it is
                            # a global (common to each replicate) file.
                            if os.path.isfile(
                                    os.path.join(
                                        cwd, "rep" + str(i), args[0])):

                                # Set the file path
                                filepath = os.path.join(
                                    cwd, "rep" + str(i), args[0])

                            # Otherwise do we have a file here.
                            elif os.path.isfile(os.path.join(cwd, args[0])):

                                # If we do then set file path.
                                filepath = os.path.join(cwd, args[0])

                                # Also update the command line to reflect a
                                # global file.
                                args[args[0]] = os.path.join("../", args[0])

                        # If we have something to load then check that it is a
                        # valid file
                        if os.path.isfile(filepath):

                            # Then mark the flag as found.
                            found_flags.append("?")

                            # FAO Gareth
                            # Search input file for any file dependencies that
                            # don't exist.
                            # try:
                            #    getattr(apps, app.lower()).file_parser(
                            #        filepath, cwd, substte)

                            # except AttributeError:
                            #     pass

                            # Maybe modify the file parser to return the
                            # ex.RequiredinputError if a file is referenced
                            # but not found. Then we can do something like this
                            # as long as the error message is raised in the
                            # parser.
                            # except ex.RequiredinputError:
                            #     raise

                        # If we can't detect a file then something is wrong.
                        else:
                            raise ex.RequiredinputError(
                                "In job '%s' it appears that the input file "
                                "is missing, check your command line is of "
                                "the form: "
                                "longbow <longbow args> app <input file>" %
                                job)

                else:

                    raise ex.RequiredinputError(
                        "In job '%s' it appears that the input file is missing"
                        ", check your command line is of the form "
                        "longbow <longbow args> app <input file>" % job)

        # Otherwise we have a more conventional command line of the form:
        # exec -a arg1 -b arg2 --foo bar
        else:

            # Run through each one.
            for index, item in enumerate(args):

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
                            tmp = flag.split(" || ")

                            # Now check if flag is present
                            if item in tmp:

                                # Mark it as found if it hasn't been already.
                                if flag not in found_flags:
                                    found_flags.append(flag)

                # Otherwise it could just be a file or a parameter.
                else:

                    # If 'replicates' == 1 then we will only check one file,
                    # else we will proceed to check files in all replicates.
                    for i in range(1, jobs[job]["replicates"] + 1):

                        filepath = ""

                        # If we do only have a single job then file path should
                        # be
                        if jobs[job]["replicates"] == 1:

                            filepath = os.path.join(cwd, item)

                        # Otherwise we have a replicate job so we should amend
                        # the paths.
                        else:

                            # We should check that the replicate directory
                            # structure exists.
                            if os.path.isdir(os.path.join(
                                    cwd, "rep" + str(i))) is False:

                                raise ex.RequiredinputError(
                                    "In job '%s' a replicate style job has "
                                    "been detected, but the directory '%s' "
                                    "cannot be found" %
                                    (job, os.path.join(cwd, "rep" + str(i))))

                            # If we have a replicate job then we should check
                            # if the file resides within ./rep{i} or if it is
                            # a global (common to each replicate) file.
                            if os.path.isfile(
                                    os.path.join(cwd, "rep" + str(i), item)):

                                # Set the file path
                                filepath = os.path.join(
                                    cwd, "rep" + str(i), item)

                            # Otherwise do we have a file here.
                            elif os.path.isfile(os.path.join(cwd, item)):

                                # If we do then set file path.
                                filepath = os.path.join(cwd, item)

                                # Also update the command line to reflect a
                                # global file.
                                args[index] = os.path.join("../", item)

                        # If we have a file then run the parser on it to check
                        # for dependencies.
                        if os.path.isfile(filepath):

                            # Replace this with the dependancy check
                            pass

                            # FAO Gareth
                            # Search input file for any file dependencies that
                            # don't exist.
                            # try:
                            #    getattr(apps, app.lower()).file_parser(
                            #        filepath, cwd, substte)

                            # except AttributeError:
                            #     pass

                            # Maybe modify the file parser to return the
                            # ex.RequiredinputError if a file is referenced
                            # but not found. Then we can do something like this
                            # as long as the error message is raised in the
                            # parser.
                            # except ex.RequiredinputError:
                            #     raise

            # Final check for if any required flags are missing.
            flags = list(set(req_flags) - set(found_flags))

            # If there are any missing still then tell the user.
            if len(flags) is not 0:

                raise ex.RequiredinputError(
                    "In job '%s' there are missing flags on the command line "
                    "'%s'. See user documentation for plug-in '%s' " %
                    (job, flags, getattr(apps, "DEFMODULES")[executable]))

        # Replace the input command line with the execution command line.
        jobs[job]["commandline"] = executable + " " + " ".join(args)

        LOGGER.info("For job '%s' - execution string: %s", job, args)

    LOGGER.info("Processing jobs - complete.")
