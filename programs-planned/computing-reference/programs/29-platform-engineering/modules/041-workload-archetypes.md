---
module_id: PLAT-041
program: Platform Engineering
level: 1
module_number: 41
title: Workload Archetypes
status: complete
last_verified: 2026-09-02
---

# Workload Archetypes

## One-Page Review

### Governing question

How should a platform classify recurring workload behavior into a small, durable set of archetypes so it can offer useful defaults and complete lifecycle paths without forcing unlike applications into one controller, hiding essential semantics, or multiplying templates without evidence?

### Essential definitions

- A **workload** is software plus its runtime inputs, dependencies, resources, identities, operations, state, and lifecycle expectations.
- A **workload archetype** is a versioned contract for recurring operational behavior and user outcomes; it is not a programming-language label or a YAML template.
- A **workload profile** is one application's declared requirements along archetype dimensions such as invocation, lifetime, state, concurrency, scaling, placement, and recovery.
- A **controller mapping** translates an archetype revision to provider resources such as a Deployment, StatefulSet, Job, CronJob, DaemonSet, or another runtime abstraction.
- A **replica** is one concurrently managed execution instance; replicas are interchangeable only when the workload contract permits it.
- **run to completion** means an execution has terminal success/failure semantics rather than an expectation of indefinite service.
- **delivery semantics** describe how work may be assigned and repeated—commonly at-most-once, at-least-once, or effectively-once under additional application mechanisms.
- A **scaling signal** is measured demand used to change capacity, such as concurrency, queue backlog/age, CPU, lag, or a schedule.
- **disruption tolerance** states which voluntary/involuntary removals, overlap, delay, and capacity loss the workload can safely endure.
- A **composite workload** is a system whose components use different archetypes, such as an HTTP service, queue consumer, scheduled reconciler, and migration job.

### Central model, mechanism, or theorem

Describe workload $w$ by profile $P(w)=(I,L,S,C,A,Q,D,R,O,G)$: invocation $I$, lifetime/termination $L$, state/identity $S$, concurrency $C$, availability/disruption $A$, scaling/queueing $Q$, delivery/retry $D$, resource/placement $R$, observability $O$, and governance/lifecycle $G$. Archetype $a$ is eligible only if its supported region contains every mandatory requirement of $P(w)$. A controller or template may implement eligible $a$, but resource kind alone cannot prove application semantics. Ambiguous or unsupported dimensions require refinement, composition, or an owned exception—not silent coercion.

### Critical invariants

- Archetypes are derived from recurring workload behavior and platform user jobs, not team names, languages, frameworks, or vendor products.
- Classification records evidence and uncertainty; a profile is not inferred solely from an image, repository, or current controller.
- Each archetype defines supported requirements, safe defaults, required inputs, status, lifecycle operations, non-guarantees, and escape conditions.
- Desired controller kind follows semantics. “Runs in Kubernetes” does not imply Deployment, and persistent storage alone does not imply correct StatefulSet behavior.
- Stateless replicas are interchangeable only when request/session/state behavior actually permits replacement, overlap, and horizontal scaling.
- Run-to-completion and scheduled work define idempotency, duplicate/missed execution, retry, deadline, concurrency, result, and retention semantics.
- Queue/event consumers define acknowledgement, visibility/lease, ordering, partition ownership, poison work, backlog, and replay before autoscaling.
- Stateful clustered workloads define identity, quorum, membership, fencing, storage topology, backup/restore, upgrade order, and disaster recovery beyond Pod identity.
- Scale-to-zero declares cold-start, buffering, deadline, burst, dependency, and minimum-capacity effects; zero replicas is not free or universally safe.
- Placement and disruption policies are feasible together and tested during rollout, maintenance, failure, and capacity shortage.
- Composite systems retain per-component archetypes and end-to-end ownership; they are not flattened into one misleading label.
- Archetype evolution includes consumer inventory, compatibility, migration, deprecation, and removal of obsolete variants.

### Common failures

Calling every process a microservice; selecting Deployment because it is familiar; assuming no local disk means stateless; using StatefulSet as a database operator; making a CronJob non-idempotent; assuming one scheduled execution exactly once; scaling consumers on CPU while backlog age explodes; scaling to zero a latency-critical service; using DaemonSet for one-per-zone rather than one-per-node; placing quorum members in one failure domain; making readiness depend on every optional dependency; applying one disruption budget to unlike components; mixing web, worker, and migration in one container; generating a template per team; and preserving obsolete archetypes because classification lacks consumer inventory.

### Compact example

An `orders` system is not assigned one archetype. Its request API is a stateless request-serving component with bounded concurrency, verified readiness, minimum replicas, zone spread, graceful drain, and latency SLO. Its queue consumer is an at-least-once event worker scaled by backlog age with acknowledgement after transactional effects, bounded retries, poison-message isolation, and scale-down drain. A nightly reconciliation is a scheduled run-to-completion component with missed-start policy, `Forbid` concurrency, idempotent operation key, deadline, checkpoint, and retained result. Schema migration is an on-demand singleton job with separate authority. The database is a managed dependency rather than mislabeled as application StatefulSet. One catalog system composes these profiles while each component receives a compatible path.

### Connections

Archetypes specialize the coherent minimum-platform boundary from [PLAT-040](040-designing-a-coherent-minimum-viable-platform.md) and reuse runtime, workload, scheduling, storage, configuration, deployment, connectivity, observability, and data-access foundations from [PLAT-021](021-container-images-as-platform-artifacts.md) through [PLAT-039](039-database-and-data-service-access.md). They drive the templates and golden paths in later modules without collapsing provider semantics into user-facing labels.

## Governing Question

What stable classification lets a platform say “this path safely supports your workload behavior” and justify its defaults, controllers, policies, tests, operations, and exclusions?

