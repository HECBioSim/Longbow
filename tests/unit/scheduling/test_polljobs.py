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
This testing module contains the tests for the polljobs method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.scheduling import _polljobs


@mock.patch('longbow.schedulers.lsf.status')
def test_polljobs_callcount(mock_status):

    """
    Test that only jobs with the correct state end up getting polled.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobtwo": {
            "laststatus": "Queued",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobthree": {
            "laststatus": "Submit Error",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfour": {
            "laststatus": "Waiting Submission",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfive": {
            "laststatus": "Finished",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobsix": {
            "laststatus": "Complete",
            "scheduler": "LSF",
            "jobid": "123456"
        }
    }

    mock_status.return_value = "Running"
    returnval = _polljobs(jobs, False)

    assert mock_status.call_count == 2, \
        "Should only be polling running and queued jobs"
    assert jobs["jobtwo"]["laststatus"] == "Running"
    assert returnval is True


@mock.patch('longbow.schedulers.lsf.status')
def test_polljobs_finished(mock_status):

    """
    Test that only jobs with the correct state end up getting polled.
    """

    jobs = {
        "lbowconf": {
            "test-machine-queue-slots": 2,
            "test-machine-queue-max": 4
        },
        "jobone": {
            "resource": "test-machine",
            "laststatus": "Running",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobtwo": {
            "resource": "test-machine",
            "laststatus": "Queued",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobthree": {
            "resource": "test-machine",
            "laststatus": "Submit Error",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfour": {
            "resource": "test-machine",
            "laststatus": "Waiting Submission",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfive": {
            "resource": "test-machine",
            "laststatus": "Finished",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobsix": {
            "resource": "test-machine",
            "laststatus": "Complete",
            "scheduler": "LSF",
            "jobid": "123456"
        }
    }

    mock_status.return_value = "Finished"
    _polljobs(jobs, False)

    assert mock_status.call_count == 2, \
        "Should only be polling running and queued jobs"
    assert jobs["jobone"]["laststatus"] == "Finished"
    assert jobs["jobtwo"]["laststatus"] == "Finished"
    assert jobs["lbowconf"]["test-machine-queue-slots"] == "0"


@mock.patch('longbow.schedulers.lsf.status')
def test_polljobs_except(mock_status):

    """
    Test that only jobs with the correct state end up getting polled.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "laststatus": "Running",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobtwo": {
            "resource": "test-machine",
            "laststatus": "Queued",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobthree": {
            "resource": "test-machine",
            "laststatus": "Submit Error",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfour": {
            "resource": "test-machine",
            "laststatus": "Waiting Submission",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfive": {
            "resource": "test-machine",
            "laststatus": "Finished",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobsix": {
            "resource": "test-machine",
            "laststatus": "Complete",
            "scheduler": "LSF",
            "jobid": "123456"
        }
    }

    mock_status.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        _polljobs(jobs, False)
