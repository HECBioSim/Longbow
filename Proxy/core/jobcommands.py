class Scheduler():
 
    def test(command):
        """Static function to form part of a factory class which will return the correct class of the scheduler specific commands"""
        
        #Scarf had to go first since for some strange reason it has qsub (PBS) present which just hangs as if waiting for input.
        tmp = command.sshconnection(["bsub -V"])
        if(tmp == 0): return Lsf()
        
        #The check for PBS.
        tmp = command.sshconnection(["qsub --version"])
        if(tmp == 0): return Pbs()
        
    test = staticmethod(test)
            
class Pbs(Scheduler):
    """A class of commands that can be invoked on machines running the PBS scheduler (Archer)"""
    
    # A function for submitting jobs
    def submit(self):
        print("PBS submit")
        
    # A function for deleting jobs    
    def delete(self):
        print("PBS delete")
        
    # A function for querying jobs
    def status(self):
        print("PBS status")
        
class Lsf(Scheduler):
    """A class of commands that can be invoked on machines running the LSF scheduler (SCARF a cluster machine at STFC used in testing)"""

    # A function for submitting jobs
    def submit(self):
        print("LSF submit")
        
    # A function for deleting jobs    
    def delete(self):
        print("LSF delete")
        
    # A function for querying jobs
    def status(self):
        print("LSF status")
