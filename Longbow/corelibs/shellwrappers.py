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
This module contains methods for interacting with the Unix shell, it includes
methods for file manipulation and directory functions. Where possible paths
are checked to make sure they are absolute paths.

The following methods can be found:

testconnections()
    This method will test that connections to hosts specified in jobs can be
    established. Problems encountered at this stage could be due to either
    badly configured hosts, networking problems, or even system maintenance/
    downtime on the HPC host.

sendtoshell()
    This method is responsible for handing off commands to the Unix shell, it
    makes use of the subprocess library from the Python standard library.

sendtossh()
    This method constructs a string containing commands to be executed via SSH.
    This string is then handed off to the sendtoshell() method for execution.

sendtorsync()
    This method constructs a string that forms an rsync command, this string is
    then handed off to the sendtoshell() method for execution.

localcopy()
    This method is for copying a file/directory between two local paths, this
    method relies on the Python standard library to perform operations.

localdelete()
    This method is for deleting a file/directory from the local machine, this
    method relies on the Python standard library to perform operations.

locallist()
    This method is for constructing a list of items present within a given
    directory. This method relies on the Python standard library to perform
    operations.

remotecopy()
    This method is for copying a file/directory between two paths on a remote
    host, this is done via passing a copy command to the sendtossh() method.

remotedelete()
    This method is for deleting a file/directory from a path on a remote host,
    this is done via passing a delete command to the sendtossh() method.

remotelist()
    This method is for listing the contents of a directory on a remote host,
    this is done via passing a list command to the sendtoshell() method.

upload()
    This method is for uploading files to a remote host, this method is
    responsible for specifying the direction that the transfer takes place.

download()
    This method is for downloading files from a remote host, this method is
    responsible for specifying the direction that the transfer takes place.
"""

import os
import shutil
import subprocess
import logging
import time

try:

    EX = __import__("corelibs.exceptions", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])

LOGGER = logging.getLogger("Longbow")


def testconnections(hosts, jobs):

    """
    This method will test that connections to hosts specified in jobs can be
    established. Problems encountered at this stage could be due to either
    badly configured hosts, networking problems, or even system maintenance/
    downtime on the HPC host.

    Required arguments are:

    hosts (dictionary) - The Longbow hosts data structure, see configuration.py
                         for more information about the format of this
                         structure.

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOGGER.info(
        "Testing connections to all resources that are referenced in the job "
        "configurations.")

    checked = []

    # Test all of the computers listed in jobs in the job configuration
    # file, there is no need to check all the ones listed in host
    # configuration each time if they are not used.
    for param in jobs:

        resource = jobs[param]["resource"]
        host = hosts[resource]

        # Have we checked this connection already?
        if resource not in checked:

            # Make sure we don't check this again.
            checked.extend([resource])

            LOGGER.debug("Testing connection to '{0}'".format(resource))

            try:

                sendtossh(host, ["ls"])

            except EX.SSHError:

                raise

            LOGGER.info("Test connection to '{0}' - passed".format(resource))


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

    LOGGER.debug("Sending the following to subprocess '{0}'".format(cmd))

    handle = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = handle.communicate()

    # Format the string to utf-8 for python 3, python 2 should be untouched.
    stdout = stdout.decode("utf-8")

    # Grab the return code.
    errorstate = handle.returncode

    return stdout, stderr, errorstate


def sendtossh(host, args):

    """
    This method constructs a string containing commands to be executed via SSH.
    This string is then handed off to the sendtoshell() method for execution.

    Required arguments are:

    host (dictionary) - A dictionary containing a single host, this is not to
                        be confused with hosts. The best way to get a single
                        dictionary for a host from hosts is to do:
                        host = hosts[hostname]

    args (list) - A list containing commands to be sent to SSH, multiple
                  commands should each be an entry in the list.

    Return parameters are:

    shellout (tuple of strings) - Contains the three strings returned from the
                                  sendtoshell() method. These are standard
                                  output, standard error and the exit code.
    """

    # basic ssh command.
    cmd = ["ssh", "-p " + host["port"], host["user"] + "@" + host["host"]]

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

            raise EX.SSHError(
                "SSH failed, make sure a normal terminal can connect to SSH "
                "to be sure there are no connection issues.", shellout)

        # If number of retries hits 3 then give up.
        if i is 3:

            raise EX.SSHError(
                "SSH failed, make sure a normal terminal can connect to SSH "
                "to be sure there are no connection issues.", shellout)

        LOGGER.debug("Retry SSH after 10 second wait.")

        # Wait 10 seconds to see if problem goes away before trying again.
        time.sleep(10)

    return shellout


