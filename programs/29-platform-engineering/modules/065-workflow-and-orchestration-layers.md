---
module_id: PLAT-065
program: Platform Engineering
level: 2
module_number: 65
title: Workflow and Orchestration Layers
status: complete
last_verified: 2026-09-02
---

# Workflow and Orchestration Layers

## One-Page Review

### Governing question

How should a platform coordinate long-running, failure-prone work across people and independent systems while preserving domain authority, durable progress, safe retries, cancellation, compensation, version compatibility, tenant isolation, and operator control?

### Essential definitions

- A **workflow definition** is a versioned program or graph that declares coordination logic; a **workflow execution** is one durable instance with identity, inputs, history, state, and outcome.
- An **orchestrator** decides what should happen next from durable history; an **activity** performs bounded external work and reports an outcome.
- **Durable execution** reconstructs coordination state after process or infrastructure failure from persisted history or checkpoints.
- **Idempotency key** identifies one logical effect so repeated delivery can return or converge on the same result without duplicating it.
- **Retry** repeats an attempt after a classified failure; it is not proof of exactly-once effect.
- **Timeout** bounds a kind of waiting; **deadline** bounds the remaining business duration of a workflow or action.
- **Compensation** is a domain-specific forward action that semantically mitigates a completed effect; it is not database rollback.
- **Signal** or **event** delivers external information to an execution; a **query** reads execution state without changing it.
- **Correlation key** associates external messages with the correct execution or business subject.
- **human task** is a durable request for authorized human judgment with assignee, evidence, deadline, escalation, and immutable decision record.
- **workflow-owned state** records coordination progress; **domain-owned state** remains authoritative in the service that owns the business fact.
- **operator intervention** is a governed command such as retry, skip, compensate, cancel, migrate, or terminate with authorization, reason, and audit.

### Central model, mechanism, or theorem

Model an execution as

$$
W=(i,d,v,x,H,s,b),
$$

where $i$ is stable execution identity, $d$ definition, $v$ definition version, $x$ immutable or versioned input, $H$ ordered durable history, $s$ derived coordination state, and $b$ business correlation identity. A deterministic transition function $F_v(H,x)$ must reproduce the same commands for the same compatible history; nondeterministic I/O belongs in activities. For logical activity $j$, every attempt carries an idempotency key $k=(i,j,o)$ where $o$ distinguishes intentional repetitions. Delivery may be at least once, but the effect authority deduplicates or reconciles $k$. A saga orders committed effects and defined compensations; compensation reduces business harm but cannot promise restoration of the pre-workflow world.

### Critical invariants

- Every request maps to one stable execution identity or an explicitly new intent; client retries cannot silently create duplicate workflows.
- Durable history is append-only or equivalently auditable, and a compatible definition replays it deterministically.
- External I/O occurs in bounded activities, not inside replayed decision logic.
- Every side-effecting activity defines idempotency, timeout, retry classification, result reconciliation, and ambiguous-outcome handling.
- Workflow state never becomes an unauthorized replica of domain truth; consequential decisions reread or validate the domain authority.
- Retries are bounded by deadlines, budgets, backoff, jitter, and dependency health; permanent failures do not spin.
- Compensation order, preconditions, idempotency, possible failure, and residual obligations are explicit.
- Signals, approvals, callbacks, queries, cancellation, and operator commands authenticate and authorize the current action and execution.
- In-flight executions retain compatible code/schema semantics across deployment, rollback, worker loss, and migration.
- Queues, workers, history, schedules, search, and rate limits isolate tenants and workflow classes so one fan-out cannot exhaust the platform.
- Terminal states distinguish succeeded, failed, canceled, compensated, partially compensated, terminated, and timed out.
- Every manual override records actor, authority, reason, prior state, command, result, and follow-up obligation.

### Common failures

A portal request thread as workflow engine; a CI pipeline as universal business coordinator; nondeterministic replay; direct network calls in orchestration code; random execution IDs on retry; “exactly once” effects without receiver deduplication; retrying validation errors; infinite retries without deadline; fixed retry storms; timeout without cancellation semantics; compensations assumed infallible; reverse API calls called rollback; stale approval reused after inputs change; unsigned callbacks; events correlated by display name; workflow database treated as domain authority; mutable definitions breaking in-flight histories; secrets in history; unbounded fan-out; shared hot queue; replay-duplicated logs; operator database edits; termination mistaken for cancellation; and deletion of history before obligations close.

### Compact example

An environment-vending request starts execution `env/acme/payments/prod/42` using definition version 3. The orchestrator records authorization evidence, requests approval, and waits durably. After approval it calls account, network, identity, and catalog activities with stable operation keys. The account call times out after committing; a status lookup by key discovers success, so the retry returns the existing account. Network policy fails permanently. Compensation disables the account and revokes provisional identity, but billing closure is asynchronous, so the execution ends `partially_compensated` with an owned obligation. A later deployment keeps version-3 replay compatible while new requests use version 4. The portal reads status; it does not own the account's existence.

### Connections

This module coordinates the layered APIs from [PLAT-061](061-platform-api-layers.md), portal requests from [PLAT-062](062-developer-portal-architecture.md), catalog context from [PLAT-063](063-software-catalogs.md), and ownership contracts from [PLAT-064](064-ownership-and-metadata.md). PLAT-066 specializes policy decision and enforcement. Environment vending, service brokerage, eventing, audit, and platform reliability follow in PLAT-067 through PLAT-069, PLAT-079, and PLAT-081.

## Governing Question

How can a platform provide reusable coordination for multi-system and human processes without hiding distributed failure, centralizing every domain decision, or turning the developer portal into a fragile monolith?

Platform journeys often outlive one request: create an account, await approval, allocate network ranges, provision identity, deploy baselines, register metadata, and notify an owner. Each participant can be slow, unavailable, duplicated, reordered, or independently changed. A synchronous handler and a few retries do not create durable semantics.

