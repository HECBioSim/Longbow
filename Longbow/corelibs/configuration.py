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

"""
This module contains methods for loading and saving to Longbow (ini)
configuration files in addition to methods for extracting the resultant
information into Longbow data structures. The templates for these data
structures and their forms are also declared within this module.

The following data structures can be found:

HOSTTEMPLATE
    The template of the hosts data structure. The Longbow API will assume
    that variables listed here are to be found in this structure.

HOSTREQUIRED
    A dictionary to mark parameters that are required to be initialised during
    configuration and their error messages for cases when missing.

JOBTEMPLATE
    The template of the job data structure. The Longbow API will assume
    that variables listed here are to be found in this structure.

JOBREQUIRED
    A dictionary to mark parameters that are required to be initialised during
    configuration and their error messages for cases when missing.

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
    honour comments and simply amend the file structure with new or changed
    data.
"""

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
    "account": "",
    "accountflag": "",
    "corespernode": "24",
    "handler": "",
    "host": "",
    "port": "22",
    "remoteworkdir": "",
    "scheduler": "",
    "user": ""
}

HOSTREQUIRED = {
    "host": "The parameter 'hosts' has not been set in your configuration "
            "file, the most natural place is to set this in your hosts.conf, "
            "the path is normally what you would supply to SSH (the part "
            "after the '@').",
    "user": "The paramter 'users' has not been set in your configuration "
            "file, the most natural place is to set this in your hosts.conf, "
            "the user is the same as what you would normally supply to SSH "
            "(the part before the '@').",
    "remoteworkdir": "The parameter 'remoteworkdir' has not been set in your "
                     "configuration file, the most natural place to set this "
                     "is in the host.conf if your working directory never "
                     "changes, or in the job.conf if you are changing this on "
                     "a per job basis."
}

