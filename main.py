import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime
import re
# from collections import deque
from pygooglechart import PieChart3D


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

with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'w') as f:
    f.write('Number of READs: %d\n\n' % read_count)
    f.write('Number of WRITEs: %d\n\n' % write_count)
    f.write('READ size: %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' % (read_sectors, sectors_to_kb(read_sectors), sectors_to_mb(read_sectors), sectors_to_gb(read_sectors), sectors_to_tb(read_sectors)))
    f.write('WRITE size: %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' % (write_sectors, sectors_to_kb(write_sectors), sectors_to_mb(write_sectors), sectors_to_gb(write_sectors), sectors_to_tb(write_sectors)))
    f.write('Total size of requested sectors (READ + WRITE): %d sectors (%0.1f KB) (%0.1f MB) (%0.1f GB) (%0.1f TB)\n\n' % (read_sectors+write_sectors, sectors_to_kb(read_sectors+write_sectors), sectors_to_mb(read_sectors+write_sectors), sectors_to_gb(read_sectors+write_sectors), sectors_to_tb(read_sectors+write_sectors)))
    f.write('READ percentage: {:.1%}\n\n'.format(read_count / total_requests))
    f.write('WRITE percentage: {:.1%}\n\n'.format(write_count / total_requests))

    if read_count != 0:
        f.write('Average READ size: %0.1f KB\n\n' % sectors_to_kb(read_sectors / read_count))
    else:
        f.write('Average READ size: 0 KB\n\n')


    if write_count != 0:
        f.write('Average WRITE size: %0.1f KB\n\n' % sectors_to_kb(write_sectors / write_count))
    else:
        f.write('Average WRITE size: 0 KB\n\n')

    f.write('Maximum requested address (sector offset): %d GB\n\n' % sectors_to_gb(max(starting_sectors)))
    f.write('Minimum requested address (sector offset): %d GB\n\n' % sectors_to_gb(min(starting_sectors)))



# Pie chart
labels = ['Read', 'Write']
sizes = [read_count, write_count]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 20}, colors=['#0000ff', '#ff0000'])

# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')
plt.tight_layout()
plt.gcf().set_size_inches(12, 6)
plt.savefig('2d_pie.png', dpi=60) 
plt.close()



# 3d pie chart

chart = PieChart3D(600, 300)

chart.add_data([read_count, write_count])

chart.set_colours(['1e12c4', 'db2121'])
chart.title = 'Read/Write Percentage'

chart.set_pie_labels(['Read: {:.1%}'.format(read_count / total_requests), 'Write: {:.1%}'.format(write_count / total_requests)])
chart.set_title_style(font_size=20)
chart.download('3d_pie.png')


for key in sector_range:
    sector_range[key] = round(sector_range[key] / total_requests * 100, 1)



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
plt.savefig('mixed_rw_bar.png', dpi=60) 
plt.close()



