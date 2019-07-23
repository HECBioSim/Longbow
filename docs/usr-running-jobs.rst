Running Jobs
************

**This section explains Longbow concepts for running jobs.**

Running jobs with Longbow is designed to be as intuitive as possible. In fact, the command to submit a job using Longbow deliberately mimics that to run the MD code itself::

    longbow [longbow arguments] executable [executableargs]

Due to the way Longbow handles its command-line, in many cases, users can simply place the command "longbow" in front of the ordinary MD command-line to run their job using Longbow. In the following sections, guidelines to running the various types of jobs Longbow supports are outlined. Namely, single jobs, replicate jobs and multi-jobs.
 
Single Jobs
===========

Single jobs are the simplest type of job that Longbow can run, these are the Longbow enabled equivalent of single jobs submitted to the batch system with the added benefit of having Longbow handle all staging and monitoring of jobs for you.

For a simple CHARMM job that may be submitted with the following::

    charmm -i example.inp

The Longbow equivalent could be as simple as::

    longbow charmm -i example.inp

Generally users like to see output on the terminal they are using so our command-line becomes a tad longer::

    longbow --verbose charmm -i input.inp

Or with longbow arguments hosts, job and log files explicitly stated::

    longbow --job /path/filename --log /path/filename --hosts /path/filename charmm -i example.inp

That is all there is to it, the results files will appear in the working directory of your local machine as if the jobs had run there. There are examples of single jobs for all five supported packages covered in our **quick start section**.

**Referring to other files within input files**

Note, that for a single job, Longbow would expect and require all executableargs input files to be in the current working directory where the job is being ran from. Furthermore, Longbow requires just filenames to be provided, both on the Longbow command line in executableargs and within input files. DO NOT provide the paths to the files. The exception is when the user wishes to use a file that is already on the HPC machine as an additional input file. In this case the user should give the full path to the file.

Below is a CHARMM example demonstrating these points:

    longbow --job /path/filename --log /path/filename --hosts /path/filename charmm -i example.inp

Notice in the the command-line that the path to example.inp has NOT been provided as this should be in the current working directory. But inside that input file we might have:: 

    ...
    # input file in the current working directory provided WITHOUT the path as required
    read param card name par_all27_prot_lipid.prm
    ...
    # input file on the remote resource provided WITH the path as required
    OPEN UNIT 1 CARD READ NAME /charmm/c34b2/toppar/top_all27_prot_na.rtf
    ...

The file supplied without its full path should reside in the current working directory along with your other job files and Longbow will detect it and stage it to the simulation directory on the HPC machine. However the file with the full path points to a path of a file that is already stored on the HPC machine, perhaps as part of a large library of common files in a database.

 

Replicate Jobs
==============

Replicate jobs are the Longbow equivalent of job arrays, they are useful for submitting larger numbers of jobs that have similar files and command-line structures.

By default, replicate jobs have a very defined directory structure, the subdirectories must be of the format /repX where X is a number from 1 to N where N is the number of replicate jobs you wish to run. However the naming scheme can be changed such that different directory naming can be used to match your use case for example by supplying "replicate-naming = run" in a configuration file you can now have directories of the format runX where x is a number from 1 to N where N is the number of replicates.

Longbow can also handle "global files", these are files that would be identical across all of the replicate jobs and thus would simply be duplicating files if they were to be transferred, this is a waste of disk space. So to prevent this wastage, Longbow allows files to be placed in the job parent directory (ie the same level as the repx directories). Longbow will then detect these files and automatically change the paths in the generated job submit files to point to the global ones. Global files can also act like overrides so if there is a file of the same name within the repX directory and parent directory then the parent directory file overrides the ones in the individual jobs. 

Furthermore, if all input files are "global", you have no need to create the repX directories at all, Longbow will generate them for you, but this is only useful if the input files are identical across all simulations.

A real example of a similar structure for a NAMD replicate job can be found in the **quick start examples** section of this guide. An illustrative example of how such a job would be structured and its corresponding command-line can be seen below::

    current working directory/
        solvated.pdb
        solvated.psf
        par_all27_prot_lipid.prm
        /rep1
            example.in
            relres.coor
            relres.vel
            relres.xsc
        /rep2
            example.in
            relres.coor
            relres.vel
            relres.xsc
        /rep3
            example.in
            relres.coor
            relres.vel
            relres.xsc
        .
        .
        .
        /repN
            example.in
            relres.coor
            relres.vel
            relres.xsc

This job can be executed with a command of the form::

    longbow --verbose -replicates N namd2 example.in

**Referring to other files within input files**

