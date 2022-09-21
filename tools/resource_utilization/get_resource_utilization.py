import time
import disk_utilization as disk
import cpu_utilization as cpu
import gpu_utilization as gpu


iostat_file = input('Enter iostat file path: ')
start_time = time.time()

print('Retrieving data ...')


disk.draw_io_bandwidth(iostat_file)
disk.disk_utilization(iostat_file)
cpu.cpu_utilization(iostat_file)
# gpu.gpu_utilization(iostat_file)


print('Total execution time: %0.1f seconds: ' %round(time.time() - start_time, 2))
