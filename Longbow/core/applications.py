"""The application module provides methods for testing whether the requested
application executable is present on the remote machine and for processing the
command line arguments of the job in a code specific manner."""

import logging
import os
import core.shellwrappers as shellwrappers

LOGGER = logging.getLogger("Longbow")

def testapp(hosts, jobs):

    """Test whether the application executable is reachable. This method
    does support testing for modules."""

    LOGGER.info("Testing the executables defined for each job.")

    for job in jobs:

        LOGGER.info("  Checking executable '%s' on '%s'",
                    jobs[job]["executable"], jobs[job]["resource"])

        cmd = []
        if jobs[job]["modules"] is "":

            LOGGER.debug("  Checking without modules.")
        else:

            LOGGER.debug("  Checking with modules.")

            for module in jobs[job]["modules"].split(","):

                module.replace(" ", "")
                cmd.extend(["module load " + module])

        cmd.extend(["which " + jobs[job]["executable"] + " &> /dev/null"])

        try:

            shellwrappers.sendtossh(hosts[jobs[job]["resource"]], cmd)
            LOGGER.info("  Executable check - passed.")

        except Exception:

            raise RuntimeError("Executable check - failed")


def processjobs(args, jobs):

    """Process the jobs command line, this method will extract information
    from the command line and construct a list of files to be staged."""

    LOGGER.info("Processing job/s and detecting files that require " +
                "upload.")

    required = {"amber": ["-c", "-i", "-p"],
                "charmm": ["-i"],
                "gromacs": ["-s"],
                "lammps": ["-i"],
                "namd": ["<"]
                }

    for job in jobs:

        # Some initialisation.
        filelist = []
        flags = []
        executable = jobs[job]["executable"]

        # If the commandline was specified in the job configuration file
        # then process it into a list. This should be the case for
        # multijobs.
        if jobs[job]["commandline"] is not "":

            args = jobs[job]["commandline"].split()

        # Otherwise check if it came in on the command line to the main
        # app, this should be the case for single and single batch jobs.
        elif len(args) is 0:

            raise RuntimeError("Commandline arguments were not provided.")

        LOGGER.debug("  Args for job '%s': %s", job, args)

        # Now we should check that the required flags have been supplied if
        # the program being used is one of the ones we are supporting.
        if jobs[job]["program"] is not "":

            # Find missing flags.
            flags = list(set(required[jobs[job]["program"].lower()]) -
                         set(args))

            # Check for missing flags.
            if len(flags) is not 0:

                raise RuntimeError("in job '%s' " % job + "there are " +
                                   "missing flags from command line: %s " %
                                   flags + "see documentation for %s " %
                                   jobs[job]["program"])

        # Path correction for multijobs.
        cwd = jobs[job]["localworkdir"]

        if len(jobs) > 1:

            # Add the job name to the path.
            cwd = os.path.join(cwd, job)
            jobs[job]["localworkdir"] = cwd

        # Check that the directory exists.
        if os.path.isdir(cwd) is False:

            raise RuntimeError("The working directory '%s' cannot be " %
                               cwd + "found for job %s" % job)

        # Run through the commandline and search the working directory for
        # any matches, any that are found we will assume they need staging.
        for index, item in enumerate(args):

            filepath = os.path.join(cwd, item)

            # Check it is there.
            if os.path.isfile(filepath) is True:

                # Add it to the list.
                filelist.append(item)

                # If we have a batch job then fix for overrides.
                if int(jobs[job]["batch"]) > 1:
                    args[index] = os.path.join("../", item)

            # If we have no file and batch mode is used then we should
            # have some dirs to look in.
            elif int(jobs[job]["batch"]) > 1:

                # Else we just process all the files as normal.
                for i in range(1, int(jobs[job]["batch"])+1):

                    filepath = os.path.join(cwd, "rep" + str(i), item)

                    if os.path.isfile(filepath) is True:

                        # Add file to list of files required to upload.
                        filelist.append(os.path.join("rep" + str(i), item))

        # Concatenate executable and args back into a string.
        args = executable + " " + " ".join(args)

        # Add the filelist to the job configuration.
        jobs[job]["filelist"] = filelist

        # Replace the input commandline with the execution commandline.
        jobs[job]["commandline"] = args

        # Log results.
        LOGGER.info("  For job '%s' - files for upload: " % job +
                    ", ".join(filelist))
        LOGGER.info("  For job '%s' - execution string: %s",
                    job, args)

    LOGGER.info("  Processing jobs - complete.")
