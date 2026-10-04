# Q2.2
clock_per_instruction = 5

q1_n_instructions = 7
q2_n_instructions = 3
q1_cycle_time = 1
q2_cycle_time = q1_cycle_time * 1.24

q1_n_cycles = q1_n_instructions + clock_per_instruction - 1
q2_n_cycles = q2_n_instructions + clock_per_instruction - 1

q1_execution_time = q1_n_cycles * q1_cycle_time
q2_execution_time = q2_n_cycles * q2_cycle_time

speedup = q1_execution_time/q2_execution_time
# print("Q2.2 q1_execution_time: ", q1_execution_time)
# print("Q2.2 q2_execution_time: ", q2_execution_time)
print(f'Q2.2 speedup: q2 has a speedup of {speedup} time over q1')

# Q3.3
CPI_not_taken = 1
CPI_taken = 3
avg_branching_CPI = 0.8 * CPI_taken + 0.2 * CPI_not_taken
print(f'Q3.3 Average branching CPI: {avg_branching_CPI}')

# Q3.4
branch_frequency = 0.17
avg_non_branching_CPI = 1.6386
avg_CPI = branch_frequency * avg_branching_CPI + (1 - branch_frequency) * avg_non_branching_CPI
print(f'Q3.4 Average CPI: {avg_CPI}')

# Q3.5
cycle_time_penalty = 1.18
dedicated_taken_CPI = 2
avg_dedicated_branching_CPI = 0.8 * dedicated_taken_CPI + 0.2 * CPI_not_taken
print(f'Q3.5 Average dedicated branching CPI: {avg_dedicated_branching_CPI}')

# Q3.6
branch_delay_CPI = 0.8 * (0.60 * 1 + 0.4 * 3) + 0.2 * 1
print(f'Q3.6 Average branch delay branching CPI: {branch_delay_CPI}')
