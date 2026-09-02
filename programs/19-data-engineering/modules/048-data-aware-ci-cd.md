---
module_id: DE-048
program: Data Engineering
level: 1
module_number: 48
title: Data-Aware CI/CD
status: complete
last_verified: 2026-09-03
---

# Data-Aware CI/CD

## One-Page Review

### Governing question

How can a delivery system prove that a proposed data change has been tested over the complete affected graph, preserves producer and consumer contracts, promotes exactly the reviewed artifacts and bindings, and has a safe response for both software and already-produced data?

### Essential definitions

- **Data-aware continuous integration** classifies a proposed change, closes that change over data dependencies and consumers, then runs evidence appropriate to the resulting risk rather than treating a repository as an undifferentiated software package.
- **Data-aware continuous delivery** produces an immutable, deployable artifact and evidence bundle; **continuous deployment** additionally promotes an accepted bundle automatically under policy.
- A **change set** is the reviewed difference in transformation code, schemas, contracts, orchestration, configuration interfaces, dependencies, infrastructure, reference data, or policy.
- The **impact closure** of a change set is the conservative set of assets, jobs, contracts, and consumers whose behavior or compatibility may change through declared or inferred dependencies.
- A **gate** is a versioned predicate over identified evidence with an owner, severity, applicability rule, expiry or waiver process, and fail-closed behavior for missing required results.
- A **candidate generation** is an isolated data output produced by a particular artifact, configuration, input cut, and execution attempt before publication.
- **Promotion** changes the approved environment or reader reference to an already identified artifact or candidate; rebuilding during promotion creates a different candidate.
- A **compatibility window** is the interval in which old and new producers, schemas, readers, and state representations are deliberately allowed to coexist.
- **Expand-contract** first introduces a backward-compatible representation, migrates producers/data/readers, verifies adoption, and only then removes the old representation.
- A **data rollback** restores or republishes compatible data state; it is distinct from rolling back code because writes, messages, deletes, and external effects may survive a software rollback.
- A **forward repair** emits a corrected generation or compensating facts while preserving history and lineage.
- A **release evidence bundle** binds source revision, artifact digest, dependency/provenance attestations, compiled graph, impact decision, test results, environment bindings, migrations, candidate identities, approvals, and publication receipt.

### Central model, mechanism, or theorem

Let $G=(V,E)$ be the governed dependency graph. A change classifier maps reviewed difference $\Delta$ to seed nodes $C_0\subseteq V$ and changed interfaces. Conservative impact is a least fixed point:

$$
I_0=C_0,
\qquad
I_{k+1}=I_k\cup\{v\in V:\exists u\in I_k,(u,v)\in E\}\cup X(I_k,\Delta),
\qquad
I^*=I_n=I_{n+1},
$$

where $X$ adds consumers reached through contracts, semantic dependencies, macros, policies, dynamic references, or uncertain lineage not represented by ordinary graph edges. A selected build is sound only if $I^*$ over-approximates every behaviorally affected node.

For candidate $c$, the applicable gate set is $R(c,I^*,\Delta,r)$ under release policy version $r$. Deployment is admissible only when each required gate has one fresh result bound to the same candidate and all blocking predicates pass:

$$
\operatorname{admit}(c)=
\operatorname{identity}(c)
\land
\operatorname{complete}(R,c)
\land
\bigwedge_{g\in R}g(c)
\land
\operatorname{migrationSafe}(c)
\land
\operatorname{publicationSafe}(c).
$$

This is conditional assurance, not proof that all future data is correct. If dependency discovery is incomplete, tests use different artifacts or cuts, required evidence is missing, a waiver is unowned, or promotion rebuilds the candidate, a green interface is not a valid release decision.

### Critical invariants

- Every source, generated artifact, dependency lock, compiled plan, schema, policy, configuration interface, and migration has a stable identity and provenance.
- Change classification includes code, contracts, schemas, macros, packages, runtime/engine versions, orchestration, infrastructure, access policy, reference data, and state transitions.
- Impact selection includes downstream consumers and hidden/dynamic dependencies; uncertainty widens selection rather than silently narrowing it.
- Tests, scans, data comparisons, approvals, and deployment all refer to the same immutable candidate and compatible input/reference cut.
- Required gates are derived by versioned policy, are visible before approval, distinguish fail/error/skip/missing/warn, and fail closed for missing blocking evidence.
- CI uses isolated namespaces, credentials, checkpoints, catalogs, topics, and publication targets; it cannot read or mutate production unless an explicit governed exception permits a narrow read.
- Fixtures are synthetic or approved and minimized; production identifiers, secrets, rare values, and linkable relationships do not leak into logs, caches, artifacts, or forks.
- Schema, state, and data migrations have compatibility windows, idempotent/resumable operations, adoption evidence, and an explicit point after which old code cannot safely return.
- Candidate data remains private until contract, reconciliation, lineage, security, and publication conditions pass.
- Canary, shadow, or dual-run output cannot become authoritative by accident; its audience, side effects, comparison rule, and cleanup are explicit.
- Code rollback never implies data rollback. Every release records whether to revert code, restore a pointer, republish a prior snapshot, compensate, or forward-repair.
- Publication is conditional on the expected parent/current version and yields a durable receipt; concurrent or stale publishers cannot overwrite newer accepted state.

### Common failures

Common failures include running only tests in edited files; ignoring downstream consumers; trusting stale lineage; treating a SQL compile as semantic validation; comparing row counts while allocations changed; rebuilding an artifact after review; deploying a mutable image tag; letting CI share production credentials or state; copying raw production rows into fixtures; allowing skipped tests to appear green; retrying flaky checks until one passes; approving an unbounded waiver; applying a destructive migration before compatible readers exist; rolling back code after irreversible writes; running a shadow job with real notifications or mutations; promoting data before its lineage and reconciliation finish; signing an artifact without proving what build inputs produced it; and storing evidence that cannot be joined to the published generation.

### Compact example

A change edits `orders_clean`. The graph declares `orders_clean -> sales -> report`; `sales` also reads unchanged `rates`. Conservative closure selects `orders_clean`, `sales`, and `report`. Policy requires a contract and unit gate for `orders_clean`, unit/integration/reconciliation gates for `sales`, and a consumer gate for `report`. All six pass against one artifact digest and isolated candidate, so promotion may proceed; `orders_raw` and `rates` are reused only because their immutable identities are recorded. If the reconciliation result is missing, or a dynamic report dependency cannot be resolved, admission is false even when every executed check is green.

### Connections

[DE-040](040-testing-a-multi-stage-batch-pipeline.md) supplies detailed test oracles and scenarios. [DE-041](041-directed-acyclic-graphs-and-dependencies.md) through [DE-047](047-parameterization-and-environment-separation.md) supply dependency, asset, trigger, retry, partition, backfill, and environment semantics that delivery must preserve. DE-049 next develops the persistent operational state that release evidence references.

## Governing Question

What evidence would let an independent reviewer reconstruct why a data change was selected, which assets and consumers could be affected, what exactly was built and tested, which data and environment bindings were used, why promotion was allowed, and how already-produced effects would be repaired if the release were wrong?

