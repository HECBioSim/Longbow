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

import sys
import corelibs.exceptions as ex
from mains import console

if __name__ == "__main__":

    """Main entry point for Longbow.

    To run Longbow, simply write longbow.py before the command you wish to be executed using
    your chosen simulation package e.g.:
    
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

    # Check an executable or job configuration file has been provided
    if COMMANDLINEARGS[0] not in ("charmm", "pmemd", "pmemd.MPI", "mdrun" +
       "lmp_xc30", "namd2") and COMMANDLINEARGS.count("-job") == 0:
        raise ex.CommandlineargsError("A recognised executable or job " +
            "configuration file must be specified on the command line")

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
    console(COMMANDLINEARGS, FILES, MODE, MACHINE)
