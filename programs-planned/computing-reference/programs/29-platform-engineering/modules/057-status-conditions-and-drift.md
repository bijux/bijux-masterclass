---
module_id: PLAT-057
program: Platform Engineering
level: 2
module_number: 57
title: Status, Conditions, and Drift
status: complete
last_verified: 2026-09-02
---

# Status, Conditions, and Drift

## One-Page Review

### Governing question

How should a platform report current, generation-correlated, freshness-bounded knowledge and detect meaningful drift without turning status into desired state, an event history, a secret store, or a source of controller conflict?

### Essential definitions

- **status** is a controller-produced projection of current knowledge about a resource; it is neither desired state nor reality itself.
- A **condition** is the latest observation of one named property, with status `True`, `False`, or `Unknown`, an observed generation, transition time, machine reason, and human message.
- **observed generation** identifies the desired-state generation on which a status claim was based.
- **freshness** bounds how long an observation remains adequate for a particular decision.
- **polarity** states whether `True` means normal (`Ready`) or abnormal (`Degraded`); it must be documented per condition type.
- A **reason** is a stable machine-readable cause category; a **message** is occurrence-specific human detail.
- **drift** is a meaningful difference between authorized effective intent and observed state after schema, default, ownership, and comparison policy are applied.
- **normalization** maps semantically equivalent representations to a comparison form.
- A **drift policy** maps a classified difference to correct, adopt, ignore, report, pause, delete, or escalate.
- **flapping** is repeated condition or effect transition caused by noisy evidence, unstable thresholds, or competing authorities.

### Central model, mechanism, or theorem

Let desired generation be $g$, effective intent $e_g$, world observation $o_t$, and status projection $S=P(e_g,o_t,k)$ using durable controller state $k$. A condition $c$ is usable for a current decision only when its type/producer is trusted, $c.\text{observedGeneration}=g$, and observation age is within the property-specific freshness bound. For required conditions $C$, a conservative readiness aggregate is `False` if any fresh current requirement is definitively false, `True` if every requirement is fresh/current/true, and `Unknown` otherwise. Drift is computed per owned path after normalization:

$$
\Delta=\{p\mid p\in A,\ N_e(e_g[p])\not\equiv N_o(o_t[p])\},
$$

where $A$ is the controller’s declared comparison/authority set. Detection alone authorizes no mutation; policy $\pi(p,\text{cause},\text{risk})$ selects the response.

### Critical invariants

- Spec/admitted intent, controller workflow, observed domain facts, and presentation status remain separate.
- Every consequential condition is generation-correlated and freshness-qualified; stale or absent evidence becomes `Unknown`, never silently current.
- Condition types are unique and owned; writers update only their fields/types with optimistic concurrency.
- `lastTransitionTime` changes only when the condition’s `status` changes under the documented contract, not on every reconcile, reason, or message refresh.
- Reasons are bounded stable API values; messages are sanitized details and never parsing interfaces.
- Readiness reports the managed outcome, while progressing, degraded, drifted, deletion, and controller health remain distinguishable.
- Drift comparison canonicalizes defaults, versions, ordering, units, server-generated fields, and secrets before classifying a difference.
- Field/effect ownership determines whether a difference is corrected, adopted, ignored, reported, paused, or escalated.
- Status writes are semantically deduplicated and bounded in size/rate; histories and high-cardinality evidence live elsewhere.
- Upgrades preserve condition meaning, polarity, reasons, ownership, generation semantics, and old-status interpretation.

### Common failures

Setting `Ready=True` for generation 8 while spec is generation 9; treating absent condition as healthy; encoding workflow in one `phase`; changing `lastTransitionTime` on every poll; parsing messages; using hundreds of unbounded reasons; putting logs, child lists, secrets, or provider payloads in status; letting two controllers own `Ready`; aggregating one green child while another is unknown; byte-diffing defaulted or reordered objects; correcting HPA-owned replicas; adopting a malicious security change; confusing empty drift scan with fresh proof; retrying status conflicts with stale objects; triggering a reconcile loop from timestamp-only writes; and changing a condition’s meaning in place.

### Compact example

A `Database` at generation 12 requests version 16. Status still contains `Ready=True, observedGeneration=11`, so consumers treat readiness as unknown for generation 12. The operator sets `Progressing=True` with stable reason `Upgrading`, retains `Ready=True` only if version 15 is still serving under a documented availability condition, and reports target/current versions separately. Provider observation is timestamped and expires after five minutes for routing decisions. Drift comparison ignores provider-generated ID and normalizes storage units, adopts an allowed provider maintenance timestamp, reports a human-added tag, and immediately corrects an unauthorized public endpoint because ownership/risk policies differ. `lastTransitionTime` changes only when a condition moves among `True`, `False`, and `Unknown`; changing progress detail updates the message without fabricating a new transition.

### Connections

This module builds on reconciliation from [PLAT-052](052-desired-state-and-reconciliation.md), CRD schemas from [PLAT-053](053-custom-resource-definitions.md), workflow state from [PLAT-054](054-operator-state-machines.md), and deletion evidence from [PLAT-056](056-finalizers-and-deletion.md). It uses observability foundations from [PLAT-038](038-observability-provisioning.md). PLAT-058 and PLAT-059 extend condition aggregation across dependencies and failure recovery.

## Governing Question

How can an API tell consumers what a controller currently knows, which desired revision that knowledge covers, how fresh and trustworthy it is, and what meaningful difference remains—without creating false health, unstable automation, or controller fights?

Status is a public claim made under uncertainty. A controller sees cached Kubernetes objects, delayed provider APIs, partial workflow checkpoints, health probes, and policy revisions. The world can change immediately after observation. Therefore status is not “actual state”; it is a versioned, time-qualified projection of evidence.

Conditions make important properties machine-readable while preserving uncertainty. Drift detection compares effective intent with observation, but the comparison is meaningful only after ownership and normalization. Together they form the explanatory surface of reconciliation: what target was evaluated, what is true now, what is unknown, what differs, what action policy selected, and what should happen next.

## Why This Matters

Other systems automate from status. A rollout controller waits for readiness, a composition waits for dependencies, an autoscaler reads current capacity, a user interface colors resources, and incident automation pages on degradation. A stale green condition can authorize traffic or deletion incorrectly. An ambiguous red condition can trigger destructive replacement.

