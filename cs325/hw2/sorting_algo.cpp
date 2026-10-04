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
	if(arr.size() < 2){
		return arr;
	}
	//spliting into 3rds
	vector<int> first(arr.begin(), arr.begin() + arr.size()/3), 
		second(arr.begin() + arr.size()/3, arr.begin() + arr.size()*2/3), 
		third(arr.begin() + arr.size()*2/3, arr.end());
	//if it is only 2 out of 3 we will not continue to merge first set however it does not matter since size is 0
	if(arr.size() != 2)
		first = merge3(first);
	second = merge3(second);
	third = merge3(third);
	int i = 0;
	vector<int>::iterator firstitr = first.begin(), 
		seconditr = second.begin(), 
		thirditr = third.begin();
	//selecting the smallest and putting it in the sorted array
	while(firstitr != first.end() && seconditr != second.end() && thirditr != third.end()){
		if(*firstitr <= *seconditr && *firstitr <= *thirditr)
			arr[i++] = *(firstitr++);
		else if(*seconditr <= *firstitr && *seconditr <= *thirditr)
			arr[i++] = *(seconditr++);
		else if(*thirditr <= *seconditr && *thirditr <= *firstitr)
			arr[i++] = *(thirditr++);
	}
	//3 different cases when 1 thirds is emptied
	if(firstitr == first.end()){
		while(thirditr != third.end() && seconditr != second.end()){
			if(*thirditr < *seconditr)
				arr[i++] = *(thirditr++);
			else
				arr[i++] = *(seconditr++);
		}
	} else if(seconditr == second.end()){
		while(firstitr != first.end() && thirditr != third.end()){
			if(*firstitr < *thirditr)
				arr[i++] = *(firstitr++);
			else
				arr[i++] = *(thirditr++);
		}
	}
	else{
		while(firstitr != first.end() && seconditr != second.end()){
			if(*firstitr < *seconditr)
				arr[i++] = *(firstitr++);
			else
				arr[i++] = *(seconditr++);
		}
	}
	//empties the remaining into the sroted array
	while(firstitr != first.end())
		arr[i++] = *(firstitr++);
	while(seconditr != second.end())
		arr[i++] = *(seconditr++);
	while(thirditr != third.end())
		arr[i++] = *(thirditr++);
	//reutrning the sorted array
	return arr;
}