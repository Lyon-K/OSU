CC=g++ -std=c++11
FILE=tsp_solver

all: 1 2 3 4 5

1: hw7.cpp tsp_example_1.txt
	$(CC) hw7.cpp -o $(FILE) && $(FILE) tsp_example_1.txt && python tsp-verifier.py tsp_example_1.txt tsp_example_1.txt.tour

2: hw7.cpp tsp_example_2.txt
	$(CC) hw7.cpp -o $(FILE) && $(FILE) tsp_example_2.txt && python tsp-verifier.py tsp_example_2.txt tsp_example_2.txt.tour

3: hw7.cpp tsp_example_3.txt
	$(CC) hw7.cpp -o $(FILE) && $(FILE) tsp_example_3.txt && python tsp-verifier.py tsp_example_3.txt tsp_example_3.txt.tour

4: hw7.cpp tsp_example_4.txt
	$(CC) hw7.cpp -o $(FILE) && $(FILE) tsp_example_4.txt && python tsp-verifier.py tsp_example_4.txt tsp_example_4.txt.tour

5: hw7.cpp tsp_example_5.txt
	$(CC) hw7.cpp -o $(FILE) && $(FILE) tsp_example_5.txt && python tsp-verifier.py tsp_example_5.txt tsp_example_5.txt.tour

clean:
	rm -f $(FILE) tsp_example_1.txt.tour tsp_example_2.txt.tour tsp_example_3.txt.tour tsp_example_4.txt.tour tsp_example_5.txt.tour