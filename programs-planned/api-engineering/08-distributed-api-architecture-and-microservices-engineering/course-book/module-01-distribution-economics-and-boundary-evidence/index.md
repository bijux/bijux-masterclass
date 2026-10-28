# Module 01 — Distribution Economics, Boundary Evidence, and Architecture Fitness Functions

> **Program stage:** Course 8 of 10 — Distribute ownership deliberately.

> **Central question:** When does a remote service boundary create more value than the coordination, latency, failure, and operational costs it introduces?

## Where this module fits

Course 8 begins from this incoming boundary: **The Course 7 platform with governed HTTP, event, and RPC interfaces and migration history through 015.**

This module establishes the course’s first new responsibility by asking: **When does a remote service boundary create more value than the coordination, latency, failure, and operational costs it introduces?** Its capstone increment is **Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services**. That result is required before **Service Boundaries, Bounded Contexts, and Contract Ownership** can be studied honestly.

## Learning outcomes

- Treat distribution as an economic and organizational decision rather than a maturity badge.
- Compare modular-monolith and service extraction options using change, scale, failure, security, and ownership evidence.
- Define architecture fitness functions that can reject an attractive but harmful decomposition.
- Distinguish independently deployable process boundaries from independently owned business services.
- Calculate the synchronous latency and availability cost of proposed remote edges.
- Write an architecture decision that includes reversal criteria and residual risk.

## Capstone increment

Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services.

## Distribution is an exchange, not an upgrade

A modular monolith and a microservice system are not points on a universal maturity ladder. Distribution exchanges local simplicity for a different set of capabilities: independent release, isolated scaling, fault containment, separate security policy, and organizational ownership. The price is permanent network uncertainty, more state copies, more credentials, more compatibility windows, and more operational surfaces.

The decision therefore begins with a sentence that can be falsified:

> Extracting Notification Delivery will let a separately accountable team change retry policy and retention independently, while removing webhook failure from the run-completion path, at an acceptable cost in event lag and operational ownership.

That claim names value, mechanism, and cost. “We need microservices” names none.

## Start from the modular baseline

The existing platform is not a ball of mud. It already has modules, transaction boundaries, contracts, event publication, worker protocols, telemetry, and performance evidence. That matters because a good extraction preserves an existing seam; it does not create cohesion by moving files into another repository.

Before proposing a service, measure:

- which modules change together;
- which invariants commit together;
- which workloads scale differently;
- which failures should be isolated;
- which secrets and retention rules differ;
- who reviews and operates the capability;
- how many synchronous edges the split creates;
- whether rollback can restore the old path.

If the current module cannot be explained, tested, and released internally, the network will not improve it.

## Boundary evidence categories

### Ownership

One team or accountable group must own the capability, its contract, its data, its SLOs, and its incidents. A service shared by five teams is usually a coordination queue with a network endpoint.

### Data autonomy

A business service must own its writes. If two services update the same tables, or one service reaches into another database for a join, deployment independence is fictional. Some components—gateway and worker plane—may be legitimate non-data services, but their lack of data authority must be explicit.

### Change independence

Study real change history. If two capabilities always change in one release because one rule spans them, splitting increases coordination. If they change for distinct reasons and can evolve under contracts, separation may help.

### Scale isolation

Artifact egress and webhook retries have resource shapes distinct from run metadata. That is meaningful. “This class is large” is not.

### Failure isolation

Notification unavailability should not prevent run completion. Extracting notification can improve failure isolation because the event boundary already exists. Splitting run state from idempotency would reduce isolation because every mutation would require another dependency.

### Security and compliance

Artifacts may need independent retention, encryption, and egress controls. This can justify a boundary, but only if authorization remains complete. A security label is not evidence if the new service trusts headers from the old one.

### Operational cost

Every service adds deployment, monitoring, patching, capacity, secrets, backups, incident routing, and compatibility work. The scorecard subtracts this cost rather than hiding it.

## Fitness functions

Architecture decisions decay unless protected. Course 8 turns key properties into fitness functions:

```text
one authoritative writer per fact
no synchronous dependency cycle
public synchronous depth <= 2
all services have one accountable owner
no gateway-owned business state
supported old/new version matrix passes
shadow comparison is clean before cutover
reconciliation has no unexplained findings
```

Some fitness functions run in CI. Others are review gates backed by evidence. The important feature is that a future change can fail them.

## The candidate review

### Notification Delivery — extract first

Notification is already event-driven. It owns retry timing, destination handling, delivery history, and operational concerns distinct from Analysis Control. Its failure need not block the core workflow. The extraction adds consumer lag and another database, but not a synchronous critical-path call.

### Artifact Delivery — extract second

Artifact bytes, checksums, object storage, retention, and egress have a distinct scaling profile. The extraction is conditional because authorization and completion currently depend on run state. Course 8 first designs narrow capabilities, event-fed references, and orphan reconciliation.

