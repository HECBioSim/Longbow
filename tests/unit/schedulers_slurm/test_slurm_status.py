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
This test module contains tests for the slurm scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.schedulers.slurm as slurm

out = ("             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)\n"
       "               600 interacti  run2.sh     user CA       0:19      1 blade01)\n"
       "               601 interacti  run2.sh     user CD       0:19      1 blade01)\n"
       "               602 interacti  run2.sh     user CF       0:19      1 blade01)\n"
       "               603 interacti  run2.sh     user CG       0:19      1 blade01)\n"
       "               604 interacti  run2.sh     user F        0:19      1 blade01)\n"
       "               605 interacti  run2.sh     user NF       0:19      1 blade01)\n"
       "               606 interacti  run2.sh     user PD       0:19      1 blade01)\n"
       "               607 interacti  run2.sh     user PR       0:19      1 blade01)\n"
       "               608 interacti  run2.sh     user R        0:19      1 blade01)\n"
       "               609 interacti  run2.sh     user S        0:19      1 blade01)\n"
       "               610 interacti  run2.sh     user TO       0:19      1 blade01)\n")


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state1(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "600"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Cancelled"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state2(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "601"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Completed"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state3(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "602"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Configuring"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state4(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "603"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Completing"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state5(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "604"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Failed"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state6(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "605"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Node Failure"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state7(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "606"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Pending"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state8(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "607"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Preempted"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state9(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "608"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == ("Running")


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state10(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "609"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Suspended"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state11(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "610"
    }

    mock_ssh.return_value = (out, "", 0)

    output = slurm.status(job)

    assert output == "Timed out"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_status_state12(mock_ssh):

    """
    Test if job status is grabbed.
    """

    job = {
        "user": "test",
        "jobid": "3538341"
    }

    mock_ssh.return_value = ("", "", 0)

    output = slurm.status(job)

    assert output == "Finished"


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
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

        slurm.status(job)
