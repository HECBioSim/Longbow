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
This test module contains tests for the slurm scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.schedulers.slurm import submit


@mock.patch('longbow.shellwrappers.sendtossh')
def test_submit_jobid1(mock_ssh):

    """
    Test if job id can be grabbed.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.return_value = ("Submitted batch job 5346", "", 0)

    submit(job)

    assert job["jobid"] == "5346"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_submit_jobid2(mock_ssh):

    """
    Test if Jobsubmit exception is triggered if job id can't be grabbed.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.return_value = ("success", "", 0)

    with pytest.raises(exceptions.JobsubmitError):

        submit(job)


@mock.patch('longbow.shellwrappers.sendtossh')
def test_submit_except1(mock_ssh):

    """
    Test if Queuemax exception is triggered based on output from scheduler.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.side_effect = exceptions.SSHError(
        "Error", ("out", "Batch job submission failed: Job violates accounting"
                  "/QOS policy (job submit limit, user's size and/or time "
                  "limits)", 0))
    mock_ssh.return_value = ("success", "Error", 0)

    with pytest.raises(exceptions.QueuemaxError):

        submit(job)


@mock.patch('longbow.shellwrappers.sendtossh')
def test_submit_except2(mock_ssh):

    """
    Check that jobsubmit exception is raised on generic SSH failure.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.side_effect = exceptions.SSHError("Error", ("out", "err", 0))
    mock_ssh.return_value = ("success", "error", 0)

    with pytest.raises(exceptions.JobsubmitError):

        submit(job)
