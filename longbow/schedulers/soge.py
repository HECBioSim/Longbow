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

"""A module containing the code to interact with Son of Grid Engine.

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

QUERY_STRING = "env | grep -i 'sge'"


def delete(job):
    """Delete a job."""
    # Initialise variables.
    jobid = job["jobid"]

    try:

        shellout = shellwrappers.sendtossh(job, ["qdel " + jobid])

    except exceptions.SSHError:

        raise exceptions.JobdeleteError("Unable to delete job.")

    return shellout[0]


def prepare(job):
    """Create the SGE jobfile ready for submitting jobs."""
    # Open file for SGE script.
    sgefile = os.path.join(job["localworkdir"], "submit.soge")
    jobfile = open(sgefile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n"
                  "#$ -cwd -V\n")

    jobfile.write("#$ -N " + job["jobname"] + "\n")

    if job["queue"] != "":

        jobfile.write("#$ -q " + job["queue"] + "\n")

    # Account to charge (if supplied).
    if job["account"] != "":

        # if no accountflag is provided use the default
        if job["accountflag"] == "":

            jobfile.write("#$ -A " + job["account"] + "\n")

        # else use the accountflag provided
        else:

            jobfile.write("#$ " + job["accountflag"] + " " + job["account"] +
                          "\n")

    jobfile.write("#$ -l h_rt=" + job["maxtime"] + ":00\n")

    if job["memory"] != "":

        jobfile.write("#$ -l h_vmem=" + job["memory"] + "G\n")

    # Email user.
    if job["email-address"] != "":

        if job["email-flags"] != "":

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

    jobfile.write("export OMP_NUM_THREADS=1\n\n")

    # Redirect stdout
    if job["stdout"] != "":

        jobfile.write("#$ -o " + job["stdout"] + "\n")

    # Redirect stderr
    if job["stderr"] != "":

        jobfile.write("#$ -e " + job["stderr"] + "\n\n")

    # Load any custom scripts.
    if job["scripts"] != "":

        scripts = job["scripts"].split(',')

        if len(scripts) > 0:

            for item in scripts:

                jobfile.write(item.strip() + "\n")

            jobfile.write("\n")

    if job["modules"] != "":

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
    job["upload-include"] = job["upload-include"] + ", submit.soge"
    job["subfile"] = "submit.soge"


def status(job):
    """Query a job status."""
    # Initialise variables.
    states = {
        "h": "Held",
        "qw": "Queued",
        "r": "Running"
    }

    jobstate = ""

    shellout = shellwrappers.sendtossh(job, ["qstat -u " + job["user"]])

    # PBS will return a table, so split lines into a list.
    stdout = shellout[0].split("\n")

    # Look up the job state and convert it to Longbow terminology.
    # Now match the jobid against the list of jobs, extract the line and
    # split it into a list
    for line in stdout:

        line = line.split()

        if len(line) > 0 and job["jobid"] in line[0]:

            jobstate = states[line[4]]
            break

    if jobstate == "":

        jobstate = "Finished"

    return jobstate


def submit(job):
    """Submit a job."""
    # Change into the working directory and submit the job.
    cmd = ["cd " + job["destdir"] + "\n", "qsub " + job["subfile"]]

    # Process the submit
    try:

        shellout = shellwrappers.sendtossh(job, cmd)

    except exceptions.SSHError as inst:

        if "per user" in inst.stderr or "per-user" in inst.stderr:

            raise exceptions.QueuemaxError

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
