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
This test module contains tests for the SoGE scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.schedulers.soge import status

out = ("job-ID  prior name       user         state submit/start at     queue      master  ja-task-ID\n"
       "---------------------------------------------------------------------------------------------\n"
       "     20     0 sleep.sh   sysadm1      h     12/23/2003 23:22:09 frontend-0 MASTER            \n"
       "     21     0 sleep.sh   sysadm1      r     12/23/2003 23:22:09 frontend-0 MASTER            \n"
       "     22     0 sleep.sh   sysadm1      qw    12/23/2003 23:22:06                              \n")


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state1(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "20"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Held"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state2(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "21"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Running"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state3(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "22"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Queued"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state4(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538341"
    }

    mock_ssh.return_value = ("", "", 0)

    output = status(job)

    assert output == "Finished"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_except1(mock_ssh):

    """
    Test if SSH Error is handled.
    """

    job = {
        "user": "test",
        "jobid": ""
    }

    mock_ssh.side_effect = exceptions.SSHError("OUT", "ERR")

    with pytest.raises(exceptions.SSHError):

        status(job)
