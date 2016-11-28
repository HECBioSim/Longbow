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
This testing module contains basic testing for the NAMD plugin.
"""

import pytest
import Longbow.corelibs.exceptions as exceptions
import Longbow.apps.namd as namd


def test_newfilechecks_test1():

    """
    Blank test, make sure all blanks don't do anything.
    """

    addfile = ""
    newfile = ""
    path = ""

    namd._newfilechecks(addfile, newfile, path)


def test_newfilechecks_test2():

    """
    Check that if we have an input file in a repx directory pointing to a file
    in the job parent directory (../) that newfile returns as cwd.
    """

    addfile = "rep1/test1.file"
    newfile = "../test2.file"
    path = "path"

    newfile = namd._newfilechecks(addfile, newfile, path)

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

        namd._newfilechecks(addfile, newfile, path)

def test_newfilechecks_test4():

    """
    Check that if we have an input file in the cwd pointing to a file
    above this directory (../../) that an exception is raised.
    """

    addfile = "test1.file"
    newfile = "../../test2.file"
    path = "path"

    with pytest.raises(exceptions.RequiredinputError):

        namd._newfilechecks(addfile, newfile, path)


def test_newfilechecks_test5():

    """
    If we have a file in a repx directory refering to a file without ../ or
    rep/ in the path then it is likely to be in the same directory. Test this.
    """

    addfile = "rep1/test1.file"
    newfile = "test2.file"
    path = "path"

    newfile = namd._newfilechecks(addfile, newfile, path)

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

    newfile = namd._newfilechecks(addfile, newfile, path)

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

        namd._newfilechecks(addfile, newfile, path)


def test_newfilechecks_test8():

    """
    Test for newfile in repx.
    """

    addfile = "test1.file"
    newfile = "rep2/test2.file"
    path = "path"

    newfile = namd._newfilechecks(addfile, newfile, path)

    assert newfile == "rep2/test2.file"
