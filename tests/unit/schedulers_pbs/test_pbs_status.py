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
This test module contains tests for the PBS scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.schedulers.pbs import status

out = ("Job ID          Username Queue    Jobname    SessID NDS TSK Memory Time  S Time \n"
       "--------------- -------- -------- ---------- ------ --- --- ------ ----- - -----\n"
       "3530460.sdb     katrine  long     Uio67         --    8 192    --  48:00 B   -- \n"
       "3530473.sdb     katrine  long     IRM10         --    8 192    --  48:00 E   -- \n"
       "3537896.sdb     katrine  standard BiPip         --    8 192    --  01:00 H   -- \n"
       "3537971.sdb     katrine  standard Pol-test      --    8 192    --  00:10 M   -- \n"
       "3537972.sdb     katrine  standard Pol-test      --    8 192    --  00:10 Q   -- \n"
       "3537974.sdb     katrine  standard Pol-test      --    8 192    --  00:10 R   -- \n"
       "3538328.sdb     katrine  standard Pol-test      --    8 192    --  00:10 S   -- \n"
       "3538333.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 T   -- \n"
       "3538337.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 U   -- \n"
       "3538340.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 W   -- \n"
       "3538341.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 X   -- \n")


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state1(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3530460"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Subjob(s) Running"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state2(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3530473"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Exiting"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state3(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537896"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Held"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state4(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537971"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Job Moved to Server"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state5(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537972"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Queued"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state6(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537974"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Running"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state7(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538328"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Suspended"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state8(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538333"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Job Moved to New Location"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state9(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538337"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == ("Cycle-Harvesting Job is Suspended Due to Keyboard "
                      "Activity")


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state10(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538340"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Waiting for Start Time"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_status_state11(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538341"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Subjob Completed Execution/Has Been Deleted"


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
