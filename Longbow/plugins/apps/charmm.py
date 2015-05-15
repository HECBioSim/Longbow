# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of the Longbow software which was developed as part of
# the HECBioSim project (http://www.hecbiosim.ac.uk/).
#
# HECBioSim facilitates and supports high-end computing within the
# UK biomolecular simulation community on resources such as Archer.
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

"""."""

import os
import re

try:
    import Longbow.corelibs.exceptions as ex
except ImportError:
    import corelibs.exceptions as ex


EXECDATA = {
    "charmm": ["?"]
    }


def file_parser(filename, path, files, substitutions=None):
    '''
    Recursive function that will assimilate from charmm input files a list of
    files (files) to be staged to the execution host. filename will be added
    to the list and any files mentioned in filename will also be added and
    searched. Substitutions is a dictionary of "@" style variables specified
    on the command line.
    '''

    # Check the location of filename
    addfile = ""

    # if the filename has an absolute path but doesn't exist locally, assume
    # it is on the HPC
    if os.path.isabs(filename) is True:
        if os.path.isfile(filename) is False:
            addfile = ""

        else:
            raise ex.RequiredinputError(
                    "It appears that the"
                    "user is trying to refer to a file %s"
                    "using an explicit path. Please just provide"
                    "the names of input files" % filename)

    # elif the file is in the given path
    elif os.path.isfile(os.path.join(path, filename)) is True:
            addfile = os.path.join(path, filename)

    # Now look for references to other files in the input file if not done so
    # already
    if addfile and (addfile not in files or not files):

        files.append(addfile)

        # Create a dictionary for any variable substitutions
        variables = {} if not substitutions else substitutions

        fil = None
        # Open the file
        try:
            fil = open(addfile, "r")
        except IOError:
            ex.RequiredinputError("Can't read the %s file:" % addfile)

        if fil:
            # search every line for possible input files
            for line in fil:

                # Remove comments
                if '!' in line:
                    end = line.index('!')
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

                    # Try to detect other input files
                    if ('read' in [x.lower() for x in words]) and \
                            ('name' in [x.lower() for x in words]):

                        # Grab the last word in the line
                        newfile = words[-1]

                        # Do variable substitution
                        if '@' in newfile and len(variables.keys()) > 0:
                            before, sep, after = newfile.rpartition("@")
                            for instance in variables:
                                if instance in after:

                                    newfile = before + after.replace(instance,
                                                        variables[instance])

                        # Remove any quotes
                        if (newfile[0] == newfile[-1]) and \
                                newfile.startswith(("'", '"')):

                            newfile = newfile[1:-1]

                        # work out the path of newfile
                        newpath = path
                        if newfile.count("../") == 1:
                            if re.search('rep\d', path):

                                newpath = os.path.dirname(path)
                                before, sep, after = newfile.rpartition("/")
                                newfile = after

                            else:
                                raise ex.RequiredinputError(
                                    "It appears that the"
                                    " user is trying to refer to a file %s"
                                    % newfile + " in file %s that is a" %
                                    addfile + " directory up from the %s"
                                    " directory." % path + ". Only files in %s"
                                    % path + " or a repX subdirectory can be"
                                    " copied to the HPC. If the file you are"
                                    " trying to refer to is on the HPC, give"
                                    " the explicit path to the file.")

                        elif newfile.count("../") > 1:
                            if re.search('rep\d', path):
                                raise ex.RequiredinputError(
                                    "It appears that the"
                                    "user is trying to refer to a file %s"
                                    % newfile + " in file %s that is two" %
                                    addfile + " directories up from the %s" %
                                    path + " subdirectory. Only files in %s" %
                                    path + " or %s can be copied to the HPC." %
                                    os.path.dirname(path) + " If the file you"
                                    " are trying to refer to is on the"
                                    " HPC, give the explicit path to the file")
                            else:
                                raise ex.RequiredinputError(
                                    "It appears that the"
                                    " user is trying to refer to a file %s"
                                    % newfile + " in file %s that is two"
                                    % addfile + " directories up from the %s"
                                    " directory." % path + ". Only files in %s"
                                    % path + " or a repX subdirectory can be"
                                    " copied to the HPC. If the file you are"
                                    " trying to refer to is on the HPC, give"
                                    " the explicit path to the file.")

                        # recursive function
                        file_parser(newfile, newpath, files, substitutions)

            fil.close()


def sub_dict(args):
    sub = {}
    for item in args:
        if ":" in item:
            before, sep, after = item.rpartition(":")
            sub[before] = after
        elif "=" in item:
            before, sep, after = item.rpartition("=")
            sub[before] = after

    return sub
