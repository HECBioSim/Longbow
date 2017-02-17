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
# longbow.  If not, see <http://www.gnu.org/licenses/>.

"""
This testing module contains the tests for the applications module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

from longbow.corelibs.applications import testapp
import longbow.corelibs.exceptions as ex


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testapp_exectest(m_sendtossh):

    """
    Test that the executable query is formatted correctly.
    """

    jobs = {
        "jobone": {
            "resource": "res1",
            "executable": "exec1",
            "modules": "",
            "nochecks": "false"
        }
    }

    testapp(jobs)

    assert m_sendtossh.call_count == 1
    assert m_sendtossh.call_args[0][1] == ["which exec1"]


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testapp_moduletest(m_sendtossh):

    """
    Test that modules to be loaded are appended into the executable query
    string.
    """

    jobs = {
        "jobone": {
            "resource": "res1",
            "executable": "exec1",
            "modules": "intel, amber",
            "nochecks": "false"
        }
    }

    testapp(jobs)

    assert m_sendtossh.call_count == 1
    assert "which exec1" in m_sendtossh.call_args[0][1]
    assert "module load intel\n" in m_sendtossh.call_args[0][1]
    assert "module load amber\n" in m_sendtossh.call_args[0][1]


@mock.patch('longbow.corelibs.shellwrappers.sendtossh')
def test_testapp_except(m_sendtossh):

    """
    Test that modules to be loaded are appended into the executable query
    string.
    """

    jobs = {
        "jobone": {
            "resource": "res1",
            "executable": "exec1",
            "modules": "intel, amber",
            "nochecks": "false"
        }
    }

    m_sendtossh.side_effect = ex.SSHError("Error", ("stdout", "stderr", 1))

    with pytest.raises(ex.SSHError):

        testapp(jobs)
