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
This testing module contains the tests for the testhandler method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.scheduling import _testhandler


@mock.patch('longbow.shellwrappers.sendtossh')
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


@mock.patch('longbow.shellwrappers.sendtossh')
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


@mock.patch('longbow.shellwrappers.sendtossh')
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


@mock.patch('longbow.shellwrappers.sendtossh')
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


@mock.patch('longbow.shellwrappers.sendtossh')
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
