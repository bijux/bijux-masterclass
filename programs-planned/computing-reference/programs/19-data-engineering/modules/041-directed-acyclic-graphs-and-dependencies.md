---
module_id: DE-041
program: Data Engineering
level: 1
module_number: 41
title: Directed Acyclic Graphs and Dependencies
status: complete
last_verified: 2026-09-03
---

# Directed Acyclic Graphs and Dependencies

## One-Page Review

### Governing question

How should a data workflow represent, validate, version, and operate dependencies so that every consumer uses the intended upstream generations, independent work remains parallelizable, failures have bounded effects, and changes trigger exactly the required recomputation?

### Essential definitions

- A **directed graph** $G=(V,E)$ contains nodes $V$ and ordered edges $E\subseteq V\times V$. Edge $(u,v)$ means that $v$ directly depends on $u$.
- A **directed acyclic graph** (DAG) is a directed graph with no directed path from a node back to itself.
- A **data dependency** states that a particular downstream result is not valid until named upstream data generations satisfy a declared contract.
- A **control dependency** constrains execution order. It may implement a data dependency, but order alone does not identify the data consumed.
- A **direct predecessor** is joined to a node by one edge. An **ancestor** is reachable through one or more dependency edges.
- A **topological order** is a linear ordering in which every predecessor appears before its dependent. A finite directed graph has such an order exactly when it is acyclic.
- A **source** has no predecessors; a **sink** has no dependents. **Fan-out** sends one result to several consumers; **fan-in** combines several prerequisites.
- A **readiness predicate** decides whether a particular upstream generation is acceptable for a particular downstream run. Terminal process state is not sufficient.
- A **partition mapping** maps a downstream partition to the exact upstream partitions it requires.
- A **graph version** identifies the compiled nodes, edges, edge semantics, code, parameters, and external bindings used by a run.
- The **downstream closure** of changed nodes is the changed set plus every node reachable from it; it is a conservative recomputation and impact-analysis set.
- **Declared lineage** is intended dependency metadata, **compiled lineage** is the graph produced after configuration or code generation, and **observed lineage** records what a particular execution actually read and wrote.

### Central model, mechanism, or theorem

Let each node $v\in V$ denote a logical data-production obligation and each edge $e=(u,v)$ carry contract

$$
C_e=(g_u,\pi_{u,v},r_{u,v},s_{u,v},q_{u,v}),
$$

where $g_u$ selects an immutable upstream generation, $\pi_{u,v}$ maps downstream scope to upstream partitions, $r_{u,v}$ is a readiness predicate, $s_{u,v}$ is a schema/semantic compatibility rule, and $q_{u,v}$ defines acceptable quality and completion evidence. Node $v$ is data-ready for run $x$ only when every required incoming edge resolves:

$$
\operatorname{ready}(v,x)
=
\bigwedge_{(u,v)\in E_x}
\left[
\operatorname{exists}(g_u)
\land r_{u,v}(g_u,x)
\land s_{u,v}(g_u,x)
\land q_{u,v}(g_u,x)
\right].
$$

A topological order prevents execution before a predecessor, but it does not by itself establish this predicate. Correctness additionally requires exact generation binding, complete partition mappings, compatible contracts, explicit branch/skip semantics, isolated publication, and evidence that the compiled and observed graphs agree with the declared graph.

For changed set $S$, the conservative affected set is

$$
\operatorname{closure}^{+}(S)
=S\cup\{v\in V\mid \exists s\in S:\ s\leadsto v\}.
$$

Reducing this set requires stronger semantic evidence such as unchanged code paths, field-level independence, compatible snapshots, or a proved incremental rule; reachability alone cannot justify omission.

### Critical invariants

- Every node and edge has a stable identity, owner, semantic purpose, and versioned definition.
- Data dependencies name exact datasets, generations, partitions, schema/semantic versions, and readiness evidence rather than merely upstream job success.
- The compiled graph contains no missing nodes, self-edges, directed cycles, ambiguous producers, hidden reads, or unintended disconnected outputs.
- A run binds one immutable graph version before scheduling; later graph changes create a new run identity or explicit revision.
- Every downstream partition maps to a complete and minimal set of upstream partitions, including window context and reference data.
- Fan-in waits for all required compatible inputs; optional, skipped, empty, failed, and unavailable inputs remain distinct.
- Conditional paths define which edges become required and how skipped branches affect joins.
- Independent ready nodes may run in any order without changing logical output; deterministic display order is not a semantic execution requirement.
- Failure, cancellation, retry, and manual override propagate according to declared edge policy, never inferred from a generic terminal state.
- Changes invalidate the justified downstream closure, and a published result never combines incompatible upstream epochs.
- Declared, compiled, and observed lineage are reconcilable, with deviations blocked or explicitly governed.
- Graph metadata, run manifests, overrides, and lineage respect tenant, privacy, retention, and authorization boundaries.

### Common failures

Common failures include treating a scheduler arrow as a complete data contract; waiting for “success” while reading an older table generation; omitting an external reference read; adding broad control edges that serialize independent work; removing a direct semantic edge because transitive reachability remains; selecting “latest” independently for each parent; mapping one daily output to only one hourly input; using clock offsets instead of exact interval mapping across workflows; allowing conditional skips to masquerade as success; discovering dependencies after publication eligibility; mutating a graph during a run; accepting one arbitrary topological order as the only correct order; resolving a genuine feedback process with an illegal same-run cycle; recomputing the whole estate for every change; under-invalidating from column-level lineage that is incomplete; trusting declared lineage without comparing observed reads; and exposing sensitive dataset names or cross-tenant relationships through graph metadata.

### Compact example

An orders workflow has two roots: order extraction and exchange-rate extraction. Orders normalize after their extract; rates validate after theirs. Enrichment requires both normalized orders and validated rates, followed by aggregate, validation, and publication. The deterministic teaching order is extract orders, extract rates, normalize orders, validate rates, enrich, aggregate, validate output, publish. The first two roots are simultaneously ready, as are normalize orders and validate rates in the next wave. A rate-validation change affects itself, enrichment, aggregate, output validation, and publication but not order extraction or normalization. With node durations $3,2,4,1,5,3,2,1$, the longest dependency path takes 18 units through order extraction, normalization, enrichment, aggregation, validation, and publication.

