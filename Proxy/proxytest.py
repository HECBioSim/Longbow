from proxy.systemcommands import SysCommands

uname = "rjw41005"
host = "scarf.rl.ac.uk"
port = "2222"

test = ["ls"]

command = SysCommands()
command.sshconnection(test, uname, host, port)