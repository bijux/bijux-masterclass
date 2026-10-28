---
module_id: SEPAT-097
program: Software Engineering: Patterns
level: 2
module_number: 97
title: Strangler Fig
status: complete
last_verified: 2026-08-29
---

# Strangler Fig

## One-Page Review

### Governing question

How can a system transfer one coherent capability at a time from a legacy implementation to a replacement while preserving behavior, data authority, security and rollback—and proving the old path can actually be removed?

### Essential definitions

- The **Strangler Fig pattern** incrementally creates replacement capabilities around an existing system, redirects bounded traffic, and retires superseded legacy paths.
- A **capability slice** is a coherent business behavior, interface, data ownership and operational responsibility selected for migration.
- A **seam/interception point** is a controllable boundary—gateway, facade, adapter, event route, database access abstraction—where traffic can be observed and redirected.
- A **routing policy** maps an explicit cohort/request/capability to legacy, shadow, replacement or blocked handling.
- **shadow traffic** executes a replacement path without letting it cause authoritative effects; outputs are compared after normalization.
- **semantic equivalence** means both paths satisfy the agreed contract, not necessarily byte-identical internal output.
- **source of truth/authority transfer** names which implementation may accept writes and decide business state at each migration state.
- **dual read** compares/serves from two stores under policy; **dual write** mutates both and creates a consistency problem unless a durable protocol governs it.
- A **cutover** changes authoritative routing/ownership for a cohort or capability.
- A **rollback horizon** is the period during which state and compatibility make return to the old path safe.
- **decommission evidence** proves no authorized traffic/dependencies/data/operations require the old capability.

### Central model, mechanism, or theorem

Model each capability (k) as a state machine:

\[
Legacy \rightarrow Shadow \rightarrow Canary(c) \rightarrow Replacement \rightarrow Retired.
\]

Every transition has entry evidence, an invariant set and abort/rollback action. At any instant, exactly one path owns authoritative writes for a given entity/cohort unless a documented transaction/consensus protocol provides one logical authority. Routing must be deterministic and sticky where state/session semantics require it. Retirement is reached only after routes, callers, jobs, data writes, credentials, alerts, runbooks and fallback code for the legacy slice are removed or archived under policy.

### Critical invariants

- Migration slices follow business capability/data ownership, not convenient file or controller boundaries alone.
- The interception layer preserves authentication, authorization, tenant, protocol, timeout, idempotency and observability semantics.
- Exactly one authoritative writer exists per record/cohort at a time; shadow execution cannot produce external effects.
- Routing is deterministic, auditable, bounded and fail-safe; cohorts do not flap unintentionally.
- Equivalence comparison normalizes allowed nondeterminism and detects business/security differences.
- Data backfill and change synchronization have a boundary, gap/duplicate policy and reconciliation.
- Canary promotion/rollback uses explicit correctness, latency, error, saturation and business guardrails.
- Rollback distinguishes stateless traffic reversal from state/schema ownership reversal.
- Legacy defects intentionally preserved or corrected are documented as contract decisions.
- Completion removes the superseded path; a permanent proxy plus two systems is not strangling.

### Common failures

Failures include “rewrite everything” behind one flag; slicing by UI endpoint while sharing hidden transactions; interception that weakens auth or timeouts; random per-request routing of stateful flows; dual writes without atomicity/reconciliation; shadow sending emails/payments; comparing timestamps/IDs byte-for-byte; using production users as unbounded tests; replacement reading legacy tables indefinitely; no backfill boundary; canary metrics without semantic outcomes; rollback after irreversible new writes/schema; defaulting to new on flag-service failure; forgotten batch/admin/export callers; deleting audit/history prematurely; and declaring success while the old system still receives traffic.

### Compact example

Tenant routing uses a stable hash into 100 buckets. Policy `canary_percent=10` sends only tenants in buckets 0–9 to the new invoice read path; all requests for one tenant stay together. Writes remain legacy-owned. Shadow comparisons ignore generated trace IDs but compare normalized amount, currency, permissions and record set. Promotion requires zero security/financial mismatches, acceptable latency/error bounds and a reconciled backfill position. If data remains compatible, route rollback is immediate; write ownership is not moved until a separate gate.

### Connections

