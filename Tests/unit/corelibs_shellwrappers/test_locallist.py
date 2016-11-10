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
This testing module contains the tests for the shellwrappers module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.shellwrappers as shellwrappers


def test_locallist_srcpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    src = "source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        shellwrappers.locallist(src)


@mock.patch('os.listdir')
@mock.patch('os.path.exists')
def test_locallist_returncheck(mock_exists, mock_listdir):

    """
    Test that the method is returning a list.
    """

    src = "/source/directory/path"

    mock_exists.return_value = True
    mock_listdir.return_value = ["item1", "item2"]

    output = shellwrappers.locallist(src)

    assert output[0] == "item1"
    assert output[1] == "item2"


@mock.patch('os.path.exists')
def test_locallist_exceptiontest(mock_exists):

    """
    Test that the correct exception is raised when things go wrong.
    """

    src = "/source/directory/path"

    mock_exists.return_value = False

    with pytest.raises(exceptions.LocallistError):

        shellwrappers.locallist(src)
