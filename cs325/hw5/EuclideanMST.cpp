#include <iostream>
#include <fstream>
#include <vector>
#include <cassert>
#include <cmath>
#include <limits.h>
#include "pq.h"

using namespace std;


int distance(float x1,float x2,float y1,float y2){
	return sqrt(pow((x1-x2), 2) + pow((y1-y2), 2)) + 0.5;
}

int main(){
	int t;
	ifstream fin("graph.txt");
	assert(fin.is_open());
	fin >> t;
	while(t--){
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
		vector<bool> Visited(n, false);
		struct pq* q = pq_create();	//(key,val) = (weight, n)
		pq_insert(q, 0, 0);			//initializing

		while(!pq_isempty(q)){
			int firstN = pq_first(q);
			visited[firstN] = true;
			for(int i = 0; i < n; ++i){
				if(!visited[i]){
					cout << "inserting(n,distance): " << visited[i] << ", " << graph[i][firstN] << endl;
					relax(q, i, graph[i][firstN]);
				}
			}
			pq_remove_first(q);
			break;
		}
	}
}