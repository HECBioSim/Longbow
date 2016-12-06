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


@mock.patch('Longbow.corelibs.applications._procfiles')
def test_proccommandlinetype1_test1(m_procfiles):

    """
    Test that '<' is marked as found if the command-line looks right.
    """

    job = {
        "executableargs": ["<", "input.file"],
        "jobname": "jobone"
    }
    filelist = []
    foundflags = []
    substitution = []

    apps._proccommandlinetype1(job, filelist, foundflags, substitution)

    assert "<" in foundflags
    assert m_procfiles.call_count == 1


@mock.patch('Longbow.corelibs.applications._procfiles')
def test_proccommandlinetype1_expt(m_procfiles):

    """
    Test to make sure the exception is raised if command-line is nonsense.
    """

    job = {
        "executableargs": ["input.file"],
        "jobname": "jobone"
    }
    filelist = []
    foundflags = []
    substitution = []
    m_procfiles.return_value = None

    with pytest.raises(exceptions.RequiredinputError):

        apps._proccommandlinetype1(job, filelist, foundflags, substitution)


@mock.patch('Longbow.corelibs.applications._procfiles')
def test_proccommandlinetype2_test1(m_procfiles):

    """
    Test to make sure the flags are detected and the correct number of
    function calls happen for the number of files/params.
    """

    job = {
        "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
        "jobname": "jobone"
    }
    filelist = []
    foundflags = []
    substitution = []

    apps._proccommandlinetype2(job, filelist, foundflags, substitution)

    assert foundflags == ["-i", "-c", "-p"]
    assert m_procfiles.call_count == 3


@mock.patch('Longbow.corelibs.applications._procfiles')
def test_proccommandlinetype3_test1(m_procfiles):

    """
    Test to make sure the flags are detected and the correct number of
    function calls happen for the number of files/params.
    """

    job = {
        "executableargs": ["subexec", "-i", "input", "-c", "coords", "-p",
                           "topol"],
        "jobname": "jobone"
    }
    filelist = []
    foundflags = []
    substitution = []

    apps._proccommandlinetype3(job, filelist, foundflags, substitution)

    assert foundflags == ["-i", "-c", "-p"]
    assert m_procfiles.call_count == 3


@mock.patch('Longbow.corelibs.applications._procfiles')
def test_proccommandlinetype4_test1(m_procfiles):

    """
    Test that '<' is marked as found if the command-line looks right.
    """

    job = {
        "executableargs": ["input.file"],
        "jobname": "jobone"
    }
    filelist = []
    foundflags = []
    substitution = []

    apps._proccommandlinetype4(job, filelist, foundflags, substitution)

    assert "<" in foundflags
    assert m_procfiles.call_count == 1


@mock.patch('Longbow.corelibs.applications._procfiles')
def test_proccommandlinetype4_expt(m_procfiles):

    """
    Test to make sure the exception is raised if command-line is nonsense.
    """

    job = {
        "executableargs": [],
        "jobname": "jobone"
    }
    filelist = []
    foundflags = []
    substitution = []
    m_procfiles.return_value = None

    with pytest.raises(exceptions.RequiredinputError):

        apps._proccommandlinetype4(job, filelist, foundflags, substitution)
