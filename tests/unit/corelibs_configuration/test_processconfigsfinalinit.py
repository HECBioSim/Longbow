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
This testing module contains the tests for the configuration module methods.
"""

import os
import Longbow.corelibs.configuration as conf


def test_processconfigsfinalinit1():

    """
    """

    jobs = {
        "jobone": {
            "modules": "",
            "localworkdir": "/somepath/to/dir",
            "executableargs": "arg1 arg2 arg3",
            "executable": "pmemd.MPI",
            "remoteworkdir": "/work/dir"
        },
        "jobtwo": {
            "modules": "",
            "localworkdir": "",
            "executableargs": "-a --arg2 arg3",
            "executable": "gmx",
            "remoteworkdir": "/work/dir"
        }
    }

    conf._processconfigsfinalinit(jobs)

    assert jobs["jobone"]["localworkdir"] == "/somepath/to/dir"
    assert jobs["jobone"]["executableargs"] == ["arg1", "arg2", "arg3"]
    assert jobs["jobone"]["executable"] == "pmemd.MPI"
    assert jobs["jobone"]["destdir"] != ""
    assert jobs["jobone"]["remoteworkdir"] == "/work/dir"
    assert jobs["jobone"]["modules"] == "amber"

    assert jobs["jobtwo"]["localworkdir"] == os.getcwd()
    assert jobs["jobtwo"]["executableargs"] == ["-a", "--arg2", "arg3"]
    assert jobs["jobtwo"]["executable"] == "gmx"
    assert jobs["jobtwo"]["destdir"] != ""
    assert jobs["jobtwo"]["remoteworkdir"] == "/work/dir"
    assert jobs["jobtwo"]["modules"] == "gromacs"
