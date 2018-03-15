# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council and
# The University of Nottingham
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
This testing module contains the tests for the configuration module methods.
"""

from longbow.configuration import _saveconfigdiffs


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
