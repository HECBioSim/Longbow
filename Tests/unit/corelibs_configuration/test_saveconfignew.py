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
This testing module contains the tests for the configuration module methods.
"""

import Longbow.corelibs.configuration as conf


def test_saveconfignew_test1():

    """
    A simple test to test parameter insertions into sections.
    """

    contents = ["[test1]", "param1 = 2", "param2 = test", "[test2]",
                "parama = f", "paramb = 12"]

    keydiff = {
        "test1": {
            "param3": "true"
        },
        "test2": {
            "paramc": "/path/to/something"
        }
    }

    conf._saveconfignew(contents, keydiff)

    assert contents == ["[test1]", "param1 = 2", "param2 = test",
                        "param3 = true", "[test2]", "parama = f",
                        "paramb = 12", "paramc = /path/to/something"]


def test_saveconfignew_test2():

    """
    A simple test to test parameter insertions into sections.
    """

    contents = ["[test1]", "param1 = 2", "param2 = test", "[test2]",
                "parama = f", "paramb = 12"]

    keydiff = {
        "test3": {
            "param1": "test"
        },
        "test4": {
            "param2": "1"
        }
    }

    conf._saveconfignew(contents, keydiff)

    assert contents == ["[test1]", "param1 = 2", "param2 = test",
                        "[test2]", "parama = f", "paramb = 12", "", "[test3]",
                        "param1 = test", "", "[test4]", "param2 = 1"]
