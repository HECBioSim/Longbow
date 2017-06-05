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
This testing module contains the tests for the localdelete method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.shellwrappers import localdelete


def test_localdelete_srcpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    src = "source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        localdelete(src)


@mock.patch('os.path.isfile')
@mock.patch('os.remove')
def test_localdelete_fileexcept(mock_remove, mock_isfile):

    """
    Test that delete exception is raised if remove file fails.
    """

    src = "/source/directory/path"

    mock_isfile.return_value = True
    mock_remove.side_effect = IOError()

    with pytest.raises(exceptions.LocaldeleteError):

        localdelete(src)


@mock.patch('shutil.rmtree')
@mock.patch('os.path.isdir')
@mock.patch('os.path.isfile')
def test_localdelete_direxcept(mock_isfile, mock_isdir, mock_remove):

    """
    Test that delete exception is raised if remove directory fails.
    """

    src = "/source/directory/path"

    mock_isfile.return_value = False
    mock_isdir.return_value = True
    mock_remove.side_effect = IOError()

    with pytest.raises(exceptions.LocaldeleteError):

        localdelete(src)


@mock.patch('os.path.isdir')
@mock.patch('os.path.isfile')
def test_localdelete_notexist(mock_isfile, mock_isdir):

    """
    Test that the correct exception is raised when src does not exist.
    """

    src = "/source/directory/path"

    mock_isfile.return_value = False
    mock_isdir.return_value = False

    with pytest.raises(exceptions.LocaldeleteError):

        localdelete(src)
