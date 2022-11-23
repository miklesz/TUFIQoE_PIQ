# Standard library imports


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
    chart_name = f'{naps_col_name}({pvs_col_name})'
    print(chart_name)

    return
    chart_data = []
    for pvs_line in pvs_lines[1:]:
        pvs_line_elements = pvs_line.split(',')
        try:
            naps_id = naps_ids.index(pvs_line_elements[0][:-4])
        except ValueError as err:
            print(err)
        else:
            print(pvs_line_elements[0], naps_id)


with open('pvs/pvs_stats.csv') as pvs_file:
    pvs_lines = pvs_file.readlines()

with open('13428_2013_379_MOESM1_ESM.csv') as naps_file:
    naps_lines = naps_file.readlines()
naps_ids = [naps_id.split(';')[0] for naps_id in naps_lines]
# print(naps_ids)


pvs_col_ids = [2, 3, 4, 5]
naps_col_ids = [17, 19, 21, 25, 26, 27, 28, 29, 30, 31]
for pvs_col_id in pvs_col_ids:
    for naps_col_id in naps_col_ids:
        make_chart(pvs_col_id, naps_col_id)
