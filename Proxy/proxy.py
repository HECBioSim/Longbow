import os
from core.systemcommands import SysCommands
from core.config import RemoteConfig
    
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

