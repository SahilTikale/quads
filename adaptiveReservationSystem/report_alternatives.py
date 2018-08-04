import json
import datetime
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
newlist_ids = []
for i in newlist:
    newlist_ids.append(newlist.index(i))

#print "newlist_ids: {}".format(newlist_ids)

print "Input list as obtained."
print " "
for i in sch_req_list:
    print i
print " "
print " Input list sorted by end time. "
print " "

for i in newlist:
    print i




print " "
print " ********************************"
print " "

sol_list = []

for outer in newlist:
    outer_begintime_input = dict(
        year=outer['begin'][0],
        month=outer['begin'][1],
        day=outer['begin'][2]
    )
    outer_begintime = datetime.datetime(**outer_begintime_input)
    for inner in newlist:
        no_conflict = []
        if(newlist.index(inner) < newlist.index(outer)):
            #inner_req_no = newlist.index(inner)
            #print inner
            inner_endtime_input = dict(
                year=inner['end'][0],
                month=inner['end'][1],
                day=inner['end'][2],
            )
            inner_endtime = datetime.datetime(**inner_endtime_input)
            #print "comparing endtime of job {}: {} to begin time of job {}: {}".format(
            #    newlist.index(inner), inner_endtime, newlist.index(outer), outer_begintime)
            if (inner_endtime <= outer_begintime):
#                print "comparing endtime of job {}: {} to begin time of job {}: {} No time conflict".format(
#                newlist.index(inner), inner_endtime, newlist.index(outer), outer_begintime)
                no_conflict.append(newlist.index(inner))
                no_conflict.append(newlist.index(outer))
                sol_list.append(no_conflict)
            

result = []
for i in sol_list:
    x = 0
    for j in sol_list:
        if(sol_list.index(j) < sol_list.index(i)) and j[1] == i[0]:
            result.append(j + list(set(i) -set(j)))
            x = x+1
        if x == 0 and i not in result:
            result.append(i)

# Finding longest sequence of jobs that can be scheduled without time conflict.
result.sort(key=len)

# Finding longest sequence of jobs that maximize utilization.

max_duration = 0
max_duration_jobs = []
for i in result:
    total_duration = 0
    for j in i:
        total_duration += int(newlist[j]['duration'])

    if total_duration > max_duration:
        max_duration = total_duration
        max_duration_jobs = [(i, total_duration)]
    elif total_duration == max_duration and (i, total_duration) not in max_duration_jobs:
        max_duration_jobs.append((i, total_duration))

no_conflict_list_per_request = {}
for job in newlist:
    for pair in sol_list:
        if newlist.index(job) in pair:
            temp = list(pair)
            temp.remove(newlist.index(job))
            if newlist.index(job) not in no_conflict_list_per_request.keys():
                no_conflict_list_per_request[newlist.index(job)] = temp
            else:
                no_conflict_list_per_request[newlist.index(job)].append(temp[0])



print " Scheduling Alternatives "
print " "
print "Longest sequence of jobs that can be scheduled: {}".format(result[-1])
print " "
print " "
print "Longest sequence of jobs with max cluster utilization: {}".format(max_duration_jobs)
print " "
print " "
print " Other possible choices of job sequences: "
for i in sol_list:
    print i
print " "
print "Per job_req no conflict list:"
for i in no_conflict_list_per_request:
    print "{}:   {}".format(i, no_conflict_list_per_request[i])
print " "    
print " "
print " "

request_ids = []
for i in newlist:
    request_ids.append(newlist.index(i))
print "List of jobs that conflict with given job."    
for i in no_conflict_list_per_request:
    print "{} :  {}".format( i, list(set(request_ids) - set(no_conflict_list_per_request[i])))
#    print set(newlist_ids)
    #conflict_list = list(set(i) - set(newlist_ids))
#    print "{}: {}".format(i, list(set(no_conflict_list_per_request[i]) - newlist_ids))

    







