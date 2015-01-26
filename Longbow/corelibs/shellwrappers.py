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

"""A module containing methods for interacting with the shell, it includes
methods for file manipulation and directory functions. Where possible paths
are checked to make sure they are absolute paths."""

import os
import shutil
import subprocess
import logging
import time

LOGGER = logging.getLogger("Longbow")


def testconnections(hosts, jobs):

    """A method for checking that the connection to a given machine is
    accessible, problems raised here could be due to system maintenance/
    downtime or a mistake in your host configuration."""

    LOGGER.info("Testing connections to all resources that are referenced " +
                "in the job configurations.")

    # Test all of the computers listed in jobs in the job configuration
    # file, there is no need to check all the ones listed in host
    # configuration each time if they are not used.
    for param in jobs:

        resource = jobs[param]["resource"]
        host = hosts[resource]

        LOGGER.debug("  Testing connection to %s", resource)

        try:
            sendtossh(host, ["ls &> /dev/null"])
        except:
            raise RuntimeError("Cannot reach the following resource: %s " %
                               resource + "make sure the configuration " +
                               "of this resource is correct in your " +
                               "host configuration file and there is no " +
                               "scheduled maintainence.")

        LOGGER.info("  Test connection to %s - passed", resource)


def sendtoshell(cmd):

    """The method for sending shell commands to subprocess for execution
    within a system shell."""

    LOGGER.debug("  Sending the following to subprocess: %s", cmd)

    i = 0

    # This loop is essentially so we can do 3 retries on commands that fail,
    # this is to catch when things go wrong over SSH like dropped connections,
    # issues with latency etc.
    while i is not 3:

        handle = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        stdout, stderr = handle.communicate()

        # Grab the return code.
        errorstate = handle.returncode

        # If no error exit loop, if errorcode is not 0 raise exception unless
        # code is 255
        if errorstate is 0:
            break
        elif errorstate is 255:
            i = i + 1
        else:
            raise RuntimeError("Command returned error.")

        # If number of retries or the standard output and error
        # is coming back blank then give up.
        if i is 3:
            raise RuntimeError("Subprocess error: something went wrong.")

        LOGGER.debug("  Retry last command after a 10 second wait.")

        # Wait 10 seconds to see if problem goes away before trying again.
        time.sleep(10)

    return stdout, stderr, errorstate


def sendtossh(host, args):

    """A method for constructing ssh commands."""

    # basic ssh command.
    cmd = ["ssh", "-p " + host["port"],
           host["user"] + "@" + host["host"]]

    # add the commands to be sent to ssh.
    cmd.extend(args)

    # Send to ssh.
    try:
        shellout = sendtoshell(cmd)
    except Exception as ex:
        raise ex

    return shellout


def sendtoscp(host, src, dst):

    """A method for constructing scp commands."""

    # Basic scp command.
    cmd = ["scp", "-P " + host["port"], "-r", src, dst]

    # Send to scp
    try:
        sendtoshell(cmd)
    except Exception as ex:
        raise ex


def sendtorsync(host, src, dst):

    """A method for constructing rsync commands."""

    # Basic rsync command.
    cmd = ["rsync", "-rP", "-e", "ssh -p %s" %
           host["port"], src, dst]

    # Send to rsync.
    try:
        sendtoshell(cmd)
    except Exception as ex:
        raise ex


def localcopy(src, dst):

    """A method for copying files locally. This method is able to deal with
    situations where files/directories need overwriting (beware this
    happens without asking the user). All paths should be absolute."""

    LOGGER.debug("  Copying %s " % src + "to %s" % dst)

    # Are paths absolute.
    if os.path.isabs(src) is False:
        raise RuntimeError("The source path: %s is not absolute" % src)

    if os.path.isabs(dst) is False:
        raise RuntimeError("The destination path: %s is not absolute" %
                           dst)

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
        except:
            raise RuntimeError("Could not copy the file: %s" % src)
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
        except:
            raise RuntimeError("There was a problem copying the " +
                               "directory %s" % src)
    else:
        raise RuntimeError("Could not determine if the source file or " +
                           "directory: %s exists" % src)