Some simulation codes allow files to be referenced from within the input files (the ones you gave on the command-line) and if Longbow is to work for this, it needs to detect and transfer those files to the HPC machine. You will also need to make sure you reference the paths correctly in these files based on how your job is configured. The following scenarios will show you how to do this for each different scenario.

**Input files in the repX subdirectories**

Input files in the repX subdirectories should refer to files in the same directory by providing just the filename. On the other hand files in the job parent directory should be referred to using ../filename.

Below is a modified extract from longbow-examples/ReplicateJob/rep1/example.in that demonstrates these points::

    # files in the job parent directory (longbow-examples/replicate_job/)
    structure         ../solvated.psf
    parameters        ../par_all27_prot_lipid.prm
    coordinates       ../solvated.pdb
    
    # files in the rep1 subdirectory (longbow-examples/replicate_job/rep1)
    binvelocities       relres.vel
    bincoordinates      relres.coor
    ExtendedSystem      relres.xsc

**Input files in job parent directory**

Input files in the parent directory of the repX subdirectories (current working directory e.g. longbow-examples/replicate_job) can also refer to files in the same directory and in the repX subdirectories. Files in the same directory as the input file in question can be referred to by providing no path. Files in the repX subdirectories on the other hand can be referred to by ./repX/filename.

Below is a fictitious file that is not included in the example in longbow-examples/replicate_job, but is shown here just to demonstrate the principles just outlined

in longbow-examples/replicate_job/fictitiousfile.in::

    # files in the job parent directory (longbow-examples/replicate_job/)
    structure         solvated.psf
    parameters      par_all27_prot_lipid.prm
    coordinates     solvated.pdb

    # files in the rep1 subdirectory (longbow-examples/replicate_job/rep1)
    binvelocities       ./rep1/relres.vel
    bincoordinates      ./rep1/relres.coor
    ExtendedSystem      ./rep1/relres.xsc

**How to reference files on the remote resource** 

Files that are on the remote resource should be referred to in input files by providing the full path to the file, this differentiation in path types allows Longbow to make the distinction between intentional files missing locally and a user mistake (which would be reported accordingly)::

    ...
    parameters        /namdfiles/on/the/remote/resource/par_all27_prot_lipid.prm
    ...
 
Multi-Jobs
==========

A powerful feature of Longbow is it's ability to send multiple single and replicate jobs off to many different HPC machines with the execution of a single command. Two examples of this can be found in the Longbow examples. In those examples there is an example of running a single and replicate Amber job simultaneously and an example of running multiple applications. These illustrate just two use cases of this job type, in reality all kinds of things are possible here such as running portions of jobs on different HPCs, to using different accounts or queues etc. To run a multi-job, you simply include more than one job in a job configuration file. Below is the example taken from longbow-examples/multiple_jobs/different_job_types.

longbow-examples/multiple_jobs/different_job_types/job.conf::

    [single]
    resource = Archer
    queue = short
    executable = pmemd.MPI
    maxtime = 00:10
    executableargs = -i example.in -c example.rst -p example.top -o example.out
    
    [replicate]
    resource = Archer
    queue = short
    executable = pmemd.MPI
    maxtime = 00:10
    executableargs = -i example.in -c example.rst -p example.top -o example.out
    replicates = 5

The job directory structure would look like the following::

    longbow-examples/multiple_jobs/different_job_types/
        job.conf
        single/
            example.in
            example.rst
            example.top
        replicate/
            example.rst
            example.top
            rep1/
                example.in
            rep2/
                example.in
            rep3/
                example.in
            rep4/
                example.in
            rep5/
                example.in

This job is simply run by executing the following from the directory containing job.conf::

    longbow --job job.conf --verbose

Note that it is essential for the subdirectory names to be the same as the names of the jobs in the square brackets in the job configuration file, job.conf. Longbow can handle very large numbers of jobs, even if the HPC resource you are submitting to has a limit on how many jobs can be in the queue at any single time, in these cases Longbow will batch up the jobs and submit new ones as old ones finish so as to make full use of your individual queue limits.
 
Supported Executables and Command-line Flags
============================================

Users should use the same command line flags and operators when running an MD package through longbow as they would normally. Below are the flags that are required by Longbow for each supported MD package. If those listed below are not provided Longbow will issue an error.

**Amber**

Executables: pmemd, pmemd.MPI, pmemd.cuda

Amber command line flags: -i, -c, -p

**CHARMM**

Executables: charmm, charmm_mpi, charmm_cuda

CHARMM command line flags: None are mandatory. The user must decide whether to use -i, <, ...

However, if using < on the command line, ensure that it is used in quotation marks (""). For example::

    longbow charmm "<" input.inp

