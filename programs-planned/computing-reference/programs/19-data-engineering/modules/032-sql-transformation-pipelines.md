---
module_id: DE-032
program: Data Engineering
level: 1
module_number: 32
title: SQL Transformation Pipelines
status: complete
last_verified: 2026-09-02
---

# SQL Transformation Pipelines

## One-Page Review

### Governing question

How should a team turn SQL statements into a versioned, dependency-aware, deterministic, tested, observable, and atomically published transformation system whose outputs retain their declared meaning under retries, concurrency, schema change, and scale?

### Essential definitions

- A **SQL transformation model** is a named query plus an input/output contract, not merely a text file that happens to execute.
- A **model graph** is a directed graph whose vertices are transformations or governed sources and whose edges declare data dependencies.
- A **directed acyclic graph (DAG)** is a model graph with no dependency cycle, permitting a topological execution order.
- **grain** states what one output row represents and which key identifies that representation.
- A **source cut** identifies the exact source state, snapshot, partition set, or bounded change range used by a run.
- **compilation** resolves templates, references, configuration, environment names, and dialect-specific syntax into executable SQL.
- A **materialization** maps a logical query to a physical form such as a view, table, ephemeral subquery, incremental relation, or materialized view.
- A **run manifest** binds graph/version, compiled SQL digests, source cuts, parameters, target objects, attempts, and evidence.
- A **quality gate** is an executable criterion that must pass before an output generation becomes trusted.
- **atomic publication** changes consumer-visible identity from the old complete generation to the new complete generation without exposing an intermediate partial state.
- **semantic equivalence** is equality under a declared relation covering rows, multiplicities, types, nulls, order when promised, side effects, and publication—not just equal row counts.

### Central model, mechanism, or theorem

Let $G=(V,E)$ be a transformation graph. For model $v$, let $P(v)$ be its direct parents, $Q_v$ its compiled query, $C$ the source-cut map, $K$ the contract set, and $R_v$ the relation produced for a run:

$$
R_v=Q_v\left(\{R_u:u\in P(v)\},C,K\right).
$$

The graph is schedulable as an ordinary batch pipeline only if it is acyclic. A topological order guarantees that every parent is available before its child, but it does not prove correctness. Correctness additionally requires each model to preserve its declared grain, types, null/time/duplicate semantics, source cut, and dependency identities.

For a fanout-safe aggregation, deduplicate events to authoritative identity, aggregate each many-side relation to the join key, and only then join. If order $o$ has $m_o$ order occurrences and $n_o$ refund occurrences, joining first can create $m_on_o$ pairs. Making $m_o=1$ by version resolution and $n_o\leq1$ by refund pre-aggregation prevents that unintended multiplication at order grain.

### Critical invariants

- Every source and model has a durable name, owner, contract version, input grain, output grain, key, and consumer boundary.
- Dependencies are declared from references rather than inferred only from runtime query text or orchestration order.
- A run uses one coherent source cut or explicitly records and justifies mixed cuts.
- Templates alter representation without hiding business dependencies, nondeterminism, security predicates, or destructive behavior.
- Compiled SQL, engine/dialect/version, session settings, parameters, macros, and resolved object names are attributable to the run.
- Joins have expected cardinality; deduplication uses authoritative identity/order; aggregation occurs over a declared input bag.
- Null, numeric, string/collation, time-zone, interval-boundary, and window-frame semantics are explicit and tested in the actual target dialect.
- Every model writes an isolated attempt or generation until schema, key, reconciliation, and business controls pass.
- Publication is atomic or conditionally serialized under verified engine/catalog semantics; task success alone is not publication proof.
- Retry, timeout, cancellation, and backfill cannot silently append duplicates, overwrite newer output, or mix generations.
- Lineage records logical job, physical run, exact input/output datasets, column transformations where needed, and evidence state.
- Cost and performance changes never bypass semantic comparison, authorization, or quality gates.

### Common failures

Common failures include one giant query with invisible boundaries; one file per syntactic CTE regardless of ownership; `SELECT *` across evolving sources; hard-coded production relations; hidden dependencies inside macros or dynamic SQL; joining facts before pre-aggregation; `DISTINCT` as deduplication; nullable `NOT IN`; incomplete window ordering; default window frames; current-time functions in reproducible models; compiling with different variables than were reviewed; relying on CTE materialization as a portable guarantee; rebuilding a trusted table in place; publishing before tests; treating a view as free; rerunning append logic after timeout; selecting only changed downstream nodes without a compatible source cut; recording table names but not generations; and calling a green orchestrator graph evidence of semantic correctness.

### Compact example

A fixed SQLite fixture stages six order occurrences into five typed rows, filters one rejected order, and resolves one superseded order version. It separately aggregates four refunds by order before joining. Customer `c1` receives two accepted orders with 1,700 gross cents, 300 refunded cents, and 1,400 net cents; customer `c2` receives one order with 800 gross, 100 refunded, and 700 net. The final total is 2,100 cents. Shuffling input insertion order produces the same canonical output because the winner order is total and no physical row order is relied upon.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) supplies type fidelity, [DE-011](011-grain-and-the-meaning-of-a-row.md) supplies grain, [DE-020](020-validating-an-analytical-model-against-business-questions.md) supplies question-led validation, and [DE-031](031-extract-transform-load-and-extract-load-transform.md) locates SQL relative to load. [DBE-020](../../18-database-engineering/modules/020-writing-correct-sql-under-duplicate-and-null-semantics.md) develops query-level correctness. The following Data Engineering modules extend this foundation to dataframe, partitioned, incremental, merge, backfill, correction, determinism, and batch-testing concerns.

## Governing Question

How can SQL become a trustworthy transformation pipeline rather than a collection of queries that happen to run in a convenient order?

The answer begins outside the SQL text. A transformation must name its authoritative inputs, exact source cut, row meaning, output key, type and time rules, quality criteria, physical materialization, publication protocol, owner, and consumers. SQL then implements part of that contract. An orchestrator schedules it. A database executes it. A catalog exposes it. Evidence establishes whether the combined system behaved as intended.

SQL is attractive because it is declarative: the author states a result relation and lets an engine choose a physical plan. That separation enables optimization and portability, but it also makes operational folklore dangerous. Textual CTE order does not necessarily specify materialization. Source row order does not determine a window winner. A successful `CREATE TABLE AS` does not prove that consumers saw one complete, validated generation. A fast plan does not prove that a join preserved grain.

A pipeline adds temporal and graph concerns to query correctness. Different nodes may observe different snapshots. A parent may publish while a child is running. A retry may meet a table left by an ambiguous earlier attempt. A selective build may combine a newly compiled child with an incompatible old parent. A schema change may compile but reinterpret `SELECT *`. The governing question therefore covers logical semantics, dependency identity, execution isolation, validation, and publication together.

## Why This Matters

Analytical and operational decisions rarely depend on one isolated query. They depend on chains: raw orders become typed orders; order versions become one authoritative state; refunds become order-level adjustments; customers become dimensions; those relations join into daily facts and published metrics. A defect near the beginning can be replicated into dozens of downstream products.

SQL pipelines often look simpler than general-purpose programs because dataflow is implicit in relation references. Hidden dataflow is still architecture. A hard-coded table, templated identifier, dynamic macro, external function, current-date call, or session setting is an input. If the build system does not model it, selection, lineage, cache invalidation, and replay become unsound.

