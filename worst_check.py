from PIL import Image
import glob
import os
import pyiqa
import torchvision.transforms as transforms


def print_write(string, write_f):
    print(string)
    write_f.write(f'{string}\n')


vif_metric = pyiqa.create_metric('vif')
to_tensor = transforms.ToTensor()
with open('worst/worst_check.csv', 'w') as f:
    print_write('src_name,pvs_name,vmaf,vif', f)
    for pvs_name in [glob.glob(f'worst/People_{number:03d}_*')[0] for number in range(1, 250+1)]:  # 250+1
        src_name = 'NAPS_H' + pvs_name[5:]
        os.system(f'ffmpeg -y -i "{src_name}" -pix_fmt yuv444p tmp/reference.y4m')
        os.system(f'ffmpeg -y -i "{pvs_name}" -pix_fmt yuv444p tmp/distorted.y4m')
        os.system('vmaf -r tmp/reference.y4m -d tmp/distorted.y4m -o tmp/output.csv --csv --feature vif --threads 8')
        with open('tmp/output.csv') as vmaf_file:
            vmaf = float(vmaf_file.read().split(',')[-2])

        r = Image.open(src_name).convert('RGB')
        r_tensor = to_tensor(r)
        r_tensor = r_tensor.unsqueeze(0)
        d = Image.open(pvs_name).convert('RGB')
        d_tensor = to_tensor(d)
        d_tensor = d_tensor.unsqueeze(0)
        score_tensor = vif_metric(r_tensor, d_tensor)
        vif= score_tensor.item()

        print_write(f'{src_name},{pvs_name},{vmaf},{vif}', f)
