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
This test module contains tests for the LSF scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.schedulers.lsf import submit


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_submit_jobid1(mock_ssh):

    """
    Test if job id can be grabbed.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.return_value = ("Job 2685 is submitted to default queue "
                             "[regular].", "", 0)

    submit(job)

    assert job["jobid"] == "2685"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_submit_jobid2(mock_ssh):

    """
    Test if Jobsubmit exception is triggered if job id can't be grabbed.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.return_value = ("success", "", 0)

    with pytest.raises(exceptions.JobsubmitError):

        submit(job)


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_submit_except1(mock_ssh):

    """
    Test if Queuemax exception is triggered based on output from scheduler.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.side_effect = exceptions.SSHError(
        "Error", ("out", "limit", 0))
    mock_ssh.return_value = ("success", "Error", 0)

    with pytest.raises(exceptions.QueuemaxError):

        submit(job)


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_submit_except2(mock_ssh):

    """
    Check that jobsubmit exception is raised on generic SSH failure.
    """

    job = {
        "destdir": "/path/to/destdir",
        "subfile": "submit.file"
    }

    mock_ssh.side_effect = exceptions.SSHError("Error", ("out", "err", 0))
    mock_ssh.return_value = ("success", "error", 0)

    with pytest.raises(exceptions.JobsubmitError):

        submit(job)