Logical errors are costly and plausible. Joining order rows to several line items and several refunds before aggregation multiplies both. A `LEFT JOIN` predicate moved into `WHERE` removes preserved rows. `NOT IN` with a null candidate excludes unexpected records. A `ROW_NUMBER` window without a stable tie-breaker chooses an arbitrary version. Grand totals can still match when defects offset, so row counts and aggregate parity alone are weak evidence.

Operational errors are equally important. Replacing a trusted relation in place can expose absence or partial output. Views defer work and can transfer a deployment-time success into consumer-time latency or failure. Tables isolate readers and improve repeatability but cost storage and refresh time. Incremental materializations reduce work only if their boundary, merge key, delete handling, and late-data policy are correct; later modules treat those mechanisms in depth.

Well-engineered SQL pipelines improve collaboration. Small models with declared grains give reviewers stable proof boundaries. Explicit graph edges permit topological scheduling, impact analysis, lineage, and safe selection. Compiled artifacts expose what the engine actually received. Isolated generations and quality gates separate computation from trust. These practices make SQL reviewable as production software without pretending that SQL is identical across engines.

## Prerequisites and Retrieval

Retrieve the approved business questions; source and consumer owners; source systems, snapshots, watermarks, manifests, partitions, and retention; model inventory; relation and column lineage; model contracts; table grains and keys; entity/version identities; delete and late-arrival policies; schemas, types, encodings, collations, time zones, numeric precision and rounding; SQL dialect and exact engine version; driver/runtime and session settings; templates, macros, packages and variables; environments and naming rules; roles, grants, row/column policies and sensitive classifications; materializations; dependency and selection rules; orchestrator retries/timeouts/concurrency; query plans and workload history; quotas and cost controls; data tests, unit fixtures and reconciliations; staging and publication interfaces; rollback/restore; incident history; SLOs; lineage/catalog integration; and artifact/evidence retention.

Distinguish source name from source generation; logical model from physical relation; model dependency from task ordering; graph acyclicity from semantic correctness; CTE from persisted model; query text from compiled query; compile input from runtime input; `SELECT` result from materialization; table build from publication; row uniqueness from business identity; deterministic tie-breaker from authoritative winner policy; null from zero or missing row; event time from load time; current snapshot from historical/as-of state; parse success from dialect execution; exact rebuild from incremental equivalence; isolated development schema from production; view freshness from source coherence; engine transaction from orchestrator task; and task retry from logically idempotent run.

Create a model contract table before implementation:

| Field | Required content |
|---|---|
| Identity | Stable model name, owner, version, domain, description, consumers |
| Inputs | Governed references, generation/cut requirements, expected grains and schemas |
| Output | One-row meaning, key, columns/types, nulls, units, time roles, ordering promise |
| Semantics | Filters, joins/cardinalities, dedup winner, aggregation, corrections, privacy |
| Compilation | Dialect, engine/version, packages/macros, variables, environment bindings |
| Materialization | View/table/ephemeral/incremental form, physical properties, refresh behavior |
| Validation | Compile/unit/contract/data/reconciliation/metamorphic/security/performance checks |
| Publication | Staging identity, gates, commit/pointer method, receipt, rollback and retention |
| Operations | Schedule, dependencies, concurrency, retry, timeout, SLO, alerts and owner |
| Evidence | Code/config digest, compiled SQL, source cuts, query/job IDs, metrics and lineage |

Retrieve actual vendor behavior rather than assuming generic SQL. Test edge semantics in the production dialect. Confirm DDL and DML transaction rules, view security context, identifier resolution, temporary-object lifetime, CTE treatment, window defaults, decimal behavior, timestamp conversion, collation, constraint enforcement, query cancellation, and ambiguous client timeout behavior.

## Learning Objectives

After completing this module, you should be able to:

1. define a SQL model through input, output, semantic, execution, and publication contracts;
2. construct an explicit acyclic dependency graph and derive a safe topological schedule;
3. choose model boundaries from grain, ownership, reuse, observability, and failure isolation;
4. compile templated SQL reproducibly and inventory every hidden compile/runtime input;
5. trace bag multiplicity, null behavior, types, time semantics, and window order through a model;
6. prevent fanout by resolving identity and pre-aggregating many-side relations before joins;
7. choose among view, table, ephemeral, materialized-view, and incremental strategies by evidence;
8. design layered compile, unit, contract, reconciliation, security, performance, and publication gates;
9. publish isolated output generations atomically and recover safely from retry or ambiguous completion; and
10. operate SQL transformations with lineage, observability, cost controls, change management, and rollback.

## Core Exposition

### Treat a model as a contract-bearing function

A useful abstraction is a pure relation function: named input relations enter and one named output relation leaves. Production SQL is not perfectly pure—engines read snapshots, apply session settings, call volatile functions, access external tables, and materialize side effects—but the abstraction exposes what must be controlled.

State one row in and one row out. For `stg_orders`, one output row might mean one source order occurrence after safe type conversion. For `current_orders`, one row might mean the authoritative latest state of one order as of source cut $c$. For `customer_order_summary`, one row might mean one customer across a named accounting interval. Those are different grains and deserve different contracts.

Name the output key and whether it is enforced, asserted, or only expected. Describe null as unknown, missing, not applicable, redacted, or invalid rather than treating it as one generic state. State units and time roles in names or metadata. An integer `amount` and timestamp `date` are insufficient contracts.

Separate the logical query from its materialization. The query defines candidate rows. The materialization defines when and where they become stored or evaluated, how existing output changes, what readers see, and how failure is recovered. Review both.

### Build explicit dependencies

Let each model reference governed source or model identities. A dependency edge $u\rightarrow v$ means $v$ consumes $u$. Do not create edges merely because two tasks share a schedule, and do not omit edges because a macro generated the reference.

A DAG permits a topological order $(v_1,\ldots,v_n)$ such that each parent precedes its child. The order is not necessarily unique; independent nodes can run concurrently within resource and snapshot constraints. A cycle means no ordinary full topological schedule exists. Break cycles through a state boundary, iterative algorithm with explicit convergence, or redesign—not an arbitrary task delay.

dbt documents that its `ref` function both resolves environment-aware relation names and creates dependencies used to order a model DAG. That is a concrete implementation, not a requirement to use dbt. Any system needs an equivalent explicit dependency contract.

Detect dynamic dependencies at compile time. If a macro chooses one of several sources, the manifest must record the chosen source and, where impact analysis requires it, the possible dependency set. Queries hidden in stored procedures, user-defined functions, external functions, hooks, or runtime strings need explicit ownership and lineage.

### Choose durable model boundaries

A boundary is justified when it gives a stable grain, contract, owner, reuse point, quality gate, security boundary, expensive shared result, or failure/recovery boundary. Splitting every CTE into a table produces operational clutter. Combining a domain into one enormous query hides semantics, prevents targeted checks, and makes plan failures difficult to isolate.

A common but nonmandatory layering is source declarations, staging normalization, intermediate domain logic, and published facts/dimensions/marts. Use names that express enduring domain meaning and grain. Avoid delivery-sequence names, generic numbered transformations, or temporary ownership labels.

