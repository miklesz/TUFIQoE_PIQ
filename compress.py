import glob
# import math
import os
# import pickle
import pyiqa
import sys
import torchvision.transforms as transforms
from PIL import Image


# Constants
FACTOR = 2
PVS_PATH = 'pvs'
SRC_PATH = 'src'


# Functions
def f(x):
    return (
        0,
        1 / FACTOR ** 5,
        1 / FACTOR ** 4,
        1 / FACTOR ** 3,
        1 / FACTOR ** 2,
        1 / FACTOR ** 1,
    )[int(x * 6)]


# src_list = ['Lenna_(test_image).png', 'People_001_h.jpg', 'People_160_h.jpg']

src_list = glob.glob(f'{SRC_PATH}/*')
src_list = sorted([src[len(SRC_PATH)+1:] for src in src_list])

# print(src_list)
# sys.exit()

# for i in (0.00, 0.25, 0.50, 0.75):
for i in (0/6, 1/6, 2/6, 3/6, 4/6, 5/6):
    print(i, f(i))
# sys.exit()

with open(f'{PVS_PATH}/pvs_stats.csv', 'a') as file:
    file.write('src,hrc_key,desired_metric,achieved_metric,distance_index,distance\n')

# Interesting pictures:
# - People_027_h
# - People_197_h
# - People_156_h
# - People_160_h
# - People_087_h
# - People_177_h

# for src in src_list[164+2:]:
# for src in src_list:
for src in src_list[177+1:177+1+1]:

    print(f'src = {src}')
    # src = src_list[2]

    metric = 'vif'
    hrc = {
        'A': None,
        'B': (1 - 0.1611954868) * f(5 / 6) + 0.1611954868,
        'C': (1 - 0.1611954868) * f(4 / 6) + 0.1611954868,
        'D': (1 - 0.1611954868) * f(3 / 6) + 0.1611954868,
        'E': (1 - 0.1611954868) * f(2 / 6) + 0.1611954868,
        'F': (1 - 0.1611954868) * f(1 / 6) + 0.1611954868,
        'G': (1 - 0.1611954868) * f(0 / 6) + 0.1611954868,
    }
    # hrc = {
    #     'A': None,
    #     'B': (1-0.1611954868)*.75+0.1611954868,
    #     'C': (1-0.1611954868)*.50+0.1611954868,
    #     'D': (1-0.1611954868)*.25+0.1611954868,
    #     'E': (1-0.1611954868)*.00+0.1611954868,
    # }

    # print(hrc)
    # sys.exit()

    src_no_ext = src[:src.find('.')]
    # slash_pos = src_no_ext.rfind('/')
    # if slash_pos > -1:
    #     src_past_slash_no_ext = src_no_ext[slash_pos+1:]
    # else:
    #     src_past_slash_no_ext = src_no_ext

    # print(src_no_ext)
    # print(src_past_slash_no_ext)
    # sys.exit(0)

    # Create VIF metric with default setting
    vif_metric = pyiqa.create_metric('vif')

    to_tensor = transforms.ToTensor()
    # sys.exit()

    # Main compress and metric loop
    for f_tmp in os.listdir('tmp'):
        os.remove(os.path.join('tmp', f_tmp))
    metric_values = []
    image = Image.open(f'{SRC_PATH}/{src}')

    if metric == 'vmaf':
        os.system(f'ffmpeg -y -i "{SRC_PATH}/{src}" -pix_fmt yuv444p tmp/ref.y4m')
        for q in range(101):
            pvs = os.path.join('tmp', f'{src_no_ext}_{q}.jpg')
            image.save(pvs, 'JPEG', quality=q)
            os.system(f'ffmpeg -y -i "{pvs}" -pix_fmt yuv444p tmp/dis.y4m')
            os.system('vmaf -r tmp/ref.y4m -d tmp/dis.y4m -no tmp/output.csv --csv --feature vif --threads 8')
            with open('tmp/output.csv') as vmaf_file:
                metric_values.append(float(vmaf_file.read().split(',')[-2]))
        # with open('metric_values', 'wb') as metric_values_file:
        #     pickle.dump(metric_values, metric_values_file)
        # with open('metric_values', 'rb') as metric_values_file:
        #     metric_values = pickle.load(metric_values_file)
    elif metric == 'vif':
        r = Image.open(f'{SRC_PATH}/{src}').convert('RGB')
        r_tensor = to_tensor(r)
        r_tensor = r_tensor.unsqueeze(0)
        for q in range(101):
            print(f'{q}%', end='\r')
            pvs = os.path.join('tmp', f'{src_no_ext}_{q}.jpg')
            image.save(pvs, 'JPEG', quality=q)
            d = Image.open(pvs).convert('RGB')
            d_tensor = to_tensor(d)
            d_tensor = d_tensor.unsqueeze(0)
            score_tensor = vif_metric(r_tensor, d_tensor)
            metric_values.append(score_tensor.item())
        print()

    print(metric_values)
    # sys.exit()

    for hrc_key in hrc:
        desired_metric = hrc[hrc_key]
        if desired_metric is None:
            os.system(f'cp "{SRC_PATH}/{src}" "{PVS_PATH}/{src_no_ext}_{hrc_key}.jpg"')
            print(f'hrc_key = {hrc_key}, desired_metric = {desired_metric}')
            with open(f'{PVS_PATH}/pvs_stats.csv', 'a') as file:
                file.write(f'{src},{hrc_key},1,1,None,0\n')
        else:
            distance = abs(desired_metric-metric_values[0])
            distance_index = 0
            achieved_metric = 0
            for metric_i in range(1, 101):
                if abs(desired_metric-metric_values[metric_i]) < distance:
                    distance = abs(desired_metric - metric_values[metric_i])
                    distance_index = metric_i
                    achieved_metric = metric_values[metric_i]
            pvs_file = os.path.join('tmp', f'{src_no_ext}_{distance_index}.jpg')
            os.system(f'cp "{pvs_file}" "{PVS_PATH}/{src_no_ext}_{hrc_key}.jpg"')
            print(f'hrc_key = {hrc_key}, desired_metric = {desired_metric}, achieved_metric = {achieved_metric}, '
                  f'distance_index = {distance_index}, distance = {distance}')
            with open(f'{PVS_PATH}/pvs_stats.csv', 'a') as file:
                file.write(f'{src},{hrc_key},{desired_metric},{achieved_metric},{distance_index},{distance}\n')
sys.exit()
