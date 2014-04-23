
class Staging:
    
    def stage_upstream(self, command, local_workdir, remote_workdir, filelist):
        
        #Create the dir ready for staging.
        print("Creating dir " + remote_workdir + " ready for staging files.")
        if(command.listremote(remote_workdir) != 0): 
            command.sshconnection(["mkdir " + remote_workdir])[0]
            print("dir " + remote_workdir + " created successfully.")
        else: print("dir " + remote_workdir + " already exists.")
            
        #Loop through the list of input files and upload them.
        for i in range (len(filelist)):
            command.uploadfile(local_workdir + "/" + filelist[i], remote_workdir)
            
        print("Staging files complete.")
    
    def stage_downstream(self, command, local_workdir, remote_workdir, filelist):
        
        #TODO: calls to scp download will go here
        for i in range (len(filelist)):
            print(filelist[i])