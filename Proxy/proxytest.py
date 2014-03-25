
def proxy(args, config_file):

    #Use paths relative to user dir so set this as our cwd
    os.chdir(os.path.expanduser("~"))

    remote = RemoteConfig(args, config_file)
    command = SysCommands(remote.user, remote.host, remote.port)

    test = ["ls"]

    #command.sshconnection(test)
    #command.runcommand(test)
    command.listlocal("./Desktop")
    
    print("resource = ", args.resource)
    print("program = ", args.program)

if __name__ == "__main__":
    """Main entry point for the ProxyApp as a stand-alone application. The main function proxy can be hooked directly by providing it with the correct args."""
    import os
    import argparse
    from core.systemcommands import SysCommands
    from core.config import RemoteConfig
    
    #Instantiate the parser
    parser = argparse.ArgumentParser(description = "Welcome to the ProxyApp.")
    
    #Parse the command line args
    parser.add_argument("-res", "--resource", help = "Name of the computer resource for example Archer.", required = True)
    parser.add_argument("-prog", "--program", help = "Name of the software for example Amber.", required = True)
    #parser.add_argument(nargs = "*")
    
    args = parser.parse_args()
    
    print(args)
    
    config_file = "./Workspace/Git/ProxyApp/Proxy/settings.conf"
    
    proxy(args, config_file)

