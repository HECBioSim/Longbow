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
This test module contains tests for the SGE scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.schedulers.sge import status

out = ("job-ID  prior name       user         state submit/start at     queue      master  ja-task-ID\n"
       "---------------------------------------------------------------------------------------------\n"
       "     20     0 sleep.sh   sysadm1      qw     12/23/2003 23:22:09 frontend-0 MASTER           \n"
       "     21     0 sleep.sh   sysadm1      h      12/23/2003 23:22:09 frontend-0 MASTER           \n"
       "     22     0 sleep.sh   sysadm1      r      12/23/2003 23:22:09 frontend-0 MASTER           \n")


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state1(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "20"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Queued"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state2(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "21"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Held"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state3(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "22"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Running"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state4(mock_ssh):

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
