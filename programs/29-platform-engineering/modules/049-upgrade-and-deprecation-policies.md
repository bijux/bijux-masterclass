---
module_id: PLAT-049
program: Platform Engineering
level: 1
module_number: 49
title: Upgrade and Deprecation Policies
status: complete
last_verified: 2026-09-02
---

# Upgrade and Deprecation Policies

## One-Page Review

### Governing question

How should a platform operate upgrades and deprecations across control planes, capabilities, templates, runtimes, policies, data, and consumer-owned workloads so change remains compatible where promised, urgent risk is reduced, migrations receive real capacity, and obsolete surfaces are actually retired?

### Essential definitions

- An **upgrade policy** defines supported starting states, targets, prerequisites, order, compatibility, rollout, verification, recovery, ownership, and deadlines for moving a fleet.
- A **deprecation** is an advance support-state transition announcing that a surface is discouraged and scheduled for later removal; it is not removal itself.
- A **removal** makes a formerly available surface unavailable or invalid after its declared gates are satisfied or an explicit emergency decision overrides them.
- A **support window** is the period and release set for which an owner provides named fixes, security response, compatibility, documentation, and migration help.
- **version skew** is the supported difference among simultaneously interacting component or contract revisions.
- A **migration wave** is a bounded cohort moved under common prerequisites, observation, stop conditions, and support.
- A **compatibility dimension** is a distinct preservation question—source, wire, semantic, operational, data, security, workflow, or evidence.
- A **removal gate** is a mandatory, evidenced condition such as successor readiness, consumer reconciliation, data conversion, expired exceptions, or tested recovery.
- **forward recovery** restores a valid state using a newer repair when rollback would violate changed data, external effects, trust, or policy.
- **retirement** removes the old implementation, authority, state, tooling, documentation, evidence flows, and support obligation—not merely its catalog entry.

### Central model, mechanism, or theorem

Represent supported revisions as a directed transition graph $G=(V,E)$; edge $(u,v)\in E$ exists only when moving from $u$ to $v$ has owned prerequisites, procedure, compatibility evidence, outcome checks, and recovery. A target is reachable only through a tested directed path, so “both versions are supported” does not prove direct upgradeability. For $N$ remaining consumers and verified migration throughput $\mu>0$ consumers per week, the no-arrival lower bound is $T\geq N/\mu$ weeks; deadlines shorter than $T$ require more capacity, reduced scope, accepted risk, or an honest break—not optimistic communication.

### Critical invariants

- Every governed surface has stable identity, owner, support state, consumers, dependencies, upstream constraints, evidence, and retirement condition.
- Version numbers and channels communicate declared promises; higher or “latest” never means inherently compatible, safe, or appropriate.
- Changes are classified across all compatibility dimensions and workload outcomes, including defaults, limits, error semantics, policy, telemetry, and human workflow.
- The compatibility/skew graph records tested directed transitions and mixed states; unsupported edges fail before production change.
- Inventory reconciles source, desired state, runtime, stored data, observed use, ownership, exceptions, and unreachable/unknown consumers.
- Upgrades are reviewable, immutable, progressively delivered operations with terminal outcome evidence and explicit points of irreversibility.
- Consumer-owned changes are preserved; automation proposes or performs only within delegated authority and stops on ambiguous conflicts.
- Deprecation names scope, reason, replacement, earliest removal, criteria, migration, warnings, support, owner, telemetry, and exception process.
- Migration work is funded and capacity-checked; announcing a date without a viable successor and throughput is not a policy.
- Rollback claims include data, external effects, identity, trust, policy, provider state, and old-reader compatibility; otherwise forward recovery is planned.
- Security and safety emergencies may compress compatibility windows through explicit authority, affected inventory, evidence, compensating controls, support, and retrospective.
- Removal and retirement require negative evidence that old use, authority, data, code paths, and consumers are absent or governed.

### Common failures

Equating package release with fleet upgrade; auto-following `latest`; moving immutable tags; relying on SemVer without declaring a public contract; treating additive schemas or new enum values as universally compatible; testing only latest-to-latest; assuming compatibility is symmetric or transitive; skipping supported intermediate versions; upgrading control plane and data plane in arbitrary order; reading repository manifests while ignoring deployed artifacts; treating absent telemetry as absent consumers; opening automated pull requests without migration ownership; declaring deprecation after upstream support ends; choosing a removal date without migration capacity; offering an untested replacement; keeping exceptions forever; calling old-image redeployment rollback after irreversible data or trust changes; removing an API while stored objects, offline tools, alerts, or disaster-recovery scripts still depend on it; and deleting documentation while credentials, controllers, policies, and support burden remain.

### Compact example

A platform must move 120 workloads from runtime profile 3 to 5 before profile 3 loses upstream security support in 16 weeks. The graph has tested edges 3→4 and 4→5 but no 3→5 edge; mixed runtime/library/telemetry states are bounded. Inventory reconciles deployed digests, repositories, owners, data migrations, scheduled/offline jobs, and exceptions. Pilot throughput is six verified workloads per week, so $T\geq120/6=20$ weeks before failures and new discoveries. The owner adds migration staff and automation, prioritizes internet-facing workloads, negotiates a narrow four-week maintenance extension for low-risk consumers, and stops new profile-3 admission. Each wave uses reviewable changes, canaries, outcome/security evidence, and forward recovery after schema contraction. Removal waits for zero supported consumers, converted stored state, expired exceptions, tested disaster recovery, and deletion of builders, images, policies, credentials, caches, docs, and alerts.

### Connections

