---
module_id: DE-043
program: Data Engineering
level: 1
module_number: 43
title: Scheduling and Event-Triggered Execution
status: complete
last_verified: 2026-09-03
---

# Scheduling and Event-Triggered Execution

## One-Page Review

### Governing question

How should a data workflow convert calendar intent, elapsed intervals, and external occurrences into deterministic run requests without confusing time with data completeness or event delivery with exactly-once execution?

### Essential definitions

- A **schedule definition** is a versioned rule that maps a time horizon and calendar/time-zone policy to intended execution slots or data intervals.
- A **schedule slot** is one logical occurrence of a schedule, identified independently of when the scheduler observes, admits, or starts it.
- A **data interval** is the semantic interval of data a run is expected to process. It is not necessarily the run’s wall-clock duration.
- A **logical time** or **nominal time** identifies the intended occurrence of a run under its timetable; its exact relation to interval start/end must be declared.
- A **trigger** is a rule that proposes an action or run request when a condition over time, events, or authoritative state becomes satisfied.
- An **event** is a record describing an occurrence and its context. The event is a notification/evidence item, not necessarily the authoritative state it describes.
- An **event identity** combines a stable source identity and event ID so duplicate delivery can be recognized without collapsing distinct occurrences.
- A **run request** is a durable, authorized intent to instantiate a job for an exact scope, definition version, parameter set, and input binding.
- A **run key** is a deterministic identity used to deduplicate equivalent run requests.
- **Catch-up** is policy for schedule slots that became due while scheduling was disabled, unavailable, delayed, or newly activated.
- **Overlap policy** determines whether simultaneous or still-running slots are admitted, queued, coalesced, skipped, or superseded.
- **Debouncing** delays action until a quiet period; **coalescing** combines several events into one declared scope. Both trade latency for fewer runs.
- **Reconciliation** compares expected work derived from authoritative state with recorded requests/runs/materializations and repairs missing or inconsistent intent.

### Central model, mechanism, or theorem

Let schedule version $s$ generate intended slots

$$
Slots(s,H)=((p_1,[a_1,b_1)),...,(p_n,[a_n,b_n)))
$$

for horizon $H$, where $p_i$ is a stable partition or slot key. A scheduler observation at time $q$ may propose a run only after eligibility policy is met, but observation time does not change the slot identity.

For an event-triggered partition $p$, reduce received events by identity $(source,id)$, select an authoritative compatible generation $g_{u,p}$ for every required upstream $u$, and evaluate

$$
ready(p)=all(u in U: acceptable(g_{u,p},p)).
$$

Then derive a deterministic request identity

$$
runkey=K(jobversion,p,params,(g_{u,p})_{u in U}).
$$

Duplicate or reordered notifications reproduce the same request. A later correction that changes an input generation changes the run key and creates a new, auditable intent rather than silently mutating the old run. This still requires an atomic uniqueness constraint or equivalent durable arbitration when concurrent trigger evaluators race.

### Critical invariants

- Schedule definition, calendar, time zone, time-zone database assumptions, start/end bounds, recurrence, exclusions, and catch-up policy are versioned.
- Slot, logical time, data interval, trigger observation, admission, actual start, and completion times remain distinct.
- Each intended slot has a stable identity even when execution is late, duplicated, skipped, paused, or manually requested.
- A clock tick or event creates a run request; it does not by itself prove source completeness, quality, or downstream readiness.
- Event identity, type/schema, subject, source revision/position, occurrence time, received time, and payload/reference are preserved.
- Duplicate, delayed, reordered, missing, replayed, and conflicting events have explicit handling.
- Fan-in triggers correlate exact compatible upstream generations and partitions rather than merely counting messages.
- Run keys and trigger-state updates are durably arbitrated so concurrent evaluators cannot create uncontrolled duplicate logical work.
- Overlap, coalescing, quiet period, maximum delay, backlog, pause/resume, and overload policies are explicit and observable.
- Scheduled, event-driven, manual, reconciliation, and historical requests retain distinct provenance while sharing the same data contract.
- Reconciliation can discover missed schedule slots or lost events from authoritative manifests/state.
- Trigger inputs, filters, run parameters, and metadata are authenticated, authorized, tenant-scoped, minimized, and auditable.

### Common failures

Common failures include interpreting cron as a data-completeness guarantee; using actual start time as the partition; treating every day as exactly 24 hours; omitting a time zone or business calendar; silently changing calendar rules for historical slots; equating logical date with data-interval start in every trigger path; disabling a schedule without deciding what resume does; creating one run for every poll of a permanently true condition; trusting file-exists or job-success without generation identity; accepting duplicate messages as new work; deduplicating by payload and collapsing legitimate repeats; ordering by arrival time; triggering fan-in after “two events” without checking sources or partitions; coalescing without a maximum delay; losing work when a broker drops an event; mixing manual and scheduled runs under one ambiguous key; allowing overlapping writers without publication arbitration; and exposing secrets or cross-tenant identifiers through event payloads and run parameters.

### Compact example

A daily-sales workflow expects partitions September 1–3 and requires orders plus rates. It receives seven messages: six unique events and one repeated rates event. A later orders revision replaces the earlier September 1 generation. September 1 resolves to orders o103 and rates r7; September 2 resolves to o102 and r8; September 3 has r9 but remains blocked because orders are missing. Deterministic run keys bind exact generations. Reversing message delivery produces the same two requests, while the correction changes September 1’s key from the earlier o101 binding. The schedule inventory keeps September 3 visible even though no ready run exists.

### Connections

[DE-041](041-directed-acyclic-graphs-and-dependencies.md) defines readiness edges and partition mappings; [DE-042](042-tasks-jobs-assets-and-datasets.md) defines jobs, runs, assets, and generations. This module creates run intent. DE-044 governs attempts, timeouts, retries, and idempotent side effects after admission; DE-045 deepens partitioned-asset semantics; DE-046 plans historical execution; DE-049 records full operational state.

## Governing Question

What fact should cause which exact logical run to exist, and how can the system prove that the request was neither missed nor multiplied?

“Run every day” leaves essential questions unanswered. At what civil time and in which time zone? Does a day mean a local calendar day, a UTC interval, or the preceding 24 elapsed hours? Does the run become eligible at interval start or end? What happens on daylight-saving transitions, holidays, scheduler downtime, pause/resume, or a still-running prior occurrence? Which data interval and partition should a late run process?

“Run when the file arrives” is equally incomplete. Which file version, manifest, source epoch, partition, and completeness rule? Is the message a distinct occurrence or a redelivery? What if the message arrives before the object is readable, arrives twice, arrives after a correction, or never arrives? Does one file suffice or must several sources be correlated?

