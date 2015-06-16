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

import ConfigParser as configparser
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

    # Dictionary for the host configuration parameters.
    # Contains "user" and "host" but no "resource" unlike the jobs equivalent
    hosttemplate = {
        "user": "",
        "host": "",
        "corespernode": "",
        "cores": "",
        "port": "",
        "scheduler": "",
        "handler": "",
        "accountflag": "",
        "account": "",
        "cluster": "",
        "executableargs": "",
        "frequency": "",
        "localworkdir": "",
        "modules": "",
        "maxtime": "",
        "memory": "",
        "executable": "",
        "queue": "",
        "replicates": "",
        "remoteworkdir": "",
        "download-include": "",
        "download-exclude": "",
        "upload-include": "",
        "upload-exclude": ""
    }

    # List of parameters that MUST be provided in the hosts configuration file
    required = [
        "host",
        "user",
        "remoteworkdir"
    ]

    hosts = loadconfigs(confile, hosttemplate, required)

    return hosts


def loadjobs(jobconfile, hostsconfile, param):

    """Method for processing job configuration files."""

    # Dictionary for the job configurations parameters.
    # Contains "resource" but no "user" or "host" unlike the hosts equivalent
    jobtemplate = {
        "corespernode": "",
        "cores": "",
        "port": "",
        "scheduler": "",
        "handler": "",
        "accountflag": "",
        "account": "",
        "cluster": "",
        "executableargs": "",
        "frequency": "",
        "localworkdir": "",
        "modules": "",
        "maxtime": "",
        "memory": "",
        "executable": "",
        "queue": "",
        "replicates": "",
        "remoteworkdir": "",
        "resource": "",
        "download-include": "",
        "download-exclude": "",
        "upload-include": "",
        "upload-exclude": ""
    }

    # List of parameters that MUST be provided in the job configuration file
    required = [
        ""
    ]

    resource = param["resource"]
    jobname = param["jobname"]

    jobs = {}

    # if a job configuration file has been provided, load it
    if jobconfile is not "":

        jobs = loadconfigs(jobconfile, jobtemplate, required)

    # else load an empty dictionary, use jobname provided on command line if
    # specified
    else:

        jobs[jobname if jobname else "Longbowjob"] = jobtemplate.copy()

    # For each job, determine which remote resource to use

    # Read the section headers present in the hosts configuration file.
    # This will be needed later.
    configs = configparser.ConfigParser()

    try:

        configs.read(hostsconfile)

    except IOError:

        EX.RequiredinputError("Can't read the configurations from '{}'"
                              .format(hostsconfile))

    sectionlist = configs.sections()

    for job in jobs:

        # if a resource has been specified on the command line overrule
        if resource is not "":

            # Check the machine specified on the command line is in the hosts
            # config file. If it is, use it.
            if resource in sectionlist:

                jobs[job]["resource"] = resource

            else:

                raise EX.CommandlineargsError(
                    "The '{}' resource specified on the command line is not"
                    " one of: '{}'" .format(resource, sectionlist))

        # elif a resource has not been specified in a job config, use the top
        # machine in the hosts config
        elif jobs[job]["resource"] is "":

            try:

                hostsfile = open(hostsconfile, "r")

            except IOError:

                EX.RequiredinputError("Can't read the configurations from '{}'"
                                      .format(hostsconfile))

            topremoteres = []

            for line in hostsfile:

                if line[0] == "[":

                    i = 1

                    while line[i] is not "]":

                        topremoteres.append(line[i])
                        i += 1

                    break

            topremoteres = "".join(topremoteres)
            jobs[job]["resource"] = topremoteres
            hostsfile.close()

        elif jobs[job]["resource"] not in sectionlist:

            raise EX.RequiredinputError(
                "The '{}' resource specified in the job configuration"
                " file is not one of '{}'"
                .format(jobs[job]["resource"], sectionlist))

    return jobs


def sortjobsconfigs(hostsconfig, jobsconfig, executable, cwd, args,
                    replicates):

    """Method to sort and prioritise job configuration parameters."""

    # Blank parameters for the jobs structure
    jobtemplate = {
        "cores": "",
        "cluster": "",
        "executableargs": "",
        "frequency": "",
        "localworkdir": "",
        "modules": "",
        "maxtime": "",
        "memory": "",
        "executable": "",
        "queue": "",
        "replicates": "",
        "resource": "",
        "download-include": "",
        "download-exclude": "",
        "upload-include": "",
        "upload-exclude": ""
    }

    # Parameters to be copied manually from jobsconfig to jobs
    manual = [
        "resource"
    ]

    # Parameters to be that can be provided on the command line that can
    # overrule parameters in config files
    command = [
        "executableargs",
        "executable",
        "replicates"
    ]

    # Default parameters to be stored in the jobs structure
    jobdefaults = {
        "cores": "24",
        "cluster": "",
        "executableargs": args if len(args) > 0 else "",
        "frequency": "60",
        "localworkdir": cwd,
        "modules": "",
        "maxtime": "24:00",
        "memory": "",
        "executable": executable,
        "queue": "",
        "replicates": replicates,
        "resource": "",
        "download-include": "",
        "download-exclude": "",
        "upload-include": "",
        "upload-exclude": ""
    }

    jobs = {}

    # create jobs internal structure
    for job in jobsconfig:

        jobs[job] = jobtemplate.copy()

    # prioritise parameters
    for job in jobs:

        for option in jobdefaults:

            # manually copy certain values from the jobs config from loadjobs()
            if option in manual:

                jobs[job][option] = jobsconfig[job][option]

            # certain values provided on the command line should take priority
            elif option in command and jobdefaults[option] is not "":

                jobs[job][option] = jobdefaults[option]

            # elif a parameter has been defined in jobsconfig, use it
            elif jobsconfig[job][option] is not "":

                jobs[job][option] = jobsconfig[job][option]

            # if a parameter hasn't been defined in jobsconfig but has been in
            # hostsconfig, use it
            elif hostsconfig[jobsconfig[job]["resource"]][option] is not "":

                jobs[job][option] = \
                    hostsconfig[jobsconfig[job]["resource"]][option]

            # else use default.
            else:

                jobs[job][option] = jobdefaults[option]

    return jobs


