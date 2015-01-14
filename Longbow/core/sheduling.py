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

import time
import os
import logging
import core.shellwrappers as shellwrappers
import core.staging as staging

LOGGER = logging.getLogger("Longbow")


def testenv(hosts, jobs):

    """."""

    schedulers = {"PBS": ["env | grep -i 'pbs' &> /dev/null"],
                  "LSF": ["env | grep -i 'lsf' &> /dev/null"],
                  "SGE": ["env | grep -i 'sge' &> /dev/null"]
                  }

    save = False

    # Take a look at each job.
    for job in jobs:

        resource = jobs[job]["resource"]

        if hosts[resource]["scheduler"] is "":
            LOGGER.info("No environment for this host: %s "
                        % resource + "is specified - attempting " +
                        "to determine it!")

            # Go through the schedulers we are supporting.
            for param in schedulers:
                try:
                    shellwrappers.sendtossh(hosts[resource],
                                            schedulers[param])
                    hosts[resource]["scheduler"] = param
                    LOGGER.info("The environment on this host " +
                                "appears to be %s " % param)
                    break
                except RuntimeError:
                    LOGGER.debug("Environment is not %s", param)

            save = True

        else:
            LOGGER.info("The environment on host: %s is %s", resource,
                        hosts[resource]["scheduler"])

    return save


def delete(hosts, jobs):

    """."""

    for job in jobs:

        scheduler = hosts[jobs[job]["resource"]]["scheduler"]
        host = hosts[jobs[job]["resource"]]
        jobid = jobs[job]["jobid"]

        if scheduler == "PBS":
            pbs_delete(host, jobid)

        elif scheduler == "LSF":
            lsf_delete(host, jobid)

        elif scheduler == "SGE":
            sge_delete(host, jobid)

        elif scheduler == "AMAZON":
            amazon_delete()


def monitor(hosts, jobs):

    """."""

    LOGGER.info("Monitoring job/s")

    finished = False

    for job in jobs:
        jobs[job]["laststatus"] = ""

    while finished is False:

        for job in jobs:

            if jobs[job]["laststatus"] != "Finished":

                machine = jobs[job]["resource"]
                scheduler = hosts[machine]["scheduler"]
                host = hosts[machine]

                if scheduler == "PBS":
                    status = pbs_status(host, jobs[job]["jobid"])

                if scheduler == "LSF":
                    status = lsf_status(host, jobs[job]["jobid"])

                if scheduler == "SGE":
                    sge_status(host, jobs[job]["jobid"])

                if scheduler == "AMAZON":
                    amazon_status()

                if jobs[job]["laststatus"] != status:
                    jobs[job]["laststatus"] = status
                    LOGGER.info("  Job: %s with id: %s is %s", job,
                                jobs[job]["jobid"], status)

                if jobs[job]["laststatus"] == "Running":
                    staging.stage_downstream(hosts, jobs, job)

        for job in jobs:

            if jobs[job]["laststatus"] != "Finished":
                finished = False
                break

            finished = True

        time.sleep(float(60))

    LOGGER.info("All jobs are complete.")


def prepare(hosts, jobs):

    """."""

    for job in jobs:

        scheduler = hosts[jobs[job]["resource"]]["scheduler"]

        if scheduler == "PBS":
            pbs_prepare(job, jobs)

        elif scheduler == "LSF":
            lsf_prepare(job, jobs)

        elif scheduler == "SGE":
            sge_prepare(job, jobs)

        elif scheduler == "AMAZON":
            amazon_prepare()


def submit(hosts, jobs):

    """."""

    for job in jobs:

        machine = jobs[job]["resource"]
        scheduler = hosts[machine]["scheduler"]
        host = hosts[machine]

        if scheduler == "PBS":
            pbs_submit(host, job, jobs)

        elif scheduler == "LSF":
            lsf_submit(host, job, jobs)

        elif scheduler == "SGE":
            sge_submit(host, job, jobs)

        elif scheduler == "AMAZON":
            amazon_submit()


def pbs_delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id = " + jobid)
    try:
        shellout = shellwrappers.sendtossh(host, ["qdel " + jobid])
    except:
        raise RuntimeError("Unable to delete job.")

    LOGGER.info("Job with id = " + jobid +
                " was successfully deleted.")

    return shellout[0]


