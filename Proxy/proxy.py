import os
import sys
from core.syscommands import SysCommands
from core.configs import HostConfig
from core.appcommands import Applications
from core.jobcommands import Scheduler
from core.staging import Staging

def proxy(args, app_args):
    
    #-----------------------------------------------------------------------------------------------
    #I find it easier using relative paths, in this case I'm going to run both the remote and local
    #paths relative to the "~" user dir. Before I set the working dir to the user dir, I capture the
    #absolute path of the hosts.conf.
    
    config_file = os.getcwd() + "/hosts.conf"

    #Use paths relative to user dir so set this as our cwd
    os.chdir(os.path.expanduser("~"))
    
    #-----------------------------------------------------------------------------------------------
    #Instantiate the classes.
    
    #Instantiate the remote connection configuration class.
    resource = HostConfig(args, config_file)
    
    #Instantiate the sys commands class.
    command = SysCommands(resource.user, resource.host, resource.port)
    
    #Instantiate the jobs commands class.
    schedule = Scheduler.test(command, resource)
    
    #Instantiate the staging class.
    stage = Staging()
    
    #Instantiate the application commands class.
    application = Applications.test(args, command, resource.executable)
    
    #-----------------------------------------------------------------------------------------------
    #Start processing the job setup.
    
    application.process_job(app_args)
    schedule.submit(command, "test.job")
    
    #-----------------------------------------------------------------------------------------------
    #Monitor jobs.
    
    
if __name__ == "__main__":
    """Main entry point for the ProxyApp as a stand-alone application. The main function proxy can be hooked directly by providing it with the correct args."""
    
    #Fetch command line arguments
    command_line_args = sys.argv 
    
    #Remove the first argument (the application path)
    command_line_args.pop(0)

    #Initialise a dictionary for some arguments
    args = {}
    
    #Take out the resource argument and put it into the dictionary, then remove it from the command line argument list
    if(command_line_args.count("-res") == 1):
        position = command_line_args.index("-res")
        args['resource'] = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
    else: sys.exit("Error: must supply resource")
    
    #Take out the program argument and put it into the dictionary, then remove it from the command line argument list
    if(command_line_args.count("-prog") == 1):
        position = command_line_args.index("-prog")
        args['program'] = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
    else: sys.exit("Error: must supply program")
    
    #Enter the main application function and pass it the dictionary containing the resource + application (args) 
    #plus the list of unparsed command line arguments (command_line_args).
    proxy(args, command_line_args)

