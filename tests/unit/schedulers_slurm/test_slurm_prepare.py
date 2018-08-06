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
This test module contains tests for the slurm scheduler plugin.
"""

import os
from longbow.schedulers.slurm import prepare


def test_prepare_case1():

    """
    Simple test
    """

    job = {
        "account": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "",
        "stderr": "",
        "scripts": "",
        "slurm-gres": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert job["subfile"] == "submit.slurm"
    assert job["upload-include"] == "file1, file2, submit.slurm"
    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case1.txt"), "rb").read()


def test_prepare_case2():

    """
    Test replicates
    """

    job = {
        "account": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "5",
        "stdout": "",
        "stderr": "",
        "scripts": "",
        "slurm-gres": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case2.txt"), "rb").read()


def test_prepare_case3():

    """
    Test account parameter
    """

    job = {
        "account": "accno1234",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "",
        "stderr": "",
        "scripts": "",
        "slurm-gres": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case3.txt"), "rb").read()


def test_prepare_case4():

    """
    Test account parameter
    """

    job = {
        "account": "accno1234",
        "accountflag": "-P",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "",
        "stderr": "",
        "scripts": "",
        "slurm-gres": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case4.txt"), "rb").read()


def test_prepare_case5():

    """
    Test email parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "test.email@server.com",
        "email-flags": "bn",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "",
        "stderr": "",
        "scripts": "",
        "slurm-gres": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case5.txt"), "rb").read()


def test_prepare_case6():

    """
    Test script parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "",
        "stderr": "",
        "scripts": "ls /dir, cd /dir",
        "slurm-gres": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case6.txt"), "rb").read()


def test_prepare_case7():

    """
    Test gres parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "",
        "stderr": "",
        "scripts": "ls /dir, cd /dir",
        "slurm-gres": "gpu:1",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case7.txt"), "rb").read()


def test_prepare_case8():

    """
    Test gres parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "10",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "",
        "stderr": "",
        "scripts": "ls /dir, cd /dir",
        "slurm-gres": "gpu:1",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case8.txt"), "rb").read()


def test_prepare_case9():

    """
    Simple test
    """

    job = {
        "account": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "mpirun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "stdout": "test.log",
        "stderr": "test.err",
        "scripts": "",
        "slurm-gres": "",
        "sge-peflag": "mpi",
        "sge-peoverride": "false",
        "upload-include": "file1, file2"
    }

    prepare(job)

    assert job["subfile"] == "submit.slurm"
    assert job["upload-include"] == "file1, file2, submit.slurm"
    assert open("/tmp/submit.slurm", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "tests/standards/slurm_submitfiles/case9.txt"), "rb").read()
