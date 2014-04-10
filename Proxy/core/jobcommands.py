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
            
            #The check for PBS.
            elif(command.sshconnection(["condor_version &> /dev/null"]) == 0): 
                print("This host appears to be running Condor so lets store that in the hosts.conf for next time.")
                resource.save_host_configs('scheduler', 'CONDOR')
                return Condor()
            
            #Fail we can't return a class so exit.
            else: sys.exit("Error: failed to successfully establish target scheduler environment")
            
        else:
            #Either user or a previous run has set the scheduler.
            #TODO: might be better to verify the scheduler environment but then again there would be no point in caching???
            if(resource.scheduler == 'LSF'): return Lsf()
            if(resource.scheduler == 'PBS'): return Pbs()
            if(resource.scheduler == 'CONDOR'): return Condor()
        
    test = staticmethod(test)
            
class Pbs(Scheduler):
    """A class of commands that can be invoked on machines running the PBS scheduler (Archer)."""
    
    # A function for submitting jobs
    def submit(self, command, submit_file):
        
        cmd = ["qsub " + submit_file]
        
        print(cmd)
        #command.sshconnection(cmd)
        
        #TODO: return a job id
        
    # A function for deleting jobs    
    def delete(self, job_id):
        
        #TODO: figure out a way to handle both singular and multijob deletions, I suspect that a list of job id's is the way to go here.
        cmd = ["qdel " + job_id]
        
        print(cmd)
        
    # A function for querying jobs
    def status(self, job_id):
       
        #TODO: figure out a way to handle both singular and multijob queries, I suspect that a list of job id's is the way to go here.
        cmd = ["qstat " + job_id]
        
        print(cmd)
        
    def job_file(self, file):
        
        #TODO: add multi job support
        
        with open(file) as job_file:
            job_file.write("#!/bin/bash")
            job_file.write("#PBS -N Amber")
            job_file.write("#PBS -A account")
            job_file.write("#PBS -l walltime=")
            job_file.write("#PBS -l mppwidth=")
            job_file.write("#PBS -l mppnppn=")
            job_file.write("export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)")
            job_file.write("cd $PBS_O_WORKDIR")
            
            
            
            job_file.write("done")
            job_file.write("wait")
            
    
        
class Lsf(Scheduler):
    """A class of commands that can be invoked on machines running the LSF scheduler (SCARF a cluster machine at STFC used in testing)."""

    # A function for submitting jobs
    def submit(self, command, submit_file):
        
        cmd = ["bsub " + submit_file]
        
        print(cmd)
        #command.sshconnection(cmd)
        
        #TODO: return a job id
        
    # A function for deleting jobs
    def delete(self, job_id):
        
        #TODO: figure out a way to handle both singular and multijob deletions, I suspect that a list of job id's is the way to go here.
        cmd = ["bdel " + job_id]
        
        print(cmd)
        
    # A function for querying jobs
    def status(self, job_id):
        
        #TODO: figure out a way to handle both singular and multijob queries, I suspect that a list of job id's is the way to go here.
        cmd = ["bjobs " + job_id]
        
        print(cmd)
        
    def job_file(self):
        
        print("lsf submit")
    
class Condor(Scheduler):
    """A class of commands that can be invoked on machines running the Condor scheduler."""

    #TODO: Add all the condor stuff (don't have a cluster running condor to test, so this may go in blind to begin with)

    # A function for submitting jobs
    def submit(self, command, submit_file):
        
        print("condor submit")
        
    # A function for deleting jobs
    def delete(self, job_id):
        
        print("condor delete")
        
    # A function for querying jobs
    def status(self, job_id):
        
        print("condor status")
        
    def job_file(self):
        
        print("condor job file")
