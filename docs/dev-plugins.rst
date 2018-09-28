Writing Plugins
***************

The longbow plugins are the way we chose to incorporate software/scheduler specific features into an otherwise generically written library. The scope of this guide will cover how to create a whole new plugin within an existing category of plugins. The reason that creating new categories of plugins is not covered here is because to do so, the core of Longbow would have to be modified thus would not be update safe unless you submitted your changes to us and they get accepted into the core code. If making entirely new classes of plugins interests you, then please do get in touch so that we can sort out the details and support your plugins.

Plugins are used within Longbow to extend its functionality and support to new scheduling platforms and to support new applications. In this section of the guide we will look at how to create new plugins for both new applications and new schedulers. If you do write a plugin or many plugins, and feel others would benefit from them, get in touch, we would be happy to add them into Longbow core, it doesn't matter how messy or incomplete your code is as we will help.

Application Plugins
===================

Whilst it is not neccessary to have an application plugin to launch Longbow jobs for a given application, they help when things go wrong. Application plugins help Longbow to understand what basic command-line arguments an executable needs, what the common executable names are and there are "hooks" from within Longbow core that allow basic functions to be called to check that files exist that are called inside input files on the command-line.

If a plugin does not exist then Longbow will simply try and submit a job given the command-line it was launched with, if there are files missing, or there is a typo, this might not become apparent until a decent amount of time has been wasted following error messages. These plugins help to eliminate this process entirely, plugins are also useful for beginners just starting out with HPC as they can pick out some of the basic mistakes that these types of users make.

To create a new applications plugin, follow these simple steps:

Create a new plugin file. This file should be a python file and should be placed inside the apps directory of the longbow source directory, and should be named after the application (currently Longbow uses this name to derive its default module to load).

Create the EXECDATA dictionary with the following format::

    EXECDATA = {
        "executable": {
            "subexecutables": [],
            "requiredfiles": []
        }
    }

Where you will replace "executable" with the name of the executable, if there are sub-executables such as like those in the GROMACS packages then provide a comma separated list between the square brackets, and add a comma seperated list of flags for required files so that Longbow can check they are provided at runtime.

There are a number of special cases for the "requiredfiles" parameter:

    a. In cases where the command-line uses piped input or if the only argument is the input file, simply add "<" to the list of required files.
    b. In cases where either one of a number of parameters can be given use the "||" operator between two parameters.
 
A number of examples have been given below to illustrate the above process.

The EXECDATA dictionary provided as part of the AMBER plugin::

    EXECDATA = {
        "pmemd": {
            "subexecutables": [],
            "requiredfiles": ["-c", "-i", "-p"],
        },
        "pmemd.MPI": {
            "subexecutables": [],
            "requiredfiles": ["-c", "-i", "-p"],
        },
            "pmemd.cuda": {
            "subexecutables": [],
            "requiredfiles": ["-c", "-i", "-p"],
        }
    }

The EXECDATA dictionary provided as part of the GROMACS plugin::

    EXECDATA = {
        "gmx": {
            "subexecutables": ["mdrun", "mdrun_mpi"],
            "requiredfiles": ["-s || -deffnm"],
        },
        "gmx_d": {
            "subexecutables": ["mdrun", "mdrun_mpi"],
            "requiredfiles": ["-s || -deffnm"],
        },
        "mdrun": {
            "subexecutables": [],
            "requiredfiles": ["-s || -deffnm"],
        },
        "mdrun_d": {
            "subexecutables": [],
            "requiredfiles": ["-s || -deffnm"],
        },
        "mdrun_mpi": {
            "subexecutables": [],
            "requiredfiles": ["-s || -deffnm"],
        },
        "mdrun_mpi_d": {
            "subexecutables": [],
            "requiredfiles": ["-s || -deffnm"],
        }
    }

The EXECDATA dictionary provided as part of the NAMD plugin::

    EXECDATA = {
        "namd2": {
            "subexecutables": [],
            "requiredfiles": ["<"],
        },
        "namd2.mpi": {
            "subexecutables": [],
            "requiredfiles": ["<"],
        },
        "namd2.cuda": {
            "subexecutables": [],
            "requiredfiles": ["<"],
        }
    }

Adding new plugins in this fashion should provide an easy way to add support for new applications. We would like to encourage contributions from fields other than computational biology so that we can start to increase our domain of support out of the box.