Ordinary software CI often maps a source revision to compilation, unit tests, packaging, and deployment. Data systems add mutable external inputs, long-lived datasets, historical recomputation, multiple producer/consumer versions, schema evolution, stateful checkpoints, asynchronous readers, and side effects that persist after code stops. A build can be technically valid while corrupting allocation, omitting a partition, exposing a column, or making an older reader fail.

The delivery unit is therefore not source code alone. It is a bound release candidate: source revision, resolved dependencies, compiled transformations, runtime image, schema/contracts, orchestration definition, configuration interface, policy, migration plan, and—when data is materialized—specific candidate generations. CI establishes bounded evidence about that unit. Delivery preserves its identity. Deployment makes it active only when compatibility and publication conditions hold.

Speed matters, but unsafe selection is false economy. A five-minute job that omits an affected consumer provides less assurance than a forty-minute complete job. Conversely, rebuilding every table for every documentation edit wastes feedback capacity and encourages bypasses. Data-aware CI/CD uses explicit change classification and conservative dependency closure to spend assurance effort where it changes the release decision.

The central design problem is evidence integrity. Results must be complete, fresh, attributable, tamper-evident enough for the risk, and bound to the artifact and candidate actually promoted. A dashboard full of green checks is weak evidence if some were skipped, came from a different revision, used mutable references, or tested a staging configuration that production does not share.

## Why This Matters

Data defects commonly execute successfully. A renamed column may compile in the producer but break a downstream query hours later. A join change can preserve total row count while reallocating revenue. A new partition filter can pass on a small fixture but omit daylight-saving boundaries. An image upgrade can change decimal, timezone, serialization, or optimizer behavior with no source-code diff. CI must reason about contracts and data semantics, not only process exits.

Blast radius follows dataflow. Editing a shared macro may affect hundreds of models. Changing a source schema may reach consumers outside the repository. Updating a policy may change who can read an otherwise identical table. Static graph edges are valuable, but dynamic SQL, generated names, runtime discovery, undocumented exports, dashboards, notebooks, extracts, machine-learning features, and external partners create hidden edges. An honest pipeline makes uncertainty visible and expands tests or requires explicit review.

Historical state makes releases asymmetric. Deploying a corrected transformation changes future writes, but prior partitions remain wrong until restated. Reverting the code does not retract emitted messages, reverse an external API call, reconstruct deleted rows, or change cached downstream copies. Schema contraction may make older binaries unable to restart. A release plan must model the data plane before calling rollback safe.

Data delivery is also a security boundary. CI often has broad repository access, can execute contributor-controlled code, produces logs/artifacts, and may be triggered from forks. Giving it production secrets or direct production mutation turns a code review failure into a data incident. Test datasets can themselves leak personal or commercially sensitive information. Isolation and least privilege are release correctness requirements, not optional hardening.

Reproducibility controls operational response. If a failure appears after deployment, responders need the compiled graph, artifact digest, exact configuration/bindings, dependency versions, input generation, migration status, gate results, and publication receipt. Rebuilding from the same commit later may resolve a different base image or package. Without retained evidence, neither rollback nor forward repair can be trusted.

Good delivery design improves speed because it makes reuse legitimate. Immutable unchanged parents can be deferred or referenced; affected descendants can be built in isolated schemas; contract checks can run before expensive integration; full graph rehearsals can run for high-risk or scheduled changes. The optimization rests on stable identities and a defensible selection algorithm, not wishful caching.

Finally, CI/CD governs organizational promises. Dataset owners, consuming teams, security, privacy, and operations may each own a gate. A policy-controlled evidence bundle makes those obligations inspectable. An opaque script that happens to deploy encodes the same decisions without names, ownership, expiry, or auditability.

## Prerequisites and Retrieval

Retrieve the repository and target branch; source revision and review diff; module/package ownership; transformation source and compiled output; dependency locks, container/base-image digests, compiler/adapter/engine versions, and build provenance; logical asset graph and observed lineage; dynamic references, macros, generated SQL, runtime discovery, exports, dashboards, notebooks, APIs, features, extracts, and external consumers; schemas, contracts, compatibility policy, semantic versions, deprecation dates, and consumer acknowledgements; orchestration definitions, schedules, sensors, partitions, backfill rules, concurrency, retries, timeouts, idempotency keys, checkpoints, and publication mechanisms; configuration schemas, environment bindings, secrets, identities, accounts, networks, catalogs, topics, storage prefixes, quotas, and encryption; source/reference generation identities; fixtures, masking/synthesis process, retention, deletion, and access policy; test inventory and applicability rules; historical runtime/cost baselines; security and dependency scans; migration scripts and ledgers; canary/shadow/dual-write design; rollback and forward-repair runbooks; approval/waiver policy; evidence retention; and relevant incidents and escaped defects.

Distinguish changed files from changed behavior; declared graph from observed lineage; direct nodes from transitive consumers; semantic change from formatting; source compatibility from consumer compatibility; parse/compile success from execution; unit evidence from actual-engine evidence; test selection from test effectiveness; skipped from passed; flaky from nondeterministic product behavior; cache reuse from stale result reuse; artifact identity from a tag; build from promotion; configuration interface from environment value; release candidate from published generation; schema expand from schema contract; backward-compatible read from backward-compatible write; code rollback from data restoration; candidate validation from production monitoring; signature from provenance; synthetic fixture from anonymized production data; and continuous delivery from automatic production deployment.

Construct a release contract:

| Concern | Required decision and evidence |
|---|---|
| Change | Reviewed diff, semantic classification, owners, risk tier, generated/compiled difference |
| Impact | Seed nodes, graph/lineage versions, transitive closure, hidden-dependency treatment, exclusions with proof |
| Build | Hermetic inputs, lockfiles, artifact digest, provenance, SBOM or dependency inventory, reproducibility status |
| Test | Required gates, applicability, candidate/cut identity, results, failures/errors/skips, logs and diagnostics |
| Data | Fixture origin, privacy class, source/reference generations, reconciliation, data-diff scope and comparator |
| Contract | Producer/consumer schemas and semantics, compatibility direction/window, owners, deprecation evidence |
| Migration | Ordered operations, idempotency/resume, capacity, adoption, point of no return, restoration/repair |
| Environment | Configuration interface, immutable effective binding, identity/IAM/network/state isolation |
| Rollout | Shadow/canary audience, side-effect suppression, comparison, success/abort thresholds, observation period |
| Publication | Candidate generation, expected parent, conditional action, approver/policy, receipt and reader visibility |
| Recovery | Code revert, pointer restore, snapshot availability, compensation/forward repair, reconciliation owner |
| Evidence | Bundle schema/version, storage, integrity, retention, authorization, query path and audit linkage |

Write the governing claim as a falsifiable statement: “Artifact digest `a`, compiled graph `g`, effective binding `b`, and candidate generations `d` were built from reviewed revision `s`; impact policy `p` selected closure `I`; every gate in `R(I,p)` passed over those identities; migration `m` is compatible with active readers; conditional publication replaced expected parent `q`; recovery plan `r` covers code and data effects.”

## Learning Objectives

After completing this module, you should be able to:

