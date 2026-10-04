#include <iostream>
#include <vector>
#include <fstream>
#include <cassert>
#include "sorting_algo.h"

using namespace std;

int main(){
	int n, temp;
	vector<vector<int>> data;
	ifstream fin("data.txt");
	assert(fin.is_open());
	while(fin >> n){
		data.push_back(vector<int>());
		data.back().emplace_back(n);
		for(int i = 0; i < n; ++i){
			fin >> temp;
			data.back().emplace_back(temp);
		}
	}
	fin.close();


	//dispalying the data set
	/*
	cout << "data set:" << endl;
	for(vector<vector<int>>::iterator i = data.begin(); i != data.end(); ++i){
		for(vector<int>::iterator j = i->begin(); j != i->end(); ++j){
			cout << *j << " ";
		}
		cout << endl;
	}
	*/

	//iterating through each test case
	for(vector<vector<int>>::iterator t = data.begin(); t != data.end(); ++t){
		vector<int> arr;
		arr = mergesort(*t);

		//display sorted array
		cout << "merge Sort: ";
		for(vector<int>::iterator it = arr.begin(); it != arr.end(); ++it)
			cout << *it << " ";
		cout << endl;
	}

	return 0;
}