### Analysis Control — keep cohesive

Projects, dataset metadata, run state, idempotency, leases, and authoritative event publication share invariants and transactions. Splitting them would create synchronous and compensating workflows around the system’s most sensitive decisions.

### Worker Plane — separate deployment, not data owner

Workers deserve independent scaling and lifecycle. They do not own run truth. A worker report is an attempt that Analysis Control validates against the durable lease generation.

### Table services — reject

Project Service, Dataset Table Service, and Idempotency Service mirror storage rather than capabilities. They create remote joins, shared transactions, and owner ambiguity.

## A quantitative check that does not pretend precision

Scores do not make architecture objective. They make assumptions visible. Weight ownership and data autonomy highly; subtract operational and synchronous coupling. Then require narrative evidence for each score. A boundary with a high score but no team owner remains invalid. A boundary with a moderate score may remain a module until a real workload or compliance need appears.

```python
candidate = BoundaryCandidate(
    name="notification",
    ownership=2,
    data_autonomy=2,
    change_independence=2,
    scale_isolation=1,
    failure_isolation=2,
    security_boundary=1,
    operational_cost=1,
    synchronous_coupling=0,
)
assert decision(candidate) == "extract"
```

The output is a review aid, not an autonomous architect.

## Reversal criteria

Every extraction decision needs a merge-back trigger. Examples:

- the service has no stable owner;
- every release still coordinates with Analysis Control;
- synchronous calls increase rather than decrease;
- operational load exceeds failure-isolation value;
- independent scaling is never used;
- the service’s private model becomes a shared library.

A mature architecture can merge services. Irreversibility is not sophistication.

## Python and TypeScript implications

The reference tracks represent candidates as explicit data and run the same decision outcomes. Python’s dataclass makes the weighted inputs visible. TypeScript’s interface and strict union return type make valid decisions explicit. Neither implementation is allowed to create a service because a directory exists.

## Evidence required before Module 2

The boundary scorecard must approve Notification Delivery, conditionally approve Artifact Delivery, keep Analysis Control, classify Worker Plane correctly, and reject table services. More importantly, you must defend one rejection with the same rigor as one approval.

## Worked architecture review: why Notification crosses the boundary first

A boundary review should begin with the current transaction and failure model, not with a proposed service diagram. In the Course 7 baseline, run completion and notification delivery are already separated by a durable event. Analysis Control commits the terminal run state and the corresponding event record under one authority. Delivery can happen later, can be retried, and can fail without changing whether the analysis completed. That existing temporal seam is the strongest extraction evidence in the system.

Compare three proposals.

| Proposal | Value created | New coupling | Decision |
|---|---|---|---|
| Extract Notification Delivery | independent retry, retention, receiver policy, and on-call ownership | event lag, consumer recovery, separate data store | approve first |
| Extract Artifact Delivery | isolated storage and egress scaling, retention and integrity policy | capability issuance, event-fed references, reconciliation | approve conditionally |
| Extract Idempotency | none outside the owning mutation | remote transaction on every command | reject |

The third proposal is instructive. Idempotency is technically reusable, but it is not an autonomous capability. The idempotency record has meaning only inside the mutation it protects. Moving it behind a service would create this sequence:

```text
reserve request key remotely
→ mutate run locally
→ mark request result remotely
```

A timeout between any pair of steps creates ambiguity. The original local transaction solved that problem more completely. Distribution would reduce correctness while adding latency and operations. Reuse is therefore not sufficient evidence for a service.

Notification is different because the owner can answer a complete set of questions without consulting Analysis Control synchronously:

- Which subscriptions exist?
- Which event deliveries are pending?
- Which retry policy applies?
- Which receiver has acknowledged an event?
- Which deliveries must be retained or deleted?
- Which destinations are paused?

That is a coherent decision boundary.

## Coupling is multidimensional

“Loose coupling” is too vague for an architecture decision. Evaluate at least five forms:

1. **Temporal coupling** — must both components be available at the same moment?
2. **Data coupling** — must both interpret or write the same private model?
3. **Change coupling** — do they require coordinated releases?
4. **Operational coupling** — does one team need another team to diagnose or recover routine failures?
5. **Semantic coupling** — does one invariant span both sides of the proposed boundary?

An asynchronous event removes some temporal coupling, but not necessarily semantic coupling. If the consumer cannot act without calling the producer for every message, the system remains temporally coupled in practice. If both teams edit the same event payload whenever either side changes, change coupling remains high. If one incident cannot be understood without querying five private databases, operational coupling remains high.

For each proposed boundary, write a coupling matrix:

```text
                         local module   remote service
transactional invariant      strong          weak
failure isolation             weak          strong
independent scaling           weak          strong
release coordination          low            ?
operational ownership         shared         ?
latency                       local          network
```

