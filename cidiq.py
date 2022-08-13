# Standard library imports
import csv
import glob

# Related third party imports
from PIL import Image
import pyiqa
import torchvision.transforms as transforms

# list all available metrics
models = pyiqa.list_models()
models.remove('musiq')
models.remove('musiq-ava')
models.remove('musiq-koniq')
models.remove('musiq-paq2piq')
models.remove('musiq-spaq')
models.remove('nima')
models.remove('nrqm')
models.remove('pi')

# create metrics with default setting
iqa_metrics = [pyiqa.create_metric(iqa_metric) for iqa_metric in models]

to_tensor = transforms.ToTensor()

# Save header to CSV
with open(file='cidiq.csv', mode='w') as piq_file:
    csv_writer = csv.writer(piq_file)
    csv_writer.writerow(['filename']+models)

for distorted_filename in glob.glob('CIDIQ/Images/Reproduction/2_JPEG_Compression/*'):
    print(distorted_filename)
    d = Image.open(distorted_filename).convert('RGB')
    filename = distorted_filename[45:]
    print(filename)
    reference_filename = 'CIDIQ/Images/Original/'+filename[:-10]+'.bmp'
    print(reference_filename)
    r = Image.open(reference_filename).convert('RGB')
    r_tensor = to_tensor(r)
    d_tensor = to_tensor(d)
    r_tensor = r_tensor.unsqueeze(0)
    d_tensor = d_tensor.unsqueeze(0)
    scores = []
    for iqa_metric in iqa_metrics:
        try:
            score_tensor = iqa_metric(r_tensor, d_tensor)
        except TypeError:
            score_tensor = iqa_metric(d_tensor)
        score = score_tensor.item()
        scores.append(score)
    with open(file='cidiq.csv', mode='a') as piq_file:
        csv_writer = csv.writer(piq_file)
        csv_writer.writerow([filename]+scores)
