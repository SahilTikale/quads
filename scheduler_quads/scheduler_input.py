import datetime
import sys
import argparse


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
    
elif args.start_date:
    st_date = args.start_date
    startdate_n_time = dict(
        year=st_date[0], month=st_date[1], day=st_date[2]
        )
    inputdate=datetime.datetime(**startdate_n_time)
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


