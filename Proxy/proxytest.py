from proxy.systemcommands import SysCommands
from proxy.config import RemoteConfig
import os

#Script executing directory (just in case we need it later for absolute path support).
defaultpath = os.getcwd()

#Use paths relative to user dir so set this as our cwd
os.chdir(os.path.expanduser('~'))

remote = RemoteConfig("./Workspace/Git/ProxyApp/Proxy/settings.conf")
command = SysCommands(remote.user, remote.host, remote.port)

test1 = ["cd libraries"+"\n", "ls"]
test2 = ['ls']

#command.sshconnection(test1)
#command.runcommand(test2)



