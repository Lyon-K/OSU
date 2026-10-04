#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <ctime>
#include <sys/time.h>
#include <sys/resource.h>
#include <omp.h>

// SSE stands for Streaming SIMD Extensions

#define SSE_WIDTH	4
#define ALIGNED		__attribute__((aligned(16)))


#define NUMTRIES	200

#ifndef DATASET_SIZE
#define DATASET_SIZE	1024*1024
#endif

#ifndef THREADS_PER_BLOCK
#define THREADS_PER_BLOCK 128
#endif

ALIGNED float A[DATASET_SIZE];
ALIGNED float B[DATASET_SIZE];
ALIGNED float C[DATASET_SIZE];


void	SimdMul(    float *, float *,  float *, int );
__global__ void	NonSimdMul( float *, float *,  float *, int );
float	SimdMulSum(    float *, float *, int );
__global__ void	NonSimdMulSum( float *, float *, float *, int );

void    CudaCheckError( );

int
main( int argc, char *argv[ ] )
{
	for( int i = 0; i < DATASET_SIZE; i++ )
	{
		A[i] = sqrtf( (float)(i+1) );
		B[i] = sqrtf( (float)(i+1) );
	}
    float *dA, *dB, *dC;
    cudaMalloc( (void **)(&dA), sizeof(A) );
    cudaMalloc( (void **)(&dB), sizeof(B) );
    cudaMalloc( (void **)(&dC), sizeof(C) );
    CudaCheckError( );

    // copy host memory to the device:
    cudaMemcpy( dA, A, DATASET_SIZE*sizeof(float), cudaMemcpyHostToDevice );
    cudaMemcpy( dB, B, DATASET_SIZE*sizeof(float), cudaMemcpyHostToDevice );
    CudaCheckError( );

    // setup the execution parameters:
    dim3 grid( DATASET_SIZE / THREADS_PER_BLOCK, 1, 1 );
    dim3 threads( THREADS_PER_BLOCK, 1, 1 );

	fprintf( stderr, "%12d\t", DATASET_SIZE );

	double maxPerformance = 0.;
	for( int t = 0; t < NUMTRIES; t++ )
	{
		double time0 = omp_get_wtime( );
        // create and start the timer:
        cudaDeviceSynchronize( );
        // allocate the events that we'll use for timing:
        cudaEvent_t start, stop;
        cudaEventCreate( &start );
        cudaEventCreate( &stop );
        CudaCheckError( );
        // record the start event:
        cudaEventRecord( start, NULL );
        CudaCheckError( );

		NonSimdMul<<<grid, threads>>>( dA, dB, dC, DATASET_SIZE );


		double time1 = omp_get_wtime( );
		double perf = (double)DATASET_SIZE / (time1 - time0);
		if( perf > maxPerformance )
			maxPerformance = perf;
	}
	double megaMults = maxPerformance / 1000000.;
	fprintf( stderr, "N %10.2lf\t", megaMults );
	double mmn = megaMults;


	maxPerformance = 0.;
	for( int t = 0; t < NUMTRIES; t++ )
	{
		double time0 = omp_get_wtime( );
		SimdMul( A, B, C, DATASET_SIZE );
		double time1 = omp_get_wtime( );
		double perf = (double)DATASET_SIZE / (time1 - time0);
		if( perf > maxPerformance )
			maxPerformance = perf;
	}
	megaMults = maxPerformance / 1000000.;
	fprintf( stderr, "S %10.2lf\t", megaMults );
	double mms = megaMults;
	double speedup = mms/mmn;
	fprintf( stderr, "(%6.2lf)\t", speedup );


	maxPerformance = 0.;
	float sumn, sums;
	for( int t = 0; t < NUMTRIES; t++ )
	{
		double time0 = omp_get_wtime( );
        // create and start the timer:
        cudaDeviceSynchronize( );
        // allocate the events that we'll use for timing:
        cudaEvent_t start, stop;
        cudaEventCreate( &start );
        cudaEventCreate( &stop );
        CudaCheckError( );
        // record the start event:
        cudaEventRecord( start, NULL );
        CudaCheckError( );

		NonSimdMulSum<<<grid, threads>>>( dA, dB, dC, DATASET_SIZE );

        cudaMemcpy( dA, A, DATASET_SIZE*sizeof(float), cudaMemcpyDeviceToHost);
        CudaCheckError();
		double time1 = omp_get_wtime( );
		double perf = (double)DATASET_SIZE / (time1 - time0);
		if( perf > maxPerformance )
			maxPerformance = perf;
	}
	double megaMultAdds = maxPerformance / 1000000.;
	fprintf( stderr, "N %10.2lf\t", megaMultAdds );
	mmn = megaMultAdds;


	maxPerformance = 0.;
	for( int t = 0; t < NUMTRIES; t++ )
	{
		double time0 = omp_get_wtime( );
		sums = SimdMulSum( A, B, DATASET_SIZE );
		double time1 = omp_get_wtime( );
		double perf = (double)DATASET_SIZE / (time1 - time0);
		if( perf > maxPerformance )
			maxPerformance = perf;
	}
	megaMultAdds = maxPerformance / 1000000.;
	fprintf( stderr, "S %10.2lf\t", megaMultAdds );
	mms = megaMultAdds;
	speedup = mms/mmn;
	fprintf( stderr, "(%6.2lf)\n", speedup );
	//fprintf( stderr, "[ %8.1f , %8.1f , %8.1f ]\n", C[DATASET_SIZE-1], sumn, sums );

	return 0;
}


