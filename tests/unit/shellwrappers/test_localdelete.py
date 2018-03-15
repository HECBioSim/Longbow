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
This testing module contains the tests for the localdelete method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.shellwrappers import localdelete


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
