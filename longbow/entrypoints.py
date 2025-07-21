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

"""This module contains the Longbow entry points and supporting methods.

The following gives a summary of the methods available:

main()
    This method is the main entry point for Longbow launched as an application.
    Library users should not use this method when linking Longbow at a high
    level. Developers should be calling Longbowmain() directly with the
    parameters dictionary already setup.

longbowmain(parameters)
    This method is the upper level method of the Longbow library. Users
    interested in integrating Longbow into their applications without fine
    grain control may invoke this method, along with creating the data
    structures that the main entry point of the application would normally
    create.

recover(recoveryfile)
    This method is for attempting to recover a Longbow session. This should be
    used in cases where jobs have been submitted to the host and somehow
    Longbow failed to stay connected. This will try to take the recovery file,
    written shortly after submission to recover the whole session. Jobs that
    are no longer in the queue will be marked as finished and will be staged
    as normal.
"""

import os
import sys
import logging
import subprocess

import longbow.applications as applications
import longbow.apps as apps
import longbow.configuration as configuration
import longbow.exceptions as exceptions
import longbow.scheduling as scheduling
import longbow.shellwrappers as shellwrappers
import longbow.staging as staging

PYTHONVERSION = "{0}.{1}".format(sys.version_info[0], sys.version_info[1])
LONGBOWVERSION = "1.5.3-dev"

LOG = logging.getLogger("longbow")