An archetype is a contract between application intent and platform capability. It compresses repeated decisions: whether work is request-driven or queued, indefinite or terminal, interchangeable or identity-bearing, horizontally scalable or partition-bound, restartable or checkpointed, latency-sensitive or throughput-oriented, and tolerant or intolerant of overlap and disruption.

The classification must remain useful when the underlying provider changes. “Deployment” is a Kubernetes implementation. “Stateless request service with bounded concurrency and graceful drain” is a durable behavior class that might later run on Kubernetes, a serverless service, virtual machines, or an edge runtime.

A small taxonomy improves consistency only when its boundaries are honest. If the platform hides unsupported state, ordering, hardware, network, or recovery requirements, teams inherit a deceptively easy path that fails under load or maintenance.

## Why This Matters

Defaults embody assumptions. A rolling update assumes old and new instances may overlap. Horizontal scaling assumes replicas can share work. Rescheduling assumes local execution state is disposable or recoverable. Readiness assumes traffic can move elsewhere. Retry assumes repetition is safe. The archetype makes these assumptions reviewable.

Incorrect classification creates coupled failures. A queue consumer scaled like a web server accumulates backlog. A stateful cluster spread like interchangeable replicas loses quorum. A scheduled job overlaps and double-bills customers. A node agent deployed once per cluster misses nodes. A scale-to-zero API violates its response-time objective.

Archetypes also control platform scope. Without them, teams request ad hoc knobs and the platform grows one template per application. With a requirements model, common differences become bounded profiles, rare needs become explicit exceptions, and repeated exceptions justify a new archetype.

Finally, the taxonomy creates a shared language among application, platform, security, reliability, data, and infrastructure owners. “Worker” becomes insufficient; the contract captures acknowledgement, ordering, replay, scale signal, shutdown, and result semantics.

## Prerequisites and Retrieval

Retrieve processes, threads, signals, graceful shutdown, stateless/stateful design, sessions, caches, durable storage, queues and event logs, acknowledgements and visibility leases, delivery and ordering semantics, idempotency, checkpoints, partitions, distributed consensus and quorum, batch and schedules, deadlines, concurrency, backpressure, horizontal/vertical/event scaling, resource requests/limits, accelerators, scheduling/affinity/topology, readiness/liveness/startup, disruption budgets, rolling/canary/blue-green delivery, schema migration, telemetry, SLOs, recovery objectives, security identity, secrets, cost, retention, and Kubernetes workload controllers.

You should distinguish process from workload; stateless process from stateless service; replica identity from business identity; local cache from authoritative state; request concurrency from replica count; queue depth from queue age; event delivery from effect uniqueness; Job completion from business outcome; schedule from exactly-once execution; controller restart from application recovery; Pod readiness from system availability; stable storage from correct membership; disruption budget from universal availability; and archetype from template or provider kind.

## Learning Objectives

After completing this module, you should be able to:

1. elicit a workload profile from operational behavior rather than implementation labels;
2. define a small versioned taxonomy with supported regions and non-guarantees;
3. distinguish request services, workers, batch, schedules, stateful clusters, node agents, and scale-to-zero profiles;
4. map profiles to Kubernetes and other provider resources without overclaiming semantics;
5. specify scaling, delivery, disruption, placement, state, and recovery requirements;
6. classify composite systems at component boundaries;
7. design archetype-specific defaults, validation, tests, status, and support;
8. govern exceptions and promote repeated needs into evidence-backed archetypes; and
9. evolve, migrate, and retire archetypes and their templates safely.

## Core Exposition

### Begin with behavior, not nouns

Names such as service, worker, app, daemon, task, pipeline, and database are too broad. Ask what triggers execution, how long it runs, how success ends, what may repeat, where state lives, whether instances are interchangeable, and what users expect during failure.

Observe production behavior and incident history. Repository structure or deployment YAML reveals current implementation, which may be accidental or wrong. Application owners supply domain and consistency needs; platform and reliability owners help translate them into runtime contracts.

Record uncertainty. “Probably idempotent” is not a safe retry contract. Mark unknown delivery, shutdown, storage, or recovery behavior as an admission blocker or time-bounded discovery item according to risk.

Classify components rather than whole business systems. An e-commerce system commonly combines request service, event consumer, scheduled job, migration task, frontend assets, and external stateful services.

### Write a workload profile

Capture owner, component/system identity, environments, criticality, data class, invocation source, lifetime, terminal result, concurrency, state and identity, dependencies, input/output, delivery/order, retry/idempotency, deadlines, resource shape, placement, availability, disruption, scaling signal and bounds, rollout, shutdown, telemetry, security, cost, backup/recovery, and retirement.

Separate mandatory requirements from preferences and current observations. “Needs GPU” is mandatory only when no supported CPU execution satisfies the outcome. “Runs five replicas” may be current capacity, not an invariant.

Include negative constraints: must not overlap, must not run in two regions, cannot lose local checkpoint, cannot receive traffic before cache warm-up, cannot retry after ambiguous external effect, cannot scale below quorum.

Bind the profile to evidence and revision. A profile can change when the application introduces sessions, partitioned consumption, persistent local state, new latency goals, or stronger recovery requirements.

### Define archetypes as supported regions

An archetype declares ranges and combinations the platform supports: invocation protocols, concurrency, duration, state class, replica model, scale signals and bounds, resource sizes, placements, delivery semantics, rollout strategies, security classes, observability, and recovery tiers.

Avoid a Cartesian explosion of names. Use a small base archetype with controlled profiles or traits only when combinations are tested. `request-service + gpu + stateful + singleton + scale-zero` is not automatically valid because each trait exists independently.

State exclusions and reasons. A request-service path might exclude raw host networking, stable replica identity, shared writable local disks, privileged containers, and unbounded requests. Link each unsupported need to an escape or review route.

Version archetype contracts independently of templates and provider adapters. Consumers should know which behavior revision they rely on and which changes require migration.

### Archetype: stateless request service

