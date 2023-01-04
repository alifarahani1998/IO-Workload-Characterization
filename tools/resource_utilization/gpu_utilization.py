import matplotlib.pyplot as plt
import numpy as np


# gpu utilization diagram

def gpu_utilization(gpustat_file, min_hour, interval):

    print('Generating GPU utilization diagram ...')

    gpu_util = []


    file = open('%s' %gpustat_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'NVIDIA' in line:
            gpu_util.append(float((lines[i].split())[8]))


    avg_gpu_util = round(sum(gpu_util) / len(gpu_util), 2)

    max_gpu_util = max(gpu_util)
    min_gpu_util = min(gpu_util)

    idx = []

    if min_hour == 'h':
        for i in range(len(gpu_util)):
            if i % (interval*60) == 0:
                idx.append(i)
    else:
        for i in range(len(gpu_util)):
            if i % interval == 0:
                idx.append(i)

    new_gpu_util = []

    for i, item in enumerate(gpu_util):
        if i in idx:
            new_gpu_util.append(item)

    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig, ax = plt.subplots()
    ax.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax.set_ylabel('Utilization (%)', fontweight='bold', fontsize=20.0)
    ax.set_title('GPU Utilization', fontweight='bold', fontsize=20.0)

    x = []
    for i in range(len(new_gpu_util)):
        x.append(i*interval)

    y = new_gpu_util
    ax.set_ylim([0, 100])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. GPU Util.: %1.1f' %avg_gpu_util + '%',
        'MAX GPU Util.: %1.1f' %max_gpu_util + '%',
        'MIN GPU Util.: %1.1f' %min_gpu_util + '%'
    ))

    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)

    plt.xticks(rotation=45)
    plt.xticks(np.arange(0, max(x)+1, interval))
    plt.plot(x, y, 'red')
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/gpu_util.png', dpi=60) 
    plt.close()

