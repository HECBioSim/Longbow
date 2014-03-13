import subprocess

class SysCommands:
    """A class containing all the connection related functions"""
    
    def __init__(self):
        pass
    
    # Open function is defined here
    def runcommand(self, cmd):
        handle = subprocess.Popen(cmd)
        handle.communicate()
    
    def sshconnection(self, args, uname, host, port):
        cmd = ["ssh", uname + "@" + host, "-p " + port]
        cmd.extend(args)
        self.runcommand(cmd)
                
    # Copy file function 
    def copyfilelocal(self):
        print("copy this")
        
    def copyfileremote(self):
        print("copy this")
        
    # Delete file function
    def removefile(self):
        print("delete this")
    
