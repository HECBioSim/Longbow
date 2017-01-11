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

"""A module  containing methods for dealing with configuration files.

This module contains methods for loading and saving to Longbow (ini)
configuration files in addition to methods for extracting the resultant
information into Longbow data structures. The templates for these data
structures and their forms are also declared within this module.

The following data structures can be found:

JOBTEMPLATE
    The template of the job data structure. The Longbow API will assume
    that variables listed here are to be found in this structure.

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

import Longbow.corelibs.exceptions as exceptions
import Longbow.apps as apps


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
    "handler": "",
    "host": "",
    "localworkdir": "",
    "modules": "",
    "maxtime": "24:00",
    "memory": "",
    "polling-frequency": "300",
    "port": "22",
    "queue": "",
    "remoteworkdir": "",
    "resource": "",
    "replicates": "1",
    "scheduler": "",
    "scripts": "",
    "staging-frequency": "300",
    "sge-peflag": "mpi",
    "sge-peoverride": "false",
    "user": "",
    "upload-exclude": "",
    "upload-include": ""
}


def processconfigs(parameters):
    """A method for processing the raw configuration sources.

    Parameters are loaded from the configuration files and sourced from the
    command-line and processed into Longbow friendly configuration structures.
    This is where the parameter hierarchy is applied.

    Required arguments are:

    parameters (dictionary): This parameter is required. It is used to provide
                             overrides from the application command-line.

    Return parameters are:

    jobs (dictionary) A fully processed Longbow jobs data structure.

    """
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

    # If there is no job file, then attempt to build a job from other sources.
    else:

        jobdata = {}

        if parameters["jobname"] is not "":

            jobname = parameters["jobname"]

        else:

            jobname = "LongbowJob"

        # Create an job structure from the template.
        jobdata[jobname] = JOBTEMPLATE.copy()

        # Empty values so that priority ordering is easier (important!).
        for item in jobdata[jobname]:

            jobdata[jobname][item] = ""

    jobs = _processconfigsresource(parameters, jobdata, hostsections)

    _processconfigsparams(jobs, parameters, jobdata, hostdata)

    _processconfigsvalidate(jobs)

    _processconfigsfinalinit(jobs)

    return jobs


def loadconfigs(configfile):
    """A method to load a Longbow configuration file.

    Files of this format contain the following mark-up structure.

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

        # Find section markers
        if len(item) > 0 and item[0] == "[" and item[len(item) - 1] == "]":

            # Remove the square bracket section markers.
            section = "".join(a for a in item if a not in "[]")

            # Add to list of sections.
            sections.append(section)

            # Create a new section in the data structure.
            params[section] = {}

        # Find comment markers.
        elif len(item) > 0 and item[0] is "#":

            # Ignore comments.
            pass

        # Anything else must be option data.
        elif len(item) > 0 and "=" in item:

            # Option is in the format key = param. Added regular expression so
            # that if user writes with/without spaces then we can still extract
            # the configuration info.
            key, value = re.split(" = |= | =|=", item)

            # Store the keys and values in the data structure.
            params[section][key] = value

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
    """A method for saving to a Longbow configuration file.

    Files of this format contain the following mark-up structure.

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

    # Calculate the diffs.
    _saveconfigdiffs(params, oldparams, keydiff, valuediff)

    # Update the file metastructure. Firstly handle the updates.
    _saveconfigupdates(contents, oldparams, valuediff)

    # Now handle new entries. Run through each section.
    _saveconfignew(contents, keydiff)

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
    """A method for saving to a Longbow recovery file.

    This method will write a simple ini formatted file.

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


def _processconfigsfinalinit(jobs):
    """A private method to perform some last bits of initialisation."""
    # Initialisation.
    modules = getattr(apps, "PLUGINEXECS")
    modules[""] = ""

    for job in jobs:

        # This is just for logging messages.
        jobs[job]["jobname"] = job

        # If the local working directory has not been set, then default to cwd
        if jobs[job]["localworkdir"] is "":

            jobs[job]["localworkdir"] = os.getcwd()

        jobs[job]["executableargs"] = jobs[job]["executableargs"].split()

        # If modules hasn't been set then try and use a default.
        if jobs[job]["modules"] is "":

            jobs[job]["modules"] = modules[jobs[job]["executable"]]

        # Give each job a unique base path by adding a random hash to jobname.
        destdir = job + ''.join(["%s" % randint(0, 9) for _ in range(0, 5)])

        jobs[job]["destdir"] = os.path.join(jobs[job]["remoteworkdir"],
                                            destdir)

        LOG.debug("Job '%s' will be run in the '%s' directory on the remote "
                  "resource.", job, jobs[job]["destdir"])


def _processconfigsparams(jobs, parameters, jobdata, hostdata):
    """A private method to assimilate all parameters into jobs dict."""
    # Process the parameters and apply priority ordering.
    for job in jobs:

        for item in jobs[job]:

            # This should already be dealt with.
            if item != "resource":

                # Command-line overrides are highest priority.
                if item in parameters and parameters[item] is not "":

                    jobs[job][item] = parameters[item]

                # Job file is next highest in priority.
                elif item in jobdata[job] and jobdata[job][item] is not "":

                    jobs[job][item] = jobdata[job][item]

                # Hosts file is next highest in priority.
                elif item in hostdata[jobs[job]["resource"]] and \
                        hostdata[jobs[job]["resource"]][item] is not "":

                    jobs[job][item] = hostdata[jobs[job]["resource"]][item]