This archetype receives bounded synchronous requests through HTTP, RPC, or another request/response protocol and is expected to remain available. Replicas are interchangeable for routing after readiness and do not require stable ordinal identity.

“Stateless” means correctness does not depend on irreplaceable local or replica-affine state. In-memory caches, connection pools, and temporary files may exist if loss/reconstruction is safe. User sessions belong in signed client state or an external service unless explicitly affinity-bound with failure semantics.

Define per-request deadline, cancellation, concurrency, queue, overload, retry safety, health, graceful drain, and termination. Readiness should cover the ability to serve the advertised contract, not every optional dependency or the entire downstream graph.

Scaling signals may include concurrency, requests per second, latency-aware saturation, CPU, or custom load, with minimum/maximum capacity and stabilization. Average CPU alone can miss blocked IO, uneven work, or concurrency limits.

Default delivery favors rolling or progressive replacement with version compatibility, zone spread, disruption policy, baseline replicas, resource budgets, telemetry, and rollback. Old and new versions may overlap; the application and schemas must tolerate that.

### Archetype: asynchronous event or queue consumer

This archetype pulls or receives discrete work and produces effects without a caller waiting on the same connection. Its core contract is the relationship among assignment, acknowledgement, lease/visibility, retry, ordering, checkpoint, and side effects.

Assume duplicate delivery unless the broker and complete processing path prove otherwise. Acknowledge only at the point consistent with durable effects. Use idempotency keys, deduplication, transactional inbox/outbox, or domain reconciliation where repeated effects matter.

Define partition and ordering scope. Increasing replicas may not increase concurrency beyond partition count and can cause rebalances. Scale-down must release leases or ownership safely and allow in-flight work to finish or become visible again.

Backlog count is incomplete without arrival rate, service rate, item cost, and oldest age. A target such as acceptable drain time can relate backlog $B$, effective per-replica service rate $\mu$, and replicas $n$ through approximate drain time $T\approx B/(n\mu-\lambda)$ when service capacity exceeds arrival rate $\lambda$. Variability, partition limits, failures, and scaling delay make this a sizing model, not a guarantee.

Handle poison work with bounded retries and a governed quarantine/dead-letter process. A dead-letter queue is not resolution; it needs owner, alert, inspection access, replay semantics, retention, and privacy controls.

### Archetype: on-demand run-to-completion job

This archetype starts from an explicit request or event, performs a bounded task, and reaches terminal success or failure. Examples include migrations, exports, backfills, media transforms, model training, and administrative reconciliation.

Define input snapshot/reference, operation identity, deadline, parallelism, completion count, retry/backoff, per-shard failure, checkpoint, cancellation, output/result, logs, artifact retention, and cleanup. Container exit zero is evidence of process completion, not necessarily correct business output.

Kubernetes Job manages Pods to completion and supports fixed or indexed completions, backoff, failure policy, and parallelism. Recreated Pods mean work can repeat; the application still owns idempotency and external-effect correctness.

Distinguish singleton coordination from replica count. If only one migration may mutate a schema, use a durable lease/fencing mechanism and database authority, not merely `parallelism: 1`, because separate Job objects may overlap.

Large jobs need admission, quotas, priority, checkpoint/restart, data locality, and cost bounds. Avoid letting batch consume all interactive capacity.

### Archetype: scheduled run-to-completion job

This archetype adds schedule, time zone, missed-start, overlap, suspension, catch-up, and calendar semantics to a job. Schedules express when creation is attempted; they do not promise exactly-once execution or completion before the next interval.

Kubernetes CronJob creates Jobs on a repeating schedule and documents circumstances with missed or multiple starts. Work must be idempotent, and the contract should use scheduled execution identity or domain period as an operation key.

Choose overlap behavior deliberately: allow, forbid, or replace. `Forbid` may create missed work when a prior run is long; `Replace` may terminate work without safe checkpoint; `Allow` may duplicate or contend.

Define starting deadline and catch-up after controller outage, clock/time-zone behavior, maximum duration, business calendar, manual rerun, backfill range, and evidence of the period actually processed.

Alert on missed business outcomes, excessive duration, repeated failure, stale last success, and overlap—not just controller object creation.

### Archetype: stateful identity-bearing service

This archetype contains replicas whose identity, storage, membership, or ordering is not freely interchangeable. Examples include clustered brokers, consensus stores, and shard-bearing services when the organization intentionally operates them.

Kubernetes StatefulSet supplies stable ordinal/network/storage identity plus ordered or parallel management options. It does not implement database replication, quorum, membership, leader election, fencing, backup, repair, or safe version upgrade.

Define authoritative state, replication and consistency, quorum/failure domains, membership changes, stable identity, volume topology, fencing, bootstrap, scale procedures, upgrade/skew order, backup/restore, corruption repair, disaster recovery, and decommissioning.

Persistent volumes may outlive Pods and StatefulSets under retention behavior. Storage persistence is not backup, and rescheduling a volume is not proof the application recovered consistently.

Prefer a mature managed service or operator when it owns these domain protocols. A generic platform template should not turn a StatefulSet into an implicitly supported database.

### Archetype: node-local agent

This archetype runs on each eligible node because functionality must be colocated with that node: networking, storage, telemetry, security, device management, or host maintenance.

Kubernetes DaemonSet expresses one eligible Pod per node or subset, tracking node arrival and removal. It differs from a fixed replica service and does not mean one per zone, cluster, rack, or device unless selectors and provider behavior establish that mapping.

Define eligible nodes, host access, privileges, tolerations, criticality, resource reservations, update surge/unavailability, bootstrap dependency, shutdown, node drain, and behavior when the agent is absent or incompatible.

Node agents often have elevated trust and wide blast radius. Use signed artifacts, least host access, strong admission, staged node cohorts, rollback, and independent evidence.

Avoid application teams selecting this archetype merely to gain host privileges. It should have narrow admission and ownership.

