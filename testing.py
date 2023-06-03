import xml.etree.ElementTree as ET
import re

regex = r"[^0-9\.]+"

with open('testing_modify.xml', 'r') as f:
    tree = ET.parse(f)

list = []
counter_vehicles = 0

for vehicle in tree.findall("vehicle"):
    counter_vehicles+=1
    for attr in vehicle.attrib:
        if attr == "depart":
            list.append(vehicle.attrib[attr])

route_counter = 0
for route in tree.findall("route"):
    route_counter+=1

            
print(f'Number of routes: {route_counter}')
print(len(list))
list.sort()
import datetime
human_readable_time_list = [str(datetime.timedelta(seconds=float(x))) for x in list]
print(list[:10])
print(human_readable_time_list[:10])
print(human_readable_time_list[-9:])

#tree.write("testing_modify.xml", encoding="utf-8")

with open('bus_data/gtfs_pt_stops.add.xml', 'r') as f:
    tree = ET.parse(f)

busstop_counter = 0
for route in tree.findall("busStop"):
    busstop_counter+=1

print(f'Number of busstops: {busstop_counter}')