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

"""A module containing generic scheduling methods.

This module contains generic methods for preparing, submitting, deleting and
monitoring jobs. The methods contained within this module are all based on
generic job concepts. The specific functionality that comes from each scheduler
is accessed through the plug-in framework. To make use of these methods, the
plug-in framework must be present alongside the core library.

testenv(jobs, hostconf)
    This method makes an attempt to test the environment and determine from
    a pre-configured list what scheduler and job submission handler is present
    on the machine.

delete(job)
    A method containing the generic and boiler plate Longbow code for deleting
    a job.

monitor(jobs)
    A method containing the generic and boiler plate Longbow code for
    monitoring a job, this method contains the entire structure of the loop
    that deals with monitoring jobs.

prepare(jobs)
    A method containing the generic and boiler plate Longbow code for
    constructing the submit file.

submit(jobs)
    A method containing the generic and boiler plate Longbow code for
    submitting a job.
"""

import logging
import time
import os

import Longbow.corelibs.configuration as configuration
import Longbow.corelibs.exceptions as exceptions
import Longbow.corelibs.shellwrappers as shellwrappers
import Longbow.corelibs.staging as staging
import Longbow.schedulers as schedulers


LOG = logging.getLogger("Longbow.corelibs.scheduling")
QUEUEINFO = {}
JOBFILE = os.path.join(os.path.expanduser('~/.Longbow'), "recovery-" +
                       time.strftime("%Y%m%d-%H%M%S"))


def testenv(jobs, hostconf):
    """A method for determining the sceduler and job handler on a machine.

    This method makes an attempt to test the environment and determine from
    a pre-configured list what scheduler and job submission handler is present
    on the machine.

    Required arguments are:

    hostconf (string) - The path to the host configuration file, this should be
                        provided so that if any changes are made that they can
                        be saved.

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    save = False

    checked = []
    saveparams = {}

    # Take a look at each job.
    for item in jobs:

        job = jobs[item]

        # If we have not checked this host already
        if job["resource"] not in checked:

            # Make sure we don't check the same thing again.
            checked.extend([job["resource"]])

            # If we don't have the resource defined then define it.
            if job["resource"] not in saveparams:

                saveparams[job["resource"]] = {}

            # If we have no scheduler defined by the user then find it.
            if job["scheduler"] is "":

                _testscheduler(job)
                saveparams[job["resource"]]["scheduler"] = job["scheduler"]
                save = True

            else:

                LOG.info("The environment on host '%s' is '%s'",
                         job["resource"], job["scheduler"])

            # If we have no job handler defined by the user then find it.
            if job["handler"] is "":

                _testhandler(job)
                saveparams[job["resource"]]["handler"] = job["handler"]
                save = True

            else:

                LOG.info("The handler on host '%s' is '%s'",
                         job["resource"], job["handler"])

        # If resource has been checked.
        else:

            # Then we should have a look if the resource for this job has been
            # altered.
            if job["resource"] in saveparams:

                # Then check if scheduler has been added.
                if "scheduler" in saveparams[job["resource"]]:

                    job["scheduler"] = saveparams[job["resource"]]["scheduler"]

                # Then check if handler has been added.
                if "handler" in saveparams[job["resource"]]:

                    job["handler"] = saveparams[job["resource"]]["handler"]

    # Do we have anything to change in the host file.
    if save is True:

        configuration.saveconfigs(hostconf, saveparams)


def delete(job):
    """A generic method for deleting jobs.

    A method containing the generic and boiler plate Longbow code for deleting
    a job.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    """
    scheduler = job["scheduler"]

    try:

        LOG.info("Deleting the job '%s'", job["jobname"])

        getattr(schedulers, scheduler.lower()).delete(job)

    except AttributeError:

        raise exceptions.PluginattributeError(
            "delete method cannot be found in plugin '{0}'"
            .format(scheduler))

    except exceptions.JobdeleteError:

        LOG.info("Unable to delete job '%s'", job["jobname"])

    LOG.info("Deletion successful")


def monitor(jobs):
    """A generic method for monitoring the status of jobs.

    A method containing the generic and boiler plate Longbow code for
    monitoring a job, this method contains the entire structure of the loop
    that deals with monitoring jobs.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    LOG.info("Monitoring job/s. Depending on the chosen logging mode, Longbow "
             "might appear to be doing nothing. Please be patient!")

    stageinterval, pollinterval = _monitorinitialise(jobs)

    allcomplete = False
    allfinished = False
    lastpolltime = 0
    laststagetime = 0
    saverecoveryfile = True
    recoveryfileerror = False

    # Loop until all jobs are done.
    while allcomplete is False:

        now = time.time()

        # Check if we should be polling.
        if int(now - lastpolltime) > int(pollinterval):

            lastpolltime = int(now)
            saverecoveryfile = _polljobs(jobs, saverecoveryfile)
            saverecoveryfile = _checkwaitingjobs(jobs, saverecoveryfile)

        # Check if we should be staging.
        if ((int(now - laststagetime) > int(stageinterval) and
                int(stageinterval) != 0) or allfinished is True):

            laststagetime = int(now)
            saverecoveryfile = _stagejobfiles(jobs, saverecoveryfile)

        # Update the queue info settings to each job just in case something
        # happens requiring user to use recovery.
        for job in jobs:

            jobs[job]["queue-slots"] = \
                QUEUEINFO[jobs[job]["resource"]]["queue-slots"]
            jobs[job]["queue-max"] = \
                QUEUEINFO[jobs[job]["resource"]]["queue-max"]

        # Save out the recovery files.
        if (os.path.isdir(os.path.expanduser('~/.Longbow')) and
                saverecoveryfile is True and recoveryfileerror is False):

            saverecoveryfile = False

            try:

                configuration.saveini(JOBFILE, jobs)

            except (OSError, IOError):

                recoveryfileerror = True

                LOG.warning("Could not write recovery file, possibly due to "
                            "permissions on the ~/.Longbow directory.")

        allcomplete, allfinished = _checkcomplete(jobs)

    complete = 0
    error = 0

    for job in jobs:

        if jobs[job]["laststatus"] == "Submit Error":

            error = error + 1

        else:

            complete = complete + 1

    LOG.info("Session complete - %s jobs ran - %s jobs encountered submission "
             "errors.", complete, error)