This module operationalizes the contract identities from [PLAT-019](019-golden-path-versioning.md), configuration migrations from [PLAT-035](035-configuration-management.md), workload standards from [PLAT-041](041-workload-archetypes.md) through [PLAT-048](048-security-and-compliance-defaults.md), and lifecycle obligations of every earlier platform capability. PLAT-050 uses these policies to keep a golden path attractive without trapping consumers.

## Governing Question

What policy turns a published platform change into a safe, supportable transition of real consumers and state—and turns deprecation into verified retirement rather than permanent warning noise?

Release production and fleet transition are different systems. A platform team can publish a new runtime, policy bundle, controller, provider adapter, CLI, or template in minutes. Consumers may need source changes, data conversion, approval, performance tests, maintenance windows, staff time, or vendor coordination. Declaring the release “available” does not move them.

Change also occurs on many clocks. Upstreams end support, vulnerabilities demand patches, providers remove APIs, certificates and algorithms expire, product teams plan releases, regulated changes need evidence, and platform teams have finite support capacity. A useful policy coordinates these constraints rather than announcing one universal “upgrade day.”

Deprecation earns trust only when its successor works, affected users are found, the migration journey is supported, and removal criteria are credible. Repeated warnings without removal teach users to ignore warnings; removal without support teaches them to avoid the platform.

## Why This Matters

Platforms concentrate dependencies. One control-plane upgrade can affect thousands of workloads; one obsolete plugin can prevent the next cluster version; one runtime baseline can carry a vulnerability into every generated service. Concentration provides leverage only when change propagation is engineered.

Compatibility is multidimensional. Wire bytes can remain readable while a new default changes public exposure, a new enum crashes an exhaustive client, a policy rejects recovery, a metric rename blinds alerts, or increased latency exhausts a deadline. Package-manager resolution cannot validate these semantics.

Support matrices create real cost. Every retained release adds build infrastructure, patching, tests, documentation, incident expertise, security response, providers, credentials, and exceptions. Removing too quickly transfers unplanned toil and risk to product teams; retaining forever freezes the platform. Policy makes this trade visible.

Incomplete retirement becomes latent failure. An old API may appear unused until disaster recovery replays stored objects or a quarterly job runs. An old trust root may remain an attack path. A deleted template may leave 400 independent copies. Negative evidence and lifecycle cleanup matter most at the long tail.

## Prerequisites and Retrieval

Retrieve public contracts, semantic/calendar/major versioning, immutable artifacts, stability channels, compatibility dimensions, dependency resolution and lock files, schemas and data migration, distributed mixed-version deployment, controllers and reconciliation, Kubernetes release/deprecation/skew, feature flags, progressive delivery, canaries, SLOs/error budgets, backup/restore, forward and backward compatibility, expand/contract, security patching and disclosure, supply-chain provenance, consumer inventory, templates and generated code, ownership, product communication, support models, change management, exceptions, telemetry, capacity/queueing, incident response, and decommissioning.

You should distinguish release from adoption; version order from transition reachability; compatibility from successful parsing; backward from forward compatibility; coexistence from arbitrary skew; deprecation from removal; removal from retirement; warning delivery from migration completion; repository declaration from runtime fact; no observed use from proven absence; update automation from authorization; rollback from restoration or forward recovery; exception from normal support; upstream support from platform support; and deadline from capacity-backed forecast.

## Learning Objectives

After completing this module, you should be able to:

1. inventory and classify platform surfaces, consumers, dependencies, support states, and upstream constraints;
2. analyze source, wire, semantic, operational, data, security, workflow, and evidence compatibility;
3. model tested upgrade/skew paths as a directed graph and derive safe ordering from dependencies;
4. define stability channels, support windows, patch policies, deadlines, and service obligations;
5. design reviewable upgrade plans, migration waves, canaries, stop conditions, and terminal evidence;
6. choose rollback, forward recovery, coexistence, adapter, quarantine, or restore/cutover based on reversibility;
7. publish actionable deprecations through machine and human channels without treating warnings as completion;
8. capacity-plan migrations, handle exceptions and emergencies, and support brownfield/unknown consumers; and
9. prove removal readiness and retire code, state, authority, evidence, and support surfaces.

## Core Exposition

### Define the governed surface inventory

Inventory capability APIs/resources, CLIs, SDKs/libraries, portal flows, templates/generated files, reusable workflows, runtime profiles, base/build images, controllers/operators, policy bundles, configuration and secret schemas, telemetry schemas, providers, clusters/nodes, data formats, identities/trust roots, documentation, and support channels.

For each surface record stable identifier and immutable revisions, public contract, owner/on-call, upstream/source, support channel and dates, compatible dependencies, consumers, stored state, security status, evidence, update mechanism, exception policy, replacement, and retirement condition.

Separate interface identity from implementation identity. A compatible server deployment may change digest without changing API version; a default behavior change may require contract communication even if the server package version barely changes. An umbrella platform release can name a tested bill of materials but does not erase component versions.

Discover authoritative state from APIs, deployed digests, provenance, package locks, resource storage versions, controller status, cloud/provider inventories, repositories, catalog ownership, access logs, and support records. Reconcile disagreements rather than choosing the freshest-looking source.

### Define support as an explicit service

Use a small channel set such as experimental, preview, recommended, supported, maintenance, deprecated, and retired. For each, state admission for new use, compatibility promise, patch/security policy, incident response, availability/evidence expectations, data constraints, migration obligation, maximum duration, and removal rule.

Recommended is the default for new work; supported may include other viable revisions. Maintenance accepts limited fixes while migration is underway. Deprecated still functions within its stated window but stops new adoption. Retired has no ordinary supported path.

