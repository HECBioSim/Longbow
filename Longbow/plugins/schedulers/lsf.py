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
import corelibs.exceptions as ex
import corelibs.shellwrappers as shellwrappers

LOGGER = logging.getLogger("Longbow")

QUERY_STRING = "env | grep -i 'lsf'"


def delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id: %s", jobid)

    try:
        shellout = shellwrappers.sendtossh(host, ["bkill " + jobid])

    except ex.SSHError:
        raise ex.JobdeleteError("  Unable to delete job.")

    LOGGER.info("  Deletion successful")

    return shellout[0]


def prepare(hosts, jobname, jobs):

    """Create the LSF jobfile ready for submitting jobs"""

    LOGGER.info("  Creating submit file for job: %s", jobname)

    # Open file for LSF script.
    lsffile = os.path.join(jobs[jobname]["localworkdir"], "submit.lsf")
    jobfile = open(lsffile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n")

    if jobname is not "":
        jobfile.write("#BSUB -J " + jobname + "\n")

    if jobs[jobname]["queue"] is not "":
        jobfile.write("#BSUB -q " + jobs[jobname]["queue"] + "\n")

    if jobs[jobname]["cluster"] is not "":
        jobfile.write("#BSUB -m " + jobs[jobname]["cluster"] + "\n")

    # Account to charge (if supplied).
    if hosts[jobs[jobname]["resource"]]["account"] is not "":
        # if no accountflag is provided use the default
        if hosts[jobs[jobname]["resource"]]["accountflag"] is "":
            jobfile.write("#BSUB -P " +
                          hosts[jobs[jobname]["resource"]]["account"] +
                          "\n")
        else:
            jobfile.write("#BSUB " +
                          hosts[jobs[jobname]["resource"]]["accountflag"] +
                          " " + hosts[jobs[jobname]["resource"]]["account"] +
                          "\n")

    jobfile.write("#BSUB -W " + jobs[jobname]["maxtime"] + "\n")

    jobfile.write("#BSUB -n " + hosts[jobs[jobname]["resource"]]["cores"] +
                  "\n")

    if jobs[jobname]["modules"] is not "":
        for module in jobs[jobname]["modules"].split(","):
            module.replace(" ", "")
            jobfile.write("\n" + "module load %s\n\n" % module)

    mpirun = hosts[jobs[jobname]["resource"]]["handler"]

    if int(jobs[jobname]["batch"]) == 1:

        jobfile.write(mpirun + " -lsf " + jobs[jobname]["commandline"] + "\n")

    elif int(jobs[jobname]["batch"]) > 1:

        jobfile.write("for i in {1.." + jobs[jobname]["batch"] + "};\n"
                      "do\n"
                      "  cd rep$i/\n"
                      "  " + mpirun + " -lsf " + jobs[jobname]["commandline"] +
                      " &\n"
                      "done\n"
                      "wait\n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append lsf file to list of files ready for staging.
    jobs[jobname]["filelist"].extend(["submit.lsf"])
    jobs[jobname]["subfile"] = "submit.lsf"


def status(host, jobid):

    """Method for querying job."""

    state = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["bjobs -u " + host["user"] +
                                                  " | grep " + jobid])

        stat = shellout[0].split()

        if stat[2] == "PSUSP" or stat[2] == "USUSP" or stat[2] == "SSUSP":
            state = "Held"

        elif stat[2] == "PEND":
            state = "Queued"

        elif stat[2] == "RUN":
            state = "Running"

    except ex.SSHError:
        state = "Finished"

    return state


def submit(host, jobname, jobs):

    """Method for submitting job."""

    # Set the path to remoteworkdir/jobname
    path = os.path.join(host["remoteworkdir"], jobname)

    # cd into the working directory and submit the job.
    cmd = ["cd " + path + "\n", "bsub < " +
           jobs[jobname]["subfile"] + "| grep -P -o '(?<=<)[0-9]*(?=>)'"]

    # Process the submit
    try:
        shellout = shellwrappers.sendtossh(host, cmd)[0]

    except ex.SSHError:
        raise ex.JobsubmitError("  Something went wrong when submitting.")

    output = shellout.splitlines()[0]

    LOGGER.info("  Job: %s submitted with id: %s", jobname, output)

    jobs[jobname]["jobid"] = output
