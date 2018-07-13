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
This testing module contains the tests for the submit method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.scheduling import submit


@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_single(mock_isdir, mock_submit):

    """
    Test that a single job only tries to submit something once.
    """

    jobs = {
        "lbowconf": {},
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False

    submit(jobs)

    assert mock_submit.call_count == 1, \
        "For a single job this method should only be called once"
    assert jobs["job-one"]["laststatus"] == "Queued"


@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_multiplesame(mock_isdir, mock_lsf):

    """
    Test that for multiple jobs the correct number of submission calls happen.
    """

    jobs = {
        "lbowconf": {},
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

    submit(jobs)

    assert mock_lsf.call_count == 3, \
        "For a multi job this method should only be called more than once"


@mock.patch('longbow.schedulers.slurm.submit')
@mock.patch('longbow.schedulers.pbs.submit')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_multiplediff(mock_isdir, mock_lsf, mock_pbs, mock_slurm):

    """
    Test that for multiple jobs the correct number of submission calls happen.
    """

    jobs = {
        "lbowconf": {},
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

    submit(jobs)

    assert mock_lsf.call_count == 1, \
        "For a single job this method should only be called once"
    assert mock_pbs.call_count == 1, \
        "For a single job this method should only be called once"
    assert mock_slurm.call_count == 1, \
        "For a single job this method should only be called once"


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_filewrite(mock_isdir, mock_submit, mock_savini):

    """
    Test that the recovery file write happens if everything is working.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None

    submit(jobs)

    assert mock_savini.call_count == 1


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_fileuninit(mock_isdir, mock_submit, mock_savini):

    """
    Test that if the recovery file is uninitialised that no writing happens.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": ""
        },
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None

    submit(jobs)

    assert mock_savini.call_count == 0


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_fileexcept1(mock_isdir, mock_submit, mock_savini):

    """
    Test that if the recovery file write fails it does so in a controlled way.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None
    mock_savini.side_effect = OSError

    submit(jobs)


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_fileexcept2(mock_isdir, mock_submit, mock_savini):

    """
    Test that if the recovery file write fails it does so in a controlled way.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456",
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None
    mock_savini.side_effect = IOError

    submit(jobs)


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_attrexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that errors with missing plugins are handled correctly.
    """

    jobs = {
        "lbowconf": {},
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

        submit(jobs)


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_submitexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that submission failure errors are handled correctly.
    """

    jobs = {
        "lbowconf": {},
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = exceptions.JobsubmitError("Submit Error")

    submit(jobs)

    assert jobs["job-one"]["laststatus"] == "Submit Error"


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_queueexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that queue limit events are handled correctly if a plugin raises the
    queuemax exception.
    """

    jobs = {
        "lbowconf": {},
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = exceptions.QueuemaxError("Submit Error")

    submit(jobs)

    assert jobs["job-one"]["laststatus"] == "Waiting Submission"


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_queueinfo(mock_isdir, mock_submit, mock_savini):

    """
    Check that the queueinformation counter is getting used.
    """

    jobs = {
        "lbowconf": {
            "test-machine-queue-slots": 0,
            "test-machine-queue-max": 0
        },
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
    mock_savini.return_value = None
    mock_submit.return_value = None

    submit(jobs)

    assert jobs["lbowconf"]["test-machine-queue-slots"] == "3"
    assert jobs["lbowconf"]["test-machine-queue-max"] == "3"