1. define a data release candidate and evidence bundle with stable identities across source, artifact, configuration, data, and publication;
2. classify code, contract, schema, dependency, orchestration, environment, policy, reference-data, and migration changes by risk;
3. compute conservative downstream impact closure from declared graphs, compiled artifacts, observed lineage, and explicit uncertainty;
4. derive fast and full gate sets without confusing executed checks with complete required evidence;
5. isolate CI data, credentials, state, networks, catalogs, and side effects while producing representative fixtures safely;
6. design producer/consumer compatibility windows and expand-contract sequences for schema and state evolution;
7. bind build provenance, security scans, test outcomes, data diffs, approvals, and waivers to one immutable candidate;
8. choose shadow, canary, blue/green, dual-read, and dual-write rollout patterns with explicit comparison and authority;
9. separate code rollback, metadata-pointer restoration, snapshot restoration, compensation, and forward repair; and
10. audit delivery effectiveness through selection misses, escaped defects, flakes, lead time, rollback readiness, and evidence reconstruction drills.

## Core Exposition

### Define the deliverable before the pipeline

A branch name or commit is not the complete deployable object. Build a release manifest that names the source tree, generated and compiled transformations, package lock, image digest, runtime/adapter, contract bundle, orchestration definition, configuration schema, policy, migrations, and expected graph. If candidate data is produced before approval, include each generation and its source/reference cut.

Prefer immutable content identities. A tag such as `latest`, a mutable package range, or “current production table” changes meaning over time. A digest does not prove correctness, but it makes evidence joinable. Signing a digest authenticates an assertion by a key; provenance further describes how the artifact was produced. SLSA provenance models the output artifact as a subject and describes build inputs and process, supporting verification of the expected source and build platform. It does not validate data semantics.

Build once and promote the identical artifact. A production rebuild may observe a new dependency, base image, compiler, generated timestamp, or registry state. If environment values must differ, bind them through a versioned interface and record the resolved effective configuration as [DE-047](047-parameterization-and-environment-separation.md) describes. The artifact remains identical while authorized bindings vary.

Treat generated SQL, graph manifests, and migration plans as review surfaces. Human-readable diffs catch macro expansion, column reordering, materialization changes, and unexpected dependencies that source diffs obscure. Store the generated result or its digest with tool/version provenance; never let an unreviewed generation step silently change between CI and deployment.

### Classify the change semantically

Begin with the reviewed diff but classify effects. Categories include documentation-only; nonsemantic formatting; transformation expression; filter/join/window/aggregation; contract/schema; materialization or storage layout; incremental state/checkpoint; partition scope; orchestration/dependency; retry/concurrency; reference data; package/runtime/engine; configuration interface or environment binding; access/security/privacy policy; infrastructure/capacity; migration; and deletion/deprecation.

Classification drives policy, not developer optimism. A column description may be metadata-only, but a tag can drive selection or access policy. A package lock change may alter every compiled model. A runtime upgrade can change parsing, timestamps, decimals, ordering, or files. A reference-data change can alter output with no code diff. Inspect compiled and resolved differences before assigning risk.

Use evidence-backed downgrades. To label a refactor nonsemantic, compare normalized compiled plans when meaningful, execute differential tests on representative cuts, and state what equivalence excludes. To reuse an unchanged parent, prove its immutable generation and contract are compatible. A label is an input to the gate policy, not a substitute for tests.

Unknown classifications fail toward broader review. New file types, dynamic macros, unrecognized migration commands, missing ownership, or unavailable lineage should not fall into “no tests needed.” Record `unknown`, select a safe superset, and improve the classifier after review.

### Compute conservative impact closure

Construct a dependency graph from declared sources/references, compiled transformations, orchestration dependencies, contract registries, access policies, and consumer registrations. Add observed runtime lineage as corroboration and discovery. OpenLineage defines job, run, and dataset entities with extensible facets; those events can enrich impact analysis, but absence of an event is not proof that no dependency exists.

Seed the graph with every changed semantic surface. A shared macro or package may seed all nodes that compile through it. A source contract seeds direct readers. A column-level change should follow column lineage where trustworthy, then widen to dataset lineage where expressions, dynamic SQL, or lineage gaps make precision unsafe. An access-policy change seeds affected principals and products even if transformation dataflow is identical.

Compute downstream transitive closure and include contract consumers. Also include upstream fixtures or parents needed to execute selected nodes, but distinguish “must be built” from “may be reused immutably.” dbt state selection compares resources with a prior manifest and can select modified nodes; its `defer` mechanism can resolve unselected upstream references to another environment. That optimization is sound only when state artifacts, target identities, compatibility, access, freshness, and environment semantics are deliberately controlled.

Maintain exclusion reasons. If a downstream asset is omitted because a changed column is not referenced, preserve the compiled column-use evidence and lineage version. If lineage is stale or unresolved, widen the closure. Periodically run full builds and compare failures with selected runs to measure false negatives.

Dynamic behavior requires special treatment. Generated table names, wildcard discovery, runtime catalog queries, user-defined functions, procedural code, external scripts, and dashboards may evade static graphs. Instrument runtime reads/writes, declare allowed dynamic namespaces, add conservative wildcard edges, or require owner review. Do not let graph elegance conceal incomplete observability.

### Layer gates by cost and information

Run cheap deterministic gates first: repository integrity, formatting, syntax, parse, compile, dependency resolution, graph cycles, schema/interface validation, policy-as-code, generated-diff review, secret scanning, license/dependency rules, and migration linting. Early failure saves scarce data-engine time but proves little about runtime semantics.

Next run pure/unit and contract checks over minimal fixtures. dbt unit tests support validating SQL model logic against small static inputs before full materialization. dbt data tests express assertions as queries whose returned rows are failures. These mechanisms are valuable only when assertions encode the actual domain contracts and their results are bound to the candidate.

Then run actual-engine integration over isolated state: storage formats, catalogs, transactions, permissions, UDFs, serialization, timestamps, numeric types, distributed behavior, retries, checkpoints, and publication primitives. Apache Airflow recommends DAG loader tests and unit tests for custom operators, while also emphasizing idempotent tasks and partition-specific reads/writes. Apache Beam describes testing individual functions, transforms, and complete pipelines with known inputs and expected outputs. Framework layers inform, but do not choose, the business oracle.

For affected outputs, compare old and new candidates at the same input/reference cut. Compute schema and key-set differences, insert/update/delete counts, null/domain changes, control totals, distribution shifts, and exact or sampled row differences by critical dimension. Explain every expected difference. A zero row-count delta does not establish equality; a large expected rewrite is not automatically failure.

Run consumer tests against the new producer candidate during the compatibility window. A producer can satisfy its own schema while violating a dashboard calculation, deserializer, feature contract, or external export. Contract suites owned by consumers, replayed representative requests, and dual-version integration expose directional compatibility.

Reserve full rebuilds, scale/performance checks, extended differential runs, failure injection, and disaster-recovery rehearsals for applicable risk tiers and scheduled assurance. Record what the pull-request path did not test. A nightly gate that fails after merge needs ownership and release consequences; otherwise it is monitoring theater.