### Archetype: continuously running singleton or leader

Some controllers, reconcilers, schedulers, and legacy processors require one active logical leader. A single replica reduces overlap but creates downtime and does not fence a paused or partitioned old instance.

Define leader election, lease authority, fencing token, failover delay, work resumption, checkpoint, duplicate action, and availability. Prefer multiple candidates with one fenced leader when uptime matters.

If effects cannot be idempotent or fenced, state the risk and operational recovery. Kubernetes replica count alone cannot prove a unique actor across network partitions, slow termination, or independent deployments.

Separate control-plane reconcilers from data-plane request paths. A leader outage may stop convergence without needing to stop already valid workloads.

### Archetype: scale-to-zero request or event handler

Scale-to-zero saves idle capacity for workloads whose demand and latency tolerate activation. It introduces cold start, image/config/secret fetch, placement, dependency warm-up, request buffering, burst, and control-plane availability into the response path.

Knative Serving can scale request workloads to zero and uses concurrency/scale bounds; its activator may queue traffic during activation. KEDA can scale supported resources from event-source signals. These mechanisms do not guarantee application deadlines or correct event effects.

Define maximum cold start, buffer capacity/time, activation signal freshness, burst upper bound, minimum/maximum scale, concurrency, downstream connection surge, scale-down drain, and behavior when the autoscaler or metrics path fails.

Never scale quorum members, latency-critical paths, non-replayable consumers, or components with expensive unsafe initialization to zero merely for utilization. A minimum replica may be the correct cost of an availability promise.

### Archetype: data-parallel or indexed computation

This archetype divides a finite input space into partitions or indexes processed concurrently, such as simulation, batch inference, rendering, or backfill. Each index needs deterministic ownership/result identity and bounded retry.

Define partition generation, skew, parallelism, per-index resource class, retry/failure threshold, speculative execution, checkpoint, aggregation, partial success, result manifest, and cleanup. One failed index may or may not invalidate the overall result.

Kubernetes Indexed Job can expose completion indexes and per-index status/failure behavior, but application data partitioning and output commit remain domain responsibilities.

Autoscaling parallelism is constrained by partitions, data locality, downstream quotas, and cost. More Pods can reduce throughput through contention.

### Archetype: static or client-distributed artifact

Some products build an immutable website bundle, mobile package, library, model, policy bundle, or configuration artifact rather than a long-running server. Treating them as Deployments adds an unnecessary runtime.

Define build/provenance/signing, target variants, publication, CDN/repository distribution, cache/invalidation, compatibility, rollout, rollback, revocation, usage/consumer discovery, and retention.

Client-distributed artifacts cannot be recalled instantly. Rollback may mean publishing a new version while old clients remain. Telemetry and support differ from centrally operated workloads.

This archetype often composes with a serving provider, but the durable product is the artifact and distribution contract, not a Pod.

### Treat stream processing as a specialized profile

Long-running stream processors combine queue consumption, partition ownership, checkpoints, state stores, event time, watermarks, rebalances, and recovery. They should not inherit a generic consumer path unless the platform supports those semantics.

Define source/sink guarantees, checkpoint consistency, state backend, partition rescaling, late/out-of-order data, replay, schema compatibility, savepoint/upgrade, and end-to-end effect semantics.

CPU or queue-depth scaling can conflict with partition assignment and checkpoint state. Prefer framework-aware operators or managed services when required.

Promote stream processing to a first-class archetype only when recurring demand justifies the provider, expertise, SLO, cost, and lifecycle burden; otherwise use an owned external path.

### Map profiles to controllers cautiously

Kubernetes documents Deployment for interchangeable stateless replicas, StatefulSet for sticky identity/storage, DaemonSet for node-local facilities, Job for one-off completion, and CronJob for repeated schedules. These are useful mappings, not application proofs.

Mapping logic should validate requirements before generating resources. A stable identity requirement may suggest StatefulSet, but a quorum store also requires a capable operator or managed service. A worker may use Deployment, StatefulSet, Job, or a custom resource depending on delivery and lifetime.

Record adapter revision and emitted provider resources. Status should project both archetype outcomes and provider details with provenance; do not reduce every failure to “Pod not ready.”

Test mappings against supported platform/provider versions and admission policy. A controller feature in current upstream documentation may be unavailable or configured differently in the actual fleet.

### Design archetype-specific health and lifecycle

Request-service readiness answers whether an instance should receive new requests. Consumer readiness may answer whether it can acquire partitions; during drain it should stop acquisition while completing or returning work. Job “health” is progress and terminal result, not permanent readiness.

Startup probes protect slow initialization from premature liveness restarts. Liveness should detect unrecoverable process failure, not downstream unavailability that a restart cannot repair.

Shutdown contracts differ: drain network requests, stop fetching queue items, checkpoint stream state, release leader leases, finish a batch shard, or flush a node buffer. Set grace from measured worst-case safe shutdown and enforce an upper bound.

Retention differs too. Services retain revision and operational history; jobs retain results/logs for investigation; schedules retain executions; stateful services retain backups and volumes; client artifacts retain supported versions and revocation evidence.

### Choose scaling signals from work

Apply Little's Law carefully: for stable system average concurrency $N$, throughput $\lambda$, and average time in system $W$, $N=\lambda W$. It relates population, rate, and duration under boundary/stability assumptions; it does not choose replicas or tail capacity automatically.

Request services often scale on concurrency or saturation tied to latency. Consumers scale on backlog age and service rate. Stream processors scale within partitions and checkpoint capability. Scheduled/batch work scales parallelism within deadlines and quotas. Node agents follow eligible nodes.

Set lower and upper bounds, ramp rates, stabilization, cooldown, readiness/startup effects, metric absence behavior, and dependency budgets. Autoscaling can overload databases, brokers, APIs, address pools, and secret/config systems.

