---
module_id: LSDS-025
program: Large-Scale Data Systems Engineering
level: 1
module_number: 25
title: Lazy Evaluation and Plan Construction
status: complete
last_verified: 2026-09-03
---

# Lazy Evaluation and Plan Construction

## One-Page Review

### Governing question

How should a large-scale data API record intended computation without executing it immediately, then resolve, optimize, submit, and explain the selected plan without surprising users through stale state, repeated work, hidden effects, or unbounded result materialization?

### Essential definitions

- **lazy evaluation** defers producing a transformation's data result until a demanded sink, action, or materialization requires it.
- A **lazy handle** denotes a recipe or graph node, not an already computed collection.
- A **transformation** constructs a derived lazy handle; an **action** requests an observable result or effect and triggers planning/execution.
- An **unresolved logical plan** may contain names and types that require catalog/schema analysis.
- An **analyzed plan** binds identifiers, types, functions, and policies; an **optimized plan** applies semantics-preserving rewrites.
- A **physical plan** chooses algorithms, exchanges, partitioning, resources, and runtime operators.
- **closure capture** packages values referenced by user code for later execution; its timing and serialization semantics matter.
- **common-subplan reuse** computes an equivalent shared ancestor once within a defined execution or persisted lifetime.
- **plan pruning** retains only the dependency closure needed by selected actions.
- A **plan digest** is a canonical hash over declared plan identity; it is useful only when its canonicalization and included context are explicit.

### Central model, mechanism, or theorem

Construction maps each pure transformation to a node whose inputs are prior handles, producing a DAG without reading distributed input. An action selects one or more sinks. The engine computes their transitive dependency closure, analyzes names/types/policies, normalizes and optimizes the logical graph, chooses a physical graph, and submits tasks.

Laziness separates construction time `t_c` from analysis/submission time `t_a` and worker execution time `t_e`. Every captured dependency must define which value or version is observed: snapshot at construction, serialization, analysis, task start, or each record. If this temporal contract is missing, identical source code can produce different plans or results. Laziness permits global optimization and unused-branch pruning, but does not imply caching; separate actions may recompute lineage unless submitted together or explicitly persisted.

### Critical invariants

- Constructing a pure transformation does not read its distributed source or perform its declared external sink effect.
- Each handle belongs to a known graph/session and records all data dependencies needed for execution.
- Analysis binds schema, functions, catalog objects, configuration, authorization, and snapshots under an explicit time/version policy.
- Optimization preserves declared value, error, ordering, nondeterminism, and effect semantics.
- An action submits exactly the required dependency closure plus explicitly required control/effect dependencies.
- Shared work is reused only when code, inputs, configuration, policy, nondeterminism, and result semantics are compatible.
- Repeated actions, joint actions, caching, checkpointing, and persistence have distinct execution/lifetime behavior.
- Result-collecting actions prove the returned data fits driver memory and transport limits.
- Plan explanations identify whether they show unresolved, analyzed, optimized, physical, or executed form.
- Plan, code, dependency, input, side-input, and policy versions are retained for replay and audit.

### Common failures

Frequent failures are believing a lazy handle contains data, expecting errors only at execution when analysis is eager, expecting errors at construction when analysis is deferred, mutating captured driver state after graph construction, reading mutable catalogs or paths at an unspecified time, performing side effects while constructing a plan, invoking an action inside a transformation, collecting an unbounded result to the driver, running separate actions that recompute a costly ancestor, assuming identical-looking code is safe to reuse, caching without materialization/lifetime evidence, and treating an `explain` output as the exact adaptive runtime graph.

### Compact example

A local model builds `source -> filter_even -> map_square -> sum` without reading the source. Its canonical plan is stable and digestible. The first action returns 20 and reads once. A second independent action reads again because laziness is not caching. A joint action requesting sum and even-count shares one evaluation memo and reads once more, not twice. The example demonstrates construction and action boundaries; it does not model distributed optimization, serialization, policy resolution, or cache loss.

### Connections

[LSDS-024](024-directed-acyclic-graph-execution.md) supplies DAG semantics. [LSDS-022](022-map-side-and-reduce-side-processing.md) and [LSDS-023](023-partitioners-and-combiners.md) constrain legal rewrites. [LSDS-026](../ROADMAP.md) schedules constructed stages, while [LSDS-028](../ROADMAP.md) covers lineage and recomputation.

