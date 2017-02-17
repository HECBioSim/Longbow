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

import os
import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.apps.charmm import _fileopen


def test_fileopen_test1():

    """Test if files can be loaded."""

    addfile = "simplefile.txt"
    path = os.path.join(os.getcwd(), "Tests/standards/")

    filehandle = _fileopen(path, addfile)

    assert filehandle.readline() == "test"


def test_fileopen_test2():

    """Test what happens with a bogus file."""

    addfile = "jkhggkjh.txt"
    path = os.path.join(os.getcwd(), "Tests/standards/")

    with pytest.raises(exceptions.RequiredinputError):

        _fileopen(path, addfile)
