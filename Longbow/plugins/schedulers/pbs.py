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
PBS/Torque.

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

QUERY_STRING = "env | grep -i 'pbs'"


def delete(job):

    """
    Method for deleting job.
    """

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

    """
    Create the PBS jobfile ready for submitting jobs
    """

    # Open file for PBS script.
    pbsfile = os.path.join(job["localworkdir"], "submit.pbs")
    jobfile = open(pbsfile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n")

    # Job name (if supplied)
    if job["jobname"] is not "":

        jobfile.write("#PBS -N " + job["jobname"] + "\n")

    # Queue to submit to (if supplied)
    if job["queue"] is not "":

        jobfile.write("#PBS -q " + job["queue"] + "\n")

    # Account to charge (if supplied).
    if job["account"] is not "":

        # if no accountflag is provided use the default
        if job["accountflag"] is "":

            jobfile.write("#PBS -A " + job["account"] + "\n")

        # else use the accountflag provided
        else:

            jobfile.write("#PBS " + job["accountflag"] + " " +
                          job["account"] + "\n")

    cpn = job["corespernode"]

    cores = job["cores"]

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
    ncpus = cpn

    # Number of mpi processes per node.
    mpiprocs = cpn

    # Memory size (used to select nodes with minimum memory).
    memory = job["memory"]

    tmp = "select=" + nodes + ":ncpus=" + ncpus + ":mpiprocs=" + mpiprocs

    # If user has specified memory append the flag (not all machines support
    # this).
    if memory is not "":

        tmp = tmp + ":mem=" + memory + "gb"

    # Write the resource requests
    jobfile.write("#PBS -l " + tmp + "\n")

    # Email user.
    if job["email-address"] is not "":

        if job["email-flags"] is not "":

            jobfile.write("#PBS -m " + job["email-flags"] + "\n")

        jobfile.write("#PBS -M " + job["email-address"] + "\n")

    # Walltime for job.
    jobfile.write("#PBS -l walltime=" + job["maxtime"] + ":00\n")

    # Set up replicates jobs
    if int(job["replicates"]) > 1:

        jobfile.write("#PBS -J 1-" + job["replicates"] + "\n")
        jobfile.write("#PBS -r y\n")

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

                jobfile.write(item.strip() + "\n\n")

    # Load up modules if required.
    if job["modules"] is not "":

        for module in job["modules"].split(","):

            module = module.replace(" ", "")
            jobfile.write("module load {0}\n\n" .format(module))

    # Handler that is used for job submission.
    mpirun = job["handler"]

    # CRAY's use aprun which has slightly different requirements to mpirun.
    if mpirun == "aprun":

        mpirun = mpirun + " -n " + cores + " -N " + mpiprocs

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

    """
    Method for querying job.
    """

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

    try:

        shellout = shellwrappers.sendtossh(job, ["qstat -u " + job["user"]])

    except exceptions.SSHError:

        raise

    # PBS will return a table, so split lines into a list.
    stdout = shellout[0].split("\n")

    try:

        # Now match the jobid against the list of jobs, extract the line and
        # split it into a list
        job = [line for line in stdout if job["jobid"] in line][0].split()

        # Look up the job state and convert it to Longbow terminology.
        jobstate = states[job[9]]

    except (IndexError, KeyError):

        jobstate = "Finished"

    return jobstate


def submit(job):

    """
    Method for submitting a job.
    """

    # Change into the working directory and submit the job.
    cmd = ["cd " + job["destdir"] + "\n", "qsub " + job["subfile"]]

    try:

        shellout = shellwrappers.sendtossh(job, cmd)

    except exceptions.SSHError as inst:

        if "would exceed" and "per-user limit" in inst.stderr:

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
