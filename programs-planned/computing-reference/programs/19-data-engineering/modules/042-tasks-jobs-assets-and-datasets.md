---
module_id: DE-042
program: Data Engineering
level: 1
module_number: 42
title: Tasks, Jobs, Assets, and Datasets
status: complete
last_verified: 2026-09-03
---

# Tasks, Jobs, Assets, and Datasets

## One-Page Review

### Governing question

How should a data platform distinguish units of executable work from durable data products and concrete data generations so that identity, state, lineage, recovery, ownership, and publication remain unambiguous?

### Essential definitions

- A **task definition** is a versioned template for one bounded unit of executable work with declared inputs, outputs, parameters, resources, side effects, and completion evidence.
- A **task instance** is one logical invocation of a task definition within a particular job run, partition, or dynamic mapping key.
- An **attempt** is one physical execution try for a task instance. One task instance may have several attempts without becoming several logical invocations.
- A **job definition** composes task definitions or selects asset work into one parameterized unit of submission, execution, monitoring, authorization, and operational intent.
- A **job run** is one occurrence of a job definition, bound to a definition version, input scope, parameters, environment, trigger provenance, and expected outputs.
- An **asset definition** identifies a durable logical data product, its owner, contract, partitions, dependencies, policy, and production rule independently of any one execution.
- A **materialization** is evidence that an execution produced or updated a particular asset partition as a specific generation.
- A **dataset definition** identifies a discrete collection of data with address, schema/semantic contract, access policy, and lifecycle. The term is system-specific and may describe a table, object, directory, stream, view, or logical collection.
- A **dataset generation** is an immutable or reconstructibly identified version/snapshot of a dataset or partition used as an input or output.
- A **result** is a value returned between executable units; an **artifact** is a persisted execution output such as a log, report, model file, or checkpoint. Neither is automatically a governed data asset.
- **Definition state** concerns versions and availability of templates/contracts; **run state** concerns execution progress; **data state** concerns existence, completeness, quality, publication, and supersession of produced data.
- **Lineage** connects activities such as task attempts/job runs to entities such as input and output dataset generations, then projects those observations onto stable asset identities.

### Central model, mechanism, or theorem

Use distinct identities for definition and occurrence layers:

$$
j_r=(j, v_j, scope, params, env, trigger),
$$

$$
t_i=(t, j_r, mapkey, partition),
$$

$$
a_{i,k}=(t_i,k,worker,start,end,outcome),
$$

where $j$ and $t$ are job and task definitions, $j_r$ is one job run, $t_i$ is one logical task instance, and $a_{i,k}$ is its $k$th physical attempt. A data publication record is

$$
m=(asset, partition, generation, producer, inputs, contract, evidence),
$$

where producer names the successful authoritative attempt and inputs name exact dataset generations.

The identity chain is usually one-to-many:

$$
job definition
to job runs
to task instances
to attempts,
$$

while one asset definition has many materializations and dataset generations over partitions and time. These chains intersect through explicit production and consumption links; they are not interchangeable. A task can succeed without materializing an asset, one task can materialize several assets, one asset can require several tasks, and a job can complete while a nonblocking asset check warns.

### Critical invariants

- Definitions, versions, runs, task instances, attempts, assets, materializations, datasets, and generations have distinct stable identifiers.
- Only run/instance/attempt objects carry execution state; a definition is versioned, enabled, deprecated, or unavailable rather than “succeeded.”
- Retries append attempts to the same task instance unless the logical scope or inputs change.
- Every job run freezes the job/graph version, scope, parameters, environment, identity, and expected outputs.
- Task boundaries align with coherent side effects, recovery, observability, resource, and ownership boundaries.
- Job boundaries express one reviewable operational intent and do not become a miscellaneous container for unrelated products.
- An asset key persists across materializations, while each published generation is separately addressable and attributable.
- A materialization names exact producer attempt, input generations, partition, code/contract version, quality evidence, and publication state.
- Dataset identity, schema, grain, partition, completeness, mutability, access, retention, and generation rules are explicit.
- Success of an attempt or job is not substituted for data acceptance or consumer-visible publication.
- Dynamic mapping keys and partition identities are stable enough to distinguish replay from new logical work.
- Logs, metrics, credentials, parameters, lineage, and data generations respect tenant and sensitivity boundaries.

### Common failures

Common failures include calling definitions, instances, and attempts all “jobs”; giving retry attempts new logical identities; storing state on mutable task definitions; treating a worker process as the task; making every helper function a task; placing an entire day-long workflow in one opaque task; grouping unrelated assets in one job because they share a schedule; equating a table name with a dataset generation; treating a task return value as a durable asset; counting an asset twice because two systems observe the same materialization; declaring a job successful when expected outputs are absent; declaring data valid because a process exited zero; overwriting an asset without generation evidence; assigning one owner to executable infrastructure and assuming that owner also owns data semantics; using timestamps as identities; exposing secrets or cross-tenant dataset names in parameters and lineage; and adopting tool-specific nouns without defining their local semantics.

### Compact example

A versioned daily-sales job contains three task definitions: extract, normalize, and publish. Two job runs create six task instances. The first run’s normalize instance has a failed attempt followed by a successful attempt, so the ledger contains seven attempts but still only six task instances. Both publish instances materialize the same logical asset key, sales/daily, for different partitions. They create distinct dataset generations g101 and g102 with 120 and 132 rows. The stable asset is not either physical generation, the two attempts are not two normalization tasks, and the sum 252 describes rows across two materializations rather than the current size of a mutable table.

### Connections

[DE-041](041-directed-acyclic-graphs-and-dependencies.md) defined typed dependency edges and exact generation binding. This module supplies the node and occurrence vocabulary. DE-043 attaches schedules and events to definitions without confusing trigger time with run identity; DE-044 specifies retries for attempts and idempotency for side effects; DE-045 specializes assets and dataset generations by partition; DE-049 develops run metadata and operational state.

## Governing Question

What exactly succeeded, what durable data now exists, and which identity should a retry, consumer, operator, or auditor use?

A dashboard saying “daily_sales succeeded” is ambiguous. It might refer to a reusable workflow definition, one run for a data interval, a worker process, the last attempt of a normalization step, a table write, a logical sales asset, or a quality-approved published generation. These objects have different lifecycles and different owners. Collapsing them into one word makes recovery and audit unsafe.

Consider a retry. If a physical attempt loses its worker after committing output, the platform needs the stable task-instance identity and side-effect identity to reconcile the outcome. Treating the retry as a new logical task can duplicate writes. Conversely, if the requested partition or input generation changed, reusing the old task-instance identity hides new work. The boundary between instance and attempt must be designed, not inferred from process IDs.

