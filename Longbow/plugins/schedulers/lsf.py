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
This module contains the code to interact with the various flavours of LSF.

delete(job)
    A method for deleting a single job.

prepare(job)
    The method for creating the job submission file for a single job.

status(job)
    The method for checking the status of a job.

submit(job)
    The method for submitting a single job.
"""

import os
import re

try:

    EX = __import__("corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("corelibs.shellwrappers", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("Longbow.corelibs.shellwrappers", fromlist=[''])

QUERY_STRING = "env | grep -i 'lsf'"


def delete(job):

    """
    Method for deleting job.
    """

    jobid = job["jobid"]

    try:

        shellout = SHELLWRAPPERS.sendtossh(job, ["bkill " + jobid])

    except EX.SSHError:

        raise EX.JobdeleteError("Unable to delete job.")

    return shellout[0]


def prepare(job):

    """
    Create the LSF jobfile ready for submitting jobs.
    """

    # Open file for LSF script.
    lsffile = os.path.join(job["localworkdir"], "submit.lsf")
    jobfile = open(lsffile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n")

    if job["jobname"] is not "":

        # Single job
        if int(job["replicates"]) == 1:

            jobfile.write("#BSUB -J " + job["jobname"] + "\n")

        # Job array
        elif int(job["replicates"]) > 1:

            jobfile.write("#BSUB -J " + job["jobname"] + "[1-" +
                          job["replicates"] + "]\n")

    if job["queue"] is not "":

        jobfile.write("#BSUB -q " + job["queue"] + "\n")

    if job["cluster"] is not "":

        jobfile.write("#BSUB -m " + job["cluster"] + "\n")

    # Account to charge (if supplied).
    if job["account"] is not "":

        # if no accountflag is provided use the default
        if job["accountflag"] is "":

            jobfile.write("#BSUB -P " + job["account"] + "\n")

        else:

            jobfile.write("#BSUB " + job["accountflag"] + " " +
                          job["account"] + "\n")

    jobfile.write("#BSUB -W " + job["maxtime"] + "\n")

    jobfile.write("#BSUB -n " + job["cores"] + "\n")

    if job["modules"] is not "":

        for module in job["modules"].split(","):

            module = module.replace(" ", "")
            jobfile.write("\n" + "module load {0}\n\n" .format(module))

    mpirun = job["handler"]

    # Single job
    if int(job["replicates"]) == 1:

        jobfile.write(mpirun + " -lsf " + job["executableargs"] + "\n")

    # Job array
    elif int(job["replicates"]) > 1:

        jobfile.write("cd rep${LSB_JOBINDEX}/\n" + mpirun + " -lsf " +
                      job["executableargs"] + "\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append lsf file to list of files ready for staging.
    job["upload-include"] = job["upload-include"] + ", submit.lsf"
    job["subfile"] = "submit.lsf"


def status(job):

    """
    Method for querying job.
    """

    states = {
        "DONE": "Job Exited Properly",
        "EXIT": "Job Exited in Error",
        "PEND": "Queued",
        "PSUSP": "Suspended",
        "RUN": "Running",
        "SSUSP": "Suspended",
        "UNKWN": "Unknown Status",
        "USUSP": "Suspended",
        "WAIT": "Waiting for Start Time",
        "ZOMBI": "Zombie Job"
        }

    jobstate = ""

    try:

        shellout = SHELLWRAPPERS.sendtossh(job, ["bjobs -u " + job["user"]])

    except EX.SSHError:

        raise

    # PBS will return a table, so split lines into a list.
    stdout = shellout[0].split("\n")

    # Now match the jobid against the list of jobs, extract the line and split
    # it into a list
    job = [line for line in stdout if job["jobid"] in line][0].split()

    # Look up the job state and convert it to Longbow terminology.
    try:

        jobstate = states[job[2]]

    except KeyError:

        jobstate = "Finished"

    return jobstate


def submit(job):

    """
    Method for submitting job.
    """

    # cd into the working directory and submit the job.
    cmd = ["cd " + job["destdir"] + "\n", "bsub < " + job["subfile"]]

    # Process the submit
    try:

        shellout = SHELLWRAPPERS.sendtossh(job, cmd)

    except EX.SSHError as inst:

        if "limit" in inst.stderr:

            raise EX.QueuemaxError

        else:

            raise EX.JobsubmitError(
                "Something went wrong when submitting. The following output "
                "came back from the SSH call:\nstdout: {0}\nstderr {1}"
                .format(shellout[0], shellout[1]))

    try:

        # Do the regex in Longbow rather than in the subprocess.
        jobid = re.search(r'\d+', shellout[0]).group()

    except AttributeError:

        raise EX.JobsubmitError(
            "Could not detect the job id during submission, this means that "
            "either the submission failed in an unexpected way, or that "
            "Longbow could not understand the returned information.")

    # Put jobid into the job dictionary.
    job["jobid"] = jobid
