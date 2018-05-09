import sys
from subprocess import call, check_call, check_output
import ast
import time

import initialize_hil

hil = initialize_hil.client

class FailedAPICallException(Exception):
    """An exception indicating that the server returned an error.

    Attributes:

        error_type (str): the type of the error. 
        message (str): a human readble description of the error.
    """

#Take input
host = sys.argv[1]
old_cloud = sys.argv[2]
new_cloud = sys.argv[3]

default_allocator = "HIL"
## debugging ##
print "host: "+host
print "old_cloud: "+old_cloud
print "new_cloud: "+new_cloud

## Fetching needed info from QUADS
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

# Parsing output into a dictionary
host_info = ast.literal_eval(host_output)
nics = ast.literal_eval(host_info['interfaces'])
nic = nics.keys()[0]
oldcloud_info = ast.literal_eval(oldcloud_output)
newcloud_info = ast.literal_eval(newcloud_output)


# Check to avoid mixing nodes and networks from HIL and QUADS.
# Cannot move a HIL node into QUADS network and vica versa. Abort any such request.
# The only exception is 'cloud01' as it is a default cloud for all nodes when they are
# not assigned. More like a 'free pool' in HIL.
if old_cloud == 'cloud01':
    alloc_list = [ host_info['allocator'], newcloud_info['allocator'] ]
elif new_cloud == 'cloud01':
    alloc_list = [ host_info['allocator'], oldcloud_info['allocator'] ]
else: 
    alloc_list = [ 
            host_info['allocator'], oldcloud_info['allocator'], 
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

def check_status(result, ticket):
    """ Polls network server of HIL to check if the
    allocated network job (attach, detach network) is completed.
    """
    while result['status'] != 'DONE':
        time.sleep(1)
        try:
            result = hil.node.show_networking_action(ticket['status_id'])
        except FailedAPICallException as e:
            return e
    return result['status']


def detach_node(host, nic, cloud):
    """ HIL detaches network from nic of node.
    """
    ticket = hil.node.detach_network(host, nic, cloud)
    result = hil.node.show_networking_action(ticket['status_id'])
    status = check_status(result, ticket)
    if status == 'DONE':
        print "Successfull detached from "+cloud
        hil.node.show(host)
    else:
        print "Network detach operation failed: "+status
        exit(1)

def attach_node(host, nic, cloud):
    """ HIL Attaches node to nic of network 
    in vlan/native mode.
    """

    channel='vlan/native'
    ticket = hil.node.connect_network(host, nic, cloud, channel)
    result = hil.node.show_networking_action(ticket['status_id'])
    status = check_status(result, ticket)
    if status == 'DONE':
        print "Successfull attached to "+cloud
        hil.node.show(host)
    else:
        print "Network attach operation failed: "+status
        exit(1)


def migrate_node(host, nic, oldCloud, newCloud):
    """ Moves host from oldCloud to newCloud in QUADS.
    Makes corresponding network changes on switch using
    HIL.
    """
    if oldCloud == 'cloud01':
        print "Moving node from default cloud to "+newCloud
        attach_node(host, nic, newCloud) # HIL making changes to switch
    elif newCloud == 'cloud01':
        print "Moving node from "+oldCloud+" to default cloud."
        detach_node(host, nic, oldCloud) # HIL makes changes to switch
    else:
        print "Moving node from "+oldCloud+" to new cloud "+newCloud
        detach_node(host, nic, oldCloud) # HIL makes changes to switch
        attach_node(host, nic, newCloud) # HIL making changes to switch
    # Updating corresponding changes to QUADS
    update_cloud = ['./quads-cli', '--modify-host', host, '--default-cloud', newCloud ]
    check_output(update_cloud)
    print "Successfully moved node from "+oldCloud+" to default cloud: "+newCloud

migrate_node(host, nic, old_cloud, new_cloud)
