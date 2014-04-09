import sys

class Applications:
    
    def test(args, command, executable):
        """Static function to form part of a factory class which will return the correct class of the application specific commands"""
        
        #Make arg (program) from command line lower all lower case (less susceptible to error in the wild).
        tmp = args["program"].lower()
        
        #Establish software being used and select class to instantiate.
        if(tmp == "amber"): return Amber(command, executable)
        elif(tmp == "charmm"): return Charmm(command, executable)
        elif(tmp == "gromacs"): return Gromacs(command, executable)
        elif(tmp == "lammps"): return Lammps(command, executable)
        elif(tmp == "namd"): return Namd(command, executable)
        else: sys.exit("Error: Fail to instantiate app class: check that the -prog arg is supplied correctly")
        
    test = staticmethod(test)

class Amber:
    
    def __init__(self, command, executable):
        
        #user specified Amber, lets go ahead and do some tests.
        print("Application: Amber")

        #Check to see if amber is in the path
        #TODO: Bulk this out with better checking and custom compiled versions.
        #1. check if the user specifies an executable in the job conf file
        #2. if that is not true check if there is a default amber.
        #3. possibly then check for a module and load that (this would only work though with sessions the only other way would be to append it to the .bashrc??)
        if(executable != ""):
            #if user specifies an executable to use then check for it.
            if(command.sshconnection(["which " + executable + " &> /dev/null"]) != 0):
                sys.exit("Error the executable that you specified: " + executable + " is not in your path.")
            else: print(executable + " has been found in your path.")
        else:
            #Check if there is a vanilla executable
            if(command.sshconnection(["which pmemd &> /dev/null"]) != 0):
                sys.exit("Error: fail to find amber (pmemd)")
            else: print("a vanilla pmemd is present.")
        
        #command.sshconnection(["env"])
    
    
    def process_job(self, app_args):
        print("Amber")


class Charmm:
    
    def __init__(self, command, executable):
        #user specified Charmm, lets go ahead and do some tests.
        print("Application: Charmm")
        
        #TODO: add charmm specific path checks
    
    def process_job(self, app_args):
        print("Charmm")
    
class Gromacs:
    
    def __init__(self, command, executable):
        #user specified Gromacs, lets go ahead and do some tests.
        print("Application: Gromacs")
        
        #TODO: add Gromacs specific path checks
    
    def process_job(self, app_args):
        print("Gromacs")
    
    
class Lammps:
    
    def __init__(self, command, executable):
        #user specified Lammps, lets go ahead and do some tests.
        print("Application: Lammps")
        
        #TODO: add Lammps specific path checks
    
    def process_job(self, app_args):
        print("Lammps")
    
class Namd:
    
    def __init__(self, command, executable):
        #user specified Namd, lets go ahead and do some tests.
        print("Application: Namd")
        
        #TODO: add Namd specific path checks
    
    def process_job(self, app_args):
        print("Namd")
    