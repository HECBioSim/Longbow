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
This testing module contains the tests for the main method within the
entrypoint module.
"""

import os
import pytest

try:

    from unittest import mock

except ImportError:

    import mock

import longbow.exceptions as exceptions
from longbow.entrypoints import launcher
from longbow.exceptions import UpdateExit


def _configload(_):

    "Mock configuration"

    jobs = {
        "lbowconf": {
            "recoveryfile": "recovery.file"}
        }

    return jobs


def _runningjobs(_):

    "Set up two running jobs"

    jobs = {
        "job1": {
            "laststatus": "Running"
        },
        "job2": {
            "laststatus": "Running"}
        }

    return jobs


def _finishedjobs(_):

    "Set up two running jobs"

    jobs = {
        "job1": {
            "laststatus": "Finished"
        },
        "job2": {
            "laststatus": "Finished"}
        }

    return jobs


def _completejobs(_):

    "Set up two running jobs"

    jobs = {
        "job1": {
            "laststatus": "Complete"
        }, "job2": {
            "laststatus": "Complete"}
        }

    return jobs


@mock.patch('longbow.entrypoints.longbow')
@mock.patch('os.path.isfile')
def test_main_test1(m_isfile, m_longbowmain):

    """
    Check that the longbow main method gets called, and that the parameters
    structure is being setup, this is a rudimentary test.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--verbose", "pmemd.MPI", "-O",
            "-i", "ex.in", "-c", "ex.min", "-p", "ex.top", "-o", "ex.out"]

    with mock.patch('sys.argv', args):

        launcher()

    params = m_longbowmain.call_args[0][1]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is False
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == \
        "-O -i ex.in -c ex.min -p ex.top -o ex.out"
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "longbow.log")
    assert params["recover"] == ""
    assert params["resource"] == ""
    assert params["replicates"] == ""
    assert params["verbose"] is True


@mock.patch('longbow.entrypoints.longbow')
@mock.patch('os.path.isfile')
def test_main_test2(m_isfile, m_longbowmain):

    """
    Check that the longbow main method gets called, and that the parameters
    structure is being setup, this is a rudimentary test.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "--verbose", "pmemd.MPI", "-O", "-i", "ex.in", "-c", "ex.min",
            "-p", "ex.top", "-o", "ex.out"]

    with mock.patch('sys.argv', args):

        launcher()

    params = m_longbowmain.call_args[0][1]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is False
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == \
        "-O -i ex.in -c ex.min -p ex.top -o ex.out"
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "longbow.log")
    assert params["recover"] == ""
    assert params["resource"] == "big-machine"
    assert params["replicates"] == ""
    assert params["verbose"] is True


@mock.patch('longbow.entrypoints.recovery')
@mock.patch('os.path.isfile')
def test_main_test3(m_isfile, m_recovery):

    """
    Check that the recovery method gets called, this is a rudimentary test.
    """

    m_isfile.return_value = True

    args = ["longbow", "--recover", "recovery.file", "--log", "new-log.file",
            "--verbose"]

    with mock.patch('sys.argv', args):

        launcher()

    params = m_recovery.call_args[0][1]

    assert m_recovery.call_count == 1
    assert params == "recovery.file"


@mock.patch('longbow.entrypoints.longbow')
@mock.patch('longbow.entrypoints.recovery')
@mock.patch('longbow.entrypoints.update')
@mock.patch('os.path.isfile')
def test_main_test4(m_isfile, m_update, m_recovery, m_longbow):

    """
    Check that the update method gets called, this is a rudimentary test.
    """

    m_isfile.return_value = True

    args = ["longbow", "--update", "update.file", "--log", "new-log.file",
            "--verbose"]

    with mock.patch('sys.argv', args):

        launcher()

    params = m_update.call_args[0][1]

    assert m_longbow.call_count == 0
    assert m_recovery.call_count == 0
    assert m_update.call_count == 1
    assert params == "update.file"


@mock.patch('longbow.entrypoints.longbow')
@mock.patch('longbow.entrypoints.recovery')
@mock.patch('longbow.entrypoints.update')
@mock.patch('os.path.isfile')
def test_main_test5(m_isfile, m_update, m_recovery, m_longbow):

    """
    Check that longbow doesn't launch if too many args are given.
    """

    m_isfile.return_value = True

    args = ["longbow", "--recover", "recovery.file", "--update", "update.file",
            "--log", "new-log.file", "--verbose"]

    with mock.patch('sys.argv', args):
        with pytest.raises(SystemExit) as err:
            launcher()

    assert m_longbow.call_count == 0
    assert m_recovery.call_count == 0
    assert m_update.call_count == 0
    assert err.type == SystemExit
    assert err.value.code == 1


@mock.patch('longbow.entrypoints.longbow')
@mock.patch('os.path.isfile')
def test_main_test6(m_isfile, m_longbowmain):

    """
    Test that exception handling happens properly.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "pmemd.MPI", "-O", "-i", "ex.in", "-c", "ex.min", "-p", "ex.top",
            "-o", "ex.out"]

    m_longbowmain.side_effect = exceptions.PluginattributeError

    with mock.patch('sys.argv', args):
        with pytest.raises(SystemExit) as err:
            launcher()

    params = m_longbowmain.call_args[0][1]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is False
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == \
        "-O -i ex.in -c ex.min -p ex.top -o ex.out"
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "longbow.log")
    assert params["recover"] == ""
    assert params["resource"] == "big-machine"
    assert params["replicates"] == ""
    assert params["verbose"] is False
    assert err.type == SystemExit
    assert err.value.code == 1


