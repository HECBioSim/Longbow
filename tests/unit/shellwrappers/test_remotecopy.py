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
This testing module contains the tests for the remotecopy method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import remotecopy


def test_remotecopy_srcpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    src = "source/directory/path"
    dst = "~/source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        remotecopy(job, src, dst)


def test_remotecopy_dstpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    src = "~/source/directory/path"
    dst = "source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        remotecopy(job, src, dst)


@mock.patch('longbow.shellwrappers.sendtossh')
def test_remotecopy_formattest(mock_sendtossh):

    """
    Check that the format of the ls command is constructed correctly when sent
    to the SSH method.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
    }

    src = "~/source/directory/path"
    dst = "~/destination/directory/path"

    remotecopy(job, src, dst)

    callargs = mock_sendtossh.call_args[0][1]
    testargs = "cp -r ~/source/directory/path ~/destination/directory/path"

    assert " ".join(callargs) == testargs


@mock.patch('longbow.shellwrappers.sendtossh')
def test_remotecopy_exceptiontest(mock_sendtossh):

    """
    Check that the SSH exception is percolated properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
    }

    src = "~/source/directory/path"
    dst = "~/destination/directory/path"

    mock_sendtossh.side_effect = exceptions.SSHError("SSHError", "Error")

    with pytest.raises(exceptions.RemotecopyError):

        remotecopy(job, src, dst)
