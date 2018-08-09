#!/bin/bash --login
#PBS -N testjob
#PBS -q debug
#PBS -l select=2:ncpus=24:mpiprocs=1
#PBS -l walltime=24:00:00

export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)
cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=1

module load namd

aprun -n 2 -N 1 namd2 +ppn 23 +pemap 1-23 +commap 0 bench.in > bench.log