[Facade](025-facade.md), [Adapter](021-adapter.md), [Ports and Adapters](029-ports-and-adapters-as-a-structural-pattern.md) and [Branch by Abstraction](../ROADMAP.md) create seams. [CDC](093-change-data-capture-pattern.md) and [Materialized View](096-materialized-view.md) may synchronize migration data. [Transactional Outbox](088-transactional-outbox.md) protects publication. The successor Branch by Abstraction is especially useful when routing happens inside one codebase rather than at a network edge.

## Governing Question

How should engineers turn gradual replacement into a controlled series of ownership transfers, with evidence strong enough to promote, roll back and finally delete legacy capability?

The original strangler metaphor emphasizes gradual growth around an old system rather than a high-risk wholesale rewrite. The important engineering unit is not “percentage of code rewritten”; it is a capability whose traffic, behavior, data and operations have moved. A route that points to new code while writes, reports and emergency procedures still depend on legacy is not complete.

The pattern reduces blast radius and creates feedback, but temporarily increases architecture: two implementations, routing, synchronization, comparison and duplicated operations. Without removal criteria, the migration layer becomes permanent complexity. Each slice needs a short, explicit lifecycle and a measurable endpoint.

## Why This Matters

Large rewrites accumulate untested assumptions until a single cutover. Meanwhile the legacy system changes, business rules remain undocumented, and teams learn too late that batch jobs, integrations or operator workflows were omitted. Incremental replacement exposes those dependencies earlier and can deliver value progressively.

Yet partial migration is a distributed-systems problem. Requests can cross old/new paths, writes can diverge, caches/sessions differ, schemas evolve and retries can duplicate effects. A proxy only redirects bytes; it does not transfer domain authority. Data synchronization via CDC only copies row changes; it does not prove equivalent decisions. Rollback after the new system accepts data the old schema cannot represent may be impossible.

Success therefore depends on capability discovery, contract/evidence design, explicit authority states and decommission discipline—not on the presence of a gateway or feature flag.

## Prerequisites and Retrieval

Learners should retrieve:

- bounded contexts, business capabilities, data ownership and transaction boundaries;
- facades, adapters, anti-corruption layers and stable interfaces;
- feature flags, deterministic cohorts, canary releases and rollback;
- contract, characterization, differential and property-based testing;
- CDC, outbox, idempotency, backfill and reconciliation;
- authentication/authorization, sessions, rate limits and audit logging;
- SLOs, telemetry correlation, incident response and capacity;
- schema expand/migrate/contract and backward compatibility.

Before continuing, identify why routing `/orders/*` to a new service may still be an invalid slice if checkout, refund jobs and reporting share order transactions/data through other interfaces.

## Learning Objectives

After this module, learners can:

1. distinguish incremental strangling from a rewrite deployed behind a flag;
2. identify capability slices and hidden callers/data dependencies;
3. design interception without changing security/protocol semantics;
4. implement deterministic cohorts, shadowing and canary routing;
5. specify authoritative write ownership and data transition states;
6. design semantic differential oracles and characterization evidence;
7. define promotion, rollback horizon and irreversible-change gates;
8. migrate batch/admin/event/reporting paths, not only primary APIs;
9. prove decommission through traffic, dependency, data and operational evidence;
10. choose a different migration strategy when no safe seam exists.

## Core Exposition

### Inventory behavior before drawing target boxes

Build a capability/dependency map from observed traffic, code, database queries, schedules, queues, reports, operator procedures, credentials and ownership interviews. Record business outcomes, clients, protocols, SLOs, security classifications, data read/write sets and transaction boundaries. Runtime telemetry reveals dark callers; static analysis reveals rare paths; neither alone is complete.

Choose a slice with a stable boundary, meaningful value, manageable data and limited coupling. A read-only catalog search often precedes payments. Avoid slicing one step of an atomic workflow unless an adapter preserves the transaction. The first slice should teach routing/testing/operations but not be trivial enough to hide real forces.

### Establish contract and characterization

Legacy behavior is evidence, not automatically specification. Capture representative and adversarial requests, outputs, side effects, authorization decisions, error codes, timeouts, pagination/order, rounding/timezone and performance. Classify each observed behavior:

- required contract;
- tolerated legacy quirk to preserve temporarily;
- defect to correct with explicit product/security approval;
- undefined behavior to reject or specify.

Create contract tests independent of either implementation plus golden/characterization fixtures. For nondeterministic fields, normalize only justified values (request IDs, timestamps within rules), never business/security outcomes. Compare sets with declared ordering semantics; compare money exactly under decimal policy; compare authorization before payload.