Drift correction concentrates authority. A byte-level difference may be a harmless default, an HPA-owned value, a provider-maintained timestamp, an emergency operator action, or a hostile security change. Treating every difference as “repair desired state” causes oscillation, overwrites legitimate actors, and can amplify incidents.

Status also affects control-plane scale. Updating a heartbeat every second produces storage writes, watch events, reconciles, audit volume, and compaction pressure even when semantics did not change. Embedding every child or historical attempt makes routine GET and watch expensive.

Compatibility matters because condition types, polarity, reasons, and aggregation become client contracts. Renaming `Healthy` to `Ready`, redefining `False`, or resetting observed generation during an upgrade can break automation even when the CRD schema still validates.

## Prerequisites and Retrieval

Retrieve Kubernetes spec/status and `/status` subresource, metadata generation and resource version, `metav1.Condition`, list-map semantics, optimistic concurrency, field ownership and Server-Side Apply, watches and caches, desired/effective/observed state, three-valued logic, observation timestamps and clocks, service-level objectives, health and readiness, state machines, idempotency, schema defaulting and conversion, canonicalization, set/list semantics, diff algorithms, security ownership, GitOps reconciliation, hysteresis and control-loop stability, metrics/logs/traces/events, privacy, API compatibility, backup/restore, and controller retirement.

You should distinguish status from state of the world; current condition from event history; generation from resource version; `Unknown` from `False`; readiness from progress; degradation from terminal failure; reason from message; last transition from last probe or update; observation time from write time; drift from representation difference; correction from ownership; adoption from authorization; controller health from resource outcome; local readiness from aggregate readiness; and status schema compatibility from semantic compatibility.

## Learning Objectives

After completing this module, you should be able to:

1. design bounded status as a generation- and freshness-qualified projection of evidence;
2. define condition types, polarity, ownership, reasons, messages, transition times, and absence semantics;
3. aggregate three-valued dependency conditions without hiding false or unknown inputs;
4. separate readiness, progress, degradation, drift, deletion, and workflow diagnostics;
5. normalize desired and observed representations before computing meaningful drift;
6. assign per-field/effect drift policies based on authority, cause, risk, and lifecycle;
7. prevent status conflicts, churn, feedback loops, flapping, and unbounded cardinality;
8. evolve, restore, and retire condition/status contracts safely; and
9. verify currentness, aggregation, drift classification, write behavior, and domain outcomes adversarially.

## Core Exposition

### Treat status as a projection, not truth

Spec records consumer-owned desired intent. Admission may default and bind policy, producing effective intent. Controller workflow state records durable progress and effect correlations. Observations describe the managed world with source and time. Status selects a bounded, API-worthy projection of these facts.

Each status field should answer a consumer question. Examples include current serving version, allocated endpoint reference, ready replica count, latest successfully applied revision, observed generation, conditions, and a compact active operation reference. If no consumer or controller needs a field, omit it.

Do not mirror spec mechanically into status. `status.requestedSize=spec.size` proves only that code copied a value. Report the effective target if default/policy transformation matters, and report observed size separately. Avoid one field that sometimes means requested and sometimes means actual.

Status can be wrong or stale. Document producer, observation source, correlation, and freshness where consequence demands it. A provider resource version or observation timestamp can be more useful than the controller write time. If direct observation is too expensive, state the cache consistency and scan interval behind the claim.

### Use the status subresource as an ownership boundary

For CRDs with the status subresource enabled, writes to the primary endpoint ignore status changes and writes to `/status` ignore non-status changes. This supports separate authorization: consumers modify spec while controllers modify status. It does not make individual status fields conflict-free.

Multiple controllers still update one object revision. A stale full-status update can erase a peer’s condition or observation. Allocate condition types and fields to producers; use narrow patches or a single aggregator; reread and recompute after conflict. Server-Side Apply field ownership can help where schema list-map semantics and manager boundaries are designed, but force ownership is not routine conflict handling.

Represent conditions as a list keyed by `type`, with at most one entry per type. Schema list-map annotations and compatible patch semantics prevent duplicate types and improve merge behavior. Do not depend on list order.

Status is controller-owned, but consumers may still need explicit operations such as acknowledge, pause, retry, or force. Put authorized intent in spec or a dedicated operation resource; never ask users to edit status as a command channel.

### Define every condition as an API contract

For each condition type, document:

- the property and scope it claims;
- producer and authoritative evidence;
- positive or negative polarity;
- meaning of `True`, `False`, `Unknown`, and absence;
- generation and freshness rules;
- stable reason vocabulary and whether it is guaranteed;
- when transition time changes;
- relationships to other conditions and terminality;
- security/redaction rules; and
- compatibility and retirement policy.

Kubernetes conditions use `type`, `status`, `observedGeneration`, `lastTransitionTime`, `reason`, and `message`. `status` is one of `True`, `False`, or `Unknown`. Absence of a known condition should normally be treated like unknown, especially before the responsible controller first observes the resource. Producers should initialize important conditions on their first visit, even when evidence is unknown.

Use names that express properties: `Ready`, `Progressing`, `Degraded`, `BackupVerified`, `DependenciesReady`, `Drifted`, `DeletionBlocked`. Avoid a chronological sequence such as `Provisioning`, `Configuring`, `Done` as mutually exclusive condition types; workflow checkpoints belong in a separate compact field or operation resource.

### Make polarity and composition explicit

Positive-polarity `Ready=True` means normal. Negative-polarity `Degraded=True` means abnormal. Neither convention is universally superior. Positive conditions make direct readiness easy; abnormal-true conditions make exceptional dimensions visible. Mixing them without documentation produces inverted alerts and aggregation bugs.

Do not infer `Ready=True` merely from `Degraded=False`. The system may be progressing, unobserved, or blocked for another reason. Likewise `Progressing=False` can mean complete, stalled, paused, or not started. Define relations as truth tables, not intuition.

For required positive conditions, use a conservative three-valued conjunction: any definitive current `False` makes the aggregate `False`; all current/fresh `True` makes it `True`; otherwise it is `Unknown`. For optional or quorum dependencies, define a separate rule rather than weakening the meaning of `Ready` silently.

