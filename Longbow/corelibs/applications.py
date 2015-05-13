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
from _ast import Sub
from fileinput import filename

"""The application module provides methods for testing whether the requested
application executable is present on the remote machine and for processing the
command line arguments of the job in a code specific manner."""

import logging
import os
import re

try:
    import Longbow.corelibs.exceptions as ex
except ImportError:
    import corelibs.exceptions as ex

try:
    import Longbow.corelibs.shellwrappers as shellwrappers
except ImportError:
    import corelibs.shellwrappers as shellwrappers

try:
    import Longbow.plugins.apps as apps
except ImportError:
    import plugins.apps as apps


LOGGER = logging.getLogger("Longbow")


def testapp(hosts, jobs):

    """Test whether the application executable is reachable. This method
    does support testing for modules."""

    checked = {}

    LOGGER.info("Testing the executables defined for each job.")

    for job in jobs:

        resource = jobs[job]["resource"]
        executable = jobs[job]["executable"]

        # If we haven't checked this resource then it is likely not in the dict
        if resource not in checked:
            checked[resource] = []

        # Now check if we have tested this exec already.
        if executable not in checked[resource]:

            # If not then add it to the list now.
            checked[resource].extend([executable])

            LOGGER.info(
                "Checking executable '%s' on '%s'", executable, resource)

            cmd = []
            if jobs[job]["modules"] is "":
                LOGGER.debug("Checking without modules.")

            else:
                LOGGER.debug("Checking with modules.")

                for module in jobs[job]["modules"].split(","):
                    module.replace(" ", "")
                    cmd.extend(["module load " + module + "\n"])

            cmd.extend(["which " + executable])

            try:
                shellwrappers.sendtossh(hosts[resource], cmd)
                LOGGER.info("Executable check - passed.")

            except ex.SSHError:
                LOGGER.error("Executable check - failed.")
                raise


def processjobs(jobs):

    """Process the jobs command line, this method will extract information
    from the command line and construct a list of files to be staged."""

    LOGGER.info("Processing job/s and detecting files that require upload.")

    # Get dict of executables and their required flags.
    required = getattr(apps, "EXECFLAGS")

    for job in jobs:

        # Some initialisation.
        filelist = []
        flags = []
        executable = jobs[job]["executable"]

        # Process the command line into a list.
        args = jobs[job]["commandline"].split()

        LOGGER.debug("Args for job '%s': %s", job, args)

        # Now we should check that the required flags have been supplied if
        # the program being used is one of the ones we are supporting.
        if executable is not "":

            # Find missing flags.
            flags = list(set(required[executable]) -
                         set(args))

            # Check for missing flags.
            if len(flags) is not 0:

                # This is to handle cases where there can be multiple required
                # flags where the user only has to give on (-s vs -defnm).
                for flag in flags:
                    if " || " in flag:
                        tmp = flag.split(" || ")

                        # Now we have split the flags find and delete any that
                        # match in the list of missing flags
                        for item in tmp:
                            if item in args:
                                flags.remove(flag)
                                break

            # Do we still have missing flags.
            if len(flags) is not 0:

                # Jobs that don't use a commandline flag to denote the input
                # file, such NAMD can be dealt with like this.
                if "?" in flags:

                    # The only thing we can really do is check that something
                    # is given on the cmdline.
                    if args is "":
                        raise ex.RequiredinputError(
                            "in job '%s' it appears that the input file is "
                            "missing" % job)

                    elif len(args) is 1 and args[0] is "<":
                        raise ex.RequiredinputError(
                            "in job '%s' it appears that the %s input "
                            "file is missing" % (job, jobs[job]["modules"]))

                else:
                    raise ex.RequiredinputError(
                        "in job '%s' there are missing flags on the command"
                        "line '%s'. See documentation for module '%s' " %
                        (job, flags, jobs[job]["modules"]))

        for item in args:
            if item.count(os.path.pardir) > 0 or os.path.isabs(item):
                raise ex.RequiredinputError(
                        "In job %s input files are being provided with "
                        "explicit paths or from directories above "
                        "localworkdir. This is not supported" % job)

        # Path correction for multijobs.
        cwd = jobs[job]["localworkdir"]

        if len(jobs) > 1:

            # Add the job name to the path.
            cwd = os.path.join(cwd, job)
            jobs[job]["localworkdir"] = cwd

        # Check that the directory exists.
        if os.path.isdir(cwd) is False:

            raise ex.DirectorynotfoundError(
                "The working directory '%s' " % cwd + "cannot be found for "
                "job '%s'" % job)

        # Detect command line substitutions
        # Create dictionary of charmm substitutions
        if jobs[job]["executable"] == "charmm":
            substte = {}
            for item in args:
                if ":" in item:
                    before, sep, after = item.rpartition(":")
                    substte[before] = after
                elif "=" in item:
                    before, sep, after = item.rpartition("=")
                    substte[before] = after

        # Create dictionary of lammps substitutions
        elif jobs[job]["executable"] == "lmp_xc30":
            substte = {}
            for index, item in enumerate(args):
                if item == "-var" or item == "-v":
                    substte[args[index + 1]] = args[index + 2]

        # Run through the commandline and search for
        # matches, any that are found we will assume they need staging.
        for index, item in enumerate(args):

            # if single job
            if int(jobs[job]["replicates"]) == 1:

                # Check it is there.
                if item not in filelist:
                    # charmm
                    if executable == "charmm":
                        CHARMM_parser(item, cwd, filelist, substte)

                    # lammps
                    elif executable == "lmp_xc30":
                        LAMMPS_parser(item, cwd, filelist, substte)

                    # NAMD
                    elif executable == "namd2":
                        NAMD_parser(item, cwd, filelist)

                    # amber and gromacs
                    else:
                        filelist.append(os.path.join(cwd, item))

            # elif replicate job
            else:
                for i in range(1, int(jobs[job]["replicates"])+1):
                    if item not in filelist:

                        # charmm
                        if executable == "charmm":
                            filepath = os.path.join(cwd, "rep" + str(i))

                            if os.path.isdir(filepath) is True:
                                CHARMM_parser(item, filepath, filelist,
                                              substte)

                        # lammps
                        elif executable == "lmp_xc30":
                            filepath = os.path.join(cwd, "rep" + str(i))

                            if os.path.isdir(filepath) is True:
                                LAMMPS_parser(item, filepath, filelist,
                                              substte)

                        # namd
                        elif executable == "namd2":
                            filepath = os.path.join(cwd, "rep" + str(i))

                            if os.path.isdir(filepath) is True:
                                NAMD_parser(item, filepath, filelist)

                        # amber and gromacs
                        else:

                            # if the file is in rep${i} subdirectory
                            if os.path.isfile(os.path.join(cwd, "rep" + str(i),
                                                           item)) is True:

                                # Add file to list of files required to upload.
                                filepath = os.path.join(cwd, "rep" + str(i),
                                                        item)
                                filelist.append(filepath)

                            # elif the file is in the parent directory
                            elif os.path.isfile(os.path.join(cwd, item)) \
                                    is True:

                                # Add file to list of files required to upload.
                                filepath = os.path.join(cwd, item)
                                filelist.append(filepath)
                                args[index] = os.path.join("../", item)

        # If the flag is the extra files upload then pop it out of the args
        # list as the file will have been got for staging but we don't want
        # to pass this on to the MD code.
        while "-stage" in args:
            index = args.index("-stage")
            args.pop(index)
            args.pop(index)

        # Concatenate executable and args back into a string.
        args = executable + " " + " ".join(args)

        # Add the filelist to the job configuration.
        jobs[job]["filelist"] = filelist

        # Replace the input commandline with the execution commandline.
        jobs[job]["commandline"] = args

        # Log results.
        LOGGER.info(
            "For job '%s' - files for upload: " % job + ", ".join(filelist))

        LOGGER.info(
            "For job '%s' - execution string: %s", job, args)

    LOGGER.info("Processing jobs - complete.")