def localdelete(src):

    """A method for deleting local files, is able to deal with files and
    directory trees, this method takes absolute paths only."""

    LOGGER.debug("  Deleting: %s", src)

    # Check if path is absolute.
    if os.path.isabs(src) is False:
        raise RuntimeError("The path: %s is not an absolute path" % src)

    # Check if we are deleting a file or directory and call the appropriate
    # method.
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            raise RuntimeError("Something went wrong when trying to " +
                               "delete the file %s " % src)
    elif os.path.isdir(src):
        try:
            shutil.rmtree(src)
        except:
            raise RuntimeError("Something went wrong when trying to " +
                               "delete the directory %s " % src)
    else:
        raise RuntimeError("Could not determine whether the source is a " +
                           "file or directory.")


def locallist(src):

    """A method for listing a local directory contents, this method takes
    absolute paths only."""

    LOGGER.debug("  Listing the contents of: %s", src)

    # Check if path is absolute.
    if os.path.isabs(src) is False:
        raise RuntimeError("The path: %s is not an absolute path", src)

    # Check if the path exists, and list if it does.
    if os.path.exists(src):
        filelist = os.listdir(src)
    else:
        raise RuntimeError("The dir on path: %s does not exist", src)

    return filelist


def remotecopy(host, src, dst):

    """A method for copying files/directories on the remote machine."""

    LOGGER.debug("Copying %s " % src + "to %s" % dst)

    # Just use cp for this with recursive set in case of directory.
    cmd = ["cp", "-r", src, dst]

    # Send to subprocess.
    try:
        sendtossh(host, cmd)
    except:
        raise RuntimeError("Could not copy the file/dir: %s " % src +
                           "to: %s" % dst)


def remotedelete(host, src):

    """A method for deleting files/directories on the remote machine."""

    LOGGER.debug("  Deleting: %s", src)

    # Just use rm for this with recursive set in case of directory.
    cmd = ["rm", "-r", src]

    # Send to subprocess.
    try:
        sendtossh(host, cmd)
    except:
        raise RuntimeError("Could not delete the file/directory: %s", src)


def remotelist(host, src):

    """A method to list a directory on the remote resource."""

    LOGGER.debug("  Listing the contents of: %s", src)

    # Are paths absolute.
    if os.path.isabs(src) is False:
        raise RuntimeError("The source path: %s is not absolute" % src)

    # Shell command ls for listing in a shell.
    cmd = ["ls" + " " + src]

    # Send command to subprocess.
    try:
        shellout = sendtossh(host, cmd)
    except:
        raise RuntimeError("Could not list the directory: %s" % src)

    # Split the stdout into a list.
    filelist = shellout[0].split()

    return filelist


def upload(protocol, host, src, dst):

    """A method for uploading files to remote hosts."""

    dst = (host["user"] + "@" +
           host["host"] + ":" + dst)

    LOGGER.debug("  Copying %s " % src + "to %s" % dst)

    # Are paths absolute.
    if os.path.isabs(src) is False:
        raise RuntimeError("The source path: %s is not absolute", src)

    # Send command to subprocess.
    try:
        if protocol is "rsync":
            sendtorsync(host, src, dst)
        elif protocol is "scp":
            sendtoscp(host, src, dst)
        else:
            raise RuntimeError("Cannot handle the protocol: " + protocol)
    except:
        raise RuntimeError("Could not upload: %s " % src +
                           "to %s" % dst)


def download(protocol, host, src, dst):

    """A method for downloading files from remote hosts."""

    src = (host["user"] + "@" +
           host["host"] + ":" + src)

    LOGGER.debug("  Copying %s " % src + "to %s" % dst)

    # Are paths absolute.
    if os.path.isabs(dst) is False:
        raise RuntimeError("The destination path: %s is not absolute" %
                           dst)

    # Send command to subprocess.
    try:
        if protocol is "rsync":
            sendtorsync(host, src, dst)
        elif protocol is "scp":
            sendtoscp(host, src, dst)
        else:
            raise RuntimeError("Cannot handle the protocol: " + protocol)
    except:
        raise RuntimeError("Could not download: %s " % src +
                           "to %s" % dst)
