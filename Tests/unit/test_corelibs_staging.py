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

# ---------------------------------------------------------------------------#
# Tests for stage_upstream()


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

# ---------------------------------------------------------------------------#
# Tests for stage_downstream()


@mock.patch('Longbow.corelibs.shellwrappers.download')
def test_stage_downstream_except(mock_download):

    """
    Test if staging exception is correctly raised if rsync exception happens.
    """

    job = {
        "jobname": "jobone",
        "destdir": "/path/to/jobone12484",
        "localworkdir": "/path/to/local/dir"
    }

    mock_download.side_effect = exceptions.RsyncError("Rsync Error", "output")

    with pytest.raises(exceptions.StagingError):

        staging.stage_downstream(job)


@mock.patch('Longbow.corelibs.shellwrappers.download')
def test_stage_downstream_params(mock_download):

    """
    Test that a dict actually makes it to the download method.
    """

    job = {
        "jobname": "jobone",
        "destdir": "/path/to/jobone12484",
        "localworkdir": "/path/to/local/dir"
    }

    staging.stage_downstream(job)

    downloadarg1 = mock_download.call_args[0][0]

    assert isinstance(downloadarg1, dict)

# ---------------------------------------------------------------------------#
# Tests for cleanup()


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_single(mock_delete, mock_list):

    """
    Test that the correct number of function calls are made.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    staging.cleanup(jobs)

    assert mock_delete.call_count == 1, \
        "There is only one job, this should only be called once"
    assert mock_list.call_count == 1, \
        "There is only one job, this should only be called once"


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_multiple(mock_delete, mock_list):

    """
    Test that the correct number of function calls are made.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            },
        "jobtwo": {
            "destdir": "/path/to/jobtwo12484",
            "remoteworkdir": "/path/to/local/dir"
            },
        "jobthree": {
            "destdir": "/path/to/jobthree12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    staging.cleanup(jobs)

    assert mock_delete.call_count == 3, \
        "There is only one job, this should only be called once"
    assert mock_list.call_count == 3, \
        "There is only one job, this should only be called once"


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_params(mock_delete, mock_list):

    """
    Test the correct arguments make it to the method calls.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    staging.cleanup(jobs)

    listarg1 = mock_list.call_args[0][0]
    deletearg1 = mock_delete.call_args[0][0]

    assert isinstance(listarg1, dict)
    assert isinstance(deletearg1, dict)


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_nodelete(mock_delete, mock_list):

    """
    Test that the following exception is handled correctly.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/jobone12484"
            }
    }

    mock_list.return_value = None
    mock_delete.return_value = None

    staging.cleanup(jobs)

    assert mock_delete.call_count == 0, "Should not be called in this case."


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest1(mock_delete, mock_list):

    """
    Test that the listerror exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = exceptions.RemotelistError("List Error", "blah")

    staging.cleanup(jobs)


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest2(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = KeyError("blah")

    staging.cleanup(jobs)


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest3(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.side_effect = exceptions.RemotedeleteError("Error", "blah")
    mock_list.return_value = None

    staging.cleanup(jobs)


@mock.patch('Longbow.corelibs.shellwrappers.remotelist')
@mock.patch('Longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest4(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = NameError("blah")

    staging.cleanup(jobs)