def pbs_prepare(jobname, jobs):

    """Create the PBS jobfile ready for submitting jobs"""

    LOGGER.info("Creating submit file for job: %s", jobname)

    # Open file for PBS script.
    pbsfile = os.path.join(jobs[jobname]["localworkdir"], "submit.pbs")
    jobfile = open(pbsfile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash \n"
                  "#PBS -N " + jobname + " \n"
                  "#PBS -l select=" + jobs[jobname]["nodes"] + " \n"
                  "#PBS -l walltime=" + jobs[jobname]["maxtime"] + ":00:00 \n"
                  "#PBS -A " + jobs[jobname]["account"] + "\n\n"
                  "export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR) \n"
                  "cd $PBS_O_WORKDIR \n"
                  "export OMP_NUM_THREADS=1 \n\n")

    if jobs[jobname]["modules"] is not "":
        for module in jobs[jobname]["modules"].split(","):
            module.replace(" ", "")
            jobfile.write("module load %s \n\n" % module)

    if int(jobs[jobname]["batch"]) == 1:

        jobfile.write("aprun -n " + jobs[jobname]["cores"] + " -N " +
                      jobs[jobname]["corespernode"] + " " +
                      jobs[jobname]["commandline"] + " \n")

    elif int(jobs[jobname]["batch"]) > 1:

        jobfile.write("basedir=$PBS_O_WORKDIR \n"
                      "for i in {1.." + jobs[jobname]["batch"] + "}; \n"
                      "do \n"
                      "  cd $basedir/rep$i/ \n"
                      "  aprun -n " + jobs[jobname]["cores"] + " -N " +
                      jobs[jobname]["corespernode"] + " " +
                      jobs[jobname]["commandline"] + " & \n"
                      "done \n"
                      "wait \n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append pbs file to list of files ready for staging.
    jobs[jobname]["filelist"].extend(["submit.pbs"])
    jobs[jobname]["subfile"] = "submit.pbs"

    LOGGER.info("  Complete")


def pbs_status(host, jobid):

    """Method for querying job."""

    status = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["qstat | grep " + jobid])

        stat = shellout[0].split()

        if stat[4] == "H":
            status = "Held"

        elif stat[4] == "Q":
            status = "Queued"

        elif stat[4] == "R":
            status = "Running"

    except RuntimeError:
        status = "Finished"

    return status


def pbs_submit(host, jobname, jobs):

    """Method for submitting a job."""

    LOGGER.info("Submitting the job: %s to the remote host.", jobname)
    path = os.path.join(jobs[jobname]["remoteworkdir"], jobname)
    # Change into the working directory and submit the job.
    cmd = ["cd " + path + "\n", "qsub " + jobs[jobname]["subfile"]]

    # Process the submit
    try:
        shellout = shellwrappers.sendtossh(host, cmd)[0]
    except:
        raise RuntimeError("Something went wrong when submitting.")

    output = shellout.rstrip("\r\n")

    LOGGER.info("  Job submitted with id = " + output)

    jobs[jobname]["jobid"] = output


def lsf_delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id = " + jobid)

    try:
        shellout = shellwrappers.sendtossh(host, ["bkill " + jobid])
    except:
        raise RuntimeError("Unable to delete job.")

    LOGGER.info("Job with id = " + jobid +
                " was successfully deleted.")

    return shellout[0]


def lsf_prepare(jobname, jobs):

    """Create the LSF jobfile ready for submitting jobs"""

    LOGGER.info("Creating submit file for job: %s", jobname)

    # Open file for LSF script.
    lsffile = os.path.join(jobs[jobname]["localworkdir"], "submit.lsf")
    jobfile = open(lsffile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash \n"
                  "#BSUB -J " + jobname + " \n"
                  "#BSUB -W " + jobs[jobname]["maxtime"] + ":00 \n"
                  "#BSUB -n " + jobs[jobname]["cores"] + "\n\n")

    if jobs[jobname]["modules"] is not "":
        for module in jobs[jobname]["modules"].split(","):
            module.replace(" ", "")
            jobfile.write("module load %s \n\n" % module)

    if int(jobs[jobname]["batch"]) == 1:

        jobfile.write("mpirun -lsf " + jobs[jobname]["corespernode"] + " " +
                      jobs[jobname]["commandline"] + " \n")

    elif int(jobs[jobname]["batch"]) > 1:

        jobfile.write("for i in {1.." + jobs[jobname]["batch"] + "}; \n"
                      "do \n"
                      "  cd rep$i/ \n"
                      "  mpirun -lsf " + jobs[jobname]["commandline"] + " & \n"
                      "done \n"
                      "wait \n")

    # Close the file (housekeeping)
    jobfile.close()

    # Append lsf file to list of files ready for staging.
    jobs[jobname]["filelist"].extend(["submit.lsf"])
    jobs[jobname]["subfile"] = "submit.lsf"

    LOGGER.info("  Complete")


def lsf_status(host, jobid):

    """Method for querying job."""

    status = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["bjobs | grep " + jobid])

        stat = shellout[0].split()

        if stat[4] == "PSUSP" or stat[4] == "USUSP" or stat[4] == "SSUSP":
            status = "Held"

        elif stat[4] == "PEND":
            status = "Queued"

        elif stat[4] == "RUN":
            status = "Running"

    except RuntimeError:
        status = "Finished"

    return status


def lsf_submit(host, jobname, jobs):

    """Method for submitting job."""

    LOGGER.info("Submitting the job: %s to the remote host.", jobname)

    # cd into the working directory and submit the job.
    path = os.path.join(jobs[jobname]["remoteworkdir"], jobname)
    cmd = ["cd " + path + "\n", "qsub " +
           jobs[jobname]["subfile"] + "| grep -P -o '(?<=<)[0-9]*(?=>)'"]

    # Process the submit
    try:
        shellout = shellwrappers.sendtossh(host, cmd)[0]
    except:
        raise RuntimeError("Something went wrong when submitting.")

    output = shellout.splitlines()[0]

    LOGGER.info("  Job submitted with id = " + output)

    jobs[jobname]["jobid"] = output


def sge_delete(host, jobid):

    """."""

    print host, jobid


def sge_prepare(jobname, jobs):

    """."""

    print jobname, jobs


def sge_status(host, jobid):

    """."""

    print host, jobid


def sge_submit(host, jobname, jobs):

    """."""

    print host, jobname, jobs


def amazon_delete():

    """."""

    pass


def amazon_prepare():

    """."""

    pass


def amazon_status():

    """."""

    pass


def amazon_submit():

    """."""

    pass
