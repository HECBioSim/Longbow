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

"""."""

import os
import re

try:

    import corelibs.exceptions as exceptions

except ImportError:

    import Longbow.corelibs.exceptions as exceptions


EXECDATA = {
    "namd2": {
        "subexecutables": [],
        "requiredfiles": ["<"],
        },
    "namd2.mpi": {
        "subexecutables": [],
        "requiredfiles": ["<"],
        },
    "namd2.cuda": {
        "subexecutables": [],
        "requiredfiles": ["<"],
        }
    }


def file_parser(filename, path, files, substitutions=None):
    '''
    Recursive function that will assimilate from NAMD input files a list of
    files (files) to be staged to the execution host. filename will be added
    to the list and any files mentioned in filename will also be added and
    searched. Substitutions is a dictionary of "$" style variables.
    '''

    # Check the location of filename
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

    # Now look for references to other files in the input file if not done so
    # already
    if addfile and (addfile not in files or not files):

        files.append(addfile)

        # Create a dictionary for any variable substitutions
        # Define keywords and create a dictionary for variable substitutions
        keywords = ['coordinates', 'extendedsystem', 'structure', 'parameters',
                    'velocities', 'binvelocities', 'bincoordinates',
                    'ambercoor', 'parmfile', 'conskfile', 'tclforcesscript',
                    'fixedatomsfile', 'grotopfile', 'grocoorfile']

        variables = {}

        fil = None

        # Open the file
        try:

            fil = open(os.path.join(path, addfile), "r")

        except IOError:

            exceptions.RequiredinputError("Can't read the file '{0}'"
                                          .format(addfile))

        if fil:

            # search every line for possible input files
            for line in fil:

                # Remove comments
                if '#' in line:

                    end = line.index('#')

                else:

                    end = len(line)

                words = line[:end].split()

                if len(words) > 0:

                    # allow substitutions from inside the input file as well
                    if words[0].lower() == 'set':

                        if words[2] == "=":

                            variables[words[1]] = words[3]

                        else:

                            variables[words[1]] = words[2]

                    # if this line is reading in an input file
                    if words[0].lower() in keywords:

                        newfile = words[-1]

                        # Do variable substitution
                        if '$' in newfile and len(variables.keys()) > 0:

                            before, _, after = newfile.rpartition("$")

                            for instance in variables:

                                if instance in after:

                                    newfile = before + after.replace(
                                        instance, variables[instance])

                        # deduce the location of newfile
                        newpath = path

                        if newfile.count("../") == 1:

                            # if we are in a repX subdirectory, the file must
                            # be in cwd
                            if re.search(r'rep\d', addfile):

                                before, _, after = newfile.rpartition("/")
                                newfile = after

                            # else we must be in cwd so issue a warning about
                            # referring to a file that is above cwd
                            else:

                                raise exceptions.RequiredinputError(
                                    "It appears that the"
                                    " user is trying to refer to a file '{0}'"
                                    " in file '{1}' that is a"
                                    " directory up from the '{2}'"
                                    " directory. Only files in '{3}'"
                                    " or a repX subdirectory can be"
                                    " copied to the remote resource. If the "
                                    "file you are trying to refer to is on the"
                                    " remote resource, give"
                                    " the explicit path to the file.".format(
                                        newfile, addfile, path, path))

                        # elif ../../ is used in an input script issue an error
                        elif newfile.count("../") > 1:

                            raise exceptions.RequiredinputError(
                                "It appears that the user is trying to refer "
                                "to a file '{0}' in file '{1}' that's multiple"
                                " directories up from a valid directory. This "
                                "is not permitted. If the file you are trying "
                                "to refer to is on the remote resource, give "
                                "the explicit "
                                "path to the file.".format(newfile, addfile))

                        # elif we are in a repX subdirectory and the file
                        # isn't in ../ or ./repX, the file is presumably in the
                        # same directory
                        elif (re.search(r'rep\d', addfile) and not
                              re.search(r'rep\d', newfile)):

                            splitpath, _ = os.path.split(addfile)
                            newfile = os.path.join(splitpath, newfile)

                        # elif newfile is indicated to be in a repX
                        # subdirectory...
                        elif re.search(r'rep\d', newfile):

                            # if we are already in a repX subdirectory issue a
                            # warning
                            if re.search(r'rep\d', addfile):

                                raise exceptions.RequiredinputError(
                                    "It appears that the"
                                    "user is trying to refer to a file '{0}'"
                                    " that is in a repX/repX "
                                    "subdirectory. This is not "
                                    "permitted.".format(newfile))

                            # else we must be in cwd...
                            else:

                                newfile = "rep" + newfile.split("rep")[1]

                        # recursive function
                        file_parser(newfile, newpath, files, substitutions)

            fil.close()
