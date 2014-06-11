import logging

logger = logging.getLogger("ProxyApp")

class Applications:
    
    
    """A factory class which will return the correct class of the application specific commands"""
        
    def test(command, jobparams):
        
        # Make arg (program) from command line lower all lower case (less susceptible to error in the wild).
        tmp = jobparams["program"].lower()
        
        # Establish software being used and select class to instantiate.
        if(tmp == "amber"): return Amber(command, jobparams["executable"])
        elif(tmp == "charmm"): return Charmm(command, jobparams["executable"])
        elif(tmp == "gromacs"): return Gromacs(command, jobparams["executable"])
        elif(tmp == "lammps"): return Lammps(command, jobparams["executable"])
        elif(tmp == "namd"): return Namd(command, jobparams["executable"])
        else:
            raise RuntimeError("Failed to instantiate the app class, check that the program parameter is set and corresponds to one of the supported applications")
        
    test = staticmethod(test)

class Amber:
    
    
    """Class specific to methods for processing Amber jobs."""
    
    def __init__(self, command, executable):
        
        
        logger.info("Application requested is Amber, now test to see if it's executable; " + executable + " is in your path.")

        # Check to see if amber is in the path
        if(executable != ""):
            # If user specifies an executable to use then check for it.
            if(command.runremote(["which " + executable + " &> /dev/null"])[0] != 0):
                raise RuntimeError(executable + " is not in your path, if your machine uses modules add the module load to your bash profile.")
            else: 
                logger.info(executable + " has been found in your path.")
        else:
            raise("The executable parameter was not set.")
    
    def processjob(self, app_args, executable):
        
        logger.info("Processing job to extract files that require upload.")
        
        # List for files that need staging.
        filelist = []
        
        # Append executable to args string.
        args = executable 
        
        # Process the command line args and find files for staging.
        for item in app_args:
            index = app_args.index(item)
            
            # Put ALL of the args specified on the commandline into a string.
            args = args + " " + item
            
            # Find the amber input files that require staging.
            if(item == "-i"): filelist.append(app_args[index+1])
            if(item == "-c"): filelist.append(app_args[index+1])
            if(item == "-p"): filelist.append(app_args[index+1])
        
        # Log results.
        logger.info("Files for upload: " + "".join(filelist))
        logger.info("String for submitting simulation: " + args)
        
        return filelist, args

class Charmm:
    
    
    """Class specific to methods for processing Charmm jobs."""
    
    def __init__(self, command, executable):
        
        logger.info("Application requested is Charmm, now test to see if it's executable; " + executable + " is in your path.")
        
        # TODO: add charmm specific path checks
    
    def processjob(self, app_args):
        print("Charmm job")
    
class Gromacs:
    
    
    """Class specific to methods for processing Gromacs jobs."""
    
    def __init__(self, command, executable):
        
        logger.info("Application requested is Gromacs, now test to see if it's executable; " + executable + " is in your path.")
        
        # TODO: add Gromacs specific path checks
    
    def processjob(self, app_args):
        print("Gromacs job")
    
    
class Lammps:
    
    
    """Class specific to methods for processing Lammps jobs."""
    
    def __init__(self, command, executable):
        
        logger.info("Application requested is Lammps, now test to see if it's executable; " + executable + " is in your path.")
        
        # TODO: add Lammps specific path checks
    
    def processjob(self, app_args):
        print("Lammps job")
    
class Namd:
    
    
    """Class specific to methods for processing Namd jobs."""
    
    def __init__(self, command, executable):
        
        logger.info("Application requested is Namd, now test to see if it's executable; " + executable + " is in your path.")
        
        # TODO: add Namd specific path checks
    
    def processjob(self, app_args):
        print("Namd job")
    