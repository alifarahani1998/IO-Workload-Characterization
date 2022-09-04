import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import re
# from collections import deque
from pygooglechart import PieChart3D


input_file = input('Enter the name of trace (input) file: ')
start_time = time.time()

print('Retrieving data ...')


df = pd.read_table('%s' % input_file, header=0, usecols=['R/W', 'start_sector', '#sectors'], delim_whitespace=True, dtype=str, na_filter=False)


total_requests = 0
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


# size of individual IOs

for index in df.index:
        
    if df['#sectors'][index] != '' and not re.match('^.*[a-zA-Z]+.*', df['#sectors'][index]):

        temp = sectors_to_kb(int(df['#sectors'][index]))

        total_requests += 1

        if 'R' in df['R/W'][index]:
            read_count += 1
            read_range[compare_size(temp)] += 1
        elif 'W' in df['R/W'][index]:
            write_count += 1
            write_range[compare_size(temp)] += 1
        
        sector_range[compare_size(temp)] += 1
         


starting_sectors = list(df['start_sector'])


for item in list(starting_sectors):
    if item == '0' or item == '' or re.match('^.*[a-zA-Z]+.*', item) or '[' in item:
        starting_sectors.remove(item)

starting_sectors = [int(i) for i in starting_sectors]

print('Generating 2D pie diagram ...')

# Pie chart
labels = ['Read', 'Write']
sizes = [read_count, write_count]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 20}, colors=['#0000ff', '#ff0000'])

# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')
plt.tight_layout()
plt.gcf().set_size_inches(12, 6)
plt.savefig('../results/diagram_results/2d_pie.png', dpi=60) 
plt.close()

print('Generating 3D pie diagram ...')

# 3d pie chart

chart = PieChart3D(600, 300)

chart.add_data([read_count, write_count])

chart.set_colours(['1e12c4', 'db2121'])
chart.title = 'Read/Write Percentage'

chart.set_pie_labels(['Read: {:.1%}'.format(read_count / total_requests), 'Write: {:.1%}'.format(write_count / total_requests)])
chart.set_title_style(font_size=20)
chart.download('../results/diagram_results/3d_pie.png')


for key in sector_range:
    sector_range[key] = round(sector_range[key] / total_requests * 100, 1)


print('Generating mixed_rw_bar diagram ...')

# Mixed R/W IO sizes diagram

plt.rcParams.update({'font.size': 15.0, 'font.weight': 'bold'})
plt.rcParams['figure.figsize'] = [12, 6]

plt.bar(list(sector_range.keys()), list(sector_range.values()), color ='navy', width = 0.5)

plt.ylim([0, 100])

for key in sector_range:
    if sector_range[key] != 0:
        plt.text(key, sector_range[key], sector_range[key], ha = 'center', color='red')

plt.xlabel('I/O Size (KB)', fontweight='bold', fontsize=20.0)

plt.ylabel('Frequency (%)', fontweight='bold', fontsize=20.0)

plt.title('Distribution of I/O Sizes', fontweight='bold', fontsize=20.0)

plt.tight_layout()
plt.savefig('../results/diagram_results/mixed_rw_bar.png', dpi=60) 
plt.close()



for key in read_range:
    read_range[key] = round(read_range[key] / total_requests * 100, 1)

for key in write_range:
    write_range[key] = round(write_range[key] / total_requests * 100, 1)

print('Generating separated_rw_bar diagram ...')

# separated R/W IO sizes diagram

labels = list(read_range.keys())
read_means = list(read_range.values())
write_means = list(write_range.values())

x = np.arange(len(labels))  # the label locations
width = 0.4  # the width of the bars
plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, read_means, width, label='READ', color='navy')
rects2 = ax.bar(x + width/2, write_means, width, label='WRITE', color='orange')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Frequency (%)', fontweight='bold', fontsize=20.0)
ax.set_xlabel('I/O Size (KB)', fontweight='bold', fontsize=20.0)
ax.set_title('Distribution of I/O Sizes', fontweight='bold', fontsize=20.0)
ax.set_xticks(x, labels)
ax.set_ylim([0, 100])
ax.legend()

ax.bar_label(rects1, padding=3, fmt='%g ', color='navy')
ax.bar_label(rects2, padding=3, fmt=' %g', color='orange')

fig.tight_layout()

plt.gcf().set_size_inches(12, 6)
plt.savefig('../results/diagram_results/separated_rw_bar.png', dpi=60) 
plt.close()



# access frequency of IOs

starting_sectors = sorted(starting_sectors)
dic_duplicated = {}

for item in starting_sectors:
    if not item in dic_duplicated:
        dic_duplicated[item] = 1
    else:
        dic_duplicated[item] += 1

dic_duplicated = {str(key): value for key, value in dic_duplicated.items()}



# CDF diagram


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


    plt.rcParams.update({'font.size': 15.0, 'font.weight': 'bold'})

    plt.bar(list(dup_range.keys()), list(dup_range.values()), color ='navy', width = 0.5)

    plt.ylim([0, 100])

    for key in dup_range:
        if dup_range[key] != 0:
            plt.text(key, dup_range[key], dup_range[key], ha = 'center', color='red')

    plt.xlabel('Frequency Range', fontweight='bold', fontsize=20.0)

    plt.ylabel('Distribution of Range (%)', fontweight='bold', fontsize=20.0)

    plt.title('Cumulative Distribution Function (CDF)', fontweight='bold', fontsize=20.0)
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../results/diagram_results/cdf_%d.png' % fn, dpi=60) 
    plt.close()

    for key in dup_range:
        if dup_range[key] >= 50:
            splitted = key.split('-')
            cdf_freq_range(fn + 1, int(splitted[0]), int(splitted[1]), (int(splitted[1])/5)-1)

print('Generating cdf diagrams ...')

cdf_freq_range(1, 1, 300, 49)


print('Generating access_freq diagram ...')

# access frequency (TWSD) diagram

plt.rcParams.update({'font.size': 15.0, 'font.weight': 'bold'})

plt.bar(list(dic_duplicated.keys()), list(dic_duplicated.values()), color ='black', width = 0.2)

plt.ylim([0, max(dic_duplicated.values())])

plt.xlabel('Address Range (sector offset)', fontweight='bold', fontsize=20.0)

plt.ylabel('Number of I/O Requests', fontweight='bold', fontsize=20.0)


plt.title('Access Frequency of I/Os', fontweight='bold', fontsize=20.0)
plt.tight_layout()
plt.xticks([])
plt.gcf().set_size_inches(12, 6)
plt.savefig('../results/diagram_results/access_freq.png', dpi=60) 
plt.close()


print('Total execution time: %0.1f seconds: ' % round(time.time() - start_time, 2))
