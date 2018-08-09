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

import pytest

from longbow.configuration import _processconfigsresource
import longbow.exceptions as ex


def test_processconfigsresource1():

    """
    Simple test with close to defaults.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    jobdata = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "",
            "memory": "",
            "scripts": "",
            "staging-frequency": "",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "",
            "sge-peoverride": "",
            "port": "",
            "queue": "",
            "remoteworkdir": "",
            "resource": "",
            "replicates": "",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    expected = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "env-fix": "false",
            "executable": "",
            "executableargs": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "mpiprocs": "",
            "nochecks": False,
            "scripts": "",
            "slurm-gres": "",
            "staging-frequency": "300",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "polling-frequency": "300",
            "port": "22",
            "queue": "",
            "recoveryfile": "",
            "remoteworkdir": "",
            "resource": "host1",
            "replicates": "1",
            "replicate-naming": "rep",
            "scheduler": "",
            "subfile": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    hostsections = ["host1", "host2", "host3"]

    jobs = _processconfigsresource(parameters, jobdata, hostsections)

    for item in jobs["LongbowJob"]:

        assert jobs["LongbowJob"][item] == expected["LongbowJob"][item]


def test_processconfigsresource2():

    """
    Test with resource on command-line.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "host2",
        "replicates": "",
        "verbose": False
    }

    jobdata = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "",
            "memory": "",
            "scripts": "",
            "staging-frequency": "",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "",
            "sge-peoverride": "",
            "port": "",
            "queue": "",
            "remoteworkdir": "",
            "resource": "",
            "replicates": "",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    expected = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "env-fix": "false",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "mpiprocs": "",
            "nochecks": False,
            "scripts": "",
            "slurm-gres": "",
            "staging-frequency": "300",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "recoveryfile": "",
            "remoteworkdir": "",
            "resource": "host2",
            "replicates": "1",
            "replicate-naming": "rep",
            "scheduler": "",
            "subfile": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    hostsections = ["host1", "host2", "host3"]

    jobs = _processconfigsresource(parameters, jobdata, hostsections)

    for item in jobs["LongbowJob"]:

        assert jobs["LongbowJob"][item] == expected["LongbowJob"][item]


def test_processconfigsresource3():

    """
    Test for defaulting when resource parameter is missing from jobdata. This
    could be for example when using jobfiles and no resource is specified
    anywhere.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    jobdata = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "",
            "memory": "",
            "scripts": "",
            "staging-frequency": "",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "",
            "sge-peoverride": "",
            "port": "",
            "queue": "",
            "remoteworkdir": "",
            "replicates": "",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    expected = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "env-fix": "false",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "mpiprocs": "",
            "nochecks": False,
            "scripts": "",
            "slurm-gres": "",
            "staging-frequency": "300",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "recoveryfile": "",
            "remoteworkdir": "",
            "resource": "host1",
            "replicates": "1",
            "replicate-naming": "rep",
            "scheduler": "",
            "subfile": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    hostsections = ["host1", "host2", "host3"]

    jobs = _processconfigsresource(parameters, jobdata, hostsections)

    for item in jobs["LongbowJob"]:

        assert jobs["LongbowJob"][item] == expected["LongbowJob"][item]


def test_processconfigsresource4():

    """
    Test for host specified in job file.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    jobdata = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "",
            "memory": "",
            "scripts": "",
            "staging-frequency": "",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "",
            "sge-peoverride": "",
            "port": "",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host3",
            "replicates": "",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    expected = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "24",
            "corespernode": "24",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "env-fix": "false",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "300",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "24:00",
            "memory": "",
            "mpiprocs": "",
            "nochecks": False,
            "scripts": "",
            "slurm-gres": "",
            "staging-frequency": "300",
            "stdout": "",
            "stderr": "",
            "sge-peflag": "mpi",
            "sge-peoverride": "false",
            "port": "22",
            "queue": "",
            "recoveryfile": "",
            "remoteworkdir": "",
            "resource": "host3",
            "replicates": "1",
            "replicate-naming": "rep",
            "scheduler": "",
            "subfile": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    hostsections = ["host1", "host2", "host3"]

    jobs = _processconfigsresource(parameters, jobdata, hostsections)

    for item in jobs["LongbowJob"]:

        assert jobs["LongbowJob"][item] == expected["LongbowJob"][item]


def test_processconfigsresource5():

    """
    Test for missing resource parameter exception.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    jobdata = {
        "LongbowJob": {
            "account": "",
            "accountflag": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "polling-frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
            "lsf-cluster": "",
            "modules": "",
            "maxtime": "",
            "memory": "",
            "scripts": "",
            "staging-frequency": "",
            "sge-peflag": "",
            "sge-peoverride": "",
            "port": "",
            "queue": "",
            "remoteworkdir": "",
            "resource": "host10",
            "replicates": "",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    hostsections = ["host1", "host2", "host3"]

    with pytest.raises(ex.ConfigurationError):

        _processconfigsresource(parameters, jobdata, hostsections)