Keep source-near staging narrow: rename, cast, normalize, expose ingestion metadata, and quarantine invalid records. Resolve version identity in an owned model. Aggregate at the declared grain before joining to another fact-like relation. Keep presentation rules from silently changing authoritative measures.

Persist only when the boundary earns it. An ephemeral/inline model reduces stored objects but repeats work and removes an inspectable recovery point. A persisted intermediate costs storage and refresh but can isolate failures and enable reuse. Evidence decides.

### Make compilation reproducible

Templating can remove repetition and encode dialect adapters, but the rendered query is the executable artifact. Record source revision, model code digest, macro/package versions, variable values, environment target, resolved database/schema names, dialect, adapter/compiler version, and compiled SQL digest.

Restrict templates to structural choices that remain inspectable. Values should use parameters where supported. Dynamic identifiers require allowlists and explicit dependency registration. Never concatenate untrusted text into executable SQL. A macro that silently inserts tenant filters, current dates, or destructive hooks is a material part of the contract.

Compilation should be deterministic for identical declared inputs. Environment-specific relation names may differ, but a normalized logical digest should explain that difference. Volatile compile-time timestamps, unordered metadata iteration, ambient environment variables, network lookups, and mutable package versions undermine reproducibility.

Review compiled SQL as well as source templates. Validate that references resolved to the intended environment, casts and predicates survived macro expansion, generated aliases are unique, and no production object appears in a development build.

### Establish one coherent source cut

A topologically correct run can still be temporally inconsistent. If `orders` reads at 10:00 and `refunds` reads at 10:20 without an as-of rule, the join may combine states that never formed one business snapshot.

Prefer immutable input generations, transactionally consistent snapshots, or bounded source manifests. Record cut $C(s)$ for every source $s$. If the engine provides one statement snapshot, a single query may be coherent within its documented rules; separate model statements may observe later commits unless a shared snapshot or immutable parents are used.

Mixed cuts are sometimes intentional. A daily fact may join today’s events to the latest approved monthly budget. State that contract, including acceptable staleness and revision behavior. “Latest” without a resolved generation is not reproducible.

Selective builds need cut compatibility. Rebuilding a child against an old parent and new sibling may produce a hybrid generation. The run manifest should either bind all upstream generations or prove compatibility under declared model/version and source-cut rules.

### Engineer SQL semantics explicitly

SQL commonly uses bag semantics: duplicates persist unless an operator removes them. Trace multiplicity through joins and aggregation. If left key $k$ has $a_k$ occurrences and right key $k$ has $b_k$, an equijoin can emit $a_kb_k$ pairs. That multiplication may be intended for event combinations; it is usually wrong when both sides carry order-level measures.

Resolve duplicate identity before aggregation. A `ROW_NUMBER()` winner needs a partition key and a total order. Order by authoritative source version, correction time, source priority, ingestion sequence, and stable occurrence ID as the domain requires. Adding an arbitrary ID makes the result repeatable but does not make the winner authoritative.

Aggregate each many side to the intended join key. Refund events can become one row per order with `SUM(refund_cents)`. Then join to one authoritative order row. Assert both intermediate grains. Never use `DISTINCT` on the final projection to hide a multiplication defect; equal-valued legitimate events may be collapsed while unequal duplicates remain.

Use three-valued logic deliberately. `WHERE` retains only true predicates; false and unknown are both removed. Nullable `NOT IN` can become unknown due to a null candidate. Outer-join predicates differ in `ON` and `WHERE`. `COUNT(*)`, `COUNT(x)`, and `COUNT(DISTINCT x)` answer different questions. Record expected null and empty-input behavior.

Types are semantic. Cast source strings under explicit invalid-value policy. Use fixed precision and governed rounding for money. State overflow behavior. Normalize or govern string collation before equality and grouping. Convert timestamps with named source zone, ambiguity policy, precision, and half-open interval boundaries.

### Use CTEs as proof boundaries, not storage promises

CTEs can make one query reviewable: each name can state a grain and isolate one transformation. They do not by themselves create a persistent checkpoint, transaction, quality gate, or universally materialized intermediate.

PostgreSQL documents version-specific CTE folding and `MATERIALIZED`/`NOT MATERIALIZED` controls. Other engines have different optimizers. Treat a CTE as a logical relation unless the target documentation and actual plan establish physical behavior. If reuse, isolation, or stable performance requires persistence, choose a governed materialization explicitly.

Avoid chains of CTEs that merely rename columns without establishing a meaningful invariant. Conversely, do not compress identity resolution, fanout control, time assignment, and business aggregation into one opaque select list. A reviewer should be able to state the grain and key after every risk-bearing boundary.

Recursive CTEs require a separate contract: seed, recursive transition, duplicate handling, cycle policy, maximum depth, termination/convergence, and resource bounds. A DAG of batch models can contain a model whose internal SQL is recursive; the model graph itself must still handle that model as one node with declared behavior.

### Specify windows completely

Window functions preserve row occurrences while computing partition-relative values. Specify partition, peer ordering, total winner ordering, and frame independently. `ROW_NUMBER()` used for deduplication needs a total winner order. `RANK()` may intentionally retain peers. An ordered aggregate needs an explicit frame when the default would not express the intended running or full-partition calculation.

PostgreSQL’s window-function documentation distinguishes partition ordering from the window frame and notes that default frames can produce unhelpful `last_value` behavior. Verify exact target semantics. Final presentation order is separate again: a window `ORDER BY` does not promise query-result order.

Test ties, null order, equal timestamps, duplicate versions, empty partitions, and late corrections. A query that appears stable on one physical layout may change after compaction, indexing, clustering, or engine upgrade if the logical order is incomplete.

### Select a materialization intentionally

A view stores a query definition and evaluates it under the engine’s view, snapshot, authorization, and optimization rules. It is easy to update and storage-light, but cost, latency, source availability, and failures move to read time. Deep view stacks can make performance and lineage difficult to reason about.

A table captures a result generation. It can isolate consumers from upstream changes and provide predictable read performance, but it costs build time/storage and becomes stale. Build it in an isolated name, validate it, and publish it. PostgreSQL’s `CREATE TABLE AS` documentation makes the basic distinction clear: it creates and fills a new table from a query; pipeline-level validation and publication remain the application’s responsibility.

An ephemeral model is substituted into consumers. It can remove needless persisted boundaries but may duplicate expensive logic, enlarge compiled queries, and make direct inspection unavailable. A materialized view gives engine-managed refresh behavior whose freshness, concurrency, eligibility, and failure rules must be verified per product.

An incremental model changes only part of an existing result. It is not simply a faster table. It adds boundary, uniqueness, delete, late-arrival, schema-change, concurrency, and equivalence obligations. Use full rebuilds until an incremental contract is justified; DE-034 and later modules develop the required methods.

Compare alternatives using observed scan/shuffle, latency, concurrency, storage, freshness, failure isolation, lineage, rebuild time, and operator toil. A materialization is part of the public operational contract, not a decorator chosen from habit.

### Separate build, validation, and publication

Never write an unvalidated candidate directly into the trusted consumer name unless the engine transaction and failure semantics prove readers cannot observe an invalid or partial state. Create an attempt-specific staging relation or immutable generation bound to run ID and input manifest.

