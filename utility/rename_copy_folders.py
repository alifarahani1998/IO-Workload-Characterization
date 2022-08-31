import os
import shutil

source_folder = 'F:\Academics\MATLAB\FaceDetectionOpenCV\lfw_funneled'
destination_folder = 'F:\Academics\MATLAB\FaceDetectionOpenCV\lfw_funneled_new'


def rename_copy_folder(repeat):

    directory_list = os.listdir(source_folder)    
    count = 1

    for folder in directory_list:
        
        flip = folder
        flop = str(count) + ('_%d' %repeat)

        os.rename(os.path.join(source_folder, flip), os.path.join(source_folder, flop))
        count += 1
    
    
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
    

for i in range(1, 3):
    rename_copy_folder(i)

