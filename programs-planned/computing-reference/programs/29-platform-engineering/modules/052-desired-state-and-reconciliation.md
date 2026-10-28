---
module_id: PLAT-052
program: Platform Engineering
level: 2
module_number: 52
title: Desired State and Reconciliation
status: complete
last_verified: 2026-09-02
---

# Desired State and Reconciliation

## One-Page Review

### Governing question

How should a platform turn durable, versioned intent into safe convergent effects when observations are stale, events are lost or duplicated, writes conflict, providers time out, desired state changes mid-flight, and deletion itself requires work?

### Essential definitions

- **desired state** is the durable outcome a consumer or higher-level controller is authorized to request; it is not a script of provider calls.
- **observed state** is versioned, time-qualified evidence about managed reality; absence of evidence is not evidence of absence.
- **reconciliation** is a repeatable comparison of current desired and observed state that plans bounded actions, records status, and schedules further observation when necessary.
- A **level-based** controller derives work from the latest state, while an **edge-based** handler assumes each transition event must be processed exactly once.
- A **fixed point** is a state where another reconcile under unchanged intent and reality proposes no effect and only stable status.
- **idempotency** means repeating an operation with the same identity does not create a different logical outcome; it does not mean every transport attempt is executed once.
- **field ownership** names which actor may assert a field, whereas **resource versioning** detects an object-level stale read-modify-write.
- **drift policy** declares whether a difference is corrected, adopted, ignored, reported, paused, or routed to human decision.
- **unknown outcome** means a request may have taken effect even though the controller did not receive authoritative completion evidence.
- A **finalizer** is a durable claim that deletion cannot finish until its owner completes or explicitly dispositiones cleanup.
- **observed generation** correlates status with the desired-state generation on which the observation or decision was based.

### Central model, mechanism, or theorem

Let $d_g$ be desired state at generation $g$, $w$ the external world, $o=O(w,t)$ a time-qualified observation, and $R(d_g,o,k)=(A,s,q)$ a reconciliation function producing bounded actions $A$, status $s$, and next scheduling decision $q$ from durable correlation state $k$. A fixed point satisfies $A=\varnothing$ and stable $s$ under unchanged $d_g$ and $w$. Event delivery alone cannot prove convergence. Eventual convergence additionally requires a quiescent/compatible target, attainability, fair execution, sufficiently fresh observation, eventual successful effects or terminal classification, stable ownership, and no competing controller that continually undoes the result.

### Critical invariants

- Desired state is authenticated, authorized, validated, versioned, durably stored, and separable from controller-owned status.
- Reconcile requests carry resource identity, not an instruction to replay a historical event; every run rereads relevant current state.
- A lost, duplicate, reordered, coalesced, or expired event may delay work but cannot permanently hide drift once resync occurs.
- Effects use stable logical identity, idempotency/correlation, conditional writes, and post-timeout observation before destructive retry.
- Each field and external effect has one explicit authority or a deterministic conflict/transfer protocol.
- Status identifies desired generation, observation source/time/freshness, condition status/reason, and terminal versus retryable failure.
- Retry delay, attempts or elapsed time, queue size, concurrency, per-key hot-loop behavior, fairness, and resync are bounded and observable.
- Drift is classified by ownership and consequence; correction is never assumed universally safer than adoption or pause.
- Deletion keeps enough durable state and authority to clean up, prove orphaning, or surface an unresolved obligation.
- Controller upgrades preserve stored intent, status meaning, field ownership, in-flight correlations, finalizers, and old/new skew.
- Convergence claims are scoped to a resource generation, target population, observation freshness, and domain outcome.

### Common failures

Treating a watch as a durable exactly-once command log; replaying event payloads instead of rereading state; equating an empty queue with convergence; blind overwrite of user or peer-controller fields; retrying an ambiguous create and duplicating infrastructure; holding a worker while polling a long provider operation; unlimited immediate requeues; one poison resource starving a shard; setting `Ready=True` without `observedGeneration`; reporting stale status as current; correcting intentional operator changes without a drift contract; using leader election as an exactly-once guarantee; removing finalizers to make dashboards green; deleting the control record before the external effect; building multi-resource invariants from unrelated eventual writes; rolling a new controller that cannot interpret old correlations; and claiming convergence while desired state or policy continues changing.

### Compact example

A `DatabaseClaim` requests class, region, owner, recovery tier, and deletion policy. Admission stores generation 7 and a stable external identity. A reconciler reads the latest claim, status, secret reference, policy revision, and provider observation. It records `Provisioning`, submits an idempotent create, persists the provider operation identity, and returns without blocking. A watch or timed poll requeues the key. After a timeout, the next run searches by correlation identity before retrying. A user changes size, creating generation 8; status for generation 7 remains visibly stale until the new plan is observed. A manual provider tag is adopted, but an unauthorized public endpoint is corrected because drift policies differ. On deletion, a finalizer keeps the claim while connections drain, a backup is verified, the instance is deleted or explicitly orphaned, credentials and network bindings are removed, and terminal evidence is retained. Only then is the finalizer removed.

### Connections

This module deepens capability contracts and declarative resources from [PLAT-007](007-platform-capabilities-versus-tool-catalogs.md), [PLAT-015](015-apis-and-declarative-resources.md), and [PLAT-023](023-kubernetes-declarative-resources.md), and applies the plane boundary from [PLAT-051](051-control-plane-and-data-plane-separation.md). PLAT-053 through PLAT-056 develop custom resources, operators, finalizers, and multi-tenant controllers; later fleet, upgrade, reliability, and governance modules reuse the convergence model.