Preserve component evidence. An aggregate reason can identify the highest-priority failing or unknown dependency and link to bounded details, but one green summary must not erase a red child. PLAT-058 develops scalable dependency aggregation.

### Correlate status with desired generation

`metadata.generation` tracks changes to desired-state semantics according to the resource strategy. `resourceVersion` tracks storage revisions and supports watch/concurrency. A condition’s `observedGeneration` says which desired generation the producer evaluated; it does not replace the concurrency token.

If spec is generation 12 and `Ready=True` was based on generation 11, a consumer must not treat it as proof that generation 12 is ready. Depending on domain, generation 11 may still be serving successfully; report this as current availability plus stale target reconciliation rather than overwriting evidence with a misleading failure.

Useful fields can separate `observedGeneration`, `appliedRevision`, `currentVersion`, `targetVersion`, and `availableRevision`. A controller may acknowledge generation 12 before its long-running effect finishes. Therefore “observed” means evaluated, not achieved, unless the field contract says otherwise.

On generation change, update status carefully. Initialize or mark target-dependent conditions `Unknown`/`Progressing` for the new generation while preserving independent observed facts. Do not stamp every old condition with the new generation merely because one controller loop read the object.

### Give observations freshness semantics

Generation currentness does not imply world currentness. A provider was queried at 10:00 for generation 12; at 11:00 the spec is still generation 12, but the database may have failed. Define a freshness bound by property and decision.

Let condition $c$ be current at time $t$ when

$$
\operatorname{current}(c,g,t)=(c.g=g)\land(t-c.t_o\le \tau_c)\land\operatorname{trusted}(c.source),
$$

where $t_o$ is authoritative observation time and $\tau_c$ is its freshness budget. A five-minute inventory observation may be adequate for a dashboard but not for a destructive failover guard. Carry observation time separately when `lastTransitionTime` cannot serve that purpose.

When evidence expires, change the dependent claim to `Unknown` or make consumers compute unknown from explicit age. Avoid periodic status heartbeats merely to look fresh: refreshing write time without refreshing evidence is dishonest, and high-rate heartbeats burden the API.

Clocks have error. For cross-system timestamps, document skew tolerance or use provider versions/leases. A future timestamp must not grant indefinite freshness.

### Use transition time correctly

`lastTransitionTime` records when condition `status` last changed among `True`, `False`, and `Unknown`. Kubernetes apimachinery helpers preserve it when reason, message, or observed generation changes without a status change. Follow the chosen API contract consistently.

Do not reset it on every reconcile, probe, or retry. That destroys duration queries such as “how long has Ready been false?” and creates status churn. If consumers need last successful probe, last attempt, last reconciliation, or last heartbeat, define a separate bounded timestamp with update policy.

The underlying property may transition between observations; the exact time can be unknown. Use the observation/write time as a documented approximation rather than claiming impossible precision. During restore, avoid rewriting historical transition times merely because records were reloaded.

### Design reasons for machines and messages for people

Reasons are stable, bounded, CamelCase categories such as `DependenciesNotReady`, `ProviderUnavailable`, `InvalidConfiguration`, `UpgradeInProgress`, or `ObservationExpired`. Clients can group or route them when the API promises stability.

Messages include contextual human detail: which dependency, retry time, or safe next action. They may change, be localized, truncated, or redacted. Clients must not parse them. Never interpolate credentials, raw provider responses, tokens, customer payloads, or uncontrolled high-cardinality data.

Avoid a reason per provider error string or object name. Map volatile errors to a stable taxonomy and expose protected detail through logs/traces or referenced operation records. Keep causal chains bounded; one useful message beats a status-sized stack trace.

### Separate outcome, progress, and controller health

`Ready` should describe whether the resource currently delivers its promised domain capability, not whether the last reconcile returned no error. A controller can be healthy while a provider outage makes the resource unready; a resource can continue serving while the controller is down or an upgrade progresses.

`Progressing` describes active movement toward a target. `Degraded` describes impaired operation. They can coexist with readiness: an old database version may remain ready while an upgrade progresses; one replica failure may be degraded while quorum service remains ready.

Terminal invalid intent differs from transient failure and unknown observation. Use stable reasons and recovery descriptions. A corrected generation can clear a terminal condition. Avoid a `Failed` phase that prevents future reconciliation forever.

Controller health belongs in controller metrics, deployment health, leader/queue telemetry, and perhaps a fleet-level control-plane condition. Do not make every resource `Ready=False` instantly because one controller Pod restarted; instead let observation freshness reveal when claims can no longer be trusted.

### Define drift after normalization

Raw serialized equality is rarely semantic equality. API defaulting can add fields; conversion can reorder or transform representations; maps and set-like lists can serialize differently; quantities can use equivalent units; providers generate IDs and timestamps; admission injects metadata; secrets may be write-only.

Define a comparison schema per owned path. Normalize defaults, versions, units, ordering, case only where semantically insensitive, and provider representations. Exclude server-generated and peer-owned fields. Treat unobservable/write-only fields through hashes, versions, rotations, or attestation rather than assuming equality.

Canonicalization must be versioned and tested. Over-normalization can hide real differences: sorting an ordered firewall rule list changes semantics; lowercasing a case-sensitive identifier corrupts identity. Under-normalization creates noisy correction loops.

Record desired/effective revision, observed identity/version/time, comparator version, and a bounded drift summary. Large diffs belong in protected artifacts or events, not unbounded status.

### Classify cause and ownership before responding

For each path/effect, identify authoritative owner and permitted co-managers. Differences can arise from controller lag, provider default, autonomous control such as HPA, human emergency change, another reconciler, API migration, restore, compromise, or changed external reality.

Map categories to policy:

- **correct** when this controller is authoritative and convergence is safe;
- **adopt** when external/current value is authorized to become intent through an audited write path;
- **ignore** for explicitly unowned or non-semantic fields;
- **report** when visibility is needed but mutation is not authorized;
- **pause** when conflict or consequence requires decision;
- **delete/quarantine** for prohibited resources under explicit policy; or
- **escalate** when cause or ownership is unknown.

Adoption is a desired-state mutation and requires authorization; status cannot silently become spec. Correction is an effect and requires idempotency, preconditions, rate limits, and unknown-outcome handling. Security drift may prioritize containment, but destructive action still needs verified identity and policy.

