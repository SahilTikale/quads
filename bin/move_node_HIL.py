import sys
from subprocess import call, check_call, check_output
import ast
import time

import initialize_hil
hil = initialize_hil.client


#Take input
host = sys.argv[1]
old_cloud = sys.argv[2]
new_cloud = sys.argv[3]

default_allocator = "HIL"
move_into = False
move_from = False




print "host: "+host
print "old_cloud: "+old_cloud
print "new_cloud: "+new_cloud


host_args = ['./quads-cli', '--show-host', host]
oldcloud_args = ['./quads-cli', '--show-cloud', old_cloud]
newcloud_args = ['./quads-cli', '--show-cloud', new_cloud]

host_output = check_output(host_args)
oldcloud_output = check_output(oldcloud_args)
newcloud_output = check_output(newcloud_args)

# Input Validation
for output in [ host_output, oldcloud_output, newcloud_output ]:
    if 'Error' in output:
        print "Aborting Script: "+output
        exit(1)

host_info = ast.literal_eval(host_output)
nics = ast.literal_eval(host_info['interfaces'])
nic = nics.keys()[0]
old_cloud_info = ast.literal_eval(oldcloud_output)
newcloud_info = ast.literal_eval(newcloud_output)

if old_cloud == 'cloud01':
    alloc_list = [ host_info['allocator'], newcloud_info['allocator'] ]
    move_into = True
elif new_cloud == 'cloud01':
    alloc_list = [ host_info['allocator'], oldcloud_info['allocator'] ]
    move_from = True
else: 
    alloc_list = [ 
            host_info['allocator'], old_cloud_info['allocator'], 
            newcloud_info['allocator']         
            ]


# Allocator Validation
for allocator in alloc_list: 
    if allocator == default_allocator:
        print "All objects belong to allocator: "+ allocator
    else:
        print "Error: allocator mismatch "+allocator + " is different than "+ default_allocator
        print "Aborting script"
        exit(1)

def move_from_DefaultCloud(host, oldCloud, newCloud):

    update_cloud = ['./quads-cli', '--modify-host', host, '--default-cloud', newCloud ]
    pass

def move_into_DefaultCloud(host, oldCloud, newCloud):
    """ HIL detaches node from network of oldCloud, 
    QUADS updates its datastructure that the node belongs to 
    default cloud.
    """
    ticket = hil.node.detach_network(host, nic, oldCloud)
    result = hil.node.show_networking_action(ticket['status_id'])
    while result['status'] != 'DONE':
        time.sleep(1)
        try:
            result = hil.node.show_networking_action(ticket['status_id'])
        except FailedAPICallException as e:
            print e
            exit(1)

    update_cloud = ['./quads-cli', '--modify-host', host, '--default-cloud', newCloud ]
    print "Successfully moved node from "+oldCloud+" to default cloud: "+newCloud

def move_from_old_to_new(host, oldCloud, newCloud):
    update_cloud = ['./quads-cli', '--modify-host', host, '--default-cloud', newCloud ]
    pass










print "Output: "
print host_output

print " "

print ast.literal_eval(host_output)

print "Default Allocator: "+allocator

