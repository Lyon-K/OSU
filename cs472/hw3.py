# Q1
byte_offset = (1 - 0) + 1
block_offset = (5 - 2) + 1
index = (8 - 6) + 1
tag = (31 - 10) + 1
valid = 1

# Q1.1
cache_block_size = (2 ** block_offset) * (2 ** byte_offset)
print(f'Q1.1: {cache_block_size} bytes')

# Q1.2
num_entries = 2 ** index
print(f'Q1.2: {num_entries} entries')

# Q1.3
data_storage = cache_block_size * (num_entries * 8)
total_bits_required = num_entries * ((cache_block_size * 8) + tag + valid)
print(f'Q1.3: {total_bits_required / data_storage}')

# Q1.4
print('Q1.4:')
nums = [1, 348, 576, 9870, 7980, 364, 4360, 614, 4740, 3000, 1440, 3]
for idx, num in enumerate(nums):
    block_address = num // 64
    block_ID_in_cache = (block_address % 16)
    print(f'\t({idx+1}) {num}: BA={block_address}, BID={block_ID_in_cache}')

# Q1.7
print('Q1.7:')
index = range(16)
tag = ['EMpTY' for _ in range(16)]
data = ['EMpTY' for _ in range(16)]
for i in range(12):
    block_address = nums[i] // 64
    block_ID_in_cache = (block_address % 16)
    tag[block_ID_in_cache] = (bin(nums[i])[:-10])[2:]
    if tag[block_ID_in_cache] == '':
        tag[block_ID_in_cache] = '0'.rjust(22,'0')
    else:
        tag[block_ID_in_cache] = tag[block_ID_in_cache].rjust(22,'0')
    data[block_ID_in_cache] = f'MEM[{block_address*64}-{block_address*64+63}]'
    if i == 11:
        print(f'ITERATION {i}')
        for entry in range(16):
            print(f'{entry}\t{tag[entry]}\t{data[entry]}')
        print('')

# Q2
print('Q2:')
nums = [3, 180, 43, 2, 191, 88, 311, 49, 186, 240]
cache_content_index = [0 for _ in range(4)]
cache_content = [['   ' for _ in range(3)] for _ in range(4)]
visited = []
for i, num in enumerate(nums):
    block_address = num//16
    index = block_address % (1 << 2)
    offset = num % 16
    if (index, block_address) in visited:
        print(f'HIT: Byte Address: {num}; BA: {block_address}; I: {index}; O: {offset}')
        if cache_content[index][cache_content_index[index]] != '   ':
            cache_content_index[index] = (cache_content_index[index] + 1) % 3 
    else:
        print(f'MISS: Byte Address: {num}; BA: {block_address}; I: {index}; O: {offset}')
        cache_content[index][cache_content_index[index]] = f'{block_address * 16}-{block_address * 16 + 15}'
        visited.append((index, block_address))
        cache_content_index[index] = (cache_content_index[index] + 1) % 3
    print(cache_content)
    print('')

# Q3.1
print('Q3.1:')
p1_mem_access_time = 70
p2_mem_access_time = 80
p3_mem_access_time = 100

p1_miss_rate = 0.15
p1_hit_rate = 1 - p1_miss_rate
p1_hit_time = 0.77
p2_miss_rate = 0.1
p2_hit_rate = 1 - p2_miss_rate
p2_hit_time = 1.4
p3_miss_rate = 0.07
p3_hit_rate = 1 - p3_miss_rate
p3_hit_time = 4

p1_effective_clock_time = p1_hit_time + p1_miss_rate * p1_mem_access_time
p2_effective_clock_time = p2_hit_time + p2_miss_rate * p2_mem_access_time
p3_effective_clock_time = p3_hit_time + p3_miss_rate * p3_mem_access_time
print(f'Q3.2 p1 effective clock time: {p1_effective_clock_time}ns')
print(f'Q3.2 p2 effective clock time: {p2_effective_clock_time}ns')
print(f'Q3.2 p3 effective clock time: {p3_effective_clock_time}ns\n')

# Q3.3
print('Q3.3:')
base_CPI = 2
p1_miss_I_cache = 1 * p1_miss_rate * (p1_mem_access_time/p1_hit_time)
p1_miss_D_cache = 0.36 * p1_miss_rate * (p1_mem_access_time/p1_hit_time)
p1_effective_CPI = base_CPI + p1_miss_I_cache + p1_miss_D_cache
p1_effective_time = p1_effective_CPI * p1_hit_time

p2_miss_I_cache = 1 * p2_miss_rate * (p2_mem_access_time/p2_hit_time)
p2_miss_D_cache = 0.36 * p2_miss_rate * (p2_mem_access_time/p2_hit_time)
p2_effective_CPI = base_CPI + p2_miss_I_cache + p2_miss_D_cache
p2_effective_time = p2_effective_CPI * p2_hit_time

p3_miss_I_cache = 1 * p3_miss_rate * (p3_mem_access_time/p3_hit_time)
p3_miss_D_cache = 0.36 * p3_miss_rate * (p3_mem_access_time/p3_hit_time)
p3_effective_CPI = base_CPI + p3_miss_I_cache + p3_miss_D_cache
p3_effective_time = p3_effective_CPI * p3_hit_time

# print(f'Q3.3 p1 effective CPI: {p1_effective_CPI} cycles')
# print(f'Q3.3 p2 effective CPI: {p2_effective_CPI} cycles')
# print(f'Q3.3 p3 effective CPI: {p3_effective_CPI} cycles')

print(f'Q3.3 p1 effective clock speed: {p1_effective_time} ns/ins')
print(f'Q3.3 p2 effective clock speed: {p2_effective_time} ns/ins')
print(f'Q3.3 p3 effective clock speed: {p3_effective_time} ns/ins')

# Q4
print('\nQ4:')
L1_local_miss = 0.2
L1_local_hit = 1 - L1_local_miss
L2_local_miss = 0.4
L2_local_hit = 1 - L2_local_miss
L3_global_miss = 0.05
L3_local_miss = L3_global_miss / L1_local_miss / L2_local_miss
L3_local_hit = 1 - L3_local_miss
print(f'Q4.1: L1_local_miss * L2_local_hit \n\t= {L1_local_miss * L2_local_hit}')
print(f'Q4.2: L1_local_miss * L2_local_miss * L3_local_hit \n\t= {L1_local_miss * L2_local_miss * L3_local_hit}')

L1_hit_time = 1
L2_hit_time = 5
L3_hit_time = 10
main_memory = 100
print(f'''L1_hit_time + L2_hit_time * L1_local_miss + L3_hit_time * (L1_local_miss * L2_local_miss) + main_memory * L3_global_miss 
      \t={L1_hit_time} + {L2_hit_time} * {L1_local_miss} + {L3_hit_time} * ({L1_local_miss} * {L2_local_miss}) + {main_memory} * {L3_global_miss}
      \t={L1_hit_time + L2_hit_time * L1_local_miss + L3_hit_time * (L1_local_miss * L2_local_miss) + main_memory * L3_global_miss}''')