## Governing Question

In an eager program, calling a function normally computes its result now. A large-scale data API often cannot do that economically: the input may span petabytes, require a cluster, or not even be reachable from the driver. Instead, transformations return handles that describe future computation. Execution begins only when the program requests an output or explicitly submits the pipeline.

This temporal separation is powerful and treacherous. The engine sees a larger graph and can push filters, eliminate unused columns, combine operators, select joins, and share work. The user, however, may not know when an invalid column is reported, which version of a table is read, whether a mutated variable is captured, or why two `count` calls scan input twice.

The governing question is how to make plan construction a precise interface rather than a timing trick. Every layer must state what is recorded, what is resolved later, what triggers execution, what can be rewritten, and which identities make an observed run reproducible.

## Why This Matters

Lazy construction gives an optimizer context. A filter written after a projection may be pushed toward the source; two expressions may be fused; a branch never demanded by any action can be removed; and multiple requested results can share an ancestor. These choices can reduce input reads, serialization, shuffle, materialization, and elapsed time.

Without a clear contract, the same choices cause operational incidents. A job passes construction and fails hours later on a missing column because analysis was deferred. A relative path resolves differently on the cluster. A closure embeds a 4-GiB object in every task. A mutable lookup changes between graph creation and action. A debugging `collect` brings millions of records into the driver and kills it.

Planning itself consumes resources. Building millions of nodes, serializing large closures, contacting catalogs, collecting statistics, optimizing expressions, generating code, and shipping a plan can dominate a small computation. Observability must separate construction, analysis, optimization, submission, queueing, and execution rather than labeling all pre-task delay as scheduler latency.

The distinction also matters for governance. A logical plan may name sensitive tables and purposes before any worker reads data. Policy can reject illegal flows early, but only if identities and intended sinks are represented. Deferred binding that silently resolves a newer table, function, or policy version can invalidate prior review.

## Prerequisites and Retrieval

Recall immutable data and partition identity from [LSDS-003](003-range-hash-and-consistent-partitioning.md), task graphs and stages from [LSDS-005](005-distributed-task-graphs.md) through [LSDS-007](007-narrow-and-wide-transformations.md), serialization and closure movement from [LSDS-008](008-serialization-across-workers.md), and work/movement/state accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

Retrieve MapReduce execution and action-like submission from [LSDS-021](021-mapreduce-execution-model.md), operator placement from [LSDS-022](022-map-side-and-reduce-side-processing.md), aggregation and partition compatibility from [LSDS-023](023-partitioners-and-combiners.md), and logical/physical/runtime DAG distinctions from [LSDS-024](024-directed-acyclic-graph-execution.md).

You should understand pure functions, side effects, lexical closures, immutable values, schemas and types, hashes, graph dependency closure, query operators, partitions, caches, retries, and versioned data snapshots.

## Learning Objectives

After this module, you should be able to:

1. distinguish a lazy handle from its future distributed value;
2. identify construction, analysis, optimization, physical planning, submission, and execution boundaries;
3. classify transformations, actions, materializations, and metadata-triggering operations in a concrete API;
4. define temporal semantics for paths, tables, configuration, functions, closures, clocks, randomness, and credentials;
5. explain why laziness enables pruning, pushdown, fusion, and joint-result sharing;
6. predict when repeated actions recompute work and when persistence or joint submission can reuse it;
7. construct canonical plan identities without conflating presentation text with complete replay identity;
8. validate optimizer rewrites using reference semantics and adversarial inputs;
9. bound driver results, plan size, captured state, catalog work, and optimization overhead; and
10. preserve explainability, security, governance, and reproducibility from construction through committed output.

## Core Exposition

A lazy handle is best understood as an immutable reference to a node plus its owning planning context. It may expose schema or partition metadata, but it does not generally hold all records. Printing the handle may show a plan. Iterating, collecting, counting, writing, or explicitly running it may trigger analysis and execution depending on the API.

### Construction is graph mutation, not data mutation

Calling `filter`, `map`, `select`, or `join` typically adds a logical node whose inputs are existing handles and returns a new handle. The prior handle remains valid and unchanged. This functional shape makes branches explicit: one source can feed several derived plans.

