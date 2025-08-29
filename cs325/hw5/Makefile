CC=g++ --std=c++11 -g -fpermissive

all: EuclideanMST

EuclideanMST: EuclideanMST.cpp dynarray.h dynarray.o pq.h pq.o
	$(CC) EuclideanMST.cpp dynarray.o pq.o -o EuclideanMST && ./EuclideanMST

dynarray.o: dynarray.cpp dynarray.h
	$(CC) -c dynarray.cpp

pq.o: pq.cpp pq.h
	$(CC) -c pq.cpp

clean:
	rm -f *.o EuclideanMST