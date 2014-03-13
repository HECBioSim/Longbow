from proxy.systemcommands import SysCommands

test = []

uname = "rjw41005"
host = "scarf.rl.ac.uk"
port = "2222"

test.extend(["ssh", uname + "@" + host, "-p " + port])
test.extend(["ls"])

command = SysCommands()
command.runcommand(test)