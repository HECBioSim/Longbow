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
This testing module contains the tests for the remotecopy method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.shellwrappers import remotecopy


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

        remotecopy(job, src, dst)


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

        remotecopy(job, src, dst)


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
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

    remotecopy(job, src, dst)

    callargs = mock_sendtossh.call_args[0][1]
    testargs = "cp -r ~/source/directory/path ~/destination/directory/path"

    assert " ".join(callargs) == testargs


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
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

        remotecopy(job, src, dst)
