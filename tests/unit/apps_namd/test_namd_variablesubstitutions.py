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
This testing module contains basic testing for the NAMD plugin.
"""

from longbow.apps.namd import _variablesubstitutions


def test_varsubstitutions_test1():

    """
    Test for blank items.
    """

    newfile = ""
    variables = {}

    _variablesubstitutions(newfile, variables)

    assert newfile == ""


def test_varsubstitutions_test2():

    """
    Test for the substitution.
    """

    newfile = "$myvar.xsc"
    variables = {"myvar": "myprot"}

    newfile = _variablesubstitutions(newfile, variables)

    assert newfile == "myprot.xsc"
