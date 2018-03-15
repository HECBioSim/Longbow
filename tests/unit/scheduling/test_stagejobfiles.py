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
This testing module contains the tests for the stagejobfiles method within the
scheduling module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.scheduling import _stagejobfiles


@mock.patch('longbow.staging.stage_downstream')
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

    _stagejobfiles(jobs, False)

    assert mock_download.call_count == 2, "Should download two jobs files"
    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Complete"
