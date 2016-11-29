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

import pytest

import Longbow.corelibs.configuration as conf
import Longbow.corelibs.exceptions as ex


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
            "cluster": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
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
        }
    }

    hostsections = ["host1", "host2", "host3"]

    jobs = conf._processconfigsresource(parameters, jobdata, hostsections)

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
            "cluster": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
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
            "resource": "host2",
            "replicates": "1",
            "scheduler": "",
            "user": "",
            "upload-exclude": "",
            "upload-include": ""
        }
    }

    hostsections = ["host1", "host2", "host3"]

    jobs = conf._processconfigsresource(parameters, jobdata, hostsections)

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
            "cluster": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
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
        }
    }

    hostsections = ["host1", "host2", "host3"]

    jobs = conf._processconfigsresource(parameters, jobdata, hostsections)

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
            "cluster": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
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

    hostsections = ["host1", "host2", "host3"]

    jobs = conf._processconfigsresource(parameters, jobdata, hostsections)

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
            "cluster": "",
            "cores": "",
            "corespernode": "",
            "download-exclude": "",
            "download-include": "",
            "email-address": "",
            "email-flags": "",
            "executable": "",
            "executableargs": "",
            "frequency": "",
            "handler": "",
            "host": "",
            "localworkdir": "",
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

        conf._processconfigsresource(parameters, jobdata, hostsections)
