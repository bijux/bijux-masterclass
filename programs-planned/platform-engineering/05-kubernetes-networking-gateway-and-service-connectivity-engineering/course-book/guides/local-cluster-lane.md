# Guide — optional kind and Cilium evidence lane

The local cluster lane exists to observe real Kubernetes admission, reconciliation, CNI attachment, Service forwarding, DNS, policy, and Gateway behavior on one machine.

## What it can prove

- manifests are accepted by the pinned API server;
- Pods receive real network attachments;
- Services and EndpointSlices are programmed by the installed data plane;
- CoreDNS answers cluster records;
- Cilium enforces selected policies;
- Gateway API resources attach and route under the installed controller;
- positive and negative probes behave as expected.

## What it cannot prove

- independent zone or node failure domains beyond local process isolation;
- cloud load-balancer provisioning and source preservation;
- managed DNS behavior;
- cloud NAT or private endpoint behavior;
- production capacity, latency, or cost;
- upgrades in the organization’s target environment.

## Workflow

```bash
make kind-proof
```

The guarded script checks required tools, creates a disposable cluster, installs the pinned lane, applies resources in order, runs positive and negative probes, collects evidence, and deletes the cluster.

Read the script before execution. Do not point the commands at an existing shared context. Preserve implementation versions and conformance information with the report.
