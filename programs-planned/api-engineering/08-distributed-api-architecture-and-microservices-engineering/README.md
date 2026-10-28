# Course 8 — Distributed API Architecture and Microservices Engineering

This is the eighth course in the Bijux Masterclass API Engineering program.

It continues the same Analysis Runs Platform after the learner has already mastered public HTTP contracts, durable service implementation, API security, reliability and observability, performance and traffic control, event-driven integration, and typed gRPC communication.

Course 8 therefore does not begin with containers or a service count. It begins with a harder question:

> Which capabilities deserve independent ownership and deployment, and how do we preserve correctness when local calls, local transactions, and one release unit no longer contain the workflow?

## Governing responsibility

> Decompose a proven service only where ownership and evidence justify distribution, then preserve correctness, security, operability, and release independence across the resulting network.

## Program progression

```text
Course 1  Specify the public promise
Course 2  Implement the promise durably
Course 3  Defend the promise
Course 4  Observe and recover the promise
Course 5  Sustain the promise under pressure
Course 6  Extend the promise across asynchronous time
Course 7  Engineer typed internal invocation and streaming
Course 8  Distribute ownership deliberately
```

Course 7 supplied typed remote boundaries but deliberately did not approve service extraction. Course 8 consumes that exact 46-file handoff and uses boundary, ownership, failure, release, security, and operational evidence to decide what becomes remote.

## Final architecture

The course extracts two capabilities:

1. **Notification Delivery** — first, because durable events already isolate delivery from run completion.
2. **Artifact Delivery** — second, because storage, integrity, retention, and egress form a distinct capability, but only after authorization and reconciliation are redesigned.

It retains **Analysis Control** as one cohesive authority for projects, dataset metadata, runs, idempotency, worker leases, state transitions, process-manager state, and event publication.

It treats **Worker Plane** as a compute plane and **Edge Gateway** as an edge component. Neither is assigned invented business-data ownership.

The course rejects:

- a service for every table;
- shared application databases;
- an Idempotency Service;
- gateway-owned workflows;
- synchronous notification in the completion path;
- Artifact Service calling Control on every authorization decision;
- Worker Plane deciding run truth;
- ownerless shared-data services;
- a service mesh as the owner of retries, security policy, or business correctness.

## Learner product

The authoritative product is [`course-book/`](course-book/):

```text
59 navigated pages
10 complete numbered modules
120 exercises
120 matching worked answers
10 failure-oriented labs
10 evidence checkpoints
```

The chapters are self-contained. The learner does not need to search architecture reports or implementation comments to understand the subject. The capstone and proof system provide evidence for the book; they do not replace it.

Read:

```text
course-book/start-here.md
```

## Capstone evidence

The capstone contains four complementary layers.

### 1. Architecture and policy evidence

Boundary scorecard, service catalogue, data ownership, dependency graph, consistency policy, saga catalogue, security policy, release policy, extraction plan, version ledger, and architecture decision records.

### 2. Cross-language semantic references

A dependency-light Python reference and strict TypeScript reference prove the same externally relevant invariants, including one writer per fact, cycle rejection, versioned projections, saga compensation, capability bytes, routing, version skew, strangler transitions, and reconciliation.

### 3. Five-process network laboratory

A real loopback laboratory starts:

- Edge Gateway;
- Analysis Control;
- Artifact Service;
- Notification Service;
- Worker Plane.

It performs remote calls, authenticates workload hops, delegates a checksum- and size-bound artifact capability, completes one run, relays one committed event, and then terminates Artifact Service. The gateway must return authoritative run state with an explicit partial marker instead of pretending that missing artifact details mean no artifacts exist.

### 4. Production-shaped environment routes

Owner-local PostgreSQL migrations, an executable Compose build, Kubernetes workloads and NetworkPolicies, mixed-version releases, planted defects, and a sanitized Course 9 handoff.

Environment-backed claims are reported only when executed. A local network tour is not presented as proof of production capacity, live database locking, or cluster policy enforcement.

## Course boundary

The course preserves:

- Public HTTP API 1.2 and OpenAPI 3.1.2;
- Analysis Events API 1.0 and AsyncAPI 3.1.0;
- Analysis RPC API 1.0 and its Protobuf contracts;
- Security, Reliability, Performance, Event, and gRPC profiles 1.0;
- legacy migration history through 015.

It adds:

- Distributed Architecture Profile 1.0;
- service-owned migration histories;
- explicit service, data, contract, deadline, retry, and operator ownership;
- a cross-language artifact capability profile;
- incremental extraction, rollback, decommission, and merge-back policy;
- a governed graph-access boundary for Course 9.

## Language strategy

Course 1 used Python and TypeScript symmetrically to establish contract independence. Courses 2–8 use one primary implementation track and one comparative reference track.

Choose Python or TypeScript as the primary track. Implement and explain the complete architecture there. Use the second track to test parity in the guarantees that cross the boundary. Do not duplicate framework ceremony merely to make two directory trees look identical.

## Start

```bash
make help
make doctor
make predecessor-proof
make capstone-tour
make network-lab-proof
make core-proof
```

In a provisioned environment:

```bash
TEST_DATABASE_URL=... make postgres-proof
make compose-proof
make kubernetes-proof
make docs-build
make full-proof
```

The complete inventory is in [`COURSE-CONTENTS.md`](COURSE-CONTENTS.md). The exact release evidence and unexecuted environment boundaries are in `FINAL-VERIFICATION.md`.