def launcher():
    """Entry point for Longbow when used as an application.

    This method is the main entry point for Longbow launched as an application.
    Library users should not use this method when linking Longbow at a high
    level. Developers doing high level linking should be calling Longbow()
    directly with the parameters dictionary already setup.

    This method takes the information from sys.argv and processes this into a
    dictionary format ready to fire longbow().

    """
    # -------------------------------------------------------------------------
    # Some defaults and parameter initialisation

    # Fetch command line arguments as list and remove longbow exec
    commandlineargs = sys.argv
    commandlineargs.pop(0)

    # Initialise parameters that could alternatively be provided in
    # configuration files
    parameters = {
        "debug": False,
        "disconnect": False,
        "executable": "",
        "executableargs": "",
        "hosts": "",
        "job": "",
        "jobname": "",
        "log": "",
        "maxtime": "",
        "nochecks": False,
        "recover": "",
        "resource": "",
        "replicates": "",
        "update": "",
        "verbose": False
    }

    # Specify all recognised longbow arguments
    alllongbowargs = [
        "--about",
        "--debug",
        "--disconnect",
        "--examples",
        "-h",
        "--help",
        "--hosts",
        "--job",
        "--jobname",
        "--log",
        "--maxtime",
        "--nochecks",
        "--recover",
        "--resource",
        "--replicates",
        "--update",
        "-V",
        "--verbose",
        "--version"
    ]

    # -------------------------------------------------------------------------
    # Detection of commandline flags and sub functionality.

    # Detect Longbow arguments, the executable and the executable arguments
    # from the command-line.
    longbowargs = _commandlineproc(alllongbowargs, commandlineargs, parameters)

    # Check for information flags such as help or about
    _messageflags(longbowargs)

    # Check if user is wanting to download examples
    _downloadexamples(longbowargs)

    # Grab the Longbow command-line arguments and their values.
    _parsecommandlineswitches(parameters, longbowargs)

    # Logging should be started here, such that only users of the application
    # have logging rules and filters setup. Library users will want/need to
    # set up their own handlers.
    _setuplogger(parameters)

    # -------------------------------------------------------------------------
    # Setup the top level exception handler, this handler should give the user
    # nicely formatted and understandable error messages (unless run in debug
    # mode).

    # The top level exception handler, this level is simply for the graceful
    # exit and final reporting of errors only. All actions should have been
    # taken by this stage.
    try:

        # Log the start up message, if the user got this far then we are ok to
        # properly start Longbow.
        LOG.info("Welcome to Longbow!")
        LOG.info("This software was developed as part of the EPSRC-funded "
                 "HECBioSim project (http://www.hecbiosim.ac.uk/)")
        LOG.info("HECBioSim facilitates high-end biomolecular simulation "
                 "on resources such as ARCHER")
        LOG.info("Longbow is Copyright (C) of Science and Technology "
                 "Facilities Council and The University of Nottingham.")
        LOG.info("Longbow was created by Dr James T. Gebbie-Rayet, Dr Gareth "
                 "B. Shannon and Prof Charles A. Laughton.")
        LOG.info("Please cite our paper: Gebbie-Rayet, J, Shannon, G, "
                 "Loeffler, H H and Laughton, C A 2016 Longbow: A "
                 "Lightweight Remote Job Submission Tool. Journal of "
                 "Open Research Software, 4: e1, "
                 "DOI: http://dx.doi.org/10.5334/jors.95")
        LOG.info("Python version: %s", PYTHONVERSION)
        LOG.info("Longbow version: %s", LONGBOWVERSION)
        LOG.info("Longbow Commandline: %s", (" ").join(sys.argv))

        _hostfileproc(parameters)
        _jobfileproc(parameters)

        LOG.info("hosts file is: '%s'", parameters["hosts"])

        # If no executable and jobfile has been given then fail.
        if (parameters["executable"] == "" and parameters["job"] == "" and
                parameters["recover"] == "" and parameters["update"] == ""):

            raise exceptions.RequiredinputError(
                "There was no executable or job file given on the "
                "command-line, you need to supply one or the other otherwise "
                "Longbow cannot decipher what you would like to do.")

        # ---------------------------------------------------------------------
        # Call one of the main methods at the top level of the library.

        jobs = {}

        # If recovery or update mode is not active then this is a new run.
        if parameters["recover"] == "" and parameters["update"] == "":

            LOG.info("Initialisation complete.")

            longbow(jobs, parameters)

        # If recovery mode is set then start the recovery process.
        elif parameters["recover"] != "" and parameters["update"] == "":

            LOG.info("Starting recovery mode to reconnect monitoring of jobs.")

            recovery(jobs, parameters["recover"])

        # If update mode is set then start the update process.
        elif parameters["recover"] == "" and parameters["update"] != "":

            LOG.info("Starting update mode to refresh progress of jobs.")

            update(jobs, parameters["update"])

        # If too many arguments are set, we have a problem
        else:

            raise exceptions.CommandlineargsError(
                "You have both the --recover and --update command-line flags "
                "set, these cannot be used together as they enable "
                "conflicting functionality. Either reconnect with persistent "
                "monitoring (--recover) or reconnect to refresh the status of "
                "jobs and sync current files before disconnecting again "
                "(--update).")

    # If the user interrupts Longbow then they are aborting the jobs, so kill
    # off any running jobs and then remove the job directories. Otherwise just
    # raise all other errors to the top level where in future we can attempt to
    # recover.
    except KeyboardInterrupt:

        LOG.info("User interrupt detected.")

        if len([a for a in jobs if "lbowconf" not in a]) >= 1:

            LOG.info("Kill any queued or running jobs and clean up.")

            # If we are exiting at this stage then we need to kill off
            for item in [a for a in jobs if "lbowconf" not in a]:

                job = jobs[item]

                if "laststatus" in job:

                    # If job is not finished delete and stage.
                    if (job["laststatus"] != "Complete" and
                            job["laststatus"] != "Finished" and
                            job["laststatus"] != "Submit Error"):

                        # Kill it.
                        scheduling.delete(job)

                        # Transfer the directories as they are.
                        staging.stage_downstream(job)

                    # Job is finished then just stage.
                    elif job["laststatus"] != "Submit Error":

                        # Transfer the directories as they are.
                        staging.stage_downstream(job)

            staging.cleanup(jobs)

    # If disconnect mode is enabled then the disconnect exception is raised,
    # allow to disconnect gracefully.
    except exceptions.DisconnectException:

        LOG.info("User specified --disconnect flag on command-line, so "
                 "Longbow will exit.")
        LOG.info("You can reconnect this session for persistent monitoring by "
                 "using the recovery file:")
        LOG.info("longbow --recover {0} --verbose"
                 .format(jobs["lbowconf"]["recoveryfile"]))
        LOG.info("Or an update of current progress followed by disconnecting "
                 "can be done using:")
        LOG.info("longbow --update {0} --verbose"
                 .format(jobs["lbowconf"]["recoveryfile"]))

    # If disconnect mode is enabled then the disconnect exception is raised,
    # allow to disconnect gracefully.
    except exceptions.UpdateExit:

        LOG.info("Update of current job progress has completed, exiting.")
        LOG.info("You can reconnect this session for persistent monitoring by "
                 "using the recovery file:")
        LOG.info("longbow --recover {0} --verbose"
                 .format(jobs["lbowconf"]["recoveryfile"]))
        LOG.info("Or an update of current progress followed by disconnecting "
                 "can be done using:")
        LOG.info("longbow --update {0} --verbose"
                 .format(jobs["lbowconf"]["recoveryfile"]))

    # If a problem happens assign the correct level of debug logging.
    except Exception as err:

        if parameters["debug"] is True:

            LOG.exception(err)

        else:

            LOG.error(err)

        exit(1)

    # Show nice exit message.
    finally:

        LOG.info("Good bye from Longbow!")
        LOG.info("Check out http://www.hecbiosim.ac.uk/ for other "
                 "powerful biomolecular simulation software tools.")


