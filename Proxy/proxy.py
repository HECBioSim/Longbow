import os
import sys
import logging
from core.shellwrappers import ShellCommands
from core.configs import HostConfig, JobConfig
from core.appcommands import Applications
from core.jobcommands import Scheduler
from core.staging import Staging

def proxy(currentpath, app_args, configfile, jobfile, logfile, debug):
    
    """The main function that forms the basis for operating the core library. 
    This can serve as a template for building more advanced applications. 
    Here some of the classes are doing auto configuration through the use of 
    factory classes, however the same things can be done by calling the 
    respective classes, for example (scheduler can be used by calling the 
    lsf or pbs classes if known). The arguments for this function should be:
    
    proxy(args, configfile, jobfile, logfile, debug):
    
    args       = A string of arguments normally passed to the command line 
                 when running the program normally.
    configfile = Path (absolute) to the config file pass blank ("") to use 
                 a default location.
    jobfile    = Path (absolute) to the job config file pass blank ("") to 
                 use a default location. 
    logfile    = Path (absolute) to the log file pass blank ("") to use a 
                 default location. 
    debug      = Pass "True" if debug output is required.
    """
    
    #TODO: Support multiple job submission as both reps and batches (see comments throughout code).
    #TODO: Local methods in shellwrappers should have the shell based commands replaced with the native python
    #      versions.
    #TODO: Formatting and add remaining exceptions (the placeholder marker below marks progress point).
    #TODO: Various classes and methods are missing documentation comments and also hashed comments, add these.
    
    #------------------------------------------------------------------------
    # Setup some basic files.
    
    # The path that the proxy is executed from is passed from sysargv so that 
    # we can point the app to the location of the default config files. If custom 
    # file locations are required then supply an absolute path.
    
    
    # Current dir to get the 
    currentdir = os.path.dirname(currentpath)
    
    # Host config file (user, host, port and scheduler) supplied with -config or 
    # uses this default location.
    if(configfile == ""): configfile = currentdir + "/hosts.conf"
    
    # Job config file supplied with -job or uses this default location
    if(jobfile == ""): jobfile = currentdir + "/job.conf"
    
    # Logfile for troubleshooting supplied with -log or uses this default location
    if(logfile == ""): logfile = currentdir + "/log"
    
    
    #------------------------------------------------------------------------
    # Set up the package wide logger.
    
    # Create a package-wide logger called logger.
    logger = logging.getLogger("ProxyApp")
    logger.setLevel(logging.DEBUG)
    
    # Create a logging format - in debug mode it is useful to have the .py files.
    if(debug==True):
        logformat = logging.Formatter("%(asctime)s - %(name)s - %(filename)-18s - %(levelname)-8s - %(message)s")
    else:
        logformat = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Default is to write to the log file and set level to debug and bind format.
    loghandle = logging.FileHandler(logfile, mode = "w")
    loghandle.setLevel(logging.DEBUG)
    loghandle.setFormatter(logformat)
    logger.addHandler(loghandle)
    
    if(debug==True):
        loghandle = logging.StreamHandler()
        loghandle.setLevel(logging.DEBUG)
        loghandle.setFormatter(logformat)
        logger.addHandler(loghandle)
    
    # Test entry stating the app is started.
    logger.info("ProxyApp is now started.")

    
    #------------------------------------------------------------------------
    # All paths after this initial configuration (for example the working dir
    # inside the job config file) should be relative to the home (~) directory.


    # Use paths relative to user dir so set this as our cwd.
    os.chdir(os.path.expanduser("~"))
    
    
    #------------------------------------------------------------------------
    # Instantiate the classes.
    
    try:
        
        # Instantiate the class and store the job config params in an object, note this will also
        # automatically read the chosen file followed by some checking.
        jobconf = JobConfig(jobfile)
    
        # Instantiate the remote connection configuration class. This is where host 
        # connections are dealt with, it was convenient to support different hosts this way.
        resource = HostConfig(jobconf.jobparams, configfile)
        
        # Instantiate the shell commands class.
        shellcommand = ShellCommands(resource.hostparams)
        
        # Instantiate the jobs commands class, this return the correct class for the 
        # scheduler environment. If not specified in the host.conf
        # then testing will try to determine the scheduling environment to use.
        job = Scheduler.test(shellcommand, resource)

        # Instantiate the staging class.
        stage = Staging()
    
        # Instantiate the application commands class, this will return the correct 
        # class for the application specified on command line. Some tests as to whether
        # the application is actually in your path will happen automatically.
        application = Applications.test(shellcommand, jobconf.jobparams)
        
        
        #------------------------------------------------------------------------
        # Start processing the job setup and submit.
    
        # Process the command line args to separate out all the files that need staging
        # and form a nice string for the scheduler.
        filelist, arglist = application.processjob(app_args, jobconf.jobparams["executable"])
    
        # Create the jobfile and append it to the list of files that need uploading.
        filelist, submitfile = job.jobfile(jobconf.jobparams, arglist, filelist)
    
        # Stage all of the job files along with the scheduling script.
        stage.stage_upstream(shellcommand, jobconf.jobparams, filelist)

        # Submit the job to the scheduler.
        jobid = job.submit(shellcommand, jobconf.jobparams, submitfile)
        

        #------------------------------------------------------------------------
        # Monitor jobs.
    
    
        job.monitor(shellcommand, stage, jobconf.jobparams, jobid)
        

        #------------------------------------------------------------------------
        # Final transfer of data and clean up.
    

        # Download final results.
        stage.stage_downstream(shellcommand, jobconf.jobparams)
    
        # Remove the remote directory.
        shellcommand.remotedelete(jobconf.jobparams["remoteworkdir"])


    except Exception as e:
        if (debug == True): 
            logger.exception(e)
        else:
            logger.error(e) 

    logger.info("Closing ProxyApp.")


    #------------------------------------------------------------------------


