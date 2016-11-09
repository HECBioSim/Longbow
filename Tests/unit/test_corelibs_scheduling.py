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
This testing module contains the tests for the scheduling module methods.
"""

try:

    from unittest import mock

except ImportError:

    import mock

import pytest

import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.scheduling as scheduling


def changescheduler(job):

    """
    Change the scheduler when call to mocked function is made.
    """

    if job["resource"] == "test-machine":

        job["scheduler"] = "lsf"

    else:

        job["scheduler"] = "pbs"


def changehandler(job):

    """
    Change the handler when call to mocked function is made.
    """

    if job["resource"] == "test-machine":

        job["handler"] = "mpiexec"

    else:

        job["handler"] = "aprun"


def addjobid(job):

    """
    Add a job id to job
    """

    job["jobid"] = "123456"

# ---------------------------------------------------------------------------#
# Tests for testenv()


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testhandler')
@mock.patch('Longbow.corelibs.scheduling._testscheduler')
def test_testenv_single(mock_sched, mock_hand, mock_save):

    """
    Test that a single job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "test",
            "handler": "test",
        }
    }

    hostconf = "/path/to/configfile"

    scheduling.testenv(jobs, hostconf)

    assert mock_sched.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_hand.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_save.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testhandler')
@mock.patch('Longbow.corelibs.scheduling._testscheduler')
def test_testenv_multi(mock_sched, mock_hand, mock_save):

    """
    Test that a multi job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "test",
            "handler": "test",
        },
        "jobtwo": {
            "resource": "test-machine",
            "scheduler": "test",
            "handler": "test",
        },
        "jobthree": {
            "resource": "test-machine2",
            "scheduler": "test",
            "handler": "test",
        }
    }

    hostconf = "/path/to/configfile"

    scheduling.testenv(jobs, hostconf)

    assert mock_sched.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_hand.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"
    assert mock_save.call_count == 0, \
        "Testing for scheduler should not be done, as it is set already"


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testscheduler')
def test_testenv_scheduler(mock_sched, mock_save):

    """
    Test that a multi job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "",
            "handler": "test"
        },
        "jobtwo": {
            "resource": "test-machine",
            "scheduler": "",
            "handler": "test"
        },
        "jobthree": {
            "resource": "test-machine2",
            "scheduler": "",
            "handler": "test"
        }
    }

    hostconf = "/path/to/configfile"

    mock_sched.side_effect = changescheduler

    scheduling.testenv(jobs, hostconf)

    assert jobs["jobone"]["scheduler"] == "lsf"
    assert jobs["jobtwo"]["scheduler"] == "lsf"
    assert jobs["jobthree"]["scheduler"] == "pbs"
    assert mock_sched.call_count == 2
    assert mock_save.call_count == 1


