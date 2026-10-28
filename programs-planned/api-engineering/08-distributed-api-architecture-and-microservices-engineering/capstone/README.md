# Course 8 capstone

This directory is the executable support system for the reader-first course book. It continues the Analysis Runs Platform from Course 7 and performs two evidence-backed extractions: Notification Delivery first and Artifact Delivery second. Analysis Control remains one cohesive business authority; Worker Plane and Edge Gateway remain compute and edge components rather than invented data owners.

## Authoritative architecture artifacts

Read `architecture/` in this order:

1. `boundary-scorecard.yaml`
2. `service-catalog.yaml`
3. `data-ownership.yaml`
4. `dependency-graph.yaml`
5. `consistency-policy.yaml`
6. `saga-catalog.yaml`
7. `security-policy.yaml`
8. `release-policy.yaml`
9. `extraction-plan.yaml`
10. `version-ledger.yaml`
11. `adr/`

These files state why each boundary exists, which facts it owns, which calls are allowed, how versions coexist, how cutover reverses, and when a service should be merged back.

## Executable implementation layers

### Semantic reference tracks

- `tracks/python-distributed` — primary dependency-light Python reference;
- `tracks/typescript-distributed` — strict TypeScript comparative reference.

They prove boundary scoring, single-writer ownership, versioned projections, dependency cycles, sagas, capability bytes, routing, version skew, strangler phases, and reconciliation without external infrastructure.

### Multi-process network laboratory

`network-lab/` starts five independent processes:

- Edge Gateway;
- Analysis Control;
- Artifact Service;
- Notification Service;
- Worker Plane.

The tour performs real loopback TCP calls, uses workload and delegated capability tokens, completes one run, delivers one notification, terminates Artifact Service, and proves that the gateway returns an explicitly partial response rather than false complete data.

### Production-shaped boundaries

- `database/` gives each business service an owner-local PostgreSQL migration history while preserving legacy migrations 001–015 for extraction evidence;
- `topology/compose.yaml` builds the network laboratory in separate containers;
- `topology/kubernetes/` records Deployment, Service, and NetworkPolicy intent;
- `security/` defines the exact cross-language artifact capability profile;
- `releases/`, `planted-defects/`, and `final-defense/` make architecture acceptance falsifiable.

## Core routes

From the course root:

```bash
make predecessor-proof
make python-proof
make typescript-proof
make capstone-tour
make network-lab-proof
make core-proof
```

## Evidence boundary

The semantic and five-process loopback proofs execute without external services. They are real mechanism evidence, but they are not production-capacity or durable-database evidence.

Live PostgreSQL locking, migration coexistence, container networking, cluster policy enforcement, and representative traffic require the environment-backed laboratories described in the course book. Those routes are reported as executed only when their dependencies are present.
