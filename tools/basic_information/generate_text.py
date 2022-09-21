import pandas as pd
import time
from datetime import datetime
import re
import csv
# from collections import deque


input_file = input('Enter trace (input) file path: ')
app_name = input('Enter the name of traced application: ')
now = datetime.now()
start_time = time.time()

print('Retrieving data ...')

df = pd.read_table('%s' %input_file, header=0, usecols=['R/W', 'start_sector', '#sectors'], delim_whitespace=True, dtype=str, na_filter=False)


total_requests = 0
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
    if value >= 1 and value <= 4:
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


print('Generating basic results ...')

# size of individual IOs

for index in df.index:
        
    if df['#sectors'][index] != '' and not re.match('^.*[a-zA-Z]+.*', df['#sectors'][index]):

        temp = sectors_to_kb(int(df['#sectors'][index]))

        total_requests += 1

        if 'R' in df['R/W'][index]:
            read_sectors += int(df['#sectors'][index])
            read_count += 1
            read_range[compare_size(temp)] += 1
        elif 'W' in df['R/W'][index]:
            write_sectors += int(df['#sectors'][index])                        
            write_count += 1
            write_range[compare_size(temp)] += 1
        
        sector_range[compare_size(temp)] += 1
         


starting_sectors = list(df['start_sector'])


for item in list(starting_sectors):
    if item == '0' or item == '' or re.match('^.*[a-zA-Z]+.*', item) or '[' in item:
        starting_sectors.remove(item)

starting_sectors = [int(i) for i in starting_sectors]


# stat for all IOs

with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'w') as f:
    f.write('Number of Read requests: %d\n\n' %read_count)
    f.write('Number of Write requests: %d\n\n' %write_count)
    f.write('Read size: %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(read_sectors, sectors_to_kb(read_sectors), sectors_to_mb(read_sectors), sectors_to_gb(read_sectors), sectors_to_tb(read_sectors)))
    f.write('Write size: %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(write_sectors, sectors_to_kb(write_sectors), sectors_to_mb(write_sectors), sectors_to_gb(write_sectors), sectors_to_tb(write_sectors)))
    f.write('Total size of requested sectors (Reed + Write): %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' %(read_sectors+write_sectors, sectors_to_kb(read_sectors+write_sectors), sectors_to_mb(read_sectors+write_sectors), sectors_to_gb(read_sectors+write_sectors), sectors_to_tb(read_sectors+write_sectors)))
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

    f.write('Maximum requested address (sector offset): %d GB\n\n' %sectors_to_gb(max(starting_sectors)))
    f.write('Minimum requested address (sector offset): %d GB\n\n' %sectors_to_gb(min(starting_sectors)))




for key in sector_range:
    sector_range[key] = round(sector_range[key] / total_requests * 100, 1)



with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
    f.write('\n***Distribution of I/O Requests (total R/W)***\n')
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
    read_range[key] = round(read_range[key] / total_requests * 100, 1)

for key in write_range:
    write_range[key] = round(write_range[key] / total_requests * 100, 1)



with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
    f.write('\n\n***Distribution of I/O Requests (Read)***\n')
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

    f.write('\n\n***Distribution of I/O Requests (Write)***\n')
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

sorted_starting_sectors = sorted(starting_sectors)
dic_duplicated = {}

for item in sorted_starting_sectors:
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


def cdf_freq_range(fn, s, e, i):

    dup_range = {
    '%d-%d' %(s, s+i): 0,
    '%d-%d' %((s+i+1), (s+2*i+1)): 0,
    '%d-%d' %((s+2*i+2), (s+3*i+2)): 0,
    '%d-%d' %((s+3*i+3), (s+4*i+3)): 0,
    '%d-%d' %((s+4*i+4), (s+5*i+4)): 0,
    '%d-%d' %((s+5*i+5), e): 0,
    '>%d' %e: 0
    }


    for key in dic_duplicated:
        if dic_duplicated[key] >= s and dic_duplicated[key] <= (s+i):
            dup_range['%d-%d' %(s, s+i)] += 1
        elif dic_duplicated[key] >= (s+i+1) and dic_duplicated[key] <= (s+2*i+1):
            dup_range['%d-%d' %((s+i+1), (s+2*i+1))] += 1
        elif dic_duplicated[key] >= (s+2*i+2) and dic_duplicated[key] <= (s+3*i+2):
            dup_range['%d-%d' %((s+2*i+2), (s+3*i+2))] += 1
        elif dic_duplicated[key] >= (s+3*i+3) and dic_duplicated[key] <= (s+4*i+3):
            dup_range['%d-%d' %((s+3*i+3), (s+4*i+3))] += 1
        elif dic_duplicated[key] >= (s+4*i+4) and dic_duplicated[key] <= (s+5*i+4):
            dup_range['%d-%d' %((s+4*i+4), (s+5*i+4))] += 1
        elif dic_duplicated[key] >= (s+5*i+5) and dic_duplicated[key] <= e:
            dup_range['%d-%d' %((s+5*i+5), e)] += 1
        elif dic_duplicated[key] > e:
            dup_range['>%d' %e] += 1

    for key in dup_range:
        dup_range[key] = round(dup_range[key] / len(dic_duplicated) * 100, 1)


    with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
        f.write('\n\n\t***Cumulative Distribution Function (CDF)***\n')
        f.write('\tFrequency Range\t\tDistribution of Range (%)\n\t---------------\t\t-------------------------\n')
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %(s, s+i, dup_range['%d-%d' %(s, s+i)]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+i+1), (s+2*i+1), dup_range['%d-%d' %((s+i+1), (s+2*i+1))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+2*i+2), (s+3*i+2), dup_range['%d-%d' %((s+2*i+2), (s+3*i+2))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+3*i+3), (s+4*i+3), dup_range['%d-%d' %((s+3*i+3), (s+4*i+3))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+4*i+4), (s+5*i+4), dup_range['%d-%d' %((s+4*i+4), (s+5*i+4))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+5*i+5), e, dup_range['%d-%d' %((s+5*i+5), e)]))
        f.write('\t    [>%d]\t\t\t%0.1f\n\n\n\n' %(e, dup_range['>%d' %e]))

    for key in dup_range:
        if dup_range[key] >= 50:
            splitted = key.split('-')
            cdf_freq_range(fn + 1, int(splitted[0]), int(splitted[1]), (int(splitted[1])/5)-1)