@mock.patch('Longbow.corelibs.configuration.saveconfigs')
@mock.patch('Longbow.corelibs.scheduling._testhandler')
def test_testenv_handler(mock_hand, mock_save):

    """
    Test that a multi job with the scheduler and handlers set does not try to
    set them.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "scheduler": "lsf",
            "handler": ""
        },
        "jobtwo": {
            "resource": "test-machine",
            "scheduler": "lsf",
            "handler": ""
        },
        "jobthree": {
            "resource": "test-machine2",
            "scheduler": "pbs",
            "handler": ""
        }
    }

    hostconf = "/path/to/configfile"

    mock_hand.side_effect = changehandler

    scheduling.testenv(jobs, hostconf)

    assert jobs["jobone"]["handler"] == "mpiexec"
    assert jobs["jobtwo"]["handler"] == "mpiexec"
    assert jobs["jobthree"]["handler"] == "aprun"
    assert mock_hand.call_count == 2
    assert mock_save.call_count == 1

# ---------------------------------------------------------------------------#
# Tests for delete()


@mock.patch('Longbow.plugins.schedulers.lsf.delete')
def test_delete_single(mock_delete):

    """
    Test that a single job only tries to delete once.
    """

    job = {
        "jobname": "job-one",
        "resource": "test-machine",
        "scheduler": "LSF",
        "jobid": "test456"
    }

    scheduling.delete(job)

    assert mock_delete.call_count == 1, \
        "For a single job this method should only be called once"


@mock.patch('Longbow.plugins.schedulers.lsf.delete')
def test_delete_attrexcept(mock_delete):

    """
    Test that errors with missing plugins are handled correctly.
    """

    job = {
        "jobname": "job-one",
        "resource": "test-machine",
        "scheduler": "LSF",
        "jobid": "test456"
    }

    mock_delete.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.delete(job)


@mock.patch('Longbow.plugins.schedulers.lsf.delete')
def test_delete_deleteexcept(mock_delete):

    """
    Test that job delete exception is handled in a controlled way.
    """

    job = {
        "jobname": "job-one",
        "resource": "test-machine",
        "scheduler": "LSF",
        "jobid": "test456"
    }

    mock_delete.side_effect = exceptions.JobdeleteError("Delete Error")

    scheduling.delete(job)

# ---------------------------------------------------------------------------#
# Tests for monitor()


@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_testpollfrequency(mock_init, mock_poll, mock_wait):

    """
    Test that the polling frequency is working.
    """

    import time

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running"
        }
    }
    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = False, 0, 3
    mock_poll.return_value = False
    mock_wait.return_value = False
    mock_poll.side_effect = [None, exceptions.PluginattributeError]

    start = time.time()

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.monitor(jobs)

    end = time.time()

    assert mock_poll.call_count == 2
    assert int(end - start) > 2


@mock.patch('Longbow.corelibs.scheduling._stagejobfiles')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_teststagefreq(mock_init, mock_poll, mock_wait, mock_down):

    """
    Test that the staging frequency is working
    """

    import time

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Running"
        }
    }
    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = False, 2, 2
    mock_poll.return_value = False
    mock_down.return_value = False
    mock_wait.return_value = False
    mock_down.side_effect = [None, None, exceptions.PluginattributeError]

    start = time.time()

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.monitor(jobs)

    end = time.time()

    assert mock_poll.call_count == 3
    assert mock_down.call_count == 3
    assert int(end - start) > 4


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.corelibs.staging.stage_downstream')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_complete(mock_init, mock_poll, mock_wait, mock_down,
                          mock_save):

    """
    """

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error"
        }
    }
    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = False, 500, 100
    mock_poll.return_value = False
    mock_down.return_value = False
    mock_down.return_value = None
    mock_save.return_value = None
    mock_wait.return_value = False

    scheduling.monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"
    assert jobs["jobtwo"]["laststatus"] == "Complete"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.corelibs.staging.stage_downstream')
@mock.patch('Longbow.corelibs.scheduling._checkwaitingjobs')
@mock.patch('Longbow.corelibs.scheduling._polljobs')
@mock.patch('Longbow.corelibs.scheduling._monitorinitialise')
def test_monitor_except(mock_init, mock_poll, mock_wait, mock_down,
                        mock_save):

    """
    """

    jobs = {
        "jobone": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Finished"
        },
        "jobtwo": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Complete"
        },
        "jobthree": {
            "resource": "hpc1",
            "queue-max": "0",
            "queue-slots": "0",
            "laststatus": "Submit Error"
        }
    }
    scheduling.QUEUEINFO["hpc1"] = {}
    scheduling.QUEUEINFO["hpc1"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["hpc1"]["queue-max"] = "2"

    mock_init.return_value = False, 2, 2
    mock_poll.return_value = False
    mock_down.return_value = False
    mock_down.return_value = None
    mock_save.side_effect = IOError
    mock_wait.return_value = False

    scheduling.monitor(jobs)

    assert jobs["jobone"]["laststatus"] == "Complete"

# ---------------------------------------------------------------------------#
# Tests for prepare()


@mock.patch('Longbow.plugins.schedulers.lsf.prepare')
def test_prepare_single(mock_prepare):

    """
    Test that a single job only tries to create a submit file once.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    scheduling.prepare(jobs)

    assert mock_prepare.call_count == 1, \
        "For a single job this method should only be called once"


@mock.patch('Longbow.plugins.schedulers.lsf.prepare')
def test_prepare_multiple(mock_prepare):

    """
    Test that for multiple jobs the correct number of submit files are called
    for creation.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test123"
        },
        "job-two": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        },
        "job-three": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test789"
        }
    }

    scheduling.prepare(jobs)

    assert mock_prepare.call_count == 3, \
        "For a multi job this method should be called once for each job"


@mock.patch('Longbow.plugins.schedulers.lsf.prepare')
def test_prepare_attrexcept(mock_prepare):

    """
    Test that errors with missing plugins are handled correctly.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_prepare.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.prepare(jobs)

