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

# Depending on how longbow is installed/utilised the import will be slightly
# different, this should handle both cases.
try:

    CONFIGURATION = __import__("corelibs.configuration", fromlist=[''])
    EX = __import__("corelibs.exceptions", fromlist=[''])
    SCHEDULERS = __import__("plugins.schedulers", fromlist=[''])
    SHELLWRAPPERS = __import__("corelibs.shellwrappers", fromlist=[''])
    STAGING = __import__("corelibs.staging", fromlist=[''])

except ImportError:

    CONFIGURATION = __import__("Longbow.corelibs.configuration", fromlist=[''])
    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    SCHEDULERS = __import__("Longbow.plugins.schedulers", fromlist=[''])
    SHELLWRAPPERS = __import__("Longbow.corelibs.shellwrappers", fromlist=[''])
    STAGING = __import__("Longbow.corelibs.staging", fromlist=[''])

LOG = logging.getLogger("Longbow.corelibs.scheduling")
QUEUEINFO = {}


def testenv(jobs, hostconf):

    """
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

    schedulerqueries = getattr(SCHEDULERS, "QUERY")

    handlers = {
        "aprun": ["which aprun"],
        "mpirun": ["which mpirun"]
    }

    save = False

    checked = []
    saveparams = {}

    # Take a look at each job.
    for item in jobs:

        job = jobs[item]
        resource = job["resource"]

        # If we have not checked this host already
        if resource not in checked:

            # Make sure we don't check the same thing again.
            checked.extend([resource])

            # If we don't have the resource defined then define it.
            if resource not in saveparams:

                saveparams[resource] = {}

            # If we have no scheduler defined by the user then find it.
            if job["scheduler"] is "":

                LOG.info("No environment for this host '{0}' is specified - "
                         "attempting to determine it!".format(resource))

                # Go through the schedulers we are supporting.
                for param in schedulerqueries:

                    try:

                        SHELLWRAPPERS.sendtossh(job, schedulerqueries[param])

                        job["scheduler"] = param
                        saveparams[resource]["scheduler"] = param

                        LOG.info("The environment on this host is '{0}'"
                                 .format(param))
                        break

                    except EX.SSHError:

                        LOG.debug("Environment is not '{0}'".format(param))

                if job["scheduler"] is "":

                    raise EX.SchedulercheckError(
                        "Could not find the job scheduling system.")

                # If we changed anything then mark for saving.
                save = True

            else:

                LOG.info("The environment on host '{0}' is '{1}'"
                         .format(resource, job["scheduler"]))

            # If we have no job handler defined by the user then find it.
            if job["handler"] is "":

                LOG.info("No queue handler was specified for host '{0}' - "
                         "attempting to find it".format(resource))

                # Go through the handlers and find out which is there.
                # Load modules first as this is necessary for some remote
                # resources
                cmdmod = []

                for module in job["modules"].split(","):

                    module = module.replace(" ", "")
                    cmdmod.extend(["module load " + module + "\n"])

                for param in handlers:

                    try:

                        cmd = cmdmod[:]
                        cmd.extend(handlers[param])
                        SHELLWRAPPERS.sendtossh(job, cmd)

                        job["handler"] = param
                        saveparams[resource]["handler"] = param

                        LOG.info("The batch queue handler is '{0}'"
                                 .format(param))

                        break

                    except EX.SSHError:

                        LOG.debug("The batch queue handler is not '{0}'"
                                  .format(param))

                if job["handler"] is "":

                    raise EX.HandlercheckError(
                        "Could not find the batch queue handler.")

                # If we changed anything then mark for saving.
                save = True

            else:

                LOG.info("The handler on host '{0}' is '{1}'"
                         .format(resource, job["handler"]))

        # If resource has been checked.
        else:

            # Then we should have a look if the resource for this job has been
            # altered.
            if resource in saveparams:

                # Then check if scheduler has been added.
                if "scheduler" in saveparams[resource]:

                    job["scheduler"] = saveparams[resource]["scheduler"]

                # Then check if handler has been added.
                if "handler" in saveparams[resource]:

                    job["handler"] = saveparams[resource]["handler"]

    # Do we have anything to change in the host file.
    if save is True:

        CONFIGURATION.saveconfigs(hostconf, saveparams)


def delete(job):

    """
    A method containing the generic and boiler plate Longbow code for deleting
    a job.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.
    """

    scheduler = job["scheduler"]

    try:

        LOG.info("Deleting the job '{0}'" .format(job["jobname"]))

        getattr(SCHEDULERS, scheduler.lower()).delete(job)

    except AttributeError:

        raise EX.PluginattributeError(
            "delete method cannot be found in plugin '{0}'"
            .format(scheduler))

    except EX.JobdeleteError:

        LOG.info("Unable to delete job '{0}'".format(job["jobname"]))

    LOG.info("Deletion successful")


def monitor(jobs):

    """
    A method containing the generic and boiler plate Longbow code for
    monitoring a job, this method contains the entire structure of the loop
    that deals with monitoring jobs.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOG.info("Monitoring job/s")

    # Some initial values
    allfinished = False
    interval = 0
    longbowdir = os.path.expanduser('~/.Longbow')
    jobfile = os.path.join(longbowdir, "jobs.recovery")

    # Find out which job has been set the highest polling frequency and use
    # that.
    for item in jobs:

        job = jobs[item]

        # If we came from recovery mode then rebuild the queueinfo structure.
        if job["resource"] not in QUEUEINFO:

            QUEUEINFO[job["resource"]] = {"queue-slots": job["queue-slots"],
                                          "queue-max": job["queue-max"]}

        # Don't initialise if already set (submission errors are passed here)
        if "laststatus" not in job:
            job["laststatus"] = ""

        if interval < int(job["frequency"]):

            interval = int(job["frequency"])

    # Save out the recovery files.
    if os.path.isdir(longbowdir):

        try:

            CONFIGURATION.saveini(jobfile, jobs)

        except (OSError, IOError):

            LOG.warning(
                "Could not write recovery file, possibly due to permissions "
                "on the ~/.Longbow directory.")

    # Loop until all jobs are done.
    while allfinished is False:

        for item in jobs:

            job = jobs[item]
            scheduler = job["scheduler"]

            if (job["laststatus"] != "Finished" and
                    job["laststatus"] != "Submit Error" and
                    job["laststatus"] != "Waiting Submission"):

                # Get the job status.
                try:

                    status = getattr(SCHEDULERS, scheduler.lower()).status(job)

                except AttributeError:

                    raise EX.PluginattributeError(
                        "status method cannot be found in plugin '{0}'"
                        .format(scheduler))

                # If the last status is different then change the flag (stops
                # logfile getting flooded!)
                if job["laststatus"] != status:

                    job["laststatus"] = status

                    LOG.info("Status of job '{0}' with id '{1}' is '{2}'"
                             .format(item, job["jobid"], status))

                    # Save out the recovery files.
                    if os.path.isdir(longbowdir):

                        try:

                            CONFIGURATION.saveini(jobfile, jobs)

                        except (OSError, IOError):

                            LOG.warning(
                                "Could not write recovery file, possibly due "
                                "to permissions on the ~/.Longbow directory.")

                # If the job is not finished and we set the polling frequency
                # higher than 0 (off) then stage files.
                if (job["laststatus"] == "Running" or
                        job["laststatus"] == "Subjob(s) running" and
                        interval is not 0):

                    STAGING.stage_downstream(job)

                # If job is done wait 60 seconds then transfer files (this is
                # to stop users having to wait till all jobs end to grab last
                # bit of staged files.)
                if job["laststatus"] == "Finished":

                    QUEUEINFO[job["resource"]]["queue-slots"] = \
                        str(int(QUEUEINFO[job["resource"]]["queue-slots"]) - 1)

                    LOG.info("Job '{0}' is finishing, staging will begin in "
                             "60 seconds".format(item))

                    time.sleep(60.0)

                    STAGING.stage_downstream(job)

            # Check if we can submit any further jobs.
            if job["laststatus"] == "Waiting Submission":

                # If we have less occupied slots than the queue-max then we
                # can submit.
                if int(QUEUEINFO[job["resource"]]["queue-slots"]) < \
                   int(QUEUEINFO[job["resource"]]["queue-max"]):

                    # Try and submit this job.
                    try:

                        getattr(SCHEDULERS, scheduler.lower()).submit(job)

                        job["laststatus"] = "Queued"

                        LOG.info("Job '{0}' submitted with id '{1}'"
                                 .format(item, job["jobid"]))

                        # Increment the queue counter by one (used to count
                        # the slots).
                        QUEUEINFO[job["resource"]]["queue-slots"] = str(
                            int(QUEUEINFO[job["resource"]]["queue-slots"]) + 1)

                    # Submit method can't be found.
                    except AttributeError:

                        raise EX.PluginattributeError(
                            "submit method cannot be found in plugin '{0}'"
                            .format(scheduler))

                    # Some sort of error in submitting the job.
                    except EX.JobsubmitError as err:

                        LOG.error(err)

                        job["laststatus"] = "Submit Error"

                    # This time if a queue error is raised it might be due to
                    # other constraints such as resource limits on the queue.
                    except EX.QueuemaxError:

                        LOG.error("Job is still failing to submit, which "
                                  "could indicate problems with resource "
                                  "limits for this particular queue - marking "
                                  "this as in error state")

                        job["laststatus"] = "Submit Error"

        # If the polling interval is set at zero then staging will be disabled
        # however continue to poll jobs but do it on a low frequency. Staging
        # will however still occur once the job is finished.
        if interval is 0:

            # Default to 5 minute intervals
            time.sleep(300.0)

        # Update the queue info settings to each job just in case something
        # happens requiring user to use recovery.
        for item in jobs:

            job = jobs[item]

            job["queue-slots"] = QUEUEINFO[job["resource"]]["queue-slots"]
            job["queue-max"] = QUEUEINFO[job["resource"]]["queue-max"]

        # Find out if all jobs are completed.
        for item in jobs:

            job = jobs[item]

            # If a single job has a flag not associated with being done then
            # carry on.
            if job["laststatus"] != "Finished" and \
               job["laststatus"] != "Submit Error":

                allfinished = False
                break

            allfinished = True

        # If we still have jobs running then wait here for desired time before
        # looping again.
        if allfinished is False:

            time.sleep(float(interval))

    LOG.info("All jobs are complete.")


