
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

hello there


## Setting up the datacenter with a switch named REDHAT and 10 nodes.

```
sudo ./create_datacenter.sh -fullsetup 10 redhat
```

