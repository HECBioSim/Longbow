import argparse

class Applications:
    
    def test(args):
        """Static function to form part of a factory class which will return the correct class of the application specific commands"""
        
        tmp = args.program
        if(tmp == 'Amber'): return Amber()
        if(tmp == 'Charmm'): return Charmm()
        if(tmp == 'Gromacs'): return Gromacs()
        if(tmp == 'Lammps'): return Lammps()
        if(tmp == 'Namd'): return Namd()
        
    test = staticmethod(test)

class Amber:
    
    def something(self):
        print("Amber")
    
    #parser = argparse.ArgumentParser()
    
    #parser.add_argument("-i", "--test1", help = "Name of the computer resource for example Archer.", required = True)
    #parser.add_argument("-j", "--test2", help = "Name of the software for example Amber.", required = True)
    #parser.add_argument("-k", "--test3", help = "Name of the computer resource for example Archer.", required = True)
    
    #remnants = parser.parse_args(remnants)
    
    #print(remnants)

class Charmm:
    
    def something(self):
        print("Charmm")
    
class Gromacs:
    
    def something(self):
        print("Gromacs")
    
    
class Lammps:
    
    def something(self):
        print("Lammps")
    
class Namd:
    
    def something(self):
        print("Namd")
    