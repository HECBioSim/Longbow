import logging
import os

logger = logging.getLogger("ProxyApp")

class Applications:
    
    
    """A factory class which will return the correct class of the application 
    specific commands"""
        
    def test(command, jobparams):
        
        # Make arg (program) from command line lower all lower case (less 
        # susceptible to error in the wild).
        prog = jobparams["program"].capitalize()

        if (prog == ""): raise RuntimeError("The program parameter was not set in job config file.")
        
        # Test if the executable is there.
        logger.info("Application requested is " + prog + 
                    ", now test to see if it's executable; " + 
                    jobparams["executable"] + " is in your path.")

        # Check to see if executable is in the path
        if(jobparams["executable"] != ""): 
            
            if(command.runremote(["which " + jobparams["executable"] + " &> /dev/null"])[0] != 0):   
                raise RuntimeError(jobparams["executable"] + " is not in your path, if your machine uses modules add the module load to your bash profile.")
            else:  
                logger.info(jobparams["executable"] + " has been found in your path.")
        else:
            raise RuntimeError("The executable parameter was not set in job config file.")
        
        # Return the class 
        return globals()[prog]()
        
    test = staticmethod(test)

class Amber:
    
    
    """Class specific to methods for processing Amber jobs."""
    
    
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

    
    def processjob(self, app_args):
        print("Charmm job")
        
        
class Gromacs:
    
    
    """Class specific to methods for processing Gromacs jobs."""

    
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
                if(item == "-s" or
                   item == "-cpi" or
                   item == "-table" or
                   item == "-tabletf" or
                   item == "-tablep" or
                   item == "-tableb" or
                   item == "-rerun" or
                   item == "-ei" or
                   item == "-j" or
                   item == "-membed" or
                   item == "-mp" or
                   item == "-mn"): 
                    
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
                if(item == "-s" or
                   item == "-cpi" or
                   item == "-table" or
                   item == "-tabletf" or
                   item == "-tablep" or
                   item == "-tableb" or
                   item == "-rerun" or
                   item == "-ei" or
                   item == "-j" or
                   item == "-membed" or
                   item == "-mp" or
                   item == "-mn"):
                    
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
    
    
class Lammps:
   
 
    """Class specific to methods for processing Namd jobs.""" 
    
    
    def processjob(self, app_args):
        print("Lammps job")
    
    
class Namd:
    
    
    """Class specific to methods for processing Namd jobs."""

    
    def processjob(self, app_args):
        print("Namd job")


class Generic:

    """Class specific to methods for processing generic jobs."""
        
        
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
            
                # Put ALL of the args specified on the commandline into a string.
                args = args + " " + item
            
                # Check it is there.
                if(os.path.isfile(jobparams["localworkdir"] + "/" + item) == True):  
                
                    # Add it to the list.
                    filelist.append(item)

        # Else the batch should have many.    
        elif(int(jobparams["batch"]) > 1):
            
            # Process the batch job and extract any globals
            iappargs = iter(app_args)
            for item in iappargs:
                 
                # If a file with the same name as those in the subdirs is placed in the workdir then this 
                # will override those and act as a default.
                if(os.path.isfile(jobparams["localworkdir"] + "/" + item) == True):
                        
                    # Add file to list of files required to upload.
                    filelist.append(item)
                        
                    args = args + " ../" + item
                        
                else:
                        
                    # Put ALL of the args specified on the command line into a string.
                    args = args + " " + item
                        
                    # Else we just process all the files as normal.
                    for i in range(1, int(jobparams["batch"])+1):
                        
                        if(os.path.isfile(jobparams["localworkdir"] + "/rep" + str(i) + "/" + item) == True):
                            
                            # Add file to list of files required to upload.
                            filelist.append("rep" + str(i) + "/" + item)                                 
                
        # Log results.
        logger.info("Files for upload: " + ", ".join(filelist))
        logger.info("String for submitting simulation: " + args)
        
        return filelist, args