if __name__ == "__main__":
    
    """Main entry point for the ProxyApp as a stand-alone application. The main 
    function "proxy" can be hooked directly by providing it with the correct args.
    
    To  override the default config files and log from being the default ones inside
    the proxyapp directory use the following flags.
    
    -conf (absolute path eg -conf /home/user/some/dir).
    
    -job  (absolute path eg -job /home/user/some/dir).
    
    -log  (absolute path eg -log /home/user/some/dir).
    
    To specify the job is a batch job append the -reps x where x is the number of reps.
    
    To put the app in debug mode supply -debug
    
    """
    
    
    #------------------------------------------------------------------------
    # Some defaults.
    

    # Fetch command line arguments
    command_line_args = sys.argv 
    
    # Remove the first argument (the application path)
    currentpath = command_line_args[0]
    command_line_args.pop(0)
    
    # Initialise file path params, so we can pass blank to signify use default paths 
    # if not supplied.
    confile = ""
    jobfile = ""
    logfile = ""
    debug = False


    #------------------------------------------------------------------------
    # Pull out some of the ProxyApp specific commandline args leaving behind the target
    # app args.


    # Take out the config file path, then remove it from the command line argument list.
    if(command_line_args.count("-conf") == 1):
        position = command_line_args.index("-conf")
        confile = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
     
    # Take out the job config file path, then remove it from the command line argument list.
    if(command_line_args.count("-job") == 1):
        position = command_line_args.index("-job")
        jobfile = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
     
    # Take out the log file path, then remove it from the command line argument list.
    if(command_line_args.count("-log") == 1):
        position = command_line_args.index("-log")
        logfile = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
        
    # Take out the reps parameter, then remove it from the command line list.
    if(command_line_args.count("-reps") == 1):
        position = command_line_args.index("-reps")
        reps = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
    
    # Take out the debug parameter, then remove it from the command line list.
    if(command_line_args.count("-debug") == 1):
        position = command_line_args.index("-debug")
        command_line_args.pop(position)
        debug =True
        
    
    #------------------------------------------------------------------------
    # Call ProxyApp.
        
    # Enter the main application.
    proxy(currentpath, command_line_args, confile, jobfile, logfile, debug) 
    