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
This testing module contains the tests for the monitor method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.scheduling import monitor


def jobstatus(jobs, _):

    """
    Change status of the job
    """

    for job in [a for a in jobs if "lbowconf" not in a]:

        if jobs[job]["laststatus"] == "Queued":

            jobs[job]["laststatus"] = "Running"

        elif jobs[job]["laststatus"] == "Running":

            jobs[job]["laststatus"] = "Finished"


@mock.patch('longbow.scheduling._checkwaitingjobs')
@mock.patch('longbow.scheduling._polljobs')
@mock.patch('longbow.scheduling._monitorinitialise')
def test_monitor_testpollfrequency(mock_init, mock_poll, mock_wait):

    """
    Test that the polling frequency is working.
    """

    import time

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS",
            "hpc1-queue-slots": 1,
            "hpc1-queue-max": 2
        },
        "jobone": {
            "resource": "hpc1",
            "laststatus": "Running"
        }
    }

    mock_init.return_value = 0, 2
    mock_poll.return_value = False
    mock_wait.return_value = False
    mock_poll.side_effect = [None, exceptions.PluginattributeError]

    start = time.time()

    with pytest.raises(exceptions.PluginattributeError):

        monitor(jobs)

    end = time.time()

    assert mock_poll.call_count == 2
    assert int(end - start) > 1


@mock.patch('longbow.scheduling._stagejobfiles')
@mock.patch('longbow.scheduling._checkwaitingjobs')
@mock.patch('longbow.scheduling._polljobs')
@mock.patch('longbow.scheduling._monitorinitialise')
def test_monitor_teststagefreq(mock_init, mock_poll, mock_wait, mock_down):

    """
    Test that the staging frequency is working
    """

    import time

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS",
            "hpc1-queue-slots": 1,
            "hpc1-queue-max": 2
        },
        "jobone": {
            "resource": "hpc1",
            "laststatus": "Running"
        }
    }

    mock_init.return_value = 1, 1
    mock_poll.return_value = False
    mock_down.return_value = False
    mock_wait.return_value = False
    mock_down.side_effect = [None, None, exceptions.PluginattributeError]

    start = time.time()

    with pytest.raises(exceptions.PluginattributeError):

        monitor(jobs)

    end = time.time()

    assert mock_poll.call_count == 3
    assert mock_down.call_count == 3
    assert int(end - start) > 2


@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling._checkwaitingjobs')
@mock.patch('longbow.scheduling._polljobs')
@mock.patch('longbow.scheduling._monitorinitialise')
def test_monitor_complete1(mock_init, mock_poll, mock_wait, mock_down,
                           mock_save):

    """
    Test that when all jobs complete the method exits.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS",
            "hpc1-queue-slots": 1,
            "hpc1-queue-max": 2
        },
        "jobone": {
            "resource": "hpc1",
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "laststatus": "Submit Error"
        }
    }

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_wait.return_value = False
    mock_down.return_value = None
    mock_save.return_value = None

    monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"
    assert mock_down.call_count == 1


@mock.patch('os.path.isdir', mock.MagicMock(return_value="true"))
@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling._checkwaitingjobs')
@mock.patch('longbow.scheduling._polljobs')
@mock.patch('longbow.scheduling._monitorinitialise')
def test_monitor_complete2(mock_init, mock_poll, mock_wait, mock_down,
                           mock_save):

    """
    Test that when all jobs complete the method exits.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS",
            "hpc1-queue-slots": 1,
            "hpc1-queue-max": 2
        },
        "jobone": {
            "resource": "hpc1",
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "laststatus": "Submit Error"
        },
        "jobfour": {
            "resource": "hpc1",
            "laststatus": "Queued"
        },
        "jobfive": {
            "resource": "hpc1",
            "laststatus": "Running"
        }
    }

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_poll.side_effect = jobstatus
    mock_wait.return_value = False
    mock_down.return_value = None
    mock_save.return_value = None

    monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert mock_down.call_count == 3
    assert mock_save.call_count == 1


