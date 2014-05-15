import sys
import configparser
import logging

logger = logging.getLogger("ProxyApp Core")

class HostConfig:
    
    def __init__(self, resource, configfile):
        
        
        """Some declarations and their initialisation (for specific error checking) 
        followed by some config params loading and some checking."""
        
        self.configfile = configfile
        self.resource = resource
        
        # Dictionary for the host config params.
        hostparams = {
                      "host": "",
                      "port": "",
                      "user": "",
                      "scheduler": ""
                      }
        
        # Load the remote resource configuration from the .conf file.
        self.loadhostconfigs()
        
        # Check the configuration parameters for some basic errors.
        self.checkparams()
        
        
    def loadhostconfigs(self):
        
        
        """Load the parameters from the config file."""
        
        logger.info("Loading configuration for destination computer from %s" % self.configfile)
        
        # Bind the hosts file to the config parser
        config = configparser.ConfigParser()
        config.read(self.configfile)
        
        # Check that we have some sections to read.
        sectionlist = config.sections()
        if(len(sectionlist) == 0):
            raise RuntimeError("No sections defined in the host config file each section defines \
                                a supercomputer resource connection details, sections are defined \
                                within [] followed by a list of params: \
                                [section name] \
                                param1 = val1 \
                                param2 = val2 \
                                etc.")
        
        # Make all sections in sectionlist lower case to be case agnostic.
        sectionlist = [x.lower() for x in sectionlist]
        
        # Check now if the section we want is there.
        if (self.resource.lower() not in sectionlist):
            raise RuntimeError("The resource specified in the job configuration is not \
                                found, this could either not exist or be misspelled.")

        # Lets now check if the section that is chosen actually has any options.
        optionlist = config.options(self.resource)
        if(len(optionlist) == 0):
            raise RuntimeError("No options are specified in the specified config file section \
                                sections are defined within [] followed by a list of params: \
                                [section name] \
                                param1 = val1 \
                                param2 = val2 \
                                etc.")
            
        # Now load in the options and place them into the hostparams dictionary, the scheduler
        # option can be missing as this can be tested later using the test functions of the library.
        for param in self.hostparams:
            try:
                self.hostparams["param"] = config[self.resource][param]
            except:
                if(param == "scheduler")
        
            
    def savehostconfigs(self, flag, value):
        
        
        """Save the parameters to the config file."""
        
        #Bind the hosts file to the config parser
        configs = configparser.ConfigParser()
        
        configs.read(self.configfile)
        
        configs.set(self.resource, flag, value)
        
        with open(self.configfile, 'w') as conf:
            configs.write(conf)
            
                
    def checkparams(self):
        
        
        """Some rudimentary checks on the parameters, make sure the key ones exist."""
        
        #Exit with error if no username is provided.
        if (self.user == ""):
            sys.exit("ERR: No username provided for remote resource in the .conf file")
            
        #Exit with error message if the host field is blank.
        if (self.host == ""):
            sys.exit("ERR: No host provided for remote resource in the .conf file")
               
        #Some machines require non standard ports, if not specified then set it to the default ssh port.
        if (self.port == ""):
            self.port = "22"
            print("Port has not been specified for remote host, setting for ssh default on port 22")
            
            
class JobConfig:
    
    #TODO: add support here later for multijob batch prescription
    def __init__(self, jobfile):
        
        
        logger.info("Loading the job configuration parameters")
        
        # Dictionary for the host config params.
        jobparams = {
                      "resource": "",
                      "program": "",
                      "account": "",
                      "localworkdir": "",
                      "remoteworkdir": "",
                      "maxtime": "",
                      "nodes": "",
                      "cores": "",
                      "corespernode": "",
                      "executable": "",
                      "frequency": "",
                      }
        
        # Get the configs
        self.loadjobconfigs(jobfile)
        
        self.checkparams()
        
        
    def loadjobconfigs(self, jobfile):
        

        # Bind the config parser to the job file
        jobconfigs = configparser.ConfigParser()
        jobconfigs.read(jobfile)
        
        # Parse all the config entries under default
        for index in jobconfigs['default']:
            vars(self)[index] = jobconfigs['default'][index]
            
            
    def checkparams(self):
        
        
        pass
            