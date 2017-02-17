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
This testing module contains the tests for the _checkcomplete method within
the scheduling module.
"""

import Longbow.corelibs.scheduling as scheduling


def test_checkcomplete_single1():

    """
    Check that a running job doesn't let longbow exit
    """

    jobs = {
        "jobone": {
            "laststatus": "Running"
        }
    }

    complete, finished = scheduling._checkcomplete(jobs)

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

    complete, finished = scheduling._checkcomplete(jobs)

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

    complete, finished = scheduling._checkcomplete(jobs)

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

    complete, finished = scheduling._checkcomplete(jobs)

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

    complete, finished = scheduling._checkcomplete(jobs)

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

    complete, finished = scheduling._checkcomplete(jobs)

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

    complete, finished = scheduling._checkcomplete(jobs)

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

    complete, finished = scheduling._checkcomplete(jobs)

    assert finished is False
    assert complete is True
