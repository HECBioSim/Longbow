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

# ---------------------------------------------------------------------------#
# Tests for testconnections()


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

# ---------------------------------------------------------------------------#
# Tests for sendtossh()


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtossh_returncheck(mock_sendtoshell):

    """
    This test will check that the sendtossh method will exit and return the
    raw return values from sendtoshell.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    args = ["ls"]

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    output = shellwrappers.sendtossh(job, args)

    assert output[0] == "Output message", "method is not returning stdout"
    assert output[1] == "Error message", "method is not returning stderr"
    assert output[2] == 0, "method is not returning the error code"


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtossh_errorcode(mock_sendtoshell):

    """
    This test will check that if the error code is not 0 or 255 that the
    SSHError exception is raised.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    args = ["ls"]

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 1

    with pytest.raises(exceptions.SSHError):

        shellwrappers.sendtossh(job, args)


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtossh_formattest(mock_sendtoshell):

    """
    Testing the format of the rsync call sent to the shell. This test
    will check that calls without masks get formed correctly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    shellwrappers.sendtossh(job, ["ls"])

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = "ssh -p 22 juan_trique-ponee@massive-machine ls"

    assert " ".join(callargs) == testargs


@mock.patch('time.sleep')
@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtossh_retries(mock_sendtoshell, mock_time):

    """
    This test will check that if an error code of 255 is raised, that the
    retries happen and that eventually upon failure that the SSHError
    exception is raised.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    args = ["ls"]

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 255

    # Set the timout for retries to 0 seconds to speed up test.
    mock_time.return_value = None

    with pytest.raises(exceptions.SSHError):

        shellwrappers.sendtossh(job, args)

    assert mock_sendtoshell.call_count == 3, "This method should retry 3 times"

# ---------------------------------------------------------------------------#
# Tests for sendtorsync()


@mock.patch('time.sleep')
@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtorsync_retries(mock_sendtoshell, mock_time):

    """
    Test that the rsync method will try three times if rsync fails before
    finally raising the RsyncError exception.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 1

    # Set the timout for retries to 0 seconds to speed up test.
    mock_time.return_value = None

    with pytest.raises(exceptions.RsyncError):

        shellwrappers.sendtorsync(job, "src", "dst", "", "")

    assert mock_sendtoshell.call_count == 3, "This method should retry 3 times"


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtorsync_rsyncformat1(mock_sendtoshell):

    """
    Testing the format of the rsync call sent to the shell. This test
    will check that calls without masks get formed correctly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    shellwrappers.sendtorsync(job, "src", "dst", "", "")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = "rsync -azP -e ssh -p 22 src dst"

    assert " ".join(callargs) == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtorsync_rsyncformat2(mock_sendtoshell):

    """
    Testing the format of the rsync call sent to the shell. This test will
    check that calls with just exclude masks get formed correctly for a single
    excluded file.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    shellwrappers.sendtorsync(job, "src", "dst", "", "exfile")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = "rsync -azP --exclude exfile -e ssh -p 22 src dst"

    assert " ".join(callargs) == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtorsync_rsyncformat3(mock_sendtoshell):

    """
    Testing the format of the rsync call sent to the shell. This test will
    check that calls with just exclude masks get formed correctly for multiple
    excluded files.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    shellwrappers.sendtorsync(job, "src", "dst", "", "exfile1, exfile2")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = ("rsync -azP --exclude exfile1 --exclude exfile2 -e ssh -p 22 "
                "src dst")

    assert " ".join(callargs) == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_sendtorsync_rsyncformat4(mock_sendtoshell):

    """
    Testing the format of the rsync call sent to the shell. This test will
    check that calls with file masks get formed correctly for multiple excluded
    files.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    # Set the return values of sendtoshell.
    mock_sendtoshell.return_value = "Output message", "Error message", 0

    shellwrappers.sendtorsync(job, "src", "dst", "incfile", "exfile1, exfile2")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = ("rsync -azP --include incfile --exclude exfile1 --exclude "
                "exfile2 -e ssh -p 22 src dst")

    assert " ".join(callargs) == testargs

# ---------------------------------------------------------------------------#
# Tests for localcopy()


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_localcopy_(mock_sendtoshell):

    """
    docstring
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    return

