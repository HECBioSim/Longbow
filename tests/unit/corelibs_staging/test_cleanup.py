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
This testing module contains the tests for the cleanup method within the
staging module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.staging import cleanup


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_single(mock_delete, mock_list):

    """
    Test that the correct number of function calls are made.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    cleanup(jobs)

    assert mock_delete.call_count == 1, \
        "There is only one job, this should only be called once"
    assert mock_list.call_count == 1, \
        "There is only one job, this should only be called once"


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_multiple(mock_delete, mock_list):

    """
    Test that the correct number of function calls are made.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            },
        "jobtwo": {
            "destdir": "/path/to/jobtwo12484",
            "remoteworkdir": "/path/to/local/dir"
            },
        "jobthree": {
            "destdir": "/path/to/jobthree12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    cleanup(jobs)

    assert mock_delete.call_count == 3, \
        "There is only one job, this should only be called once"
    assert mock_list.call_count == 3, \
        "There is only one job, this should only be called once"


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_params(mock_delete, mock_list):

    """
    Test the correct arguments make it to the method calls.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    cleanup(jobs)

    listarg1 = mock_list.call_args[0][0]
    deletearg1 = mock_delete.call_args[0][0]

    assert isinstance(listarg1, dict)
    assert isinstance(deletearg1, dict)


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_nodelete(mock_delete, mock_list):

    """
    Test that the following exception is handled correctly.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/jobone12484"
            }
    }

    mock_list.return_value = None
    mock_delete.return_value = None

    cleanup(jobs)

    assert mock_delete.call_count == 0, "Should not be called in this case."


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest1(mock_delete, mock_list):

    """
    Test that the listerror exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = exceptions.RemotelistError("List Error", "blah")

    cleanup(jobs)


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest2(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = KeyError("blah")

    cleanup(jobs)


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest3(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.side_effect = exceptions.RemotedeleteError("Error", "blah")
    mock_list.return_value = None

    cleanup(jobs)


@mock.patch('longbow.corelibs.shellwrappers.remotelist')
@mock.patch('longbow.corelibs.shellwrappers.remotedelete')
def test_cleanup_excepttest4(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir"
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = NameError("blah")

    cleanup(jobs)