def sendtorsync(src, dst, port, includemask, excludemask):

    """
    This method constructs a string that forms an rsync command, this string is
    then handed off to the sendtoshell() method for execution.

    Required arguments are:

    src (string) - A string containing the source directory for transfer, if
                   this is a download then this should include the host
                   information. See the download and upload methods for how
                   this should be done (or just make use of those two methods).

    dst (string) - A string containing the destination directory for transfer,
                   if this is an upload then this should include the host
                   information. See the download and upload methods for how
                   this should be done (or just make use of those two methods).

    port (port) - A string containing the port number as to which should be
                  used for transfer.

    includemask (string) - This is a string that should contain a comma
                           separated list of files for transfer.

    excludemask (string) - This is a string that should specify which files
                           should be excluded from rsync transfer, this is
                           useful for not transfering large unwanted files.
    """

    include = []
    exclude = []

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

            raise EX.RsyncError(
                "rsync failed, make sure a normal terminal can connect to "
                "rsync to be sure there are no connection issues.", shellout)

        LOGGER.debug("Retry rsync after 10 second wait.")

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

    LOGGER.debug("Copying '{0}' to '{1}'".format(src, dst))

    # Expand tildas (if present) otherwise these will not change anything.
    src = os.path.expanduser(src)
    dst = os.path.expanduser(dst)

    # Are paths absolute.
    if os.path.isabs(src) is False:

        raise EX.AbsolutepathError("The source path is not absolute", src)

    if os.path.isabs(dst) is False:

        raise EX.AbsolutepathError("The destination path is not absolute", dst)

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

            raise EX.LocalcopyError("Could not copy the file", src)

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

            raise EX.LocalcopyError("Could not copy the directory '{0}'"
                                    .format(src))


def localdelete(src):

    """
    This method is for deleting a file/directory from the local machine, this
    method relies on the Python standard library to perform operations.

    Required arguments are:

    src (string) - A string containing the absolute path of the file/directory
                   to be deleted.
    """

    LOGGER.debug("Deleting '{0}'".format(src))

    # Expand tildas (if present) otherwise these will not change anything.
    src = os.path.expanduser(src)

    # Check if path is absolute.
    if os.path.isabs(src) is False:

        raise EX.AbsolutepathError("The source path is not absolute", src)

    # Check if we are deleting a file or directory and call the appropriate
    # method.
    if os.path.isfile(src):

        try:

            os.remove(src)

        except IOError:

            raise EX.LocaldeleteError("Could not delete file", src)

    elif os.path.isdir(src):

        try:

            shutil.rmtree(src)

        except IOError:

            raise EX.LocaldeleteError("Could not delete file", src)


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

    LOGGER.debug("Listing the contents of '{0}'".format(src))

    # Expand tildas (if present) otherwise these will not change anything.
    src = os.path.expanduser(src)

    # Check if path is absolute.
    if os.path.isabs(src) is False:

        raise EX.AbsolutepathError("The source path is not absolute", src)

    # Check if the path exists, and list if it does.
    if os.path.exists(src):

        filelist = os.listdir(src)

    else:

        raise EX.LocallistError("Local directory does not exist.", src)

    return filelist


def remotecopy(host, src, dst):

    """
    This method is for copying a file/directory between two paths on a remote
    host, this is done via passing a copy command to the sendtossh() method.

    Required arguments are:

    host (dictionary) - A dictionary containing a single host, this is not to
                        be confused with hosts. The best way to get a single
                        dictionary for a host from hosts is to do:
                        host = hosts[hostname]

    src (string) - A string containing the absolute path of the file/directory
                   to be copied (on the host).

    dst (string) - A string containing the destination absolute path to be
                   copied to (on the host).
    """

    LOGGER.debug("Copying '{0}' to '{1}'".format(src, dst))

    # Are paths absolute. Do we start with tildas, if so since we are going
    # through the shell allow it to expand the tilda on the remote host for us.
    if os.path.isabs(src) is False and src[0] != "~":

        raise EX.AbsolutepathError("The source path is not absolute", src)

    if os.path.isabs(dst) is False and dst[0] != "~":

        raise EX.AbsolutepathError("The destination path is not absolute", dst)

    # Just use cp for this with recursive set in case of directory.
    cmd = ["cp -r", src, dst]

    # Send to subprocess.
    try:

        sendtossh(host, cmd)

    except EX.SSHError:

        raise EX.RemotecopyError("Could not copy file to host ", src, dst)


