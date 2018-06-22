Getting Started
***************

**Longbow is designed with beginner users in mind**

The best way to get started with using Longbow is to start out with the examples provided by us. This section will help you get going as quickly as possible, however whilst this section does enable you to get up and running quickly it is recommended that you read the later sections of this documentation to see the full range of features that are available. 

It is intended that if you are completely new to Longbow or for fresh installs, you should work through the following parts sequentially in order to get a feel for the steps involved in configuring Longbow.

Create Password-less SSH
========================

Once you have selected the first HPC machine that you would like to use with Longbow. The first and most important part (if you don't wish to write your password hundreds of times) is to configure SSH to connect using keyfiles instead of a password. A handy guide has been written on this `here <http://www.hecbiosim.ac.uk/passwordless-ssh>`_.

Once you have done this, then you are ready for the next part, below.

.. _add-hpc:

Adding a HPC machine to Longbow
===============================

This part is going to explain how to get your first HPC machine configured ready for running jobs. We are going to assume that you have not configured this file before, users that have previously configured their hosts can simply skip this part and use their existing information.

The first step is to make sure that the ~/.longbow/hosts.conf file got created during installation. You can do this by opening up a terminal and do::

    ls ~/.longbow

If you can see the hosts.conf file in the output of the above command then you can skip ahead to the next step, if however you see that the ~/.longbow directory is missing then you should create it by::

    mkdir ~/.longbow

Now we want to open up ~/.longbow/hosts.conf in our favourite text editor, here we will use nano. This step is valid for all users whether or not hosts.conf exists or not as it will be created if it does not exist and for those that have it already, any contents will be replaced in the next step::

    nano ~/.longbow/hosts.conf

Now we want to add in the configuration for our HPC resource in this example we will be adding configuration for an account on ARCHER but you can add something else in place of this. Longbow automatically chooses the HPC machine at the top of your hosts.conf if the you do not specify one to use when running a job, so by keeping your favourite HPC machine at the top then unless specified then this is where Longbow will run them. Copy and paste the following into your hosts.conf::

    [Archer]
    host = login.archer.ac.uk
    user = myusername
    remoteworkdir = /work/myproject/myproject/myusername/
    account = account-code

Now to explain a little about the information here. 

The name of HPC resource goes in the square brackets, this is important since we will use this name later when referring to resources to run on. 

You should then go through and edit the options underneath by replacing "myusername" with your login username on ARCHER, "myproject" with your project code (for example e280) on ARCHER and "account-code" with the your account code (for example e280-Surname).

That is it for the basic setup! There are lots more parameters that can be configured at the host level (see the **Longbow Configuration** and **Running Jobs** sections for more information). A good rule of thumb to decide where to use a parameter is if it doesn't change on a given HPC between jobs then you can put it in hosts.conf under the correct HPC machine.

Download Longbow Examples
=========================

Before getting started with running Longbow examples, you will need to download them. The are two ways to get these examples:

1. On the command-line, change to the location where you wish to download the examples to and run::

    longbow --examples

2. Download them manually from `here <http://www.hecbiosim.ac.uk/longbow-examples>`_ and unzip to a location of your choice.

Quick Start Examples
====================

In the examples directory you extracted in the previous part you should find a "quick_start" directory. Here there are input files for five common MD packages. Change into your favourite one to run a simple MD job. The command-line for each is given below.

longbow-examples/quick_start/amber::

    longbow --verbose pmemd.MPI -O -i example.in -c example.min -p example.top -o example.out

longbow-examples/quick_start/charmm::

    longbow --verbose charmm -i example.inp ">" example.out

longbow-examples/quick_start/gromacs::

    longbow --verbose gmx mdrun -s example.tpr -deffnm output

longbow-examples/quick_start/lammps::

    longbow --verbose lmp_xc30 -i example.in -l output

longbow-examples/quick_start/namd::

    longbow --verbose namd2 example.in ">" example.out

or for SMP builds (NAMD v2.12+)*::

    longbow --verbose namd2 +ppn 23 +pemap 1-23 +commap 0 example.in ">" example.out

\*The parameters "cores" and "corespernode" must be set to "1" in your hosts.conf

And that's it! Longbow should submit a job to the HPC machine specified at the top of ~/.longbow/hosts.conf.

Notice that the above commands are similar to ordinary MD commands except the longbow executable precedes them. This is designed to make Longbow as intuitive to use as possible.

For most users the job will run successfully first time. If your job does not, go to the :ref:`troubleshooting` or ask for :ref:`support`.

A Simple Replicate Job Example
==============================

Replicate jobs are convenient for submitting ensembles of jobs where the command-line for submission is identical for each job but either a number of different runs of the same files or slight variations of the input files are desirable. Replicates enables you to rapidly setup and launch large volumes of such simulations.

The replicate job example can be found in 'longbow-examples/replicate_job'. This particular example is a replicate job consisting of 5 NAMD replicates. You will notice that the jobs are split over 5 different directories of the naming structure repx where x = 1:5. Each directory then contains a portion of the input files which could contain slightly different parameters/variables. This job is also showing how global files are used, these are files that are input files that are identical between each replicate and thus we can save on transfer time and disk space only having one copy. Longbow will detect such files placed at the same directory level as the repx directories and automatically handle them for you.

To run this replicate job, you will notice it is not too much different from the simple NAMD example in the previous section. The difference being the --replicates flag to Longbow::

    longbow --verbose --replicates 5 namd2 example.in

or for SMP builds (NAMD v2.12+)*::

    longbow --verbose --replicates 5 namd2 +ppn 23 +pemap 1-23 +commap 0 example.in ">" example.out

\*The parameters "cores" and "corespernode" must be set to "1" in your hosts.conf

Each of the replicates will have been submitted and run and their results downloaded into the correct directories. That's it you have run your first replicate job!

Multijob Examples
=================

Multi-jobs are the most flexible type of job Longbow offers, they are basically a fully customisable ensemble of jobs. The following two examples show the flexibility and power of using this type of job. These jobs use a job configuration file to gain control over each jobs parameters separately.

Many Different Single Jobs
--------------------------

In the 'multiple-jobs/different_applications' directory, you can find a number of jobs that each use a different MD code and a job configuration script. This job configuration script allows us to provide parameters that differ on a per job basis, this means we can submit very different jobs to the same HPC machine all at once.

In the 'longbow-examples/multiple-jobs/different_applications' run::

    longbow --job job.conf --verbose

Longbow will launch each job to the same HPC machine but for each one, will use the correct MD code.

Mixed Job Types
---------------

Have a bunch of simulations where some are replicates and some are simple single use jobs? Then you can mix these too.

Change into 'longbow-examples/multiple-jobs/different_job_types' and run::

    longbow --job job.conf --verbose

You will notice that the command-line for multijobs looks identical for each use case, that was intentional! You can use this simple method to build extremely complex job workflows involving different input files, different codes, different HPC machines or different resource levels.
