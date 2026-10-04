#include <stdio.h>
#define _USE_MATH_DEFINES
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

#ifndef NUMT
#define NUMT 4
#endif

omp_lock_t	Lock;
volatile int	NumInThreadTeam;
volatile int	NumAtBarrier;
volatile int	NumGone;

unsigned int seed = 0;

int	    NowYear;		// 2024- 2029
int	    NowMonth;		// 0 - 11

float	NowPrecip;		// inches of rain per month
float	NowTemp;		// temperature this month
float	NowHeight;		// grain height in inches
int	    NowNumDeer;		// number of deer in the current population
int     NowNumZombie;      // number of zombie in the current population


const float GRAIN_GROWS_PER_MONTH =     12.0;
const float ONE_DEER_EATS_PER_MONTH =	1.0;
const float ZOMBIE_CHANCE_TO_INFECT =   0.05;

const float AVG_PRECIP_PER_MONTH =		7.0;	// average
const float AMP_PRECIP_PER_MONTH =		6.0;	// plus or minus
const float RANDOM_PRECIP =			    2.0;	// plus or minus noise

const float AVG_TEMP =				    60.0;	// average
const float AMP_TEMP =				    20.0;	// plus or minus
const float RANDOM_TEMP =			    10.0;	// plus or minus noise

const float MIDTEMP =				    40.0;
const float MIDPRECIP =				    10.0;

float
SQR( float x )
{
    return x*x;
}

void
TimeOfDaySeed( )
{
	struct tm y2k = { 0 };
	y2k.tm_hour = 0;   y2k.tm_min = 0; y2k.tm_sec = 0;
	y2k.tm_year = 100; y2k.tm_mon = 0; y2k.tm_mday = 1;

	time_t  timer;
	time( &timer );
	double seconds = difftime( timer, mktime(&y2k) );
	unsigned int seed = (unsigned int)( 1000.*seconds );    // milliseconds
	srand( seed );
}

// specify how many threads will be in the barrier:
//	(also init's the Lock)
void
InitBarrier( int n )
{
    NumInThreadTeam = n;
    NumAtBarrier = 0;
	omp_init_lock( &Lock );
}


// have the calling thread wait here until all the other threads catch up:

void
WaitBarrier( )
{
    omp_set_lock( &Lock );
    {
        NumAtBarrier++;
        if( NumAtBarrier == NumInThreadTeam )
        {
            NumGone = 0;
            NumAtBarrier = 0;
            // let all other threads get back to what they were doing
            // before this one unlocks, knowing that they might immediately
            // call WaitBarrier( ) again:
            while( NumGone != NumInThreadTeam-1 );
            omp_unset_lock( &Lock );
            return;
        }
    }
    omp_unset_lock( &Lock );

    while( NumAtBarrier != 0 );	// this waits for the nth thread to arrive

    #pragma omp atomic
    NumGone++;			// this flags how many threads have returned
}


float
Ranf( float low, float high )
{
        float r = (float) rand();               // 0 - RAND_MAX
        float t = r  /  (float) RAND_MAX;       // 0. - 1.

        return   low  +  t * ( high - low );
}

void Deer() {
    int prevZombie = 1;
    while (NowYear < 2030 ){
        int nextNumDeer = NowNumDeer;
        int carryingCapacity = (int)( NowHeight );
        // printf("subtracted %d deers\n", NowNumZombie - prevZombie);
        nextNumDeer -= NowNumZombie - prevZombie;
        prevZombie = NowNumZombie;
        if( nextNumDeer < carryingCapacity )
                nextNumDeer++;
        else
                if( nextNumDeer > carryingCapacity )
                        nextNumDeer--;

        if( nextNumDeer < 0 )
                nextNumDeer = 0;

        
        WaitBarrier( ); // DoneComputing barrier:
        
        NowNumDeer = nextNumDeer;
        WaitBarrier( ); // DoneAssigning barrier:


        WaitBarrier( ); // DonePrinting barrier:
    }
}

