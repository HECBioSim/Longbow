from proxy.systemcommands import SysCommands
from proxy.config import RemoteConfig

configs = RemoteConfig("me.conf")
command = SysCommands(configs.uname, configs.host, configs.port)

test = ["cd libraries"+"\n", "ls"]


command.sshconnection(test)
#command.runcommand(test)

#command.list("/dir2")