## Governing Question

How can a platform continually reduce meaningful difference between declared intent and real outcomes without depending on perfect event delivery, erasing another actor's work, amplifying failure through retries, or abandoning effects whose result is uncertain?

Declarative APIs are often summarized as “say what you want, not how to do it.” That is only the interface half. A useful platform must repeatedly observe, decide, act, and explain until the requested outcome is reached, rejected, superseded, paused, deleted, or shown to require intervention. The controller operates across API storage, caches, queues, other controllers, external providers, and a changing world. Every boundary admits delay and partial failure.

Reconciliation makes those failures ordinary by deriving work from durable state rather than trusting a transient command. It does not make effects exactly once, state immediately consistent, or all desired states achievable. Reliable reconciliation comes from explicit identity, ownership, observation, conflict, retry, deletion, and status contracts.

## Why This Matters

Platform controllers concentrate repeated authority. A harmless-looking mismatch can trigger thousands of writes, delete data, oscillate capacity, overwrite security policy, or overload a shared provider. Automation accelerates both correction and damage.

Events are unreliable as complete history. Watches disconnect, retained history expires, handlers restart, queues coalesce duplicate keys, and caches lag. If correctness requires replaying every edge exactly once, ordinary control-plane behavior becomes data loss. Level-based reconciliation can recover by listing and comparing current state.

External APIs create ambiguous outcomes. A create may succeed while the response is lost. Immediate retry can duplicate a database, address, payment, or DNS record. Conversely, assuming success can strand intent. Controllers need stable correlation and an observe-before-repeat rule.

Status is another API, not decoration. Consumers and controllers make decisions from readiness, failure, endpoint, and deletion state. A green condition based on an old generation or stale observation can be more dangerous than an explicit `Unknown`.

Deletion exposes lifecycle truth. Removing the declaration does not undo cloud resources, data, credentials, routes, or obligations. A reconciled deletion protocol preserves the record until disposition is known.

## Prerequisites and Retrieval

Retrieve declarative APIs, resource identity and versioning, spec/status separation, optimistic concurrency, field ownership, idempotency, conditional requests, event streams and watches, cache consistency, queues and fair scheduling, exponential backoff and jitter, partial failure, timeouts, leases and fencing, eventual consistency, fixed points, control theory, transactions and sagas, state machines, authentication/authorization, tenancy, audit, schema evolution, progressive delivery, backup/restore, and decommissioning.

You should distinguish desired from defaulted/admitted/effective state; observed from inferred state; an event from authoritative state; resource generation from storage `resourceVersion`; idempotency from exactly-once execution; reconciliation from rollout; convergence from queue emptiness; steady state from permanent stasis; field ownership from object ownership; drift from malicious change; retryable from terminal and unknown outcome; finalizer from cleanup code; deletion requested from deletion complete; and control-loop health from managed outcome health.

## Learning Objectives

After completing this module, you should be able to:

1. model desired, observed, effective, and terminal state with generation and freshness;
2. design a level-based reconcile contract that tolerates missed, duplicate, reordered, and coalesced events;
3. define stable resource/effect identity, idempotency, conditional writes, and unknown-outcome recovery;
4. allocate field and effect ownership and resolve conflicts or transfers without blind overwrite;
5. specify status conditions, reasons, observed generations, observation times, and domain outcomes;
6. build bounded queues, fairness, rate limiting, backoff, jitter, resync, and poison-resource isolation;
7. choose correction, adoption, ignore, report, pause, or deletion policies for drift;
8. coordinate multi-resource and external workflows without pretending eventual writes are atomic; and
9. test, upgrade, recover, and retire reconcilers and their managed effects safely.

## Core Exposition

### Model four kinds of state before writing a loop

Start with declared desired state: the consumer-owned outcome accepted by the API. Admission may default, validate, authorize, and bind policy to produce admitted intent. A controller may derive an implementation plan or effective configuration. The world then contains actual resources and effects, of which the controller has only observations. Status summarizes what the controller knows and has decided.

Keep these states separate. `spec.replicas=3` is desired. A defaulted disruption policy is admitted/effective intent. Three created Pods are controller-managed resources. Three ready application instances are an observed domain outcome. `Ready=True` is a claim about that outcome and needs generation/freshness.

For a resource at generation $g$, record the policy/schema/controller revisions used to interpret it. The same stored declaration can produce different effects after default, policy, or provider revisions change. If such changes are intended to trigger reconciliation, make those dependencies observable and versioned.

Never treat the controller's cache as reality without qualification. It is a useful, potentially stale observation. For external systems, store observation source, provider resource/operation identity, provider version where available, and observation time. Transition old evidence to `Unknown` when its freshness contract expires.

### Make reconciliation level-based

A reconcile request should normally identify a resource key. The function rereads the latest desired object and all necessary related state, observes managed effects as needed, then computes the next bounded actions. It does not assume why it was queued or replay the triggering payload as a command.

This property makes event loss recoverable. A create and three updates may coalesce into one key; the reconcile sees only the latest generation and moves toward it. A duplicate key yields the same comparison. A delete/update reorder is resolved by current existence, deletion timestamp, generation, and owned dependencies.

Events still matter for latency and efficiency. Watch desired objects, owned dependents, relevant policy/configuration, provider callbacks, and dependency health. Map each event to the smallest affected set of resource keys. Use periodic resync or durable inventory comparison to repair missed mappings and external drift. An event is a hint that state may differ, not proof of what the current state is.