JOBTEMPLATE = {
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

JOBREQUIRED = {
    "executableargs": "Command-line arguments could not be detected properly "
                      "on the command-line or in a configuration file. If "
                      "your application requires input of the form "
                      "'executable < input_file' then make sure that you put "
                      "the '<' in quotation marks.",
    "executable": "An executable has not been specified on the command-line "
                  "or in a configuration file.",
    "replicates": "The parameter 'replicates' is required to be set, this "
                  "parameter has an internal default for when not specified "
                  "so something may have gone wrong when specifying a value "
                  "for it in the configuration file."
}


def processconfigs(hostfile, jobfile, cwd, params):

    """
    Method for processing the raw configuration structures loaded from the
    configuration files into Longbow friendly configuration structures.
    This is where the parameter hierarchy is applied.

    Required arguments are:

    hostfile (string): This should be an absolute path to a configuration
                       file, this parameter is required.

    jobfile (string): This should be an absolute path to a configuration
                      file, this parameter is optional (empty string if not
                      needed).

    args (string): This should be an absolute path to a configuration
                       file, this parameter is required.

    cwd (string): This should be an absolute path to a configuration
                       file, this parameter is required.

    executable (string): This should be an absolute path to a configuration
                       file, this parameter is required.

    params (dictionary): This should be an absolute path to a configuration
                       file, this parameter is required.

    Return parameters are:

    hosts (dictionary): A fully processed Longbow hosts data structure.

    jobs (dictionary) A fully processed Longbow jobs data structure.
    """

    # Define our main data structures.
    hosts = {}
    jobs = {}

    # Define a dictionary of module defaults based on the plug-in names and
    # executables.
    modules = getattr(APPS, "DEFMODULES")
    modules[""] = ""

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

    # If there is no file then the job structure will be built up from things
    # we know from the hosts, the command line and defaults. In this case we
    # would only ever have 1 job.
    else:

        jobdata = {}

        # Did the user supply a jobname on the command line, if not default it.
        if params["jobname"] is not "":

            jobname = params["jobname"]

        else:
            jobname = "LongbowJob"

        jobdata[jobname] = JOBTEMPLATE.copy()

        # It is important that this one is empty so not to accidentally
        # interfere with prioritisation in the next step (saves on duplicating
        # data structures just to have one empty and one with default values).
        for item in jobdata[jobname]:

            jobdata[jobname][item] = ""

    # Process the basic host configuration
    for host in hostdata:

        # Create a base host structure along with known defaults.
        hosts[host] = HOSTTEMPLATE.copy()

        # At this stage just grab all parameters that belong in the hosts.
        for item in hosts[host]:

            # We don't want to overwrite internal defaults.
            try:

                if hostdata[host][item] is not "":

                    hosts[host][item] = hostdata[host][item]

            except KeyError:

                pass

    # Process the basic job configuration.
    for job in jobdata:

        # Create a base job structure along with known defaults.
        jobs[job] = JOBTEMPLATE.copy()

        for item in jobs[job]:

            # At this stage just grab all parameters that belong in the jobs,
            # which are not empty to avoid overwriting defaults.
            try:

                if jobdata[job][item] is not "":

                    jobs[job][item] = jobdata[job][item]

            except KeyError:

                pass

    # Now process some overrides, the basic order of precedence is;
    # Command line > job config file > host config file > internal defaults.

    # Before we go further lets check that the job/s have been assigned a host.
    # This is important for checking for values provided for jobs in the host
    # conf.
    for job in jobs:

        # If not then can we find one to use?
        if jobs[job]["resource"] is "":

            # First check the params from the command line.
            if params["resource"] is not "":

                # If this host has been set up then use it.
                if params["resource"] in hostsections:

                    jobs[job]["resource"] = params["resource"]

                # Otherwise we have a problem, so tell the user.
                else:

                    raise EX.CommandlineargsError(
                        "The resource '{0}' that was given on the command line"
                        " has not been configured in the host.conf. The hosts "
                        "available are '{0}'".format(
                            params["resource"], hostsections))

            # Otherwise lets try and use the top host in the list from
            # host.conf. This should never be an empty list since the
            # parser would provide an error on load.
            else:

                jobs[job]["resource"] = hostsections[0]

        # Otherwise run some validation.
        else:

            # Does the host exist?
            if jobs[job]["resource"] not in hostsections:

                # If not tell the user.
                raise EX.CommandlineargsError(
                    "The resource '{0}' that was given in the job config file"
                    " has not been configured in the host.conf. The hosts "
                    "available are '{0}'".format(
                        params["resource"], hostsections))

    # Now we can go ahead and process the overrides. For this it is probably
    # best to use the jobs data as the main source, this way we will only deal
    # with hosts that are being used.
    for job in jobs:

        resource = jobs[job]["resource"]

        # Host overrides first.

        # For the host that is provided for this job, is there anything that is
        # overriding in the job configuration file?
        for item in jobdata[job]:

            # We can check this like this.
            if item in hosts[resource] and jobdata[job][item] is not "":

                # Then override.
                hosts[resource][item] = jobdata[job][item]

        # For the host that is provided in this job, is there anything that is
        # overriding on the command line?
        for item in params:

            # We can check this like this.
            if item in hosts[resource] and params[item] is not "":

                # Then override.
                hosts[resource][item] = params[item]

        # Job overrides next.

        # Now the overrides from the hosts.conf are of lower priority than
        # those on the command line or any data that was supplied in the
        # job.conf but higher than any internal defaults.
        for item in hostdata[resource]:

            # We have already handled this.
            if item is not "resource":

                # Does the item match anything in the job?
                if item in jobs[job]:

                    # Then we have an override, but check priority first.
                    # Make sure item didn't come from higher priority job.conf?
                    if item not in jobdata[job] or jobdata[job][item] is "":

                        # Override.
                        jobs[job][item] = hostdata[resource][item]

        # For the currently selected job, are there any overrides that have
        # been given on the command line?
        for item in params:

            # We have already handled this.
            if item is not "resource":

                # We can check this like this.
                if item in jobs[job] and params[item] is not "":

                    # Then override.
                    jobs[job][item] = params[item]

    # Check parameters that are required for running jobs are provided.
    # Here we will only do validation on hosts that are referenced in jobs,
    # this should cut down on annoyances to the user.
    for job in jobs:

        resource = jobs[job]["resource"]

        # Validate for host referenced within job.
        for validationitem in HOSTREQUIRED:

            # If no value has been set.
            if hosts[resource][validationitem] is "":

                # Throw an exception.
                raise EX.ConfigurationError(HOSTREQUIRED[validationitem])

        # Validate required parameters have been set.
        for validationitem in JOBREQUIRED:

            # If no value has been set.
            if jobs[job][validationitem] is "":

                # Throw an exception.
                raise EX.ConfigurationError(JOBREQUIRED[validationitem])

    # Some final initialisation.
    for job in jobs:

        # If the local working directory has not been set, then default to cwd
        if jobs[job]["localworkdir"] is "":

            jobs[job]["localworkdir"] = cwd

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

        # Give each job a remote base path, a random hash will be added to this
        # during job processing
        jobs[job]["destdir"] = hosts[jobs[job]["resource"]]["remoteworkdir"]

    return hosts, jobs


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
                         file.

    params (dictionary): This should contain the data structure that should
                         be saved (typically hosts of job configs structure).
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