The scheduler is a producer of durable intent, not a clock-driven function call. It translates an input fact into a run request whose identity, scope, definition version, parameters, input bindings, provenance, and authorization can be audited. Run creation and eventual execution are later state transitions.

The system also needs negative evidence. It must identify expected slots with no request, accepted events with no resulting decision, ready partitions not materialized, and requests that never became runs. Without an inventory of expectations and reconciliation, “nothing happened” is indistinguishable from “nothing was required.”

## Why This Matters

Time-based scheduling is deceptively familiar. Cron syntax is compact, but calendar meaning is not. A local day may be 23 or 25 hours across daylight-saving transitions. Month length varies. Business days exclude holidays that differ by jurisdiction and year. A fixed 24-hour interval drifts relative to a 09:00 local-time obligation. Incorrect calendars silently process the wrong population.

Logical and physical time diverge. A run for Monday’s data may be created Tuesday after the interval closes, queued for an hour, start later, and finish Wednesday. Using actual start time inside transformation logic makes delay change the answer. Immutable interval/partition parameters preserve semantic scope.

Event delivery is also imperfect. Brokers, webhooks, watchers, and polling systems can duplicate, delay, reorder, or lose notifications. CloudEvents specifies source plus ID uniqueness so duplicates can be recognized, but a formatting standard does not make transport or business effects exactly once. Durable consumer state and deterministic request identity remain necessary.

Events describe occurrences, while data pipelines require state. An “object created” event may refer to one part of a multipart delivery. A “producer succeeded” message may precede catalog visibility. A later correction may supersede the announced generation. The trigger should resolve authoritative manifests and readiness rather than blindly convert every message into work.

Fan-in magnifies ambiguity. If sales needs orders and exchange rates, receiving any two messages is not enough: both could be duplicate orders notifications or belong to different dates. Correlation must name source, partition, generation, schema, quality, and compatibility.

Scheduling policy also controls load. Catching up a year of missed hourly slots can overwhelm compute and downstream services. One event per row can create a run storm. Coalescing reduces overhead but delays data and can obscure per-event accountability. Overlap and admission rules need explicit cost, latency, and correctness trade-offs.

Finally, triggers are authority surfaces. A forged event or malicious parameter can launch expensive work, access another tenant, overwrite data, or exfiltrate metadata. Authentication, authorization, schema validation, quotas, allowlisted parameters, and audit belong before run creation.

## Prerequisites and Retrieval

Retrieve all job/schedule/trigger definitions and versions; intended products, partitions, data intervals, owners, and service objectives; cron, fixed-interval, recurrence, business-calendar, start/end, exclusion, holiday, and time-zone rules; time-zone database/version assumptions; logical-time and manual-trigger semantics; pause/resume, catch-up, missed-slot, and historical-run policy; overlap, queue, replace, coalesce, debounce, maximum-delay, concurrency, and overload policy; expected run inventory and existing run keys; event sources, subscriptions, filters, schemas, identities, subjects, occurrence/receive times, revisions, sequence positions, ordering partitions, retention, replay, acknowledgement, and dead-letter handling; authoritative dataset manifests/generations; fan-in and partition mappings; completeness, watermark, quality, and publication predicates; polling/watch cursors; reconciliation state; manual/repair interfaces; job parameters and secret references; authentication, authorization, tenant scope, quotas, and audit; schedule/run/materialization history; scheduler availability and clock evidence; incidents; and dashboards for lag, backlog, duplicates, missed work, and freshness.

Distinguish calendar recurrence from fixed elapsed interval; local civil time from UTC instant; time-zone name from numeric offset; schedule definition from slot; slot time from data interval; interval start from end; logical/nominal time from requested/admitted/started/completed time; occurrence time from producer publish, broker, receive, and processing time; schedule tick from data readiness; event from authoritative state; event identity from subject; duplicate delivery from repeated legitimate occurrence; arrival order from source revision/order; event filter from authorization; run request from job run; run key from run ID; catch-up from backfill; pause from cancellation; skipped slot from fulfilled no-op; debounce from permanent delay; coalescing from data loss; overlapping execution from concurrent publication; and notification acknowledgement from completed business effect.

Create a trigger contract:

| Concern | Required decision and evidence |
|---|---|
| Intent | Job/asset, owner, reason, expected outputs, and service objective |
| Definition | Schedule/trigger version, active interval, environment, and change policy |
| Time | Calendar, time zone, recurrence, interval mapping, boundaries, exclusions, tzdb |
| Slot | Stable slot/partition key, logical time, eligibility, deadline, and provenance |
| Event | Source+ID, type/schema, subject, revision/position, occurrence/receive time, payload reference |
| Readiness | Exact sources, generations, partitions, completeness, compatibility, quality |
| Request | Deterministic run key, job version, parameters, inputs, authorization, creation receipt |
| Multiplicity | Deduplication, correlation, coalescing, debounce, overlap, concurrency, replacement |
| Absence | Missing-event/slot detection, proactive deadline, reconciliation cursor, repair |
| Overload | Backlog bounds, priority, quotas, rate limits, shedding, pause, escalation |
| Evidence | Decision trace, ignored/blocked reason, request/run/materialization/publication link |
| Governance | Owners, tenant filtering, secret handling, retention, replay, audit, deprecation |

Write a falsifiable rule: “For tenant T and local business day d under calendar C version 5, create at most one active request for job J version 7 and exact orders/rates generation tuple G. The request becomes eligible after interval close and only when both manifests are complete and compatible. Duplicate events reproduce the same key; a corrected generation creates a superseding request; reconciliation alerts by deadline L if either input or request evidence is absent.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish schedule definitions, slots, logical times, data intervals, run requests, job runs, and physical execution times;
2. choose among cron/calendar, fixed-interval, business-calendar, event-driven, state-polling, manual, and hybrid triggers;
3. specify time zones, daylight-saving behavior, interval boundaries, calendars, exclusions, eligibility, deadlines, and catch-up;
4. design stable slot identities and deterministic run keys for concurrent and replayed trigger evaluation;
5. consume events with explicit source/ID, schema, subject, revision, ordering, deduplication, and authoritative-state lookup;
6. correlate multi-input events to exact compatible dataset generations and partitions;
7. govern debounce, coalescing, overlap, backlog, concurrency, quotas, and event storms;
8. reconcile expected schedule slots and authoritative ready data against requests, runs, materializations, and publications;
9. measure schedule delay, event delay, readiness delay, queue delay, execution time, end-to-end freshness, and missing-work risk; and
10. secure, test, migrate, pause, resume, replay, and decommission scheduling and trigger definitions.

