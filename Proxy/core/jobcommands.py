import sys
import time


class Scheduler():
 
    def test(command, resource):
        """Static function to form part of a factory class which will return the correct class of the scheduler specific commands"""
        
        if (resource.scheduler == ""):
            print("No scheduler for this host is specified - let's see if it can be determined!")
            
            #Check for LSF
            if(command.sshconnection(["env | grep -i 'lsf' &> /dev/null"])[0] == 0):
                print("This host appears to be running LSF so lets store that in the hosts.conf for next time.")
                resource.save_host_configs('scheduler', 'LSF')
                return Lsf()
        
            #The check for PBS.
            elif(command.sshconnection(["env | grep -i 'pbs' &> /dev/null"])[0] == 0): 
                print("This host appears to be running PBS so lets store that in the hosts.conf for next time.")
                resource.save_host_configs('scheduler', 'PBS')
                return Pbs()
            
            #The check for Condor, condor doesn't appear to have any environment variables that we can use.
            elif(command.sshconnection(["condor_version &> /dev/null"])[0] == 0): 
                print("This host appears to be running Condor so lets store that in the hosts.conf for next time.")
                resource.save_host_configs('scheduler', 'CONDOR')
                return Condor()
            
            #Fail we can't return a class so exit.
            else: sys.exit("Error: failed to successfully establish target scheduler environment")
            
        else:
            
            #Either user or a previous run has set the scheduler.
            if(resource.scheduler == 'LSF'): 
                print("Scheduler: LSF")
                return Lsf()
            if(resource.scheduler == 'PBS'): 
                print("Scheduler: PBS")
                return Pbs()
            if(resource.scheduler == 'CONDOR'): 
                print("Scheduler: CONDOR")
                return Condor()
        
    test = staticmethod(test)
            
            
class Pbs(Scheduler):
    """A class of commands that can be invoked on machines running the PBS scheduler (Archer)."""
    
    # A function for submitting jobs
    def submit(self, command, workdir, submitfile):
        
        #cd into the working directory and submit the job.
        cmd = ["cd " + workdir + "\n","qsub " + submitfile]
        
        #process the submit
        error, output = command.sshconnection(cmd)
        
        output = output.rstrip("\r\n")
        
        #check status here.
        if(error == 0):
            print(time.strftime("%x"), " ", time.strftime("%X"), "  Job submitted with id = " + output)
        else:
            print("Something went wrong when submitting. Here is the error code = ",  error)

        return output
        
    # A function for deleting jobs    
    def delete(self, command, jobid):
        
        error, output = command.sshconnection(["qdel " + jobid])
        
        return error, output
        
    # A function for querying jobs
    def status(self, command, jobid):
               
        error, output = command.sshconnection(["qstat | grep " + jobid])
        output = output.split()
        
        return error, output
        
    def jobfile(self, filepath, nodes, cores, corespernode, reps, account, walltime, args, filelist):
        
        #TODO: add multi job support
        #TODO: this method may become code specific, if that is the case then move this to the appcommands under the relevant app class.
        #TODO: come up with some sensible defaults for if a param is left out of job.conf
        #TODO: come up with a sensible job naming scheme for -N
        
        #Open file for PBS script.
        file = "job.pbs"
        jobfile = open(filepath + "/" + file, "w+")
        
        jobfile.write("#!/bin/bash \n")
        jobfile.write("#PBS -N Test \n")
        jobfile.write("#PBS -l select="+nodes+" \n")
        jobfile.write("#PBS -l walltime=" + walltime + ":00:00 \n")
        jobfile.write("#PBS -A " + account + "\n")
        
        #Make sure links are resolved (not symbolic)
        jobfile.write("export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR) \n")
        jobfile.write("cd $PBS_O_WORKDIR \n")
        jobfile.write("export OMP_NUM_THREADS=1 \n")
        
        #Assemble the aprun string
        jobfile.write("aprun -n " + cores + " -N " + corespernode + " " + args + " & \n")
        
        jobfile.write("done \n")
        jobfile.write("wait \n")
        
        #Close the file (housekeeping)
        jobfile.close()
    
        #Append pbs file to list of files ready for staging.
        filelist.extend([file])
        
        print("List of files for upload: ", filelist)
        
        return filelist, file
    
    def monitor(self, command, stage, frequency, jobid, localworkdir, remoteworkdir):
        
        done = "False"
                
        while (done == "False"):
        
            error, status = self.status(command, jobid)
            
            if(error == 0):

                if(status[4] == "E"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Exiting")
            
                elif(status[4] == "H"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Held")
        
                elif(status[4] == "Q"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Queued")
        
                elif(status[4] == "R"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Running")
                
                    stage.stage_downstream(command, localworkdir, remoteworkdir)
            
                elif(status[4] == "T"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Transferring job")
        
                elif(status[4] == "W"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Waiting")   
            
            else: done = "True"     
                        
            time.sleep(float(frequency))

            
class Lsf(Scheduler):
    """A class of commands that can be invoked on machines running the LSF scheduler (SCARF a cluster machine at STFC used in testing)."""


    # A function for submitting jobs
    def submit(self, command, submitfile):
        
        cmd = ["bsub " + submitfile]
        
        print(cmd)
        
        
    # A function for deleting jobs
    def delete(self, jobid):
        
        cmd = ["bdel " + jobid]
        
        print(cmd)
        
        
    # A function for querying jobs
    def status(self, jobid):
        
        cmd = ["bjobs " + jobid]
        
        print(cmd)
        
        
    # A function for creating the LSF submit file.
    def jobfile(self):
        pass
        
    
    # A function for monitoring LSF jobs.   
    def monitor(self):
        pass
    
    
class Condor(Scheduler):
    """A class of commands that can be invoked on machines running the Condor scheduler."""

    #TODO: Add all the condor stuff (don't have a cluster running condor to test, so this may go in blind to begin with)

    # A function for submitting condor jobs.
    def submit(self, command, submitfile):
        pass
        
        
    # A function for deleting condor jobs.
    def delete(self, jobid):
        pass

        
    # A function for querying condor jobs.
    def status(self, jobid):
        pass


    # A function for creating the job file for submitting.  
    def jobfile(self):
        pass
    
    
    # A function for condor specific monitoring.
    def monitor(self):
        pass
