import os
import string
import shutil

path="F:/test/File"
os.chdir(path)


def copy():
    os.chdir(path)
    dst_dir = 'F:/test/New_File'
    for f in os.listdir(path):
        try:
            shutil.copy(f, dst_dir)
        except OSError as err:
            print(err)
    print('copy done!')



alphabet = list(string.ascii_lowercase)
new_alphabet = ['a', 'b', 'c', 'd']

for letter1 in alphabet:
    for letter2 in alphabet:
        for letter3 in new_alphabet:
            i = 0
            for file in os.listdir(path):

                new_file_name = "%s%s%s%d.jpg" %(letter1, letter2, letter3, i)
                os.rename(file, new_file_name)

                i += 1
            print('rename done!')
            copy()
