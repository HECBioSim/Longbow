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
This module contains methods for setting up and configuring the standard
logging module provided by the python standard library. There are different
types of logger configuration within this module, and these types lend
themselves to fulfil the requirements of Longbow.

The following methods can be found in this module:

setuplogger()
    This method is used by Longbow to determine which level of logging is
    required based on user input. This method is specific to the function
    of Longbow and may or may not be suitable for developers to use in their
    own software.

standardlogger()
    This method configures the python logger to log to the specified file,
    the standard logging profile only writes out messages marked at info,
    warning and error level. Statements in the code that are marked as debug
    will be hidden by this logger.

verboselogger()
    This method configures the python logger to log to the specified file along
    with placing the same information into the standard output (usually a
    terminal or console), the verbose logging profile only writes out messages
    marked at info, warning and error level. Statements in the code that are
    marked as debug will be hidden by this logger.

debuglogger()
    This method configures the python logger to log to the specified file along
    with placing the same information into the standard output (usually a
    terminal or console). The debug logging profile will write out messages
    marked under all levels, this is to enable maximum information for
    debugging purposes.
"""

import logging


def setuplogger(logfile, loggername, mode):

    """
    This method is used by Longbow to determine which level of logging is
    required based on user input. This method is specific to the function
    of Longbow and may or may not be suitable for developers to use in their
    own software.

    Required arguments are:

    logfile (string) - path to file that will be written to.

    loggername (string) - Longbow modules all look for a module called
                          "longbow", so this should be the same if you are
                          using this to configure a longbow logger.

    mode (dictionary) -  A dictionary that contains true/false pairs for the
                         parameters debug and verbose, if all are false then
                         a standard logger will be set up.
    """

    if mode["debug"]:

        debuglogger(logfile, loggername)

    elif mode["verbose"]:

        verboselogger(logfile, loggername)

    else:

        standardlogger(logfile, loggername)


def standardlogger(logfile, loggername):

    """
    This method configures the python logger to log to the specified file,
    the standard logging profile only writes out messages marked at info,
    warning and error level. Statements in the code that are marked as debug
    will be hidden by this logger.

    Required arguments are:

    logfile (string) - path to file that will be written to.

    loggername (string) - Longbow modules all look for a module called
                          "longbow", so this should be the same if you are
                          using this to configure a longbow logger.
    """

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

    """
    This method configures the python logger to log to the specified file along
    with placing the same information into the standard output (usually a
    terminal or console), the verbose logging profile only writes out messages
    marked at info, warning and error level. Statements in the code that are
    marked as debug will be hidden by this logger.

    Required arguments are:

    logfile (string) - path to file that will be written to.

    loggername (string) - Longbow modules all look for a module called
                          "longbow", so this should be the same if you are
                          using this to configure a longbow logger.
    """

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

    """
    This method configures the python logger to log to the specified file along
    with placing the same information into the standard output (usually a
    terminal or console). The debug logging profile will write out messages
    marked under all levels, this is to enable maximum information for
    debugging purposes.

    Required arguments are:

    logfile (string) - path to file that will be written to.

    loggername (string) - Longbow modules all look for a module called
                          "longbow", so this should be the same if you are
                          using this to configure a longbow logger.
    """

    # Create a logger.
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.DEBUG)

    # Define a logging format.
    logformat = logging.Formatter("%(asctime)s - %(name)s - " +
                                  "%(filename)-18s - %(levelname)-8s" +
                                  " -   %(message)s")

    # Default is to write to the log file, set level and bind format.
    loghandler = logging.FileHandler(logfile, mode="w")
    loghandler.setLevel(logging.DEBUG)
    loghandler.setFormatter(logformat)
    logger.addHandler(loghandler)

    loghandler = logging.StreamHandler()
    loghandler.setLevel(logging.DEBUG)
    loghandler.setFormatter(logformat)
    logger.addHandler(loghandler)