@mock.patch('os.path.isdir', mock.MagicMock(return_value="true"))
@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling._checkwaitingjobs')
@mock.patch('longbow.scheduling._polljobs')
@mock.patch('longbow.scheduling._monitorinitialise')
def test_monitor_run1(mock_init, mock_poll, mock_wait, mock_down,
                      mock_save):

    """
    Test that when all jobs complete the method exits.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS",
            "hpc1-queue-slots": 1,
            "hpc1-queue-max": 2
        },
        "jobone": {
            "resource": "hpc1",
            "laststatus": "Running"
        },
        "jobtwo": {
            "resource": "hpc1",
            "laststatus": "Running"
        },
        "jobthree": {
            "resource": "hpc1",
            "laststatus": "Queued"
        },
        "jobfour": {
            "resource": "hpc1",
            "laststatus": "Queued"
        },
        "jobfive": {
            "resource": "hpc1",
            "laststatus": "Queued"
        }
    }

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_poll.side_effect = jobstatus
    mock_wait.return_value = False
    mock_down.return_value = None
    mock_save.return_value = None

    monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert mock_down.call_count == 5
    assert mock_save.call_count == 1


@mock.patch('os.path.isdir', mock.MagicMock(return_value="true"))
@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling._checkwaitingjobs')
@mock.patch('longbow.scheduling._polljobs')
@mock.patch('longbow.scheduling._monitorinitialise')
def test_monitor_except(mock_init, mock_poll, mock_wait, mock_down,
                        mock_save):

    """
    Check that if an exception is thrown on the save recovery file, that
    it does not bring the whole application down.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery-YYMMDD-HHMMSS",
            "hpc1-queue-slots": 1,
            "hpc1-queue-max": 2
        },
        "jobone": {
            "resource": "hpc1",
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "laststatus": "Submit Error"
        }
    }

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_down.return_value = None
    mock_save.side_effect = IOError
    mock_wait.return_value = False

    monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert mock_save.call_count == 1


@mock.patch('os.path.isdir', mock.MagicMock(return_value="true"))
@mock.patch('longbow.configuration.saveini')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling._checkwaitingjobs')
@mock.patch('longbow.scheduling._polljobs')
@mock.patch('longbow.scheduling._monitorinitialise')
def test_monitor_update(mock_init, mock_poll, mock_wait, mock_down, mock_save):

    """
    Test that when all jobs complete the method exits.
    """

    jobs = {
        "lbowconf": {
            "update": True,
            "recoveryfile": "recovery-YYMMDD-HHMMSS",
            "hpc1-queue-slots": 2,
            "hpc1-queue-max": 8
        },
        "jobone": {
            "resource": "hpc1",
            "laststatus": "Running"
        },
        "jobtwo": {
            "resource": "hpc1",
            "laststatus": "Running"
        },
        "jobthree": {
            "resource": "hpc1",
            "laststatus": "Queued"
        },
        "jobfour": {
            "resource": "hpc1",
            "laststatus": "Queued"
        },
        "jobfive": {
            "resource": "hpc1",
            "laststatus": "Queued"
        }
    }

    mock_init.return_value = 0, 1
    mock_poll.return_value = True
    mock_poll.side_effect = jobstatus
    mock_wait.return_value = True

    with pytest.raises(exceptions.UpdateExit):

        monitor(jobs)

    assert jobs["lbowconf"]["update"] is False
    assert jobs["jobone"]["laststatus"] == "Finished"
    assert jobs["jobtwo"]["laststatus"] == "Finished"
    assert jobs["jobthree"]["laststatus"] == "Running"
    assert jobs["jobfour"]["laststatus"] == "Running"
    assert jobs["jobfive"]["laststatus"] == "Running"
    assert mock_poll.call_count == 1
    assert mock_wait.call_count == 1
    assert mock_down.call_count == 0
    assert mock_save.call_count == 1
