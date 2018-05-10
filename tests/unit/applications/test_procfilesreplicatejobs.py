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

from longbow.applications import _procfilesreplicatejobs


def test_procfilesreplicatejobs_t1():

    """
    Test that the input file within the repx directory can be found.
    """

    app = "amber"
    arg = "input"
    cwd = os.path.join(os.getcwd(), "tests/standards/jobs/replicate")
    initargs = ["-i", "input", "-c", "coords", "-p", "topol"]
    rep = "rep1"

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
    rep = "rep1"

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
    rep = "rep1"

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
    rep = "rep2"

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
    rep = "rep4"

    fileitem = _procfilesreplicatejobs(app, arg, cwd, initargs, rep)

    assert m_mkdir.call_count == 1
    assert fileitem == ""