### Prevent ownership fights and oscillation

If GitOps owns `Deployment.spec.replicas` while HPA also writes it, each controller sees the other as drift and alternates values. Resolve authority: GitOps seeds and then ignores/releases that path, HPA owns it, and status reports current/desired capacity under the right contract. Current Flux APIs, for example, provide scoped ignore rules tied to drift detection and apply behavior; broad unscoped ignores can hide unrelated drift.

Server-Side Apply managed fields help discover and enforce field claims, but Update writers can still replace values and force can steal ownership. Maintain an organizational field/effect ownership matrix beyond the mechanism.

Noisy measurements cause flapping even with one owner. Use hysteresis, minimum stable duration, confidence/quorum, consecutive observations, and cooldown where domain-safe. Do not delay urgent security containment behind generic smoothing.

Detect feedback from status itself. A controller that updates `lastChecked` every run triggers its own watch, writes again, and hot-loops. Predicate events by meaningful generation/dependency changes, and write status only when semantic content or an explicit low-rate freshness checkpoint changes.

### Aggregate without hiding uncertainty

Parent resources often summarize hundreds of children. Specify required membership from a consistent inventory revision. If the set changes during aggregation, record the snapshot or generation used. Missing, stale, or unauthorized child observations normally yield unknown rather than optimistic success.

Do not copy every child condition into the parent. Store counts by stable category, a bounded sample of blocking references, aggregate observed revision, and a link/query path to detail. High-cardinality metrics and logs can carry diagnosis without bloating each resource.

For quorum systems, readiness may require $r$ of $n$ eligible members plus diversity and freshness, not simple AND. State the formula and failure-domain constraints. For safety prerequisites such as verified backup before deletion, one unknown requirement should block the action even if availability remains true.

Aggregation is a policy decision. Preserve distinction between current service, desired rollout completion, and dependency health so clients choose the right gate.

### Make drift scanning scalable and honest

Event-driven reconciliation reduces latency but misses external changes and events that cannot be mapped. Periodic scans repair coverage. Define inventory completeness, pagination/snapshot semantics, rate limits, priority, and maximum detection age.

If $N$ objects are scanned by $w$ workers at mean rate $\mu$ objects per worker-second, the ideal full-scan time is

$$
T_s=\frac{N}{w\mu}.
$$

Actual maximum detection time includes scheduling interval, pagination, backoff, provider limits, failures, and long-tail objects. “Last scan found no drift” is meaningful only with inventory revision, coverage, comparator version, and finish time.

Use risk-tiered frequency. Public exposure and credential drift may need watches or frequent checks; immutable archive labels may tolerate daily scans. Add jitter to avoid synchronized provider load. A paused controller should say whether detection, correction, or both are paused.

### Bound status size, rate, and history

Status is served on every GET/watch and persisted in the API store. Keep it compact. Do not embed unbounded child arrays, full diffs, raw logs, retry histories, or event streams. Use separate operation/audit resources with retention and access control.

Perform semantic equality before writing. Stable sort list-map conditions if presentation requires it, but do not treat order as meaning. Coalesce message updates, cap samples, and update high-frequency measurements through metrics rather than status unless API consumers truly require them.

Kubernetes Events are short-lived occurrence signals, logs explain execution, metrics aggregate numeric behavior, traces correlate calls, and status describes the latest API contract. Each can be lost or retained differently. Do not rely on status as a complete audit history.

Watch status-write conflicts and object size. A controller that cannot report status should expose metrics and retry with bounded backoff, but must not perform unsafe effects whose guard depends on unrecorded status/checkpoints.

### Secure and audit the status surface

Status is often broadly readable. Exclude credentials, signed URLs, provider request bodies, internal network topology, personal data, and raw multi-tenant error text. Reference a Secret or protected operation record by name/UID when authorized clients need detail.

Treat observed external values as untrusted input. Sanitize control characters, bound length, and avoid rendering injection. A malicious provider tag must not become a reason, metric label, shell command, or HTML message without encoding.

Authorize `/status` writes narrowly by resource and controller identity. Admission and audit can enforce condition ownership when shared controllers are risky. Detect a compromised writer that stamps current generation without performing observation; generation correlation is evidence structure, not cryptographic truth.

Audit changes to readiness semantics, drift policy, force correction, adoption into spec, ignored security paths, manual condition repair, and comparator version. Routine message churn should not overwhelm material audit events.

### Evolve and retire status contracts

Condition types and reasons are API surface. Add new types compatibly; clients must tolerate unknown additions and ordering. Do not invert polarity or redefine an existing reason. Introduce a new condition/type or API version, dual-publish during migration, and document precedence.

Conversion must preserve meaning across served/storage versions. If a new version separates `Ready` and `Available`, old clients need a conservative projection. Restore must retain observed generation, external revision, and transition semantics while marking observations unknown if freshness cannot survive.

Rolling controller versions may alternate status writes. Ensure they share condition schemas and comparator semantics or route ownership by version. Unknown newer fields should be preserved by merge behavior; old controllers must not erase them with broad updates.

Before retiring a condition producer, inventory consumers, alerts, policies, dashboards, automation, stored objects, and backups. Transfer ownership or mark the condition obsolete through a documented compatibility path. Stop declaring a condition only after absence semantics and clients are safe; otherwise a healthy-looking absence can mask a dead controller.

### Verify claims, not just serialization

Test condition truth tables for every `True`/`False`/`Unknown` and absence combination. Advance generation without reconciliation, expire observation time, skew clocks, change only reason/message, and assert transition time behavior. Race two status writers and inject conflicts.

Generate semantically equivalent objects with reordered maps/set-lists, alternate units, defaulted fields, converted versions, and provider-generated metadata; assert no drift. Generate ordered-list, security, identity, and ownership differences; assert correct classification and response. Inject HPA/GitOps ownership conflict and verify no oscillation.

Pause detection and correction separately. Drop watch events and prove periodic scan repairs coverage. Partition provider observation, restore stale status, rotate comparator/controller versions, and retire a producer. Verify actual domain state and consumer decisions, not merely that a JSON condition exists.

## Definitions and Notation