## Core Exposition

### Start from the data obligation

Choose a trigger only after defining what output should exist for which scope. “Daily” may mean one result per UTC date, per tenant-local business day, per source close, or per complete delivery. The output contract supplies the partition and completeness semantics; the trigger supplies a proposal time.

For a bounded interval $[a,b)$, state whether execution becomes eligible at $a$, at $b$, after a delay, or after independent completeness evidence. End-of-interval processing usually waits until $b$ because data can arrive throughout the interval. A trigger at midnight on day d+1 may therefore create the run for day d.

Do not read current time inside core transformation logic to infer scope. Pass immutable interval/partition parameters from the run manifest. The same logical request can then run late, replay, or move between environments without changing its population.

Name an owner for schedule meaning. Platform operators can run the scheduler, but domain owners decide which calendar, close, lateness, and missing-input policy produces valid data.

### Model schedule as intended slots

A schedule definition expands into a set or sequence of intended slots over a bounded horizon. Each slot has stable identity, logical/nominal time, data interval/partition, eligibility instant, deadline, and schedule-definition version.

Persist enough slot inventory to answer:

- Was this slot intended under the active version?
- Was it eligible, suppressed, paused, skipped, or expired?
- Did it create a request, and under which run key?
- Did a request create a run and accepted output?
- If rules changed, which version governs historical interpretation?

Avoid using actual run ID as slot identity. Concurrent controllers may create two run objects for the same slot before deduplication. Conversely, a correction may legitimately create a new request for the same partition with different generations. Slot identity and generation-bound run key solve different problems.

Schedules are intent generators, not timers with perfect delivery. A controller may observe a due slot late or more than once. Durable uniqueness and reconciliation make evaluation repeatable.

### Choose calendar or elapsed-time semantics

A fixed interval says “every N elapsed seconds from anchor A.” It is suitable for cadence unrelated to civil clock, but a 24-hour interval will shift relative to local wall time across offset changes.

A cron/calendar rule says “at these civil times/dates.” It requires a named time zone and precise interpretation of gaps and repeated local times. “09:00 Europe/Stockholm” differs from “08:00 UTC,” especially across daylight-saving transitions.

A business calendar adds working days, holidays, early closes, fiscal periods, and exceptional closures. Version the calendar and assign ownership. A simple weekday cron cannot correctly express all holidays; Airflow’s custom-timetable example similarly shows why weekday cron can produce a Friday-to-Monday interval and miss holiday requirements.

RFC 5545 recurrence rules can represent rich recurrences and time-zone components, but using a standard syntax does not choose the business policy for ambiguous/nonexistent local times. Test actual generated instants around every transition and calendar change.

Record time-zone database assumptions where reproducibility matters. Civil-time rules are political data and can change. Historical reruns should preserve the original interval identities or explicitly migrate them.

### Separate every relevant clock

Track at least:

- interval start/end: semantic data scope;
- logical/nominal time: schedule occurrence identity;
- eligibility time: earliest request evaluation;
- trigger observation time: controller noticed the fact;
- event occurrence time: source says the occurrence happened;
- event publish/broker/receive times: transport path;
- request creation and admission times;
- actual run/task start/end times; and
- materialization/publication time.

These differences yield actionable latency components. Schedule delay is observation/request minus eligibility. Event transport delay is receive minus occurrence when clocks/semantics are trustworthy. Readiness delay is ready minus interval end or expected source time. Queue delay is run start minus admission. Execution duration is end minus start. Publication delay completes the end-to-end freshness path.

Do not subtract timestamps from unsynchronized sources without uncertainty bounds. Clock drift can make negative apparent latency. Broker position or producer revision can be stronger ordering evidence than wall time.

### Define catch-up, pause, and resume

When a schedule activates after its start, the controller may create all past slots, only the latest, none, or an explicitly bounded set. State the policy. Airflow exposes catch-up behavior for unrun data intervals; the broader design lesson is that missing past intervals need a deliberate choice.

Pause should stop creating or admitting new work according to a declared boundary. It does not automatically cancel active runs or erase due slots. Record pause actor, reason, time, affected definitions/tenants, and whether events/slots continue accumulating.

On resume, options include catch all missed slots, create latest only, coalesce a range, require manual approval, or expire old work. Estimate load and downstream impact before releasing a large backlog. Preserve which slots were intentionally skipped versus simply not observed.

Backfill in DE-046 is an explicit historical execution plan with scope and capacity controls. Catch-up is scheduler policy for due slots. They may use the same job but have different provenance and approval.

### Define overlap and concurrency policy

If a new slot becomes eligible while a prior run is active, policy can:

- allow concurrent runs when partitions and sinks are isolated;
- queue in slot order;
- forbid/skip overlap and reconcile later;
- replace or cancel older work when only latest state matters;
- coalesce several slots into a range run; or
- block pending operator decision.

Kubernetes CronJob exposes Allow, Forbid, and Replace policies and documents approximate job creation, including possible duplicates or omissions. A data platform needs additional semantics: whether partitions overlap, whether cancellation is safe, and whether publication is fenced.

“Forbid” can turn a slow prior run into a missed slot. “Replace” can leave partial side effects. “Allow” can race on mutable targets. The scheduler policy must align with task idempotency and candidate/publication isolation developed in DE-044.

Apply concurrency limits by tenant, job, asset, source, warehouse, or global budget as appropriate. Capacity admission must not silently mutate the run’s data interval or input generations.

### Treat an event as notification with identity

An event record should carry source, event ID, type/version or schema URI, subject, occurrence time, producer revision/sequence when available, data/manifest reference, trace/causation context, and tenant/security classification.

CloudEvents requires source, ID, specification version, and type, and defines source plus ID as the uniqueness scope for distinct events. Use this as an interoperable envelope where suitable, then add domain fields. Do not deduplicate only by ID if sources can collide.

The subject names what changed; it is not the event identity. Two legitimate updates to the same file/customer/partition have the same subject but distinct occurrence IDs/revisions. Payload hashing can detect exact redelivery but may collapse semantically distinct assertions or vary because of nonsemantic serialization.

Persist the raw accepted event before acknowledging when recovery requires replay. Validate envelope and schema, authenticate producer/channel, authorize tenant/type/scope, enforce size/rate limits, and quarantine invalid or suspicious inputs.

### Convert events into authoritative state

An object-created message may arrive before listing/read visibility, may refer to a temporary upload, or may be followed by a manifest correction. Resolve the authoritative object generation and manifest under the source contract.

Maintain trigger state per source/partition:

