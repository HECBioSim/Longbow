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

from longbow.configuration import processconfigs
import longbow.exceptions as ex


def test_processconfigs_test1():

    """
    Test missing host file raises exception.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

        processconfigs(parameters)


def test_processconfigs_test2():

    """
    Test missing job file raises exception.
    """

    conffile = os.path.join(os.getcwd(), "tests/standards/simplehostfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
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

        processconfigs(parameters)


def test_processconfigs_test3():

    """
    Test a single job with hostfile and command-line
    """

    conffile = os.path.join(os.getcwd(), "tests/standards/simplehostfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "pmemd.MPI",
        "executableargs":
            "-O -i example.in -c example.min -p example.top -o example.out",
        "hosts": conffile,
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "HPC1-shortqueue",
        "replicates": "",
        "verbose": False
    }

    jobs = processconfigs(parameters)

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

    conffile = os.path.join(os.getcwd(), "tests/standards/simplehostfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "pmemd.MPI",
        "executableargs":
            "-O -i example.in -c example.min -p example.top -o example.out",
        "hosts": conffile,
        "job": "",
        "jobname": "test-job",
        "log": "",
        "recover": "",
        "resource": "HPC1-shortqueue",
        "replicates": "",
        "verbose": False
    }

    jobs = processconfigs(parameters)

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

    hostfile = os.path.join(os.getcwd(), "tests/standards/simplehostfile.txt")
    jobfile = os.path.join(os.getcwd(), "tests/standards/simplejobfile.txt")

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
        "hosts": hostfile,
        "job": jobfile,
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "HPC1-shortqueue",
        "replicates": "",
        "verbose": False
    }

    jobs = processconfigs(parameters)

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