Let $d_g$ be desired state at generation $g$, $e_g=A(d_g,p)$ admitted/effective intent under policy revision $p$, $w_t$ the world at time $t$, and $o_t=O(w_t)$ a sourced observation. Status is projection $S=P(e_g,o_t,k)$ from intent, observation, and durable controller state $k$.

A condition is tuple

$$
c=(\text{type},v,g_o,t_o,t_x,r,m,s),
$$

where $v\in\{T,F,U\}$ is three-valued status, $g_o$ observed generation, $t_o$ observation time when modeled, $t_x$ last status-transition time, $r$ reason, $m$ message, and $s$ source/producer. Kubernetes `metav1.Condition` directly carries all except a distinct $t_o$ and producer; APIs add fields or establish ownership conventions when needed.

For trusted producer set $Q$ and freshness bound $\tau_c$, define

$$
\operatorname{Current}(c,g,t)\equiv(g_o=g)\land(t-t_o\le\tau_c)\land(s\in Q).
$$

For required positive conditions $C$, conservative aggregate $R(C)$ is $F$ if any current condition is $F$; it is $T$ if every condition is present, current, and $T$; otherwise it is $U$. Priority between stale false and current false must be documented; this chapter treats stale evidence as unknown unless another current fact establishes failure.

Let $A_c$ be paths controller $c$ compares/owns, $N_e,N_o$ versioned normalizers, and $\equiv_p$ semantic equality for path $p$. Then

$$
\Delta_c=\{p\in A_c\mid N_e(e_g[p])\not\equiv_p N_o(o_t[p])\}.
$$

Drift policy $\pi(p,owner,cause,risk,lifecycle)$ returns a response such as correct, adopt, ignore, report, pause, delete, or escalate. The policy, not membership in $\Delta_c$, authorizes action.

For inventory size $N$, workers $w$, and mean scan rate $\mu$, ideal scan time $T_s=N/(w\mu)$. This is a capacity estimate under stationary simplified assumptions, not proof of maximum detection latency.

## Mechanisms, Invariants, or Proof Structure

### Status and drift protocol

1. Read current spec generation, effective-policy revision, status resource version, controller checkpoints, and owned condition entries.
2. Observe domain state with source identity, external version, observation time, and known consistency/freshness limits.
3. Normalize desired and observed values by versioned, field-aware comparators.
4. Classify differences by semantic path, field/effect owner, cause confidence, risk, and lifecycle state.
5. Select drift response from explicit policy; never infer correction authority from inequality alone.
6. Compute domain facts, target progress, degradation, deletion, and controller diagnostics separately.
7. Set each owned condition’s `True`/`False`/`Unknown`, observed generation, stable reason, sanitized bounded message, and transition time only on status change.
8. Aggregate dependencies using declared three-valued/quorum rules and a consistent membership revision.
9. Write only semantic status changes through narrow conflict-safe ownership; reread and recompute after conflict.
10. Schedule event-driven and periodic observation according to freshness and drift-risk budgets.
11. Verify consumers, upgrades, restore, and retirement against actual domain outcomes and stale/hostile evidence.

### Invariant and aggregation argument

Assume required conditions have unique trusted producers, currentness checks are applied, absence is unknown, and the aggregate follows the defined rule. If aggregate is `True`, every required condition exists, matches generation $g$, remains within freshness, comes from a trusted producer, and is `True`. Therefore aggregate true cannot be produced by a missing, stale, wrong-generation, untrusted, false, or unknown requirement within the model.

The converse is not a real-world health proof. Producers can be wrong, observations can become false immediately, freshness bounds can be too weak, and requirements can be omitted. The argument establishes conservative propagation of modeled evidence.

For drift, normalization and ownership prevent selected representation and authority false positives only if schemas are complete and correct. A path in $\Delta_c$ establishes a classified mismatch, not cause, authorization, or safety of correction. Those enter through $\pi$ and effect protocols.

### Executable contract inventory

This synthetic inventory checks ten condition/drift designs against ten controls. It does not query a cluster or establish correctness of a real controller.

