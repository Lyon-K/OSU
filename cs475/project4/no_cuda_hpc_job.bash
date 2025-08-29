#!/bin/bash
#SBATCH -J proj4
#SBATCH -A cs475-575
#SBATCH -p classgpufinal
#SBATCH --constraint=v100
#SBATCH --gres=gpu:1
#SBATCH -o output.out
#SBATCH -e output.err
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=keel@oregonstate.edu

ml slurm
ml cuda/11.6

echo "ARRAY_SIZE    N   NonSimdMul  S      SimdMul  ( SpeedUp)      N   NonSimdSum  S      SimdSum  ( SpeedUp)"



for t in 2 4 8 16
do
    echo "t:$t"
    for n in 1024*16 1024*32 1024*64 1024*128 1024*256 1024*512 1048576 2097152 4194304 8388608 16777216 33554432 67108864 134217728
    do
        gcc -o all04 all04.cpp -lm -fopenmp -DARRAYSIZE=$n -DNUMT=$t
        ./all04
    done
done

