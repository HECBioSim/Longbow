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

try:

    import corelibs.exceptions as exceptions

except ImportError:

    import Longbow.corelibs.exceptions as exceptions

LOG = logging.getLogger("Longbow.corelibs.shellwrappers")


def testconnections(jobs):

    """
    This method will test that connections to hosts specified in jobs can be
    established. Problems encountered at this stage could be due to either
    badly configured hosts, networking problems, or even system maintenance/
    downtime on the HPC host.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOG.info("Testing connections to all resources that are referenced in the "
             "job configurations.")

    checked = []

    # Test all of the computers listed in jobs in the job configuration
    # file, there is no need to check all the ones listed in host
    # configuration each time if they are not used.
    for item in jobs:

        job = jobs[item]
        resource = job["resource"]

        # Have we checked this connection already?
        if resource not in checked:

            # Make sure we don't check this again.
            checked.extend([resource])

            LOG.debug("Testing connection to '%s'", resource)

            try:

                sendtossh(job, ["ls"])

            except exceptions.SSHError:

                raise

            LOG.info("Test connection to '%s' - passed", resource)


def sendtoshell(cmd):

    """
    This method is responsible for handing off commands to the Unix shell, it
    makes use of the subprocess library from the Python standard library.

    REquired arguments are:

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

    # Format the string to utf-8 for python 3, python 2 should be untouched.
    if not isinstance(stdout, str):

        stdout = stdout.decode("utf-8")

    # Grab the return code.
    errorstate = handle.returncode

    return stdout, stderr, errorstate


def sendtossh(job, args):

    """
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

    # add the commands to be sent to ssh.
    cmd.extend(args)

    i = 0

    # This loop is essentially so we can do 3 retries on commands that fail,
    # this is to catch when things go wrong over SSH like dropped connections,
    # issues with latency etc.
    while i is not 3:

        # Send to ssh.
        shellout = sendtoshell(cmd)

        errorstate = shellout[2]

        # If no error exit loop, if errorcode is not 0 raise exception unless
        # code is 255
        if errorstate is 0:

            break

        elif errorstate is 255:

            i = i + 1

        else:

            raise exceptions.SSHError(
                "SSH failed, make sure a normal terminal can connect to SSH "
                "to be sure there are no connection issues.", shellout)

        # If number of retries hits 3 then give up.
        if i is 3:

            raise exceptions.SSHError(
                "SSH failed, make sure a normal terminal can connect to SSH "
                "to be sure there are no connection issues.", shellout)

        LOG.debug("Retry SSH after 10 second wait.")

        # Wait 10 seconds to see if problem goes away before trying again.
        time.sleep(10)

    return shellout


def sendtorsync(job, src, dst, includemask, excludemask):

    """
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

    include = []
    exclude = []
    port = job["port"]

    # Figure out if we are using masks to specify files.
    if excludemask is not "" and includemask is "":

        # Exclude masks are a comma separated list.
        for mask in excludemask.split(","):

            mask = mask.replace(" ", "")
            exclude.append("--exclude")
            exclude.append(mask)

        cmd = ["rsync", "-azP"]
        cmd.extend(exclude)
        cmd.extend(["-e", "ssh -p " + port, src, dst])

    elif excludemask is not "" and includemask is not "":

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
    while i is not 3:

        # Send to SSH.
        shellout = sendtoshell(cmd)

        errorstate = shellout[2]

        # If no error exit loop, if errorcode is not 0 raise exception unless
        # code is 255
        if errorstate is 0:

            break

        else:

            i = i + 1

        # If number of retries hits 3 then give up.
        if i is 3:

            raise exceptions.RsyncError(
                "rsync failed, make sure a normal terminal can connect to "
                "rsync to be sure there are no connection issues.", shellout)

        LOG.debug("Retry rsync after 10 second wait.")

        # Wait 10 seconds to see if problem goes away before trying again.
        time.sleep(10)


def localcopy(src, dst):

    """
    This method is for copying a file/directory between two local paths, this
    method relies on the Python standard library to perform operations.

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
    if os.path.isfile(src):

        try:

            # Check if the destination exists.
            if os.path.exists(dst):

                # Copy it.
                shutil.copy(src, dst)

            else:
                os.makedirs(dst)
                shutil.copy(src, dst)

        except (shutil.Error, IOError):

            raise exceptions.LocalcopyError("Could not copy the file", src)

    elif os.path.isdir(src):

        try:

            # Check if the destination exists.
            if os.path.exists(dst):

                # Remove the existing and then copy it.
                shutil.rmtree(dst)

                shutil.copytree(src, dst)

            else:

                # Copy it.
                shutil.copytree(src, dst)

        except (shutil.Error, IOError):

            raise exceptions.LocalcopyError(
                "Could not copy the directory '{0}'".format(src))


def localdelete(src):

    """
    This method is for deleting a file/directory from the local machine, this
    method relies on the Python standard library to perform operations.

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


def locallist(src):

    """
    This method is for constructing a list of items present within a given
    directory. This method relies on the Python standard library to perform
    operations.

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

    """
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

    """
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

    """
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

    """
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

    """
    This method is for downloading files from a remote host, this method is
    responsible for specifying the direction that the transfer takes place.

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
