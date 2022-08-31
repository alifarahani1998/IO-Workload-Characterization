import os
import shutil

path = 'F:\Compressed\coco128\images\\train2017\\'

source_folder = 'F:\Compressed\coco128\images\\train2017\\'
destination_folder = 'F:\Compressed\coco128\images\\train\\'


def rename_files(repeat):

    directory_list = os.listdir(path)

    for i, filename in enumerate(directory_list):
        
        src_file = filename
        dst_file = filename.removesuffix(str(filename)[repeat:]) + 'a%d' %(repeat + i) + '.jpg'

        os.rename(os.path.join(path, src_file), os.path.join(path, dst_file))

    print('renaming done!')


def copy_files():
    for file_name in os.listdir(source_folder):
        
        source = source_folder + file_name
        destination = destination_folder + file_name

        shutil.copyfile(source, destination)
        
    print('copying done!')


for i in range(1, 201):
    rename_files(i)
    copy_files()