def CHARMM_parser(filename, path, files, substitutions=None):
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
                        if '@' in newfile:
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
                        CHARMM_parser(newfile, newpath, files, substitutions)

            fil.close()


def LAMMPS_parser(filename, path, files, substitutions=None):
    '''
    Recursive function that will assimilate from lammps input files a list of
    files (files) to be staged to the execution host. filename will be added
    to the list and any files mentioned in filename will also be added and
    searched. Substitutions is a dictionary of "$" style variables specified
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
        # Define keywords and create a dictionary for variable substitutions
        keywords = ['read_data', 'read_restart', 'read_dump']
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

                # if line commented out, skip
                if line[0] == "#":
                    continue

                # Remove comments
                if '#' in line:
                    end = line.index('#')
                else:
                    end = len(line)

                words = line[:end].split()
                if len(words) > 0:

                    # allow substitutions from inside the input file as well
                    if words[0].lower() == 'variable':
                        variables[words[1]] = words[3]

                    # if this line is reading in an input file
                    if words[0].lower() in keywords:
                        newfile = words[1]

                        # Do variable substitution
                        if '$' in newfile:
                            start = newfile.index('$')+1
                            if newfile[start] == '{':
                                end = newfile[start:].index('}')+start
                                var = variables[newfile[start+1:end]]
                                newfile = newfile[0:start-1] + var + \
                                        newfile[end+1:]
                            else:
                                end = start+1
                                var = variables[newfile[start:end]]
                                newfile = newfile[0:start-1] + var + \
                                        newfile[end:]

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
                        LAMMPS_parser(newfile, newpath, files, substitutions)

        fil.close()


def NAMD_parser(filename, path, files):
    '''
    Recursive function that will assimilate from NAMD input files a list of
    files (files) to be staged to the execution host. filename will be added
    to the list and any files mentioned in filename will also be added and
    searched. Substitutions is a dictionary of "$" style variables specified
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
        # Define keywords and create a dictionary for variable substitutions
        keywords = ['coordinates', 'ExtendedSystem', 'structure', 'parameters',
                    'paraTypeXplor', 'paraTypeCharmm', 'velocities',
                    'binvelocities', 'bincoordinates']
        variables = {}

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
                        if '$' in newfile:
                            before, sep, after = newfile.rpartition("$")
                            for instance in variables:
                                if instance in after:
                                    newfile = before + after.replace(instance,
                                                        variables[instance])

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
                        NAMD_parser(newfile, newpath, files)

        fil.close()
