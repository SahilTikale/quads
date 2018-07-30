import json
import sys
from operator import itemgetter
from pathlib2 import Path

""" Following module reads from the backlog.json and reports the list of jobs that can be scheduled.
Input: list of dictionaries, Each dictionary is a job scheduling request.
Output: List of list of dictionary: Each inner list is a list of dictionaries 
        Stating which jobs can be scheduled toghether sorted by start time.
"""


backlog = Path("requestBackLog.json")

if backlog.is_file():
    sch_req_list = json.loads(open(backlog.name).read())
else:
    print "Error: File "+backlog.name+" not found."
    print "Aborting."
    sys.exit(1)



newlist = sorted(sch_req_list, key=itemgetter('end'))

print "Input list as obtained."

for i in sch_req_list:
    print i

print " Input list sorted by end time. "

for i in newlist:
    print i

for i in newlist:
    print newlist.index(i)

sol_list = []

for outer in newlist:
    outer_req_no = newlist.index(i)
    if outer_req_no == 0:
        # If the item is first in new list put it in its own solution list.
        sol = [outer_req_no]
        sol_list.append(sol)
    else:
        # create an end time object from list to key 'end'
        outer_endtime_input = dict(
        year=outer['end'][0], month=outer['end'][1], day=outer['end'][2],
        hour=outer['end'][3], minute=outer['end'][4]
    )
        outer_endtime = datetime.datetime(**outer_endtime_input)
        for inner in newlist:
            inner_req_no = newlist.index(i)
            inner_endtime_input = dict(
                year=inner['end'][0], month=inner['end'][1],
                day=inner['end'][2],
                hour=inner['end'][3], minute=inner['end'][4]
            )
	    inner_endtime =	datetime.datetime(**inner_endtime_input)
        
        
        
        

    
    
