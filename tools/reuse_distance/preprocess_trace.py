import time
import os
import csv

input_file = input('Enter trace (input) file path: ')
start_time = time.time()


if not os.path.exists('../../results'):
    os.mkdir('../../results')
    os.mkdir('../../results/text_results')
elif not os.path.exists('../../results/text_results'):
    os.mkdir('../../results/text_results')

print('processing trace ...')


lines = []
new_lines = []

with open('%s' %input_file, 'r') as f:
    lines = f.read().splitlines()

for line in lines:
    if 'F' not in line and 'N' not in line and 'M' not in line and 'maj/min' not in line and '+' in line:
        splitted_line = line.split()
        size = int(splitted_line[9])
        if size > 8:
            splitted_line[9] = '8'
            for i in range(size // 8):
                new_line = ''
                for item in splitted_line:
                    new_line += item + ' '
                
                new_lines.append(new_line[:-1])
                splitted_line[7] = str(int(splitted_line[7]) + 1)
        else:
            new_line = ''
            for item in splitted_line:
                new_line += item + ' '
            
            new_lines.append(new_line[:-1])

starting_sectors = []
    
with open('../../results/text_results/preprocess_trace.txt', 'w') as f:
    for item in new_lines:
        starting_sectors.append(int(item.split()[7]))
        f.write(item + '\n')

starting_sectors.sort()

dic_duplicated = {}

for item in starting_sectors:
    if not item in dic_duplicated:
        dic_duplicated[item] = 1
    else:
        dic_duplicated[item] += 1

for key in dict(dic_duplicated):
    if not dic_duplicated[key] > 1:
        del dic_duplicated[key]


dic_duplicated = {str(key): value for key, value in dic_duplicated.items()}


with open('../../results/text_results/preprocess_access_freq.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    for key in dic_duplicated:
        writer.writerow([key, dic_duplicated[key]])


print('Total execution time: %0.1f seconds' %round(time.time() - start_time, 2))
