# Final verification and evidence boundary

This record distinguishes evidence that executed during the Course 8 release build from routes that require an external environment.

## Release identity

```text
Course:     Distributed API Architecture and Microservices Engineering
Sequence:   08
Version:    1.0.0
Profile:    Distributed Architecture Profile 1.0
Predecessor: Course 7 gRPC and Protobuf Engineering
Successor handoff: Course 9 GraphQL Schema and Runtime Engineering
```

## Executed dependency-light evidence

The following checks executed from the course source tree and are included in `make core-proof`:

- exact verification of the 46-file Course 7 handoff;
- 61-page course-book structure;
- 120 exercises and 120 identically headed worked answers;
- ten complete labs and ten evidence checkpoints;
- boundary scorecard and architecture fitness functions;
- five-component service catalogue and one-writer ownership for eight fact families;
- owner-local data policy, versioned projections, gap detection, and staleness decisions;
- acyclic synchronous dependency graph and bounded public depth;
- saga duplicates, after-commit ambiguity, stale-attempt compensation, and reconciliation;
- exact Python/TypeScript artifact-capability token parity;
- routing, health, supported version skew, and strangler transition policy;
- legacy migrations 001–015 and four owner-local migration histories;
- ten cross-language vector files with 46 identified cases;
- Python reference suite: 31 tests;
- TypeScript reference suite: 20 tests plus strict compilation;
- complete semantic Analysis Runs workflow;
- five-process loopback network laboratory;
- real remote gateway, control, artifact, worker, and notification calls;
- explicit partial gateway response after terminating Artifact Service;
- ten planted architecture defects rejected by their assigned gates;
- final architecture defense;
- exact eight-file Course 9 handoff;
- duplicate-key-aware JSON, YAML, and TOML parsing;
- local Markdown-link verification;
- educational-depth and repeated-prose guards;
- Python syntax and repository-hygiene checks.

The five-process network laboratory produced these required outcomes:

```text
services started:          5
remote calls exercised:    yes
run outcome:               completed
artifact effects:          1
notification deliveries:  1
complete gateway view:     partial=false
after artifact failure:    partial=true
warning:                   artifactsUnavailable
```

## Static environment declarations verified

The dependency-light proof parses and checks:

- service-owned PostgreSQL migration trees;
- the executable Docker Compose build declaration;
- Kubernetes Namespace, Secret fixture, ServiceAccounts, Deployments, Services, event broker, and NetworkPolicies;
- accepted and rejected distributed release candidates;
- architecture decisions, reconciliation reports, and fault-plan structure.

Parsing a declaration is not the same as operating the declared environment.

## Environment-backed routes not executed in the release environment

The release environment did not provide Docker, Kubernetes tooling, PostgreSQL command-line tools, or MkDocs. Therefore these claims are explicitly **not executed**:

- live PostgreSQL migration application, locks, transaction isolation, and cross-process reconciliation;
- independent database credentials and network-enforced database isolation;
- Docker container build and Compose networking;
- Kubernetes API validation, scheduling, readiness, Service routing, Secret integration, and NetworkPolicy enforcement;
- live event-broker retention and redelivery;
- strict MkDocs rendering;
- representative production latency, capacity, cost, and failure-recovery evidence.

The package includes explicit routes for these environments:

```bash
TEST_DATABASE_URL=... make postgres-proof
make compose-proof
make kubernetes-proof
make docs-build
make full-proof
```

A missing dependency is reported as unavailable or not executed. It is not converted into a pass.

## Scope of the reference implementations

The Python and TypeScript tracks are executable architecture models. The Python network laboratory adds real process and TCP boundaries. Together they prove mechanisms and cross-language invariants.

They do not claim to be a complete production deployment. In particular:

- the dependency-light network laboratory keeps state in memory;
- its driver simulates one bounded broker-relay step;
- the course capability token is a documented teaching profile, not an Internet standard;
- the Kubernetes Secret is a laboratory fixture, not an operated secret-management design;
- static NetworkPolicy files do not prove a cluster’s CNI enforces them;
- deterministic failure schedules do not replace representative production game days.

## Release archive verification

The published Course 8 ZIP is built from the exact manifest with sorted entries, fixed timestamps, and preserved executable modes. The release procedure requires two byte-identical builds, duplicate- and unsafe-path inspection, ZIP CRC verification, clean extraction, exact extracted-manifest verification, and rerunning the dependency-light proof and capstone tours from the extracted copy.

The external release record beside the ZIP contains the final archive digest, byte size, and member count. Archive evidence does not enlarge the claims made by the course; it proves that the published bytes preserve the source tree that passed the stated checks.

## Trustworthy completion rule

Course 8 is complete as a self-learning course and reference package when its exact manifest and dependency-light proof pass. A learner may claim the stronger environment-backed outcomes only after executing the corresponding laboratories and preserving their machine-readable evidence.
