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
This testing module contains the tests for the stage_upstream method within
the staging module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.staging import stage_upstream


@mock.patch('longbow.shellwrappers.upload')
@mock.patch('longbow.shellwrappers.sendtossh')
def test_stage_upstream_singlejob(mock_ssh, mock_upload):

    """
    Test if a single call is made to SSH and rsync. Multiples here are bad.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "resource": "test-machine"
            }
    }

    stage_upstream(jobs)

    assert mock_ssh.call_count == 1, \
        "There is only one job, this should only be called once"
    assert mock_upload.call_count == 1, \
        "There is only one job, this should only be called once"


@mock.patch('longbow.shellwrappers.upload')
@mock.patch('longbow.shellwrappers.sendtossh')
def test_stage_upstream_multijobs(mock_ssh, mock_upload):

    """
    Test if multiple calls are made to SSH and rsync.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "resource": "test-machine"
            },
        "jobtwo": {
            "destdir": "/path/to/jobtwo12484",
            "resource": "test-machine"
            },
        "jobthree": {
            "destdir": "/path/to/jobthree12484",
            "resource": "test-machine"
            },
        "jobfour": {
            "destdir": "/path/to/jobfour12484",
            "resource": "test-machine"
            }
    }

    stage_upstream(jobs)

    assert mock_ssh.call_count == 4, \
        "There is only one job, this should only be called once"
    assert mock_upload.call_count == 4, \
        "There is only one job, this should only be called once"


@mock.patch('longbow.shellwrappers.sendtossh')
def test_stage_upstream_sshexcept(mock_ssh):

    """
    Test if the SSH exception is raised if passed up from the SSH call.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "resource": "test-machine"
            }
    }

    mock_ssh.side_effect = exceptions.SSHError("SSH Error", "output")

    with pytest.raises(exceptions.SSHError):

        stage_upstream(jobs)


@mock.patch('longbow.shellwrappers.upload')
@mock.patch('longbow.shellwrappers.sendtossh')
def test_stage_upstream_rsyncexcept(mock_ssh, mock_upload):

    """
    Test if staging exception is correctly raised if rsync exception happens.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "resource": "test-machine",
            "localworkdir": "/path/to/local/dir"
            }
    }

    mock_ssh.return_value = None
    mock_upload.side_effect = exceptions.RsyncError("Rsync Error", "output")

    with pytest.raises(exceptions.StagingError):

        stage_upstream(jobs)


@mock.patch('longbow.shellwrappers.upload')
@mock.patch('longbow.shellwrappers.sendtossh')
def test_stage_upstream_params(mock_ssh, mock_upload):

    """
    Test the correct arguments make it to the upload method.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "resource": "test-machine",
            "localworkdir": "/path/to/local/dir"
            }
    }

    stage_upstream(jobs)

    uploadarg1 = mock_upload.call_args[0][0]
    ssharg1 = mock_ssh.call_args[0][0]
    ssharg2 = mock_ssh.call_args[0][1]

    assert isinstance(uploadarg1, dict)
    assert isinstance(ssharg1, dict)
    assert isinstance(ssharg2, list)
    assert ssharg2[0] == "mkdir -p /path/to/jobone12484\n"
