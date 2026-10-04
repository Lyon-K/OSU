#include <stdio.h>
#include <omp.h>
#include <algorithm>

#ifndef ARR_SIZE    //Array size
#define ARR_SIZE (1 << 25)
#endif

#ifndef NUMT    //Num threads
#define NUMT 1
#endif

#define NUMTRIES 20  // how many times to run the timing to get reliable timing data

// Global arrays for parallelization
float A[ARR_SIZE];
float B[ARR_SIZE];
float C[ARR_SIZE];

int main() {
    #ifdef _OPENMP // Ensuring OpenMP is available
        fprintf(stderr, "OpenMP version %d is supported here\n", _OPENMP);
    #else
        fprintf(stderr, "OpenMP is not supported here - sorry!\n");
        exit(0);
    #endif

    omp_set_num_threads( NUMT ); // Set num threads

    double maxMegaMults = 0.;

    for (int t = 0; t < NUMTRIES; ++t) {
        double start = omp_get_wtime();

        #pragma omp parallel for    // parallelizing the folowing for block 
        for (int i  = 0; i < ARR_SIZE; ++i) C[i] = A[i] * B[i];
        
        maxMegaMults = std::max(maxMegaMults, ARR_SIZE / (omp_get_wtime() - start) / 1000000); // Save max across runs
    }

    fprintf(stderr, "Threads = %d, Peak Performance = %8.2lf MegaMults/Sec\n", NUMT, maxMegaMults);

    return 0;
}