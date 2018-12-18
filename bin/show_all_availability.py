import yaml
import json
from datetime import datetime, timedelta
from pathlib2 import Path


def load_data_into_dict(data):
    """ Reads all the data stored in quads yaml file.
    converts it into a single dictionary object.
    """
    if data.is_file():
        with open(data.as_posix(), 'r') as file:
            quads = yaml.safe_load(file)
    return quads

def save_data_to_json(data, filename):
    """ Saves <data> (eg. dict, list etc) as json to <filename>. """
    with open(filename, 'w') as file_name:
        json.dump(data, file_name)

def calculate_availability(date_obj, input_schedule):
    """ Calculate availability of nodes for one day given by <date_obj>
    Segregated node availability type wise
    Return it as <result> dictionary object 
    """
    result = {'misc':[]} # Today's node availability will be found here.
    now_timestamp = date_obj.strftime("%s")
    print "DEBUG: Starting with total hosts: {}".format(len(quads['hosts']))
    for host in quads['hosts'].keys():
        host_name = host
        host_dict = quads['hosts'][host]
        last_key = host_dict['schedule'].keys()[-1]
        end_date = host_dict['schedule'][last_key]['end']
        end_obj = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
        end_timestamp = end_obj.strftime('%s')
        if now_timestamp > end_timestamp: # Node is available for scheduling
            # Adding node info to the results
            if 'type' in host_dict.keys():
                if host_dict['type'] in result.keys():
                    result[host_dict['type']].append(host)
                else:
                    result[host_dict['type']] = [host]
            else:
                result['misc'].append(host)
            quads['hosts'].pop(host)
    
    return result


def merge_results(dict_1, dict_2):
    """ Takes as an input a dictionary with key: value format as
    <string>:[list of items]. Merges the item list for common keys
    from dict_2 to dict_1. Adds new keys from dict_2 to dict_1
    Returns a merged dictionary
    """
    dict_3 = dict_1.copy()
    for	item in	dict_2:
        if item	in dict_3.keys():
            dict_3[item] = dict_3[item] + dict_2[item]
	else:
            dict_3[item] = dict_2[item]
    return dict_3

# Find the current availability as of now.
data = Path("../schedule.yaml")
quads = load_data_into_dict(data)

#date_obj = datetime(2018, 8, 15, 11, 34, 45, 247969)
date_obj = datetime.today() #date object set to current time.
date_obj = date_obj.replace(microsecond=0)
timestamp = date_obj.strftime("%s")
avail_nodes = {} # node availability per day will be found here.
busy_nodes = {}
interval = 1
total_nodes = len(quads['hosts'])
upuntil_today = {}

# Calculate all availability in the future:
while(len(quads['hosts']) > 0):
    print "Day: {} -- {}".format(interval, date_obj.strftime('%c'))
    only_today = calculate_availability(date_obj, quads)
    upuntil_today = merge_results(upuntil_today, only_today)
    avail_nodes[timestamp] = upuntil_today
    busy_nodes[timestamp] = len(quads['hosts'])
    date_obj = date_obj + timedelta(days=interval)
    timestamp = date_obj.strftime("%s")


save_data_to_json(avail_nodes, "all_availabilty.json")

print "********* RESULT DICTIONARY *************"

#print today_result.keys()
#print avail_nodes

print "*****************************************"

timestamps = avail_nodes.keys()
#print timestamps
timestamps.sort()

for timestamp in timestamps:
    dt_obj = datetime.fromtimestamp(float(timestamp))
    print " "
    print "Availability on {}".format(dt_obj.strftime('%c'))
    print "Node availability Type wise: "
    for node_types in avail_nodes[timestamp].keys():
        print " {:20s} :   {:5d}".format(node_types, len(avail_nodes[timestamp][node_types]))

    print "*"*35
    print " {:20s} :   {:5d}".format("Total Availability", (total_nodes - busy_nodes[timestamp]))
    print " {:20s} :   {:5d}".format("Nodes still busy", busy_nodes[timestamp])
    print " "
    
#print " ************* Raw data structure of available nodes ******************* "
#print avail_nodes

days = []
DellR630 = []
DellR620 = []
R620 = []
misc = []
type_1029p = []
total_avail = []
busy = []

for timestamp in timestamps:
    dt_obj = datetime.fromtimestamp(float(timestamp))
    free_nodes = 0
    days.append(dt_obj.isoformat())
    misc.append(len(avail_nodes[timestamp]['misc']))
    free_nodes += len(avail_nodes[timestamp]['misc'])
    R620.append(len(avail_nodes[timestamp]['R620']))
    free_nodes += len(avail_nodes[timestamp]['R620'])
    DellR620.append(len(avail_nodes[timestamp]['DellR620']))
    free_nodes += len(avail_nodes[timestamp]['DellR620'])
    DellR630.append(len(avail_nodes[timestamp]['DellR630']))
    free_nodes += len(avail_nodes[timestamp]['DellR630'])
    type_1029p.append(len(avail_nodes[timestamp]['1029p']))
    free_nodes += len(avail_nodes[timestamp]['1029p'])
    total_avail.append(free_nodes)
    busy.append(340-free_nodes)


print "*"*100
print "                          **** Node availability per day, sorted per type. ****"
print "*"*100

print "{:20s} {:10s} {:10s} {:10s} {:10s} {:10s} {:12s} {:12s} ".format("Days_time", "DellR630", "DellR620", "R620", "misc", "1029p", "Total_free", "Still Busy")

for day, x, y, z, m, t, free, not_free in zip(days, DellR630, DellR620, R620, misc, type_1029p, total_avail, busy):
    print "{:20s} {:8d} {:10d} {:10d} {:10d} {:10d} {:12d} {:12d} ".format(day, x, y, z, m, t, free, not_free)

    
print " "*100
print "*"*100
