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
This testing module contains the tests for the messageflags method within the
entrypoint module.
"""

import pytest

from longbow.corelibs.entrypoints import _messageflags


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
