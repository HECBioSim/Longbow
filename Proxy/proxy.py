import os
import sys
from core.shellwrappers import ShellCommands
from core.configs import HostConfig, JobConfig
from core.appcommands import Applications
from core.jobcommands import Scheduler
from core.staging import Staging

def proxy(app_args, debug, configfile, jobfile, logfile):
    
    """The main function that forms the basis for operating the core library. This can serve as a template
    for building more advanced applications. Here most of the classes are doing auto configuration through 
    the use of factory classes, however the same things can be done by calling the respective classes for
    example (scheduler can be used by calling the lsf or pbs classes if known or preferred)."""
    
    #TODO: Support multiple job submission as both reps and batches.
    #TODO: Create advanced monitoring methods.
    #TODO: Replace sys.exits throughout the application with exception raising. Also this would be a good time to introduce the logfile.
    #TODO: Fix issues with files that are not being uploaded sometimes, this must be something failing somewhere (possibly ssh or scp) all commands should have their returns checked.
    
    
    #-----------------------------------------------------------------------------------------------
    #I find it easier using relative paths, in this case I'm going to run both the remote and local
    #paths relative to the "~" user dir. Before I set the working dir to the user dir, I capture the
    #absolute path of the hosts.conf and job.conf.
    
    
    #Current dir to get the 
    currentdir = os.getcwd()
    
    #Host config file (user, host, port and scheduler)
    if(configfile == ""): configfile = currentdir + "/hosts.conf"
    
    #TODO: add this as a commandline arg -conf (like Charlie's app) which means that I want to use a relative path too.
    if(jobfile == ""): jobfile = currentdir + "/job.conf"
    
    #Logfile for troubleshooting.
    #TODO: this log file isn't yet used, include it when sys.exits are replaced by exception handling.
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
    
    #Instantiate the sys commands class.
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
    
    #TODO: That number "8" is currently not used but it is to remind me to do something good surrounding reps.
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
    
    """Main entry point for the ProxyApp as a stand-alone application. The main function proxy can be hooked directly by providing it with the correct args."""
    
    #Fetch command line arguments
    command_line_args = sys.argv 
    
    #Remove the first argument (the application path)
    command_line_args.pop(0)
    
    #Enter the main application function and pass it the dictionary containing the resource + application (args) 
    #plus the list of unparsed command line arguments (command_line_args).
    proxy(command_line_args, "True")
    