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
This testing module contains the tests for the commandlineproc method within
the entrypoint module.
"""

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.entrypoints as mains

ALLLONGBOWARGS = [
    "-about",
    "--about",
    "-debug",
    "--debug",
    "-disconnect",
    "--disconnect",
    "-examples",
    "--examples",
    "-h",
    "-help",
    "--help",
    "-hosts",
    "--hosts",
    "-job",
    "--job",
    "-jobname",
    "--jobname",
    "-log",
    "--log",
    "-recover",
    "--recover",
    "-resource",
    "--resource",
    "-replicates",
    "--replicates",
    "-V",
    "-verbose",
    "--verbose",
    "-version",
    "--version"
    ]


def test_cmdlineproc_test1():

    """
    Test that if there is nothing on the command-line that nothing happens.
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

    commandlineargs = []

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == []
    assert longbowargs == []


def test_cmdlineproc_test2():

    """Test a single dashed longbow arg."""

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

    commandlineargs = ["-about"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == []
    assert longbowargs == ["-about"]


def test_cmdlineproc_test3():

    """Test a double dashed longbow arg."""

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

    commandlineargs = ["--about"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == []
    assert longbowargs == ["--about"]


def test_cmdlineproc_test4():

    """Test multiple Longbow arguments."""

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

    commandlineargs = ["--hosts", "hosts.file", "--jobname", "test",
                       "--replicates", "1000", "--disconnect"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == []
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--replicates", "1000", "--disconnect"]


def test_cmdlineproc_test5():

    """Test executable with Longbow args."""

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

    commandlineargs = ["--hosts", "hosts.file", "--jobname", "test",
                       "--replicates", "1000", "--disconnect", "pmemd.MPI"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == "pmemd.MPI"
    assert parameters["executableargs"] == []
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--replicates", "1000", "--disconnect"]


def test_cmdlineproc_test6():

    """Test executable with Longbow args and executable args."""

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

    commandlineargs = ["--hosts", "hosts.file", "--jobname", "test",
                       "--replicates", "1000", "--disconnect", "pmemd.MPI",
                       "-O", "-i", "ex.in", "-c", "ex.min", "-p", "ex.top",
                       "-o", "ex.out"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == "pmemd.MPI"
    assert parameters["executableargs"] == ["-O", "-i", "ex.in", "-c",
                                            "ex.min", "-p", "ex.top",
                                            "-o", "ex.out"]
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--replicates", "1000", "--disconnect"]


def test_cmdlineproc_test7():

    """Test unknown executable with Longbow args."""

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

    commandlineargs = ["--hosts", "hosts.file", "--jobname", "test",
                       "--replicates", "1000", "--disconnect", "test.exe"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == []
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--replicates", "1000", "--disconnect"]


def test_cmdlineproc_test8():

    """
    Test unknown executable with Longbow args and exec args.
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

    commandlineargs = ["--hosts", "hosts.file", "--jobname", "test",
                       "--replicates", "1000", "--disconnect", "test.exe",
                       "-i", "input.file", "param1", "--someflag"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == ["-i", "input.file", "param1",
                                            "--someflag"]
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--replicates", "1000", "--disconnect"]


def test_cmdlineproc_test9():

    """
    Test unknown executable with Longbow args and exec args, this one tests
    when longbow args ends with a param of type --flag <value>
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

    commandlineargs = ["--hosts", "hosts.file", "--jobname", "test",
                       "--disconnect", "--replicates", "1000", "test.exe",
                       "-i", "input.file", "param1", "--someflag"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == ["-i", "input.file", "param1",
                                            "--someflag"]
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--disconnect", "--replicates", "1000"]


def test_cmdlineproc_test10():

    """Test unknown executable with just the executable."""

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

    commandlineargs = ["test.exe"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == []
    assert longbowargs == []


def test_cmdlineproc_test11():

    """Test unknown executable without Longbow args and with exec args."""

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

    commandlineargs = ["test.exe", "-i", "input.file", "param1", "--someflag"]

    longbowargs = mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                                         parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == ["-i", "input.file", "param1",
                                            "--someflag"]
    assert longbowargs == []


def test_cmdlineproc_test12():

    """Test for bogus command-line flags."""

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

    commandlineargs = ["--hosts", "hosts.file", "--bogus", "--jobname", "test",
                       "--replicates", "1000", "--disconnect", "pmemd.MPI",
                       "-O", "-i", "ex.in", "-c", "ex.min", "-p", "ex.top",
                       "-o", "ex.out"]

    with pytest.raises(exceptions.CommandlineargsError):

        mains._commandlineproc(ALLLONGBOWARGS, commandlineargs,
                               parameters)