Construction can still execute driver code. Arguments are evaluated eagerly by the host language; builders may validate syntax; user code may compute a filename; and registration may contact a service. "Lazy" applies to specified data operations, not every line around them. Library documentation and tests must identify the boundary.

Avoid external effects during construction. A builder that creates tables, sends messages, or reads mutable remote state becomes hard to retry and difficult to distinguish from the eventual action. If discovery is required, represent its resolved snapshot in the plan or make the boundary explicit.

### Transformation, metadata request, action, and sink

A transformation returns another distributed handle. An action requests an observable result such as a count, a local sample, or a write. Some APIs distinguish terminal sink construction from a later whole-pipeline `run`; others make the write call itself an action. Metadata access such as `schema`, `columns`, or `explain` may trigger analysis or a remote request without scanning all data.

Therefore, do not memorize universal method categories. For the exact engine/version, document whether each operation performs local validation, remote analysis, source enumeration, job submission, result collection, or publication. A method can change classification between client modes.

### Planning pipeline

A useful conceptual pipeline is:

1. **parse/build** unresolved expressions and graph nodes;
2. **analyze** names, types, schemas, functions, catalogs, policy, and compatibility;
3. **normalize** equivalent representations into a canonical form;
4. **optimize logically** through projection/filter pushdown, constant folding, simplification, and safe reuse;
5. **select physical operators** such as broadcast/hash/sort joins, exchanges, aggregation strategies, and file scans;
6. **prepare runtime graph** with stages, partitions, resources, code artifacts, and attempt/commit contracts; and
7. **execute and adapt** within guarded semantics, recording runtime decisions.

Engines combine or reorder these phases. The model is for asking precise questions, not imposing internal class names. An explanation must label the phase it represents.

### Analysis timing and deferred errors

An unresolved column name can be rejected during transformation construction, when schema is requested, when the action is analyzed, or by a worker. Earlier errors shorten feedback and keep failures near the cause. Deferred analysis reduces client coupling and supports remote planning, but pushes failures later and makes session/catalog state part of execution.

Test timing rather than assuming it. Pin the relevant client/server mode, catalog snapshot, current database, search path, locale, case-sensitivity, function registry, and policy version. A plan that refers to `sales` by name is incomplete if `sales` can resolve differently later.

### Temporal capture semantics

Laziness asks: "later, using what?" A source path can mean files present at construction, at action submission, or during worker listing. A table identifier can mean a versioned snapshot or whatever is current. A closure can serialize the value held when the task is packaged, or consult external mutable state each call.

Prefer immutable explicit parameters: snapshot IDs, absolute governed URIs, schema versions, timezone, locale, seed, clock policy, model digest, side-input digest, and configuration. For intentionally dynamic inputs, record the resolution event and result in run metadata. "Latest" is a policy, not a reproducible identifier.

Host-language closures deserve special care. Capturing an object can serialize its entire reachable graph, include credentials, or fail on the cluster. Capturing a mutable variable and changing it before action may produce client-mode-specific behavior. Broadcast or side-input mechanisms express bounded shared data more clearly and expose lifecycle and authorization.

### Selected sinks and dependency pruning

An action identifies one or more desired sinks. The planner walks backward to compute their transitive dependencies. Unselected branches may be pruned if they have no required effects. This is why side effects hidden inside transformations are unsafe: an optimizer can remove, duplicate, reorder, or retry them.

Multi-output transforms and audit/error branches require explicit sink semantics. If error quarantine is mandatory even when the main result alone is requested, make it part of the declared effect contract rather than relying on incidental traversal.

### Repeated actions and joint submission

Lazy lineage is not a cache. If `count(x)` and `write(x)` are separate actions, the engine may evaluate `x` twice. Persistence can retain partitions between actions, but only after materialization, and eviction or worker loss can cause recomputation. A joint multi-result submission can share common ancestors within one graph without promising reuse across later jobs.

Choose among recomputation, joint action, cache, and durable materialization using ancestor cost, result size, fan-out, action timing, memory pressure, failure probability, determinism, and governance. Verify from runtime metrics; source-read counters are often more revealing than the surface plan.

### Common-subplan identity

