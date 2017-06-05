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
This testing module contains the tests for the downloadexamples method within
the entrypoint module.
"""

import os
import shutil
import subprocess

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

from longbow.corelibs.entrypoints import _downloadexamples


def test_downloadexamples_wget():

    """
    Test that the wget call happens.
    """

    longbowargs = ["blah", "i", "-examples"]

    with pytest.raises(SystemExit):

        _downloadexamples(longbowargs)

    assert not os.path.isfile(
        os.path.join(os.getcwd(), "longbow-examples.zip"))
    assert os.path.isdir(os.path.join(os.getcwd(), "LongbowExamples/"))

    if os.path.isdir(os.path.join(os.getcwd(), "LongbowExamples/")):

        shutil.rmtree(os.path.join(os.getcwd(), "LongbowExamples/"))


@mock.patch('subprocess.check_call')
def test_downloadexamples_curl(mock_check_call):

    """
    Test that the curl call happens but this time make sure --examples works.
    """

    longbowargs = ["blah", "i", "--examples"]

    mock_check_call.side_effect = subprocess.CalledProcessError("", "")

    with pytest.raises(SystemExit):

        _downloadexamples(longbowargs)

    assert not os.path.isfile(
        os.path.join(os.getcwd(), "longbow-examples.zip"))
    assert os.path.isdir(os.path.join(os.getcwd(), "LongbowExamples/"))

    if os.path.isdir(os.path.join(os.getcwd(), "LongbowExamples/")):

        shutil.rmtree(os.path.join(os.getcwd(), "LongbowExamples/"))
