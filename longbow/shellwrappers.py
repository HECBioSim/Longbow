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

"""A module containing methods for interacting with the Unix shell.

This module contains methods for interacting with the Unix shell, it includes
methods for file manipulation and directory functions. Where possible paths
are checked to make sure they are absolute paths.

The following methods can be found:

testconnections(jobs)
    This method will test that connections to hosts specified in jobs can be
    established. Problems encountered at this stage could be due to either
    badly configured hosts, networking problems, or even system maintenance/
    downtime on the HPC host.

sendtoshell(cmd)
    This method is responsible for handing off commands to the Unix shell, it
    makes use of the subprocess library from the Python standard library.

sendtossh(job, args)
    This method constructs a string containing commands to be executed via SSH.
    This string is then handed off to the sendtoshell() method for execution.

sendtorsync(job, src, dst, includemask, excludemask)
    This method constructs a string that forms an rsync command, this string is
    then handed off to the sendtoshell() method for execution.

localcopy(src, dst)
    This method is for copying a file/directory between two local paths, this
    method relies on the Python standard library to perform operations.

localdelete(src)
    This method is for deleting a file/directory from the local machine, this
    method relies on the Python standard library to perform operations.

locallist(src)
    This method is for constructing a list of items present within a given
    directory. This method relies on the Python standard library to perform
    operations.

remotecopy(job, src, dst)
    This method is for copying a file/directory between two paths on a remote
    host, this is done via passing a copy command to the sendtossh() method.

remotedelete(job)
    This method is for deleting a file/directory from a path on a remote host,
    this is done via passing a delete command to the sendtossh() method.

remotelist(job)
    This method is for listing the contents of a directory on a remote host,
    this is done via passing a list command to the sendtoshell() method.

upload(job)
    This method is for uploading files to a remote host, this method is
    responsible for specifying the direction that the transfer takes place.

download(job)
    This method is for downloading files from a remote host, this method is
    responsible for specifying the direction that the transfer takes place.
"""

import os
import shutil
import subprocess
import logging
import time

import longbow.exceptions as exceptions

LOG = logging.getLogger("longbow.shellwrappers")


def checkconnections(jobs):
    """Test that connections to HPC machines can be established.

    This method will test that connections to hosts specified in jobs can be
    established. It will at the same time check if the basic Linux environment
    looks like it is configured for a non-login shell, if not then the
    environment fix mode is turned on by setting

    jobs["somejob"]["env-fix] = true

    this will make sure that /etc/profile is sourced on certain calls to the
    remote machine. Problems encountered at this stage could be due to either
    badly configured hosts, networking problems, or even system
    maintenance/downtime on the HPC host.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """
    LOG.info("Performing basic connection and environment tests for all "
             "machines referenced in jobs.")
    checked = []

    # Test all of the computers listed in jobs in the job configuration
    # file, there is no need to check all the ones listed in host
    # configuration each time if they are not used.
    for item in [a for a in jobs if "lbowconf" not in a]:

        # Have we checked this connection already?
        if jobs[item]["resource"] not in checked:

            # Make sure we don't check this again.
            checked.extend([jobs[item]["resource"]])

            LOG.debug("Testing connection to '%s'", jobs[item]["resource"])

            # Test that the connection works.
            sendtossh(jobs[item], ["ls"])

            LOG.info("Test connection to '%s' - passed",
                     jobs[item]["resource"])

            # Test that basic enviroment looks ok.
            try:

                sendtossh(jobs[item], ["module avail"])

            except exceptions.SSHError as err:

                # If the module command is not found, then it is highly likely
                # that the non-login shells do not source the /etc/profile in
                # which the system loads a lot of the environment.
                if ("bash: module: command not found" in err.stdout or
                        "bash: module: command not found" in err.stderr):

                    # Go over all jobs referencing this machine and switch on
                    # the environment fix.
                    for job in [a for a in jobs if "lbowconf" not in a]:

                        if jobs[job]["resource"] == jobs[item]["resource"]:

                            jobs[job]["env-fix"] = "true"


def sendtoshell(cmd):
    """Send assembled commands to the Unix shell.

    This method is responsible for handing off commands to the Unix shell, it
    makes use of the subprocess library from the Python standard library.

    Required arguments are:

    cmd (string) - A fully qualified Unix command.

    Return parameters are:

    stdout (string) - Contains the output from the standard output of the Unix
                      shell.

    stderr (string) - Contains the output from the standard error of the Unix
                      shell.

    errorstate (string) - Contains the exit code that the Unix shell exits
                          with.

    """
    LOG.debug("Sending the following to subprocess '%s'", cmd)

    handle = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = handle.communicate()

    # Format stdout to utf-8 for python 3, python 2 should be untouched.
    if not isinstance(stdout, str):

        stdout = stdout.decode("utf-8")

    # Format stderr to utf-8 for python 3, python 2 should be untouched.
    if not isinstance(stderr, str):

        stderr = stderr.decode("utf-8")

    # Grab the return code.
    errorstate = handle.returncode

    return stdout, stderr, errorstate