def prepare(jobs):
    """A generic method for creating job submit scripts.

    A method containing the generic and boiler plate Longbow code for
    constructing the submit file.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    LOG.info("Creating submit files for job/s.")

    for item in jobs:

        job = jobs[item]
        scheduler = job["scheduler"]

        try:

            LOG.info("Creating submit file for job '%s'", item)

            getattr(schedulers, scheduler.lower()).prepare(job)

            LOG.info("Submit file created successfully")

        except AttributeError:

            raise exceptions.PluginattributeError(
                "prepare method cannot be found in plugin '{0}'"
                .format(scheduler))

    LOG.info("Submit file/s created.")


def submit(jobs):
    """A generic method for submitting jobs.

    A method containing the generic and boiler plate Longbow code for
    submitting a job.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    # Initialise some counters.
    submitted = 0
    queued = 0
    error = 0

    LOG.info("Submitting job/s.")

    for item in jobs:

        job = jobs[item]

        # Have we got this resource already?
        if job["resource"] not in QUEUEINFO:

            # no, well create it.
            QUEUEINFO[job["resource"]] = {"queue-slots": str(0),
                                          "queue-max": str(0)}

    for item in jobs:

        job = jobs[item]
        scheduler = job["scheduler"]

        # Try and submit.
        try:

            getattr(schedulers, scheduler.lower()).submit(job)

            LOG.info("Job '%s' submitted with id '%s'", item, job["jobid"])

            job["laststatus"] = "Queued"

            # Increment the queue counter by one (used to count the slots).
            QUEUEINFO[job["resource"]]["queue-slots"] = \
                str(int(QUEUEINFO[job["resource"]]["queue-slots"]) + 1)

            submitted += 1

        # Submit method can't be found.
        except AttributeError:

            raise exceptions.PluginattributeError(
                "submit method cannot be found in plugin '{0}'"
                .format(scheduler))

        # Some sort of error in submitting the job.
        except exceptions.JobsubmitError as err:

            LOG.error(err)

            job["laststatus"] = "Submit Error"

            error += 1

        # Hit maximum slots on resource, Longbow will sub-schedule these.
        except exceptions.QueuemaxError:

            LOG.info("The job '%s' has been held back by Longbow due to "
                     "reaching queue slot limit, it will be submitted when a "
                     "slot opens up.", item)

            # We will set a flag so that we can inform the user that it is
            # handled.
            job["laststatus"] = "Waiting Submission"

            queued += 1

        # We want to find out what the maximum number of slots we have are.
        if int(QUEUEINFO[job["resource"]]["queue-slots"]) > \
                int(QUEUEINFO[job["resource"]]["queue-max"]):

            QUEUEINFO[job["resource"]]["queue-max"] = \
                QUEUEINFO[job["resource"]]["queue-slots"]

    # Store a copy of the queueinfo data in the jobs data structure in case
    # recovery is needed.
    for item in jobs:

        job = jobs[item]

        job["queue-slots"] = QUEUEINFO[job["resource"]]["queue-slots"]
        job["queue-max"] = QUEUEINFO[job["resource"]]["queue-max"]

    # Save out the recovery files.
    if os.path.isdir(os.path.expanduser('~/.Longbow')):

        try:

            LOG.info("Recovery file will be placed at path '%s'", JOBFILE)

            configuration.saveini(JOBFILE, jobs)

        except (OSError, IOError):

            LOG.warning(
                "Could not write recovery file, possibly due to permissions "
                "on the ~/.Longbow directory.")

    LOG.info("%s Submitted, %s Held due to queue limits and %s Failed.",
             submitted, queued, error)


