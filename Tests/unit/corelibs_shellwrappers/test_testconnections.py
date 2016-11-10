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
This testing module contains the tests for the shellwrappers module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.shellwrappers as shellwrappers


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testconnections_single(mock_sendtossh):

    """
    Test that the connection test is launched.
    """

    jobs = {
        "LongbowJob1": {
            "resource": "resource1"
        }
    }

    shellwrappers.testconnections(jobs)

    assert mock_sendtossh.call_count == 1, "sendtossh should be called once"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

    shellwrappers.testconnections(jobs)

    assert mock_sendtossh.call_count == 2, "sendtossh should be called twice"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

        shellwrappers.testconnections(jobs)