- latest accepted revision or source position;
- exact generation and completeness;
- schema/quality/compatibility state;
- event IDs contributing to the decision;
- last reconciliation cursor; and
- requests/materializations already derived.

Apply source ordering, not receive order. For equal revision with conflicting generation, fail closed and escalate. For stale revisions, retain the event evidence but do not regress current trigger state.

Use event payloads as hints or evidence, not uncontrolled job parameters. Fetch authorized state and bind immutable inputs. If the source makes the event itself authoritative, specify signature, retention, schema, ordering, and replay semantics accordingly.

### Correlate fan-in by partition and generation

For required sources $U$, readiness is a join over source, target partition, and compatibility—not an event count. Maintain one state cell per $(source,partition)$ and evaluate the exact dependency predicate from DE-041.

For orders plus rates, require one complete orders generation and the mapped rate partitions/snapshot. Two orders events do not satisfy the rates edge. An orders event for day d and rates event for day d+1 do not form a valid cut.

An AND trigger waits for all required evidence. An OR trigger creates work for any qualifying source but still binds other needed inputs through fallback/currentness rules. Optional inputs need explicit degraded semantics. Airflow’s asset-aware scheduling supports AND/OR conditions; regardless of tool, the data contract decides what combination is valid.

Keep correlation state durable and bounded. Define expiry, late completion, correction, and cleanup. Never delete evidence merely because one run was requested; a later correction may require a superseding run.

### Deduplicate run intent, not just messages

Message deduplication prevents repeated processing of the same envelope. Run-request deduplication prevents different messages or evaluators from creating the same logical work. You need both.

Canonicalize a run key from job/definition version, partition/scope, effective parameters, and exact relevant input generations. Store it under a uniqueness constraint or compare-and-create operation. Race-prone “check then insert” logic can still duplicate requests.

If duplicate evaluation finds an existing matching request, attach additional event/decision evidence rather than creating a run. If a later source correction changes a bound generation, derive a different key and mark its relationship to the earlier request/materialization.

Do not embed secrets in keys. Use stable secret-reference/version identifiers when configuration affects semantics. Define canonical ordering and normalization so logically identical maps produce the same key.

Run ID identifies one job-run object. Run key identifies equivalence of requested intent. A platform may have multiple physical attempts or even replacement run objects tied to one logical key under recovery policy, but it must preserve the relationship.

### Avoid level-triggered infinite execution

An event is ideally an edge: “generation G became published.” A polling condition such as “file X exists” is a level that remains true. If every poll treats true as new, the workflow triggers forever.

Store transition state: last observed object generation, version, modification token, source offset, or condition epoch. Trigger only when a new qualifying state appears, or pair the state with a deterministic run key that deduplicates repeated observations.

Airflow’s event-scheduling documentation warns that conditions which remain true, such as persistent file existence or a job remaining successful, can cause infinite rescheduling. This is a general systems property, not merely a product rule.

Polling is still useful when no push event exists. Use durable cursors, bounded intervals with jitter/backoff, rate limits, and authoritative snapshots. Reconciliation polling can complement push events even when the normal path is event-driven.

### Govern debounce and coalescing

Debounce waits for a quiet period before requesting work. It fits bursty updates where only the consolidated state matters. Coalescing combines events into a batch or range. Define:

- grouping key such as tenant/asset/partition;
- quiet period;
- maximum wait;
- maximum events/bytes/partitions;
- exact included source range or event IDs;
- late-event and correction behavior;
- priority and service objective; and
- failure/replay identity.

Without maximum wait, continuous traffic can starve execution forever. Without stable boundaries, replay can create a different batch. Seal a batch with a manifest/cursor range and deterministic key.

Do not coalesce obligations that require separate audit, isolation, priority, schema, or ownership. A large tenant must not delay or expose another tenant’s work. Fairness and quotas belong in admission.

Event storms can arise from feedback, mass updates, duplicated notifications, or a newly enabled consumer. Apply bounded queues, per-source/tenant quotas, rate limiting, collapse by authoritative generation when safe, and explicit overload state. Silent dropping breaks reconciliation.

### Combine time and event triggers deliberately

Hybrid patterns include:

- run when data is ready, but alert/fallback at a deadline;
- run on event, plus periodic reconciliation for missed events;
- run after both an asset update and a calendar boundary;
- run periodically using the latest compatible snapshot;
- accumulate events until a fixed close; and
- schedule a provisional run, then supersede after late data under policy.

State the Boolean and temporal semantics. “Event OR midnight” can create two requests unless both paths derive the same key. “Event AND interval close” needs durable queued event state. “All assets updated since last run” must define per-source generations and last accepted cut.

Time triggers make expected absence observable; event triggers reduce latency. The combination is often stronger than either alone when run identity and reconciliation unify them.

### Handle missing, delayed, and corrected inputs

Define an expected-arrival or readiness deadline by source/partition. At deadline, choose block/alert, use approved fallback, publish degraded output, skip with explicit unfulfilled state, or create a repair plan. Never convert missing to empty implicitly.

Late input can request the original partition, a correction window, or a future cumulative run depending on ownership and influence. Bind exact revised generation and point to superseded request/materialization. DE-038’s restatement model applies after trigger detection.

Out-of-order events require source revision/position semantics. Arrival time is not authority. Equal-rank conflicting events must not be broken by arbitrary lexical generation ID unless the contract authorizes it.

Tombstone/delete events can invalidate rather than create data. Route them through the same identity and authorization controls and compute affected downstream scope.

### Make manual and repair triggers first-class

Manual runs are not outside governance. Record requester/approver, reason, ticket/incident, selected definition version, scope, parameters, input generations, authorization, and relation to scheduled/event intent.

Do not assume a manually supplied logical date equals the timetable’s data interval. Airflow explicitly documents that manual run data intervals depend on the timetable and trigger path. Resolve and display both.

Repair/reconciliation runs should use the same production contracts and candidate publication, but distinct provenance and possibly stricter approval/capacity controls. Avoid an unrestricted “run with arbitrary JSON” interface.

Dry-run/preview should show resolved slots, partitions, generations, run keys, estimated work/cost, conflicts, active runs, and permissions without creating requests. Preview itself must not consume event state.

### Reconcile from authoritative inventories

Reconciliation closes the gap between intent and delivered notifications. Periodically compare:

1. schedule versions and intended slots;
2. authoritative source manifests and ready partitions;
3. accepted events and trigger-state reductions;
4. durable run requests and job runs;
5. materializations, quality, and publication; and
6. consumer-visible freshness.

