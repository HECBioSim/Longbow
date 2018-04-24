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
This testing module contains the tests for the parsecommandlineswitches method
within the entrypoint module.
"""

import pytest

import longbow.exceptions as exceptions
from longbow.entrypoints import _parsecommandlineswitches


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

    _parsecommandlineswitches(parameters, longbowargs)

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
    assert parameters["verbose"] is False
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

    _parsecommandlineswitches(parameters, longbowargs)

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

        _parsecommandlineswitches(parameters, longbowargs)


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

        _parsecommandlineswitches(parameters, longbowargs)


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

    _parsecommandlineswitches(parameters, longbowargs)

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
