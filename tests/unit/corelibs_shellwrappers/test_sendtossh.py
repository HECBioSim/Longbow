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
This testing module contains the tests for the sendtossh method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.shellwrappers import sendtossh


@mock.patch('longbow.corelibs.shellwrappers.sendtoshell')
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

    output = sendtossh(job, args)

    assert output[0] == "Output message", "method is not returning stdout"
    assert output[1] == "Error message", "method is not returning stderr"
    assert output[2] == 0, "method is not returning the error code"


@mock.patch('longbow.corelibs.shellwrappers.sendtoshell')
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

        sendtossh(job, args)


@mock.patch('longbow.corelibs.shellwrappers.sendtoshell')
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

    sendtossh(job, ["ls"])

    callargs = mock_sendtoshell.call_args[0][0]
    testargs = "ssh -p 22 juan_trique-ponee@massive-machine ls"

    assert " ".join(callargs) == testargs


@mock.patch('time.sleep')
@mock.patch('longbow.corelibs.shellwrappers.sendtoshell')
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

        sendtossh(job, args)

    assert mock_sendtoshell.call_count == 3, "This method should retry 3 times"
