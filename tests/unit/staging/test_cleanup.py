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
This testing module contains the tests for the cleanup method within the
staging module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import longbow.exceptions as exceptions
from longbow.staging import cleanup


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_single(mock_delete, mock_list):

    """
    Test that the correct number of function calls are made.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    cleanup(jobs)

    assert mock_delete.call_count == 1, \
        "There is only one job, this should only be called once"
    assert mock_list.call_count == 1, \
        "There is only one job, this should only be called once"


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_multiple(mock_delete, mock_list):

    """
    Test that the correct number of function calls are made.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            },
        "jobtwo": {
            "destdir": "/path/to/jobtwo12484",
            "remoteworkdir": "/path/to/local/dir",
            },
        "jobthree": {
            "destdir": "/path/to/jobthree12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    cleanup(jobs)

    assert mock_delete.call_count == 3, \
        "There is only one job, this should only be called once"
    assert mock_list.call_count == 3, \
        "There is only one job, this should only be called once"


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_params(mock_delete, mock_list):

    """
    Test the correct arguments make it to the method calls.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    cleanup(jobs)

    listarg1 = mock_list.call_args[0][0]
    deletearg1 = mock_delete.call_args[0][0]

    assert isinstance(listarg1, dict)
    assert isinstance(deletearg1, dict)


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_nodelete(mock_delete, mock_list):

    """
    Test that the following exception is handled correctly.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/jobone12484",
            }
    }

    mock_list.return_value = None
    mock_delete.return_value = None

    cleanup(jobs)

    assert mock_delete.call_count == 0, "Should not be called in this case."


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_excepttest1(mock_delete, mock_list):

    """
    Test that the listerror exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = exceptions.RemotelistError("List Error", "blah")

    cleanup(jobs)


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_excepttest2(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = KeyError("blah")

    cleanup(jobs)


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_excepttest3(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    mock_delete.side_effect = exceptions.RemotedeleteError("Error", "blah")
    mock_list.return_value = None

    cleanup(jobs)


@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_excepttest4(mock_delete, mock_list):

    """
    Test that the KeyError exception is entercepted and does not percolate
    up from here.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    mock_delete.return_value = None
    mock_list.side_effect = NameError("blah")

    cleanup(jobs)


@mock.patch('os.remove')
@mock.patch('os.path.isfile')
@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_recoveryfilerm1(m_delete, m_list, m_isfile, m_remove):

    """
    Test that the recoveryfile would be removed.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    m_isfile.return_value = True
    m_delete.return_value = None
    m_list.return_value = None

    cleanup(jobs)

    assert m_remove.call_count == 1


@mock.patch('os.remove')
@mock.patch('os.path.isfile')
@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_recoveryfilerm2(m_delete, m_list, m_isfile, m_remove):

    """
    Test that the recoveryfile would be removed.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": ""
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    m_isfile.return_value = True
    m_delete.return_value = None
    m_list.return_value = None

    cleanup(jobs)

    assert m_remove.call_count == 0


@mock.patch('os.remove')
@mock.patch('os.path.isfile')
@mock.patch('longbow.shellwrappers.remotelist')
@mock.patch('longbow.shellwrappers.remotedelete')
def test_cleanup_recoveryfilerm3(m_delete, m_list, m_isfile, m_remove):

    """
    Test that the recoveryfile would be removed.
    """

    jobs = {
        "lbowconf": {
            "recoveryfile": "rec.file"
        },
        "jobone": {
            "destdir": "/path/to/jobone12484",
            "remoteworkdir": "/path/to/local/dir",
            }
    }

    m_isfile.return_value = False
    m_delete.return_value = None
    m_list.return_value = None

    cleanup(jobs)

    assert m_remove.call_count == 0
