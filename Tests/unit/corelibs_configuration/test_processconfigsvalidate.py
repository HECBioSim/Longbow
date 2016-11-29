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


def test_validate_test1():

    """
    Test to make sure that if the 'executable' is empty throw an exception.
    """

    jobs = {
        "testjob": {
            "executable": "",
            "executableargs": "arg1 arg2 arg3",
            "host": "login.machine.ac.uk",
            "user": "user",
            "remoteworkdir": "/work/dir",
            "replicates": "1"
        }
    }

    with pytest.raises(ex.ConfigurationError):

        conf._processconfigsvalidate(jobs)


def test_validate_test2():

    """
    Test to make sure that if the 'executableargs' is empty throw an exception.
    """

    jobs = {
        "testjob": {
            "executable": "testexec",
            "executableargs": "",
            "host": "login.machine.ac.uk",
            "user": "user",
            "remoteworkdir": "/work/dir",
            "replicates": "1"
        }
    }

    with pytest.raises(ex.ConfigurationError):

        conf._processconfigsvalidate(jobs)


def test_validate_test3():

    """
    Test to make sure that if the 'host' is empty throw an exception.
    """

    jobs = {
        "testjob": {
            "executable": "testexec",
            "executableargs": "arg1 arg2 arg3",
            "host": "",
            "user": "user",
            "remoteworkdir": "/work/dir",
            "replicates": "1"
        }
    }

    with pytest.raises(ex.ConfigurationError):

        conf._processconfigsvalidate(jobs)


def test_validate_test4():

    """
    Test to make sure that if the 'user' is empty throw an exception.
    """

    jobs = {
        "testjob": {
            "executable": "testexec",
            "executableargs": "arg1 arg2 arg3",
            "host": "login.machine.ac.uk",
            "user": "",
            "remoteworkdir": "/work/dir",
            "replicates": "1"
        }
    }

    with pytest.raises(ex.ConfigurationError):

        conf._processconfigsvalidate(jobs)


def test_validate_test5():

    """
    Test to make sure that if the 'remoteworkdir' is empty throw an exception.
    """

    jobs = {
        "testjob": {
            "executable": "testexec",
            "executableargs": "arg1 arg2 arg3",
            "host": "login.machine.ac.uk",
            "user": "user",
            "remoteworkdir": "",
            "replicates": "1"
        }
    }

    with pytest.raises(ex.ConfigurationError):

        conf._processconfigsvalidate(jobs)


def test_validate_test6():

    """
    Test to make sure that if the 'replicates' is empty throw an exception.
    """

    jobs = {
        "testjob": {
            "executable": "testexec",
            "executableargs": "arg1 arg2 arg3",
            "host": "login.machine.ac.uk",
            "user": "user",
            "remoteworkdir": "/work/dir",
            "replicates": ""
        }
    }

    with pytest.raises(ex.ConfigurationError):

        conf._processconfigsvalidate(jobs)
