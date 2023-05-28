# This script is for preprocessing GTFS files from VBB to filter out unnecessary data.
import pandas as pd
from enum import Enum
import csv
import zipfile
import os
import shutil


gtfsFile = 'GTFS.zip' # Write here the path of the GTFS.zip file. Otherwise you can also create a GTFS named directory and extract it manually to that directory. Note: When your GTFS files are in the same directory as the GTFS.zip, you can write 'GTFS.zip' instead of the path
extractGTFS = True  # if you want to extract the GTFS.zip manually then write False and check if the extractDirName Variable has the same name as your directory with the extracted GTFS files
extractDirName = 'GTFS'  # you can change the name of the directory of the unfiltered extracted GTFS files. Notice: if you want to extract the GTFS.zip manually, you should write the name of the directory here. Otherwise write GTFS
filteredGTFSDirName = 'GTFS_filtered'  # thats the output name of the directory / .zip file with the filtered files
zipFilteredDir = True  # if you want to zip the filtered output, type in: True

# Write here the type of public transport that should be considered
class FilterType(Enum):
    BUS=True
    TRAM=False
    FERRIES=False
    UBAHN=False
    SBAHN=False

# Write here the agency_id for the agency to be included in the dataset
class AgencyId(Enum):
    AGENCY=[796] # for BVG this should be 796, for SBahn 1; If you want to filter for multiple agencies write it as a list like this: [796, 1]

# change the vehicle_id if necessary
class Vehicle(Enum):
    BUS=700
    TRAM=900
    FERRIES=1000
    UBAHN=402
    SBAHN=109

# exclude Schienenersatzverkehr from filtering (=> U-Bahn und Tram)
excludedLines = "^(^U|M[?=\d]{1}$|M10$|M13$|M17$)"

# You can change the filenames of the GTFS files
agencyFile = 'agency.txt'
routeFile = 'routes.txt'
tripsFile = 'trips.txt'
stoptimesFile = 'stop_times.txt'
stopsFile = 'stops.txt'
transfersFile = 'transfers.txt'
pathwaysFile = 'pathways.txt'
shapesFile = 'shapes.txt'
calendarDatesFile = 'calendar_dates.txt'
calendarFile = 'calendar.txt'
frequenciesFile = 'frequencies.txt'
levelsFile = 'levels.txt'



#### Notice: The following code is for functionality and does not need to be changed

if(extractGTFS):
    with zipfile.ZipFile(gtfsFile, 'r') as zip_ref:
        zip_ref.extractall('GTFS')

if not os.path.exists(filteredGTFSDirName):
   os.makedirs(filteredGTFSDirName)
shutil.copy2(extractDirName + '/' + calendarDatesFile, filteredGTFSDirName+'/calendar_dates.txt')
shutil.copy2(extractDirName + '/' + calendarFile, filteredGTFSDirName+'/calendar.txt') 
shutil.copy2(extractDirName + '/' + frequenciesFile, filteredGTFSDirName+'/frequencies.txt')
shutil.copy2(extractDirName + '/' + levelsFile, filteredGTFSDirName+'/levels.txt') 

def removeEscapedChars(path):
    with open(path, "r+") as textfile:
        data = textfile.read()
        replacedEscapedChars= data.replace("\\","")
        textfile.seek(0)
        textfile.write(replacedEscapedChars)
        textfile.truncate()


# agency.txt
dataAgency = pd.read_csv(extractDirName + '/' + agencyFile, sep=",")
filterForAgency = dataAgency[dataAgency["agency_id"].apply(lambda x : x in AgencyId.AGENCY.value)]
removeUnnecessaryDataAgency = filterForAgency.drop(columns=["agency_phone","agency_lang"])
removeUnnecessaryDataAgency.to_csv(filteredGTFSDirName+'/agency.txt', sep=",", index = False, quoting=csv.QUOTE_NONNUMERIC)


# routes.txt
dataRoutes = pd.read_csv(extractDirName + '/' + routeFile, sep=",")
filterForRoutesAgency = dataRoutes[dataRoutes["agency_id"].apply(lambda x : x in AgencyId.AGENCY.value)]
filterForRoutesType = filterForRoutesAgency[filterForRoutesAgency["route_type"].apply(lambda x : (FilterType.BUS.value and x==Vehicle.BUS.value)
                                                                                      or (FilterType.TRAM.value and x==Vehicle.TRAM.value)
                                                                                      or (FilterType.FERRIES.value and x==Vehicle.FERRIES.value)
                                                                                      or (FilterType.UBAHN.value and x==Vehicle.UBAHN.value)
                                                                                      or (FilterType.SBAHN.value and x==Vehicle.SBAHN.value))]                                            