<!-- bijux-verify: {"id":"status-drift-contract-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"credible=2\nincomplete=6\nunsafe=2\n"}} -->
```python
required = {
    "generation_current", "observation_fresh", "unique_condition_owner",
    "transition_time_correct", "stable_reason", "normalized_diff",
    "field_ownership", "drift_policy", "bounded_redacted", "recovery_tested",
}

designs = {
    "database": required,
    "network": required,
    "stale-green": required - {"generation_current", "observation_fresh"},
    "message-api": required - {"stable_reason"},
    "heartbeat-churn": required - {"transition_time_correct"},
    "byte-diff": required - {"normalized_diff"},
    "shared-ready": required - {"unique_condition_owner", "field_ownership"},
    "blind-correct": required - {"drift_policy"},
    "secret-status": required - {"bounded_redacted"},
    "untested-restore": required - {"recovery_tested"},
}

counts = {"credible": 0, "incomplete": 0, "unsafe": 0}
for controls in designs.values():
    missing = required - controls
    category = "credible" if not missing else ("incomplete" if len(missing) == 1 else "unsafe")
    counts[category] += 1
for category in ("credible", "incomplete", "unsafe"):
    print(f"{category}={counts[category]}")
```

The categories are review prompts rather than risk scores. One omitted control can be catastrophic, and complete rows still need real evidence about observation, ownership, provider behavior, consumers, and recovery.

## Alternatives and Trade-Offs

### Positive versus abnormal-true conditions

Positive `Ready=True` is direct for gates and aggregation. Abnormal-true `Degraded=True` highlights exceptions and can be sparse, but absence can look healthy when the producer is dead. Use explicit `Unknown` and documented polarity; combine complementary properties only when their relationship is defined.

### Top-level observed generation versus per-condition generation

One top-level value is compact and works when one controller updates all status atomically. Per-condition generation preserves independent producer/evidence correlation. Mixed ownership usually favors per-condition values plus any meaningful aggregate revision.

### Transition time versus probe/update time

Transition time supports duration in one state without churn. Probe time supports freshness but changes often. Keep them separate where both matter; do not overload transition time or refresh timestamps without new evidence.

### Single aggregator versus multiple writers

A single aggregator gives consistent conditions and fewer write conflicts but becomes a coupling and availability point. Multiple writers preserve domain ownership but require disjoint fields/types, merge semantics, and conservative aggregation. Choose by organizational and consistency boundary.

### Phase enum versus orthogonal conditions

A phase is compact and convenient for a dominant workflow, but collapses simultaneous availability, progress, degradation, backup, and deletion. Conditions express independent properties. Use a small diagnostic workflow checkpoint alongside—not instead of—domain conditions.

### Correct versus adopt drift

Correction preserves declared authority but can erase emergency or peer-owned changes. Adoption preserves reality but mutates intent and can legitimize compromise. Both require policy and authorization; unknown ownership should pause/escalate.

### Exact byte diff versus semantic diff

Byte diff is simple and auditable but noisy under defaults, order, versions, and generated fields. Semantic diff reduces noise and fights but adds comparator complexity and risk of hiding differences. Version and test normalization per field.

### Event-driven versus periodic drift detection

Events provide low latency and low steady scanning but can be missed and may not cover external systems. Periodic inventory repairs coverage at provider and API cost. Combine them with risk-tiered intervals and explicit detection-age claims.

### Inline detail versus referenced operation record

Inline status is easy to fetch and gate but increases object size, exposure, and churn. Separate records support histories and restricted detail but add lifecycle and query complexity. Keep stable summaries inline and bounded detail behind references.

### Hysteresis versus immediate correction

Hysteresis reduces noise and oscillation but delays response. Use it for noisy performance thresholds; bypass or shorten it for high-confidence security and safety violations under explicit policy.

### Stable reason taxonomy versus provider-specific reasons

Stable reasons support automation and aggregation. Provider-specific codes improve diagnosis but explode cardinality and compatibility. Map them to stable categories and carry protected provider detail elsewhere.

### Preserve stale status versus clear on restart

Preserving status retains useful last-known evidence but can mislead unless freshness is enforced. Clearing loses diagnosis and can cause automation churn. Preserve correlation and transition history while making expired observations explicitly unknown.

## Failure Modes and Misconceptions

1. **“Status is actual state.”** It is a producer’s projection from observations and can be stale, partial, or wrong.
2. **“Ready true means current.”** It needs matching observed generation and adequate observation freshness.
3. **“Missing means false.”** For known conditions, absence normally means unknown/unobserved, not healthy or definitively failed.
4. **“Unknown is a weak false.”** Unknown denotes inadequate evidence; response can differ fundamentally from known failure.
5. **“Condition order shows priority.”** Conditions are keyed by type; order is not semantics.
6. **“Update transition time every reconcile.”** That destroys transition duration and causes write/watch churn.
7. **“Reason is a message summary.”** Reason is a stable machine category; messages contain changing human detail.
8. **“Clients may parse message text.”** Messages are not compatibility interfaces and may be redacted or revised.
9. **“Observed generation means achieved generation.”** It proves evaluation correlation only unless the field contract adds achievement semantics.
10. **“Ready false means controller broken.”** The managed outcome, dependency, policy, or provider may be unhealthy while the controller works correctly.
11. **“No drift found means no drift exists.”** Coverage, age, inventory, comparator, and observation reliability bound the claim.
12. **“JSON inequality is drift.”** Defaults, ordering, generated fields, units, and versions require semantic normalization.
13. **“Drift authorizes correction.”** Ownership and response policy decide action.
14. **“Adoption is harmless.”** It mutates desired authority and can canonize malicious or accidental state.
15. **“Server-Side Apply eliminates controller fights.”** It detects some field conflicts; forced ownership and non-apply writers still need governance.
16. **“One phase tells the whole story.”** Availability, rollout, degradation, backup, drift, and deletion are orthogonal.
17. **“Status should contain the full history.”** Histories grow without bound and belong in events, logs, audit, or operation resources.
18. **“A heartbeat makes observation fresh.”** Only renewed authoritative evidence does.
19. **“Old controllers can ignore new conditions safely.”** Broad status updates can erase them and semantic skew can invert decisions.
20. **“Stopping the producer makes its condition false.”** Stored conditions remain; freshness and retirement contracts must make loss of evidence visible.

## Worked Examples

### Example 1

**Situation.** A resource is generation 9. `Ready=True` has `observedGeneration: 8`, while `Progressing=True` has generation 9.

**Reasoning.** The old readiness claim does not establish generation 9’s target. If generation 8 still serves, an API may report `Available=True` for the current serving revision while `Ready` for the latest desired outcome is `Unknown` or `False` according to contract. `Progressing=True` correctly describes work on generation 9. Consumers gating rollout must require generation-current readiness.

**Conclusion.** Preserve useful old availability evidence, but never present stale-generation readiness as proof of the new target.

### Example 2

**Situation.** `Ready=False` remains false for 20 minutes. Its reason changes from `ProviderBusy` to `RetryBackoff`, and its message changes every retry.

**Reasoning.** The condition status never changed, so `lastTransitionTime` remains the time readiness became false. Reason/message may update with semantic deduplication. If clients need last attempt, add a separately governed field or use events/metrics. Resetting transition time would falsely report a new outage every retry.

**Conclusion.** Transition time follows three-valued status, not diagnostic text changes.

### Example 3

**Situation.** A parent requires three dependencies: A is current `True`, B is current `False`, and C is stale `True`.

**Reasoning.** Under conservative conjunction, current false B makes aggregate `False`; stale C is treated unknown but cannot override a known failure. If B later becomes true while C remains stale, aggregate becomes `Unknown`, not true. Only three present/current/trusted true conditions yield true.

**Conclusion.** Three-valued aggregation preserves both definitive failure and uncertainty.

### Example 4

**Situation.** Desired storage is `1024Mi`; provider observation is `1Gi`. Map keys serialize in different order, and the provider adds `createdAt`.

**Reasoning.** A versioned comparator converts quantities to bytes, compares maps independent of key order, and excludes provider-owned `createdAt`. Both quantities equal $1{,}073{,}741{,}824$ bytes, so there is no semantic drift. If an ordered firewall rule list changed order, the comparator would preserve order because it affects behavior.

**Conclusion.** Normalize according to field semantics, not a global sorting or string-equality rule.

### Example 5

**Situation.** Git declares Deployment replicas 3 while HPA changes them to 7; GitOps repeatedly restores 3.

**Reasoning.** Two authorities create oscillation. Define GitOps as owner of template and initial replica seed, release/ignore the replica path after HPA ownership, and let HPA manage replicas within policy. Status can report current 7, HPA target, and policy bounds. A scoped ignore is safer than ignoring replicas on every object.

**Conclusion.** Correct drift by authority boundary; do not make two valid controllers fight over one field.

### Example 6

**Situation.** Two controllers update separate conditions using full stale status objects.

**Reasoning.** Controller A reads version 20 and writes `BackupVerified=True`. Controller B also read 20 and writes `NetworkReady=True`; its update conflicts after A. Retrying the identical version-20 object would erase A if accepted later. B rereads version 21, merges only its owned condition by type, preserves A, recomputes aggregate, and conditionally writes.

**Conclusion.** Status subresource separation does not replace per-field ownership and conflict recomputation.

### Example 7

**Situation.** One million objects need periodic external drift scans. Fifty workers each sustain 20 objects/second. Estimate ideal scan time.

**Reasoning.** Aggregate rate is $50\times20=1{,}000$ objects/second. Thus

$$
T_s=\frac{1{,}000{,}000}{1{,}000}=1{,}000\text{ seconds}\approx16.67\text{ minutes}.
$$

If scans start every 30 minutes, an object near the end can already have substantial detection age; provider limits, retries, and arrivals extend it. High-risk objects need prioritized or event-driven observation.

**Conclusion.** Detection freshness must include scan capacity and scheduling, not just the configured interval.

### Example 8

**Situation.** A provider returns an error containing an access token and customer SQL. The controller wants to put it in condition message.

**Reasoning.** Status is broadly readable and durable. Map the error to stable reason `ProviderRejected`, produce a sanitized bounded message such as “provider rejected configuration; see operation op-31,” and store restricted detail only in an appropriately protected record/log with retention. Prevent raw error strings from becoming metric labels.

**Conclusion.** Conditions explain safe action without becoming a secret or high-cardinality telemetry channel.

### Example 9

**Situation.** Latency alternates around a 200 ms threshold, causing `Degraded` and an expensive failover every minute.

**Reasoning.** Define degradation after three consecutive measurements over 220 ms and recovery after five under 180 ms, with minimum dwell and failover cooldown. Preserve immediate override for confirmed data corruption or endpoint compromise. Test measurement gaps as unknown rather than low latency.

**Conclusion.** Domain-specific hysteresis prevents noisy status from driving oscillating effects without delaying unrelated safety signals.

### Example 10

**Situation.** A new controller splits `Ready` into `Available` and `LatestGenerationReady`, while old clients understand only `Ready`.

**Reasoning.** Add the new conditions without redefining old polarity. During compatibility, compute old `Ready` conservatively from new evidence and dual-publish with matching generation. Ensure old controllers preserve unknown new types or fence writers by version. Migrate clients and alerts, test conversions/restores, then deprecate old `Ready` under a documented absence/retirement contract.

**Conclusion.** Evolve condition meaning additively and conservatively; schema acceptance alone does not preserve client decisions.

## Cross-Program Connections

1. **API & Service Engineering:** resource representations, status subresources, compatibility, machine error reasons, caching, and conditional writes define the public observation contract.
2. **Distributed Systems:** partial observation, staleness, three-valued knowledge, eventual consistency, and failure detectors explain why unknown is fundamental.
3. **Control Theory:** measurement, delay, noise, hysteresis, oscillation, stability, and setpoint tracking shape drift correction.
4. **Database Systems:** materialized projections, MVCC/resource versions, normalization, conflict resolution, and change data capture underpin status maintenance.
5. **Formal Methods:** predicates, three-valued aggregation, invariants, abstraction functions, and counterexamples make condition guarantees precise.
6. **Security Engineering:** authority, untrusted observations, status redaction, injection, adoption risk, and audit protect the control surface.
7. **Reliability Engineering:** SLOs, freshness budgets, failure classification, alerts, retry/backoff, and recovery testing make status operationally useful.
8. **Data Engineering:** schema evolution, late data, watermarks, materialized views, deduplication, and backfill resemble observed-generation projections.
9. **Human-Computer Interaction:** stable terminology, actionable messages, progressive disclosure, and honest uncertainty prevent dashboards from misleading operators.
10. **Systems Engineering:** measurement boundaries, evidence, configuration authority, hazards, lifecycle compatibility, and retirement keep local status claims scoped.

## References

1. Kubernetes SIG Architecture. [API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md). Retrieved 2026-09-02. Defines spec/status and condition guidance.
2. Kubernetes. [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/). Retrieved 2026-09-02. Documents status subresource and custom-resource behavior.
3. Kubernetes. [CustomResourceDefinition API](https://kubernetes.io/docs/reference/kubernetes-api/apiextensions/custom-resource-definition-v1/). Retrieved 2026-09-02. Defines status subresource and condition fields including observed generation.
4. Kubernetes apimachinery. [Condition helper implementation](https://github.com/kubernetes/apimachinery/blob/master/pkg/api/meta/conditions.go). Retrieved 2026-09-02. Documents transition-time and condition update behavior.
5. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02. Covers generation, resource versions, watches, and concurrency.
6. Kubernetes. [Server-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/). Retrieved 2026-09-02. Documents field managers, ownership, conflicts, and relinquishing fields.
7. Kubernetes SIGs. [cli-utils kstatus](https://github.com/kubernetes-sigs/cli-utils/blob/master/pkg/kstatus/README.md). Retrieved 2026-09-02. Develops current status aggregation and unknown/stalled/reconciling concepts.
8. Flux. [Kustomization](https://fluxcd.io/flux/components/kustomize/kustomizations/). Retrieved 2026-09-02. Documents periodic drift detection/correction, suspension, conditions, and scoped ignore behavior.
9. Flux. [Kustomize API v1](https://fluxcd.io/flux/components/kustomize/api/v1/). Retrieved 2026-09-02. Defines current drift ignore rule schema and targeting.
10. OpenGitOps. [Principles](https://opengitops.dev/). Retrieved 2026-09-02. Defines declarative, versioned/immutable, pulled, and continuously reconciled desired state.
11. Leslie Lamport. “Time, Clocks, and the Ordering of Events in a Distributed System.” *Communications of the ACM* 21(7), 1978.
12. NIST. [Guide for Security-Focused Configuration Management of Information Systems, SP 800-128](https://csrc.nist.gov/pubs/sp/800/128/upd1/final). 2019 update. Grounds authorized baselines and configuration monitoring.
13. Karl J. Åström and Richard M. Murray. *Feedback Systems: An Introduction for Scientists and Engineers*. Princeton University Press, 2008.
14. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly Media, 2017. See replication, time, streams, derived data, and distributed-system uncertainty.

## Exercises

### Exercise 1

Define a `Ready` condition contract for a managed database: property, producer, polarity, `True`/`False`/`Unknown`/absence, observed generation, freshness, reason vocabulary, transition time, message, and relationship to `Progressing` and `Degraded`.

### Exercise 2

For four required dependencies with states current true, stale true, current unknown, and current false, derive aggregate readiness. Then change the false to current true and derive again. State every assumption.

### Exercise 3

A controller byte-diffs desired YAML against a provider object and continually corrects quantity spelling, map order, generated timestamps, HPA replicas, and a manually opened public port. Diagnose each difference and design comparators, ownership, and response policies.

### Exercise 4

Design status storage and update behavior for a parent with 50,000 children, three condition producers, high-frequency health samples, detailed provider errors, and clients that need rollout and current-service gates.

### Exercise 5

Plan a rolling status-contract migration that changes comparator version, adds freshness, splits one readiness condition into two, restores objects from old backups, and eventually retires the old condition producer.

## Answers to the Exercises

### Answer 1

`Ready` claims that the database currently provides the promised serving capability for the target semantics named by its observed generation. The database operator owns it; positive polarity means `True` is normal. `True` requires reachable serving endpoint, required replicas/quorum, accepted health, and no safety condition that invalidates service. `False` requires current definitive evidence of unmet serving requirements. `Unknown` means evidence is absent, stale, conflicting, unauthorized, or outcome-ambiguous. Before first observation, absence is interpreted as unknown; the controller initializes it on first visit.

`observedGeneration` is the spec generation evaluated, not a storage resource version or automatic proof the target was achieved. Provider health evidence might expire after, for example, five minutes for dashboard/gating, with shorter fresh observation required before destructive failover. `lastTransitionTime` changes only when status moves among true/false/unknown. Stable reasons might include `Serving`, `EndpointUnavailable`, `QuorumLost`, `DependenciesNotReady`, `ObservationExpired`, and `ConfigurationInvalid`; messages contain sanitized bounded detail and a safe next action. `Progressing=True` may coexist with `Ready=True` while an old version serves during upgrade. `Degraded=True` may coexist with readiness under reduced redundancy; neither is inferred solely from the other.

### Answer 2

Assume all four are required positive-polarity conditions, producer identities are trusted, membership is complete for one parent revision, currentness includes matching generation and adequate freshness, and any current false has priority. With current true, stale true, current unknown, and current false, aggregate is `False` because at least one current requirement is definitively false. The stale true contributes unknown, not success, and current unknown also prevents success.

After the false becomes current true, no requirement is definitively false, but stale true and current unknown remain, so aggregate is `Unknown`. It becomes `True` only when all four are present, current, trusted, and true. If the API instead uses quorum/optional dependencies, it must define a different formula and cannot call this conservative conjunction unchanged.

### Answer 3

Quantity spelling is representational: normalize both to the same base unit. Map order is non-semantic: compare keyed entries independent of serialization. Generated timestamps are provider-owned: exclude them while retaining them as observations if useful. HPA replicas are a legitimate peer-controller value: release/ignore that specific field in the GitOps/controller comparison and document HPA authority. The public port is security-sensitive. If platform policy owns exposure and the identity/observation is verified, classify it as prohibited drift and correct or quarantine immediately with conditional/idempotent effects and audit; do not adopt it simply because it exists.

Version comparators and test negative cases: ordered rule lists must retain order, case-sensitive identifiers must not be folded, and write-only secrets need version/hash/rotation evidence. Record a bounded drift summary with desired revision, observed provider version/time, comparator revision, owner, classification, and selected policy. Inequality alone authorizes no mutation.

### Answer 4

Keep parent status bounded: target and current serving revisions; total/ready/failed/unknown child counts tied to an inventory revision; aggregate `Available`, `LatestGenerationReady`, `Progressing`, `Degraded`, and `DependenciesReady`; a bounded sample of blocking child references; observation finish time; and a reference to a protected rollout/diagnostic resource. Do not embed 50,000 child entries.

Assign each producer disjoint condition types or fields. Use list-map-by-type schema, narrow patches, and resource-version conflict reread/recompute; appoint one aggregator for parent readiness so three writers do not race on `Ready`. Preserve child facts in child status/indexed inventory. High-frequency samples go to metrics; only threshold transitions or low-rate fresh observations update status. Detailed provider errors map to stable redacted reasons/messages with protected logs or operation records.

Clients gating current service use `Available` with source/freshness. Rollout clients require `LatestGenerationReady=True` with matching observed generation and inventory revision. `Progressing` does not imply unavailable. Cap message/sample cardinality, avoid timestamp-only hot loops, test dropped watches with periodic aggregation, and authorize `/status` writers narrowly.

### Answer 5

Version the comparator and status semantics first. New controllers read old status but treat missing freshness as unknown after a conservative bound. Add observation time/source and new `Available` plus `LatestGenerationReady` conditions without changing old `Ready`. During dual publication, derive old `Ready` conservatively from new current evidence, preserve transition time when status does not change, and stamp each condition with the generation actually evaluated.

Ensure rolling old/new writers preserve unknown condition types and fields through narrow merges, or fence ownership by controller version. Store comparator revision in drift summaries; shadow-run old/new comparison and investigate disagreements before enabling new correction. Test defaults, conversions, field ownership, security drift, and oscillation.

On restore, preserve historical correlations but expire observations whose source time/freshness cannot survive; never refresh them merely at restore time. Replay provider inventory to rebuild current claims. Inventory every old client, alert, policy, dashboard, stored version, and backup. Migrate consumers to the two new gates, publish deprecation and precedence, then stop old `Ready` only when absence cannot be misread as healthy. Drain/transfer the old producer, update backups and disaster-recovery tests, revoke its status permission after zero ownership remains, and retain audit of the semantic migration.
