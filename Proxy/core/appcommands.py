import logging
import os

logger = logging.getLogger("ProxyApp")

class Applications:
    
    
    """A factory class which will return the correct class of the application specific commands"""
        
    def test(command, jobparams):
        
        # Make arg (program) from command line lower all lower case (less susceptible to error in the wild).
        tmp = jobparams["program"].lower()
        
        # Establish software being used and select class to instantiate.
        if(tmp == "amber"): return Amber(command, jobparams)
        elif(tmp == "charmm"): return Charmm(command, jobparams)
        elif(tmp == "gromacs"): return Gromacs(command, jobparams)
        elif(tmp == "lammps"): return Lammps(command, jobparams)
        elif(tmp == "namd"): return Namd(command, jobparams)
        else:
            raise RuntimeError("Failed to instantiate the app class, check that the program parameter is set and corresponds to one of the supported applications")
        
    test = staticmethod(test)

class Amber:
    
    
    """Class specific to methods for processing Amber jobs."""
    
    def __init__(self, command, jobparams):
        
        
        logger.info("Application requested is Amber, now test to see if it's executable; " + jobparams["executable"] + " is in your path.")

        # Check to see if amber is in the path
        if(jobparams["executable"] != ""):
            # If user specifies an executable to use then check for it.
            if(command.runremote(["which " + jobparams["executable"] + " &> /dev/null"])[0] != 0):
                raise RuntimeError(jobparams["executable"] + " is not in your path, if your machine uses modules add the module load to your bash profile.")
            else: 
                logger.info(jobparams["executable"] + " has been found in your path.")
        else:
            raise("The executable parameter was not set.")
    
    def processjob(self, app_args, jobparams):
        
        logger.info("Processing job/s to extract files that require upload.")
        
        # List for files that need staging.
        filelist = []
        
        # Append executable to args string.
        args = jobparams["executable"] 
        
        # Does the batch contain just a single job.
        if(int(jobparams["batch"]) == 1):
        
            # Process the command line args and find files for staging.
            iappargs = iter(app_args)
            for item in iappargs:
                index = app_args.index(item)
            
                # Put ALL of the args specified on the commandline into a string.
                args = args + " " + item
            
                # Find the amber input files that require staging.
                if(item == "-i" or
                   item == "-c" or
                   item == "-p" or
                   item == "-ref"): 
                    
                    # Add them to the list.
                    filelist.append(app_args[index+1])
                    
                    # Check it is there.
                    if(os.path.isfile(jobparams["localworkdir"] + "/" + app_args[index+1]) == False):
                        raise RuntimeError("A file you have supplied on commandline does not exist.")                    
                    
        # Else the batch should have many.    
        elif(int(jobparams["batch"]) > 1):
            
            # Process the batch job and extract any globals
            iappargs = iter(app_args)
            for item in iappargs:
                index = app_args.index(item)
                
                # Put ALL of the args specified on the command line into a string.
                args = args + " " + item
                
                # This only really needs doing for the inputs.
                if(item == "-i" or
                   item == "-c" or
                   item == "-p" or
                   item == "-ref"):
                    
                    # If a file with the same name as those in the subdirs is placed in the workdir then this 
                    # will override those and act as a default.
                    if(os.path.isfile(jobparams["localworkdir"] + "/" + app_args[index+1]) == True):
                        
                        # Add file to list of files required to upload.
                        filelist.append(app_args[index+1])
                        
                        args = args + " ../" + app_args[index+1]
                        
                        next(iappargs, None)
                        
                    else:
                        # Else we just process all the files as normal.
                        for i in range(1, int(jobparams["batch"])+1):
                            
                            # Add file to list of files required to upload.
                            filelist.append("rep" + str(i) + "/" + app_args[index+1])
                            
                            # Check it is there.
                            if(os.path.isfile(jobparams["localworkdir"] + "/rep" + str(i) + "/" + app_args[index+1]) == False):
                                raise RuntimeError("A file you have supplied on command line does not exist.")                                     
                    
        # Log results.
        logger.info("Files for upload: " + ", ".join(filelist))
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
    