# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of
# the HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the
# UK biomolecular simulation community on resources such as Archer.
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

""" The staging module provides methods for processing the transfer of files
between the local host and the remote host job directories. The following
methods are contained within this module:

stage_upstream(jobs)
stage_downstream(jobs)
cleanup(jobs)

Where jobs is a dictionary of job configurations."""

import os
import logging

try:
    import Longbow.corelibs.exceptions as ex
except ImportError:
    import corelibs.exceptions as ex

try:
    import Longbow.corelibs.shellwrappers as shellwrappers
except ImportError:
    import corelibs.shellwrappers as shellwrappers

LOGGER = logging.getLogger("Longbow")


def stage_upstream(hosts, jobs):

    """Method for staging files to the remote machines, this method takes
    a dictionary of jobs and processes the information from the filelist.
    """

    LOGGER.info("Staging files for job/s.")

    for job in jobs:

        host = hosts[jobs[job]["resource"]]
        src = jobs[job]["localworkdir"]
        dst = jobs[job]["destdir"]

        # Check if job directory exists on the remote hosts and delete it.
        try:
            shellwrappers.remotelist(host, dst)

            LOGGER.debug("directory '%s' already exists, emptying its "
                         "contents in preparation for staging.", dst)

            shellwrappers.remotedelete(host, dst)

        # If we have absolute path errors then we have a problem.
        except ex.AbsolutepathError:
            raise

        # If it doesn't exist then move on.
        except ex.RemotelistError:
            pass

        LOGGER.info("Transfering files for job: '%s' to host '%s'",
                    job, jobs[job]["resource"])

        # Transfer files upstream.
        try:
            shellwrappers.upload(
                host, src + "/", dst, jobs[job]["upload-include"],
                jobs[job]["upload-exclude"])

        except ex.RsyncError:
            raise ex.StagingError("Could not stage file '%s' upstream" % src)

    LOGGER.info("Staging files upstream - complete.")


def stage_downstream(hosts, jobs, jobname):

    """Method for returning files from the remote machines."""

    # Have we been passed a single job or set of jobs.
    if jobname == "All":

        LOGGER.info("Staging from remote to local host.")

        # We must have multiple jobs so loop through them.
        for job in jobs:
            remoteworkdir = hosts[jobs[job]["resource"]]["remoteworkdir"]

            # Download the whole directory with rsync.
            host = hosts[jobs[job]["resource"]]
            src = jobs[job]["destdir"] + "/"
            dst = jobs[job]["localworkdir"]

            try:
                shellwrappers.download(
                    host, src, dst, jobs[job]["rsync-include"],
                    jobs[job]["rsync-exclude"])

            except (ex.SCPError, ex.RsyncError):
                raise ex.StagingError("Could not download file '%s' " % src +
                                      "to location '%s'" % dst)

        LOGGER.info("Staging files downstream - complete.")

    # Else we have a single job.
    else:
        LOGGER.info("For job %s staging files downstream.", jobname)

        remoteworkdir = hosts[jobs[jobname]["resource"]]["remoteworkdir"]
        host = hosts[jobs[jobname]["resource"]]
        src = jobs[jobname]["destdir"] + "/"
        dst = jobs[jobname]["localworkdir"]

        # Download the whole directory with rsync.
        try:
            shellwrappers.download(host, src, dst,
                jobs[jobname]["download-include"],
                jobs[jobname]["download-exclude"])

        except (ex.SCPError, ex.RsyncError):
            raise ex.StagingError("Could not download file '%s' " % src +
                                  "to location '%s'" % dst)

        LOGGER.info("staging complete.")


def cleanup(hosts, jobs):

    """Method for cleaning up the remote work directory."""

    LOGGER.info("Cleaning up the work directories.")

    for job in jobs:
        try:
            remoteworkdir = hosts[jobs[job]["resource"]]["remoteworkdir"]
            host = hosts[jobs[job]["resource"]]
            path = os.path.join(remoteworkdir, job)

            shellwrappers.remotelist(host, path)

            LOGGER.info("Deleting directory for job '%s' - '%s'", job, path)

            shellwrappers.remotedelete(hosts[jobs[job]["resource"]], path)

        except ex.RemotelistError:
            # directory doesn't exist.
            LOGGER.debug("Directory on path '%s' does not exist - skipping.",
                         path)

        except ex.RemotedeleteError:
            raise

    LOGGER.info("Cleaning up complete.")
