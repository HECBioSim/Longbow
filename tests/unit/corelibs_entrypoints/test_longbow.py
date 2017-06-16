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
This testing module contains the tests for the longbowmain method within the
entrypoint module.
"""

try:

    from unittest import mock

except ImportError:

    import mock

from longbow.corelibs.entrypoints import longbow


@mock.patch('longbow.corelibs.staging.cleanup')
@mock.patch('longbow.corelibs.scheduling.submit')
@mock.patch('longbow.corelibs.staging.stage_upstream')
@mock.patch('longbow.corelibs.scheduling.prepare')
@mock.patch('longbow.corelibs.applications.processjobs')
@mock.patch('longbow.corelibs.applications.checkapp')
@mock.patch('longbow.corelibs.scheduling.checkenv')
@mock.patch('longbow.corelibs.shellwrappers.checkconnections')
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

    longbow(params)

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
@mock.patch('longbow.corelibs.applications.checkapp')
@mock.patch('longbow.corelibs.scheduling.checkenv')
@mock.patch('longbow.corelibs.shellwrappers.checkconnections')
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

    longbow(params)

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
@mock.patch('longbow.corelibs.applications.checkapp')
@mock.patch('longbow.corelibs.scheduling.checkenv')
@mock.patch('longbow.corelibs.shellwrappers.checkconnections')
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

    longbow(params)

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
@mock.patch('longbow.corelibs.applications.checkapp')
@mock.patch('longbow.corelibs.scheduling.checkenv')
@mock.patch('longbow.corelibs.shellwrappers.checkconnections')
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

    longbow(params)

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
@mock.patch('longbow.corelibs.applications.checkapp')
@mock.patch('longbow.corelibs.scheduling.checkenv')
@mock.patch('longbow.corelibs.shellwrappers.checkconnections')
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

    longbow(params)

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
