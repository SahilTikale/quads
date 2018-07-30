import datetime
import sys
import argparse
import json
from pathlib2 import Path

backlog = Path("requestBackLog.json")



def initialize_backlog(filename, sch_req):
    """ Create a json file, with an empty list."""
    sch_req_list = []
    sch_req_list.append(sch_req)
    with open(filename, mode='w') as f:
        json.dump(sch_req_list, f)
    

def append_to_backlog(filename, sch_req):
    """ Appends input request data-structure to exisiting json file."""
    sch_req_list = json.loads(open(filename).read())
    sch_req_list.append(sch_req)
    with open(filename, mode='w') as f:
        json.dump(sch_req_list, f)
    
    
    

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--node_group", help="input the cluster type")
parser.add_argument("-q", "--qty", help="input the qty of Nodes required")
parser.add_argument("-tt", "--duration", help="No of days that nodes will be used. ")
parser.add_argument("-dt", "--start_date", nargs='+', type=int, help="Start date takes three values <year> <month> <day>")
parser.add_argument("-st", "--start_time",nargs='+', type=int, help="Start time takes two values <hour> <minute>")
parser.parse_args()

args = parser.parse_args()

if args.node_group:
    group_name=args.node_group
    print "group_name: "+group_name
    
if args.qty:
    node_qty=args.qty
    print "Number of nodes: "+args.qty

if args.duration:
    duration=args.duration
    print "Duration: "+duration+" weeks"

if args.start_date and args.start_time and args.duration:
    st_date = args.start_date
    st_time = args.start_time
    startdate_n_time = dict(
        year=st_date[0], month=st_date[1], day=st_date[2],
        hour=st_time[0], minute=st_time[1]
    )
    inputdate=datetime.datetime(**startdate_n_time)
    duration = datetime.timedelta(days=int(args.duration))
    print "Provisioning starts on: {}".format(inputdate)
    print "Provisioning duration ends on : {}".format(inputdate + duration)
    
elif args.start_date and args.duration:
    st_date = args.start_date
    startdate_n_time = dict(
        year=st_date[0], month=st_date[1], day=st_date[2]
        )
    duration = datetime.timedelta(days=int(args.duration))
    inputdate=datetime.datetime(**startdate_n_time)
    print "Provisioning starts on: {}".format(inputdate)
    print "Provisioning duration ends on : {}".format(inputdate + duration)
    print "Input Date is: {}".format(inputdate)

elif args.start_time:
    print "Please provide a start_date. Aborting."
    sys.exit(1)

    print args.start_time
    print type(args.start_time)
    t = datetime.time(args.start_time[0], args.start_time[1], args.start_time[2])
    print t, t.hour, t.minute, t.second
    print type(t.hour)
    print ("The time is {} hour {} minute and {} second".format(t.hour, t.minute, t.second))
    print "Creating a dictionary object from request."


if args.start_time:
    starting_at = args.start_date+args.start_time
else:
    starting_at = args.start_date
end_date = inputdate + duration
end_time = [ end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute ]    
sch_req = { 'group':args.node_group or None,
          'qty':args.qty or None,
          'begin':starting_at or None,
          'end': end_time,
          'duration':args.duration
    }


if backlog.is_file():
    append_to_backlog(backlog.name, sch_req)
else:
    initialize_backlog(backlog.name, sch_req)
    
#sch_req_list = []
#sch_req_list.append(sch_req)
#
#with open('schedule_req_register.json', mode='w') as f:
#    json.dump(sch_req_list, f)


request_list = json.loads(open('requestBackLog.json').read())
print request_list
print type(request_list)

#print json.dumps(sch_req)



# Converting dictionary to json
sch_req_json = json.dumps(sch_req)
# Converting json back to dictionary
sch_req_dict = json.loads(sch_req_json)

#print sch_req_json
#print sch_req_dict

#print " "
#print type(sch_req_dict)
#print sch_req_dict['1']['group']



#print end_date

#print end_date.year


#print "Ending on: {}".format(end_time)

    

sys.exit(0)

    



if (len(sys.argv) == 1):
    print "give some command line arguments. "
    print "Usage: "+sys.argv[0]+" <cluster_type> <node_qty> <duration> <start_time>"
else:
    group_name=sys.argv[1] or None
    node_qty=sys.argv[2] or None
    duration=sys.argv[3] or None  #In days
    days_from_now=sys.argv[4] or None
    start_time=sys.argv[5] or None

    print "Input request: "
    print "Node from cluster: "+group_name
    print "Number of nodes: "+node_qty
    print "Duration Requested: "+duration
    print "Starting at: "+stime
    print "Ending at: "

    


    
print len(sys.argv)


