import argparse

class Applications:

    def Amber(self):
    
        parser = argparse.ArgumentParser()
    
        parser.add_argument("-i", "--test1", help = "Name of the computer resource for example Archer.", required = True)
        parser.add_argument("-j", "--test2", help = "Name of the software for example Amber.", required = True)
        parser.add_argument("-k", "--test3", help = "Name of the computer resource for example Archer.", required = True)
    
        #remnants = parser.parse_args(remnants)
    
        #print(remnants)
    
    def Charmm(self):
        pass
    
    def Gromacs(self):
        pass
    
    def Lammps(self):
        pass
    
    def Namd(self):
        pass