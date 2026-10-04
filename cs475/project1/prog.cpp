#include <stdio.h>
#include <omp.h>
#include <math.h>
#include <time.h>

#ifndef NUMTRIALS   // Number of trial runs
#define NUMTRIALS 100000
#endif

#ifndef NUMT        // Nunber of threads
#define NUMT 1
#endif

#define BEFOREY     80.f
#define BEFOREY_DY  5.f
#define AFTERY      20.f
#define AFTERY_DY   1.f
#define DISTX       70.f
#define DISTX_DX    5.f
#define G           9.8f
#define RADIUS      3.f

float BeforeY[NUMTRIALS];
float AfterY[NUMTRIALS];
float DistX[NUMTRIALS];
float Results[NUMTRIALS];

float calc_vx(float beforey, float aftery) {
    return sqrt(2. * G * (beforey - aftery));
}

float calc_t(float aftery) {
    return sqrt((2. * aftery) / G);
}

float calc_dx(float vx, float t) {
    return vx * t;
}

float gen_rand_val(float val, float div) {
    return val + div * (((float) rand() / (RAND_MAX / 2)) - 1);
}

int main() {
    #ifndef _OPENMP
        #ifndef CSV
            fprintf(stderr, "OpenMP is supported -- version = %d\n", _OPENMP );
        #endif
    #else
        fprintf(stderr, "OpenMP is not supported here - sorry!\n");
        exit(0);
    #endif
    
    omp_set_num_threads( NUMT );
    
    srand(time(NULL))
    // #pragma omp parallel for
    for (int i = 0; i < NUMTRIALS; ++i) {
        BeforeY = gen_rand_val(BEFOREY, BEFOREY_DY);
        AfterY = gen_rand_val(AFTERY, AFTERY_DY);
        DistX = gen_rand_val(DISTX, DISTX_DX);
    }

    #pragma omp parallel for
    for(int i = 0; i < NUMTRIALS; ++i) {
        dx = calc_dx(
            calc_vx(BeforeY, AfterY), 
            calc_t(AfterY))
    }

    return 0;
}