Platform support can be shorter than upstream support if integration, expertise, providers, or tests are absent. It cannot safely be longer unless the organization owns backports, builds, security analysis, and operations. Publish both timelines and the limiting dependency.

Do not make preview a loophole for permanent critical production state. Consequence creates obligations regardless of label. Either strengthen the channel or constrain its data, authority, duration, and recovery.

### Classify every change before scheduling it

Describe current and target behavior and enumerate affected contracts. Classify change as compatible, conditionally compatible, incompatible, security/safety urgent, or evidence-only for each dimension.

**Source** asks whether code/configuration still builds or validates. **Wire** asks whether old/new participants encode and decode safely. **Semantic** asks whether meaning, defaults, errors, ordering, and idempotency remain. **Operational** covers latency, load, availability, resources, rate limits, scaling, and recovery. **Data** covers stored versions, conversion, replay, retention, and downgrade.

**Security** covers identities, permissions, trust roots, algorithms, secrets, exposure, audit, and threat assumptions. **Workflow** covers steps, approvals, automation, diagnostics, and ownership. **Evidence** covers metrics/logs/traces/status/compliance meaning and historical continuity.

“Additive” is local syntax, not a universal conclusion. New response fields can overflow buffers, new enum values can break exhaustive clients, new labels can explode cardinality, and new defaults can alter security or cost.

### Model transitions and skew as a directed graph

Let revisions be vertices $V$. Add directed edge $(u,v)$ only when the exact transition has documented prerequisites, implementation, test evidence, success checks, recovery, and support. Direction matters: upgrading 3→4 may be safe while downgrading 4→3 loses data. Reachability is not transitive evidence; tested 3→4 and 4→5 provides an owned path, not proof of direct 3→5.

Represent interacting components as supported tuple set $\Omega$. Include old/new client-server, control-plane/node, controller/resource schema, producer-consumer, binary/data, library/runtime, policy/resource, telemetry producer/query, and provider/adapter versions.

Kubernetes publishes concrete skew and upgrade ordering across API servers, controllers, kubelets, proxies, and clients. Its current policy illustrates why the oldest highly available API server can narrow allowed component versions and why components are upgraded in order. Copy the reasoning discipline, not version counts that may differ for your distribution.

Reject unsupported tuples before change. “It starts” is not support evidence. Record known-but-untested combinations as unknown rather than compatible.

### Derive upgrade order from dependency and reversibility

Build a dependency graph over identity/trust, control plane, admission/policy, providers, controllers, schemas/storage, runtimes/libraries, workload code, telemetry consumers, and cleanup. A target component moves only when predecessors can tolerate both current and target states.

Use expand/migrate/contract for shared contracts. Add new representation and dual compatibility; migrate producers/consumers/state while measuring both; remove the old representation only after all supported dependents and rollback readers retire.

For trust-root or credential rotation, distribute new trust, issue new credentials, verify adoption, revoke old authority, and test recovery. For event/data schema changes, account for retained messages, backups, replay, CDC, and offline readers. For policy tightening, ensure workloads and emergency actions validate before enforcement.

Mark irreversible edges: destructive data conversion, external notification, resource deletion, provider cutover, trust revocation, billing effect, or consumer-visible event. Move the recovery strategy from rollback to forward fix, restore elsewhere, compatibility adapter, traffic shift, or quarantine at that point.

### Write the upgrade plan as an operation

An upgrade plan names change ID, owner/approvers, reason, current/target immutable identities, affected scope, prerequisites, compatibility findings, transition/skew edges, ordering, cohorts, schedule, capacity, automated/manual actions, data changes, security implications, expected outcomes, telemetry, stop thresholds, rollback/forward recovery, irreversibility, communication, support, and completion criteria.

Bind execution to reviewed identities. Never approve `latest`, mutable branches, or unresolved dependency ranges for a fleet change. Record build/provenance and effective configuration/policy.

Make every attempt idempotent or reconcilable. A timeout after provider change can leave unknown state; query by durable operation/resource identity before retry. Persist per-consumer desired and observed revision, conditions, errors, last attempt, next action, and terminal evidence.

Completion is a verified consumer/workload outcome: correct build, deployment, data invariant, health, service behavior, security posture, telemetry/evidence, and support state. Package installation alone is intermediate state.

### Segment consumers into migration waves

Choose waves by risk and learning: internal fixtures, platform-owned workloads, opt-in partners, low-consequence production, representative typical services, high-scale/stateful/regulated workloads, and long-tail exceptions. Do not leave every difficult workload until the final week; sample hard archetypes early.

Each wave has entry prerequisites, maximum size/blast radius, observation interval, outcome and guardrail metrics, support staffing, stop/rollback authority, and exit evidence. Account for correlated failure: ten workloads sharing one database or tenant are not ten independent canaries.

Compare outcomes before/after, not merely deployment health. Observe user-facing SLOs, correctness, data invariants, resource/cost change, security policy, telemetry continuity, support volume, and recovery.

Pause automatically for unambiguous harm; route ambiguous business trade-offs to an accountable owner. A rollout controller cannot decide that a 5% latency increase is acceptable for a critical settlement workflow without policy.

### Capacity-plan the migration program

Inventory remaining consumers $N$, verified throughput $\mu$, failure/rework rate, staff/support capacity, blackout periods, approvals, and new arrivals. With no arrivals and constant throughput, $T\geq N/\mu$. Real schedules require contingency for unknowns, blocked owners, failures, and changing scope.

Forecast by archetype/risk rather than using one average. A stateless library update and a regulated stateful migration do not consume equal capacity. Maintain work-in-progress limits so support and incident response do not collapse.