### Connections

[DE-040](040-testing-a-multi-stage-batch-pipeline.md) treated a pipeline as a testable graph of stage and edge contracts. This module makes the graph itself operationally precise. DE-042 distinguishes tasks, jobs, assets, and datasets; DE-043 adds schedules and event triggers; DE-044 adds retry, timeout, and idempotency policy; DE-045 and DE-046 specialize partition mappings and backfill planning.

## Governing Question

What must an edge mean before an orchestrator may safely conclude that downstream work is ready?

“Run B after run A” is an ordering statement, not a data guarantee. It does not say which output of A, which partition, which schema version, which quality state, or which publication generation B will read. A may have exited successfully after producing an empty dataset, publishing only some partitions, writing a quarantined candidate, or noticing that another run already owns the output. B may still resolve an older object through a mutable table name. The visible arrow can therefore be satisfied while the data dependency is violated.

Conversely, not every desired ordering is a data dependency. Two jobs may be serialized because they compete for a scarce warehouse slot, touch a maintenance window, or share an unsafe external API. Encoding that resource policy as a data edge invents lineage, expands invalidation, and prevents safe parallelism. Dependency design begins by separating logical data requirements from scheduling, resource, organizational, notification, and convenience constraints.

The governing question has two levels. At definition time, is the graph well formed and semantically complete? At run time, did every edge resolve to compatible immutable inputs for this exact downstream result? Acyclicity answers only part of the first question. Topological scheduling answers only the ordering part of the second.

A useful graph is simultaneously a correctness model, an impact map, an execution partial order, and an evidence index. Those roles overlap but are not identical. Preserve their distinctions explicitly instead of asking one untyped arrow to mean everything.

## Why This Matters

Dependencies determine what data can be trusted together. If a revenue table uses orders through 10:00 but currency rates through 09:00 without a declared compatibility rule, every individual input can be valid while the combined result is not. A graph that binds generations and epochs makes that inconsistency reviewable and preventable.

Missing edges create races and stale reads. A downstream model may begin before a slowly arriving reference partition is complete, or a selected subgraph may omit a prerequisite whose read is hidden in a user-defined function. The run can be reproducible only by accident. Observed lineage and explicit external-input declarations are defenses against this class.

False edges carry a different cost. An unnecessary dependency serializes work, lengthens recovery, broadens the downstream closure, and makes unrelated failures contagious. Operators then bypass the graph with manual overrides, weakening auditability. Minimality is valuable, but only after semantic completeness is established.

Graph topology controls blast radius. A high-fan-out reference dataset may invalidate hundreds of products; a long fan-in join may be blocked by one low-criticality input. Seeing these structures before an incident supports ownership, service objectives, caching, fallback design, and review of whether a shared dependency is too broad.

Cycles reveal unresolved time or state semantics. Fraud scores may influence investigations, whose outcomes retrain the next score. That is a valid feedback system over epochs, but it is not a same-generation DAG. Naming score model $t$, decisions $t$, labels $t+1$, and model $t+1$ converts an apparent cycle into an acyclic version graph and exposes the lag.

Change management also depends on reachability. If a source schema, transformation, reference generation, or policy changes, the downstream closure gives a conservative candidate set for retest, rebuild, notification, and contract review. Under-invalidation publishes stale derivations; indiscriminate full recomputation wastes capacity and may exceed recovery objectives.

Finally, graph metadata can be sensitive. Dataset names reveal customers, health conditions, investigations, or commercial relationships. Cross-tenant lineage can become an information leak even when underlying data access is correctly denied. Graph design therefore includes authorization, redaction, retention, and audit policy.

## Prerequisites and Retrieval

Retrieve the complete logical data-product inventory; stable node and edge identifiers; owners and consumer contracts; current declared workflow definitions; compiled graphs after macros, environment configuration, dynamic mapping, and code generation; actual input/output lineage from representative runs; source and reference manifests; immutable dataset-generation identifiers; schemas and semantic versions; partition definitions, calendars, time zones, watermarks, window context, and mapping rules; conditional branches, trigger rules, skip/empty/failure semantics, and join behavior; publication and candidate-generation rules; external workflow and cross-system dependencies; graph/version/run manifests; selection and backfill behavior; retry and override records; service objectives and freshness requirements; resource/concurrency constraints; security classifications and tenant boundaries; incident history; change-impact procedures; and graph validation/test results.

Distinguish logical node from run instance; data product from producing computation; direct predecessor from ancestor; data dependency from control ordering; dependency from resource exclusion; definition graph from per-run expanded graph; graph version from mutable source code; declared from compiled from observed lineage; source from root run; sink from published product; readiness from process completion; empty from missing; optional from skipped; skip from failure; successful computation from accepted dataset; generation identity from table name; partition ownership from read context; wall-clock alignment from semantic interval mapping; direct edge from transitive reachability; legal feedback across epochs from a same-run cycle; downstream closure from mandatory rebuild set; graph reachability from field-level influence; and critical path estimate from a duration guarantee.

Create a dependency contract table:

| Concern | Required decision and evidence |
|---|---|
| Identity | Stable node, edge, product, graph-version, run, and generation identifiers |
| Meaning | Data, control, resource, quality, publication, or notification relationship |
| Producer | One authoritative producer or a governed multi-producer resolution rule |
| Input binding | Exact upstream generation, code/reference epoch, and compatibility range |
| Partition mapping | Downstream scope to complete upstream ownership and context partitions |
| Readiness | Existence, completeness, quality, schema, freshness, and publication predicates |
| Branching | Condition, required/optional edges, skip propagation, and fan-in trigger rule |
| Failure | Block, degrade, substitute, quarantine, cancel, or continue policy with authority |
| Change | Invalidation seed, closure rule, exemptions, evidence, and consumer notification |
| Runtime | Immutable compiled graph, selected subgraph, resolved edges, and overrides |
| Lineage | Declared/compiled/observed reconciliation and hidden-read detection |
| Governance | Owner, access control, tenant scope, retention, redaction, and audit |

Write one edge in falsifiable form: “For downstream partition 2026-09-01, enrichment requires the published normalized-orders generation selected from source manifest M and all 24 validated hourly rate partitions for the same UTC day under schema range 3.x; missing, quarantined, superseded, or unvalidated inputs do not satisfy readiness.”

