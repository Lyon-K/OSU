#include <stdio.h>
#include <stdlib.h>
#include "omp.h"

using namespace std;

int main () {
    fprintf( stderr, "%d\n", omp_get_num_procs());
    return 0;
}