**Gromacs**

Executables: gmx, gmx_d, mdrun, mdrun_d, mdrun_mpi, mdrun_mpi_d

Gromacs command line flags: -s or -deffnm

**LAMMPS**

Executable: lmp_xc30, lmp_linux, lmp_gpu, lmp_mpi, lmp_cuda, lmp

LAMMPS command line flags: -i

**NAMD**

Executable: namd2, namd2.mpi, namd2.cuda

NAMD command line flags: None are mandatory. An input file is expected to follow the executable: namd2
 
Supported Substitutions
=======================

Longbow will detect input files such as topology files that need to be copied to the HPC machine along with the primary input file to the executable. Longbow does this by searching the primary input file for references to other files. Any additional input files that are found are also searched for references to input files in a recursive fashion until all input files are found. 

Longbow can detect when a user has performed a parameter substitution for input files either when provided on the command line as executableargs or within an input file itself. Below the substitutions that are supported are outlined package by package. 

**CHARMM**

Format of command line substitutions supported::

    longbow charmm myvar:myprot "<" example.inp
    longbow charmm myvar=myprot "<" example.inp

In-file substitutions supported::

    SET myvar = myprot
    OPEN UNIT 1 CARD READ NAME @myvar.pdb
 
and::

    SET myvar myprot
    OPEN UNIT 1 CARD READ NAME @myvar.pdb 

**LAMMPS**

Format of command line substitutions supported::

    longbow lmp_xc30 -var myvar mydata -i example.in -l output
    longbow lmp_xc30 -v p myprot -i example.in -l output

In-file substitutions supported::

    variable myvar equal mydata
    read_data       ${myvar}.data

and::

    variable p equal myprot
    coordinates     $p.pdb

**NAMD**

In-file substitutions supported::

    set myvar = myprot
    ExtendedSystem      $myVar.xsc

and::

    set myvar2 myparam
    parameters          $myvar2.prm

**Amber**
Not currently supported.

**Gromacs**
Not currently supported.
 
Disconnectable Sessions
=======================

A useful feature is the ability for Longbow to disconnect itself shortly after submitting jobs off to the HPC machines. This is useful for people running Longbow on desktop/laptop computers that don't have the luxury of being able to keep a connection live for the duration of simulations. By supplying a simple flag --disconnect, this tells Longbow that you simply want to submit and forget your jobs. 

Longbow will simply submit your jobs and then write out the details to a recovery file, by doing this the user always has the option to reconnect to the session later to automatically download files or to continue polling if desired. To initiate this feature one just simply adds the --disconnect flag to the Longbow part of the command-line::

    longbow --verbose --disconnect --log new.log namd2 ">" output.out

Persistent Reconnect/Recover Sessions
=====================================

For recovering an intentionally disconnected Longbow session or for the hopefully more rare occasions that Longbow for some reason crashes, be it due to a spate of network instability or simply rotten luck. Longbow has a recovery mode, this recovery mode is designed to reconnect Longbow with jobs that are running on the HPC. 

Even if you know that all your jobs have managed to finish since Longbow crashed you can still reconnect and have Longbow complete the final staging for you, this is particularly handy if you had many jobs running through your Longbow session. 

To start Longbow in recovery mode, you will need to supply the following command-line::

    longbow --recover recoveryfilename

You do not need to provide the path to a recovery file as Longbow stores these in ~/.longbow so it knows where to find them. They will typically have the time stamp of when the Longbow session was started, further inspection of the internals of the recovery file can confirm the job information to assist with choosing the correct recovery file (the filename will also appear in your logfile). 

A small number of flags can be provided with the recover flag, such as the debug, verbose or the log flag. Often users will want to display the outcome of the recovery to their terminal to make sure the session is recovered, or to change the location of the logging to a new file such that if anything goes wrong they have all information at hand. Here is an example of a user that wants to log to the screen to monitor the recovery, but also to log to a new file so there is a record of what went wrong in the original log file::

    longbow --verbose --log new.log --recover recoveryfilename

Update Disconnected Sessions
============================

For grabbing an update of job status and to download a snapshot of the current simulation output (can save transfer time at the end) an update mode is available. This mode will simply connect and grab the latest job/s status, it will update the state of downloaded files. Also, if you have jobs that have been held back by Longbow due to queue slot limits, and jobs already submitted have finished running, then Longbow will submit these before exiting disconnecting again. Once all jobs are finished and downloaded, then running this update mode will trigger the correct cleanup and exit procedure as if it was running in persistent mode.

To invoke this recovery mode, you just simply need to provide the recovery file to the --update flag::

    longbow --update recoveryfilename