## Learning Objectives

After completing this module, you should be able to:

1. model data-production obligations as a directed graph with typed, versioned edge contracts;
2. distinguish logical data dependencies from control, resource, schedule, quality, and notification relationships;
3. prove a finite graph acyclic or exhibit a directed cycle, and derive valid topological orders and readiness waves;
4. specify exact generation binding, readiness predicates, partition mappings, fan-in, fan-out, and conditional paths;
5. represent iterative and feedback processes as acyclic versioned or epoch-indexed graphs;
6. validate graph structure for missing nodes, self-edges, cycles, ambiguous producers, hidden dependencies, and orphan outputs;
7. compute conservative downstream closures and justify any narrower rebuild or retest set;
8. version a compiled graph and reconcile declared, compiled, and observed lineage for each run;
9. reason about cross-workflow dependencies, dynamic graphs, publication, failure propagation, overrides, and recovery; and
10. govern dependency metadata for ownership, service objectives, security, privacy, tenancy, retention, and audit.

## Core Exposition

### Start with data obligations, not executable containers

A useful node says what data obligation becomes true, not merely which process starts. “Validated daily orders for tenant A and UTC date d” is stronger than “PythonOperator 17.” The former has a product identity, partition, schema, quality contract, and observable generation. Several implementations could satisfy it; one implementation could also produce several products.

This module uses nodes as logical production obligations so the graph describes correctness. DE-042 will compare tasks, jobs, assets, and datasets in detail. For now, record both the logical product and its producing action when the distinction matters. An activity may consume several entities and generate several entities; W3C PROV-O similarly distinguishes Entity, Activity, and Agent and offers explicit used, generated, and derived-from relations.

Edges point from prerequisite to dependent. Pick one convention and state it, because libraries differ in input representation. Here $(u,v)$ means “v depends directly on u.” A predecessor map therefore stores each node with the set it requires. Python’s standard-library TopologicalSorter also accepts a node-to-predecessors graph.

### Give every edge a type and contract

At minimum, distinguish:

- **data edge**: downstream output semantically derives from an upstream dataset;
- **control edge**: one action must occur after another even without data flow;
- **quality edge**: publication requires a validation result;
- **publication edge**: a candidate must be promoted before a consumer may resolve it;
- **resource constraint**: actions cannot overlap because of capacity or mutual exclusion;
- **notification edge**: an event follows a state transition but does not make the data valid; and
- **observed lineage edge**: runtime evidence says a read or write happened.

These may be related. A data edge usually induces some control constraint, but a storage engine may reuse an already-published parent without rerunning its producer. A resource constraint belongs in a scheduler policy or resource graph, not data lineage. A quality assertion may itself be a data product whose exact result must be bound to the candidate it evaluated.

An edge contract names the upstream product and generation-selection rule, downstream scope, partition mapping, readiness and quality predicates, compatibility range, failure/skip behavior, and evidence. Without these, the graph supplies reachability but not trustworthy consumption.

### Bind generations, not mutable names

Suppose enrichment requires orders and rates. Resolving “orders_current” and “rates_current” at separate instants can produce a combination no producer or owner approved. Instead, the run manifest selects immutable generation IDs under an epoch or compatibility rule before execution. Every retry uses the same bindings unless a new run/revision is created.

Version references deliberately. dbt’s ref function declares a dependency and can resolve a versioned model; an unpinned reference may select the latest version under its rules. In any system, “latest” is a policy, not an identity. Record what it resolved to.

The graph version should cover compiled topology, edge types and predicates, code artifacts, parameters that affect topology, environment-specific external bindings, and schema/semantic compatibility declarations. Hashes can detect change, but a hash is not a human-meaningful contract and does not prove the referenced content is correct.

### Define readiness as a data predicate

For downstream run $x$, predecessor completion is necessary only when that run actually produces the required generation. Readiness can require:

- the exact generation exists and its manifest is durable;
- every required partition is present;
- schema and semantic versions are compatible;
- blocking quality assertions passed for that same candidate;
- watermark or source completeness meets the declared boundary;
- publication or isolation state is acceptable;
- the upstream epoch matches other fan-in inputs; and
- authorization permits the downstream identity to resolve it.

Treat missing, empty, quarantined, skipped, failed, cancelled, superseded, and successful as different states. An empty partition can be a valid complete dataset with zero rows. A missing partition has no such evidence. A skipped optional branch may be acceptable under one fan-in rule, whereas a skipped required branch must block.

Airflow documents DAGs as workflows containing tasks and dependencies/control flow, with trigger rules affecting how upstream states permit downstream scheduling. That mechanism is useful, but the data system must still bind task state to the precise dataset generation and quality evidence.

### Validate acyclicity and topological order

A directed cycle $v_0\to v_1\to\cdots\to v_k=v_0$ says each member requires a later member in the same dependency interpretation. No node in that cycle can become ready from the graph alone. Detect cycles during compilation, before operational scheduling.

Kahn’s algorithm maintains each node’s unresolved-predecessor count. It begins with all zero-count nodes, emits ready nodes, removes their outgoing edges, and exposes newly ready nodes. If fewer than $|V|$ nodes are emitted, a cycle remains. Depth-first search with temporary/permanent marks is another valid method.

Topological order is generally not unique. For edges $a\to c$ and $b\to c$, both $(a,b,c)$ and $(b,a,c)$ are valid. Deterministic lexical tie-breaking helps tests, manifests, and review diffs; it does not mean a runtime must serialize ready nodes lexically. Correct independent nodes may execute concurrently or complete in different orders.

A readiness wave groups nodes exposed together when processing prior waves as a barrier. It is useful for explanation and coarse planning, not an optimal schedule: resource limits, durations, streaming availability, and partial fan-in can yield a different runtime plan.

### Treat fan-in and fan-out deliberately

Fan-out makes one upstream change operationally important. A country-code reference used by hundreds of products needs strong compatibility, staged publication, owner notification, and impact analysis. It may warrant domain-specific intermediate products to avoid coupling every consumer to an excessively broad source.

