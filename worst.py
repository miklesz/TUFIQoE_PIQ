from PIL import Image
import glob
for src_name in [glob.glob(f'NAPS_H/People_{number:03d}_*')[0] for number in range(1,250+1)]:
    print(src_name)
    image = Image.open(src_name)
    pvs_name = 'worst'+src_name[6:]
    print(pvs_name)
    image.save(pvs_name, 'JPEG', quality=0)
# print(glob.glob('NAPS_H/People_001*')[0])