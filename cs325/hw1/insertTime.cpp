#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include "sorting_algo.h"
#define N_START 5000
#define N_STEP 5000
#define RUNS 10

using namespace std;

int main(){
	long long n = N_START;
	vector<vector<int>> data;
	srand(time(NULL));
	for(long long j = 0; j < 10; ++j){
		data.push_back(vector<int>());
		for(long long i = 0; i < n; ++i){
			data.back().push_back(rand()%10001);
		}
		n += N_STEP;
	}

	//iterating through each test case
	n = N_START;
	for(vector<vector<int>>::iterator t = data.begin(); t != data.end(); ++t){
		double avgTime = 0;
		for(long long i = 0; i < RUNS; ++i){
			clock_t startTime = clock();
			vector<int> arr = insertsort(*t);
			avgTime += double(clock() - startTime) / CLOCKS_PER_SEC / RUNS;
		}
		cout << n << "\t" << avgTime << endl;
		n+= N_STEP;
	}
	return 0;
}