with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
    f.write('\n***Distribution of I/O Requests (total R/W)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' % sector_range['1-4'])
    f.write('\t    [5-8]\t\t    %0.1f\n' % sector_range['5-8'])
    f.write('\t    [9-12]\t\t    %0.1f\n' % sector_range['9-12'])
    f.write('\t    [13-16]\t\t    %0.1f\n' % sector_range['13-16'])
    f.write('\t    [17-20]\t\t    %0.1f\n' % sector_range['17-20'])
    f.write('\t    [21-24]\t\t    %0.1f\n' % sector_range['21-24'])
    f.write('\t    [25-48]\t\t    %0.1f\n' % sector_range['25-48'])
    f.write('\t    [49-64]\t\t    %0.1f\n' % sector_range['49-64'])
    f.write('\t    [65-128]\t\t    %0.1f\n' % sector_range['65-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' % sector_range['>128'])



for key in read_range:
    read_range[key] = round(read_range[key] / total_requests * 100, 1)

for key in write_range:
    write_range[key] = round(write_range[key] / total_requests * 100, 1)



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
plt.savefig('separated_rw_bar.png', dpi=60) 
plt.close()




with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
    f.write('\n\n***Distribution of I/O Requests (READ)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' % read_range['1-4'])
    f.write('\t    [5-8]\t\t    %0.1f\n' % read_range['5-8'])
    f.write('\t    [9-12]\t\t    %0.1f\n' % read_range['9-12'])
    f.write('\t    [13-16]\t\t    %0.1f\n' % read_range['13-16'])
    f.write('\t    [17-20]\t\t    %0.1f\n' % read_range['17-20'])
    f.write('\t    [21-24]\t\t    %0.1f\n' % read_range['21-24'])
    f.write('\t    [25-48]\t\t    %0.1f\n' % read_range['25-48'])
    f.write('\t    [49-64]\t\t    %0.1f\n' % read_range['49-64'])
    f.write('\t    [65-128]\t\t    %0.1f\n' % read_range['65-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' % read_range['>128'])

    f.write('\n\n***Distribution of I/O Requests (WRITE)***\n')
    f.write('\tI/O Size (KB)\t\tFrequency (%)\n\t-------------\t\t-------------\n')
    f.write('\t    [1-4]\t\t    %0.1f\n' % write_range['1-4'])
    f.write('\t    [5-8]\t\t    %0.1f\n' % write_range['5-8'])
    f.write('\t    [9-12]\t\t    %0.1f\n' % write_range['9-12'])
    f.write('\t    [13-16]\t\t    %0.1f\n' % write_range['13-16'])
    f.write('\t    [17-20]\t\t    %0.1f\n' % write_range['17-20'])
    f.write('\t    [21-24]\t\t    %0.1f\n' % write_range['21-24'])
    f.write('\t    [25-48]\t\t    %0.1f\n' % write_range['25-48'])
    f.write('\t    [49-64]\t\t    %0.1f\n' % write_range['49-64'])
    f.write('\t    [65-128]\t\t    %0.1f\n' % write_range['65-128'])
    f.write('\t    [>128]\t\t    %0.1f\n' % write_range['>128'])




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
        

# print(reuse_dis_dic)






# access frequency of IOs

starting_sectors = sorted(starting_sectors)
dic_duplicated = {}
empty_list = []
for item in starting_sectors:
    if not item in dic_duplicated:
        dic_duplicated[item] = 1
    else:
        dic_duplicated[item] += 1
    empty_list.append(' ')

dic_duplicated = {str(key): value for key, value in dic_duplicated.items()}



with open('%s_%s_2.txt' % (app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'w') as f:
    f.write('\t\t***Access Frequency of I/Os***\n')
    f.write('\tAddress (sector offset)\t\tNumber of I/O Requests\n\t-----------------------\t\t----------------------\n')
    for key in dic_duplicated:
        f.write('\t\t%s\t\t\t\t%d\n' % (key, dic_duplicated[key]))
   


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


    with open('%s_%s_2.txt' % (app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'a') as f:
        f.write('\n\n\t  ***Cumulative Distribution Function (CDF)***\n')
        f.write('\tFrequency Range\t\tDistribution of Range (%)\n\t---------------\t\t-------------------------\n')
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %(s, s+i, dup_range['%d-%d' %(s, s+i)]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+i+1), (s+2*i+1), dup_range['%d-%d' %((s+i+1), (s+2*i+1))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+2*i+2), (s+3*i+2), dup_range['%d-%d' %((s+2*i+2), (s+3*i+2))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+3*i+3), (s+4*i+3), dup_range['%d-%d' %((s+3*i+3), (s+4*i+3))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+4*i+4), (s+5*i+4), dup_range['%d-%d' %((s+4*i+4), (s+5*i+4))]))
        f.write('\t    [%d-%d]\t\t\t%0.1f\n' %((s+5*i+5), e, dup_range['%d-%d' %((s+5*i+5), e)]))
        f.write('\t    [>%d]\t\t\t%0.1f\n\n\n\n' %(e, dup_range['>%d' %e]))


    plt.rcParams.update({'font.size': 15.0, 'font.weight': 'bold'})

    plt.bar(list(dup_range.keys()), list(dup_range.values()), color ='navy', width = 0.5)

    plt.ylim([0, 100])

    for key in dup_range:
        if dup_range[key] != 0:
            plt.text(key, dup_range[key], dup_range[key], ha = 'center', color='red')

    plt.xlabel('\nFrequency Range', fontweight='bold', fontsize=20.0)

    plt.ylabel('Distribution of Range (%)\n', fontweight='bold', fontsize=20.0)

    plt.title('Cumulative Distribution Function (CDF)\n', fontweight='bold', fontsize=20.0)
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('%d_cdf.png' % fn, dpi=60) 
    plt.close()

    for key in dup_range:
        if dup_range[key] >= 50:
            splitted = key.split('-')
            cdf_freq_range(fn + 1, int(splitted[0]), int(splitted[1]), (int(splitted[1])/5)-1)

cdf_freq_range(1, 1, 300, 49)



plt.rcParams.update({'font.size': 15.0, 'font.weight': 'bold'})

plt.bar(list(dic_duplicated.keys()), list(dic_duplicated.values()), color ='black', width = 0.2)

plt.ylim([0, max(dic_duplicated.values())])

plt.xlabel('Address Range (sector offset)', fontweight='bold', fontsize=20.0)

plt.ylabel('Number of I/O Requests', fontweight='bold', fontsize=20.0)

plt.title('Access Frequency of I/Os', fontweight='bold', fontsize=20.0)
plt.tight_layout()
plt.gcf().set_size_inches(12, 6)
plt.savefig('access_freq.png', dpi=60) 
plt.close()



with open('%s_%s_1.txt' % (app_name, "{:%Y-%m-%d_%H-%M}".format(now)), 'r+') as f: s = f.read(); f.seek(0); f.write('*** Total execution time: %0.1f seconds ***\n\n' % round(time.time() - start_time, 2) + s)