If every historical transition is itself a business obligation—such as a payment or append-only audit event—model it as a durable event/work resource with identity and terminal status. Do not smuggle command-log semantics into an ordinary mutable desired-state object.

### Define a pure decision boundary and bounded effects

Separate observation and planning from effect execution conceptually, even if implemented in one process. Given desired state, observations, policy, and durable correlations, a planner should return a comprehensible set of actions and status decisions. This makes unit tests and dry-run/diff possible.

Bound each reconcile by effects, bytes, calls, and elapsed time. Create a small batch, persist correlation/status, and requeue rather than holding a worker through a 30-minute cloud operation. Bounded work improves fairness and makes shutdown/restart safe.

Order actions using prerequisites and risk. Establish identity before creating dependents, validate backup before destructive replacement, remove traffic before terminating capacity, and verify replacement before retiring the old resource. State the rollback or forward-recovery point for irreversible steps.

Avoid status churn. Write status only when its semantic content changes or freshness policy requires an update; do not update timestamps on every no-op and trigger yourself indefinitely.

### Specify convergence and its assumptions

Let $R(d_g,o,k)=(A,s,q)$. The controller is at a local fixed point when another run with unchanged inputs proposes $A=\varnothing$, produces semantically stable status $s$, and needs only scheduled re-observation $q$ required by freshness. This is local because other controllers and the external world can still change.

A distance $\delta(d,o)$ can help prioritize progress, but it is domain-specific. Replica count difference is numeric; an unsafe public endpoint, missing backup, schema migration, and unknown provider result cannot be safely collapsed into one scalar. Prefer ordered predicates and invariants for high-consequence state.

Eventual convergence is a conditional claim. Desired input and relevant policy must become quiescent or mutually compatible; the target must be attainable; observations and workers must eventually run; transient operations must eventually succeed or become terminal; permissions/quota must permit progress; and peers must not undo the action. Changing demand can produce healthy continual regulation without a global fixed point.

Define convergence per generation and population. A controller may have processed generation 12 while half the fleet remains on revision 11. An API resource can be reconciled while its application outcome is unhealthy. Report both controller progress and domain effect.

### Build identity before retries

Assign a stable logical identity to the desired resource and each externally significant effect. Use API UID plus owned effect name, or a persisted operation/idempotency key that survives controller restart and leadership change. Do not derive identity from an attempt timestamp.

If a create request times out, classify the outcome as unknown. Query by idempotency key, operation ID, unique tag, deterministic name, or provider inventory. Retry creation only when the provider contract proves the same logical effect will be returned or absence is authoritative.

Idempotency belongs end to end. A client-side key is useless if an intermediate broker discards it. Define retention, scope, collision behavior, payload mismatch, response replay, and deletion/recreation semantics. A provider that accepts one request per key may still execute non-idempotent downstream work unless its contract covers the effect.

For updates, include preconditions or provider versions where possible. For deletion, repeat by stable external identity and treat “not found” according to ownership and observation reliability. Never guess that timeout means failure.

### Use optimistic concurrency for shared API state

Read-modify-write must protect against lost updates. In Kubernetes, a stale `resourceVersion` on update yields a conflict; the controller rereads current state, recomputes its change, and retries under bounds. Do not retry the identical stale object.

Patch semantics matter. A broad replacement can erase fields added after the read. A narrow patch reduces accidental ownership but can still violate invariants if based on stale values. Use conditional operations when the new value depends on current state.

Server-Side Apply tracks field managers and reports conflicting assertions. A controller should apply only fields it owns, use a stable manager identity, and force conflicts only for objects/fields whose authoritative ownership is explicit. Force is a governance decision, not generic conflict handling.

`generation` and `resourceVersion` solve different problems. Generation tracks changes to desired-state semantics according to resource strategy. Resource version identifies storage revisions for concurrency/watch. Status should correlate with generation; writes should use concurrency controls appropriate to the API.

### Allocate ownership at field and effect granularity

Write an ownership table for consumer fields, admission defaults, policy-derived values, controller-managed child objects, autoscaler values, credentials, provider resources, and status. One resource can legitimately have multiple managers when fields are disjoint.

Avoid two controllers continuously setting the same field. If authority must transfer—such as replicas moving from a human declaration to an autoscaler—define the handoff state, shared value, field release, acceptance evidence, and rollback. Server-Side Apply can represent field transfer, but cannot decide organizational authority.

External effects need ownership too. Tags/labels should identify owning control resource UID, tenant, controller, and operation where the provider supports them. Decide whether pre-existing resources may be adopted and what proof prevents hijacking another owner’s resource.

Leader election prevents ordinary concurrent active loops but not stale external actors, delayed requests, or duplicate effects. Add fencing tokens where the provider can reject obsolete authority, plus idempotency and observation where it cannot.

### Turn drift into policy, not surprise

Drift is observed state differing from authorized effective intent. It can result from failure, a human emergency change, another controller, provider defaults, autonomous scaling, malicious action, restore, or changed reality. Cause and ownership determine response.

Choose per field/effect: correct automatically, adopt into desired state, ignore as provider-owned, report only, pause for approval, or mark unsupported. Security exposure may require immediate correction; an emergency operator change may require preservation and review; provider-generated identifiers are observed, not corrected.

Record correction loops and flap rate. Repeated alternating changes indicate competing controllers or an impossible invariant. Stop or degrade before an automated tug-of-war overloads the API or harms service.

