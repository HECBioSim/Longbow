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

import Longbow.corelibs.scheduling as scheduling


def changescheduler(job):

    """
    Change the scheduler when call to mocked function is made.
    """

    if job["resource"] == "test-machine":

        job["scheduler"] = "lsf"

    else:

        job["scheduler"] = "pbs"


def changehandler(job):

    """
    Change the handler when call to mocked function is made.
    """

    if job["resource"] == "test-machine":

        job["handler"] = "mpiexec"

    else:

        job["handler"] = "aprun"


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testhandler')
@mock.patch('Longbow.corelibs.scheduling._testscheduler')
def test_testenv_single(mock_sched, mock_hand, mock_save):

    """
    Test that a single job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "test",
            "handler": "test",
        }
    }

    hostconf = "/path/to/configfile"

    scheduling.testenv(jobs, hostconf)

    assert mock_sched.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_hand.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_save.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testhandler')
@mock.patch('Longbow.corelibs.scheduling._testscheduler')
def test_testenv_multi(mock_sched, mock_hand, mock_save):

    """
    Test that a multi job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "test",
            "handler": "test",
        },
        "jobtwo": {
            "resource": "test-machine",
            "scheduler": "test",
            "handler": "test",
        },
        "jobthree": {
            "resource": "test-machine2",
            "scheduler": "test",
            "handler": "test",
        }
    }

    hostconf = "/path/to/configfile"

    scheduling.testenv(jobs, hostconf)

    assert mock_sched.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_hand.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_save.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testscheduler')
def test_testenv_scheduler(mock_sched, mock_save):

    """
    Test that a multi job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "",
            "handler": "test"
        },
        "jobtwo": {
            "resource": "test-machine",
            "scheduler": "",
            "handler": "test"
        },
        "jobthree": {
            "resource": "test-machine2",
            "scheduler": "",
            "handler": "test"
        }
    }

    hostconf = "/path/to/configfile"

    mock_sched.side_effect = changescheduler

    scheduling.testenv(jobs, hostconf)

    assert jobs["jobone"]["scheduler"] == "lsf"
    assert jobs["jobtwo"]["scheduler"] == "lsf"
    assert jobs["jobthree"]["scheduler"] == "pbs"
    assert mock_sched.call_count == 2
    assert mock_save.call_count == 1


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testhandler')
def test_testenv_handler(mock_hand, mock_save):

    """
    Test that a multi job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "lsf",
            "handler": ""
        },
        "jobtwo": {
            "resource": "test-machine",
            "scheduler": "lsf",
            "handler": ""
        },
        "jobthree": {
            "resource": "test-machine2",
            "scheduler": "pbs",
            "handler": ""
        }
    }

    hostconf = "/path/to/configfile"

    mock_hand.side_effect = changehandler

    scheduling.testenv(jobs, hostconf)

    assert jobs["jobone"]["handler"] == "mpiexec"
    assert jobs["jobtwo"]["handler"] == "mpiexec"
    assert jobs["jobthree"]["handler"] == "aprun"
    assert mock_hand.call_count == 2
    assert mock_save.call_count == 1
