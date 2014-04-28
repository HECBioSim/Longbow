
class Staging:
    
    def stage_upstream(self, command, localworkdir, remoteworkdir, filelist):
        
        #Create the dir ready for staging.
        print("Creating dir " + remoteworkdir + " ready for staging files.")
        
        if(command.listremote(remoteworkdir) != 0): 
            
            command.sshconnection(["mkdir " + remoteworkdir])[0]
            print("dir " + remoteworkdir + " created successfully.")
            
        else: print("dir " + remoteworkdir + " already exists.")
            
        #Loop through the list of input files and upload them.
        for i in range (len(filelist)):
            
            command.uploadfile(localworkdir + "/" + filelist[i], remoteworkdir)
            
        print("Staging files complete.")
    
    def stage_downstream(self, command, localworkdir, remoteworkdir):
        
        print("staging downstream")
        
        command.downloadfile(remoteworkdir + "/*", localworkdir)
        
        print("staging files downstream complete.")