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

from longbow.corelibs.configuration import _saveconfigdiffs


def test_saveconfigdiffs_test1():

    """
    A simple test to check that no diffs get found if params == oldparams.
    """

    keydiff = {}
    valuediff = {}
    params = {
        "test1": {
            "param1": "1",
            "param2": "test",
            "param3": "true"
        },
        "test2": {
            "parama": "",
            "paramb": "1293",
            "paramc": "/path/to/something"
        }
    }

    oldparams = {
        "test1": {
            "param1": "1",
            "param2": "test",
            "param3": "true"
        },
        "test2": {
            "parama": "",
            "paramb": "1293",
            "paramc": "/path/to/something"
        }
    }

    _saveconfigdiffs(params, oldparams, keydiff, valuediff)

    assert keydiff == {}
    assert valuediff == {}


def test_saveconfigdiffs_test2():

    """
    A simple test to check that value changes get picked up.
    """

    keydiff = {}
    valuediff = {}
    params = {
        "test1": {
            "param1": "1",
            "param2": "test",
            "param3": "true"
        },
        "test2": {
            "parama": "",
            "paramb": "1293",
            "paramc": "/path/to/something"
        }
    }

    oldparams = {
        "test1": {
            "param1": "2",
            "param2": "test",
            "param3": "true"
        },
        "test2": {
            "parama": "",
            "paramb": "12",
            "paramc": "/path/to/somethingelse"
        }
    }

    _saveconfigdiffs(params, oldparams, keydiff, valuediff)

    # Check keydiff.
    assert keydiff == {}

    # Check valuediff.
    assert valuediff["test1"]["param1"] == "1"
    assert valuediff["test2"]["paramb"] == "1293"
    assert valuediff["test2"]["paramc"] == "/path/to/something"


def test_saveconfigdiffs_test3():

    """
    A simple test to check that missing keys get picked up.
    """

    keydiff = {}
    valuediff = {}
    params = {
        "test1": {
            "param1": "1",
            "param2": "test",
            "param3": "true"
        },
        "test2": {
            "parama": "",
            "paramb": "1293",
            "paramc": "/path/to/something"
        }
    }

    oldparams = {
        "test1": {
            "param1": "2",
            "param2": "test",
        },
        "test2": {
            "parama": "",
            "paramb": "12",
        }
    }

    _saveconfigdiffs(params, oldparams, keydiff, valuediff)

    # Check keydiff.
    assert keydiff["test1"]["param3"] == "true"
    assert keydiff["test2"]["paramc"] == "/path/to/something"

    # Check valuediff.
    assert valuediff["test1"]["param1"] == "1"
    assert valuediff["test2"]["paramb"] == "1293"
