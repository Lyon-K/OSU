from __future__ import annotations
from board import Board
from collections.abc import Callable


'''
Heuristics
'''
def BF(_: Board) -> int:
    return 0

def MT(board: Board) -> int:
    return int(board.state[0][0] != 1) + int(board.state[0][1] != 2) + int(board.state[0][2] != 3) \
        + int(board.state[1][0] != 4) + int(board.state[1][1] != 5) + int(board.state[1][2] != 6) \
        + int(board.state[2][0] != 7) + int(board.state[2][1] != 8)

def CB(board: Board) -> int:
    coords = {1: (0,0), 2: (0,1), 3: (0,2), 4: (1,0), 5: (1,1), 6: (1,2), 7: (2,0), 8: (2,1), 0: (0,0)}
    return city_block_calculator(coords[1], coords[board.state[0][0]]) + city_block_calculator(coords[2], coords[board.state[0][1]]) + city_block_calculator(coords[3], coords[board.state[0][2]]) \
        + city_block_calculator(coords[4], coords[board.state[1][0]]) + city_block_calculator(coords[5], coords[board.state[1][1]]) + city_block_calculator(coords[6], coords[board.state[1][2]]) \
        + city_block_calculator(coords[7], coords[board.state[2][0]]) + city_block_calculator(coords[8], coords[board.state[2][1]]) + city_block_calculator(coords[0], coords[board.state[2][2]])

def NA(board: Board) -> int:
    # coords = {1: (0,0), 2: (0,1), 3: (0,2), 4: (1,0), 5: (1,1), 6: (1,2), 7: (2,0), 8: (2,1), 0: (0,0)}
    score = 0
    score += 1 if board.state[0][0] != 1 and board.state[0][1] != 2 and board.state[0][2] != 3 else 0
    score += 1 if board.state[1][0] != 4 and board.state[1][1] != 5 and board.state[1][2] != 6 else 0
    score += 1 if board.state[2][0] != 7 and board.state[2][1] != 8 and board.state[2][2] != 0 else 0
    return score



'''
A* Search 
'''
def a_star_search(board: Board, heuristic: Callable[[Board], int]):
    # Time bound
    # seconds = 60
    # timeBound = seconds * 10 ** 9
    visited_state = {str(board): True}
    path_states  = [[]]
    board_states = [board]
    state_heuristic = [heuristic(board)]
    solution = []
    while True:
        # Limit time
        # if time_out_of_bound(start, time.time_ns(), timeBound):
        #     break

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

        # Check for completion
        if current_board.goal_test():
            solution = current_path
            break
    return solution


'''
HELPER FUNCITONS
'''
# def time_out_of_bound(start, end, timeBound):
#     return end - start > timeBound

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