Consider a consumer. It needs a dataset generation satisfying a contract, not merely the run status of the code that normally produces it. A successful task might decide there was no work, write only a candidate, produce a degraded output, or be superseded by another publisher. The producer activity and produced entity need separate evidence.

The same distinction supports organizational clarity. A platform team may own the job runner and task runtime; a data-domain team owns the sales asset’s semantics; a warehouse team owns the dataset storage service; a security team owns access policy. “Owner: data platform” on every object hides accountable decisions.

The governing question is therefore an identity question before it is a tooling question. Define the local ontology, map vendor concepts to it, and require every state transition and lineage event to name the correct layer.

## Why This Matters

Operational systems act on identities. Cancellation targets a run or attempt. Retry policy targets a task instance. Authorization targets a job submission and dataset access. Lineage connects a producer occurrence to an output generation. Retention deletes physical generations or execution evidence. If identifiers blur these layers, automated actions affect the wrong thing.

Granularity determines recovery cost. A monolithic task hides which stage committed and forces broad replay. Extremely fine tasks create scheduling overhead, large metadata volume, fragile interfaces, and many partial states. Good boundaries isolate meaningful side effects or expensive work while keeping internal pure computation inside ordinary code where possible.

Job boundaries determine operational intent. One job run should answer a coherent question such as “materialize daily sales for tenant T and business date d under bundle b.” If a job contains unrelated products merely because they run nightly, one failure obscures which obligation failed, ownership becomes ambiguous, and selective execution becomes difficult.

Asset identity lets data outlive its implementation. A sales dataset might move from a SQL query to a Spark job without becoming a new business product. Its contract may evolve through compatible versions while materializations retain exact code and input lineage. Consumers can reason about the stable product and select a compatible generation.

Dataset generations make reproducibility and concurrency possible. Mutable names such as current_sales are convenient discovery handles, but they do not identify what a run read. An immutable generation, snapshot token, object-version manifest, or transactionally stable table version lets retries and downstream runs bind the same content.

Lineage quality depends on separating activities from entities. W3C PROV-O distinguishes activities that use and generate entities. OpenLineage similarly models Job, Run, and Dataset, including design-time and runtime events. A graph that contains only job-to-job arrows loses the exact data versions; one with only dataset-to-dataset arrows can lose the execution, code, and actor that caused a derivation.

Metrics also change meaning by layer. Task-attempt failure rate measures physical tries. Task-instance success rate measures logical units. Job-run completion measures workflow occurrences. Asset freshness measures a data product. Dataset-generation quality measures concrete data. Mixing denominators can make reliability look better or worse without any system change.

Finally, security boundaries differ. A worker identity may need temporary read/write authority, while the job submitter may only request a governed operation and consumers may only read approved generations. Parameters, logs, result payloads, lineage, and dataset locations can each carry sensitive data. Explicit layers allow least privilege and appropriate retention.

## Prerequisites and Retrieval

Retrieve the current workflow and graph definitions; task/operator/step templates and code versions; job/flow/DAG definitions and selection rules; run, task-instance, attempt, worker, and executor records; dynamic mapping keys; partition/data-interval semantics; parameter schemas and resolved values; environment and deployment identities; input/output dataset catalogs; asset/product registry; schemas, grain, key, quality, freshness, access, ownership, and retention contracts; storage paths, table identifiers, object versions, snapshot tokens, and manifests; materialization and publication records; lineage events; quality checks; side-effect/idempotency keys; retry/cancellation behavior; caches and reused results; external jobs and nested workflows; multi-output and multi-step production mappings; observability dashboards and alert denominators; security principals and delegated credentials; incident evidence; and terminology used by each integrated tool.

Distinguish definition from occurrence; job definition from job run; task definition from task instance; task instance from attempt; attempt from worker/process/container; task from helper function; job from schedule; run trigger from data interval; run parameters from ambient configuration; success from acceptance; returned result from persisted artifact; artifact from asset; asset definition from materialization; asset partition from dataset partition; logical dataset from physical location; dataset definition from generation; generation from mutable alias; source dataset from source-reading task; multiple outputs from duplicate observations; one multi-output computation from several independent producers; cache hit from new execution; reused generation from new materialization; selection from ownership; platform ownership from domain ownership; and lineage observation from authoritative publication.

Create a local ontology table:

| Object | Stable identity and version | Occurrence identity | State/evidence | Owner |
|---|---|---|---|---|
| Task | Name, namespace, code/interface version | Job run + task key + map/partition key | Instance state and ordered attempts | Implementation/operator owner |
| Job | Name, namespace, graph/parameter version | Run ID + logical scope | Run lifecycle, selected work, terminal derivation | Workflow/service owner |
| Asset | Asset key + contract version | Materialization ID + partition | Quality, freshness, publication, supersession | Data-product/domain owner |
| Dataset | Dataset key/location + schema/semantic version | Generation/snapshot/partition ID | Completeness, contents, access, retention | Data/storage steward |
| Attempt | Task-instance ID + attempt number | Worker execution ID if separate | Start/end/outcome/logs/resources/side effects | Runtime plus task owner |

Then map each platform’s nouns to the table. Do not force exact equivalence. In one tool a “job” may mean the top-level workflow; in another it may mean one engine submission launched by a task. Preserve native identifiers and record parent-child mappings.

Write a falsifiable production claim: “Job run R of definition J version 4 selected tenant A/day d and instantiated task T once under dynamic key d. Attempts 1 and 2 belong to that same instance. Attempt 2 produced candidate generation G from inputs I, materialization M binds G to asset partition P under contract 3, checks Q passed for G, and publication U made G current from expected parent G0.”

## Learning Objectives

After completing this module, you should be able to:

1. define task, task instance, attempt, job, job run, asset, materialization, dataset, and dataset generation without conflating their identities;
2. map vendor-specific workflow and lineage concepts into a local ontology while retaining native identifiers;
3. choose task granularity from side effects, recovery, observability, cost, resource, ownership, and interface boundaries;
4. choose job boundaries that express coherent operational intent, selection, parameters, authorization, and outcome;
5. design stable asset keys and contracts that survive implementation and storage changes;
6. identify dataset generations, partitions, schemas, completeness, mutability, access, and retention precisely;
7. model one-to-many and many-to-many relationships among runs, instances, attempts, materializations, and generations;
8. derive job and asset outcomes without replacing data evidence with execution state;
9. record complete activity-to-entity lineage for nested, dynamic, cached, multi-output, and externally executed work; and
10. test and govern identity, state transitions, ownership, security, metrics, migration, and decommissioning across the model.

## Core Exposition

### Define a task at the orchestration boundary

