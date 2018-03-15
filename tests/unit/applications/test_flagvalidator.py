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
This testing module contains the tests for the applications module methods.
"""

import pytest

from longbow.applications import _flagvalidator
import longbow.exceptions as ex


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