Import/adoption must validate identity, tenant, lifecycle responsibility, data disposition, policy, and current safety. “Same name” is rarely sufficient proof of ownership.

### Make status a precise, monotonic explanation where possible

Status should answer: what generation was considered; what was observed and when; which operation/revision is active; what conditions hold; why progress is waiting or blocked; what the consumer can do; and when the controller will try again.

Use conditions with stable types and machine-readable reasons. `Ready`, `Progressing`, `Degraded`, or domain-specific conditions need documented polarity and summaries. `Unknown` is legitimate when observation is missing or stale. Messages add human detail but are not stable automation interfaces.

Set `observedGeneration` on status or individual conditions so readers can reject a green result about an older spec. Do not advance it merely because the object was dequeued; advance it only for the state the condition actually evaluates.

Separate terminal invalid intent from transient provider failure and unknown outcome. Preserve the last successful effect while a new generation fails when safe, and report both active and desired revisions. Avoid unbounded histories in status; use events, logs, traces, or separate operation resources for detailed history.

### Engineer work queues for fairness and repair

Queue keys, not event payloads, and deduplicate identical keys. Multiple changes before processing then require one current-state evaluation. Ensure dependent events enqueue owners through indexes rather than listing the whole fleet.

Use exponential backoff for retryable failure. A simple cap is $b_k=\min(B,b_0 2^k)$ for attempt $k$; add jitter so many controllers do not synchronize. Bound attempts or elapsed retry for operations whose caller needs a terminal decision, while continuing low-rate reconciliation where the durable desired state still exists.

Distinguish error retry from deliberate polling. A controller-runtime reconcile error is normally rate-limited with exponential backoff; a known external completion time or health refresh should request an explicit `RequeueAfter`. A permanent validation failure should not hot-loop until relevant input changes.

Cap queue depth and concurrency, isolate tenants/classes, and prioritize lifecycle/safety work carefully. One poison key must not occupy every worker. Measure queue depth/age, adds, retries, processing latency, errors by reason, hot keys, dropped/coalesced work, provider throttling, and oldest unfinished generation.

Resync is a repair mechanism, not permission to ignore watch correctness. Stagger and shard full inventories, paginate, cache, and prevent reconnect/list storms. If the system cannot finish a resync before the next one, reduce work or add capacity rather than stacking scans.

### Handle dependencies without deadlock

A desired resource often references identity, network, secret, policy, artifact, quota, or another capability. Validate reference scope and authorization. Report a dependency condition rather than retrying an impossible provider call.

Avoid cycles such as A waiting for B `Ready` while B waits for A. Define partial order, bootstrap state, or a joint coordinator. Readiness gates should express the minimum prerequisite for the next safe action, not total completion of the other resource.

Watch dependencies and enqueue consumers through bounded indexes. If one global policy change affects a million resources, stage the fan-out with revisions, cohorts, and rate limits. Do not synchronously enqueue the entire fleet without capacity analysis.

Cache dependency observations with freshness. A transient dependency API outage may permit continued last-known-good operation but should not authorize new high-risk effects unless the contract allows it.

### Coordinate multi-resource workflows explicitly

Writing several API objects separately is not an atomic transaction. Readers can observe intermediate states, a controller can crash between steps, and rollback may be impossible after an external effect.

Model a workflow state machine or operation resource with durable step identity and compensations. Each step checks current desired generation, prerequisites, prior effect evidence, and cancellation/deletion. Use prepare/commit-style activation where resources can be staged then switched atomically at a boundary.

For replacement, create the new resource, verify domain readiness, shift traffic, observe, then retire the old. If desired state changes mid-flight, either safely retarget the workflow or mark the prior generation superseded and reconcile from current reality. Never blindly continue an obsolete destructive plan.

Sagas provide compensating actions, not transaction rollback equivalence. A deleted database may not be recoverable by “create database.” State irreversible points, backup/evidence requirements, and human authorization.

### Reconcile deletion as desired state

Deletion request changes the goal from “resource present” to a disposition contract. Stop admitting new dependents, drain or transfer work, preserve or export data as promised, delete or orphan external effects, remove routes/credentials/secrets, and record evidence.

A finalizer is a durable key indicating which controller owns unfinished cleanup. When deletion timestamp appears, run deletion reconciliation; remove only your finalizer after your obligation is satisfied or an explicitly authorized orphan/force policy records the consequence. Finalizers are not executable callbacks by themselves.

Design for stuck deletion: visible condition/reason, last attempt, external identity, safe retry, escalation, and privileged disposition. Manually stripping a finalizer can abandon resources or data. If it is necessary after the owner disappears, first inventory and complete or explicitly accept the obligation.

Deletion order matters. Removing credentials before deleting a cloud resource can make cleanup impossible. Removing the control record before the provider confirms disposition destroys correlation. Preserve least authority necessary to finish, then revoke it promptly.

### Secure reconciliation authority

Use a dedicated workload identity and least-privilege permissions per controller boundary. Separate spec/status, namespace/tenant, provider account/project, and destructive operations where practical. Admission must not assume reconciliation will repair unauthorized intent after side effects.

Validate all observed/provider data before using it in resource names, patches, status, logs, or shell-like integrations. Protect secrets from status and logs. Correlation tags must not contain credentials or sensitive tenant data.

Audit desired changes, admission decisions, field conflicts/force, high-consequence actions, adoption, orphaning, finalizer overrides, and break-glass access. Correlate resource UID, generation, reconcile/operation identity, controller revision, actor, and provider request without claiming every loop iteration is a business event.

