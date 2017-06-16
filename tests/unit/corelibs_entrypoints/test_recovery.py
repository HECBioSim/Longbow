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

import longbow.corelibs.exceptions as exceptions
from longbow.corelibs.entrypoints import recovery


@mock.patch('longbow.corelibs.configuration.loadconfigs')
@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('os.path.isfile')
def test_recovery_check(mock_file, mock_mon, mock_clean, mock_load):

    """
    Check that the correct function calls are made.
    """

    mock_file.return_value = True
    mock_load.return_value = ("", "", "testjobs")

    recovery("recovery.file")

    assert mock_mon.call_args[0][0] == "testjobs"
    assert mock_clean.call_args[0][0] == "testjobs"


@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('os.path.isfile')
def test_recovery_except(mock_isfile, mock_monitor, mock_cleanup):

    """
    Check that exception is raised on bad file.
    """

    mock_isfile.return_value = False
    mock_monitor.return_value = None
    mock_cleanup.return_value = None

    with pytest.raises(exceptions.RequiredinputError):

        recovery("recovery.file")


@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling.delete')
@mock.patch('longbow.corelibs.configuration.loadconfigs')
@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('os.path.isfile')
def test_recovery_interupt(m_file, m_mon, m_clean, m_load, m_del, m_down):

    """
    Check that user interrupt doesn't result in unhandled exception.
    """

    m_file.return_value = True
    m_mon.side_effect = KeyboardInterrupt
    m_clean.return_value = None
    m_load.return_value = ("", "", {"testjobs": {}})
    m_del.return_value = None
    m_down.return_value = None

    recovery("recovery.file")

    assert m_clean.call_count == 1
    assert m_down.call_count == 0
    assert m_del.call_count == 0


@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling.delete')
@mock.patch('longbow.corelibs.configuration.loadconfigs')
@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('os.path.isfile')
def test_recovery_interupt2(m_file, m_mon, m_clean, m_load, m_del, m_down):

    """
    Check that user interrupt doesn't result in unhandled exception. Also test
    the case where jobs are running.
    """

    m_file.return_value = True
    m_mon.side_effect = KeyboardInterrupt
    m_clean.return_value = None
    m_load.return_value = ("", "", {"testjobs": {"laststatus": "Running"}})
    m_del.return_value = None
    m_down.return_value = None

    recovery("recovery.file")

    assert m_clean.call_count == 1
    assert m_down.call_count == 1
    assert m_del.call_count == 1


@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling.delete')
@mock.patch('longbow.corelibs.configuration.loadconfigs')
@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('os.path.isfile')
def test_recovery_interupt3(m_file, m_mon, m_clean, m_load, m_del, m_down):

    """
    Check that user interrupt doesn't result in unhandled exception. Also test
    the case where jobs are finished.
    """

    m_file.return_value = True
    m_mon.side_effect = KeyboardInterrupt
    m_clean.return_value = None
    m_load.return_value = ("", "", {"testjobs": {"laststatus": "Complete"}})
    m_del.return_value = None
    m_down.return_value = None

    recovery("recovery.file")

    assert m_clean.call_count == 1
    assert m_down.call_count == 1
    assert m_del.call_count == 0