Fan-in combines independent prerequisites. Define whether all are required, whether some are optional, and which generations form a compatible cut. A join of orders and exchange rates may require a full day of orders plus 24 hourly rate partitions. “Both parent jobs succeeded” is weaker than proving this mapping.

At a fan-in join, distinguish terminal-state rules from data completeness. “All successful,” “none failed,” “at least one succeeded,” and “branch selected” are different control predicates. Each must be reconciled with what data the node promises to emit.

### Map partitions by semantics

A downstream partition need not map one-to-one to an upstream partition. Common mappings include:

- one daily output from 24 hourly inputs;
- one monthly output from all daily inputs in the month;
- a rolling seven-day feature from the owned day plus six context days;
- a dimension snapshot selected as-of event time;
- a global reference generation used by every tenant/day output;
- one upstream partition fanning into several downstream regions; and
- key-based mappings unrelated to wall-clock boundaries.

Define ownership separately from read context. A windowed node may own output day $d$ while reading $d-6$ through $d$. A change to context day $d-3$ can invalidate several later owned outputs.

Time mapping needs calendar, time zone, boundary inclusivity, precision, daylight-saving policy, watermark/completeness rule, and source-to-business-time interpretation. Sleeping until a fixed clock offset does not prove the correct interval exists.

### Make conditions part of the graph semantics

Conditional branches can be represented as guarded edges or as a compiled per-run subgraph. Either approach must make the predicate, evaluated inputs, version, outcome, and resulting required edges observable.

Do not let a skip silently satisfy a normal-success dependency. At a branch join, define expected selected paths and whether unselected paths produce explicit empty products, absent optional products, or skip receipts. Downstream logic must distinguish them.

Conditions based on data discovered during execution need special care. If discovery changes the dependency set, perform it before freezing readiness for affected nodes, or create a new immutable graph/run revision. Adding an unnoticed dependency after a downstream candidate is eligible to publish violates the original readiness proof.

### Convert feedback into a versioned acyclic graph

Many data systems are iterative: yesterday’s state feeds today’s update; labels train a model that creates later decisions; an aggregate feeds a threshold used next period. The logical domain may have feedback, but each materialized generation can remain acyclic when time or version is explicit.

For recurrence

$$
S_{t+1}=F(S_t,\Delta_{t+1}),
$$

node $S_{t+1}$ depends on prior generation $S_t$ and new input $\Delta_{t+1}$, not on itself. A bootstrap $S_0$, checkpoint policy, and monotone epoch order break the apparent cycle. If convergence iterations occur inside one node, the internal algorithm may loop while the external product graph remains acyclic.

Do not “fix” a real same-run cycle by deleting an edge. Identify the missing lag, ownership boundary, fixed-point computation, or manual decision. The repaired graph should explain which generation influences which.

### Compute downstream closure conservatively

For change seeds $S$, graph traversal over outgoing edges gives the reachable downstream closure. Use it to identify candidate rebuilds, regression tests, contract reviews, owner notifications, cache invalidations, and incident blast radius.

Reachability over-approximates semantic influence when a node reads only unaffected fields or partitions. Narrowing may be justified by complete column lineage, predicate/partition analysis, stable schema compatibility, and a reviewed incremental rule. Record why each excluded reachable node remains valid.

Reachability can also under-approximate when dependencies are hidden, dynamically resolved, or absent from the graph. Compare declared and compiled graphs with observed reads and writes. Unexpected observed edges are defects or governed exceptions, not harmless telemetry differences.

Transitive reduction removes edges while preserving reachability in a DAG. It is unsafe as a blanket cleanup when edges have different semantics. If $A\to C$ directly binds a quality-approved generation, paths $A\to B\to C$ do not necessarily preserve that contract. Remove an edge only when mediation preserves every required property, not merely reachability.

### Version dynamic and external dependencies

Dynamic mapping can expand one logical node into partitions or discovered entities. Define a deterministic expansion input, stable child identity, maximum/failure behavior, and an immutable expansion manifest. Replaying the run should recover the same logical graph even if external discovery later changes.

Cross-workflow dependencies deserve explicit dataset events or generation contracts. Polling another workflow’s last success can bind the wrong interval, environment, or retry. Name the upstream product, partition mapping, compatible graph/code epoch, and authoritative evidence.

External APIs, manually delivered files, and governed approvals are root inputs even when no internal task produces them. Give them manifest/receipt nodes rather than leaving them invisible. A root is not “dependency free”; its completeness obligation is simply discharged outside this graph.

### Reconcile declared, compiled, and observed graphs

The declared graph is what authors intend. Compilation can add macro-generated references, environment-specific routes, selected partitions, or code-derived dependencies. Observed lineage records what a concrete execution used and generated. These views serve different evidence roles.

Reconcile them:

1. Every required declared edge should compile for the applicable run.
2. Every compiled data edge should resolve to an exact input generation or an explicit unavailable state.
3. Every observed read should match an authorized compiled dependency.
4. Every promised output should have observed generation/publication evidence.
5. Differences should block, warn, or receive a time-bounded exception according to risk.

OpenLineage’s lineage job facet permits explicit per-target source relationships, avoiding a false Cartesian interpretation when a job lists several inputs and outputs. This illustrates why edge precision matters: “job used A and B, produced C and D” does not prove that both outputs derive from both inputs.

Observed lineage is not automatically complete. Drivers, views, stored procedures, cached results, external services, and engine limitations can hide access. Treat instrumentation coverage as a measured property.

### Operate from an immutable run manifest

Before scheduling, persist graph version, selected nodes, expanded partitions, edge contracts, exact input generations, parameters, code/environment identities, authorization context, and expected outputs. Changes after binding produce a new run identity or explicit revision.

Record node states and edge-resolution evidence separately. A node retry should not silently resolve newer parents. An authorized rebind must invalidate affected descendants and create auditable evidence.

Publication is a sink obligation, not just the final process. The publication node verifies candidate completeness, blocking quality evidence, parent expectation, exact graph/run identity, and consumer-visible result. A notification may follow publication but must be idempotent and must not define the truth of the data transition.

Manual overrides need scope, actor, reason, evidence, expiry, downstream effects, and an immutable record. “Mark successful” is dangerous when it manufactures a state without a dataset generation. Prefer “adopt generation g after independent verification” or “waive quality rule q for candidate g under authority a.”

