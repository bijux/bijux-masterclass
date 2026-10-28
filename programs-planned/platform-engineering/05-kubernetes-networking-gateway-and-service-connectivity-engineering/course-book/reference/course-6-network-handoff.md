# Course 6 network handoff

Storage and stateful workloads inherit these network facts:

- namespace and workload inventory;
- Service names, ports, and DNS contracts;
- Pod/Service address-family expectations;
- default-deny baseline and storage-related policy gaps;
- Gateway and public TLS boundary;
- egress and private-connectivity rules;
- topology and traffic-policy assumptions;
- MTU and source-identity behavior;
- unresolved CNI, cloud, and multi-zone evidence.

The handoff does not claim that API traffic evidence proves CSI, database replication, snapshot, backup, restore, or fencing paths. Course 6 must define and test those separately.
