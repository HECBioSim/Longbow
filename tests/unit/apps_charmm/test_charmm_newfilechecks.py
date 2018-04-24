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
This testing module contains basic testing for the CHARMM plugin.
"""

import pytest
import longbow.exceptions as exceptions
from longbow.apps.charmm import _newfilechecks


def test_newfilechecks_test1():

    """
    Blank test, make sure all blanks don't do anything.
    """

    addfile = ""
    newfile = ""
    path = ""

    _newfilechecks(addfile, newfile, path)


def test_newfilechecks_test2():

    """
    Check that if we have an input file in a repx directory pointing to a file
    in the job parent directory (../) that newfile returns as cwd.
    """

    addfile = "rep1/test1.file"
    newfile = "../test2.file"
    path = "path"

    newfile = _newfilechecks(addfile, newfile, path)

    assert newfile == "test2.file"


def test_newfilechecks_test3():

    """
    Check that if we have an input file in the cwd pointing to a file
    above this directory (../) that an exception is raised.
    """

    addfile = "test1.file"
    newfile = "../test2.file"
    path = "path"

    with pytest.raises(exceptions.RequiredinputError):

        _newfilechecks(addfile, newfile, path)


def test_newfilechecks_test4():

    """
    Check that if we have an input file in the cwd pointing to a file
    above this directory (../../) that an exception is raised.
    """

    addfile = "test1.file"
    newfile = "../../test2.file"
    path = "path"

    with pytest.raises(exceptions.RequiredinputError):

        _newfilechecks(addfile, newfile, path)


def test_newfilechecks_test5():

    """
    If we have a file in a repx directory refering to a file without ../ or
    rep/ in the path then it is likely to be in the same directory. Test this.
    """

    addfile = "rep1/test1.file"
    newfile = "test2.file"
    path = "path"

    newfile = _newfilechecks(addfile, newfile, path)

    assert newfile == "rep1/test2.file"


def test_newfilechecks_test6():

    """
    If we have a file in a repx directory refering to a file without ../ or
    rep/ in the path then it is likely to be in the same directory. Test again
    with a longer path
    """

    addfile = "somepath/rep1/test1.file"
    newfile = "test2.file"
    path = "path"

    newfile = _newfilechecks(addfile, newfile, path)

    assert newfile == "somepath/rep1/test2.file"


def test_newfilechecks_test7():

    """
    If we have a newfile in a repx directory referenced from within a repx
    directory then this is bogus.
    """

    addfile = "rep1/test1.file"
    newfile = "rep1/test2.file"
    path = "path"

    with pytest.raises(exceptions.RequiredinputError):

        _newfilechecks(addfile, newfile, path)


def test_newfilechecks_test8():

    """
    Test for newfile in repx.
    """

    addfile = "test1.file"
    newfile = "rep2/test2.file"
    path = "path"

    newfile = _newfilechecks(addfile, newfile, path)

    assert newfile == "rep2/test2.file"