def longbow(jobs, parameters):
    """Entry point at the top level of the Longbow library.

    Being the top level method that makes calls on the Longbow library.
    This is a good place to link against Longbow if a developer does not want
    to link against the executable, or if low level linking is not needed or is
    over-kill.

    Required inputs are:
    parameters (dictionary): A dictionary containing the parameters and
                             overrides from the command-line.

    """
    # A failure at this level will result in jobs being killed off before
    # escalating the exception to trigger graceful exit.

    # Load configurations and initialise Longbow data structures.
    jobparams = configuration.processconfigs(parameters)

    # Copy to jobs so when exceptions are raised the structure is available.
    for param in jobparams:

        jobs[param] = jobparams[param]

    # Test all connection/s specified in the job configurations
    shellwrappers.checkconnections(jobs)

    # Test the hosts listed in the jobs configuration file have their
    # scheduler environments listed, if not then test and save them.
    scheduling.checkenv(jobs, parameters["hosts"])

    # Test that for the applications listed in the job configuration
    # file are available and that the executable is present.
    if parameters["nochecks"] is False:

        applications.checkapp(jobs)

    # Process the jobs command line arguments and find files for
    # staging.
    applications.processjobs(jobs)

    # Create jobfile and add it to the list of files that needs
    # uploading.
    scheduling.prepare(jobs)

    # Stage all of the job files along with the scheduling script.
    staging.stage_upstream(jobs)

    # Submit all jobs.
    scheduling.submit(jobs)

    # Process the disconnect function.
    if parameters["disconnect"] is True:

        raise exceptions.DisconnectException

    # Monitor all jobs.
    scheduling.monitor(jobs)

    # Clean up all jobs
    staging.cleanup(jobs)


def recovery(jobs, recoveryfile):
    """Recover a Longbow session.

    This method is for attempting to recover a failed Longbow session or to
    reconnect to an intentionally disconnected session. It will try to take the
    recovery file, written shortly after submission to recover the whole
    session. Once the data has been loaded from the recovery file and a new job
    data structure populated, this method will then re-enter the monitoring
    function to continue where it left off. Any jobs that finished in the
    meantime will be marked accordingly and then file staging will continue.

    Required inputs are:
    recoveryfile (string): A path to the recovery file.

    """

    jobfile = os.path.join(os.path.expanduser('~/.longbow'), recoveryfile)

    LOG.info("Attempting to find the recovery file '{0}'".format(jobfile))

    # Load the jobs recovery file.
    if os.path.isfile(jobfile):

        LOG.info("Recovery file found.")

        _, _, jobparams = configuration.loadconfigs(jobfile)

        # Copy to jobs so when exceptions are raised the structure is
        # available.
        for param in jobparams:

            jobs[param] = jobparams[param]

    else:

        raise exceptions.RequiredinputError(
            "Recovery file could not be found, make sure you haven't deleted "
            "the recovery file and that you are not providing the full path, "
            "just the file name is needed.")

    # Rejoin at the monitoring stage. This will assume that all jobs that
    # are no longer in the queue have completed.
    scheduling.monitor(jobs)

    # Cleanup the remote working directory.
    staging.cleanup(jobs)


