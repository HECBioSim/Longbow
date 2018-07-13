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
This testing module contains the tests for the recovery method within the
entrypoint module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import longbow.exceptions as exceptions
from longbow.entrypoints import recovery


@mock.patch('longbow.configuration.loadconfigs')
@mock.patch('longbow.staging.cleanup')
@mock.patch('longbow.scheduling.monitor')
@mock.patch('os.path.isfile')
def test_recovery_check(mock_file, mock_mon, mock_clean, mock_load):

    """
    Check that the correct function calls are made.
    """

    mock_file.return_value = True
    mock_load.return_value = ("", "", {"testjobs": {}})

    recovery({}, "recovery.file")

    assert mock_mon.call_args[0][0] == {"testjobs": {}}
    assert mock_clean.call_args[0][0] == {"testjobs": {}}


@mock.patch('longbow.staging.cleanup')
@mock.patch('longbow.scheduling.monitor')
@mock.patch('os.path.isfile')
def test_recovery_except(mock_isfile, mock_monitor, mock_cleanup):

    """
    Check that exception is raised on bad file.
    """

    mock_isfile.return_value = False
    mock_monitor.return_value = None
    mock_cleanup.return_value = None

    with pytest.raises(exceptions.RequiredinputError):

        recovery({}, "recovery.file")

