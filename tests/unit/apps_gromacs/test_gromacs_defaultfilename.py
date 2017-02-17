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
This testing module contains basic testing for the GROMACS plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import Longbow.apps.gromacs as gromacs


@mock.patch('os.path.isfile')
def test_defaultfilename1(m_isfile):

    """
    Test that the gromacs tpr file is captured in cases where -deffnm is used.
    """

    path = "/some/path/to/jobdir"
    item = "test"
    initargs = ["-deffnm", "test"]

    m_isfile.return_value = True

    filename, initargs = gromacs.defaultfilename(path, item, initargs)

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

    filename, initargs = gromacs.defaultfilename(path, item, initargs)

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

    filename, initargs = gromacs.defaultfilename(path, item, initargs)

    assert filename == ""
    assert initargs == ["-s", "test"]