def update(jobs, updatefile):
    """Trigger update of a disconnected Longbow session.

    This method will start the update process on an existing but disconnected
    Longbow session. All job statuses will be checked and updated in the
    recovery file and all output files will be synced before disconnecting."""

    jobfile = os.path.join(os.path.expanduser('~/.longbow'), updatefile)

    LOG.info("Attempting to find the recovery file '{0}'".format(jobfile))

    # Load the jobs recovery file.
    if os.path.isfile(jobfile):

        LOG.info("Recovery file found.")

        _, _, jobparams = configuration.loadconfigs(jobfile)

        # Copy to jobs so when exceptions are raised the structure is
        # available.
        for param in jobparams:

            jobs[param] = jobparams[param]

    else:

        raise exceptions.RequiredinputError(
            "Recovery file could not be found, make sure you haven't deleted "
            "the recovery file and that you are not providing the full path, "
            "just the file name is needed.")

    # Add the updater key
    jobs["lbowconf"]["update"] = True

    # Enter monitoring loop
    scheduling.monitor(jobs)

    # Cleanup the remote working directory.
    staging.cleanup(jobs)


def _commandlineproc(alllongbowargs, cmdlnargs, parameters):
    """Process the command-line arguments.

    This method is used to process the command-line to discover any Longbow
    arguments, executables and their arguments.

    """
    # Initialise variables.
    executable = ""
    longbowargs = []
    execargs = []

    # Search for recognised executables on the commandline
    for item in cmdlnargs:

        if item in getattr(apps, "EXECLIST"):

            longbowargs = cmdlnargs[:cmdlnargs.index(item)]
            executable = item
            execargs = cmdlnargs[cmdlnargs.index(item) + 1:]
            break

    # If a known executable wasn't found then treat command-line as strictly
    # of the form: longbow <longbow args> exec [exec args].
    if executable == "":

        for index, item in enumerate(cmdlnargs):

            # if item provided on the commandline doesn't appear to be a
            # longbow argument, then assume the first is the exec and anything
            # after it are exec args.
            previtem = cmdlnargs[index - 1].replace("-", "")

            # If previous item not in parameters then we have found the exec.
            if item not in alllongbowargs and previtem not in parameters:

                longbowargs = cmdlnargs[:index]
                executable = item
                execargs = cmdlnargs[index + 1:]
                break

            # If previous item in parameters then check that it is a bool type
            # flag.
            elif (item not in alllongbowargs and previtem in parameters and
                    isinstance(parameters[previtem], bool)):

                longbowargs = cmdlnargs[:index]
                executable = item
                execargs = cmdlnargs[index + 1:]
                break

        # If nothing but Longbow arguments are found then assume other stuff
        # is in configuration files. This will be checked later.
        if len(execargs) == 0 and executable == "":

            longbowargs = cmdlnargs

    # make sure the user hasn't provided bogus longbow arguments or those
    # that aren't recognised on the command line
    for item in longbowargs:

        if item.startswith("-") and item not in alllongbowargs:

            allowedargs = " ".join(alllongbowargs)

            raise exceptions.CommandlineargsError(
                "Argument '{0}' is not a recognised Longbow argument. "
                "Recognised arguments are: {1}".format(item, allowedargs))

    parameters["executable"] = executable
    parameters["executableargs"] = " ".join(execargs)

    return longbowargs


def _downloadexamples(longbowargs):
    """Longbow examples downloader."""
    # Test for the examples command line flag, download files and exit if found
    if longbowargs.count("-examples") or longbowargs.count("--examples") == 1:

        # Check if the examples have already been downloaded first.
        if not os.path.isfile(
                os.path.join(os.getcwd(), "longbow-examples.zip")):

            print("Downloading examples...")

            try:

                subprocess.check_call([
                    "wget", "http://www.hecbiosim.ac.uk/file-store/"
                    "longbow-examples.zip", "-O",
                    os.path.join(os.getcwd(), "longbow-examples.zip")])

            except subprocess.CalledProcessError:

                subprocess.call([
                    "curl", "-L", "http://www.hecbiosim.ac.uk/file-store/"
                    "longbow-examples.zip", "-o",
                    os.path.join(os.getcwd(), "longbow-examples.zip")])

            # Unzip the archive file.
            print("Extracting the archive file...")

            subprocess.call(
                ["unzip", "-d", os.path.join(os.getcwd(), "longbow-examples/"),
                 os.path.join(os.getcwd(), "longbow-examples.zip")])

            print("Removing the zip archive file...")

            os.remove(os.path.join(os.getcwd(), "longbow-examples.zip"))

            print("Done.")

        exit(0)


