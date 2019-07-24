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
This testing module contains basic testing for the NAMD plugin.
"""

import os

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.apps.namd import file_parser


@mock.patch('longbow.apps.namd._fileopen')
@mock.patch('longbow.apps.namd._filechecks')
def test_fileparser_test1(m_check, m_file):

    """
    Test that if add file is already in the files list that nothing happens.
    """

    filename = "testfile"
    path = ""
    files = ["testfile", "anotherfile"]
    substitutions = {}

    m_check.return_value = "testfile"

    file_parser(filename, path, files, substitutions)

    assert m_file.call_count == 0


@mock.patch('longbow.apps.namd._internalsubstitutions')
def test_fileparser_test2(m_subs):

    """
    Test that with a blank file the recursive checks aren't attempted.
    """

    filename = "apps_fileparserblank.txt"
    path = os.path.join(os.getcwd(), "tests/standards/")
    files = ["anotherfile"]
    substitutions = {}

    file_parser(filename, path, files, substitutions)

    assert m_subs.call_count == 0


def test_fileparser_test3():

    """
    Test with simple dependant files.
    """

    filename = "apps_fileparsernamd.txt"
    path = os.path.join(os.getcwd(), "tests/standards/")
    files = []
    substitutions = {}

    file_parser(filename, path, files, substitutions)

    assert files == ["apps_fileparsernamd.txt", "apps_recursivetest.txt"]


def test_fileparser_test4():

    """
    Test with a binary file.
    """

    filename = "namdcoordfile.coor"
    path = os.path.join(os.getcwd(), "tests/standards/")
    files = []
    substitutions = {}

    file_parser(filename, path, files, substitutions)

    assert files == ["namdcoordfile.coor"]


@mock.patch('longbow.apps.namd._internalsubstitutions')
def test_fileparser_test5(subs):

    """
    Test with a binary file check file still added for upload on mocked except.

    This is test is really a bit of a fake, since it is difficult to mock the
    exception in the way it is thrown organically. But this test does do the
    trick!
    """

    filename = "namdcoordfile.coor"
    path = os.path.join(os.getcwd(), "tests/standards/")
    files = []
    substitutions = {}

    subs.side_effect = UnicodeDecodeError('blah', b'', 80, 0, '')

    file_parser(filename, path, files, substitutions)

    assert files == ["namdcoordfile.coor"]
