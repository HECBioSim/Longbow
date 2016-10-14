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

"""
This module contains methods for loading and saving to Longbow (ini)
configuration files in addition to methods for extracting the resultant
information into Longbow data structures. The templates for these data
structures and their forms are also declared within this module.

The following data structures can be found:

JOBTEMPLATE
    The template of the job data structure. The Longbow API will assume
    that variables listed here are to be found in this structure.

REQUIRED
    A dictionary to mark parameters that are required to be initialised during
    configuration and their error messages for cases when missing.

The following methods can be found:

processjobs(parameters)
    Method for processing the raw configuration structures loaded from the
    configuration files into Longbow friendly configuration structures.
    This is where the parameter hierarchy is applied.

loadconfigs(configfile)
    Method for loading and extracting data from the Longbow configuration
    files.

saveconfigs(configfile, params)
    Method for saving data to Longbow configuration files, this method will
    honour comments and simply amend the file structure with new or changed
    data.

saveini(inifile, params)
    A method to save an ini file formatted file (inifile) from a dictionary
    structure (params). This method is much simpler than the saveconfigs
    method which has been tuned to simply update configuration files.
"""

import logging
import re
import os
from random import randint

# Depending on how Longbow is installed/utilised the import will be slightly
# different, this should handle both cases.
try:

    import corelibs.exceptions as exceptions
    import plugins.apps as apps

except ImportError:

    import Longbow.corelibs.exceptions as exceptions
    import Longbow.plugins.apps as apps


LOG = logging.getLogger("Longbow.corelibs.configuration")

JOBTEMPLATE = {
    "account": "",
    "accountflag": "",
    "cluster": "",
    "cores": "24",
    "corespernode": "24",
    "download-exclude": "",
    "download-include": "",
    "email-address": "",
    "email-flags": "",
    "executable": "",
    "executableargs": "",
    "frequency": "300",
    "handler": "",
    "host": "",
    "localworkdir": "",
    "modules": "",
    "maxtime": "24:00",
    "memory": "",
    "scripts": "",
    "sge-peflag": "mpi",
    "sge-peoverride": "false",
    "port": "22",
    "queue": "",
    "remoteworkdir": "",
    "resource": "",
    "replicates": "1",
    "scheduler": "",
    "user": "",
    "upload-exclude": "",
    "upload-include": ""
}

REQUIRED = {
    "executable": "An executable has not been specified on the command-line "
                  "or in a configuration file.",
    "executableargs": "Command-line arguments could not be detected properly "
                      "on the command-line or in a configuration file. If "
                      "your application requires input of the form "
                      "'executable < input_file' then make sure that you put "
                      "the '<' in quotation marks.",
    "host": "The parameter 'host' has not been set in your configuration "
            "file, the most natural place is to set this in your hosts.conf, "
            "the path is normally what you would supply to SSH (the part "
            "after the '@').",
    "user": "The parameter 'user' has not been set in your configuration "
            "file, the most natural place is to set this in your hosts.conf, "
            "the user is the same as what you would normally supply to SSH "
            "(the part before the '@').",
    "remoteworkdir": "The parameter 'remoteworkdir' has not been set in your "
                     "configuration file, the most natural place to set this "
                     "is in the host.conf if your working directory never "
                     "changes, or in the job.conf if you are changing this on "
                     "a per job basis.",
    "replicates": "The parameter 'replicates' is required to be set, this "
                  "parameter has an internal default for when not specified "
                  "so something may have gone wrong when specifying a value "
                  "for it in the configuration file."
}


