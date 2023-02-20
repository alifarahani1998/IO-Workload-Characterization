import matplotlib.pyplot as plt


def cpu_gpu_disk(iostat_file, gpustat_file, min_hour, interval):

    print('Generating CPU/GPU/Disk Util diagram ...')

    cpu_util = []
    gpu_util = []
    disk_util = []


    file = open('%s' %iostat_file, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if 'user' in line:
            cpu_util.append(float((lines[i+1].split())[0]))
        if 'util' in line:
            disk_util.append(float((lines[i+1].split())[20]))
    
    new_file = open('%s' %gpustat_file, 'r')
    new_lines = new_file.readlines()
    for i, line in enumerate(new_lines):
        if 'NVIDIA' in line:
            gpu_util.append(float((new_lines[i].split())[8]))


    avg_cpu_util = round(sum(cpu_util) / len(cpu_util), 2)
    avg_gpu_util = round(sum(gpu_util) / len(gpu_util), 2)
    avg_disk_util = round(sum(disk_util) / len(disk_util), 2)

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
    new_gpu_util = []
    new_disk_util = []

    for i, item in enumerate(cpu_util):
        if i in idx:
            new_cpu_util.append(item)

    for i, item in enumerate(gpu_util):
        if i in idx:
            new_gpu_util.append(item)

    for i, item in enumerate(disk_util):
        if i in idx:
            new_disk_util.append(item)

    if len(new_gpu_util) > len(new_cpu_util):
        dif = len(new_gpu_util) - len(new_cpu_util)
        for i in range(dif):
            new_gpu_util.pop()
    elif len(new_cpu_util) > len(new_gpu_util):
        dif = len(new_cpu_util) - len(new_gpu_util)
        for i in range(dif):
            new_cpu_util.pop()
            new_disk_util.pop()

    x = []
    for i in range(len(new_cpu_util)):
        x.append(i*interval)

    y = new_cpu_util
    v = new_disk_util
    z = new_gpu_util

    plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

    fig = plt.figure()
 
    ax = fig.add_subplot(111)
    lns1 = ax.plot(x, v, '-', marker='o', label='Disk', color='red')
    lns2 = ax.plot(x, z, '-', marker='o', label='GPU', color='green')
    lns3 = ax.plot(x, y, '-', marker='o', label='CPU', color='blue')
    
    lns = lns1+lns2+lns3
    labs = [l.get_label() for l in lns]

    

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    textstr = '\n'.join((
        'Avg. CPU Util.: %1.1f' %avg_cpu_util + '%',
        'Avg. GPU Util.: %1.1f ' %avg_gpu_util + '%',
        'Avg. Disk Util.: %1.1f ' %avg_disk_util + '%'
    ))
    
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    ax.set_xlabel('Time (%s)' %min_hour, fontweight='bold', fontsize=20.0)
    ax.set_ylabel('Utilization (%)', fontweight='bold', fontsize=20.0)
    ax.tick_params(axis='x', labelrotation = 45)
    ax.set_ylim(0, max(max(new_gpu_util), max(new_disk_util), max(new_cpu_util)) + 5)
    ax.legend(lns, labs, loc='upper right')
    plt.tight_layout()
    plt.gcf().set_size_inches(12, 6)
    plt.savefig('../../results/diagram_results/cpu_gpu_disk.png', dpi=60) 
    plt.close()
