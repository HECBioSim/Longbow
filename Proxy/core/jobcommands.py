import time
import logging

logger = logging.getLogger("ProxyApp")

class Scheduler():
    
    
    """A factory class which will return the correct class of the scheduler specific commands"""

    def test(command, resource):
        
        if (resource.hostparams["scheduler"] == ""):
            logger.info("No scheduler for this host is specified - attempt to determine it!")
            
            # Check for LSF
            if(command.runremote(["env | grep -i 'lsf' &> /dev/null"])[0] == 0):
                logger.info("This host appears to be running LSF so lets store that in the hosts.conf for next time.")
                resource.savehostconfigs('scheduler', 'LSF')
                return Lsf()
        
            # The check for PBS.
            elif(command.runremote(["env | grep -i 'pbs' &> /dev/null"])[0] == 0): 
                logger.info("This host appears to be running PBS so lets store that in the hosts.conf for next time.")
                resource.savehostconfigs('scheduler', 'PBS')
                return Pbs()
            
            # Fail we can't return a class so exit.
            else:
                raise RuntimeError("Unable to establish the scheduling environment to use, if it is known then provide it in hostconfig file.")
            
        else:
            
            # Either user or a previous run has set the scheduler.
            if(resource.hostparams["scheduler"].lower() == 'lsf'): 
                logger.info("Scheduler: LSF")
                return Lsf()
            elif(resource.hostparams["scheduler"].lower() == 'pbs'): 
                logger.info("Scheduler: PBS")
                return Pbs()
            else:
                raise RuntimeError("Unable to establish the scheduling environment to use, check for typos in the hostconfig file.")
        
    test = staticmethod(test)
            
            
class Pbs(Scheduler):
    
    
    """A class of commands that can be invoked on machines running the PBS scheduler (Archer)."""
    
    def submit(self, command, jobparams, submitfile):
        
        # Change into the working directory and submit the job.
        cmd = ["cd " + jobparams["remoteworkdir"] + "\n","qsub " + submitfile]
        
        # Process the submit
        error, output = command.runremote(cmd)
        
        output = output.rstrip("\r\n")
        
        # Check status here.
        if(error == 0):
            logger.info("Job submitted with id = " + output)
        else:
            raise RuntimeError("Something went wrong when submitting.")

        return output
        
          
    def delete(self, command, jobid):
        
        error, output = command.runremote(["qdel " + jobid])
        
        return error, output
        

    def status(self, command, jobid):
               
        error, output = command.runremote(["qstat | grep " + jobid])
        output = output.split()
        
        return error, output
        
    
    def jobfile(self, jobparams, args, filelist):
        
        
        """Create the PBS jobfile ready for submitting jobs"""
        
        #TODO: add multi job support
        #TODO: come up with some sensible defaults for if a param is left out of job.conf
        #TODO: come up with a sensible job naming scheme for -N
        
        # Open file for PBS script.
        pbsfile = "job.pbs"
        jobfile = open(jobparams["localworkdir"] + "/" + pbsfile, "w+")
        
        # Write the PBS script
        jobfile.write("#!/bin/bash \n"
                      "#PBS -N Test \n"
                      "#PBS -l select=" + jobparams["nodes"] + " \n"
                      "#PBS -l walltime=" + jobparams["maxtime"] + ":00:00 \n"
                      "#PBS -A " + jobparams["account"] + "\n"
                      "export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR) \n"
                      "cd $PBS_O_WORKDIR \n"
                      "export OMP_NUM_THREADS=1 \n"
                      "aprun -n " + jobparams["cores"] + " -N " + jobparams["corespernode"] + " " + args + " & \n")

        #jobfile.write("wait \n")
        
        # Close the file (housekeeping)
        jobfile.close()
    
        # Append pbs file to list of files ready for staging.
        filelist.extend([pbsfile])
        
        logger.info("Files for upload: " + "".join(filelist))
        
        return filelist, pbsfile


    def monitor(self, command, stage, jobconf, jobid):
        
        done = False
                
        while (done == False):
        
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
                
                    stage.stage_downstream(command, jobconf.local_workdir, jobconf.remote_workdir)
            
                elif(status[4] == "T"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Transferring job")
        
                elif(status[4] == "W"): 
                    print(time.strftime("%x"), " ", time.strftime("%X"), "  Waiting")   
            
            else: done = True     
                        
            time.sleep(float(jobconf.frequency))

            
class Lsf(Scheduler):
    
    
    """A class of commands that can be invoked on machines running the LSF scheduler (SCARF a cluster machine at STFC used in testing)."""


    def submit(self, command, jobparams, submitfile):
        
        # cd into the working directory and submit the job.
        cmd = ["cd " + jobparams["remoteworkdir"] + "\n","qsub " + submitfile + "| grep -P -o '(?<=\<)[0-9]*(?=\>)'"]
        
        #process the submit
        error, output = command.runremote(cmd)
        
        output = output.splitlines()[0]
                
        #check status here.
        if(error == 0):
            logger.info("Job submitted with id = " + output)
        else:
            raise RuntimeError("Something went wrong when submitting.")

        return output
        
        
    def delete(self, command, jobid):
        
        error, output = command.runremote(["bkill " + jobid])
        
        return error, output
        
        

    def status(self, command, jobid):
        
        error, output = command.runremote(["bjobs " + jobid])
        
        return error, output
        
        

    def jobfile(self, jobparams, args, filelist):
        
        
        """Create the LSF jobfile ready for submitting jobs"""
        
        #TODO: add multi job support
        #TODO: come up with some sensible defaults for if a param is left out of job.conf
        #TODO: come up with a sensible job naming scheme for -N
        
        # Open file for LSF script.
        lsffile = "job.lsf"
        jobfile = open(jobparams["localworkdir"] + "/" + lsffile, "w+")
        
        # Write the PBS script
        jobfile.write("#!/bin/bash \n"
                      "#BSUB -J Test \n"
                      "#BSUB -W " + jobparams["maxtime"] + ":00 \n"
                      "#BSUB -n " + jobparams["cores"] + "\n"
                      "mpirun -lsf" + " " + args + "\n")
        
        # Close the file (housekeeping)
        jobfile.close()
    
        # Append pbs file to list of files ready for staging.
        filelist.extend([lsffile])
        
        logger.info("Files for upload: " + "".join(filelist))
        
        return filelist, lsffile
        
     
    def monitor(self):
        pass
