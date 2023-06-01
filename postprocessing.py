import xml.etree.ElementTree as ET
import re

pattern = '\D+'
test_string = "('207769938',)"
p = re.compile(pattern)
print(p.sub('ABC@', s))
results = re.findall(pattern, test_string)
print(results)

"""
with open('bus_data/gtfs_pt_vehicles.add.xml', 'r') as f:
    tree = ET.parse(f)

for route in tree.findall("route"):
    for a in route.attrib:
        if a == "id":
            print(route.attrib[a])
            route.attrib[a] = str(counter)
            counter = counter + 1
            #print("Success")
        #route.attrib[a] = route.attrib[a].replace("id", "123456")



tree.write("testing_modify.xml", encoding="utf-8")
"""

