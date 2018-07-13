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
This testing module contains the tests for the _checkwaitingjobs method within
the scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.scheduling import _checkwaitingjobs


def addjobid(job):

    """
    Add a job id to job
    """

    job["jobid"] = "123456"


@mock.patch('longbow.schedulers.lsf.submit')
def test_checkwaitingjobs_none(mock_submit):

    """
    Check that if no jobs are marked as waiting that nothing gets submitted.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "resource": "hpc-1"
        },
        "jobtwo": {
            "laststatus": "Finished",
            "resource": "hpc-1"
        },
        "jobthree": {
            "laststatus": "Complete",
            "resource": "hpc-1"
        }
    }

    _checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 0, "Should not be trying to submit"


@mock.patch('longbow.schedulers.lsf.submit')
def test_checkwaitingjobs_one(mock_submit):

    """
    Check that in cases that when there are two jobs waiting and only slot,
    that only one job gets submitted.
    """

    jobs = {
        "lbowconf": {
            "test-machine-queue-slots": 1,
            "test-machine-queue-max": 2
        },
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = addjobid

    _checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 1, "Should be submitting one job"
    assert jobs["lbowconf"]["test-machine-queue-slots"] == "2"


@mock.patch('longbow.schedulers.lsf.submit')
def test_checkwaitingjobs_two(mock_submit):

    """
    Check that in cases where there are multiple jobs but a lot less than the
    number of slots available only the correct number of jobs are submitted.
    """

    jobs = {
        "lbowconf": {
            "test-machine-queue-slots": 1,
            "test-machine-queue-max": 8
        },
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = addjobid

    _checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 2, "Should be submitting two jobs"
    assert jobs["lbowconf"]["test-machine-queue-slots"] == "3"


@mock.patch('longbow.schedulers.lsf.submit')
def test_checkwaitingjobs_except1(mock_submit):

    """
    Check if the plugin is not found that the correct exception is raised.
    """

    jobs = {
        "lbowconf": {
            "test-machine-queue-slots": 1,
            "test-machine-queue-max": 8
        },
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        _checkwaitingjobs(jobs, False)


@mock.patch('longbow.schedulers.lsf.submit')
def test_checkwaitingjobs_except2(mock_submit):

    """
    Check that if the submit error is thrown that the job is simply marked
    as in error state.
    """

    jobs = {
        "lbowconf": {
            "test-machine-queue-slots": 1,
            "test-machine-queue-max": 8
        },
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = exceptions.JobsubmitError

    _checkwaitingjobs(jobs, False)

    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Submit Error"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"


@mock.patch('longbow.schedulers.lsf.submit')
def test_checkwaitingjobs_except3(mock_submit):

    """
    Check that if the max queue error is thrown that the job is simply marked
    as in error state.
    """

    jobs = {
        "lbowconf": {
            "test-machine-queue-slots": 1,
            "test-machine-queue-max": 8
        },
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = exceptions.QueuemaxError

    _checkwaitingjobs(jobs, False)

    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Submit Error"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"