def _processconfigsresource(parameters, jobdata, hostsections):
    """A private method to figure out which HPC each job should use."""
    # Initialise.
    jobs = {}

    # Process resource/s for job/s.
    for job in jobdata:

        # Create a base job structure along with known defaults.
        jobs[job] = JOBTEMPLATE.copy()

        # Before we go further, check that the job has been assigned a host.
        try:

            if jobdata[job]["resource"] is "":

                # Has a host been named on the command-line?
                if parameters["resource"] is not "":

                    jobs[job]["resource"] = parameters["resource"]

                # Otherwise lets try and use the top host from host.conf.
                else:

                    jobs[job]["resource"] = hostsections[0]

            # It should be given the job conf.
            else:

                jobs[job]["resource"] = jobdata[job]["resource"]

        except KeyError:

            jobs[job]["resource"] = hostsections[0]

        # Validate that we have this host listed.
        if jobs[job]["resource"] not in hostsections:

            raise exceptions.ConfigurationError(
                "The resource '{0}' that was given in the job config file "
                "has not been configured in the host.conf. The hosts "
                "available are '{1}'"
                .format(jobs[job]["resource"], hostsections))

    return jobs


def _processconfigsvalidate(jobs):
    """A private method to perform validation."""
    # Initialise required messages for flags.
    required = {
        "executable": "An executable has not been specified on the "
                      "command-line or in a configuration file.",
        "executableargs": "Command-line arguments could not be detected "
                          "properly on the command-line or in a configuration "
                          "file. If your application requires input of the"
                          "form 'executable < input_file' then make sure that "
                          "you put the '<' in quotation marks.",
        "host": "The parameter 'host' has not been set in your configuration "
                "file, the most natural place is to set this in your "
                "hosts.conf, the path is normally what you would supply to "
                "SSH (the part after the '@').",
        "user": "The parameter 'user' has not been set in your configuration "
                "file, the most natural place is to set this in your "
                "hosts.conf, the user is the same as what you would normally "
                "supply to SSH (the part before the '@').",
        "remoteworkdir": "The parameter 'remoteworkdir' has not been set in "
                         "your configuration file, the most natural place to "
                         "set this is in the host.conf if your working "
                         "directory never changes, or in the job.conf if you "
                         "are changing this on a per job basis.",
        "replicates": "The parameter 'replicates' is required to be set, this "
                      "parameter has an internal default for when not "
                      "specified so something may have gone wrong when "
                      "specifying a value for it in the configuration file."
    }
    # Check parameters that are required for running jobs are provided.
    for job in jobs:

        # Validate required parameters have been set.
        for validationitem in required:

            if jobs[job][validationitem] is "":

                raise exceptions.ConfigurationError(required[validationitem])


def _saveconfigdiffs(params, oldparams, kdiff, vdiff):
    """A private method to calculate configuration data diffs.

    This method is a private method used by the saveconfigs method to calculate
    diffs between data held in the application and data held in configuration
    files. These diffs are then used to apply changes to existing configuration
    files during saving.

    """
    # Run through each section in the data.
    for section in params:

        # Run through each parameter in this section.
        for option in params[section]:

            try:

                # Check continuity between data in file and Longbow.
                if (params[section][option] != "" and
                        params[section][option] != oldparams[section][option]):

                    try:

                        # If parameter is changed try adding it to the diff
                        vdiff[section][option] = params[section][option]

                    except KeyError:

                        # Missing section.
                        vdiff[section] = {option: params[section][option]}

            # If we get a key error then the paramater is a new one.
            except KeyError:

                try:

                    # Try adding to diff
                    kdiff[section][option] = params[section][option]

                except KeyError:

                    # Missing section.
                    kdiff[section] = {option: params[section][option]}


def _saveconfigupdates(contents, oldparams, valuediff):
    """A private method to update the file metastructure for existing params.

    This method is a private method used by the saveconfigs method to update
    parameters that already exist in the configuration file, with the new
    values if they have changed.

    """
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

            for item in [" = ", " =", "= ", "="]:

                try:

                    # Get the line index to edit.
                    editposition = (
                        sectionstartindex +
                        contents[sectionstartindex:sectionendindex].index(
                            str(option) + item +
                            str(oldparams[section][option])))

                    break

                except ValueError:

                    pass

            # Edit the entry.
            contents[editposition] = (
                str(option) + " = " + str(valuediff[section][option]))


def _saveconfignew(contents, keydiff):
    """A private method to calculate configuration data diffs.

    This method is a private method used by the saveconfigs method to add new
    parameters to the configuration file, if they have been created.

    """
    for section in keydiff:

        try:
            # Find the section start.
            sectionstartindex = contents.index("[" + section + "]")

            # Find the section end.
            try:
                sectionendindex = contents.index(
                    [a for a in contents if "[" and "]" in a and
                     contents.index(a) > sectionstartindex][0])

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