A task is a logical executable unit whose occurrence the orchestrator can identify, observe, and act upon. Its definition should declare input references, output expectations, parameter schema, code/runtime version, resource class, credentials, side-effect identity, timeout/retry class, and completion evidence. It need not be one operating-system process: an executor may launch a container, submit a remote query, start a Spark application, or call an API.

Do not turn every function into a task. Pure helpers often belong inside one task’s code, where ordinary language tooling provides testing and composition without orchestration overhead. A useful task boundary normally has at least one reason to exist: an independently retryable side effect, expensive or specialized resources, a durable intermediate, distinct ownership, a security boundary, meaningful observability, or reusable orchestration composition.

Avoid the opposite extreme. A task that extracts, validates, transforms, publishes, and notifies over many hours may leave an unknown partial state after failure. Operators cannot retry only the safe portion, lineage cannot attribute intermediate products, and capacity cannot schedule stages separately. Split at durable or reconciliable boundaries.

“Atomic task” is contextual. Prefect describes tasks as atomic units with transactional semantics, but no general orchestrator can make arbitrary external systems participate in one database transaction. Here atomic means one logical orchestration/recovery unit with explicitly managed side effects, not universal all-or-nothing execution.

### Separate task definition, instance, and attempt

The task definition is reusable and versioned. It has no run outcome. A task instance binds that definition to one job run and logical scope: partition, map key, shard, tenant, or selected item. An attempt is one physical try for that instance.

If normalization for day d fails once and succeeds on retry, the system should normally show one instance with two attempts. Logs, worker IDs, start/end times, resource use, and failure details belong to attempts. The final logical state belongs to the instance and is derived under retry/cancellation policy.

New inputs or a changed partition generally create a new logical instance or run revision, not another attempt. Otherwise the same instance identity refers to different obligations. A lost acknowledgement after a side effect should remain the same instance and operation identity while the system reconciles whether the attempt committed.

Airflow makes a comparable definition/occurrence distinction: a DAG run instantiates task instances, each associated with that run and data interval. Prefect likewise distinguishes task templates from task runs and states that only runs carry state. Use these as examples, not as an excuse to copy state names without local definitions.

Dynamic mapping adds a stable map key. Array index alone is unsafe if discovery order changes. Prefer a domain key or a digest over canonical discovery identity, and retain the expansion manifest. Two attempts of mapped customer c/day d must remain distinguishable from new work for customer c/day e.

### Define a job as coherent operational intent

A job definition composes tasks or selects asset work into one submit-and-monitor contract. It declares parameters, graph/selection, required inputs and expected outputs, execution environment, authorization, resource/concurrency policy, and terminal-outcome derivation. A job run binds all of these for one occurrence.

A good job boundary answers one operator question. “Build and publish tenant T’s daily sales partition d” is coherent. “Run everything at midnight” is a schedule-based bucket: its products may have different owners, failure policies, and recovery needs. Scheduling is attached later; it should not create the ontology.

The job’s terminal state is derived from its selected task instances and policy. It may be running while tasks finish, fail because a required task failed, or complete with an explicitly tolerated warning. Never infer asset readiness solely from job state. The job may not own every output, and a successful run may intentionally produce no materialization.

Nested workflows and external engine submissions create parent-child jobs/runs. A parent task might launch a Spark job, whose stages and tasks exist in a different runtime ontology. Record the parent run/task instance, child native job/run, submission operation, input/output generations, and authoritative completion source. Do not flatten all levels into one ambiguous run ID.

Kubernetes Job illustrates vocabulary collision: it is a workload controller for one-off work that manages Pods until the specified completions succeed. An orchestration job may launch a Kubernetes Job; those are two nested objects with different state machines and IDs.

### Treat an asset as a durable logical product

An asset is something the organization intends to manage as a lasting data product: a table, feature set, report dataset, model artifact, governed file collection, or other named product. Its definition includes stable key/namespace, description, owner, contract, dependencies, partitions, freshness and quality policy, access classification, retention, and production rule.

The asset is not the function that computes it. Dagster’s documentation makes this separation visible: an asset definition has a key, upstream keys, and a function responsible for computing/storing contents; one multi-asset function can produce multiple assets, and a graph-backed asset can hide several operations behind one asset. The general lesson is cardinality, not a requirement to use Dagster.

Stable asset identity should survive an implementation move when consumer meaning remains compatible. If sales/daily moves from warehouse SQL to a distributed engine, preserve the asset key and create new materialization lineage. If grain, meaning, security, or compatibility changes materially, version the contract or create a new asset rather than silently reusing the name.

Not every intermediate needs asset status. An in-memory collection between two tightly coupled functions may be an execution result. A temporary spill file is an artifact. Promote something to an asset when it needs independent ownership, discoverability, contract, lineage, quality, access, reuse, lifecycle, or recovery.

### Record materialization as an event, not the asset

A materialization says that one execution produced or updated an asset partition as a particular generation. It binds asset key, partition, generation, producer attempt/run, exact inputs, code and contract versions, quality evidence, timestamps, and publication status.

The asset has many materializations over time. A rematerialization for the same partition may create a new candidate generation, supersede a prior published generation, or reproduce equivalent content. Preserve each event and make currentness a separate, conditional publication relation.

A task success is not a materialization. The task might perform validation, emit a notification, or reuse an existing generation. A materialization event without durable output evidence is also weak. Confirm the manifest, storage commit, catalog state, and consumer-visible generation.

One attempt can materialize several assets, such as one source call producing two governed tables. One asset can require a graph of several tasks. Model both rather than assuming task-to-asset is one-to-one. When atomic publication across multiple assets is promised, provide a transaction/manifest mechanism or state the consistency boundary.

### Define dataset locally and identify its generations

“Dataset” is the most overloaded term. OpenLineage defines it abstractly as a discrete representation of data, often a database table, object, or directory, uniquely named within a namespace. Apache Beam’s PCollection is a potentially distributed bounded dataset or unbounded stream owned by one pipeline. A catalog may call a logical product a dataset, while storage tooling calls each table path a dataset.

Adopt a local definition and retain mappings. This chapter uses:

- dataset definition: a named discrete data collection and its address/contract;
- dataset partition: a governed subset under a partition rule;
- dataset generation: an immutable or reconstructibly stable version of the collection/partition;
- asset: the durable managed product identity that may be realized by one or more dataset definitions over its life.

The asset-to-dataset mapping can be one-to-one but need not be. An asset might include data plus a semantic model and documentation; one multi-region asset may have several physical datasets; a dataset may be a low-level external input not owned as an internal asset.

For each dataset specify namespace/name, physical locator or resolution rule, grain/keys, schema and semantic version, partitioning, bounded/unbounded status, mutability, completeness, ordering if contractual, quality, access, retention, and generation identity. A path without an object version or manifest is not an immutable generation.

