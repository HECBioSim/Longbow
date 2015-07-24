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



The following methods can be found:

loadconfigs()
    Method for loading and extracting data from the Longbow configuration
    files.

saveconfigs()
    Method for saving data to Longbow configuration files, this method will
    honour comments and simply ammed the file structure with new or changed
    data."""

import logging

# Depending on how longbow is installed/utilised the import will be slightly
# different, this should handle both cases.
try:

    EX = __import__("corelibs.exceptions", fromlist=[''])
    APPS = __import__("plugins.apps", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    APPS = __import__("Longbow.plugins.apps", fromlist=[''])


LOGGER = logging.getLogger("Longbow")


def loadhosts(confile):

    """Method for processing host configuration files."""

    pass


def loadjobs(jobconfile, hostsconfile, param):

    """Method for processing job configuration files."""

    pass


def sortjobsconfigs(hostsconfig, jobsconfig, executable, cwd, args,
                    replicates):

    """Method to sort and prioritise job configuration parameters."""

    pass


def sorthostsconfigs(hostsconfig, jobsconfig):

    pass


def amendjobsconfigs(hosts, jobs):

    """Method to make final amendments to the job configuration parameters"""

    pass


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
    """

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

    """Method to saving to an ini file. Files of this format contain the
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
    """

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
