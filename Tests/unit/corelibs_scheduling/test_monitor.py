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


def jobstatus(jobs, _):

    """
    Change status of the job
    """

    for job in jobs:

        if jobs[job]["laststatus"] == "Queued":

            jobs[job]["laststatus"] = "Running"

        if jobs[job]["laststatus"] == "Running":

            jobs[job]["laststatus"] = "Finished"


@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
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
            "laststatus": "Running"
        }
    }
    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = 0, 2
    mock_poll.return_value = False
    mock_wait.return_value = False
    mock_poll.side_effect = [None, exceptions.PluginattributeError]

    start = time.time()

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.monitor(jobs)

    end = time.time()

    assert mock_poll.call_count == 2
    assert int(end - start) > 1


@mock.patch('Longbow.corelibs.scheduling._stagejobfiles')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
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
            "laststatus": "Running"
        }
    }
    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = 1, 1
    mock_poll.return_value = False
    mock_down.return_value = False
    mock_wait.return_value = False
    mock_down.side_effect = [None, None, exceptions.PluginattributeError]

    start = time.time()

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.monitor(jobs)

    end = time.time()

    assert mock_poll.call_count == 3
    assert mock_down.call_count == 3
    assert int(end - start) > 2


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.corelibs.staging.stage_downstream')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
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
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error"
        }
    }

    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_wait.return_value = False
    mock_down.return_value = None
    mock_save.return_value = None

    scheduling.monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"
    assert mock_down.call_count == 1


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.corelibs.staging.stage_downstream')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
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
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error"
        },
        "jobfour": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued"
        },
        "jobfive": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running"
        }
    }

    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_poll.side_effect = jobstatus
    mock_wait.return_value = False
    mock_down.return_value = None
    mock_save.return_value = None

    scheduling.monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert mock_down.call_count == 3
    assert mock_save.call_count == 1


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.corelibs.staging.stage_downstream')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
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
            "laststatus": "Running"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued"
        },
        "jobfour": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued"
        },
        "jobfive": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Queued"
        }
    }

    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_poll.side_effect = jobstatus
    mock_wait.return_value = False
    mock_down.return_value = None
    mock_save.return_value = None

    scheduling.monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert mock_down.call_count == 5
    assert mock_save.call_count == 1


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.corelibs.staging.stage_downstream')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
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
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error"
        }
    }
    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = 0, 1
    mock_poll.return_value = False
    mock_down.return_value = None
    mock_save.side_effect = IOError
    mock_wait.return_value = False

    scheduling.monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert mock_save.call_count == 1
