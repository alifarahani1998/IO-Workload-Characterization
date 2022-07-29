import os
import shutil

path = '/home/compute2/swin_track/dataset/coco2014/images/train2014fake/'

source_folder = '/home/compute2/swin_track/dataset/coco2014/images/train2014fake/'
destination_folder = '/home/compute2/swin_track/dataset/coco2014/images/train2014/'

directory_list = os.listdir(path)

def rename_files():

    for filename in directory_list:
        src_file = filename
        dst_file = filename.removesuffix('.jpg') + '1.jpg'

        os.rename(os.path.join(path, src_file), os.path.join(path, dst_file))

    print('renaming done!')


def copy_files():
    for file_name in os.listdir(source_folder):
        
        source = source_folder + file_name
        destination = destination_folder + file_name

        shutil.copyfile(source, destination)
        
    print('copying done!')


rename_files()
copy_files()
