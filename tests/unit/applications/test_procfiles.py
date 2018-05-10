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

from longbow.applications import _procfiles
from longbow.configuration import JOBTEMPLATE


def test_procfiles_amber():

    """
    Test to make sure that the file and flag is picked up for an amber-like
    command-line.
    """
    job = JOBTEMPLATE.copy()

    arg = "coords"
    filelist = []
    foundflags = []

    job["executable"] = "pmemd.MPI"
    job["localworkdir"] = "tests/standards/jobs/single"
    job["executableargs"] = ["-i", "input", "-c", "coords", "-p", "topol"]

    substitution = {}

    foundflags = _procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["-c"]
    assert filelist == ["coords"]


def test_procfiles_charmm():

    """
    Test to make sure that the file and flag is picked up for an charmm-like
    command-line.
    """

    job = JOBTEMPLATE.copy()

    arg = "topol"
    filelist = []
    foundflags = []
    job["executable"] = "charmm"
    job["localworkdir"] = "tests/standards/jobs/single"
    job["executableargs"] = ["<", "topol"]

    substitution = {}

    foundflags = _procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["<"]
    assert filelist == ["topol"]


def test_procfiles_gromacs():

    """
    Test to make sure that the file and flag is picked up for an gromacs-like
    command-line.
    """

    job = JOBTEMPLATE.copy()

    arg = "test"
    filelist = []
    foundflags = []
    job["executable"] = "mdrun_mpi"
    job["localworkdir"] = "tests/standards/jobs/single"
    job["executableargs"] = ["-deffnm", "test"]

    substitution = {}

    foundflags = _procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["-deffnm"]
    assert filelist == ["test.tpr"]


def test_procfiles_namd1():

    """
    Test to make sure that the file and flag is picked up for an namd-like
    command-line.
    """

    job = JOBTEMPLATE.copy()

    arg = "input"
    filelist = []
    foundflags = []
    job["executable"] = "namd2"
    job["localworkdir"] = "tests/standards/jobs/single"
    job["executableargs"] = ["input"]

    substitution = {}

    foundflags = _procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["<"]
    assert filelist == ["input"]


def test_procfiles_namd2():

    """
    Test to make sure that the file and flag is picked up for an namd-like
    command-line.
    """

    job = JOBTEMPLATE.copy()

    arg = "input"
    filelist = []
    foundflags = []
    job["executable"] = "namd2"
    job["localworkdir"] = "tests/standards/jobs/single"
    job["executableargs"] = ["input", ">", "output"]

    substitution = {}

    foundflags = _procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["<"]
    assert filelist == ["input"]


def test_procfiles_reps1():

    """
    Test for replicate variant.
    """

    job = JOBTEMPLATE.copy()

    arg = "coords"
    filelist = []
    foundflags = []
    job["executable"] = "pmemd.MPI"
    job["replicates"] = "3"
    job["localworkdir"] = "tests/standards/jobs/replicate"
    job["executableargs"] = ["-i", "input", "-c", "coords", "-p", "topol"]

    substitution = {}

    foundflags = _procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["-c"]
    assert filelist == ["rep1", "rep1/coords", "rep2", "rep2/coords", "rep3",
                        "rep3/coords"]


def test_procfiles_reps2():

    """
    Test for replicate variant with global.
    """

    job = JOBTEMPLATE.copy()

    arg = "topol"
    filelist = []
    foundflags = []
    job["executable"] = "pmemd.MPI"
    job["replicates"] = "3"
    job["localworkdir"] = "tests/standards/jobs/replicate"
    job["executableargs"] = ["-i", "input", "-c", "coords", "-p", "topol"]

    substitution = {}

    foundflags = _procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["-p"]
    assert filelist == ["rep1", "topol", "rep2", "rep3"]
