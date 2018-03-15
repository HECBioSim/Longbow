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
This testing module contains the tests for the sendtossh method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import sendtossh


@mock.patch('longbow.shellwrappers.sendtoshell')
def test_sendtossh_returncheck(mock_sendtoshell):

    """
    This test will check that the sendtossh method will exit and return the
    raw return values from sendtoshell.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "env-fix": "false"
    }

    args = ["ls"]

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    output = sendtossh(job, args)

    assert output[0] == "Output message", "method is not returning stdout"
    assert output[1] == "Error message", "method is not returning stderr"
    assert output[2] == 0, "method is not returning the error code"


@mock.patch('longbow.shellwrappers.sendtoshell')
def test_sendtossh_errorcode(mock_sendtoshell):

    """
    This test will check that if the error code is not 0 or 255 that the
    SSHError exception is raised.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "env-fix": "false"
    }

    args = ["ls"]

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 1

    with pytest.raises(exceptions.SSHError):

        sendtossh(job, args)


@mock.patch('longbow.shellwrappers.sendtoshell')
def test_sendtossh_formattest(mock_sendtoshell):

    """
    Testing the format of the rsync call sent to the shell. This test
    will check that calls without masks get formed correctly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "env-fix": "false"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    sendtossh(job, ["ls"])

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = "ssh -p 22 juan_trique-ponee@massive-machine ls"

    assert " ".join(callargs) == testargs


@mock.patch('longbow.shellwrappers.sendtoshell')
def test_sendtossh_envfix(mock_sendtoshell):

    """
    Testing that the environment fix is switched on.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "env-fix": "true"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    sendtossh(job, ["ls"])

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = ("ssh -p 22 juan_trique-ponee@massive-machine source "
                "/etc/profile; ls")

    assert " ".join(callargs) == testargs


@mock.patch('time.sleep')
@mock.patch('longbow.shellwrappers.sendtoshell')
def test_sendtossh_retries(mock_sendtoshell, mock_time):

    """
    This test will check that if an error code of 255 is raised, that the
    retries happen and that eventually upon failure that the SSHError
    exception is raised.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "env-fix": "false"
    }

    args = ["ls"]

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 255

    # Set the timout for retries to 0 seconds to speed up test.
    mock_time.return_value = None

    with pytest.raises(exceptions.SSHError):

        sendtossh(job, args)

    assert mock_sendtoshell.call_count == 3, "This method should retry 3 times"
