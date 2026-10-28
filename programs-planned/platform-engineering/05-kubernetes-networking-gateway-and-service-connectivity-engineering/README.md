# Kubernetes Networking, Gateway, and Service Connectivity Engineering

Course 5 of the Platform Engineering program.

This course takes the exact Kubernetes workload contract produced by Course 4 and turns it into a deliberate connectivity system. It follows one packet from process socket to Pod namespace, CNI attachment, Node route, Service and EndpointSlice state, DNS, NetworkPolicy, topology policy, Gateway API, TLS, egress, and return path.

The governing question is:

> Which component owns each network transition, what invariant must survive it, and what evidence identifies the earliest transition that failed?

The cumulative capstone is **Atlas Connectivity Plane 1.0**.

## Course progression

```text
Course 1 — operate the Linux and cloud substrate
Course 2 — codify the cloud foundation
Course 3 — package and verify the OCI workload
Course 4 — reconcile the workload through Kubernetes APIs
Course 5 — connect, discover, segment, expose, and diagnose it
Course 6 — persist state and recover data across those exact paths
```

## Primary product

The course book is authoritative:

```text
course-book/
├── start-here.md
├── study-plan.md
├── capstone.md
├── evidence-model.md
├── standards.md
├── guides/
├── casebook/
├── reference/
├── module-00-orientation/
└── module-01 ... module-10/
    ├── index.md
    ├── exercises.md
    ├── exercise-answers.md
    ├── lab.md
    └── checkpoint.md
```

The implementation, manifests, tests, and proof scripts are executable explanations of the text. They do not hide missing theory.

## What the learner builds

Atlas Connectivity Plane 1.0 includes:

- an address-domain and packet-path architecture;
- CNI lifecycle, IPAM, route, and MTU models;
- Service, EndpointSlice, eligibility, and generation models;
- DNS search, cache, and transport models;
- additive NetworkPolicy evaluation;
- locality, source-identity, and dual-stack decisions;
- Gateway API attachment and route precedence;
- verified local TLS, SNI, hostname, authority, and proxy behavior;
- egress destination and redirect policy;
- production-intent Kubernetes and Gateway API resources;
- a guarded kind+Cilium native lane;
- ten failure-oriented laboratories;
- six operator runbooks;
- accepted, rejected, review-required, and not-executed release candidates;
- ten planted defects;
- an exact Course 6 storage-network handoff.

## Evidence model

The release distinguishes:

```text
document evidence
→ semantic evidence
→ real local DNS/TCP/TLS evidence
→ disposable Kubernetes-cluster evidence
→ real cloud/network evidence
→ operated production evidence
```

Only executed evidence is reported as executed. A valid NetworkPolicy object is not enforcement evidence. A correct Gateway object is not proof of an external load balancer. A loopback TLS exchange is not managed-certificate proof.

## Start

```bash
make doctor
make predecessor-proof
make core-proof
make capstone-tour
make manifest-proof
```

Begin at [`course-book/start-here.md`](course-book/start-here.md).
