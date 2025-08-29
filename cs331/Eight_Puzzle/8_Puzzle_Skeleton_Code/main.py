from board import Board
import numpy as np
import time
import matplotlib.pyplot as plt

'''
Heuristics
'''
def BF(_: Board) -> int:
    return 0

def MT(board: Board) -> int:
    return int(board.state[0][0] != 1) + int(board.state[0][1] != 2) + int(board.state[0][2] != 3) \
        + int(board.state[1][0] != 4) + int(board.state[1][1] != 5) + int(board.state[1][2] != 6) \
        + int(board.state[2][0] != 7) + int(board.state[2][1] != 8) + int(board.state[2][2] != 0)

def CB(board: Board) -> int:
    coords = {1: (0,0), 2: (0,1), 3: (0,2), 4: (1,0), 5: (1,1), 6: (1,2), 7: (2,0), 8: (2,1), 0: (0,0)}
    return city_block_calculator(coords[1], coords[board.state[0][0]]) + city_block_calculator(coords[2], coords[board.state[0][1]]) + city_block_calculator(coords[3], coords[board.state[0][2]]) \
        + city_block_calculator(coords[4], coords[board.state[1][0]]) + city_block_calculator(coords[5], coords[board.state[1][1]]) + city_block_calculator(coords[6], coords[board.state[1][2]]) \
        + city_block_calculator(coords[7], coords[board.state[2][0]]) + city_block_calculator(coords[8], coords[board.state[2][1]]) + city_block_calculator(coords[0], coords[board.state[2][2]])

def NA(board: Board) -> int:
    return int(board.state[0][0] != 1 or board.state[0][1] != 2 or board.state[0][2] != 3) \
        + int(board.state[1][0] != 4 or board.state[1][1] != 5 or board.state[1][2] != 6) \
        + int(board.state[2][0] != 7 or board.state[2][1] != 8 or board.state[2][2] != 0) 

# Time bound
seconds = 60
timeBound = seconds * 10 ** 9