void Grain() {
    while (NowYear < 2030 ){
        float tempFactor = exp( -SQR(( NowTemp - MIDTEMP ) / 10. ));
        float precipFactor = exp( -SQR(( NowPrecip - MIDPRECIP ) / 10. ));
        float nextHeight = NowHeight;
        nextHeight += tempFactor * precipFactor * GRAIN_GROWS_PER_MONTH;
        nextHeight -= (float)NowNumDeer * ONE_DEER_EATS_PER_MONTH;
        if( nextHeight < 0. ) nextHeight = 0.;
        WaitBarrier( ); // DoneComputing barrier:
        
        NowHeight = nextHeight;
        WaitBarrier( ); // DoneAssigning barrier:


        WaitBarrier( ); // DonePrinting barrier:
    }
}

float inches_cm (float inches) {
    return inches * 2.54;
}

float F_C (float F) {
    return (5./9.)*(F-32);
}

void Watcher() {
    while (NowYear < 2030 ){
        WaitBarrier( ); // DoneComputing barrier:
        
        WaitBarrier( ); // DoneAssigning barrier:

        printf("%16d, %16d, %16d, %16f, %16f, %16f, %16d, %16d\n", NowYear, NowMonth, (NowYear-2024)*12+NowMonth, inches_cm(NowPrecip), F_C(NowTemp), inches_cm(NowHeight), NowNumDeer, NowNumZombie);

        float ang = (  30.*(float)NowMonth + 15.  ) * ( M_PI / 180. );	// angle of earth around the sun

        float temp = AVG_TEMP - AMP_TEMP * cos( ang );
        NowTemp = temp + Ranf( -RANDOM_TEMP, RANDOM_TEMP );

        float precip = AVG_PRECIP_PER_MONTH + AMP_PRECIP_PER_MONTH * sin( ang );
        NowPrecip = precip + Ranf( -RANDOM_PRECIP, RANDOM_PRECIP );
        if( NowPrecip < 0. ) NowPrecip = 0.;

        if (++NowMonth == 12) { // update time environment
            NowMonth = 0;
            ++NowYear;
        }


        WaitBarrier( ); // DonePrinting barrier:
    }
}

void MyAgent() {
    while (NowYear < 2030 ){
        int NextNumZombie = NowNumZombie;
        int TempDeer = NowNumDeer;
        if (NowNumDeer) {
            for (int i = 0; i < NowNumZombie && TempDeer; ++i) {
                if ((rand() % (int) (1 / ZOMBIE_CHANCE_TO_INFECT)) == 0) {
                    ++NextNumZombie;
                    --TempDeer;
                }
            }
        }
        WaitBarrier( ); // DoneComputing barrier:

        NowNumZombie = NextNumZombie;
        WaitBarrier( ); // DoneAssigning barrier:


        WaitBarrier( ); // DonePrinting barrier:
    }
}


int main( int argc, char *argv[ ] )
{
#ifdef _OPENMP
	#ifndef CSV
		fprintf( stderr, "OpenMP is supported -- version = %d\n", _OPENMP );
	#endif
#else
        fprintf( stderr, "No OpenMP support!\n" );
        return 1;
#endif

    TimeOfDaySeed( );               // seed the random number generator

    // starting date and time:
    NowMonth =    0;
    NowYear  = 2024;

    // starting state (feel free to change this if you want):
    NowNumDeer = 2;
    NowHeight =  5.;
    NowNumZombie = 1;

    printf("%16s, %16s, %16s, %16s, %16s, %16s, %16s, %16s\n", "Year", "Month", "NumMonths", "Precipitation", "Temperature", "Grain Height", "NumDeers", "NowNumZombie");

    omp_set_num_threads( NUMT );

    InitBarrier( NUMT );

    #pragma omp parallel sections
    {
        #pragma omp section 
        {
            Deer();
        }

        #pragma omp section
        {
            Grain();
        }

        #pragma omp section
        {
            Watcher();
        }

        #pragma omp section
        {
            MyAgent();
        }
    }

}