def _testscheduler(job):
    """The test logic for finding out what scheduler is on the system."""
    schedulerqueries = getattr(schedulers, "QUERY")

    LOG.info("No environment for this host '%s' is specified - attempting to "
             "determine it!", job["resource"])

    # Go through the schedulers we are supporting.
    for param in schedulerqueries:

        try:

            shellwrappers.sendtossh(job, schedulerqueries[param])

            job["scheduler"] = param

            LOG.info("The environment on this host is '%s'", param)
            break

        except exceptions.SSHError:

            LOG.debug("Environment is not '%s'", param)

    if job["scheduler"] is "":

        raise exceptions.SchedulercheckError("Could not find the job "
                                             "scheduling system.")


def _testhandler(job):
    """A method for finding out job handler is on the system."""
    # Initialise variables.
    handlers = {
        "aprun": ["which aprun"],
        "mpirun": ["which mpirun"]
    }

    LOG.info("No queue handler was specified for host '%s' - attempting to "
             "find it", job["resource"])

    modules = []

    # Go through the handlers and find out which is there. Load modules first
    # as this is necessary for some remote resources
    for module in job["modules"].split(","):

        module = module.replace(" ", "")
        modules.extend(["module load " + module + "\n"])

    for param in handlers:

        try:

            cmd = modules[:]
            cmd.extend(handlers[param])
            shellwrappers.sendtossh(job, cmd)

            job["handler"] = param

            LOG.info("The batch queue handler is '%s'", param)
            break

        except exceptions.SSHError:

            LOG.debug("The batch queue handler is not '%s'", param)

    if job["handler"] is "":

        raise exceptions.HandlercheckError("Could not find the batch queue "
                                           "handler.")


def _monitorinitialise(jobs):
    """Setup the conditions for monitoring jobs."""
    # Initialise values.
    pollinterval = 0
    stageinterval = 0

    # Sort out some defaults.
    for job in jobs:

        # If we came from recovery mode then rebuild the queueinfo structure.
        if jobs[job]["resource"] not in QUEUEINFO:

            QUEUEINFO[jobs[job]["resource"]] = {
                "queue-slots": jobs[job]["queue-slots"],
                "queue-max": jobs[job]["queue-max"]
            }

        # This should always be present.
        if "laststatus" not in jobs[job]:

            jobs[job]["laststatus"] = ""

        # Set the file transfer interval.
        if stageinterval < int(jobs[job]["staging-frequency"]):

            stageinterval = int(jobs[job]["staging-frequency"])

        # Attempt to grab a polling frequency that might have been set
        if pollinterval < int(jobs[job]["polling-frequency"]):

            pollinterval = int(jobs[job]["polling-frequency"])

    # If somehow the polling interval parameter is still zero, reduce the
    # polling to once every 5 minutes.
    if pollinterval is 0:

        pollinterval = 300

    return stageinterval, pollinterval


