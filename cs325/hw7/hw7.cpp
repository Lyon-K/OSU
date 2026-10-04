#include <iostream>
#include <fstream>
#include <vector>
#include <cassert>
#include <cmath>
#include <cstring>
#include <limits.h>
#include <chrono>

using namespace std;

int distance(float x1,float x2,float y1,float y2){
	return sqrt(pow((x1-x2), 2) + pow((y1-y2), 2)) + 0.5;
}

//used for inputs
struct point{
	int n;
	int x;
	int y;
};

//used for adjacency matrix
struct qNode{
	int distance;
	int n;
	int parent;
};

//used for MST
struct node{
	int val;
	vector<node> children;
};

//adds a node to the MST with the corresponding parent node
void addNode(struct node *head, struct node *item, int parent){	//O(V)
	if(head->val == parent){				//found the parent
		head->children.push_back(*item);	//add the next node
		return;
	}
	for(int i = 0; i < head->children.size(); ++i)	//continue looking for parent
		addNode(&head->children[i], item, parent);
}

//simple in order traversal of the tree
void inorderTraversal(struct node *head, vector<int> *path){
	path->push_back(head->val);
	for(int i = 0; i < head->children.size(); ++i){
		inorderTraversal(&head->children[i], path);
	}
}


int main(int argc, char* argv[]){
	//checks for command line argument
	assert(argc == 2);
	char *file = argv[1];
	cout << fixed;

	cout << "Time:\n";
	double totalTime = 0, timeLapsed;
	chrono::time_point<chrono::system_clock> start;
	start = chrono::high_resolution_clock::now();
	//read coordinatesfrom file
	ifstream fin(file);
	assert(fin.is_open());
	int n, temp;
	fin >> n;
	vector<point> data;
	for(int i = 0; i < n; ++i){
		struct point temp;
		fin >> temp.n >> temp.x >> temp.y;
		data.push_back(temp);
	}
	fin.close();
	//time tracking
	timeLapsed =((chrono::duration<double,milli>) (chrono::high_resolution_clock::now() - start)).count();
	cout << "input(ms) = " << timeLapsed << endl;
	totalTime += timeLapsed;

	start = chrono::high_resolution_clock::now();
	//coordinates -> weighted matrix
	vector< vector<int>> graph(n, vector<int>(n,0));
	for(int i = 0; i < n; ++i)			//Theta(V)
		for(int j = 0; j < n; ++j)		//Theta(V)
			//forming edges to vertices
			graph[i][j] = distance(data[i].x, data[j].x, data[i].y, data[j].y);
	//time tracking
	timeLapsed =((chrono::duration<double,milli>) (chrono::high_resolution_clock::now() - start)).count();
	cout << "matrix(ms) = " << timeLapsed << endl;
	totalTime += timeLapsed;

	start = chrono::high_resolution_clock::now();
	//prims algo
	int weight = 0;
	vector<qNode> q;
	qNode qtemp={};
	//initializing
	for(int i = 1; i < n; ++i){	//Theta(V)
		qtemp.n = i;
		qtemp.distance = graph[0][i];
		q.push_back(qtemp);
	}

	struct node *MST = new struct node;
	MST->val = 0;
	while(q.size()){	//Theta(V)
		vector<qNode>::iterator min = q.begin();
		//O(V)
		for(vector<qNode>::iterator itr = q.begin()+1; itr != q.end(); ++itr){
			if(itr->distance < min->distance)
				min = itr;
		}
		if(min->n){
			struct node *temp = new struct node;
			temp->val = min->n;
			addNode(MST, temp, min->parent);
		}
		weight += min->distance;
		//performs relaxation
		for(int i = 0; i < q.size(); ++i){	//O(V)
			int temp = graph[q[i].n][min->n];
			if(temp < q[i].distance){
				q[i].parent = min->n;
				q[i].distance = temp;
			}
		}
		//remove visited vertex
		q.erase(min);
	}
	//time tracking
	timeLapsed =((chrono::duration<double,milli>) (chrono::high_resolution_clock::now() - start)).count();
	cout << "Prim's(ms) = " << timeLapsed << endl;
	totalTime += timeLapsed;

	start = chrono::high_resolution_clock::now();
	//TSP path finder by in order traversal of MST
	vector<int> path;
	inorderTraversal(MST, &path);	//Theta(V)
	path.push_back(0);	//initialization
	long long tspANS = 0;
	//calculate path length
	vector<int>::iterator prev = path.begin();
	for(vector<int>::iterator itr = path.begin()+1; itr != path.end(); ++itr)
		tspANS += graph[*prev++][*itr];	//Theta(V)
	//time tracking
	timeLapsed =((chrono::duration<double,milli>) (chrono::high_resolution_clock::now() - start)).count();
	cout << "TSP(ms) = " << timeLapsed << endl;
	totalTime += timeLapsed;
	cout << "total time(ms) = " << totalTime << endl;

	//write solution to file
	strcat (file, ".tour");
	ofstream fout(file);
	assert(fout.is_open());
	fout << tspANS << endl;
	for(vector<int>::iterator itr = path.begin(); itr != path.end()-1; ++itr){
		fout << *itr << endl;
	}
	fout.close();

	return 0;
}