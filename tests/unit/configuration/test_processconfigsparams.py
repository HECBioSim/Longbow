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

from longbow.configuration import _processconfigsparams


def test_processconfigsparams_test1():

    """
    Test that the commad-line parameters override everything else.
    """

    jobs = {
        "jobone": {
            "account": "",
            "accountflag": "",
            "cluster": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "scripts": "",
            "staging-frequency": "300",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host1",
            "replicates": "1",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        },
        "jobtwo": {
            "account": "",
            "accountflag": "",
            "cluster": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "scripts": "",
            "staging-frequency": "300",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host3",
            "replicates": "1",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "test.exec",
        "executableargs": "",
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    hostdata = {
        "host1": {
            "executable": "host1.exec"
        },
        "host2": {
            "executable": "host2.exec"
        },
        "host3": {
            "executable": "host3.exec"
        }
    }

    jobdata = {
        "jobone": {
            "executable": "job1.exec"
        },
        "jobtwo": {
            "executable": "job2.exec"
        }
    }

    _processconfigsparams(jobs, parameters, jobdata, hostdata)

    assert jobs["jobone"]["executable"] == "test.exec"
    assert jobs["jobtwo"]["executable"] == "test.exec"


def test_processconfigsparams_test2():

    """
    Test that the parameters in job file override those in host files.
    """

    jobs = {
        "jobone": {
            "account": "",
            "accountflag": "",
            "cluster": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "scripts": "",
            "staging-frequency": "300",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host1",
            "replicates": "1",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        },
        "jobtwo": {
            "account": "",
            "accountflag": "",
            "cluster": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "scripts": "",
            "staging-frequency": "300",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host3",
            "replicates": "1",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    hostdata = {
        "host1": {
            "executable": "host1.exec"
        },
        "host2": {
            "executable": "host2.exec"
        },
        "host3": {
            "executable": "host3.exec"
        }
    }

    jobdata = {
        "jobone": {
            "executable": "job1.exec",
            "executableargs": "-i example.in -c example.rst -p example.top"
        },
        "jobtwo": {
            "executable": "job2.exec",
            "executableargs": "-i example.in -c example.rst -p example.top"
        }
    }

    _processconfigsparams(jobs, parameters, jobdata, hostdata)

    assert jobs["jobone"]["executable"] == "job1.exec"
    assert jobs["jobone"]["executableargs"] == \
        "-i example.in -c example.rst -p example.top"
    assert jobs["jobtwo"]["executable"] == "job2.exec"
    assert jobs["jobtwo"]["executableargs"] == \
        "-i example.in -c example.rst -p example.top"


def test_processconfigsparams_test3():

    """
    Test that hosts parameters override defaults.
    """

    jobs = {
        "jobone": {
            "account": "",
            "accountflag": "",
            "cluster": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "scripts": "",
            "staging-frequency": "300",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host1",
            "replicates": "1",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        },
        "jobtwo": {
            "account": "",
            "accountflag": "",
            "cluster": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "scripts": "",
            "staging-frequency": "300",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host3",
            "replicates": "1",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    hostdata = {
        "host1": {
            "executable": "host1.exec",
            "cores": "48"
        },
        "host2": {
            "executable": "host2.exec",
            "cores": "72"
        },
        "host3": {
            "executable": "host3.exec",
            "cores": "96"
        }
    }

    jobdata = {
        "jobone": {
            "executable": "job1.exec"
        },
        "jobtwo": {
            "executable": "job2.exec"
        }
    }

    _processconfigsparams(jobs, parameters, jobdata, hostdata)

    assert jobs["jobone"]["cores"] == "48"
    assert jobs["jobtwo"]["cores"] == "96"