### Test and govern the graph

Static validation should check unique/stable IDs, known endpoints, no self-edges, acyclicity, allowed edge types, producer ownership, compatible schemas, complete partition mappings, branch joins, reachable published sinks, and policy constraints. Detect unused roots and orphan outputs for review rather than assuming they are invalid.

Contract tests should compile representative configurations and compare expected edges. Mutation tests can remove a required edge, add a false edge, alter a partition mapping, change a branch rule, or select an incompatible version and verify detection.

Integration tests should delay parents, omit partitions, return valid empty inputs, fail optional/required branches, retry nodes, alter observed lineage, and advance a parent generation during a run. Assert immutable binding, readiness, cancellation, invalidation, publication, and evidence.

Govern ownership and service levels at meaningful boundaries. For each critical node, know which team owns its contract, who approves breaking changes, which consumers receive notice, and which freshness/recovery objective applies. High fan-out or cross-domain edges deserve stronger review.

Authorize graph visibility. Redact or alias sensitive nodes, filter lineage by tenant/domain, protect run parameters and error details, and align retention with data and audit policy. Audit graph edits, overrides, manual rebinds, and lineage exceptions.

## Definitions and Notation

Let $G=(V,E)$ be a finite directed graph. With the convention $(u,v)\in E$, $u$ is a direct predecessor of $v$, and $v$ is a direct successor of $u$. Define

$$
\operatorname{pred}(v)=\{u\mid(u,v)\in E\},
\qquad
\operatorname{succ}(v)=\{w\mid(v,w)\in E\}.
$$

A directed path $u\leadsto v$ is a sequence of directed edges from $u$ to $v$. An ancestor of $v$ reaches $v$; a descendant is reachable from $v$. A source has $\operatorname{pred}(v)=\varnothing$; a sink has $\operatorname{succ}(v)=\varnothing$.

A directed cycle is a nonempty path from a node back to itself. A DAG contains no directed cycle. A topological order is a bijection $\tau:V\to\{1,\ldots,|V|\}$ such that

$$
(u,v)\in E\Longrightarrow \tau(u)<\tau(v).
$$

The ordering relation induced by reachability is partial: independent nodes may be incomparable. A linear topological order extends that partial order and is not generally unique.

For node duration estimate $d(v)\ge 0$, the earliest-finish recurrence in a dependency-only unlimited-resource model is

$$
F(v)=d(v)+
\begin{cases}
0,&\operatorname{pred}(v)=\varnothing,\\
\max_{u\in\operatorname{pred}(v)}F(u),&\text{otherwise}.
\end{cases}
$$

The maximum $F(v)$ over sinks is a longest-path estimate in the DAG. It is not a production completion guarantee: queues, resources, retries, data transfer, partial availability, and duration uncertainty are outside this recurrence.

For changed set $S$, $\operatorname{closure}^{+}(S)$ is the reflexive downstream closure. A minimal mandatory rebuild set $R$ may be smaller only with evidence:

$$
R\subseteq\operatorname{closure}^{+}(S).
$$

The subset relation states a possibility, not permission to omit reachable nodes. Every difference requires a sound equivalence or compatibility argument.

For downstream partition $p_v$, partition mapping $\pi_{u,v}(p_v)$ returns required upstream partitions. Completeness is

$$
\forall p_u\in\pi_{u,v}(p_v):
\operatorname{acceptable}(g_u,p_u,C_{u,v}).
$$

If context partitions influence output without being owned by $p_v$, they still belong in $\pi$.

Graph version $\gamma$ identifies the compiled graph and its edge semantics. Run manifest $M_x$ binds $\gamma$, selected/expanded nodes $V_x$, edges $E_x$, inputs $I_x$, code/configuration $K_x$, and expected outputs $O_x$. Reproducibility requires stable resolution of those identifiers, not only retention of a DAG source file.

## Mechanisms, Invariants, or Proof Structure

A finite graph is a DAG exactly when Kahn’s process emits every node. If a zero-predecessor node exists, removing it cannot create a cycle; repeat. If the graph is acyclic, some zero-predecessor node must exist, because following predecessors forever in a finite graph would repeat a node and form a cycle. If processing stops early, every remaining node has a remaining predecessor, so following predecessors eventually repeats and identifies a cycle.

Topological order proves only precedence. To support downstream validity, establish this assurance chain:

1. **Definition integrity:** nodes and typed edges are complete, owned, compatible, and acyclic.
2. **Compilation integrity:** configuration and dynamic expansion produce the reviewed graph version.
3. **Binding integrity:** the run freezes exact parent generations and partitions under compatible epochs.
4. **Readiness integrity:** each incoming edge’s existence, completeness, schema, quality, and publication predicate passes.
5. **Execution integrity:** observed reads/writes conform to authorized compiled edges and deterministic-envelope rules.
6. **Propagation integrity:** failures, branches, invalidations, and overrides affect descendants under declared policy.
7. **Publication integrity:** only the candidate tied to this graph/run/evidence becomes consumer-visible.
8. **Lifecycle integrity:** changes seed a conservative closure, exceptions are justified, and retained manifests permit reconstruction.

The following finite standard-library model illustrates structural validation, deterministic topological ordering, readiness waves, downstream closure, and longest-path arithmetic. It does not model datasets, partition mappings, distributed scheduling, storage, permissions, failures, quality, or publication.

