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


@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_single(mock_isdir, mock_submit):

    """
    Test that a single job only tries to submit something once.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False

    scheduling.submit(jobs)

    assert mock_submit.call_count == 1, \
        "For a single job this method should only be called once"
    assert jobs["job-one"]["laststatus"] == "Queued"


@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_multiplesame(mock_isdir, mock_lsf):

    """
    Test that for multiple jobs the correct number of submission calls happen.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test123"
        },
        "job-two": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        },
        "job-three": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test789"
        }
    }

    mock_isdir.return_value = False

    scheduling.submit(jobs)

    assert mock_lsf.call_count == 3, \
        "For a multi job this method should only be called more than once"


@mock.patch('Longbow.schedulers.slurm.submit')
@mock.patch('Longbow.schedulers.pbs.submit')
@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_multiplediff(mock_isdir, mock_lsf, mock_pbs, mock_slurm):

    """
    Test that for multiple jobs the correct number of submission calls happen.
    """

    jobs = {
        "job-one": {
            "resource": "lsf-machine",
            "scheduler": "LSF",
            "jobid": "test123"
        },
        "job-two": {
            "resource": "pbs-machine",
            "scheduler": "pbs",
            "jobid": "test456"
        },
        "job-three": {
            "resource": "slurm-machine",
            "scheduler": "Slurm",
            "jobid": "test789"
        }
    }

    mock_isdir.return_value = False

    scheduling.submit(jobs)

    assert mock_lsf.call_count == 1, \
        "For a single job this method should only be called once"
    assert mock_pbs.call_count == 1, \
        "For a single job this method should only be called once"
    assert mock_slurm.call_count == 1, \
        "For a single job this method should only be called once"


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_fileexcept1(mock_isdir, mock_submit, mock_savini):

    """
    Test that if the recovery file write fails it does so in a controlled way.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None
    mock_savini.side_effect = OSError

    scheduling.submit(jobs)


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_fileexcept2(mock_isdir, mock_submit, mock_savini):

    """
    Test that if the recovery file write fails it does so in a controlled way.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None
    mock_savini.side_effect = IOError

    scheduling.submit(jobs)


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_attrexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that errors with missing plugins are handled correctly.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.submit(jobs)


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_submitexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that submission failure errors are handled correctly.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = exceptions.JobsubmitError("Submit Error")

    scheduling.submit(jobs)

    assert jobs["job-one"]["laststatus"] == "Submit Error"


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_queueexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that queue limit events are handled correctly if a plugin raises the
    queuemax exception.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = exceptions.QueuemaxError("Submit Error")

    scheduling.submit(jobs)

    assert jobs["job-one"]["laststatus"] == "Waiting Submission"


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_queueinfo(mock_isdir, mock_submit, mock_savini):

    """
    Check that the queueinformation counter is getting used.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test123"
        },
        "job-two": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        },
        "job-three": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test789"
        }
    }
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = "0"
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = "0"

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.return_value = None

    scheduling.submit(jobs)

    assert scheduling.QUEUEINFO["test-machine"]["queue-slots"] == "3"
    assert scheduling.QUEUEINFO["test-machine"]["queue-max"] == "3"
