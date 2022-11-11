import pandas as pd
import time
from datetime import datetime
import re
import os
import csv
# from collections import deque


input_file = input('Enter trace (input) file path: ')
app_name = input('Enter the name of traced application: ')
now = datetime.now()
start_time = time.time()

file = open('%s' %input_file, 'r')
line = file.readline()

if 'maj/min' not in line:
    with open('%s' %input_file, 'r+') as f: s = f.read(); f.seek(0); f.write('  maj/min cpu #seq time pid event R/W start_sector + #sectors pname\n' + s)

if not os.path.exists('../../results'):
    os.mkdir('../../results')
    os.mkdir('../../results/text_results')
elif not os.path.exists('../../results/text_results'):
    os.mkdir('../../results/text_results')

print('Retrieving data ...')

df = pd.read_table('%s' %input_file, header=0, usecols=['R/W', 'start_sector', '#sectors'], delim_whitespace=True, dtype=str, na_filter=False)


read_sectors = 0
write_sectors = 0
read_count = 0
write_count = 0


sector_range = {
    '1-4': 0,
    '5-8': 0,
    '9-12': 0,
    '13-16': 0,
    '17-20': 0,
    '21-24': 0,
    '25-48': 0,
    '49-64': 0,
    '65-128': 0,
    '>128': 0
}


read_range = {
    '1-4': 0,
    '5-8': 0,
    '9-12': 0,
    '13-16': 0,
    '17-20': 0,
    '21-24': 0,
    '25-48': 0,
    '49-64': 0,
    '65-128': 0,
    '>128': 0
}


write_range = {
    '1-4': 0,
    '5-8': 0,
    '9-12': 0,
    '13-16': 0,
    '17-20': 0,
    '21-24': 0,
    '25-48': 0,
    '49-64': 0,
    '65-128': 0,
    '>128': 0
}


def sectors_to_kb(value):
    return round(value * 512 / 1024, 1)


def sectors_to_mb(value):
    return round(value * 512 / 1048576, 1)


def sectors_to_gb(value):
    return round(value * 512 / 1073741824, 1)

def sectors_to_tb(value):
    return round(value * 512 / 1099511627776, 1)


def compare_size(value):
    if value >= 0 and value <= 4:
        return '1-4'
    elif value >= 5 and value <= 8:
        return '5-8'
    elif value >= 9 and value <= 12:
        return '9-12'
    elif value >= 13 and value <= 16:
        return '13-16'
    elif value >= 17 and value <= 20:
        return '17-20'
    elif value >= 21 and value <= 24:
        return '21-24'
    elif value >= 25 and value <= 48:
        return '25-48'
    elif value >= 49 and value <= 64:
        return '49-64'
    elif value >= 65 and value <= 128:
        return '65-128'
    elif value > 128:
        return '>128'

starting_sectors = []

print('Generating basic results ...')

# size of individual IOs

for index in df.index:
        
    if df['#sectors'][index] != '' and not re.match('^.*[a-zA-Z]+.*', df['#sectors'][index]):

        temp = sectors_to_kb(int(df['#sectors'][index]))

        if 'R' in df['R/W'][index] and 'M' not in df['R/W'][index]:
            read_sectors += int(df['#sectors'][index])
            read_count += 1
            read_range[compare_size(temp)] += 1
            starting_sectors.append(df['start_sector'][index])
        elif 'W' in df['R/W'][index] and 'M' not in df['R/W'][index]:
            write_sectors += int(df['#sectors'][index])                        
            write_count += 1
            write_range[compare_size(temp)] += 1
            starting_sectors.append(df['start_sector'][index])
        
        sector_range[compare_size(temp)] += 1
         
total_requests = read_count + write_count

starting_sectors = [int(i) for i in starting_sectors]

starting_sectors.sort()


# stat for all IOs

