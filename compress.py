import os
# import pickle
import pyiqa
import sys
import torchvision.transforms as transforms
from PIL import Image

src_list = ['Lenna_(test_image).png', 'NAPS_H/People_001_h.jpg', 'People_160_h.jpg']

src = src_list[2]

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
    'B': .80,
    'C': .60,
    'D': .40,
    'E': .20,
}

src_no_ext = src[:src.find('.')]
slash_pos = src_no_ext.rfind('/')
if slash_pos > -1:
    src_past_slash_no_ext = src_no_ext[slash_pos+1:]
else:
    src_past_slash_no_ext = src_no_ext

print(src_no_ext)
print(src_past_slash_no_ext)
# sys.exit(0)

# Create VIF metric with default setting
vif_metric = pyiqa.create_metric('vif')

to_tensor = transforms.ToTensor()
# sys.exit()

# Main compress and metric loop
for f in os.listdir('tmp'):
    os.remove(os.path.join('tmp', f))
metric_values = []
image = Image.open(src)

if metric == 'vmaf':
    os.system(f'ffmpeg -y -i "{src}" -pix_fmt yuv444p tmp/reference.y4m')
    for q in range(101):
        pvs = os.path.join('tmp', f'{src_no_ext}_{q}.jpg')
        image.save(pvs, 'JPEG', quality=q)
        os.system(f'ffmpeg -y -i "{pvs}" -pix_fmt yuv444p tmp/distorted.y4m')
        os.system('vmaf -r tmp/reference.y4m -d tmp/distorted.y4m -o tmp/output.csv --csv --feature vif --threads 8')
        with open('tmp/output.csv') as vmaf_file:
            metric_values.append(float(vmaf_file.read().split(',')[-2]))
    # with open('metric_values', 'wb') as metric_values_file:
    #     pickle.dump(metric_values, metric_values_file)
    # with open('metric_values', 'rb') as metric_values_file:
    #     metric_values = pickle.load(metric_values_file)
elif metric == 'vif':
    r = Image.open(src).convert('RGB')
    r_tensor = to_tensor(r)
    r_tensor = r_tensor.unsqueeze(0)
    for q in range(101):
        pvs = os.path.join('tmp', f'{src_no_ext}_{q}.jpg')
        image.save(pvs, 'JPEG', quality=q)
        d = Image.open(pvs).convert('RGB')
        d_tensor = to_tensor(d)
        d_tensor = d_tensor.unsqueeze(0)
        score_tensor = vif_metric(r_tensor, d_tensor)
        metric_values.append(score_tensor.item())

print(metric_values)
# sys.exit()

for hrc_key in hrc:
    desired_metric = hrc[hrc_key]
    if desired_metric is None:
        os.system(f'cp "{src}" "{src_no_ext}_{hrc_key}.jpg"')
        print(f'hrc_key = {hrc_key}, desired_metric = {desired_metric}')
    else:
        distance = abs(desired_metric-metric_values[0])
        distance_index = 0
        for metric_i in range(1, 101):
            if abs(desired_metric-metric_values[metric_i]) < distance:
                distance = abs(desired_metric - metric_values[metric_i])
                distance_index = metric_i
        pvs_file = os.path.join('tmp', f'{src_no_ext}_{distance_index}.jpg')
        os.system(f'cp "{pvs_file}" "{src_no_ext}_{hrc_key}.jpg"')
        print(f'hrc_key = {hrc_key}, desired_metric = {desired_metric}, '
              f'distance_index = {distance_index}, distance = {distance}')
sys.exit()