def _polljobs(jobs, save):
    """A method to poll the status of all jobs.

    Poll the status of all jobs that are not in error states, queued or
    finihed.

    """
    for job in jobs:

        if (jobs[job]["laststatus"] != "Finished" and
                jobs[job]["laststatus"] != "Complete" and
                jobs[job]["laststatus"] != "Submit Error" and
                jobs[job]["laststatus"] != "Waiting Submission"):

            # Get the job status.
            try:

                status = getattr(
                    schedulers, jobs[job]["scheduler"].lower()).status(
                        jobs[job])

            except AttributeError:

                raise exceptions.PluginattributeError(
                    "Status method cannot be"
                    "found in plugin '{0}'".format(jobs[job]["scheduler"]))

            # If the last status is different then change the flag (stops
            # logfile getting flooded!)
            if jobs[job]["laststatus"] != status:

                jobs[job]["laststatus"] = status

                save = True

                if status == "Finished":

                    resource = jobs[job]["resource"]
                    QUEUEINFO[resource]["queue-slots"] = \
                        str(int(QUEUEINFO[resource]["queue-slots"]) - 1)

                LOG.info("Status of job '%s' with id '%s' is '%s'", job,
                         jobs[job]["jobid"], status)

    return save


def _stagejobfiles(jobs, save):
    """A method to stage all files for each running job.

    Stage all files for each running job. For jobs that are finished, stage
    and remove them from the QUEUEINFO data and then change their status to
    complete. This will stop future staging.

    """
    for job in jobs:

        if (jobs[job]["laststatus"] == "Running" or
                jobs[job]["laststatus"] == "Subjob(s) running" or
                jobs[job]["laststatus"] == "Finished"):

            staging.stage_downstream(jobs[job])

            if jobs[job]["laststatus"] == "Finished":

                jobs[job]["laststatus"] = "Complete"

                save = True

    return save


def _checkwaitingjobs(jobs, save):
    """Check if any jobs marked as "Waiting Submission" can be submitted."""
    for job in jobs:

        # Check if we can submit any further jobs.
        if (jobs[job]["laststatus"] == "Waiting Submission" and
                int(QUEUEINFO[jobs[job]["resource"]]["queue-slots"]) <
                int(QUEUEINFO[jobs[job]["resource"]]["queue-max"])):

            # Try and submit this job.
            try:

                getattr(schedulers,
                        jobs[job]["scheduler"].lower()).submit(jobs[job])

                jobs[job]["laststatus"] = "Queued"

                LOG.info("Job '%s' submitted with id '%s'", job,
                         jobs[job]["jobid"])

                # Increment the queue counter by one (used to count the slots).
                QUEUEINFO[jobs[job]["resource"]]["queue-slots"] = str(
                    int(QUEUEINFO[jobs[job]["resource"]]["queue-slots"]) + 1)

                save = True

            except AttributeError:

                # Submit method can't be found.
                raise exceptions.PluginattributeError(
                    "Submit method cannot be found in plugin '{0}'"
                    .format(jobs[job]["scheduler"]))

            # Some sort of error in submitting the job.
            except exceptions.JobsubmitError as err:

                LOG.error(err)

                jobs[job]["laststatus"] = "Submit Error"

            # This time if a queue error is raised it might be due to other
            # constraints such as resource limits on the queue.
            except exceptions.QueuemaxError:

                LOG.error("Job is still failing to submit, which could "
                          "indicate problems with resource limits for this "
                          "particular queue - marking this as in error state")

                jobs[job]["laststatus"] = "Submit Error"

    return save


def _checkcomplete(jobs):
    """Check if all the jobs are complete."""
    # Initialise variables
    allcomplete = False
    allfinished = False
    complete = []
    error = []
    finished = []

    for job in jobs:

        if jobs[job]["laststatus"] != "Submit Error":

            complete.append(jobs[job]["laststatus"])

        if (jobs[job]["laststatus"] != "Submit Error" and
                jobs[job]["laststatus"] != "Complete"):

            finished.append(jobs[job]["laststatus"])

        if jobs[job]["laststatus"] == "Submit Error":

            error.append(jobs[job]["laststatus"])

    if all(state == "Complete" for state in complete) and len(complete) != 0:

        allcomplete = True

    if len(error) == len(jobs):

        allcomplete = True

    if all(state == "Finished" for state in finished) and len(finished) != 0:

        allfinished = True

    return allcomplete, allfinished