Scheduler Plugins
=================

To have Longbow run jobs on schedulers that are not supported out of the box, it is necessary to write plugins to tell Longbow how to submit to this new scheduling system and then do basic tasks such as query the status etc. Whilst we endeavour to make our best effort to support fully the main schedulers, new ones crop up all the time and users might find themselves needing to write plugins to make use of say a new local machine. 

To get started creating a new scheduler plugin, you will first have to create a new python file within the schedulers directory of the Longbow install (usually will be in .local/lib/python2.7/site-packages/longbow/schedulers/). It is recommended that you name this file after the scheduler to make things easier to remember. Once you have done this, the following snippets of code will explain how to build up the plugin.

Firstly copy and paste the following block of code at the top of your newly created python file::

    # Imports should go here
    import os

    # A query to the environment that will test positive for
    # this scheduler
    QUERY_STRING = "unique query here."

You'll notice that there is a reserved place at the top for imports, as you are building up your plugin and need to import modules, then please add these here, this will keep things tidy should things go wrong.

Next up is the "QUERY_STRING" parameter. This should be a bash query that enables Longbow to detect the scheduler within the linux environment, usually the scheduler will have created many different environment variables so you should normally be able to build this with 'env' and 'grep'. For example, the PBS query string is "env | grep -i 'pbs'".

**The delete job function**
 
Next up is the function to allow Longbow to kill jobs. Copy and paste the following block below what you have done from above::

    def delete(job):
        """A Method for deleting a single job."""
        jobid = job["jobid"]

        # Try and delete the job, otherwise raise job delete exception.
        try:

            shellout = shellwrappers.sendtossh(job, ["bkill " + jobid])

        except exceptions.SSHError:

            raise exceptions.JobdeleteError("Unable to delete job.")

        return shellout[0]

The above code block contains the code for a delete function, Longbow will pass this function a job dictionary with all of the parameters for that current job. Usually though, for most schedulers, deleting simply requires the jobid in a simple bash kill command. The simplest way to do this is to use the above example, and modify the '"bkill " + jobid' part of the delete command to use the syntax of how you would normally delete a job in a command terminal window.

**The prepare script function**

The next step is to create the function that will allow Longbow to write job submit files for this new scheduler. Copy the following code block below what you have already done from above::

    def prepare(job):
        """Create the LSF jobfile ready for submitting jobs"""

        # Open file for script.
        lsffile = os.path.join(job["localworkdir"], "submit.extension")
        jobfile = open(lsffile, "w+")

        # Write the script
        jobfile.write("#!/bin/bash --login\n")

        # Your code here.

        # Append submitfile to list of files ready for staging.
        job["subfile"] = "submit.extension" # IMPORTANT

This method is slightly more tricky, we have included the bioler-plate for creating the submit file and then appending it to the job data structure. You will need to do several things here, firstly you can change the extension in "submit.extension" to match that of the scheduler name for example, submit.pbs or submit.sge etc. Then you will need to add in the logic to create your submission files where the text "# Your code here." appears. The best way to write one of these functions is to firstly look at the existing plugins for other schedulers, then grab one of your previously made job submit scripts and start to pull out the key parts, such as the scheduler directives and then the submission part. You will find that by using existing plugins, your own submit scripts and the documentation for the Longbow data structures will easily allow you to write this part.

**The job status function**

Next up is the method to allow Longbow to grab the status of a job. Copy and paste the following code block below what you have done from above::

    def status(job):
        """Method for querying job."""

        # Dictionary of states a job can take in the scheduler,
        # mapped onto Longbow states.
        states = {
            "DONE": "Job Exited Properly",
            "EXIT": "Job Exited in Error",
            "PEND": "Queued",
            "PSUSP": "Suspended",
            "RUN": "Running",
            "SSUSP": "Suspended",
            "UNKWN": "Unknown Status",
            "USUSP": "Suspended",
            "WAIT": "Waiting for Start Time",
            "ZOMBI": "Zombie Job"
        }

        # Initialise job state to blank.
        jobstate = ""

        # Query the job state
        shellout = shellwrappers.sendtossh(job, ["bjobs -u " + job["user"]])

        # Scheduler will return a table, so split lines into a list.
        stdout = shellout[0].split("\n")

        # Loop over jobs in table.
        for line in stdout:

            # Split each line into its columns.
            line = line.split()

            # If the job id of our job is present in column 0.
            if len(line) > 0 and job["jobid"] in line[0]:

                # Read the jobstate from column 2 and exit loop.
                jobstate = states[line[2]]
                break

        # If jobstate is still blank, then it must have finished.
        if jobstate == "":

            jobstate = "Finished"

        return jobstate

