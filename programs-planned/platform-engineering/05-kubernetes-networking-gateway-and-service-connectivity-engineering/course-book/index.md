# Kubernetes Networking, Gateway, and Service Connectivity Engineering

Course 5 turns the Kubernetes workload from Course 4 into a deliberate connectivity system. The subject is not “how to expose a Service.” It is the complete chain from application socket to network namespace, Pod address, Node forwarding path, Service membership, DNS, policy, Gateway, TLS, egress, topology, and operational evidence.

## Governing question

> Which component owns each network transition, what invariants must survive it, and how do we locate the earliest transition that failed?

## Course progression

```text
Course 1 — operate the Linux and network substrate
Course 2 — codify the cloud foundation
Course 3 — package and verify the OCI workload
Course 4 — reconcile the workload through Kubernetes controllers
Course 5 — connect, discover, segment, expose, and diagnose it
Course 6 — persist state and recover data across those exact paths
```

## Modules

1. Kubernetes network model, address domains, and packet paths
2. CNI lifecycle, IPAM, routes, and Node integration
3. Services, EndpointSlices, and Service data planes
4. DNS and Service discovery
5. NetworkPolicy and L3/L4 segmentation
6. Traffic locality, source identity, and dual stack
7. Gateway API architecture and Route ownership
8. TLS, HTTP semantics, and backend protocol integrity
9. Egress, external services, and service-mesh boundaries
10. Network operations, conformance, and release

## Graduate capability

A successful learner can take an observed symptom such as “the request times out” and separate it into testable transitions. They can determine whether the cause is resolver state, route selection, CNI attachment, EndpointSlice membership, stale Service programming, NetworkPolicy, Gateway attachment, certificate validation, source translation, egress peer mismatch, MTU, or application behavior.

They can also design the network before failure:

- declare address domains and overlap rules;
- choose hard and soft locality deliberately;
- preserve readiness and shutdown semantics;
- build default-deny policy from an owned flow inventory;
- separate transport source, forwarded identity, and authenticated principal;
- publish Gateway and TLS boundaries without overclaiming end-to-end trust;
- validate outbound hostnames and connected peers;
- reject a service mesh when no named capability justifies it;
- release only the features and environments for which evidence exists.

## What is deferred

Course 5 deliberately does not claim:

- durable database, CSI, snapshot, or backup behavior;
- fleet-wide multi-cluster networking;
- complete workload identity and admission policy;
- production load, capacity, or cost evidence;
- operated certificate automation;
- managed-cloud load-balancer conformance.

Those boundaries make the accepted release trustworthy. Course 6 receives the network requirements needed to study storage and data resilience without pretending that ordinary HTTP connectivity proves a storage path.
