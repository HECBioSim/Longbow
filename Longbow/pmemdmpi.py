#!/usr/bin/env python

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

"""Contains the main entry point for the Longbow program, this version calls
the main for a console based session. This version is intended for proxying of
AMBER jobs, if the user wants to proxy using the names of popular biosim
executables (mdrun, pmemd etc) then they can call them using the appropriately
named .py file in the same directory as this file."""

import sys
from mains import console

if __name__ == "__main__":

    """Main entry point for the Longbow as a stand-alone application.

    The following files must be provided:

    -hosts
    -job
    -log

    User should specify either the absolute path to the file or if just the
    name is given then the current working directory will be used for job and
    log whilst the hosts file will fall back to the one inside the
    installation directory.

    To put the app in DEBUG mode supply -debug this will give enhanced logging
    to the console standard out and file as opposed to just file, be careful
    with issuing this as it could make your logfile significantly larger.

    To get the standard level of logging information to the console standard
    output use -verbose"""

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
    OVERRIDES = {
        "program": "Amber",
        "executable": "pmemd.MPI"
        }
    MODE = {
        "debug": False,
        "verbose": False
    }

    # ------------------------------------------------------------------------
    # Pull out some of the Longbow specific commandline args leaving behind
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

    # ------------------------------------------------------------------------
    # Call Longbow.

    # Enter the mains application.
    console(COMMANDLINEARGS, FILES, OVERRIDES, MODE)
