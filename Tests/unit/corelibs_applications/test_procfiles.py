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

import Longbow.corelibs.applications as apps


def test_procfiles_amber():

    """
    Test to make sure that the file and flag is picked up for an amber-like
    command-line.
    """

    arg = "coords"
    filelist = []
    foundflags = []
    job = {
        "executable": "pmemd.MPI",
        "replicates": "1",
        "localworkdir": "Tests/standards/jobs/single",
        "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"]
    }
    substitution = {}

    foundflags = apps._procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["-c"]
    assert filelist == ["coords"]


def test_procfiles_charmm():

    """
    Test to make sure that the file and flag is picked up for an charmm-like
    command-line.
    """

    arg = "topol"
    filelist = []
    foundflags = []
    job = {
        "executable": "charmm",
        "replicates": "1",
        "localworkdir": "Tests/standards/jobs/single",
        "executableargs": ["<", "topol"]
    }
    substitution = {}

    foundflags = apps._procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["<"]
    assert filelist == ["topol"]


def test_procfiles_gromacs():

    """
    Test to make sure that the file and flag is picked up for an gromacs-like
    command-line.
    """

    arg = "test"
    filelist = []
    foundflags = []
    job = {
        "executable": "mdrun_mpi",
        "replicates": "1",
        "localworkdir": "Tests/standards/jobs/single",
        "executableargs": ["-deffnm", "test"]
    }
    substitution = {}

    foundflags = apps._procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["-deffnm"]
    assert filelist == ["test.tpr"]


def test_procfiles_namd1():

    """
    Test to make sure that the file and flag is picked up for an namd-like
    command-line.
    """

    arg = "input"
    filelist = []
    foundflags = []
    job = {
        "executable": "namd2",
        "replicates": "1",
        "localworkdir": "Tests/standards/jobs/single",
        "executableargs": ["input"]
    }
    substitution = {}

    foundflags = apps._procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["<"]
    assert filelist == ["input"]


def test_procfiles_namd2():

    """
    Test to make sure that the file and flag is picked up for an namd-like
    command-line.
    """

    arg = "input"
    filelist = []
    foundflags = []
    job = {
        "executable": "namd2",
        "replicates": "1",
        "localworkdir": "Tests/standards/jobs/single",
        "executableargs": ["input", ">", "output"]
    }
    substitution = {}

    foundflags = apps._procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["<"]
    assert filelist == ["input"]


def test_procfiles_reps():

    """
    Test for replicate variant.
    """

    arg = "coords"
    filelist = []
    foundflags = []
    job = {
        "executable": "pmemd.MPI",
        "replicates": "3",
        "localworkdir": "Tests/standards/jobs/replicate",
        "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"]
    }
    substitution = {}

    foundflags = apps._procfiles(job, arg, filelist, foundflags, substitution)

    assert foundflags == ["-c"]
    assert filelist == ["rep1", "rep1/coords", "rep2", "rep2/coords", "rep3",
                        "rep3/coords"]
