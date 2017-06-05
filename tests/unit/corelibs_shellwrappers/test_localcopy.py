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
This testing module contains the tests for the localcopy method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.shellwrappers import localcopy


def test_localcopy_srcpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    src = "source/directory/path"
    dst = "/source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        localcopy(src, dst)


def test_localcopy_dstpathcheck():

    """
    Test that the absolute path exception is raised with non absolute paths.
    """

    src = "/source/directory/path"
    dst = "source/directory/path"

    with pytest.raises(exceptions.AbsolutepathError):

        localcopy(src, dst)


@mock.patch('shutil.copy')
@mock.patch('os.path.exists')
@mock.patch('os.path.isfile')
def test_localcopy_fileexcept1(mock_isfile, mock_exists, mock_copy):

    """
    Test that the correct exception is raised if the copy fails.
    """

    src = "/source/directory/path"
    dst = "/source/directory/path"

    mock_isfile.return_value = True
    mock_exists.return_value = True
    mock_copy.side_effect = IOError

    with pytest.raises(exceptions.LocalcopyError):

        localcopy(src, dst)


@mock.patch('shutil.copy')
@mock.patch('os.makedirs')
@mock.patch('os.path.exists')
@mock.patch('os.path.isfile')
def test_localcopy_fileexcept2(mock_isfile, mock_exists, mock_dirs, mock_copy):

    """
    Test that the correct exception is raised if the copy fails.
    """

    src = "/source/directory/path"
    dst = "/source/directory/path"

    mock_isfile.return_value = True
    mock_exists.return_value = False
    mock_dirs.return_value = True
    mock_copy.side_effect = IOError

    with pytest.raises(exceptions.LocalcopyError):

        localcopy(src, dst)


@mock.patch('shutil.copytree')
@mock.patch('shutil.rmtree')
@mock.patch('os.path.exists')
@mock.patch('os.path.isdir')
def test_localcopy_direxcept1(mock_isdir, mock_exists, mock_rmt, mock_cpt):

    """
    Test that the correct exception is raised if the copy fails.
    """

    src = "/source/directory/path"
    dst = "/source/directory/path"

    mock_isdir.return_value = True
    mock_exists.return_value = True
    mock_rmt.return_value = True
    mock_cpt.side_effect = IOError

    with pytest.raises(exceptions.LocalcopyError):

        localcopy(src, dst)


@mock.patch('shutil.copytree')
@mock.patch('os.path.exists')
@mock.patch('os.path.isdir')
def test_localcopy_direxcept2(mock_isdir, mock_exists, mock_cpt):

    """
    Test that the correct exception is raised if the copy fails.
    """

    src = "/source/directory/path"
    dst = "/source/directory/path"

    mock_isdir.return_value = True
    mock_exists.return_value = False
    mock_cpt.side_effect = IOError

    with pytest.raises(exceptions.LocalcopyError):

        localcopy(src, dst)


@mock.patch('os.path.isdir')
@mock.patch('os.path.isfile')
def test_localcopy_notexist(mock_isfile, mock_isdir):

    """
    Test that the correct exception is raised if file does not exist.
    """

    src = "/source/directory/path"
    dst = "/source/directory/path"

    mock_isfile.return_value = False
    mock_isdir.return_value = False

    with pytest.raises(exceptions.LocalcopyError):

        localcopy(src, dst)
