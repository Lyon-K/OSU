#include <iostream>
#include <string.h>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <chrono>
#define ll long long
#define N_START 10
#define N_STEP 5
#define N_END 45
#define W 100

using namespace std;

ll DPKnapsack(int w, int n, int val[],  int wt[]){
	ll dp[n+1][w+1];							//space for 0->n rows and 0->w cols
	memset(dp[0], 0, sizeof(dp[0][0]) * (w + 1) * (n+1));	//0 out the array
	for(int i = 1; i < n+1; ++i){
		for(int j = 1; j < w+1; ++j){
			if(j < wt[i-1])				//if item cannot be inserted into knapsack
				dp[i][j] = dp[i-1][j];
			else						//if item can be inserted into knapsack
				dp[i][j] = max(val[i-1] + dp[i-1][j-wt[i-1]], dp[i-1][j]);
		}
	}

	/*
	//CHECKING FOR DP MAP
	cout << "dp:\n";
	for(int i = 0; i < n+1; ++i){
		for(int j = 0; j < w+1; ++j){
			cout << dp[i][j] << " ";
		}
		cout << endl;
	}
	*/
	return dp[n][w];
}

ll RecurKnapsack(int capacity, int n, int val[], int wt[]){	//current = n-1
	if(n == 0 || capacity == 0)
		return 0;	//no value
	if(wt[n-1] > capacity)	//item cannot fit into knapsack
		return RecurKnapsack(capacity, n-1, val, wt);	//go next item
	else					//item can be considered
		return max(val[n-1] + RecurKnapsack(capacity - wt[n-1], n-1, val, wt), RecurKnapsack(capacity, n-1, val, wt));
}

int main(){
	srand(time(NULL));
	int val[40], wt[40];
	for(int i = 0; i < 40; ++i){
		val[i] = rand()%100 + 1;
		wt[i] = rand()%30 + 1;
	}

	for(int i = N_START; i < N_END; i += N_STEP){
		chrono::time_point<chrono::system_clock> start;
		ll RecurAns = 0, DPAns = 0;
		cout << "N = " << left << setw(5) << i << "W = " << setw(5) << W;

		start = chrono::high_resolution_clock::now();
		RecurAns = RecurKnapsack(W, i, val, wt);
		cout << "Rec time(ms) = " << setw(12) << left
			<< ((chrono::duration<double,milli>) (chrono::high_resolution_clock::now() - start)).count();

		start = chrono::high_resolution_clock::now();
		DPAns = DPKnapsack(W, i, val, wt);
		cout << "DP time(ms) = " << setw(12) << left
			<< ((chrono::duration<double,milli>) (chrono::high_resolution_clock::now() - start)).count();

		cout << "max Rec = " << setw(6) << RecurAns 
			<< "max DP = " << setw(6) << DPAns 
			<< endl;
	}

	return 0;
}