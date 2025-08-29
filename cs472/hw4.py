import math
# Q1
num_va_bits = 38
pg_size_bytes = 4 * 2 ** 10
bytes_per_entry = 4


# Q1.1
num_entries = 2 ** (num_va_bits - math.log2(pg_size_bytes))
print('Q1.1: ')
print('num_pg_entries = 2 ** (num_va_bits - math.log2(pg_size_bytes))')
print(f'\t = 2 ^ ({num_va_bits} - {int(math.log2(pg_size_bytes))})')
print(f'\t = 2 ^ ({num_va_bits - int(math.log2(pg_size_bytes))})')
# print(f'\t = {num_pg_entries} entries')

# Q1.2
physical_memory_in_Bytes = 8 * (2 ** 10) * (2 ** 10) * (2 ** 10)
bytes_per_table = num_entries * bytes_per_entry
print('\nQ1.2: ')
print('table_size = num_pg_entries * bytes_per_entry')
print(f'\t = {bytes_per_table} Bytes')
num_tables = physical_memory_in_Bytes / bytes_per_table
print('num_tables = physical_memory_in_Bytes / table_size_in_Bytes')
print(f'\t = {physical_memory_in_Bytes} / {bytes_per_table}')
print(f'\t = {num_tables}')

# Q2
vas = [49225, 77777, 2227, 76543, 34587, 48870, 12608]
for va in vas:
    binary = bin(va)[2:].rjust(17,'0')
    va_num = va//(2**12)
    offset = va%(2**12)
    print(f'va:{va}({binary});VA#: {va_num}; Offset: {offset}')