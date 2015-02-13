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
import math
import os
import corelibs.shellwrappers as shellwrappers

LOGGER = logging.getLogger("Longbow")

QUERY_STRING = "env | grep -i 'sge' &> /dev/null"


def delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id: %s", jobid)
    try:
        shellout = shellwrappers.sendtossh(host, ["qdel " + jobid])
    except:
        raise RuntimeError("  Unable to delete job.")

    LOGGER.info("  Deleted successfully")

    return shellout[0]


def prepare(hosts, jobname, jobs):

    """Create the SGE jobfile ready for submitting jobs"""

    LOGGER.info("  Creating submit file for job: %s", jobname)

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

    if jobs[jobname]["account"] is not "":
        if hosts[jobs[jobname]["resource"]]["accountflag"] is "":
            jobfile.write("#$ -A " + jobs[jobname]["account"] + "\n")
        else:
            jobfile.write("#$ " +
                          hosts[jobs[jobname]["resource"]]["accountflag"] +
                          " " + jobs[jobname]["account"] + "\n")

    jobfile.write("#$ -l h_rt=" + jobs[jobname]["maxtime"] + ":00:00\n")

    cores = jobs[jobname]["cores"]

    if jobs[jobname]["corespernode"] is not "":
        cpn = jobs[jobname]["corespernode"]
    elif hosts[jobs[jobname]["resource"]]["corespernode"] is not "":
        cpn = hosts[jobs[jobname]["resource"]]["corespernode"]
    else:
        raise RuntimeError("parameter 'corespernode' was not set in either " +
                           "the host nor job configuration files.")

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

    tmp = "select=" + nodes

    # Write the resource requests
    jobfile.write("#PBS -l " + tmp + "\n")

    # TODO: "#$ -pe ib " + jobs[jobname]["cores"] + "\n\n")
    jobfile.write("#$ -pe ib " + jobs[jobname]["cores"] + "\n\n")

    if jobs[jobname]["modules"] is not "":
        for module in jobs[jobname]["modules"].split(","):
            module.replace(" ", "")
            jobfile.write("module load %s\n\n" % module)

    mpirun = hosts[jobs[jobname]["resource"]]["handler"]

    if int(jobs[jobname]["batch"]) == 1:

        jobfile.write(mpirun + " " + jobs[jobname]["commandline"] + "\n")

    elif int(jobs[jobname]["batch"]) > 1:

        jobfile.write("for i in {1.." + jobs[jobname]["batch"] + "};\n"
                      "do\n"
                      "  cd rep$i/\n"
                      "  " + mpirun + jobs[jobname]["commandline"] +
                      " &\n"
                      "done\n"
                      "wait\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append lsf file to list of files ready for staging.
    jobs[jobname]["filelist"].extend(["submit.sge"])
    jobs[jobname]["subfile"] = "submit.sge"


def status(host, jobid):

    """Method for querying job."""

    state = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["qstat | grep " + jobid])

        stat = shellout[0].split()

        if stat[4] == "h":
            state = "Held"

        elif stat[4] == "qw":
            state = "Queued"

        elif stat[4] == "r":
            state = "Running"

    except RuntimeError:
        state = "Finished"

    return state


def submit(host, jobname, jobs):

    """Method for submitting a job."""

    path = os.path.join(jobs[jobname]["remoteworkdir"], jobname)
    # Change into the working directory and submit the job.
    cmd = ["cd " + path + "\n", "qsub " + jobs[jobname]["subfile"] +
           "| grep -P -o '(?<= )[0-9]*(?= )'"]

    # Process the submit
    try:
        shellout = shellwrappers.sendtossh(host, cmd)[0]
    except:
        raise RuntimeError("  Something went wrong when submitting.")

    LOGGER.info("  Job: %s submitted with id: %s", jobname, shellout)

    jobs[jobname]["jobid"] = shellout
