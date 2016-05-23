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
The staging module provides methods for processing the transfer of files
between the local host and the remote host job directories.

The following methods are contained within this module:

stage_upstream(jobs)
    A method for staging files for each job to the target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

stage_downstream(job)
    A method for staging files for each job to from target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

cleanup(jobs)
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

LOG = logging.getLogger("Longbow.corelibs.staging")


def stage_upstream(jobs):

    """
    A method for staging files for each job to the target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOG.info("Staging files for job/s.")

    for item in jobs:

        job = jobs[item]
        destdir = job["destdir"]

        LOG.info("Transfering files for job '{0}' to host '{1}'"
                 .format(item, job["resource"]))

        try:

            SHELLWRAPPERS.sendtossh(job, ["mkdir -p " + destdir + "\n"])

            LOG.info("Creation of directory '{0}' - successful."
                     .format(destdir))

        except EX.SSHError:

            LOG.error(
                "Creation of directory '{0}' - failed. Make sure that you "
                "have write permissions at the top level of the path given."
                .format(destdir))

            raise

        # Transfer files upstream.
        try:

            SHELLWRAPPERS.upload(job)

        except EX.RsyncError:

            raise EX.StagingError(
                "Could not stage '{0}' upstream, make sure that you have "
                "supplied the correct remote working directory and that you "
                "have chosen a path that you can write to."
                .format(job["localworkdir"]))

    LOG.info("Staging files upstream - complete.")


def stage_downstream(job):

    """
    A method for staging files for each job to from target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.
    """

    LOG.info("For job '{0}' staging files downstream.".format(job["jobname"]))

    # Download the whole directory with rsync.
    try:

        SHELLWRAPPERS.download(job)

    except EX.RsyncError:

        raise EX.StagingError("Could not download file '{0}' to location '{1}'"
                              .format(job["src"], job["dst"]))

    LOG.info("Staging complete.")


def cleanup(jobs):

    """
    A method for cleaning up the working directory on the HPC host, this method
    will only delete job directories that are valid for the given Longbow
    instance, thus avoid data loss.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOG.info("Cleaning up the work directories.")

    for item in jobs:

        job = jobs[item]
        destdir = job["destdir"]
        remotedir = job["remoteworkdir"]

        try:

            SHELLWRAPPERS.remotelist(job)

            if destdir != remotedir:

                LOG.info("Deleting directory for job '{0}' - '{1}'"
                         .format(item, destdir))

                SHELLWRAPPERS.remotedelete(job)

            else:

                raise EX.RemoteworkdirError(
                    "Subdirectory of remoteworkdir not yet created")

        except EX.RemoteworkdirError:

            LOG.debug("For job '{0}', cleanup not required because the "
                      "'{0}xxxxx' subdirectory of '{1}' in which the job "
                      "would have run has not yet been created on the remote "
                      "resource.".format(item, remotedir))

        except EX.RemotelistError:

            # Directory doesn't exist.
            LOG.debug("Directory on path '{0}' does not exist - skipping."
                      .format(destdir))

        except KeyError:

            LOG.debug("For job '{0}', cleanup not required - skipping."
                      .format(item))

        except EX.RemotedeleteError:

            LOG.debug("For job '{0}', cannot delete directory '{1}' - "
                      "skipping.".format(item, destdir))

        except NameError:

            pass

    LOG.info("Cleaning up complete.")
