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
This testing module contains the tests for the testconnections method within
the shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.shellwrappers import checkconnections


def sshfunc(job, cmd):
    """Function to mock the throwing of exception for a test."""

    if cmd[0] == "module avail" and job["resource"] == "resource1":

        raise exceptions.SSHError(
            "Err", ("", "bash: module: command not found", 0))


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testconnections_single(mock_sendtossh):

    """
    Test that the connection test is launched.
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1"
        }
    }

    checkconnections(jobs)

    assert mock_sendtossh.call_count == 2, "sendtossh should be called twice"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testconnections_multiple(mock_sendtossh):

    """
    Test that the connection test is run only for each host once.
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1"
        },
        "LongbowJob2": {
            "resource": "resource2"
        },
        "LongbowJob3": {
            "resource": "resource1"
        }
    }

    checkconnections(jobs)

    assert mock_sendtossh.call_count == 4, "should be called four times"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testconnections_sshexcept(mock_sendtossh):

    """
    Test to see that if the underlying SSH call fails, the resulting
    SSHError is passed up the chain. This is important!
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1"
        },
        "LongbowJob2": {
            "resource": "resource2"
        },
        "LongbowJob3": {
            "resource": "resource1"
        }
    }

    mock_sendtossh.side_effect = exceptions.SSHError("SSH Error", "output")

    with pytest.raises(exceptions.SSHError):

        checkconnections(jobs)


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testconnections_envfix(mock_sendtossh):

    """
    Test that the environment checking works.
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1",
            "env-fix": "false"
        },
        "LongbowJob2": {
            "resource": "resource2",
            "env-fix": "false"
        },
        "LongbowJob3": {
            "resource": "resource1",
            "env-fix": "false"
        }
    }

    mock_sendtossh.side_effect = sshfunc

    checkconnections(jobs)

    assert jobs["LongbowJob1"]["env-fix"] == "true"
    assert jobs["LongbowJob2"]["env-fix"] == "false"
    assert jobs["LongbowJob3"]["env-fix"] == "true"
