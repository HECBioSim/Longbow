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

"""
The staging module provides methods for processing the transfer of files
between the local host and the remote host job directories.

The following methods are contained within this module:

stage_upstream()
    A method for staging files for each job to the target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

stage_downstream()
    A method for staging files for each job to from target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

cleanup()
    A method for cleaning up the working directory on the HPC host, this method
    will only delete job directories that are valid for the given Longbow
    instance, thus avoid data loss.
"""

import logging

try:

    EX = __import__("corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("corelibs.shellwrappers", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("Longbow.corelibs.shellwrappers", fromlist=[''])

LOGGER = logging.getLogger("Longbow")


def stage_upstream(hosts, jobs):

    """
    A method for staging files for each job to the target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

    Required arguments are:

    hosts (dictionary) - The Longbow hosts data structure, see configuration.py
                         for more information about the format of this
                         structure.

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOGGER.info("Staging files for job/s.")

    for job in jobs:

        host = hosts[jobs[job]["resource"]]
        src = jobs[job]["localworkdir"]
        dst = jobs[job]["destdir"]

        LOGGER.info("Transfering files for job '{0}' to host '{1}'"
                    .format(job, jobs[job]["resource"]))

        cmd = []
        cmd.extend(["mkdir -p " + dst + "\n"])

        try:

            SHELLWRAPPERS.sendtossh(host, cmd)

            LOGGER.info("mkdir -p '{0}' passed.".format(dst))

        except EX.SSHError:

            LOGGER.error("mkdir -p '{0}' failed.".format(dst))
            raise

        # Transfer files upstream.
        try:

            SHELLWRAPPERS.upload(
                host, src + "/", dst,
                jobs[job]["upload-include"],
                jobs[job]["upload-exclude"])

        except EX.RsyncError:

            raise EX.StagingError("Could not stage file '{0}' upstream"
                                  .format(src))

    LOGGER.info("Staging files upstream - complete.")


def stage_downstream(hosts, jobs, jobname):

    """
    A method for staging files for each job to from target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

    Required arguments are:

    hosts (dictionary) - The Longbow hosts data structure, see configuration.py
                         for more information about the format of this
                         structure.

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    jobname (string) - A string that matches the name of a job to be staged.
                       (primary key in jobs dict)
    """

    LOGGER.info("For job '{0}' staging files downstream.".format(jobname))

    host = hosts[jobs[jobname]["resource"]]
    src = jobs[jobname]["destdir"] + "/"
    dst = jobs[jobname]["localworkdir"]

    # Download the whole directory with rsync.
    try:

        SHELLWRAPPERS.download(
            host, src, dst,
            jobs[jobname]["download-include"],
            jobs[jobname]["download-exclude"])

    except (EX.SCPError, EX.RsyncError):

        raise EX.StagingError("Could not download file '{0}' "
                              "to location '{1}'".format(src, dst))

    LOGGER.info("Staging complete.")


def cleanup(hosts, jobs):

    """
    A method for cleaning up the working directory on the HPC host, this method
    will only delete job directories that are valid for the given Longbow
    instance, thus avoid data loss.

    Required arguments are:

    hosts (dictionary) - The Longbow hosts data structure, see configuration.py
                         for more information about the format of this
                         structure.

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOGGER.info("Cleaning up the work directories.")

    for job in jobs:

        try:

            host = hosts[jobs[job]["resource"]]
            path = jobs[job]["destdir"]

            SHELLWRAPPERS.remotelist(host, path)

            if path != hosts[jobs[job]["resource"]]["remoteworkdir"]:
                LOGGER.info("Deleting directory for job '{0}' - '{1}'"
                            .format(job, path))

                SHELLWRAPPERS.remotedelete(hosts[jobs[job]["resource"]], path)

            else:
                raise EX.RemoteworkdirError("Subdirectory of remoteworkdir" +
                                            " not yet created")

        except EX.RemoteworkdirError:

            LOGGER.debug("For job '{0}', cleanup not required because"
                         " the '{1}xxxxx' subdirectory of {2} in which the job"
                         " would have run has not not yet been created on the"
                         " remote resource.".format(job,
                                                    job,
                                                    host["remoteworkdir"]))

        except EX.RemotelistError:

            # Directory doesn't exist.
            LOGGER.debug("Directory on path '{0}' does not exist - skipping."
                         .format(path))

        except KeyError:

            LOGGER.debug("For job '{0}', cleanup not required - skipping."
                         .format(job))

        except EX.RemotedeleteError:

            LOGGER.debug("For job '{0}', cannot delete directory '{1}' - "
                         "skipping.".format(job, path))

    LOGGER.info("Cleaning up complete.")
