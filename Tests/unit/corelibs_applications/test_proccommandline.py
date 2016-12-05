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
This testing module contains the tests for the applications module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.applications as apps
import Longbow.corelibs.exceptions as exceptions


@mock.patch('Longbow.corelibs.applications._proccommandlinetype4')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype3')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype2')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype1')
def test_proccommandline_test1(m_proc1, m_proc2, m_proc3, m_proc4):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["<", "input.file"]
    }

    m_proc1.return_value = ([], [])

    apps._proccommandline(job, "path", [])

    assert m_proc1.call_count == 1
    assert m_proc2.call_count == 0
    assert m_proc3.call_count == 0
    assert m_proc4.call_count == 0


@mock.patch('Longbow.corelibs.applications._proccommandlinetype4')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype3')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype2')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype1')
def test_proccommandline_test2(m_proc1, m_proc2, m_proc3, m_proc4):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["-c", "file", "-i", "file", "-p", "file"]
    }

    m_proc2.return_value = ([], [])

    apps._proccommandline(job, "path", [])

    assert m_proc1.call_count == 0
    assert m_proc2.call_count == 1
    assert m_proc3.call_count == 0
    assert m_proc4.call_count == 0


@mock.patch('Longbow.corelibs.applications._proccommandlinetype4')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype3')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype2')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype1')
def test_proccommandline_test3(m_proc1, m_proc2, m_proc3, m_proc4):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "gmx",
        "executableargs": ["mdrun_mpi", "-deffnm"]
    }

    m_proc3.return_value = ([], [])

    apps._proccommandline(job, "path", [])

    assert m_proc1.call_count == 0
    assert m_proc2.call_count == 0
    assert m_proc3.call_count == 1
    assert m_proc4.call_count == 0


@mock.patch('Longbow.corelibs.applications._proccommandlinetype4')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype3')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype2')
@mock.patch('Longbow.corelibs.applications._proccommandlinetype1')
def test_proccommandline_test4(m_proc1, m_proc2, m_proc3, m_proc4):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "charmm",
        "executableargs": ["input.file"]
    }

    m_proc4.return_value = ([], [])

    apps._proccommandline(job, "path", [])

    assert m_proc1.call_count == 0
    assert m_proc2.call_count == 0
    assert m_proc3.call_count == 0
    assert m_proc4.call_count == 1


def test_proccommandline_except():

    """
    Test if the exception is raised if command-line is bad.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["", "", ""],
        "jobname": "jobone"
    }

    with pytest.raises(exceptions.RequiredinputError):

        apps._proccommandline(job, "path", [])