@mock.patch('longbow.entrypoints.longbow')
@mock.patch('os.path.isfile')
def test_main_test7(m_isfile, m_longbowmain):

    """
    Test that exception handling happens properly.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "--debug", "pmemd.MPI", "-O", "-i", "ex.in", "-c", "ex.min", "-p",
            "ex.top", "-o", "ex.out"]

    m_longbowmain.side_effect = exceptions.PluginattributeError

    with mock.patch('sys.argv', args):
        with pytest.raises(SystemExit) as err:
            launcher()

    params = m_longbowmain.call_args[0][1]

    assert m_longbowmain.call_count == 1
    assert params["debug"] is True
    assert params["disconnect"] is False
    assert params["executable"] == "pmemd.MPI"
    assert params["executableargs"] == \
        "-O -i ex.in -c ex.min -p ex.top -o ex.out"
    assert params["hosts"] == os.path.join(os.getcwd(), "hosts.conf")
    assert params["job"] == ""
    assert params["jobname"] == "testjob"
    assert params["log"] == os.path.join(os.getcwd(), "longbow.log")
    assert params["recover"] == ""
    assert params["resource"] == "big-machine"
    assert params["replicates"] == ""
    assert params["verbose"] is False
    assert err.type == SystemExit
    assert err.value.code == 1


@mock.patch('longbow.entrypoints.recovery')
@mock.patch('longbow.entrypoints.longbow')
@mock.patch('os.path.isfile')
def test_main_test8(m_isfile, m_longbowmain, m_recovery):

    """
    Test that exception handling happens properly.
    """

    m_isfile.return_value = True

    args = ["longbow", "--jobname", "testjob", "--resource", "big-machine",
            "--debug"]

    with mock.patch('sys.argv', args):
        with pytest.raises(SystemExit) as err:
            launcher()

    assert m_longbowmain.call_count == 0
    assert m_recovery.call_count == 0
    assert err.type == SystemExit
    assert err.value.code == 1


@mock.patch('longbow.staging.cleanup')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling.delete')
@mock.patch('longbow.scheduling.monitor')
@mock.patch('longbow.scheduling.submit')
@mock.patch('longbow.staging.stage_upstream')
@mock.patch('longbow.scheduling.prepare')
@mock.patch('longbow.applications.processjobs')
@mock.patch('longbow.applications.checkapp')
@mock.patch('longbow.scheduling.checkenv')
@mock.patch('longbow.shellwrappers.checkconnections')
@mock.patch('longbow.configuration.processconfigs')
@mock.patch('os.path.isfile')
def test_main_test9(m_isfile, m_procconf, m_testcon, m_testenv, m_testapp,
                    m_procjob, m_schedprep, m_stagup, m_sub, m_mon, m_del,
                    m_stagdown, m_clean):

    """Test the keyboard interrupt feature with running jobs."""

    m_isfile.return_value = True

    args = ["longbow", "--job", "testjob", "--resource", "big-machine",
            "--debug"]

    m_procconf.side_effect = _runningjobs
    m_mon.side_effect = KeyboardInterrupt

    with mock.patch('sys.argv', args):

        launcher()

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


@mock.patch('longbow.staging.cleanup')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling.delete')
@mock.patch('longbow.scheduling.monitor')
@mock.patch('longbow.scheduling.submit')
@mock.patch('longbow.staging.stage_upstream')
@mock.patch('longbow.scheduling.prepare')
@mock.patch('longbow.applications.processjobs')
@mock.patch('longbow.applications.checkapp')
@mock.patch('longbow.scheduling.checkenv')
@mock.patch('longbow.shellwrappers.checkconnections')
@mock.patch('longbow.configuration.processconfigs')
@mock.patch('os.path.isfile')
def test_main_test10(m_isfile, m_procconf, m_testcon, m_testenv, m_testapp,
                     m_procjob, m_schedprep, m_stagup, m_sub, m_mon, m_del,
                     m_stagdown, m_clean):

    """Test the keyboard interrupt feature with running jobs."""

    m_isfile.return_value = True

    args = ["longbow", "--job", "testjob", "--resource", "big-machine",
            "--debug"]

    m_procconf.side_effect = _finishedjobs
    m_mon.side_effect = KeyboardInterrupt

    with mock.patch('sys.argv', args):

        launcher()

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


@mock.patch('longbow.staging.cleanup')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling.delete')
@mock.patch('longbow.scheduling.monitor')
@mock.patch('longbow.scheduling.submit')
@mock.patch('longbow.staging.stage_upstream')
@mock.patch('longbow.scheduling.prepare')
@mock.patch('longbow.applications.processjobs')
@mock.patch('longbow.applications.checkapp')
@mock.patch('longbow.scheduling.checkenv')
@mock.patch('longbow.shellwrappers.checkconnections')
@mock.patch('longbow.configuration.processconfigs')
@mock.patch('os.path.isfile')
def test_main_test11(m_isfile, m_procconf, m_testcon, m_testenv, m_testapp,
                     m_procjob, m_schedprep, m_stagup, m_sub, m_mon, m_del,
                     m_stagdown, m_clean):

    """Test the keyboard interrupt feature with complete jobs."""

    m_isfile.return_value = True

    args = ["longbow", "--job", "testjob", "--resource", "big-machine",
            "--debug"]

    m_procconf.side_effect = _completejobs
    m_mon.side_effect = KeyboardInterrupt

    with mock.patch('sys.argv', args):

        launcher()

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


@mock.patch('longbow.staging.cleanup')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling.delete')
@mock.patch('longbow.scheduling.monitor')
@mock.patch('longbow.scheduling.submit')
@mock.patch('longbow.staging.stage_upstream')
@mock.patch('longbow.scheduling.prepare')
@mock.patch('longbow.applications.processjobs')
@mock.patch('longbow.applications.checkapp')
@mock.patch('longbow.scheduling.checkenv')
@mock.patch('longbow.shellwrappers.checkconnections')
@mock.patch('longbow.configuration.processconfigs')
@mock.patch('os.path.isfile')
def test_main_test12(m_isfile, m_procconf, m_testcon, m_testenv, m_testapp,
                     m_procjob, m_schedprep, m_stagup, m_sub, m_mon, m_del,
                     m_stagdown, m_clean):

    """Test the disconnect feature with complete jobs."""

    m_isfile.return_value = True

    args = ["longbow", "--job", "testjob", "--disconnect", "--debug"]

    m_procconf.side_effect = _configload

    with mock.patch('sys.argv', args):

        launcher()

    assert m_procconf.call_count == 1
    assert m_testcon.call_count == 1
    assert m_testenv.call_count == 1
    assert m_testapp.call_count == 1
    assert m_procjob.call_count == 1
    assert m_schedprep.call_count == 1
    assert m_stagup.call_count == 1
    assert m_sub.call_count == 1
    assert m_mon.call_count == 0
    assert m_del.call_count == 0
    assert m_stagdown.call_count == 0
    assert m_clean.call_count == 0


@mock.patch('longbow.staging.cleanup')
@mock.patch('longbow.staging.stage_downstream')
@mock.patch('longbow.scheduling.delete')
@mock.patch('longbow.scheduling.monitor')
@mock.patch('longbow.scheduling.submit')
@mock.patch('longbow.staging.stage_upstream')
@mock.patch('longbow.scheduling.prepare')
@mock.patch('longbow.applications.processjobs')
@mock.patch('longbow.applications.checkapp')
@mock.patch('longbow.scheduling.checkenv')
@mock.patch('longbow.shellwrappers.checkconnections')
@mock.patch('longbow.configuration.processconfigs')
@mock.patch('os.path.isfile')
def test_main_test13(m_isfile, m_procconf, m_testcon, m_testenv, m_testapp,
                     m_procjob, m_schedprep, m_stagup, m_sub, m_mon, m_del,
                     m_stagdown, m_clean):

    """Test the keyboard interrupt feature with complete jobs."""

    m_isfile.return_value = True

    args = ["longbow", "--job", "testjob", "--resource", "big-machine",
            "--debug"]

    m_procconf.side_effect = _configload
    m_mon.side_effect = UpdateExit

    with mock.patch('sys.argv', args):

        launcher()

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
    assert m_stagdown.call_count == 0
    assert m_clean.call_count == 0