def remotedelete(host, src):

    """
    This method is for deleting a file/directory from a path on a remote host,
    this is done via passing a delete command to the sendtossh() method.

    Required arguments are:

    host (dictionary) - A dictionary containing a single host, this is not to
                        be confused with hosts. The best way to get a single
                        dictionary for a host from hosts is to do:
                        host = hosts[hostname]

    src (string) - A string containing the absolute path of the file/directory
                   to be deleted (on the host).
    """

    LOGGER.debug("Deleting '{0}'".format(src))

    # Are paths absolute.
    if os.path.isabs(src) is False and src[0] != "~":

        raise EX.AbsolutepathError("The source path is not absolute", src)

    # Just use rm for this with recursive set in case of directory.
    cmd = ["rm -r", src]

    # Send to subprocess.
    try:

        sendtossh(host, cmd)

    except EX.SSHError:

        raise EX.RemotedeleteError(
            "Could not delete the file/directory on remote host", src)


def remotelist(host, src):

    """
    This method is for listing the contents of a directory on a remote host,
    this is done via passing a list command to the sendtoshell() method.

    Required arguments are:

    host (dictionary) - A dictionary containing a single host, this is not to
                        be confused with hosts. The best way to get a single
                        dictionary for a host from hosts is to do:
                        host = hosts[hostname]

    src (string) - A string containing the absolute path of the file/directory
                   to be listed (on the host).

    Returned parameters are:

    filelist (list) - A list of files within the specified directory.
    """

    LOGGER.debug("Listing the contents of '{0}'".format(src))

    # Are paths absolute.
    if os.path.isabs(src) is False and src[0] != "~":

        raise EX.AbsolutepathError("The source path is not absolute", src)

    # Shell command ls for listing in a shell.
    cmd = ["ls" + " " + src]

    # Send command to subprocess.
    try:

        shellout = sendtossh(host, cmd)

    except EX.SSHError:

        raise EX.RemotelistError("Could not list the directory", src)

    # Split the stdout into a list.
    filelist = shellout[0].split()

    return filelist


def upload(host, src, dst, includemask, excludemask):

    """
    This method is for uploading files to a remote host, this method is
    responsible for specifying the direction that the transfer takes place.

    Required arguments are:

    host (dictionary) - A dictionary containing a single host, this is not to
                        be confused with hosts. The best way to get a single
                        dictionary for a host from hosts is to do:
                        host = hosts[hostname]

    src (string) - A string containing the source directory for transfer.

    dst (string) - A string containing the destination directory for transfer.

    includemask (string) - This is a string that should contain a comma
                           separated list of files for transfer.

    excludemask (string) - This is a string that should specify which files
                           should be excluded from rsync transfer, this is
                           useful for not transfering large unwanted files.
    """

    # Are paths absolute.
    if os.path.isabs(src) is False and src[0] != "~":

        raise EX.AbsolutepathError("The source path is not absolute", src)

    if os.path.isabs(dst) is False and dst[0] != "~":

        raise EX.AbsolutepathError("The destination path is not absolute", dst)

    dst = (host["user"] + "@" + host["host"] + ":" + dst)

    LOGGER.debug("Copying '{0}' to '{1}'".format(src, dst))

    # Send command to subprocess.
    try:

        sendtorsync(src, dst, host["port"], includemask, excludemask)

    except EX.RsyncError:

        raise


def download(host, src, dst, includemask, excludemask):

    """
    This method is for downloading files from a remote host, this method is
    responsible for specifying the direction that the transfer takes place.

    Required arguments are:

    host (dictionary) - A dictionary containing a single host, this is not to
                        be confused with hosts. The best way to get a single
                        dictionary for a host from hosts is to do:
                        host = hosts[hostname]

    src (string) - A string containing the source directory for transfer.

    dst (string) - A string containing the destination directory for transfer.

    includemask (string) - This is a string that should contain a comma
                           separated list of files for transfer.

    excludemask (string) - This is a string that should specify which files
                           should be excluded from rsync transfer, this is
                           useful for not transfering large unwanted files.
    """

    # Are paths absolute.
    if os.path.isabs(src) is False and src[0] != "~":

        raise EX.AbsolutepathError("The source path is not absolute", src)

    if os.path.isabs(dst) is False and dst[0] != "~":

        raise EX.AbsolutepathError("The destination path is not absolute", dst)

    src = (host["user"] + "@" + host["host"] + ":" + src)

    LOGGER.debug("Copying '{0}' to '{1}'".format(src, dst))

    # Send command to subprocess.
    try:

        sendtorsync(src, dst, host["port"], includemask, excludemask)

    except EX.RsyncError:

        raise