Rate and blast-radius limits are security controls. A compromised desired object should not create unlimited effects; quotas, bounded fan-out, policy, per-tenant concurrency, and irreversible-action approval contain authority.

### Upgrade controllers and schemas without losing intent

New controller code must read old stored spec/status, managed fields, correlations, operation states, and finalizers. During rollout, old and new replicas may alternate reconciliation, so support an explicit skew window or fence versions from incompatible resources.

Make schema changes additive when possible. Conversion must preserve intent round trips; default changes must not silently mutate existing semantics; condition reasons and ownership are APIs. Test old object/new controller, new object/old controller where allowed, leadership transfer, crash at every workflow step, and rollback after stored-state change.

Do not change deterministic names, field manager identity, idempotency-key derivation, or provider tags without migration. A controller can otherwise create duplicate effects or lose ownership of existing fields.

Roll out by tenant/cell/resource cohort and observe reconcile errors, latency, conflicts, retries, queue age, provider calls, drift, deletion, and domain outcomes. Rollback binary only when it can understand state already written; otherwise use forward repair.

### Test properties, not only happy paths

Unit-test the planning function across desired/observed combinations. Repeating the same inputs should yield no additional logical effect after success. Updating desired state should supersede obsolete plans safely. Missing observation should produce `Unknown` or bounded discovery, not invented absence.

Use env/API integration tests for optimistic conflicts, status subresource, field ownership, watches, cache delay, deletion timestamp, owner references, and finalizers. Fake clients often omit important server semantics.

Inject provider timeouts before and after effect, duplicate callbacks, throttling, eventual visibility, stale reads, partial list, permission loss, quota, not-found ambiguity, and irreversible failure. Restart or change leader at every persisted boundary.

Load-test hot keys, a million quiet resources, global dependency change, watch reconnect, full resync, poison records, tenant skew, and recovery backlog. Verify useful convergence time and domain outcomes, not merely controller availability.

### Retire reconcilers without orphaning authority

Inventory every desired object, finalizer, owned child, external effect, provider operation, field manager, queue, identity, permission, webhook, status consumer, alert, backup, and restore path. Decide migrate, delete, orphan, archive, or transfer ownership for each.

Stop new admission, complete or transfer in-flight workflows, and move field/finalizer ownership under an explicit protocol. A replacement controller must understand existing correlations and deletion obligations before the old one stops.

Prove no objects retain a finalizer whose controller no longer exists. Revoke provider credentials and API permissions only after effects are dispositioned. Preserve required audit evidence without retaining executable authority.

Retirement is complete when restoring an old backup cannot silently reactivate the obsolete controller or recreate deleted effects. Update recovery procedures, images, manifests, policies, dashboards, and documentation accordingly.

### Use an executable reconciliation inventory

The following synthetic inventory checks whether ten reconcile scenarios record foundational properties. It is a review aid, not proof of convergence, idempotency, safety, ownership, or production behavior.

<!-- bijux-verify: {"id":"desired-state-reconciliation-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scenarios 10\ndesired_versioned 10\nobservation_fresh 9\nownership_explicit 9\naction_idempotent 9\nstatus_precise 9\nretry_bounded 9\ndeletion_owned 8\ndrift_policy 9\nrecovery_tested 8\n","stderr":""}} -->
```python
scenarios = [
    ("create", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("update", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("provider-timeout", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("field-conflict", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("manual-drift", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("dependency-change", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("leader-change", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("schema-upgrade", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-import", 1, 0, 0, 0, 0, 0, 0, 0, 0),
    ("forced-orphan", 1, 1, 1, 1, 1, 1, 0, 1, 0),
]
fields = [
    "desired_versioned", "observation_fresh", "ownership_explicit",
    "action_idempotent", "status_precise", "retry_bounded",
    "deletion_owned", "drift_policy", "recovery_tested",
]
print("scenarios", len(scenarios))
for index, field in enumerate(fields, start=1):
    print(field, sum(scenario[index] for scenario in scenarios))
```

The incomplete import must remain report-only until ownership and identity are proved. A forced orphan may be a valid authorized disposition, but it cannot be counted as controller-completed deletion or recovery.

## Definitions and Notation

- $d_g$: desired/admitted state at semantic generation $g$.
- $w$: relevant real-world state, only partially observable.
- $O(w,t)=o$: observation of $w$ qualified by source/version/time $t$.
- $k$: durable correlation state, including resource UID, external identity, operations, workflow step, and ownership.
- $R(d_g,o,k)=(A,s,q)$: reconciliation producing bounded actions $A$, status $s$, and scheduling decision $q$.
- $T(w,A)$: world transition caused by applying actions, potentially partial or ambiguous.
- $\delta(d,o)$: domain-specific difference measure or ordered mismatch set; not necessarily a scalar metric.
- $b_k=\min(B,b_0 2^k)$: capped exponential delay before jitter for retry attempt $k$.
- **generation**: semantic revision of desired state as defined by the API resource strategy.
- **resource version**: storage revision used for watches and optimistic concurrency, with semantics defined by the API server.
- **fixed point**: unchanged-input state where reconciliation proposes no further logical effect and stable status.
- **quiescence**: interval in which relevant desired state and policy stop changing enough for a convergence claim.
- **terminal**: no automatic retry is useful until intent, policy, authority, or the world changes.
- **unknown**: the controller cannot establish whether an effect happened or an observation remains current.

## Mechanisms, Invariants, or Proof Structure

