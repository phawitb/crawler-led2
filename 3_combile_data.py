import json 
import sys
from datetime import datetime
import csv

province = 'nonthaburi'
# province = sys.argv[1]

print('\n\n\n','='*200)
print('3_combile_data')

try:
    with open(f'data/{province}_currentlink.json', 'r') as openfile:
        C = json.load(openfile)
except:
    C = {}
try:
    with open(f'data/{province}_led.json', 'r') as openfile:
        D = json.load(openfile)
except:
    D = {}
try:
    with open(f'data/{province}_gps_data.json', 'r') as openfile:
        G = json.load(openfile)
except:
    G = {}

last_day_key = str(max([int(x) for x in C.keys()]))
print('last_day_key',last_day_key)

# for k in C.keys():
print(C[last_day_key].keys())

CB = {}
for l in C[last_day_key].keys():
    page = l
    url = C[last_day_key][l]
    data = D[url]

    # data['gps_data'] = G
    print('\n\n\n')
    dd = data['deed_number'].split(',')
    print('deed_number',dd)
    g = {}
    for d in dd:
        g[d] = G[d]
        # print(d,G[d])
    # print('gggg',g)
    data['gps_data'] = g
    print(page,url,data)
    CB[page] = {
        'link' : url,
        'data' : data
    }

# combile_data = {}
# for page in list(C[last_day_key].keys()):
#     link = C[last_day_key][page]
#     if link in D.keys():
#         # data = D[link]

#         # print()

#         if 'deed_number' in D[link].keys():
#             gps = {}
#             for d in data['deed_number']:
#                 if str(d) in G.keys():
#                     gps[str(d)] = G[str(d)]
#             data['gps_data'] = gps
 
#         combile_data[page] = {
#             'link' : link,
#             'data' : data
#         }

with open(f"data/{province}_combile_last.json", "w") as outfile:
    outfile.write(json.dumps(CB, indent=4))

with open('data/log.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([datetime.now(),'3_combile_data','finish', province])

print('combile data complete!!')