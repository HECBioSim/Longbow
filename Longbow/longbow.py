#!/usr/bin/env python

"""Contains the main entry point for the ProxyApp program, this version calls
the main for a console based session. This version is intended for generic
proxying of jobs, if the user wants to proxy using the names of popular biosim
executables (mdrun, pmemd etc) then they can call them using the appropriately
named .py file in the same directory as this file."""

import sys
from mains import console

if __name__ == "__main__":

    """Main entry point for the ProxyApp as a stand-alone application.

    The following files must be provided:

    -hosts
    -jobs
    -logs

    User should specify either the absolute path to the file or if just the
    name is given then the current working directory will be used for jobs and
    logs whilst the hosts file will fall back to the one inside the
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
        "jobs": "",
        "logs": ""
    }
    OVERRIDES = {}
    MODE = {
        "debug": False,
        "verbose": False
    }

    # ------------------------------------------------------------------------
    # Pull out some of the ProxyApp specific commandline args leaving behind
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
    if COMMANDLINEARGS.count("-jobs") == 1:
        POSITION = COMMANDLINEARGS.index("-jobs")
        FILES["jobs"] = COMMANDLINEARGS[POSITION + 1]
        COMMANDLINEARGS.pop(POSITION)
        COMMANDLINEARGS.pop(POSITION)

    # Take out the log file path, then remove it from the command
    # line argument list.
    if COMMANDLINEARGS.count("-logs") == 1:
        POSITION = COMMANDLINEARGS.index("-logs")
        FILES["logs"] = COMMANDLINEARGS[POSITION + 1]
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
    # Call ProxyApp.

    # Enter the mains application.
    console(COMMANDLINEARGS, FILES, OVERRIDES, MODE)
