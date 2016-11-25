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

"""This is the LAMMPS plugin module.

This plugin is relatively simple in the fact that adding new executables is as
simple as modifying the EXECDATA structure below. See the documentation at
http://www.hecbiosim.ac.uk/longbow-devdocs for more information.
"""

import os
import re

import Longbow.corelibs.exceptions as exceptions


EXECDATA = {
    "lmp_xc30": {
        "subexecutables": [],
        "requiredfiles": ["-i"],
    },
    "lmp_linux": {
        "subexecutables": [],
        "requiredfiles": ["-i"],
    },
    "lmp_gpu": {
        "subexecutables": [],
        "requiredfiles": ["-i"],
    },
    "lmp_mpi": {
        "subexecutables": [],
        "requiredfiles": ["-i"],
    },
    "lmp_cuda": {
        "subexecutables": [],
        "requiredfiles": ["-i"],
    },
    "lmp": {
        "subexecutables": [],
        "requiredfiles": ["-i"],
    }
}


def file_parser(filename, path, files, substitutions=None):
    """Method to find dependancy files for upload in a substitution aware way.

    Recursive function that will assimilate from charmm input files, a list of
    dependancy files to be staged to the remote host. The filename will be
    added to the list and any files mentioned in this included file will also
    be added and searched. Substitutions is a dictionary of "@" style
    variables.

    """
    addfile = _filechecks(path, filename)

    # Now look for references to other files in the input file if not done so
    # already.
    if addfile and (addfile not in files or not files):

        files.append(addfile)

        # Create a dict for any variable substitutions and define keywords.
        keywords = ['read_data', 'read_restart', 'read_dump']
        variables = {} if not substitutions else substitutions

        fil = _fileopen(path, addfile)

        # Search every line for possible input files.
        for line in fil:

            # If line commented out, skip.
            if line[0] == "#":

                continue

            # Remove comments.
            if '#' in line:

                words = line[:line.index('#')].split()

            else:

                words = line[:len(line)].split()

            if len(words) > 0:

                _internalsubstitutions(variables, words)

                # If this line is reading in an input file.
                if words[0].lower() in keywords:

                    newfile = words[-1]

                    # Do variable substitutons
                    newfile = _variablesubstitutions(newfile, variables)

                    # Deduce the location of newfile.
                    newpath = path

                    # Check newfile.
                    newfile = _newfilechecks(addfile, newfile, path)

                    # Recursive function.
                    file_parser(newfile, newpath, files, substitutions)

        fil.close()


def detectsubstitutions(args):
    """Function to detect substitutions specified on the commandline.

    This method will be called from the hooks within the applications.py
    module. This is where the applications specific code should be placed so
    that Longbow can handle substitutions.

    """
    # Initialise variables.
    removelist = []
    sub = {}

    for index, item in enumerate(args):

        if item == "-var" or item == "-v":

            sub[args[index + 1]] = args[index + 2]
            removelist.append(item)
            removelist.append(args[index + 1])
            removelist.append(args[index + 2])

    for item in removelist:

        args.remove(item)

    return sub


def _filechecks(path, filename):
    """Check the file paths to make sure they are valid."""
    # Initialise variable.
    addfile = ""

    # if the filename has an absolute path but doesn't exist locally, assume
    # it is on the remote resource
    if os.path.isabs(filename) is True:

        if os.path.isfile(filename) is False:

            addfile = ""

        else:

            raise exceptions.RequiredinputError(
                "It appears that the user is trying to refer to a file '{0}' "
                "using an explicit path. Please just provide the names of "
                "input files".format(filename))

    # elif the file is in the given path
    elif os.path.isfile(os.path.join(path, filename)) is True:

        addfile = filename

    # else issue a warning
    else:

        raise exceptions.RequiredinputError(
            "It appears the file '{0}' is not present in the expected "
            "directory.".format(filename))

    return addfile


def _fileopen(path, addfile):
    """Open a file and return the handle."""
    # Initialise variable.
    fil = None

    try:

        fil = open(os.path.join(path, addfile), "r")

    except (IOError, OSError):

        raise exceptions.RequiredinputError(
            "Can't read the file '{0}'".format(addfile))

    return fil


def _internalsubstitutions(variables, words):
    """A method to process substitutions from file."""
    # Process substitutions.
    if words[0].lower() == 'variable':

        variables[words[1]] = words[3]


def _newfilechecks(addfile, newfile, path):
    """A private method to check any new files."""
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

        # If we are already in a repX subdirectory throw exception
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
    """A method to process substitutions."""
    # Do variable substitution.
    if '$' in newfile and len(variables.keys()) > 0:

        start = newfile.index('$') + 1

        if newfile[start] == '{':

            end = newfile[start:].index('}') + start
            var = variables[newfile[start + 1:end]]
            newfile = (newfile[0:start - 1] + var + newfile[end + 1:])

        else:

            end = start + 1
            var = variables[newfile[start:end]]
            newfile = (newfile[0:start - 1] + var + newfile[end:])

    return newfile
