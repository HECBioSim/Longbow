# BSD 3-Clause License
#
# Copyright (c) 2017, Science and Technology Facilities Council and
# The University of Nottingham
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""A module containing the code to interact with PBS/Torque.

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

import longbow.exceptions as exceptions
import longbow.shellwrappers as shellwrappers

QUERY_STRING = "env | grep -i 'pbs'"


def delete(job):
    """Delete a job."""
    # Initialise variables.
    jobid = job["jobid"]

    try:

        if int(job["replicates"]) > 1:

            shellout = shellwrappers.sendtossh(job, ["qdel " + jobid + "[]"])

        else:

            shellout = shellwrappers.sendtossh(job, ["qdel " + jobid])

    except exceptions.SSHError:

        raise exceptions.JobdeleteError("Unable to delete job.")

    return shellout[0]


def prepare(job):
    """Create the PBS jobfile ready for submitting jobs."""
    # Open file for PBS script.
    pbsfile = os.path.join(job["localworkdir"], "submit.pbs")
    jobfile = open(pbsfile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n")

    # Job name (if supplied)
    jobfile.write("#PBS -N " + job["jobname"] + "\n")

    # Queue to submit to (if supplied)
    if job["queue"] != "":

        jobfile.write("#PBS -q " + job["queue"] + "\n")

    # Account to charge (if supplied).
    if job["account"] != "":

        # if no accountflag is provided use the default
        if job["accountflag"] == "":

            jobfile.write("#PBS -A " + job["account"] + "\n")

        # else use the accountflag provided
        else:

            jobfile.write("#PBS " + job["accountflag"] + " " +
                          job["account"] + "\n")

    processes = job["cores"]
    cpn = job["corespernode"]
    mpiprocs = job["mpiprocs"]

    # If not undersubscribing then.
    if mpiprocs == "" and processes < cpn:

        mpiprocs = processes

    elif mpiprocs == "":

        mpiprocs = cpn

    # Calculate the number of nodes.
    nodes = str(int(math.ceil(float(processes) / float(mpiprocs))))

    tmp = "select=" + nodes + ":ncpus=" + cpn + ":mpiprocs=" + mpiprocs

    # If user has specified memory append the flag (not all machines support
    # this).
    if job["memory"] != "":

        tmp = tmp + ":mem=" + job["memory"] + "gb"

    # Write the resource requests
    jobfile.write("#PBS -l " + tmp + "\n")

    # Email user.
    if job["email-address"] != "":

        if job["email-flags"] != "":

            jobfile.write("#PBS -m " + job["email-flags"] + "\n")

        jobfile.write("#PBS -M " + job["email-address"] + "\n")

    # Walltime for job.
    jobfile.write("#PBS -l walltime=" + job["maxtime"] + ":00\n")

    # Set up replicates jobs
    if int(job["replicates"]) > 1:

        jobfile.write("#PBS -J 1-" + job["replicates"] + "\n")
        jobfile.write("#PBS -r y\n")

    # Redirect stdout
    if job["stdout"] != "":

        jobfile.write("#PBS -o " + job["stdout"] + "\n")

    # Redirect stderr
    if job["stderr"] != "":

        jobfile.write("#PBS -e " + job["stderr"] + "\n")

    # Set some environment variables for PBS.
    jobfile.write(
        "\n" + "export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)\n"
        "cd $PBS_O_WORKDIR\n"
        "export OMP_NUM_THREADS=1\n\n")

    # Load any custom scripts.
    if job["scripts"] != "":

        scripts = job["scripts"].split(',')

        if len(scripts) > 0:

            for item in scripts:

                jobfile.write(item.strip() + "\n")

            jobfile.write("\n")

    # Load up modules if required.
    if job["modules"] != "":

        for module in job["modules"].split(","):

            module = module.replace(" ", "")
            jobfile.write("module load {0}\n\n" .format(module))

    # Handler that is used for job submission.
    mpirun = job["handler"]

    # CRAY's use aprun which has slightly different requirements to mpirun.
    if mpirun == "aprun":

        mpirun = mpirun + " -n " + processes + " -N " + mpiprocs

    # Single jobs only need one run command.
    if int(job["replicates"]) == 1:

        jobfile.write(mpirun + " " + job["executableargs"] + "\n")

    # Job array
    elif int(job["replicates"]) > 1:

        jobfile.write(
            "basedir=$PBS_O_WORKDIR \n"
            "cd $basedir/rep${PBS_ARRAY_INDEX}/\n\n" +
            mpirun + " " + job["executableargs"] + "\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append pbs file to list of files ready for staging.
    job["upload-include"] = job["upload-include"] + ", submit.pbs"
    job["subfile"] = "submit.pbs"


def status(job):
    """Query a job status."""
    # Initialise variables.
    states = {
        "B": "Subjob(s) Running",
        "E": "Exiting",
        "H": "Held",
        "M": "Job Moved to Server",
        "Q": "Queued",
        "R": "Running",
        "S": "Suspended",
        "T": "Job Moved to New Location",
        "U": "Cycle-Harvesting Job is Suspended Due to Keyboard Activity",
        "W": "Waiting for Start Time",
        "X": "Subjob Completed Execution/Has Been Deleted"
    }

    jobstate = ""

    shellout = shellwrappers.sendtossh(job, ["qstat -u " + job["user"]])

    # PBS will return a table, so split lines into a list.
    stdout = shellout[0].split("\n")

    for line in stdout:

        line = line.split()

        if len(line) > 0 and job["jobid"] in line[0]:

            jobstate = states[line[9]]
            break

    if jobstate == "":

        jobstate = "Finished"

    return jobstate


def submit(job):
    """Submit a job."""
    # Change into the working directory and submit the job.
    cmd = ["cd " + job["destdir"] + "\n", "qsub " + job["subfile"]]

    try:

        shellout = shellwrappers.sendtossh(job, cmd)

    except exceptions.SSHError as inst:

        if "would exceed" in inst.stderr and "per-user limit" in inst.stderr:

            raise exceptions.QueuemaxError

        elif "set_booleans" in inst.stderr:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. The likely cause is "
                "your particular PBS install is not receiving the "
                "information/options/parameters it " "requires "
                "e.g. '#PBS -l mem=20gb'. Check the PBS documentation and edit"
                " the configuration files to provide the necessary information"
                "e.g. 'memory = 20' in the job configuration file")

        elif "Job rejected by all possible destinations" in inst.stderr:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. This may be because "
                "you need to provide PBS with your account code and the "
                "account flag your PBS install expects (Longbow defaults to "
                "A). Check the PBS documentation and edit the configuration "
                "files to provide the necessary information e.g. "
                "'accountflag = P' and 'account = ABCD-01234-EFG'")

        elif "Job must specify budget (-A option)" in inst.stderr:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. This may be because "
                "you provided PBS with an account flag other than 'A' which "
                "your PBS install expects")

        elif "Job exceeds queue and/or server resource limits" in inst.stderr:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. PBS has reported "
                "that 'Job exceeds queue and/or server resource limits'. "
                "This may be because you set a walltime or some other "
                "quantity that exceeds the maximum allowed on your system.")

        elif "budget" in inst.stderr:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. This may be that you "
                "have entered an incorrect account code.")

        elif "illegal -N value" in inst.stderr:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. This is due to the job "
                "name being too long, consult your system administrators/"
                "documentation to query this policy (try < 15 chars).")

        else:

            raise exceptions.JobsubmitError(
                "Something went wrong when submitting. The following output "
                "came back from the SSH call:\nstdout: {0}\nstderr {1}"
                .format(inst.stdout, inst.stderr))

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
