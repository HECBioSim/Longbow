# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of
# the HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the
# UK biomolecular simulation community on resources such as ARCHER.
#
# Longbow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Longbow is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Longbow.  If not, see <http://www.gnu.org/licenses/>.

"""This module contains the methods for preparing, submitting, deleting and
monitoring jobs. The following methods abstract the schedulers:

delete()
monitor()
prepare()
submit()

The remaining methods of the form env_method() are abstractions specific to
each scheduler, it is not recommended to use these directly unless it is
necessary.
"""

import time
import logging

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

LOGGER = logging.getLogger("Longbow")


def testenv(hostconf, hosts, jobs):

    """This method makes an attempt to test the environment and determine from
    a pre-configured list what scheduler and job submission handler is present
    on the machine."""

    schedulerqueries = getattr(SCHEDULERS, "QUERY")

    handlers = {
        "aprun": ["which aprun"],
        "mpirun": ["which mpirun"]
    }

    save = False

    checked = []

    # Take a look at each job.
    for job in jobs:

        resource = jobs[job]["resource"]

        # If we have not checked this host already
        if resource not in checked:

            # Make sure we don't check the same thing again.
            checked.extend([resource])

            # If we have no scheduler defined by the user then find it.
            if hosts[resource]["scheduler"] is "":

                LOGGER.info(
                    "No environment for this host '{0}' is specified - "
                    "attempting to determine it!".format(resource))

                # Go through the schedulers we are supporting.
                for param in schedulerqueries:

                    try:

                        SHELLWRAPPERS.sendtossh(hosts[resource],
                                                schedulerqueries[param])

                        hosts[resource]["scheduler"] = param

                        LOGGER.info(
                            "The environment on this host is '{0}'"
                            .format(param))
                        break

                    except EX.SSHError:

                        LOGGER.debug("Environment is not '{0}'".format(param))

                if hosts[resource]["scheduler"] is "":

                    raise EX.SchedulercheckError(
                        "Could not find the job scheduling system.")

                # If we changed anything then mark for saving.
                save = True

            else:

                LOGGER.info(
                    "The environment on host '{0}' is '{1}'"
                    .format(resource, hosts[resource]["scheduler"]))

            # If we have no job handler defined by the user then find it.
            if hosts[resource]["handler"] is "":

                LOGGER.info(
                    "No queue handler was specified for host '{0}' - "
                    "attempting to find it".format(resource))

                # Go through the handlers and find out which is there.
                # Load modules first as this is necessary for some remote
                # resources
                cmdmod = []

                for module in jobs[job]["modules"].split(","):

                    module = module.replace(" ", "")
                    cmdmod.extend(["module load " + module + "\n"])

                for param in handlers:

                    try:

                        cmd = cmdmod[:]
                        cmd.extend(handlers[param])
                        SHELLWRAPPERS.sendtossh(hosts[resource], cmd)

                        hosts[resource]["handler"] = param

                        LOGGER.info("The batch queue handler is '{0}'"
                                    .format(param))

                        break

                    except EX.SSHError:

                        LOGGER.debug(
                            "The batch queue handler is not '{0}'"
                            .format(param))

                if hosts[resource]["handler"] is "":

                    raise EX.HandlercheckError(
                        "Could not find the batch queue handler.")

                # If we changed anything then mark for saving.
                save = True

            else:

                LOGGER.info(
                    "The handler on host '{0}' is '{1}'"
                    .format(resource, hosts[resource]["handler"]))

    # Do we have anything to change in the host file.
    if save is True:

        CONFIGURATION.saveconfigs(hostconf, hosts)


def delete(hosts, jobs, jobname):

    """The generic method for deleting jobs."""

    scheduler = hosts[jobs[jobname]["resource"]]["scheduler"]
    host = hosts[jobs[jobname]["resource"]]
    job = jobs[jobname]

    try:

        getattr(SCHEDULERS, scheduler.lower()).delete(host, job)

    except AttributeError:

        raise EX.PluginattributeError(
            "delete method cannot be found in plugin '{0}'"
            .format(scheduler))

    except EX.JobdeleteError:

        LOGGER.info("Unable to delete job '{0}'".format(jobname))


