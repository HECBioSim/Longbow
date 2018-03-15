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

"""This is the CHARMM plugin module.

This plugin is relatively simple in the fact that adding new executables is as
simple as modifying the EXECDATA structure below. See the documentation at
http://www.hecbiosim.ac.uk/longbow-devdocs for more information.
"""

import os
import re

import longbow.exceptions as exceptions


EXECDATA = {
    "charmm": {
        "subexecutables": [],
        "requiredfiles": ["<"],
    },
    "charmm_mpi": {
        "subexecutables": [],
        "requiredfiles": ["<"],
    },
    "charmm_cuda": {
        "subexecutables": [],
        "requiredfiles": ["<"],
    }
}


def file_parser(filename, path, files, substitutions=None):
    """Find dependancy files and add them to the upload list.

    Recursive function that will assimilate from charmm input files, a list of
    dependancy files to be staged to the remote host. The filename will be
    added to the list and any files mentioned in this included file will also
    be added and searched. Substitutions is a dictionary of "@" style
    variables.

    """
    # Initialise variables.
    addfile = _filechecks(path, filename)

    # Now look for references to other files in the input file if not done so
    # already.
    if addfile and (addfile not in files or not files):

        # Then we don't want to check this again.
        files.append(addfile)

        # Create a dictionary for any variable substitutions.
        variables = {} if not substitutions else substitutions

        # Open the input file.
        fil = _fileopen(path, addfile)

        # Search every line for possible input files.
        for line in fil:

            # Remove comments.
            if '!' in line:

                words = line[:line.index('!')].split()

            else:

                words = line[:len(line)].split()

            if len(words) > 0:

                _internalsubstitutions(variables, words)

                # Try to detect other input files.
                if (('read' in [x.lower() for x in words]) and
                        ('name' in [x.lower() for x in words])):

                    # Grab the last word in the line.
                    newfile = words[-1]

                    # Do variable substitutons
                    newfile = _variablesubstitutions(newfile, variables)

                    # Remove any quotes.
                    newfile.replace("'", "").replace('"', '')

                    # Deduce the location of newfile.
                    newpath = path

                    # Check newfile.
                    newfile = _newfilechecks(addfile, newfile, path)

                    # Recursive function.
                    file_parser(newfile, newpath, files, substitutions)

        fil.close()


def detectsubstitutions(args):
    """Detect substitutions specified on the commandline.

    This method will be called from the hooks within the applications.py
    module. This is where the applications specific code should be placed so
    that Longbow can handle substitutions.

    """
    # Initialise variables
    removelist = []
    sub = {}

    for item in args:

        if ":" in item:

            before, _, after = item.rpartition(":")
            sub[before] = after
            removelist.append(item)

        elif "=" in item:

            before, _, after = item.rpartition("=")
            sub[before] = after
            removelist.append(item)

    for item in removelist:

        args.remove(item)

    return sub


def _filechecks(path, filename):
    """Check the file paths to make sure they are valid."""
    # Initialise variables
    addfile = ""

    # If the filename has an absolute path but doesn't exist locally, assume
    # it is on the remote resource
    if os.path.isabs(filename) is True:

        if os.path.isfile(filename) is False:

            addfile = ""

        else:

            raise exceptions.RequiredinputError(
                "It appears that the user is trying to refer to a file '{0}' "
                "using an explicit path. Please just provide the names of "
                "input files".format(filename))

    # Else, if the file is in the given path
    elif os.path.isfile(os.path.join(path, filename)) is True:

        addfile = filename

    # Otherwise issue a warning
    else:

        raise exceptions.RequiredinputError(
            "It appears the file '{0}' is not present in the expected"
            " directory.".format(filename))

    return addfile


def _fileopen(path, addfile):
    """Open a file and return the handle."""
    # Initialise variable
    fil = None

    try:

        fil = open(os.path.join(path, addfile), "r")

    except (IOError, OSError):

        raise exceptions.RequiredinputError(
            "Can't read the file '{0}'".format(addfile))

    return fil


def _internalsubstitutions(variables, words):
    """Process substitutions from file."""
    # Process substitutions.
    if words[0].lower() == 'set':

        if words[2] == "=":

            variables[words[1]] = words[3]

        else:

            variables[words[1]] = words[2]


def _newfilechecks(addfile, newfile, path):
    """Perform basic checks of on any new file."""
    if newfile.count("../") == 1:

        # If we are in a repX subdirectory, the file must be in cwd.
        if re.search(r'rep\d', addfile):

            _, _, newfile = newfile.rpartition("/")

        # Else we must be in cwd so issue a warning about referring to a file
        # that is above cwd.
        else:

            raise exceptions.RequiredinputError(
                "It appears that the user is trying to refer to a file '{0}' "
                "in file '{1}' that is a directory up from the '{2}' "
                "directory. Only files in '{2}' or a repX subdirectory can be "
                "copied to the remote resource. If the file you are trying to "
                "refer to is on the remote resource, give the explicit path "
                "to the file.".format(newfile, addfile, path))

    # Else ../../ is used in an input script issue an error.
    elif newfile.count("../") > 1:

        raise exceptions.RequiredinputError(
            "It appears that the user is trying to refer to a file '{0}' in "
            "file '{1}' that's multiple directories up from a valid "
            "directory. This is not permitted. If the file you are trying to "
            "refer to is on the remote resource, give the explicit path to "
            "the file.".format(newfile, addfile))

    # Else we are in a repX subdirectory and the file isn't in ../ or ./repX,
    # the file is likely in the same directory.
    elif re.search(r'rep\d', addfile) and not re.search(r'rep\d', newfile):

        splitpath, _ = os.path.split(addfile)
        newfile = os.path.join(splitpath, newfile)

    # Else newfile is indicated to be in a repX subdirectory.
    elif re.search(r'rep\d', newfile):

        # If we are already in a repX subdirectory throw exception.
        if re.search(r'rep\d', addfile):

            raise exceptions.RequiredinputError(
                "It appears that the user is trying to refer to a file '{0}' "
                "that is in a repX/repX subdirectory. This is not permitted."
                .format(newfile))

        # Else we must be in cwd.
        else:

            newfile = "rep" + newfile.split("rep")[1]

    return newfile


def _variablesubstitutions(newfile, variables):
    """Process substitutions."""
    # Do variable substitution.
    if '@' in newfile and len(variables.keys()) > 0:

        before, _, after = newfile.rpartition("@")

        for instance in variables:

            if instance in after:

                newfile = before + after.replace(instance, variables[instance])

    return newfile
