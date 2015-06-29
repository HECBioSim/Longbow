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

"""."""

import logging
import os

try:

    EX = __import__("corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("corelibs.shellwrappers", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("Longbow.corelibs.shellwrappers", fromlist=[''])

LOGGER = logging.getLogger("Longbow")

QUERY_STRING = "env | grep -i 'sge'"


def delete(host, job):

    """Method for deleting job."""

    jobid = job["jobid"]

    LOGGER.info("Deleting the job with id '{0}'" .format(jobid))

    try:

        shellout = SHELLWRAPPERS.sendtossh(host, ["qdel " + jobid])

    except EX.SSHError:

        raise EX.JobdeleteError("Unable to delete job.")

    LOGGER.info("Deleted successfully")

    return shellout[0]


def prepare(hosts, jobname, jobs):

    """Create the SGE jobfile ready for submitting jobs"""

    LOGGER.info("Creating submit file for job '{0}'" .format(jobname))

    # Open file for LSF script.
    sgefile = os.path.join(jobs[jobname]["localworkdir"], "submit.sge")
    jobfile = open(sgefile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n"
                  "#$ -cwd -V\n")

    if jobname is not "":

        jobfile.write("#$ -N " + jobname + "\n")

    if jobs[jobname]["queue"] is not "":

        jobfile.write("#$ -q " + jobs[jobname]["queue"] + "\n")

    # Account to charge (if supplied).
    if hosts[jobs[jobname]["resource"]]["account"] is not "":

        # if no accountflag is provided use the default
        if hosts[jobs[jobname]["resource"]]["accountflag"] is "":

            jobfile.write("#$ -A " +
                          hosts[jobs[jobname]["resource"]]["account"] + "\n")

        # else use the accountflag provided
        else:

            jobfile.write("#$ " +
                          hosts[jobs[jobname]["resource"]]["accountflag"] +
                          " " + hosts[jobs[jobname]["resource"]]["account"] +
                          "\n")

    jobfile.write("#$ -l h_rt=" + jobs[jobname]["maxtime"] + ":00\n")

    # Job array
    if int(jobs[jobname]["replicates"]) > 1:

        jobfile.write("#$ -t 1-" + jobs[jobname]["replicates"] + "\n")

    jobfile.write("#$ -pe ib " + jobs[jobname]["cores"] +
                  "\n\n")

    if jobs[jobname]["modules"] is not "":

        for module in jobs[jobname]["modules"].split(","):

            module = module.replace(" ", "")
            jobfile.write("module load {0}\n\n" .format(module))

    mpirun = hosts[jobs[jobname]["resource"]]["handler"]

    # Single job
    if int(jobs[jobname]["replicates"]) == 1:

        jobfile.write(mpirun + " " + jobs[jobname]["executableargs"] + "\n")

    # Job array
    elif int(jobs[jobname]["replicates"]) > 1:

        jobfile.write("cd rep${SGE_TASK_ID}/\n" +
                      mpirun + jobs[jobname]["executableargs"] + "\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append lsf file to list of files ready for staging.
    jobs[jobname]["upload-include"] = (
        jobs[jobname]["upload-include"] + ", submit.sge")
    jobs[jobname]["subfile"] = "submit.sge"


def status(host, jobid):

    """Method for querying job."""

    state = ""

    try:

        shellout = SHELLWRAPPERS.sendtossh(host, ["qstat -u " + host["user"] +
                                                  " | grep " + jobid])

        stat = shellout[0].split()

        if stat[4] == "h":

            state = "Held"

        elif stat[4] == "qw":

            state = "Queued"

        elif stat[4] == "r":

            state = "Running"

    except EX.SSHError:

        state = "Finished"

    return state


def submit(host, jobname, jobs):

    """Method for submitting a job."""

    # Set the path to remoteworkdir/jobnamexxxxx
    path = jobs[jobname]["destdir"]

    # Change into the working directory and submit the job.
    cmd = ["cd " + path + "\n", "qsub " + jobs[jobname]["subfile"] +
           " | grep -P -o '(?<= )[0-9]*(?= )'"]

    # Process the submit
    try:

        shellout = SHELLWRAPPERS.sendtossh(host, cmd)[0]

    except EX.SSHError:

        raise EX.JobsubmitError("  Something went wrong when submitting.")

    LOGGER.info("Job '{0}' submitted with id '{1}'" .format(jobname, shellout))

    jobs[jobname]["jobid"] = shellout
