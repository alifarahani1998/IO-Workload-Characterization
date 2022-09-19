import pandas as pd
import time
from datetime import datetime


input_file = input('Enter trace (input) file name: ')
now = datetime.now()
start_time = time.time()

print('Retrieving data ...')

df = pd.read_table('%s' %input_file, header=0, usecols=['average_size_rd', 'average_time_rd', 'max_size', 'max_time', 'min_size', 'min_time'], delim_whitespace=True, dtype=str, na_filter=False)



def byte_to_kb(value):
    return round(value / 1024, 1)


def byte_to_mb(value):
    return round(value / 1048576, 1)


def byte_to_gb(value):
    return round(value / 1073741824, 1)

def byte_to_tb(value):
    return round(value / 1099511627776, 1)

total_requests = 0
total_avg_size = 0
total_avg_time = 0
total_max_size = 0
total_max_time = 0
total_min_size = 0
total_min_time = 0

print('Generating results ...')

# size of individual IOs

for index in df.index:
        
    if df['average_size_rd'][index] != '' and df['average_time_rd'][index] != '':

        total_requests += 1
        
        total_avg_size += float(df['average_size_rd'][index])
        total_avg_time += float(df['average_time_rd'][index])

        total_max_size += float(df['max_size'][index])
        total_max_time += float(df['max_time'][index])

        total_min_size += float(df['min_size'][index])
        total_min_time += float(df['min_time'][index])
         
print('Total requests: ', total_requests)
print('Total avg size: %s GB' % str(byte_to_gb(total_avg_size/total_requests)))
print('Total avg time: %s ns' % str(round(total_avg_time/total_requests, 1)))


print('Total max size: %s GB' % str(byte_to_gb(total_max_size/total_requests)))
print('Total max time: %s ns' % str(round(total_max_time/total_requests, 1)))


print('Total min size: %s GB' % str(byte_to_gb(total_min_size/total_requests)))
print('Total min time: %s ns' % str(round(total_min_time/total_requests, 1)))

max_size = byte_to_gb(total_max_size/total_requests)
avg_size = byte_to_gb(total_avg_size/total_requests)
min_size = byte_to_gb(total_min_size/total_requests)


from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

# np.random.seed(20210706)

# Create fake x-data
x = np.arange(10)
# Create fake y-data
a = 4.5
b = 0.5
# c = 500
y=[7, 8, 7.5, 9, 10, 9.2, 12, 13, 12, 14]
# y = a * np.exp(b * x) + c  # Use the second formulation from above
# y = y + np.random.normal(scale=np.sqrt(np.max(y)), size=len(x))  # Add noise
plt.rcParams.update({'font.size': 14.0, 'font.weight': 'bold'})

# Fit the function a * np.exp(b * t) to x and y
popt, pcov = curve_fit(lambda t, a, b: a * np.exp(b * t), x, y)
# Extract the optimised parameters
a = popt[0]
b = popt[1]
x_fitted_curve_fit = np.linspace(np.min(x), np.max(x), 100)
y_fitted_curve_fit = a * np.exp(b * x_fitted_curve_fit)
x_labs = [
    '250', '270', '290', '310', '330',
    '350', '370', '390', '410', '430'
]
textstr = '\n'.join((
        'MAX size: %1.1f GB' %max_size,
        'AVG size: %1.1f GB' %avg_size,
        'MIN size: %1.1f GB' %min_size,
    ))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# Plot
ax = plt.axes()
ax.bar(x, y)
# ax.plot(x_fitted_curve_fit, y_fitted_curve_fit, label='Ideal curve', color='red')
ax.set_xticks(x)
ax.set_xticklabels(x_labs)
ax.set_xlim([0.5, len(y) - 0.5])
ax.tick_params(axis='x', length=0, labelsize=12)
xlocs = np.arange(len(y) + 1) - 0.5
ax.set_xticks(xlocs, minor=True)
ax.set_ylim([0, max(y) + 3])
ax.set_title('Cache size vs Reuse time', fontweight='bold', fontsize=15.0)
ax.set_ylabel('Cache size (GB)', fontweight='bold', fontsize=15.0)
ax.set_xlabel('Reuse time (ns)', fontweight='bold', fontsize=15.0)
# ax.legend()
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
plt.tight_layout()
plt.gcf().set_size_inches(12, 6)
plt.show()