Two nodes are reusable only if their full semantics match. Textually equal expressions can differ by input snapshot, schema, timezone, locale, floating policy, function implementation, random seed, current user, row-level security, purpose, or allowed destination. Conversely, syntactically different expressions may normalize to the same result.

A canonical plan key should encode operator kind, canonical parameters, ordered input keys, schema/type policy, relevant configuration, function/code identities, input snapshots, and security/purpose context. Secrets should be represented by safe version identifiers, not copied into digests or logs.

Hash equality is not a proof of semantic equality unless the canonical representation is complete and collision handling is defined. Use digests for identity and comparison, supported by full metadata and tests.

### Rewrite rules and observability

Projection pruning removes unused fields. Predicate pushdown moves filters toward capable sources. Constant folding evaluates deterministic constants. Operator fusion combines compatible adjacent transforms. Join reordering changes association/order under valid relational conditions. Partial aggregation reduces exchanged state under merge laws.

Each rule has guards. A filter involving nondeterminism, exceptions, user-visible order, an outer join, or access-control side channel may not move freely. Floating-point and approximate operations can be sensitive to reassociation. A user-defined function may be opaque or effectful. The optimizer must either know the law or decline the rewrite.

Expose rule names, before/after plan identities, estimates, reasons for rejection, and adaptive decisions. Avoid logging literal sensitive predicates or sampled values. Plan explainability should work at logical, optimized, physical, and observed runtime levels.

### Plan size and construction cost

Programmatic loops can create millions of tiny nodes. Large literal lists and captured objects inflate plan serialization. Deep expression trees stress analyzers and code generators. Repeated catalog calls, statistics lookup, and optimizer fixpoint iterations add latency before any task starts.

Measure node/edge count, expression depth, serialized plan bytes, closure bytes, construction CPU/memory, analysis RPCs, catalog time, optimization iterations/time, generated code size, and submission payload. Use higher-level operators, parameter tables, batched expressions, and stable reusable definitions where semantics permit.

### Actions and driver safety

Distributed results should normally remain distributed or be written to governed storage. `collect`, conversion to a local table, or an unconstrained iterator can exceed driver memory, message size, or timeout. Even `take` and `show` may scan substantial input depending on ordering and filters.

Before a local-result action, bound row count and serialized bytes, define truncation/order, handle backpressure, and avoid printing sensitive values. Driver memory is shared with planning, status, and result decoding; an estimate must leave headroom.

### Caching, persistence, and checkpoints

Calling `cache` often marks a lazy plan for persistence; it may not execute immediately. The first action materializes partitions as they are computed. Later actions can reuse retained partitions, while missing partitions are recomputed from lineage. A durable checkpoint has different availability, integrity, and retention semantics.

Cache keys must include semantic identity and tenant/policy boundaries. Metrics must show hit/miss, materialized partitions, bytes, eviction, recomputation, and stale prevention. Unpersisting is a lifecycle action with asynchronous or engine-specific behavior; do not treat memory release as instantaneous without evidence.

### Nondeterminism and effects

Clocks, random numbers, unordered input, process-local hashes, external API calls, and mutable tables can make separate actions differ. Decide whether nondeterminism is intended. For reproducibility, inject a seed and stable per-record derivation, pin snapshots, define ordering/ties, and isolate effects in commit-aware sinks.

An optimizer may evaluate a deterministic constant once, but must not collapse an intended per-record random operation. Conversely, labeling an effectful function as pure can cause duplication or elimination. Function metadata is a correctness contract.

### Testing and replay

Test construction without data reads, action-trigger behavior, early/deferred errors, closure serialization, selected-sink pruning, repeated/joint actions, cache loss, plan canonicalization, rewrite equivalence, resource bounds, and side-effect isolation. Use source counters and instrumented fakes to locate boundaries.

For replay, preserve unresolved and analyzed plans when useful, optimized/physical plan digests, rule decisions, code/dependency artifacts, input snapshots, schema/catalog/function/policy versions, configuration, seeds/clocks, resource plan, attempts, and output manifests. Reanalysis under a newer catalog is a new run, not a faithful replay, unless equivalence is established.

### Security, governance, and human impact

Plans reveal intended data flow before execution and are ideal for early policy enforcement. Validate source/sink purpose, tenant, region, sensitivity, minimization, retention, and allowed joins. Repeat enforcement at runtime because the planner and workers can differ in identity or topology.

