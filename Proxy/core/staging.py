
class Staging:
    
    def __init__(self):
        pass
    
    def stage_upstream(self, command, local_workdir, remote_workdir, filelist):
        
        #calls to scp upload will go here
        for i in range (len(filelist)):
            print(filelist[i])
    
    def stage_downstream(self, command, local_workdir, remote_workdir, filelist):
        
        #calls to scp download will go here
        for i in range (len(filelist)):
            print(filelist[i])