# Start here

This course begins where Kubernetes Architecture and Workload Engineering ends. Course 4 produced an immutable Atlas API and worker release, reconciled it through Kubernetes workload controllers, and documented readiness, shutdown, resource, placement, and supply-chain requirements. Course 5 asks the question that those objects cannot answer alone:

> How does a packet move from one process to another, which component owns every transformation, and what evidence proves that connectivity is correct rather than merely accidental?

The course is not a catalogue of `kubectl` commands and it is not a tutorial for one CNI, Gateway controller, cloud load balancer, or service mesh. Those implementations matter, but the durable skill is being able to reason across them.

## What you will build

The cumulative product is **Atlas Connectivity Plane 1.0**:

```text
client
  ↓ DNS and route selection
public TLS listener
  ↓ Gateway API attachment and HTTP routing
Atlas API Service
  ↓ EndpointSlice membership and Service data plane
Ready Atlas API Pod
  ↓ controlled east-west and egress paths
worker, DNS, and approved external dependencies
```

The final release includes:

- a packet-path and address-domain architecture;
- deterministic CNI/IPAM, Service, DNS, NetworkPolicy, Gateway, TLS, and egress models;
- a real loopback DNS–Service–TLS Gateway laboratory;
- current production-intent Kubernetes and Gateway API resources;
- a guarded kind+Cilium native lane;
- failure cases, runbooks, release candidates, and planted defects;
- an exact handoff for Kubernetes Storage, Stateful Workloads, and Data Resilience Engineering.

## The learning contract

Each numbered module has five learner-facing files:

- `index.md` is the authoritative chapter;
- `exercises.md` tests transfer, not recall;
- `exercise-answers.md` provides worked reasoning;
- `lab.md` introduces a controlled failure or ambiguity;
- `checkpoint.md` defines non-compensable evidence before progression.

Read the chapter before opening the implementation. The code is an executable explanation of mechanisms already introduced in prose. It is not where the missing theory is hidden.

## Prerequisites

You should be able to:

- inspect Linux processes, sockets, routes, interfaces, namespaces, and files;
- explain TCP connection establishment, DNS queries, HTTP authority, and TLS hostname verification;
- read Kubernetes object metadata, spec, status, conditions, owner references, and controller events;
- reason about Pods, Deployments, Jobs, readiness, graceful termination, requests, limits, and scheduling;
- run Python tests and read small Go programs;
- read YAML without treating it as executable truth.

The exact Course 4 handoff is under `capstone/predecessor/handoff/`. Run `make predecessor-proof` before making changes.

## How to study one module

1. **State the path before reading the solution.** Draw source, destination, intermediate identities, and expected transformations.
2. **Read the chapter with an ownership question.** For each state change, name the controller, process, kernel component, or external system allowed to perform it.
3. **Answer the exercises without the answer book.** Include the evidence that would falsify your conclusion.
4. **Run the lab.** Preserve baseline and failure evidence before repair.
5. **Compare with the worked answers.** Differences in architecture are acceptable only when their invariants and evidence are explicit.
6. **Close the checkpoint.** A plausible explanation without the required artifact is not completion.

## Primary and native evidence lanes

The dependency-light lane runs on Python, Go, and OpenSSL. It provides deterministic evidence for the reasoning model and a real loopback DNS, proxy, HTTP, and TLS path.

The native lane uses kind, Cilium, Kubernetes 1.36, Gateway API 1.6, and cluster tools when available. It proves behavior of that concrete environment. It does not automatically prove a managed-cloud CNI, load balancer, DNS service, or production topology.

The course distinguishes:

```text
semantic proof
host/process proof
local-cluster proof
real-environment proof
production operational evidence
```

Never promote a claim to a higher evidence class merely because the lower-class test passed.

## Commands

From the course directory:

```bash
make doctor
make predecessor-proof
make core-proof
make capstone-tour
make manifest-proof
```

With the optional native toolchain:

```bash
make kind-proof
make docs-build
```

Begin with Module 1 only after the predecessor proof passes and you can explain why a Ready Pod can still be unreachable from another Node.
