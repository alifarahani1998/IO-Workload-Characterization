import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime
import re
from collections import deque



input_file = input('Enter the name of trace (input) file: ')
app_name = input('Enter the name of traced application: ')
now = datetime.now()
start_time = time.time()

df = pd.read_table('%s' % input_file, header=0, usecols=['R/W', 'start_sector', '#sectors'], delim_whitespace=True, dtype=str, na_filter=False)


total_requests = 0
read_sectors = 0
write_sectors = 0
read_count = 0
write_count = 0


sector_range = {
    '1-4': 0,
    '4-8': 0,
    '8-12': 0,
    '12-16': 0,
    '16-20': 0,
    '20-24': 0,
    '24-48': 0,
    '48-64': 0,
    '64-128': 0,
    '>128': 0
}


read_range = {
    '1-4': 0,
    '4-8': 0,
    '8-12': 0,
    '12-16': 0,
    '16-20': 0,
    '20-24': 0,
    '24-48': 0,
    '48-64': 0,
    '64-128': 0,
    '>128': 0
}


write_range = {
    '1-4': 0,
    '4-8': 0,
    '8-12': 0,
    '12-16': 0,
    '16-20': 0,
    '20-24': 0,
    '24-48': 0,
    '48-64': 0,
    '64-128': 0,
    '>128': 0
}


def sectors_to_kb(value):
    return round(value * 512 / 1024, 2)


def sectors_to_mb(value):
    return round(value * 512 / 1048576, 2)


def sectors_to_gb(value):
    return round(value * 512 / 1073741824, 2)

def sectors_to_tb(value):
    return round(value * 512 / 1099511627776, 2)


def compare_size(value):
    if value >= 1 and value < 4:
        return '1-4'
    elif value >= 4 and value < 8:
        return '4-8'
    elif value >= 8 and value < 12:
        return '8-12'
    elif value >= 12 and value < 16:
        return '12-16'
    elif value >= 16 and value < 20:
        return '16-20'
    elif value >= 20 and value < 24:
        return '20-24'
    elif value >= 24 and value < 48:
        return '24-48'
    elif value >= 48 and value < 64:
        return '48-64'
    elif value >= 64 and value < 128:
        return '64-128'
    elif value >= 128:
        return '>128'


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
    if item == '' or re.match('^.*[a-zA-Z]+.*', item) or '[' in item:
        starting_sectors.remove(item)

starting_sectors = [int(i) for i in starting_sectors]


# stat for all IOs

with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H:%M}".format(now)), 'w') as f:
    f.write('Number of reads: %d\n' % read_count)
    f.write('Number of writes: %d\n' % write_count)
    f.write('Size of reads: %d sectors (%0.2f KB) (%0.2f MB) (%0.2f GB) (%0.2f TB)\n' % (read_sectors, sectors_to_kb(read_sectors), sectors_to_mb(read_sectors), sectors_to_gb(read_sectors), sectors_to_tb(read_sectors)))
    f.write('Size of writes: %d sectors (%0.2f KB) (%0.2f MB) (%0.2f GB) (%0.2f TB)\n' % (write_sectors, sectors_to_kb(write_sectors), sectors_to_mb(write_sectors), sectors_to_gb(write_sectors), sectors_to_tb(write_sectors)))
    f.write('Total size of requested sectors: %d sectors (%0.2f KB) (%0.2f MB) (%0.2f GB) (%0.2f TB)\n' % (read_sectors+write_sectors, sectors_to_kb(read_sectors+write_sectors), sectors_to_mb(read_sectors+write_sectors), sectors_to_gb(read_sectors+write_sectors), sectors_to_tb(read_sectors+write_sectors)))
    f.write('Read percentage: {:.2%}\n'.format(read_count / total_requests))
    f.write('Write percentage: {:.2%}\n'.format(write_count / total_requests))

    f.write('Maximum address (sector offset): %d GB\n' % sectors_to_gb(max(starting_sectors)))
    f.write('Minimum address (sector offset): %d GB\n' % sectors_to_gb(min(starting_sectors)))



# plotting R/W percentage pie chart for R/W

items = [read_count, write_count]
my_labels = '#Reads', '#Writes'
plt.pie(items, labels=my_labels, autopct='%1.1f%%')
plt.title('R/W Percentage\n')
plt.axis('equal')
plt.gcf().set_size_inches(20, 10)
plt.savefig('1.png', dpi=300) 
plt.close()


for key in sector_range:
    sector_range[key] = round(sector_range[key] / total_requests * 100, 2)


plt.rcParams.update({'font.size': 15.0, 'font.weight': 'bold'})

plt.bar(list(sector_range.keys()), list(sector_range.values()), color ='grey', width = 0.5)