Validation proceeds in layers. Parse and compile catch syntax and reference errors. Unit fixtures test local branches and boundaries. Contract checks validate columns and types. Data checks validate keys, nulls, relationships, domains, and accepted exceptional rows. Reconciliations compare source controls, key sets, additive totals, and both directions of set difference. Business-question checks validate fitness. Security and performance checks cover nonfunctional correctness.

Only a designated publication controller should change trusted identity. It verifies the candidate, expected prior generation, run state, and authorization, then performs a target transaction, atomic rename/swap, or conditional metadata-pointer update supported by the platform. BigQuery documents atomic multi-statement DML transactions with snapshot isolation and explicit limitations; that concrete contract must not be generalized to unrelated engines or permanent DDL.

Record a publication receipt containing logical output, candidate generation, previous generation, query/job/transaction ID, manifest digest, checks, publisher, and commit time. On client timeout, look up that identity before retrying. Rollback generally means repointing to a retained valid generation or performing a governed compensating operation—not rerunning arbitrary old DML.

### Make retries idempotent and concurrency safe

A retry should address the same logical run identity and immutable inputs. It may reuse a verified candidate or rebuild the same candidate generation. It must not append the same output again or overwrite a newer successful generation.

Separate `run_id` from `attempt_id`. Several attempts can implement one logical run. Bind each candidate to attempt and manifest; bind publication to run and expected current generation. A compare-and-swap condition prevents a late attempt from replacing a newer output.

Limit concurrent writers per logical output unless the publication protocol safely serializes them. A scheduled build, manual repair, and backfill can otherwise race. Partition-disjoint writes still need a complete dataset manifest and compatibility rule before the partition set is trusted.

Cancellation is not proof of rollback. Query engines may continue server-side work after a client disconnect, or may have committed before the acknowledgement was lost. Persist job IDs and query target state. Classify outcomes as succeeded, failed, cancelled, or unknown; resolve unknown rather than treating it as failed and blindly issuing another mutation.

### Build a layered test strategy

Static checks inspect parseability, forbidden constructs, qualified references, declared dependencies, deterministic functions, explicit columns, naming, and contract coverage. Lint rules help consistency but cannot establish business meaning.

Unit fixtures should be small enough to derive manually and include empty input, duplicate identity, newer/older versions, null keys and values, unmatched and multiply matched joins, rejected statuses, boundary times, ties, negative/reversal rows, and type extremes. Derive expected rows independently from the production query.

dbt describes data tests as SQL assertions that return failing rows. That pattern is broadly useful: a uniqueness check selects duplicated keys; a relationship check selects missing parents; an invariant check selects impossible measures. A test’s pass means its violating-row query returned none under a named snapshot—not universal correctness.

Use reconciliation at multiple boundaries: source-to-stage counts and rejects; pre/post-dedup identity counts; join match/fanout distributions; input and output additive controls; unmatched key sets; partition coverage; and published-versus-candidate differences. Test both missing and extra records, not only totals.

Metamorphic tests describe changes without a full oracle. Reordering input must not change deterministic output. Adding a rejected order must not change accepted totals. Adding one refund must reduce net by that refund exactly once. Duplicating an obsolete order version must not affect the winner. These relations expose multiplicity and hidden-order defects.

Run high-risk queries in the actual dialect against representative scale. Local SQLite or another small engine is a semantic teaching aid, not proof of warehouse types, collation, optimizer, transactions, or performance.

### Validate graph changes in continuous integration

Compile every changed model and inspect the dependency diff. Run unit and contract tests for changed nodes. Select downstream models based on the graph, but consider macro/package/source-contract changes that affect many nodes. A shared macro change may require a broad rebuild even when no model file changed.

Create an isolated schema/catalog namespace for each review build. Ensure it resolves only authorized nonproduction inputs or governed snapshots. Prevent accidental writes to production by credentials and policy, not naming convention alone.

Compare compiled SQL, contract, lineage, row/key/reconciliation results, and representative plans against the accepted base. Classify intentional semantic changes explicitly. Row-count equality does not make a change safe, while an intended contract migration may correctly change every row.

Promotion should use the same reviewed artifact. Recompiling with different packages, macros, variables, or adapter versions creates a new artifact that lacks the original evidence. Where environment bindings necessarily differ, validate the normalized logical artifact and the final resolved bindings.

### Observe the data plane and control plane

Data-plane evidence includes rows read/written, bytes, partitions, rejects, duplicate/version counts, null/domain distributions, join fanout, unmatched keys, aggregates, reconciliation deltas, and output digests under documented canonicalization.

Control-plane evidence includes graph/code/config version, compiled SQL digest, source and parent generations, run/attempt/job/query/transaction IDs, state transitions, start/end/queue time, engine/runtime/session settings, resource usage, tests, candidate and publication identities, and owner acknowledgements.

OpenLineage’s object model distinguishes Jobs, Runs, and Datasets and attaches changing run information through events/facets. That separation is useful: a model definition evolves, executions are distinct, and a physical dataset generation can change. Record column lineage where impact, privacy, or metric provenance requires it, but do not assume parsed column lineage captures dynamic SQL, procedural side effects, or business semantics completely.

Metrics need dimensions. Duration without model/version/warehouse/queue state hides regressions. Row count without source cut hides missing partitions. Cost without scanned input and concurrency hides waste. Alert on broken invariants and SLO burn, not every harmless distribution fluctuation.

### Tune only after semantics are fixed

Capture representative actual query plans where safe: scan/partition pruning, cardinality estimates, join order/algorithm, exchanges/shuffles, sorts, aggregation stages, memory, spill/temp I/O, parallelism, cache effects, locks, queue and slot/warehouse usage. Compare hot/cold and skewed parameters.

Projection and predicate pushdown can reduce work, but a predicate moved across an outer join, window, aggregation, limit, volatile expression, or security barrier may change results. Pre-aggregation can improve both correctness and performance when it establishes the intended grain. Approximate algorithms, nondeterministic aggregations, and lossy casts need explicit contracts.

CTE inlining or materialization is engine/version/plan behavior. Do not use a CTE as a performance hint unless the dialect supports and the plan confirms it. Likewise, clustering, partitioning, indexes, statistics, and result caches change physical work but do not repair a wrong logical population.

Set budgets for scanned bytes, elapsed and queue time, spill, output volume, concurrent load, and total cost. A query that passes correctness but exceeds its operating envelope is not ready to publish. Performance gates must tolerate controlled variation and distinguish infrastructure contention from plan regressions.

### Govern security and privacy end to end

Use separate least-privilege roles for compile/read, candidate write, test, publish, and administration where practical. A transformation worker should not gain unrestricted ability to replace every trusted dataset. Publication authority should be narrow and auditable.

Parameterize values and allowlist identifiers. Templates are code generation, not injection protection. Keep secrets out of SQL text, compiled artifacts, query labels, logs, and test fixtures. Consider whether warehouses retain query history and error samples.

Preserve tenant predicates and row/column policies through staging and publication. Test positive and negative authorization contexts. Understand whether views use invoker or definer rights and whether materialization copies data outside the original policy boundary. Derived values can remain sensitive even after source columns are removed.