def sendtossh(job, args):
    """Construct SSH commands and hand them off to the shell.

    This method constructs a string containing commands to be executed via SSH.
    This string is then handed off to the sendtoshell() method for execution.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    args (list) - A list containing commands to be sent to SSH, multiple
                  commands should each be an entry in the list.

    Return parameters are:

    shellout (tuple of strings) - Contains the three strings returned from the
                                  sendtoshell() method. These are standard
                                  output, standard error and the exit code.

    """
    # basic ssh command.
    cmd = ["ssh", "-p " + job["port"], job["user"] + "@" + job["host"]]

    # Source the /etc/profile on machines where problems have been detected
    # with the environment.
    if job["env-fix"] == "true":

        cmd.append("source /etc/profile;")

    # add the commands to be sent to ssh.
    cmd.extend(args)

    i = 0

    # This loop is essentially so we can do 3 retries on commands that fail,
    # this is to catch when things go wrong over SSH like dropped connections,
    # issues with latency etc.
    while i != 3:

        # Send to ssh.
        shellout = sendtoshell(cmd)

        errorstate = shellout[2]

        # If no error exit loop, if errorcode is not 0 raise exception unless
        # code is 255
        if errorstate == 0:

            break

        elif errorstate == 255:

            i = i + 1

        else:

            raise exceptions.SSHError(
                "SSH failed, make sure a normal terminal can connect to SSH "
                "to be sure there are no connection issues.", shellout)

        # If number of retries hits 3 then give up.
        if i == 3:

            raise exceptions.SSHError(
                "SSH failed, make sure a normal terminal can connect to SSH "
                "to be sure there are no connection issues.", shellout)

        LOG.debug("Retry SSH after 10 second wait.")

        # Wait 10 seconds to see if problem goes away before trying again.
        time.sleep(10)

    return shellout


def sendtorsync(job, src, dst, includemask, excludemask):
    """Construct Rsync commands and hand them off to the shell.

    This method constructs a string that forms an rsync command, this string is
    then handed off to the sendtoshell() method for execution.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    src (string) - A string containing the source directory for transfer, if
                   this is a download then this should include the host
                   information. See the download and upload methods for how
                   this should be done (or just make use of those two methods).

    dst (string) - A string containing the destination directory for transfer,
                   if this is an upload then this should include the host
                   information. See the download and upload methods for how
                   this should be done (or just make use of those two methods).

    includemask (string) - This is a string that should contain a comma
                           separated list of files for transfer.

    excludemask (string) - This is a string that should specify which files
                           should be excluded from rsync transfer, this is
                           useful for not transfering large unwanted files.

    """
    # Initialise variables.
    include = []
    exclude = []
    port = job["port"]

    # Figure out if we are using masks to specify files.
    if excludemask != "" and includemask == "":

        # Exclude masks are a comma separated list.
        for mask in excludemask.split(","):

            mask = mask.replace(" ", "")
            exclude.append("--exclude")
            exclude.append(mask)

        cmd = ["rsync", "-azP"]
        cmd.extend(exclude)
        cmd.extend(["-e", "ssh -p " + port, src, dst])

    elif excludemask != "" and includemask != "":

        # Exclude masks are a comma separated list.
        for mask in excludemask.split(","):

            mask = mask.replace(" ", "")
            exclude.append("--exclude")
            exclude.append(mask)

        # Exclude masks are a comma separated list.
        for mask in includemask.split(","):

            mask = mask.replace(" ", "")
            include.append("--include")
            include.append(mask)

        cmd = ["rsync", "-azP"]
        cmd.extend(include)
        cmd.extend(exclude)
        cmd.extend(["-e", "ssh -p " + port, src, dst])

    else:

        # Just normal rsync
        cmd = ["rsync", "-azP", "-e", "ssh -p " + port, src, dst]

    i = 0

    # This loop is essentially so we can do 3 retries on commands that fail,
    # this is to catch when things go wrong over SSH like dropped connections,
    # issues with latency etc.
    while i != 3:

        # Send to SSH.
        shellout = sendtoshell(cmd)

        errorstate = shellout[2]

        # If no error exit loop, if errorcode is not 0 raise exception unless
        # code is 255
        if errorstate == 0:

            break

        else:

            i = i + 1

        # If number of retries hits 3 then give up.
        if i == 3:

            raise exceptions.RsyncError(
                "rsync failed, make sure a normal terminal can connect to "
                "rsync to be sure there are no connection issues.", shellout)

        LOG.debug("Retry rsync after 10 second wait.")

        # Wait 10 seconds to see if problem goes away before trying again.
        time.sleep(10)


