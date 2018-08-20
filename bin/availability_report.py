import yaml
from datetime import datetime, timedelta
from pathlib2 import Path

data = Path("../schedule.yaml")

quads = {}
print "size of quads dictionary: {}".format(len(quads))

def load_data_into_dict(data):
    global quads

    if data.is_file():
        with open(data.as_posix(), 'r') as file:
            quads = yaml.safe_load(file)


load_data_into_dict(data)

print type(quads)
print "size of quads dictionary: {}".format(len(quads))

result = {'misc':[]}

# Find the current availability as of now.
now_obj = datetime.today()
now_timestamp = now_obj.strftime("%s")

print "Total hosts: {}".format(len(quads['hosts']))

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

print " "
print result
print " "
print "Nodes ready for scheduling today"
for item in result.keys():
    print " {}:  {}".format(item, len(result[item]))
                            
print "Nodes Still busy as of today: {}".format(len(quads['hosts']))