def processconfigs(parameters):

    """
    Method for processing the raw configuration structures loaded from the
    configuration files into Longbow friendly configuration structures.
    This is where the parameter hierarchy is applied.

    Required arguments are:

    parameters (dictionary): This parameter is required. It is used to provide
                             overrides from the application command-line.

    Return parameters are:

    jobs (dictionary) A fully processed Longbow jobs data structure.
    """

    # Define our main data structure.
    jobs = {}

    # Define a dictionary of module defaults based on the plug-in names and
    # executables.
    modules = getattr(apps, "PLUGINEXECS")
    modules[""] = ""

    # Try and load the host file.
    try:

        _, hostsections, hostdata = loadconfigs(parameters["hosts"])

    except exceptions.ConfigurationError:

        raise

    # If we have been given a job file then try and load it.
    if parameters["job"] is not "":

        try:

            _, _, jobdata = loadconfigs(parameters["job"])

        except exceptions.ConfigurationError:

            raise

    # If there is no file then the job structure will be built up from things
    # we know. In this case we would only ever have 1 job.
    else:

        jobdata = {}

        # Did the user supply a jobname on the command line, if not default
        # it.
        if parameters["jobname"] is not "":

            jobname = parameters["jobname"]

        else:

            jobname = "LongbowJob"

        # There will only be one job so create an job structure from the
        # template.
        jobdata[jobname] = JOBTEMPLATE.copy()

        # It is important that this one is empty so not to accidentally
        # interfere with prioritisation in the next step (saves on duplicating
        # data structures just to have one empty and one with default values).
        for item in jobdata[jobname]:

            jobdata[jobname][item] = ""

    # Process the basic job configuration.
    for job in jobdata:

        # Create a base job structure along with known defaults.
        jobs[job] = JOBTEMPLATE.copy()

        # Before we go further lets check that the job has been assigned a
        # host. This is important for copying the correct information from the
        # hosts.conf.

        # If user has not indicated which resource to use or didn't use a
        # job.conf then check other sources.
        try:

            if jobdata[job]["resource"] is "":

                # Since at this point we only have command-line as higher
                # priority.
                if parameters["resource"] is not "":

                    jobs[job]["resource"] = parameters["resource"]

                # Otherwise lets try and use the top host in the list from
                # host.conf. This should never be an empty list since the
                # parser would provide an error on load.
                else:

                    jobs[job]["resource"] = hostsections[0]

            # Just copy it over.
            else:

                jobs[job]["resource"] = jobdata[job]["resource"]

        except KeyError:

            jobs[job]["resource"] = hostsections[0]

        # Validate that we have this host listed.
        if jobs[job]["resource"] not in hostsections:

            # If not tell the user.
            raise exceptions.CommandlineargsError(
                "The resource '{0}' that was given in the job config file "
                "has not been configured in the host.conf. The hosts "
                "available are '{1}'"
                .format(jobs[job]["resource"], hostsections))

        # Now we can go ahead and process the all the parameters and apply
        # priority ordering.
        for item in jobs[job]:

            # We don't need to include this as we have just dealt with it.
            if item is not "resource":

                # Command-line overrides are highest priority.
                if item in parameters and parameters[item] is not "":

                    # Store it.
                    jobs[job][item] = parameters[item]

                # Job file is next highest in priority.
                elif item in jobdata[job] and jobdata[job][item] is not "":

                    # Store it.
                    jobs[job][item] = jobdata[job][item]

                # Hosts file is next highest in priority.
                elif item in hostdata[jobs[job]["resource"]] and \
                        hostdata[jobs[job]["resource"]][item] is not "":

                    # Store it.
                    jobs[job][item] = hostdata[jobs[job]["resource"]][item]

    # Check parameters that are required for running jobs are provided.
    # Here we will only do validation on hosts that are referenced in jobs,
    # this should cut down on annoyances to the user.
    for job in jobs:

        # Validate required parameters have been set.
        for validationitem in REQUIRED:

            # If no value has been set.
            if jobs[job][validationitem] is "":

                # Throw an exception.
                raise exceptions.ConfigurationError(REQUIRED[validationitem])

    # Some final initialisation.
    for job in jobs:

        # This is just for logging messages.
        jobs[job]["jobname"] = job

        # If the local working directory has not been set, then default to cwd
        if jobs[job]["localworkdir"] is "":

            jobs[job]["localworkdir"] = os.getcwd()

        # Fix for python 3 where basestring is now str.
        try:

            # If the exec arguments are in string form, split to list.
            if isinstance(jobs[job]["executableargs"], basestring):

                jobs[job]["executableargs"] = (
                    jobs[job]["executableargs"].split())

        except NameError:

            # If the exec arguments are in string form, split to list.
            if isinstance(jobs[job]["executableargs"], str):

                jobs[job]["executableargs"] = (
                    jobs[job]["executableargs"].split())

        # If modules hasn't been set then try and use a default.
        if jobs[job]["modules"] is "":

            jobs[job]["modules"] = modules[jobs[job]["executable"]]

        # Give each job a unique remote base path by adding a random hash to
        # jobname.
        destdir = job + ''.join(["%s" % randint(0, 9) for _ in range(0, 5)])

        jobs[job]["destdir"] = os.path.join(jobs[job]["remoteworkdir"],
                                            destdir)

        LOG.debug("Job '%s' will be run in the '%s' directory on the remote "
                  "resource.", job, jobs[job]["destdir"])

    return jobs


