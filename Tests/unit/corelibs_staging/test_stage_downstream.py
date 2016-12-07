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
This testing module contains the tests for the stage_downstream method within
the staging module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.staging as staging


@mock.patch('Longbow.corelibs.shellwrappers.download')
def test_stage_downstream_except(mock_download):

    """
    Test if staging exception is correctly raised if rsync exception happens.
    """

    job = {
        "jobname": "jobone",
        "destdir": "/path/to/jobone12484",
        "localworkdir": "/path/to/local/dir"
    }

    mock_download.side_effect = exceptions.RsyncError("Rsync Error", "output")

    with pytest.raises(exceptions.StagingError):

        staging.stage_downstream(job)


@mock.patch('Longbow.corelibs.shellwrappers.download')
def test_stage_downstream_params(mock_download):

    """
    Test that a dict actually makes it to the download method.
    """

    job = {
        "jobname": "jobone",
        "destdir": "/path/to/jobone12484",
        "localworkdir": "/path/to/local/dir"
    }

    staging.stage_downstream(job)

    downloadarg1 = mock_download.call_args[0][0]

    assert isinstance(downloadarg1, dict)
