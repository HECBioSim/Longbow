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
This test module contains tests for the PBS scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.schedulers.pbs import status

out = ("Job ID          Username Queue    Jobname    SessID NDS TSK Memory Time  S Time \n"
       "--------------- -------- -------- ---------- ------ --- --- ------ ----- - -----\n"
       "3530460.sdb     katrine  long     Uio67         --    8 192    --  48:00 B   -- \n"
       "3530473.sdb     katrine  long     IRM10         --    8 192    --  48:00 E   -- \n"
       "3537896.sdb     katrine  standard BiPip         --    8 192    --  01:00 H   -- \n"
       "3537971.sdb     katrine  standard Pol-test      --    8 192    --  00:10 M   -- \n"
       "3537972.sdb     katrine  standard Pol-test      --    8 192    --  00:10 Q   -- \n"
       "3537974.sdb     katrine  standard Pol-test      --    8 192    --  00:10 R   -- \n"
       "3538328.sdb     katrine  standard Pol-test      --    8 192    --  00:10 S   -- \n"
       "3538333.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 T   -- \n"
       "3538337.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 U   -- \n"
       "3538340.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 W   -- \n"
       "3538341.sdb     katrine  standard ZrF-mir       --    4  96    --  00:20 X   -- \n")


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state1(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3530460"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Subjob(s) Running"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state2(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3530473"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Exiting"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state3(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537896"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Held"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state4(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537971"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Job Moved to Server"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state5(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537972"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Queued"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state6(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3537974"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Running"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state7(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538328"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Suspended"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state8(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538333"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Job Moved to New Location"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state9(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538337"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == ("Cycle-Harvesting Job is Suspended Due to Keyboard "
                      "Activity")


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state10(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538340"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Waiting for Start Time"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state11(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538341"
    }

    mock_ssh.return_value = (out, "", 0)

    output = status(job)

    assert output == "Subjob Completed Execution/Has Been Deleted"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_state12(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538341"
    }

    mock_ssh.return_value = ("", "", 0)

    output = status(job)

    assert output == "Finished"


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_status_except1(mock_ssh):

    """
    Test if SSH Error is handled.
    """

    job = {
        "user": "test",
        "jobid": ""
    }

    mock_ssh.side_effect = exceptions.SSHError("OUT", "ERR")

    with pytest.raises(exceptions.SSHError):

        status(job)
