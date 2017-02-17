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

import os
import pytest

from longbow.corelibs.configuration import loadconfigs
import longbow.corelibs.exceptions as ex


def test_loadconfigs_test1():

    """
    Test that loadconfigs can parse a configuration file.
    """

    conffile = os.path.join(os.getcwd(), "Tests/standards/simplehostfile.txt")

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
            os.getcwd(), "Tests/standards/simplefile.txt"))


def test_loadconfigs_test4():

    """
    Test that loadconfigs throws a configuration file exception on bad path.
    """

    with pytest.raises(ex.ConfigurationError):

        loadconfigs(os.path.join(
            os.getcwd(), "Tests/standards/configjustsections.txt"))
