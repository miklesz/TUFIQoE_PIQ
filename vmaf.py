# Standard library imports
import csv
import glob
import os

# Save header to CSV
with open(file='vmaf.csv', mode='w') as piq_file:
    csv_writer = csv.writer(piq_file)
    csv_writer.writerow(['filename', 'vmaf'])

for distorted_filename in glob.glob('TUFIQoEMOS_final/*'):
    os.system(f'ffmpeg -y -i {distorted_filename} tmp/distorted.y4m')
    filename = distorted_filename[17:]
    reference_filename = 'NAPS_H/'+filename[:-6]+'.jpg'
    os.system(f'ffmpeg -y -i {reference_filename} tmp/reference.y4m')
    os.system('vmaf -r tmp/reference.y4m -d tmp/distorted.y4m -o tmp/output.csv --csv --threads 8')
    with open('tmp/output.csv') as vmaf_file:
        vmaf = vmaf_file.read().split(',')[-2]
    with open(file='vmaf.csv', mode='a') as piq_file:
        csv_writer = csv.writer(piq_file)
        csv_writer.writerow([filename, vmaf])
