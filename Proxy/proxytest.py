from proxy.systemcommands import SysCommands

uname = "rjw41005"
host = "scarf.rl.ac.uk"
port = "2222"

test = ["ls"]

command = SysCommands(uname, host, port)
command.sshconnection(test)
#command.copyfilelocal("../../../dir1/test", "../../../dir2")