### Make gate evaluation explicit

Represent every gate as data: identifier/version, owner, applicability expression, required inputs, candidate identity, execution identity, start/end, result, severity, evidence links, and freshness. Valid results include pass, fail, error, skipped, missing, cancelled, and waived. Only pass satisfies a blocking predicate unless a separately authorized, unexpired waiver names the exact gate and candidate scope.

Compute the required set before evaluating admission. Otherwise a broken test-discovery step can produce zero failures and a green build. Compare required identifiers with observed results; duplicates, conflicting results, wrong candidate digests, stale timestamps, or absent evidence fail completeness.

Retries require discipline. Infrastructure errors may be retried under a bounded policy, retaining every attempt. A deterministic assertion failure should not be rerun until lucky. If a check is genuinely flaky, quarantine may protect unrelated delivery only when risk owners accept the gap, scope/expiry are explicit, and repair is tracked. Repeatedly running until success destroys the estimated failure probability and audit trail.

Separate warnings from acceptance. Informational drift can warn; a known hard contract violation blocks. Thresholds need owners, windows, minimum sample sizes, seasonality/segmentation, and change control. Do not derive a threshold from the candidate it is judging or silently turn failure into warning when a release is urgent.

### Isolate CI environments and data

Give each run a unique namespace and least-privilege identity. Isolate catalogs/schemas, object prefixes, checkpoints, locks, queues/topics, caches, temporary tables, feature flags, and publication pointers. Deny production writes at IAM and network layers, not only through naming conventions. Fork-originated or untrusted changes receive stricter credentials and no protected secrets.

Use synthetic fixtures for logic and edge cases. When distribution or scale matters, generate shaped data with explicit seeds and constraints. If production-derived data is necessary, establish purpose, minimization, approval, masking/tokenization, access, isolation, retention, deletion, and reidentification assessment. Removing direct names is not sufficient when rare combinations or stable hashes remain linkable.

Prevent leakage through failure paths. Query results, stack traces, diff artifacts, screenshots, caches, warehouse history, object versions, and workflow metadata can retain values. Redact by schema/classification, cap samples, encrypt evidence, restrict viewers, and delete ephemeral namespaces on both success and failure. Cleanup itself must use validated narrow targets.

Test production permissions without giving CI production authority by validating policies statically, assuming constrained test roles, and running post-deployment read-only/deny probes under controlled identities. A staging success cannot prove production IAM, network, keys, quotas, or provider features are correct.

### Govern schemas and consumer compatibility

Define compatibility by operations, not file-format slogans. Adding a nullable field may be backward-readable but can break `SELECT *` consumers, positional loaders, strict validators, generated classes, policy defaults, or exports. Changing type, precision, nullability, enumeration, key, grain, time semantics, or meaning may be incompatible even if decoding succeeds.

State direction and population: can old readers consume new data; can new readers consume old data; can old and new writers coexist; can replayed historical data be interpreted? Include batch files already emitted, queued messages, cached extracts, and long-running jobs. Contract tests should exercise supported version pairs.

Use expand-contract for risky evolution. First add the new representation without removing the old. Deploy readers that tolerate both and writers that populate the compatible form. Backfill or migrate historical state, validate reconciliation and adoption, switch authority, observe, then remove the old representation only after consumer evidence and retention windows permit. Each step is a separately recoverable release.

Avoid simultaneous producer/consumer flag flips that require perfect coordination. Version contracts, advertise deprecation dates, register consumers, and measure use. Unknown consumers widen the compatibility window or block destructive contraction. Emergency overrides need an explicit incident decision and communication plan.

### Treat migrations as stateful releases

A migration operates on durable state and may outlive a deployment. Give it an identity, preconditions, bounded scope, owner, estimated load, concurrency/lock policy, resumable cursor, idempotency behavior, validation, postconditions, and receipt. Test on representative volume and physical layout; a correct small migration can exhaust logs, locks, quota, or maintenance windows at scale.

Order operations by compatibility. Create structures before writers require them. Populate before readers depend on complete values. Validate before making constraints blocking. Stop old writers before contracting formats they emit. Preserve a restoration point before irreversible deletion. Separate cleanup from the critical activation path when delay improves safety.

Define the point of no return. Before it, code or metadata-pointer rollback may restore service. After old data is transformed or deleted, return may require snapshot restoration, reverse migration, or forward repair. Test the chosen path and ensure retention covers the decision window.

Migration success is not process exit. Reconcile counts and keys, rejected rows, checksums/control totals, schema/constraints, lineage, access policies, and consumer reads. Record partial progress and unknown commit outcomes so a retry does not duplicate effects. [DE-044](044-retries-timeouts-and-idempotency.md) provides the operation semantics; delivery policy decides whether migration evidence admits activation.

### Promote candidates without rebuilding

Build data into an isolated candidate generation or branch. Apache Iceberg branches and tags provide named references to snapshots and support audit/experimental workflows; the general release pattern is to validate an immutable generation then change reader authority through controlled metadata. Product features differ, so verify actual isolation, retention, and concurrency behavior.

Promotion should be a small conditional transaction: “make candidate `c` current only if current is expected parent `p`, policy decision `d` is valid, and migration state `m` is accepted.” This prevents a stale pipeline from overwriting a newer release. Return a receipt with old/new identities, actor/policy, time, and outcome.

If storage cannot atomically switch a multi-asset product, design a release manifest that readers resolve consistently, or order publication with compatibility guarantees. Publishing tables independently can expose mixed generations. A successful sequence still needs recovery for a crash between steps.

Never mutate the candidate after tests. Post-test optimization, compaction, file rewriting, masking, copying, or schema alteration creates a new physical state that needs identity and relevant validation. If promotion necessarily copies data, validate the copy result and bind its receipt to the logical candidate.

### Use shadow and canary modes honestly

A shadow run executes new logic on representative inputs without becoming authoritative. Suppress notifications, external API calls, irreversible writes, billing, and downstream triggers; route output to isolated storage. Compare against current production under declared equivalence and explain expected deltas. Shadowing observes available traffic/data, not rare future cases.

A canary makes the new version authoritative for a bounded partition, tenant, shard, time window, or reader cohort. Define allocation stability, minimum volume, guardrails, observation duration, abort thresholds, and how downstream aggregation keeps canary/control populations separate. Selection must avoid unfair or unsafe exposure.

Blue/green data rollout maintains old and new candidate generations and switches readers. It works when both remain compatible and storage/compute cost is acceptable. Dual-read compares results but can double load; dual-write introduces consistency and replay complexity. Neither pattern eliminates migrations or consumer contracts.

Automated rollback is safe only for a narrow, rehearsed class of failures. A latency regression before any durable effects may revert traffic. A semantic defect that wrote shared state usually needs freeze, containment, reconciliation, and a reviewed repair. Encode which alerts authorize automation and which summon an incident owner.

### Separate software rollback from data recovery

Inventory effects: immutable dataset publication, mutable updates/deletes, emitted events, checkpoints, caches, indexes, feature values, notifications, external calls, access changes, and consumer copies. For each, choose a recovery mechanism and retention horizon.

