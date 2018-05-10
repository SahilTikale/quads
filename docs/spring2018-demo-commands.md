
 Integrating QUADS with HIL 
=========================== 

Spring 2018 status report

## Agenda:

* [Background](#background)
* [DEMO 1 Datacenter in a laptop](#demo-1-datacenter-in-a-laptop)
* [Introducing HIL into QUADS](#introducing-hil-into-quads) 
* [New APIs and CLIs added to QUADS](#new-apis-and-clis-added-to-quads)
* [DEMO 2 HIL managing network isolation for QUADS](#demo-2-hil-managing-network-isolation-for-quads)
  * Inquiring about the allocator (HIL)
  * Automatic host registration in QUADS from HIL
  * Automatic cloud registration in QUADS from HIL
  * Fetching per node info
  * Fetching per cloud info
  * Script that moves host between clouds
* Going from here

## If Time permits:
* Things to do

## Background

* Hardware Isolation Layer or [HIL](https://github.com/CCI-MOC/hil) is a micro-service that performs the following functions:
  * **Administer networks across different switches:** Provides users with a single switch agnostic interface to manage multitude of switches, without having to know any switch specific info.
  * **Proxies OBM interface:** Users can power cycle nodes, set boot devices etc., without having to know the IPMI passwords. 
  * **Provides user access control:** Unauthorized users cannot powercycle nodes or administer networks.
  
* Advantages for QUADS:
  * QUADS can run on a wide variety of infrastructure. Not just juniper switches.
  * No additional administration overhead. Set once, use multiple times (IPMI passwords, host information etc)
  

## Demo 1 Datacenter in a laptop:
* This simulates a simple datacenter model with 10 hosts connected to a switch. 
* The following commands will help you set a cluster of 10 hosts (network name spaces) connected to a openvswitch.
* Using the script [create_datacenter.sh](https://github.com/SahilTikale/HIL_contrib/blob/master/hilInYourLap/create_datacenter.sh) you also can create this setup in a fedora VM.
```bash
sudo ./create_datacenter.sh -fullsetup 10 redhat
```
* Setup DHCP servers for two networks (vlan 100 and 200):
* Setup a host (network namespace) that runs a DHCP server for vlan 100:
```bash
sudo ./create_datacenter.sh -setDHCP redhat 100 10.1.100.2/24 10.1.100.10,10.1.100.50,255.255.255.0
```
* Setup a host (network namespace) that runs a DHCP server for vlan 200:
```bash
sudo ./create_datacenter.sh -setDHCP redhat 200 10.1.200.2/24 10.1.200.10,10.1.200.50,255.255.255.0
```
* Commands to confirm the successful setup:
```bash
ps -ef |grep tap
sudo ip netns identify <pid found from previous command>
sudo ip netns exec
sudo ip netns exec dhcp_100 ip a
```
* HIL has an openvswitch driver to manage the above decribed setup. Install it, set it up.
* In a real datacenter that would involve:
* Populating per host info like: ipmi password, network interface, mac address etc
* Populating per switch authentication info: ip address, authentication info(user, password, public key etc)
* Exact steps are not covered here for brevity. You can find them [on github](https://github.com/CCI-MOC/hil) or by refering to [HIL documentation](http://hil.readthedocs.io/en/latest/)

## Introducing HIL into QUADS
* Assuming that datacenter-in-a-laptop exists and HIL is setup correctly, install QUADS from github as [described here](https://github.com/SahilTikale/quads#installing-quads-from-github)
* Following steps introduces HIL into QUADS setup as follows:
* QUADS uses `quads/conf/quads.yml` to configure its changes. I added following additional parameters.
```yaml
#Enable external Host allocator
allocator_activated: true   #If this is False all of the allocator related QUADS calls will return error stating so.
allocator_name: HIL         #It can be a list if QUADS interfaces with multiple allocators. eg [REDHAT's-HIL, MOC-HIL, FLOCX]
                            #For each allocator the following info may vary, or may need additional parameters.
allocator_url: http://127.0.0.1:6000
allocator_project_name: quads  # Project is how HIL shared nodes and networks among multiple users.
allocator_username: quads_user # Quads can access nodes allocated only to its own project.
allocator_password: quads
```
* HIL is a RESTful api micro-service. I have written a client library to make it easy for other systems (like QUADS) to consume these APIs.
* Following modifications were done to introduce HIL client library into QUADS code-base.
 * Copied the [hil client library](https://github.com/CCI-MOC/hil/tree/master/hil/client) to quads as `quads/lib/hil_client_lib`
 * Added a script to `quads/bin/initialize_hil.py` that is used by `quads/bin/quads-cli` to setup connection to HIL using relevant credentials.

## New APIs and CLIs added to QUADS
 
* Later following calls were added to `quads/bin/quads-cli`, some of them required writing **new APIs in QUADS**.
```bash
  --ls-allocator        Outputs name of the external allocator 
  --ls-hil-nodes        lists all nodes available with HIL
  --ls-allocated-nodes  lists nodes allocated to QUADS project with HIL
  --ls-allocated-networks
                        lists networks allocated to QUADS project with HIL
  --allocator ALLOCATOR
                        Defined allocator for a host or cloud
  --fetch-allocated-nodes
                        Fetches nodes from external allocator
  --fetch-allocated-networks
                        Fetches networks from external allocator
  --modify-host MODIFYHOSTRESOURCE
                        modify attributes of a host resource
  --host-interfaces HOSTINTERFACES
                        interfacename:mac_addresses separated by whitespace
  --cloud-vlan CLOUDVLAN
                        permissible integer range for vlans
  --show-host HOSTINFO  All information regarding host
  --show-cloud CLOUDINFO
                        All information regarding cloud
                       
 ```
 * Modified some of the existing APIs:
 `/api/v1/host` : Now requires: `--allocator` and `--host-interfaces` 
 `/api/v1/cloud`: Now requrires: `--allocator` and `--cloud-vlan`
 
 * Added following APIs and corresponding CLIs:
 `/api/v1/modifyhost`: Updates the cloud allocation of a given node. 
 `/api/v1/allhostinfo`: returns all attributes specific to a host definition from `schedule.yaml` 
 `/api/vi/allcloudinfo`: returns all attributes specific to a cloud definition from `schedule.yaml`
 
 * Made changes to the QUADS data structure to accomodate the idea of external allocator.
 
 ## DEMO 2 HIL managing network isolation for QUADS






