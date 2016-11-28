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
This testing module contains basic testing for the LAMMPS plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.apps.lammps as lammps


@mock.patch('os.path.isfile')
def test_filechecks1(m_isfile):

    """
    Check that the required input exception is raised with non absolute path
    and a non file.
    """

    m_isfile.return_value = False

    path = "test/path"
    filename = "file"

    with pytest.raises(exceptions.RequiredinputError):

        lammps._filechecks(path, filename)


@mock.patch('os.path.isfile')
def test_filechecks2(m_isfile):

    """
    Check that the file is identified with non absolute path and a valid file.
    """

    m_isfile.return_value = True

    path = "/test/path"
    filename = "file"

    addfile = lammps._filechecks(path, filename)

    assert addfile == "file"


@mock.patch('os.path.isfile')
def test_filechecks3(m_isfile):

    """
    Check that the required input exception is raised with non absolute path
    and a non file.
    """

    m_isfile.return_value = True

    path = "/test/path"
    filename = "/some/file/path/to/file"

    with pytest.raises(exceptions.RequiredinputError):

        lammps._filechecks(path, filename)


@mock.patch('os.path.isfile')
def test_filechecks4(m_isfile):

    """
    Check that the file is identified with non absolute path and a valid file.
    """

    m_isfile.return_value = False

    path = "/test/path"
    filename = "/some/file/path/to/file"

    addfile = lammps._filechecks(path, filename)

    assert addfile == ""
