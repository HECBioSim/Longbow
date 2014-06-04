import subprocess
import logging

logger = logging.getLogger("ProxyApp")

class ShellCommands:
    
    """A wrapper class for the methods that wrap common shell commands."""
    
    def __init__(self, hostparams):
    
        
        """On calling the class we want some initial information to be available to 
        the methods, such as default paths and host details. Here we are also going 
        to check if the host can be reached."""
        
        self.host = hostparams["user"] + "@" + hostparams["host"]
        self.port = hostparams["port"]
        
        logger.info("Testing the connection to " + self.host)
        
        # Test the host connection to see if we can connect
        if (self.runremote(["ls &> /dev/null"])[0] == 0):
            logger.info("Connection established to " + self.host)
        else: 
            raise RuntimeError("Cannot reach host " + self.host + 
                               " make sure the configuration is correct and that you can access" +
                               " host in a normal terminal")
    
    
    def runcommand(self, cmd):
        
        
        """Any command that is called here is passed to a subprocess shell for execution."""
        
        # Call to python subprocess, here we will send commands to be run in a terminal as a list 
        # and return the output back. The [0] on the communicate is basically because at the moment 
        # information from stderr is not needed. 
        handle = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output = handle.communicate()[0]
        errorstate = handle.returncode
        
        # The returned information is in byte format so lets put it into a useful string format.
        output = output.decode("utf-8")
        
        return errorstate, output
    

    def runremote(self, args):
        
        
        """If commands are destined for remote execution then they are appended to ssh before passing to subprocess."""
        
        cmd = ["ssh", self.host, "-p " + self.port]
        
        cmd.extend(args)

        errorstate, output = self.runcommand(cmd)
        
        return errorstate, output
                

    def localcopy(self, from_path, to_path):
        
        
        """To copy files around locally on the local resource call this method."""
        
        cmd = ["cp", "-r", from_path, to_path]
        
        errorstate = self.runcommand(cmd)[0]
        
        return errorstate
                

    def localdelete(self, path):
        
        
        """This method will delete a file on the local resource."""
        
        cmd = ["rm", "-r", path]

        errorstate = self.runcommand(cmd)[0]
        
        return errorstate
        

    def locallist(self, path):
        
        
        """Listing dirs is simply the ls [path]."""
        
        cmd = ["ls", path]
        
        errorstate = self.runcommand(cmd)[0]
        
        #TODO: we should probably do something with the output and return from here this might be useful (test = out.split()) 
        
        return errorstate
    

    def remotecopy(self, from_path, to_path):
        
        
        """To copy files around locally but on the remote resource call this method."""
        
        cmd = ["cp", "-r", from_path, to_path]
        
        errorstate = self.runremote(cmd)[0]
        
        return errorstate
        

    def remotedelete(self, path):
        
        
        """This method will delete a file on the remote resource."""
        
        cmd = ["rm", "-r", path]

        errorstate = self.runremote(cmd)[0]
        
        return errorstate 
    

    def remotelist(self, path):
        
        
        """Listing dirs remotely is much easier when done remotely as ls [path] can be called over ssh."""
        
        cmd = ["ls", path]
    
        errorstate = self.runremote(cmd)[0]
        
        #TODO: we should probably do something with the output and return from here this might be useful (test = out.split()) 
        
        return errorstate

    
    def upload(self, from_path, to_path):
        
        
        """To copy a file from the local resource to the remote resource (upload) call this method."""
        
        cmd = ["scp", "-P " + self.port, "-r", from_path, self.host + ":" + to_path]
        
        errorstate = self.runcommand(cmd)[0]
        
        return errorstate
        

    def download(self, from_path, to_path):
        
        
        """To copy a file from the remote resource to the local resource (download) call this method."""
        
        cmd = ["scp", "-P " + self.port, "-r", self.host + ":" + from_path, to_path]
        
        errorstate = self.runcommand(cmd)[0]
        
        return errorstate

