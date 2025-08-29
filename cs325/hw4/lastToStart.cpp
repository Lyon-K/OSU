#include <iostream>
#include <fstream>
#include <cassert>
#include <vector>
#include <string.h>

using namespace std;

struct activity{
	int n;
	int start;
	int finish;
};

//refer to HW1 for additional details, a function pointer is added for start time evaluation
vector<activity> mergesort(vector<activity> arr, bool (*comp)(activity a, activity b)){
	int m = arr.size() / 2, i = 0;
	if(arr.size() < 2)
		return arr;
	vector<activity> left(arr.begin(), arr.begin() + m);
	left = mergesort(left, comp);
	vector<activity> right(arr.begin() + m, arr.end());
	right = mergesort(right, comp);
	
	vector<activity>::iterator leftitr = left.begin(), rightitr = right.begin();
	while(leftitr != left.end() && rightitr != right.end()){
		if(comp(*leftitr, *rightitr))
			arr[i++] = *(leftitr++);
		else
			arr[i++] = *(rightitr++);
	}
	while(leftitr != left.end())
		arr[i++] = *(leftitr++);
	while(rightitr != right.end())
		arr[i++] = *(rightitr++);
	return arr;
}

//a<b return true for star time
bool comp(activity a, activity b){
	return a.start > b.start;
}


int main(){
	int n;
	ifstream fin("act.txt");					//read from file
	assert(fin.is_open());						//ensure there is nothing wrong with opening the file
	vector<vector<struct activity> > j;			//to hold all 3 test cases of vector<struct activity>
	while(fin >> n){
		j.push_back(vector<struct activity>());
		for(int i = 0; i < n; ++i){
			struct activity temp;				//each activity of a schedule
			fin >> temp.n;
			fin >> temp.start;
			fin >> temp.finish;
			j.back().push_back(temp);			//add to the latest test case
		}
	}

	//start solving
	for(int t = 0; t < j.size(); ++t){			//loop every test case
		j[t] = mergesort(j[t], &comp);			//sort according to comp, a.start > b.start
		int count = 1, prev = j[t][0].start;	//always take last to start, so count begins at 1
		for(int i = 1; i < j[t].size(); ++i){	//go through all ordered jobs
			if(j[t][i].finish <= prev){			//if this is true, we choose them in our optimal solution
				j[t][count++] = j[t][i];		//reusing the array because we don't need it anymore
				prev = j[t][i].start;			//updates the previous starting time to match with condition
			}
		}
		//print # of activities then acitivities in reverse
		cout << "Set " << t+1 << endl;
		cout << "Number of activities selected = " << count
			<< "\nActivities: ";
		for(int i = count-1; i >= 0; --i)
			cout << j[t][i].n << " ";
		cout << "\n\n";
	}
	return 0;
}