removeUnnecessaryDataRoutes = filterForRoutesType.drop(columns=["route_desc", "route_color","route_text_color","route_long_name"])

# remove Schienenersatzverkehr from routes.txt
removeSchienenersatzverkehr = removeUnnecessaryDataRoutes[removeUnnecessaryDataRoutes["route_short_name"].str.match(excludedLines) == False]
removeSchienenersatzverkehr.to_csv(filteredGTFSDirName+'/routes.txt', sep=",", index = False, quoting=csv.QUOTE_NONNUMERIC)


# trips.txt
# look for route_id in trips.txt and remove unnecessary data
dataRoutesNew = removeSchienenersatzverkehr
dataTrips = pd.read_csv(extractDirName + '/' + tripsFile, sep=",", dtype={'route_id': 'str', 'service_id': 'int', 'trip_id': 'int', 
                                                          'trip_headsign':'str','trip_short_name': 'str', 'direction_id': 'int','block_id':'str',
                                                            'shape_id':'int', 'wheelchair_accessible': 'int', 'bikes_allowed': 'int'})

filterForTrips = dataTrips[dataTrips["route_id"].isin(dataRoutesNew["route_id"])].copy()

columnsList="route_id","trip_headsign","trip_short_name","block_id",
for col in columnsList:
    if(col == "block_id"):
        filterForTrips[col] = filterForTrips[col].apply(lambda x: '"' + str(x) + '"' if(len(str(x))>3) else None)
    else: filterForTrips[col] = filterForTrips[col].apply(lambda x: '"' + str(x) + '"')

removeNaN = filterForTrips.replace('"nan"','""')
removeUnnecessaryDataRoutes = removeNaN.drop(columns=["wheelchair_accessible", "bikes_allowed"])
headerQuoted = removeUnnecessaryDataRoutes.rename(columns=lambda x: '"' + str(x) + '"')
headerQuoted.to_csv(filteredGTFSDirName+'/trips.txt', sep=",", index = False, doublequote=True, quoting=csv.QUOTE_NONE, escapechar="\\")
removeEscapedChars(filteredGTFSDirName+'/trips.txt')


# stop_times.txt
# look for trip_id in stop_times.txt and remove unnecessary data
dataTripsNew = filterForTrips
dataStopTimes = pd.read_csv(extractDirName + '/' + stoptimesFile, sep=",", dtype={'trip_id':'int','stop_id': 'str','stop_sequence': 'int',
                                                           'pickup_type':'int', 'drop_off_type': 'int','stop_headsign': 'str',
                                                           'arrival_time':'object','departure_time':'object'})
columnsList="stop_id", "stop_headsign"
for col in columnsList:
    dataStopTimes[col] = dataStopTimes[col].apply(lambda x: '"' + str(x) + '"')

dataStopTimes2 = dataStopTimes.replace('"nan"','""')

filterForStopTimes = dataStopTimes2[dataStopTimes2["trip_id"].isin(dataTripsNew["trip_id"])]
removeUnnecessaryDataRoutes = filterForStopTimes.drop(columns=["pickup_type", "drop_off_type"])
headerQuoted = removeUnnecessaryDataRoutes.rename(columns=lambda x: '"' + str(x) + '"')
headerQuoted.to_csv(filteredGTFSDirName+'/stop_times.txt', sep=",", index = False, quoting=csv.QUOTE_NONE, escapechar="\\")
removeEscapedChars(filteredGTFSDirName+'/stop_times.txt')


# stops.txt
# look for stop_id in stops.txt, compare it with stop_id in stop_times.txt and remove unnecessary data
dataStopTimesNew = filterForStopTimes
dataStops = pd.read_csv(extractDirName + '/' + stopsFile, sep=",", dtype={'trip_id':'int','stop_id': 'str','stop_sequence': 'int', 'pickup_type':'int',
                                                   'drop_off_type': 'int','stop_headsign': 'str', 'stop_lat':'str', 'stop_lon':'str',
                                                   'parent_station':'object'})
columnsList="stop_id","stop_code","stop_name","stop_desc","stop_lat","stop_lon","parent_station","platform_code","zone_id"
for col in columnsList:
    if(col == "parent_station"):
        dataStops["parent_station"] = dataStops["parent_station"].apply(lambda x: '"' + str(x) + '"' if(len(str(x))>3) else None)
    else: dataStops[col] = dataStops[col].apply(lambda x: '"' + str(x) + '"')