def main():
    #data collection
    # for m in [10,20,30,40,50]:
    plot_m = [10,20,30,40,50]
    # First plot
    BF_plot_solved_percentage = []
    MT_plot_solved_percentage = []
    CB_plot_solved_percentage = []
    NA_plot_solved_percentage = []
    # Second plot
    BF_plot_total_nodes_generated = []
    MT_plot_total_nodes_generated = []
    CB_plot_total_nodes_generated = []
    NA_plot_total_nodes_generated = []
    # Third plot
    BF_plot_time_to_solve = []
    MT_plot_time_to_solve = []
    CB_plot_time_to_solve = []
    NA_plot_time_to_solve = []
    # Fourth plot
    BF_plot_solution_lengths = []
    MT_plot_solution_lengths = []
    CB_plot_solution_lengths = []
    NA_plot_solution_lengths = []
    for m in [10,20,30,40,50]:
        # Heuristic algo
        heuristic = BF
        total_solved = 0
        time_to_solve = []
        solution_lengths = []
        total_nodes_generated = [] 
        for seed in range(0,10):
            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            # NOTE: process_time does not work on windows
            # start =  time.process_time()
            start =  time.time_ns()   
            '''
            ***********************************************
            Solve the Board state here with A*
            ***********************************************
            '''
            visited_state = {str(board): True}
            path_states  = [[]]
            board_states = [board]
            state_heuristic = [heuristic(board)]
            solution = []
            nodes_generated = 0
            # print("Starting board: \n", str(board))
            while True:
                # Limit time
                if time_out_of_bound(start, time.time_ns()):
                    # print("Latest path: ", path_states[len(path_states)-1])
                    print(f'Solution not found in {seconds} seconds')
                    break
                # Choose branch 
                heuristic_choice = min_heuristic_state(state_heuristic)
                current_board = board_states.pop(heuristic_choice)
                current_path = path_states.pop(heuristic_choice)
                current_state_heuristic = state_heuristic.pop(heuristic_choice)
                
                # Compute next states
                for (state, move) in current_board.next_action_states():
                    if visited_state.get(str(state)) is True:
                        continue
                    visited_state[str(current_board)] = True
                    board_states.append(state)
                    path_states.append(current_path + [move])
                    state_heuristic.append(current_state_heuristic + heuristic(state))
                    nodes_generated += 1

                # Check for completion
                if current_board.goal_test():
                    # print("GOAL REACHED")
                    solution = current_path
                    break
            end =  time.time_ns()
            solution_cpu_time = end-start
            # print(" Solution: ", solution)
            # print("Time taken: ", solution_cpu_time / (10 ** 9), 's')
            total_nodes_generated.append(nodes_generated)
            solution_length = len(solution)
            if solution_length:
                total_solved += 1
                solution_lengths.append(solution_length)
                time_to_solve.append(solution_cpu_time / (10 ** 9))
        BF_plot_solved_percentage.append(total_solved*10)
        BF_plot_total_nodes_generated.append(sum(total_nodes_generated))
        BF_plot_time_to_solve.append(np.average(time_to_solve) if len(time_to_solve) else -1)
        BF_plot_solution_lengths.append(np.average(solution_lengths) if len(solution_lengths) else -1)
        print(f'''
        Heuristic: {heuristic.__name__}
        times shuffled(m): {m}
        total solved: {total_solved}
        nodes generated: {total_nodes_generated}
        time to solve: {time_to_solve}s
        solution lengths: {solution_lengths}
        ''')
        # Heuristic algo
        heuristic = MT
        total_solved = 0
        time_to_solve = []
        solution_lengths = []
        total_nodes_generated = [] 
        for seed in range(0,10):
            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            # NOTE: process_time does not work on windows
            # start =  time.process_time()
            start =  time.time_ns()   
            '''
            ***********************************************
            Solve the Board state here with A*
            ***********************************************
            '''
            visited_state = {str(board): True}
            path_states  = [[]]
            board_states = [board]
            state_heuristic = [heuristic(board)]
            solution = []
            nodes_generated = 0
            # print("Starting board: \n", str(board))
            while True:
                # Limit time
                if time_out_of_bound(start, time.time_ns()):
                    # print("Latest path: ", path_states[len(path_states)-1])
                    print(f'Solution not found in {seconds} seconds. board:\n{board}')
                    break
                # Choose branch 
                heuristic_choice = min_heuristic_state(state_heuristic)
                current_board = board_states.pop(heuristic_choice)
                current_path = path_states.pop(heuristic_choice)
                current_state_heuristic = state_heuristic.pop(heuristic_choice)
                
                # Compute next states
                for (state, move) in current_board.next_action_states():
                    if visited_state.get(str(state)) is True:
                        continue
                    visited_state[str(current_board)] = True
                    board_states.append(state)
                    path_states.append(current_path + [move])
                    state_heuristic.append(current_state_heuristic + heuristic(state))
                    nodes_generated += 1

                # Check for completion
                if current_board.goal_test():
                    # print("GOAL REACHED")
                    solution = current_path
                    break
            end =  time.time_ns()
            solution_cpu_time = end-start
            # print(" Solution: ", solution)
            # print("Time taken: ", solution_cpu_time / (10 ** 9), 's')
            total_nodes_generated.append(nodes_generated)
            solution_length = len(solution)
            if solution_length:
                total_solved += 1
                solution_lengths.append(solution_length)
                time_to_solve.append(solution_cpu_time / (10 ** 9))
        MT_plot_solved_percentage.append(total_solved*10)
        MT_plot_total_nodes_generated.append(sum(total_nodes_generated))
        MT_plot_time_to_solve.append(np.average(time_to_solve) if len(time_to_solve) else -1)
        MT_plot_solution_lengths.append(np.average(solution_lengths) if len(solution_lengths) else -1)
        print(f'''
        Heuristic: {heuristic.__name__}
        times shuffled(m): {m}
        total solved: {total_solved}
        nodes generated: {total_nodes_generated}
        time to solve: {time_to_solve}s
        solution lengths: {solution_lengths}
        ''')
        # Heuristic algo
        heuristic = CB
        total_solved = 0
        time_to_solve = []
        solution_lengths = []
        total_nodes_generated = [] 
        for seed in range(0,10):
            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            # NOTE: process_time does not work on windows
            # start =  time.process_time()
            start =  time.time_ns()   
            '''
            ***********************************************
            Solve the Board state here with A*
            ***********************************************
            '''
            visited_state = {str(board): True}
            path_states  = [[]]
            board_states = [board]
            state_heuristic = [heuristic(board)]
            solution = []
            nodes_generated = 0
            # print("Starting board: \n", str(board))
            while True:
                # Limit time
                if time_out_of_bound(start, time.time_ns()):
                    # print("Latest path: ", path_states[len(path_states)-1])
                    print(f'Solution not found in {seconds} seconds. board:\n{board}')
                    break
                # Choose branch 
                heuristic_choice = min_heuristic_state(state_heuristic)
                current_board = board_states.pop(heuristic_choice)
                current_path = path_states.pop(heuristic_choice)
                current_state_heuristic = state_heuristic.pop(heuristic_choice)
                
                # Compute next states
                for (state, move) in current_board.next_action_states():
                    if visited_state.get(str(state)) is True:
                        continue
                    visited_state[str(current_board)] = True
                    board_states.append(state)
                    path_states.append(current_path + [move])
                    state_heuristic.append(current_state_heuristic + heuristic(state))
                    nodes_generated += 1

                # Check for completion
                if current_board.goal_test():
                    # print("GOAL REACHED")
                    solution = current_path
                    break
            end =  time.time_ns()
            solution_cpu_time = end-start
            # print(" Solution: ", solution)
            # print("Time taken: ", solution_cpu_time / (10 ** 9), 's')
            total_nodes_generated.append(nodes_generated)
            solution_length = len(solution)
            if solution_length:
                total_solved += 1
                solution_lengths.append(solution_length)
                time_to_solve.append(solution_cpu_time / (10 ** 9))
        CB_plot_solved_percentage.append(total_solved*10)
        CB_plot_total_nodes_generated.append(sum(total_nodes_generated))
        CB_plot_time_to_solve.append(np.average(time_to_solve) if len(time_to_solve) else -1)
        CB_plot_solution_lengths.append(np.average(solution_lengths) if len(solution_lengths) else -1)
        print(f'''
        Heuristic: {heuristic.__name__}
        times shuffled(m): {m}
        total solved: {total_solved}
        nodes generated: {total_nodes_generated}
        time to solve: {time_to_solve}s
        solution lengths: {solution_lengths}
        ''')
        # Heuristic algo
        heuristic = NA
        total_solved = 0
        time_to_solve = []
        solution_lengths = []
        total_nodes_generated = [] 
        for seed in range(0,10):
            # Sets the seed of the problem so all students solve the same problems
            board = Board(m, seed)
            
            # NOTE: process_time does not work on windows
            # start =  time.process_time()
            start =  time.time_ns()   
            '''
            ***********************************************
            Solve the Board state here with A*
            ***********************************************
            '''
            visited_state = {str(board): True}
            path_states  = [[]]
            board_states = [board]
            state_heuristic = [heuristic(board)]
            solution = []
            nodes_generated = 0
            # print("Starting board: \n", str(board))
            while True:
                # Limit time
                if time_out_of_bound(start, time.time_ns()):
                    # print("Latest path: ", path_states[len(path_states)-1])
                    print(f'Solution not found in {seconds} seconds. board:\n{board}')
                    break
                # Choose branch 
                heuristic_choice = min_heuristic_state(state_heuristic)
                current_board = board_states.pop(heuristic_choice)
                current_path = path_states.pop(heuristic_choice)
                current_state_heuristic = state_heuristic.pop(heuristic_choice)
                
                # Compute next states
                for (state, move) in current_board.next_action_states():
                    if visited_state.get(str(state)) is True:
                        continue
                    visited_state[str(current_board)] = True
                    board_states.append(state)
                    path_states.append(current_path + [move])
                    state_heuristic.append(current_state_heuristic + heuristic(state))
                    nodes_generated += 1

                # Check for completion
                if current_board.goal_test():
                    # print("GOAL REACHED")
                    solution = current_path
                    break
            end =  time.time_ns()
            solution_cpu_time = end-start
            # print(" Solution: ", solution)
            # print("Time taken: ", solution_cpu_time / (10 ** 9), 's')
            total_nodes_generated.append(nodes_generated)
            solution_length = len(solution)
            if solution_length:
                total_solved += 1
                solution_lengths.append(solution_length)
                time_to_solve.append(solution_cpu_time / (10 ** 9))
        NA_plot_solved_percentage.append(total_solved*10)
        NA_plot_total_nodes_generated.append(sum(total_nodes_generated))
        NA_plot_time_to_solve.append(np.average(time_to_solve) if len(time_to_solve) else -1)
        NA_plot_solution_lengths.append(np.average(solution_lengths) if len(solution_lengths) else -1)
        print(f'''
        Heuristic: {heuristic.__name__}
        times shuffled(m): {m}
        total solved: {total_solved}
        nodes generated: {total_nodes_generated}
        time to solve: {time_to_solve}s
        solution lengths: {solution_lengths}
        ''')

    print(f'''
    Percentage of problems solved: {float(total_solved / 10): .2%}
    Number of search nodes generated: {sum(total_nodes_generated)}
    Average CPU time per problem: {float(sum(time_to_solve)/total_solved)}s
    The average solution length: {float(sum(solution_lengths)/total_solved)}
    ''')

    plt.figure(1)
    plt.title("Percentage of problems solved")
    plt.plot(plot_m, BF_plot_solved_percentage, label="BF")
    plt.plot(plot_m, MT_plot_solved_percentage, label="MT")
    plt.plot(plot_m, CB_plot_solved_percentage, label="CB")
    plt.plot(plot_m, NA_plot_solved_percentage, label="NA")
    plt.xlabel("m")
    plt.ylabel("Solved")
    plt.legend()
    
    plt.figure(2)
    plt.title("Number of search nodes generated")
    plt.plot(plot_m, BF_plot_total_nodes_generated, label="BF")
    plt.plot(plot_m, MT_plot_total_nodes_generated, label="MT")
    plt.plot(plot_m, CB_plot_total_nodes_generated, label="CB")
    plt.plot(plot_m, NA_plot_total_nodes_generated, label="NA")
    plt.xlabel("m")
    plt.ylabel("Nodes generated")
    plt.legend()
    
    plt.figure(3)
    plt.title("Average CPU time per problem")
    plt.plot(plot_m, BF_plot_time_to_solve, label="BF")
    plt.plot(plot_m, MT_plot_time_to_solve, label="MT")
    plt.plot(plot_m, CB_plot_time_to_solve, label="CB")
    plt.plot(plot_m, NA_plot_time_to_solve, label="NA")
    plt.xlabel("m")
    plt.ylabel("Time(s)")
    plt.legend()
    
    plt.figure(4)
    plt.title("The average solution length")
    plt.plot(plot_m, BF_plot_solution_lengths, label="BF")
    plt.plot(plot_m, MT_plot_solution_lengths, label="MT")
    plt.plot(plot_m, CB_plot_solution_lengths, label="CB")
    plt.plot(plot_m, NA_plot_solution_lengths, label="NA")
    plt.xlabel("m")
    plt.ylabel("Solution length")
    plt.legend()
    plt.show()


'''
HELPER FUNCITONS
'''
def time_out_of_bound(start, end):
    return end - start > timeBound

def min_heuristic_state(heuristics):
    min_val = heuristics[0]
    min_idx = 0
    for i, val in enumerate(heuristics):
        if val < min_val:
            min_val = val
            min_idx = i
    return min_idx

def city_block_calculator(p1: tuple, p2: tuple) -> int:
    return abs(p1[0]-p2[0]) + abs(p1[1] - p2[1])

if __name__ == "__main__":
    main()