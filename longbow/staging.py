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

"""A module containing methods for staging files to and from remote machines.

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
import os

import longbow.exceptions as exceptions
import longbow.shellwrappers as shellwrappers

LOG = logging.getLogger("longbow.staging")


def stage_upstream(jobs):
    """Transfer files for all jobs, to a remote HPC machine.

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

    for item in [a for a in jobs if "lbowconf" not in a]:

        job = jobs[item]
        destdir = job["destdir"]

        LOG.info("Transfering files for job '%s' to host '%s'",
                 item, job["resource"])

        try:

            shellwrappers.sendtossh(job, ["mkdir -p " + destdir + "\n"])

            LOG.info("Creation of directory '%s' - successful.", destdir)

        except exceptions.SSHError:

            LOG.error(
                "Creation of directory '%s' - failed. Make sure that you "
                "have write permissions at the top level of the path given.",
                destdir)

            raise

        # Transfer files upstream.
        try:

            shellwrappers.upload(job)

        except exceptions.RsyncError:

            raise exceptions.StagingError(
                "Could not stage '{0}' upstream, make sure that you have "
                "supplied the correct remote working directory and that you "
                "have chosen a path that you can write to."
                .format(job["localworkdir"]))

    LOG.info("Staging files upstream - complete.")


def stage_downstream(job):
    """Transfer all files for a job, back from the HPC machine.

    A method for staging files for each job to from target HPC host. The
    underlying utility behind this transfer is rsync, thus it is possible
    to supply rsync file masks to blacklist unwanted large files. By default
    rsync is configured to transfer blockwise and only transfer the
    newest/changed blocks, this saves a lot of time during persistant staging.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    """
    LOG.info("For job '%s' staging files downstream.", job["jobname"])

    # Download the whole directory with rsync.
    try:

        shellwrappers.download(job)

    except exceptions.RsyncError:

        raise exceptions.StagingError(
            "Could not download a file from '{0}' to '{1}'".format(
                job["destdir"], job["localworkdir"]))

    LOG.info("Staging complete.")


def cleanup(jobs):
    """Clean up the working directory on the HPC machine.

    This method will only delete job directories that are valid for jobs within
    a given Longbow instance, thus avoiding catastrophic data loss. It will
    also fail gracefully with debug level log messages should the cleanup
    function be triggered at a stage prior to remote job directory creation.
    This method also contains the code for cleaning up the recovery file used
    in the session.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.

    """
    LOG.info("Cleaning up the work directories.")

    for item in [a for a in jobs if "lbowconf" not in a]:

        job = jobs[item]
        destdir = job["destdir"]
        remotedir = job["remoteworkdir"]

        try:

            shellwrappers.remotelist(job)

            if destdir != remotedir:

                LOG.info("Deleting directory for job '%s' - '%s'",
                         item, destdir)

                shellwrappers.remotedelete(job)

            else:

                raise exceptions.RemoteworkdirError(
                    "Subdirectory of remoteworkdir not yet created")

        except exceptions.RemoteworkdirError:

            LOG.debug("For job '%s', cleanup not required because the "
                      "'%sxxxxx' subdirectory of '%s' in which the job "
                      "would have run has not yet been created on the remote "
                      "resource.", item, item, remotedir)

        except exceptions.RemotelistError:

            # Directory doesn't exist.
            LOG.debug("Directory on path '%s' does not exist - skipping.",
                      destdir)

        except KeyError:

            LOG.debug("For job '%s', cleanup not required - skipping.", item)

        except exceptions.RemotedeleteError:

            LOG.debug("For job '%s', cannot delete directory '%s' - skipping.",
                      item, destdir)

        except NameError:

            pass

    recfile = jobs["lbowconf"]["recoveryfile"]
    fpath = os.path.expanduser('~/.longbow')

    if (recfile != "" and os.path.isfile(os.path.join(fpath, recfile))):

        LOG.info("Removing the recovery file.")

        os.remove(os.path.join(fpath, recfile))

    LOG.info("Cleaning up complete.")
