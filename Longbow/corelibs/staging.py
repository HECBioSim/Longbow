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

""" The staging module provides methods for processing the transfer of files
between the local host and the remote host job directories. The following
methods are contained within this module:

stage_upstream(jobs)
stage_downstream(jobs)
cleanup(jobs)

Where jobs is a dictionary of job configurations."""

import os
import logging
import corelibs.shellwrappers as shellwrappers

LOGGER = logging.getLogger("Longbow")


def stage_upstream(hosts, jobs):

    """Method for staging files to the remote machines, this method takes
    a dictionary of jobs and processes the information from the filelist.
    """

    LOGGER.info("Staging files for job/s.")

    for job in jobs:

        # Check that the working directory exists.
        try:
            shellwrappers.remotelist(hosts[jobs[job]["resource"]],
                                     jobs[job]["remoteworkdir"])
            LOGGER.debug("  Work directory '%s' found.",
                         jobs[job]["remoteworkdir"])
        except:
            raise RuntimeError("Work directory '%s' could not be found " %
                               jobs[job]["remoteworkdir"] + "on remote " +
                               "machine '%s'." % jobs[job]["resource"])

        # Check if path is already on remote host and delete its contents
        # if it does.
        path = os.path.join(jobs[job]["remoteworkdir"], job)
        try:
            shellwrappers.remotelist(hosts[jobs[job]["resource"]], path)
            LOGGER.debug("  directory '%s' already exists, emptying" +
                         " its contents in preparation for staging.", path)
            shellwrappers.remotedelete(hosts[jobs[job]["resource"]], path)
            shellwrappers.sendtossh(hosts[jobs[job]["resource"]],
                                    ["mkdir " + path])
        except RuntimeError:
            # Directory doesn't exist so create it.
            shellwrappers.sendtossh(hosts[jobs[job]["resource"]],
                                    ["mkdir " + path])

        # Loop through all files.
        LOGGER.info("  Transfering files for job: '%s' to host: %s",
                    job, jobs[job]["resource"])

        for item in jobs[job]["filelist"]:

            # Source of the file locally.
            src = os.path.join(jobs[job]["localworkdir"], item)

            # Does the item contain a sub directory.
            directory = os.path.dirname(item)
            if directory is not "":

                subdir = os.path.join(path, directory)

                # Then does it already exist
                try:
                    shellwrappers.remotelist(hosts[jobs[job]["resource"]],
                                             subdir)
                # If not then make it.
                except RuntimeError:
                    shellwrappers.sendtossh(hosts[jobs[job]["resource"]],
                                            ["mkdir " + subdir])

            # Transfer file upstream.
            shellwrappers.upload("rsync", hosts[jobs[job]["resource"]], src,
                                 os.path.join(path, directory))

    LOGGER.info("Staging files upstream - complete.")


def stage_downstream(hosts, jobs, jobname):

    """Method for returning files from the remote machines."""

    # Have we been passed a single job or set of jobs.
    if jobname == "All":

        LOGGER.info("Staging from remote to local host.")

        # We must have multiple jobs so loop through them.
        for job in jobs:

            # Download the whole directory with rsync.
            host = hosts[jobs[job]["resource"]]
            src = os.path.join(jobs[job]["remoteworkdir"], job + "/")
            dst = jobs[job]["localworkdir"]
            shellwrappers.download("rsync", host, src, dst)

        LOGGER.info("Staging files downstream - complete.")

    # Else we have a single job.
    else:
        LOGGER.info("  For job %s staging files downstream.", jobname)

        host = hosts[jobs[jobname]["resource"]]
        src = os.path.join(jobs[jobname]["remoteworkdir"], jobname + "/")
        dst = jobs[jobname]["localworkdir"]
        # Download the whole directory with rsync.
        shellwrappers.download("rsync", host, src, dst)

        LOGGER.info("  staging complete.")


def cleanup(hosts, jobs):

    """Method for cleaning up the remote work directory."""

    LOGGER.info("Cleaning up the work directories.")

    for job in jobs:

        try:

            path = os.path.join(jobs[job]["remoteworkdir"], job)
            host = hosts[jobs[job]["resource"]]

            shellwrappers.remotelist(host, path)

            LOGGER.info("  Deleting directory for job '%s' - %s", job, path)

            shellwrappers.remotedelete(hosts[jobs[job]["resource"]], path)

        except RuntimeError:
            # directory doesn't exist.
            LOGGER.debug("Directory on path '%s' does not exist - skipping.",
                         path)

    LOGGER.info("Cleaning up complete.")
