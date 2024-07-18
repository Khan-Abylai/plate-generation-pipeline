from glob import glob
import os
import shutil
# path = '/home/yeleussinova/data_SSD/usa_plate_images/california/synthetic'
# orig_images = '/home/yeleussinova/data_SSD/exp_us_001'
# out_path = '/home/yeleussinova/data_SSD/usa_plate_images/california/original'
# img_names = [x[:8] for x in os.listdir(path)]
# files = [x for x in glob(os.path.join(orig_images, "*", "*")) if ".jpg" in x]
# print(img_names)
# out_label = open('label_calif.txt', 'w')
# for file in files:
#     if file.split('/')[-1].replace('.jpg', '') in img_names:
#         # shutil.copy(file, out_path)
#         f = file.split('/')[-2]
#         label = open(orig_images + '/' + f + '/plate.txt', 'r')
#         plate = label.readline()
#         out_label.writelines(file + ' ' + plate + '\n')

path = '/home/yeleussinova/data_SSD/usa_plate_images/california/A'
img = '/home/yeleussinova/data_SSD/usa_plate_images/california/orig_plates'
to = '/home/yeleussinova/data_SSD/usa_plate_images/california/B'

images = os.listdir(img)

for im in images:
    shutil.copy(os.path.join(path, im), to)

