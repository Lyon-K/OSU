import os

# Program name
prog = "prog"

# Number of threads
for t in [1, 4, 16]:
    cmd = f"g++ -DNUMT={t} {prog}.cpp -o {prog} -lm -fopenmp"
    # Compiling source code
    os.system(cmd)
    # Executing
    os.system(f'./{prog}')

pp1 = 1022.72
pp4 = 3980.47
s = pp4/pp1
print(f"Speedup = (Peak performance for 4 threads) / (Peak performance for 1 thread) \n= {1022.72}/{3980.47} = {s}")
print(f"Fp = (4./3.)*( 1. - (1./S) ) \n= {(4./3.)*( 1. - (1./s) )}")