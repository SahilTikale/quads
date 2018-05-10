
 Integrating QUADS with HIL 
=========================== 

Spring 2018 status report

## Agenda:

* [Background](#background)
* [DEMO 1 Datacenter in a laptop](#demo-1-datacenter-in-a-laptop)
* Introducing HIL into QUADS 
* List of calls added to QUADS (cli and api)
* Changes made to QUADS datastructure (schedule.yaml)
* DEMO: 
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




