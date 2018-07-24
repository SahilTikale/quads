Adaptive Reservation System (ARS)
======================================

For a cluster of bare-metal servers, ARS processes batch of node-reservations requests and
provides the best possible requests that can be allocated to maximize overall utilization of the cluster.


## Problem context:

  Bare-metal clusters are physical machines devoid of any operating system.
  Considering that there is a way to share these nodes among different users that need subset of the capacity of the cluster,
  we need a system to efficiently allocate these nodes efficiently such that many small, big, short-term and long-term reservations
  are made with least amount of intra-request conflict.


## Policy 1: Same cluster, constant quantity of nodes per request:

  In a given cluster, collect a finite number of reservation request and find the best subset of these requests that maximizes the
  overall utilization of the cluster. Note that each request may have different start and end time, that may be conflicting with
  other reservations. Basic version solves only for time-conflicts. It assumes that all requests ask for same number of nodes from
  the cluster.


## Policy 2: Same cluster, variable quantity of nodes per request:

  For requests that need different number of nodes. We will find the best fit of reservation request that do not time conflict
  and then among such subsets, choose the one that maximizes the overall utilization of cluster.

## Policy 3: Same cluster, variable quantity of nodes, priority based requests:


  