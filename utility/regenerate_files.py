import os
import shutil
import string


path = 'F:/test/lfw_funneled_new1/'

source_folder = 'F:/test/lfw_funneled_new1/'
destination_folder = 'F:/test/lfw_funneled_new2/'


def rename_files(i, j):

    directory_list = os.listdir(path)

    for k, filename in enumerate(directory_list):
        
        dst_file = '%s%s%d' %(i, j, k) + '.jpg'

        os.rename(os.path.join(path, filename), os.path.join(path, dst_file))

    print('renaming done!')


def copy_files():
    for file_name in os.listdir(source_folder):
        
        source = source_folder + file_name
        destination = destination_folder + file_name

        shutil.copyfile(source, destination)
        
    print('copying done!')


for i in range(0, 44):
    for j in range(0, 44):
        rename_files(i, j)
        copy_files()


# alphabet = list(string.ascii_lowercase)

# for i in alphabet:
#     for j in alphabet:
#         rename_files(i, j)
#         copy_files()

