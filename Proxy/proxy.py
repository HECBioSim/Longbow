import os
import sys
from core.shellwrappers import ShellCommands
from core.configs import HostConfig, JobConfig
from core.appcommands import Applications
from core.jobcommands import Scheduler
from core.staging import Staging

def proxy(app_args, configfile, jobfile, logfile, debug):
    
    """The main function that forms the basis for operating the core library. This can serve as a template
    for building more advanced applications. Here some of the classes are doing auto configuration through 
    the use of factory classes, however the same things can be done by calling the respective classes for
    example (scheduler can be used by calling the lsf or pbs classes if known or preferred). The arguments 
    for this function should be:
    
    proxy(args, configfile, jobfile, logfile, debug):
    
    args       = a string of arguments normally passed to the command line when running the program normally.
    configfile = path (absolute) to the config file pass blank ("") to use a default location.
    jobfile    = path (absolute) to the job config file pass blank ("") to use a default location. 
    logfile    = path (absolute) to the log file pass blank ("") to use a default location. 
    debug      = pass "True" if debug output is required.
    """
    
    #TODO: Support multiple job submission as both reps and batches.
    #TODO: Create advanced monitoring methods.
    #TODO: Replace sys.exits throughout the application with exception raising. Also this would be a good time to introduce the logfile.
    #TODO: Fix issues with files that are not being uploaded sometimes, this must be something failing somewhere (possibly ssh or scp) 
    #      all commands should have their returns checked.
    #TODO: log file isn't yet used, include it when sys.exits are replaced by exception handling.
    
    #-----------------------------------------------------------------------------------------------
    #Setup some basic files and paths.
    
    #I find it easier using relative paths, in this case I'm going to run both the remote and local
    #paths relative to the "~" user dir. The config files used here are all mandatory, the user can
    #choose whether they want to use the default locations or custom ones by supplying them on the 
    #command line. 
    
    
    #Current dir to get the 
    currentdir = os.getcwd()
    
    #Host config file (user, host, port and scheduler) supplied with -config or uses this default location.
    if(configfile == ""): configfile = currentdir + "/hosts.conf"
    
    #Job config file supplied with -job or uses this default location
    if(jobfile == ""): jobfile = currentdir + "/job.conf"
    
    #Logfile for troubleshooting supplied with -log or uses this default location
    if(logfile == ""): logfile = currentdir + "/log"
        
    logfile = open(logfile, "w+")

    #Use paths relative to user dir so set this as our cwd
    os.chdir(os.path.expanduser("~"))
    
    
    #-----------------------------------------------------------------------------------------------
    #Instantiate the classes.
    
    
    #Load the job configuration file.
    jobconf = JobConfig(jobfile)
    
    #Instantiate the remote connection configuration class. This is where host connections are dealt with
    #It was convenient to support different hosts this way.
    resource = HostConfig(jobconf.resource, configfile)
    
    #Instantiate the shell commands class.
    command = ShellCommands(resource.user, resource.host, resource.port)
    
    #Instantiate the jobs commands class, this return the correct class for the scheduler environment. If not specified in the host.conf
    #then testing will try to determine the scheduling environment to use.
    job = Scheduler.test(command, resource)
    
    #Instantiate the staging class.
    stage = Staging()
    
    #Instantiate the application commands class, this will return the correct class for the application specified on command line.
    #Some tests as to whether the application is actually in your path will happen automatically.
    application = Applications.test(command, jobconf.program, jobconf.executable)
    
    
    #-----------------------------------------------------------------------------------------------
    #Start processing the job setup and submit.
    
    
    #Process the command line args to separate out all the files that need staging and form a nice string for the scheduler.
    filelist, arglist = application.processjob(app_args)
    
    #(perhaps a local working dir so this becomes more of an application and less like a script).
    filelist, submitfile = job.jobfile(jobconf.local_workdir, jobconf.cores, jobconf.corespernode, "8", jobconf.account, jobconf.maxtime, arglist, filelist)

    #Stage all of the job files along with the scheduling script.
    stage.stage_upstream(command, jobconf.local_workdir, jobconf.remote_workdir, filelist)
    
    #Submit the job to the scheduler.
    jobid = job.submit(command, jobconf.remote_workdir, submitfile)
    
    
    #-----------------------------------------------------------------------------------------------
    #Monitor jobs.
    
    
    job.monitor(command, stage, jobconf.frequency, jobid, jobconf.local_workdir, jobconf.remote_workdir)
    
    
    #-----------------------------------------------------------------------------------------------
    #Final transfer of data and clean up.
    

    #Download final results.
    stage.stage_downstream(command, jobconf.local_workdir, jobconf.remote_workdir)
    
    #Remove the remote directory.
    command.removefileremote(jobconf.remote_workdir)


if __name__ == "__main__":
    
    """Main entry point for the ProxyApp as a stand-alone application. The main function proxy can be 
    hooked directly by providing it with the correct args."""
    
    
    #Fetch command line arguments
    command_line_args = sys.argv 
    
    #Remove the first argument (the application path)
    command_line_args.pop(0)
    
    #Initialise file path params, so we can pass blank to signify use default paths if not supplied.
    confile = ""
    jobfile = ""
    logfile = ""

    #Take out the config file path, then remove it from the command line argument list.
    if(command_line_args.count("-config") == 1):
        position = command_line_args.index("-config")
        confile = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
     
    #Take out the job config file path, then remove it from the command line argument list.
    if(command_line_args.count("-job") == 1):
        position = command_line_args.index("-job")
        jobfile = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
     
    #Take out the log file path, then remove it from the command line argument list.
    if(command_line_args.count("-log") == 1):
        position = command_line_args.index("-log")
        logfile = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
        
    #Take out the reps parameter, then remove it from the command line list.
    if(command_line_args.count("-reps") == 1):
        position = command_line_args.index("-reps")
        logfile = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
    
    #Enter the main application.
    proxy(command_line_args, confile, jobfile, logfile, "True")   

    