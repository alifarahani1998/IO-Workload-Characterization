import os
import string
import shutil

path = '/mnt/samsung_ssd/fawkes/dataset/4k_human_images'
os.chdir(path)


def copy():
    os.chdir(path)
    dst_dir = '/mnt/samsung_ssd/fawkes/dataset/4k_human_images_1'
    for f in os.listdir(path):
        try:
            shutil.copy(f, dst_dir)
        except OSError as err:
            print(err)
    print('copy done!')



alphabet = list(string.ascii_lowercase)
new_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

for letter1 in new_alphabet:
#    for letter2 in new_alphabet:
#        for letter3 in new_alphabet:
            i = 0
            for file in os.listdir(path):

                new_file_name = "%s%d.png" %(letter1, i)
                os.rename(file, new_file_name)

                i += 1
            print('rename done!')
            copy()

