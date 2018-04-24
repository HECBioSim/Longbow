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
This testing module contains the tests for the monitorinitialise method within
the scheduling module.
"""

from longbow.scheduling import _monitorinitialise


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

    stageintval, pollintval = _monitorinitialise(jobs)

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

    stageintval, pollintval = _monitorinitialise(jobs)

    assert stageintval == 100, "The highest should be used: 100"
    assert pollintval == 400, "Should be 400 if frequency = 0"
