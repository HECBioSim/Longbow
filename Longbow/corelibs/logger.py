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

"""Module containing the logging methods. Methods for creating
loggers of either a standard, verbose or debug nature are found here."""

import logging


def setuplogger(logfile, loggername, mode):

    """Setup the correct logger based on """

    if mode["debug"]:
        debuglogger(logfile, loggername)
    elif mode["verbose"]:
        verboselogger(logfile, loggername)
    else:
        standardlogger(logfile, loggername)


def standardlogger(logfile, loggername):

    """The standard logger will be configured to simply write log events
    from the package into the specified file."""

    # Create a logger.
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)

    # Define a logging format.
    logformat = logging.Formatter("%(asctime)s - %(message)s")

    # Set logger to write to file, set level and bind format.
    loghandle = logging.FileHandler(logfile, mode="w")
    loghandle.setLevel(logging.INFO)
    loghandle.setFormatter(logformat)
    logger.addHandler(loghandle)


def verboselogger(logfile, loggername):

    """The debug logger will be configured to write a more advanced output
    from log events to both the specified file and standard out."""

    # Create a logger.
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)

    # Define a logging format.
    logformat = logging.Formatter("%(asctime)s - %(message)s")

    # Default is to write to the log file, set level and bind format.
    loghandler = logging.FileHandler(logfile, mode="w")
    loghandler.setLevel(logging.INFO)
    loghandler.setFormatter(logformat)
    logger.addHandler(loghandler)

    loghandler = logging.StreamHandler()
    loghandler.setLevel(logging.INFO)
    loghandler.setFormatter(logformat)
    logger.addHandler(loghandler)


def debuglogger(logfile, loggername):

    """The debug logger will be configured to write a more advanced output
    from log events to both the specified file and standard out."""

    # Create a logger.
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)

    # Define a logging format.
    logformat = logging.Formatter("%(asctime)s - %(name)s - " +
                                  "%(filename)-18s - %(levelname)-8s" +
                                  " - %(message)s")

    # Default is to write to the log file, set level and bind format.
    loghandler = logging.FileHandler(logfile, mode="w")
    loghandler.setLevel(logging.DEBUG)
    loghandler.setFormatter(logformat)
    logger.addHandler(loghandler)

    loghandler = logging.StreamHandler()
    loghandler.setLevel(logging.DEBUG)
    loghandler.setFormatter(logformat)
    logger.addHandler(loghandler)
