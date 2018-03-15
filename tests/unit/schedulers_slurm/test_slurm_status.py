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
This test module contains tests for the slurm scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.schedulers.slurm import status

out = ("             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)\n"
       "               600 interacti  run2.sh     user CA       0:19      1 blade01)\n"
       "               601 interacti  run2.sh     user CD       0:19      1 blade01)\n"
       "               602 interacti  run2.sh     user CF       0:19      1 blade01)\n"
       "               603 interacti  run2.sh     user CG       0:19      1 blade01)\n"
       "               604 interacti  run2.sh     user F        0:19      1 blade01)\n"
       "               605 interacti  run2.sh     user NF       0:19      1 blade01)\n"
       "               606 interacti  run2.sh     user PD       0:19      1 blade01)\n"
       "               607 interacti  run2.sh     user PR       0:19      1 blade01)\n"
       "               608 interacti  run2.sh     user R        0:19      1 blade01)\n"
       "               609 interacti  run2.sh     user S        0:19      1 blade01)\n"
       "               610 interacti  run2.sh     user TO       0:19      1 blade01)\n")


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state1(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "600"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Cancelled"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state2(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "601"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Completed"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state3(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "602"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Configuring"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state4(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "603"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Completing"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state5(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "604"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Failed"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state6(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "605"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Node Failure"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state7(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "606"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Pending"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state8(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "607"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Preempted"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state9(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "608"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == ("Running")


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state10(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "609"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Suspended"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state11(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "610"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Timed out"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state12(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538341"
    }

    mock_ssh.return_value = ("", "", 0)

    output = status(job)

    assert output == "Finished"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_except1(mock_ssh):

    """
    Test if SSH Error is handled.
    """

    job = {
        "user": "test",
        "jobid": ""
    }

    mock_ssh.side_effect = exceptions.SSHError("OUT", "ERR")

    with pytest.raises(exceptions.SSHError):

        status(job)