def loadconfigs(configfile):

    """
    Method to load an ini file. Files of this format contain the following
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
                         file.

    Return parameters are:

    contents (list): This is the raw file structure where each line is an item
                     in the list.

    sections (list): This is a list of section headers in the data (preserves
                     order).

    data (dict of dicts): This is a structure containing the data loaded from
                          the file, a dictionary is created for each heading in
                          the ini file. Then the parameters and values under
                          each heading will form a dictionary within the
                          corresponding heading section (dictionary of
                          dictionaries).
    """

    LOG.info("Loading configuration information from file '%s'", configfile)

    sections = []
    params = {}

    # Open configuration file.
    try:

        tmp = open(configfile, "r")

        # Grab all of the information from the file.
        contents = tmp.readlines()

    except IOError:

        raise exceptions.ConfigurationError(
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

                    # Option is in the format key = param. Added regular
                    # expression so that if user writes with/without spaces
                    # then we can still extract the configuration info.
                    key, value = re.split(" = |= | =|=", item)

                    # Store the keys and values in the data structure.
                    params[section][key] = value

            except NameError:

                # Issue warning.
                pass

    # Check if there are zero sections.
    if len(sections) is 0:

        raise exceptions.ConfigurationError(
            "Error no sections are defined in configuration file '{0}'"
            .format(configfile))

    # Check for sections with zero options.
    for section in sections:

        if len(params[section]) is 0:

            raise exceptions.ConfigurationError(
                "Error section '{0}' contains no parameter definitions using "
                "configuration file '{1}'".format(section, configfile))

    return contents, sections, params


def saveconfigs(configfile, params):

    """
    Method for saving to an ini file. Files of this format contain the
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
                         file.

    params (dictionary): This should contain the data structure that should
                         be saved (typically hosts or job configs structure).
    """

    LOG.info("Saving configuration information to file '%s'", configfile)

    keydiff = {}
    valuediff = {}

    # Load up the original file including comment structure (list).
    try:

        contents, _, oldparams = loadconfigs(configfile)

    except exceptions.ConfigurationError:

        contents = []
        oldparams = {}

    # Run through each section in the data.
    for section in params:

        # Run through each parameter in this section.
        for option in params[section]:

            if params[section][option] != "":

                try:

                    # Check for continuity between data in file and that in
                    # Longbow.
                    if params[section][option] != oldparams[section][option]:

                        try:

                            # If parameter is changed try adding it to the diff
                            valuediff[section][option] = \
                                params[section][option]

                        except KeyError:

                            # If this is the first time then section won't
                            # exist.
                            valuediff[section] = \
                                {option: params[section][option]}

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
                    str(option) + " = " + str(oldparams[section][option])))

            # Edit the entry.
            contents[editposition] = (
                str(option) + " = " + str(valuediff[section][option]))

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
                    sectionendindex,
                    str(option) + " = " + str(keydiff[section][option]))

        # Doesn't exist so it is a new section.
        except ValueError:

            # Append the section.
            contents.extend(["", "[" + section + "]"])

            # Now run through each option.
            for option in keydiff[section]:

                # And append it to the end of the list.
                contents.append(
                    str(option) + " = " + str(keydiff[section][option]))

    try:

        # Open file for writing.
        tmp = open(configfile, "w")

        # Write it all out.
        for item in contents:
            tmp.write(item + "\n")

        # Close file.
        tmp.close()

    except IOError:

        raise exceptions.ConfigurationError(
            "Error saving to '{0}'".format(configfile))


def saveini(inifile, params):

    """
    Method for saving to a Longbow recovery file. This method will write
    to an inifile.

    Required arguments are:

    configfile (string): This should be an absolute path to a revovery file.

    params (dictionary): This should contain the data structure that should
                         be saved (typically hosts or jobs structure).
    """

    LOG.info("Saving current state to recovery file '%s'", inifile)

    ini = open(inifile, "w")

    for section in params:

        ini.write("[" + str(section) + "]\n")

        for option in params[section]:

            ini.write(str(option) + " = " + str(params[section][option]) +
                      "\n")

        ini.write("\n")

    ini.close()
