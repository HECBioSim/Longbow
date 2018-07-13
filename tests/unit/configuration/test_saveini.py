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

import os
from longbow.configuration import saveini


def test_saveini_test1():

    """
    A simple test for the ini file save method, this will test the ability for
    Longbow to save out recovery files.
    """

    params = {
        "Section": {
            "param": "val"
        }
    }

    saveini("/tmp/initest", params)

    assert open("/tmp/initest", "rb").read() == open(
        os.path.join(os.getcwd(),
                     "tests/standards/saveini.txt"), "rb").read()


def test_saveini_test2():

    """
    A more advanced test checking that the internal configuration data is
    saved.
    """

    params = {
        "lbowconf": {
            "update": False,
            "hpc1-queue-max": 0,
            "hpc1-queue-slots": 0
        },
        "job1": {
            "param1": "val1",
            "param2": "val2",
        },
        "job2": {
            "parama": "vala",
            "paramb": "valb",
        },
        "job3": {
            "parami": "vali",
            "paramii": "valii",
        }
    }

    saveini("/tmp/initest2", params)

    with open("/tmp/initest2", "rb") as tmpfile:
        tmpcontents = tmpfile.read().decode("utf-8")

    assert "[lbowconf]\n" in tmpcontents
    assert "hpc1-queue-max = 0\n" in tmpcontents
    assert "update = False\n" in tmpcontents
    assert "hpc1-queue-slots = 0\n" in tmpcontents
    assert "[job3]\n" in tmpcontents
    assert "[job2]\n" in tmpcontents
    assert "[job1]\n" in tmpcontents
    assert "param1 = val1\n" in tmpcontents
    assert "param2 = val2\n" in tmpcontents
    assert "parama = vala\n" in tmpcontents
    assert "paramb = valb\n" in tmpcontents
    assert "parami = vali\n" in tmpcontents
    assert "paramii = valii\n" in tmpcontents