The orchestration layer must remember progress, decide the next command, wait without holding a process, recover after failure, and explain the result. Yet it must avoid becoming the authoritative database for every integrated system. Coordination state and domain state serve different purposes.

Tools differ—code-first durable execution, declarative state machines, DAG engines, business-process engines, CI systems, event choreography—but the engineering questions persist: identity, durability, delivery semantics, failure classification, compensation, authorization, versioning, scale, and operability.

## Why This Matters

Without durable coordination, developers retry requests when the browser times out. Those retries create duplicate accounts, environments, tickets, or charges. Operators then inspect several systems to infer which partial effects exist and which cleanup actions are safe.

Long-running work crosses ownership and trust boundaries. A platform may request an account, but a cloud organization owns account existence. A workflow may wait for security approval, but the authorization policy decides who can approve. Preserving these boundaries limits blast radius and prevents stale orchestration data from overriding reality.

Failures are ambiguous. A network timeout does not reveal whether a remote write committed. Repeating blindly may duplicate an effect; declaring failure may abandon a successful resource. Stable operation identity and status reconciliation turn ambiguity into a recoverable state.

Workflow changes are unusually risky because old executions coexist with new code. A deployment can replay months-old history through modified branches. Schema and worker evolution therefore require explicit compatibility, routing, migration, or draining strategies.

A shared workflow capability is a platform product. It must offer understandable status, predictable error handling, secure callbacks, tenant isolation, repair tools, and evidence—not merely an engine installation.

## Prerequisites and Retrieval

Retrieve finite-state machines, event sourcing and replay, queues and delivery semantics, distributed transactions and sagas, idempotency, correlation, retries/backoff/jitter, timeouts/deadlines/cancellation, eventual consistency, optimistic concurrency, schemas and versioning, human approval, authentication and authorization, secrets, multi-tenancy, rate limiting, observability and tracing, audit, disaster recovery, and control-plane reconciliation.

You should distinguish workflow definition from execution; orchestration from choreography; decision from activity; command from event; scheduling from execution; attempt from logical operation; retry from redelivery; timeout from failure; cancellation from termination; compensation from rollback; durable history from logs; query from signal; correlation key from execution ID; workflow state from domain state; process version from input schema version; and operator intervention from database mutation.

## Learning Objectives

After completing this module, you should be able to:

1. decide when a platform journey needs durable workflow rather than synchronous composition, reconciliation, CI, or choreography;
2. separate deterministic orchestration decisions from side-effecting activities;
3. design stable workflow, business, activity, attempt, and correlation identities;
4. specify retries, timeouts, deadlines, cancellation, heartbeats, and ambiguous-result reconciliation;
5. model sagas and compensations without claiming distributed rollback;
6. build secure signals, callbacks, human approvals, queries, and operator commands;
7. evolve definitions, schemas, workers, and histories while executions remain active;
8. isolate tenants, bound fan-out and history, and operate queues and workers reliably;
9. preserve domain authority, secrets, audit, and deletion obligations; and
10. test replay, duplication, ordering, outages, partial effects, migration, and disaster recovery.

## Core Exposition

### Decide whether coordination is actually needed

Use synchronous composition when work is short, participants can meet one request deadline, and failure can be returned without persistent partial state. Use a domain controller when one declared resource should converge continuously toward desired state. Use CI/CD for build and delivery lifecycle under source revision. Use a workflow when progress spans time, independent systems, human decisions, or ordered compensations.

Do not create a workflow for one idempotent API call. A durable engine adds storage, workers, history, compatibility, operations, and security. It earns that cost when the business process must survive restarts, waits, retries, or partial effects.

Choreography can suit loosely coupled reactions where no component owns the entire outcome. Orchestration suits journeys needing explicit progress, deadlines, ordering, compensation, and a single coordination view. Hybrid designs are common: an orchestrator emits domain commands and consumes events without owning participant internals.

Define the workflow boundary in domain terms. “Provision production environment” may be one orchestration; “ensure database replicas equal three” belongs to a database controller. Avoid an enterprise mega-workflow that encodes every platform capability.

### Separate definition, execution, and business subject

A workflow definition is versioned coordination logic. An execution is one run with durable identity and history. The business subject—request, tenant, environment, account, migration—has its own stable identity. Keep all three explicit.

Choose execution IDs from stable request identity or accept a client-supplied idempotency token. Define reuse policy: reject duplicate active requests, return existing status, or allow an intentional new occurrence. Random IDs generated after a client timeout defeat deduplication.

An execution can coordinate several business subjects, and a business subject can have several intentional executions over time. Store occurrence or operation identity so a retry and a legitimate repeat do not collide.

Correlation keys for callbacks and events must be unambiguous, scoped, and non-secret. Do not correlate on mutable display name or user-provided label. Validate expected source, event type, current state, and occurrence before accepting a message.

### Keep decision logic deterministic

Replay-based engines reconstruct state by re-executing workflow code against recorded history. The same history must yield the same sequence of commands. Current wall clock, unconstrained randomness, direct network calls, mutable global configuration, filesystem reads, and unordered iteration can change decisions.

Use engine-provided deterministic time, timers, random values, and version markers. Pass configuration as versioned input or obtain it through a recorded activity. Sort unordered collections before decisions if the language/runtime does not guarantee order.

Decision logic should schedule activities, timers, child workflows, and waits; receive outcomes and signals; and update compact coordination state. Put external I/O, CPU-heavy work, and nondeterministic libraries in activities.

Event sourcing is one implementation, not the definition of workflow. A state-machine engine may persist checkpoints rather than replay code. The invariant is recoverable, auditable progress with compatible next-decision semantics.

### Design activities as effect boundaries

An activity performs one bounded unit of external work: create account, apply policy, query status, send message, or validate evidence. Boundaries should align with the effect authority and recovery semantics, not arbitrary code organization.

