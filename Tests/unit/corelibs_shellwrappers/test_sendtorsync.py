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
This testing module contains the tests for the sendtorsync method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.shellwrappers as shellwrappers


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
