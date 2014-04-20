
class Staging:
    
    def stage_upstream(self, command, local_workdir, remote_workdir, filelist):
        
        #Create the dir ready for staging.
        if(command.listremote(remote_workdir) != 0): 
            command.sshconnection(["mkdir " + remote_workdir])
                    
        #Loop through the list of input files and upload them.
        for i in range (len(filelist)):
            command.uploadfile(local_workdir + "/" + filelist[i], remote_workdir)
    
    def stage_downstream(self, command, local_workdir, remote_workdir, filelist):
        
        #TODO: calls to scp download will go here
        for i in range (len(filelist)):
            print(filelist[i])