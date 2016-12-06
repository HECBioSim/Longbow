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
This testing module contains the tests for the applications module methods.
"""

import os

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.applications as apps
import Longbow.corelibs.exceptions as exceptions


def _proccommandline(job, filelist):

    """Quick method to mock functionality"""
    for index, arg in enumerate(job["executableargs"]):

        if arg[0] == "-":

            filelist.append(job["executableargs"][index + 1])

    return []


def test_processjobs_abspath():

    """Test exception is thrown when using absolute paths on command-line."""

    jobs = {
        "jobone": {
            "executableargs": ["-flag", "/path/to/file"]
        }
    }

    with pytest.raises(exceptions.RequiredinputError):

        apps.processjobs(jobs)


def test_processjobs_pardir():

    """
    Test exception is thrown when using paths above workdir on command-line.
    """

    jobs = {
        "jobone": {
            "executableargs": ["-flag", "../../file"]
        }
    }

    with pytest.raises(exceptions.RequiredinputError):

        apps.processjobs(jobs)


@mock.patch('Longbow.corelibs.applications._proccommandline')
@mock.patch('Longbow.corelibs.applications._flagvalidator')
def test_processjobs_singlejob(m_validator, m_proccommandline):

    """Test for single job, make sure parameters are all set correctly."""

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "Tests/standards/jobs/single"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    m_proccommandline.side_effect = _proccommandline

    m_validator.return_value = None

    apps.processjobs(jobs)

    assert jobs["jobone"]["upload-exclude"] == "*"
    assert jobs["jobone"]["localworkdir"] == os.path.join(
        os.getcwd(), "Tests/standards/jobs/single")
    assert jobs["jobone"]["executableargs"] == \
        "pmemd.MPI -i input -c coords -p topol"
    assert jobs["jobone"]["upload-include"] == "input, coords, topol"


@mock.patch('Longbow.corelibs.applications._proccommandline')
@mock.patch('Longbow.corelibs.applications._flagvalidator')
def test_processjobs_multijob(m_validator, m_proccommandline):

    """Test for multi job, make sure parameters are all set correctly."""

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "Tests/standards/jobs/multi"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        },
        "jobtwo": {
            "executableargs": ["-i", "inp", "-c", "coord", "-p", "top"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "Tests/standards/jobs/multi"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    m_proccommandline.side_effect = _proccommandline

    m_validator.return_value = None

    apps.processjobs(jobs)

    assert jobs["jobone"]["upload-exclude"] == "*"
    assert jobs["jobone"]["localworkdir"] == os.path.join(
        os.getcwd(), "Tests/standards/jobs/multi/jobone")
    assert jobs["jobone"]["executableargs"] == \
        "pmemd.MPI -i input -c coords -p topol"
    assert jobs["jobone"]["upload-include"] == "input, coords, topol"

    assert jobs["jobtwo"]["upload-exclude"] == "*"
    assert jobs["jobtwo"]["localworkdir"] == os.path.join(
        os.getcwd(), "Tests/standards/jobs/multi/jobtwo")
    assert jobs["jobtwo"]["executableargs"] == \
        "pmemd.MPI -i inp -c coord -p top"
    assert jobs["jobtwo"]["upload-include"] == "inp, coord, top"


def test_processjobs_direxcept():

    """Test exception is thrown when job directory is missing."""

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "Tests/standards/jobs/error"),
            "executable": "pmemd.MPI",
            "upload-include": "",
            "upload-exclude": ""
        }
    }

    with pytest.raises(exceptions.DirectorynotfoundError):

        apps.processjobs(jobs)


@mock.patch('Longbow.corelibs.applications._proccommandline')
@mock.patch('Longbow.corelibs.applications._flagvalidator')
def test_processjobs_include(m_validator, m_proccommandline):

    """Test that if user has provided upload-includes that they don't get
    overriden.
    """

    jobs = {
        "jobone": {
            "executableargs": ["-i", "input", "-c", "coords", "-p", "topol"],
            "localworkdir": os.path.join(os.getcwd(),
                                         "Tests/standards/jobs/single"),
            "executable": "pmemd.MPI",
            "upload-include": "test.file",
            "upload-exclude": ""
        }
    }

    m_proccommandline.side_effect = _proccommandline

    m_validator.return_value = None

    apps.processjobs(jobs)

    assert jobs["jobone"]["upload-include"] == \
        "test.file, input, coords, topol"