1. Persist authenticated, authorized, validated desired state independently from controller-owned status.
2. Assign stable resource/effect identities, generations, ownership, and policy/schema revisions.
3. Watch relevant state only to enqueue keys; reread current desired, dependent, correlation, and observed state on every reconcile.
4. Compute a bounded action plan from the latest state and stop obsolete plans when generation changes.
5. Protect shared writes with narrow ownership, field management, and optimistic concurrency; reread after conflict.
6. Persist idempotency/operation identity before effects and resolve unknown outcomes by observation before retry.
7. Report condition, reason, observed generation, active revision, freshness, terminal/retryable/unknown state, and next action.
8. Bound work, concurrency, queue, retries, polling, resync, and fan-out; add jitter, fairness, and poison-key isolation.
9. Reconcile drift and deletion under explicit correction/adoption/orphan/disposition policy.
10. Coordinate multi-resource changes as persisted workflows with prerequisites, compensations, and irreversible points.
11. Test duplicate/missed events, stale caches, conflicts, timeouts, leader change, partial effects, scale, upgrades, restore, and retirement.

The fixed-point claim is local: if unchanged $d_g$, observation $o$, and correlation $k$ cause $A=\varnothing$, another identical decision cannot reduce difference further. It does not prove that $o$ is fresh, that $w$ equals $o$, or that the desired outcome is safe. Those are separate observation and domain invariants.

Level-based repair follows because a complete current observation contains the relevant level even when intermediate edges are absent. This only holds if the observation and ownership mapping are sufficient; hidden external state or an incomplete list can still prevent repair.

The backoff formula caps retry spacing but does not bound total load by itself. Attempt limits, elapsed deadlines, jitter distribution, concurrency, caller retry layers, provider cost, and queue admission all affect amplification.

## Alternatives and Trade-Offs

- **Level-based reconciliation versus command processing:** current-state comparison repairs missed edges; durable commands preserve each obligation but require event identity, ordering, and terminal processing.
- **Watch versus periodic observation:** watches reduce latency/list load; resync repairs missed mappings and external changes at scan cost.
- **Full observation versus cached/indexed observation:** full reads simplify reasoning; caches reduce load but introduce staleness and mapping complexity.
- **Read-modify-write versus Server-Side Apply:** conditional updates support value-dependent logic; apply simplifies declarative field management but requires explicit field ownership.
- **Correct versus adopt drift:** correction preserves declared authority; adoption preserves emergency/provider change but can launder unauthorized state.
- **One controller versus cooperating controllers:** one owner simplifies invariants; disjoint field/effect owners improve modularity but require stable handoffs.
- **Immediate effect versus persisted workflow:** direct action reduces latency; workflows survive long operations and partial failure with more state.
- **Frequent status versus write suppression:** fresh status aids decisions; unnecessary updates amplify storage/watch load and can self-trigger loops.
- **Aggressive retry versus bounded backoff:** rapid retry reduces isolated transient latency; bounds/jitter protect dependencies and fairness during failure.
- **Global queue versus tenant/cell queues:** one queue is efficient; isolation contains poison keys and noisy tenants at scheduling cost.
- **Automatic correction versus approval:** automation reduces drift time; approval protects irreversible, ambiguous, or human-owned changes.
- **Finalized deletion versus immediate API removal:** finalizers preserve obligations; stuck cleanup retains objects and needs escalation/disposition.
- **In-place update versus replacement:** in-place is cheaper; staged replacement offers verification/rollback boundaries but doubles temporary capacity and complicates identity.
- **Rollback versus forward recovery:** rollback is fast before incompatible state; forward repair is safer after schema/effect irreversibility.

## Failure Modes and Misconceptions

- **“The event says update, so apply its payload.”** The payload may be stale and later edges may be coalesced; enqueue the identity and reread current state.
- **“Every event will arrive.”** Watch history can expire and clients reconnect; list/watch and bounded resync must repair gaps.
- **“The queue is empty, therefore converged.”** External reality may drift, observation may be stale, and mappings may miss a resource.
- **“Idempotent means exactly once.”** It means repeats preserve one logical outcome under a scoped contract; attempts can execute multiple times.
- **“A timeout means nothing happened.”** The effect may have committed; query by stable correlation before retrying.
- **“Leader election prevents duplicates.”** An old leader or delayed request can still act; use fencing/idempotency/observation.
- **“Conflict means force.”** Conflict exposes another owner or stale computation; reread and resolve authority before override.
- **“The controller owns the whole child object.”** Users, admission, autoscalers, and peers may own disjoint fields.
- **“Generation and resourceVersion are interchangeable.”** One tracks desired semantics; the other supports storage concurrency/watch semantics.
- **“Ready remains true until failure is proved.”** Once observation is too stale or for an older generation, current readiness may be unknown.
- **“More status is more observable.”** Per-loop writes and unbounded history overload storage and obscure stable signals.
- **“Drift should always be corrected.”** Emergency change, provider-owned state, or transferred authority can make correction harmful.
- **“Retry forever because intent is durable.”** Retry at a safe low rate when useful, but expose terminal/blocked state and prevent queue starvation.
- **“A finalizer runs cleanup.”** It only blocks removal; a live, authorized reconciler must perform and verify cleanup.
- **“Removing a stuck finalizer fixes deletion.”** It removes the record and may abandon data, cost, credentials, or policy.
- **“Several eventual writes form a transaction.”** Intermediate states and crash boundaries are observable; use workflow/activation protocols.
- **“A reconcile success means the product outcome is healthy.”** It may only mean no API call failed; verify domain results.
- **“Rollback the binary to recover.”** New stored state or external effects may be unreadable/irreversible; forward repair may be required.

