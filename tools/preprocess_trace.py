import time

input_file = input('Enter trace (input) file path: ')
start_time = time.time()

print('processing trace ...')


lines = []
new_lines = []

with open('%s' %input_file, 'r') as f:
    lines = f.read().splitlines()

for line in lines:
    if 'F' not in line and '+' in line and 'maj/min' not in line:
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


with open('../data/preprocess_trace.txt', 'w') as f:
    for item in new_lines:
        f.write(item + '\n')

print('Total execution time: %0.1f seconds: ' %round(time.time() - start_time, 2))
