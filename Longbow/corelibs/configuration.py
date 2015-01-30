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
        "corespernode": "",
        "host": "",
        "port": "22",
        "scheduler": "",
        "handler": "",
        "user": ""
    }

    required = [
        "host",
        "user"
    ]

    hosts = loadconfigs(confile, hosttemplate, required, {})

    return hosts


def loadjobs(cwd, confile, overrides):

    """Method for processing job configuration files."""

    # Dictionary for the job configurations parameters.
    jobtemplate = {
        "account": "",
        "batch": "1",
        "cluster": "",
        "commandline": "",
        "cores": "",
        "corespernode": "",
        "executable": "",
        "frequency": "60",
        "localworkdir": cwd,
        "modules": "",
        "maxtime": "",
        "memory": "",
        "nodes": "",
        "program": "",
        "remoteworkdir": "",
        "queue": "",
        "resource": ""
    }

    required = [
        "executable",
        "remoteworkdir",
        "resource"
    ]

    jobs = loadconfigs(confile, jobtemplate, required, overrides)

    return jobs


def loadconfigs(confile, template, required, overrides):

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
            # Is this option being overridden.
            if option in overrides:
                params[section][option] = overrides[option]
            else:
                try:
                    params[section][option] = configs.get(section, option)
                except configparser.NoOptionError:
                    if option in required:
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
