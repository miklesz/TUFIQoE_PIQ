import os
import pickle
from PIL import Image
src = 'Lenna_(test_image).png'
hrc = {
    'A': None,
    'B': 80,
    'C': 60,
    'D': 40,
    'E': 20,
}
metric = 'vmaf'
src_no_ext = src[:src.find('.')]

# # Main compress and metric loop
# for f in os.listdir('tmp'):
#     os.remove(os.path.join('tmp', f))
# image = Image.open(src)
# os.system(f'ffmpeg -y -i "{src}" -pix_fmt yuv444p tmp/reference.y4m')
# metric_values = []
# for q in range(101):
#     pvs = os.path.join('tmp', f'{src_no_ext}_{q}.jpg')
#     image.save(pvs, 'JPEG', quality=q)
#     os.system(f'ffmpeg -y -i "{pvs}" -pix_fmt yuv444p tmp/distorted.y4m')
#     os.system('vmaf -r tmp/reference.y4m -d tmp/distorted.y4m -o tmp/output.csv --csv --threads 8')
#     with open('tmp/output.csv') as vmaf_file:
#         metric_values.append(float(vmaf_file.read().split(',')[-2]))
# with open('metric_values', 'wb') as metric_values_file:
#     pickle.dump(metric_values, metric_values_file)

with open('metric_values', 'rb') as metric_values_file:
    metric_values = pickle.load(metric_values_file)
print(metric_values)
for hrc_key in hrc:
    print(hrc_key)
    desired_metric = hrc[hrc_key]
    print(desired_metric)
    if desired_metric is None:
        os.system(f'cp "{src}" "{src_no_ext}_{hrc_key}.jpg"')
    else:
        distance = abs(desired_metric-metric_values[0])
        distance_i = 0
        for metric_i in range(1, 101):
            if abs(desired_metric-metric_values[metric_i]) < distance:
                distance = abs(desired_metric - metric_values[metric_i])
                distance_i = metric_i
        pvs_file = os.path.join('tmp', f'{src_no_ext}_{distance_i}.jpg')
        os.system(f'cp "{pvs_file}" "{src_no_ext}_{hrc_key}.jpg"')
        print(distance_i, distance)