def sorthostsconfigs(hostsconfig, jobsconfig):

    """Method to sort and prioritise hosts configuration parameters."""

    # Parameters to be stored in the hosts structure
    hosttemplate = {
        "corespernode": "",
        "port": "",
        "scheduler": "",
        "handler": "",
        "accountflag": "",
        "account": "",
        "remoteworkdir": "",
        "user": "",
        "host": ""
    }

    # Parameters to be copied manually from hostsconfig to hosts
    manual = [
        "host",
        "user"
    ]

    # Default parameters to be stored in the hosts structure excluding user and
    # host
    hostdefaults = {
        "corespernode": "24",
        "port": "22",
        "scheduler": "",
        "handler": "",
        "accountflag": "",
        "account": "",
        "remoteworkdir": ""
    }

    hosts = {}

    # create default hosts internal structure
    for job in jobsconfig:

        hosts[jobsconfig[job]["resource"]] = hosttemplate.copy()

        for item in manual:

            hosts[jobsconfig[job]["resource"]][item] = \
                hostsconfig[jobsconfig[job]["resource"]][item]

    # prioritise parameters
    for job in jobsconfig:

        for option in hostdefaults:

            # Job configuration parameters always take priority
            if jobsconfig[job][option] is not "":

                hosts[jobsconfig[job]["resource"]][option] = \
                    jobsconfig[job][option]

            # else use the hosts parameter if provided
            elif hostsconfig[jobsconfig[job]["resource"]][option] is not "":

                hosts[jobsconfig[job]["resource"]][option] = \
                    hostsconfig[jobsconfig[job]["resource"]][option]

            # if parameter has not been defined in hosts or jobs use default
            else:

                hosts[jobsconfig[job]["resource"]][option] = \
                    hostdefaults[option]

    return hosts


def amendjobsconfigs(hosts, jobs):

    """Method to make final amendments to the job configuration parameters"""

    # Dictionary to map executable to a default module
    modules = getattr(APPS, "DEFMODULES")
    modules[""] = ""

    for job in jobs:

        # Check we have an executable provided
        if jobs[job]["executable"] is "":

            raise EX.CommandlineargsError(
                "An executable has not been specified on the command-line "
                "or in a configuration file")

        # Check we have command line arguments provided
        if jobs[job]["executableargs"] is "":

            raise EX.CommandlineargsError(
                "Command-line arguments could not be detected properly on the "
                "command-line or in a configuration file. If your application "
                "requires input of the form 'executable < input_file' then "
                "make sure that you put the \"<\" in quotation marks.")

        # if the executableargs parameter is a string, we need to split it up into
        # a list of strings
        elif isinstance(jobs[job]["executableargs"], basestring):

            jobs[job]["executableargs"] = jobs[job]["executableargs"].split()

        # If modules hasn't been defined in a config file, use default
        if jobs[job]["modules"] is "":

            jobs[job]["modules"] = modules[jobs[job]["executable"]]

        # If replicates hasn't been defined anywhere, set to "1"
        if jobs[job]["replicates"] is "":

            jobs[job]["replicates"] = "1"

        # Give each job a remote basepath, a random hash will be added to this
        # later.
        jobs[job]["destdir"] = hosts[jobs[job]["resource"]]["remoteworkdir"]


def loadconfigs(confile, template, required):

    """Method to load configurations from file."""

    LOGGER.info("Loading configuration information from file '{}'"
                .format(confile))

    # Instantiate the configparser and read the configuration file.
    configs = configparser.ConfigParser()

    try:

        configs.read(confile)

    except IOError:

        raise EX.ConfigurationError(
            "Can't read the configurations from '{}'" .format(confile))

    # Grab a list of the section headers present in file.
    sectionlist = configs.sections()
    sectioncount = len(sectionlist)

    # If we don't have any sections then raise an exception.
    if sectioncount is 0:

        raise EX.ConfigurationError(
            "In file '{}' no sections can be detected or the file is not in "
            "ini format." .format(confile))

    # Temporary dictionary for storing the configurations in.
    params = {}
    for section in sectionlist:

        params[section] = template.copy()

        # Grab the option count from the section.
        optioncount = len(configs.options(section))

        # If we have no options then raise an exception.
        if optioncount is 0:

            raise EX.ConfigurationError(
                "There are no parameters listed under the section '{}'"
                .format(section))

        # Store option values in our dictionary structure.
        for option in template:

            try:

                params[section][option] = configs.get(section, option)

            except configparser.NoOptionError:

                if option in required:

                    raise EX.ConfigurationError(
                        "The parameter '{}' is required" .format(option))

                else:

                    pass

    return params


def saveconfigs(confile, params):

    """Method to save parameters to file."""

    LOGGER.info("Saving configuration information to file '{}'"
                .format(confile))

    # Bind the hosts file to the config parser and read it in.
    configs = configparser.ConfigParser()
    configs.read(confile)

    for section in params:

        for option in params[section]:

            if params[section][option] is not "":

                # Append the new option and value to the configuration.
                configs.set(section, option, params[section][option])

    # Save it.
    with open(confile, 'w') as conf:

        configs.write(conf)
