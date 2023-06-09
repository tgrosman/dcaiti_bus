import xml.etree.ElementTree as ET
import re
import pandas as pd

regex = r"[^0-9\.]+"

with open('testing_modify.xml', 'r') as f:
    tree = ET.parse(f)

route_list = []
counter_vehicles = 0

for vehicle in tree.findall("vehicle"):
    counter_vehicles+=1
    for attr in vehicle.attrib:
        if attr == "depart":
            route_list.append(vehicle.attrib[attr])

route_counter = 0
for route in tree.findall("route"):
    route_counter+=1#

            
print(f'Number of routes: {route_counter}')
#print(len(route_list))
print(f'Number of vehicles: {counter_vehicles}')
route_list.sort()
import datetime
human_readable_time_list = [str(datetime.timedelta(seconds=float(x))) for x in route_list]
#print(route_list[:10])
#print(human_readable_time_list[:10])
#print(human_readable_time_list[-9:])

#tree.write("testing_modify.xml", encoding="utf-8")

with open('bus_data/gtfs_pt_stops.add.xml', 'r') as f:
    tree = ET.parse(f)
busstop_names = []
busstop_counter = 0
busstop_id_list = []
for busstop in tree.findall("busStop"):
    busstop_id_list.append(busstop.attrib['id'])
    busstop_names.append(busstop.attrib['name'])

print(f'Number of busstops: {len(busstop_id_list)}')

with open('bus_data/gtfs_pt_vehicles.add.xml', 'r') as f:
    tree = ET.parse(f)

busline_list = []
for vehicle in tree.getroot().iter('param'):
    if vehicle.attrib['key'] == 'gtfs.route_name':
        busline_list.append(vehicle.attrib['value'])

#print(len(busline_list))
busline_list = list(dict.fromkeys(busline_list))
print(f'Number of unique buslines: {len(busline_list)}')
#print(busline_list)
trimmed_buses_depart_time  = [75650, 78050, 16790, 16670, 17870]
trimmed_buses_depart_time = [str(datetime.timedelta(seconds=x)) for x in trimmed_buses_depart_time]
print(trimmed_buses_depart_time)

trimmed_vehicles = ["('207919866',).0", "('207919867',).0", "('207955877',).0", "('207972152',).0", "('207972153',).0"]
bus_lines_of_interest = [221, 170 , 110]
headsign_list = []
for vehicle in tree.findall('vehicle'):
    if any(vehicle.attrib['id'] == id for id in trimmed_vehicles):
        for bus_line in bus_lines_of_interest:
            if vehicle[0].attrib['value'] == str(bus_line):
                tmp = {"route": vehicle.attrib['route'], bus_line:vehicle[1].attrib['value'], 'depart': str(datetime.timedelta(seconds=float(vehicle.attrib['depart'])))}
                headsign_list.append(tmp)



def get_route_ids_by_headsign(headsign: str) -> list:
    tmp_list = []
    for vehicle in tree.findall('vehicle'):
        if vehicle[1].attrib['value'] == headsign:
            tmp_list.append(vehicle.attrib['route'])
    tmp_list = list(dict.fromkeys(tmp_list))
    return tmp_list


headsign_of_interest = 'U Oskar-Helene-Heim (Berlin)'
print(f'Route IDs by headsign: {get_route_ids_by_headsign(headsign_of_interest)}')
"""
for child in tree.getroot().iter('vehicle'):
    for bus_line in bus_lines_of_interest:
        if child[0].attrib['value'] == str(bus_line):
            print(child[1].attrib['value'])
            headsign_list.append(child[1].attrib['value'])
"""
    
print(f'Headsigns of trimmed lines: {headsign_list}')

dt_routes = pd.read_csv('routes_date.csv')
#print(dt_routes.head())
routes_name = dt_routes['route_short_name'].values.tolist()
import collections
print([item for item, count in collections.Counter(routes_name).items() if count > 1])
#print(f'Duplicate route: {duplicate_route_gtfs}')
#print(len(list(dict.fromkeys(routes_name))))
#print(busline_list)
#diff_routes = list(set(busline_list) - set(routes_name))
#print(diff_routes)

dt_stops = pd.read_csv('stops_date.csv')
#print(dt_stops.head())
stops_name = dt_stops['stop_name'].values.tolist()
#print(f'Hier: {len(list(dict.fromkeys(stops_name)))}')
print(len(stops_name))
print(len(busstop_names))


def entry_part_of_two_lists(list_1: list [str], list_2: list [str]) -> list [str]:
    tmp_list = []
    for element_1 in list_1:
        if element_1 in list_2:
            tmp_list.append(element_1)
    return tmp_list



busstop_names.sort()
stops_name.sort()
#print(busstop_names[:10])
print(stops_name[:10])
from collections import Counter
print('Linie')
counter_stops_name = Counter(stops_name)
counter_busstop_names = Counter(busstop_names)
print(counter_stops_name['Abgeordnetenhaus (Berlin)'])
print(counter_busstop_names['Abgeordnetenhaus (Berlin)'])
shared_items = {k: counter_busstop_names[k] for k in counter_busstop_names if k in counter_stops_name and counter_busstop_names[k] == counter_stops_name[k]}
print(shared_items)
print(sum(counter_stops_name.values()))
print(sum(counter_busstop_names.values()))
"""
same_list = entry_part_of_two_lists(busstop_names, stops_name)
print(len(same_list))

def get_difference(list_1: list [str], list_2: list [str]) -> list [str]:
    tmp_list = []
    for element_1 in list_1:
        if not element_1 in list_2:
            tmp_list.append(element_1)
    return tmp_list


diff_list = get_difference(stops_name, busstop_names)
print(len(diff_list))
#print(diff_list)
"""