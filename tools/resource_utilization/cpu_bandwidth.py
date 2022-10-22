import matplotlib.pyplot as plt
import numpy as np


# cpu utilization diagram

def cpu_bandwidth(iostat_file, min_hour, interval):

    print('Generating CPU/Bandwidth diagram ...')

    cpu_util = []
    read_list = []
    write_list = []


    file = open('%s' %iostat_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'user' in line:
            cpu_util.append(float((lines[i+1].split())[0]))
        if 'rMB/s' in line:
            read_list.append(float((lines[i+1].split())[2]))
        if 'wMB/s' in line:
            write_list.append(float((lines[i+1].split())[8]))


    avg_cpu_util = round(sum(cpu_util) / len(cpu_util), 2)
    avg_read = round(sum(read_list) / len(read_list), 2)
    avg_write = round(sum(write_list) / len(write_list), 2)

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
    new_read_list = []
    new_write_list = []

    for i, item in enumerate(cpu_util):
        if i in idx:
            new_cpu_util.append(item)

    for i, item in enumerate(read_list):
        if i in idx:
            new_read_list.append(item)

    for i, item in enumerate(write_list):
        if i in idx:
            new_write_list.append(item)

    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax1.set_ylabel('CPU Utilization (%)', fontweight='bold', fontsize=20.0)
    ax1.set_ylim([0, 100])

    x = []
    for i in range(len(new_cpu_util)):
        x.append(i*interval)

    y = new_cpu_util
    v = new_write_list
    z = new_read_list
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('\nI/O Bandwidth (MB/s)', fontweight='bold', fontsize=20.0)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. CPU Util.: %1.1f' %avg_cpu_util + '%',
        'Avg. Read: %1.1f MB/s' %avg_read,
        'Avg. Write: %1.1f MB/s' %avg_write
    ))


    ax2.text(0.05, 0.95, textstr, transform=ax2.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    ax1.tick_params(axis='x', labelrotation = 45)
    plt.xticks(np.arange(0, max(x)+1, interval))
    plt.plot(x, y, linestyle="-", marker="o", label="CPU")
    plt.plot(x, z, linestyle="-", marker="o", label="Read")
    plt.plot(x, v, linestyle="-", marker="o", label="Write")
    plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol=3)
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/cpu_bandwidth.png', dpi=60) 
    plt.close()
