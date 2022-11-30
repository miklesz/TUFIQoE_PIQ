# Standard library imports
import sys


# Library imports
import matplotlib.pyplot as plt
import numpy as np


# Functions
def make_chart(my_pvs_col_id, my_naps_col_id):
    pvs_col_name = pvs_lines[0].split(',')[my_pvs_col_id]
    if pvs_col_name[-1] == '\n':
        pvs_col_name = pvs_col_name[:-1]
    # print(pvs_col_name)
    if my_naps_col_id <= 21:
        naps_col_name = naps_lines[1].split(';')[my_naps_col_id]
    else:
        naps_col_name = naps_lines[2].split(';')[my_naps_col_id]
    # print(naps_col_name)
    chart_name = f'{pvs_col_name}({naps_col_name})'.replace('/', '_')
    # print(chart_name)
    chart_x = []
    chart_y = []
    levels = []

    # return
    for pvs_line in pvs_lines[1:]:
        pvs_line_elements = pvs_line.split(',')
        try:
            naps_id = naps_ids.index(pvs_line_elements[0][:-4])
        except ValueError as err:
            # print(err)
            pass
        else:
            # print()
            naps_line = naps_lines[naps_id]
            naps_line_elements = naps_line.split(';')
            # print(pvs_line_elements)
            # print(naps_line_elements)
            pvs_string = pvs_line_elements[my_pvs_col_id]
            naps_string = naps_line_elements[my_naps_col_id].replace(',', '.')
            level_string = pvs_line_elements[1]
            if pvs_string != 'None':
                # print(f'>{pvs_string}<')
                pvs_value = float(pvs_string)
                naps_value = float(naps_string)
                # print(pvs_value, naps_value)
                # print(pvs_line_elements[0], naps_ids[naps_id])
                # print(pvs_line_elements[my_pvs_col_id], naps_id)
                chart_x.append(naps_value)
                chart_y.append(pvs_value)
                levels.append(level_string)
    # plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.scatter(chart_x, chart_y)
    plt.xlabel(naps_col_name)
    plt.ylabel(pvs_col_name)
    plt.title(chart_name)
    plt.savefig(f'scatter_plots/{chart_name}.png')
    # plt.show()
    plt.clf()

    x_dict = {}
    y_dict = {}
    for i in range(len(chart_x)):
        # print(chart_x[i], chart_y[i], levels[i])
        if levels[i] in x_dict.keys():
            x_dict[levels[i]].append(chart_x[i])
            y_dict[levels[i]].append(chart_y[i])
        else:
            x_dict[levels[i]] = [chart_x[i]]
            y_dict[levels[i]] = [chart_y[i]]

    for key in x_dict:
        r = np.corrcoef(x_dict[key], y_dict[key])
        pearson = r[0, 1]
        # print(key, pearson)
        # print(y_dict[key])
        with open('scatter_plots/scatter_plots_correlation.csv', 'a') as corr_file:
            print(f'{pvs_col_name},{naps_col_name},{key},{pearson}')
            corr_file.write(f'{pvs_col_name},{naps_col_name},{key},{pearson}\n')

    # print(x_dict)
    # print(y_dict)

    # r = np.corrcoef(chart_x, chart_y)
    # pearson = r[0, 1]
    # print(pearson)


with open('pvs/pvs_stats_old.csv') as pvs_file:
    pvs_lines = pvs_file.readlines()

with open('13428_2013_379_MOESM1_ESM.csv') as naps_file:
    naps_lines = naps_file.readlines()
naps_ids = [naps_id.split(';')[0] for naps_id in naps_lines]
# print(naps_ids)

with open('scatter_plots/scatter_plots_correlation.csv', 'w') as corr_file:
    corr_file.write('pvs_parameter,naps_parameter,level,pearson\n')

pvs_col_ids = [2, 3, 4, 5]
naps_col_ids = [17, 19, 21, 25, 26, 27, 28, 29, 30, 31]
# pvs_col_ids = [4]
# naps_col_ids = [17]
for pvs_col_id in pvs_col_ids:
    for naps_col_id in naps_col_ids:
        make_chart(pvs_col_id, naps_col_id)
