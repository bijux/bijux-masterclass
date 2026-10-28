# Evidence model

Distributed architecture claims span more layers than local application claims. Course 8 classifies evidence so that a passing low-level check is not presented as proof of the whole system.

## Evidence classes

| Class | What it establishes | What it does not establish |
|---|---|---|
| Structural | files, schemas, owners, graphs, and policies exist and are internally consistent | live behavior or real ownership capacity |
| Semantic | deterministic models implement the intended rule | network, database, or process behavior |
| Component | one service honors its contract and local invariants | end-to-end distributed outcome |
| Contract | supported producer/consumer combinations agree | data ownership or workflow recovery |
| Topology | service graph, routes, identities, and network policies are coherent | authoritative business-state correctness |
| Failure | a controlled schedule produces the expected recovery | all production schedules |
| Reconciliation | durable states agree or produce actionable findings | absence of future divergence |
| Release | supported versions coexist, cut over, and roll back within a declared window | unlimited future compatibility |
| Operator | alerts, runbooks, owner, and recovery decisions exist | that every incident will be handled perfectly |
| Environment-backed | actual databases, brokers, containers, or clusters execute the route | environments not tested |

## Claim-to-proof examples

```text
Claim: Notification does not block run completion
Proof: dependency graph forbids the synchronous edge,
       completion path test succeeds during Notification failure,
       event/outbox evidence remains durable.

Claim: Artifact upload creates one effect after response loss
Proof: stable effect identity, duplicate schedule,
       owner-state inspection, reconciliation.

Claim: Artifact Service is independently deployable
Proof: owned migrations, old/new interface matrix,
       shadow comparison, route rollback, no shared database write.

Claim: tenant isolation survives gateway compromise
Proof: Artifact authorizes delegated/capability context locally;
       trusted identity-header planted defect is rejected.
```

## Distributed ambiguity

The most important schedules are ambiguous outcomes:

- caller times out after callee commit;
- event is published but acknowledgement is lost;
- artifact is stored but the run attempt becomes stale;
- new route returns a different representation during shadow;
- rollback occurs after the new service emitted an external effect;
- projection receives version 15 without version 14;
- old consumer processes a new additive event during rolling release.

The course demands stable identities and durable comparison points for these schedules. “Retry and hope” is not evidence.

## Proof sensitivity

A proof suite should demonstrate that it can fail. Course 8 includes ten planted defects. Each defect identifies the gate that must reject it. For example:

```text
DIST-01 shared database
    rejected by ownership and data proof

DIST-03 synchronous cycle
    rejected by dependency graph proof

DIST-05 dual write
    rejected by data and extraction proof

DIST-08 trusted identity header
    rejected by security proof

DIST-09 unsupported version skew
    rejected by release proof
```

If a planted defect passes, repair the proof before trusting the architecture.

## Honest environment boundaries

The dependency-light model proves deterministic semantics. It does not prove:

- PostgreSQL isolation under live concurrent connections;
- real DNS refresh and connection draining;
- Kubernetes NetworkPolicy enforcement;
- container shutdown ordering;
- service-mesh behavior;
- production latency or capacity;
- real certificate rotation.

Those routes are present as environment-backed labs. The final verification record must distinguish executed from unexecuted evidence.
