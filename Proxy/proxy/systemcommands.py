import subprocess

class SysCommands:
    """A class containing all the connection related functions"""
    
    def __init__(self):
        pass
    
    # Open function is defined here
    def runcommand(self, cmd):
        handle = subprocess.Popen(cmd)
        handle.communicate()
                
    # Copy file function 
    def copyfilelocal(self):
        print("copy this")
        
    def copyfileremote(self):
        print("copy this")
        
    # Delete file function
    def removefile(self):
        print("delete this")
    
