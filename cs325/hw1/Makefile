CC=g++ --std=c++11 -g -O3

all: test_insertsort test_mergesort insertTime mergeTime

test_insertsort: test_insertsort.cpp sorting_algo.h sorting_algo.o
	$(CC) test_insertsort.cpp sorting_algo.o -o test_insertsort && ./test_insertsort

test_mergesort: test_mergesort.cpp sorting_algo.h sorting_algo.o
	$(CC) test_mergesort.cpp sorting_algo.o -o test_mergesort && ./test_mergesort

insertTime: insertTime.cpp sorting_algo.h sorting_algo.o
	$(CC) insertTime.cpp sorting_algo.o -o insertTime && ./insertTime

mergeTime: mergeTime.cpp sorting_algo.h sorting_algo.o
	$(CC) mergeTime.cpp sorting_algo.o -o mergeTime && ./mergeTime

sorting_algo.o: sorting_algo.cpp sorting_algo.h
	$(CC) -c sorting_algo.cpp

clean:
	rm -f *.o test_insertsort test_mergesort insertTime mergeTime