<!-- bijux-verify: {"id":"data-dependency-dag-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"topology=('extract_orders', 'extract_rates', 'normalize_orders', 'validate_rates', 'enrich', 'aggregate', 'validate_output', 'publish')\nready_waves=(('extract_orders', 'extract_rates'), ('normalize_orders', 'validate_rates'), ('enrich',), ('aggregate',), ('validate_output',), ('publish',))\nrates_change_closure=('aggregate', 'enrich', 'publish', 'validate_output', 'validate_rates')\norders_change_closure=('aggregate', 'enrich', 'extract_orders', 'normalize_orders', 'publish', 'validate_output')\npublish_earliest_finish=18\ncritical_path=('extract_orders', 'normalize_orders', 'enrich', 'aggregate', 'validate_output', 'publish')\ncycle_detected=True\nmissing_dependency_detected=True\n","stderr":""}} -->
```python
from heapq import heapify, heappop, heappush

PREDECESSORS = {
    "extract_orders": set(),
    "extract_rates": set(),
    "normalize_orders": {"extract_orders"},
    "validate_rates": {"extract_rates"},
    "enrich": {"normalize_orders", "validate_rates"},
    "aggregate": {"enrich"},
    "validate_output": {"aggregate"},
    "publish": {"validate_output"},
}
DURATION = {
    "extract_orders": 3,
    "extract_rates": 2,
    "normalize_orders": 4,
    "validate_rates": 1,
    "enrich": 5,
    "aggregate": 3,
    "validate_output": 2,
    "publish": 1,
}


def validate(graph):
    names = set(graph)
    missing = sorted({dep for deps in graph.values() for dep in deps} - names)
    self_edges = sorted(node for node, deps in graph.items() if node in deps)
    if missing or self_edges:
        raise ValueError((missing, self_edges))


def topology(graph):
    validate(graph)
    remaining = {node: len(deps) for node, deps in graph.items()}
    children = {node: set() for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            children[dep].add(node)
    ready = [node for node, degree in remaining.items() if degree == 0]
    heapify(ready)
    order = []
    waves = []
    while ready:
        wave = tuple(sorted(ready))
        waves.append(wave)
        next_ready = []
        while ready:
            node = heappop(ready)
            order.append(node)
            for child in sorted(children[node]):
                remaining[child] -= 1
                if remaining[child] == 0:
                    heappush(next_ready, child)
        ready = next_ready
    if len(order) != len(graph):
        raise ValueError("cycle")
    return tuple(order), tuple(waves), children


def downstream(children, changed):
    affected = set(changed)
    pending = list(changed)
    while pending:
        node = pending.pop()
        for child in children[node]:
            if child not in affected:
                affected.add(child)
                pending.append(child)
    return tuple(sorted(affected))


def earliest_finish(graph, order, duration):
    finish = {}
    parent = {}
    for node in order:
        candidates = sorted(
            ((finish[dep], dep) for dep in graph[node]),
            key=lambda item: (item[0], item[1]),
        )
        prior, chosen = candidates[-1] if candidates else (0, None)
        finish[node] = prior + duration[node]
        parent[node] = chosen
    path = []
    node = max(order, key=lambda name: (finish[name], name))
    while node is not None:
        path.append(node)
        node = parent[node]
    return finish, tuple(reversed(path))


order, waves, children = topology(PREDECESSORS)
finish, critical_path = earliest_finish(PREDECESSORS, order, DURATION)
print(f"topology={order}")
print(f"ready_waves={waves}")
print(f"rates_change_closure={downstream(children, {'validate_rates'})}")
print(f"orders_change_closure={downstream(children, {'extract_orders'})}")
print(f"publish_earliest_finish={finish['publish']}")
print(f"critical_path={critical_path}")
try:
    topology({"a": {"b"}, "b": {"a"}})
except ValueError as error:
    print(f"cycle_detected={str(error) == 'cycle'}")
try:
    topology({"a": {"missing"}})
except ValueError as error:
    print(f"missing_dependency_detected={error.args[0][0] == ['missing']}")
```

The two roots form the first wave. Because both roots are removed together, normalize-orders and validate-rates form the second wave. Their fan-in exposes enrichment, followed by the single chain to publication. Lexical ordering makes the printed linearization stable, while the wave structure preserves the intended concurrency.

The rate-change closure includes validation, enrichment, aggregate, output validation, and publication. It excludes the order branch because no path reaches it. The 18-unit path is computed as $3+4+5+3+2+1$. The alternative rate branch reaches enrichment at time $2+1=3$, earlier than the order branch’s $3+4=7$, so it does not determine the illustrative longest path.

The model rejects undeclared predecessors before sorting and reports a cycle when not all nodes can be emitted. A production validator should additionally return a useful cycle witness, validate edge types/contracts, inspect dynamic expansions, check producer uniqueness, and reconcile observed lineage.

## Alternatives and Trade-Offs

**Task-centric versus data-product-centric graphs.** Task graphs map directly to executable units and control state. Product graphs express freshness, lineage, partitions, and consumer contracts more naturally. Many systems need a bipartite or linked view of activities and data entities. Avoid pretending either projection captures both completely.

**Explicit dependencies versus inferred lineage.** Explicit edges are reviewable before execution and support planning. Inference from SQL, code, logs, or engine metadata finds hidden relationships but can be incomplete or overbroad. Use explicit declarations as the contract and observed/inferred lineage as reconciliation evidence.

**Static versus dynamic graphs.** Static graphs are easier to validate, visualize, authorize, and reproduce. Dynamic expansion handles discovered files, tenants, and partitions without enormous source definitions. Freeze expansion inputs and results so each run still has an immutable finite graph.

**Fine versus coarse nodes.** Fine nodes localize failure and invalidation and expose parallelism, but increase metadata, scheduling, and edge-management cost. Coarse nodes hide internal dependencies and enlarge retries. Choose boundaries at independently owned, testable, materialized, or recoverable obligations.

**Direct edges versus minimal reachability.** Extra direct edges can preserve important semantic contracts, quality gates, or generation bindings. Redundant untyped control edges can reduce parallelism. Assess semantic equivalence before transitive reduction.

**Global rebuild versus selective invalidation.** Full rebuild is simple and can be a strong oracle, but may be too slow or expensive. Selective rebuild meets recovery goals only when partition/field lineage and compatibility rules are reliable. Escalate to a broader closure under uncertainty.

**Barrier waves versus eager scheduling.** Waves are deterministic and easy to reason about. Eager scheduling starts a node as soon as its particular parents are ready and can shorten completion. Logical output must not depend on which ready node happens to finish first.

**Cross-workflow polling versus dataset events.** Polling may be easy to add but tends to bind wall-clock/run state rather than data identity. Dataset events or manifests carry generation and partition semantics but require shared contracts and durable event handling.

**Strict blocking versus governed degradation.** Blocking protects correctness when every parent is essential. Some products can use a pinned fallback, omit an optional enrichment, or publish a clearly degraded version. Such behavior requires an explicit alternate contract, visible quality state, consumer acceptance, and expiry—not a generic “continue on failure.”

**Whole-product versus column-level lineage.** Whole-product edges are robust and conservative. Column/expression lineage can narrow impact but is vulnerable to dynamic SQL, row filters, keys, constraints, metadata, UDFs, and semantic changes that do not appear as simple field flow. Use narrower analysis only within measured coverage.

## Failure Modes and Misconceptions

- **“A DAG guarantees correctness.”** Acyclicity permits a topological order; it says nothing about missing edges, bad data, wrong generations, incomplete partitions, or publication.
- **“Upstream success means data-ready.”** Process state must be tied to the exact generation, manifest, quality evidence, and compatibility contract.
- **“The scheduler order is lineage.”** Resource or maintenance ordering can create false lineage, while hidden table/API reads create missing lineage.
- **“There is one topological order.”** Independent nodes can appear in multiple valid orders. Tests that demand one arbitrary order need an explicit tie-breaker.
- **“Transitive edges are always redundant.”** Reachability may be redundant while edge-level quality, partition, or version semantics are not.
- **“Latest is consistent.”** Independently resolved latest parents can belong to incompatible epochs. Freeze exact generations.
- **“Daily maps to daily.”** Time zones, windows, late-data policies, and upstream granularity can make the mapping many-to-many.
- **“Skipped is successful.”** A skip represents branch/control state. It satisfies a data edge only if the edge contract defines the corresponding absence or empty product.
- **“A feedback domain cannot use a DAG.”** Index states and decisions by version or epoch; the apparent cycle often crosses time.
- **“Delete the edge to break the cycle.”** This hides an obligation and creates a race. Identify the lag, fixed point, or ownership error.
- **“The closure is the exact rebuild set.”** It is conservative under complete edges. Semantic narrowing needs evidence; hidden edges can still make it incomplete.
- **“Observed lineage is ground truth.”** Instrumentation may miss cached, indirect, external, or engine-internal access. Measure its coverage.
- **“Dynamic means mutable.”** Runtime expansion can still produce an immutable versioned per-run graph.
- **“A hash explains a graph.”** Digests support identity/integrity but do not communicate meaning, ownership, or compatibility.
- **“Manual success is harmless.”** It may fabricate readiness without a generation. Overrides must identify what evidence substitutes for the normal transition.
- **“Graph metadata is non-sensitive.”** Names, topology, parameters, and lineage can reveal protected relationships and require access control.

## Worked Examples

### Example 1

Graph $a\to c$, $b\to c$, $c\to d$ has two valid topological orders beginning with $a,b$ or $b,a$. The readiness waves are $\{a,b\},\{c\},\{d\}$. Serializing $a$ before $b$ is a deterministic display choice, not a dependency.

### Example 2

A daily sales output needs 24 hourly sale partitions and one rates snapshot selected as-of the close. If hour 17 is missing, “hourly ingestion succeeded” is insufficient. The edge contract blocks until the exact 24-part manifest and rates generation satisfy completeness and quality.

### Example 3

Risk score $t$ influences review decisions $t$, whose outcomes become labels $t+1$, which train model $t+1$. The domain feedback is represented as edges across indexed generations. A same-run edge from model $t+1$ back to its own labels would be an invalid cycle.

### Example 4

Node C reads A directly for an entitlement check and also reads B, which derives aggregates from A. Removing A-to-C because A reaches C through B loses the direct entitlement-generation contract even though graph reachability remains.

### Example 5

A branch chooses domestic or international tax enrichment. The join requires exactly the selected branch plus normalized orders, while the unselected branch emits a recorded skip, not a fabricated empty success. The branch predicate and chosen graph are stored in the run manifest.

### Example 6

A seven-day rolling feature owned by day 10 reads days 4–10. Correcting day 6 invalidates owned outputs for days 6–12, subject to availability and retention. One-to-one date mapping would miss days 7–12.

### Example 7

A run freezes orders generation O7 and rates generation R4. While it executes, O8 becomes current. A retry continues using O7. Adopting O8 requires a new run/rebind and invalidates descendants; silently reading O8 would create a mixed run.

### Example 8

Declared lineage says report C depends on model B. Observed query lineage also shows a direct read from spreadsheet A. Until A is declared, versioned, authorized, and included in invalidation, the graph is incomplete and C’s reproducibility claim is bounded.

### Example 9

Two workflows align by local “daily success,” but one uses UTC days and the other America/New_York business days. Clock-based polling can pair different intervals. A partition mapping with explicit boundaries and time-zone rules identifies the required source cut.

### Example 10

A customer reference has 200 consumers. A breaking identifier change seeds a large downstream closure. Owners may introduce a versioned compatibility projection so old consumers remain on generation 1 while migrated consumers adopt generation 2, reducing simultaneous blast radius without hiding lineage.

## Cross-Program Connections

[DSE-041](../../17-data-structures-engineering/modules/041-adjacency-matrices-lists-and-edge-arrays.md) develops concrete graph representations; this module applies predecessor and successor structures to dataset generations, partitions, and operations. [CONPAR-041](../../04-programming-languages-concurrent-and-parallel-programming/modules/041-task-parallelism-and-dependency-graphs.md) analyzes work, span, grain, and runtime scheduling; here the central concern is data readiness and compatible lineage.

[SYSENG-022](../../26-systems-engineering/modules/022-functional-decomposition.md) connects graph nodes to system decomposition and interfaces. [API-077](../../28-api-and-service-engineering/modules/077-fan-out-and-tail-latency.md) examines service fan-out, where request latency and failure edges differ from dataset derivation. [PLAT-084](../../29-platform-engineering/modules/084-platform-dependency-mapping.md) addresses platform-wide dependency mapping and operational use.

Within Data Engineering, [DE-023](023-file-arrival-and-manifest-processing.md) provides manifest and arrival inputs; [DE-034](034-partitioned-processing.md) and [DE-040](040-testing-a-multi-stage-batch-pipeline.md) supply partition and assurance foundations. DE-042–DE-050 build the operational vocabulary, schedules, retries, partitioned assets, backfills, environments, CI/CD, run metadata, and complete workflow design on this graph model.

## References

1. Python Software Foundation, [graphlib — Functionality to Operate with Graph-Like Structures](https://docs.python.org/3/library/graphlib.html). Documents predecessor-form graphs, topological ordering, ready-node processing, and cycle detection. Accessed 2026-09-03.
2. Apache Airflow, [DAGs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html). Documents DAG workflow structure, task dependencies, control flow, trigger rules, branching, and cross-DAG dependencies. Accessed 2026-09-03.
3. Apache Airflow, [Architecture Overview](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html). Describes DAG/task dependency ordering and versioned DAG bundle behavior in the platform architecture. Accessed 2026-09-03.
4. dbt Labs, [ref](https://docs.getdbt.com/reference/dbt-jinja-functions/ref). Documents dependency declaration, graph construction, build ordering, and references to versioned models. Accessed 2026-09-03.
5. Argo Workflows, [DAG](https://argo-workflows.readthedocs.io/en/latest/walk-through/dag/). Documents multi-root dependency graphs, dependency declarations, conditional enhanced-depends expressions, and fail-fast behavior. Accessed 2026-09-03.
6. Apache Beam, [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Defines a pipeline as a user-constructed graph of transforms over data collections. Accessed 2026-09-03.
7. Apache Beam, [Design Your Pipeline](https://beam.apache.org/documentation/pipelines/design-your-pipeline/). Describes a pipeline as a DAG of steps with multiple sources and sinks and transforms with multiple inputs or outputs. Accessed 2026-09-03.
8. Dagster, [Dagster Documentation](https://docs.dagster.io/). Introduces its declarative asset dependency model and integrated lineage/observability. Accessed 2026-09-03.
9. OpenLineage, [Lineage Job Facet](https://openlineage.io/docs/spec/facets/job-facets/lineage/). Defines explicit input-to-output lineage relationships for jobs and explains why broad input/output arrays can imply false dependencies. Accessed 2026-09-03.
10. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/). Defines Entity, Activity, Agent, usage, generation, derivation, communication, and qualified influence relations for provenance. Accessed 2026-09-03.

## Exercises

### Exercise 1

For predecessor map $A:\varnothing$, $B:\varnothing$, $C:\{A\}$, $D:\{A,B\}$, $E:\{C,D\}$, list all sources and sinks, produce one topological order, give barrier-style readiness waves, and compute the downstream closure of change set $\{B\}$.

### Exercise 2

A daily customer metric reads its day’s events, the prior six days for a rolling feature, a customer snapshot selected as-of each event, and a global policy generation. Write edge contracts and partition mappings. Explain the affected owned-output dates when an event partition on day 8 changes.

### Exercise 3

A workflow contains edges “model depends on labels,” “labels depend on decisions,” and “decisions depend on model.” Diagnose the cycle and redesign it as an acyclic epoch-indexed graph. State bootstrap and reproducibility evidence.

### Exercise 4

An orchestrator reports that all upstream tasks for publication succeeded, but the candidate references orders generation O12 while validation evaluated O11, and exchange-rate generation R8 was resolved after the run began. Determine whether publication is safe and design the run-manifest/readiness checks that would prevent the state.

### Exercise 5

Design a graph-assurance plan for a dynamically expanded, multi-tenant workflow with conditional enrichment, an external reference, and a high-fan-out published product. Include static, compilation, runtime-lineage, mutation, failure, invalidation, security, override, and publication evidence.

## Answers to the Exercises

### Answer 1

Sources are A and B; sink is E. One valid order is $A,B,C,D,E$, though $B,A,D,C,E$ is also valid. Barrier waves are $\{A,B\}$, $\{C,D\}$, $\{E\}$. From B, the path reaches D and then E, so the reflexive downstream closure is $\{B,D,E\}$. C is excluded because its only predecessor is A.

### Answer 2

For owned output day $d$, the events edge maps to context partitions $d-6,\ldots,d$, with explicit calendar/time-zone boundaries and completeness evidence. The customer edge selects immutable snapshot generation/valid-time rows covering each event time, with uniqueness and no-gap/no-overlap rules. The policy edge binds one immutable compatible global generation. If day 8 events change, rolling outputs owned by days 8 through 14 can change because each includes day 8 in its seven-day context; later effects require a different rule. Also invalidate outputs whose as-of customer resolution changes for corrected event times, and verify the policy generation remains compatible.

### Answer 3

The unindexed graph requires each node before itself through a directed path. Introduce model $M_t$, decisions $D_t$, outcomes/labels $L_{t+1}$, and next model $M_{t+1}$, with $M_t\to D_t\to L_{t+1}\to M_{t+1}$. Bootstrap with approved $M_0$ and state what creates first labels. Evidence binds training dataset/label generation, feature/reference cuts, code/environment, decision interval, model artifact, evaluation, and epoch. Rebuilding epoch $t+1$ uses the same $M_t,D_t,L_{t+1}$ bindings instead of current mutable names.

### Answer 4

Publication is unsafe. Validation of O11 does not authorize a candidate containing O12, and late resolution of R8 violates immutable input binding even if R8 is valid. The run manifest must freeze graph version, candidate ID, O12/R8 generation IDs, partitions, schemas, quality-policy versions, code/configuration, and expected parent before execution. Each validation receipt must name that candidate and its exact parents. Publication checks receipt equality, all edge readiness predicates, unchanged candidate fingerprint, and an expected-parent conditional transition. Any rebind creates a new run/revision and invalidates validation and descendants.

### Answer 5

Statically validate stable tenant-scoped identities, known endpoints, edge types, producer rules, branch joins, external-root contracts, partition mappings, acyclicity, and authorized sinks. Compile representative tenants/configurations, freeze discovery inputs and child manifests, and diff expected graph shapes. Reconcile every observed read/write with compiled edges, including indirect external reads, while measuring instrumentation gaps. Mutate by deleting the external edge, changing tenant/partition mapping, treating skip as success, and adding a cross-tenant edge; the suite must fail. Inject missing/late reference, partial expansion, branch failure, retry, cancellation, lineage loss, and parent advance. Compute downstream closure for code/schema/reference changes, then justify narrower tenant/partition sets. Enforce tenant-filtered graph visibility, redacted parameters, least-privilege reads, retention, and audit. Overrides name actor, authority, exact generation, reason, expiry, and descendants. Publication requires complete expansion, exact compatible parents, candidate-bound quality evidence, expected parent, consumer-visible verification, and idempotent notification.
