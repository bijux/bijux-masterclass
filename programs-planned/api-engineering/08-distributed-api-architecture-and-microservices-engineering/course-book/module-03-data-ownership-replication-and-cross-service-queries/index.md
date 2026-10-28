# Data Ownership, Replication, and Cross-Service Query Design

**Module 03 of 10**

> **Governing question:** How can each service own its writes while the system still answers cross-capability questions without shared tables or hidden distributed transactions?

## Place in the program

Course 7 introduced typed internal RPC but deliberately refused to equate a remote method with an independently owned service. Course 8 now uses ownership, data, failure, release, and operational evidence to decide which capabilities deserve distribution.

## Learning outcomes

- enforce one authoritative writer for each business fact
- distinguish owned data, replicated views, caches, and derived analytics
- design event-fed projections with version and gap handling
- choose API composition, local read models, or asynchronous reports from latency and consistency needs
- state staleness and monotonicity guarantees in contracts and user experience
- reconcile orphaned, missing, and divergent records without bypassing service ownership

## Capstone result

Split authoritative data ownership, build versioned projections for cross-service reads, define staleness budgets, and prove reconciliation for missing, duplicate, and out-of-order updates.


## Database per service means authority per service

“Database per service” is frequently reduced to “different connection strings.” The important rule is authority: only the owning service may write the canonical fact. Separate schemas in one PostgreSQL cluster can be a valid transitional deployment, but application code still must not query across them as if the network boundary did not exist.

The course creates independent migration histories because independent release requires independent schema evolution. The legacy migration line through 015 remains historical evidence. New service databases start their own heads:

```text
analysis-control     001
artifact-service     001–002
notification-service 001–002
platform-catalog     001
```

A global migration number 016 for all services would preserve the old release train.

## Four data categories

### Owned data

Canonical business facts. Only the owner writes them.

### Replicated views

Derived state copied through a contract. The replica records source identity and version, can detect gaps, and can be rebuilt.

### Caches

Disposable acceleration with explicit freshness and invalidation. A cache miss or eviction must not change authority.

### Analytics

Historical or aggregated data that supports analysis but does not drive transactional decisions unless an explicit contract promotes it.

Confusing these categories is dangerous. A replica that applications start updating becomes a second owner. A cache used as the only authorization source becomes authority by accident.

## Cross-service query choices

### API composition

The gateway requests authoritative parts from several services and composes the response. This is useful when freshness matters and fan-out is bounded. The response must disclose partial results rather than silently omit unavailable parts.

For `run-with-artifacts`, Analysis Control owns the run and Artifact Service owns artifact details. The gateway can return the run with `artifactsUnavailable` when the artifact service is unavailable. It must not pretend the run has no artifacts.

### Local projection

A service consumes events into a local read model. This removes synchronous dependency but introduces staleness. Notification Service keeps a run view for delivery policy. The view records run version and pauses on gaps.

### Dedicated report

Large cross-domain queries belong in a reporting path or data product, not the transactional request path. The report can state its snapshot time and completeness.

### Batch lookup

When composition is necessary, use bounded batch methods rather than one call per row. Remote N+1 is more expensive and less reliable than database N+1.

## Versioned projection behavior

A correct projection distinguishes four cases:

```text
incoming version = current + 1  apply
incoming version = current      duplicate
incoming version < current      stale
incoming version > current + 1  gap
```

A gap is not “eventual consistency.” It is missing evidence. The consumer pauses the affected key or partition, requests replay, and records an operational finding.

```python
projection = VersionedProjection()
assert projection.apply("run-1", 1, {"state": "queued"}, now_ms=0) == "apply"
assert projection.apply("run-1", 1, {"state": "queued"}, now_ms=1) == "duplicate"
assert projection.apply("run-1", 3, {"state": "completed"}, now_ms=2) == "gap"
```

## Staleness is a product property

A local view must state:

- expected propagation target;
- maximum acceptable age for a use case;
- what the UI or caller sees when the target is exceeded;
- how the service catches up;
- whether monotonic reads are required;
- whether a stale decision is safe.

