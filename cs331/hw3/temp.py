def print_board(arr):
    print(f'''
     _ _ _
    |{arr[0]}|{arr[1]}|{arr[2]}|
    |{arr[3]}|{arr[4]}|{arr[5]}|
    |{arr[6]}|{arr[7]}|{arr[8]}|
     - - - 
    ''')

arr = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

print("depth 0")
print_board(arr)

print("depth 1")
for i in range(9):
    new_arr = arr.copy()
    new_arr[i] = 'X'
    print_board(new_arr)

print("depth 2")
for i in range(9):

    d1_arr = arr.copy()
    
    d1_arr[i] = 'X'
    for j in range(9):
        if i != j:
            d2_arr = d1_arr.copy()
            d2_arr[j] = 'O'
            print_board(d2_arr)
