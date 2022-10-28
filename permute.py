# Standard library imports
import random
import requests


# Constants
URL = 'http://pbz.kt.agh.edu.pl/~testySubiektywne/PIQMOS/config/src.csv'
ORDERS = 5
LEVELS = ('A', 'B', 'C', 'D', 'E')

srcs = [line.split(',')[0] for line in str(requests.get(URL).content).split('\\n')[1:-1]]
print(srcs)
print(type(srcs))
order_id = 0
with open('orders.csv', 'w') as file:
    file.write(f'order_id,{",".join(srcs)}\n')
    for five_id in range(ORDERS//5+1):
        versions = [random.sample(LEVELS, len(LEVELS)) for src in srcs]
        for in_five_id in range(5):
            print(versions)
            # file.write(f'{order_id},\n')
            order_id += 1
