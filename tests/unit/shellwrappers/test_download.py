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
This testing module contains the tests for the download method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import download


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

        download(job)


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

        download(job)


@mock.patch('longbow.shellwrappers.sendtorsync')
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

    download(job)

    callargs = mock_sendtorsync.call_args[0][1]

    assert callargs.endswith("/")


@mock.patch('longbow.shellwrappers.sendtorsync')
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

    download(job)

    callargs = mock_sendtorsync.call_args[0][1]
    testargs = job["user"] + "@" + job["host"] + ":" + job["destdir"]

    assert callargs == testargs


@mock.patch('longbow.shellwrappers.sendtorsync')
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

        download(job)