def prepare(jobs):

    """
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

            LOG.info("Creating submit file for job '{0}'" .format(item))

            getattr(SCHEDULERS, scheduler.lower()).prepare(job)

            LOG.info("Submit file created successfully")

        except AttributeError:

            raise EX.PluginattributeError(
                "prepare method cannot be found in plugin '{0}'"
                .format(scheduler))

    LOG.info("Submit file/s created.")


def submit(jobs):

    """
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

            getattr(SCHEDULERS, scheduler.lower()).submit(job)

            LOG.info("Job '{0}' submitted with id '{1}'"
                     .format(item, job["jobid"]))

            job["laststatus"] = "Queued"

            # Increment the queue counter by one (used to count the slots).
            QUEUEINFO[job["resource"]]["queue-slots"] = \
                str(int(QUEUEINFO[job["resource"]]["queue-slots"]) + 1)

            submitted += 1

        # Submit method can't be found.
        except AttributeError:

            raise EX.PluginattributeError("submit method cannot be found in "
                                          "plugin '{0}'".format(scheduler))

        # Some sort of error in submitting the job.
        except EX.JobsubmitError as err:

            LOG.error(err)

            job["laststatus"] = "Submit Error"

            error += 1

        # Hit maximum slots on resource, Longbow will sub-schedule these.
        except EX.QueuemaxError:

            LOG.info("The job '{0}' has been held back by Longbow due to "
                     "reaching queue slot limit, it will be submitted when a "
                     "slot opens up.".format(item))

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

    LOG.info("{0} Submitted, {1} Held due to queue limits and {2} Failed."
             .format(submitted, queued, error))
