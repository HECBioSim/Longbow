#!/usr/bin/env python

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
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Longbow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""Contains the main entry point for the Longbow program, this version calls
the main for a console based session."""

import os
import sys
import logging
import corelibs.applications as applications
import corelibs.configuration as configuration
import corelibs.exceptions as ex
import corelibs.logger as log
import corelibs.scheduling as scheduling
import corelibs.shellwrappers as shellwrappers
import corelibs.staging as staging


def main(args, files, mode, machine):

    """This is the main for a console based app, this is designed to run in a
    python/unix shell and is thus the main choice for headless machines like a
    local cluster or for users that don't require a GUI."""

    # -------------------------------------------------------------------------
    # Determine some basic information

    # Get current directory (where we are run from).
    cwd = os.getcwd()

    # Get the execution directory (where we are installed).
    execdir = os.path.dirname(os.path.realpath(__file__))

    # Test whether the executable has been provided on the command line
    try:
        if args[0] in ("charmm", "pmemd", "pmemd.MPI", "mdrun", "lmp_xc30",
                       "namd2"):
            executable = args[0]
            args.pop(0)

    except IndexError:
        executable = ""

    # Convert command line arguments into a space separated string
    args = " ".join(args)

    # -------------------------------------------------------------------------
    # Setup some basic file paths.

    try:
        # log
        # if a filename hasn't been provided default to log
        if files["log"] is "":
            files["log"] = "log"

        # if the path hasn't been provided default to the current working
        # directory
        if os.path.isabs(files["log"]) is False:
            files["log"] = os.path.join(cwd, files["log"])

        # ---------------------------------------------------------------------
        # Setup the logger.

        log.setuplogger(files["log"], "Longbow", mode)

        logger = logging.getLogger("Longbow")

        # ---------------------------------------------------------------------

        # hosts
        # if a filename hasn't been provided default to hosts.conf
        if files["hosts"] is "":
            files["hosts"] = "hosts.conf"
        # if the path hasn't been provided look in the current working
        # directory and then the execution directory if needs be
        if os.path.isabs(files["hosts"]) is False:
            if os.path.isfile(os.path.join(cwd, files["hosts"])):
                files["hosts"] = os.path.join(cwd, files["hosts"])

            elif os.path.isfile(os.path.join(execdir, files["hosts"])):
                files["hosts"] = os.path.join(execdir, files["hosts"])

            else:
                raise ex.RequiredinputError("No host configuration file "
                    "found in the current working directory %s or in the"
                    "execution directory %s." % (cwd, execdir))

        # job
        # if a job configuration file has been supplied but the path hasn't
        # look in the current working directory and then the execution
        # directory if needs be
        if files["job"] is not "" and os.path.isabs(files["job"]) is False:
            if os.path.isfile(os.path.join(cwd, files["job"])):
                files["job"] = os.path.join(cwd, files["job"])

            elif os.path.isfile(os.path.join(execdir, files["job"])):
                files["job"] = os.path.join(execdir, files["job"])

            else:
                raise ex.RequiredinputError("The job configuration file %s "
                    "couldn't be found in the current working directory %s "
                    "or in the execution directory %s."
                    % (files["job"], cwd, execdir))

    # -------------------------------------------------------------------------
    # setup and run some tests.

        # Log that we are starting up.
        logger.info("Welcome to Longbow!")
        logger.info("This software was developed as part of the EPSRC-funded"
                    " HECBioSim project (http://www.hecbiosim.ac.uk/)")
        logger.info("HECBioSim facilitates high-end biomolecular simulation "
                    "on resources such as Archer")
        logger.info("Longbow is Copyright (C) of James T Gebbie-Rayet and "
                    "Gareth B Shannon 2015.")
        logger.info("Initialisation complete.")

        logger.info("hosts file is: %s", files["hosts"])

        # Load the configuration of the hosts.
        hosts = configuration.loadhosts(files["hosts"])

        # Load the configuration of the jobs
        jobs = configuration.loadjobs(files["job"], files["hosts"], machine)

        # Sort and prioritise configuration parameters
        configuration.sortconfigs(hosts, jobs, executable, cwd, args)

        # Test the connection/s specified in the job configurations
        shellwrappers.testconnections(hosts, jobs)

        # Test the hosts listed in the jobs configuration file have their
        # scheduler environments listed, if not then test and save them.
        scheduling.testenv(files["hosts"], hosts, jobs)

        # Test that for the applications listed in the job configuration
        # file are available and that the executable is present.
        applications.testapp(hosts, jobs)

        # ---------------------------------------------------------------------
        # Start processing the setup and staging for each job.

        # Process the jobs command line arguments and find files for
        # staging.
        applications.processjobs(jobs)

        # Create jobfile and add it to the list of files that needs
        # uploading.
        scheduling.prepare(hosts, jobs)

        # Stage all of the job files along with the scheduling script.
        staging.stage_upstream(hosts, jobs)

        # ---------------------------------------------------------------------
        # Submit the job/s to the scheduler.
        scheduling.submit(hosts, jobs)

        # ---------------------------------------------------------------------
        # Monitor job/s.
        scheduling.monitor(hosts, jobs)

    # -------------------------------------------------------------------------
    # Handle the errors and Longbow exit.

    except (ex.RsyncError, ex.SCPError, ex.SSHError) as err:

        # Output the information about the problem.
        if mode["debug"]:
            logger.exception(err)
        else:
            logger.error(err)

        logger.error("stdout: %s", str(err.stdout))
        logger.error("stderr: %s", str(err.stderr))
        logger.error("errorcode: %s", str(err.errorcode))

    except (SystemExit, KeyboardInterrupt):

        logger.info("User interrupt - performing cleanup.")

        # User has decided to kill Longbow, check if there are any jobs still
        # running.
        for job in jobs:
            if "jobid" in jobs[job]:
                # If job is not finished delete and stage.
                if jobs[job]["laststatus"] != "Finished" and \
                   jobs[job]["laststatus"] != "Submit Error":

                    # Kill it.
                    scheduling.delete(hosts, jobs, job)

                    # Transfer the directories as they are.
                    staging.stage_downstream(hosts, jobs, job)
                # Job is finished then just stage.
                elif jobs[job]["laststatus"] != "Submit Error":
                    # Transfer the directories as they are.
                    staging.stage_downstream(hosts, jobs, job)

    except ex.RequiredinputError as err:
        logger.error(err)

    except Exception as err:
        if mode["debug"]:
            logger.exception(err)
        else:
            logger.error(err)

    finally:
        # Cleanup.
        staging.cleanup(hosts, jobs)

        logger.info("Good bye from Longbow!")
        logger.info("Check out http://www.hecbiosim.ac.uk/ for other " +
                    "powerful biomolecular simulation software tools.")

    # -------------------------------------------------------------------------