Pointer rollback can repoint readers to a prior immutable generation if it still exists and remains schema-compatible. Snapshot restoration reconstructs storage but may discard legitimate concurrent writes. Reverse migration attempts to undo transformations and is often lossy. Compensation appends correcting facts/effects. Forward repair computes a new correct generation from trusted inputs and preserves the defective generation for audit.

Choose by semantics, not instinct. If consumers already acted on wrong events, hiding the source table does not undo their actions. If later correct writes coexist with corrupted ones, restoring an old snapshot may cause new loss. Freeze further publication, identify affected scope, communicate contracts, and reconcile each consumer.

Record recovery readiness in admission: prior compatible artifact and binding, retained source data/snapshot, restore time, forward-repair job, consumer notification, authority, and tested date. A release can knowingly accept limited rollback, but that is a risk decision rather than an implied property of the deployment tool.

### Preserve provenance and supply-chain evidence

Pin dependencies, base images, compiler/adapters, plugins, and generated tools. Produce a dependency inventory or SBOM where appropriate; scan known vulnerabilities and licenses under versioned policy. Verify artifact signatures and provenance at promotion. Restrict who can alter workflows, runners, registries, policies, and evidence stores.

Hermeticity is a spectrum. A build that downloads mutable packages or queries live metadata can vary. Record every external input, cache key, and resolver; prefer content-addressed inputs and controlled builders. Reproducible builds provide additional confidence when independent builds match, but nondeterminism should be explained rather than normalized away.

Supply-chain evidence does not prove transformation correctness. Conversely, perfect unit tests do not prove the deployed artifact came from reviewed source. Admission composes both. Protect the composition point from confused-deputy attacks: policy must verify repository, branch/review, builder identity, subject digest, environment, and authorization.

### Retain an auditable evidence bundle

Use a versioned schema. Store identities rather than ambiguous names: revision, artifact, compiled graph, policy, configuration, migration, input/reference, candidate, and parent/current generation. Include impact seeds/closure/exclusions, required/observed gates, every attempt, warnings/waivers, approvals, timestamps, and publication receipt.

Make evidence queryable by both release and dataset generation. Operators investigating a table should find the release; reviewers inspecting a release should find its outputs and consumers. OpenLineage events can connect runs, jobs, and datasets, while the release system adds review, policy, provenance, and publication decisions.

Control access and retention. Evidence can include schema names, code, vulnerabilities, business metrics, failing rows, or sensitive identifiers. Store diagnostic samples separately when necessary, use stable references, and preserve integrity without retaining prohibited data. Test retrieval periodically; an unreadable archive is not assurance.

Measure the system: selection false negatives found by full runs, escaped defects by missing gate, flaky/error rates, queue and execution time by risk tier, waiver count/age, migration failure/recovery time, candidate-to-publication delay, rollback/repair readiness, and evidence reconstruction success. Optimize bottlenecks without weakening unnamed obligations.

## Definitions and Notation

Let:

- $S$ be a reviewed source revision and $\Delta(S,S_0)$ its difference from accepted base $S_0$;
- $G=(V,E)$ be a versioned dependency graph with nodes for assets, jobs, contracts, policies, and consumers;
- $C_0$ be seed nodes directly implicated by change classification;
- $I^*$ be the conservative fixed-point impact closure;
- $A$ be an immutable built artifact and $h(A)$ its content digest;
- $B$ be an immutable effective environment-binding manifest;
- $Q$ be identified source/reference input generations;
- $D$ be one or more isolated candidate data generations;
- $c=(S,h(A),B,Q,D)$ be the candidate identity tuple;
- $r$ be a release-policy version;
- $R(c,I^*,\Delta,r)$ be the complete set of applicable required gates;
- $o_g(c)$ be the observed result for gate $g$ bound to $c$;
- $M$ be migration state and evidence;
- $P$ be the expected current parent generation; and
- $\pi(c,P)$ be a conditional publication producing a receipt or conflict.

Define downstream closure over explicit edges as

$$
\operatorname{desc}_G(C_0)=\{v\in V:\exists c\in C_0\text{ and a directed path }c\leadsto v\}.
$$

Because $G$ may omit dynamic or organizational dependencies, define an uncertainty expansion $U(\Delta,G,L)$ using compiled artifacts and observed lineage $L$. Then

$$
I^*=C_0\cup\operatorname{desc}_G(C_0)\cup U(\Delta,G,L).
$$

This notation deliberately permits over-selection. Soundness requires every actually affected node be in $I^*$; minimality is an optimization objective, not a correctness precondition.

Gate completeness is

$$
\operatorname{complete}(c,R)\iff
\forall g\in R,\ \exists!\,o_g:
o_g.\operatorname{candidate}=c
\land o_g.\operatorname{fresh}
\land o_g.\operatorname{policy}=r.
$$

The unique result requirement prevents a decision from silently choosing among conflicting attempts. A retry policy must nominate the authoritative attempt while retaining history.

Compatibility is directional. Write $x\rightsquigarrow_R y$ when reader version $R$ can interpret data written under representation $x$ as intended under $y$. Encoding compatibility is weaker than semantic compatibility. A window $W=[t_e,t_c)$ begins at expansion and ends only after adoption evidence permits contraction.

Let $E_D$ be durable data/external effects of deployment. Software rollback $A_1\to A_0$ does not imply $E_D\to E_{D0}$. Recovery is a separately verified function

