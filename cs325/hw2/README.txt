HW2
name: Lyon Kee
email: keel@oregonstate.edu

Language: c++
Running command: make
(optional) Notes: you might have to make clean and make again if it was already compiled, or simply ./(file) to run that output file. Sometimes, when you run and the computer is busy, an error of "collect2: fatal error: vfork: Resource temporarily unavailable" will occur, by doing ./(file) after making it will allow it to run, I would sometimes get this error and sometimes not, but simply copying the line that is executed and executing it will run.


additional notes:

You can change the data set generation range by changing the starting n, steps, and runs by changing the constants at the begining of the file in line 6-8 given by N_START, N_STEP, AND RUNS respectively.

to run all tests:
make clean && make

to run mergesort3:
make mergesort3

to run mergesort3Time:
make mergesort3Time

to clean directory of unnecessary files:
make clean