When deadline precedes plausible completion, change a real variable: add automation and people, reduce supported scope, provide a compatible adapter, negotiate upstream/provider extension, isolate risk, revise deadline, or explicitly accept/break. Do not hide the gap in “teams notified.”

Allocate migration work in roadmaps and service objectives. Platform-caused migrations are product work, not free labor available whenever the platform ships.

### Automate updates within delegated authority

Dependency bots can discover versions and prepare pull requests; template updaters can compute old template, local modifications, and new template; reconcilers can move managed resources. Each mechanism needs permissions, pinned tooling, provenance, rate limits, grouping, tests, owner routing, conflict behavior, and rollback.

Automatic proposal is safer than automatic production merge when consumer-owned code or semantics change. Auto-merge may be appropriate for bounded compatible patches with passing representative tests, low blast radius, and fast rollback; define the exact class.

Never overwrite local changes to make the fleet appear current. If generated code has transferred ownership, merge conflicts and semantic differences require product review. Move truly platform-owned behavior into versioned libraries/workflows/controllers so it can be updated without copying.

Prevent pull-request floods. Group compatible updates, limit concurrency, prioritize security and expiring support, and close/supersede obsolete proposals. Measure verified adoption, not PR count.

### Migrate data and durable state explicitly

Inventory storage schema, resource storage versions, indexes, caches, queues/events, backups, replicas, derived data, encryption/key versions, and offline/recovery readers. Define invariants such as row counts, balances, uniqueness, referential integrity, checksums, order, privacy, and application outcomes.

Use online expand/backfill/dual-read or write/verify/contract where semantics permit. Backfills are production workloads: checkpoint, rate-limit, prioritize foreground traffic, handle retries/idempotency, observe lag/errors, and reconcile omissions.

Snapshots provide recovery inputs only when restoration, compatibility, time, capacity, and business invariants are tested. A backup written by version 5 may not be readable by version 3.

Retained events and disaster-recovery archives extend compatibility windows. Removing a reader because live traffic is migrated can break replay during the next incident.

### Upgrade control planes and providers safely

Treat managed services as shared stateful systems. Check provider release notes and deadlines, version skew, quotas/capacity, APIs, plugins/drivers, admission webhooks, CRDs/conversion, network/storage behavior, node images, and workload disruption budgets.

Qualify target versions in representative environments with production-like scale and policy. Preflight every cluster/account/tenant; drift makes nominally equal environments different. Upgrade highly available components under documented skew and prove quorum/control reconciliation.

Canary nodes or clusters with representative workloads before broad rollout. Test scheduling, networking, DNS, storage attach/mount, identity, secrets, policy, telemetry, autoscaling, disruption, backup/restore, and emergency access.

Provider rollback may be unavailable. Plan restore into a new resource, traffic/data cutover, or forward repair; record provider authority, support escalation, and point of no return.

### Publish an actionable deprecation contract

Deprecation notice includes stable surface/version, status change date, reason and risk, affected behavior, replacement and its stability, migration guide/tool, compatibility window, warnings, earliest removal date, objective removal gates, support/contact, owner, telemetry, exception process, and later updates.

RFC 9745 defines an HTTP `Deprecation` response header and RFC 8594 defines `Sunset` plus a link relation for sunset information. These signals can help HTTP consumers but do not replace direct inventory, documentation, ownership, or non-HTTP channels.

Emit warnings at use and authoring boundaries: API responses/audit, CLI stderr, compiler/linter, schema validation, portal/catalog, CI, admission, dashboards, and direct owner notification. Warnings must be machine-readable enough to route and deduplicate, with replacement/date/link.

Rate-limit repeated warnings without making them invisible. A warning on every high-volume request becomes noise/cost; aggregated unique consumer/surface evidence can preserve actionability.

### Build a truthful consumer inventory

Combine declared dependencies with observed use and runtime/storage facts. Repositories can be archived while deployments remain; downloads may not be live use; telemetry may be sampled or blocked; offline tools and disaster-recovery scripts may run rarely; dynamic reflection/proxies can hide versions.

Record consumer identity, owner/on-call, environments, deployed and desired versions, last verified use, stored data, workload/risk class, migration state, blockers, exception, deadline, and evidence source/freshness.

Use states such as unknown, assessed, ready, migrating, verification-failed, blocked, verified, excepted, unreachable, and retired. “Notification sent” is not a migration state.

Confirm high-consequence consumers directly and exercise rare paths. Treat unowned/unreachable consumers as risks requiring escalation, containment, or retirement—not as zero use.

### Define removal gates and negative evidence

Before removal, require a stable supported successor; migration behavior/tools/docs/support; reconciled authoritative inventory; zero supported consumers on old surface or approved unexpired exceptions; compatible/converted stored data and backups; tested recovery/DR; telemetry and compliance continuity; security approval; and staffed incident plan.

Negative evidence is bounded. Show no old API calls, artifacts, runtime processes, stored object versions, policy evaluations, credentials, provider resources, or scheduled/offline use across a justified observation window. State blind spots and retention/replay horizons.

Use a final deny/warn rehearsal in representative non-production or selected cohorts. Quarantine or block new old-version creation before disabling reads needed for migration. Preserve read/export tools when disposal or legal access requires them.

Removal is an explicit change with canary, telemetry, abort/forward plan, communication, and post-removal monitoring. Never bury it in unrelated maintenance.

### Handle exceptions without expanding normal support

An exception identifies exact consumer/surface/revision, reason, incompatibility or risk, owner, approver/risk owner, compensating controls, support limits, evidence, migration plan, milestones, expiry, and incident action. It must not imply the whole old version remains supported.

Isolate exceptional consumers when possible: dedicated build path, nodes, provider instance, network boundary, read-only compatibility service, or frozen artifact registry. Continue vulnerability and incident monitoring.

