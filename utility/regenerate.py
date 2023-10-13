import os
import shutil
source_dir = '/mnt/samsung/img_cls_reg_dataset'
dest_dir = '/mnt/samsung/img_cls_reg_dataset_new'
i = 1
base = 100

total_size = 0
while total_size < base * 1024 * 1024 * 1024:
	for filename in os.listdir(source_dir):
		if filename.endswith('.jpg'):
			new_filename = f'image{i}.jpg'
			shutil.copy(os.path.join(source_dir, filename), os.path.join(dest_dir, new_filename))
			i += 1
			total_size += os.path.getsize(os.path.join(dest_dir, new_filename))
			if total_size >= base * 1024 *1024 * 1024:
			    break
	if total_size >= base * 1024 * 1024 * 1024:
		break
