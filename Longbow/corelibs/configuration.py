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

"""This module contains methods for loading and saving configuration
files as well as methods for processing host and job configuration files.
The following methods can be found:

loadhosts()
    Method containing the structure template for host configuration files.
loadjobs()
    Method containing the structure template for job configuration files.
loaddefaultjobconfigs()
    Method containing the structure template for the default job configuration
loadconfigs()
    Method containing the code for parsing configuration files.
saveconfigs()
    Method containing the code for saving configuration files."""

import ConfigParser as configparser
import logging
import corelibs.exceptions as ex

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
        "commandline": "",
        "frequency": "",
        "localworkdir": "",
        "modules": "",
        "maxtime": "",
        "memory": "",
        "nodes": "",
        "executable": "",
        "queue": "",
        "batch": "",
        "remoteworkdir": ""
    }

    required = [
        "host",
        "user",
        "remoteworkdir"
    ]

    hosts = loadconfigs(confile, hosttemplate, required)

    return hosts


def loadjobs(jobconfile, hostsconfile, remoteres):

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
        "commandline": "",
        "frequency": "",
        "localworkdir": "",
        "modules": "",
        "maxtime": "",
        "memory": "",
        "nodes": "",
        "executable": "",
        "queue": "",
        "batch": "",
        "remoteworkdir": "",
        "resource": ""
    }

    jobs = {}

    # if a job configuration file has been provided, load it
    if jobconfile is not "":
        jobs = loadconfigs(jobconfile, jobtemplate, "")

    # else load an empty dictionary
    else:
        jobs["Longbowjob"] = jobtemplate.copy()

    # determine which remote resource to use if none has been set
    for job in jobs:
        if jobs[job]["resource"] is "":

            # Instantiate the configparser and read the configuration file.
            configs = configparser.ConfigParser()

            try:
                configs.read(hostsconfile)

            except IOError:
                ex.RequiredinputError("Can't read the configurations from: %s"
                                      % hostsconfile)

            # Grab a list of the section headers present in file.
            sectionlist = configs.sections()

            # if the machine flag has not been set use the first machine in the
            # hosts
            if remoteres is "":
                jobs[job]["resource"] = sectionlist[0]

            elif remoteres not in sectionlist:
                raise ex.CommandlineargsError("The %s machine specified on the"
                    " command line is not one of: %s"
                    % (remoteres, sectionlist))
            else:
                jobs[job]["resource"] = remoteres

    return jobs


def sortconfigs(hosts, jobs, executable, cwd, args):

    """Method to sort and prioritise configuration parameters."""

    # Dictionary to map executable to a default module
    modules = {
        "charmm": "charmm",
        "pmemd": "amber",
        "pmemd.MPI": "amber",
        "lmp_xc30": "lammps",
        "namd2": "namd",
        "mdrun": "gromacs",
        "": ""
    }

    # Parameters to be stored in the hosts structure excluding user and host
    hosttemplate = {
        "corespernode": "24",
        "cores": "24",
        "port": "22",
        "scheduler": "",
        "handler": "",
        "accountflag": "",
        "account": "",
        "remoteworkdir": ""
    }

    # Parameters to be stored in the jobs structure excluding resource
    jobtemplate = {
        "cluster": "",
        "commandline": args,
        "frequency": "60",
        "localworkdir": cwd,
        "modules": modules[executable],
        "maxtime": "24:00",
        "memory": "",
        "nodes": "",
        "executable": executable,
        "queue": "",
        "batch": "1",
    }

    for job in jobs:

        # hosts
        for option in hosttemplate:

            # Job configuration parameters always take priority
            if jobs[job][option] is not "":
                hosts[jobs[job]["resource"]][option] = jobs[job][option]

            # if parameter has not been defined in hosts or jobs use default
            elif hosts[jobs[job]["resource"]][option] is "":
                hosts[jobs[job]["resource"]][option] = hosttemplate[option]

            # Clean up
            del jobs[job][option]

        # jobs
        for option in jobtemplate:
            if jobs[job][option] is "":

                # if a parameter hasn't been defined in jobs but has been in
                # hosts, use it
                if hosts[jobs[job]["resource"]][option] is not "":
                    jobs[job][option] = hosts[jobs[job]["resource"]][option]

                # if parameter has not been defined in hosts or jobs use
                # default
                else:
                    jobs[job][option] = jobtemplate[option]

            # Clean up
            del hosts[jobs[job]["resource"]][option]

        # Check we have an executable and command line arguments provided
        if jobs[job]["executable"] is "":
            raise ex.CommandlineargsError(
                "An executable has not been specified on the command line "
                "or in a configuration file")

        if jobs[job]["commandline"] is "":
            raise ex.CommandlineargsError(
                "Command line arguments have not been specified on the "
                "command line or in a configuration file")


def loadconfigs(confile, template, required):

    """Method to load configurations from file."""

    LOGGER.info("Loading configuration information from file '%s'", confile)

    # Instantiate the configparser and read the configuration file.
    configs = configparser.ConfigParser()

    try:
        configs.read(confile)

    except IOError:
        raise ex.ConfigurationError(
            "Can't read the configurations from '%s'" % confile)

    # Grab a list of the section headers present in file.
    sectionlist = configs.sections()
    sectioncount = len(sectionlist)

    # If we don't have any sections then raise an exception.
    if sectioncount is 0:
        raise ex.ConfigurationError(
            "In file '%s' " % confile + "no sections can be detected or the "
            "file is not in ini format.")

    # Temporary dictionary for storing the configurations in.
    params = {}
    for section in sectionlist:
        params[section] = template.copy()

        # Grab the option count from the section.
        optioncount = len(configs.options(section))

        # If we have no options then raise an exception.
        if optioncount is 0:
            raise ex.ConfigurationError(
                "There are no parameters listed under the section '%s'" %
                section)

        # Store option values in our dictionary structure.
        for option in template:
            try:
                params[section][option] = configs.get(section, option)

            except configparser.NoOptionError:
                if option in required:
                    raise ex.ConfigurationError(
                        "The parameter %s is required" % option)

                else:
                    pass

    return params


def saveconfigs(confile, params):

    """Method to save parameters to file."""

    LOGGER.info("Saving configuration information to file '%s'", confile)

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
