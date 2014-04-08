import sys

class Scheduler():
 
    def test(command, resource):
        """Static function to form part of a factory class which will return the correct class of the scheduler specific commands"""
        
        if (resource.scheduler == ""):
            #Scarf had to go first since for some strange reason it has qsub (PBS) present which just hangs as if waiting for input.
            #todo: add writing ability for hosts.conf so this check is only ever done once per host.
            if(command.sshconnection(["bsub -V"]) == 0): 
                resource.save_host_configs('scheduler', 'LSF')
                return Lsf()
        
            #The check for PBS.
            #todo: add writing ability for hosts.conf so this check is only ever done once per host.
            elif(command.sshconnection(["qsub --version"]) == 0): 
                resource.save_host_configs('scheduler', 'PBS')
                return Pbs()
            
            #Fail
            else: sys.exit("Error: failed to successfully establish target scheduler environment")
            
        else:
            if(resource.scheduler == 'LSF'): return Lsf()
            if(resource.scheduler == 'PBS'): return Pbs()
        
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
