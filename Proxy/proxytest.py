from proxy.systemcommands import SysCommands
from proxy.config import RemoteConfig

remote = RemoteConfig("archer.conf")
command = SysCommands(remote.user, remote.host, remote.port)

test = ["cd libraries"+"\n", "ls"]


command.sshconnection(test)
#command.runcommand(test)