Observe desired/current/ready capacity, pending/unschedulable instances, scale recommendation, metric timestamp, activation delay, saturation, queue age, throttling, and downstream impact.

### Match placement and disruption to semantics

Declare hard placement only for correctness, security, hardware, data locality, or licensed constraints. Use preferences for optimization when scarcity should not block the workload.

Spread replicas across meaningful failure domains, but ensure enough eligible capacity exists during surge and maintenance. Anti-affinity, topology spread, taints, volumes, GPUs, architecture, and policy combine; validate feasibility.

PodDisruptionBudget limits some voluntary evictions through the Eviction API. It cannot prevent involuntary loss, direct deletion, or controller rollout unavailability, and an overly strict budget can block node maintenance.

Stateful quorum and node agents need archetype-specific disruption calculations. A percentage default is not safe for every replica count or role.

Test node drain, zone loss, preemption, autoscaler removal, rolling update, stuck unready Pod, scarce hardware, volume-zone conflict, and control-plane delay.

### Compose archetypes at system boundaries

A catalog `System` may own many `Component` profiles. Preserve relationships, APIs, resources, data flows, owners, and SLO dependencies while keeping each controller contract bounded.

Coordinate version and schema compatibility across components. A request-service rollout may publish work consumed by old and new workers; a migration job may change a database used by both; a scheduled reconciler may repair missed events.

End-to-end reliability is not the minimum of green component readiness alone. Model queue backlog, data freshness, consistency, dependency budgets, and failure propagation.

Offer compositions as golden paths only after testing their interaction. Do not create a monolithic template that deploys every possible component.

### Build an admission questionnaire and classifier

Ask deterministic questions with evidence: Does it terminate? What invokes it? Can two instances process simultaneously? May work repeat? Is identity stable? What state survives replacement? What is the ordering scope? What signals demand? What is the deadline? What hardware/location is mandatory? What failure loses correctness?

Return candidate archetypes, matched facts, conflicts, unknowns, exclusions, and next actions. Allow human review; a classifier should not fabricate certainty.

Keep the logic versioned and test it with canonical profiles, boundary cases, and previously misclassified workloads. Explain every result so teams can correct the profile rather than game opaque policy.

Do not infer high-risk traits from repository scanning alone. Generated hints can prefill questions, but owners attest semantics and tests validate behavior.

### Govern defaults, exceptions, and new archetypes

For each archetype publish supported use cases, decision table, required fields, defaults, limits, provider mappings, security posture, examples, test suite, SLO/support, cost model, escape path, and deprecation policy.

An exception states the unmet dimension, why current archetypes fail, owner, provider, minimum security/telemetry/cost/lifecycle obligations, review date, and removal or promotion criterion.

Aggregate exception reasons and rejected profiles. Create a new archetype only when multiple durable users share behavior and the platform can own its full lifecycle—not because one team wants a different base image.

Merge or retire variants when their semantic distinction disappears. Too many near-identical archetypes increase decision, testing, support, and migration cost.

### Validate archetypes with behavior tests

Static tests validate required inputs and incompatible combinations. Render tests inspect provider resources. Integration tests create, update, scale, fail, recover, and delete a representative workload through the actual platform path.

Behavior tests inject duplicate events, partial effects, long requests, poison work, missed schedules, overlapping jobs, leader loss, node drain, zone failure, cold activation, metric staleness, checkpoint restore, and forced termination as applicable.

Test negative claims: a request path cannot request stable ordinals; a schedule without idempotency cannot use catch-up; a node agent cannot be admitted by an ordinary application role; a scale-zero profile cannot claim an incompatible latency objective.

Observe terminal business evidence, not only controller readiness. Synthetic fixtures do not prove production correctness, but they can reject contradictory mappings.

### Evolve profiles and consumers safely

Maintain inventory of archetype revision, adapter, template, provider resources, owners, exceptions, and last validation for every component. Detect manual drift and classification mismatch.

Additive optional fields can be compatible if defaults preserve semantics. Changing retry, rollout overlap, shutdown, identity, storage retention, or delivery semantics may require explicit migration.

Offer lint warnings, dry runs, compatibility reports, automated proposals, canaries, and rollback. Migrate representative low-risk consumers before fleet rollout.

Retirement requires no admitted or observed consumers, migrated provider resources, resolved exceptions, removed documentation/templates/classifier branches, and retained evidence according to policy.

The following executable inventory is synthetic classification evidence. It counts declared profile controls and does not prove application semantics, controller correctness, delivery guarantees, availability, recovery, or safe migration.

