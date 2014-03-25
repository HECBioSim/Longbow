import subprocess
import os

class SysCommands:
    """A class containing all the connection related functions."""
    
    def __init__(self, user, domain, port):
        """On calling the class we want some initial information to be available to the methods, such as default paths and host details."""
        self.host = user + "@" + domain
        self.port = port
        
        #Change to the users home dir and operate as a base (locally).
        self.base = os.getcwd()
    
    # Open function is defined here
    # This runs the command in a sub process
    def runcommand(self, cmd):
        """Here any command that is assembled and passed for calling is sent to a subprocess shell"""
        handle = subprocess.Popen(cmd)
        handle.communicate()
    
    # The ssh connection is setup here
    # All commands needing ssh should be passed through here
    def sshconnection(self, args):
        """If commands are destined for remote execution then they are appended to ssh before passing to subprocess."""
        cmd = ["ssh", self.host, "-p " + self.port]
        cmd.extend(args)
        
        self.runcommand(cmd)
                
    # Copy file function locally on local machine
    def copyfilelocal(self, from_path, to_path):
        """To copy files around locally on the local resource call this method."""
        cmd = ["cp", "-R", self.base + from_path, self.base + to_path]
        
        print(cmd)
        self.runcommand(cmd)
                
    # Copy the file locally on remote machine
    def copyfileremote(self, from_path, to_path):
        """To copy files around locally but on the remote resource call this method."""
        cmd = ["cp", "-R", from_path, to_path]
        
        print(cmd)
        self.sshconnection(cmd)
        
    # Transfer the file between local and remote machines
    def uploadfile(self, from_path, to_path):
        """To copy a file from the local resource to the remote resource (upload) call this method."""
        cmd = ["scp", "-R", self.base + from_path, self.host + "/" + to_path]
        
        print(cmd)
        self.sshconnection(cmd)
        
    # Transfer the file between local and remote machines
    def downloadfile(self, from_path, to_path):
        """To copy a file from the remote resource to the local resource (download) call this method."""
        cmd = ["scp", "-R", self.host + "/" + from_path, self.base + to_path]
        
        print(cmd)
        self.sshconnection(cmd)

    # Delete local file function
    def removefilelocal(self, path):
        """This method will delete a file on the local resource."""
        cmd = ["rm", "-R", self.base + path]

        print(cmd)
        self.runcommand(cmd)
        
    # Delete remote file function
    def removefileremote(self, path):
        """This method will delete a file on the remote resource."""
        cmd = ["rm", "-R", path]

        print(cmd)
        self.sshconnection(cmd)  
    
    # Return a list of all directory contents (for some reason cd doesn't work locally)
    def listlocal(self, path):
        """Listing dirs is simply the ls [path]."""
        #contents = os.listdir(self.base + path) 
        cmd = ["ls", path]
        
        print(cmd)
        self.runcommand(cmd)
    
    # Return a list of all directory contents (remote)
    def listremote(self, path):
        """Listing dirs remotely is much easier when done remotely as ls [path] can be called over ssh."""
        cmd = ["ls", path]
    
        print(cmd)
        self.sshconnection(cmd) 
