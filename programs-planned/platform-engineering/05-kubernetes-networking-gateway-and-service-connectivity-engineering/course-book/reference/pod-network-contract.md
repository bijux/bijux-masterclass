# Pod network contract

A Pod network release should state:

- how the runtime invokes the CNI chain;
- stable attachment identity and generation;
- address families and atomic allocation behavior;
- Pod CIDR ownership and overlap rules;
- default routes and exceptions;
- underlay or overlay path;
- MTU calculation;
- source-address behavior;
- policy enforcement location;
- Node-loss and stale-allocation recovery;
- plugin readiness and garbage collection;
- observability at namespace, Node, and implementation levels.

The contract must distinguish intended Kubernetes network properties from implementation evidence. “Every Pod gets an IP” does not describe allocation conflicts, partial attachment, cleanup, or route convergence.
