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

import pytest

from longbow.configuration import saveconfigs
import longbow.exceptions as ex


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

    configfile = "/usr/saveconfigtest1"
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
