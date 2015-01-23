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

"""This module containst the methods for preparing, submitting, deleting and
monitoring jobs. The following methods abstract the schedulers:

delete()
monitor()
prepare()
submit()

The remaining methods of the form env_method() are abstractions specific to
each scheduler, it is not recommended to use these directly unless it is
necessary.
"""

import time
import os
import logging
import sys
import math
import corelibs.shellwrappers as shellwrappers
import corelibs.configuration as config
import corelibs.staging as staging

LOGGER = logging.getLogger("Longbow")


def testenv(hostconf, hosts, jobs):

    """This method makes an attempt to test the environment and determine from
    a pre-configured list what scheduler and job submission handler is present
    on the machine."""

    schedulers = {"PBS": ["env | grep -i 'pbs' &> /dev/null"],
                  "LSF": ["env | grep -i 'lsf' &> /dev/null"],
                  "SGE": ["env | grep -i 'sge' &> /dev/null"]
                  }

    handlers = {"aprun": ["which aprun"],
                "mpirun": ["which mpirun"]
                }

    save = False

    # Take a look at each job.
    for job in jobs:

        resource = jobs[job]["resource"]

        # If we have no scheduler defined by the user then find it.
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
                    LOGGER.info("  The environment on this host is: %s", param)
                    break
                except RuntimeError:
                    LOGGER.debug("  Environment is not %s", param)

            # If we changed anything then mark for saving.
            save = True

        else:
            LOGGER.info("The environment on host: %s is %s", resource,
                        hosts[resource]["scheduler"])

        # If we have no job handler defined by the user then find it.
        if hosts[resource]["handler"] is "":
            LOGGER.info("No queue handler was specified for host %s - " +
                        "attempting to find it", resource)

            # Go through the handlers and find out which is there.
            for param in handlers:
                try:
                    shellwrappers.sendtossh(hosts[resource], handlers[param])
                    hosts[resource]["handler"] = param
                    LOGGER.info("  The batch queue handler is %s", param)
                    break
                except RuntimeError:
                    LOGGER.debug("  The batch queue handler is not %s", param)

            # If we changed anything then mark for saving.
            save = True

        else:
            LOGGER.info("The handler on host: %s is %s", resource,
                        hosts[resource]["handler"])

    # Do we have anything to change in the host file.
    if save is True:
        config.saveconfigs(hostconf, hosts)


def delete(hosts, jobs, jobname):

    """The generic method for deleting jobs."""

    if jobname == "All":

        for job in jobs:

            scheduler = hosts[jobs[job]["resource"]]["scheduler"]
            host = hosts[jobs[job]["resource"]]
            jobid = jobs[job]["jobid"]

            getattr(sys.modules[__name__], scheduler.lower() +
                    "_delete")(host, jobid)

    else:

        scheduler = hosts[jobs[jobname]["resource"]]["scheduler"]
        host = hosts[jobs[jobname]["resource"]]
        jobid = jobs[jobname]["jobid"]

        getattr(sys.modules[__name__], scheduler.lower() +
                "_delete")(host, jobid)


def monitor(hosts, jobs):

    """The generic method for monitoring jobs, this methods contains the
    monitoring loop and logic for keeping track of jobs and initiating
    staging of jobs."""

    LOGGER.info("Monitoring job/s")

    # Some initial values
    allfinished = False
    interval = 0

    # Find out which job has been set the highest polling frequency and use
    # that.
    for job in jobs:
        jobs[job]["laststatus"] = ""
        if interval < jobs[job]["frequency"]:
            interval = jobs[job]["frequency"]

    # Loop until all jobs are done.
    while allfinished is False:

        for job in jobs:

            if jobs[job]["laststatus"] != "Finished":

                machine = jobs[job]["resource"]
                scheduler = hosts[machine]["scheduler"]
                host = hosts[machine]

                # Get the job status.
                status = getattr(sys.modules[__name__], scheduler.lower() +
                                 "_status")(host, jobs[job]["jobid"])

                # If the last status is different then change the flag (stops
                # logfile getting flooded!)
                if jobs[job]["laststatus"] != status:
                    jobs[job]["laststatus"] = status
                    LOGGER.info("  Job: %s with id: %s is %s", job,
                                jobs[job]["jobid"], status)

                # If the job is running and we set the polling frequency higher
                # higher than 0 (off) then stage files.
                if jobs[job]["laststatus"] == "Running" and interval is not 0:
                    staging.stage_downstream(hosts, jobs, job)

                # If job is done then transfer files (this is to stop users
                # having to wait till all jobs end to grab last bit of staged
                # files.)
                if jobs[job]["laststatus"] == "Finished":
                    staging.stage_downstream(hosts, jobs, job)

        # Find out if all jobs are completed.
        for job in jobs:

            if jobs[job]["laststatus"] != "Finished":
                allfinished = False
                break

            allfinished = True

        # If we still have jobs running then wait here for desired time before
        # looping again.
        if allfinished is False:
            time.sleep(float(interval))

    LOGGER.info("All jobs are complete.")


