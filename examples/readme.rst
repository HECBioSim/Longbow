****************
Longbow Examples
****************

longbow-examples contains a set of Molecular Dynamics input files that you can
use to learn how to use Longbow.

In the section below there is a list of the commands that will show you how to
submit the Longbow examples as jobs on an external resource (HPC) using these
files. 

Prior to attempting the examples you should firstly ensure that you have an
active account on a HPC machine and that the MD package of interest is
installed, then follow the documentation for adding your first HPC machine
account to Longbow at the following link

http://www.hecbiosim.ac.uk/longbow-docs?showall=&start=2#2.1

Note - We ensure that these examples work on the UK national supercomputer
ARCHER, whilst there is no reason to suspect that they will not work elsewhere,
there is a chance that software has been installed with different executable
names or in other non-default ways. In these cases you might need to slightly
modify the procedures described below. We are happy to provide support if
required.


How to Run
**********

The following instructions will assume you have downloaded and extracted the
examples and changed into the 'longbow-examples' directory path.

Quick Start Examples
********************

In the 'quick_start' directory, you can choose examples for your favourite
Molecular Dynamics package and learn how to submit a simple longbow job from
your local machine. 

AMBER
-----

Change into 'longbow-examples/quick_start/amber' and run:

longbow --verbose pmemd.MPI -O -i example.in -c example.min -p example.top -o example.out

CHARMM
------

Change into 'longbow-examples/quick_start/charmm' and run:

longbow --verbose charmm -i example.inp ">" example.out

GROMACS
-------

Change into 'longbow-examples/quick_start/gromacs' and run:

longbow --verbose gmx mdrun -s example.tpr -deffnm output

LAMMPS
------

Change into 'longbow-examples/quick_start/lammps' and run:

longbow --verbose lmp_xc30 -i example.in -l output

NAMD
----

Change into 'longbow-examples/quick_start/namd' and run:

longbow --verbose namd2 example.in ">" example.out

or for SMP builds (NAMD v2.12+)*:

longbow --verbose namd2 +ppn 23 +pemap 1-23 +commap 0 example.in ">" example.out

*The parameters "cores" and "corespernode" must be set to "1" in your hosts.conf

Replicate Job Example
*********************

In this directory, you will learn how to submit a replicate job. These are
useful for submitting ensembles of jobs where the command-line is identical but
a number of different runs or slightly different input files are used.

Change into 'longbow-examples/replicate_job' and run:

longbow --verbose --replicates 5 namd2 example.in

or for SMP builds (NAMD v2.12+)*:

longbow --verbose --replicates 5 namd2 +ppn 23 +pemap 1-23 +commap 0 example.in ">" example.out

*The parameters "cores" and "corespernode" must be set to "1" in your hosts.conf

Multi-Job Example
*****************

Multi-jobs are the most flexible type of job Longbow offers, they are basically
a fully customisable ensemble of jobs. The following examples show the
flexibility and power of using this type of job. These jobs use a job
configuration file to gain control over each jobs parameters separately.

Many Different Single Jobs
--------------------------

In the 'multiple-jobs/different_applications' directory, you can learn how to
submit multiple jobs that each use a different molecular dynamics package.

Change into 'longbow-examples/multiple-jobs/different_applications' and run:

longbow --job job.conf --verbose

Mixed Job Types
---------------

Have a bunch of simulations where some are replicates and some are simple
single use jobs? Then you can mix these too.

In the 'multiple-jobs/different_job_types' directory, you can learn how to
submit multiple jobs that are different types.

Change into 'longbow-examples/multiple-jobs/different_job_types' and run:

longbow --job job.conf --verbose


That's it for our quick start guide, check out the documentation for more 
in-depth information on what is configurable. You can build on the basic
concepts in these examples to create large-scale, multi-machine, large-volume
jobs where you no longer have to worry about job scripts and moving around
files.
