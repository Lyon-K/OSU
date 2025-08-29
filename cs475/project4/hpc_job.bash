#!/bin/bash
#SBATCH -J proj4
#SBATCH -A cs475-575
#SBATCH -p classgputest
#SBATCH --constraint=v100
#SBATCH --gres=gpu:1
#SBATCH -o output.out
#SBATCH -e output.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=keel@oregonstate.edu

ml slurm
ml cuda/11.6

nvcc -o all04 all04.cu -lm -Xcompiler=-fopenmp
./all04