def _hostfileproc(parameters):
    """Locate the host configuration file."""
    # Hosts - if a filename hasn't been provided default to hosts.conf
    if parameters["hosts"] == "":

        parameters["hosts"] = "hosts.conf"

    # If a full absolute path has not been provided then check within the
    # current working directory, ~/.longbow directory and the execution
    # directory.
    if os.path.isabs(parameters["hosts"]) is False:

        # CWD.
        cwd = os.path.join(os.getcwd(), parameters["hosts"])

        # Path for ~/.longbow directory.
        longbowdir = os.path.join(os.path.expanduser("~/.longbow"),
                                  parameters["hosts"])

        if os.path.isfile(cwd):

            parameters["hosts"] = cwd

        # The ~/.longbow directory.
        elif os.path.isfile(longbowdir):

            parameters["hosts"] = longbowdir

        else:

            raise exceptions.RequiredinputError(
                "No host configuration file found in the current working "
                "directory '{0}', the execution directory '{1}' or in the "
                "~/.longbow directory."
                .format(os.getcwd(),
                        os.path.dirname(os.path.realpath(__file__))))


def _jobfileproc(parameters):
    """Locate the job configuration file."""
    # Job - if a job configuration file has been supplied but the path hasn't
    # look in the current working directory and then the execution directory
    # if needs be.
    if parameters["job"] != "":

        if os.path.isabs(parameters["job"]) is False:

            # Path for CWD.
            cwd = os.path.join(os.getcwd(), parameters["job"])

            if os.path.isfile(cwd):

                parameters["job"] = cwd

            else:

                raise exceptions.RequiredinputError(
                    "The job configuration file '{0}' couldn't be found in "
                    "the current working directory '{1}', the execution "
                    "directory '{2}'."
                    .format(parameters["job"], os.getcwd(),
                            os.path.dirname(os.path.realpath(__file__))))


def _messageflags(longbowargs):
    """Check if user has asked for service messages."""
    # Test for the about command line flag, print message and exit if found.
    if longbowargs.count("-about") == 1 or longbowargs.count("--about") == 1:

        # Text aligned against an 80 character width.
        print("Welcome to Longbow!\n\n"
              "Longbow is a remote job submission utility designed for "
              "biomolecular\n"
              "simulation. This software was developed as part of the "
              "EPSRC-funded HECBioSim\n"
              "project http://www.hecbiosim.ac.uk/\n\n"
              "HECBioSim facilitates high-end biomolecular simulation on "
              "resources such as\n"
              "ARCHER.\n\n"
              "Longbow is Copyright (C) of James T Gebbie-Rayet and Gareth B "
              "Shannon 2015.\n\n"
              "Please cite our paper: Gebbie-Rayet, J, Shannon, G, Loeffler, "
              "H H and\n"
              "Laughton, C A 2016 Longbow: A Lightweight Remote Job Submission"
              " Tool. Journal\n"
              "of Open Research Software, 4: e1, "
              "DOI: http://dx.doi.org/10.5334/jors.95")

        exit(0)

    # Test for the version command line flag, print message and exit if found.
    if (longbowargs.count("-version") == 1 or
            longbowargs.count("--version") == 1 or
            longbowargs.count("-V") == 1):

        print("Longbow v{0}".format(LONGBOWVERSION))

        exit(0)

    # Test for the help command line flag, print message and exit if found.
    if (longbowargs.count("-help") == 1 or longbowargs.count("--help") == 1 or
            longbowargs.count("-h") == 1):

        # Text aligned against an 80 character width in the terminal window.
        print("Welcome to Longbow!\n\n"
              "Usage:\n\n"
              "Before running Longbow, first setup a password-less SSH "
              "connection with a\n"
              "target remote resource and setup configuration files according "
              "to the\n"
              "documentation.\n\n"
              "documentation https://longbow.readthedocs.io/latest/ \n\n"
              "Submit jobs using the following syntax:\n\n"
              "longbow [longbow args] executable [executable args]\n\n"
              "e.g.:\n"
              "%longbow --verbose pmemd.MPI -i example.in -c example.min -p "
              "example.top -o output\n\n"
              "longbow args:\n\n"
              "--about                   : prints Longbow description.\n"
              "--debug                   : additional output to assist "
              "debugging.\n"
              "--disconnect              : instructs Longbow to disconnect and"
              " exit\n                            after submitting jobs.\n"
              "--examples                : downloads example files to "
              "./LongbowExamples\n"
              "--help, -h                : prints Longbow help.\n"
              "--hosts [file name]       : specifies the hosts configuration "
              "file name.\n"
              "--job [file name]         : specifies the job configuration "
              "file name.\n"
              "--jobname [job name]      : the name of the job to be "
              "submitted.\n"
              "--log [file name]         : specifies the file Longbow output "
              "should be directed to.\n"
              "--maxtime [HH:MM]         : set the maximum job time for all "
              "jobs.\n"
              "--recover [file name]     : launches the recovery mode.\n"
              "--resource [name]         : specifies the remote resource.\n"
              "--replicates [number]     : number of replicate jobs to be "
              "submitted.\n"
              "--verbose                 : additional run-time info to be "
              "output.\n"
              "--update [file name]      : launches the update mode to sync "
              "current job progress and files.\n"
              "--version, -V             : prints Longbow version number.\n"
              "\n"
              "Read the documentation at https://longbow.readthedocs.io/latest/" 
              "for more information on how to setup and run jobs using Longbow.")

        exit(0)


