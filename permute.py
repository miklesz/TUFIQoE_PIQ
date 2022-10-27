# Standard library imports
import requests


URL = 'http://pbz.kt.agh.edu.pl/~testySubiektywne/PIQMOS/config/src.csv'
src = [line.split(',')[0] for line in str(requests.get(URL).content).split('\\n')[1:-1]]
print(src)
print(type(src))