For each activity define input/output schema, operation key, target authority, credential scope, start-to-close and schedule-to-close timeouts, heartbeat or checkpoint behavior, retryable/non-retryable errors, rate limit, cancellation behavior, and result reconciliation.

Activities may be delivered more than once. The engine can durably record a completed result, but a worker can commit the remote effect and fail before reporting it. Exactly-once workflow history does not make the remote API exactly once.

Prefer target APIs accepting an idempotency key and returning the existing outcome. Otherwise create an operation registry or reconcile by a stable provider reference. “Search by similar name” is unsafe deduplication.

### Design idempotency end to end

An idempotent activity maps repeated attempts of one logical operation to the same acceptable effect. It does not mean every HTTP request is byte-identical or that all operations commute.

Construct the operation key from execution ID, logical activity identity, and intentional occurrence. Persist it at the effect authority in the same atomic boundary as the effect when possible. Store request digest and result so reuse with different inputs is rejected.

If the target cannot deduplicate, use read-before-write only when identity and consistency make it safe. A platform-side ledger can reduce duplication but cannot atomically cover a remote commit without protocol support; ambiguous outcomes still require reconciliation.

Compensations also need stable keys. Retrying “delete account” or “refund charge” must not create additional harm. A compensation for one occurrence must not undo a later legitimate occurrence.

### Classify failures before retrying

Distinguish transient dependency failure, throttling, timeout/unknown result, invalid input, failed precondition, authorization denial, conflict, policy denial, capacity exhaustion, cancellation, and internal defect. Each has different action.

Retry transient and explicitly retryable failures with exponential backoff, jitter, cap, attempt or elapsed budget, and dependency-aware circuit breaking. Respect server retry hints. Validation and permission errors ordinarily require changed input or authority, not repetition.

Set per-attempt timeout, overall activity deadline, and workflow business deadline. Unlimited retries can outlive the request's value, hide incidents, consume queues, and surprise users months later.

Timeout means the caller stopped waiting; it does not establish that the target stopped. On ambiguous side effects, query by operation key before retrying. Record both target result and delivery/reporting uncertainty.

### Treat cancellation as a protocol

Cancellation is a requested transition with defined propagation and cleanup; termination stops coordination immediately. They are not interchangeable. Cancellation may wait for activities to reach safe points or run compensation. Termination can leave external effects and obligations.

Define which states accept cancellation, who may request it, whether approval is needed, how child workflows and activities receive it, how non-cancelable effects behave, and which terminal state results.

Activities should heartbeat or checkpoint during long work, observe cancellation, and stop only at safe boundaries. External systems may not support cancellation after commit; then reconcile and compensate if policy allows.

Changing a request after approval is not always cancellation plus resume. Material input changes should invalidate approval and start a new versioned decision or execution.

### Use sagas for multi-system effects

A saga decomposes a long transaction into committed local actions and compensating actions. It provides a way to manage partial progress, not ACID isolation across participants.

Define each forward action's commit evidence, compensation, compensation preconditions, order, deadline, authorization, idempotency, and failure handling. Reverse order is common because later actions depend on earlier ones, but domain semantics can require another order.

Some effects are irreversible: a notification was read, a secret was disclosed, a DNS name was observed, or an external party acted. Compensation can disable, revoke, issue a correction, or create an obligation; it cannot erase history.

Compensation can fail or be forbidden after subsequent state changes. End states must represent partially compensated and manual-remediation-required outcomes. Never mark “rolled back” merely because compensation was requested.

### Orchestrate human decisions explicitly

A human task needs subject, requested action, authoritative evidence snapshot or references, eligible principals, separation-of-duty constraints, deadline, escalation, decision options, comment policy, and immutable decision record.

Authenticate the responder and authorize at decision time. A link possession alone is insufficient for high-risk approval. Resolve current group membership and ensure the requester cannot approve where separation of duty applies.

Bind approval to a digest of material inputs and policy version. If region, classification, cost, owner, or requested privilege changes, expire or invalidate the approval. Do not reuse a generic “approved” flag.

Model delegation, absence, expiration, rejection, request-for-change, and withdrawal. Escalation routes the task; it must not silently convert non-response into approval.

### Secure signals, callbacks, and events

Signals mutate workflow progress and therefore are commands at a trust boundary. Authenticate the sender, authorize the action, validate schema and size, check nonce or message ID, and enforce expected current state.

Use signed callbacks or authenticated message channels with narrow audience and expiry. A callback token should identify a capability no broader than one action on one execution; avoid placing long-lived secrets in URLs or history.

Deduplicate messages by stable event ID and source revision. Define ordering behavior: buffer within a bound, reject stale occurrence, or reconcile from the source. Arrival order is not automatically business order.

CloudEvents can standardize event envelopes, but envelope conformance does not establish business semantics, authorization, delivery guarantee, or correct correlation.

### Preserve domain authority

The workflow owns intent progress: requested, waiting approval, scheduling account creation, compensation pending. The account service owns whether account `A-17` exists and its lifecycle. The authorization service owns current permission. The billing system owns charges.

Cache domain outputs in history for deterministic decisions, but record source revision and observation. Before a consequential later action, reread or use freshness-bounded evidence according to policy. A months-old workflow snapshot cannot prove current authorization.

Avoid dual writes where the workflow updates its own “account active” field and the account service independently updates reality. Store provider reference and last observation, then query or consume authoritative events.

If participants offer desired-state APIs, the workflow can create resources and wait on conditions rather than micromanage their internal steps. This composes orchestration with reconciliation.

### Design workflow state and history carefully

History must contain enough to reproduce decisions and audit commands/outcomes. It should not contain secrets, unbounded payloads, high-volume logs, or every poll result. Store large artifacts in governed object storage and record content-addressed references with access policy.

Separate immutable event history from searchable visibility indexes. Indexes can lag and omit restricted data; they are not execution authority. Queries should return explicit freshness and authorization-filtered fields.