### Create the seam

External seams include reverse proxy/API gateway, DNS/path router, message router or facade service. Internal seams include an interface, adapter, repository boundary or branch by abstraction. Database interception is usually the most dangerous because shared schema preserves coupling and bypass paths.

The seam must preserve method/path/body/headers, identity and tenant context, tracing, deadlines/cancellation, rate limits, idempotency keys, retries, cache semantics and error mapping. It must have bounded latency/failure behavior. If policy service is unavailable, default to the safe known owner—not arbitrary replacement. Version and audit routing policy; provide a tested emergency control without turning it into an unreviewed bypass.

### Progress through explicit traffic states

**Legacy.** All authority/traffic old; collect baseline evidence.

**Shadow.** Legacy response/effect remains authoritative. A sanitized copy executes replacement in effect-disabled mode; outputs/decisions are compared. Shadow load is rate-limited and cannot write, email, bill, enqueue, reserve inventory or pollute caches. Sensitive data access is separately approved.

**Canary.** Deterministic cohorts receive replacement authoritative reads or writes under defined scope. Keep users/tenants/entities sticky. Start internal/synthetic, then low-risk cohorts. Observe semantic mismatches, error/latency/saturation and business outcomes.

**Replacement.** New implementation owns capability for all in-scope traffic/data. Legacy may remain rollback/read-only for a defined horizon; stop its writers/jobs.

**Retired.** Routes, dependencies, code/runtime, credentials, data copies and operational obligations are removed or archived. Monitoring proves no authorized traffic during a soak period.

Do not skip states mechanically; some capabilities cannot shadow sensitive effects and instead use offline replay or synthetic datasets.

### Move data ownership deliberately

Common transition topologies:

1. new reads legacy authority through an anti-corruption adapter;
2. backfill a new read model at boundary (p_0), then CDC/outbox changes after (p_0);
3. new owns writes while publishing compatibility facts for legacy readers;
4. legacy becomes read-only/archive, then retires.

Avoid application dual writes. If both stores must reflect one command, designate one authority and propagate durably. A new store populated from legacy is derived until write ownership transfers. At cutover, fence old writers/jobs, drain/inventory in-flight work, record boundary, reconcile, enable new writer and monitor. Primary-key mapping, defaults, nullability, time/money precision and deletes need explicit semantics.

Rollback before write transfer is mostly routing. After new-only writes, rollback requires reverse synchronization and old schema/logic capable of representing them. Define a rollback horizon and forbid incompatible changes until it expires, or state that recovery is forward-fix/failover rather than rollback. Never advertise a rollback button that loses accepted writes.

### Compare semantically and safely

For each shadow/canary request record correlated legacy/new decision, normalized output digest, side-effect intent (not execution), latency and errors. Difference classification distinguishes harmless presentation, expected approved correction, compatibility defect, security defect and unknown. Sample rates must cover rare/high-risk cases; 99.9% equality can conceal every high-value exception.

Comparison itself must avoid data leakage. Store minimal digests/field paths, restrict raw samples, redact tokens/PII and expire evidence. Shadowing can double source load and call external dependencies; isolate/stub effects and capacity-limit it. When the legacy system is wrong, “matching legacy” is not the oracle—use contract/domain invariants and human-approved correction.

### Promote with multi-dimensional gates

Entry/promotion gates include:

- contract/security test pass and unsupported behavior inventory;
- data backfill and delta reconciliation at a named boundary;
- zero unresolved critical semantic/security mismatches;
- error, timeout, latency and saturation within budgets;
- capacity/load/failure tests and observability/runbook readiness;
- cohort size/duration sufficient for rare workflows;
- rollback compatibility/evidence valid;
- owner, on-call, support and compliance approval.

Automate stop/rollback for clear signals while preserving human judgment for ambiguous business risk. Averages hide tail/cohort/tenant harm; segment by route, operation, cohort and classification. Ensure comparison/canary metrics themselves cannot fail open.

### Handle workflows, events and scheduled paths

Interactive APIs are visible; cron jobs, queues, callbacks, exports, reconciliation, admin tools, audit/reporting and disaster procedures are frequently missed. Maintain a caller registry and observe legacy entry points. Events may be published by both paths during transition; include stable logical IDs and exactly one authoritative publisher to avoid duplicate facts.

