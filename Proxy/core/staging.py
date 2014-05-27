import logging

logger = logging.getLogger("ProxyApp")

class Staging:
    
    def stage_upstream(self, command, jobparams, filelist):
        
        logger.info("Preparing to stage files to remote host.")
        
        if(command.listremote(jobparams["remoteworkdir"]) != 0): 
            
            command.sshconnection(["mkdir " + jobparams["remoteworkdir"]])[0]
            logger.info(jobparams["remoteworkdir"] + " created successfully.")
            
        else: 
            logger.info(jobparams["remoteworkdir"] + " already exists so files will be staged here.")
            
        # Loop through the list of input files and upload them.
        for i in range (len(filelist)):
            
            command.uploadfile(jobparams["localworkdir"] + "/" + filelist[i], jobparams["remoteworkdir"])
            
        logger.info("Staging files complete.")
    
    def stage_downstream(self, command, jobconf):
        
        print("staging downstream")
        
        command.downloadfile(jobconf.remote_workdir + "/*", jobconf.local_workdir)
        
        print("staging files downstream complete.")