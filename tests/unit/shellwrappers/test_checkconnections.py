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
This testing module contains the tests for the testconnections method within
the shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import checkconnections


def sshfunc(job, cmd):
    """Function to mock the throwing of exception for a test."""

    if cmd[0] == "module avail" and job["resource"] == "resource1":

        raise exceptions.SSHError(
            "Err", ("", "bash: module: command not found", 0))


@mock.patch('longbow.shellwrappers.sendtossh')
def test_testconnections_single(mock_sendtossh):

    """
    Test that the connection test is launched.
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1"
        }
    }

    checkconnections(jobs)

    assert mock_sendtossh.call_count == 2, "sendtossh should be called twice"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_testconnections_multiple(mock_sendtossh):

    """
    Test that the connection test is run only for each host once.
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1"
        },
        "LongbowJob2": {
            "resource": "resource2"
        },
        "LongbowJob3": {
            "resource": "resource1"
        }
    }

    checkconnections(jobs)

    assert mock_sendtossh.call_count == 4, "should be called four times"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_testconnections_sshexcept(mock_sendtossh):

    """
    Test to see that if the underlying SSH call fails, the resulting
    SSHError is passed up the chain. This is important!
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1"
        },
        "LongbowJob2": {
            "resource": "resource2"
        },
        "LongbowJob3": {
            "resource": "resource1"
        }
    }

    mock_sendtossh.side_effect = exceptions.SSHError("SSH Error", "output")

    with pytest.raises(exceptions.SSHError):

        checkconnections(jobs)


@mock.patch('longbow.shellwrappers.sendtossh')
def test_testconnections_envfix(mock_sendtossh):

    """
    Test that the environment checking works.
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1",
            "env-fix": "false"
        },
        "LongbowJob2": {
            "resource": "resource2",
            "env-fix": "false"
        },
        "LongbowJob3": {
            "resource": "resource1",
            "env-fix": "false"
        }
    }

    mock_sendtossh.side_effect = sshfunc

    checkconnections(jobs)

    assert jobs["LongbowJob1"]["env-fix"] == "true"
    assert jobs["LongbowJob2"]["env-fix"] == "false"
    assert jobs["LongbowJob3"]["env-fix"] == "true"