A delivery dashboard may tolerate a 30-second run view. Authorization for an artifact download should not depend on a 30-second replica unless the capability itself encodes the current decision and expires quickly.

## Replication is not synchronization

Two services must not “keep tables in sync” through bilateral updates. Replication has direction: owner to consumer. If Artifact Service needs tenant and run identifiers, the upload capability or command supplies them under an authenticated contract. It does not update Control’s tables. Artifact Service publishes its fact; Control records an artifact reference under its own transaction.

## Reconciliation

Distributed systems accumulate ambiguity:

- an artifact exists without a Control reference;
- Control references an object that was lost;
- a run completed but Notification never created a delivery;
- a projection paused on a gap;
- two services disagree on a version.

Reconciliation reads each authority through a safe administrative interface or controlled snapshot, compares stable identifiers, and produces findings. Repair remains owner-specific. A reconciliation job must not become a super-service that writes every database.

The capstone classifies:

```text
orphan-artifact:<id>
missing-artifact:<id>
missing-notification:<run-id>
```

A repair action uses a stable idempotency key and is audited.

## Data migration during extraction

Avoid uncontrolled dual writes. The artifact extraction uses:

1. backfill historical content into the new owner;
2. verify checksums and identifiers;
3. shadow candidate reads while legacy remains authoritative;
4. switch new writes to Artifact Service through one controlled path;
5. retain rollback reads for a bounded window;
6. remove legacy writes;
7. decommission after reconciliation.

If temporary dual publication is unavoidable, one source remains authoritative and every duplicate effect has stable identity. “Write both and compare later” is not a plan.

## Python and TypeScript implications

Both tracks implement a versioned projection with identical classifications. TypeScript rejects versions outside the safe-integer range; Python’s arbitrary-size integers do not excuse accepting values that the cross-language contract cannot preserve. Shared vectors define the portable boundary.

## Evidence required before Module 4

You need a single-writer data map, independent migration heads, one projection with gap handling, a stated staleness policy, and reconciliation that finds all planted missing and orphaned effects.
## Authority, copies, and derived state

Every stored value in a distributed system should be classified as one of four categories:

1. **authoritative fact** — only the owning service may decide and write it;
2. **replicated fact** — a versioned copy of an authoritative fact;
3. **derived state** — computed from facts and rebuildable;
4. **ephemeral state** — caches, leases, or routing state with an explicit lifetime.

The classification determines recovery. An authoritative fact requires backup, migration, and controlled mutation. A projection requires replay or backfill. A cache can be dropped. Treating all tables alike produces dangerous recovery plans.

For example:

```text
analysis-control.analysis_run          authoritative
notification.run_view                  replicated
notification.delivery_summary          derived
edge.project_cache                     ephemeral
```

Notification Service may use its run view to select a template, but it cannot change the run state. If its projection is missing version 14 after receiving version 15, it pauses the subject and requests replay. It never “fixes” the source by writing to Control’s database.

## Database per service is an ownership rule

“Database per service” does not require a separate database server for every service. It requires that schemas, credentials, migrations, and writes are owned independently.

A learning or small production topology may host multiple service databases on one PostgreSQL cluster. The important controls are:

- separate database or schema ownership;
- separate credentials;
- no cross-owner writes;
- no application joins across private schemas;
- owner-controlled migrations;
- backup and restore responsibilities;
- audited exceptions for administrative recovery.

A shared physical server can create correlated failure, but it need not erase logical ownership. Conversely, separate servers do not create ownership if services exchange superuser credentials.

## Four cross-service query strategies

Suppose the public API needs a run with artifact details.

### 1. API composition

The gateway requests authoritative run data from Control and artifact data from Artifact Service, then combines them.

Use when:

- fan-out is small and bounded;
- fresh values are required;
- partial response semantics are acceptable;
- the latency budget covers both calls.

The Course 8 result is explicit when Artifact is unavailable:

```json
{
  "runId": "run-42",
  "state": "completed",
  "artifacts": [],
  "partial": true,
  "warnings": ["artifactsUnavailable"]
}
```

The gateway does not pretend that no artifacts exist.

### 2. Consumer-owned projection

