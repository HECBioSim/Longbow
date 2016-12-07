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

import Longbow.corelibs.configuration as conf
import Longbow.corelibs.exceptions as ex


def test_processconfigs_test1():

    """
    Test missing host file raises exception.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "/tmp/hostfile.conf",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    with pytest.raises(ex.ConfigurationError):

        conf.processconfigs(parameters)


def test_processconfigs_test2():

    """
    Test missing job file raises exception.
    """

    conffile = os.path.join(os.getcwd(), "Tests/standards/simplehostfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": conffile,
        "job": "/tmp/jobfile.conf",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    with pytest.raises(ex.ConfigurationError):

        conf.processconfigs(parameters)


def test_processconfigs_test3():

    """
    Test a single job with hostfile and command-line
    """

    conffile = os.path.join(os.getcwd(), "Tests/standards/simplehostfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "pmemd.MPI",
        "executableargs": ["-O", "-i", "example.in", "-c", "example.min", "-p",
                           "example.top", "-o", "example.out"],
        "hosts": conffile,
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "HPC1-shortqueue",
        "replicates": "",
        "verbose": False
    }

    jobs = conf.processconfigs(parameters)

    assert "LongbowJob" in jobs
    assert jobs["LongbowJob"]["executable"] == "pmemd.MPI"
    assert jobs["LongbowJob"]["resource"] == "HPC1-shortqueue"
    assert jobs["LongbowJob"]["executableargs"] == [
        "-O", "-i", "example.in", "-c", "example.min", "-p", "example.top",
        "-o", "example.out"]
    assert jobs["LongbowJob"]["queue"] == "short"
    assert jobs["LongbowJob"]["user"] == "test"
    assert jobs["LongbowJob"]["host"] == "login.test.ac.uk"
    assert jobs["LongbowJob"]["remoteworkdir"] == "/work/dir"
    assert jobs["LongbowJob"]["corespernode"] == "24"
    assert jobs["LongbowJob"]["account"] == "acc200"
    assert jobs["LongbowJob"]["handler"] == "aprun"
    assert jobs["LongbowJob"]["scheduler"] == "pbs"
    assert jobs["LongbowJob"]["maxtime"] == "00:18"
    assert jobs["LongbowJob"]["cores"] == "24"
    assert jobs["LongbowJob"]["replicates"] == "1"


def test_processconfigs_test4():

    """
    Test a single job with hostfile and command-line and a provided job name.
    """

    conffile = os.path.join(os.getcwd(), "Tests/standards/simplehostfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "pmemd.MPI",
        "executableargs": ["-O", "-i", "example.in", "-c", "example.min", "-p",
                           "example.top", "-o", "example.out"],
        "hosts": conffile,
        "job": "",
        "jobname": "test-job",
        "log": "",
        "recover": "",
        "resource": "HPC1-shortqueue",
        "replicates": "",
        "verbose": False
    }

    jobs = conf.processconfigs(parameters)

    assert "test-job" in jobs
    assert jobs["test-job"]["executable"] == "pmemd.MPI"
    assert jobs["test-job"]["resource"] == "HPC1-shortqueue"
    assert jobs["test-job"]["executableargs"] == [
        "-O", "-i", "example.in", "-c", "example.min", "-p", "example.top",
        "-o", "example.out"]
    assert jobs["test-job"]["queue"] == "short"
    assert jobs["test-job"]["user"] == "test"
    assert jobs["test-job"]["host"] == "login.test.ac.uk"
    assert jobs["test-job"]["remoteworkdir"] == "/work/dir"
    assert jobs["test-job"]["corespernode"] == "24"
    assert jobs["test-job"]["account"] == "acc200"
    assert jobs["test-job"]["handler"] == "aprun"
    assert jobs["test-job"]["scheduler"] == "pbs"
    assert jobs["test-job"]["maxtime"] == "00:18"
    assert jobs["test-job"]["cores"] == "24"
    assert jobs["test-job"]["replicates"] == "1"


def test_processconfigs_test5():

    """
    Test a multijob with hostfile and jobfile
    """

    hostfile = os.path.join(os.getcwd(), "Tests/standards/simplehostfile.txt")
    jobfile = os.path.join(os.getcwd(), "Tests/standards/simplejobfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": hostfile,
        "job": jobfile,
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "HPC1-shortqueue",
        "replicates": "",
        "verbose": False
    }

    jobs = conf.processconfigs(parameters)

    assert "amber" in jobs
    assert "gromacs_s" in jobs
    assert "gromacs_d" in jobs
    assert "lammps" in jobs
    assert "namd" in jobs

    assert jobs["amber"]["executable"] == "pmemd.MPI"
    assert jobs["gromacs_s"]["executable"] == "mdrun_mpi"
    assert jobs["gromacs_d"]["executable"] == "mdrun_mpi_d"
    assert jobs["namd"]["executable"] == "namd2"
    assert jobs["lammps"]["executable"] == "lmp_xc30"

    assert jobs["amber"]["cores"] == "24"
    assert jobs["gromacs_s"]["cores"] == "24"
    assert jobs["gromacs_d"]["cores"] == "72"
    assert jobs["namd"]["cores"] == "24"
    assert jobs["lammps"]["cores"] == "48"

    assert jobs["amber"]["remoteworkdir"] == "/work/dir"
    assert jobs["gromacs_s"]["remoteworkdir"] == "/work/dir"
    assert jobs["gromacs_d"]["remoteworkdir"] == "/work/dir"
    assert jobs["namd"]["remoteworkdir"] == "/work/dir2"
    assert jobs["lammps"]["remoteworkdir"] == "/work/dir2"
