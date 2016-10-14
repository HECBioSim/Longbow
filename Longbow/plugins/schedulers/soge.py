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
This module contains the code to interact with the various flavours of
Son of Grid Engine.

delete(job)
    A method for deleting a single job.

prepare(job)
    The method for creating the job submission file for a single job.

status(job)
    The method for checking the status of a job.

submit(job)
    The method for submitting a single job.
"""

import math
import os
import re

try:

    import corelibs.exceptions as exceptions
    import corelibs.shellwrappers as shellwrappers

except ImportError:

    import Longbow.corelibs.exceptions as exceptions
    import Longbow.corelibs.shellwrappers as shellwrappers

QUERY_STRING = "env | grep -i 'sge'"


def delete(job):

    """
    Method for deleting job.
    """

    jobid = job["jobid"]

    try:

        shellout = shellwrappers.sendtossh(job, ["qdel " + jobid])

    except exceptions.SSHError:

        raise exceptions.JobdeleteError("Unable to delete job.")

    return shellout[0]


def prepare(job):

    """
    Create the SGE jobfile ready for submitting jobs.
    """

    # Open file for SGE script.
    sgefile = os.path.join(job["localworkdir"], "submit.sge")
    jobfile = open(sgefile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n"
                  "#$ -cwd -V\n")

    if job["jobname"] is not "":

        jobfile.write("#$ -N " + job["jobname"] + "\n")

    if job["queue"] is not "":

        jobfile.write("#$ -q " + job["queue"] + "\n")

    # Account to charge (if supplied).
    if job["account"] is not "":

        # if no accountflag is provided use the default
        if job["accountflag"] is "":

            jobfile.write("#$ -A " + job["account"] + "\n")

        # else use the accountflag provided
        else:

            jobfile.write("#$ " + job["accountflag"] + " " + job["account"] +
                          "\n")

    jobfile.write("#$ -l h_rt=" + job["maxtime"] + ":00\n")

    # Email user.
    if job["email-address"] is not "":

        if job["email-flags"] is not "":

            jobfile.write("#$ -m " + job["email-flags"] + "\n")

        jobfile.write("#$ -M " + job["email-address"] + "\n")

    # Job array
    if int(job["replicates"]) > 1:

        jobfile.write("#$ -t 1-" + job["replicates"] + "\n")

    cores = job["cores"]
    cpn = job["corespernode"]

    # Load levelling override. In cases where # of cores is less than
    # corespernode, user is likely to be undersubscribing.
    if int(cores) < int(cpn):

        cpn = cores

    # Calculate the number of nodes.
    nodes = float(cores) / float(cpn)

    # Makes sure nodes is rounded up to the next highest integer.
    nodes = str(int(math.ceil(nodes)))

    # Number of cpus per node (most machines will charge for all available cpus
    # per node whether you are using them or not)
    # ncpus = cpn

    # Number of mpi processes per node.
    # mpiprocs = cpn

    tmp = "nodes=" + nodes

    # Write the resource requests
    jobfile.write("#$ -l " + tmp + "\n")

    jobfile.write("#$ -pe ib " + cores + "\n\n")

    # Load any custom scripts.
    if job["scripts"] != "":

        scripts = job["scripts"].split(',')

        if len(scripts) > 0:

            for item in scripts:

                jobfile.write(item.strip() + "\n\n")

    if job["modules"] is not "":

        for module in job["modules"].split(","):

            module = module.replace(" ", "")
            jobfile.write("module load {0}\n\n" .format(module))

    mpirun = job["handler"]

    # Single job
    if int(job["replicates"]) == 1:

        jobfile.write(mpirun + " " + job["executableargs"] + "\n")

    # Job array
    elif int(job["replicates"]) > 1:

        jobfile.write("cd rep${SGE_TASK_ID}/\n" + mpirun +
                      job["executableargs"] + "\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append lsf file to list of files ready for staging.
    job["upload-include"] = job["upload-include"] + ", submit.sge"
    job["subfile"] = "submit.sge"


def status(job):

    """
    Method for querying job.
    """

    states = {
        "h": "Held",
        "qw": "Queued",
        "r": "Running"
        }

    jobstate = ""

    try:

        shellout = shellwrappers.sendtossh(job, ["qstat -u " + job["user"]])

    except exceptions.SSHError:

        raise

    # PBS will return a table, so split lines into a list.
    stdout = shellout[0].split("\n")

    # Look up the job state and convert it to Longbow terminology.
    try:

        # Now match the jobid against the list of jobs, extract the line and
        # split it into a list
        job = [line for line in stdout if job["jobid"] in line][0].split()

        jobstate = states[job[4]]

    except (IndexError, KeyError):

        jobstate = "Finished"

    return jobstate


def submit(job):

    """
    Method for submitting a job.
    """

    # Change into the working directory and submit the job.
    cmd = ["cd " + job["destdir"] + "\n", "qsub " + job["subfile"]]

    # Process the submit
    try:

        shellout = shellwrappers.sendtossh(job, cmd)

    except exceptions.SSHError as inst:

        if "per user" or "per-user" in inst.stderr:

            raise exceptions.QueuemaxError

        else:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. The following output "
                "came back from the SSH call:\nstdout: {0}\nstderr {1}"
                .format(shellout[0], shellout[1]))

    try:

        # Do the regex in Longbow rather than in the subprocess.
        jobid = re.search(r'\d+', shellout[0]).group()

    except AttributeError:

        raise exceptions.JobsubmitError(
            "Could not detect the job id during submission, this means that "
            "either the submission failed in an unexpected way, or that "
            "Longbow could not understand the returned information.")

    # Put jobid into the job dictionary.
    job["jobid"] = jobid