# ---------------------------------------------------------------------------#
# Tests for submit()


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_single(mock_isdir, mock_submit):

    """
    Test that a single job only tries to submit something once.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False

    scheduling.submit(jobs)

    assert mock_submit.call_count == 1, \
        "For a single job this method should only be called once"
    assert jobs["job-one"]["laststatus"] == "Queued"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_multiplesame(mock_isdir, mock_lsf):

    """
    Test that for multiple jobs the correct number of submission calls happen.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test123"
        },
        "job-two": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        },
        "job-three": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test789"
        }
    }

    mock_isdir.return_value = False

    scheduling.submit(jobs)

    assert mock_lsf.call_count == 3, \
        "For a multi job this method should only be called more than once"


@mock.patch('Longbow.plugins.schedulers.slurm.submit')
@mock.patch('Longbow.plugins.schedulers.pbs.submit')
@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_multiplediff(mock_isdir, mock_lsf, mock_pbs, mock_slurm):

    """
    Test that for multiple jobs the correct number of submission calls happen.
    """

    jobs = {
        "job-one": {
            "resource": "lsf-machine",
            "scheduler": "LSF",
            "jobid": "test123"
        },
        "job-two": {
            "resource": "pbs-machine",
            "scheduler": "pbs",
            "jobid": "test456"
        },
        "job-three": {
            "resource": "slurm-machine",
            "scheduler": "Slurm",
            "jobid": "test789"
        }
    }

    mock_isdir.return_value = False

    scheduling.submit(jobs)

    assert mock_lsf.call_count == 1, \
        "For a single job this method should only be called once"
    assert mock_pbs.call_count == 1, \
        "For a single job this method should only be called once"
    assert mock_slurm.call_count == 1, \
        "For a single job this method should only be called once"


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_fileexcept1(mock_isdir, mock_submit, mock_savini):

    """
    Test that if the recovery file write fails it does so in a controlled way.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None
    mock_savini.side_effect = OSError

    scheduling.submit(jobs)


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_fileexcept2(mock_isdir, mock_submit, mock_savini):

    """
    Test that if the recovery file write fails it does so in a controlled way.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = True
    mock_submit.return_value = None
    mock_savini.side_effect = IOError

    scheduling.submit(jobs)


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_attrexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that errors with missing plugins are handled correctly.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        scheduling.submit(jobs)


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_submitexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that submission failure errors are handled correctly.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = exceptions.JobsubmitError("Submit Error")

    scheduling.submit(jobs)

    assert jobs["job-one"]["laststatus"] == "Submit Error"


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_queueexcept(mock_isdir, mock_submit, mock_savini):

    """
    Test that queue limit events are handled correctly if a plugin raises the
    queuemax exception.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        }
    }

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.side_effect = exceptions.QueuemaxError("Submit Error")

    scheduling.submit(jobs)

    assert jobs["job-one"]["laststatus"] == "Waiting Submission"


@mock.patch('Longbow.corelibs.configuration.saveini')
@mock.patch('Longbow.plugins.schedulers.lsf.submit')
@mock.patch('os.path.isdir')
def test_submit_queueinfo(mock_isdir, mock_submit, mock_savini):

    """
    Check that the queueinformation counter is getting used.
    """

    jobs = {
        "job-one": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test123"
        },
        "job-two": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test456"
        },
        "job-three": {
            "resource": "test-machine",
            "scheduler": "LSF",
            "jobid": "test789"
        }
    }
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = "0"
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = "0"

    mock_isdir.return_value = False
    mock_savini.return_value = None
    mock_submit.return_value = None

    scheduling.submit(jobs)

    assert scheduling.QUEUEINFO["test-machine"]["queue-slots"] == "3"
    assert scheduling.QUEUEINFO["test-machine"]["queue-max"] == "3"

# ---------------------------------------------------------------------------#
# Tests for _testscheduler()


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testscheduler_detection1(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": "",
        "scheduler": ""
    }

    mock_ssh.return_value = None

    scheduling._testscheduler(job)

    assert job["scheduler"] in ["lsf", "pbs", "sge", "soge", "slurm"]


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testscheduler_detection2(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered. Throw in a failure event.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": "",
        "scheduler": ""
    }

    mock_ssh.side_effect = [exceptions.SSHError("SSH Error", "Error"), None]

    scheduling._testscheduler(job)

    assert job["scheduler"] in ["lsf", "pbs", "sge", "soge", "slurm"]


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testscheduler_except(mock_ssh):

    """
    Test that the correct exception is raised when nothing can be detected.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": "",
        "scheduler": ""
    }

    mock_ssh.side_effect = exceptions.SSHError("SSH Error", "Error")

    with pytest.raises(exceptions.SchedulercheckError):

        scheduling._testscheduler(job)

