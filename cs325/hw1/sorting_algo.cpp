#include "sorting_algo.h"



vector<int> insertsort(vector<int> arr){
	int temp;
	for(vector<int>::iterator current = arr.begin() + 1; current != arr.end(); ++current){
		temp = *current;
		vector<int>::iterator i;	//need move declaration to the top?
		for(i = current - 1; i != arr.begin() - 1 && *i > temp; --i)
			*(i + 1) = *i;	//swap to the right
		*(i + 1) = temp;	//insert at the correct position
	}
	return arr;
}

vector<int> mergesort(vector<int> arr){
	int m = arr.size() / 2, i = 0;
	if(arr.size() < 2)
		return arr;
	vector<int> left(arr.begin(), arr.begin() + m);
	left = mergesort(left);
	vector<int> right(arr.begin() + m, arr.end());
	right = mergesort(right);
	
	vector<int>::iterator leftitr = left.begin(), rightitr = right.begin();
	while(leftitr != left.end() && rightitr != right.end()){
		if(*leftitr < *rightitr)
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

vector<int> merge3(vector<int> arr){
	if(arr.size() < 2)
		return arr;
	vector<int> first(arr.begin(), arr.begin() + arr.size()/3), 
		second(arr.begin() + arr.size()/3, arr.begin() + arr.size()*2/3), 
		third(arr.begin() + arr.size()*2/3, arr.end());
	second = merge3(second);
	third = merge3(third);
	int i = 0;
	vector<int>::iterator firstitr = first.begin(), 
		seconditr = second.begin(), 
		thirditr = third.begin();
	if(arr.size() != 2)
		first = merge3(first);
	while(firstitr != first.end() && seconditr != second.end() && thirditr != third.end()){
		if(*firstitr < *seconditr && *firstitr < *thirditr)
			arr[i++] = *(firstitr++);
		else if(*seconditr < *firstitr && *seconditr < *thirditr)
			arr[i++] = *(seconditr++);
		else if(*thirditr < *seconditr && *thirditr < *firstitr)
			arr[i++] = *(thirditr++);
	}
	if(firstitr == first.end()){
		firstitr = thirditr;
	} else if(seconditr == second.end()){
		seconditr = thirditr;
	}
	while(firstitr != first.end() && seconditr != second.end()){
		if(*firstitr < *seconditr)
			arr[i++] = *(firstitr++);
		else
			arr[i++] = *(seconditr++);
	}
	while(firstitr != first.end())
		arr[i++] = *(firstitr++);
	while(seconditr != second.end())
		arr[i++] = *(seconditr++);
	return arr;
}
