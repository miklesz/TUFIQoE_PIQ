import glob
import math
import os
# import pickle
import pyiqa
import sys
import torchvision.transforms as transforms
from PIL import Image


# Constants
SRC_PATH = 'src'
PVS_PATH = 'pvs'


# Functions
def half_third_f(x):
    # print(int(x*4))
    return (0, 1/(2.5*2.5*2.5), 1/(2.5*2.5), 1/2.5)[int(x*4)]


def third_f(x):
    # print(int(x*4))
    return (0, 1/(3*3*3), 1/(3*3), 1/3)[int(x*4)]


def half_f(x):
    # print(int(x*4))
    return (0, 1/8, 1/4, 1/2)[int(x*4)]


def exp_f(x):
    return (math.exp(x)-1)/(math.e-1)


def lin_f(x):
    return x


def f(x):
    return half_third_f(x)


# src_list = ['Lenna_(test_image).png', 'People_001_h.jpg', 'People_160_h.jpg']

src_list = glob.glob(f'{SRC_PATH}/*')
src_list = sorted([src[len(SRC_PATH)+1:] for src in src_list])

# print(src_list)
# sys.exit()

for i in (0.00, 0.25, 0.50, 0.75):
    print(f(i))
# sys.exit()

with open(f'{PVS_PATH}/pvs_stats.csv', 'a') as file:
    file.write('src,hrc_key,desired_metric,achieved_metric,distance_index,distance\n')

for src in src_list[164+2:]:

    print(f'src = {src}')
    # src = src_list[2]

    # metric = 'vmaf'
    # hrc = {
    #     'A': None,
    #     'B': 80,
    #     'C': 60,
    #     'D': 40,
    #     'E': 20,
    # }

    metric = 'vif'
    hrc = {
        'A': None,
        'B': (1-0.1611954868)*f(.75)+0.1611954868,
        'C': (1-0.1611954868)*f(.50)+0.1611954868,
        'D': (1-0.1611954868)*f(.25)+0.1611954868,
        'E': (1-0.1611954868)*f(.00)+0.1611954868,
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
            os.system('vmaf -r tmp/ref.y4m -d tmp/dis.y4m -o tmp/output.csv --csv --feature vif --threads 8')
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
