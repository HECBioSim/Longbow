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

from longbow.corelibs.applications import _proccommandline
import longbow.corelibs.exceptions as exceptions


@mock.patch('longbow.corelibs.applications._procfiles')
def test_proccommandline_test1(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["<", "input.file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 1
    assert m_procfiles.call_args[0][1] == "input.file"


@mock.patch('longbow.corelibs.applications._procfiles')
def test_proccommandline_test2(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["-c", "file", "-i", "file", "-p", "file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 3
    assert m_procfiles.call_args[0][1] == "file"


@mock.patch('longbow.corelibs.applications._procfiles')
def test_proccommandline_test3(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "gmx",
        "executableargs": ["mdrun_mpi", "-deffnm", "filename"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 1
    assert m_procfiles.call_args[0][1] == "filename"


@mock.patch('longbow.corelibs.applications._procfiles')
def test_proccommandline_test4(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "charmm",
        "executableargs": ["input.file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 1
    assert m_procfiles.call_args[0][1] == "input.file"


@mock.patch('longbow.corelibs.applications._procfiles')
def test_proccommandline_test5(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "namd2",
        "executableargs": ["input.file", ">", "output.file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 2
    assert m_procfiles.call_args[0][1] == "output.file"


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

        _proccommandline(job, [], [], {})