def _parsecommandlineswitches(parameters, longbowargs):
    """Command-line processor.

    Look through the longbow commandline args and pick out parameters of the
    form --flag [value].

    """
    for parameter in parameters:

        # Is this a flag, if it is then next parameter is the value.
        if (longbowargs.count("-" + parameter) == 1 or
                longbowargs.count("--" + parameter) == 1):

            try:

                position = longbowargs.index("-" + parameter)

            except ValueError:

                position = longbowargs.index("--" + parameter)

            if (position + 1 == len(longbowargs) or
                    longbowargs[position + 1].startswith("-")):

                if parameters[parameter] == "":

                    raise exceptions.CommandlineargsError(
                        "Please specify a valid value for the --" + parameter +
                        " command line parameter e.g. longbow --" + parameter +
                        "value ...")

                if parameters[parameter] is True:

                    parameters[parameter] = False

                elif parameters[parameter] is False:

                    parameters[parameter] = True

            else:

                parameters[parameter] = longbowargs[position + 1]


def _setuplogger(parameters):
    """Logger setup.

    Configure the Longbow logger, this is for the application. Library users
    should configure their own logging.

    """
    # If no log file name was given then default to "log".
    if parameters["log"] == "":

        parameters["log"] = "longbow.log"

    # If the path isn't absolute then create the log in CWD.
    if os.path.isabs(parameters["log"]) is False:

        parameters["log"] = os.path.join(os.getcwd(), parameters["log"])

    # In debug mode we would like more information and also to switch on the
    # debug messages, otherwise stick to information level logging.
    if parameters["debug"] is True:

        logformat = logging.Formatter('%(asctime)s - %(levelname)-8s - '
                                      '%(name)s - %(message)s',
                                      '%Y-%m-%d %H:%M:%S')

        LOG.setLevel(logging.DEBUG)

    else:

        logformat = logging.Formatter('%(asctime)s - %(message)s',
                                      '%Y-%m-%d %H:%M:%S')

        LOG.setLevel(logging.INFO)

    # All logging types use the file handler, so append the logfile.
    handler = logging.FileHandler(parameters["log"], mode="w")
    handler.setFormatter(logformat)
    LOG.addHandler(handler)

    # Verbose and debugging mode need console output as well as logging to
    # file.
    if parameters["debug"] is True or parameters["verbose"] is True:

        handler = logging.StreamHandler()
        handler.setFormatter(logformat)
        LOG.addHandler(handler)
