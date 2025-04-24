import csv
import os
import time

input_file = input('Enter reuse output path: ')
start_time = time.time()


if not os.path.exists('../../results'):
    os.mkdir('../../results')
    os.mkdir('../../results/text_results')
elif not os.path.exists('../../results/text_results'):
    os.mkdir('../../results/text_results')

print('converting reuse output to CSV file ...')

with open('%s' %input_file, 'r') as file:
    lines = file.read().splitlines()

with open('../../results/text_results/reuse_output.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    for line in lines:
        writer.writerow(line.split())


print('Total execution time: %0.1f seconds' %round(time.time() - start_time, 2))
