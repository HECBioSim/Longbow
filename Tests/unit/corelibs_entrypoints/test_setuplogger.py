# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of the
# HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the UK
# biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# Longbow is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""
This testing module contains the tests for the main method within the
entrypoint module.
"""

import logging

import Longbow.corelibs.entrypoints as mains


def test_setuplogger_testdebug():

    """
    Test to check if the logging method sets up logging properly. This is
    a very rudimentary check as it is difficult to test this.
    """

    parameters = {
        "debug": True,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "job.conf",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    mains._setuplogger(parameters)

    log = logging.getLogger("Longbow")
    log.debug("debug1")
    log.info("info1")

    logfile = open("log", "r")
    contents = logfile.readlines()

    assert "debug1" in contents[0]
    assert "info1" in contents[1]


def test_setuplogger_testverbose():

    """
    Test to check if the logging method sets up logging properly. This is
    a very rudimentary check as it is difficult to test this.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "job.conf",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": True
    }

    mains._setuplogger(parameters)

    log = logging.getLogger("Longbow")
    log.debug("debug1")
    log.info("info1")

    logfile = open("log", "r")
    contents = logfile.readlines()

    assert "debug1" not in contents[0]
    assert "debug1" not in contents[1]
    assert "info1" in contents[0]
