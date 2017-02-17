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
This testing module contains the tests for the longbowmain method within the
entrypoint module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.corelibs.entrypoints import longbowmain


@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.submit')
@mock.patch('longbow.corelibs.staging.stage_upstream')
@mock.patch('longbow.corelibs.scheduling.prepare')
@mock.patch('longbow.corelibs.applications.processjobs')
@mock.patch('longbow.corelibs.applications.testapp')
@mock.patch('longbow.corelibs.scheduling.testenv')
@mock.patch('longbow.corelibs.shellwrappers.testconnections')
@mock.patch('longbow.corelibs.configuration.processconfigs')
def test_longbowmain_disconnect(m_procconf, m_testcon, m_testenv, m_testapp,
                                m_procjob, m_schedprep, m_stagup, m_sub,
                                m_clean):

    """
    Check that the disconnect mode is activated.
    """

    params = {
        "hosts": "some/file",
        "disconnect": True,
        "nochecks": False
        }

    longbowmain(params)

    assert m_procconf.call_count == 1
    assert m_testcon.call_count == 1
    assert m_testenv.call_count == 1
    assert m_testapp.call_count == 1
    assert m_procjob.call_count == 1
    assert m_schedprep.call_count == 1
    assert m_stagup.call_count == 1
    assert m_sub.call_count == 1
    assert m_clean.call_count == 0


@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('longbow.corelibs.scheduling.submit')
@mock.patch('longbow.corelibs.staging.stage_upstream')
@mock.patch('longbow.corelibs.scheduling.prepare')
@mock.patch('longbow.corelibs.applications.processjobs')
@mock.patch('longbow.corelibs.applications.testapp')
@mock.patch('longbow.corelibs.scheduling.testenv')
@mock.patch('longbow.corelibs.shellwrappers.testconnections')
@mock.patch('longbow.corelibs.configuration.processconfigs')
def test_longbowmain_testcalls1(m_procconf, m_testcon, m_testenv, m_testapp,
                                m_procjob, m_schedprep, m_stagup, m_sub, m_mon,
                                m_clean):

    """
    Check that the correct function calls are made.
    """

    params = {
        "hosts": "some/file",
        "disconnect": False,
        "nochecks": False
        }

    longbowmain(params)

    assert m_procconf.call_count == 1
    assert m_testcon.call_count == 1
    assert m_testenv.call_count == 1
    assert m_testapp.call_count == 1
    assert m_procjob.call_count == 1
    assert m_schedprep.call_count == 1
    assert m_stagup.call_count == 1
    assert m_sub.call_count == 1
    assert m_mon.call_count == 1
    assert m_clean.call_count == 1


@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('longbow.corelibs.scheduling.submit')
@mock.patch('longbow.corelibs.staging.stage_upstream')
@mock.patch('longbow.corelibs.scheduling.prepare')
@mock.patch('longbow.corelibs.applications.processjobs')
@mock.patch('longbow.corelibs.applications.testapp')
@mock.patch('longbow.corelibs.scheduling.testenv')
@mock.patch('longbow.corelibs.shellwrappers.testconnections')
@mock.patch('longbow.corelibs.configuration.processconfigs')
def test_longbowmain_testcalls2(m_procconf, m_testcon, m_testenv, m_testapp,
                                m_procjob, m_schedprep, m_stagup, m_sub, m_mon,
                                m_clean):

    """
    Check that the correct function calls are made.
    """

    params = {
        "hosts": "some/file",
        "disconnect": False,
        "nochecks": True
        }

    longbowmain(params)

    assert m_procconf.call_count == 1
    assert m_testcon.call_count == 1
    assert m_testenv.call_count == 1
    assert m_testapp.call_count == 0
    assert m_procjob.call_count == 1
    assert m_schedprep.call_count == 1
    assert m_stagup.call_count == 1
    assert m_sub.call_count == 1
    assert m_mon.call_count == 1
    assert m_clean.call_count == 1


@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling.delete')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('longbow.corelibs.scheduling.submit')
@mock.patch('longbow.corelibs.staging.stage_upstream')
@mock.patch('longbow.corelibs.scheduling.prepare')
@mock.patch('longbow.corelibs.applications.processjobs')
@mock.patch('longbow.corelibs.applications.testapp')
@mock.patch('longbow.corelibs.scheduling.testenv')
@mock.patch('longbow.corelibs.shellwrappers.testconnections')
@mock.patch('longbow.corelibs.configuration.processconfigs')
def test_longbowmain_killrunning(m_procconf, m_testcon, m_testenv, m_testapp,
                                 m_procjob, m_schedprep, m_stagup, m_sub,
                                 m_mon, m_del, m_stagdown, m_clean):

    """
    Check that the correct function calls are made.
    """

    params = {
        "hosts": "some/file",
        "disconnect": False,
        "nochecks": False
        }

    m_procconf.return_value = {
        "job1": {
            "laststatus": "Running"
            },
        "job2": {
            "laststatus": "Running"
            }
        }

    m_mon.side_effect = KeyboardInterrupt

    longbowmain(params)

    assert m_procconf.call_count == 1
    assert m_testcon.call_count == 1
    assert m_testenv.call_count == 1
    assert m_testapp.call_count == 1
    assert m_procjob.call_count == 1
    assert m_schedprep.call_count == 1
    assert m_stagup.call_count == 1
    assert m_sub.call_count == 1
    assert m_mon.call_count == 1
    assert m_del.call_count == 2
    assert m_stagdown.call_count == 2
    assert m_clean.call_count == 1


@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.staging.stage_downstream')
@mock.patch('longbow.corelibs.scheduling.delete')
@mock.patch('longbow.corelibs.scheduling.monitor')
@mock.patch('longbow.corelibs.scheduling.submit')
@mock.patch('longbow.corelibs.staging.stage_upstream')
@mock.patch('longbow.corelibs.scheduling.prepare')
@mock.patch('longbow.corelibs.applications.processjobs')
@mock.patch('longbow.corelibs.applications.testapp')
@mock.patch('longbow.corelibs.scheduling.testenv')
@mock.patch('longbow.corelibs.shellwrappers.testconnections')
@mock.patch('longbow.corelibs.configuration.processconfigs')
def test_longbowmain_killcomplete(m_procconf, m_testcon, m_testenv, m_testapp,
                                  m_procjob, m_schedprep, m_stagup, m_sub,
                                  m_mon, m_del, m_stagdown, m_clean):

    """
    Check that the correct function calls are made.
    """

    params = {
        "hosts": "some/file",
        "disconnect": False,
        "nochecks": False
        }

    m_procconf.return_value = {
        "job1": {
            "laststatus": "Complete"
            },
        "job2": {
            "laststatus": "Complete"
            }
        }

    m_mon.side_effect = KeyboardInterrupt

    longbowmain(params)

    assert m_procconf.call_count == 1
    assert m_testcon.call_count == 1
    assert m_testenv.call_count == 1
    assert m_testapp.call_count == 1
    assert m_procjob.call_count == 1
    assert m_schedprep.call_count == 1
    assert m_stagup.call_count == 1
    assert m_sub.call_count == 1
    assert m_mon.call_count == 1
    assert m_del.call_count == 0
    assert m_stagdown.call_count == 2
    assert m_clean.call_count == 1
