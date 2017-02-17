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
This testing module contains the tests for the testscheduler method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.scheduling import _testscheduler


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testscheduler_detection1(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": "",
        "scheduler": ""
    }

    mock_ssh.return_value = None

    _testscheduler(job)

    assert job["scheduler"] in ["lsf", "pbs", "sge", "soge", "slurm"]


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testscheduler_detection2(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered. Throw in a failure event.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": "",
        "scheduler": ""
    }

    mock_ssh.side_effect = [exceptions.SSHError("SSH Error", "Error"), None]

    _testscheduler(job)

    assert job["scheduler"] in ["lsf", "pbs", "sge", "soge", "slurm"]


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testscheduler_except(mock_ssh):

    """
    Test that the correct exception is raised when nothing can be detected.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": "",
        "scheduler": ""
    }

    mock_ssh.side_effect = exceptions.SSHError("SSH Error", "Error")

    with pytest.raises(exceptions.SchedulercheckError):

        _testscheduler(job)