Bound history growth. Use child workflows, continuation into a new execution, snapshots, compaction supported by the engine, or archival. Preserve links so operators can traverse the logical journey.

Define retention by business, audit, privacy, and recovery obligations. Deleting engine history while resources or compensations remain active destroys recovery evidence. Retaining personal data forever is also unsafe.

### Version definitions and data together

An in-flight execution can live across many deployments. Pin or record definition version at start. Workers must route compatible histories to compatible code, preserve old branches, migrate explicitly, or drain old executions.

Replay compatibility is stricter than API compatibility. Reordering commands, changing activity identity, adding a timer on an old path, or reading a new mutable setting can break history even if input/output schemas still parse.

Version input, signal, activity result, and error schemas. Old histories contain old payloads. Use tolerant decoders and explicit transformations; never assume a database migration rewrites immutable history.

Test new workers by replaying representative production histories in a protected environment. Exercise deployment, rollback, mixed workers, and long sleepers. Retain old code and dependencies for the maximum supported execution duration or migrate with verified tooling.

### Compose workflows without a central monolith

Keep workflows aligned to capabilities and bounded contexts. A parent can coordinate child workflows through stable contracts, but it should not inspect every child's internal state. Ownership and deployment should follow domain responsibility.

Avoid one universal “platform workflow” with switches for all products. It becomes tightly coupled to every API and impossible to version independently. Prefer reusable libraries for retry, approval, and evidence contracts plus separate workflow definitions.

Use events for facts and commands for requested actions. Do not have several orchestrators command the same lifecycle without arbitration. Choose one process owner or use a domain resource/controller that serializes intent.

Expose an orchestration API separate from the portal. CLI, API, templates, and automation should invoke the same versioned contract and observe the same execution status.

### Isolate tenants, queues, and workers

Partition or route task queues by trust domain, workload class, dependency, region, and criticality where useful. A noisy batch workflow should not starve production incident remediation.

Enforce per-tenant start rate, concurrent executions, queued tasks, fan-out width, history bytes, payload size, schedules, signals, and search queries. Admission must reject or defer before overload becomes shared failure.

Workers use least-privilege credentials appropriate to their activities. Do not give every general worker administrator access to every provider. Isolate high-risk activities and restrict which workflows can schedule them.

Scale on backlog age and execution latency, not CPU alone. Apply backpressure to callers and parent workflows. Protect the engine database, visibility store, message brokers, and downstream APIs independently.

### Make workflows observable without replay noise

Expose execution ID, business correlation, definition/version, state, current wait, last progress time, deadline, activity attempts, dependency, compensation state, owner, and repair action. Distinguish scheduled, started, heartbeat, completed, failed, and timed-out timestamps.

Propagate trace context across client, workflow decision, activity, and participant APIs while recognizing long waits and retries. Use stable links where one trace cannot span months. Include workflow and operation keys in structured logs.

Replay can execute logging code repeatedly. Use replay-aware logging or event-derived logs so dashboards do not count historical decisions as new attempts.

Metrics include start/success/failure/cancel/compensation rates, end-to-end latency by outcome, wait age, activity latency and attempt count, ambiguous effects, queue backlog age, worker poll health, history growth, deadline misses, stuck executions, and manual interventions.

### Design operator intervention as a safe API

Operators need inspect, retry activity, redrive signal, cancel, terminate, compensate, repair correlation, migrate, and mark external resolution. Each command has preconditions, authorization, reason, preview, idempotency, and audit.

Prefer workflow messages or supported engine APIs over editing persistence tables. Direct mutation can violate history consistency, bypass authorization, and make replay impossible.

“Skip” must record what invariant is waived and which downstream activities may proceed. “Mark complete” needs authoritative external evidence, not operator intuition. High-risk overrides may require dual approval.

Assign residual obligations to an active owner with deadline. An execution is not operationally resolved merely because its alert was silenced.

### Test workflows as histories and failures

Unit-test transition logic with deterministic clocks and generated histories. Test every state/event pair, duplicate and reordered signals, exact deadlines, cancellation races, and invalid transitions.

Activity contract tests inject commit-before-timeout, timeout-before-commit, partial response, throttling, permanent denial, stale status, and duplicated request. Verify stable keys and reconciliation against a fake or sandbox authority.

Replay old histories against new workers. Run property tests such as “one logical operation creates at most one active provider object” under duplicates and crashes. Fault-test worker loss, queue delay, engine failover, dependency outage, and network partition.

Exercise human tasks with identity changes, delegation, expired approval, changed input digest, and unauthorized callback. Load-test worst-case fan-out, mass wake-up, schedule bursts, and one hostile tenant.

### Recover and retire safely

Back up engine state, namespace/queue configuration, encryption keys, definition artifacts, version routing, search schemas, schedules, and non-derivable operator decisions. Participant systems still hold domain truth.

After restore, prevent duplicate dispatch until engine position and participant effects are reconciled. Query ambiguous operations by idempotency key, restore compatible workers, rebuild visibility indexes, verify timers and signals, and then resume gradually.

To retire a workflow definition, stop new starts, inventory active/sleeping executions and external callbacks, drain or migrate them, close compensations and human tasks, revoke credentials, and retain decoders/history for audit policy.

To replace an engine, prove identity mapping, history/outcome preservation, callback routing, schedules, worker version support, search authorization, and disaster recovery. Starting new workflows on the replacement while draining old ones is often safer than translating arbitrary histories.

## Definitions and Notation

Let $D$ be workflow definitions, $V$ definition versions, $I$ execution identities, $A$ activities, $K$ operation keys, $H$ ordered histories, $C$ commands, $E$ events, $S$ states, and $T$ time.

An execution is $W=(i,d,v,x,H,s,b)$. For a replay-based engine, deterministic decision means that compatible executions of $F_v(H,x)$ emit the same command sequence. External outcomes enter through recorded events rather than unrecorded reads.

