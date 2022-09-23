import matplotlib.pyplot as plt
import numpy as np
import os


if not os.path.exists('../../results'):
    os.mkdir('../../results')
    os.mkdir('../../results/diagram_results')
elif not os.path.exists('../../results/diagram_results'):
    os.mkdir('../../results/diagram_results')


# io bandwidth diagram

def draw_io_bandwidth(iostat_file, min_hour, interval):
    print('Generating I/O bandwidth diagram ...')


    read_list = []
    write_list = []


    file = open('%s' %iostat_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'rMB/s' in line:
            read_list.append(float((lines[i+1].split())[2]))
        if 'wMB/s' in line:
            write_list.append(float((lines[i+1].split())[8]))


    avg_read = round(sum(read_list) / len(read_list), 2)
    avg_write = round(sum(write_list) / len(write_list), 2)

    read_max = max(read_list)
    write_max = max(write_list)

    idx = []

    if min_hour == 'h':
        for i in range(len(read_list)):
            if i % (interval*60) == 0:
                idx.append(i)
    else:
        for i in range(len(read_list)):
            if i % interval == 0:
                idx.append(i)

    new_read_list = []
    new_write_list = []

    for i, item in enumerate(read_list):
        if i in idx:
            new_read_list.append(item)

    for i, item in enumerate(write_list):
        if i in idx:
            new_write_list.append(item)


    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig, ax = plt.subplots()
    ax.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax.set_ylabel('Bandwidth (MB/s)', fontweight='bold', fontsize=20.0)
    ax.set_title('Distribution of I/O Bandwidth', fontweight='bold', fontsize=20.0)

    x = []
    for i in range(len(new_read_list)):
        x.append(i*interval)

    y = new_write_list
    z = new_read_list
    ax.set_ylim([0, max(read_max, write_max) + 20])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. Read: %1.1f MB/s' %avg_read,
        'Avg. Write: %1.1f MB/s' %avg_write
    ))

    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.xticks(rotation=45)
    plt.xticks(np.arange(0, max(x)+1, interval))
    plt.plot(x, z, linestyle="-", marker="o", label="Read")
    plt.plot(x, y, linestyle="-", marker="o", label="Write")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/io_bandwidth.png', dpi=60) 
    plt.close()



# disk utilization diagram

def disk_utilization(iostat_file, min_hour, interval):
    print('Generating disk utilization diagram ...')

    disk_util = []


    file = open('%s' %iostat_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'util' in line:
            disk_util.append(float((lines[i+1].split())[20]))

    avg_disk_util = round(sum(disk_util) / len(disk_util), 2)

    max_disk_util = max(disk_util)
    min_disk_util = min(disk_util)

    idx = []

    if min_hour == 'h':
        for i in range(len(disk_util)):
            if i % (interval*60) == 0:
                idx.append(i)
    else:
        for i in range(len(disk_util)):
            if i % interval == 0:
                idx.append(i)

    new_disk_util = []

    for i, item in enumerate(disk_util):
        if i in idx:
            new_disk_util.append(item)


    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig, ax = plt.subplots()
    ax.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax.set_ylabel('Utilization (%)', fontweight='bold', fontsize=20.0)
    ax.set_title('Disk Utilization', fontweight='bold', fontsize=20.0)

    x = []
    for i in range(len(new_disk_util)):
        x.append(i*interval)

    y = new_disk_util
    ax.set_ylim([0, 100])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. Disk Util.: %1.1f' %avg_disk_util + '%',
        'MAX Disk Util.: %1.1f' %max_disk_util + '%',
        'MIN Disk Util.: %1.1f' %min_disk_util + '%'
    ))

    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.xticks(rotation=45)
    plt.xticks(np.arange(0, max(x)+1, interval))
    plt.plot(x, y)
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/disk_util.png', dpi=60) 
    plt.close()
