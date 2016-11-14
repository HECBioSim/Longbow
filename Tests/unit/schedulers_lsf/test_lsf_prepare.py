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
This test module contains tests for the LSF scheduler plugin.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest
import os

import Longbow.corelibs.exceptions as exceptions
import Longbow.schedulers.lsf as lsf


def test_prepare_case1():

    """
    """

    jobfile = open("/tmp/submit.lsf", "w+")

    jobfile.write("line 1\n")
    jobfile.write("line 2\n")
    jobfile.write("line 3")

    jobfile.close()

    assert open("/tmp/submit.lsf", "rb").read() == open(os.path.join(os.getcwd(), "Tests/standards/testcase1.txt"), "rb").read()