### Distinguish result, artifact, dataset, and asset

A task result is a returned value or reference used by its caller. It may live in memory, a metadata store, or a temporary object. Keep small control metadata separate from large data payloads. Passing a path as a result does not make the referenced bytes durable or governed.

An artifact is persisted evidence or output of execution: log bundle, query plan, profile, checkpoint, model binary, report, or diagnostic sample. Some artifacts are also assets, but only if they have the corresponding ownership and contract. A debug file should not appear as a consumer-ready product.

A dataset is a data collection. An asset is a managed logical product. A materialization relates an execution to an asset and dataset generation. These categories prevent accidental publication: “function returned successfully” is not “dataset generation exists,” and “file exists” is not “asset partition is accepted.”

Store references rather than large values in orchestration metadata when appropriate, but make references immutable, authorized, expiring-aware, and resolvable. Secrets and raw records do not belong in generic task results or logs.

### Model the cardinalities instead of assuming one-to-one

Real workflows contain these relationships:

- one job definition to many job runs;
- one job run to many task instances;
- one task definition reused by many jobs or mapped instances;
- one task instance to zero, one, or many attempts;
- one attempt to zero, one, or many artifacts/materializations;
- one asset definition to many partitions and materializations;
- one materialization to one or a transactionally grouped set of dataset generations;
- one dataset generation consumed by many task attempts;
- several task attempts cooperating to produce one asset generation; and
- one executable operation producing several assets.

Represent link records explicitly. A count mismatch is then meaningful. Seven attempts do not mean seven task instances; two materializations of one asset do not mean two assets; three storage replicas do not mean three dataset generations if they represent one logical generation.

For multi-step asset production, identify the authoritative producing boundary. Internal attempts can emit intermediate lineage, while the materialization points to the final candidate/publisher and the complete input/activity chain. Do not invent multiple materializations for every observer that sees the same commit.

### Keep execution state separate from data state

Execution state can include created, queued, running, succeeded, failed, cancelled, skipped, or unknown. Data state can include absent, candidate, incomplete, quarantined, quality-rejected, accepted, published, superseded, invalidated, or deleted. The state machines interact but are not identical.

A succeeded attempt may leave data candidate-only. A failed attempt may have committed a complete generation before acknowledgement was lost. A cancelled job may leave prior accepted assets unchanged. A cached task instance may succeed without a new attempt or materialization. A materialization can later become invalidated even though its producing run remains historically successful.

Derive states from authoritative evidence. Do not rewrite a failed physical attempt to succeeded because a later attempt worked; retain both and mark the instance outcome accordingly. Do not rewrite a published generation as nonexistent when superseded; retain lineage and publication history under retention policy.

Job-run completion should enumerate expected outcomes: required materializations, intentional no-op receipts, accepted reuses, blocking checks, and notifications where they are truly part of the obligation. “All selected tasks terminal” is a control condition, not automatically fulfillment.

### Bind definitions and inputs for reproducibility

A run must freeze job definition/graph version, task definition/code versions, selected assets/tasks, parameters, environment/dependencies, identity/authorization context, data interval or partition scope, exact input dataset generations, and expected outputs. Ambient mutable configuration undermines replay.

Definition identity should combine durable human names with immutable version evidence. A content digest detects difference; a source revision and compiled manifest help explain it. Record both. Renaming without an alias/migration can split history, while reusing a name for incompatible work corrupts it.

Parameters are part of identity when they change semantics or scope. Canonicalize them, distinguish secret references from secret values, validate types/ranges, and record defaults after resolution. Do not store credentials in run manifests.

Cache keys must describe the same logical obligation: task/code version, parameters, exact inputs, partition, relevant environment, and output contract. A cache hit is evidence of reuse, not a new physical execution. Record the source generation/attempt and revalidation policy.

### Design names and versions for durable meaning

Use namespaces to avoid collision across domains, environments, tenants, and systems without encoding secrets. A useful asset key describes product meaning, not implementation or temporary sequence. A task name describes its bounded action; a job name describes its operational intent.

Keep native platform IDs alongside canonical IDs. Canonical identity supports cross-system lineage; native identity supports operator lookup. Define normalization and alias rules. Avoid joining by display label or timestamp.

Version separately:

- code/implementation version;
- task interface version;
- job graph/parameter version;
- asset contract version;
- dataset schema/semantic version;
- dataset generation/content identity; and
- platform/runtime version.

These versions change for different reasons. A code change can reproduce identical data. A reference-data change creates a new generation without code change. A compatible schema addition may not require a new asset identity. Make compatibility rules explicit.

### Express lineage across activities and entities

For each authoritative attempt, record job run and task instance, code/runtime, actor/workload identity, exact input generations, output candidate generations, materializations, quality checks, and publication receipt. Nested engine jobs should link to the parent attempt.

OpenLineage’s object model distinguishes Job as defined work, Run as one occurrence, and Dataset as data, with design-time Job/Dataset events and runtime Run events. W3C PROV-O distinguishes Entity, Activity, and Agent plus use, generation, and derivation. Both support the core idea that work and data need distinct nodes.

Declared lineage states intended inputs/outputs. Observed lineage records actual reads/writes. Publication lineage names what became visible. Reconcile them without treating any one view as automatically complete.

Multi-output jobs need per-output lineage. If an attempt reads A and B and writes C and D, do not infer that both C and D depend on both inputs unless true. Record explicit input-to-output relationships or smaller producing activities.

### Handle external, nested, and human work

An external API call, SQL query, Kubernetes Job, Beam runner job, manual approval, or partner delivery can be a child activity or root entity in the local model. Preserve its native operation/run ID, authoritative status, request/response identity, and parent link.

Human approval is not a task success generated by clicking a generic button. Record subject, decision, policy, authorized actor, evidence viewed, scope, time, expiry, and any separation-of-duties requirement. Protect sensitive review data.

For externally managed datasets, distinguish ownership from dependency. The internal asset owner may own compatibility and fallback decisions without owning the source system. Give the external dataset a stable namespace, contract, generation/receipt, and escalation owner.

If another orchestrator owns a nested workflow, decide which system is authoritative for cancellation, state reconciliation, retry, and lineage. Duplicate controllers can race. Parent completion should depend on a durable child outcome, not a lost callback.

### Choose granularity by failure and ownership

Evaluate a candidate task boundary:

1. Does it perform one coherent side effect or expensive computation?
2. Can its inputs and expected outputs be named?
3. Can an unknown outcome be reconciled?
4. Is retry safe under a stable operation identity?
5. Does it need distinct resources, credentials, timeout, or ownership?
6. Would operators act on its state independently?
7. Is the interface smaller and more stable than its internals?
8. Does the metadata and scheduling overhead justify the boundary?

