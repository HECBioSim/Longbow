# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of Longbow.
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

"""This module contains the methods that act as the main entry point for the
different modes of Longbow, the main entry types are console and GUI based."""

import os
import sys
import logging
import corelibs


def console(args, files, overrides, mode):

    """This is the main for a console based app, this is designed to run in a
    python/unix shell and is thus the main choice for headless machines like a
    local cluster or for users that don't require a GUI."""

    # Get current directory (where we are run from).
    cwd = os.getcwd()

    # Get the execution directory (where we are installed).
    execdir = os.path.dirname(os.path.realpath(__file__))


    # -----------------------------------------------------------------
    # Setup some basic file paths.

    # Check if a file name/path is supplied. If just the name is supplied
    # then for logs output to the current working directory. For hosts 
    # and jobs prioritise the named files in the current working directory 
    # over those in the execution directory if they exist.
    try:
        for param in files:
            if files[param] is "":
                raise RuntimeError("Error: nothing was supplied for the " +
                                   "%s file, please supply " %
                                   param + "its name with the -%s " %
                                   param + "flag.")
            else:
                if os.path.isabs(files[param]) is False:
                    if param == "hosts" or param == "jobs":
                        if os.path.isfile(cwd + "/" + files[param]):
                            paths = cwd
                        elif os.path.isfile(execdir + "/" + files[param]):
                            paths = execdir
                    elif param == "logs":
                        paths = cwd
                    files[param] = os.path.join(paths, files[param])

    except RuntimeError as ex:
        sys.exit(ex)

    # -----------------------------------------------------------------
    # Setup the logger.

    corelibs.setuplogger(files["logs"], "Longbow", mode)

    logger = logging.getLogger("Longbow")

    # Log that we are starting up.
    logger.info("Longbow - initialisation complete.")

    # -----------------------------------------------------------------
    # setup and run some tests.

    try:

        # Load the configuration of the hosts.
        hosts = corelibs.loadhosts(files["hosts"])

        # Load the configuration of the jobs.
        jobs = corelibs.loadjobs(cwd, files["jobs"], overrides)

        # Test the connection/s specified in the job configurations
        corelibs.testconnections(hosts, jobs)

        # Test the hosts listed in the jobs configuration file have their
        # scheduler environments listed, if not then test and save them.
        corelibs.testenv(files["hosts"], hosts, jobs)

        # Test that for the applications listed in the job configuration
        # file are available and that the executable is present.
        corelibs.testapp(hosts, jobs)

        # -----------------------------------------------------------------
        # Start processing the setup and staging for each job.

        # Process the jobs command line arguments and find files for
        # staging.
        corelibs.processjobs(args, jobs)

        # Create jobfile and add it to the list of files that needs
        # uploading.
        corelibs.prepare(hosts, jobs)

        # Stage all of the job files along with the scheduling script.
        corelibs.stage_upstream(hosts, jobs)

        # -----------------------------------------------------------------
        # Submit the job/s to the scheduler.
        corelibs.submit(hosts, jobs)

        # -----------------------------------------------------------------
        # Monitor job/s.
        corelibs.monitor(hosts, jobs)

        # -----------------------------------------------------------------
        # Clean up.

        # Remove the remote directory.
        corelibs.cleanup(hosts, jobs)

    except RuntimeError as ex:
        if mode["debug"]:
            logger.exception(ex)
        else:
            logger.error(ex)

    logger.info("Closing Longbow.")

    # -----------------------------------------------------------------


def gui():

    """This method forms the entry point to utilise the GUI, this main function
    is designed primarily for users that want a desktop GUI."""

    pass