Logical activity occurrence $o$ has operation key $k=(i,a,o)$. Let $Effect(k)$ denote the authoritative effect associated with $k$. Receiver deduplication seeks the invariant that all accepted attempts using the same $k$ and request digest identify one logical $Effect(k)$; it does not claim that the network delivered one request.

Let forward actions be $f_1,...,f_n$ and compensations be $c_1,...,c_n$. If actions through $f_m$ commit and $f_{m+1}$ fails, a common saga policy attempts $c_m,...,c_1$. The final state depends on compensation outcomes and intervening domain changes; it is not algebraic inversion.

For attempt $r$ with initial delay $d_0$, backoff factor $g>1$, and cap $d_{max}$, a nominal delay is $d_r=min(d_{max},d_0 g^{r-1})$ plus bounded jitter. Retry is permitted only while attempt, elapsed, business-deadline, and dependency budgets remain.

Let $P(success)$ be observed workflow success rate only when every accepted outcome meets the business contract. Treating compensated or manually closed executions as success without separate labels corrupts the measure.

## Mechanisms, Invariants, or Proof Structure

### Durable orchestration protocol

1. Define the business outcome, process owner, boundaries, participants, deadlines, and authoritative facts.
2. Choose synchronous, controller, choreography, CI, or durable workflow deliberately.
3. Assign stable execution, business, activity, occurrence, message, and provider identities.
4. Separate deterministic decisions from bounded side-effecting activities.
5. Specify each activity's schemas, idempotency, timeouts, retries, reconciliation, cancellation, and credentials.
6. Model states, events, commands, waits, human decisions, terminal outcomes, and invalid transitions.
7. Define compensation and residual obligations for every committed effect that may need mitigation.
8. Authenticate and authorize starts, signals, approvals, queries, callbacks, activities, and operator commands.
9. Pin versions, preserve replay compatibility, version payloads, and test histories before deployment.
10. Bound tenant concurrency, fan-out, payload/history, queue use, schedules, and downstream demand.
11. Observe progress, ambiguity, attempts, deadlines, compensation, backlog, version, and intervention.
12. Test crashes, duplicates, ordering, partial effects, migration, restore, drain, and retirement.

### Core invariants

- **Stable intent identity:** repeated delivery of one start request resolves to one intended execution.
- **Deterministic decisions:** compatible replay over one history yields one command sequence.
- **Effect isolation:** external I/O occurs only in activity/effect boundaries.
- **Idempotent occurrence:** repeated attempts for one operation key cannot create unintended duplicate logical effects.
- **Bounded persistence:** retries and waits respect explicit technical and business budgets.
- **Authority preservation:** participants remain authoritative for their domain facts.
- **Compensation honesty:** rollback is never claimed without verified domain outcome.
- **Authorized progress:** every state-changing external input is authenticated and authorized for current state.
- **Version continuity:** every active history has compatible code and payload decoders.
- **Tenant containment:** one tenant or workflow class cannot consume unbounded shared capacity.
- **Terminal precision:** terminal status preserves failure, cancellation, and compensation distinctions.
- **Audited repair:** every override is an authorized durable event with owned follow-up.

### Proof sketch: durable history does not imply exactly-once effects

Suppose activity attempt $q$ sends operation $k$ to service $R$. Service $R$ commits the effect, then the response is lost before the workflow engine records completion. Durable history contains only “attempt started” and a timeout. Any recovery algorithm using history alone cannot distinguish this execution from one where the request never reached $R$. If it retries, the first case can duplicate the effect; if it does not, the second case can omit the effect. Therefore engine durability alone cannot guarantee exactly-once remote effects. Receiver-side deduplication or authoritative reconciliation using stable $k$ supplies the missing information. This is a proof sketch of insufficiency under an ambiguous communication failure.

### Executable retry-budget model

This synthetic program computes capped exponential delays without jitter and shows that the business deadline stops further attempts. It illustrates arithmetic, not a production retry scheduler or dependency policy.

