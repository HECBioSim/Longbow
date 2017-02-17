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

import pytest

from longbow.corelibs.configuration import saveconfigs
import longbow.corelibs.exceptions as ex


def test_saveconfigs_test1():

    """
    Test to see if the save configuration method works with a simple data
    structure.
    """

    configfile = "/tmp/saveconfigtest1"
    params = {
        "test1": {
            "param1": "2",
            "param2": "test",
            "param3": "true"
        },
        "test2": {
            "parama": "f",
            "paramb": "12",
            "paramc": "/path/to/somethingelse"
        }
    }

    saveconfigs(configfile, params)

    filestructure = open("/tmp/saveconfigtest1", "r").readlines()
    assert "[test1]\n" in filestructure
    assert "param1 = 2\n" in filestructure
    assert "param2 = test\n" in filestructure
    assert "param3 = true\n" in filestructure

    assert "[test2]\n" in filestructure
    assert "parama = f\n" in filestructure
    assert "paramb = 12\n" in filestructure
    assert "paramc = /path/to/somethingelse\n" in filestructure


def test_saveconfigs_test2():

    """
    Try to write somewhere forbidden
    """

    configfile = "/opt/saveconfigtest1"
    params = {
        "test1": {
            "param1": "2",
            "param2": "test",
            "param3": "true"
        },
        "test2": {
            "parama": "f",
            "paramb": "12",
            "paramc": "/path/to/somethingelse"
        }
    }

    with pytest.raises(ex.ConfigurationError):

        saveconfigs(configfile, params)
