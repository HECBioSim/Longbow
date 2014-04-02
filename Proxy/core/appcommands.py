import sys

class Applications:
    
    def test(args, app_args):
        """Static function to form part of a factory class which will return the correct class of the application specific commands"""
        
        #Make arg (program) from command line lower all lower case (less susceptible to error in the wild).
        tmp = args["program"].lower()
        
        #Establish software being used and select class to instantiate.
        if(tmp == "amber"): return Amber(app_args)
        elif(tmp == "charmm"): return Charmm(app_args)
        elif(tmp == "gromacs"): return Gromacs(app_args)
        elif(tmp == "lammps"): return Lammps(app_args)
        elif(tmp == "namd"): return Namd(app_args)
        else: sys.exit("Fail to instantiate app class: check that the -prog arg is supplied correctly")
        
    test = staticmethod(test)

class Amber:
    
    def __init__(self, app_args):
                
        print(app_args)
        
        #("-i", "--mdin", help = "Input control data for the min/md run.", required = True)
        #("-o", "--mdout", help = "Output user readable state info and diagnostics -o stdout will send output to the terminal instead of file.")
        #("-inf", "--mdinfo", help = "Output latest mdout-format energy info.")
        #("-p", "--prmtop", help = "Input molecular topology, force field, periodic box type, atom and residue names.", required = True)
        #("-c", "--inpcrd", help = "Input initial coordinates and (optionally) velocities and periodic box size", required = True)
        #("-ref", "--refc", help = "Input (optional) reference coords for position restraints; also used for targeted MD.")
        #("-mtmd", "--mtmd", help = "Input (optional) containing list of files and parameters for targeted MD to multiple targets.")
        #("-x", "--mdcrd", help = "Output coordinate sets saved over trajectory.")
        #("-y", "--inptraj", help = "Input coordinate sets in trajectory format, when imin=5.")
        #("-v", "--mdvel", help = "Output velocity sets saved over trajectory.")
        #("-e", "--mden", help = "Output extensive energy data over trajectory.")
        #("-r", "--restrt", help = "Output final coordinates, velocity, and box dimensions if any - for restarting run.")
        #("-cpin", "--cpin", help = "Input protonation state definitions.")
        #("-cprestrt", "--cprestrt", help = "Protonation state definitions, final protonation states for restart (same format as cpin).")
        #("-cpout", "--cpout", help = "Output protonation state data saved over trajectory.")
        #("-evbin", "--evbin", help = "Input for EVB potentials.")
        #("-O", "--prmtop", help = "Overwrite output files if they exis.")
        #("-A", "--prmtop", help = "Append output files if they exist (used mainly for replica exchange).")
    
    def something(self):
        print("Amber")


class Charmm:
    
    def __init__(self, remnant_args):
        pass
    
    def something(self):
        print("Charmm")
    
class Gromacs:
    
    def __init__(self, remnant_args):
        pass
    
    def something(self):
        print("Gromacs")
    
    
class Lammps:
    
    def __init__(self, remnant_args):
        pass
    
    def something(self):
        print("Lammps")
    
class Namd:
    
    def __init__(self, remnant_args):
        pass
    
    def something(self):
        print("Namd")
    