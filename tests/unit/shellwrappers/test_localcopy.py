# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council and
# The University of Nottingham
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
This testing module contains the tests for the localcopy method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import localcopy


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
