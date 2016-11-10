# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of the
# HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the UK
# biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 2 of the License, or (at your option) any later
# version.
#
# Longbow is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""
This testing module contains the tests for the scheduling module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.scheduling as scheduling


def addjobid(job):

    """
    Add a job id to job
    """

    job["jobid"] = "123456"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_none(mock_submit):

    """
    Check that if no jobs are marked as waiting that nothing gets submitted.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running"
        },
        "jobtwo": {
            "laststatus": "Finished"
        },
        "jobthree": {
            "laststatus": "Complete"
        }
    }

    scheduling._checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 0, "Should not be trying to submit"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_one(mock_submit):

    """
    Check that in cases that when there are two jobs waiting and only slot,
    that only one job gets submitted.
    """

    jobs = {
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
    scheduling.QUEUEINFO["test-machine"] = {}
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 2

    scheduling._checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 1, "Should be submitting one job"
    assert scheduling.QUEUEINFO["test-machine"]["queue-slots"] == "2"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_two(mock_submit):

    """
    Check that in cases where there are multiple jobs but a lot less than the
    number of slots available only the correct number of jobs are submitted.
    """

    jobs = {
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
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 8

    scheduling._checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 2, "Should be submitting two jobs"
    assert scheduling.QUEUEINFO["test-machine"]["queue-slots"] == "3"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_except1(mock_submit):

    """
    Check if the plugin is not found that the correct exception is raised.
    """

    jobs = {
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
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 8

    with pytest.raises(exceptions.PluginattributeError):

        scheduling._checkwaitingjobs(jobs, False)


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_except2(mock_submit):

    """
    Check that if the submit error is thrown that the job is simply marked
    as in error state.
    """

    jobs = {
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
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 8

    scheduling._checkwaitingjobs(jobs, False)

    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Submit Error"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_except3(mock_submit):

    """
    Check that if the max queue error is thrown that the job is simply marked
    as in error state.
    """

    jobs = {
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
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = "8"

    scheduling._checkwaitingjobs(jobs, False)

    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Submit Error"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"