dataStops2 = dataStops.replace('"nan"','""')

filterForStops = dataStops2[dataStops2["stop_id"].isin(dataStopTimesNew["stop_id"])]
#filterForStops = dataStops2[dataStops2["stop_id"] == '"de:12054:900230025::1"']  # ignore this, it's for testing
removeUnnecessaryDataRoutes = filterForStops.drop(columns=["level_id"])
headerQuoted = removeUnnecessaryDataRoutes.rename(columns=lambda x: '"' + str(x) + '"')
headerQuoted.to_csv(filteredGTFSDirName+'/stops.txt', sep=",", index = False, doublequote=True, quoting=csv.QUOTE_NONE, escapechar="\\")
removeEscapedChars(filteredGTFSDirName+'/stops.txt')


# transfers.txt
# look for stop_id in transfers.txt, compare it with stop_id in stop.txt and remove unnecessary data
dataStopsNew = filterForStops
dataTransfers = pd.read_csv(extractDirName + '/' + transfersFile, sep=",")
stopId = dataStopsNew['stop_id'].apply(lambda x: x.split(':')[0]).drop_duplicates()
routeId = dataRoutesNew['route_id'].drop_duplicates()
tripId = dataTripsNew['trip_id'].drop_duplicates()
filterForTransfers = dataTransfers[(dataTransfers["from_stop_id"].isin(stopId)|dataTransfers["to_stop_id"].isin(stopId)
                                    |dataTransfers["from_route_id"].isin(routeId)|dataTransfers["to_route_id"].isin(routeId)
                                    |dataTransfers["from_trip_id"].isin(tripId)|dataTransfers["to_trip_id"].isin(tripId))].copy()

columnsList="from_stop_id","to_stop_id","from_route_id","to_route_id","from_trip_id","to_trip_id", "min_transfer_time"
for col in columnsList:
    if(col == "min_transfer_time"):
        filterForTransfers[col] = filterForTransfers[col].apply(lambda x: f'{x:.0f}' if(x>=0) else None)
    else: filterForTransfers[col] = filterForTransfers[col].apply(lambda x: '"' + str(x) + '"' if(len(str(x))>3) else None)

dataTransfers2 = filterForTransfers.replace('"nan"','""')

headerQuoted = dataTransfers2.rename(columns=lambda x: '"' + str(x) + '"')
headerQuoted.to_csv(filteredGTFSDirName+'/transfers.txt', sep=",", index = False, quoting=csv.QUOTE_NONE, escapechar="\\")
removeEscapedChars(filteredGTFSDirName+'/transfers.txt')


# pathways.txt
# look for stop_id in pathways.txt, compare it with stop_id in stop.txt and remove unnecessary data
dataPathways = pd.read_csv(extractDirName + '/' + pathwaysFile, sep=",", dtype={'pathway_id':'str'})
splittedPathways = dataPathways['from_stop_id'].apply(lambda x: x.split(':')[0]).drop_duplicates()
splittedPathways2 = dataPathways['to_stop_id'].apply(lambda x: x.split(':')[0]).drop_duplicates()
filterForPathways = dataPathways[(dataPathways["from_stop_id"].isin(splittedPathways)|dataPathways["to_stop_id"].isin(splittedPathways2))]
removeUnnecessaryDataRoutes = filterForPathways.drop(columns=["stair_count", "max_slope", "length", "traversal_time", "signposted_as"])
removeUnnecessaryDataRoutes.to_csv(filteredGTFSDirName+'/pathways.txt', sep=",", index = False, quoting=csv.QUOTE_NONNUMERIC)


# shapes.txt
# look for shape_id in shapes.txt, compare it with shape_id in trips.txt and remove unnecessary data
dataShapes = pd.read_csv(extractDirName + '/' + shapesFile, sep=",")
filterForShapes = dataShapes[dataShapes['shape_id'].isin(dataTripsNew['shape_id'])].copy()

for col in "shape_pt_lat", "shape_pt_lon":
    filterForShapes.loc[:,col]=filterForShapes[col].apply(lambda x: f'{x:.6f}')
    
filterForShapes.to_csv(filteredGTFSDirName+'/shapes.txt', sep=",", index = False, quoting=csv.QUOTE_NONE)

if(zipFilteredDir):
    shutil.make_archive(filteredGTFSDirName, 'zip', filteredGTFSDirName)