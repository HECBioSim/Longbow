from proxy.systemcommands import SysCommands

#Connection parameters
uname = "rjw41005"
host = "scarf.rl.ac.uk"
port = "2222"

test = ["cd libraries"+"\n", "ls"]

command = SysCommands(uname, host, port)
command.sshconnection(test)
#command.runcommand(test)

#command.list("/dir2")

