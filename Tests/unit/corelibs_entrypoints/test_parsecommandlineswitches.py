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
This testing module contains the tests for the parsecommandlineswitches method
within the entrypoint module.
"""

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.entrypoints as mains


def test_parsecmdlineswitches_test1():

    """
    Test that with no commandline parameter, that nothing gets made up.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    longbowargs = []

    mains._parsecommandlineswitches(parameters, longbowargs)

    assert parameters["debug"] is False
    assert parameters["disconnect"] is False
    assert parameters["executable"] == ""
    assert parameters["executableargs"] == []
    assert parameters["hosts"] == ""
    assert parameters["job"] == ""
    assert parameters["jobname"] == ""
    assert parameters["log"] == ""
    assert parameters["recover"] == ""
    assert parameters["resource"] == ""
    assert parameters["replicates"] == ""
    assert parameters["verbose"] == False
    assert len(parameters) == 12


def test_parsecmdlineswitches_test2():

    """
    Test that parameters get picked up and the disconnect param is ignored,
    also make sure nothing extra is added.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    longbowargs = ["-resource", "whoppa", "-log", "logfile", "--job",
                   "jobfile", "-hosts", "hostfile", "--jobname", "test",
                   "-replicates", "5", "--disconnect", "--verbose",
                   "--recover", "recfile"]

    mains._parsecommandlineswitches(parameters, longbowargs)

    assert parameters["debug"] is False
    assert parameters["disconnect"] is True
    assert parameters["executable"] == ""
    assert parameters["executableargs"] == []
    assert parameters["hosts"] == "hostfile"
    assert parameters["job"] == "jobfile"
    assert parameters["jobname"] == "test"
    assert parameters["log"] == "logfile"
    assert parameters["recover"] == "recfile"
    assert parameters["resource"] == "whoppa"
    assert parameters["replicates"] == "5"
    assert parameters["verbose"] is True
    assert len(parameters) == 12


def test_parsecmdlineswitches_test3():

    """
    Check that the exception is raised when a param value is missed.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    longbowargs = ["-resource", "whoppa", "-log", "logfile", "--job",
                   "jobfile", "-hosts", "hostfile", "--jobname", "test",
                   "-replicates", "5", "--disconnect", "--recover"]

    with pytest.raises(exceptions.CommandlineargsError):

        mains._parsecommandlineswitches(parameters, longbowargs)


def test_parsecmdlineswitches_test4():

    """
    Check that the exception is raised when a param value is missed.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    longbowargs = ["-resource", "whoppa", "-log", "logfile", "--job",
                   "jobfile", "-hosts", "hostfile", "--jobname", "-replicates",
                   "5", "--disconnect", "--recover", "recfile"]

    with pytest.raises(exceptions.CommandlineargsError):

        mains._parsecommandlineswitches(parameters, longbowargs)


def test_parsecmdlineswitches_test5():

    """
    Test for hypocthetical true to false switch.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": True
    }

    longbowargs = ["-resource", "whoppa", "-log", "logfile", "--job",
                   "jobfile", "-hosts", "hostfile", "--jobname", "test",
                   "-replicates", "5", "--disconnect", "--verbose",
                   "--recover", "recfile"]

    mains._parsecommandlineswitches(parameters, longbowargs)

    assert parameters["debug"] is False
    assert parameters["disconnect"] is True
    assert parameters["executable"] == ""
    assert parameters["executableargs"] == []
    assert parameters["hosts"] == "hostfile"
    assert parameters["job"] == "jobfile"
    assert parameters["jobname"] == "test"
    assert parameters["log"] == "logfile"
    assert parameters["recover"] == "recfile"
    assert parameters["resource"] == "whoppa"
    assert parameters["replicates"] == "5"
    assert parameters["verbose"] is False
    assert len(parameters) == 12