## Worked Examples

### Example 1

A controller misses three update events during a watch disconnect. Relisting shows generation 14, and one level-based reconcile computes directly from generation 14. Conclusion: current state, not edge replay, provides repair.

### Example 2

A network create times out after the provider commits. The controller searches by persisted claim UID/idempotency key, finds the network, and adopts its provider ID instead of issuing a second create. Conclusion: unknown outcome requires observation before retry.

### Example 3

A user edits a Deployment label while a platform controller owns image and security context. A narrow apply preserves the label; a whole-object update would erase it. Conclusion: ownership is field-specific.

### Example 4

An autoscaler and service controller alternately write replicas, generating hundreds of updates. A handoff removes replicas from the service manager and lets the autoscaler own it. Conclusion: competing control loops oscillate rather than converge.

### Example 5

`Ready=True` has `observedGeneration: 8`, but the object is at generation 10. The portal displays “reconciling/unknown for current configuration,” while the old active revision remains healthy. Conclusion: readiness needs generation context.

### Example 6

Ten thousand failed claims retry immediately against a throttled provider. Capped exponential backoff with jitter, per-tenant concurrency, and terminal handling for invalid regions preserve healthy work. Conclusion: retry scheduling is a correctness and blast-radius mechanism.

### Example 7

A human temporarily closes a public endpoint during an incident. The controller's drift policy recognizes a break-glass annotation and pauses rather than reopening it, while recording expiry and review. Conclusion: automatic correction can undo safety work without authority context.

### Example 8

A database replacement creates and verifies a replica, shifts clients, validates recovery, then deletes the old instance. A generation change before traffic shift supersedes the old workflow. Conclusion: multi-resource change needs persisted stages and obsolete-plan checks.

### Example 9

A claim is deleted while the provider is unreachable. Its finalizer retains external identity and reports `Deleting=Unknown`; it is not stripped. After recovery, cleanup completes and credentials are revoked before finalizer removal. Conclusion: deletion is reconciliation.

### Example 10

A new controller changes its field-manager name and deterministic provider tag. Canary tests show conflicts and attempted duplicate discovery, so rollout stops and a migration preserves old ownership/correlation. Conclusion: operational identities are compatibility surface.

## Cross-Program Connections

- **Control theory:** reference value, sensor, error, actuator, delay, saturation, stability, hysteresis, and oscillation illuminate control loops, while software adds ownership and partial failure.
- **Distributed systems:** stale reads, partitions, retries, idempotency, leases, fencing, eventual consistency, and impossibility of inferring remote outcome shape reconciliation.
- **Data structures:** work queues, priority queues, indexes, sets, deduplication, graphs, and state machines determine controller scale and dependency traversal.
- **Database systems:** optimistic concurrency, compare-and-swap, transactions, isolation, logs, materialized views, and sagas explain storage and workflow boundaries.
- **API engineering:** schemas, spec/status, generations, conditions, long-running operations, idempotency keys, errors, and versions are public reconcile contracts.
- **Reliability engineering:** overload, backoff, jitter, poison work, SLOs, graceful degradation, recovery, and fault injection protect control and managed outcomes.
- **Security engineering:** least privilege, tenant scope, field authority, adoption proof, audit, break glass, deletion, and secret handling limit automated power.
- **Data engineering:** desired-to-observed comparison resembles declarative pipelines, CDC materialization, late data, watermarks, replay, and data quality reconciliation.
- **Systems engineering:** requirements allocation, interface state, modes, invariants, verification, lifecycle, and disposal prevent local-loop thinking.
- **Organizational design:** controller ownership mirrors team authority; ambiguous boundaries manifest as field fights, manual drift, and unresolved deletion.

## References

1. Kubernetes Authors, “Controllers,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/architecture/controller/
2. Kubernetes Authors, “Kubernetes API Concepts,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/api-concepts/
3. Kubernetes Authors, “Server-Side Apply,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/server-side-apply/
4. Kubernetes Authors, “Finalizers,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/
5. Kubernetes SIG Architecture, “API Conventions,” current repository documentation, retrieved 2026-09-02. https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
6. Kubernetes Authors, “Operator Pattern,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
7. Kubernetes Authors, “Extending Kubernetes,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/extend-kubernetes/
8. Kubernetes SIG API Machinery, “controller-runtime reconcile package,” current Go package documentation, retrieved 2026-09-02. https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/reconcile
9. Crossplane Authors, “Managed Resources,” version 1.20 documentation, retrieved 2026-09-02. https://docs.crossplane.io/v1.20/concepts/managed-resources/
10. Marc Brooker, “Timeouts, Retries, and Backoff with Jitter,” Amazon Builders’ Library, retrieved 2026-09-02. https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
11. David Yanacek, “Avoiding Insurmountable Queue Backlogs,” Amazon Builders’ Library, retrieved 2026-09-02. https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
12. Amazon Web Services, “REL05-BP03 Control and Limit Retry Calls,” AWS Well-Architected Framework, retrieved 2026-09-02. https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_limit_retries.html
13. Roy Fielding and Richard Taylor, eds., “JSON Patch,” RFC 6902, April 2013. https://www.rfc-editor.org/rfc/rfc6902
14. Betsy Beyer et al., “Addressing Cascading Failures,” Site Reliability Engineering, Google, 2016. https://sre.google/sre-book/addressing-cascading-failures/

## Exercises

### Exercise 1

