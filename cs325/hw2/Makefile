CC=g++ --std=c++11 -g

all: mergesort3 mergesort3Time

mergesort3: mergesort3.cpp sorting_algo.h sorting_algo.o
	$(CC) mergesort3.cpp sorting_algo.o -o mergesort3 && ./mergesort3

mergesort3Time: mergesort3Time.cpp sorting_algo.h sorting_algo.o
	$(CC) mergesort3Time.cpp sorting_algo.o -o mergesort3Time && ./mergesort3Time

sorting_algo.o: sorting_algo.cpp sorting_algo.h
	$(CC) -c sorting_algo.cpp

clean:
	rm -f *.o mergesort3 mergesort3Time