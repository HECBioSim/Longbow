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
This testing module contains the tests for the sendtoshell method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.shellwrappers import sendtoshell


def test_sendtoshell_stdoutcapture():

    """
    Capture stdout for a known command and see if the output is actually
    returned.
    """

    stdout = sendtoshell(["uname"])[0]

    assert stdout == "Linux\n"


def test_sendtoshell_stderrcapture():

    """
    Capture stderr for a known command and see if the output is actually
    returned.
    """

    stderr = sendtoshell(["ls", "-al dir"])[1]

    assert stderr != ""


def test_sendtoshell_errcodesuccess():

    """
    Capture errcode for a known command and see if it is a success code.
    """

    errcode = sendtoshell(["uname"])[2]

    assert errcode == 0


def test_sendtoshell_errcodefailure():

    """
    Capture errcode for a known command and see if it is a failure code.
    """

    errcode = sendtoshell(["ls", "-al dir"])[2]

    assert errcode == 2


@mock.patch('subprocess.Popen')
def test_sendtoshell_unicode(mock_subprocess):

    """
    Test the unicode line, would pass in python 3 but not 2.
    """

    try:

        mock_subprocess.return_value.communicate.return_value = \
            unicode("Linux"), ""

    except NameError:

        mock_subprocess.return_value.communicate.return_value = \
            "Linux", ""

    stdout = sendtoshell(["uname"])[0]

    assert stdout == "Linux"


@mock.patch('subprocess.Popen')
def test_sendtoshell_unicode2(mock_subprocess):

    """
    Test the unicode line, would pass in python 3 but not 2.
    """

    try:

        mock_subprocess.return_value.communicate.return_value = \
            "", unicode("Linux")

    except NameError:

        mock_subprocess.return_value.communicate.return_value = \
            "", "Linux"

    stderr = sendtoshell(["uname"])[1]

    assert stderr == "Linux"
