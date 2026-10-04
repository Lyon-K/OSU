#include <iostream>
#include <fstream>
#include <vector>
#include <cassert>
#include <cmath>
#include <limits.h>

using namespace std;


int distance(float x1,float x2,float y1,float y2){
	return sqrt(pow((x1-x2), 2) + pow((y1-y2), 2)) + 0.5;
}

int main(){
	int t, x = 0;
	ifstream fin("graph.txt");
	assert(fin.is_open());
	fin >> t;
	while(t--){
		cout << "Test case " << ++x << ": ";
		int n;
		fin >> n;
		vector< pair<int, int>> data;
		for(int i = 0; i < n; ++i){
			int x,y;
			fin >> x >> y;
			data.emplace_back(x,y);
		}

		//coordinates -> weighted matrix
		int graph[n][n];
		for(int i = 0; i < n; ++i)			//Theta(v)
			for(int j = 0; j < n; ++j)		//Theta(v)
				//forming edges to vertices
				graph[i][j] = distance(data[i].first, data[j].first, data[i].second, data[j].second);
		
		//prims
		int weight = 0;
		vector< pair<int, int>> q;	//(key,val) = (weight, n)
		q.emplace_back(0,0);
		for(int i = 1; i < n; ++i){	//initializing
			q.emplace_back(INT_MAX, i);
		}

		while(q.size()){
			pair<int, int> min = q[0];
			for(int i = 1; i < q.size(); ++i){	//looks for min vertex
				if(q[i].first < min.first)
					min = q[i];
			}
			weight += min.first;
			for(int i = 0; i < q.size(); ++i){	//performs relaxation
				int temp = graph[q[i].second][min.second];
				if(temp < q[i].first){
					q[i].first = temp;
				}
			}
			//remove visited vertex
			for(auto itr = q.begin(); itr != q.end(); ++itr){
				if(itr->second == min.second){
					q.erase(itr);
					break;
				}
			}
		}
		cout << "MST weight " << weight << endl;
	}
}