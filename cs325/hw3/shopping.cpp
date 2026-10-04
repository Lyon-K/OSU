#include <iostream>
#include <string.h>
#include <fstream>
#include <cassert>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

void DPCompute(int dp[][201], int w, int n, int val[], int wt[]){
	for(int i = 1; i < n+1; ++i){
		for(int j = 1; j < w+1; ++j){
			if(j < wt[i-1])				//if item cannot be inserted into knapsack
				dp[i][j] = dp[i-1][j];
			else						//if item can be inserted into knapsack
				dp[i][j] = max(val[i-1] + dp[i-1][j-wt[i-1]], dp[i-1][j]);
		}
	}
}

void DPBacktrack(int dp[][201], int w, int n, int val[], int wt[]){	//returns items
	vector<int> ans;
	while(n && w){
		if(dp[n][w] == dp[n-1][w])	//if value did not originate from this item
			--n;
		else{
			ans.push_back(n);		//pushback the correct item number
			w -= wt[n---1];
		}
	}
	for(int i = ans.size()-1; i >= 0; --i)	//print it backwards
		cout << ans[i] << " ";
}


int main(){
	int t, i = 1;
	ifstream fin("shopping.txt");
	assert(fin.is_open());
	fin >> t;
	while(t--){
		//get inputs here
		int n, f;
		fin >> n;
		int val[n], wt[n];
		for(int i = 0; i < n; ++i){
			fin >> val[i] >> wt[i];
		}
		fin >> f;
		int m[f];
		for(int i = 0; i < f; ++i){
			fin >> m[i];
		}

		//start solving here
		cout << "Test Case " << i++ << endl;
		int maxW = *max_element(m, m+f);
		int dp[101][201];
		int total = 0;
		memset(dp, 0, sizeof(dp[0][0]) * n+1 * maxW+1);
		DPCompute(dp, maxW, n, val, wt);
		for(int i = 0; i < f; ++i){
			total += dp[n][m[i]];
		}
		cout << "Total Price " << total << endl;
		cout << "Member Items:\n";
		for(int i = 0; i < f; ++i){
			cout << i+1 << ": ";
			DPBacktrack(dp, m[i], n, val, wt);
			cout << endl;
		}
	}
	fin.close();

	return 0;
}