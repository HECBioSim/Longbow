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

import Longbow.corelibs.configuration as conf


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

    conf._processconfigsparams(jobs, parameters, jobdata, hostdata)

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

    conf._processconfigsparams(jobs, parameters, jobdata, hostdata)

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

    conf._processconfigsparams(jobs, parameters, jobdata, hostdata)

    assert jobs["jobone"]["cores"] == "48"
    assert jobs["jobtwo"]["cores"] == "96"
