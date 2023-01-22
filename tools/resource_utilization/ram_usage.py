import matplotlib.pyplot as plt
import numpy as np


# RAM usage diagram

def ram_usage(ram_usage_file, min_hour, interval):

    print('Generating RAM usage diagram ...')

    ram_usage = []


    file = open('%s' %ram_usage_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'Mem' in line:
            total_ram = float((lines[i].split())[1].removesuffix('Gi'))
            if 'Mi' in (lines[i].split())[2]:
                ram_usage.append(float((lines[i].split())[2].removesuffix('Mi')))
            else:
                ram_usage.append(float((lines[i].split())[2].removesuffix('Gi')))


    avg_ram_usage = round(sum(ram_usage) / len(ram_usage), 2)

    max_ram_usage = max(ram_usage)
    min_ram_usage = min(ram_usage)

    idx = []

    if min_hour == 'h':
        for i in range(len(ram_usage)):
            if i % (interval*60) == 0:
                idx.append(i)
    else:
        for i in range(len(ram_usage)):
            if i % interval == 0:
                idx.append(i)

    new_ram_usage = []

    for i, item in enumerate(ram_usage):
        if i in idx:
            new_ram_usage.append(item)

    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig, ax = plt.subplots()
    ax.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax.set_ylabel('RAM Usage (GB)', fontweight='bold', fontsize=20.0)
    ax.set_title('RAM Usage (Total RAM = %sGB)' %total_ram, fontweight='bold', fontsize=20.0)

    x = []
    for i in range(len(new_ram_usage)):
        x.append(i*interval)

    y = new_ram_usage
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. RAM Usage: %1.1fGB' %avg_ram_usage + '%',
        'MAX RAM Usage: %1.1fGB' %max_ram_usage + '%',
        'MIN RAM Usage: %1.1fGB' %min_ram_usage + '%',
    ))

    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.xticks(rotation=45)
    plt.xticks(np.arange(0, max(x)+1, interval))
    plt.plot(x, y, 'red')
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/ram_usage.png', dpi=60) 
    plt.close()

