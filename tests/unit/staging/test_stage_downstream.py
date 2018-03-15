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
This testing module contains the tests for the stage_downstream method within
the staging module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.staging import stage_downstream


@mock.patch('longbow.shellwrappers.download')
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

        stage_downstream(job)


@mock.patch('longbow.shellwrappers.download')
def test_stage_downstream_params(mock_download):

    """
    Test that a dict actually makes it to the download method.
    """

    job = {
        "jobname": "jobone",
        "destdir": "/path/to/jobone12484",
        "localworkdir": "/path/to/local/dir"
    }

    stage_downstream(job)

    downloadarg1 = mock_download.call_args[0][0]

    assert isinstance(downloadarg1, dict)
