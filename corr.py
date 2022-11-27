# Standard library imports
import sys


# Library imports
import matplotlib.pyplot as plt


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
    print(chart_name)
    chart_x = []
    chart_y = []

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
            if pvs_string != 'None':
                # print(f'>{pvs_string}<')
                pvs_value = float(pvs_string)
                naps_value = float(naps_string)
                # print(pvs_value, naps_value)
                # print(pvs_line_elements[0], naps_ids[naps_id])
                # print(pvs_line_elements[my_pvs_col_id], naps_id)
                chart_x.append(naps_value)
                chart_y.append(pvs_value)
    # plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.scatter(chart_x, chart_y)
    plt.xlabel(naps_col_name)
    plt.ylabel(pvs_col_name)
    plt.title(chart_name)
    plt.savefig(f'scatter_plots/{chart_name}.png')
    # plt.show()
    plt.clf()


with open('pvs/pvs_stats_old.csv') as pvs_file:
    pvs_lines = pvs_file.readlines()

with open('13428_2013_379_MOESM1_ESM.csv') as naps_file:
    naps_lines = naps_file.readlines()
naps_ids = [naps_id.split(';')[0] for naps_id in naps_lines]
# print(naps_ids)


pvs_col_ids = [2, 3, 4, 5]
naps_col_ids = [17, 19, 21, 25, 26, 27, 28, 29, 30, 31]
# pvs_col_ids = [2]
# naps_col_ids = [17]
for pvs_col_id in pvs_col_ids:
    for naps_col_id in naps_col_ids:
        make_chart(pvs_col_id, naps_col_id)
