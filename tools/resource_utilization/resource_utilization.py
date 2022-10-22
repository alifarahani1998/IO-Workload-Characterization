import time
import os
import disk_utilization as disk
import cpu_utilization as cpu
import gpu_utilization as gpu
import cpu_bandwidth as cb


iostat_file = input('Enter iostat file path: ')
gpustat_file = input('Enter gpustat file path (if not desired, type no): ')
min_hour_input = input('Enter time format (h/m): ')
if min_hour_input == 'h':
    min_hour_input = 'h'
    interval_input = input('Enter hour interval: ')
elif min_hour_input == 'm':
    min_hour_input = 'm'
    interval_input = input('Enter minute interval: ')
else:
    print('Input format error!')
    exit()

start_time = time.time()

if not os.path.exists('../../results'):
    os.mkdir('../../results')
    os.mkdir('../../results/diagram_results')
elif not os.path.exists('../../results/diagram_results'):
    os.mkdir('../../results/diagram_results')

print('Retrieving data ...')


disk.draw_io_bandwidth(iostat_file, min_hour_input, int(interval_input))
disk.disk_utilization(iostat_file, min_hour_input, int(interval_input))
cpu.cpu_utilization(iostat_file, min_hour_input, int(interval_input))
cb.cpu_bandwidth(iostat_file, min_hour_input, int(interval_input))

if gpustat_file != 'no':
    gpu.gpu_utilization(gpustat_file, min_hour_input, int(interval_input))


print('Total execution time: %0.1f seconds' %round(time.time() - start_time, 2))
