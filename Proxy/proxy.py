import os
import argparse
from core.systemcommands import SysCommands
from core.config import RemoteConfig
from core.application import *
from core.jobcommands import *

def proxy(args, remnant_args, config_file):

    #Use paths relative to user dir so set this as our cwd
    os.chdir(os.path.expanduser("~"))

    #Instantiate the remote connection configuration class.
    remote = RemoteConfig(args, config_file)
    
    #Instantiate the sys commands class.
    command = SysCommands(remote.user, remote.host, remote.port)
    
    #Instantiate the jobs commands class.
    jobcommand = Scheduler()
    
    #Instantiate the application commands class.
    application = Applications()
    
    
    

if __name__ == "__main__":
    """Main entry point for the ProxyApp as a stand-alone application. The main function proxy can be hooked directly by providing it with the correct args."""
    
    #Instantiate the parser.
    parser = argparse.ArgumentParser(description = "Welcome to the ProxyApp.")
    
    #Set up the first two command line parameters to parse.
    parser.add_argument("-res", "--resource", help = "Name of the computer resource for example Archer.", required = True)
    parser.add_argument("-prog", "--program", help = "Name of the software for example Amber.", required = True)
    
    #Parse the known params into args and return the rest in remnants.
    args, remnants = parser.parse_known_args()

    #Configuration file (maybe do something with this later to make it's specification nicer)
    config_file = "./Workspace/Git/ProxyApp/Proxy/settings.conf"
    
    #Enter the main application function and pass it the dictionary containing the resource + application (args) 
    #plus the list of unparsed command line arguments (remnants).
    proxy(args, remnants, config_file)