# ---------------------------------------------------------------------------#
# Tests for _testhandler()


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_detection1(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.return_value = None

    scheduling._testhandler(job)

    assert job["handler"] in ["aprun", "mpirun"]


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_detection2(mock_ssh):

    """
    Test that a handler can be detected. It is hard to specify exactly which
    to go for due to dictionaries being unordered. Throw in a failure event.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.side_effect = [exceptions.SSHError("SSH Error", "Error"), None]

    scheduling._testhandler(job)

    assert job["handler"] in ["aprun", "mpirun"]


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_except(mock_ssh):

    """
    Test that the correct exception is raised when nothing can be detected.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.side_effect = exceptions.SSHError("SSH Error", "Error")

    with pytest.raises(exceptions.HandlercheckError):

        scheduling._testhandler(job)


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_modules1(mock_ssh):

    """
    Test that the module string remains empty after calling this method.
    """

    job = {
        "modules": "",
        "resource": "test-machine",
        "handler": ""
    }

    mock_ssh.return_value = None

    scheduling._testhandler(job)

    assert job["modules"] == ""


@mock.patch('Longbow.corelibs.shellwrappers.sendtossh')
def test_testhandler_modules2(mock_ssh):

    """
    For provided modules, check that they are bring sent to SSH
    """

    job = {
        "modules": "lsf, intel",
        "resource": "test-machine",
        "handler": ""
    }

    scheduling._testhandler(job)

    callargs = mock_ssh.call_args[0][1]

    assert 'module load lsf\n' in callargs
    assert 'module load intel\n' in callargs

# ---------------------------------------------------------------------------#
# Tests for _monitorinitialise()


def test_monitorinitialise_test1():

    """
    Test some default parameters
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "0",
            "frequency": "0"
        },
        "jobtwo": {
            "resource": "test-machine",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "0",
            "frequency": "0"
        }
    }

    finished, stageintval, pollintval = scheduling._monitorinitialise(jobs)

    assert finished is False, "Should always be false here."
    assert stageintval == 0, "Should be zero if staging-frequency = 0"
    assert pollintval == 300, "Should be 300 if frequency = 0"


def test_monitorinitialise_test2():

    """
    Test some default parameters
    """

    jobs = {
        "jobone": {
            "resource": "test-machine3",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "100",
            "frequency": "400"
        },
        "jobtwo": {
            "resource": "test-machine3",
            "queue-max": "0",
            "queue-slots": "0",
            "staging-frequency": "0",
            "frequency": "0"
        }
    }

    finished, stageintval, pollintval = scheduling._monitorinitialise(jobs)

    assert finished is False, "Should always be false here."
    assert stageintval == 100, "The highest should be used: 100"
    assert pollintval == 400, "Should be 400 if frequency = 0"

# ---------------------------------------------------------------------------#
# Tests for _polljobs()


@mock.patch('Longbow.plugins.schedulers.lsf.status')
def test_polljobs_callcount(mock_status):

    """
    Test that only jobs with the correct state end up getting polled.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobtwo": {
            "laststatus": "Queued",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobthree": {
            "laststatus": "Submit Error",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfour": {
            "laststatus": "Waiting Submission",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfive": {
            "laststatus": "Finished",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobsix": {
            "laststatus": "Complete",
            "scheduler": "LSF",
            "jobid": "123456"
        }
    }

    mock_status.return_value = "Running"
    returnval = scheduling._polljobs(jobs, False)

    assert mock_status.call_count == 2, \
        "Should only be polling running and queued jobs"
    assert jobs["jobtwo"]["laststatus"] == "Running"
    assert returnval is True