Review renewal against current evidence and capacity; automatic renewal hides a failed policy. Charge visible support/risk cost to planning, not as punishment but to prevent invisible permanence.

If the successor does not cover a legitimate recurring need, treat that as product evidence and add a supported profile or retain the capability honestly.

### Override ordinary timelines for emergencies

Security compromise, safety hazard, data corruption, provider shutdown, or severe reliability defect may make continued compatibility unacceptable. Invoke predefined authority and severity criteria; identify affected inventory, evidence/confidence, disclosure boundary, safe target, temporary control, deadline, update path, support, and retrospective.

State which ordinary promise is overridden. Do not label an incompatible emergency change a patch merely to preserve metrics. Prefer the narrowest effective intervention and prioritize exposed/high-consequence consumers.

Rollback to compromised trust, vulnerable artifacts, corrupt schemas, or unsafe behavior may be forbidden. Prepare forward recovery, isolation, traffic stop, credential revocation, and alternative provider paths.

Emergency completion still needs reconciliation: all affected resources addressed or accepted, temporary authority revoked, exceptions reviewed, evidence retained, and policy improved.

### Measure transition outcomes and policy health

Track inventory coverage/freshness, supported and deprecated populations, time outside support, transition-path coverage, oldest/newest skew, update availability, assessment/start/verified lead time, throughput, failure/rework/rollback/forward-recovery rate, wave harm, owner response, warning reach, blockers, exception age, vulnerability exposure, support load, and removal incidents.

Latest-version percentage is not sufficient. It can reward forced risky upgrades, ignore verified outcomes, and hide unknown consumers. Track service/product outcomes and consumer maintenance burden.

Measure forecast accuracy and queue health. If arrivals exceed verified completion for long, deprecation debt grows even while individual migrations succeed. Reduce simultaneous change, simplify profiles, or add capacity.

Review policy exceptions and emergency overrides for systemic causes: weak compatibility, missing migration tools, short upstream choices, fragmented ownership, or unrealistic support windows.

### Retire the old system completely

After removal, delete or revoke old APIs/endpoints, controllers/operators, conversion/admission webhooks, CLI paths, libraries, templates/actions, images/builders, dependency mirrors/caches, resource schemas, feature flags, policies, service accounts/roles, secrets/keys/certificates/trust roots, network routes, provider resources, data replicas/backups under retention rules, telemetry producers/queries/alerts/dashboards, update jobs, exceptions, and support queues.

Archive required specifications, migration decisions, evidence, incident history, and tombstones without keeping executable authority alive. Redirect discovery to the successor and make accidental old use fail clearly.

Re-scan after the observation window for resurrection: cached artifacts, restored backups, dormant schedules, forks, and disaster-recovery automation can reintroduce the old version.

Retirement completes when the organization no longer operates or implicitly promises the old surface, residual retained data/records have explicit purpose and access, and future recovery cannot silently recreate unsupported state.

### Use an executable transition inventory

This synthetic inventory checks ten migration records for minimum policy fields. It does not prove compatibility, consumer ownership, production safety, schedule feasibility, recovery, or absence of undiscovered users.