def monitor(hosts, jobs):

    """The generic method for monitoring jobs, this methods contains the
    monitoring loop and logic for keeping track of jobs and initiating
    staging of jobs."""

    LOGGER.info("Monitoring job/s")

    # Some initial values
    allfinished = False
    interval = 0

    # Find out which job has been set the highest polling frequency and use
    # that.
    for job in jobs:

        jobs[job]["laststatus"] = ""

        if interval < int(jobs[job]["frequency"]):

            interval = int(jobs[job]["frequency"])

    # Loop until all jobs are done.
    while allfinished is False:

        for job in jobs:

            if jobs[job]["laststatus"] != "Finished" and \
               jobs[job]["laststatus"] != "Submit Error":

                machine = jobs[job]["resource"]
                scheduler = hosts[machine]["scheduler"]
                host = hosts[machine]

                # Get the job status.
                try:

                    status = getattr(
                        SCHEDULERS, scheduler.lower()).status(
                            host, jobs[job]["jobid"])

                except AttributeError:

                    raise EX.PluginattributeError(
                        "status method cannot be found in plugin '{0}'"
                        .format(scheduler))

                # If the last status is different then change the flag (stops
                # logfile getting flooded!)
                if jobs[job]["laststatus"] != status:

                    jobs[job]["laststatus"] = status
                    LOGGER.info(
                        "Status of job '{0}' with id '{1}' is '{2}'"
                        .format(job, jobs[job]["jobid"], status))

                # If the job is not finished and we set the polling frequency
                # higher than 0 (off) then stage files.
                if (jobs[job]["laststatus"] == "Running" or
                        jobs[job]["laststatus"] == "Subjob(s) running" and
                        interval is not 0):

                    STAGING.stage_downstream(hosts, jobs, job)

                # If job is done wait 60 seconds then transfer files (this is
                # to stop users having to wait till all jobs end to grab last
                # bit of staged files.)
                if jobs[job]["laststatus"] == "Finished":

                    LOGGER.info(
                        "Job '{0}' is finishing, staging will begin in 60 "
                        "seconds".format(job))

                    time.sleep(60.0)

                    STAGING.stage_downstream(hosts, jobs, job)

        # If the polling interval is set at zero then staging will be disabled
        # however continue to poll jobs but do it on a low frequency. Staging
        # will however still occur once the job is finished.
        if interval is 0:

            time.sleep(120.0)

        # Find out if all jobs are completed.
        for job in jobs:

            if jobs[job]["laststatus"] != "Finished" and \
               jobs[job]["laststatus"] != "Submit Error":

                allfinished = False
                break

            allfinished = True

        # If we still have jobs running then wait here for desired time before
        # looping again.
        if allfinished is False:

            time.sleep(float(interval))

    LOGGER.info("All jobs are complete.")


def prepare(hosts, jobs):

    """The generic methods for preparing jobs, this points to the correct
    scheduler specific method for job preparation."""

    LOGGER.info("Creating submit files for job/s.")

    for job in jobs:

        scheduler = hosts[jobs[job]["resource"]]["scheduler"]

        try:

            getattr(SCHEDULERS, scheduler.lower()).prepare(hosts, job, jobs)

        except AttributeError:

            raise EX.PluginattributeError(
                "prepare method cannot be found in plugin '{0}'"
                .format(scheduler))

    LOGGER.info("Submit file/s created.")


def submit(hosts, jobs):

    """Generic method for submitting jobs, this points to the scheduler
    specific method for job submission."""

    LOGGER.info("Submitting job/s.")

    for job in jobs:

        machine = jobs[job]["resource"]
        scheduler = hosts[machine]["scheduler"]
        host = hosts[machine]

        try:

            getattr(SCHEDULERS, scheduler.lower()).submit(host, job, jobs)

        except AttributeError:

            raise EX.PluginattributeError(
                "submit method cannot be found in plugin '{0}'"
                .format(scheduler))

        except EX.JobsubmitError as err:

            LOGGER.info(
                "Submitting job '{0}' failed with message - '{1}'"
                .format(job, err))

            jobs[job]["laststatus"] = "Submit Error"

    LOGGER.info("Submission complete.")