The question marks are deliberate. A repository or deployment split does not automatically create ownership or release independence. Those properties must be proven.

## Quantifying critical-path cost

Suppose a public request currently has a 700 ms objective. A proposed decomposition adds two sequential remote calls with 120 ms and 180 ms p95 latency. Ignoring processing variance, the budget left for the original work becomes:

```text
700 ms - 120 ms - 180 ms = 400 ms
```

The availability effect is also multiplicative when all dependencies are required. If the gateway, Control, and Artifact services each achieve 99.9% availability and the request requires all three, the rough upper bound is:

```text
0.999 × 0.999 × 0.999 = 0.997002
```

or about 99.70%, before considering shared failures and network paths. This calculation is not a complete reliability model, but it exposes the cost of required synchronous edges. An extraction justified by “independent scaling” may still be unacceptable if it consumes the public SLO.

Course 8 therefore gives the dependency graph a maximum public synchronous depth of two. That is a local architecture policy derived from this platform’s objectives, not a universal rule. A different system may justify a different limit. What matters is that the limit is explicit and testable.

## Team ownership is part of the architecture

A service without an accountable owner is not independent. Its interfaces may have a repository, but routine questions will still queue behind a shared group:

- Who approves an incompatible change?
- Who responds to an alert at 03:00?
- Who owns retention and deletion?
- Who decides whether a replay is safe?
- Who pays the operational cost?
- Who can merge the service back when the boundary fails?

The capstone service catalogue requires one owner for every service and one writer for every authoritative fact. The gateway is owned as an edge component, but it owns no business facts. The worker plane has an operational owner, but Analysis Control remains the writer of leases and run state. These distinctions prevent “ownership” from becoming a label attached to a deployment.

## Architecture fitness functions as executable policy

A useful fitness function has four parts:

```text
property
→ observed representation
→ failing condition
→ owner of remediation
```

Example:

```text
Property: no synchronous cycles
Representation: dependency-graph.yaml
Failure: depth-first traversal revisits an active node
Owner: architecture review plus the service adding the edge
```

The Course 8 proof suite checks the declared graph for cycles and maximum depth. It also verifies that rejected candidates remain rejected. This matters because architecture degradation is often incremental: one “temporary” callback, one shared table, one gateway rule. A scorecard without a failing proof becomes historical prose.

Not every fitness function is machine-complete. “One accountable owner” cannot be proven from YAML alone. The machine can detect missing or duplicate owner identifiers, while review evidence establishes whether the named owner actually has authority and operational capacity. The course labels that difference rather than pretending all architecture can be automated.

## A boundary decision record

Before approving an extraction, write a decision with these fields:

```text
Capability:
Current module owner:
Proposed service owner:
Authoritative facts:
Inbound contracts:
Outbound contracts:
Required synchronous dependencies:
Asynchronous dependencies:
Independent change evidence:
Independent scale evidence:
Failure-isolation value:
Security or retention difference:
Migration path:
Rollback path:
Reconciliation oracle:
Operational cost:
Reversal criteria:
Decision:
```

A proposal that cannot fill these fields is not ready. “We will decide after extraction” transfers design uncertainty into production.

## Design review: a plausible but wrong split

Consider a Dataset Service extracted because datasets are a prominent noun. It owns the `datasets` table, while Analysis Control still owns project policy and run submission. Every run submission now requires:

1. Control authenticates the caller.
2. Control calls Dataset Service for metadata and ownership.
3. Dataset Service may call Project Service for project policy.
4. Control creates the run and idempotency record.
5. Worker execution later calls Dataset Service again.

The split adds synchronous depth, duplicates authorization context, and moves no independent business decision. Dataset lifecycle changes still coordinate with project and run rules. The service is a remote table gateway. The correct response is not to add caching or a service mesh; it is to reject the boundary.

This example establishes the central discipline of Course 8: **the first microservice skill is the ability not to create a microservice.**

## Module synthesis

You are ready to leave this module when you can **treat distribution as an economic and organizational decision rather than a maturity badge, compare modular-monolith and service extraction options using change, scale, failure, security, and ownership evidence, and define architecture fitness functions that can reject an attractive but harmful decomposition** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Reject Project Service, Dataset Table Service, and Idempotency Service with concrete failure paths** and requiring the following oracle: **Every approved service has one owner, autonomous writes or an explicitly non-data role, independent value, acceptable coordination cost, and reversal criteria. At least three attractive but harmful services are rejected.**

The cumulative platform now includes **Publish a measured boundary scorecard that approves Notification Delivery for first extraction, approves Artifact Delivery conditionally, keeps Analysis Control cohesive, and rejects table-shaped services**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Service Boundaries, Bounded Contexts, and Contract Ownership](../module-02-service-boundaries-and-contract-ownership/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
