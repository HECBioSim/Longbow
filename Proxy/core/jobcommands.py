class Scheduler():
 
    def test(self):
        
        submitter = 'LSF'
        
        if(submitter=='PBS'): return Pbs()
        if(submitter=='LSF'): return Lsf()
        
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
            
Schedule = Scheduler.test('')

Schedule.submit()