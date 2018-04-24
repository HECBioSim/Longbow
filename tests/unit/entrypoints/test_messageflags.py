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
This testing module contains the tests for the messageflags method within the
entrypoint module.
"""

import pytest

from longbow.entrypoints import _messageflags


def test_messageflags_sdashabout():

    """
    Test that the -about flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "-about"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)


def test_messageflags_ddashabout():

    """
    Test that the --about flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "--about"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)


def test_messageflags_sdashversion():

    """
    Test that the -version flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "-version"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)


def test_messageflags_ddashversion():

    """
    Test that the --version flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "--version"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)


def test_messageflags_version():

    """
    Test that the -V flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "-V"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)


def test_messageflags_sdashhelp():

    """
    Test that the -help flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "-help"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)


def test_messageflags_ddashhelp():

    """
    Test that the --help flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "--help"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)


def test_messageflags_help():

    """
    Test that the -h flag results in the systemexit exception being
    raised.
    """

    longbowargs = ["blah", "i", "-h"]

    with pytest.raises(SystemExit):

        _messageflags(longbowargs)
