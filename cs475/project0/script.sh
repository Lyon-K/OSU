#!/bin/bash

#number of threads:
for t in 1 2 3 4
do
    echo NUMT: $t
    g++ -DNUMT=$t prog.cpp -o prog -lm -fopenmp
    ./prog
done