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

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.scheduling import monitor, QUEUEINFO


def jobstatus(jobs, _):

    """
    Change status of the job
    """

    for job in jobs:

        if jobs[job]["laststatus"] == "Queued":

            jobs[job]["laststatus"] = "Running"

        if jobs[job]["laststatus"] == "Running":

            jobs[job]["laststatus"] = "Finished"


@mock.patch('longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('longbow.corelibs.scheduling._polljobs')
@mock.patch('longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_testpollfrequency(mock_init, mock_poll, mock_wait):

    """
    Test that the polling frequency is working.
    """

    import time

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        }
    }
    QUEUEINFO["hpc1"] = {}
    QUEUEINFO["hpc1"]["queue-slots"] = "1"
    QUEUEINFO["hpc1"]["queue-max"] = "2"

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


@mock.patch('longbow.corelibs.scheduling._stagejobfiles')
@mock.patch('longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('longbow.corelibs.scheduling._polljobs')
@mock.patch('longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_teststagefreq(mock_init, mock_poll, mock_wait, mock_down):

    """
    Test that the staging frequency is working
    """

    import time

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        }
    }
    QUEUEINFO["hpc1"] = {}
    QUEUEINFO["hpc1"]["queue-slots"] = "1"
    QUEUEINFO["hpc1"]["queue-max"] = "2"

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


@mock.patch('longbow.corelibs.configuration.saveini')
@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('longbow.corelibs.scheduling._polljobs')
@mock.patch('longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_complete1(mock_init, mock_poll, mock_wait, mock_down,
                           mock_save):

    """
    Test that when all jobs complete the method exits.
    """

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Finished",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        }
    }

    QUEUEINFO["hpc1"] = {}
    QUEUEINFO["hpc1"]["queue-slots"] = "1"
    QUEUEINFO["hpc1"]["queue-max"] = "2"

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


@mock.patch('longbow.corelibs.configuration.saveini')
@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('longbow.corelibs.scheduling._polljobs')
@mock.patch('longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_complete2(mock_init, mock_poll, mock_wait, mock_down,
                           mock_save):

    """
    Test that when all jobs complete the method exits.
    """

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Finished",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobfour": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobfive": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        }
    }

    QUEUEINFO["hpc1"] = {}
    QUEUEINFO["hpc1"]["queue-slots"] = "1"
    QUEUEINFO["hpc1"]["queue-max"] = "2"

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


@mock.patch('longbow.corelibs.configuration.saveini')
@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('longbow.corelibs.scheduling._polljobs')
@mock.patch('longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_run1(mock_init, mock_poll, mock_wait, mock_down,
                      mock_save):

    """
    Test that when all jobs complete the method exits.
    """

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobfour": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobfive": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        }
    }

    QUEUEINFO["hpc1"] = {}
    QUEUEINFO["hpc1"]["queue-slots"] = "1"
    QUEUEINFO["hpc1"]["queue-max"] = "2"

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


@mock.patch('longbow.corelibs.configuration.saveini')
@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('longbow.corelibs.scheduling._polljobs')
@mock.patch('longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_except(mock_init, mock_poll, mock_wait, mock_down,
                        mock_save):

    """
    Check that if an exception is thrown on the save recovery file, that
    it does not bring the whole application down.
    """

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Finished",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error",
            "recoveryfile": "recovery-YYMMDD-HHMMSS"
        }
    }
    QUEUEINFO["hpc1"] = {}
    QUEUEINFO["hpc1"]["queue-slots"] = "1"
    QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_down.return_value = None
    mock_save.side_effect = IOError
    mock_wait.return_value = False

    monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert mock_save.call_count == 1
