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
This testing module contains basic testing for the CHARMM plugin.
"""

from longbow.apps.charmm import EXECDATA


def test_basic1():

    """
    Test that the data structure is a dictionary.
    """

    assert isinstance(EXECDATA, dict)


def test_basic2():

    """
    Test that the data structure has values.
    """

    assert len(EXECDATA) > 0


def test_basic3():

    """
    Test that the data structure has values.
    """

    for param in EXECDATA:

        assert isinstance(EXECDATA[param], dict)
        assert "subexecutables" in EXECDATA[param]
        assert "requiredfiles" in EXECDATA[param]
