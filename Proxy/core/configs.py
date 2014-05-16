import configparser
import logging

logger = logging.getLogger("ProxyApp")

class HostConfig:
    
    """A class containing the host configuration methods."""
    
    def __init__(self, jobparams, configfile):
        
        
        """Declare the hostparams data structure, this is to ensure that is the user adds
           junk to their config or mispells something then it can be picked up and an 
           exception be raised. Also set here is a few class wide params to ensure that
           once instantiated we don't have to keep passing things around the library.
           For the time being, instantiating this class will trigger an autoload of the 
           config file."""
        
        self.configfile = configfile
        self.resource = jobparams["resource"]
        
        # Dictionary for the host config params.
        self.hostparams = {
                      "host": "",
                      "port": "",
                      "user": "",
                      "scheduler": ""
                      }
        
        # Load the remote resource configuration from the .conf file.
        self.loadhostconfigs()
        
        
    def loadhostconfigs(self):
        
        
        """Load the parameters from the config file."""
        
        logger.info("Loading configuration for destination computer from %s" % self.configfile)
        
        # Bind the hosts file to the config parser
        hostconfigs = configparser.ConfigParser()
        hostconfigs.read(self.configfile)
        
        # Check that we have some sections to read.
        sectionlist = hostconfigs.sections()
        if(len(sectionlist) == 0):
            raise RuntimeError("No sections defined in the host config file each section defines " +
                               "a supercomputer resource connection details, sections are defined " +
                               "within [] followed by a list of params of the form param1 = val1")
        
        # Make all sections in sectionlist lower case to be case agnostic.
        sectionlist = [x.lower() for x in sectionlist]
        
        # Check now if the section we want is there.
        if (self.resource.lower() not in sectionlist):
            raise RuntimeError("The resource specified in the job configuration is not " +
                               "found, this could either not exist or be misspelled.")

        # Lets now check if the section that is chosen actually has any options.
        optionlist = hostconfigs.options(self.resource)
        if(len(optionlist) == 0):
            raise RuntimeError("No options are specified in the specified config file section " +
                               "sections are defined within [] followed by a list of params of " +
                               "the form param1 = val1")
            
        # Now load in the options and place them into the hostparams dictionary, the scheduler
        # option can be missing as this can be tested later using the test functions of the library.
        for param in self.hostparams:
            try:
                self.hostparams[param] = hostconfigs[self.resource][param]
            except Exception as e:
                if(param != "scheduler"):
                    raise RuntimeError("Nothing has been specified for host parameter " + param + 
                                       " this is not optional.") from e
                    
                    if(param == "port"):
                        self.hostparams["port"] = "22"
                        logging.info("No port specified for host " + self.resource + " the default " +
                                     "port 22 is going to be used.")
                        
        
            
    def savehostconfigs(self, flag, value):
        
        
        """Save the parameters to the config file."""
        
        # Bind the hosts file to the config parser and read it in.
        configs = configparser.ConfigParser()
        configs.read(self.configfile)
        
        # Append the new option and value to the configuration.
        configs.set(self.resource, flag, value)
        
        # Save it.
        with open(self.configfile, 'w') as conf:
            configs.write(conf)
            
            
class JobConfig:
    
    """A class containing the job configuration methods."""
    
    def __init__(self, jobfile):
        
    
        """The data structure that is loaded from the config file is declared in a dictionary
           this is to prevent non useful data that a user might decide to provide being loaded
           into ProxyApp. This could be useful if other programs make use of this library and
           common config files are desired.
           For the time being, instantiating this class will trigger an autoload of the job
           config file."""
           
        # Dictionary for the host config params.
        # TODO: For multijob groups this probably ought to be either a dictionary of dictionaries 
        # or a list of dictionaries (basically a 2D data structure. For batching jobs, add the batch
        # or reps param to the dictionary. Implementing both of these will allow one to supply all of
        # single jobs, batched jobs, multiple single jobs with different configs, multiple batched jobs
        # this should just about nail most job requirements.
        self.jobparams = {
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
        
        # Get the configs.
        self.loadjobconfigs(jobfile)
        
        
    def loadjobconfigs(self, jobfile):
        
        
        """Load the parameters from the job config file."""
        
        logger.info("Loading up the job configuration file and obtain all job set parameters.")
        
        # Bind the config parser to the job file.
        jobconfigs = configparser.ConfigParser()
        jobconfigs.read(jobfile)
        
        # Check that we have some sections to read.
        sectionlist = jobconfigs.sections()
        if(len(sectionlist) == 0):
            raise RuntimeError("No sections defined in the job config file each section defines " +
                               "a job configuration, sections are defined within [] followed by a " +
                               "list of params of the form param1 = val1 etc.")
        
        #TODO: Delete this once the multijobs is supported.
        # Parse all the config entries under default.
        section = sectionlist[0]
        
        # Parse all the config entries under first section.
        for param in self.jobparams:
            
            try:
                self.jobparams[param] = jobconfigs[section][param]
            except Exception as e:
                if (param != "batch"):
                    raise RuntimeError("The " + param + " parameter seems to have something wrong with it, " +
                                       "either it is missing or it maybe the param name is not all " +
                                       "lowercase or misspelled.") from e
                else:
                    pass
        
        #TODO: Once the multijobs are supported then this should be used and modified accordingly if necessary.
        # Loop through all sections in the jobfile (we are assuming any job config specified is there
        # to be run. 
        #for section in sectionlist:
           
            # Parse all the config entries under default.
            #for param in self.jobparams:
            
                #try:
                #    self.jobparams[param] = jobconfigs[section][param]
                #except:
                #   if (param != "batch"):
                        #raise RuntimeError("The " + param + " seems have something wrong with it, either it \
                        #                    is missing or it maybe the param name is not all lowercase or missspelled.")
                        #else:
                            #pass
            