Use masked or synthetic development fixtures where production data is not authorized. Prevent small-cell disclosure and unsafe debugging exports. Lineage must identify sensitive propagation without granting catalog readers access to raw values.

### Evolve schemas and semantics deliberately

Avoid `SELECT *` at stable boundaries. An added upstream column can alter output contracts, expose sensitive data, change positional unions, or cause ambiguous names. Enumerate and cast published columns. At source-near layers, preserve unknown fields only under a deliberate evolution and privacy policy.

Classify changes as compatible additive, restrictive, breaking, or semantic. A type widening may still alter comparison or storage. Renaming a metric while keeping its values is an interface change; keeping a name while changing population is a more dangerous semantic change.

Version model contracts and coordinate consumers. Run old and new generations in parallel for high-risk migrations, compare keys/components/questions, and publish through an explicit compatibility plan. Retain rollback inputs and prior valid output until the observation window closes.

When a model is removed or renamed, retire its physical relations and lineage under governance. Tooling may not automatically drop orphaned relations. Stale tables can keep serving obsolete meaning and confuse discovery.

### Operate incidents and recovery

Classify failures by compile/reference, source availability/cut, engine/resource, semantic/data-quality, security, candidate build, publication, or downstream consumption. The response differs: retry transient compute, quarantine invalid input, block publication on semantic failure, revoke unsafe output, or roll back the trusted pointer.

Preserve evidence before cleanup: run manifest, compiled SQL, engine job and plan, input generations, candidate relation, test failures, logs, and publication state. Avoid deleting the only failing rows or recompiling an unrecorded variant during diagnosis.

A recovery drill should rebuild from retained source cuts into an isolated generation, reproduce or explicitly explain changed outputs, run gates, and publish/roll back under controlled authorization. Measure recovery time and resource capacity at realistic scale.

After an incident, improve the contract or mechanism that failed. “Be careful with joins” is weak. A declared many-to-one key assertion and fanout gate are durable controls. “Retry the model” is weak. An immutable candidate identity and ambiguous-commit lookup protocol make retry safe.

## Definitions and Notation

Let:

- $G=(V,E)$ be the model dependency graph, with source and transformation vertices;
- $P(v)=\{u:(u,v)\in E\}$ be the direct parents of model $v$;
- $C(s)$ be the immutable cut or generation selected for source $s$;
- $Q_v$ be the fully compiled, dialect-specific query for $v$;
- $K_v$ be the model contract: grain, key, schema, null/type/time rules, invariants, and publication policy;
- $R_v^r$ be the candidate relation produced for model $v$ in logical run $r$;
- $M_r$ be the immutable run manifest containing graph/code/config, cuts, compiled digests, attempts, checks, and target identities;
- $g_v^r$ be the physical candidate generation for $R_v^r$; and
- $p_v$ be the trusted pointer or consumer-visible identity for model $v$.

For a topological order $\tau$, every edge $(u,v)$ must satisfy $\tau(u)<\tau(v)$. This proves predecessor availability only. A valid candidate additionally satisfies:

$$
R_v^r=Q_v\left(\{R_u^r:u\in P(v)\},C,K_v\right)
$$

under the recorded engine and session semantics, and passes gate set $A_v(R_v^r,M_r)$.

Publication is a conditional state transition:

$$
p_v:g_{old}\longrightarrow g_v^r
$$

only if $A_v$ passes and the observed prior pointer still equals the expected $g_{old}$. This comparison prevents a stale attempt from overwriting a newer generation.

For left and right bag multiplicities $a_k$ and $b_k$ at join key $k$, an equijoin can emit $a_kb_k$ pairs. If version resolution establishes $a_k\leq1$ and right pre-aggregation establishes $b_k\leq1$, order-grain output has at most one joined row per $k$. These inequalities require enforced or validated premises; naming a CTE `deduplicated` or `aggregated` proves nothing.

A deterministic model requires a declared equivalence relation $\approx$ such that repeated evaluation over identical declared inputs yields:

$$
Q_v(I;\theta)\approx Q_v(I;\theta),
$$

where $\theta$ includes engine, session, templates, parameters, and reference generations. The expression is a reproducibility obligation, not a claim that arbitrary engines produce byte-identical physical layouts.

## Mechanisms, Invariants, or Proof Structure

Use this review and execution sequence:

1. freeze business question, input/output grain, key, semantics, owner, and consumers;
2. resolve every source/model reference to an exact authorized generation or cut;
3. compile deterministically and persist templates, macros, variables, dialect, bindings, and SQL digest;
4. reject dependency cycles and derive a resource-aware topological schedule;
5. trace bag multiplicity, three-valued predicates, types, time, deduplication, joins, aggregation, and windows;
6. build each materialized model in an isolated attempt/generation with query/job identity;
7. run unit, contract, key, null, relationship, reconciliation, business, security, and performance gates;
8. publish through a verified conditional/atomic mechanism and record its receipt;
9. emit job/run/dataset lineage and data/control-plane metrics; and
10. retain inputs, artifacts, candidate/prior generations, and evidence through the rollback and audit horizon.

The finite pipeline below expresses the intended transformation in SQL. It is marked schematic because the repository’s isolated verifier deliberately does not provide a database engine; production verification must run compiled SQL in the target dialect.

<!-- bijux-verify: {"id":"sql-transformation-query","mode":"schematic","language":"sql","toolchain":"none","reason":"SQL execution depends on a selected database dialect and engine, neither of which is provided by the isolated snippet runner; the following executable Python model independently recomputes the finite contract."} -->
```sql
with typed_orders as (
  select record_id, order_id, customer_id, source_version, status,
         cast(amount_text as integer) as gross_cents, ingested_at
  from raw_orders
  where status in ('accepted', 'rejected')
    and amount_text not glob '*[^0-9]*'
),
ranked_orders as (
  select *, row_number() over (
    partition by order_id
    order by source_version desc, ingested_at desc, record_id desc
  ) as winner_rank
  from typed_orders
),
accepted_orders as (
  select order_id, customer_id, gross_cents
  from ranked_orders
  where winner_rank = 1 and status = 'accepted'
),
refunds_by_order as (
  select order_id, sum(refund_cents) as refund_cents
  from raw_refunds
  group by order_id
),
order_net as (
  select o.order_id, o.customer_id, o.gross_cents,
         coalesce(r.refund_cents, 0) as refund_cents,
         o.gross_cents - coalesce(r.refund_cents, 0) as net_cents
  from accepted_orders o
  left join refunds_by_order r on r.order_id = o.order_id
)
select customer_id, count(*) as order_count,
       sum(gross_cents) as gross_cents,
       sum(refund_cents) as refund_cents,
       sum(net_cents) as net_cents
from order_net
group by customer_id
order by customer_id
```

The independent executable model below is deliberately small enough to recompute. It establishes two local facts: version resolution plus refund pre-aggregation prevents fanout in this fixture, and a complete winner order makes output independent of insertion order. It does not execute or validate the schematic SQL and does not establish cross-dialect equivalence, production snapshot coherence, atomic publication, security, performance, or recovery.

