import argparse

class Amber:
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-i", "--test1", help = "Name of the computer resource for example Archer.", required = True)
    parser.add_argument("-j", "--test2", help = "Name of the software for example Amber.", required = True)
    parser.add_argument("-k", "--test3", help = "Name of the computer resource for example Archer.", required = True)
    
    #remnants = parser.parse_args(remnants)
    
    #print(remnants)
    
class Charmm:
    pass
    
class Gromacs:
    pass
    
class Lammps:
    pass
    
class Namd:
    pass