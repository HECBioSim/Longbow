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
This testing module contains the tests for the sendtorsync method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import sendtorsync


@mock.patch('time.sleep')
@mock.patch('longbow.shellwrappers.sendtoshell')
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

        sendtorsync(job, "src", "dst", "", "")

    assert mock_sendtoshell.call_count == 3, "This method should retry 3 times"


@mock.patch('longbow.shellwrappers.sendtoshell')
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

    sendtorsync(job, "src", "dst", "", "")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = "rsync -azP -e ssh -p 22 src dst"

    assert " ".join(callargs) == testargs


@mock.patch('longbow.shellwrappers.sendtoshell')
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

    sendtorsync(job, "src", "dst", "", "exfile")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = "rsync -azP --exclude exfile -e ssh -p 22 src dst"

    assert " ".join(callargs) == testargs


@mock.patch('longbow.shellwrappers.sendtoshell')
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

    sendtorsync(job, "src", "dst", "", "exfile1, exfile2")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = ("rsync -azP --exclude exfile1 --exclude exfile2 -e ssh -p 22 "
                "src dst")

    assert " ".join(callargs) == testargs


@mock.patch('longbow.shellwrappers.sendtoshell')
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

    sendtorsync(job, "src", "dst", "incfile", "exfile1, exfile2")

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = ("rsync -azP --include incfile --exclude exfile1 --exclude "
                "exfile2 -e ssh -p 22 src dst")

    assert " ".join(callargs) == testargs
