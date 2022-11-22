with open('13428_2013_379_MOESM1_ESM.csv') as naps_file:
    naps_lines = naps_file.readlines()
naps_ids = [naps_id.split(';')[0] for naps_id in naps_lines]
print(naps_ids)

with open('pvs/pvs_stats.csv') as pvs_file:
    pvs_lines = pvs_file.readlines()

chart_data = []
for pvs_line in pvs_lines[1:]:
    pvs_line_elements = pvs_line.split(',')
    try:
        naps_id = naps_ids.index(pvs_line_elements[0][:-4])
    except ValueError as err:
        print(err)
    else:
        print(pvs_line_elements[0], naps_id)
