#!/bin/bash
#SBATCH -J JobName
#SBATCH -A cs475-575
#SBATCH -p classgpufinal
#SBATCH --constraint=v100
#SBATCH --gres=gpu:1
#SBATCH -o output.out
#SBATCH -e output.err

ml cuda cudnn

for t in 1024 4096 16384 65536 262144 1048576 2097152 4194304
do
        for b in 8 32 64 128 256 512 1024 2048 4096 8192
        do
                /usr/local/apps/cuda/11.7/bin/nvcc -DNUMTRIALS=$t -DBLOCKSIZE=$b -o proj05  proj05.cu
                ./proj05
        done
done
