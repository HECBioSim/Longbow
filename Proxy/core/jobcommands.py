import sys

class Scheduler():
 
    def test(command, resource):
        """Static function to form part of a factory class which will return the correct class of the scheduler specific commands"""
        
        if (resource.scheduler == ""):
            print("No scheduler for this host is specified - let's see if it can be determined!")
            
            #Scarf had to go first since for some strange reason it has qsub (PBS) present which just hangs as if waiting for input.
            #todo: it might be better to take a look at the loaded modules to find the scheduler
            
            #Check for LSF
            if(command.sshconnection(["bsub -V &> /dev/null"]) == 0):
                print("This host appears to be running LSF so lets store that in the hosts.conf for next time.")
                resource.save_host_configs('scheduler', 'LSF')
                return Lsf()
        
            #The check for PBS.
            elif(command.sshconnection(["qsub --version &> /dev/null"]) == 0): 
                print("This host appears to be running PBS so lets store that in the hosts.conf for next time.")
                resource.save_host_configs('scheduler', 'PBS')
                return Pbs()
            
            #Fail we can't return a class so exit.
            else: sys.exit("Error: failed to successfully establish target scheduler environment")
            
        else:
            #Either user or a previous run has set the scheduler.
            #TODO: might be better to verify the scheduler environment but then again there would be no point in caching???
            if(resource.scheduler == 'LSF'): return Lsf()
            if(resource.scheduler == 'PBS'): return Pbs()
        
    test = staticmethod(test)
            
class Pbs(Scheduler):
    """A class of commands that can be invoked on machines running the PBS scheduler (Archer)"""
    
    # A function for submitting jobs
    def submit(self, command, submit_file):
        
        cmd = ["qsub " + submit_file]
        
        print(cmd)
        #command.sshconnection(cmd)
        
        #TODO: return a job id
        
    # A function for deleting jobs    
    def delete(self, job_id):
        
        #TODO: figure out a way to handle both singular and multijob deletions, I suspect that a list of job id's is the way to go here.
        cmd = ["qdel", job_id]
        
        print(cmd)
        
    # A function for querying jobs
    def status(self, job_id):
       
        #TODO: figure out a way to handle both singular and multijob queries, I suspect that a list of job id's is the way to go here.
        cmd = ["qstat", job_id]
        
        print(cmd)
        
    def job_file(self):
        pass
        
class Lsf(Scheduler):
    """A class of commands that can be invoked on machines running the LSF scheduler (SCARF a cluster machine at STFC used in testing)"""

    # A function for submitting jobs
    def submit(self, command, submit_file):
        
        cmd = ["bsub " + submit_file]
        
        print(cmd)
        #command.sshconnection(cmd)
        
        #TODO: return a job id
        
    # A function for deleting jobs
    def delete(self, job_id):
        
        #TODO: figure out a way to handle both singular and multijob deletions, I suspect that a list of job id's is the way to go here.
        cmd = ["bdel", job_id]
        
        print(cmd)
        
    # A function for querying jobs
    def status(self, job_id):
        
        #TODO: figure out a way to handle both singular and multijob queries, I suspect that a list of job id's is the way to go here.
        cmd = ["bjobs", job_id]
        
        print(cmd)
        
    def job_file(self):
        pass
