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
This testing module contains the tests for the stagejobfiles method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import Longbow.corelibs.scheduling as scheduling


@mock.patch('Longbow.corelibs.staging.stage_downstream')
def test_stagejobfiles_singlerun(mock_download):

    """
    Test if the staging method is working properly. Jobs marked as running or
    finished should be downloaded. Jobs that are marked as finished, should be
    marked as complete after download, signifying the last download.
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

    scheduling._stagejobfiles(jobs, False)

    assert mock_download.call_count == 2, "Should download two jobs files"
    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Complete"
