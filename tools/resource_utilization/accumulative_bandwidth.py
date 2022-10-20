from pickletools import markobject
import matplotlib.pyplot as plt
import numpy as np
import os
import time

iostat_files = []
num_iostat_files = input('Enter number of iostat files: ')

for i in range(int(num_iostat_files)):
    path = input('Enter iostat_%d file path: ' %(i+1))
    name = input('Enter traced application name: ')
    iostat_files.append({'path': path, 'name': name})
    
start_time = time.time()

if not os.path.exists('../../results'):
    os.mkdir('../../results')
    os.mkdir('../../results/diagram_results')
elif not os.path.exists('../../results/diagram_results'):
    os.mkdir('../../results/diagram_results')

read_list = []
write_list = []

app_name = []
avg_read = []
avg_write = []

for i in range(len(iostat_files)):
    app_name.append(iostat_files[i]['name'])
    file = open('%s' %iostat_files[i]['path'], 'r')
    lines = file.readlines()
    for j, line in enumerate(lines):
        if 'rMB/s' in line:
            read_list.append(float((lines[j+1].split())[2]))
        if 'wMB/s' in line:
            write_list.append(float((lines[j+1].split())[8]))
    avg_read.append(round(sum(read_list) / len(read_list), 2))
    avg_write.append(round(sum(write_list) / len(write_list), 2))
    read_list.clear()
    write_list.clear()


x = np.arange(len(app_name))  # the label locations
width = 0.4  # the width of the bars
plt.rcParams.update({'font.size': 12.0, 'font.weight': 'bold'})
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, avg_read, width, label='Read', color='navy')
rects2 = ax.bar(x + width/2, avg_write, width, label='Write', color='orange')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Avg. Bandwidth (MB/s)', fontweight='bold', fontsize=15.0)
ax.set_xlabel('Workload', fontweight='bold', fontsize=15.0)
ax.set_title('Accumulative I/O Bandwidth', fontweight='bold', fontsize=15.0)
ax.set_xticks(x, app_name)
ax.set_ylim([0, max(max(avg_read), max(avg_write)) + 5])
plt.xticks(rotation=45)
ax.legend()

ax.bar_label(rects1, padding=3, fmt='%g ', color='navy')
ax.bar_label(rects2, padding=3, fmt=' %g', color='orange')

fig.tight_layout()

plt.gcf().set_size_inches(12, 6)
plt.savefig('../../results/diagram_results/accumulative_bandwidth.png', dpi=60) 
plt.close()


print('Total execution time: %0.1f seconds' %round(time.time() - start_time, 2))
