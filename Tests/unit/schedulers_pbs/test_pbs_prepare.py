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
This test module contains tests for the PBS scheduler plugin.
"""

import os
import Longbow.schedulers.pbs as pbs


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
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert job["subfile"] == "submit.pbs"
    assert job["upload-include"] == "file1, file2, submit.pbs"
    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case1.txt"), "rb").read()


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
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case2.txt"), "rb").read()


def test_prepare_case3():

    """
    Test undersubscription
    """

    job = {
        "account": "",
        "cluster": "cluster1",
        "cores": "16",
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
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case3.txt"), "rb").read()


def test_prepare_case4():

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
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case4.txt"), "rb").read()


def test_prepare_case5():

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
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case5.txt"), "rb").read()


def test_prepare_case6():

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
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case6.txt"), "rb").read()


def test_prepare_case7():

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
        "scripts": "ls /dir, cd /dir",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case7.txt"), "rb").read()


def test_prepare_case8():

    """
    Test handler parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "aprun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case8.txt"), "rb").read()


def test_prepare_case9():

    """
    Test memory parameters
    """

    job = {
        "account": "",
        "accountflag": "",
        "cluster": "",
        "cores": "24",
        "corespernode": "24",
        "executableargs": "pmemd.MPI -O -i e.in -c e.min -p e.top -o e.out",
        "handler": "aprun",
        "email-address": "",
        "email-flags": "",
        "jobname": "testjob",
        "localworkdir": "/tmp",
        "maxtime": "24:00",
        "memory": "8",
        "modules": "amber",
        "queue": "debug",
        "replicates": "1",
        "scripts": "",
        "upload-include": "file1, file2"
    }

    pbs.prepare(job)

    assert open("/tmp/submit.pbs", "rb").read() == open(
        os.path.join(
            os.getcwd(),
            "Tests/standards/pbs_submitfiles/case9.txt"), "rb").read()
