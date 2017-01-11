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
This testing module contains the tests for the monitorinitialise method within
the scheduling module.
"""

import Longbow.corelibs.scheduling as scheduling


def test_monitorinitialise_test1():

    """
    Test some default parameters
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "0",
            "polling-frequency": "0"
        },
        "jobtwo": {
            "resource": "test-machine",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "0",
            "polling-frequency": "0"
        }
    }

    stageintval, pollintval = scheduling._monitorinitialise(jobs)

    assert stageintval == 0, "Should be zero if staging-frequency = 0"
    assert pollintval == 300, "Should be 300 if frequency = 0"


def test_monitorinitialise_test2():

    """
    Test some default parameters
    """

    jobs = {
        "jobone": {
            "resource": "test-machine3",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "100",
            "polling-frequency": "400"
        },
        "jobtwo": {
            "resource": "test-machine3",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "0",
            "polling-frequency": "0"
        }
    }

    stageintval, pollintval = scheduling._monitorinitialise(jobs)

    assert stageintval == 100, "The highest should be used: 100"
    assert pollintval == 400, "Should be 400 if frequency = 0"
