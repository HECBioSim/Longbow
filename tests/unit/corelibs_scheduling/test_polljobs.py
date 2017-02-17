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
This testing module contains the tests for the polljobs method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.scheduling import _polljobs, QUEUEINFO


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

    QUEUEINFO["test-machine"]["queue-slots"] = "2"
    mock_status.return_value = "Finished"
    _polljobs(jobs, False)

    assert mock_status.call_count == 2, \
        "Should only be polling running and queued jobs"
    assert jobs["jobone"]["laststatus"] == "Finished"
    assert jobs["jobtwo"]["laststatus"] == "Finished"
    assert QUEUEINFO["test-machine"]["queue-slots"] == "0"


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
