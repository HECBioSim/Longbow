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
This testing module contains the tests for the testhandler method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.scheduling import _testhandler


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_detection1(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.return_value = None

    _testhandler(job)

    assert job["handler"] in ["aprun", "mpirun"]


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_detection2(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered. Throw in a failure event.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.side_effect = [exceptions.SSHError("SSH Error", "Error"), None]

    _testhandler(job)

    assert job["handler"] in ["aprun", "mpirun"]


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_except(mock_ssh):

    """
    Test that the correct exception is raised when nothing can be detected.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.side_effect = exceptions.SSHError("SSH Error", "Error")

    with pytest.raises(exceptions.HandlercheckError):

        _testhandler(job)


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_modules1(mock_ssh):

    """
    Test that the module string remains empty after calling this method.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.return_value = None

    _testhandler(job)

    assert job["modules"] == ""


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_modules2(mock_ssh):

    """
    For provided modules, check that they are bring sent to SSH
    """

    job = {
        "modules": "lsf, intel",
        "resource": "test-machine",
        "handler": ""
    }

    _testhandler(job)

    callargs = mock_ssh.call_args[0][1]

    assert 'module load lsf\n' in callargs
    assert 'module load intel\n' in callargs
