# Standard library imports
import random
import requests


# Constants
URL = 'http://pbz.kt.agh.edu.pl/~testySubiektywne/PIQMOS/config/src.csv'
SERIES = 1
LEVELS = ('A', 'B', 'C', 'D', 'E')


# Functions
def print_write(file_object, line):
    print(line)
    file_object.write(f'{line}\n')


srcs = [line.split(',')[0] for line in str(requests.get(URL).content).split('\\n')[1:-1]]
no = 0
with open('orders.csv', 'w') as file:
    print_write(file, f'no,{",".join(srcs)}')
    for five_id in range(SERIES):
        versions = [random.sample(LEVELS, len(LEVELS)) for src in srcs]
        for in_five_id in range(5):
            print_write(
                file,
                f'{no},{",".join([srcs[i][:srcs[i].rfind(".")] + "_" + versions[i][in_five_id] + ".jpg" for i in range(len(srcs))])}'
            )
            no += 1