Captured closures and plan literals can leak secrets or personal data into submission payloads, caches, histories, and explain output. Scan and redact safely; reference managed secret identities rather than values. When decisions affect people, preserve subgroup/error branches, quality evidence, timeliness, accessibility, correction/appeal paths, and named affected-party/domain oversight.

## Definitions and Notation

- `H`: lazy handle identifying a logical node and owning planning context.
- `L_u`: unresolved logical plan; `L_a`: analyzed/bound logical plan; `L_o`: optimized logical plan.
- `P`: physical plan; `R`: observed runtime graph and attempts.
- `deps(s)`: transitive dependency closure required by selected sink set `s`.
- `t_c`: construction time; `t_a`: analysis/submission time; `t_e`: worker execution time.
- **transformation**: plan-building operation returning a distributed handle.
- **action**: demand for an observable result/effect that triggers planning or execution.
- **metadata trigger**: operation that may analyze/resolve without scanning full data.
- **closure**: function plus captured lexical environment prepared for later use.
- **canonical plan**: normalized representation with an explicit identity schema.
- `digest(plan)`: cryptographic digest of that canonical representation, not of omitted external state.
- **joint action**: one submission selecting multiple results so shared dependencies may execute once.
- **persistence hint**: request to retain materialized partitions; it is not itself proof of execution or durability.

## Mechanisms, Invariants, or Proof Structure

Audit a lazy plan with this sequence:

1. Classify each API operation as construction, local validation, remote analysis, metadata access, action, materialization request, or publication.
2. Enumerate nodes, edges, owning session, selected sinks, mandatory audit/error sinks, and dependency closure.
3. Define when every source, table, schema, function, configuration, closure, clock, seed, credential, and policy is resolved.
4. Bind identifiers/types/authorization and record the analyzed plan plus resolution evidence.
5. Canonicalize using a versioned identity schema and calculate a plan digest without exposing secrets.
6. Apply each rewrite only under explicit semantic guards; compare values, errors, ordering, nondeterminism, and effects.
7. Select physical algorithms, exchanges, partitions, caches, resources, and task/commit semantics.
8. Bound plan/closure size, planning cost, source enumeration, driver results, intermediate state, and action fan-out.
9. Test separate actions, joint actions, persistence, eviction/loss, retry, adaptive changes, cancellation, and partial failure.
10. Preserve all identities and observed plan decisions through committed output, replay, retention, and deletion.

The semantic argument is observational: for every allowed input and environment snapshot, the optimized execution must produce the same declared values, ordering, errors, and effects as the reference plan, except for explicitly permitted approximation or nondeterminism. Pure relational equivalence is insufficient if exceptions, policy, or effects are observable.

The reuse argument is conjunctive. Common subplans must match across operator/parameters, ordered inputs, code, schema, configuration, snapshot, nondeterminism, identity/purpose, and output contract. A mismatch in any relevant component forbids reuse or requires a proved compatibility rule.

