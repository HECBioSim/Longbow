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
This testing module contains the tests for the main method within the
entrypoint module.
"""

import os

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.entrypoints import _jobfileproc


@mock.patch("os.path.isfile")
def test_jobfileproc_test1(m_isfile):

    """
    Test for job file in the current working directory
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "job.conf",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    m_isfile.side_effect = [True]

    _jobfileproc(parameters)

    assert parameters["job"] == os.path.join(os.getcwd(), "job.conf")


@mock.patch("os.path.isfile")
def test_hostfileproc_test2(m_isfile):

    """
    Check that the exception gets raised if nothing can be found.
    """

    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": [],
        "hosts": "",
        "job": "job.conf",
        "jobname": "",
        "log": "",
        "recover": "",
        "resource": "",
        "replicates": "",
        "verbose": False
    }

    m_isfile.side_effect = [False]

    with pytest.raises(exceptions.RequiredinputError):

        _jobfileproc(parameters)
