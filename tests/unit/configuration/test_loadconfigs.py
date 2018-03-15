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
import pytest

from longbow.configuration import loadconfigs
import longbow.exceptions as ex


def test_loadconfigs_test1():

    """
    Test that loadconfigs can parse a configuration file.
    """

    conffile = os.path.join(os.getcwd(), "tests/standards/simplehostfile.txt")

    contents, sections, params = loadconfigs(conffile)

    assert contents == ["[HPC1-shortqueue]", "queue = short", "user = test",
                        "host = login.test.ac.uk", "remoteworkdir = /work/dir",
                        "corespernode = 24", "account = acc200",
                        "handler = aprun", "scheduler = pbs",
                        "maxtime = 00:18", "",
                        "# Comment-y goodness", "[HPC1]", "user = test",
                        "host = login.test.ac.uk",
                        "remoteworkdir = /work/dir2", "corespernode = 24",
                        "account = acc300"]

    assert sections == ['HPC1-shortqueue', 'HPC1']

    assert params["HPC1-shortqueue"]["corespernode"] == "24"
    assert params["HPC1-shortqueue"]["host"] == "login.test.ac.uk"
    assert params["HPC1-shortqueue"]["remoteworkdir"] == "/work/dir"
    assert params["HPC1-shortqueue"]["corespernode"] == "24"
    assert params["HPC1-shortqueue"]["account"] == "acc200"
    assert params["HPC1-shortqueue"]["handler"] == "aprun"
    assert params["HPC1-shortqueue"]["scheduler"] == "pbs"
    assert params["HPC1-shortqueue"]["maxtime"] == "00:18"

    assert params["HPC1"]["corespernode"] == "24"
    assert params["HPC1"]["host"] == "login.test.ac.uk"
    assert params["HPC1"]["remoteworkdir"] == "/work/dir2"
    assert params["HPC1"]["corespernode"] == "24"
    assert params["HPC1"]["account"] == "acc300"


def test_loadconfigs_test2():

    """
    Test that loadconfigs throws a configuration file exception on bad path.
    """

    with pytest.raises(ex.ConfigurationError):

        loadconfigs("/tmp/sometestfile")


def test_loadconfigs_test3():

    """
    Test that loadconfigs throws a configuration file exception on bad path.
    """

    with pytest.raises(ex.ConfigurationError):

        loadconfigs(os.path.join(
            os.getcwd(), "tests/standards/simplefile.txt"))


def test_loadconfigs_test4():

    """
    Test that loadconfigs throws a configuration file exception on bad path.
    """

    with pytest.raises(ex.ConfigurationError):

        loadconfigs(os.path.join(
            os.getcwd(), "tests/standards/configjustsections.txt"))