<!-- bijux-verify: {"id":"lazy-plan-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"plan=sum(map_square(filter_even(source[numbers])))\ndigest=c9f2d8b57e3f\nreads_before=0\nfirst_total=20 reads_after=1\nsecond_total=20 reads_after=2\njoint=(20, 2) reads_after=3\n","stderr":""}} -->
```python
from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class Node:
    op: str
    inputs: tuple = ()
    payload: tuple = ()


reads = 0


def explain(node):
    if node.op == "source":
        return f"source[{node.payload[0]}]"
    return f"{node.op}({','.join(explain(item) for item in node.inputs)})"


def evaluate(node, memo):
    global reads
    if node in memo:
        return memo[node]
    values = tuple(evaluate(item, memo) for item in node.inputs)
    if node.op == "source":
        reads += 1
        result = node.payload[1]
    elif node.op == "filter_even":
        result = tuple(value for value in values[0] if value % 2 == 0)
    elif node.op == "map_square":
        result = tuple(value * value for value in values[0])
    elif node.op == "sum":
        result = sum(values[0])
    elif node.op == "count":
        result = len(values[0])
    else:
        raise ValueError(node.op)
    memo[node] = result
    return result


def run(node):
    return evaluate(node, {})


def run_many(nodes):
    memo = {}
    return tuple(evaluate(node, memo) for node in nodes)


numbers = Node("source", payload=("numbers", (1, 2, 3, 4)))
evens = Node("filter_even", (numbers,))
squares = Node("map_square", (evens,))
total = Node("sum", (squares,))
even_count = Node("count", (evens,))
plan = explain(total)

print(f"plan={plan}")
print(f"digest={sha256(plan.encode()).hexdigest()[:12]}")
print(f"reads_before={reads}")
print(f"first_total={run(total)} reads_after={reads}")
print(f"second_total={run(total)} reads_after={reads}")
print(f"joint={run_many((total, even_count))} reads_after={reads}")
```

The evaluator deliberately uses a fresh memo for each independent action and one memo for a joint action. A production plan digest must include far more than this display string, including source snapshots, schemas, code, configuration, and policy context.

## Alternatives and Trade-Offs

**Eager versus lazy data execution.** Eager execution produces immediate feedback and intuitive effects. Lazy execution exposes the whole graph for optimization and avoids unused work, but delays failures and makes temporal capture explicit.

**Eager versus deferred analysis.** Eager schema/name resolution catches mistakes near construction and can power tooling. Deferred analysis supports thin clients, remote catalogs, and unresolved portable plans. It also makes session/catalog state at action time consequential.

**Opaque closures versus declarative expressions.** Closures are expressive and fit host-language code. Declarative expressions are easier to inspect, type, optimize, serialize, govern, and translate. Use closures when needed, with explicit code and capture identity.

**Separate versus joint actions.** Separate actions are simple and independently retryable but can repeat ancestors. Joint submission exposes common work and coordinated planning but couples lifetimes, failures, and resource peaks.

**Recompute versus persist.** Recompute avoids retained state and stale caches. Persistence helps repeated expensive deterministic ancestors but consumes capacity, expands access lifetime, and still needs loss/recompute semantics.

**Client-side versus server-side planning.** Client planning gives immediate local explanations and reduces server work. Server planning sees authoritative catalogs, policies, statistics, and runtime capabilities. Split planning requires protocol/version compatibility and records of both forms.

**Stable static plan versus adaptive execution.** Static plans are easier to compare and replay. Adaptive execution can use observed cardinality and skew, but needs legal rewrite guards, decision logs, and an observed-plan identity.

**Automatic common-subplan reuse versus explicit materialization.** Automatic reuse reduces boilerplate and I/O when identity is sound. Explicit materialization creates a visible ownership and recovery boundary but adds storage, cleanup, and publication cost.

## Failure Modes and Misconceptions

**"The transformation already ran because no error appeared."** A returned handle usually records intent. Data-dependent errors can remain latent until analysis or action.

**"Lazy means no work happens on the driver."** Host-language arguments, validation, graph construction, serialization, catalog calls, and optimization all consume driver/client resources.

**"All errors are lazy."** Syntax, local types, and sometimes schema analysis can fail eagerly; other client modes defer the same validation.

**"The handle is a collection in memory."** It denotes distributed lineage. Converting it to a local object may trigger an action and exceed driver capacity.

**"Calling cache computes and permanently stores everything."** It commonly marks persistence; materialization happens during an action, partitions can be partial, and caches can evict or disappear.

**"Two actions share work automatically."** They may be separate jobs and recompute every ancestor unless jointly submitted or backed by retained/durable materialization.

**"The closure sees whatever the driver variable contains during worker execution."** Capture/serialization timing is engine-specific; mutable state and client modes make this assumption unsafe.

**"A plan string is a replay record."** It may omit snapshots, code, configuration, functions, policies, secrets, adaptive decisions, and physical details.

**"Equivalent SQL text means safe cache reuse."** Search path, catalog version, user policy, timezone, functions, and input snapshots can differ.

**"Optimizer rewrites only affect performance."** They can change errors, order, nondeterminism, floating results, effects, and data placement unless guarded.

**"Explain is the executed plan."** Explain may show one planning phase; adaptive runtime choices and failed/retried attempts require observed evidence.

**"Hidden side effects in map run once."** Branch pruning, retries, speculation, fusion, and recomputation can omit or repeat them.

## Worked Examples

### Example 1

`filtered = records.filter(valid)` returns immediately, but a source-read counter remains zero. `filtered.count()` resolves the plan and scans partitions. A test that asserts no source access during construction distinguishes lazy data execution from eager driver argument evaluation.

### Example 2

A client constructs `select("missing")`. One engine mode has the schema locally and rejects it now; a remote mode stores an unresolved attribute and rejects it when `schema` or an action triggers server analysis. Both can be lazy about data execution. Error timing belongs in the API contract and tests.

### Example 3

A plan captures `threshold=10`, then driver code changes it to 20 before the action. Depending on closure capture and serialization timing, workers may use 10 or 20. Pass an immutable parameter into the node and include it in plan identity; do not infer behavior from local lexical intuition.

### Example 4

A source refers to `/events/current`. At construction it points to snapshot A; before action an operator advances it to B. If the contract resolves at action, B is correct but the run must record B. If review approved A, use A's immutable identifier. A mutable alias cannot serve as replay identity.

### Example 5

The program derives `clean`, then calls `clean.count()` and `clean.write(path)` separately. Runtime counters show two scans. Joint submission could share the ancestor in one graph; persistence could reuse partitions across actions; durable materialization could decouple publication. Compare memory, failures, time separation, and governance.

### Example 6

An unused debug branch maps records through a costly parser but has no selected sink. Dependency pruning removes it. If the parser also wrote audit rows through a hidden effect, audit silently disappears. Required audit output must be an explicit sink or part of a transactional data contract.

### Example 7

Predicate pushdown changes `read all -> UDF -> filter` into a source predicate. It is safe only if the source implements the same null, type, locale, and error semantics and moving the filter does not bypass required validation or policy logging. Compare adversarial values and observable errors to a reference plan.

### Example 8

A closure captures a large machine-learning model and a credential-bearing client object. Plan serialization becomes gigabytes and leaks secrets. Store the model as a versioned authorized artifact/side input and acquire scoped runtime credentials through the platform; include safe version IDs in plan metadata.

### Example 9

An analyst calls `collect()` after a filter expected to return 1,000 rows. Data drift returns 50 million variable-width rows, exhausting the driver. Use a distributed write or enforce a bounded limit with explicit deterministic ordering, row/byte guards, truncation semantics, and sensitive-output controls.

### Example 10

Two benefit-eligibility plans look identical but run for users under different row-level policies and purposes. A cache keyed only by expression text can expose one population to the other. Reuse identity includes tenant, policy and purpose context; named privacy/domain review verifies minimization, appeal, correction, and deletion.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) connects laziness to evaluation order, effects, purity, types, and observational equivalence.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies futures, dependency scheduling, races, and deferred work.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies graph closure, canonicalization, hashing, and optimization complexity.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects unresolved/analyzed/optimized/physical plans to catalogs, relational algebra, cost models, and transactions.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) applies lazy plans to pipeline composition, materialization, quality, lineage, and publication.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies snapshots, retries, nondeterminism, partial failure, and commit.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies closure/plan secret handling, authorization context, purpose binding, and audit.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) connects driver and worker memory, processes, scheduling, and resource limits.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) explains plan RPCs, artifact distribution, source access, and collection transport.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects submission, plan services, caches, identities, policy admission, and observability.

