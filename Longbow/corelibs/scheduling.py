# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of Longbow.
#
# Longbow is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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
import corelibs.shellwrappers as shellwrappers
import corelibs.exceptions as ex
import corelibs.configuration as configuration
import corelibs.staging as staging
import plugins.schedulers as schedulers

LOGGER = logging.getLogger("Longbow")


def testenv(hostconf, hosts, jobs):

    """This method makes an attempt to test the environment and determine from
    a pre-configured list what scheduler and job submission handler is present
    on the machine."""

    schedulerqueries = getattr(schedulers, "QUERY")

    handlers = {"aprun": ["which aprun"],
                "mpirun": ["which mpirun"]
                }

    save = False

    checked = []

    # Take a look at each job.
    for job in jobs:

        resource = jobs[job]["resource"]

        # If the we have not checked this host already
        if resource not in checked:

            # Make sure we don't check the same thing again.
            checked.extend([resource])

            # If we have no scheduler defined by the user then find it.
            if hosts[resource]["scheduler"] is "":
                LOGGER.info("No environment for this host '%s' "
                            % resource + "is specified - attempting " +
                            "to determine it!")

                # Go through the schedulers we are supporting.
                for param in schedulerqueries:
                    try:
                        shellwrappers.sendtossh(hosts[resource],
                                                schedulerqueries[param])

                        hosts[resource]["scheduler"] = param

                        LOGGER.info("  The environment on this host is '%s'",
                                    param)
                        break

                    except ex.SSHError:
                        LOGGER.debug("  Environment is not '%s'", param)

                if hosts[resource]["scheduler"] is "":
                    raise ex.SchedulercheckError("  Could not find the job " +
                        "scheduling system.")

                # If we changed anything then mark for saving.
                save = True

            else:
                LOGGER.info("The environment on host '%s' is '%s'", resource,
                            hosts[resource]["scheduler"])

            # If we have no job handler defined by the user then find it.
            if hosts[resource]["handler"] is "":
                LOGGER.info("No queue handler was specified for host '%s' - " +
                            "attempting to find it", resource)

                # Go through the handlers and find out which is there.
                for param in handlers:
                    try:
                        shellwrappers.sendtossh(hosts[resource],
                                                handlers[param])

                        hosts[resource]["handler"] = param

                        LOGGER.info("  The batch queue handler is '%s'", param)

                        break

                    except ex.SSHError:
                        LOGGER.debug("  The batch queue handler is not '%s'",
                                     param)

                if hosts[resource]["handler"] is "":
                    raise ex.HandlercheckError("  Could not find the batch "
                        "queue handler.")

                # If we changed anything then mark for saving.
                save = True

            else:
                LOGGER.info("The handler on host '%s' is '%s'", resource,
                            hosts[resource]["handler"])

    # Do we have anything to change in the host file.
    if save is True:
        configuration.saveconfigs(hostconf, hosts)


def delete(hosts, jobs, jobname):

    """The generic method for deleting jobs."""

    if jobname == "All":

        for job in jobs:

            scheduler = hosts[jobs[job]["resource"]]["scheduler"]
            host = hosts[jobs[job]["resource"]]
            jobid = jobs[job]["jobid"]

            try:
                getattr(schedulers, scheduler.lower()).delete(host, jobid)

            except AttributeError:
                raise ex.PluginattributeError("delete method cannot be " +
                    "found in plugin '%s'", scheduler)

            except ex.JobdeleteError:
                LOGGER.info("  Unable to delete job '%s'", job)

    else:

        scheduler = hosts[jobs[jobname]["resource"]]["scheduler"]
        host = hosts[jobs[jobname]["resource"]]
        jobid = jobs[jobname]["jobid"]

        try:
            getattr(schedulers, scheduler.lower()).delete(host, jobid)

        except AttributeError:
            raise ex.PluginattributeError("delete method cannot be " +
                "found in plugin '%s'", scheduler)

        except ex.JobdeleteError:
            LOGGER.info("  Unable to delete job '%s'", job)


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
        if interval < jobs[job]["frequency"]:
            interval = jobs[job]["frequency"]

    # Loop until all jobs are done.
    while allfinished is False:

        for job in jobs:

            if (jobs[job]["laststatus"] != "Finished" and
                jobs[job]["laststatus"] != "Submit Error"):

                machine = jobs[job]["resource"]
                scheduler = hosts[machine]["scheduler"]
                host = hosts[machine]

                # Get the job status.
                try:
                    status = getattr(schedulers,
                        scheduler.lower()).status(host,
                            jobs[job]["jobid"])

                except AttributeError:
                    raise ex.PluginattributeError("status method cannot be " +
                        "found in plugin '%s'", scheduler)

                # If the last status is different then change the flag (stops
                # logfile getting flooded!)
                if jobs[job]["laststatus"] != status:
                    jobs[job]["laststatus"] = status
                    LOGGER.info("  Job: %s with id: %s is %s", job,
                                jobs[job]["jobid"], status)

                # If the job is not finished and we set the polling frequency
                # higher than 0 (off) then stage files.
                if jobs[job]["laststatus"] == "Running" and interval is not 0:
                    staging.stage_downstream(hosts, jobs, job)

                # If job is done wait 60 seconds then transfer files (this is
                # to stop users having to wait till all jobs end to grab last
                # bit of staged files.)
                if jobs[job]["laststatus"] == "Finished":
                    LOGGER.info("  Job %s is finishing, staging will " % job +
                                "begin in 60 seconds")
                    time.sleep(60.0)
                    staging.stage_downstream(hosts, jobs, job)

        # Find out if all jobs are completed.
        for job in jobs:

            if (jobs[job]["laststatus"] != "Finished" and
                jobs[job]["laststatus"] != "Submit Error"):
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
            getattr(schedulers, scheduler.lower()).prepare(hosts, job, jobs)

        except AttributeError:
            raise ex.PluginattributeError("prepare method cannot be found in" +
                "plugin '%s'", scheduler)

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
            getattr(schedulers, scheduler.lower()).submit(host, job, jobs)

        except AttributeError:
            raise ex.PluginattributeError("submit method cannot be found in" +
                "plugin '%s'", scheduler)

        except ex.JobsubmitError as err:
            LOGGER.info("Submitting job '%s' failed with message - %s",
                        job, err)
            jobs[job]["laststatus"] = "Submit Error"

    LOGGER.info("Submission complete.")