def prepare(hosts, jobs):

    """The generic methods for preparing jobs, this points to the correct
    scheduler specific method for job preparation."""

    LOGGER.info("Creating submit files for job/s.")

    for job in jobs:

        scheduler = hosts[jobs[job]["resource"]]["scheduler"]

        getattr(sys.modules[__name__], scheduler.lower() +
                "_prepare")(hosts, job, jobs)

    LOGGER.info("Submit file/s created.")


def submit(hosts, jobs):

    """Generic method for submitting jobs, this points to the scheduler
    specific method for job submission."""

    LOGGER.info("Submitting job/s.")

    for job in jobs:

        machine = jobs[job]["resource"]
        scheduler = hosts[machine]["scheduler"]
        host = hosts[machine]

        getattr(sys.modules[__name__], scheduler.lower() +
                "_submit")(host, job, jobs)

    LOGGER.info("Submission complete.")


def pbs_delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id: %s" + jobid)
    try:
        shellout = shellwrappers.sendtossh(host, ["qdel " + jobid])
    except:
        raise RuntimeError("  Unable to delete job.")

    LOGGER.info("  Deletion successful.")

    return shellout[0]


def pbs_prepare(hosts, jobname, jobs):

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


def lsf_delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id: %s", jobid)

    try:
        shellout = shellwrappers.sendtossh(host, ["bkill " + jobid])
    except:
        raise RuntimeError("  Unable to delete job.")

    LOGGER.info("  Deletion successful")

    return shellout[0]


def lsf_prepare(hosts, jobname, jobs):

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

    if jobs[jobname]["account"] is not "":
        jobfile.write("#BSUB -P " + jobs[jobname]["account"] + "\n")

    jobfile.write("#BSUB -W " + jobs[jobname]["maxtime"] + "\n")

    # TODO: "#BSUB -n " + jobs[jobname]["cores"] + "\n")
    jobfile.write("#BSUB -n " + jobs[jobname]["cores"] + "\n")

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


def lsf_status(host, jobid):

    """Method for querying job."""

    status = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["bjobs | grep " + jobid])

        stat = shellout[0].split()

        if stat[2] == "PSUSP" or stat[2] == "USUSP" or stat[2] == "SSUSP":
            status = "Held"

        elif stat[2] == "PEND":
            status = "Queued"

        elif stat[2] == "RUN":
            status = "Running"

    except RuntimeError:
        status = "Finished"

    return status


def lsf_submit(host, jobname, jobs):

    """Method for submitting job."""

    # cd into the working directory and submit the job.
    path = os.path.join(jobs[jobname]["remoteworkdir"], jobname)
    cmd = ["cd " + path + "\n", "bsub < " +
           jobs[jobname]["subfile"] + "| grep -P -o '(?<=<)[0-9]*(?=>)'"]

    # Process the submit
    try:
        shellout = shellwrappers.sendtossh(host, cmd)[0]
    except:
        raise RuntimeError("  Something went wrong when submitting.")

    output = shellout.splitlines()[0]

    LOGGER.info("  Job: %s submitted with id: %s", jobname, output)

    jobs[jobname]["jobid"] = output


def sge_delete(host, jobid):

    """Method for deleting job."""

    LOGGER.info("Deleting the job with id: %s", jobid)
    try:
        shellout = shellwrappers.sendtossh(host, ["qdel " + jobid])
    except:
        raise RuntimeError("  Unable to delete job.")

    LOGGER.info("  Deleted successfully")

    return shellout[0]


def sge_prepare(hosts, jobname, jobs):

    """Create the SGE jobfile ready for submitting jobs"""

    LOGGER.info("  Creating submit file for job: %s", jobname)

    # Open file for LSF script.
    sgefile = os.path.join(jobs[jobname]["localworkdir"], "submit.sge")
    jobfile = open(sgefile, "w+")

    # Write the PBS script
    jobfile.write("#!/bin/bash --login\n"
                  "#$ -cwd -V")

    if jobname is not "":
        jobfile.write("#$ -N " + jobname + "\n")

    if jobs[jobname]["queue"] is not "":
        jobfile.write("#$ -q " + jobs[jobname]["queue"] + "\n")

    if jobs[jobname]["account"] is not "":
        jobfile.write("#$ -A " + jobs[jobname]["account"] + "\n")

    jobfile.write("#$ -l h_rt=" + jobs[jobname]["maxtime"] + ":00\n")

    # TODO: "#$ -pe ib " + jobs[jobname]["cores"] + "\n\n")

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


def sge_status(host, jobid):

    """Method for querying job."""

    status = ""

    try:
        shellout = shellwrappers.sendtossh(host, ["qstat | grep " + jobid])

        stat = shellout[0].split()

        if stat[4] == "h":
            status = "Held"

        elif stat[4] == "qw":
            status = "Queued"

        elif stat[4] == "r":
            status = "Running"

    except RuntimeError:
        status = "Finished"

    return status


def sge_submit(host, jobname, jobs):

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


def amazon_delete():

    """Delete call to Crossbow."""

    pass


def amazon_prepare():

    """Prepare call to Crossbow.."""

    pass


def amazon_status():

    """Status call to Crossbow.."""

    pass


def amazon_submit():

    """Submit call to Crossbow."""

    pass
