import matplotlib.pyplot as plt
import numpy as np


# IOPS diagram

def iops(iostat_file, min_hour, interval):
    print('Generating IOPS diagram ...')

    total_iops = []
    read_iops = []
    write_iops = []


    file = open('%s' %iostat_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'r/s' in line:
            read_iops.append(float((lines[i+1].split())[1]))
            write_iops.append(float((lines[i+1].split())[7]))
            total_iops.append(float((lines[i+1].split())[1]) + float((lines[i+1].split())[7]))
        


    avg_total_iops = round(sum(total_iops) / len(total_iops), 2)
    avg_read_iops = round(sum(read_iops) / len(read_iops), 2)
    avg_write_iops = round(sum(write_iops) / len(write_iops), 2)

    idx = []

    if min_hour == 'h':
        for i in range(len(read_iops)):
            if i % (interval*60) == 0:
                idx.append(i)
    else:
        for i in range(len(read_iops)):
            if i % interval == 0:
                idx.append(i)

    new_total_iops = []
    new_read_iops = []
    new_write_iops = []

    for i, item in enumerate(total_iops):
        if i in idx:
            new_total_iops.append(item)
    
    for i, item in enumerate(read_iops):
        if i in idx:
            new_read_iops.append(item)

    for i, item in enumerate(write_iops):
        if i in idx:
            new_write_iops.append(item)


    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig, ax = plt.subplots()
    ax.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax.set_ylabel('IOPS', fontweight='bold', fontsize=20.0)
    ax.set_title('Input/Output Operations per Second (IOPS)', fontweight='bold', fontsize=20.0)

    x = []
    for i in range(len(new_read_iops)):
        x.append(i*interval)

    m = new_total_iops
    y = new_write_iops
    z = new_read_iops
    
    ax.set_ylim([0, max(new_total_iops) + 5])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. Total IOPS: %1.1f' %avg_total_iops,
        'Avg. Read IOPS: %1.1f' %avg_read_iops,
        'Avg. Write IOPS: %1.1f' %avg_write_iops
    ))

    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.xticks(rotation=45)
    plt.xticks(np.arange(0, max(x)+1, interval))
    plt.plot(x, m, linestyle="-", marker="o", label="Total R/W")
    plt.plot(x, z, linestyle="-", marker="o", label="Read")
    plt.plot(x, y, linestyle="-", marker="o", label="Write")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/iops.png', dpi=60) 
    plt.close()
