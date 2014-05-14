import sys
import configparser
import logging

logger = logging.getLogger("ProxyApp Core")

class HostConfig:
    
    def __init__(self, resource, configfile):
        """Some declarations and their initialisation (for specific error checking) followed by some config params loading and some checking."""

        logger.info("Loading configuration for destination computer from ", configfile)
        
        self.configfile = configfile
        self.resource = resource
        
        # Dictionary for the host config params.
        hostparams = {
                      "host": "",
                      "port": "",
                      "user": "",
                      "scheduler": ""
                      }
        
        #Load the remote resource configuration from the .conf file.
        self.load_host_configs()
        
        #Check the configuration parameters for some basic errors.
        self.check_params()
        
    def load_host_configs(self):
        """Load the parameters from the config file."""
        
        #Bind the hosts file to the config parser
        configs = configparser.ConfigParser()
        configs.read(self.config_file)

        #Walk through the available file parameters for the resource specified on the command line -res flag
        for index in configs[self.resource]:
            vars(self)[index] = configs[self.resource][index]
            
    def save_host_configs(self, flag, value):
        """Save the parameters to the config file."""
        
        #Bind the hosts file to the config parser
        configs = configparser.ConfigParser()
        
        configs.read(self.configfile)
        
        configs.set(self.resource, flag, value)
        
        with open(self.configfile, 'w') as conf:
            configs.write(conf)
                
    def check_params(self):
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
        self.load_job_configs(jobfile)
        
    def load_job_configs(self, jobfile):

        # Bind the config parser to the job file
        jobconfigs = configparser.ConfigParser()
        jobconfigs.read(self.jobfile)
        
        # Parse all the config entries under default
        for index in jobconfigs['default']:
            vars(self)[index] = jobconfigs['default'][index]
            