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
This testing module contains the tests for the remotelist method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import remotelist


def test_remotelist_srcpath():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "source/directory/path"
    }

    with pytest.raises(exceptions.AbsolutepathError):

        remotelist(job)


@mock.patch('longbow.shellwrappers.sendtossh')
def test_remotelist_returncheck(mock_sendtossh):

    """
    Check that the output from the shell is deconstructed into a list properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    mock_sendtossh.return_value = "Directory1\nfile1\nfile2", "", ""

    filelist = remotelist(job)

    assert filelist[0] == "Directory1"
    assert filelist[1] == "file1"
    assert filelist[2] == "file2"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_remotelist_formattest(mock_sendtossh):

    """
    Check that the format of the ls command is constructed correctly when sent
    to the SSH method.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    remotelist(job)

    callargs = mock_sendtossh.call_args[0][1]
    testargs = "ls ~/source/directory/path"

    assert " ".join(callargs) == testargs


@mock.patch('longbow.shellwrappers.sendtossh')
def test_remotelist_exceptiontest(mock_sendtossh):

    """
    Check that the SSH exception is percolated properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    mock_sendtossh.side_effect = exceptions.SSHError("SSHError", "Error")

    with pytest.raises(exceptions.RemotelistError):

        remotelist(job)
