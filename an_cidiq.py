import matplotlib.pyplot as plt
import numpy as np


data = np.genfromtxt('cidiq_data.csv', delimiter=',')
plt.style.use('ggplot')

mos = 'mos50'

iqa = 'vif'
fig = plt.figure()
plt.scatter(data[1:, 0], data[1:, 2])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()

iqa = 'fsim'
fig = plt.figure()
plt.scatter(data[1:, 0], data[1:, 3])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()

iqa = 'mad'
fig = plt.figure()
plt.scatter(data[1:, 0], data[1:, 4])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()

iqa = 'gmsd'
fig = plt.figure()
plt.scatter(data[1:, 0], data[1:, 5])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()

mos = 'mos100'

iqa = 'vif'
fig = plt.figure()
plt.scatter(data[1:, 1], data[1:, 2])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()

iqa = 'fsim'
fig = plt.figure()
plt.scatter(data[1:, 1], data[1:, 3])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()

iqa = 'mad'
fig = plt.figure()
plt.scatter(data[1:, 1], data[1:, 4])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()

iqa = 'gmsd'
fig = plt.figure()
plt.scatter(data[1:, 1], data[1:, 5])
plt.xlabel(mos)
plt.ylabel(iqa)
fig.savefig(f'plots/{mos}_{iqa}.png')
plt.show()
