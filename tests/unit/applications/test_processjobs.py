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

import os

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

from longbow.applications import processjobs
import longbow.exceptions as exceptions


def _proccommandline(job, filelist, foundfile, _):

    """Quick method to mock functionality"""
    for index, arg in enumerate(job["executableargs"]):

        if arg[0] == "-":

            filelist.append(job["executableargs"][index + 1])

    return foundfile


def test_processjobs_abspath():

    """Test exception is thrown when using absolute paths on command-line."""

    jobs = {
        "jobone": {
            "executableargs": ["-flag", "/path/to/file"],
            "executable": "pmemd.MPI"
        }
    }

    with pytest.raises(exceptions.RequiredinputError):

        processjobs(jobs)


def test_processjobs_pardir():

    """
    Test exception is thrown when using paths above workdir on command-line.
    """

    jobs = {
        "jobone": {
            "executableargs": ["-flag", "../../file"],
            "executable": "pmemd.MPI"
        }
    }

    with pytest.raises(exceptions.RequiredinputError):

        processjobs(jobs)


@mock.patch('longbow.applications._proccommandline')
@mock.patch('longbow.applications._flagvalidator')
def test_processjobs_singlejob1(m_validator, m_proccommandline):

    """Test for single job, make sure parameters are all set correctly."""

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "tests/standards/jobs/single"),
            "executable": "/some/path/pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    m_proccommandline.side_effect = _proccommandline

    m_validator.return_value = None

    processjobs(jobs)

    assert jobs["jobone"]["upload-exclude"] == "*"
    assert jobs["jobone"]["localworkdir"] == os.path.join(
        os.getcwd(), "tests/standards/jobs/single")
    assert jobs["jobone"]["executableargs"] == \
        "/some/path/pmemd.MPI -i input -c coords -p topol"
    assert jobs["jobone"]["upload-include"] == "input, coords, topol"


@mock.patch('longbow.applications._proccommandline')
@mock.patch('longbow.applications._flagvalidator')
def test_processjobs_singlejob2(m_validator, m_proccommandline):

    """Test for single job, make sure parameters are all set correctly."""

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "tests/standards/jobs/single"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    m_proccommandline.side_effect = _proccommandline

    m_validator.return_value = None

    processjobs(jobs)

    assert jobs["jobone"]["upload-exclude"] == "*"
    assert jobs["jobone"]["localworkdir"] == os.path.join(
        os.getcwd(), "tests/standards/jobs/single")
    assert jobs["jobone"]["executableargs"] == \
        "pmemd.MPI -i input -c coords -p topol"
    assert jobs["jobone"]["upload-include"] == "input, coords, topol"


@mock.patch('longbow.applications._proccommandline')
@mock.patch('longbow.applications._flagvalidator')
def test_processjobs_multijob(m_validator, m_proccommandline):

    """Test for multi job, make sure parameters are all set correctly."""

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "tests/standards/jobs/multi"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        },
        "jobtwo": {
            "executableargs": ["-i", "inp", "-c", "coord", "-p", "top"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "tests/standards/jobs/multi"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    m_proccommandline.side_effect = _proccommandline

    m_validator.return_value = None

    processjobs(jobs)

    assert jobs["jobone"]["upload-exclude"] == "*"
    assert jobs["jobone"]["localworkdir"] == os.path.join(
        os.getcwd(), "tests/standards/jobs/multi/jobone")
    assert jobs["jobone"]["executableargs"] == \
        "pmemd.MPI -i input -c coords -p topol"
    assert jobs["jobone"]["upload-include"] == "input, coords, topol"

    assert jobs["jobtwo"]["upload-exclude"] == "*"
    assert jobs["jobtwo"]["localworkdir"] == os.path.join(
        os.getcwd(), "tests/standards/jobs/multi/jobtwo")
    assert jobs["jobtwo"]["executableargs"] == \
        "pmemd.MPI -i inp -c coord -p top"
    assert jobs["jobtwo"]["upload-include"] == "inp, coord, top"


def test_processjobs_direxcept():

    """Test exception is thrown when job directory is missing."""

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "tests/standards/jobs/error"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    with pytest.raises(exceptions.DirectorynotfoundError):

        processjobs(jobs)


@mock.patch('longbow.applications._proccommandline')
@mock.patch('longbow.applications._flagvalidator')
def test_processjobs_include(m_validator, m_proccommandline):

    """Test that if user has provided upload-includes that they don't get
    overriden.
    """

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "tests/standards/jobs/single"),
            "executable": "pmemd.MPI",
            "upload-include": "test.file",
            "upload-exclude": ""
        }
    }

    m_proccommandline.side_effect = _proccommandline

    m_validator.return_value = None

    processjobs(jobs)

    assert jobs["jobone"]["upload-include"] == \
        "test.file, input, coords, topol"


def test_processjobs_genericexec1():

    """
    Test that the generic executable case works with hard path
    """

    jobs = {
        "jobone": {
            "executableargs": ["-f", "input", "-c", "file", "-p", "test"],
            "localworkdir": os.getcwd(),
            "executable": "/opt/somesoftware/exec",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    processjobs(jobs)

    assert jobs["jobone"]["executableargs"] == \
        "/opt/somesoftware/exec -f input -c file -p test"
    assert jobs["jobone"]["upload-include"] == ""
    assert jobs["jobone"]["upload-exclude"] == "*.log"


def test_processjobs_genericexec2():

    """
    Test that the generic executable case works with module and exec only.
    """

    jobs = {
        "jobone": {
            "executableargs": ["-f", "input", "-c", "file", "-p", "test"],
            "localworkdir": os.getcwd(),
            "executable": "testexec",
            "upload-include": "",
            "upload-exclude": "",
            "modules": "testsoftware"
        }
    }

    processjobs(jobs)

    assert jobs["jobone"]["executableargs"] == \
        "testexec -f input -c file -p test"
    assert jobs["jobone"]["upload-include"] == ""
    assert jobs["jobone"]["upload-exclude"] == "*.log"
