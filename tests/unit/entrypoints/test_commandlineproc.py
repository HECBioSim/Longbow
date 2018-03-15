# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council and
# The University of Nottingham
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
This testing module contains the tests for the commandlineproc method within
the entrypoint module.
"""

import pytest

import longbow.exceptions as exceptions
from longbow.entrypoints import _commandlineproc

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
        "-maxtime",
        "--maxtime",
        "-nochecks",
        "--nochecks",
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
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == ""
    assert longbowargs == []


def test_cmdlineproc_test2():

    """Test a single dashed longbow arg."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == ""
    assert longbowargs == ["-about"]


def test_cmdlineproc_test3():

    """Test a double dashed longbow arg."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == ""
    assert longbowargs == ["--about"]


def test_cmdlineproc_test4():

    """Test multiple Longbow arguments."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == ""
    assert parameters["executableargs"] == ""
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--replicates", "1000", "--disconnect"]


def test_cmdlineproc_test5():

    """Test executable with Longbow args."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == "pmemd.MPI"
    assert parameters["executableargs"] == ""
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--replicates", "1000", "--disconnect"]


def test_cmdlineproc_test6():

    """Test executable with Longbow args and executable args."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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
                       "--maxtime", "01:00", "--replicates", "1000",
                       "--disconnect", "pmemd.MPI", "-O", "-i", "ex.in", "-c",
                       "ex.min", "-p", "ex.top", "-o", "ex.out"]

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == "pmemd.MPI"
    assert parameters["executableargs"] == \
        "-O -i ex.in -c ex.min -p ex.top -o ex.out"
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--maxtime", "01:00", "--replicates", "1000",
                           "--disconnect"]


def test_cmdlineproc_test7():

    """Test unknown executable with Longbow args."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == ""
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
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == "-i input.file param1 --someflag"
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
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == "-i input.file param1 --someflag"
    assert longbowargs == ["--hosts", "hosts.file", "--jobname", "test",
                           "--disconnect", "--replicates", "1000"]


def test_cmdlineproc_test10():

    """Test unknown executable with just the executable."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == ""
    assert longbowargs == []


def test_cmdlineproc_test11():

    """Test unknown executable without Longbow args and with exec args."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

    longbowargs = _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)

    assert parameters["executable"] == "test.exe"
    assert parameters["executableargs"] == "-i input.file param1 --someflag"
    assert longbowargs == []


def test_cmdlineproc_test12():

    """Test for bogus command-line flags."""

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

        _commandlineproc(ALLLONGBOWARGS, commandlineargs, parameters)