<!-- bijux-verify: {"id":"workload-archetype-profile-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"profiles 10\ninvocation_lifetime 10\nstate_identity 9\ndelivery_retry 8\nscaling_bounded 8\nplacement_disruption 8\nhealth_shutdown 8\nrecovery_tested 7\nobserved_owned 9\nretirement_owned 8\n","stderr":""}} -->
```python
profiles = [
    ("request-service", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("queue-consumer", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("on-demand-job", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("scheduled-job", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("stateful-service", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("node-agent", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("singleton-leader", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("scale-zero-handler", 1, 1, 1, 1, 1, 1, 0, 1, 1),
    ("indexed-computation", 1, 1, 0, 0, 0, 0, 0, 1, 0),
    ("legacy-mixed-process", 1, 0, 0, 0, 0, 0, 0, 0, 0),
]
fields = [
    "invocation_lifetime", "state_identity", "delivery_retry",
    "scaling_bounded", "placement_disruption", "health_shutdown",
    "recovery_tested", "observed_owned", "retirement_owned",
]
print("profiles", len(profiles))
for index, field in enumerate(fields, start=1):
    print(field, sum(row[index] for row in profiles))
```

## Definitions and Notation

For workload $w$, profile $P(w)=(I,L,S,C,A,Q,D,R,O,G)$ records invocation $I$, lifetime/termination $L$, state/identity $S$, concurrency $C$, availability/disruption $A$, scaling/queueing $Q$, delivery/retry $D$, resource/placement $R$, observability $O$, and governance/lifecycle $G$.

Each archetype $a$ defines supported set $\mathcal{S}_a$ over these dimensions plus required evidence and exclusions. Eligibility requires every mandatory coordinate and cross-dimension constraint of $P(w)$ to lie within $\mathcal{S}_a$; independent trait membership is insufficient when combinations conflict.

For queue backlog $B$, arrival rate $\lambda$, effective per-replica service rate $\mu$, and $n$ useful replicas, approximate drain time without new arrivals is $B/(n\mu)$; with stable continuing arrivals it is $T\approx B/(n\mu-\lambda)$ only when $n\mu>\lambda$ and boundary assumptions hold.

For a stable queueing boundary, Little's Law $N=\lambda W$ relates average population $N$, throughput $\lambda$, and average time $W$. It does not determine tail latency, replica count, or capacity under non-stationary overload.

Let archetype revision $a_v$, adapter revision $m_r$, desired workload revision $d$, and observed provider revision $o$ identify classification, mapping, requested state, and current evidence. Equality of resource kind does not imply equality of these contracts.

## Mechanisms, Invariants, or Proof Structure

The workload-archetype assurance chain is:

1. decompose a system into independently operated components and name owners/outcomes;
2. elicit invocation, lifetime, state, concurrency, delivery, scaling, placement, disruption, recovery, evidence, and lifecycle requirements;
3. separate mandatory facts, preferences, observations, and unknowns with evidence;
4. compare the complete profile and cross-dimension constraints to versioned archetype supported regions;
5. reject conflicts or route unsupported needs to composition, refinement, or an owned exception;
6. map an eligible archetype through a tested provider adapter without overclaiming application semantics;
7. apply archetype-specific defaults, policy, health, shutdown, delivery, scaling, rollout, status, and retention;
8. validate static mappings and observed behavior under success, failure, disruption, recovery, update, and deletion;
9. operate composite systems while preserving component profiles and end-to-end dependencies; and
10. inventory consumers, evolve compatibility, migrate revisions, promote repeated exceptions, and retire obsolete paths.

This chain does not prove owners described behavior correctly, the application is idempotent, a controller is defect-free, delivery is exactly once, state is recoverable, placement remains feasible, autoscaling meets an SLO, or a synthetic test represents production.

The invariants are behavior-derived taxonomy, evidence and uncertainty, explicit support/non-guarantees, semantics-before-controller, real interchangeability, terminal-work delivery contracts, queue semantics before scale, stateful domain protocols, explicit scale-zero effects, feasible placement/disruption, component-level composition, and governed evolution.

## Alternatives and Trade-Offs

**Few broad versus many narrow archetypes:** broad contracts reduce discovery and maintenance but need more controlled options and combination tests. Narrow contracts simplify defaults while multiplying choice, templates, support, and migrations.

**Base archetypes plus traits versus fixed profiles:** traits enable composition and reduce duplication, but independent traits can create invalid combinations. Fixed profiles are testable and clear but less flexible.

**Questionnaire versus automated inference:** owner questions capture intent but can be incomplete. Repository/runtime inference finds evidence but may encode accidental implementation; combine them with explainable review.

**Generic controllers versus framework operators:** generic resources are portable and familiar. Operators can own domain lifecycle such as quorum, checkpoints, or upgrades while adding privileged code, CRDs, version coupling, and operational burden.

**Long-running capacity versus scale to zero:** warm replicas improve latency and control-plane independence. Scale zero reduces idle cost while adding activation, buffering, burst, and cold-start risk.

**Managed state versus self-operated StatefulSet:** managed services reduce domain operations and may improve recovery. Self-operation offers control and portability at substantial expertise, reliability, security, and lifecycle cost.

**Strict admission versus permissive escape:** strict paths prevent contradictory configurations but can block legitimate novelty. Owned escapes preserve progress while retaining minimum obligations and demand evidence.

**Platform abstraction versus provider exposure:** abstractions stabilize user intent. Provider detail is still necessary for advanced constraints and diagnosis; use progressive disclosure rather than false uniformity.

## Failure Modes and Misconceptions

- **“Microservice is an archetype.”** it says little about invocation, state, delivery, scaling, or recovery.
- **“No disk means stateless.”** sessions, leases, partition ownership, and external side effects can make replicas non-interchangeable.
- **“Deployment is the default for everything.”** terminal, scheduled, node-local, identity-bearing, and specialized workloads need different semantics.
- **“StatefulSet operates databases.”** it supplies identity and storage mechanics, not database protocols.
- **“One replica means singleton.”** old and new instances can overlap or partition without fencing.
- **“Cron means exactly once.”** schedules may be missed or duplicated, and executions can overlap.
- **“A successful Job means the business result is correct.”** exit state does not validate output completeness or external effects.
- **“At-least-once plus deduplication is exactly once.”** deduplication scope, retention, races, and every effect boundary matter.
- **“Queue depth is enough for scaling.”** item age, arrival/service rate, partitions, cost, and poison work matter.
- **“CPU autoscaling matches demand.”** CPU can be unrelated or delayed and average utilization hides imbalance.
- **“Scale zero is only a cost choice.”** it changes latency, buffering, dependencies, and failure paths.
- **“PDB guarantees availability.”** it covers only some voluntary evictions and can block maintenance.
- **“Anti-affinity guarantees resilience.”** eligible capacity, topology meaning, storage, and correlated providers can defeat it.
- **“Readiness should check every dependency.”** optional/downstream failures can remove all serving capacity and amplify outages.
- **“One archetype per system.”** systems commonly compose components with different lifecycles.
- **“More archetypes show platform maturity.”** unsupported variants increase cognitive and operational load.
- **“The classifier can decide from code.”** runtime intent and domain effects require accountable evidence.
- **“An upstream feature is available everywhere.”** fleet version, gates, provider policy, and configuration determine support.

## Worked Examples

### Example 1

An API stores sessions only in local memory, yet is called stateless because it has no disk. Rolling replacement logs users out and horizontal routing loses sessions. External or client-bound session state makes replicas genuinely interchangeable. Conclusion: statelessness is a correctness property.

### Example 2

A payment consumer acknowledges before committing its effect and crashes. The message is lost. Acknowledgement after transactional/idempotent effect plus bounded replay aligns delivery. Conclusion: consumer archetypes begin with effect semantics.

### Example 3

A nightly CronJob sometimes starts twice and charges accounts twice. Period identity, unique operation keys, idempotent writes, overlap policy, and outcome reconciliation contain duplication. Conclusion: schedules do not promise exactly once.

### Example 4

A three-member store uses StatefulSet but all volumes and Pods occupy one zone. Zone loss removes quorum. Membership-aware topology, storage placement, disruption calculations, backup, and recovery tests are added. Conclusion: sticky identity is not resilience.

### Example 5

A node telemetry agent runs as a three-replica Deployment, leaving some nodes uncovered and duplicating others. A narrowly privileged DaemonSet targets eligible nodes with staged updates. Conclusion: placement semantics choose the controller.

### Example 6

A queue worker scales on CPU while messages wait for hours because it is IO-bound. Backlog age, arrival/service rate, partition count, scale delay, and downstream budgets drive bounded scaling. Conclusion: scale on work, not convenience.

### Example 7

A latency-critical authorization endpoint scales to zero overnight; the first request exceeds its deadline while fetching image, secrets, and connections. A warm minimum and capacity reserve preserve the SLO. Conclusion: idle cost cannot erase activation latency.

### Example 8

A singleton reconciler runs one replica, but a partitioned old Pod continues writing after replacement. Lease plus monotonically increasing fencing token makes the provider reject stale writers. Conclusion: replica count is not uniqueness.

### Example 9

A data-parallel job launches 1,000 Pods for 40 partitions and overwhelms its object store. Indexed ownership, bounded parallelism, per-index retries, checkpoints, and provider quotas improve progress. Conclusion: maximum parallelism is not maximum throughput.

### Example 10

A business system is assigned “web service,” so its migrations and workers share the same rollout and identity. Splitting request, consumer, schedule, and migration profiles enables compatible independent operations. Conclusion: classify components, then compose systems.

## Cross-Program Connections

- **Operating Systems:** processes, signals, daemons, scheduling, resources, isolation, and termination underpin runtime behavior.
- **Distributed Systems:** leases, fencing, consensus, partitions, delivery, ordering, idempotency, and recovery define non-interchangeable work.
- **Data Structures and Algorithms:** queues, priority, partitioning, work stealing, backoff, and scheduling affect throughput and fairness.
- **Database Systems:** state, transactions, replication, checkpoints, migrations, and recovery distinguish managed dependencies from generic Pods.
- **Data Engineering:** batch, stream, watermark, replay, backfill, schema, lineage, and freshness produce specialized profiles.
- **Reliability Engineering:** SLOs, overload, disruption, graceful degradation, recovery objectives, and incident testing constrain defaults.
- **Computer Security:** workload identity, privilege, host access, secrets, supply chain, tenant boundaries, and audit govern admission.
- **Cloud Economics:** warm capacity, scale zero, scarce accelerators, managed services, storage retention, and parallelism shape cost.
- **Software Engineering:** modular component boundaries, compatibility, contracts, testability, and ownership enable safe composition.

## References

1. Kubernetes, “Workload Management,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/
2. Kubernetes, “Deployments,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
3. Kubernetes, “StatefulSets,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
4. Kubernetes, “DaemonSet,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
5. Kubernetes, “Jobs,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/job/
6. Kubernetes, “CronJob,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
7. Kubernetes, “Horizontal Pod Autoscaling,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
8. Kubernetes, “Disruptions,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
9. KEDA, “Scaling Deployments, StatefulSets and Custom Resources,” version 2.20 documentation, retrieved 2026-09-02. https://keda.sh/docs/2.20/concepts/scaling-deployments/
10. Knative, “Autoscaling,” current Serving documentation, retrieved 2026-09-02. https://knative.dev/docs/serving/autoscaling/
11. Knative, “Serving Architecture,” current documentation, retrieved 2026-09-02. https://knative.dev/docs/serving/architecture/
12. CNCF TAG App Delivery, “CNCF Platforms White Paper,” current edition, retrieved 2026-09-02. https://tag-app-delivery.cncf.io/whitepapers/platforms/
13. Backstage Project, “System Model,” current documentation, retrieved 2026-09-02. https://backstage.io/docs/features/software-catalog/system-model/

## Exercises

### Exercise 1

Define workload, workload profile, archetype, controller mapping, replica, run to completion, delivery semantics, scaling signal, disruption tolerance, composite workload, and supported region. State one non-guarantee for each.

### Exercise 2

Profile an order-processing system containing HTTP API, queue consumer, scheduled reconciliation, schema migration, and database. Classify each component and define invocation, lifetime, state, delivery, scaling, placement, disruption, health, recovery, observability, and lifecycle.

### Exercise 3

A platform deploys every component with Deployment, calls no-disk processes stateless, scales all on CPU, treats one replica as a singleton, runs non-idempotent CronJobs, assumes StatefulSet protects databases, applies the same readiness/PDB, and enables scale zero globally. Diagnose at least fifteen failures and correct the taxonomy and mappings.

### Exercise 4

Design archetypes for a multi-tenant analytics platform containing interactive APIs, Kafka consumers, periodic reports, large indexed backfills, GPU model training, stream processors with checkpoints, node telemetry, and managed databases. Keep the taxonomy small while preserving material distinctions and escape paths.

### Exercise 5

An organization must replace its Kubernetes provider and reduce twelve historical workload templates to a durable archetype set. Design discovery, classification evidence, contract and adapter boundaries, compatibility tests, canaries, migration, exception handling, rollback, and proof for retiring old templates/resources.

## Answers to the Exercises

### Answer 1

A workload is software and its complete runtime/lifecycle context but does not reveal correct behavior automatically. A profile declares dimensional requirements but owner claims may be incomplete. An archetype contracts recurring supported behavior but cannot fit every combination. A controller mapping translates a contract to provider resources but does not prove application semantics. A replica is a managed instance but may not be interchangeable. Run to completion has terminal process semantics but exit success does not prove business correctness. Delivery semantics describe repetition/loss bounds but end-to-end effects require every boundary. A scaling signal measures demand but can be stale, biased, or causally weak. Disruption tolerance declares safe loss/overlap but cannot prevent involuntary failure. A composite workload joins components but component health does not prove system outcome. A supported region describes validated combinations but cannot guarantee provider capacity or production correctness.

### Answer 2

The HTTP API is a stateless request service only if sessions and authoritative state are external; it declares request deadlines/cancellation, bounded concurrency/queue, minimum and maximum replicas, readiness, zone spread, graceful drain, rollout overlap, latency/error SLO, and rollback. The queue consumer is an at-least-once asynchronous worker with partition/order scope, acknowledgement after transactional effect, idempotency key, visibility lease, bounded retry/dead-letter ownership, backlog-age scaling capped by partitions/downstream capacity, acquisition stop and drain, lag/effect telemetry, replay, and reconciliation. Scheduled reconciliation is a CronJob-mapped terminal profile with period operation key, missed-start deadline, `Forbid` or deliberately allowed overlap, idempotency, duration, manual backfill, retained results, and stale-last-success alert. Schema migration is an on-demand singleton Job with separate identity, fenced lease, lock/load budget, checkpoint, expand-contract compatibility, audit, and roll-forward/rollback boundary. The database is a managed data-service dependency with its own access, consistency, backup, failover, and recovery contract—not an application archetype forced into a StatefulSet. Catalog relationships compose owners, APIs, resources, revisions, SLOs, and retirement.

### Answer 3

Deployment cannot express terminal completion, schedules, per-node placement, or sticky identity; map by behavior to Job, CronJob, DaemonSet, StatefulSet/operator, or external provider. No disk does not prove statelessness because sessions, leases, in-memory authoritative state, partitions, and side effects can bind identity; test replacement, overlap, and horizontal routing. CPU may not represent request concurrency, queue age, partitions, deadlines, or IO saturation; choose per-archetype signals and bounds. One replica allows overlap during partitions, rollouts, or slow shutdown; use leader election and fencing. CronJobs can miss, duplicate, and overlap; use period keys, idempotency, starting deadlines, concurrency policy, backfill, and outcome reconciliation. StatefulSet supplies identity/storage, not replication, quorum, backup, repair, or upgrades; use a domain operator/managed service and recovery tests. Uniform readiness can amplify dependency failure or misrepresent Jobs/consumers; define archetype health and drain. Uniform PDB can block maintenance or fail quorum; calculate disruption and remember PDB limitations. Global scale zero violates cold-start and control-plane-independent requirements, creates connection bursts, and is unsafe for quorum or non-replayable work; admit only compatible profiles. Further corrections include delivery/ack semantics, poison work, storage retention, placement feasibility, shutdown grace, rollout compatibility, output validation, telemetry, security admission, cost, composite boundaries, and exceptions.

### Answer 4

Use five base archetypes plus controlled profiles: request service; asynchronous partitioned consumer; terminal job with on-demand/scheduled/indexed profiles; stateful stream processor as a specialized governed path; and node-local agent. Interactive APIs use request concurrency, warm minimums, zone spread, graceful drain, and latency SLO. Kafka consumers use partition/ack/checkpoint/order/rebalance semantics and lag/oldest-age scaling within partition/downstream bounds. Reports are scheduled terminal jobs with period keys, overlap/catch-up/deadline/result retention. Backfills and GPU training use indexed terminal profiles with resource class, quota, placement, checkpoints, per-index failure, result manifests, and cost; GPU is a constrained resource profile rather than a separate lifecycle archetype. Stream processors require framework-aware checkpoints/savepoints, state backend, watermarks, partition rescaling, replay, and upgrade path; promote only if recurring support justifies it. Node telemetry uses narrowly privileged eligible-node placement and staged updates. Databases remain managed resource dependencies. Trait combinations are admitted only when tested; unusual hardware, framework, or state uses an owned external path with identity, security, telemetry, cost, recovery, and expiry obligations.

### Answer 5

Inventory every component, owner, old template/version, provider resource, invocation, lifetime, state, identity, delivery, scale, placement, disruption, health, rollout, recovery, evidence, and exception. Observe runtime and incidents while asking owners to attest intent; mark contradictions and unknown high-risk dimensions. Cluster profiles by durable behavior, producing a small versioned archetype contract set independent of Kubernetes kinds. Implement old and new provider adapters behind the same identity, desired/observed revision, operation/status, policy, and lifecycle API; expose provider-specific constraints without changing archetype meaning. Build canonical and adversarial behavior fixtures for replacement/overlap, retry/duplicates, schedule miss/overlap, leader fencing, state restore, node placement, cold activation, scaling, drain, disruption, update, and deletion. Dry-run mappings and capacity, then canary low-risk consumers per archetype while comparing outcome/SLO, status, security, cost, and recovery. Unsupported profiles receive owned time-bounded exceptions rather than coercion. Rollback retains the prior adapter and compatible desired state during the evidence window. Retirement requires all consumers classified and migrated, no old operations or resources, residual volumes/identities/secrets handled, old templates/classifier rules/docs removed, negative creation tests passing, and retained audit/migration evidence.
