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
The applications module contains methods for processing the aspect of jobs
which relate to external applications (such as an MD package). The following
methods can be found within this module:

testapp(jobs)
    This method will make an attempt to check that the application executables
    required to run a job/s is present on the specified host/s. This method is
    capable of using the module system.

processjobs(jobs)
    This method will process information that is given as an intended target to
    be passed on to the executable at run time. It will check that required
    parameters (provided the respective plug-in is configured correctly) have
    been supplied, and that all files and their dependencies (again provided
    that the respective plug-in is configured for this) exist on disk.
"""

import logging
import os

# Depending on how longbow is installed/utilised the import will be slightly
# different, this should handle both cases.
try:

    import corelibs.exceptions as exceptions
    import corelibs.shellwrappers as shellwrappers
    import plugins.apps as apps

except ImportError:

    import Longbow.corelibs.exceptions as exceptions
    import Longbow.corelibs.shellwrappers as shellwrappers
    import Longbow.plugins.apps as apps


LOG = logging.getLogger("Longbow.corelibs.applications")


def testapp(jobs):

    """
    This method will make an attempt to check that the application executables
    required to run a job/s is present on the specified host/s. This method is
    capable of using the module system.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    checked = {}

    LOG.info("Testing the executables defined for each job.")

    for item in jobs:

        job = jobs[item]
        resource = job["resource"]
        executable = job["executable"]

        # If we haven't checked this resource then it is likely not in the dict
        if resource not in checked:

            checked[resource] = []

        # Now check if we have tested this exec already.
        if executable not in checked[resource]:

            # If not then add it to the list now.
            checked[resource].extend([executable])

            LOG.info("Checking executable '%s' on '%s'", executable, resource)

            cmd = []

            if job["modules"] is "":

                LOG.debug("Checking without modules.")

            else:
                LOG.debug("Checking with modules.")

                for module in job["modules"].split(","):

                    module = module.replace(" ", "")
                    cmd.extend(["module load " + module + "\n"])

            cmd.extend(["which " + executable])

            try:

                shellwrappers.sendtossh(job, cmd)
                LOG.info("Executable check - passed.")

            except exceptions.SSHError:

                LOG.error("Executable check - failed.")
                raise


def processjobs(jobs):

    """
    This method will process information that is given as an intended target to
    be passed on to the executable at run time. It will check that required
    parameters (provided the respective plug-in is configured correctly) have
    been supplied, and that all files and their dependencies (again provided
    that the respective plug-in is configured for this) exist on disk.

    Required arguments are:

    jobs (dictionary) - The Longbow jobs data structure, see configuration.py
                        for more information about the format of this
                        structure.
    """

    LOG.info("Processing job/s and detecting files that require upload.")

    # Get dictionary of executables and their required flags from plug-ins.
    appplugins = getattr(apps, "DEFMODULES")

    # Process each job.
    for job in jobs:

        # Initialise some basic parameters.
        executable = jobs[job]["executable"]
        app = appplugins[executable]
        args = jobs[job]["executableargs"]
        filelist = []

        LOG.debug("Command-line arguments for job '%s'are '%s'", job, args)

        # Check for any files that are located outside the work directory or
        # absolute paths.
        for arg in args:

            if arg.count(os.path.pardir) > 0 or os.path.isabs(arg):

                raise exceptions.RequiredinputError(
                    "In job '{0}' input files are being provided with "
                    "absolute paths or from directories above localworkdir. "
                    "This is not supported".format(job))

        # Base path to local job directory.
        cwd = jobs[job]["localworkdir"]

        # If we have multiple jobs.
        if len(jobs) > 1:

            # Add the job name to the path.
            cwd = os.path.join(cwd, job)
            job["localworkdir"] = cwd













        # Setup the rysnc upload masks.
        if jobs[job]["upload-include"] is "":

            jobs[job]["upload-include"] = (", ".join(filelist))

        else:

            jobs[job]["upload-include"] = (job["upload-include"] + ", " +
                                           ", ".join(filelist))

        jobs[job]["upload-exclude"] = "*"

        # Replace the input command line with the execution command line.
        # initargs is a copy of the original args before text enforcing
        # substitutions was removed
        jobs[job]["executableargs"] = executable + " " + " ".join(initargs)

        LOG.info("For job '%s' - execution string: %s",
                 job, jobs[job]["executableargs"])

    LOG.info("Processing jobs - complete.")


def _appcommandlinetype1():

    """
    Processor for applications that have the command-line type:

    exec input.file
    """


def _appcommandlinetype2():

    """
    Processor for applications that have the command-line type:

    exec < input.file
    exec < input.file > output.file
    """


def _appcommandlinetype3():

    """
    Processor for applications that have the command-line type:

    exec --input file1 -file file2 -parameter1 --parameter2
    """


def _appcommandlinetype4():

    """
    Processor for applications that have the command-line type:

    exec subexec --file1 file1 -file2 file2 -parameter1 --parameter2
    """
