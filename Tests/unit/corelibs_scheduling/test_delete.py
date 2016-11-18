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
This testing module contains the tests for the delete method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.scheduling as scheduling


@mock.patch('Longbow.schedulers.lsf.delete')
def test_delete_single(mock_delete):

    """
    Test that a single job only tries to delete once.
    """

    job = {
        "jobname": "job-one",
        "resource": "test-machine",
        "scheduler": "LSF",
        "jobid": "test456"
    }

    scheduling.delete(job)

    assert mock_delete.call_count == 1, \
        "For a single job this method should only be called once"


@mock.patch('Longbow.schedulers.lsf.delete')
def test_delete_attrexcept(mock_delete):

    """
    Test that errors with missing plugins are handled correctly.
    """

    job = {
        "jobname": "job-one",
        "resource": "test-machine",
        "scheduler": "LSF",
        "jobid": "test456"
    }

    mock_delete.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.delete(job)


@mock.patch('Longbow.schedulers.lsf.delete')
def test_delete_deleteexcept(mock_delete):

    """
    Test that job delete exception is handled in a controlled way.
    """

    job = {
        "jobname": "job-one",
        "resource": "test-machine",
        "scheduler": "LSF",
        "jobid": "test456"
    }

    mock_delete.side_effect = exceptions.JobdeleteError("Delete Error")

    scheduling.delete(job)