__global__
void
NonSimdMul( float *dA, float *dB, float *dC, int n )
{
    int gid = blockIdx.x*blockDim.x + threadIdx.x;
    if( gid < n )
        dC[gid] = dA[gid] * dB[gid];
}

__global__
void
NonSimdMulSum( float *dA, float *dB, float *dC, int n )
{
    int gid = blockIdx.x*blockDim.x + threadIdx.x;
    if( gid < n )
        dC[gid] = dA[gid] * dB[gid];

    float sum = 0;
    for( int i = 0; i < n; ++i ) sum += dC[i];
    return;
}


__host__
void
SimdMul( float *a, float *b,   float *c,   int len )
{
	int limit = ( len/SSE_WIDTH ) * SSE_WIDTH;
	__asm
	(
		".att_syntax\n\t"
		"movq    -24(%rbp), %r8\n\t"		// a
		"movq    -32(%rbp), %rcx\n\t"		// b
		"movq    -40(%rbp), %rdx\n\t"		// c
	);

	for( int i = 0; i < limit; i += SSE_WIDTH )
	{
		__asm
		(
			".att_syntax\n\t"
			"movups	(%r8), %xmm0\n\t"	// load the first sse register
			"movups	(%rcx), %xmm1\n\t"	// load the second sse register
			"mulps	%xmm1, %xmm0\n\t"	// do the multiply
			"movups	%xmm0, (%rdx)\n\t"	// store the result
			"addq $16, %r8\n\t"
			"addq $16, %rcx\n\t"
			"addq $16, %rdx\n\t"
		);
	}

	for( int i = limit; i < len; i++ )
	{
		c[i] = a[i] * b[i];
	}
}



__host__
float
SimdMulSum( float *a, float *b, int len )
{
	float sum[4] = { 0., 0., 0., 0. };
	int limit = ( len/SSE_WIDTH ) * SSE_WIDTH;

	__asm
	(
		".att_syntax\n\t"
		"movq    -40(%rbp), %r8\n\t"		// a
		"movq    -48(%rbp), %rcx\n\t"		// b
		"leaq    -32(%rbp), %rdx\n\t"		// &sum[0]
		"movups	 (%rdx), %xmm2\n\t"		// 4 copies of 0. in xmm2
	);

	for( int i = 0; i < limit; i += SSE_WIDTH )
	{
		__asm
		(
			".att_syntax\n\t"
			"movups	(%r8), %xmm0\n\t"	// load the first sse register
			"movups	(%rcx), %xmm1\n\t"	// load the second sse register
			"mulps	%xmm1, %xmm0\n\t"	// do the multiply
			"addps	%xmm0, %xmm2\n\t"	// do the add
			"addq $16, %r8\n\t"
			"addq $16, %rcx\n\t"
		);
	}

	__asm
	(
		".att_syntax\n\t"
		"movups	 %xmm2, (%rdx)\n\t"	// copy the sums back to sum[ ]
	);

	for( int i = limit; i < len; i++ )
	{
		sum[0] += a[i] * b[i];
	}

	return sum[0] + sum[1] + sum[2] + sum[3];
}

void
CudaCheckError( ) {
    return;
    cudaError_t e = cudaGetLastError( );
    if( e != cudaSuccess ) {
        fprintf( stderr, "CUDA failure %s:%d: '%s'\n", __FILE__,
                __LINE__, cudaGetErrorString(e));
    }
}

