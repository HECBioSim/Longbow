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
This testing module contains the tests for the shellwrappers module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.shellwrappers as shellwrappers


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
