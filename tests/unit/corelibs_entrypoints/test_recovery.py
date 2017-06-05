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