<!-- bijux-verify: {"id":"workflow-retry-budget","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"attempts=4\ndelays=1,2,4\nelapsed=7\nremaining=3\n"}} -->
```python
deadline = 10
base = 1
factor = 2
cap = 4
elapsed = 0
delays = []
attempts = 1

while attempts < 8:
    delay = min(cap, base * factor ** (attempts - 1))
    if elapsed + delay >= deadline:
        break
    delays.append(delay)
    elapsed += delay
    attempts += 1

print(f"attempts={attempts}")
print("delays=" + ",".join(str(delay) for delay in delays))
print(f"elapsed={elapsed}")
print(f"remaining={deadline - elapsed}")
```

The example yields four total attempts after waits of 1, 2, and 4 seconds, with 3 seconds left. Real policies also include attempt duration, jitter, retry hints, cancellation, downstream capacity, and a deadline check before dispatch.

### Verification strategy

Model-check or exhaustively test finite transition tables where feasible. Assert terminal states cannot emit ordinary forward commands, approval cannot apply to a changed digest, cancellation cannot become success, and compensation cannot erase residual obligations.

Replay golden and sampled production histories against every candidate worker. Compare emitted commands, payload decoders, version routing, and replay-safe logs. Test rollback to older workers within declared compatibility.

Inject crashes before send, after send, after remote commit, before result record, and after result record. Verify target deduplication and status reconciliation by operation key. Permute duplicates and message order.

Fault-test engine storage, queue, worker, identity provider, approval provider, and participant outages. Load-test fan-out, mass timer wake-up, schedule burst, long histories, and tenant quotas. Restore from backup without reissuing already committed effects.

Security testing covers forged callbacks, replayed signals, confused-deputy activity calls, cross-tenant IDs, secret/history leakage, visibility indexes, operator overrides, and stale authorization. Audit must connect every command to current identity and policy evidence.

## Alternatives and Trade-Offs

1. **Synchronous call versus durable workflow.** Synchronous composition is simpler and faster; durable workflow survives long waits and partial failures at operational cost.
2. **Orchestration versus choreography.** Orchestration centralizes progress and compensation; choreography reduces central coupling but makes end-to-end state and deadlines harder to reason about.
3. **Code-first versus declarative definition.** Code expresses complex logic and uses familiar tests; declarative graphs improve visualization and constrained analysis but can grow awkward extensions.
4. **Replay versus checkpointed state machines.** Replay offers code-like recovery and full history; explicit state persistence can relax determinism but requires careful transition and migration logic.
5. **Coarse versus fine activities.** Coarse activities reduce history and overhead; fine activities expose retries and recovery precisely. Align boundaries with effects.
6. **Receiver idempotency versus platform ledger.** Receiver deduplication covers commit atomically; a platform ledger helps legacy APIs but cannot remove every ambiguity.
7. **Unlimited retries versus bounded attempts.** Unlimited retry can survive long outages; bounded deadlines protect relevance, capacity, and user expectations.
8. **Compensation versus manual remediation.** Automation reduces toil; irreversible or changed effects may require accountable human judgment.
9. **One workflow versus child workflows.** One history is easy to trace initially; children isolate ownership, scale, reuse, and retention while adding correlation.
10. **Polling versus callbacks/events.** Polling is simple and reconciles loss; callbacks reduce latency and load but require authenticated delivery and correlation. Hybrid designs are robust.
11. **Pinned versions versus migration.** Pinning protects replay and is operationally predictable; migration reduces old-code retention but demands semantics-preserving conversion.
12. **Shared workers versus isolated workers.** Shared fleets improve utilization; isolation limits credential and noisy-neighbor blast radius.
13. **Rich history versus external artifacts.** Rich history aids replay; secrets and large payloads increase cost and risk. Store references for bulky data.
14. **Cancel versus terminate.** Cancel supports cleanup and participant cooperation; terminate stops coordination quickly but leaves effects requiring reconciliation.
15. **Live domain reads versus recorded snapshots.** Recorded values preserve determinism; live reads improve currency. Perform reads as recorded activities under explicit freshness rules.

## Failure Modes and Misconceptions

1. **A request handler can wait for the process.** Process restarts, proxies, browsers, and deadlines make it an unreliable state store.
2. **A CI pipeline is a general workflow engine.** Delivery runners may lack durable human tasks, correlation, compensation, and domain security semantics.
3. **Engine durability makes activities exactly once.** Remote commit and lost acknowledgement create unavoidable ambiguity without target cooperation.
4. **At-least-once means duplicate effects are acceptable.** It describes delivery; application design must deduplicate logical effects.
5. **Idempotent means safe with any input.** One key reused for different request data must be rejected.
6. **Every error should retry.** Invalid input, policy denial, and impossible preconditions need repair or terminal handling.
7. **Timeout means nothing happened.** The target may have committed before the response was lost.
8. **Backoff alone prevents retry storms.** Jitter, budgets, circuit breaking, and downstream admission also matter.
9. **No deadline means more reliability.** Obsolete workflows can consume capacity and perform surprising late effects.
10. **Compensation is rollback.** It is another fallible domain action in a changed world.
11. **Compensations always run in reverse.** Dependencies often suggest reverse order, but domain constraints decide.
12. **Cancellation stops external work immediately.** Participants need a cancellation protocol and safe interruption points.
13. **Termination resolves the business request.** It merely stops orchestration and may strand effects.
14. **Workflow state is domain truth.** It is a coordination projection that can be stale or incomplete.
15. **A callback token needs no authorization.** Tokens can leak, replay, or address an overly broad capability.
16. **Events arrive once and in order.** Deduplication, occurrence checks, bounds, and reconciliation are necessary.
17. **Approval remains valid after input changes.** Material changes invalidate the decision's subject.
18. **Definition deployment affects only new executions.** Replay may run old history through new code.
19. **API-compatible code is replay-compatible.** Command ordering and identities impose stronger constraints.
20. **Search visibility equals execution state.** Indexes can lag and filter; history/state authority must answer transitions.
21. **Logs emitted on replay are new events.** Without replay awareness they duplicate historical decisions.
22. **One queue simplifies operations.** It creates credential mixing, starvation, and shared blast radius.
23. **Fan-out is free because work is asynchronous.** It can overload engine storage, workers, and every participant.
24. **Operators should edit stuck rows.** Unsupported mutation destroys audit and replay consistency.
25. **Deleting history completes privacy cleanup.** External artifacts, logs, indexes, and participants may retain data.

## Worked Examples

### Example 1

**Situation.** A user retries environment creation after an HTTP timeout and receives two environments.

**Reasoning.** Accept a stable request key, map it to one execution, pass stable occurrence keys to every activity, and return existing status on repeated starts. Random execution and provider names cannot deduplicate intent.

**Conclusion.** Stable identity must span client retry through remote effect.

### Example 2

**Situation.** A replayed workflow reads current time and chooses a different timeout branch.

**Reasoning.** Replace wall-clock reads with engine-recorded workflow time and durable timers; move external reads into activities. Replay old history to verify command equivalence.

**Conclusion.** Recovery requires deterministic decision inputs.

### Example 3

**Situation.** Account creation times out after the provider committed.

**Reasoning.** Query the provider by the original operation key. If it returns the committed account and matching request digest, record success; if absent, retry with the same key. Do not create a new name.

**Conclusion.** Reconciliation resolves ambiguous outcomes.

### Example 4

**Situation.** A validation error is retried 10,000 times.

**Reasoning.** Classify it non-retryable, end in a repairable failed state with field-level diagnostics, preserve the request, and let an authorized user submit corrected input as a new occurrence or version.

**Conclusion.** Retry policy follows failure semantics, not generic failure status.

### Example 5

**Situation.** Provisioning creates an account and network, then identity binding fails permanently.

**Reasoning.** Run defined compensations in dependency-safe order. Disable network, request account closure, verify outcomes, and record delayed billing cleanup as an owned obligation. Report partially compensated until all required mitigations finish.

**Conclusion.** Honest saga outcomes preserve residual work.

### Example 6

**Situation.** A production approval is granted, then the requester changes region and privilege scope.

**Reasoning.** The approval is bound to a digest of material inputs and policy version. The change invalidates it; the workflow records the revision and requests a new authorized decision rather than reusing the old flag.

**Conclusion.** Approval applies to a specific decision subject.

### Example 7

**Situation.** Definition version 4 inserts an activity before one already recorded by version 3.

**Reasoning.** Old history would emit a different next command and fail replay. Route version-3 executions to preserved compatible code, use a version marker on compatible branches, or explicitly migrate supported state. New starts use version 4.

**Conclusion.** In-flight histories constrain code evolution.

### Example 8

**Situation.** One tenant starts a workflow that fans out to 500,000 tasks and delays security remediation.

**Reasoning.** Enforce admission and fan-out quotas, partition workload classes, cap in-flight child work, apply backpressure, and scale on backlog age. Security workflows use isolated capacity and credentials.

**Conclusion.** Asynchrony does not remove capacity coupling.

### Example 9

**Situation.** An operator wants to skip a failed network control by editing the engine database.

**Reasoning.** Offer an authorized override command that previews affected invariants, requires reason and perhaps dual approval, appends a durable event, records residual risk, and routes follow-up. Reject direct mutation.

**Conclusion.** Repair is a governed workflow operation.

### Example 10

**Situation.** The workflow engine is restored from a backup taken before several provider commits.

**Reasoning.** Pause dispatch, restore compatible workers and keys, inventory ambiguous operation keys, query each authority, append or import verified outcomes through supported recovery paths, rebuild indexes, verify timers/signals, then resume gradually.

**Conclusion.** Workflow recovery reconciles history with external truth before redelivery.

## Cross-Program Connections

1. **Distributed Systems:** messaging, partitions, ambiguity, idempotency, clocks, and failure detectors determine coordination guarantees.
2. **Database Systems:** transactions, event logs, materialized views, isolation, retention, and recovery shape durable state.
3. **Software Architecture:** bounded contexts, sagas, commands/events, coupling, and domain authority define workflow boundaries.
4. **API & Service Engineering:** idempotency keys, async operations, callbacks, error taxonomies, schemas, and compatibility define participants.
5. **Reliability Engineering:** retry budgets, deadlines, circuit breakers, queues, SLOs, observability, and disaster recovery govern operation.
6. **Security Engineering:** least privilege, confused deputy risks, approval policy, callback authentication, secrets, and audit protect execution.
7. **Human-Computer Interaction:** comprehensible status, actionable errors, approval context, cancellation, and repair paths shape trust.
8. **Formal Methods:** state machines, temporal properties, invariants, replay equivalence, and model checking expose invalid transitions.
9. **Data Engineering:** DAG execution, checkpoints, backfills, lineage, partitioning, and large artifacts share coordination mechanics.
10. **Organizational Design:** process ownership, handoffs, escalation, separation of duty, and residual obligations govern human work.

## References

1. CNCF TAG App Delivery. [CNCF Platforms White Paper](https://github.com/cncf/tag-app-delivery/blob/main/platforms-whitepaper/latest/index.md). Retrieved 2026-09-02.
2. Temporal. [Temporal Workflow](https://docs.temporal.io/workflows). Retrieved 2026-09-02.
3. Temporal. [Temporal Activities](https://docs.temporal.io/activities). Retrieved 2026-09-02.
4. Temporal. [Retry Policies](https://docs.temporal.io/encyclopedia/retry-policies). Retrieved 2026-09-02.
5. Microsoft. [Durable Orchestrator Code Constraints](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-code-constraints). Retrieved 2026-09-02.
6. Microsoft. [Orchestration Versioning](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-orchestration-versioning). Retrieved 2026-09-02.
7. AWS. [Handling Errors in Step Functions Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html). Retrieved 2026-09-02.
8. Argo Project. [Argo Workflows Documentation](https://argo-workflows.readthedocs.io/en/latest/). Retrieved 2026-09-02.
9. CNCF Open Workflow. [Open Workflow Specification](https://github.com/open-workflow-specification/specification). Retrieved 2026-09-02.
10. Object Management Group. [Business Process Model and Notation 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/). January 2014. Retrieved 2026-09-02.
11. Hector Garcia-Molina and Kenneth Salem. [Sagas](https://dl.acm.org/doi/10.1145/38713.38742). ACM SIGMOD, 1987.
12. Wil M. P. van der Aalst et al. [Workflow Patterns](https://doi.org/10.1023/A:1011368105404). Distributed and Parallel Databases 14, 2003.
13. Cloud Native Computing Foundation. [CloudEvents Specification](https://github.com/cloudevents/spec). Retrieved 2026-09-02.
14. OpenTelemetry. [Trace Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/general/trace/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define workflow definition, execution, business subject, orchestrator, activity, history, signal, query, operation key, retry, timeout, deadline, cancellation, termination, saga, compensation, and domain authority. Give four non-equivalences.

### Exercise 2

Trace a side-effecting activity through crash-before-send, commit-before-response-loss, response-before-history-record, duplicate delivery, permanent failure, and cancellation. Specify the evidence needed for each recovery decision.

### Exercise 3

Design a durable workflow for vending a production environment across account, network, identity, policy, observability, catalog, and approval systems. Include schemas, state, security, retry, compensation, and operator controls.

### Exercise 4

Design deployment and data evolution for workflows that can remain active for two years while definitions, worker runtimes, activity APIs, and input schemas change monthly.

### Exercise 5

A shared engine suffers a storage-region loss while some external effects committed after the last backup. Design recovery and later engine replacement without duplicating effects, losing callbacks, leaking tenant data, or abandoning obligations.

## Answers to the Exercises

### Answer 1

A workflow definition is versioned coordination logic; an execution is one durable run; and a business subject is the domain request or resource being coordinated. The orchestrator makes next-step decisions from durable state/history. An activity performs bounded external work. History is the authoritative ordered evidence used to recover coordination. A signal changes execution progress; a query reads it.

An operation key identifies one logical effect occurrence across attempts. Retry repeats an attempt; timeout bounds waiting; deadline bounds remaining business duration. Cancellation asks participants to stop safely and may compensate; termination stops coordination immediately. A saga sequences local commits and compensations. Compensation is a new domain action that mitigates an earlier effect. Domain authority is the participant entitled to decide its business fact.

Key non-equivalences are definition $\ne$ execution, because code and instance state differ; timeout $\ne$ failure, because the effect may have committed; compensation $\ne$ rollback, because it is fallible forward work; cancellation $\ne$ termination, because only cancellation coordinates safe stopping; and workflow state $\ne$ domain truth, because the participant remains authoritative.

### Answer 2

Before send, a crash leaves no remote effect; history plus an unsent task can be retried with the same operation key. After remote commit but before response, history cannot decide; query the authority by key and request digest. If committed, record/reconcile the result; if absent under a sufficiently strong status contract, retry with the same key.

If the response reaches the worker but the worker dies before recording completion, the case is still ambiguous to the engine; receiver deduplication makes redelivery return the existing result. Duplicate delivery always uses the same key and identical digest; the receiver rejects key reuse with different data. A permanent validation or policy failure becomes repairable or terminal rather than retrying.

For cancellation, history must show whether the activity was scheduled/started, its last heartbeat, cancel request, target cancellation capability, and whether an irreversible commit occurred. Stop before commit where supported; otherwise reconcile and run authorized compensation. Evidence includes execution and occurrence IDs, request digest, target receipt/provider ID, source revision, timestamps, attempt outcomes, heartbeat/checkpoint, cancellation acknowledgment, and authoritative final status.

### Answer 3

Accept a stable request ID, tenant, desired environment contract, owner, region, classification, cost, and policy context under a versioned schema. Create one execution per intentional occurrence. States include validating, awaiting approval, provisioning account, configuring network, binding identity, applying policy, enabling observability, registering catalog, verifying, succeeded, canceling, compensating, partially compensated, failed, and timed out.

The orchestrator remains deterministic; activities own external calls. Each receives a stable key, narrow credentials, schema version, deadline, retry classification, and reconciliation endpoint. Directory and policy services authorize start and approval at current time. Approval binds the material-input digest and enforces separation of duty. Signed callbacks include execution, occurrence, source, nonce, expiry, and expected state.

Order effects by dependency. Define compensations such as revoke provisional identity, remove policy binding, disable network, and close account, with idempotency and verified outcomes. Catalog removal cannot delete the account. Irreversible notifications receive corrective actions rather than fictional rollback. Persist references, not secrets or large provider payloads.

Expose permission-filtered status, current wait, attempts, deadline, and repair action. Bound per-tenant concurrency and fan-out; isolate privileged workers. Operator commands support retry, cancel, reconcile, compensate, and authorized skip with preview/reason/audit. Tests inject ambiguous commits, duplicates, callback replay, approval expiry, dependency outage, worker loss, partial compensation, and restore.

### Answer 4

Assign every start an immutable definition version and version all input, signal, activity-result, and error payloads. Maintain tolerant decoders and explicit transforms. Preserve compatible worker code for active versions or route task queues by version. Never change command order or identity on an old replay path.

Before deployment, replay a representative corpus of two-year histories against candidate workers and compare emitted commands. Test mixed old/new workers, rollback, sleeping timers, pending activities, signals from old clients, and old participant responses. Introduce new logic through version markers or new definition versions; new starts select the default while old executions remain pinned.

When an activity API changes, keep an adapter for old request/response schemas or introduce a new activity identity only on a versioned branch. Pass configuration as recorded input or activity result rather than reading mutable environment state during replay. Retain required runtime dependencies and security patches for supported versions.

If maintenance cost becomes unacceptable, offer a semantics-preserving migration with source/target state mapping, invariant checks, dry run, audit, and rollback boundary, or cancel/compensate and restart only when the domain permits. Track active count and maximum remaining duration per version; drain before removing code and decoders.

### Answer 5

Freeze new starts and dispatch after the loss. Restore engine storage, namespace/queue configuration, encryption keys, schedules, version routing, definition artifacts, and compatible workers into an isolated recovery environment. Treat visibility indexes as rebuildable, not authoritative. Inventory every execution and operation whose last durable record predates possible external commit.

For each ambiguous operation, query the owning participant by stable operation key and request digest. Import or append verified completion through supported recovery mechanisms; retry only when the authority proves absence or receiver deduplication makes retry safe. Reconcile pending callbacks by source event ID/revision and reject replays. Verify timers, human tasks, compensation obligations, search authorization, and tenant boundaries before gradual resume. Record irreconcilable cases as owned manual obligations rather than guessing.

For replacement, route new versioned starts to the new engine while old executions drain on the restored engine when possible. Preserve the external orchestration API so portals and clients do not couple to engine internals. If migrations are required, map execution/business/operation identities, current state, deadlines, signals, approvals, compensations, and audit; prove target invariants and prevent both engines from dispatching the same occurrence.

Move schedules and callbacks with fencing tokens or a clear effective boundary. Scope credentials and tenant data stores on both sides, validate search/export filtering, test regional failure and restore, then revoke old workers and credentials only after active histories, callbacks, and obligations reach zero. Retain historical outcomes and decoders according to audit and privacy policy.
