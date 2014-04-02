import argparse

class Applications:
    
    def test(args, remnant_args):
        """Static function to form part of a factory class which will return the correct class of the application specific commands"""
        
        tmp = args["program"].lower()
        
        if(tmp == "amber"): return Amber()
        elif(tmp == "charmm"): return Charmm(remnant_args)
        elif(tmp == "gromacs"): return Gromacs(remnant_args)
        elif(tmp == "lammps"): return Lammps(remnant_args)
        elif(tmp == "namd"): return Namd(remnant_args)
        else: print("Fail to instantiate app class: check that the -prog arg is supplied correctly")
        
    test = staticmethod(test)

class Amber:
    
    #def __init__(self, remnant_args):
        
        #pass
        #parser = argparse.ArgumentParser()
        
        #parser.add_argument("-i", "--mdin", help = "Input control data for the min/md run.", required = True)
        #parser.add_argument("-o", "--mdout", help = "Output user readable state info and diagnostics -o stdout will send output to the terminal instead of file.")
        #parser.add_argument("-inf", "--mdinfo", help = "Output latest mdout-format energy info.")
        #parser.add_argument("-p", "--prmtop", help = "Input molecular topology, force field, periodic box type, atom and residue names.", required = True)
        #parser.add_argument("-c", "--inpcrd", help = "Input initial coordinates and (optionally) velocities and periodic box size", required = True)
        #parser.add_argument("-ref", "--refc", help = "Input (optional) reference coords for position restraints; also used for targeted MD.")
        #parser.add_argument("-mtmd", "--mtmd", help = "Input (optional) containing list of files and parameters for targeted MD to multiple targets.")
        #parser.add_argument("-x", "--mdcrd", help = "Output coordinate sets saved over trajectory.")
        #parser.add_argument("-y", "--inptraj", help = "Input coordinate sets in trajectory format, when imin=5.")
        #parser.add_argument("-v", "--mdvel", help = "Output velocity sets saved over trajectory.")
        #parser.add_argument("-e", "--mden", help = "Output extensive energy data over trajectory.")
        #parser.add_argument("-r", "--restrt", help = "Output final coordinates, velocity, and box dimensions if any - for restarting run.")
        #parser.add_argument("-cpin", "--cpin", help = "Input protonation state definitions.")
        #parser.add_argument("-cprestrt", "--cprestrt", help = "Protonation state definitions, final protonation states for restart (same format as cpin).")
        #parser.add_argument("-cpout", "--cpout", help = "Output protonation state data saved over trajectory.")
        #parser.add_argument("-evbin", "--evbin", help = "Input for EVB potentials.")
        #parser.add_argument("-O", "--prmtop", help = "Overwrite output files if they exis.")
        #parser.add_argument("-A", "--prmtop", help = "Append output files if they exist (used mainly for replica exchange).")
    
        #self.app_args = parser.parse_known_args(remnant_args)
        #print(self.app_args)
    
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
    