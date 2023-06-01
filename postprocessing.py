import xml.etree.ElementTree as ET
import re

regex = r"[^0-9\.]+"

with open('bus_data/gtfs_pt_vehicles.add.xml', 'r') as f:
    tree = ET.parse(f)

for route in tree.findall("route"):
    for a in route.attrib:
        if a == "id":
            new_id = re.sub(regex, "", route.attrib[a], 0, re.MULTILINE)
            route.attrib[a] = new_id

for vehicle in tree.findall("vehicle"):
    for attr in vehicle.attrib:
        if attr == "id" or attr == "route" or attr == "line":
            new_id = re.sub(regex, "", vehicle.attrib[attr], 0, re.MULTILINE)
            vehicle.attrib[attr] = new_id


tree.write("testing_modify.xml", encoding="utf-8")


