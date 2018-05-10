
 Integrating QUADS with HIL 
=========================== 

Spring 2018 status report

## Agenda:

* [Background](#background)
* DEMO: Reflecting the real setup in a datacenter.
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
  


## Setting up the datacenter with a switch named REDHAT and 10 nodes.

```
sudo ./create_datacenter.sh -fullsetup 10 redhat
```

