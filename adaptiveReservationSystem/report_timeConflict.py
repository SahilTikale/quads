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