plt.ylim([0, 100])

for key in sector_range:
    if sector_range[key] != 0:
        plt.text(key, sector_range[key], sector_range[key], ha = 'center', color='red')

plt.xlabel('\nI/O Size (KB)', fontweight='bold')

plt.ylabel('Frequency (%)\n', fontweight='bold')

plt.title('Distribution of I/O Sizes\n', fontweight='bold', fontsize=30.0)


plt.gcf().set_size_inches(20, 10)
plt.savefig('2.png', dpi=300) 
plt.close()

with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H:%M}".format(now)), 'a') as f:
    f.write('\n\t   ***Distribution of I/O Sizes***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' % sector_range['1-4'])
    f.write('\t    [4-8]\t\t    %0.1f\n' % sector_range['4-8'])
    f.write('\t    [8-12]\t\t    %0.1f\n' % sector_range['8-12'])
    f.write('\t    [12-16]\t\t    %0.1f\n' % sector_range['12-16'])
    f.write('\t    [16-20]\t\t    %0.1f\n' % sector_range['16-20'])
    f.write('\t    [20-24]\t\t    %0.1f\n' % sector_range['20-24'])
    f.write('\t    [24-48]\t\t    %0.1f\n' % sector_range['24-48'])
    f.write('\t    [48-64]\t\t    %0.1f\n' % sector_range['48-64'])
    f.write('\t    [64-128]\t\t    %0.1f\n' % sector_range['64-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' % sector_range['>128'])




for key in read_range:
    read_range[key] = round(read_range[key] / total_requests * 100, 2)

for key in write_range:
    write_range[key] = round(write_range[key] / total_requests * 100, 2)

labels = list(read_range.keys())
men_means = list(read_range.values())
women_means = list(write_range.values())

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width, label='Read')
rects2 = ax.bar(x + width/2, women_means, width, label='Write')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Frequency (%)\n', fontweight='bold')
ax.set_xlabel('\nI/O size (KB)', fontweight='bold')
ax.set_title('Distribution of I/O Sizes\n', fontweight='bold', fontsize=30.0)
ax.set_xticks(x, labels)
ax.set_ylim([0, 100])
ax.legend()

ax.bar_label(rects1, padding=3, color='r')
ax.bar_label(rects2, padding=3, color='r')

# fig.tight_layout()

plt.gcf().set_size_inches(20, 10)
plt.savefig('3.png', dpi=300) 
plt.close()

