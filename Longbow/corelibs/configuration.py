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

"""This module contains methods for loading and saving to Longbow (ini)
configuration files in addition to methods for extracting the resultant
information into Longbow data structures. The templates for these data
structures and their forms are also declared within this module.

The following data structures can be found:

HOSTTEMPLATE
    The template of the hosts data structure. The Longbow API will assume
    that variables listed here are to be found in this structure.

HOSTREQUIRED
    A list to mark parameters that are required to be initialised during
    configuration

JOBTEMPLATE
    The template of the job data structure. The Longbow API will assume
    that variables listed here are to be found in this structure.

JOBREQUIRED
    A list to mark parameters that are required to be initialised during
    configuration

The following methods can be found:

processjobs()
    Method for processing the raw configuration structures loaded from the
    configuration files into Longbow friendly configuration structures.
    This is where the parameter hierarchy is applied.

loadconfigs()
    Method for loading and extracting data from the Longbow configuration
    files.

saveconfigs()
    Method for saving data to Longbow configuration files, this method will
    honour comments and simply ammed the file structure with new or changed
    data."""

import logging

# Depending on how Longbow is installed/utilised the import will be slightly
# different, this should handle both cases.
try:

    EX = __import__("corelibs.exceptions", fromlist=[''])
    APPS = __import__("plugins.apps", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    APPS = __import__("Longbow.plugins.apps", fromlist=[''])


LOGGER = logging.getLogger("Longbow")

HOSTTEMPLATE = {
    "accountflag": "",
    "corespernode": "24",
    "handler": "",
    "host": "",
    "port": "22",
    "remoteworkdir": "",
    "scheduler": "",
    "user": ""
}

HOSTREQUIRED = [
    "host",
    "user",
    "remoteworkdir"
]

JOBTEMPLATE = {
    "account": "",
    "cores": "24",
    "cluster": "",
    "download-exclude": "",
    "download-include": "",
    "executable": "",
    "executableargs": "",
    "frequency": "300",
    "localworkdir": "",
    "modules": "",
    "maxtime": "24:00",
    "memory": "",
    "queue": "",
    "resource": "",
    "replicates": "1",
    "upload-exclude": "",
    "upload-include": ""
}

JOBREQUIRED = [
    "executableargs",
    "executable",
    "replicates"
]


def processconfigs(hostfile, jobfile, cwd, params):

    """
    A Method for processing configuration files into the Longbow data
    format.

    Arguments are:

    hostfile (string): This should be an absolute path to a configuration
                       file, this parameter is required

    jobfile (string): This should be an absolute path to a configuration
                      file, this parameter is optional (empty string if not
                      needed)

    args (string): This should be an absolute path to a configuration
                       file, this parameter is required

    cwd (string): This should be an absolute path to a configuration
                       file, this parameter is required

    executable (string): This should be an absolute path to a configuration
                       file, this parameter is required

    params (dictionary): This should be an absolute path to a configuration
                       file, this parameter is required

    Return parameters are:

    hosts (dictionary): A fully processed Longbow hosts data structure.

    jobs (dictionary) A fully processed Longbow jobs data structure.
    """

    # TODO the param 'account' has been changed over from hosts to jobs.
    # This needs changing in the plugin specific parts.

    # Define our main data structures.
    hosts = {}
    jobs = {}

    # Try and load the host file.
    try:

        _, hostsections, hostdata = loadconfigs(hostfile)

    except EX.ConfigurationError:

        raise

    # If we have been given a job file then try and load it.
    if jobfile is not "":

        try:

            _, _, jobdata = loadconfigs(jobfile)

        except EX.ConfigurationError:

            raise

    # Otherwise we can assume that there is going to be a single job on the
    # command line.
    else:

        # No data to load.
        jobdata = {}

    # Process the host configuration
    for host in hostdata:

        # Create a host with defaults set up.
        hosts[host] = HOSTTEMPLATE.copy()

    # Process the job configuration.
    for job in jobdata:

        jobs[job] = JOBTEMPLATE.copy()

    # Validation on required params.
    print hosts
    print jobs
    import sys
    sys.exit("test over")

    return hosts, jobs


def loadconfigs(configfile):

    """Method to load an ini file. Files of this format contain the following
    mark-up structure.

    Sections of a file are marked using square brackets
    Section then contain option statements of the form "param = value"
    Comments are marked using hashes.

    An example of such a file would be:

    [section1]
    # this is the first option
    option1 = value1
    # this is the second option
    option2 = value2

    [section2]
    # this is the first option
    option1 = value1
    # this is the second option
    option2 = value2

    [section3]
    # this is the first option
    option1 = value1
    # this is the second option
    option2 = value2

    This method performs basic error handling to do with the structure of the
    ini file only. All error handling specific to Longbow should be performed
    elsewhere.

    Required arguments are:

    configfile (string): This should be an absolute path to a configuration
                         file

    Return parameters are:

    contents (list): This is the raw file structure where each line is an item
                     in the list

    sections (list): This is a list of section headers in the data (preserves
                     order)

    data (dict of dicts): This is a structure containing the data loaded from
                          the file, a dictionary is created for each heading in
                          the ini file. Then the parameters and values under
                          each heading will form a dictionary within the
                          corresponding heading section (dictionary of
                          dictionaries)
    """

    LOGGER.info("Loading configuration information from file '{0}'"
                .format(configfile))

    sections = []
    params = {}

    # Open configuration file.
    try:

        tmp = open(configfile, "r")

        # Grab all of the information from the file.
        contents = tmp.readlines()

    except IOError:

        raise EX.ConfigurationError(
            "Can't read the configurations from '{0}'".format(configfile))

    # Strip out the newline chars.
    contents = [line.strip("\n") for line in contents]

    # Close configuration file (don't need it anymore).
    tmp.close()

    # Pull out sections into list.
    for item in contents:

        # Don't care about blank lines.
        if len(item) > 0:

            try:
                # Find section markers
                if item[0] == "[" and item[len(item)-1] == "]":

                    # Remove the square bracket section markers.
                    section = "".join(a for a in item if a not in "[]")

                    # Add to list of sections.
                    sections.append(section)

                    # Create a new section in the data structure.
                    params[section] = {}

                # Find comment markers.
                elif item[0] is "#":

                    # Ignore comments.
                    pass

                # Anything else must be option data.
                else:

                    # Option is in the format key = param. So extract these.
                    key, value = item.split(" = ")

                    # Store the keys and values in the data structure.
                    params[section][key] = value

            except NameError:

                # Issue warning.
                pass

    # Check if there are zero sections.
    if len(sections) is 0:

        raise EX.ConfigurationError(
            "Error no sections are defined in configuration file '{0}'"
            .format(configfile))

    # Check for sections with zero options.
    for section in sections:

        if len(params[section]) is 0:

            raise EX.ConfigurationError(
                "Error section '{0}' contains no parameter definitions using "
                "configuration file '{1}'".format(section, configfile))

    return contents, sections, params


def saveconfigs(configfile, params):

    """
    Method to saving to an ini file. Files of this format contain the
    following mark-up structure.

    Sections of a file are marked using square brackets
    Section then contain option statements of the form "param = value"
    Comments are marked using hashes.

    An example of such a file would be:

    [section1]
    # this is the first option
    option1 = value1
    # this is the second option
    option2 = value2

    [section2]
    # this is the first option
    option1 = value1
    # this is the second option
    option2 = value2

    [section3]
    # this is the first option
    option1 = value1
    # this is the second option
    option2 = value2

    This method is comment safe, this was a major downfall of the standard
    python parser as it would wipe out comments that a user would include.

    Required arguments are:

    configfile (string): This should be an absolute path to a configuration
                         file

    params (dictionary): This should contain the data structure that should
                         be saved (typically hosts of job configs structure)
    """

    LOGGER.info("Saving configuration information to file '{0}'"
                .format(configfile))

    keydiff = {}
    valuediff = {}

    # Load up the original file including comment structure (list).
    contents, _, oldparams = loadconfigs(configfile)

    # Run through each section in the data.
    for section in params:

        # Run through each parameter in this section.
        for option in params[section]:

            try:

                # Check for continuity between data in file and that in
                # Longbow.
                if params[section][option] != oldparams[section][option]:

                    try:

                        # If parameter is changed try adding it to the diff
                        valuediff[section][option] = params[section][option]

                    except KeyError:

                        # If this is the first time then section won't exist.
                        valuediff[section] = {option: params[section][option]}

            # If we get a key error then the paramater is a new one.
            except KeyError:

                try:

                    # Try adding to diff
                    keydiff[section][option] = params[section][option]

                except KeyError:

                    # If this is the first time we will need to create the
                    # section.
                    keydiff[section] = {option: params[section][option]}

    # Update the file metastructure with these changes.
    # Firstly handle the updates.
    for section in valuediff:

        # Find the section start (so we know where to look)
        sectionstartindex = contents.index("[" + section + "]")

        # Find the section end.
        try:

            sectionendindex = contents.index(
                [a for a in contents if "[" and "]" in a and
                 contents.index(a) > sectionstartindex][0]) - 1

        except IndexError:

            sectionendindex = len(contents)

        # Limit our search to this range for the parameter.
        for option in valuediff[section]:

            # Get the line index to edit.
            editposition = (
                sectionstartindex +
                contents[sectionstartindex:sectionendindex].index(
                    option + " = " + oldparams[section][option]))

            # Edit the entry.
            contents[editposition] = (
                option + " = " + valuediff[section][option])

    # Now handle new entries. Run through each section.
    for section in keydiff:

        try:
            # Find the section start.
            sectionstartindex = contents.index("[" + section + "]")

            # Find the section end.
            try:
                sectionendindex = contents.index(
                    [a for a in contents if "[" and "]" in a and
                     contents.index(a) > sectionstartindex][0]) - 1

            except IndexError:

                sectionendindex = len(contents)

            # Now for each option.
            for option in keydiff[section]:

                # Insert into the list in the appropriate place.
                contents.insert(
                    sectionendindex, option + " = " + keydiff[section][option])

        # Doesn't exist so it is a new section.
        except ValueError:

            # Append the section.
            contents.extend(["", "[" + section + "]"])

            # Now run through each option.
            for option in keydiff[section]:

                # And append it to the end of the list.
                contents.append(option + " = " + keydiff[section][option])

    try:

        # Open file for writing.
        tmp = open(configfile, "w")

        # Write it all out.
        for item in contents:
            tmp.write(item + "\n")

        # Close file.
        tmp.close()

    except IOError:

        raise EX.ConfigurationError(
            "Error saving to '{0}'".format(configfile))
