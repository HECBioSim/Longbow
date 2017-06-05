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
This test module contains tests for the PBS scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.schedulers.lsf import status

out = ("953580  scarf45 DONE  scarf      scarf.rl.ac             3t3b_sym   Feb 26 13:26\n"
       "953601  scarf45 EXIT  scarf      scarf.rl.ac             3t3b_asym  Feb 26 13:27\n"
       "953631  scarf45 PEND  scarf      scarf.rl.ac             4t1m1b     Feb 26 13:52\n"
       "953710  scarf45 PSUSP scarf      scarf.rl.ac             1t1m4b     Feb 26 14:30\n"
       "953711  scarf45 RUN   scarf      scarf.rl.ac             1t2m3b     Feb 26 14:32\n"
       "953712  scarf45 SSUSP scarf      scarf.rl.ac             1t3m2b     Feb 26 14:34\n"
       "953713  scarf45 UNKWN scarf      scarf.rl.ac             2m4b       Feb 26 14:35\n"
       "953715  scarf45 USUSP scarf      scarf.rl.ac             2t1m3b     Feb 26 14:37\n"
       "953716  scarf45 WAIT  scarf      scarf.rl.ac             2t3m1b     Feb 26 14:39\n"
       "953717  scarf45 ZOMBI scarf      scarf.rl.ac             2t4b       Feb 26 14:40\n")


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state1(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953580"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Job Exited Properly"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state2(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953601"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Job Exited in Error"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state3(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953631"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Queued"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state4(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953710"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Suspended"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state5(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953711"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Running"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state6(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953712"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Suspended"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state7(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953713"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Unknown Status"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state8(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953715"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Suspended"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state9(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953716"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == ("Waiting for Start Time")


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state10(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "953717"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Zombie Job"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state11(mock_ssh):

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


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
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
