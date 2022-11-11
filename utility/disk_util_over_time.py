utility_number = 0

iostat_input_file = input('Enter iostat file path: ')
runtime = input('Enter application runtime in minutes: ')
util_limit = input('Enter application runtime in minutes: ')

file = open('%s' %iostat_input_file, 'r')
lines = file.readlines()

for i, line in enumerate(lines):
    if 'util' in line:
        if float((lines[i+1].split())[20]) > float(util_limit):
            utility_number += 1

print('Number of lines with satisfied limit: %d' %utility_number)
print('Proportion of time with active disk util: {:.2%}'.format((utility_number-1)/int(runtime)))