Design a level-based reconciler for an external object store bucket. Specify desired, admitted, observed, and status state; resource/effect identity; ownership; event mappings; resync; and convergence assumptions.

### Exercise 2

A provider returns a timeout for create, exposes eventually consistent list, and offers no idempotency key. Design an unknown-outcome protocol that minimizes duplicates without claiming certainty. Include identifiers, delays, observation, escalation, and deletion implications.

### Exercise 3

Two controllers and users share a workload object: the platform owns image/security defaults, an autoscaler owns replicas, and users own routing labels. Define field ownership, conditional updates, conflict behavior, authority transfer, status, and upgrade tests.

### Exercise 4

A controller starts at 1-second retry delay, doubles to a 5-minute cap, and applies full jitter uniformly from zero to the capped delay. Compute the uncapped and capped delay at attempts 0, 1, 8, 9, and 12; give the mean jittered delay, then explain why the arithmetic is not a retry-load proof.

### Exercise 5

Design deletion and retirement for a database controller managing instances, backups, credentials, DNS, network policy, finalizers, and provider operations. Include unreachable-provider, force/orphan, audit, controller upgrade, and restore scenarios.

## Answers to the Exercises

### Answer 1

Desired state includes claim UID, owner/tenant, region, name policy, versioning, encryption class, access policy, retention, and deletion disposition. Admission binds policy/default revisions and rejects unauthorized public access. Observed state carries provider bucket ID, tags, configuration version, access findings, last observation time, and confidence; status carries observed generation, active configuration, conditions/reasons, endpoint reference, and operation correlation without credentials. A stable effect identity derives from claim UID and is persisted before create. Users own intent; admission owns defaults; the controller owns provider configuration and status; provider-generated IDs are observed. Claim, policy, credential, and owned-reference changes enqueue the key; provider callbacks are hints; staggered inventory resync repairs missed events and manual drift. Convergence for generation $g$ requires quiescent compatible policy, attainable region/quota, fresh provider observation, successful/terminal effects, stable ownership, and no competing actor. Domain verification checks encryption/access/versioning, not only API success.

### Answer 2

Persist a globally unique claim/effect token before calling create and place it in the provider name or unique tag if either is atomically searchable. On timeout mark `CreateOutcomeUnknown`, retain the request fingerprint/time, and stop blind creation. Wait beyond the documented visibility interval with jitter, then query direct lookup and paginated inventory repeatedly under a bounded observation window. If exactly one matching resource appears, validate tenant/configuration and adopt its immutable provider ID; if multiple appear, quarantine/escalate; if none appears, uncertainty remains because list is eventually consistent. After a risk-based deadline, require operator/provider evidence before retry or use a new attempt linked to the original and detect duplicates later. Surface consequence and block dependent destructive work. Deletion must search by all attempt correlations and cannot remove the finalizer until every possible effect is deleted or an authorized orphan decision accepts the uncertainty. Without provider idempotency or authoritative absence, exactly-once creation cannot be guaranteed.

### Answer 3

Publish an ownership matrix: users apply routing labels under their manager; platform controller applies image digest and security-context fields; admission may default but should not fight later managers; autoscaler owns replicas once scaling is enabled. Each actor applies only its fields with stable manager identity. Value-dependent operations use fresh reads and resource-version preconditions. Conflicts trigger reread and an authority decision; the platform forces only its documented authoritative security/image fields, never user labels or autoscaler replicas. Scaling handoff first aligns the replica value, lets managers temporarily share/assert it, removes replicas from the user's/platform configuration, and confirms the autoscaler has ownership; disabling reverses through an explicit state. Status records effective image/security revision, autoscaler reference, observed generation, conflicts, and current application outcome. Tests cover user updates during reconcile, server-side apply conflicts, handoff interruption, old/new manager names, schema list/map topology, rollback, and no oscillating writes.

### Answer 4

Before the cap, $b_k=1\times2^k$ seconds: attempts 0 and 1 have caps 1 and 2 seconds; attempt 8 has 256 seconds. Attempt 9 would be 512 seconds uncapped but is capped at 300 seconds, as is attempt 12 whose uncapped value is 4096 seconds. With full jitter uniformly on $[0,b_k]$, mean delays are 0.5, 1, 128, 150, and 150 seconds respectively. This does not prove retry load: arrival cohorts, synchronization outside jitter, attempt/elapsed limits, success probability, service time, downstream throttling, other client layers, concurrency, queue age, payload cost, and fairness determine traffic. Uniform jitter can also produce near-zero delays. Model the whole retry population and test failure/recovery bursts.

### Answer 5

Deletion sets a durable desired disposition. Stop new bindings, drain connections, create and verify the promised final backup, remove DNS/traffic, delete or revoke credentials at the point that preserves remaining cleanup access, remove network bindings, then delete the provider instance by immutable ID and verify absence under provider consistency rules. A controller finalizer retains claim, correlations, backup evidence, and authority until every obligation is complete. Provider unreachability yields `Deleting=Unknown/Blocked` with last observation/attempt and bounded retry, not finalizer removal. Force/orphan requires privileged authorization, explicit data/cost/security consequence, inventory evidence, retained owner, and audit; orphan transfers responsibility rather than claiming deletion. New controller versions must read old steps, IDs, conditions, and finalizers and survive leader change at each boundary. Retirement stops admission, migrates or dispositiones all claims/effects, proves no finalizers remain, revokes credentials, deletes queues/webhooks/images/policies, updates status consumers and runbooks, and ensures restoring backups cannot reactivate the old reconciler or duplicate effects.
