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
import math

try:

    EX = __import__("corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("corelibs.shellwrappers", fromlist=[''])

except ImportError:

    EX = __import__("Longbow.corelibs.exceptions", fromlist=[''])
    SHELLWRAPPERS = __import__("Longbow.corelibs.shellwrappers", fromlist=[''])

LOGGER = logging.getLogger("Longbow")

QUERY_STRING = "env | grep -i 'pbs'"


def delete(host, job):

    """Method for deleting job."""

    jobid = job["jobid"]

    LOGGER.info("Deleting the job with id '{0}'" .format(jobid))

    try:

        if int(job["replicates"]) > 1:

            shellout = SHELLWRAPPERS.sendtossh(host, ["qdel " + jobid + "[]"])

        else:

            shellout = SHELLWRAPPERS.sendtossh(host, ["qdel " + jobid])

    except EX.SSHError:

        raise EX.JobdeleteError("Unable to delete job.")

    LOGGER.info("Deletion successful.")

    return shellout[0]


def prepare(hosts, jobname, jobs):

    """Create the PBS jobfile ready for submitting jobs"""

    LOGGER.info("Creating submit file for job '{0}'" .format(jobname))

    # Open file for PBS script.
    pbsfile = os.path.join(jobs[jobname]["localworkdir"], "submit.pbs")
    jobfile = open(pbsfile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n")

    # Job name (if supplied)
    if jobname is not "":

        jobfile.write("#PBS -N " + jobname + "\n")

    # Queue to submit to (if supplied)
    if jobs[jobname]["queue"] is not "":

        jobfile.write("#PBS -q " + jobs[jobname]["queue"] + "\n")

    # Account to charge (if supplied).
    if hosts[jobs[jobname]["resource"]]["account"] is not "":

        # if no accountflag is provided use the default
        if hosts[jobs[jobname]["resource"]]["accountflag"] is "":

            jobfile.write("#PBS -A " +
                          hosts[jobs[jobname]["resource"]]["account"] +
                          "\n")

        # else use the accountflag provided
        else:

            jobfile.write("#PBS " +
                          hosts[jobs[jobname]["resource"]]["accountflag"] +
                          " " + hosts[jobs[jobname]["resource"]]["account"] +
                          "\n")

    cpn = hosts[jobs[jobname]["resource"]]["corespernode"]

    cores = jobs[jobname]["cores"]

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
    memory = jobs[jobname]["memory"]

    tmp = "select=" + nodes + ":ncpus=" + ncpus + ":mpiprocs=" + mpiprocs

    # If user has specified memory append the flag (not all machines support
    # this).
    if memory is not "":

        tmp = tmp + ":mem=" + memory + "gb"

    # Write the resource requests
    jobfile.write("#PBS -l " + tmp + "\n")

    # Walltime for job.
    jobfile.write("#PBS -l walltime=" + jobs[jobname]["maxtime"] + ":00\n")

    # Set up replicates jobs
    if int(jobs[jobname]["replicates"]) > 1:

        jobfile.write("#PBS -J 1-" + jobs[jobname]["replicates"] + "\n")
        jobfile.write("#PBS -r y\n")

    # Set some environment variables for PBS.
    jobfile.write("\n"
                  "export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)\n"
                  "cd $PBS_O_WORKDIR\n"
                  "export OMP_NUM_THREADS=1\n"
                  "\n")

    # Load up modules if required.
    if jobs[jobname]["modules"] is not "":

        for module in jobs[jobname]["modules"].split(","):

            module = module.replace(" ", "")
            jobfile.write("module load {0}\n\n" .format(module))

    # Handler that is used for job submission.
    mpirun = hosts[jobs[jobname]["resource"]]["handler"]

    # CRAY's use aprun which has slightly different requirements to mpirun.
    if mpirun == "aprun":

        mpirun = mpirun + " -n " + cores + " -N " + mpiprocs

    # Single jobs only need one run command.
    if int(jobs[jobname]["replicates"]) == 1:

        jobfile.write(mpirun + " " + jobs[jobname]["executableargs"] + "\n")

    # Job array
    elif int(jobs[jobname]["replicates"]) > 1:

        jobfile.write("basedir=$PBS_O_WORKDIR \n"
                      "cd $basedir/rep${PBS_ARRAY_INDEX}/\n\n" +
                      mpirun + " " + jobs[jobname]["executableargs"] + "\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append pbs file to list of files ready for staging.
    jobs[jobname]["upload-include"] = (
        jobs[jobname]["upload-include"] + ", submit.pbs")
    jobs[jobname]["subfile"] = "submit.pbs"


def status(host, jobid):

    """Method for querying job."""

    state = ""

    try:

        shellout = SHELLWRAPPERS.sendtossh(host, ["qstat -u " + host["user"] +
                                                  " | grep " + jobid])

        stat = shellout[0].split()

        if stat[9] == "H":

            state = "Held"

        elif stat[9] == "Q":

            state = "Queued"

        elif stat[9] == "R":

            state = "Running"

        elif stat[9] == "B":

            state = "Subjob(s) running"

        elif stat[9] == "E":

            state = "Exiting"

        elif stat[9] == "M":

            state = "Job moved to server"

        elif stat[9] == "S":

            state = "Suspended"

        elif stat[9] == "T":

            state = "Job moved to new location"

        elif stat[9] == "U":

            state = ("Cycle-harvesting job is suspended due to keyboard " +
                     "activity")

        elif stat[9] == "W":

            state = "Waiting for start time"

        elif stat[9] == "X":

            state = "Subjob completed execution/has been deleted"

    except EX.SSHError:

        state = "Finished"

    return state


def submit(host, jobname, jobs):

    """Method for submitting a job."""

    # Set the path to remoteworkdir/jobnamexxxxx
    path = jobs[jobname]["destdir"]

    # Change into the working directory and submit the job.
    cmd = ["cd " + path + "\n", "qsub " + jobs[jobname]["subfile"] +
           " | grep -P -o '[0-9]*(?=.)'"]

    # Process the submit
    try:

        shellout = SHELLWRAPPERS.sendtossh(host, cmd)[0]

    except EX.SSHError as inst:

        if "set_booleans" in inst.stderr:

            raise EX.JobsubmitError(
                "Something went wrong when submitting. The likely cause is "
                "your particular PBS install is not receiving the "
                "information/options/parameters it " "requires "
                "e.g. '#PBS -l mem=20gb'. Check the PBS documentation and edit"
                " the configuration files to provide the necessary information"
                "e.g. 'memory = 20' in the job configuration file")

        elif "Job rejected by all possible destinations" in inst.stderr:

            raise EX.JobsubmitError(
                "Something went wrong when submitting. This may be because "
                "you need to provide PBS with your account code and the "
                "account flag your PBS install expects (Longbow defaults to "
                "A). Check the PBS documentation and edit the configuration "
                "files to provide the necessary information e.g. "
                "'accountflag = P' and 'account = ABCD-01234-EFG'")

        elif "Job must specify budget (-A option)" in inst.stderr:

            raise EX.JobsubmitError(
                "Something went wrong when submitting. This may be because "
                "you provided PBS with an account flag other than 'A' which "
                "your PBS install expects")

        elif "Job exceeds queue and/or server resource limits" in inst.stderr:

            raise EX.JobsubmitError(
                "Something went wrong when submitting. PBS has reported "
                "that 'Job exceeds queue and/or server resource limits'. "
                "This may be because you set a walltime or some other "
                "quantity that exceeds the maximum allowed on your system.")

        elif "budget" in inst.stderr:

            raise EX.JobsubmitError(
                "Something went wrong when submitting. This may be that you "
                "have entered an incorrect account code.")

        elif "illegal -N value" in inst.stderr:

            raise EX.JobsubmitError(
                "Something went wrong when submitting. This is due to the job "
                "name being too long, consult your system administrators/"
                "documentation to query this policy (try < 15 chars).")

        else:

            raise EX.JobsubmitError("Something went wrong when submitting.")

    output = shellout.rstrip("\r\n")

    LOGGER.info("Job '{0}' submitted with id '{1}'" .format(jobname, output))

    jobs[jobname]["jobid"] = output