@mock.patch('Longbow.plugins.schedulers.lsf.status')
def test_polljobs_finished(mock_status):

    """
    Test that only jobs with the correct state end up getting polled.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "laststatus": "Running",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobtwo": {
            "resource": "test-machine",
            "laststatus": "Queued",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobthree": {
            "resource": "test-machine",
            "laststatus": "Submit Error",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfour": {
            "resource": "test-machine",
            "laststatus": "Waiting Submission",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfive": {
            "resource": "test-machine",
            "laststatus": "Finished",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobsix": {
            "resource": "test-machine",
            "laststatus": "Complete",
            "scheduler": "LSF",
            "jobid": "123456"
        }
    }

    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = "2"
    mock_status.return_value = "Finished"
    scheduling._polljobs(jobs, False)

    assert mock_status.call_count == 2, \
        "Should only be polling running and queued jobs"
    assert jobs["jobone"]["laststatus"] == "Finished"
    assert jobs["jobtwo"]["laststatus"] == "Finished"
    assert scheduling.QUEUEINFO["test-machine"]["queue-slots"] == "0"


@mock.patch('Longbow.plugins.schedulers.lsf.status')
def test_polljobs_except(mock_status):

    """
    Test that only jobs with the correct state end up getting polled.
    """

    jobs = {
        "jobone": {
            "resource": "test-machine",
            "laststatus": "Running",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobtwo": {
            "resource": "test-machine",
            "laststatus": "Queued",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobthree": {
            "resource": "test-machine",
            "laststatus": "Submit Error",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfour": {
            "resource": "test-machine",
            "laststatus": "Waiting Submission",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobfive": {
            "resource": "test-machine",
            "laststatus": "Finished",
            "scheduler": "LSF",
            "jobid": "123456"
        },
        "jobsix": {
            "resource": "test-machine",
            "laststatus": "Complete",
            "scheduler": "LSF",
            "jobid": "123456"
        }
    }

    mock_status.side_effect = AttributeError

    with pytest.raises(exceptions.PluginattributeError):

        scheduling._polljobs(jobs, False)

# ---------------------------------------------------------------------------#
# Tests for _stagejobfiles()


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

# ---------------------------------------------------------------------------#
# Tests for _checkwaitingjobs()


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_none(mock_submit):

    """
    Check that if no jobs are marked as waiting that nothing gets submitted.
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

    scheduling._checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 0, "Should not be trying to submit"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_one(mock_submit):

    """
    Check that in cases that when there are two jobs waiting and only slot,
    that only one job gets submitted.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = addjobid
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 2

    scheduling._checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 1, "Should be submitting one job"
    assert scheduling.QUEUEINFO["test-machine"]["queue-slots"] == "2"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_two(mock_submit):

    """
    Check that in cases where there are multiple jobs but a lot less than the
    number of slots available only the correct number of jobs are submitted.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = addjobid
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 8

    scheduling._checkwaitingjobs(jobs, False)

    assert mock_submit.call_count == 2, "Should be submitting two jobs"
    assert scheduling.QUEUEINFO["test-machine"]["queue-slots"] == "3"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_except1(mock_submit):

    """
    Check if the plugin is not found that the correct exception is raised.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = AttributeError
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 8

    with pytest.raises(exceptions.PluginattributeError):

        scheduling._checkwaitingjobs(jobs, False)


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_except2(mock_submit):

    """
    Check that if the submit error is thrown that the job is simply marked
    as in error state.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = exceptions.JobsubmitError
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = 1
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = 8

    scheduling._checkwaitingjobs(jobs, False)

    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Submit Error"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"


@mock.patch('Longbow.plugins.schedulers.lsf.submit')
def test_checkwaitingjobs_except3(mock_submit):

    """
    Check that if the max queue error is thrown that the job is simply marked
    as in error state.
    """

    jobs = {
        "jobone": {
            "laststatus": "Running",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobtwo": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        },
        "jobthree": {
            "laststatus": "Waiting Submission",
            "resource": "test-machine",
            "scheduler": "LSF"
        }
    }

    mock_submit.side_effect = exceptions.QueuemaxError
    scheduling.QUEUEINFO["test-machine"]["queue-slots"] = "1"
    scheduling.QUEUEINFO["test-machine"]["queue-max"] = "8"

    scheduling._checkwaitingjobs(jobs, False)

    assert jobs["jobone"]["laststatus"] == "Running"
    assert jobs["jobtwo"]["laststatus"] == "Submit Error"
    assert jobs["jobthree"]["laststatus"] == "Submit Error"

# ---------------------------------------------------------------------------#
# Tests for _checkfinished()


def test_checkfinished_singlefalse():

    """
    Check that a running job doesn't let longbow exit
    """

    jobs = {
        "jobone": {
            "laststatus": "Finished"
        }
    }

    state = scheduling._checkfinished(jobs)

    assert state is False


def test_checkfinished_singletrue():

    """
    Check that a complete job triggers completion.
    """

    jobs = {
        "jobone": {
            "laststatus": "Complete"
        }
    }

    state = scheduling._checkfinished(jobs)

    assert state is True


def test_checkfinished_multifalse():

    """
    Check that a running job doesn't let longbow exit
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

    state = scheduling._checkfinished(jobs)

    assert state is False


def test_checkfinished_multitrue():

    """
    Check that a complete job triggers completion.
    """

    jobs = {
        "jobone": {
            "laststatus": "Complete"
        },
        "jobtwo": {
            "laststatus": "Complete"
        },
        "jobthree": {
            "laststatus": "Complete"
        }
    }

    state = scheduling._checkfinished(jobs)

    assert state is True