# ---------------------------------------------------------------------------#
# Tests for localdelete()


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_localdelete_(mock_sendtoshell):

    """
    docstring
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    return

# ---------------------------------------------------------------------------#
# Tests for locallist()


@mock.patch('Longbow.corelibs.shellwrappers.sendtoshell')
def test_locallist_(mock_sendtoshell):

    """
    docstring
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    return

# ---------------------------------------------------------------------------#
# Tests for remotecopy()


def test_remotecopy_srcpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    src = "source/directory/path"

    dst = "~/source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.remotecopy(job, src, dst)


def test_remotecopy_dstpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine"
    }

    src = "~/source/directory/path"

    dst = "source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.remotecopy(job, src, dst)


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_remotecopy_formattest(mock_sendtossh):

    """
    Check that the format of the ls command is constructed correctly when sent
    to the SSH method.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
    }

    src = "~/source/directory/path"

    dst = "~/destination/directory/path"

    shellwrappers.remotecopy(job, src, dst)

    callargs = mock_sendtossh.call_args[0][1]
    testargs = "cp -r ~/source/directory/path ~/destination/directory/path"

    assert " ".join(callargs) == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_remotecopy_exceptiontest(mock_sendtossh):

    """
    Check that the SSH exception is percolated properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
    }

    src = "~/source/directory/path"

    dst = "~/destination/directory/path"

    mock_sendtossh.side_effect = exceptions.SSHError("SSHError", "Error")

    with pytest.raises(exceptions.RemotecopyError):

        shellwrappers.remotecopy(job, src, dst)

# ---------------------------------------------------------------------------#
# Tests for remotedelete()


def test_remotedelete_srcpath():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "source/directory/path"
    }

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.remotedelete(job)


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_remotedelete_formattest(mock_sendtossh):

    """
    Check that the format of the ls command is constructed correctly when sent
    to the SSH method.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    shellwrappers.remotedelete(job)

    callargs = mock_sendtossh.call_args[0][1]
    testargs = "rm -r ~/source/directory/path"

    assert " ".join(callargs) == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_remotedelete_exceptiontest(mock_sendtossh):

    """
    Check that the SSH exception is percolated properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    mock_sendtossh.side_effect = exceptions.SSHError("SSHError", "Error")

    with pytest.raises(exceptions.RemotedeleteError):

        shellwrappers.remotedelete(job)

# ---------------------------------------------------------------------------#
# Tests for remotelist()


def test_remotelist_srcpath():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "source/directory/path"
    }

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.remotelist(job)


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_remotelist_returncheck(mock_sendtossh):

    """
    Check that the output from the shell is deconstructed into a list properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    mock_sendtossh.return_value = "Directory1\nfile1\nfile2", "", ""

    filelist = shellwrappers.remotelist(job)

    assert filelist[0] == "Directory1"
    assert filelist[1] == "file1"
    assert filelist[2] == "file2"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_remotelist_formattest(mock_sendtossh):

    """
    Check that the format of the ls command is constructed correctly when sent
    to the SSH method.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    shellwrappers.remotelist(job)

    callargs = mock_sendtossh.call_args[0][1]
    testargs = "ls ~/source/directory/path"

    assert " ".join(callargs) == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_remotelist_exceptiontest(mock_sendtossh):

    """
    Check that the SSH exception is percolated properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/source/directory/path"
    }

    mock_sendtossh.side_effect = exceptions.SSHError("SSHError", "Error")

    with pytest.raises(exceptions.RemotelistError):

        shellwrappers.remotelist(job)

# ---------------------------------------------------------------------------#
# Tests for upload()


def test_upload_srcpath():

    """
    Test that the absolutepatherror exception is raised for non absolute
    source path.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "localworkdir": "source/directory/path"
    }

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.upload(job)