<!-- bijux-verify: {"id":"upgrade-deprecation-transition-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"consumers 10\nowned 9\npath_tested 8\ncompatibility_checked 9\ndata_accounted 8\nwave_assigned 8\nrecovery_defined 8\ndeprecation_reached 9\nexception_expires 9\nretirement_checked 8\n","stderr":""}} -->
```python
consumers = [
    ("public-api", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("internal-api", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("event-consumer", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("batch", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("stateful", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("control-plane", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("offline-recovery", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("regulated-legacy", 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("unowned-service", 0, 0, 1, 0, 0, 0, 1, 0, 0),
    ("emergency-adapter", 1, 0, 0, 0, 0, 0, 0, 1, 0),
]
fields = [
    "owned", "path_tested", "compatibility_checked", "data_accounted",
    "wave_assigned", "recovery_defined", "deprecation_reached",
    "exception_expires", "retirement_checked",
]
print("consumers", len(consumers))
for index, field in enumerate(fields, start=1):
    print(field, sum(consumer[index] for consumer in consumers))
```

The incomplete records remain explicit risks. The unowned service cannot be counted as migrated, and the emergency adapter needs a bounded path and retirement plan even though it temporarily preserves compatibility.

## Definitions and Notation

- $G=(V,E)$: directed upgrade-transition graph.
- $V$: immutable supported or historically relevant revisions/states.
- $E$: tested, owned directed transitions.
- $(u,v)$: transition from current revision $u$ to target $v$.
- $\Omega$: set of simultaneously supported component/contract tuples.
- $N$: reconciled consumers remaining for a transition.
- $\mu$: empirically verified terminal migrations per unit time under stated capacity.
- $T$: minimum no-arrival elapsed migration time under the simple throughput bound.
- $\lambda$: newly discovered or newly entering migration demand per unit time.
- $\kappa=(\kappa_s,\kappa_w,\kappa_m,\kappa_o,\kappa_d,\kappa_{sec},\kappa_f,\kappa_e)$: source, wire, semantic, operational, data, security, workflow, and evidence compatibility assessments.
- **terminal migration**: target state whose workload/data/security/evidence outcomes pass, not merely an attempted update.
- **observation window**: justified period over which old use and control outcomes are checked, including rare/replay paths.
- **unknown**: unresolved inventory, compatibility, operation, or evidence state that cannot be treated as success.

## Mechanisms, Invariants, or Proof Structure

1. Catalog every versioned surface, owner, contract, support state, dependencies, upstream dates, consumers, data, and evidence.
2. Classify proposed change across $\kappa$ and mark irreversible effects.
3. Construct transition edges and supported skew set $\Omega$ from tested evidence.
4. Topologically order dependencies and select expand/migrate/contract, coexistence, adapter, replace/restore, or forward-only path.
5. Reconcile consumer inventory and forecast capacity using terminal throughput, unknowns, failures, and arrivals.
6. Publish immutable target, upgrade plan, deprecation contract, migration tooling, warnings, support, and exception route.
7. Qualify representative hard archetypes, then progress bounded waves with outcome/guardrail evidence and stop authority.
8. Reconcile desired revision, runtime, data, security, telemetry, exceptions, and consumer outcome after every wave.
9. Apply removal gates and bounded negative evidence; escalate unknown/unowned consumers rather than deleting them from scope.
10. Remove under observation, then retire all code, state, authority, infrastructure, evidence jobs, and support residue.
11. Audit forecasts, incidents, exceptions, and resurrection to improve future support and selection policy.

The throughput bound assumes no new arrivals, constant verified throughput, and independent capacity. If $N=120$ and $\mu=6$ per week, at least 20 weeks are required. Failures, discovery, or shared bottlenecks increase time. When ongoing arrival $\lambda\geq\mu$, backlog cannot decline under that steady-state model; the organization must reduce arrivals/scope or increase throughput.

Compatibility is not generally symmetric: a new reader may accept old data while the old reader rejects new data. It is not generally transitive as evidence: separate tested edges do not establish a skipped direct transition. The directed graph prevents version order from being mistaken for migration proof.

## Alternatives and Trade-Offs

- **Rolling in-place versus replace/cutover:** rolling saves capacity and preserves endpoints but requires skew; replacement isolates validation/rollback but duplicates state/cost and needs cutover.
- **Automatic merge versus reviewable proposal:** auto-merge accelerates bounded changes; review protects consumer semantics and local ownership.
- **Long support versus short support:** long windows reduce forced change but multiply patch/test/expertise cost; short windows reduce matrix cost but increase consumer disruption.
- **Direct upgrade versus required hops:** direct paths are faster but need explicit evidence; intermediate hops reuse tested conversions while adding time and failure opportunities.
- **Backward compatibility versus adapter:** native compatibility simplifies consumers but burdens core code; adapters isolate legacy semantics but create another operated component.
- **Rollback versus forward recovery:** rollback is fast before irreversible state; forward recovery respects new state/trust but requires prepared repair paths.
- **Fleet wave versus team-paced pull:** coordinated waves concentrate support/evidence; team pacing respects roadmaps but prolongs skew and exposure.
- **Usage telemetry versus declared inventory:** telemetry shows observed use but misses rare/offline paths; declarations add ownership context but become stale.
- **Warning at every use versus aggregation:** per-use warning maximizes visibility but creates noise/cost; aggregation must retain unique affected consumers and urgency.
- **Hard deadline versus removal gates:** date certainty drives planning; evidence gates prevent unsafe removal. Use an earliest date plus mandatory gates and escalation.
- **Quarantine versus immediate removal:** quarantine limits new harm and preserves diagnosis/migration; immediate removal closes exposure faster but can destroy continuity.
- **Provider-managed versus platform-managed upgrade:** providers reduce operations but constrain timing/rollback; platform ownership increases control and maintenance burden.
- **Exception isolation versus extending fleet support:** isolation limits test/security burden; fleet extension may be warranted for a recurring legitimate cohort.
- **One large change versus incremental transitions:** bundling reduces coordination events but hides causal failures; incremental edges improve diagnosis while extending transition time.

## Failure Modes and Misconceptions

- **“The new release exists, so upgrade is done.”** consumers, running state, data, and evidence must reach verified target outcomes.
- **“Higher version is safer.”** safety depends on threat, compatibility, support, configuration, and evidence.
- **“SemVer decides whether our change is compatible.”** it communicates a promise relative to a declared public API; semantic judgment remains.
- **“Both endpoints are supported, so direct transition works.”** only tested directed edges establish a migration path.
- **“Compatibility is symmetric.”** new readers may accept old data while old readers cannot accept new data.
- **“Compatibility is transitive.”** sequential supported edges do not prove a skipped conversion or direct rollout.
- **“Additive changes cannot break.”** enums, defaults, fields, labels, limits, latency, and policy can break bounded consumers.
- **“Latest-to-latest tests are enough.”** mixed versions, old data, upgrade order, rollback, and offline readers dominate transitions.
- **“A pull request is a migration.”** it may be unreviewed, conflicting, unmerged, undeployed, or behaviorally failed.
- **“No traffic means no consumer.”** rare schedules, DR scripts, stored data, replay, sampling, or blocked telemetry may be invisible.
- **“Deprecation is a warning.”** it is a support-state contract with successor, timeline, migration, gates, and owner.
- **“Notification sent means responsibility transferred.”** the platform must offer a viable migration and support; consumer ownership still needs commitment.
- **“A deadline creates capacity.”** throughput, failures, unknowns, and staff determine feasibility.
- **“Rollback is the old image.”** data, external effects, trust revocation, provider state, and old-reader compatibility decide.
- **“A snapshot guarantees rollback.”** restoration time, completeness, application invariants, and reader compatibility must be tested.
- **“Security fixes never need compatibility.”** urgency may override a promise, but inventory, support, verification, and forward recovery remain.
- **“An exception keeps the version supported.”** it bounds one consumer and carries residual risk; normal support does not expand silently.
- **“Zero deprecated calls proves removal readiness.”** storage, offline/recovery tools, uninstrumented paths, and authority can remain.
- **“Removal is retirement.”** builders, images, controllers, credentials, data, telemetry, docs, and support may persist.
- **“Once retired, old state cannot return.”** backups, caches, forks, dormant schedules, or DR automation can resurrect it.

## Worked Examples

### Example 1

Runtime 3 and 5 are supported, but only edges 3→4 and 4→5 are tested because each changes bytecode and configuration formats. The orchestrator rejects 3→5 and schedules both hops. Conclusion: supported endpoints do not imply a supported direct transition.

### Example 2

A response adds an enum member under a minor version. Contract tests show an exhaustive generated client throws on unknown values. Emission is gated until clients become open-enum compatible. Conclusion: wire-additive can be semantically incompatible.

### Example 3

There are 120 consumers and observed verified throughput is six per week. $T\geq120/6=20$ weeks, exceeding a 16-week support deadline. The program adds capacity, narrows automation, and negotiates an isolated maintenance bridge. Conclusion: dates must reconcile with throughput.

### Example 4

An updater opens 200 dependency pull requests. Only 30 merge; 12 fail production canaries and 158 are ignored or conflict. Reporting “200 upgrades delivered” is false; terminal migration records show 18 verified. Conclusion: proposals and merges are intermediate, not outcomes.

### Example 5

A database rollout adds a nullable column, deploys dual readers/writers, backfills with checkpoints, verifies invariants, and then makes the field required. Binary rollback is available before contraction; after it, recovery is forward. Conclusion: irreversibility changes recovery strategy.

### Example 6

API telemetry shows no deprecated calls for 60 days. A quarterly disaster-recovery test restores objects stored in the old version and invokes an offline converter. Removal waits for conversion and a tested new drill. Conclusion: the observation window must include rare and recovery paths.

### Example 7

A Kubernetes control-plane target supports older nodes, but an admission webhook cannot decode the new resource version. Preflight blocks the wave until the webhook handles equivalent versions. Conclusion: published component skew does not prove local integration skew.

### Example 8

A compromised trust root requires immediate revocation. Ordinary coexistence would preserve attacker access, so incident authority distributes new trust, moves verified consumers, quarantines stragglers, revokes old trust, and forbids rollback. Conclusion: emergency incompatibility can be safer when explicit and reconciled.

### Example 9

A regulated workload cannot leave an old provider before approval. Its exception binds one account, blocks new resources, isolates network/identity, funds patches, monitors risk, and expires after a dated approval plan. Conclusion: narrow isolation avoids silently extending fleet support.

### Example 10

After API removal, an old builder, registry tag, service account, conversion webhook, alert, and backup restore script remain. Retirement removes/revokes them, archives required evidence, and rechecks after the DR cycle. Conclusion: negative lifecycle cleanup extends beyond endpoint shutdown.

## Cross-Program Connections

- **API engineering:** versions, compatibility, deprecation/sunset signals, clients, schemas, errors, and long-running operations define interface transitions.
- **Software engineering:** dependency graphs, SemVer, builds, tests, refactoring, feature flags, generated code, and release automation create upgrade mechanisms.
- **Distributed systems:** mixed versions, partial failure, retries, unknown outcomes, consensus, state conversion, and irreversible effects constrain ordering.
- **Data engineering:** expand/backfill/dual operation/contract, event replay, CDC, backups, lineage, retention, and validation govern durable migrations.
- **Reliability engineering:** canaries, SLOs, error budgets, blast radius, stop conditions, restoration, and incident response protect fleet change.
- **Security engineering:** vulnerability response, provenance, trust rotation, identity/permission change, exposure, exceptions, and revocation may compress timelines.
- **Systems engineering:** configuration baselines, interface control, verification, change control, technology refresh, maintainability, and disposal structure lifecycle evidence.
- **Product management:** channels, support promises, segmentation, communication, adoption, and migration experience determine trust.
- **Operations research:** dependency ordering, throughput, arrivals, work-in-progress, bottlenecks, and forecast error make schedules honest.
- **Organizational design:** ownership, funding, incentives, escalation, cross-team coordination, and provider contracts decide whether migration capacity exists.

## References

1. Semantic Versioning Authors, “Semantic Versioning 2.0.0,” current specification, retrieved 2026-09-02. https://semver.org/
2. Kubernetes Authors, “Kubernetes Deprecation Policy,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/deprecation-policy/
3. Kubernetes Authors, “Version Skew Policy,” current documentation, retrieved 2026-09-02. https://kubernetes.io/releases/version-skew-policy/
4. Kubernetes Authors, “Deprecated API Migration Guide,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/deprecation-guide/
5. IETF, “The Deprecation HTTP Response Header Field,” RFC 9745, March 2025. https://www.rfc-editor.org/rfc/rfc9745
6. IETF, “The Sunset HTTP Header Field,” RFC 8594, May 2019. https://www.rfc-editor.org/rfc/rfc8594
7. OpenTelemetry Authors, “Versioning and Stability for OpenTelemetry Clients,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/versioning-and-stability/
8. OpenTelemetry Authors, “Telemetry Stability,” current specification, retrieved 2026-09-02. https://opentelemetry.io/docs/specs/otel/telemetry-stability/
9. Google, “AIP-180: Backwards Compatibility,” current guidance, retrieved 2026-09-02. https://google.aip.dev/180
10. Google, “AIP-185: API Versioning,” current guidance, retrieved 2026-09-02. https://google.aip.dev/185
11. GitHub, “Configuring Dependabot Version Updates,” current documentation, retrieved 2026-09-02. https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-version-updates
12. National Institute of Standards and Technology, “Secure Software Development Framework (SSDF) Version 1.1,” SP 800-218, February 2022. https://doi.org/10.6028/NIST.SP.800-218
13. Cloud Native Computing Foundation Platforms Working Group, “Platforms White Paper,” April 2023. https://tag-app-delivery.cncf.io/whitepapers/platforms/
14. Google, “Canarying Releases,” Site Reliability Engineering Workbook, 2018. https://sre.google/workbook/canarying-releases/

## Exercises

### Exercise 1

Construct a directed transition and skew model for CLI 2/3, API 1/2, controller 4/5, storage A/B, and policy P/Q. State tested edges, mixed tuples, upgrade order, irreversible points, and rejected transitions.

### Exercise 2

A platform has 240 consumers, verifies eight migrations per week, discovers two additional consumers per week for six weeks, and expects a 20% rework load. Produce a bounded schedule and explain which assumptions must be measured rather than asserted.

### Exercise 3

Write a deprecation contract for a runtime profile whose upstream support ends in 24 weeks. Include successor, inventory, warning channels, waves, capacity, support, exceptions, removal gates, recovery, and retirement.

### Exercise 4

Design an emergency transition after compromise of an artifact-signing identity. Cover authority, inventory, trust change, artifact verification, prioritization, incompatibility, rollback prohibition, exceptions, communications, and reconciliation.

### Exercise 5

Plan removal and retirement of a Kubernetes custom resource version that has live resources, stored objects, conversion webhooks, generated clients, policies, dashboards, backup/restore, and one offline quarterly consumer.

## Answers to the Exercises

### Answer 1

Model each meaningful composed state as a vertex or use a tuple set $\Omega$. Example edges: CLI2/API1→CLI3/API1 after client compatibility; controller4/storageA→controller5/storageA only when controller5 reads/writes A; then enable API2 and dual A/B conversion; migrate stored objects A→B; move policy P→Q after both resource versions pass; finally retire API1/controller4/storageA. Test old/new clients against served APIs and controllers against both storage forms. Reject CLI2/API2 if responses are incompatible, controller4/storageB if it cannot decode B, and direct storage A→B without the conversion/backup edge. Storage contraction, external effects, and removal of API1 are irreversible points; before them rollback uses dual compatibility, afterward use forward repair or restore into a compatible system. Exact tuples require evidence rather than version-order inference.

### Answer 2

The simple initial lower bound is $240/8=30$ weeks. Six weeks of discovery add 12 consumers, producing 252 base items. Treating 20% rework as additional throughput demand yields about $252\times1.2=302.4$, so a planning approximation is 303 migration-equivalents and at least $303/8=37.875$, about 38 weeks. This is not a queueing theorem: clarify whether eight is gross attempts or terminal completions and whether rework is already included; arrivals may continue; consumers vary in effort; staff, blackouts, dependencies, and correlated failures change throughput. Use cohort-specific distributions and contingency, measure terminal weekly completions, discovery, failure/rework, wait states, and support capacity, and revise the forecast. A shorter deadline needs more capacity, less scope, an adapter/extension, isolation, or explicit risk—not rounding.

### Answer 3

Publish the exact profile/revisions, reason and upstream/security limit, supported successor of equal or greater maturity, announcement date, new-admission stop, earliest removal at or before the 24-week boundary, and objective gates. Reconcile repository, artifact, deployment, scheduled/offline, data, owner, and exception inventory. Emit CI/template/catalog/runtime warnings plus direct owner notices with replacement and guide. Qualify representative stateless, event, batch, stateful, high-scale, and regulated consumers early. Forecast terminal throughput with failures/unknowns, fund update tooling and support, and use waves with outcome/security/telemetry guardrails. Exceptions bind one consumer, isolation/patching, risk owner, milestones, and expiry. Gates require stable successor, zero unsupported/unknown consumers, converted data/backups, tested recovery, telemetry continuity, and incident readiness. After removal, revoke builders/images/credentials/policies, delete caches/actions/docs/alerts, retain governed evidence, and test against resurrection.

### Answer 4

Invoke documented incident authority and identify compromised issuer/key, signing interval, repositories/builders, artifacts and deployments, registries, consumers, and unknowns. Establish a protected new identity and verifier trust, rebuild or independently validate affected artifacts from trusted source/build paths, and prioritize public/high-authority/restricted-data workloads. Where safe, distribute new trust before enforcing it; do not retain compromised trust merely for compatibility. Quarantine unverifiable artifacts, stop publication/deployment, revoke old authority, and communicate exact affected scope without unsafe disclosure. State that rollback to old-signed artifacts is forbidden. Narrow exceptions require alternative verification, isolation, monitoring, owner, and very short expiry. Reconcile every digest/deployment, revoke temporary incident access, remove cached trust and credentials, preserve evidence, review false classification, and update builder/identity separation and emergency policy.

### Answer 5

Inventory served and storage versions, every live object and controller, schemas/conversion webhooks, clients/repos/artifacts, admission and authorization policy, telemetry queries/alerts, backups/archives, DR tools, and the quarterly consumer. Serve old and new versions with lossless conversion where promised; update controllers, clients, policy, and observability to tolerate both. Migrate stored objects explicitly and verify round trips, defaults, unknown fields, and application invariants. Exercise backup restore and the quarterly workflow using the successor; absence of live calls is insufficient. Stop new old-version writes, warn/deny canaries, reconcile zero old requests/objects/readers across the observation horizon, and resolve exceptions. Remove serving only after recovery evidence passes, then retire conversion webhook/certificates/roles, old generated clients/schemas/policies/dashboards, storage code, test fixtures, and update jobs. Retain version specifications and audit evidence as required and recheck after a DR restore cycle for resurrection.
