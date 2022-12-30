# Standard library imports
import random
import requests


# Constants
# URL = 'http://pbz.kt.agh.edu.pl/~testySubiektywne/PIQMOS/config/src.csv'
URL = 'http://pbz.kt.agh.edu.pl/~testySubiektywne/PIQMOS/config/src_internal.csv'
SERIES = 1000
LEVELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G')


# Functions
def print_write(file_object, line):
    print(line)
    file_object.write(f'{line}\n')


# Main
lines = str(requests.get(URL).text).split('\n')[1:]
if not lines[-1]:
    lines.pop()
print("BEGIN DOWNLOAD")
print(lines)
print('END DOWNLOAD')
srcs = [line.split(',')[0] for line in lines]
dots = [srcs[i].rfind('.') for i in range(len(srcs))]
no = 0
with open('orders.csv', 'w') as file:
    print_write(file, f'no,{",".join(srcs)}')
    for five_id in range(SERIES):
        hrcs = [random.sample(LEVELS, len(LEVELS)) for src in srcs]
        for hrc in range(7):
            print_write(
                file,
                # f'{no},{",".join([srcs[i][:dots[i]]+"_"+hrcs[i][hrc]+srcs[i][dots[i]:] for i in range(len(srcs))])}'
                f'{no},{",".join([hrcs[i][hrc] for i in range(len(srcs))])}'
            )
            no += 1
