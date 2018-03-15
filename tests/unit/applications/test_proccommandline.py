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
This testing module contains the tests for the applications module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

from longbow.applications import _proccommandline
import longbow.exceptions as exceptions


@mock.patch('longbow.applications._procfiles')
def test_proccommandline_test1(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["<", "input.file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 1
    assert m_procfiles.call_args[0][1] == "input.file"


@mock.patch('longbow.applications._procfiles')
def test_proccommandline_test2(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["-c", "file", "-i", "file", "-p", "file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 3
    assert m_procfiles.call_args[0][1] == "file"


@mock.patch('longbow.applications._procfiles')
def test_proccommandline_test3(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "gmx",
        "executableargs": ["mdrun_mpi", "-deffnm", "filename"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 1
    assert m_procfiles.call_args[0][1] == "filename"


@mock.patch('longbow.applications._procfiles')
def test_proccommandline_test4(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "charmm",
        "executableargs": ["input.file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 1
    assert m_procfiles.call_args[0][1] == "input.file"


@mock.patch('longbow.applications._procfiles')
def test_proccommandline_test5(m_procfiles):

    """
    Test that the correct method is selected based on the command-line.
    """

    job = {
        "executable": "namd2",
        "executableargs": ["input.file", ">", "output.file"]
    }

    _proccommandline(job, [], [], {})

    assert m_procfiles.call_count == 2
    assert m_procfiles.call_args[0][1] == "output.file"


def test_proccommandline_except():

    """
    Test if the exception is raised if command-line is bad.
    """

    job = {
        "executable": "pmemd.MPI",
        "executableargs": ["", "", ""],
        "jobname": "jobone"
    }

    with pytest.raises(exceptions.RequiredinputError):

        _proccommandline(job, [], [], {})
