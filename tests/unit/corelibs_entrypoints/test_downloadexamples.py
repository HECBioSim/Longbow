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
import subprocess

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

from longbow.corelibs.entrypoints import _downloadexamples


@mock.patch('subprocess.call')
@mock.patch('subprocess.check_call')
def test_downloadexamples_wget(mock_output, mock_call):

    """
    Test that the wget call happens.
    """

    longbowargs = ["blah", "i", "-examples"]

    with pytest.raises(SystemExit):

        _downloadexamples(longbowargs)

    assert mock_output.call_args[0][0] == \
        ['wget', 'http://www.hecbiosim.ac.uk/downloads/send/2-software/' +
         '4-longbow-examples', '-O',
         os.path.join(os.getcwd(), "LongbowExamples.zip")]
    assert mock_call.call_count == 1


@mock.patch('subprocess.call')
@mock.patch('subprocess.check_call')
def test_downloadexamples_curl(mock_output, mock_call):

    """
    Test that the curl call happens but this time make sure --examples works.
    """

    longbowargs = ["blah", "i", "--examples"]

    mock_output.side_effect = subprocess.CalledProcessError("", "")

    with pytest.raises(SystemExit):

        _downloadexamples(longbowargs)

    assert mock_call.call_args_list[0][0][0] == \
        ["curl", "-L", "http://www.hecbiosim.ac.uk/downloads/send/" +
         "2-software/4-longbow-examples", "-o",
         os.path.join(os.getcwd(), "LongbowExamples.zip")]
    assert mock_call.call_count == 2