Control consumes `ArtifactPublished` events into an artifact-reference projection.

Use when:

- queries are frequent;
- bounded staleness is acceptable;
- the event contains enough data;
- replay and gap detection exist.

The projection stores source version and event identity. An older event cannot overwrite a newer view.

### 3. Batch or analytical copy

An analytical store receives governed extracts.

Use when:

- interactive freshness is not required;
- complex joins are analytical rather than transactional;
- lineage and deletion propagation are defined.

This is not a shortcut for an application endpoint.

### 4. Keep the query local

If a query is central to one invariant and cannot tolerate remote or stale data, the proposed boundary may be wrong. Architecture is allowed to move the boundary rather than invent increasingly complex synchronization.

## Versioned projection algorithm

A projection update should be monotonic per source subject:

```python
def apply(current, event):
    if event.version <= current.version:
        return "duplicate-or-stale"
    if event.version != current.version + 1:
        return "gap"
    return project(current, event)
```

Real systems may have snapshots, tombstones, and partitioned sequences, but the invariant remains: a consumer must know whether it has a complete prefix of the history it claims to represent.

A global event offset alone may not prove subject completeness when messages are partitioned. Course 8 records source fact version in the projection and uses event identity for delivery deduplication.

## Staleness is part of the interface

“Eventually consistent” is incomplete. Define:

- expected propagation target;
- maximum tolerated age;
- how age is measured;
- what the caller sees when the target is missed;
- whether reads fall back to authority;
- how a gap is repaired;
- which decisions may never use the stale view.

The capstone’s notification run view has a 30-second target and a pause-and-replay gap policy. It is suitable for template selection and delivery context. It is not suitable for authorizing a mutation of the run.

The gateway project cache has a five-second target and can bypass the cache. That makes staleness a performance trade-off, not an authority transfer.

## Replication does not create multi-writer state

A common error is to let a replicated view become writable for convenience. Notification may display a project label, then a feature request adds “rename project” to its admin API. If Notification writes its local copy and later publishes an update, the platform now has two writers and conflict semantics it never designed.

The correct options are:

- route the command to the owning service;
- expose an owner operation;
- redefine the business boundary deliberately and migrate authority;
- reject the feature in that context.

Do not turn replication into synchronization by accident.

## Reconciliation is a first-class mechanism

Events and retries reduce inconsistency; they do not prove absence of inconsistency. Reconciliation compares durable owner state and durable dependent state.

For artifact completion, useful findings include:

```text
artifact exists but Control has no reference      orphan candidate
Control references missing artifact               integrity incident
artifact checksum differs from reference          corruption incident
completed run has two current artifacts            invariant breach
projection version behind source beyond target    lag incident
```

Each finding needs:

- stable finding identity;
- severity;
- source evidence;
- owner;
- repair action or manual-review state;
- idempotent rerun behavior.

Reconciliation should be read-only by default. Repair is a separate, authorized action with a stable key.

## Data migration during extraction

Moving Artifact authority is not a `COPY TABLE` operation. A safe sequence is:

1. freeze the target data model and identity rules;
2. create the Artifact-owned store;
3. backfill immutable bytes and metadata with source checksums;
4. record source-to-target identity mapping;
5. compare count, checksum, owner, and retention state;
6. shadow reads against both paths;
7. route new writes to one owner only;
8. retain a bounded rollback read path;
9. remove legacy writers;
10. decommission old data after retention and audit gates.

“Controlled importer” in the capstone extraction plan is not uncontrolled dual write. One migration process owns each imported effect and records it idempotently. Application requests never write both stores independently.

## Why distributed transactions are not the default answer

A coordinator can provide atomic commit across participants in some environments, but it does not remove ownership, availability, latency, or recovery costs. It can also make a local failure block multiple services.

Course 8 first asks whether the invariant should remain within one service. Analysis Control keeps run, idempotency, lease, and event outbox together for this reason. Cross-service workflows use durable state, idempotent effects, and compensation when true independent ownership exists.

The lesson is not “never use distributed transactions.” It is “do not use them to rescue a boundary that split one invariant.”
