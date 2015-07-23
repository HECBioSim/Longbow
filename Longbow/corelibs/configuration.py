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

"""This module contains methods for loading and saving configuration
files as well as methods for processing host and job configuration files.
The following methods can be found:

loadhosts()
    Method containing the structure template for host configuration files.
loadjobs()
    Method containing the structure template for job configuration files.
def sortjobsconfigs()
    Method to sort and prioritise jobs configuration parameters.
def sorthostsconfigs():
    Method to sort and prioritise hosts configuration parameters.
def amendjobsconfigs(hosts, jobs)
    Method to make final amendments to the job configuration parameters.
loadconfigs()
    Method containing the code for parsing configuration files.
saveconfigs()
    Method containing the code for saving configuration files."""

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
    data = {}

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
                    data[section] = {}

                # Find comment markers.
                elif item[0] is "#":

                    # Ignore comments.
                    pass

                # Anything else must be option data.
                else:

                    # Option is in the format key = param. So extract these.
                    key, value = item.split(" = ")

                    # Store the keys and values in the data structure.
                    data[section][key] = value

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

        if len(data[section]) is 0:

            raise EX.ConfigurationError(
                "Error section '{0}' contains no parameter definitions using "
                "configuration file '{1}'".format(section, configfile))

    return data, sections


def saveconfigs(confile, params):

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

    pass