cdf_freq_range(1, 1, 300, 49)


# print('Generating reuse_distance results ...')


# reuse distance

# reuse_dis_dic = {}   # dictionary of lists >> key shows address and values show reuse distance
# reuse_dis_stack = deque()

# for item in starting_sectors:
#     counter = 0
#     temp_list = []
#     for i in reuse_dis_stack:
#         if i == item:
#             while reuse_dis_stack[-1] != item:
#                 temp_list.append(reuse_dis_stack.pop())
#                 counter += 1
#             reuse_dis_dic[str(item)].append(counter)
#             reuse_dis_stack.pop()
#             temp_list.reverse()
#             for j in temp_list:
#                 reuse_dis_stack.append(j)
#             reuse_dis_stack.append(item)
#             break
#     if counter == 0:
#         reuse_dis_dic[str(item)] = [-1]
#         reuse_dis_stack.append(item)


# for key, value in list(reuse_dis_dic.items()):
#     if value == [-1]:
#         del reuse_dis_dic[key]
#     else:
#         value.remove(-1)


# with open('../../results/text_results/%s_reuse_dis_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'w') as f:
#     for key in reuse_dis_dic:
#         f.write('%s: %s\n' %(key, reuse_dis_dic[key]))


with open('../../results/text_results/%s_basic_results_%s.txt' %(app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'r+') as f: s = f.read(); f.seek(0); f.write('*** Total execution time: %0.1f seconds ***\n\n' %round(time.time() - start_time, 2) + s)

print('Total execution time: %0.1f seconds: ' %round(time.time() - start_time, 2))