Classify gaps: expected slot absent, event absent but data ready, event present but unprocessed, trigger state ready but request absent, request without run, run without accepted output, output without publication, or duplicate/conflicting intent.

Repair idempotently with the same deterministic keys. Do not invent an event if authoritative data is enough; record reconciliation provenance. If state is uncertain, quarantine/escalate rather than manufacture success.

Reconciliation has its own cursor, coverage horizon, access, cost, and lag objective. Test it independently by suppressing normal notifications and scheduler observations.

### Observe the full latency and correctness funnel

Count expected slots, eligible slots, accepted events, unique occurrences, ready partitions, requests, admitted runs, started/completed runs, accepted materializations, publications, and fresh consumer views. Preserve denominators.

Measure distributions and tails for:

- schedule observation delay;
- event transport/processing delay;
- data readiness delay;
- request/admission/queue delay;
- execution duration;
- validation/publication delay; and
- end-to-end interval-close or occurrence-to-consumer freshness.

Track duplicate, stale, conflicting, invalid, unauthorized, quarantined, and dead-letter events; missing inputs; blocked correlations; backlog age; coalescing size/wait; skipped/expired slots; overlapping runs; reconciliation repairs; and false/missed triggers.

A low average trigger latency can coexist with missing old partitions or a harmed tenant. Segment by source, tenant, partition class, trigger path, schedule version, and outcome while applying privacy/minimum-group controls.

### Secure and govern the trigger surface

Authenticate event producers and manual requesters. Authorize source/type/tenant/asset/job/parameter combinations. Validate schema, signatures, timestamps within policy, revisions, and payload references. Rate-limit by identity and bound resource cost.

Do not trust a tenant ID, storage path, job name, or parameters solely because they appear in a signed payload; verify the producer is authorized to assert them. Resolve secrets server-side from allowlisted references.

Prevent confused-deputy behavior: a low-privilege producer should not trigger a high-privilege job over arbitrary data. Derive permitted job/scope from policy, not payload-controlled templates.

Minimize event and trigger retention while preserving audit/replay obligations. Encrypt sensitive data, redact logs and run keys, tenant-filter interfaces, and protect dead-letter payloads. Audit definition changes, pauses, cursor resets, replays, manual requests, overrides, and deletions.

### Test schedules and triggers adversarially

For schedules, generate slots across start/end, leap days, month/year boundaries, short/long months, weekends/holidays, daylight-saving gaps/folds, time-zone rule changes, pause/resume, controller downtime, and definition changes. Compare a reviewed oracle of expected intervals and keys.

For events, inject duplicates, reordering, stale and equal-conflict revisions, delay, loss, corrupt/oversize payload, unauthorized tenant/type, replay after retention, broker redelivery, poison messages, event storms, and source reset. Verify no missed or multiplied intent.

For fan-in, vary missing/late/duplicate parents, mismatched partitions, incompatible generations, optional inputs, correction after request, and queued evidence. For hybrid triggers, race schedule, event, manual, and reconciliation evaluators and require one equivalent request key.

For state, crash between event receipt and trigger-state commit, between state commit and request creation, and after request creation before acknowledgement. Durable transactional/outbox or reconciliation mechanisms must restore the same intent.

For operations, test overlap policies, concurrency caps, backlog release, coalescing maximum delay, pause/resume, clock skew, scheduler failover, authorization revocation, and conditional publication. Retain the decision trace explaining why each event/slot was ignored, blocked, coalesced, or requested.

## Definitions and Notation

Let schedule definition $s$ have version $v_s$, calendar/time-zone policy $C_s$, active horizon $H_s$, and recurrence $R_s$. Expansion function $Slots(s,H)$ returns finite slot records over bounded horizon $H$.

Each slot

$$
z=(s,v_s,p,[a,b),l,e,d)
$$

contains stable partition/slot key $p$, half-open data interval $[a,b)$, logical time $l$, eligibility time $e$, and deadline $d$. Actual observation, request, admission, start, and end times are separate fields.

Event

$$
x=(source,id,type,schema,subject,t_o,t_r,revision,reference)
$$

contains occurrence time $t_o$ and receive time $t_r$. Identity is pair $(source,id)$. Subject may repeat across distinct events. Revision or source position supplies ordering only within its declared scope.

For required upstream set $U$ and target partition $p$, trigger state maps each $(u,p)$ to selected exact generation:

$$
state:U times P to Generation union Unavailable.
$$

Readiness is

$$
ready(p)=all(u in U: complete(state(u,p)) and compatible(state(u,p),p)).
$$

For eligible binding vector $G_p$, deterministic request key is

$$
K=hash(canonical(jobversion,p,params,G_p)).
$$

The hash supports compact identity only if canonicalization, included fields, algorithm, and collision handling are governed. The logical tuple is the contract.

Let $E_H$ be expected schedule slots in horizon $H$, $Q_H$ durable run requests, and $M_H$ accepted materializations. Reconciliation sets include:

$$
missingRequests=E_H minus slots(Q_H),
$$

$$
missingOutputs=keys(Q_H) minus requestKeys(M_H).
$$

In practice, skip/expiry/no-op/waiver states qualify these differences; raw set subtraction is a diagnostic candidate, not a final verdict.

## Mechanisms, Invariants, or Proof Structure

The scheduling assurance chain is:

1. **Obligation integrity:** output partition, interval, owner, completeness, and deadline are explicit.
2. **Temporal integrity:** schedule/calendar/time-zone version expands deterministically to stable slots, including boundary cases.
3. **Event integrity:** accepted events have authenticated source/ID, schema, subject, ordering/revision, and retained evidence.
4. **State integrity:** duplicates and stale events do not regress state; conflicts fail closed; exact authoritative generations are resolved.
5. **Readiness integrity:** all required partition mappings, completeness, quality, and compatibility predicates hold.
6. **Request integrity:** deterministic generation-bound keys and durable arbitration create one equivalent logical intent despite evaluator races.
7. **Operational integrity:** catch-up, overlap, coalescing, backlog, pause/resume, admission, and manual actions preserve scope and evidence.
8. **Reconciliation integrity:** expected slots and authoritative ready data are compared with requests, runs, outputs, and publications.
9. **Governance integrity:** trigger authority, tenant boundaries, secrets, quotas, audit, retention, and deprecation are enforced.

The following finite standard-library model illustrates event identity, revision reduction, fan-in readiness, schedule inventory, deterministic run keys, delivery-order independence, and correction rekeying. It does not implement calendars, time zones, transport, durability, concurrency, authorization, execution, quality, or publication.