<!-- bijux-verify: {"id":"sql-transformation-reference-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"typed_orders=5\nrejected_orders=1\nsuperseded_orders=1\ncustomers=((\u0027c1\u0027, 2, 1700, 300, 1400), (\u0027c2\u0027, 1, 800, 100, 700))\ngross_cents=2500\nrefund_cents=400\nnet_cents=2100\nreplay_stable=True\n","stderr":""}} -->
```python
from collections import defaultdict
import random

ORDERS = [
    ("x1", "o1", "c1", 1, "accepted", "1000", "2026-08-01T00:00:01Z"),
    ("x2", "o1", "c1", 2, "accepted", "1200", "2026-08-01T00:00:02Z"),
    ("x3", "o2", "c1", 1, "rejected", "700", "2026-08-01T00:00:03Z"),
    ("x4", "o3", "c1", 1, "accepted", "500", "2026-08-01T00:00:04Z"),
    ("x5", "o4", "c2", 1, "accepted", "800", "2026-08-01T00:00:05Z"),
    ("x6", "o5", "c3", 1, "invalid", "bad", "2026-08-01T00:00:06Z"),
]
REFUNDS = [
    ("r1", "o1", 200),
    ("r2", "o1", 100),
    ("r3", "o2", 50),
    ("r4", "o4", 100),
]

def build(seed):
    orders = ORDERS.copy()
    refunds = REFUNDS.copy()
    random.Random(seed).shuffle(orders)
    random.Random(seed + 100).shuffle(refunds)

    typed = [
        row for row in orders
        if row[4] in {"accepted", "rejected"} and row[5].isdecimal()
    ]
    winners = {}
    for row in typed:
        order_id = row[1]
        authority = (row[3], row[6], row[0])
        if order_id not in winners or authority > winners[order_id][0]:
            winners[order_id] = (authority, row)

    refunds_by_order = defaultdict(int)
    for _, order_id, refund_cents in refunds:
        refunds_by_order[order_id] += refund_cents

    customers = defaultdict(lambda: [0, 0, 0, 0])
    for _, row in winners.values():
        _, order_id, customer_id, _, status, amount_text, _ = row
        if status != "accepted":
            continue
        gross = int(amount_text)
        refunded = refunds_by_order[order_id]
        summary = customers[customer_id]
        summary[0] += 1
        summary[1] += gross
        summary[2] += refunded
        summary[3] += gross - refunded

    rows = tuple(
        (customer_id, *customers[customer_id])
        for customer_id in sorted(customers)
    )
    rejected = sum(row[4] == "rejected" for row in typed)
    superseded = len(typed) - len(winners)
    return rows, len(typed), rejected, superseded

first, typed, rejected, superseded = build(7)
second, _, _, _ = build(91)
print(f"typed_orders={typed}")
print(f"rejected_orders={rejected}")
print(f"superseded_orders={superseded}")
print(f"customers={first}")
print(f"gross_cents={sum(row[2] for row in first)}")
print(f"refund_cents={sum(row[3] for row in first)}")
print(f"net_cents={sum(row[4] for row in first)}")
print(f"replay_stable={first == second}")
```

The SQL and reference model intentionally drop invalid `o5` before the typed boundary, retain both valid `o1` occurrences until an authoritative version window chooses version 2, filter the authoritative rejected `o2`, and aggregate refunds before joining. Refund `r3` for rejected `o2` does not enter accepted-order net. The SQL output orders by customer because SQL does not promise physical order without `ORDER BY`.

The example’s `GLOB` predicate and integer cast are SQLite-specific teaching choices. A production pipeline needs an explicit invalid-numeric parser/quarantine contract in its own engine. The example also assumes refunds are immutable uniquely keyed events; versioned or duplicated refunds would need their own identity-resolution stage before aggregation.

## Alternatives and Trade-Offs

**One query versus a model graph.** One query can share a statement snapshot, avoid persisted intermediates, and let the optimizer see across boundaries. It can become hard to test, own, reuse, isolate, and recover. A graph creates contracts and selective execution but adds objects, scheduling, snapshot coordination, and stale-parent risk. Split at semantic/operational boundaries, not line count.

**CTE versus persisted intermediate.** A CTE keeps logic local and avoids lifecycle management. Persistence provides inspectability, reuse, failure isolation, stable statistics, and recovery at storage and refresh cost. Engine-specific materialization behavior must be measured.

**View versus table.** A view offers current logical results and low deployment storage, while shifting compute, availability, and possibly snapshot inconsistency to reads. A table gives a bounded generation and fast stable reads but requires refresh, storage, publication, and staleness management.

**Declarative select versus procedural DML.** A select-defined candidate is easy to test independently and materialize through a controlled adapter. Custom DML can be efficient or necessary but expands idempotency, transaction, concurrency, retry, and dialect obligations.

**Full rebuild versus incremental change.** Full builds are simpler semantic oracles and handle deletes/corrections naturally within the selected cut; they may exceed time/cost windows. Incremental builds reduce work but require boundary completeness and equivalence testing. Maintain periodic full comparison even after incremental adoption.

**Warehouse-native SQL versus external/dataframe processing.** SQL exploits data locality, optimizer statistics, governance, and familiar review. External engines provide libraries, custom algorithms, and compute isolation but add movement and serialization. DE-033 develops dataframe pipelines; hybrid boundaries should retain equivalent contracts and lineage.

**Handwritten repetition versus macros.** Repeated explicit SQL can drift and be tedious. Macros centralize invariants and portability but can hide dependencies and generate surprising code. Prefer narrow, deterministic, tested macros with inspectable compiled output.

**Portable subset versus dialect specialization.** Portable SQL can lower migration cost and make behavior familiar. Dialect features may provide correctness, performance, atomicity, or governance unavailable in the subset. Isolate specialized behavior behind tested adapters and record the exact dialect rather than claiming portability from syntax similarity.

**Early versus late validation.** Early checks localize defects and prevent expensive downstream work. Some business and relationship invariants require integrated outputs. Use cheap source/stage gates early and end-to-end reconciliation before publication.

**Serial versus parallel graph execution.** Parallel independent nodes reduce makespan but increase warehouse contention and can expose cut inconsistencies. Schedule within resource budgets and generation dependencies; graph independence does not imply resource independence.

**Automatic versus manual publication.** Automatic promotion reduces latency when deterministic critical gates are strong. Manual approval adds judgment for high-consequence semantic changes but can become ceremonial. Bind approval to immutable evidence and expire it when the candidate changes.

## Failure Modes and Misconceptions

- **“The DAG is green, so the data is correct.”** A graph reports execution state. Correctness needs semantic contracts, independent checks, and publication evidence.
- **“Topological order gives a consistent snapshot.”** It orders parents before children; separate statements can still observe different source or parent generations.
- **“A CTE is materialized.”** Treatment depends on engine, version, query, hints, and optimizer. Inspect documentation and plans.
- **“One CTE equals one model.”** Syntax does not define an ownership or persistence boundary. Split by durable grain, contract, reuse, and recovery needs.
- **“`SELECT *` is future-proof.”** It silently changes contracts, positional unions, privacy exposure, and downstream compilation.
- **“`DISTINCT` fixes duplicates.”** It collapses equal projections rather than resolving entity/event identity and can hide fanout.
- **“The latest timestamp identifies truth.”** Ties, clock skew, late arrivals, source precedence, corrections, and tombstones require an authoritative winner policy.
- **“Window ordering orders the final result.”** Only the query’s final `ORDER BY` promises presentation order.
- **“Views are always fresh.”** Their answers depend on underlying snapshots, caching/materialization, transaction timing, and source availability.
- **“Views are free.”** Compute and failure move to consumer time; repeated reads and deep stacks can be expensive.
- **“Tables are reproducible.”** A mutable table without input generations, code/config identity, and publication receipt is only stored state.
- **“Templates make SQL portable.”** Dialects differ in types, functions, collation, time, null order, DDL, transactions, and optimizer behavior.
- **“Compilation is deterministic.”** Ambient variables, mutable packages, metadata order, current time, and network lookup can alter rendered SQL.
- **“Passing locally proves warehouse behavior.”** A small engine fixture does not prove production dialect, plans, scale, concurrency, security, or transactions.
- **“A transaction wraps the whole deployment.”** Product-specific DDL and multi-statement limitations may prevent that assumption.
- **“Timeout means failure.”** The server may still be running or may have committed. Resolve by persisted job/run/candidate identity.
- **“Retry means execute again.”** A safe retry resumes or reconciles one logical run; blind append or replace can duplicate or regress data.
- **“Downstream selection is always safe.”** New children can combine incompatible old parents, cuts, macros, or contracts.
- **“Equal row counts prove equivalence.”** Keys, multiplicity, types, nulls, components, and slices can differ while counts match.
- **“Optimization is semantics-neutral.”** Hand rewrites can move filters, change join multiplicity, alter rounding order, or expose nondeterministic ties.
- **“Lineage parser output is complete.”** Dynamic SQL, procedures, macros, external functions, and business meaning can escape parsing.
- **“Tests should run after publication.”** Post-publication monitoring is necessary, but critical candidate gates must protect trusted consumers first.
- **“Removing model code removes the table.”** Orphaned relations may remain discoverable and consumed until explicitly retired.
- **“The orchestrator owns transactions.”** It coordinates tasks; the engine/catalog owns data commits and must provide authoritative receipts.

## Worked Examples

### Example 1

A team has `raw_orders`, `stg_orders`, `current_orders`, `refunds_by_order`, and `customer_net_revenue`. Edges are source-to-stage, stage-to-current, raw-refunds-to-refund-aggregate, and both order-grain models to customer revenue. A topological scheduler may build the orders and refunds branches concurrently, then build revenue after both publish candidates. The manifest binds exact parent generations; “both tasks finished today” is insufficient.

### Example 2

Two valid occurrences exist for order `o1`: versions 1 and 2. A developer uses `SELECT DISTINCT order_id, customer_id, amount`. Because amounts differ, both rows survive. The correct current-state stage partitions by `order_id`, orders by authoritative source version plus stable tie-breakers, retains rank one, and asserts one row per order. Distinct value elimination is not version resolution.

### Example 3

One order has two lines and three refunds. Joining raw lines to raw refunds produces six pairs. Summing line and refund amounts from that bag multiplies both measures. Aggregate lines to one row per order and refunds to one row per order, assert those keys, then join. The maximum multiplicity becomes one per order under the validated premises.

### Example 4

A SQL template calls `ref('current_orders')` and a macro that chooses a tax table from an ambient region variable. The declared graph contains only `current_orders`, so a tax-table change does not select the model. The repair makes region an explicit versioned variable, registers the resolved tax dataset as an input, pins the macro package, and records compiled SQL and relation bindings.

### Example 5

A developer expects a PostgreSQL CTE referenced twice to be inlined for predicate pushdown. The documented behavior depends on side effects, reference count, and materialization controls. The team examines the actual version’s plan, then either rewrites, uses an appropriate documented control, or persists a shared intermediate. It does not treat CTE spelling as a portable physical guarantee.

### Example 6

A `ROW_NUMBER()` model orders corrections only by `corrected_at`. Two corrections share the timestamp. Results appear stable until a compaction changes scan order. The contract adds source authority and occurrence ID to a total order, tests tied timestamps and shuffled insertion, and flags conflicts where the tie-breaker is deterministic but not evidence of business authority.

### Example 7

A nightly build writes directly to `finance.revenue`. A quality test fails after the replacement, so consumers already see invalid output. The redesign builds `revenue__generation_<id>`, runs schema, key, ledger, privacy, and performance gates, then conditionally moves a catalog pointer from the expected prior generation. The receipt supports audit and fast rollback.

### Example 8

A client times out while publishing. The orchestrator marks the task failed and begins another attempt. Because the first transaction may have committed, the worker first queries the publication receipt by logical run ID. If committed, it adopts success; if absent and the prior pointer remains expected, it retries; if state conflicts, it stops for reconciliation.

### Example 9

A source adds `email_address`. A staging model uses `SELECT *`, and a downstream table begins storing the sensitive column even though no business contract requested it. Explicit projection would have prevented propagation. The response classifies and removes exposure, audits generated artifacts and query history, adds a privacy-aware schema change gate, and updates source evolution policy.

### Example 10

A view-based pipeline is functionally correct but a dashboard now takes 90 seconds because every read recomputes three large joins. The team captures plans and workload concurrency, identifies a stable reused order-grain boundary, materializes it as isolated table generations, validates semantic equivalence on keys/components, sets refresh and cost SLOs, and preserves views for lightweight projections. Materialization follows evidence rather than a blanket rule.

## Cross-Program Connections

Database Engineering supplies SQL’s bag, null, type, constraint, plan, transaction, locking, and isolation semantics. The dedicated correctness treatment in [DBE-020](../../18-database-engineering/modules/020-writing-correct-sql-under-duplicate-and-null-semantics.md) is the query-level prerequisite; this module adds graph, compilation, materialization, evidence, and publication.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects model contracts to modularity, dependency direction, versioning, and durable ownership. SQL templates and macros are software components and need tests, pinned dependencies, reviewable interfaces, and release discipline.

[Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) connects fixtures, independent oracles, metamorphic relations, mutation tests, coverage limits, and release gates. A high test count cannot compensate for untested business questions or circular expected values.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects retries, ambiguous completion, logical clocks/cuts, idempotency, concurrency, conditional writes, and consistency. An orchestrated warehouse pipeline is a distributed system across clients, schedulers, engines, catalogs, object stores, and consumers.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects requirements, interfaces, hazards, verification evidence, configuration control, observability, and recovery drills. A SQL result is only one component inside a sociotechnical decision system.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects published relations to versioned consumer contracts, compatibility, authorization, idempotency, and SLOs. A table or semantic view can be an API even when no HTTP endpoint exists.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects paved-road compilation, isolated environments, credentials, scheduling, lineage, policy, cost controls, and self-service. A platform should make safe defaults easy while leaving engine-specific behavior visible.

Security Engineering connects least privilege, injection resistance, tenant isolation, sensitive-data propagation, audit, and incident response. Materialization and query history can create new protected copies even when the final projection omits a sensitive field.

## References

1. dbt Labs, [SQL models](https://docs.getdbt.com/docs/build/sql-models). Defines a dbt SQL model as a select statement, documents model materializations, compiled artifacts, dialect execution, and graph construction through references. Accessed 2026-09-02.
2. dbt Labs, [About the `ref` function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref). Documents dependency creation, environment-aware relation resolution, and versioned model references. Accessed 2026-09-02.
3. dbt Labs, [Add data tests to your DAG](https://docs.getdbt.com/docs/build/data-tests). Documents SQL assertions that select failing records and their attachment to model resources. Accessed 2026-09-02.
4. PostgreSQL Global Development Group, [WITH queries](https://www.postgresql.org/docs/current/queries-with.html). Documents common table expressions, recursion, data-modifying CTEs, and version-specific materialization controls. Accessed 2026-09-02.
5. PostgreSQL Global Development Group, [Window functions](https://www.postgresql.org/docs/current/functions-window.html). Documents partitions, peer ordering, frames, ranking, and aggregate window behavior. Accessed 2026-09-02.
6. PostgreSQL Global Development Group, [CREATE TABLE AS](https://www.postgresql.org/docs/current/sql-createtableas.html). Documents creating and populating a new table from query output. Accessed 2026-09-02.
7. Google Cloud, [Multi-statement transactions](https://cloud.google.com/bigquery/docs/transactions). Documents BigQuery transaction scope, snapshot isolation, commit/rollback behavior, concurrency, transaction IDs, and limitations. Accessed 2026-09-02.
8. OpenLineage, [Object model](https://openlineage.io/docs/spec/object-model/). Defines Job, Run, Dataset, runtime events, metadata events, and extensible facets for lineage. Accessed 2026-09-02.
9. SQLite, [Window functions](https://www.sqlite.org/windowfunctions.html). Documents SQLite window syntax and behavior used by the finite executable teaching fixture. Accessed 2026-09-02.

## Exercises

### Exercise 1

A pipeline has sources `orders` and `refunds`; models `stg_orders`, `current_orders`, `refunds_by_order`, `order_net`, and `customer_daily`; and edges `orders -> stg_orders -> current_orders -> order_net -> customer_daily` plus `refunds -> refunds_by_order -> order_net`. Give one valid topological schedule, identify which nodes may run concurrently, and explain why the schedule alone does not establish a coherent source cut or correct output.

### Exercise 2

At order `o7`, `current_orders` accidentally contains two occurrences with gross values 100 and 120, while `refunds` contains three immutable events of 10, 20, and 5. Compute the row count, summed gross, and summed refund after joining the two raw sides on `order_id` and aggregating. Then compute the intended result if order version 120 wins and refunds are pre-aggregated. State the required grain assertions.

### Exercise 3

A model chooses the latest account state using `ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY updated_at DESC)`. Two rows for account `a1` share timestamp `2026-08-31T12:00:00Z`: source version 7/occurrence `x7` says `active`, and version 8/occurrence `x8` says `closed`. Diagnose the contract defect, write a sufficient winner order if higher source version is authoritative, and explain why merely appending occurrence ID may provide determinism without authority.

### Exercise 4

A deployment compiles a table model, writes directly to `analytics.customer_value`, runs uniqueness after the write, and retries the whole build when the client times out. Redesign its build, gate, publication, receipt, timeout-resolution, and rollback protocol. Include the identities that must be recorded.

### Exercise 5

An optimization replaces a persisted order-grain intermediate with an inlined CTE, pushes `WHERE refund_cents > 0` below a left join, and changes an explicit full-partition window frame to the engine default. Design a validation plan that separates semantic equivalence from performance benefit and names adversarial cases, evidence, and acceptance criteria.

## Answers to the Exercises

### Answer 1

One valid order is `orders`, `refunds`, `stg_orders`, `refunds_by_order`, `current_orders`, `order_net`, `customer_daily`. Sources are availability boundaries rather than necessarily executed tasks. `stg_orders` and `refunds_by_order` may run concurrently once their sources are resolved; `current_orders` depends only on `stg_orders`; `order_net` waits for `current_orders` and `refunds_by_order`; `customer_daily` waits for `order_net`.

The schedule proves only predecessor order. It does not prove that `orders` and `refunds` represent a compatible as-of state, that separate statements share a snapshot, that parent generations match the run manifest, or that any query preserves grain/null/type/time semantics. Bind exact source cuts and parent generations, then validate model contracts and publication.

### Answer 2

The raw join forms $2\times3=6$ pairs. Each gross occurrence repeats three times, so summed gross is $3(100+120)=660$. Each refund repeats for two order occurrences, so summed refund is $2(10+20+5)=70$. The resulting net from those corrupted aggregates would be 590.

If authoritative version resolution first retains gross 120 and refunds pre-aggregate to $10+20+5=35$, the order-grain join emits one row with gross 120, refund 35, and net 85. Assert exactly one `current_orders` row per `order_id` and at most one `refunds_by_order` row per `order_id`; also assert unique refund identity before aggregation and reconcile refund totals before and after the boundary.

### Answer 3

`updated_at` is not a total order, so either tied row may receive rank one. If source version is authoritative and occurrence ID resolves otherwise equal occurrences, use `ORDER BY updated_at DESC, source_version DESC, occurrence_id DESC`, or put source version first if its authority is independent of timestamp. Under the stated data, version 8/`x8` wins and state is `closed`.

Appending only occurrence ID would make repeated execution select consistently, but lexical/highest occurrence ID may have no business authority. Determinism answers “same winner”; authority answers “correct winner.” The contract must define source version monotonicity, conflicts, late corrections, tombstones, and ties, then test them.

### Answer 4

Compile once with pinned code, macros, variables, dialect/adapter, environment bindings, and input generations; persist the compiled SQL digest. Build an isolated candidate such as a generation keyed by logical `run_id` and `attempt_id`, leaving the trusted relation unchanged. Run schema/type, key, null, relationship, reconciliation, business-question, privacy, and representative performance gates against that candidate.

A publisher checks all gates and compares the trusted pointer with the manifest’s expected prior generation. It atomically/conditionally switches to the candidate under verified target semantics and writes a receipt containing model/contract version, run and attempt IDs, input and parent generations, candidate and prior/trusted generations, query/job/transaction IDs, compiled digest, gate evidence, publisher, and commit time.

After timeout, query the job/transaction and receipt by logical run identity. Adopt an already committed result; retry only if the outcome is absent and preconditions still hold; stop on conflict. Rollback repoints to the retained prior valid generation or uses a governed compensating operation, then records another receipt. Blind rebuilding or append is unsafe.

### Answer 5

Freeze one input/source cut, engine/version, session, parameters, code, and output equivalence relation. Run old and new forms against an independent fixture and representative snapshot. Compare canonical keys, per-key multiplicity, columns/types/nulls, additive components, totals, both set differences, and ordered results where promised—not only row counts.

Adversarial cases include an order with no refund, one with one refund, one with several refunds, a stored null refund, negative/reversal refund, duplicate refund identity, tied window peers, empty/all-null partitions, and boundary times. Moving `refund_cents > 0` below a left join may remove no-refund orders or change whether the predicate filters matches versus final rows. The default window frame may differ from the explicit full partition, especially for ordered `last_value` or aggregates.

Only after semantic gates pass should the team compare actual plans, scans, cardinality estimates, joins, sorts, memory/spill, duration, concurrency, and cost on representative scale. Accept when declared semantic outputs and security are equivalent, resource/SLO thresholds pass, the plan is stable across representative parameters, and the new failure/recovery boundary is acceptable. Otherwise retain the persisted model or revise the rewrite.
