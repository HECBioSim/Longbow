
class Staging:
    
    def stage_upstream(self, command, jobconf, filelist):
        
        #Create the dir ready for staging.
        print("Creating dir " + jobconf.remote_workdir + " ready for staging files.")
        
        if(command.listremote(jobconf.remote_workdir) != 0): 
            
            command.sshconnection(["mkdir " + jobconf.remote_workdir])[0]
            print("dir " + jobconf.remote_workdir + " created successfully.")
            
        else: print("dir " + jobconf.remote_workdir + " already exists.")
            
        #Loop through the list of input files and upload them.
        for i in range (len(filelist)):
            
            command.uploadfile(jobconf.local_workdir + "/" + filelist[i], jobconf.remote_workdir)
            
        print("Staging files complete.")
    
    def stage_downstream(self, command, jobconf):
        
        print("staging downstream")
        
        command.downloadfile(jobconf.remote_workdir + "/*", jobconf.local_workdir)
        
        print("staging files downstream complete.")