$$
\rho(E_D,Q,\text{history})\to(E_D',\text{receipt})
$$

whose postconditions include reconciliation and consumer handling.

## Mechanisms, Invariants, or Proof Structure

The assurance argument is a chain. Each link has a concrete failure consequence.

1. **Change completeness.** The reviewed diff and resolved/generated differences classify every behavior-bearing surface. If packages, reference data, policies, or runtime change outside classification, impact and gates are unsound.
2. **Graph conservatism.** Seed nodes plus explicit descendants plus uncertainty expansion contain every affected producer and consumer. If a hidden edge is missed, selected CI can pass while an untested consumer breaks.
3. **Candidate identity.** Source, artifact, bindings, inputs, migrations, and candidate data are immutable and joined. If any component floats, test evidence can describe another release.
4. **Gate derivation.** Versioned policy deterministically maps risk and impact to a complete required set. If discovery failure looks like zero tests, admission is unsafe.
5. **Evidence validity.** Each required gate ran against the candidate, produced one authoritative fresh result, and retained diagnostic evidence. Skip, cancellation, infrastructure error, or stale cache is not pass.
6. **Compatibility and migration safety.** Active producer/consumer/state versions coexist through a deliberate window, and migration operations are resumable and reconciled. Without this link, a locally correct version can fail during mixed deployment.
7. **Isolation and least privilege.** CI and prepublication candidates cannot accidentally mutate authoritative state or leak protected data. Without enforcement, validation can itself cause the incident.
8. **Conditional publication.** The reviewed candidate becomes current only if expected parent, policy, migration, and approval still match. Without compare-and-set behavior, a stale successful run can overwrite a newer release.
9. **Recovery sufficiency.** Code and every durable effect have a compatible restore, compensation, or forward-repair plan. Without this link, “rollback available” is a UI label rather than an operational property.
10. **Traceability.** The publication receipt and dataset lineage point back to the evidence bundle. Without traceability, incident reconstruction and audit cannot establish what was accepted.

The conclusion is bounded: under complete change discovery, conservative dependencies, correct policy, representative oracles, enforced environment controls, and truthful evidence, the system justifies promotion of the identified candidate. It does not prove correctness for unknown future inputs, undiscovered consumers, compromised builders, wrong domain contracts, or untested platform behavior.

An impact selector should satisfy monotonicity: adding a changed seed or dependency edge must not remove previously selected nodes. Its cached output must be keyed by change, graph, lineage, classifier, and policy versions. When one input is unavailable, the selector returns an error or broader set, never an empty success.

An evidence cache is reusable only if the gate definition, artifact/candidate-relevant inputs, tool version, environment class, and freshness policy match. A unit result may be content-addressed broadly; a production-binding policy check or data reconciliation cannot be reused across different bindings or input generations merely because source is identical.

The following executable model demonstrates a small conservative closure and fail-closed gate decision. It does not discover real SQL lineage, validate a data system, or prove production isolation.

<!-- bijux-verify: {"id":"impact-and-gate-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"changed_nodes=(\u0027orders_clean\u0027,)\nimpacted_nodes=(\u0027orders_clean\u0027, \u0027report\u0027, \u0027sales\u0027)\nrequired_checks=(\u0027consumer:report\u0027, \u0027contract:orders_clean\u0027, \u0027integration:sales\u0027, \u0027reconciliation:sales\u0027, \u0027unit:orders_clean\u0027, \u0027unit:sales\u0027)\npassing_checks=6\nmissing_checks=()\ndeploy_allowed=True\nunaffected_nodes=(\u0027orders_raw\u0027, \u0027rates\u0027)\nproduction_data_used=False\nartifact_digest_bound=True\nrollback_requires_data_plan=True\n","stderr":""}} -->
```python

graph = {
    "orders_raw": (),
    "orders_clean": ("orders_raw",),
    "rates": (),
    "sales": ("orders_clean", "rates"),
    "report": ("sales",),
}

changed = ("orders_clean",)


def downstream_closure(dependencies, seeds):
    impacted = set(seeds)
    grew = True
    while grew:
        before = len(impacted)
        for node, parents in dependencies.items():
            if any(parent in impacted for parent in parents):
                impacted.add(node)
        grew = len(impacted) != before
    return tuple(sorted(impacted))


checks_by_node = {
    "orders_clean": ("contract:orders_clean", "unit:orders_clean"),
    "sales": ("integration:sales", "reconciliation:sales", "unit:sales"),
    "report": ("consumer:report",),
}

impacted = downstream_closure(graph, changed)
required = tuple(sorted({gate for node in impacted for gate in checks_by_node[node]}))
observed = {gate: "passed" for gate in required}
missing = tuple(gate for gate in required if observed.get(gate) != "passed")
unaffected = tuple(sorted(set(graph) - set(impacted)))

print(f"changed_nodes={changed}")
print(f"impacted_nodes={impacted}")
print(f"required_checks={required}")
print(f"passing_checks={sum(result == 'passed' for result in observed.values())}")
print(f"missing_checks={missing}")
print(f"deploy_allowed={not missing}")
print(f"unaffected_nodes={unaffected}")
print("production_data_used=False")
print("artifact_digest_bound=True")
print("rollback_requires_data_plan=True")
```

The expected output reports changed node `orders_clean`; impacted nodes `orders_clean`, `report`, and `sales`; the six required checks in sorted order; six passing checks; no missing checks; deployment allowed; unaffected nodes `orders_raw` and `rates`; no production data used; artifact digest bound; and a required data-aware rollback plan.

## Alternatives and Trade-Offs

**Full graph versus selected CI.** Full builds reduce selection risk and expose composition, but consume time, compute, quota, and scarce environments. Selected CI accelerates feedback and enables parallel work, but its validity depends on complete graph/change discovery and immutable parent reuse. Use selected checks on ordinary changes, widen for uncertainty/high risk, and run periodic full comparisons to measure misses.

**Ephemeral fixtures versus production-like subsets.** Synthetic fixtures give known oracles, privacy control, and boundary precision. They can miss scale, skew, rare combinations, and platform behavior. Production-derived subsets improve realism but introduce approval, minimization, linkage, retention, and leakage risk and may still lack known answers. Combine synthetic semantics with governed scale/distribution tests.

**Mocks versus actual infrastructure.** Mocks localize logic and run quickly. They cannot reproduce SQL semantics, catalog permissions, storage commits, distributed ordering, locks, quotas, or failure modes. Keep pure tests broad and integration environments narrow but representative.

**Schema registry enforcement versus consumer-driven contracts.** Central schemas provide discoverability and uniform checks. They may validate encoding while missing business meaning or unregistered consumers. Consumer-owned suites capture actual expectations but can become slow, flaky, or unavailable. Use a producer contract baseline plus registered critical consumer evidence and deprecation governance.

**Rebuild versus defer/reuse.** Rebuilding parents maximizes environmental consistency but costs time and may require large source copies. Reusing immutable production/staging parents is efficient, but differences in access, freshness, schema, macros, policies, or semantics can invalidate results. Record exact generations and compatibility, and rebuild when relevant parents or environment behavior changed.

**Shadow versus canary.** Shadow execution avoids authoritative exposure but may suppress behaviors and cannot reveal all consumer effects. Canary deployment tests real authority for a limited cohort but exposes some users/data and complicates reconciliation. Choose according to reversibility, partitionability, and harm.

**Blue/green versus in-place migration.** Blue/green preserves a known generation and supports atomic reader switching but doubles storage/compute and complicates concurrent writes. In-place migration can be cheaper but has tighter compatibility and recovery requirements. Immutable analytical outputs favor generation switching; large mutable stores may require careful expand-contract and online migration.

**Rollback versus forward repair.** Rollback is fast when effects are reversible and prior artifacts/data remain compatible. Forward repair preserves later valid work and audit history but may take longer and requires trusted replay inputs. Decide from effect semantics rather than making one method universal.

**Manual approval versus automated deployment.** Manual review can integrate domain/context judgments but adds latency and can become ceremonial. Automation is consistent and fast when policy inputs are machine-verifiable. Automate bounded facts and require accountable judgment for destructive migrations, unexplained data diffs, sensitive policy changes, or limited recovery.

**Central pipeline versus federated ownership.** Central gates standardize evidence and controls; one team can become a bottleneck and miss domain semantics. Federated suites preserve consumer/domain ownership but risk inconsistent quality. A shared evidence/gate schema with domain-owned predicates supports both.

## Failure Modes and Misconceptions

- **“Only edited models need tests.”** Downstream behavior, shared macros, contracts, policies, and consumers can change without direct edits. Compute conservative closure.
- **“The lineage graph is authoritative because it is generated.”** Static graphs miss dynamic references; runtime lineage misses paths that did not execute. Version and combine evidence, then represent uncertainty.
- **“A compile proves the SQL is safe.”** Compilation proves a tool accepted syntax/references under one context. It does not prove correct rows, permissions, performance, migration, or consumer compatibility.
- **“All green checks mean all required checks passed.”** Discovery may omit gates; errors may be converted to skip; stale cached results may be attached. Compare required and authoritative observed sets.
- **“Retrying a test is harmless.”** Retry-until-green hides intermittent defects and invalidates failure-rate interpretation. Distinguish infrastructure retry from product nondeterminism and retain attempts.
- **“A signed image is the reviewed image.”** A signature authenticates an assertion about a digest. Verify builder, source, inputs, provenance, repository/review, and promotion subject.
- **“The same commit rebuilds the same artifact.”** Floating dependencies, base images, compilers, timestamps, generated inputs, and live metadata can vary. Pin and record inputs; promote by digest.
- **“Staging proves production behavior.”** Accounts, IAM, networks, keys, quotas, engine settings, scale, and data differ. Test invariants and allowed differences; use bounded production verification.
- **“Masked production data is anonymous.”** Stable tokens, rare combinations, free text, and joins can reidentify people. Apply purpose, minimization, access, retention, and expert privacy review.
- **“Read-only production access is risk-free.”** Queries can expose data, consume capacity, trigger audit costs, and leak results through logs. Authorize narrow views and enforce limits.
- **“Adding a nullable column is always compatible.”** Positional/strict readers, `SELECT *`, policies, exports, and business assumptions can fail. Test actual supported consumers.
- **“Dual write guarantees a safe migration.”** Partial failure, ordering, retry, and divergence create two truths. Define authority, reconciliation, repair, and exit criteria.
- **“Shadow output cannot cause harm.”** Notifications, callbacks, shared caches, locks, billing, or downstream discovery can still fire. Suppress and isolate every side effect.
- **“Canary means ten percent of rows.”** Row sampling may split entities, corrupt aggregates, or expose sensitive cohorts. Canary on a stable semantic boundary with explicit reconciliation.
- **“Rolling back code restores data.”** Persisted writes and consumer actions remain. Use pointer restore, snapshot, compensation, or forward repair as appropriate.
- **“A snapshot makes rollback safe.”** Restore can erase legitimate concurrent writes, violate newer schemas, or miss external effects. Test scope, compatibility, and reconciliation.
- **“A warning is almost a pass.”** Warning is a policy outcome with an owner and response. It cannot satisfy a blocking obligation by presentation color.
- **“A waiver is permanent documentation.”** Waivers must name scope, reason, approver, compensating control, expiry, and removal. Unbounded waivers silently redefine policy.
- **“A data diff explains itself.”** Expected business changes and defects can have identical counts. Compare keys/dimensions, annotate expected deltas, and obtain domain ownership.
- **“More CI jobs mean more assurance.”** Duplicate weak checks create noise. Trace gates to failure claims and escaped defects, then test reconstruction and recovery.

## Worked Examples

### Example 1

A tax-rate mapping changes. No transformation file imports it syntactically because the mapping is loaded from a governed table. Change classification identifies reference data, seeds all readers recorded in contracts and runtime lineage, and selects their downstream reports. CI pins old and proposed rate generations, runs exact effective-date boundaries, computes value movement by jurisdiction, and obtains owner approval for expected deltas. Treating the change as “no code diff” would have selected nothing.

### Example 2

A shared `normalize_currency` macro changes rounding from half-up to half-even. The compiled manifest shows 38 dependent models. Column lineage is incomplete for generated expressions, so the selector widens to every macro consumer and their financial descendants. Unit boundaries cover halfway values; integration uses the production decimal type; reconciliation reports per-currency movements. Unaffected nonfinancial branches reuse immutable parent generations by digest.

### Example 3

A producer adds nullable `campaign_id`. Registry validation calls it backward-compatible, but one CSV export uses positional columns and a dashboard issues `SELECT *`. Consumer-driven checks fail both. The release changes the export to an explicit column order, updates the dashboard contract, deploys tolerant readers, then adds the field. Compatibility depends on operations, not the abstract schema rule alone.

### Example 4

A pull request from a fork exercises an order pipeline. CI receives synthetic identifiers, a disposable catalog, a run-scoped object prefix, and no production credentials. Network policy denies the production warehouse and event bus. Failure artifacts contain capped synthetic rows. A protected post-merge job later validates production policy bindings without executing contributor-controlled code with broad authority.

### Example 5

A migration replaces integer cents with fixed-scale decimal amounts. Expansion adds the new column; writers dual-populate under a deterministic conversion; a backfill records cursor and source generation; reconciliation compares keys and exact amounts; readers switch; adoption telemetry proves the old field unused; contraction occurs in a later release. Rollback before contraction can use the old field. After contraction, restoration or forward repair is required, so the point of no return is explicit.

### Example 6

A selected dbt build changes `orders_clean` and defers unchanged `orders_raw` and `rates` to production generations. The evidence bundle records the comparison manifest, deferred target identities, access mode, freshness, and environment differences. Because a source contract also changed, reuse is rejected and the relevant source fixture is rebuilt. Deferral is an optimization governed by compatibility, not a blanket shortcut.

### Example 7

A new recommendation feature runs in shadow mode. It reads a policy-approved replay cut, writes to an isolated candidate, disables notifications and online writes, and compares keyed scores plus ranking metrics with the accepted model. The comparison reveals expected model movement and an unexpected missing tenant. Publication blocks until lineage shows a dynamically generated tenant table was absent from impact selection.

### Example 8

A canary aggregation serves two low-risk internal tenants. Allocation is stable by tenant, not random rows, so complete tenant totals remain interpretable. Guardrails cover freshness, reconciliation, error rate, and cost for two schedule cycles. An alert freezes expansion. Because output is immutable and consumers resolve a tenant-specific pointer, the canary can restore the prior generation without discarding other tenants' work.

### Example 9

A bad release emits duplicate invoice events before detection. Reverting the producer stops new duplicates but cannot undo messages already consumed. The incident inventory identifies consumer ledgers and emails. A compensating event is safe for ledger consumers, while customer communication requires case review. The release record connects emitted event ranges to artifact and input generations, allowing exact reconciliation.

### Example 10

A security scan passes for image digest `sha256:a`. A deployment script rebuilds from the same commit and pushes mutable tag `release`, now digest `sha256:b` after a base-image update. Admission rejects the deployment because test, provenance, and scan evidence bind `a`. The correct response is to inspect and validate `b` or promote `a`, never to relabel evidence.

## Cross-Program Connections

Software engineering contributes hermetic builds, dependency locking, unit/integration testing, artifact repositories, feature flags, and deployment automation. Data engineering extends these with graph impact, mutable inputs, materialized generations, consumer schemas, historical repair, and semantic reconciliation.

Distributed systems explains why publication and migration need operation identities, idempotency, compare-and-set transitions, and reconciliation after unknown outcomes. A CI service reporting timeout cannot tell whether a catalog pointer changed; safe retry depends on durable state, not process memory.

Database engineering contributes schema compatibility, online migration, isolation, locks, write-ahead history, snapshots, and restore behavior. Analytical object tables may use immutable snapshots while operational stores require expand-contract and careful mutable-state migration; the recovery model must match storage semantics.

Security engineering contributes provenance, signing, least privilege, protected branches/environments, secret isolation, runner trust, policy enforcement, and audit. A supply-chain control proves origin/integrity claims; data tests prove different semantic claims. Both must join at admission.

Privacy engineering contributes purpose limitation, data minimization, synthetic generation, masking/tokenization analysis, access/retention/deletion, and reidentification assessment. Test realism never grants automatic authority to copy production data.

Site reliability engineering contributes progressive delivery, service-level signals, canary guardrails, incident response, rollback criteria, capacity protection, and recovery drills. Data systems add delayed correctness signals and persistent data effects, making forward repair and consumer reconciliation central.

Formal methods contribute fixed-point closure, monotone selection, invariants, pre/postconditions, and evidence composition. The notation clarifies assumptions; it does not remove the need for domain-authoritative contracts or empirical platform tests.

Governance and product management contribute ownership, compatibility commitments, deprecation communication, approval, waiver expiry, and acceptable risk. “Automatically deploy” remains an organizational policy expressed through machine-verifiable and human-reviewed predicates.

## References

1. dbt Labs. [Node selection methods: state](https://docs.getdbt.com/reference/node-selection/methods#state). Accessed 2026-09-03. Primary documentation for selecting resources by comparison with a prior manifest.
2. dbt Labs. [Defer](https://docs.getdbt.com/reference/node-selection/defer). Accessed 2026-09-03. Primary documentation for resolving references to unselected upstream resources in another environment.
3. dbt Labs. [Unit tests](https://docs.getdbt.com/docs/build/unit-tests). Accessed 2026-09-03. Primary documentation for validating model SQL logic against small static inputs.
4. dbt Labs. [Data tests](https://docs.getdbt.com/docs/build/data-tests). Accessed 2026-09-03. Primary documentation for assertions represented by queries returning failing records.
5. Apache Airflow. [Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html). Accessed 2026-09-03. Primary documentation covering idempotent tasks, partition-specific processing, DAG loading, and operator testing.
6. Apache Beam. [Test your pipeline](https://beam.apache.org/documentation/pipelines/test-your-pipeline/). Accessed 2026-09-03. Primary documentation for testing functions, transforms, and complete pipelines with known inputs and outputs.
7. OpenLineage. [About OpenLineage and its specification](https://openlineage.io/docs/). Accessed 2026-09-03. Primary project documentation for extensible run, job, and dataset lineage metadata.
8. SLSA. [Provenance](https://slsa.dev/spec/v1.2/provenance). Accessed 2026-09-03. Primary specification for describing an artifact's build process, materials, and subject identity.
9. Apache Iceberg. [Branching and Tagging](https://iceberg.apache.org/docs/latest/branching/). Accessed 2026-09-03. Primary documentation for named snapshot references used by audit and experimental workflows.

## Exercises

### Exercise 1

A pull request changes a shared date macro, one model description, an access-policy tag, and the warehouse adapter lock. Design the seed set and uncertainty expansion for impact analysis. State which elements cannot safely be classified as documentation-only and why.

### Exercise 2

A pipeline reports five executed gates, all passed. Policy requires schema, unit, integration, reconciliation, consumer, security, and provenance gates. The consumer gate was skipped due to unavailable infrastructure, and provenance refers to a different image digest. Compute the admission result and specify the evidence corrections required.

### Exercise 3

Design an expand-contract release for renaming `customer_tier` to `service_tier` when two registered readers update quickly, one monthly extract updates slowly, and unknown ad hoc queries may use `SELECT *`. Include compatibility tests, adoption evidence, contraction criteria, and recovery.

### Exercise 4

A canary transformation wrote incorrect balances for one tenant and emitted settlement messages. The prior table snapshot exists, but valid balance updates occurred after the canary. Decide among code rollback, snapshot restore, compensation, and forward repair. Define the reconciliation evidence needed before closing the incident.

### Exercise 5

For the executable graph, add an `audit_export` node that depends dynamically on `orders_clean` but is absent from the declared graph. Explain how compiled inspection, runtime lineage, an uncertainty rule, and periodic full-build comparison could discover or contain the omission. State what happens when lineage is unavailable.

## Answers to the Exercises

### Answer 1

Seed every model that compiles through the shared date macro, every resource whose authorization semantics depend on the access-policy tag, and every node built through the changed adapter. The description is documentation-only only if tags/metadata generation and external contracts do not derive behavior from it. The macro is semantic because date boundaries can change outputs; the policy tag is behavioral because access can change without dataflow; the adapter can affect compilation, types, transactions, quoting, and runtime behavior across the graph. Compare generated manifests/plans and widen to all adapter-built nodes unless verified compatibility supports a narrower set.

### Answer 2

Admission is false. The required set has seven gates, but only five valid passes are reported; skipped consumer evidence is not a pass, and provenance bound to another digest is invalid for this candidate. Run the consumer suite or obtain a narrow authorized, expiring waiver under policy; generate/verify provenance whose subject equals the promoted image digest; then recompute completeness so every required gate has one fresh authoritative result. Merely relabeling the skip or copying the other digest's attestation would corrupt evidence.

### Answer 3

First add `service_tier` while retaining `customer_tier`, define their equality/mapping invariant, and publish both through explicit views/contracts. Test old readers on new rows and new readers on historical rows. Update the two fast readers, then the monthly extract; measure query/column usage where reliable and obtain registered consumer acknowledgement. Because unknown `SELECT *` consumers exist, maintain the old column through a communicated deprecation window and provide a compatibility view rather than infer safety from silence. Backfill the new field with an identified resumable operation and reconcile keys/values. Contract only after the extract has completed successfully, observation/retention windows pass, usage evidence is acceptable, and the owner accepts residual unknown-consumer risk. Before contraction, rollback can return writers/readers to the old field; after contraction, retain a restoration migration or compatibility view and the source needed for forward repair.

### Answer 4

Roll back or disable the faulty code immediately to stop new damage, but do not restore the old snapshot over valid later updates. Compute the exact affected tenant/key/time/event scope from release and lineage records. Forward-repair balances from trusted immutable inputs while preserving later valid writes, using version/compare conditions; issue idempotent compensating settlement messages for consumers whose contract supports them and coordinate exceptions with settlement owners. Reconcile source occurrences, current balances, repaired keys, duplicate/compensation event identities, every consumer acknowledgement, and financial controls. Preserve the defective generation and incident receipts under policy. Snapshot restore would be appropriate only to an isolated generation or if no valid concurrent changes/external effects existed.

### Answer 5

Compiled SQL or generated manifests may reveal the dynamic relation if the name resolves during compilation. Runtime read events can add an observed `orders_clean -> audit_export` edge, with version/freshness and coverage recorded. An uncertainty rule can conservatively seed every export when shared dynamic discovery code changes or when a node reads from the relevant namespace. Periodic full builds compare selected-CI outcomes with the complete graph and turn a discovered selection miss into a regression fixture for the selector. If lineage or compilation is unavailable or ambiguous, selection widens to the safe export set or blocks; it must not interpret missing evidence as no dependency.
