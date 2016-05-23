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
This module contains the code to interact with the various flavours of slurm.

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

    EX = __import__("corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("corelibs.shellwrappers", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("Longbow.corelibs.shellwrappers", fromlist=[''])

QUERY_STRING = "which sbatch"


def delete(job):

    """
    Method for deleting job.
    """

    jobid = job["jobid"]

    try:

        shellout = SHELLWRAPPERS.sendtossh(job, ["scancel " + jobid])

    except EX.SSHError:

        raise EX.JobdeleteError("Unable to delete job.")

    return shellout[0]


def prepare(job):

    """
    Create the SLURM jobfile ready for submitting jobs.
    """

    # Open file for SLURM script.
    slurmfile = os.path.join(job["localworkdir"], "submit.slurm")
    jobfile = open(slurmfile, "w+")

    # Write the SLURM script
    jobfile.write("#!/bin/bash --login\n")

    # Job name (if supplied)
    if job["jobname"] is not "":

        jobfile.write("#SBATCH -J " + job["jobname"] + "\n")

    # Queue to submit to (if supplied)
    if job["queue"] is not "":

        jobfile.write("#SBATCH -p " + job["queue"] + "\n")

    # Account to charge (if supplied)
    if job["account"] is not "":

        # if no accountflag is provided use the default
        if job["accountflag"] is "":

            jobfile.write("#SBATCH -A " + job["account"] + "\n")

        else:

            jobfile.write("#SBATCH " + job["accountflag"] + " " +
                          job["account"] + "\n")

    cores = job["cores"]
    cpn = job["corespernode"]

    # Specify the total number of mpi tasks required
    jobfile.write("#SBATCH -n " + cores + "\n")

    # If user has specified corespernode for under utilisation then
    # set the total nodes (-N) parameter.
    if cpn is not "":

        nodes = float(cores) / float(cpn)

        # Make sure nodes is rounded up to the next highest integer
        nodes = str(int(math.ceil(nodes)))
        jobfile.write("#SBATCH -N " + nodes + "\n")

    # Walltime for job
    jobfile.write("#SBATCH -t " + job["maxtime"] + ":00\n\n")

    # Load up modules if required.
    if job["modules"] is not "":

        for module in job["modules"].split(","):

            module = module.replace(" ", "")
            jobfile.write("module load {0}\n\n" .format(module))

    # Handler that is used for job submission.
    mpirun = job["handler"]

    # Single jobs only need one run command.
    if int(job["replicates"]) == 1:

        jobfile.write(mpirun + " " + job["executableargs"] + "\n")

    # Ensemble jobs need a loop.
    elif int(job["replicates"]) > 1:

        jobfile.write("basedir = `pwd`\n"
                      "for i in {1.." + job["replicates"] + "};\n"
                      "do\n"
                      "  cd $basedir/rep$i/\n"
                      "  " + mpirun + " " + job["executableargs"] +
                      "\n"
                      "done\n"
                      "wait\n")

    # Close the file
    jobfile.close()

    # Append submitfile to list of files ready for staging.
    job["upload-include"] = job["upload-include"] + ", submit.slurm"
    job["subfile"] = "submit.slurm"


def status(job):

    """
    Method for querying job.
    """

    states = {
        "CA": "Cancelled",
        "CD": "Completed",
        "CF": "Configuring",
        "CG": "Completing",
        "F": "Failed",
        "NF": "Node Failure",
        "PD": "Pending",
        "PR": "Preempted",
        "R": "Running",
        "S": "Suspended",
        "TO": "Timed out"
        }

    jobstate = ""

    try:

        shellout = SHELLWRAPPERS.sendtossh(job, ["squeue -u " + job["user"]])

    except EX.SSHError:

        raise

    # PBS will return a table, so split lines into a list.
    stdout = shellout[0].split("\n")

    # Now match the jobid against the list of jobs, extract the line and split
    # it into a list
    job = [line for line in stdout if job["jobid"] in line][0].split()

    # Look up the job state and convert it to Longbow terminology.
    try:

        jobstate = states[job[4]]

    except KeyError:

        jobstate = "Finished"

    return jobstate


def submit(job):

    """
    Method for submitting job.
    """

    # Change into the working directory and submit the job.
    cmd = ["cd " + job["destdir"] + "\n", "sbatch " + job["subfile"]]

    # Process the submit
    try:

        shellout = SHELLWRAPPERS.sendtossh(job, cmd)

    except EX.SSHError as inst:

        if "violates" and "job submit limit" in inst.stderr:

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
