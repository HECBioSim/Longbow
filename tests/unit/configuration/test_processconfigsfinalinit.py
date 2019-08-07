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
This testing module contains the tests for the configuration module methods.
"""
try:

    from unittest import mock

except ImportError:

    import mock

import os
from longbow.configuration import _processconfigsfinalinit


def pluginsdata(_, data):

    """
    mocked getattr call for external data.
    """

    if data == "PLUGINEXECS":

        return {"testexec": "testmodule"}

    elif data == "MODNAMEOVERRIDES":

        return {"testmodule": "fictionmodule"}


def test_processconfigsfinalinit1():

    """
    Tests for basic functionality of the final initialisation checking method.
    """

    jobs = {
        "jobone": {
            "modules": "",
            "localworkdir": "/somepath/to/dir",
            "executableargs": "arg1 arg2 arg3",
            "executable": "pmemd.MPI",
            "remoteworkdir": "/work/dir"
        },
        "jobtwo": {
            "modules": "",
            "localworkdir": "",
            "executableargs": "-a --arg2 arg3",
            "executable": "gmx",
            "remoteworkdir": "/work/dir"
        }
    }

    _processconfigsfinalinit(jobs)

    assert jobs["jobone"]["localworkdir"] == "/somepath/to/dir"
    assert jobs["jobone"]["executableargs"] == ["arg1", "arg2", "arg3"]
    assert jobs["jobone"]["executable"] == "pmemd.MPI"
    assert jobs["jobone"]["destdir"] != ""
    assert jobs["jobone"]["remoteworkdir"] == "/work/dir"
    assert jobs["jobone"]["modules"] == "amber"

    assert jobs["jobtwo"]["localworkdir"] == os.getcwd()
    assert jobs["jobtwo"]["executableargs"] == ["-a", "--arg2", "arg3"]
    assert jobs["jobtwo"]["executable"] == "gmx"
    assert jobs["jobtwo"]["destdir"] != ""
    assert jobs["jobtwo"]["remoteworkdir"] == "/work/dir"
    assert jobs["jobtwo"]["modules"] == "gromacs"


def test_processconfigsfinalinit2():

    """
    Test with an absolute path for the executable.
    """

    jobs = {
        "test": {
            "modules": "",
            "localworkdir": "/somepath/to/dir",
            "executableargs": "arg1 arg2 arg3",
            "executable": "/some/path/to/mdrun_mpi_d",
            "remoteworkdir": "/work/dir"
        }
    }

    _processconfigsfinalinit(jobs)

    assert jobs["test"]["localworkdir"] == "/somepath/to/dir"
    assert jobs["test"]["executableargs"] == ["arg1", "arg2", "arg3"]
    assert jobs["test"]["executable"] == "/some/path/to/mdrun_mpi_d"
    assert jobs["test"]["destdir"] != ""
    assert jobs["test"]["remoteworkdir"] == "/work/dir"
    assert jobs["test"]["modules"] == ""


@mock.patch('longbow.configuration.getattr')
def test_processconfigsfinalinit3(attr):

    """
    Test the modulename overrides
    """

    jobs = {
        "jobone": {
            "modules": "",
            "localworkdir": "/somepath/to/dir",
            "executableargs": "arg1 arg2 arg3",
            "executable": "testexec",
            "remoteworkdir": "/work/dir"
        }
    }

    attr.side_effect = pluginsdata

    _processconfigsfinalinit(jobs)

    assert jobs["jobone"]["localworkdir"] == "/somepath/to/dir"
    assert jobs["jobone"]["executableargs"] == ["arg1", "arg2", "arg3"]
    assert jobs["jobone"]["executable"] == "testexec"
    assert jobs["jobone"]["destdir"] != ""
    assert jobs["jobone"]["remoteworkdir"] == "/work/dir"
    assert jobs["jobone"]["modules"] == "fictionmodule"
