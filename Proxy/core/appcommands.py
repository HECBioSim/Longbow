import sys

class Applications:
    
    def test(args, app_args, command):
        """Static function to form part of a factory class which will return the correct class of the application specific commands"""
        
        #Make arg (program) from command line lower all lower case (less susceptible to error in the wild).
        tmp = args["program"].lower()
        
        #Establish software being used and select class to instantiate.
        if(tmp == "amber"): return Amber(app_args, command)
        elif(tmp == "charmm"): return Charmm(app_args, command)
        elif(tmp == "gromacs"): return Gromacs(app_args, command)
        elif(tmp == "lammps"): return Lammps(app_args, command)
        elif(tmp == "namd"): return Namd(app_args, command)
        else: sys.exit("Error: Fail to instantiate app class: check that the -prog arg is supplied correctly")
        
    test = staticmethod(test)

class Amber:
    
    def __init__(self, app_args, command):
                
        
        
        self.check_app(command)
        
    def check_app(self, command):
        
        #Bulk this out with better checking and custom compiled versions.
        if(command.sshconnection(["which pmemd"]) != 0):
            sys.exit("Error: fail to find amber")
    
    def something(self):
        print("Amber")


class Charmm:
    
    def __init__(self, app_args, command):
        pass
    
    def something(self):
        print("Charmm")
    
class Gromacs:
    
    def __init__(self, app_args, command):
        pass
    
    def something(self):
        print("Gromacs")
    
    
class Lammps:
    
    def __init__(self, app_args, command):
        pass
    
    def something(self):
        print("Lammps")
    
class Namd:
    
    def __init__(self, app_args, command):
        pass
    
    def something(self):
        print("Namd")
    