with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'w') as f:
    f.write('Number of Read requests: %d\n\n' %read_count)
    f.write('Number of Write requests: %d\n\n' %write_count)
    f.write('Read size: %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(read_sectors, sectors_to_kb(read_sectors), sectors_to_mb(read_sectors), sectors_to_gb(read_sectors), sectors_to_tb(read_sectors)))
    f.write('Write size: %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(write_sectors, sectors_to_kb(write_sectors), sectors_to_mb(write_sectors), sectors_to_gb(write_sectors), sectors_to_tb(write_sectors)))
    f.write('Total requests size (Read + Write): %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(read_sectors+write_sectors, sectors_to_kb(read_sectors+write_sectors), sectors_to_mb(read_sectors+write_sectors), sectors_to_gb(read_sectors+write_sectors), sectors_to_tb(read_sectors+write_sectors)))
    f.write('Read percentage: {:.1%}\n\n'.format(read_count / total_requests))
    f.write('Write percentage: {:.1%}\n\n'.format(write_count / total_requests))

    if read_count != 0:
        f.write('Average Read size: %0.1f KB\n\n' %sectors_to_kb(read_sectors / read_count))
    else:
        f.write('Average Read size: 0 KB\n\n')


    if write_count != 0:
        f.write('Average Write size: %0.1f KB\n\n' %sectors_to_kb(write_sectors / write_count))
    else:
        f.write('Average Write size: 0 KB\n\n')

    f.write('Maximum requested address (sector offset): (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(sectors_to_kb(max(starting_sectors)), sectors_to_mb(max(starting_sectors)), sectors_to_gb(max(starting_sectors)), sectors_to_tb(max(starting_sectors))))
    f.write('Minimum requested address (sector offset): (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(sectors_to_kb(min(starting_sectors)), sectors_to_mb(min(starting_sectors)), sectors_to_gb(min(starting_sectors)), sectors_to_tb(min(starting_sectors))))


for key in sector_range:
    sector_range[key] = round(sector_range[key] / total_requests * 100, 1)



with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
    f.write('\n***Distribution of I/O Sizes (Total R/W)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' %sector_range['1-4'])
    f.write('\t    [5-8]\t\t    %0.1f\n' %sector_range['5-8'])
    f.write('\t    [9-12]\t\t    %0.1f\n' %sector_range['9-12'])
    f.write('\t    [13-16]\t\t    %0.1f\n' %sector_range['13-16'])
    f.write('\t    [17-20]\t\t    %0.1f\n' %sector_range['17-20'])
    f.write('\t    [21-24]\t\t    %0.1f\n' %sector_range['21-24'])
    f.write('\t    [25-48]\t\t    %0.1f\n' %sector_range['25-48'])
    f.write('\t    [49-64]\t\t    %0.1f\n' %sector_range['49-64'])
    f.write('\t    [65-128]\t\t    %0.1f\n' %sector_range['65-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' %sector_range['>128'])



for key in read_range:
    if read_count != 0:
        read_range[key] = round(read_range[key] / read_count * 100, 1)
    else:
        read_range[key] = 0

for key in write_range:
    if write_count != 0:
        write_range[key] = round(write_range[key] / write_count * 100, 1)
    else:
        write_range[key] = 0



with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
    f.write('\n\n***Distribution of I/O Sizes (Read)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' %read_range['1-4'])
    f.write('\t    [5-8]\t\t    %0.1f\n' %read_range['5-8'])
    f.write('\t    [9-12]\t\t    %0.1f\n' %read_range['9-12'])
    f.write('\t    [13-16]\t\t    %0.1f\n' %read_range['13-16'])
    f.write('\t    [17-20]\t\t    %0.1f\n' %read_range['17-20'])
    f.write('\t    [21-24]\t\t    %0.1f\n' %read_range['21-24'])
    f.write('\t    [25-48]\t\t    %0.1f\n' %read_range['25-48'])
    f.write('\t    [49-64]\t\t    %0.1f\n' %read_range['49-64'])
    f.write('\t    [65-128]\t\t    %0.1f\n' %read_range['65-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' %read_range['>128'])

    f.write('\n\n***Distribution of I/O Sizes (Write)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' %write_range['1-4'])
    f.write('\t    [5-8]\t\t    %0.1f\n' %write_range['5-8'])
    f.write('\t    [9-12]\t\t    %0.1f\n' %write_range['9-12'])
    f.write('\t    [13-16]\t\t    %0.1f\n' %write_range['13-16'])
    f.write('\t    [17-20]\t\t    %0.1f\n' %write_range['17-20'])
    f.write('\t    [21-24]\t\t    %0.1f\n' %write_range['21-24'])
    f.write('\t    [25-48]\t\t    %0.1f\n' %write_range['25-48'])
    f.write('\t    [49-64]\t\t    %0.1f\n' %write_range['49-64'])
    f.write('\t    [65-128]\t\t    %0.1f\n' %write_range['65-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' %write_range['>128'])


print('Generating access_freq results ...')

# access frequency of IOs

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


with open('../../results/text_results/%s_access_freq_%s.csv' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    for key in dic_duplicated:
        writer.writerow([key, dic_duplicated[key]])



with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'r+') as f: s = f.read(); f.seek(0); f.write('*** Total execution time: %0.1f seconds ***\n\n' %round(time.time() - start_time, 2) + s)

print('Total execution time: %0.1f seconds' %round(time.time() - start_time, 2))
