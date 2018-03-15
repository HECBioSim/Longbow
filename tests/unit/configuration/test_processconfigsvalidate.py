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

from longbow.configuration import _processconfigsvalidate
import longbow.exceptions as ex


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

        _processconfigsvalidate(jobs)


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

        _processconfigsvalidate(jobs)


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

        _processconfigsvalidate(jobs)


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

        _processconfigsvalidate(jobs)


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

        _processconfigsvalidate(jobs)


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

        _processconfigsvalidate(jobs)