<!-- bijux-verify: {"id":"schedule-event-run-intent","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"received_events=7\nunique_events=6\nduplicate_events=1\nexpected_partitions=('2026-09-01', '2026-09-02', '2026-09-03')\nready_partitions=('2026-09-01', '2026-09-02')\nblocked_partitions=(('2026-09-03', ('orders',)),)\nrun_keys=('daily_sales:2026-09-01:orders=o103:rates=r7', 'daily_sales:2026-09-02:orders=o102:rates=r8')\norder_independent=True\nlate_correction_rekeys_day1=True\ncreated_run_requests=2\n","stderr":""}} -->
```python
EXPECTED_PARTITIONS = ("2026-09-01", "2026-09-02", "2026-09-03")
REQUIRED_SOURCES = ("orders", "rates")
EVENTS = (
    ("evt-o-101", "orders", "2026-09-01", "o101", 1),
    ("evt-r-7", "rates", "2026-09-01", "r7", 1),
    ("evt-r-7", "rates", "2026-09-01", "r7", 1),
    ("evt-o-102", "orders", "2026-09-02", "o102", 1),
    ("evt-o-103", "orders", "2026-09-01", "o103", 2),
    ("evt-r-8", "rates", "2026-09-02", "r8", 1),
    ("evt-r-9", "rates", "2026-09-03", "r9", 1),
)


def plan(events):
    unique = {}
    duplicates = 0
    for event in events:
        event_id, source, _partition, _generation, _revision = event
        identity = (source, event_id)
        if identity in unique:
            if unique[identity] != event:
                raise ValueError("conflicting duplicate event")
            duplicates += 1
        else:
            unique[identity] = event
    latest = {}
    for _event_id, source, partition, generation, revision in unique.values():
        key = (source, partition)
        candidate = (revision, generation)
        if key in latest and latest[key][0] == revision and latest[key][1] != generation:
            raise ValueError("equal-revision conflict")
        if key not in latest or candidate > latest[key]:
            latest[key] = candidate
    requests = []
    blocked = []
    for partition in EXPECTED_PARTITIONS:
        missing = tuple(
            source
            for source in REQUIRED_SOURCES
            if (source, partition) not in latest
        )
        if missing:
            blocked.append((partition, missing))
            continue
        bindings = tuple(
            (source, latest[(source, partition)][1])
            for source in REQUIRED_SOURCES
        )
        run_key = "daily_sales:" + partition + ":" + ":".join(
            f"{source}={generation}"
            for source, generation in bindings
        )
        requests.append((partition, run_key))
    return tuple(requests), tuple(blocked), duplicates


requests, blocked, duplicates = plan(EVENTS)
reversed_requests, reversed_blocked, _ = plan(tuple(reversed(EVENTS)))
initial_requests, _, _ = plan(EVENTS[:4])
print(f"received_events={len(EVENTS)}")
print(f"unique_events={len(EVENTS) - duplicates}")
print(f"duplicate_events={duplicates}")
print(f"expected_partitions={EXPECTED_PARTITIONS}")
print(f"ready_partitions={tuple(partition for partition, _key in requests)}")
print(f"blocked_partitions={blocked}")
print(f"run_keys={tuple(key for _partition, key in requests)}")
print(
    "order_independent="
    f"{(requests, blocked) == (reversed_requests, reversed_blocked)}"
)
print(
    "late_correction_rekeys_day1="
    f"{initial_requests[0][1] != requests[0][1]}"
)
print(f"created_run_requests={len(requests)}")
```

The duplicate rates envelope shares source and event ID with identical content, so it contributes evidence but no new occurrence. Revision 2 for September 1 orders supersedes revision 1. Because selection is based on revision rather than arrival, reversing delivery preserves readiness and keys.

Two of three expected slots become ready. September 3 remains explicitly blocked with missing tuple orders, rather than disappearing because no run was created. The generated keys bind both sources. The correction changes the September 1 key because o103 differs from o101, permitting a distinct superseding intent.

The example uses lexical generation comparison only after revision in the tuple assignment, but equal-revision conflicting generations fail before selection. Production systems must not use arbitrary lexical ordering as authority.

## Alternatives and Trade-Offs

**Cron/calendar versus fixed interval.** Cron keeps civil-time alignment; elapsed intervals keep uniform duration. Choose from domain meaning, not syntax familiarity, and test offset transitions.

**Time-driven versus event-driven.** Time creates a predictable expectation and detects absence; events reduce latency and reflect actual changes. Hybrid event-plus-reconciliation designs often provide stronger coverage.

**Push versus poll.** Push reduces repeated queries but depends on event delivery and producer integration. Polling can recover authoritative state but costs requests and can become level-triggered. Durable cursors and generation comparison matter in both.

**At interval start versus after interval close.** Start-triggered work reduces latency for proactive/continuous processing but cannot assume full interval completeness. End-triggered work fits bounded batch outputs but may delay results. State the data contract.

**Catch all versus latest only.** Catch-up preserves each historical obligation but can create load and obsolete intermediate output. Latest-only suits snapshot semantics but is wrong for independently owned partitions or events. Coalesced ranges need explicit lineage.

**Allow versus queue/forbid/replace overlap.** Allow maximizes throughput for isolated partitions. Queue preserves order. Forbid may miss deadlines; replace requires safe cancellation and supersession. Publication fencing is independent.

**One event per run versus coalescing.** Per-event runs maximize traceability and latency responsiveness but can overwhelm control/compute planes. Coalescing saves overhead but needs sealed ranges, maximum wait, and consumer acceptance.

**Event payload versus authoritative lookup.** Payload-only execution reduces lookup latency and can support replay if events are authoritative. Lookup reduces trust in stale/spoofed hints and resolves completeness. Define which is the source of truth and retain exact versions.

**Wall-clock time versus source position/revision.** Time works across systems but suffers skew and ambiguous semantics. Positions/revisions provide scoped order but may reset or be incomparable across partitions. Preserve both.

**Central versus domain-owned calendars.** Central service avoids duplicated code and supports audit. Domain owners still decide business holidays/closes and approve changes. Versioned calendar products can separate implementation from authority.

**Strict readiness versus deadline fallback.** Strict fan-in protects completeness. An approved fallback can meet availability needs with degraded labeling and later correction. Never silently weaken the predicate.

## Failure Modes and Misconceptions

- **“Cron means once.”** Scheduler evaluation and job creation can be delayed, omitted, or duplicated; use stable slots and durable request keys.
- **“Daily means 24 hours.”** Civil days vary across time zones and daylight-saving transitions.
- **“Run start determines partition.”** Queue delay would change data scope; bind the logical interval before execution.
- **“Logical date always equals interval start.”** Timetable and trigger paths define the relation; manual paths may differ.
- **“The clock proves data is ready.”** Time supplies eligibility or a deadline, not source completeness.
- **“An event proves state.”** Resolve authoritative generation/manifest unless the contract makes the signed event itself authoritative.
- **“Event ID is globally unique.”** Standards commonly scope uniqueness by source; preserve both.
- **“Same subject means duplicate.”** The same object/partition can have legitimate corrections and revisions.
- **“Arrival order is source order.”** Networks reorder; use source position/revision or explicit conflict policy.
- **“Two messages satisfy two parents.”** Correlate named sources, partitions, generations, and compatibility.
- **“Exactly-once delivery gives exactly-once output.”** Business effects cross storage and controllers; deterministic intent and idempotent publication are still required.
- **“Polling true is an event.”** Persistent true conditions can trigger repeatedly unless state transitions are tracked.
- **“Debounce until quiet is safe.”** Continuous traffic can starve work without a maximum delay.
- **“Pause means no backlog.”** Decide whether slots/events accumulate, expire, coalesce, or require approval.
- **“Forbid overlap preserves every slot.”** Slow work can make later occurrences missed.
- **“Manual means exceptional and untracked.”** Manual and repair runs need stronger provenance and authorization.
- **“No event means no data.”** Notifications can be lost; reconcile against authoritative state.
- **“Metadata cannot leak data.”** Event subjects, paths, parameters, tenant keys, and errors can be sensitive.

## Worked Examples

### Example 1

A 09:00 Europe/Stockholm schedule and a 09:00 UTC schedule coincide only during part of the year. Store the named zone and slot instants; do not replace the former with a fixed offset.

### Example 2

A daily batch starts at 02:00 after queue delay but owns the prior calendar day. It receives interval and partition from the run manifest. Reading current date would process the wrong day during delayed or historical execution.

### Example 3

One file-created condition remains true for a week. A poller compares object generation G with last observed generation and creates one request key. Rechecking existence alone would create unbounded runs.

### Example 4

Orders event d arrives twice; rates event d arrives once. Source+event-ID deduplication leaves two distinct occurrences, and source/partition correlation satisfies the two-parent join exactly once.

### Example 5

An orders correction with higher source revision arrives after the first partition was published. The trigger creates a new generation-bound key linked as a correction; it does not rewrite the old request or treat the event as stale by wall-clock arrival alone.

### Example 6

A schedule is paused for 90 daily slots. Resume preview estimates data availability, compute, downstream rate limits, and obsolete slots. Operators approve bounded batches rather than releasing all work simultaneously.

### Example 7

A per-minute job runs for three minutes. Allow creates isolated minute partitions concurrently; Forbid skips/defers occurrences; Replace cancels earlier work. The correct choice depends on partition independence, side effects, and freshness semantics.

### Example 8

A stream of updates never becomes quiet. Debounce with 30-second quiet period and five-minute maximum wait seals a manifest at five minutes, preventing starvation while allowing later events into the next batch.

### Example 9

An event is accepted and trigger state committed, then the process crashes before request creation. Reconciliation sees ready state without the deterministic run key and creates it once. A check-then-create race without uniqueness could duplicate it.

### Example 10

A signed event for tenant A contains a parameter requesting tenant B’s dataset. Signature proves producer identity, not authority for arbitrary scope. Policy rejects the request and audits the attempt without invoking the high-privilege job.

## Cross-Program Connections

[API-061](../../28-api-and-service-engineering/modules/061-commands-events-and-messages.md) distinguishes occurrences from commands and transport records. [API-062](../../28-api-and-service-engineering/modules/062-event-schema-design.md), [API-065](../../28-api-and-service-engineering/modules/065-ordering-and-partition-keys.md), [API-066](../../28-api-and-service-engineering/modules/066-delivery-and-acknowledgment.md), and [API-067](../../28-api-and-service-engineering/modules/067-idempotent-consumers.md) supply event contract, ordering, delivery, and consumer foundations.

[PLAT-043](../../29-platform-engineering/modules/043-batch-and-scheduled-workload-templates.md) and [PLAT-044](../../29-platform-engineering/modules/044-event-driven-workload-templates.md) provide platform golden paths; [PLAT-069](../../29-platform-engineering/modules/069-platform-eventing.md) covers the shared event substrate. This module defines the data-workflow semantics those capabilities must preserve.

Within Data Engineering, [DE-022](022-watermarks-and-high-water-marks.md) governs source progress, [DE-023](023-file-arrival-and-manifest-processing.md) governs complete deliveries, [DE-034](034-partitioned-processing.md) governs interval ownership/context, [DE-038](038-late-corrections-and-restatement.md) governs corrections, and [DE-041](041-directed-acyclic-graphs-and-dependencies.md) through [DE-042](042-tasks-jobs-assets-and-datasets.md) define graph and object identity.

## References

1. Apache Airflow, [DAG Runs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html). Documents scheduled/manual runs, data intervals, logical dates, catch-up, and backfill distinctions. Accessed 2026-09-03.
2. Apache Airflow, [Asset-Aware Scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html). Documents data-update scheduling, queued asset events, push/pull sources, AND/OR conditions, and time-plus-asset schedules. Accessed 2026-09-03.
3. Apache Airflow, [Event-Driven Scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/event-scheduling.html). Documents external-event scheduling and the risk of infinite execution from persistent state conditions. Accessed 2026-09-03.
4. Apache Airflow, [Customizing DAG Scheduling with Timetables](https://airflow.apache.org/docs/apache-airflow/stable/howto/timetable.html). Demonstrates explicit interval, weekday, holiday, time-zone, and manual-run timetable semantics. Accessed 2026-09-03.
5. Kubernetes, [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/). Documents cron/time-zone schedules, deadlines, concurrency policies, pause/resume effects, missed schedules, and approximate job creation. Accessed 2026-09-03.
6. Cloud Native Computing Foundation, [CloudEvents Specification](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md). Defines event, producer/source/consumer, source-plus-ID identity, type, subject, occurrence time, schema, and data context. Accessed 2026-09-03.
7. RFC Editor, [RFC 5545: Internet Calendaring and Scheduling Core Object Specification](https://www.rfc-editor.org/rfc/rfc5545.html). Defines recurrence rules, time-zone components, ambiguous/nonexistent local-time handling, exclusions, and interval recurrence semantics. Accessed 2026-09-03.
8. Prefect, [Schedule Flow Runs](https://docs.prefect.io/v3/concepts/schedules). Distinguishes interval, cron, and recurrence-rule schedules and describes time-zone/daylight-saving considerations. Accessed 2026-09-03.
9. Prefect, [Events](https://docs.prefect.io/v3/concepts/events). Defines event occurrence, resource, related-resource, payload, ID, and causal-following fields used by automations. Accessed 2026-09-03.
10. Apache Kafka, [Design](https://kafka.apache.org/40/design/design/). Documents delivery-semantics boundaries and the conditions around transactional exactly-once processing. Accessed 2026-09-03.

## Exercises

### Exercise 1

A job must process each Europe/Stockholm business day after local close, excluding Swedish holidays. Define schedule version, slot identity, data interval, eligibility, time-zone/DST and calendar policy, pause/resume, catch-up, and test cases. Explain why fixed 24-hour cadence is insufficient.

### Exercise 2

For one partition, the consumer receives orders revision 5, a duplicate of that event, rates revision 2, stale orders revision 4, and an equal-revision conflicting orders generation at revision 5. Specify event identities, reduction, fan-in readiness, run key, conflict response, and retained evidence.

### Exercise 3

A state watcher polls “file exists” every minute and has launched 500 identical runs. Redesign it as edge-sensitive event/poll processing with durable cursor, authoritative generation, deterministic request identity, crash recovery, missing-event reconciliation, and security controls.

### Exercise 4

A per-five-minute job often takes twelve minutes and writes a mutable aggregate. Compare Allow, Forbid/queue, Replace, and coalesced-range policies. Choose a design and state partition, side-effect, cancellation, deadline, correction, and publication requirements.

### Exercise 5

Design an assurance plan for a hybrid workflow triggered when orders and rates are ready, with a 06:00 deadline fallback and hourly reconciliation. Include clock fields, input correlation, duplicate/reorder/loss, trigger races, run keys, late corrections, pause/resume, backlog, observability, tenant security, tests, and recovery evidence.

## Answers to the Exercises

### Answer 1

Define versioned calendar C with Europe/Stockholm zone, governed Swedish holiday/exception list, local day boundaries, business-day predicate, close time, and time-zone database assumptions. Slot key can be canonical business date plus schedule version; interval is the corresponding local midnight-to-midnight or business-open-to-close interval converted to exact instants, with half-open boundaries. Eligibility is after close plus declared grace/completeness predicate; deadline is separately recorded.

Test spring gap, autumn fold, leap day, year/month boundaries, weekends, each holiday/early close, calendar revision, start/end bounds, delayed observation, and manual mapping. Pause records whether due slots accumulate. Resume preview applies approved catch-all, bounded batch, latest/coalesced, or expiry policy. A fixed 24-hour cadence preserves elapsed duration, not local close: offset transitions shift wall time, and business holidays/exceptional closes cannot be derived from duration alone.

### Answer 2

Identity is source plus event ID, so the exact redelivery is counted once as an occurrence but retained as delivery evidence. Source-scoped revision selects orders revision 5 over stale revision 4 and rates revision 2 for the same target partition. If the first revision-5 orders generation and the later revision-5 generation differ, authority is ambiguous: fail closed, quarantine/correlate the conflict, alert the source owner, and create no ready request until a tie policy or corrected higher revision resolves it.

After resolution, readiness requires exact complete compatible orders/rates generations. The run key includes job/definition version, partition, effective parameters, and both generations. Retain raw envelopes, source/ID, payload digests, receive/occurrence times, revisions, broker positions, duplicate link, conflict details, authoritative lookup, decision trace, readiness evidence, and any request receipt. Arrival order must not break the tie.

### Answer 3

Track the last observed object generation/version or manifest revision, not Boolean existence. On each poll, resolve authenticated authorized object metadata; only a new complete qualifying generation advances the durable cursor. Validate schema/tenant/path and derive a generation-bound run key under an atomic unique insert. Repeated polls attach observations to the same decision.

Commit trigger state and request through a transaction/outbox where possible; otherwise reconcile cursor state against the request table after crashes. Periodically list authoritative generations over a coverage horizon so lost watcher notifications create the same deterministic requests. Apply bounded polling, jitter, quotas, payload limits, least-privilege credentials, tenant/path allowlists, redacted logs, audit, retention, and poison/conflict handling. Test crashes before/after cursor and request commits plus concurrent watchers.

### Answer 4

Allow overlaps three partitions in flight but mutable aggregate writes can race unless each run owns isolated candidates and publication serializes/merges correctly. Forbid without queue can miss slots; queue preserves them but backlog/freshness grows. Replace reduces stale work but cancellation after partial mutable writes is unsafe. A coalesced range can process several five-minute partitions in one run, reducing overhead, but must seal exact boundaries and preserve per-partition lineage.

A defensible design is isolated per-partition or bounded-range candidates, queued/coalesced admission with maximum wait/backlog, and conditional publication/merge using exact ordered partitions. Cancellation stops computation but never assumes rollback of committed effects. Run keys bind range and input generations. Deadline policy exposes degradation rather than overwriting scope. Late inputs create correction keys and affected ranges. If independent isolated writes are available, limited Allow may be safe; the choice must be verified against target transaction semantics.

### Answer 5

Define source event occurrence/publish/broker/receive times; interval/logical/eligibility/deadline times; request/admission/start/end/materialization/publication times; clock uncertainty; and exact partition mappings. Reduce source+ID duplicates, select by source revision/position, reject equal conflicts, and join orders/rates for the same partition and compatible generations. Event path, 06:00 fallback, and hourly reconciliation all derive the same canonical key from job version, partition, parameters, and generations under durable uniqueness.

At 06:00, missing input triggers governed block/alert or explicitly approved degraded fallback; it does not invent completeness. Reconciliation compares authoritative manifests, accepted events, trigger state, requests, runs, and publications, repairing lost events/requests idempotently. A late correction produces a new key linked to supersession. Pause retains actor/reason and backlog policy; resume previews volume/cost and releases bounded cohorts. Metrics cover expected slots, unique events, readiness, blocked age, duplicates/conflicts, request/run/output funnel, every latency component, repairs, and freshness by tenant/source.

Authenticate producers, authorize source/type/tenant/job/parameters, resolve secrets server-side, enforce quotas and tenant-filtered metadata, retain/redact evidence, and audit replays/overrides. Tests race all trigger paths, duplicate/reorder/drop events, delay sources, crash at commit boundaries, skew clocks, cross DST/calendar boundaries, flood traffic, revoke authority, overlap runs, and advance generations during evaluation. Recovery evidence binds raw events, authoritative manifests, trigger cursor/state, decision trace, run-key receipt, job/run, materialization, checks, publication, and consumer observation.
