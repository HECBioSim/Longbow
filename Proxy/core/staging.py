import time
import os
import logging

logger = logging.getLogger("ProxyApp")

class Staging:
    
    def stage_upstream(self, command, jobparams, filelist):
        
        logger.info("Preparing to stage files to remote host.")
        
        # Check if the directory exists already.
        if(command.remotelist(jobparams["remoteworkdir"]) != 0): 
            
            # If not then try to create it, commands over SSH are prone to failure so a loop of 3 tries is used
            # with a wait time; escaping if there is not a problem.
            for i in range(3):
            
                error = command.runremote(["mkdir " + jobparams["remoteworkdir"]])[0]
                
                # If we have success then break.
                if(error == 0):
                    break
                
                # If we haven't escaped wait 10 seconds and have another go.
                time.sleep(10)
            
            # Check if we have escaped else we maxed out the retries and failed.
            if(error != 0):
                raise RuntimeError("Could not create directory")
            else:
                logger.info("dir '" + jobparams["remoteworkdir"] + "' created successfully.")   
            
        else: 
            logger.info("'" + jobparams["remoteworkdir"] + "' already exists so files will be staged here.")
            
        # Loop through the list of input files and upload them.
        for i in range (len(filelist)):
            
            for j in range(3):
                
                if(os.path.dirname(filelist[i]) != ""):
                    if(command.remotelist(jobparams["remoteworkdir"] + "/" + os.path.dirname(filelist[i])) != 0):
                        command.runremote(["mkdir " + jobparams["remoteworkdir"] + "/" + os.path.dirname(filelist[i])])
                
                error = command.upload(jobparams["localworkdir"] + "/" + filelist[i], jobparams["remoteworkdir"] + "/" + os.path.dirname(filelist[i]))
            
                # If we have success then break.
                if(error == 0):
                    break
            
                # If we haven't escaped wait 10 seconds and have another go.
                time.sleep(10)
            
            # Check if we have escaped else we maxed out the retries and failed.
            if(error != 0):
                raise RuntimeError("Could not upload file '" + filelist[i] + "'")
                
        logger.info("Staging files complete.")
    
    def stage_downstream(self, command, jobparams):
        
        logger.info("Staging from remote to local host.")
        
        for i in range(3):
        
            error = command.download(jobparams["remoteworkdir"] + "/*", jobparams["localworkdir"])
            
            # If we have success then break.
            if(error == 0):
                break

            # If we haven't escaped wait 10 seconds and have another go.
            time.sleep(10)
            
        # Check if we have escaped else we maxed out the retries and failed.
        if(error != 0):
            raise RuntimeError("Failed to download files from remote.")
        else:
            logger.info("Staging files complete.")
            