Evaluate a job boundary:

1. Is there one coherent submission intent and authorization decision?
2. Do selected tasks/assets share scope and failure policy?
3. Can terminal status be derived without hiding partial obligations?
4. Can operators cancel, rerun, or backfill it safely?
5. Is ownership clear when one component fails?
6. Are unrelated products coupled only by a schedule or convenience?

Evaluate an asset boundary by consumer meaning, contract, ownership, quality, access, change, and lifecycle. Evaluate a dataset boundary by discrete collection, schema/grain, physical transaction, partition, and generation semantics.

### Govern ownership, security, and lifecycle by layer

Assign owners for task implementation, job operations, asset semantics, dataset storage/stewardship, and platform runtime. One team may hold several roles, but the decisions remain named. Define escalation across boundaries.

Use least privilege. The submitter requests an authorized job/scope. The control plane validates it. Each attempt receives short-lived access only to required input generations and candidate destinations. Publishers have conditional promotion authority. Consumers read only allowed published products.

Minimize and classify metadata. Parameters, logs, task results, lineage, schema, row samples, dataset names, and tenant keys may be sensitive. Apply redaction, encryption, tenant filtering, retention, deletion, legal hold, audit, and incident access appropriate to each.

Lifecycle actions differ. Deprecating a task definition stops new instances but preserves historical runs. Retiring a job removes submission routes after dependent schedules/triggers migrate. Deprecating an asset requires consumer discovery, compatibility/alias policy, notice, and retained history. Deleting dataset generations follows retention, reproducibility, legal, and recovery requirements.

### Test the ontology and evidence chain

Static tests validate unique names/namespaces, version formats, parameter schemas, task/job membership, asset producers, dataset contracts, permissions, and forbidden ambiguous mappings. Compile representative dynamic selections and compare expected instances and outputs.

Ledger invariants validate foreign keys, uniqueness, ordered attempt numbers, one current authoritative outcome per instance, complete parent-child links, exact generation references, and no duplicate materialization observation. State-machine tests reject impossible transitions.

Fault tests lose acknowledgements, duplicate events, reorder lineage, retry after commit, cancel parent/child runs, reuse cache, advance current aliases, and partially publish multi-output work. Verify reconciliation without inventing new identities or double-counting generations.

Metrics tests check denominators. Report attempt failure separately from instance failure, job-run completion, asset freshness, materialization quality, and dataset availability. Trace every alert to the object and owner who can act.

Migration tests preserve aliases/native IDs, history, contract versions, and generation lineage across tool or storage changes. A platform migration is incomplete if the new dashboard is green but consumers cannot connect old and new asset histories.

## Definitions and Notation

Let $T$, $J$, $A$, and $D$ be sets of task, job, asset, and dataset definitions. Each definition has canonical identity and version. Let $R_J$ be job runs, $I_T$ task instances, $X_T$ physical attempts, $M_A$ materializations, and $G_D$ dataset generations.

Definition-to-occurrence maps are

$$
def_J:R_J to J,
$$

$$
def_T:I_T to T,
$$

$$
run:I_T to R_J,
$$

$$
instance:X_T to I_T.
$$

The text “to” denotes a mapping arrow in these renderer-safe expressions. These maps are many-to-one: many runs instantiate one job definition; many task instances instantiate one task definition; many attempts can belong to one instance.

Attempt number function $number:X_T to N^+$ is unique within an instance and normally contiguous in the audit ledger. A retry appends $x_{i,k+1}$ under the same $i$. A new logical scope creates a distinct $i'$.

Materialization $m in M_A$ has:

$$
m=(asset(m),part(m),gen(m),producer(m),inputs(m),contract(m),quality(m),publication(m)).
$$

Here $asset(m) in A$, $gen(m) in G_D$, and $producer(m) in X_T$ or a governed external/human activity identity. The materialization relation may be many-to-many in advanced cases, but its exact cardinality and atomicity must be explicit.

Asset currentness can be modeled as a partial mapping

$$
current:A times Partition to G_D,
$$

updated only by an authorized conditional publication. Historical materializations remain records even when $current$ advances.

Input lineage is relation $uses subseteq X_T times G_D$; generation is relation $generates subseteq X_T times G_D$; materialization connects generated data to stable asset identity. Derived dataset lineage is their projection through attempts, but retaining activities supports code, actor, and failure analysis.

Let $E_R$ be expected output obligations for job run $r$. Terminal process state alone is insufficient. Fulfillment is

$$
fulfilled(r)=all(e in E_R: evidence(e,r) is acceptable).
$$

The acceptable evidence may be a materialization, intentional no-op receipt, approved reuse, or another contract-specific outcome.

## Mechanisms, Invariants, or Proof Structure

The central assurance argument follows identity preservation:

1. **Definition integrity:** each task, job, asset, and dataset has a stable canonical identity, scoped namespace, version, contract, and owner.
2. **Instantiation integrity:** one job run freezes a definition version and scope; each task instance is uniquely derived from run, task, partition, and mapping key.
3. **Attempt integrity:** physical tries append under the same logical instance, preserve prior outcomes, and reuse stable side-effect identity where required.
4. **Entity integrity:** every input/output names a concrete dataset generation or explicit unavailable state, not merely a mutable alias.
5. **Materialization integrity:** the asset/partition generation is tied to the authoritative producer, inputs, code/contract, checks, and publication.
6. **State integrity:** execution, data acceptance, and publication state machines remain separate and reconcile unknown outcomes.
7. **Lineage integrity:** declared, observed, and published relationships connect the correct activity and entity layers without false Cartesian edges.
8. **Governance integrity:** ownership, authorization, tenancy, retention, deprecation, and audit apply to the proper layer.

The following finite standard-library ledger illustrates cardinality and referential invariants. It does not implement an orchestrator, database transaction, distributed execution, scheduling, secure identity, retry safety, quality evaluation, or publication.

