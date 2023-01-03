# import datetime as dt
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from matplotlib.collections import PolyCollection

# data = [    (dt.datetime(2018, 7, 17, 0, 15), dt.datetime(2018, 7, 17, 0, 30), 'CPU'),
#             (dt.datetime(2018, 7, 17, 0, 30), dt.datetime(2018, 7, 17, 0, 45), 'GPU'),
#             (dt.datetime(2018, 7, 17, 0, 45), dt.datetime(2018, 7, 17, 1, 0), 'I/O'),
#             (dt.datetime(2018, 7, 17, 1, 0), dt.datetime(2018, 7, 17, 1, 30), 'CPU'),
#             (dt.datetime(2018, 7, 17, 1, 15), dt.datetime(2018, 7, 17, 1, 30), 'GPU'), 
#             (dt.datetime(2018, 7, 17, 1, 30), dt.datetime(2018, 7, 17, 1, 45), 'I/O')
#         ]

# items = {"CPU" : 1, "GPU" : 2, "I/O" : 3}
# colormapping = {"CPU" : "C0", "GPU" : "C1", "I/O" : "C2"}

# verts = []
# colors = []
# for d in data:
#     v =  [(mdates.date2num(d[0]), items[d[2]]-.4),
#           (mdates.date2num(d[0]), items[d[2]]+.4),
#           (mdates.date2num(d[1]), items[d[2]]+.4),
#           (mdates.date2num(d[1]), items[d[2]]-.4),
#           (mdates.date2num(d[0]), items[d[2]]-.4)]
#     verts.append(v)
#     colors.append(colormapping[d[2]])

# bars = PolyCollection(verts, facecolors=colors)

# fig, ax = plt.subplots()
# ax.add_collection(bars)
# ax.autoscale()
# loc = mdates.MinuteLocator(byminute=[0, 15, 30, 45])
# ax.xaxis.set_major_locator(loc)
# ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(loc))

# ax.set_yticks([1, 2, 3])
# ax.set_yticklabels(["CPU", "GPU", "I/O"])
# plt.show()

###############################################################################

# from audioop import reverse
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np

# print('Retrieving data ...')

# df = pd.read_table('data/lirec_none_trace.txt', header=0, usecols=['time', 'event', 'R/W'], delim_whitespace=True, dtype=str, na_filter=False)

# for i in range(df.shape[0] - 1, -1, -1):
#     rowSeries = df.iloc[i]
#     if rowSeries.values[1] == 'C':
#         last_time = float(rowSeries.values[0])
#         break


# if (int(last_time/60)) < 200:
#     last_time = int(last_time/60)
#     if last_time > 100:
#         interval = 10
#     elif last_time < 100 and last_time > 50:
#         interval = 5
#     else:
#         interval = 2
#     min_hour_check = 'm'
# else:
#     last_time = int(last_time/3600)
#     if last_time > 100:
#         interval = 10
#     elif last_time < 100 and last_time > 50:
#         interval = 5
#     else:
#         interval = 2
#     min_hour_check = 'h'

# print('Processing data ...')

# write_end_checkpoint = 0
# read_end_checkpoint = 0
# read_threshold = 0
# write_start_checkpoint = 0
# read_start_checkpoint = 0
# flag = False

# for index in df.index:
#     if 'W' in df['R/W'][index] and df['event'][index] == 'C':
#         write_end_checkpoint = float(df['time'][index])
#         if flag:
#             plt.hlines(0, read_start_checkpoint, read_end_checkpoint, colors='blue', lw=100, label='Read')
#             write_start_checkpoint = read_end_checkpoint
#         if read_threshold > 0:
#             read_threshold -= 1
#             flag = False
#     elif 'R' in df['R/W'][index] and df['event'][index] == 'C':
#         read_end_checkpoint = float(df['time'][index])
#         read_threshold += 1
#         if read_threshold > 100:
#             flag = True
#             plt.hlines(0, write_start_checkpoint, write_end_checkpoint, colors='orange', lw=100, label='Write')
#             read_start_checkpoint = write_end_checkpoint
            

# print('Drawing timeline chart ...')

# # plt.text(x + 1, 1.01, ha='center')
# plt.yticks([])
# from matplotlib.lines import Line2D
# custom_lines = [Line2D([0], [0], color='orange', lw=5),
#                 Line2D([0], [0], color='blue', lw=5)]
# plt.legend(custom_lines, ['Write', 'Read'], loc='upper center', ncol=2)
# plt.ylim([0, 1])
# plt.xlim([0, max(write_end_checkpoint, read_end_checkpoint)])
# plt.xticks(np.arange(0, max(write_end_checkpoint, read_end_checkpoint), 20000), rotation=45)
# plt.grid()
# plt.xlabel('Time (s)', fontweight='bold', fontsize=15.0)
# plt.gcf().set_size_inches(12, 2.2)
# plt.tight_layout()
# plt.savefig('results/io_timeline.png') 

###############################################################################


from audioop import reverse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

print('Retrieving data ...')

df = pd.read_table('../data/lirec_none_trace.txt', header=0, usecols=['time', 'event', 'R/W'], delim_whitespace=True, dtype=str, na_filter=False)

# for i in range(df.shape[0] - 1, -1, -1):
#     rowSeries = df.iloc[i]
#     if rowSeries.values[1] == 'C':
#         last_time = float(rowSeries.values[0])
#         break


# if (int(last_time/60)) < 200:
#     last_time = int(last_time/60)
#     if last_time > 100:
#         interval = 10
#     elif last_time < 100 and last_time > 50:
#         interval = 5
#     else:
#         interval = 2
#     min_hour_check = 'm'
# else:
#     last_time = int(last_time/3600)
#     if last_time > 100:
#         interval = 10
#     elif last_time < 100 and last_time > 50:
#         interval = 5
#     else:
#         interval = 2
#     min_hour_check = 'h'

print('Processing data ...')

write_end_checkpoint = 0
read_end_checkpoint = 0
read_threshold = 0
write_start_checkpoint = 0
read_start_checkpoint = 0
flag = False

for index in df.index:
    if 'W' in df['R/W'][index] and df['event'][index] == 'C':
        write_end_checkpoint = float(df['time'][index])
        if flag:
            plt.hlines(0, read_start_checkpoint, read_end_checkpoint, colors='blue', lw=100, label='Read')
            write_start_checkpoint = read_end_checkpoint
        if read_threshold > 0:
            read_threshold -= 1
            flag = False
    elif 'R' in df['R/W'][index] and df['event'][index] == 'C':
        read_end_checkpoint = float(df['time'][index])
        read_threshold += 1
        if read_threshold > 100:
            flag = True
            plt.hlines(0, write_start_checkpoint, write_end_checkpoint, colors='orange', lw=100, label='Write')
            read_start_checkpoint = write_end_checkpoint
            

print('Drawing timeline chart ...')

# plt.text(x + 1, 1.01, ha='center')
plt.yticks([])
from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color='orange', lw=5),
                Line2D([0], [0], color='blue', lw=5)]
plt.legend(custom_lines, ['Write', 'Read'], loc='upper center', ncol=2)
plt.ylim([0, 1])
plt.xlim([0, max(write_end_checkpoint, read_end_checkpoint)])
# plt.xticks(np.arange(0, max(write_end_checkpoint, read_end_checkpoint), 20000), rotation=45)
plt.grid()
plt.xlabel('Time (s)', fontweight='bold', fontsize=15.0)
plt.gcf().set_size_inches(12, 2.2)
plt.tight_layout()
plt.savefig('../io_timeline.png') 
