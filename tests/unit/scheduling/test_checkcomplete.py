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
This testing module contains the tests for the _checkcomplete method within
the scheduling module.
"""

from longbow.scheduling import _checkcomplete


def test_checkcomplete_single1():

    """
    Check that a running job doesn't let longbow exit
    """

    jobs = {
        "jobone": {
            "laststatus": "Running"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is False
    assert complete is False


def test_checkcomplete_single2():

    """
    Check that a running job doesn't let longbow exit
    """

    jobs = {
        "jobone": {
            "laststatus": "Finished"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is True
    assert complete is False


def test_checkcomplete_single3():

    """
    Check that a complete job triggers completion.
    """

    jobs = {
        "jobone": {
            "laststatus": "Complete"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is False
    assert complete is True


def test_checkcomplete_multi1():

    """
    Check that a running job doesn't let longbow exit
    """

    jobs = {
        "jobone": {
            "laststatus": "Running"
        },
        "jobtwo": {
            "laststatus": "Finished"
        },
        "jobthree": {
            "laststatus": "Complete"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is False
    assert complete is False


def test_checkcomplete_multi2():

    """
    Check that a complete job triggers completion.
    """

    jobs = {
        "jobone": {
            "laststatus": "Finished"
        },
        "jobtwo": {
            "laststatus": "Finished"
        },
        "jobthree": {
            "laststatus": "Finished"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is True
    assert complete is False


def test_checkcomplete_multi3():

    """
    Check that a complete job triggers completion.
    """

    jobs = {
        "jobone": {
            "laststatus": "Complete"
        },
        "jobtwo": {
            "laststatus": "Complete"
        },
        "jobthree": {
            "laststatus": "Complete"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is False
    assert complete is True


def test_checkcomplete_multi4():

    """
    Check that submit error is ignored.
    """

    jobs = {
        "jobone": {
            "laststatus": "Submit Error"
        },
        "jobtwo": {
            "laststatus": "Complete"
        },
        "jobthree": {
            "laststatus": "Complete"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is False
    assert complete is True


def test_checkcomplete_multi5():

    """
    Check that submit error is ignored.
    """

    jobs = {
        "jobone": {
            "laststatus": "Submit Error"
        },
        "jobtwo": {
            "laststatus": "Submit Error"
        },
        "jobthree": {
            "laststatus": "Submit Error"
        }
    }

    complete, finished = _checkcomplete(jobs)

    assert finished is False
    assert complete is True
