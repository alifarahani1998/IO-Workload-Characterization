import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import time


trace_file = input('Enter trace file path: ')
runtime = input('Enter application runtime in minutes: ')

start_time = time.time()

print('Retrieving data ...')

file = open('%s' %trace_file, 'r')
line = file.readline()

if 'maj/min' not in line:
    with open('%s' %trace_file, 'r+') as f: s = f.read(); f.seek(0); f.write('  maj/min cpu #seq time pid event R/W start_sector + #sectors pname\n' + s)

df = pd.read_table('%s' %trace_file, header=0, usecols=['time', 'start_sector', '#sectors'], delim_whitespace=True, dtype=str, na_filter=False)


print('Processing ...')

def sector_to_block(value):
    return (value/8)

def nsec_to_min(value):
    return (value/60)


for index in df.index:
    if nsec_to_min(float(df['time'][index])) < float(runtime) and df['#sectors'][index] != '' and not re.match('^.*[a-zA-Z]+.*', df['#sectors'][index]):
        x = np.array([nsec_to_min(float(df['time'][index]))])
        y = np.array([sector_to_block(int(df['start_sector'][index]))])
        plt.scatter(x, y, color='red')

plt.ylim([0, 500000000])
plt.title('Accessed Locations of Disk', fontweight='bold', fontsize=20.0)
plt.xlabel('Time (m)', fontweight='bold', fontsize=15.0)
plt.ylabel('Logical Block Address (4KB)', fontweight='bold', fontsize=15.0)
plt.savefig('../result/access_freq.png')

print('Total execution time: %0.1f seconds' %round(time.time() - start_time, 2))
