#!/bin/bash
#SBATCH -J  Proj07
#SBATCH -A  cs475-575
#SBATCH -p  classmpifinal
#SBATCH -N  8 # number of nodes
#SBATCH -n  16 # number of tasks
#SBATCH -o  proj07.out
#SBATCH -e  proj07.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=keel@oregonstate.edu

module load openmpi
mpic++ proj07.cpp -o proj07 -lm
for np in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
do
    mpiexec -mca btl self,tcp -np $np ./proj07
done