Long-running workflows can straddle cutover. Pin workflow instance to owner/version or provide compatible state transfer; do not route each step independently. Sessions/caches similarly require stickiness or shared compatible state. In-flight requests must drain or be idempotently retried across the seam.

### Decommission is part of correctness

Define deletion criteria before migration: zero routed/observed callers for a soak period; all writes fenced; batch/event/admin/report consumers moved; data retention/archive/legal hold resolved; fallback expired; backups restore without reactivating old authority; credentials/secrets revoked; hosts/licenses/alerts/runbooks removed; ownership/catalog/docs updated.

Keep evidence and recoverable archives as policy requires, but do not leave a live zombie system “just in case.” A permanent intermediary may be a valid facade, yet if it still supports two implementations without an exit decision, the strangler program has not converged.

### Deterministic cohort routing model

The executable model maps tenant identities stably to buckets and routes a bounded canary. It does not use nondeterministic runtime hashing.

<!-- bijux-verify: {"id":"sepat-097-sticky-canary-routing","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"tenant-a bucket=96 route=legacy\ntenant-b bucket=9 route=new\ntenant-c bucket=22 route=legacy\ntenant-b-repeat=new\nnew-count=1 legacy-count=2\n","stderr":""}} -->
```python
def bucket(tenant):
    return (sum(ord(character) for character in tenant) * 13) % 100

def route(tenant, canary_percent):
    return "new" if bucket(tenant) < canary_percent else "legacy"

tenants = ["tenant-a", "tenant-b", "tenant-c"]
counts = {"new": 0, "legacy": 0}
for tenant in tenants:
    destination = route(tenant, 10)
    counts[destination] += 1
    print(tenant + " bucket=" + str(bucket(tenant)) + " route=" + destination)

print("tenant-b-repeat=" + route("tenant-b", 10))
print("new-count=" + str(counts["new"]) + " legacy-count=" + str(counts["legacy"]))
```

The run proves only deterministic example bucketing and a 10-bucket threshold. Its checksum is not cryptographically secure or statistically uniform. It does not implement policy distribution, authentication, capacity, sessions, data ownership, shadow isolation, concurrency, rollback or production cohort selection.

## Definitions and Notation

Let capability (k) have contract (C_k), legacy implementation (L_k), replacement (N_k), cohort space (U), deterministic assignment (h:U\rightarrow\{0,\ldots,99\}), and policy (R_t(k,u)). Let (A_t(k,u)\in\{L,N\}) be authoritative writer at time (t). The single-authority invariant is (|A_t(k,u)|=1) for each record/cohort except under an explicitly proven logical atomicity protocol.

Let normalization (norm_C(output)) remove only contract-declared nondeterminism. Semantic differential result is (D(x)=compare_C(norm_C(L(x)),norm_C(N(x)))), including authorization, effect intent and errors—not payload alone.

Let data snapshots be (B_L(p)) and migrated (B_N(p)) at comparable boundary (p). Reconciliation asserts a defined projection (M(B_L(p))\equiv_C B_N(p)), not raw schema equality. **Traffic coverage** is the observed fraction across meaningful operation/risk strata; **rollback compatibility** means every accepted new state in horizon can be represented/replayed safely by the old path, stronger than route reversibility.

## Mechanisms, Invariants, or Proof Structure

1. **Map capability/dependencies.** Include APIs, jobs, events, data, operators, security and disaster paths.
2. **Define contract.** Classify legacy behavior, edge cases, SLOs and approved differences with independent oracles.
3. **Choose seam/slice.** Bound coherent authority/transaction and select least invasive interception.
4. **Build parity.** Implement replacement plus adapters, correlation, effect-disabled shadow mode and operational controls.
5. **Prepare data.** Define authority, backfill boundary, synchronization, keys/deletes/schema and reconciliation.
6. **Shadow safely.** Compare normalized semantics on representative/adversarial cohorts without external effects.
7. **Canary deterministically.** Sticky bounded cohorts, capacity/error/semantic/security gates and fast fail-safe routing.
8. **Transfer writes.** Fence old writers, drain in-flight work, record boundary, reconcile and enforce single authority.
9. **Complete ecosystem.** Move batch/admin/event/reporting/support/DR paths and validate rollback/forward recovery.
10. **Retire.** Prove zero dependencies/traffic, resolve retention, revoke credentials and remove old runtime/code/operations.

Incremental migration reduces per-transition blast radius if slices are independently controllable and gates detect relevant failures before expansion. It does not mathematically reduce total complexity; during overlap it increases it. Safety depends on single authority, deterministic routing, valid oracle and rollback premises. Hidden dependencies or an oracle shared with the replacement defeat the argument.

## Alternatives and Trade-Offs

**In-place modular refactoring** removes legacy structure without duplicate runtime/data. Prefer when code is changeable, tests/seams can be created and deployment boundary need not change.

**Branch by Abstraction** changes implementations behind an internal interface in one deployable; excellent for libraries/subsystems without network routing.

**Parallel run** executes old/new for comparison and can support regulated migrations; it is a strangler technique but expensive and dangerous for effects.

**Big-bang replacement** may be rational for small, frozen, well-specified systems with easy rollback/data migration. It concentrates risk but avoids long coexistence.

**Replatform/rehost** changes runtime without changing capability semantics; do not call it strangling if no incremental capability replacement occurs.

**Commercial replacement/SaaS** shifts implementation but still needs capability/data/integration cutover and exit planning.

**Retire without replace** is often best for unused capability; migration inventory should challenge demand.

**Encapsulate and retain** behind a facade can be durable when replacement value is low and isolation is sufficient.

Choose based on changeability, seam availability, capability coupling, data/write model, regulatory comparison, urgency, team capacity and coexistence cost.

## Failure Modes and Misconceptions

- **“A proxy makes a strangler.”** It supplies a seam, not capability, data or ownership transfer.
- **“Incremental rewrite is automatically safer.”** Overlap adds failure modes; gates/rollback make it safer.
- **“Endpoint equals capability.”** Hidden jobs/transactions/events may cross it.
- **“Legacy behavior is specification.”** Preserve required behavior; review defects/quirks explicitly.
- **“Shadow is read-only.”** Replacement dependencies can still email, bill, cache or mutate unless isolated.
- **“Random routing is a canary.”** Stateful entities need deterministic sticky cohorts and bounded exposure.
- **“Dual write keeps stores synchronized.”** Partial failure/order/schema drift creates split authority.
- **“CDC transfers domain ownership.”** It copies technical changes; cutover requires decision/writer fencing.
- **“Rollback is flip the route.”** New state/schema/effects may be incompatible with legacy.
- **“Equal JSON proves parity.”** Security, side effects, errors, ordering and allowed nondeterminism matter.
- **“One week with no alarms proves coverage.”** Rare jobs/tenants/period-close paths may be absent.
- **“Canary averages are sufficient.”** Segment tails and high-risk outcomes.
- **“Old database can stay shared.”** Replacement remains coupled and decommission cannot complete.
- **“Migration ends at 100% traffic.”** Jobs, data, credentials, fallback and operations must retire.
- **“Migration scaffolding is permanent architecture.”** Remove or justify each router/adapter/flag after convergence.

## Worked Examples

### Example 1

**Situation.** Team proposes migrating one controller while it shares a transaction with inventory and payment tables.

**Reasoning.** Controller is a code boundary, not independent capability. Extract read-only inquiry first or introduce a transactional facade/aggregate seam. Splitting one write step would create cross-system atomicity.

**Conclusion.** Slice by business consistency/data ownership, not convenient source folders.

### Example 2

**Situation.** New invoices produce a different JSON field order and trace ID but identical authorized amounts/currency/status.

**Reasoning.** Contract normalization ignores field order/trace ID, compares exact money/status/authorization and set/order rules. Raw byte inequality is noise; normalizing amount would hide a defect.

**Conclusion.** Differential oracles normalize only declared nondeterminism.

### Example 3

**Situation.** Shadow payment handler calls the real processor but discards its response.

**Reasoning.** The charge already occurred. Shadow must stop before effect boundary or use a provider sandbox/stub and compare effect intent. Stable production idempotency keys alone may pollute ledgers.

**Conclusion.** Shadow safety concerns effects, not response routing.

### Example 4

**Situation.** Canary assigns randomly per request; user alternates between carts.

**Reasoning.** Session/state diverges and comparisons are meaningless. Hash stable tenant/cart/user identity and maintain compatible sessions, or restrict canary to stateless reads.

**Conclusion.** Stateful canaries require sticky assignment at the ownership key.

### Example 5

**Situation.** Legacy commit succeeds but new database dual write fails.

**Reasoning.** Retrying may duplicate legacy effect; ignoring diverges. Keep legacy as sole authority and relay changes durably via outbox/CDC into derived new store until controlled writer transfer.

**Conclusion.** One authority plus reliable propagation is safer than uncoordinated dual ownership.

### Example 6

**Situation.** New writes introduce a status legacy cannot represent; a severe latency regression appears.

**Reasoning.** Routing rollback would lose/misread accepted state. Before transfer, maintain backward representability or reverse adapter; otherwise declare forward recovery, pause new writes and fix. Rollback gate should have rejected incompatible status while horizon open.

**Conclusion.** State compatibility, not flag availability, determines rollback.

### Example 7

**Situation.** API traffic is 100% new, yet monthly billing still queries legacy tables.

**Reasoning.** Capability is not retired. Move/report against new authority, validate period close, then observe zero legacy reads before archival. Killing legacy now breaks a rare critical path.

**Conclusion.** Decommission inventory includes scheduled and operator paths beyond request traffic.

### Example 8

**Situation.** Replacement disagrees with legacy on tax rounding.

**Reasoning.** Determine governing regulation/product contract, historical promise and customer impact; do not optimize for parity blindly. Approve correction, version contract, communicate and test affected cohorts; or preserve legacy rounding intentionally.

**Conclusion.** Legacy differential is evidence, while authoritative specification decides approved behavior.

### Example 9

**Situation.** A router control-plane outage occurs during 20% canary.

**Reasoning.** Routers use last-known signed policy with expiry/fail-safe default to known owner, not fetch per request. Alert, freeze promotion and avoid cohort flapping. Emergency override is authenticated/audited/tested.

**Conclusion.** Migration routing is production control-plane state requiring availability/security design.

### Example 10

**Situation.** A hospital replaces medication ordering while old/new rule engines disagree on contraindication warnings.

**Reasoning.** Shadow only de-identified or approved data and never issues orders. Compare exact clinical rule/version, patient context and false-negative/positive strata. Cutover needs data reconciliation, fail-closed degradation, clinician workflow training and rollback-safe state. Named human clinical-safety, privacy, security and pharmacy reviewers approve discrepancies and gates.

**Conclusion.** High-stakes strangling requires domain-governed equivalence and cannot promote solely on aggregate technical metrics.

## Cross-Program Connections

- **Software Evolution:** characterization, seams, dependency discovery and incremental delivery make replacement tractable.
- **Architecture:** bounded contexts and data ownership determine capability slices and extraction topology.
- **Distributed Systems:** dual-write gaps, ordering, idempotency, fencing and state transfer govern coexistence.
- **Database Engineering:** backfill, schema compatibility, replication and reconciliation support ownership migration.
- **Security Engineering:** interception must preserve auth; shadow/copies expand data and control-plane exposure.
- **Testing and Quality:** differential/contract/adversarial tests and independent oracles drive promotion evidence.
- **Reliability Engineering:** cohorts, SLO guardrails, capacity, rollback and decommission runbooks constrain blast radius.
- **Platform Engineering:** gateways, flags, telemetry and deployment automation can enable—but not define—the pattern.

## References

- Martin Fowler, [Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html), revised 2024, retrieved 2026-08-29. Foundational incremental replacement metaphor and transformation guidance.
- Microsoft Azure Architecture Center, [Strangler Fig Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig), retrieved 2026-08-29. Current guidance on proxy-based incremental migration, applicability and issues.
- Amazon Web Services, [Strangler Fig Pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html), AWS Prescriptive Guidance, retrieved 2026-08-29. Current phases, routing and migration considerations.
- Chris Birchall, *Re-Engineering Legacy Software*, Manning, 2016. Practical incremental legacy change, seams, testing and migration approaches.
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall, 2004. Foundational seams and characterization-test techniques.
- Sam Newman, *Monolith to Microservices*, O'Reilly Media, 2019. Incremental decomposition, data migration and operational trade-offs.
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017. Replication, streams, derived data and distributed consistency relevant to coexistence.
- Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010. Deployment pipeline, canary/release and rollback evidence foundations.

## Exercises

### Exercise 1

Define capability slice, seam, shadow, canary, authority transfer and decommission evidence. Distinguish route rollback from state rollback.

### Exercise 2

A 10% tenant canary shows 0.2% output mismatch. Classify what evidence is needed before promotion; explain why the percentage alone is insufficient.

### Exercise 3

Diagnose a migration where writes go to both stores, shadow emails customers, cohorts flap, and a quarterly export still reads legacy.

### Exercise 4

Compare Strangler Fig, in-place refactoring, Branch by Abstraction, big-bang replacement and retirement for a modular monolith with one unsupported vendor subsystem.

### Exercise 5

Design a strangler plan for an unfamiliar national benefits-eligibility service. Cover seams, data, correctness, security, cohorts, rollback, exceptional/manual workflows and retirement evidence.

## Answers to the Exercises

### Answer 1

A capability slice is coherent business behavior plus interface, data and ownership. A seam is a controllable interception boundary. Shadow executes replacement without authoritative effects and compares semantics. Canary gives deterministic bounded cohorts authoritative replacement behavior. Authority transfer fences old decision/writes and designates new authority at a named boundary. Decommission evidence proves no callers/jobs/events/data obligations/credentials/operations require legacy. Route rollback merely redirects requests; state rollback additionally requires every new accepted state/effect/schema to be representable and synchronized back within the horizon. After irreversible state, only forward recovery may be honest.

### Answer 2

Segment mismatches by operation, tenant/risk, authorization, money/state effect, error and approved nondeterminism. One security false-negative or incorrect high-value payment can block promotion even when 99.8% matches. Verify sample/traffic coverage includes rare workflows, legacy correctness classification, independent contract/domain oracle and no shadow effects. Also require data reconciliation at a named position, error/timeout/latency/saturation budgets, capacity/failure tests, support/runbook readiness and rollback compatibility. Resolve/approve every critical mismatch and set duration/cohort evidence sufficient for expected rare-event frequency. The scalar rate hides severity, correlated cohorts and unobserved paths.

### Answer 3

Stop expansion and external shadow effects. Dual writes create split authority: select one store (likely legacy until planned cutover), capture its committed changes through outbox/CDC, reconcile the derived store and fence the other writer. Shadow email proves effect isolation failed; use intent capture/sandbox and investigate duplicates. Cohort flapping requires deterministic sticky key and last-known fail-safe versioned policy. Quarterly export means decommission inventory was incomplete; migrate/validate it through a period fixture before retirement. Add effect-ledger alerts, routing audit, caller/database telemetry and explicit write/cutover state machine. Do not declare rollback until new-state compatibility is proven.

### Answer 4

Refactor in place for modules that are changeable and share one transaction; create tests/seams without distributed coexistence. Use Branch by Abstraction to replace an internal library/vendor client behind one interface with build/run-time switching. Use Strangler Fig for capabilities needing independently routed deployment/data ownership, especially around the unsupported vendor subsystem, with an anti-corruption seam. Big-bang is reasonable only if the subsystem is small/frozen, fully specified and its data cutover/rollback is cheap. Retire functionality with no consumers rather than recreate it. A hybrid is strongest: modularize/refactor to create seams, branch the internal dependency, strangle externally separable capabilities, and delete unused portions.

### Answer 5

Inventory online applications, appeals, caseworker/admin tools, batch eligibility runs, external agencies, letters/payments, fraud/audit, disaster and legal retention. Slice a read-only status capability before eligibility decision; route through an authenticated facade preserving identity, tenant/jurisdiction, deadlines, idempotency and audit. Establish independent statutory-rule fixtures and characterization; classify legacy defects with policy owners. Shadow only approved minimized data with all payment/letter/case effects disabled, then use deterministic jurisdiction/case cohorts and risk strata.

Keep one eligibility writer. Backfill new storage at boundary, relay changes durably, reconcile case/rule/version/benefit amounts and deletes, then fence/drain legacy jobs before transferring writes. Return command/version evidence, pin long-running appeals to compatible workflow owner, and keep manual exception routes explicit. Define backward-representable rollback horizon; after new-only rule/state, use forward recovery unless reverse mapping is proven. Gate on zero critical statutory/security mismatches, latency/capacity, accessibility, reconciliation and support readiness. Named human benefits-policy, legal, privacy, security and caseworker reviewers approve corrections/degraded modes. Retire only after zero observed callers through seasonal/quarterly cycles, all agency/batch/manual paths move, archives/legal holds resolve, credentials and fallback expire, and restore exercises no longer reactivate legacy authority.