def localcopy(src, dst):
    """Copy files from one local path to another.

    This method is for copying a file/directory between two local paths, this
    method relies on the Python standard library to perform operations. This
    method will test the path and use the correct python methods for
    transferring an object whether it be a file or a directory. Note that this
    function requires that you pass absolute paths as both the source and
    destination paths.

    Required arguments are:

    src (string) - A string containing the absolute path of the file/directory
                   to be copied.

    dst (string) - A string containing the destination absolute path to be
                   copied to.

    """
    LOG.debug("Copying '%s' to '%s'", src, dst)

    # Expand tildas (if present) otherwise these will not change anything.
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)

    # Are paths absolute.
    if os.path.isabs(src) is False:

        raise exceptions.AbsolutepathError(
            "The source path is not absolute", src)

    if os.path.isabs(dst) is False:

        raise exceptions.AbsolutepathError(
            "The destination path is not absolute", dst)

    # Is the source a file or a directory? They are dealt with slightly
    # differently.
    try:

        if os.path.isfile(src):

            # Check if the destination exists.
            if os.path.exists(dst):

                # Copy it.
                shutil.copy(src, dst)

            else:
                os.makedirs(dst)
                shutil.copy(src, dst)

        elif os.path.isdir(src):

            # Check if the destination exists.
            if os.path.exists(dst):

                # Remove the existing and then copy it.
                shutil.rmtree(dst)

                shutil.copytree(src, dst)

            else:

                # Copy it.
                shutil.copytree(src, dst)

        else:

            raise exceptions.LocalcopyError("Could not copy file it appears "
                                            "to not exist.", src)

    except (shutil.Error, IOError):

        raise exceptions.LocalcopyError("Could not copy the directory", src)


def localdelete(src):
    """Delete local file/directory.

    This method is for deleting a file/directory from the local machine, this
    method relies on the Python standard library to perform operations. This
    method will test the path and use the correct variant of the python methods
    for deleting a file or a directory. Note that this function requires that
    you pass absolute paths as the source path.

    Required arguments are:

    src (string) - A string containing the absolute path of the file/directory
                   to be deleted.

    """
    LOG.debug("Deleting '%s'", src)

    # Expand tildas (if present) otherwise these will not change anything.
    src = os.path.expanduser(src)

    # Check if path is absolute.
    if os.path.isabs(src) is False:

        raise exceptions.AbsolutepathError(
            "The source path is not absolute", src)

    # Check if we are deleting a file or directory and call the appropriate
    # method.
    if os.path.isfile(src):

        try:

            os.remove(src)

        except IOError:

            raise exceptions.LocaldeleteError("Could not delete file", src)

    elif os.path.isdir(src):

        try:

            shutil.rmtree(src)

        except IOError:

            raise exceptions.LocaldeleteError("Could not delete file", src)

    else:

        raise exceptions.LocaldeleteError(
            "Could not delete file it appears to not exist.", src)


def locallist(src):
    """List the contents of a local directory.

    This method is for constructing a list of items present within a given
    directory. This method relies on the Python standard library to perform
    operations. Note that this method is not recursive, nor will it give
    information on whether an object is a file or directory, however it is
    trivial to run these tests using standard Python. Note that this function
    requires that you pass absolute paths as the source path.

    Required arguments are:

    src (string) - A string containing the absolute path to a directory to
                   be listed.

    Return parameters are:

    filelist (list) - A list of files within the specified directory.

    """
    LOG.debug("Listing the contents of '%s'", src)

    # Expand tildas (if present) otherwise these will not change anything.
    src = os.path.expanduser(src)

    # Check if path is absolute.
    if os.path.isabs(src) is False:

        raise exceptions.AbsolutepathError(
            "The source path is not absolute", src)

    # Check if the path exists, and list if it does.
    if os.path.exists(src):

        filelist = os.listdir(src)

    else:

        raise exceptions.LocallistError("Local directory does not exist.", src)

    return filelist