with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H:%M}".format(now)), 'a') as f:
    f.write('\n\t***Distribution of I/O Sizes (READ)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' % read_range['1-4'])
    f.write('\t    [4-8]\t\t    %0.1f\n' % read_range['4-8'])
    f.write('\t    [8-12]\t\t    %0.1f\n' % read_range['8-12'])
    f.write('\t    [12-16]\t\t    %0.1f\n' % read_range['12-16'])
    f.write('\t    [16-20]\t\t    %0.1f\n' % read_range['16-20'])
    f.write('\t    [20-24]\t\t    %0.1f\n' % read_range['20-24'])
    f.write('\t    [24-48]\t\t    %0.1f\n' % read_range['24-48'])
    f.write('\t    [48-64]\t\t    %0.1f\n' % read_range['48-64'])
    f.write('\t    [64-128]\t\t    %0.1f\n' % read_range['64-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' % read_range['>128'])

    f.write('\n\t***Distribution of I/O Sizes (WRITE)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' % write_range['1-4'])
    f.write('\t    [4-8]\t\t    %0.1f\n' % write_range['4-8'])
    f.write('\t    [8-12]\t\t    %0.1f\n' % write_range['8-12'])
    f.write('\t    [12-16]\t\t    %0.1f\n' % write_range['12-16'])
    f.write('\t    [16-20]\t\t    %0.1f\n' % write_range['16-20'])
    f.write('\t    [20-24]\t\t    %0.1f\n' % write_range['20-24'])
    f.write('\t    [24-48]\t\t    %0.1f\n' % write_range['24-48'])
    f.write('\t    [48-64]\t\t    %0.1f\n' % write_range['48-64'])
    f.write('\t    [64-128]\t\t    %0.1f\n' % write_range['64-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' % write_range['>128'])




# reuse distance

reuse_dis_dic = {}   # dictionary of lists >> key shows address and values show reuse distance
reuse_dis_stack = deque()

for item in starting_sectors:
    counter = 0
    temp_list = []
    for i in reuse_dis_stack:
        if i == item:
            while reuse_dis_stack[-1] != item:
                temp_list.append(reuse_dis_stack.pop())
                counter += 1
            reuse_dis_dic[str(item)].append(counter)
            reuse_dis_stack.pop()
            temp_list.reverse()
            for j in temp_list:
                reuse_dis_stack.append(j)
            reuse_dis_stack.append(item)
            break
    if counter == 0:
        reuse_dis_dic[str(item)] = [-1]
        reuse_dis_stack.append(item)
        

print(reuse_dis_dic)






# access frequency of IOs

starting_sectors = sorted(starting_sectors)
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


plt.rcParams.update({'font.size': 10.0, 'font.weight': 'bold'})

plt.bar(list(dic_duplicated.keys()), list(dic_duplicated.values()), color ='grey', width = 0.2)

# plt.ylim([0, 400])
plt.ylim([0, max(dic_duplicated.values()) + 10])

plt.xlabel('\nAddress Range (sector offset)', fontweight='bold', fontsize=20.0)

plt.ylabel('Number of I/O Requests\n', fontweight='bold', fontsize=20.0)

plt.title('Access Frequency of I/Os\n', fontweight='bold', fontsize=30.0)

plt.gcf().set_size_inches(20, 10)
plt.savefig('4.png', dpi=300) 
plt.close()



with open('%s_%s_2.txt' % (app_name, "{:%Y-%m-%d_%H:%M}".format(now)), 'w') as f:
    f.write('\t\t***Access Frequency of I/Os***\n')
    f.write('\tAddress (sector offset)\t\tNumber of I/O Requests\n\t-----------------------\t\t----------------------\n')
    for key in dic_duplicated:
        f.write('\t\t%s\t\t\t\t%d\n' % (key, dic_duplicated[key]))
   


# CDF diagram

dup_range = {
    '1-50': 0,
    '50-100': 0,
    '100-150': 0,
    '150-200': 0,
    '200-250': 0,
    '250-300': 0,
    '>300': 0
}

for key in dic_duplicated:
    if dic_duplicated[key] >= 1 and dic_duplicated[key] < 50:
        dup_range['1-50'] += 1
    elif dic_duplicated[key] >= 50 and dic_duplicated[key] < 100:
        dup_range['50-100'] += 1
    elif dic_duplicated[key] >= 100 and dic_duplicated[key] < 150:
        dup_range['100-150'] += 1
    elif dic_duplicated[key] >= 150 and dic_duplicated[key] < 200:
        dup_range['150-200'] += 1
    elif dic_duplicated[key] >= 200 and dic_duplicated[key] < 250:
        dup_range['200-250'] += 1
    elif dic_duplicated[key] >= 250 and dic_duplicated[key] < 300:
        dup_range['250-300'] += 1
    elif dic_duplicated[key] >= 300:
        dup_range['>300'] += 1


for key in dup_range:
    dup_range[key] = round(dup_range[key] / len(dic_duplicated) * 100, 2)


plt.rcParams.update({'font.size': 15.0, 'font.weight': 'bold'})

plt.bar(list(dup_range.keys()), list(dup_range.values()), color ='grey', width = 0.5)

plt.ylim([0, 100])

for key in dup_range:
    if dup_range[key] != 0:
        plt.text(key, dup_range[key], dup_range[key], ha = 'center', color='red')

plt.xlabel('\nFrequency Range', fontweight='bold')

plt.ylabel('Distribution of Range (%)\n', fontweight='bold')

plt.title('Cumulative Distribution Function (CDF)\n', fontweight='bold', fontsize=30.0)

plt.gcf().set_size_inches(20, 10)
plt.savefig('5.png', dpi=300) 
plt.close()


with open('%s_%s_2.txt' % (app_name, "{:%Y-%m-%d_%H:%M}".format(now)), 'a') as f:
    f.write('\n\t  ***Cumulative Distribution Function (CDF)***\n')
    f.write('\tFrequency Range\t\tDistribution of Range (%)\n\t---------------\t\t-------------------------\n')
    f.write('\t    [1-50]\t\t\t%0.1f\n' % dup_range['1-50'])
    f.write('\t    [50-100]\t\t\t%0.1f\n' % dup_range['50-100'])
    f.write('\t    [100-150]\t\t\t%0.1f\n' % dup_range['100-150'])
    f.write('\t    [150-200]\t\t\t%0.1f\n' % dup_range['150-200'])
    f.write('\t    [200-250]\t\t\t%0.1f\n' % dup_range['200-250'])
    f.write('\t    [250-300]\t\t\t%0.1f\n' % dup_range['250-300'])
    f.write('\t    [>300]\t\t\t%0.1f\n' % dup_range['>300'])





with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H:%M}".format(now)), 'r+') as f: s = f.read(); f.seek(0); f.write('*** Total execution time: %0.2f seconds ***\n' % round(time.time() - start_time, 2) + s)