## References

1. Apache Spark. [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html). Accessed 2026-09-03.
2. Apache Spark. [Eager vs Lazy: Spark Connect vs Spark Classic](https://spark.apache.org/docs/latest/spark-connect-gotchas.html). Accessed 2026-09-03.
3. Apache Spark. [SQL Performance Tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html). Accessed 2026-09-03.
4. Dask. [Dask Delayed](https://docs.dask.org/en/stable/delayed.html). Accessed 2026-09-03.
5. Dask. [User Interfaces: Laziness and Computing](https://docs.dask.org/en/stable/user-interfaces.html). Accessed 2026-09-03.
6. Dask. [Stages of Computation](https://docs.dask.org/en/stable/phases-of-computation.html). Accessed 2026-09-03.
7. Dask. [High Level Graphs](https://docs.dask.org/en/stable/high-level-graphs.html). Accessed 2026-09-03.
8. Apache Beam. [Basics of the Beam Model](https://beam.apache.org/documentation/basics/). Accessed 2026-09-03.
9. Apache Beam. [Create Your Pipeline](https://beam.apache.org/documentation/pipelines/create-your-pipeline/). Accessed 2026-09-03.
10. Apache Beam. [Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/). Accessed 2026-09-03.
11. Apache Calcite. [Algebra](https://calcite.apache.org/docs/algebra.html). Accessed 2026-09-03.
12. DuckDB. [EXPLAIN: Inspect Query Plans](https://duckdb.org/docs/stable/guides/meta/explain.html). Accessed 2026-09-03.

## Exercises

### Exercise 1

Run the compact lazy evaluator by hand. Explain source-read counts for construction, two independent actions, and the joint action, and state what the digest omits.

### Exercise 2

Specify temporal capture semantics for a plan using a table alias, local closure, random sample, current time, registered function, and secret-backed external service.

### Exercise 3

Prove or refute reuse of two visually identical aggregate subplans submitted by different users, sessions, snapshots, and timezones.

### Exercise 4

Design tests and observability for a filter/projection/join rewrite and a 10-million-node planning incident.

### Exercise 5

Specify named review and evidence for a lazy eligibility or clinical-risk plan that performs adaptive optimization and local result collection.

## Answers to the Exercises

### Answer 1

Construction creates immutable nodes and calls no evaluator, so reads remain zero. Each `run(total)` creates a fresh memo and reaches the source once, producing 20 and advancing reads to one then two. `run_many` uses one memo for total and count; both share `evens` and the source, so the pair is `(20,2)` and reads advances only to three. The twelve-character demo digest covers only a display string. A production identity also needs canonicalization version, operator parameters, ordered inputs, source snapshots, schemas, function/code/dependencies, configuration, timezone/locale/numeric policy, seed/clock, user/purpose/policy context, and collision handling.

### Answer 2

Resolve the table alias to an immutable snapshot during analysis and record alias plus snapshot. Serialize an explicit immutable closure parameter and code digest at submission, rejecting unsupported reachable state. Derive sampling randomness from a pinned seed and stable record identity. Replace wall-clock reads with an injected logical timestamp and timezone. Bind the registered function to implementation/version plus type semantics. Represent the service by endpoint/API/schema version and managed credential identity, acquiring a scoped secret at task start without storing its value in the plan; capture response snapshots or declare nondeterminism and idempotency/replay limits.

### Answer 3

Visual equality is insufficient. Reuse is valid only if canonical operators/parameters, ordered input snapshots, schemas, functions, configuration including timezone, numeric/null semantics, nondeterminism, user row-level policy, tenant, purpose, and output contract match or a reviewed compatibility rule proves irrelevance. Different snapshots directly change input. Different timezones can change date grouping. Different users/policies can change visible rows and make cross-user reuse a disclosure. Therefore the proposed facts refute unconditional reuse; compare complete semantic identities and isolate caches by policy domain.

### Answer 4

For the rewrite, store before/after logical plans and rule/guard, evaluate a reference on empty, singleton, duplicate, null, malformed, outer-join, timezone/locale, exception, and skew cases, and compare values, ordering and errors. Measure source columns/rows/bytes, UDF calls, exchange, memory, spill, and duration. For the planning incident, capture node/edge count, expression depth, closure/literal bytes, construction CPU/memory, plan serialization bytes/time, catalog RPCs/time, optimizer rules/iterations/time, generated code, and submission size. Reproduce with a minimized builder, then batch expressions or use higher-level nodes while comparing canonical semantics and planning/resource bounds.

### Answer 5

Pin unresolved/analyzed/optimized/physical and observed plan identities, legal adaptive rules, code/dependencies, function/catalog/policy versions, data snapshots, schemas, purpose, jurisdiction, seed/clock, statistics, resources, identity, and sink/result limits. Test subgroup, missing, null, extreme, late, appeal/correction, snapshot drift, policy drift, cache isolation, retry, adaptive branches, and bounded collection; compare to an independently specified reference and report error/fairness/coverage by affected group. Named review includes clinical or eligibility domain owners, data stewards, privacy/legal/records/jurisdiction specialists, affected communities or ethics oversight, fairness/statistics experts, security/identity, platform/runtime, accessibility, incident recovery, and independent assurance. Optimization or convenience cannot waive consent/purpose, minimization, explanation, correction, appeal, retention, deletion, or driver-disclosure controls.
