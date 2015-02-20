# Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B Shannon 2015.
#
# This file is part of Longbow.
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

"""This module contains methods for loading and saving confinguration
files as well as methods for processing host and job confinguration files.
The following methods can be found:

host()
    Method containing the structure template for host configuration files.
job()
    Method containing the structure template for job configuration files.
loadconfigs()
    Method containing the code for parsing configuration files.
saveconfigs()
    Method containing the code for saving configuration files."""

import ConfigParser as configparser
import logging

LOGGER = logging.getLogger("Longbow")


def loadhosts(confile):

    """Method for processing host configuration files."""

    # Dictionary for the host configuration parameters.
    hosttemplate = {
        "corespernode": "24",
        "cores": "24",
        "host": "",
        "port": "22",
        "scheduler": "",
        "handler": "",
        "user": "",
        "accountflag": "",
        "account": "",
        "remoteworkdir": ""
    }

    required = [
        "host",
        "user",
        "remoteworkdir"
    ]

    hosts = loadconfigs(confile, hosttemplate, required)

    return hosts


def loadjobs(cwd, confile, executable, hostsconfile, remoteres):

    """Method for processing job configuration files."""

    # Dictionary to determine the module to load based on the command line
    # executable
    modules = {
            "charmm": "charmm",
            "pmemd": "amber",
            "pmemd.MPI": "amber",
            "lmp_xc30": "lampps",
            "namd2": "namd",
            "mdrun": "gromacs",
            "": ""
        }

    # Dictionary for the job configurations parameters.
    jobtemplate = {
        "account": "",
        "cluster": "",
        "commandline": "",
        "cores": "",
        "frequency": "60",
        "localworkdir": cwd,
        "modules": modules[executable],
        "maxtime": "24:00",
        "memory": "",
        "nodes": "",
        "executable": executable,
        "queue": "",
        "batch": "1",
        "resource": "",
        "remoteworkdir": ""
    }

    # If the executable is not specified on the command line, require
    # it to be in a job configuration file if provided
    if executable == "":
        required = [
            "executable",
            "resource"
        ]
    else:
        required = [
            "resource"
        ]

    if confile is None:
        jobs = loaddefaultjobconfigs(jobtemplate, hostsconfile, remoteres)
    else:
        jobs = loadconfigs(confile, jobtemplate, required)

    return jobs


def loaddefaultjobconfigs(template, hostsconfile, remoteres):

    """Method to load default job configurations."""

    LOGGER.info("Loading default job configuration information.")

    LOGGER.info("Loading configuration information from file: %s ",
                hostsconfile)

    # Instantiate the configparser and read the configuration file.
    configs = configparser.ConfigParser()

    try:
        configs.read(hostsconfile)
    except:
        raise RuntimeError("Can't read the configurations from: %s",
                           hostsconfile)

    # Grab a list of the section headers present in file.
    sectionlist = configs.sections()

    params = {}
    params["myjob"] = template.copy()

    if remoteres is not "":
        params["myjob"]["resource"] = remoteres
    else:
        params["myjob"]["resource"] = sectionlist[0]

    print params["myjob"]

    return params


def loadconfigs(confile, template, required):

    """Method to load configurations from file."""

    LOGGER.info("Loading configuration information from file: %s ", confile)

    # Instantiate the configparser and read the configuration file.
    configs = configparser.ConfigParser()

    try:
        configs.read(confile)
    except:
        raise RuntimeError("Can't read the configurations from: %s", confile)

    # Grab a list of the section headers present in file.
    sectionlist = configs.sections()
    sectioncount = len(sectionlist)

    # If we don't have any sections then raise an exception.
    if sectioncount is 0:
        raise RuntimeError("In file %s " % confile + "no sections can be " +
                           "detected or the file is not in ini format.")

    # Temporary dictionary for storing the configurations in.
    params = {}
    for section in sectionlist:
        params[section] = template.copy()

        # Grab the option count from the section.
        optioncount = len(configs.options(section))

        # If we have no options then raise an exception.
        if optioncount is 0:
            raise RuntimeError("There are no parameters listed under the" +
                               " section %s" % section)

        # Store option values in our dictionary structure.
        for option in template:
            try:
                params[section][option] = configs.get(section, option)
            except configparser.NoOptionError:
                if option in required and option == "executable":
                    raise RuntimeError("If the executable is not specified " +
                                       "on the command line, it must be " +
                                       "in the job configuration file")
                elif option in required:
                    raise RuntimeError("The parameter %s is required" %
                                       option)
                else:
                    pass

    return params


def saveconfigs(confile, params):

    """Method to save parameters to file."""

    LOGGER.info("Saving configuration information to file %s ", confile)

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