def test_upload_dstpath():

    """
    Test that the absolutepatherror exception is raised for non absolute
    destination path.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "localworkdir": "~/destination/directory/path",
        "destdir": "destination/directory/path"
    }

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.upload(job)


@mock.patch('Longbow.corelibs.shellwrappers.sendtorsync')
def test_upload_pathslash(mock_sendtorsync):

    """
    Check that the source path has a slash appended to it if there isn't one
    at the end.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/destination/directory/path",
        "localworkdir": "/destination/directory/path",
        "upload-include": "",
        "upload-exclude": ""
    }

    shellwrappers.upload(job)

    callargs = mock_sendtorsync.call_args[0][1]

    assert callargs.endswith("/")


@mock.patch('Longbow.corelibs.shellwrappers.sendtorsync')
def test_upload_pathformat(mock_sendtorsync):

    """
    Check that the remote path is constructed properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/destination/directory/path",
        "localworkdir": "/destination/directory/path",
        "upload-include": "",
        "upload-exclude": ""
    }

    shellwrappers.upload(job)

    callargs = mock_sendtorsync.call_args[0][2]
    testargs = job["user"] + "@" + job["host"] + ":" + job["destdir"]

    assert callargs == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtorsync')
def test_upload_exceptiontest(mock_sendtorsync):

    """
    Check that if the rsync method raises the rsync exception that it
    percolates up.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/destination/directory/path",
        "localworkdir": "/destination/directory/path",
        "upload-include": "",
        "upload-exclude": ""
    }

    mock_sendtorsync.side_effect = exceptions.RsyncError("RsyncError", "Error")

    with pytest.raises(exceptions.RsyncError):

        shellwrappers.upload(job)

# ---------------------------------------------------------------------------#
# Tests for download()


def test_download_srcpath():

    """
    Test that the absolutepatherror exception is raised for non absolute
    source path.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "source/directory/path"
    }

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.download(job)


def test_download_dstpath():

    """
    Test that the absolutepatherror exception is raised for non absolute
    destination path.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/destination/directory/path",
        "localworkdir": "destination/directory/path"
    }

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.download(job)


@mock.patch('Longbow.corelibs.shellwrappers.sendtorsync')
def test_download_pathslash(mock_sendtorsync):

    """
    Check that the source path has a slash appended to it if there isn't one
    at the end.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/destination/directory/path",
        "localworkdir": "/destination/directory/path",
        "download-include": "",
        "download-exclude": ""
    }

    shellwrappers.download(job)

    callargs = mock_sendtorsync.call_args[0][1]

    assert callargs.endswith("/")


@mock.patch('Longbow.corelibs.shellwrappers.sendtorsync')
def test_download_pathformat(mock_sendtorsync):

    """
    Check that the remote path is constructed properly.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/destination/directory/path",
        "localworkdir": "/destination/directory/path",
        "download-include": "",
        "download-exclude": ""
    }

    shellwrappers.download(job)

    callargs = mock_sendtorsync.call_args[0][1]
    testargs = job["user"] + "@" + job["host"] + ":" + job["destdir"]

    assert callargs == testargs


@mock.patch('Longbow.corelibs.shellwrappers.sendtorsync')
def test_download_exceptiontest(mock_sendtorsync):

    """
    Check that if the rsync method raises the rsync exception that it
    percolates up.
    """

    job = {
        "port": "22",
        "user": "juan_trique-ponee",
        "host": "massive-machine",
        "destdir": "~/destination/directory/path",
        "localworkdir": "/destination/directory/path",
        "download-include": "",
        "download-exclude": ""
    }

    mock_sendtorsync.side_effect = exceptions.RsyncError("RsyncError", "Error")

    with pytest.raises(exceptions.RsyncError):

        shellwrappers.download(job)