The code above gives a good example of how to get the status from the scheduler, this code was taken from the LSF plugin already supplied with Longbow, you will have to modify this to work with your scheduler. A few important points to note:

1. The states dictionary, will need to be updated to reflect the states that your new scheduler uses, the left hand column containing "PEND" and "RUN" are the scheduler states, and those on the right are Longbow states. Currently, only the "Queued" and "Running" states are required, so all of the other states can in theory be omitted, although then Longbow would not be able to report on them, it is better to include them where possible.

2. The following line::

    shellout = shellwrappers.sendtossh(job, ["bjobs -u " + job["user"]])


Will need to be modified, you will need to change the last part "bjobs -u " + job["user"] within the square brackets (important that the outer square brackets remain) to match the command you would normally type into your terminal to query all jobs running under your user id (the user query gives nicer and more generic output than per jobid).

3. The following lines::

    # If the job id of our job is present in column 0.
    if len(line) > 0 and job["jobid"] in line[0]:

        # Read the jobstate from column 2 and exit loop.
        jobstate = states[line[2]]
        break


Will need to be modified to take account for any difference in how the data is returned by the scheduler. This code is assuming the job id appears in column 0 and that the state appears in column 2, these will both have to be corrected if this is not the case.

**The job submit function**

Next up is the method Longbow will use to submit jobs to the scheduler. Copy the following block of code below what you have done from above::

    def submit(job):
        """A method to submit a job."""
        # command to change into working directory and then submit the job.
        cmd = ["cd " + job["destdir"] + "\n", "bsub < " + job["subfile"]]

        try:

            # Send the submit command.
            shellout = shellwrappers.sendtossh(job, cmd)

        except exceptions.SSHError as inst:

            # If we have hit a queue limit, raise a special exception to trigger
            # subqueuing (not all machines will have this setup).
            if "limit" in inst.stderr:

                raise exceptions.QueuemaxError

            # Otherwise raise a submission exception and attach error information.
            else:

                raise exceptions.JobsubmitError(
                    "Something went wrong when submitting. The following output "
                    "came back from the SSH call:\nstdout: {0}\nstderr {1}"
                    .format(inst.stdout, inst.stderr))

        try:

            # Do the regex to extract the job id.
            jobid = re.search(r'\d+', shellout[0]).group()

        except AttributeError:

            raise exceptions.JobsubmitError(
                "Could not detect the job id during submission, this means that "
                "either the submission failed in an unexpected way, or that "
                "Longbow could not understand the returned information.")

        # Put jobid into the job dictionary.
        job["jobid"] = jobid

The above code block shows the basic layout of how a submit method should work. There are a number of ways this method can be adapted:

1. Firstly the line::

    cmd = ["cd " + job["destdir"] + "\n", "bsub < " + job["subfile"]]


Should be modified so that the second part with the bsub command, matches the command that your scheduler normally uses to submit jobs to its queue.

2. If the machine that you are using, or you know the scheduler doesn't support queue slot limits, then you can remove the following block of code::

    # If we have hit a queue limit, raise a special exception to trigger
    # subqueuing (not all machines will have this setup).
    if "limit" in inst.stderr:

        raise exceptions.QueuemaxError


and just raise the job submit error without an if/else.

3. In the same way the code in point 2 was deleted, you can also add extra checks to this to check for common scheduler errors and raise the job submit exception with a custom error message. This is useful for example, if there is an obscure error that keeps tripping you up and forcing you to read the scheduler documentation to find out what it means. See the pbs plugin for examples of this.

4. If the following line fails to extract the job id from what is returned::

    jobid = re.search(r'\d+', shellout[0]).group()

Then you will need to write your own parsing line.
 
All of the above steps should get you well on your way to producing a new scheduler plugin, if any of the documentation above is not clear, or you need help then please get in touch for support through our support channels.

 