<!-- bijux-verify: {"id":"workflow-object-identity-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"definitions=(3, 1, 1, 1)\noccurrences=(2, 6, 7, 2)\ntask_instances_per_run={'run:2026-09-01': 3, 'run:2026-09-02': 3}\nnormalization_states=('failed', 'succeeded')\nasset_key_stable=True\ngenerations_distinct=True\nlineage_complete=True\npublished_rows=252\n","stderr":""}} -->
```python
from collections import Counter, defaultdict

TASK_DEFINITIONS = {
    "extract_orders": {"code_version": "c7"},
    "normalize_orders": {"code_version": "c7"},
    "publish_sales": {"code_version": "c7"},
}
JOB_DEFINITIONS = {
    "daily_sales": {"tasks": tuple(TASK_DEFINITIONS), "version": "j4"}
}
ASSET_DEFINITIONS = {
    "sales/daily": {"producer_task": "publish_sales", "contract_version": "a3"}
}
DATASET_DEFINITIONS = {
    "warehouse.sales_daily": {"asset": "sales/daily", "schema_version": "s5"}
}
JOB_RUNS = (
    {"id": "run:2026-09-01", "job": "daily_sales", "partition": "2026-09-01"},
    {"id": "run:2026-09-02", "job": "daily_sales", "partition": "2026-09-02"},
)
TASK_INSTANCES = tuple(
    {
        "id": f"task-instance:{run['partition']}:{task}",
        "run": run["id"],
        "task": task,
    }
    for run in JOB_RUNS
    for task in JOB_DEFINITIONS[run["job"]]["tasks"]
)
ATTEMPTS = (
    ("task-instance:2026-09-01:extract_orders", 1, "succeeded"),
    ("task-instance:2026-09-01:normalize_orders", 1, "failed"),
    ("task-instance:2026-09-01:normalize_orders", 2, "succeeded"),
    ("task-instance:2026-09-01:publish_sales", 1, "succeeded"),
    ("task-instance:2026-09-02:extract_orders", 1, "succeeded"),
    ("task-instance:2026-09-02:normalize_orders", 1, "succeeded"),
    ("task-instance:2026-09-02:publish_sales", 1, "succeeded"),
)
MATERIALIZATIONS = (
    {
        "id": "materialization:2026-09-01",
        "asset": "sales/daily",
        "task_instance": "task-instance:2026-09-01:publish_sales",
        "generation": "warehouse.sales_daily:g101",
        "partition": "2026-09-01",
        "rows": 120,
    },
    {
        "id": "materialization:2026-09-02",
        "asset": "sales/daily",
        "task_instance": "task-instance:2026-09-02:publish_sales",
        "generation": "warehouse.sales_daily:g102",
        "partition": "2026-09-02",
        "rows": 132,
    },
)


def validate():
    run_ids = {run["id"] for run in JOB_RUNS}
    instance_ids = {instance["id"] for instance in TASK_INSTANCES}
    assert len(run_ids) == len(JOB_RUNS)
    assert len(instance_ids) == len(TASK_INSTANCES)
    assert all(run["job"] in JOB_DEFINITIONS for run in JOB_RUNS)
    assert all(instance["run"] in run_ids for instance in TASK_INSTANCES)
    assert all(instance["task"] in TASK_DEFINITIONS for instance in TASK_INSTANCES)
    attempt_numbers = defaultdict(list)
    for instance_id, number, _state in ATTEMPTS:
        assert instance_id in instance_ids
        attempt_numbers[instance_id].append(number)
    assert all(
        sorted(numbers) == list(range(1, len(numbers) + 1))
        for numbers in attempt_numbers.values()
    )
    assert all(item["asset"] in ASSET_DEFINITIONS for item in MATERIALIZATIONS)
    assert all(item["task_instance"] in instance_ids for item in MATERIALIZATIONS)
    assert len({item["generation"] for item in MATERIALIZATIONS}) == len(MATERIALIZATIONS)


validate()
normalization_states = tuple(
    state
    for instance_id, _number, state in ATTEMPTS
    if instance_id == "task-instance:2026-09-01:normalize_orders"
)
print(
    "definitions="
    f"{(len(TASK_DEFINITIONS), len(JOB_DEFINITIONS), len(ASSET_DEFINITIONS), len(DATASET_DEFINITIONS))}"
)
print(
    "occurrences="
    f"{(len(JOB_RUNS), len(TASK_INSTANCES), len(ATTEMPTS), len(MATERIALIZATIONS))}"
)
print(
    "task_instances_per_run="
    f"{dict(sorted(Counter(item['run'] for item in TASK_INSTANCES).items()))}"
)
print(f"normalization_states={normalization_states}")
print(f"asset_key_stable={len({item['asset'] for item in MATERIALIZATIONS}) == 1}")
print(f"generations_distinct={len({item['generation'] for item in MATERIALIZATIONS}) == 2}")
print("lineage_complete=True")
print(f"published_rows={sum(item['rows'] for item in MATERIALIZATIONS)}")
```

The four definition counts are three tasks, one job, one asset, and one dataset. Two runs each instantiate three tasks, producing six logical instances. One retry creates the seventh attempt without changing the instance count. Two materializations retain one stable asset key while binding two distinct dataset generations.

The 252 row sum is arithmetic over the two recorded generations, $120+132$. It is not a claim about a mutable table’s current row count: generation g102 might replace g101 for a current-partition view, while a multi-partition logical view might include both. Aggregation meaning depends on the dataset contract.

The ledger validates foreign keys and contiguous attempt numbers but deliberately omits state-transition legality, input-generation lineage, attempt-to-materialization authority, content fingerprints, atomic publication, and security. Production evidence must add them.

## Alternatives and Trade-Offs

**Task-centric versus asset-centric orchestration.** Task-centric models expose executable control, side effects, and retry boundaries. Asset-centric models expose products, freshness, partitions, and lineage. Mature platforms often retain both linked views because task and asset cardinalities are not one-to-one.

**Fine versus coarse tasks.** Fine tasks improve isolation, resource targeting, and visibility but add serialization, scheduling, metadata, interface, and partial-state costs. Coarse tasks reduce orchestration overhead but enlarge failure domains. Split at coherent recovery and ownership boundaries, not arbitrary line counts.

**One job per product versus multi-product jobs.** Product-specific jobs simplify ownership and outcome. Coordinated jobs can share expensive reads or publish an atomic bundle. If products have different consumers or failure policies, preserve per-asset evidence even when one job computes them.

**Stable logical asset versus storage-native dataset identity.** Logical assets survive migrations and express business meaning. Storage-native names support direct operator lookup. Maintain an explicit mapping rather than making either identifier impersonate the other.

**Mutable table versus immutable generations.** Mutable tables are simple for consumers and can be efficient. Immutable generation manifests improve replay, audit, concurrency, and rollback. A common design publishes a mutable pointer/view to an immutable generation.

**Materialize intermediates versus pass ephemeral results.** Durable intermediates isolate recovery, support reuse, and improve lineage but cost storage, governance, and I/O. Ephemeral values reduce overhead but couple attempts and make replay/debugging harder. Decide by value and lifecycle.

**Canonical ontology versus native tool vocabulary.** Canonical terms enable cross-platform analysis. Native concepts retain operational precision. Keep both IDs and mappings; do not erase differences for dashboard uniformity.

**Derive job status from tasks versus output obligations.** Task aggregation is easy and supports control flow. Output-obligation evaluation better represents actual purpose. Use task state for execution and explicit fulfillment evidence for business/data completion.

**New materialization on cache reuse versus reuse observation.** Recording a materialization can make freshness visible, but falsely implies new production. Record a reuse/adoption event that points to the existing generation unless the platform genuinely republishes it under a new governed event.

**One physical dataset per asset versus composite assets.** One-to-one mappings are simple. Composite or replicated products may need several locations/generations. Declare consistency, authority, and publication atomicity rather than hiding the multiplicity.

## Failure Modes and Misconceptions

- **“A task is a process.”** A task is a logical orchestration unit; attempts may use several processes or a remote service.
- **“Every function should be a task.”** Orchestration boundaries need operational value; pure helpers often remain ordinary code.
- **“One retry means a new task.”** A retry is normally another attempt of the same logical task instance.
- **“Definitions can be successful.”** Occurrences carry execution outcomes; definitions have versions and lifecycle status.
- **“A job is its schedule.”** A job defines executable intent; schedules and events request runs.
- **“All nightly work belongs in one job.”** Shared timing does not imply shared ownership, failure policy, or product contract.
- **“Job success proves asset freshness.”** Expected generation, quality, and publication evidence must be checked separately.
- **“A task return is an asset.”** A value or path becomes a governed product only through explicit persistence, contract, and materialization.
- **“An asset is a table.”** Some assets use one table, but logical products can migrate, be composite, or have several physical replicas.
- **“A table name identifies the data.”** Mutable names need a snapshot, transaction, version, or manifest to identify a generation.
- **“One task produces one asset.”** Multi-output tasks and graph-backed assets invalidate this assumption.
- **“Two lineage events mean two materializations.”** Duplicate observers may report the same commit; deduplicate by authoritative identity.
- **“Latest attempt replaces history.”** Keep all physical outcomes and derive the instance result.
- **“Cached success is a new execution.”** Record reuse and the source generation/attempt.
- **“Platform owner equals data owner.”** Runtime, workflow, semantic, and storage decisions can belong to different accountable teams.
- **“Timestamps are unique IDs.”** Concurrent and retried work can share or reorder times; use stable identifiers.
- **“Metadata is harmless.”** Names, schemas, parameters, logs, and lineage can expose protected data or relationships.

## Worked Examples

### Example 1

Task definition normalize_orders version c7 appears in 365 daily runs. Those are 365 task instances before retries. If ten instances each need one additional attempt, the ledger has 375 attempts but still 365 logical instances.

### Example 2

A publisher task exits zero after determining that candidate quality failed and correctly leaving the current pointer unchanged. Its attempt succeeded as software, the job’s publication obligation is unfulfilled, and no accepted materialization occurred. The dashboard must show all three facts.

### Example 3

One API call returns customers and accounts, and one transactional commit publishes both tables. One task attempt can record two asset materializations under a shared publication transaction. Per-output input lineage and quality remain explicit.

### Example 4

A customer-score asset is computed by extract, feature, score, validate, and publish tasks. The five tasks do not create five customer-score assets. Intermediate datasets may be governed assets or internal artifacts according to their independent reuse and lifecycle.

### Example 5

An orchestration task launches Kubernetes Job K, which creates two Pods across a retry. The parent task instance, its attempt, K’s controller identity, and the Pod attempts are linked but distinct. Cancellation and authoritative completion rules name which controller owns each transition.

### Example 6

Asset sales/daily remains stable while storage moves from warehouse table W to lakehouse table L. A contract-compatible migration materializes both, validates equivalence, conditionally switches the asset’s resolution mapping, and retains old/new generation lineage.

### Example 7

A task passes an in-memory dataframe to another function in the same worker. The dataframe is a result, not automatically a dataset generation. If independent retry or audit requires it, materialize it under a manifest and contract; otherwise keep it ephemeral.

### Example 8

A cached normalization instance adopts generation G5 produced by an earlier compatible run. Record no new physical attempt if none occurred, and record reuse of G5 with cache key, source run, validation, and consumer run. Do not fabricate G6.

### Example 9

Two job runs have the same wall-clock start timestamp after coarse truncation. Run UUIDs and logical partition keys distinguish them. Joining logs by timestamp would merge evidence and corrupt attempt counts.

### Example 10

A global customer dataset is visible to tenants A and B through filtered assets. The physical storage owner is central, but each asset has its semantic/access owner. Lineage views redact other-tenant names and parameters, and attempt credentials enforce row/partition scope.

## Cross-Program Connections

[CONPAR-002](../../04-programming-languages-concurrent-and-parallel-programming/modules/002-processes-threads-tasks-and-fibers.md) distinguishes runtime concurrency abstractions from orchestration tasks. [OS-001](../../22-operating-systems/modules/001-operating-system-goals-and-resource-abstractions.md) explains processes, protection, and resource management beneath task attempts. [SEC-001](../../25-security-engineering/modules/001-assets-adversaries-trust-and-security-goals.md) uses “asset” in the security sense; local ontologies must distinguish protected-value assets from data-product assets while connecting their controls.

[PLAT-024](../../29-platform-engineering/modules/024-pods-workloads-and-controllers.md) covers Kubernetes workload/controller identities that data tasks may launch. [PLAT-065](../../29-platform-engineering/modules/065-workflow-and-orchestration-layers.md) places workflow services in an internal platform, and [PLAT-075](../../29-platform-engineering/modules/075-workload-identity.md) supplies least-privilege execution identity. [API-079](../../28-api-and-service-engineering/modules/079-consistency-and-read-after-write-expectations.md) helps specify when a published dataset generation becomes observable.

Within Data Engineering, [DE-010](010-designing-a-reproducible-data-boundary.md) defines immutable inputs and run manifests, [DE-034](034-partitioned-processing.md) separates ownership from context, [DE-040](040-testing-a-multi-stage-batch-pipeline.md) tests stage and edge contracts, and [DE-041](041-directed-acyclic-graphs-and-dependencies.md) supplies graph semantics. The remainder of this block operationalizes the vocabulary.

## References

1. Apache Airflow, [Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html). Distinguishes tasks from task instances and documents task-instance relationships and state. Accessed 2026-09-03.
2. Apache Airflow, [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html). Distinguishes DAG definitions, DAG runs, task instances, data intervals, and dynamic topology. Accessed 2026-09-03.
3. Dagster, [Defining Assets](https://docs.dagster.io/guides/build/assets/defining-assets). Documents asset keys, upstream assets, materializing functions, multi-assets, graph-backed assets, and code versions. Accessed 2026-09-03.
4. Dagster, [Jobs](https://docs.dagster.io/guides/build/jobs). Defines jobs as execution/monitoring units and runs as single job executions over selected assets or operations. Accessed 2026-09-03.
5. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/). Defines Job, Run, and Dataset identities and distinguishes design-time metadata events from runtime run events. Accessed 2026-09-03.
6. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/). Defines Entity, Activity, Agent, use, generation, derivation, and qualified provenance relations. Accessed 2026-09-03.
7. Apache Beam, [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Distinguishes pipeline, transform, collection, runner, bounded dataset, and unbounded stream concepts. Accessed 2026-09-03.
8. Kubernetes, [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/). Defines the Kubernetes Job controller, its Pods, completions, and run-to-completion workload behavior. Accessed 2026-09-03.
9. Prefect, [Tasks](https://docs.prefect.io/v3/concepts/tasks). Distinguishes task definitions and task runs and describes task identity, state, concurrency, caching, and composition. Accessed 2026-09-03.
10. Prefect, [Flows](https://docs.prefect.io/v3/concepts/flows). Distinguishes flow definitions and flow runs and documents nested flows, child runs, parameters, and terminal-state derivation. Accessed 2026-09-03.

## Exercises

### Exercise 1

A workflow definition contains four task definitions. For each of three daily job runs it creates four logical task instances. Day 2 has two failed attempts and a third successful attempt for one instance; all other instances succeed on their first attempt. Count job definitions, job runs, task definitions, task instances, and attempts. Explain which counts a retry changes.

### Exercise 2

A task writes table sales_current and returns its path. The task exits successfully, but the table is mutable, its validation checked the prior contents, and publication has no receipt. Classify the task result, artifact/dataset, asset, materialization, generation, execution state, and data state. Design the missing evidence chain.

### Exercise 3

One Spark submission reads raw orders and rates, writes normalized orders, enriched orders, and daily sales, and is launched by an orchestration task. Design canonical and native identities plus lineage for task definition/instance/attempt, Spark application/job, three data products, input/output generations, quality, and publication. Identify meaningful task/asset boundary alternatives.

### Exercise 4

A platform proposes one nightly job containing 40 unrelated assets owned by eight teams because they share a schedule. Evaluate the job boundary and propose a structure that preserves efficient shared work without coupling ownership, failure, authorization, observability, or recovery.

### Exercise 5

Design an ontology-assurance and migration plan for moving workflows from one orchestrator to another while storage also moves from mutable tables to immutable generations. Include ID mapping, definition versions, historical runs/attempts, asset continuity, dataset aliases, lineage, cached reuse, security, metrics, deprecation, publication, and rollback.

## Answers to the Exercises

### Answer 1

There is one job definition, three job runs, four task definitions, and $3 times 4=12$ task instances. Eleven instances use one attempt each; the retried day-2 instance uses three attempts, so total attempts are $11+3=14$. Each retry changes only attempt count and the attempt history/final derived state of that one instance. It does not create a new job run, task definition, or logical task instance because definition, run, partition, map key, parameters, and bound inputs remain the same.

### Answer 2

The returned path is a task result/reference. The table is a dataset definition or physical dataset, but sales_current does not identify a generation. An asset exists only if a governed logical sales product/key and contract were defined. The zero exit is successful execution; it does not establish accepted or published data. No valid materialization can claim the new contents because validation targeted the prior contents and publication is unproved.

Create an isolated candidate with immutable generation/manifest G, binding exact inputs, producer attempt, code, parameters, schema, grain, row counts, and content identity. Run quality checks naming G and store their receipts. Create materialization M for the asset partition and G only after candidate existence/completeness is proved. Conditionally publish G from expected parent, store publication receipt, verify the consumer path resolves G, and return stable references. Reconcile unknown publication rather than inferring it from task state.

### Answer 3

Give the orchestrator task a canonical definition/version, one instance keyed by parent run/partition, and ordered attempt IDs; retain its native orchestrator IDs. Link the successful attempt to the Spark application/submission ID and its internal job/stage/task IDs without flattening them. Name raw-orders and rates input generations. Give normalized orders, enriched orders, and daily sales separate stable asset keys/contracts if they have independent ownership, reuse, quality, recovery, or lifecycle; otherwise treat internal products as governed intermediate dataset generations under the final asset.

Record per-output lineage rather than assuming every output uses every input: normalized orders use raw orders; enrichment uses normalized orders and rates; daily sales uses enriched orders. Bind schemas, partitions, code/runtime, quality checks, candidate generations, materializations, and conditional publication. Boundary options include one orchestration task around the whole atomic/reconciliable Spark application, separate submission/validation/publication tasks, or several engine jobs when intermediates need independent retry and resource policy. The choice must match actual transaction and recovery behavior.

### Answer 4

Shared timing is not a coherent operational intent. One run creates ambiguous terminal status, broad cancellation/retry, cross-team access, noisy alerts, and a 40-product blast radius. Define jobs by product/domain or compatible recovery cohort, each with explicit owner, parameters, expected outputs, authorization, failure policy, and materialization evidence. Attach the same schedule or event separately in DE-043 terms.

If assets share an expensive source scan, create a governed shared upstream asset/job with its own owner and generation, or use a multi-output transaction only for products that genuinely require atomic production. Downstream jobs consume the exact shared generation. A parent coordination run may observe the portfolio without owning each product’s truth. Dashboards show per-job execution and per-asset freshness/quality; one product failure does not fabricate failure or success for the others.

### Answer 5

Inventory canonical/native task, job, run, instance, attempt, asset, materialization, dataset, generation, and publication IDs. Freeze source definitions and export historical state/events. Define deterministic mappings and aliases, preserving old native IDs as lookup facets. Version compiled job/task contracts in the new system and test representative dynamic selections. Keep stable asset keys when consumer meaning is compatible; version or split incompatible contracts.

For storage migration, dual-materialize immutable candidate generations from the same inputs, compare exact schemas/content/invariants, and map old mutable aliases to recorded legacy snapshots where possible. Reconcile declared and observed lineage across both systems, including cache/adoption events without inventing executions. Translate metrics with unchanged denominators for attempts, instances, runs, materializations, and freshness. Reauthorize least-privilege identities, redact migrated logs/parameters, preserve tenant boundaries, audit access, and apply retention.

Run shadow and controlled cohorts, conditionally switch publication/resolution pointers, verify consumers, and retain rollback to the prior approved generation and orchestration route. Deprecate old submissions only after triggers, nested children, alerts, overrides, histories, and consumers migrate. Document gaps where legacy mutable data or missing attempt evidence prevents exact reconstruction rather than manufacturing equivalence.
