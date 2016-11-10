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
This testing module contains the tests for the staging module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.staging as staging


@mock.patch('Longbow.corelibs.shellwrappers.upload')
@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

    staging.stage_upstream(jobs)

    assert mock_ssh.call_count == 1, \
        "There is only one job, this should only be called once"
    assert mock_upload.call_count == 1, \
        "There is only one job, this should only be called once"


@mock.patch('Longbow.corelibs.shellwrappers.upload')
@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

    staging.stage_upstream(jobs)

    assert mock_ssh.call_count == 4, \
        "There is only one job, this should only be called once"
    assert mock_upload.call_count == 4, \
        "There is only one job, this should only be called once"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

        staging.stage_upstream(jobs)


@mock.patch('Longbow.corelibs.shellwrappers.upload')
@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

        staging.stage_upstream(jobs)


@mock.patch('Longbow.corelibs.shellwrappers.upload')
@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

    staging.stage_upstream(jobs)

    uploadarg1 = mock_upload.call_args[0][0]
    ssharg1 = mock_ssh.call_args[0][0]
    ssharg2 = mock_ssh.call_args[0][1]

    assert isinstance(uploadarg1, dict)
    assert isinstance(ssharg1, dict)
    assert isinstance(ssharg2, list)
    assert ssharg2[0] == "mkdir -p /path/to/jobone12484\n"
