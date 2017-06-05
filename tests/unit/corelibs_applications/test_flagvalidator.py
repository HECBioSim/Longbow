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
This testing module contains the tests for the applications module methods.
"""

import pytest

from longbow.corelibs.applications import _flagvalidator
import longbow.corelibs.exceptions as ex


def test_flagvalidator_pass():

    """Test that the flag test passes if correct."""

    foundflags = ["-c", "-i", "-p"]

    job = {
        "executable": "pmemd.MPI"
    }

    _flagvalidator(job, foundflags)


def test_flagvalidator_fail():

    """Test that the flag test fails with exception if not correct."""

    foundflags = ["-c", "-i"]

    job = {
        "executable": "pmemd.MPI",
        "jobname": "jobone"
    }

    with pytest.raises(ex.RequiredinputError):

        _flagvalidator(job, foundflags)


def test_flagvalidator_ortest():

    """Test that cases with -flag || --flag work."""

    foundflags = ["-deffnm"]

    job = {
        "executable": "mdrun"
    }

    _flagvalidator(job, foundflags)
