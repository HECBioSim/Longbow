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
This testing module contains the tests for the sendtoshell method within the
shellwrappers module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.corelibs.shellwrappers import sendtoshell


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
