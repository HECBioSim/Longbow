import subprocess
import os

class SysCommands:
    """A class containing all the connection related functions"""
    
    def __init__(self, uname, domain, port):
        self.host = uname + "@" + domain
        self.port = port
        
        #Script executing directory (just in case).
        self.defaultpath = os.getcwd()

        #Change to the users home dir and operate as a base (locally).
        os.chdir(os.path.expanduser('~') + "/Desktop")
        self.base = os.getcwd()
        
    def __del__(self):
        os.chdir(self.defaultpath)
    
    # Open function is defined here
    # This runs the command in a sub process
    def runcommand(self, cmd):
        handle = subprocess.Popen(cmd)
        handle.communicate()
    
    # The ssh connection is setup here
    # All commands needing ssh should be passed through here
    def sshconnection(self, args):
        cmd = ["ssh", self.host, "-p " + self.port]
        cmd.extend(args)
        
        self.runcommand(cmd)
                
    # Copy file function locally on local machine
    def copyfilelocal(self, from_path, to_path):
        cmd = ["cp", "-R", self.base + from_path, self.base + to_path]
        
        print(cmd)
        self.runcommand(cmd)
                
    # Copy the file locally on remote machine
    def copyfileremote(self, from_path, to_path):
        cmd = ["cp", "-R", from_path, to_path]
        
        print(cmd)
        self.sshconnection(cmd)
        
    # Transfer the file between local and remote machines
    def uploadfile(self, from_path, to_path):
        cmd = ["scp", "-R", self.base + from_path, self.host + "/" + to_path]
        
        print(cmd)
        self.sshconnection(cmd)
        
    # Transfer the file between local and remote machines
    def downloadfile(self, from_path, to_path):
        cmd = ["scp", "-R", self.host + "/" + from_path, self.base + to_path]
        
        print(cmd)
        self.sshconnection(cmd)

    # Delete local file function
    def removefilelocal(self, path):
        cmd = ["rm", "-R", self.base + path]

        print(cmd)
        self.runcommand(cmd)
        
    # Delete remote file function
    def removefileremote(self, path):
        cmd = ["rm", "-R", path]

        print(cmd)
        self.sshconnection(cmd)  
    
    # Return a list of all directory contents (for some reason cd doesn't work locally)
    def listlocal(self, path):
        contents = os.listdir(self.base + path) 
        
        print(contents)
        return contents
    
    # Return a list of all directory contents (remote)
    def listremote(self, path):
        cmd = ["cd " + path + "\n", "ls"]
    
        print(cmd)
        self.sshconnection(cmd) 
