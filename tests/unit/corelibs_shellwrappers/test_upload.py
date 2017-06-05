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
This testing module contains the tests for the upload method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.shellwrappers import upload


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

        upload(job)


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

        upload(job)


@mock.patch('longbow.corelibs.shellwrappers.sendtorsync')
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

    upload(job)

    callargs = mock_sendtorsync.call_args[0][1]

    assert callargs.endswith("/")


@mock.patch('longbow.corelibs.shellwrappers.sendtorsync')
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

    upload(job)

    callargs = mock_sendtorsync.call_args[0][2]
    testargs = job["user"] + "@" + job["host"] + ":" + job["destdir"]

    assert callargs == testargs


@mock.patch('longbow.corelibs.shellwrappers.sendtorsync')
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

        upload(job)
