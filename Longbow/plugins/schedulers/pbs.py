# Longbow is Copyright (C) of James T Gebbie-Rayet 2015.
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

"""."""

import logging
import os
import math
import corelibs.shellwrappers as shellwrappers

LOGGER = logging.getLogger("Longbow")

QUERY_STRING = "env | grep -i 'pbs' &> /dev/null"


def delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id: %s" + jobid)
    try:
        shellout = shellwrappers.sendtossh(host, ["qdel " + jobid])
    except:
        raise RuntimeError("  Unable to delete job.")

    LOGGER.info("  Deletion successful.")

    return shellout[0]


def prepare(hosts, jobname, jobs):

    """Create the PBS jobfile ready for submitting jobs"""

    LOGGER.info("  Creating submit file for job: %s", jobname)

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
    if jobs[jobname]["account"] is not "":
        jobfile.write("#PBS -A " + jobs[jobname]["account"] + "\n")

    # If user hasn't specified corespernode for under utilisation then
    # user the hosts max corespernode.
    if jobs[jobname]["nodes"] is not "":
        nodes = jobs[jobname]["nodes"]
    else:
        if jobs[jobname]["corespernode"] is not "":
            nodes = jobs[jobname]["cores"] / jobs[jobname]["corespernode"]
        else:
            nodes = int(jobs[jobname]["cores"]) / \
                int(hosts[jobs[jobname]["resource"]]["corespernode"])

        # Makes sure nodes is rounded up to the next highest integer.
        nodes = str(int(math.ceil(nodes)))

    # Number of cpus per node (most machines will charge for all whether you
    # are using them or not)
    ncpus = hosts[jobs[jobname]["resource"]]["corespernode"]

    # If user hasn't specified corespernode for the job (for under utilisation)
    # then default to hosts max corespernode (max utilised).
    if jobs[jobname]["corespernode"] is not "":
        mpiprocs = jobs[jobname]["corespernode"]
    else:
        mpiprocs = hosts[jobs[jobname]["resource"]]["corespernode"]

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

    # Set some environment variables for PBS.
    jobfile.write("\n"
                  "export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)\n"
                  "cd $PBS_O_WORKDIR\n"
                  "export OMP_NUM_THREADS=1\n"
                  "\n")

    # Load up modules if required.
    if jobs[jobname]["modules"] is not "":
        for module in jobs[jobname]["modules"].split(","):
            module.replace(" ", "")
            jobfile.write("module load %s\n\n" % module)

    # Handler that is used for job submission.
    mpirun = hosts[jobs[jobname]["resource"]]["handler"]

    # CRAY's use aprun which has slightly different requirements to mpirun.
    if mpirun == "aprun":
        mpirun = mpirun + " -n " + jobs[jobname]["cores"] + " -N " + mpiprocs

    # Single jobs only need one run command.
    if int(jobs[jobname]["batch"]) == 1:

        jobfile.write(mpirun + " " + jobs[jobname]["commandline"] + "\n")

    # Ensemble jobs need a loop.
    elif int(jobs[jobname]["batch"]) > 1:

        jobfile.write("basedir=$PBS_O_WORKDIR \n"
                      "for i in {1.." + jobs[jobname]["batch"] + "};\n"
                      "do\n"
                      "  cd $basedir/rep$i/\n"
                      "  " + mpirun + " " + jobs[jobname]["commandline"] +
                      " &\n"
                      "done\n"
                      "wait\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append pbs file to list of files ready for staging.
    jobs[jobname]["filelist"].extend(["submit.pbs"])
    jobs[jobname]["subfile"] = "submit.pbs"


def status(host, jobid):

    """Method for querying job."""

    state = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["qstat | grep " + jobid])

        stat = shellout[0].split()

        if stat[4] == "H":
            state = "Held"

        elif stat[4] == "Q":
            state = "Queued"

        elif stat[4] == "R":
            state = "Running"

    except RuntimeError:
        state = "Finished"

    return state


def submit(host, jobname, jobs):

    """Method for submitting a job."""

    path = os.path.join(jobs[jobname]["remoteworkdir"], jobname)
    # Change into the working directory and submit the job.
    cmd = ["cd " + path + "\n", "qsub " + jobs[jobname]["subfile"]]

    # Process the submit
    try:
        shellout = shellwrappers.sendtossh(host, cmd)[0]
    except:
        raise RuntimeError("  Something went wrong when submitting.")

    output = shellout.rstrip("\r\n")

    LOGGER.info("  Job: %s submitted with id: %s", jobname, output)

    jobs[jobname]["jobid"] = output
