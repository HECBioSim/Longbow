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
This testing module contains basic testing for the GROMACS plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.apps.gromacs import defaultfilename


@mock.patch('os.path.isfile')
def test_defaultfilename1(m_isfile):

    """
    Test that the gromacs tpr file is captured in cases where -deffnm is used.
    """

    path = "/some/path/to/jobdir"
    item = "test"
    initargs = ["-deffnm", "test"]

    m_isfile.return_value = True

    filename, initargs = defaultfilename(path, item, initargs)

    assert filename == "test.tpr"
    assert initargs == ['-s', '../test.tpr', '-deffnm', 'test']


@mock.patch('os.path.isfile')
def test_defaultfilename2(m_isfile):

    """
    Test the negative case.
    """

    path = "/some/path/to/jobdir"
    item = "test"
    initargs = ["-deffnm", "test"]

    m_isfile.return_value = False

    filename, initargs = defaultfilename(path, item, initargs)

    assert filename == ""
    assert initargs == ["-deffnm", "test"]


@mock.patch('os.path.isfile')
def test_defaultfilename3(m_isfile):

    """
    Test the -s case.
    """

    path = "/some/path/to/jobdir"
    item = "test"
    initargs = ["-s", "test"]

    m_isfile.return_value = False

    filename, initargs = defaultfilename(path, item, initargs)

    assert filename == ""
    assert initargs == ["-s", "test"]
