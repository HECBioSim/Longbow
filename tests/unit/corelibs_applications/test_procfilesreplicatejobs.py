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

from longbow.corelibs.applications import _procfilesreplicatejobs


def test_procfilesreplicatejobs_t1():

    """
    Test that the input file within the repx directory can be found.
    """

    app = "amber"
    arg = "input"
    cwd = os.path.join(os.getcwd(), "tests/standards/jobs/replicate")
    initargs = ["-i", "input", "-c", "coords", "-p", "topol"]
    rep = 1

    fileitem = _procfilesreplicatejobs(app, arg, cwd, initargs, rep)

    assert fileitem == "rep1/input"
    assert initargs[1] == "input"


def test_procfilesreplicatejobs_t2():

    """
    Test that the input file within cwd is found.
    """

    app = "amber"
    arg = "topol"
    cwd = os.path.join(os.getcwd(), "tests/standards/jobs/replicate")
    initargs = ["-i", "input", "-c", "coords", "-p", "topol"]
    rep = 1

    fileitem = _procfilesreplicatejobs(app, arg, cwd, initargs, rep)

    assert fileitem == "topol"
    assert initargs[5] == "../topol"


def test_procfilesreplicatejobs_t3():

    """
    Test that the input file within cwd is found.
    """

    app = "amber"
    arg = "test"
    cwd = os.path.join(os.getcwd(), "tests/standards/jobs/replicate")
    initargs = ["-i", "input", "-c", "coords", "-p", "topol"]
    rep = 1

    fileitem = _procfilesreplicatejobs(app, arg, cwd, initargs, rep)

    assert fileitem == ""


def test_procfilesreplicatejobs_t4():

    """
    Test a real application hook to see if this works.
    """

    app = "gromacs"
    arg = "test"
    cwd = os.path.join(os.getcwd(), "tests/standards/jobs/replicate")
    initargs = ["-deffnm", "test"]
    rep = 2

    fileitem = _procfilesreplicatejobs(app, arg, cwd, initargs, rep)

    assert fileitem == "rep2/test.tpr"


@mock.patch('os.mkdir')
def test_procfilesreplicatejobs_t5(m_mkdir):

    """
    Test a real application hook to see if this works.
    """

    app = "gromacs"
    arg = "test"
    cwd = os.path.join(os.getcwd(), "tests/standards/jobs/replicate")
    initargs = ["-deffnm", "test"]
    rep = 4

    fileitem = _procfilesreplicatejobs(app, arg, cwd, initargs, rep)

    assert m_mkdir.call_count == 1
    assert fileitem == ""
