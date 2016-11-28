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

import os

try:

    from unittest import mock

except ImportError:

    import mock

import Longbow.apps.lammps as lammps


@mock.patch('Longbow.apps.lammps._filechecks')
def test_fileparser_test1(m_check):

    """
    Test that if add file is already in the files list that nothing happens.
    """

    filename = "testfile"
    path = ""
    files = ["testfile", "anotherfile"]
    substitutions = {}

    m_check.return_value = "testfile"

    lammps.file_parser(filename, path, files, substitutions)


@mock.patch('Longbow.apps.lammps._internalsubstitutions')
def test_fileparser_test2(m_subs):

    """
    Test that with a blank file the recursive checks aren't attempted.
    """

    filename = "apps_fileparserblank.txt"
    path = os.path.join(os.getcwd(), "Tests/standards/")
    files = ["anotherfile"]
    substitutions = {}

    lammps.file_parser(filename, path, files, substitutions)

    assert m_subs.call_count == 0


def test_fileparser_test3():

    """
    Test with simple dependant files.
    """

    filename = "apps_fileparserlammps.txt"
    path = os.path.join(os.getcwd(), "Tests/standards/")
    files = []
    substitutions = {}

    lammps.file_parser(filename, path, files, substitutions)

    assert files == ["apps_fileparserlammps.txt", "apps_recursivetest.txt"]