def remotecopy(job, src, dst):
    """Copy files between paths on a remote HPC machine.

    This method is for copying a file/directory between two paths on a remote
    host, this is done via passing a copy command to the sendtossh() method.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    src (string) - A string containing the absolute path of the file/directory
                   to be copied (on the host).

    dst (string) - A string containing the destination absolute path to be
                   copied to (on the host).

    """
    LOG.debug("Copying '%s' to '%s'", src, dst)

    # Are paths absolute. Do we start with tildas, if so since we are going
    # through the shell allow it to expand the tilda on the remote host for us.
    if os.path.isabs(src) is False and src[0] != "~":

        raise exceptions.AbsolutepathError(
            "The source path is not absolute", src)

    if os.path.isabs(dst) is False and dst[0] != "~":

        raise exceptions.AbsolutepathError(
            "The destination path is not absolute", dst)

    # Send to subprocess.
    try:

        sendtossh(job, ["cp -r", src, dst])

    except exceptions.SSHError:

        raise exceptions.RemotecopyError(
            "Could not copy file to host ", src, dst)


def remotedelete(job):
    """Delete a file/directory on a remote HPC machine.

    This method is for deleting a file/directory from a path on a remote host,
    this is done via passing a delete command to the sendtossh() method.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    """
    LOG.debug("Deleting '%s'", job["destdir"])

    # Are paths absolute.
    if os.path.isabs(job["destdir"]) is False and job["destdir"][0] != "~":

        raise exceptions.AbsolutepathError(
            "The source path is not absolute ", job["destdir"])

    # Send to subprocess.
    try:

        sendtossh(job, ["rm -r", job["destdir"]])

    except exceptions.SSHError:

        raise exceptions.RemotedeleteError(
            "Could not delete the file/directory on remote host",
            job["destdir"])


def remotelist(job):
    """List the contents of a directory on a remote HPC machine.

    This method is for listing the contents of a directory on a remote host,
    this is done via passing a list command to the sendtoshell() method.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    Returned parameters are:

    filelist (list) - A list of files within the specified directory.

    """
    LOG.debug("Listing the contents of '%s'", job["destdir"])

    # Are paths absolute.
    if os.path.isabs(job["destdir"]) is False and job["destdir"][0] != "~":

        raise exceptions.AbsolutepathError(
            "The source path is not absolute ", job["destdir"])

    # Send command to subprocess.
    try:

        shellout = sendtossh(job, ["ls" + " " + job["destdir"]])

    except exceptions.SSHError:

        raise exceptions.RemotelistError(
            "Could not list the directory ", job["destdir"])

    # Split the stdout into a list.
    filelist = shellout[0].split()

    return filelist


def upload(job):
    """Upload a file/s to a remote machine.

    This method is for uploading files to a remote host, this method is
    responsible for specifying the direction that the transfer takes place.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    """
    # Are paths absolute.
    if os.path.isabs(job["localworkdir"]) is False and \
            job["localworkdir"][0] != "~":

        raise exceptions.AbsolutepathError(
            "The source path is not absolute", job["localworkdir"])

    # We want to transfer whole directory.
    if job["localworkdir"].endswith("/") is not True:

        job["localworkdir"] = job["localworkdir"] + "/"

    if os.path.isabs(job["destdir"]) is False and job["destdir"][0] != "~":

        raise exceptions.AbsolutepathError(
            "The destination path is not absolute", job["destdir"])

    dst = (job["user"] + "@" + job["host"] + ":" + job["destdir"])

    LOG.debug("Copying '%s' to '%s'", job["localworkdir"], dst)

    # Send command to subprocess.
    try:

        sendtorsync(job, job["localworkdir"], dst, job["upload-include"],
                    job["upload-exclude"])

    except exceptions.RsyncError:

        raise


def download(job):
    """Download file/s from a remote machine.

    This method is for downloading files from a remote host, this method is
    responsible for specifying the direction that the transfer takes place.
    This method will make the appropriate call to the rsync method based on
    data for a given job, the rsync method should not be called directly and
    this method should be used instead.

    Required arguments are:

    job (dictionary) - A single job dictionary, this is often simply passed in
                       as a subset of the main jobs dictionary.

    """
    # Are paths absolute.
    if os.path.isabs(job["destdir"]) is False and job["destdir"][0] != "~":

        raise exceptions.AbsolutepathError(
            "The source path is not absolute", job["destdir"])

    # We want to transfer whole directory.
    if job["destdir"].endswith("/") is not True:

        job["destdir"] = job["destdir"] + "/"

    if os.path.isabs(job["localworkdir"]) is False and \
            job["localworkdir"][0] != "~":

        raise exceptions.AbsolutepathError(
            "The destination path is not absolute", job["localworkdir"])

    src = (job["user"] + "@" + job["host"] + ":" + job["destdir"])

    LOG.debug("Copying '%s' to '%s'", src, job["localworkdir"])

    # Send command to subprocess.
    try:

        sendtorsync(job, src, job["localworkdir"], job["download-include"],
                    job["download-exclude"])

    except exceptions.RsyncError:

        raise
