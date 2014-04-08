import sys
import configparser

class HostConfig:
    
    def __init__(self, args, config_file):
        """Some declarations and their initialisation (for specific error checking) followed by some config params loading and some checking."""
        
        self.config_file = config_file
        self.args = args
        
        #Declare and initialise some params to default values.
        self.user = ""
        self.host = ""
        self.port = ""
        self.account = ""
        self.workdir = ""
        self.maxtime = ""
        self.cores = ""
        self.program = ""
        self.frequency = ""
        self.scheduler = ""
        self.config_file = config_file
        
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
        for index in configs[self.args['resource']]:
            vars(self)[index] = configs[self.args['resource']][index]
            
    def save_host_configs(self, flag, value):
        """Save the parameters to the config file."""
        
        #Bind the hosts file to the config parser
        configs = configparser.ConfigParser()
        
        configs.read(self.config_file)
        
        configs.set(self.args['resource'], flag, value)
        
        with open(self.config_file, 'w') as conf:
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
    
        