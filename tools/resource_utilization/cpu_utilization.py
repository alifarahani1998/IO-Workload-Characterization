import matplotlib.pyplot as plt
import numpy as np
import os


# cpu utilization diagram

def cpu_utilization(iostat_file, min_hour, interval):

    print('Generating CPU utilization diagram ...')

    cpu_util = []


    file = open('%s' %iostat_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'user' in line:
            cpu_util.append(float((lines[i+1].split())[0]))


    avg_cpu_util = round(sum(cpu_util) / len(cpu_util), 2)

    max_cpu_util = max(cpu_util)
    min_cpu_util = min(cpu_util)

    idx = []

    if min_hour == 'h':
        for i in range(len(cpu_util)):
            if i % (interval*60) == 0:
                idx.append(i)
    else:
        for i in range(len(cpu_util)):
            if i % interval == 0:
                idx.append(i)

    new_cpu_util = []

    for i, item in enumerate(cpu_util):
        if i in idx:
            new_cpu_util.append(item)

    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig, ax = plt.subplots()
    ax.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax.set_ylabel('Utilization (%)', fontweight='bold', fontsize=20.0)
    ax.set_title('CPU Utilization', fontweight='bold', fontsize=20.0)

    x = []
    for i in range(len(new_cpu_util)):
        x.append(i*interval)

    y = new_cpu_util
    ax.set_ylim([0, 100])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. CPU Util.: %1.1f' %avg_cpu_util + '%',
        'MAX CPU Util.: %1.1f' %max_cpu_util + '%',
        'MIN CPU Util.: %1.1f' %min_cpu_util + '%'
    ))

    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.xticks(rotation=45)
    plt.xticks(np.arange(0, max(x)+1, interval))
    plt.plot(x, y, 'orange')
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/cpu_util.png', dpi=60) 
    plt.close()

