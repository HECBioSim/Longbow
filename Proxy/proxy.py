import os
import sys
from core.syscommands import SysCommands
from core.config import RemoteConfig
from core.appcommands import Applications
from core.jobcommands import Scheduler

def proxy(args, remnant_args):
    
    config_file = os.getcwd() + "/hosts.conf"

    #Use paths relative to user dir so set this as our cwd
    os.chdir(os.path.expanduser("~"))

    #Instantiate the remote connection configuration class.
    remote = RemoteConfig(args, config_file)
    
    #Instantiate the sys commands class.
    command = SysCommands(remote.user, remote.host, remote.port)
    
    #Instantiate the jobs commands class.
    schedule = Scheduler.test(command)
    
    #Instantiate the application commands class.
    application = Applications.test(args, remnant_args)

    schedule.submit()
    application.something()
    
    
if __name__ == "__main__":
    """Main entry point for the ProxyApp as a stand-alone application. The main function proxy can be hooked directly by providing it with the correct args."""
    
    #Fetch command line arguments
    command_line_args = sys.argv 
    
    #Remove the firs arg (the application path)
    command_line_args.pop(0)

    #Initialise a dictionary for some args
    args = {}
    
    #Take out the resource arg and put it into the dictionary, then remove it from the command line arg list
    if(command_line_args.count("-res") == 1):
        position = command_line_args.index("-res")
        args['resource'] = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
    else: sys.exit("Error: must supply resource")
    
    #Take out the program arg and put it into the dictionary, then remove it from the command line arg list
    if(command_line_args.count("-prog") == 1):
        position = command_line_args.index("-prog")
        args['program'] = command_line_args[position + 1]
        command_line_args.pop(position)
        command_line_args.pop(position)
    else: sys.exit("Error: must supply resource")
    
    #Enter the main application function and pass it the dictionary containing the resource + application (args) 
    #plus the list of unparsed command line arguments (command_line_args).
    proxy(args, command_line_args)

