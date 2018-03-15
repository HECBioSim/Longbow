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
This testing module contains the tests for the testenv method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.scheduling import checkenv


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


@mock.patch('longbow.configuration.saveconfigs')
@mock.patch('longbow.scheduling._testhandler')
@mock.patch('longbow.scheduling._testscheduler')
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

    checkenv(jobs, hostconf)

    assert mock_sched.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_hand.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_save.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"


@mock.patch('longbow.configuration.saveconfigs')
@mock.patch('longbow.scheduling._testhandler')
@mock.patch('longbow.scheduling._testscheduler')
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

    checkenv(jobs, hostconf)

    assert mock_sched.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_hand.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_save.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"


@mock.patch('longbow.configuration.saveconfigs')
@mock.patch('longbow.scheduling._testscheduler')
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

    checkenv(jobs, hostconf)

    assert jobs["jobone"]["scheduler"] == "lsf"
    assert jobs["jobtwo"]["scheduler"] == "lsf"
    assert jobs["jobthree"]["scheduler"] == "pbs"
    assert mock_sched.call_count == 2
    assert mock_save.call_count == 1


@mock.patch('longbow.configuration.saveconfigs')
@mock.patch('longbow.scheduling._testhandler')
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

    checkenv(jobs, hostconf)

    assert jobs["jobone"]["handler"] == "mpiexec"
    assert jobs["jobtwo"]["handler"] == "mpiexec"
    assert jobs["jobthree"]["handler"] == "aprun"
    assert mock_hand.call_count == 2
    assert mock_save.call_count == 1