if __name__ == "__main__":

    """Main entry point for Longbow.

    To run Longbow, simply write longbow.py before the command you wish to
    be executed using your chosen simulation package e.g.:

    %longbow.py pmemd.MPI -i test.in -c test.min -p test.top -o output

    In addition, the following flags may be provided:

    -hosts filename
    -job filename
    -log filename
    -machine resource
    -debug
    -verbose

    Read the documentation at http://www.hecbiosim.ac.uk/ for more information
    on how to setup and run jobs using Longbow.
     """

    # ------------------------------------------------------------------------
    # Some defaults.

    # Fetch command line arguments
    COMMANDLINEARGS = sys.argv

    # Remove the first argument (the application path)
    COMMANDLINEARGS.pop(0)

    # Initialise file path params, so we can pass blank to signify use default
    # paths if not supplied.
    FILES = {
        "hosts": "",
        "job": "",
        "log": ""
    }
    MACHINE = ""
    MODE = {
        "debug": False,
        "verbose": False
    }

    # ------------------------------------------------------------------------
    # Pull out some of the specific commandline args leaving behind
    # the target app args.

    # Take out the config file path, then remove it from the command
    # line argument list.
    if COMMANDLINEARGS.count("-hosts") == 1:
        POSITION = COMMANDLINEARGS.index("-hosts")
        FILES["hosts"] = COMMANDLINEARGS[POSITION + 1]
        COMMANDLINEARGS.pop(POSITION)
        COMMANDLINEARGS.pop(POSITION)

    # Take out the job config file path, then remove it from the command
    # line argument list.
    if COMMANDLINEARGS.count("-job") == 1:
        POSITION = COMMANDLINEARGS.index("-job")
        FILES["job"] = COMMANDLINEARGS[POSITION + 1]
        COMMANDLINEARGS.pop(POSITION)
        COMMANDLINEARGS.pop(POSITION)

    # Take out the log file path, then remove it from the command
    # line argument list.
    if COMMANDLINEARGS.count("-log") == 1:
        POSITION = COMMANDLINEARGS.index("-log")
        FILES["log"] = COMMANDLINEARGS[POSITION + 1]
        COMMANDLINEARGS.pop(POSITION)
        COMMANDLINEARGS.pop(POSITION)

    # Take out the DEBUG parameter, then remove it from the command line list.
    if COMMANDLINEARGS.count("-debug") == 1:
        POSITION = COMMANDLINEARGS.index("-debug")
        COMMANDLINEARGS.pop(POSITION)
        MODE["debug"] = True

    # Take out the DEBUG parameter, then remove it from the command line list.
    if COMMANDLINEARGS.count("-verbose") == 1:
        POSITION = COMMANDLINEARGS.index("-verbose")
        COMMANDLINEARGS.pop(POSITION)
        MODE["verbose"] = True

    # Take out the machine name, then remove it from the command
    # line argument list.
    if COMMANDLINEARGS.count("-machine") == 1:
        POSITION = COMMANDLINEARGS.index("-machine")
        MACHINE = COMMANDLINEARGS[POSITION + 1]
        COMMANDLINEARGS.pop(POSITION)
        COMMANDLINEARGS.pop(POSITION)

    # ------------------------------------------------------------------------
    # Call Longbow.

    # Enter the mains application.
    main(COMMANDLINEARGS, FILES, MODE, MACHINE)
