---
module_id: DBE-058
program: Database Engineering
level: 2
module_number: 58
title: Iterator and Volcano Execution
status: complete
last_verified: 2026-08-30
---

# Iterator and Volcano Execution

## One-Page Review

### Governing question

How can a database execute an arbitrary physical-plan tree through a small, composable operator interface while preserving row semantics, lifecycle safety, early termination, resource ownership, and observable failure behavior?

### Essential definitions

An **iterator operator** exposes lifecycle operations conceptually equivalent to `open`, `next`, and `close`. **Pull execution** means a parent requests the next result from its children on demand. **Volcano-style execution** combines a uniform iterator interface with parameterized operators, support functions, and exchange mechanisms that separate data processing from parallelism. A **pipeline** is a connected region in which records can flow without complete intermediate materialization. A **pipeline breaker** must consume or retain a substantial input boundary before producing ordinary output. **Operator state** is execution-local mutable state such as cursors, hash tables, buffers, counters, or child positions. **End of stream** is a control result distinct from a SQL row containing NULLs. **Rescan** restarts an operator under a declared parameter/snapshot contract. **Backpressure** is a mechanism by which downstream demand limits upstream production.

### Central model, mechanism, or theorem

For a plan tree, initialize every node with immutable plan configuration plus execution-local state. A call to the root's `next` recursively requests only the child work needed for one root result or end-of-stream. If every operator implements its local relational semantics, preserves multiplicity, respects its input/output schema, and obeys lifecycle and cancellation contracts, structural composition implements the physical plan. Streaming operators can pass records with bounded state; blocking operators such as full sort consume their input on first demand and then serve stored results. A parent that stops early must close the entire reachable subtree even if no child has reached end-of-stream.

### Critical invariants

- Each execution has distinct operator state; an immutable plan may be shared only where the engine contract permits.
- `open` establishes resources before `next`; `next` returns one legal record or an unambiguous end marker; `close` is idempotent and releases owned resources.
- Every emitted occurrence is derived from eligible input occurrences exactly as the operator's physical semantics require.
- Parent and child agree on schema, representation, ownership, parameter values, snapshot, and end/error protocol.
- A streaming operator retains only bounded incremental state; a blocking or stateful operator declares and governs its materialization.
- Early termination, error, timeout, and cancellation propagate and close all initialized descendants.
- Rescan either reconstructs valid state under the same contract or is explicitly unsupported/materialized.
- Instrumentation observes execution without changing row identity, evaluation count, error timing, or resource cleanup.

### Common failures

Failures include confusing SQL NULL with end-of-stream; reusing mutable state across executions; calling `next` before successful initialization; losing or duplicating rows in a filtering loop; evaluating volatile expressions more than specified; retaining borrowed child storage after advance; assuming every iterator is streaming; forgetting that sort's first `next` drains its child; failing to close after `LIMIT`; rescanning a nonrewindable child; swallowing child errors as exhaustion; measuring only root rows; performing cancellation checks too rarely; leaking temporary state; and treating tuple-at-a-time dispatch as universally efficient on modern CPUs.

### Compact example

The executable composes scan, filter, blocking sort, projection, and limit. The first root demand causes sort to consume five rows, retain three qualifying rows, and then return the highest score. `LIMIT 2` stops with one sorted row still buffered, yet close propagates through every node. Exact counters demonstrate that demand-driven control does not imply every child stops early across a blocking boundary.

### Connections

Retrieve [Logical and Physical Plans](051-logical-and-physical-plans.md), [Nested-Loop Joins](053-nested-loop-joins.md), and [External Sorting and Spilling](057-external-sorting-and-spilling.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to vectorized execution, pipeline profiling, optimization, parallel query, and distributed execution.

## Governing Question

What local interface, state, ownership, and control-flow contracts let independently implemented physical operators compose into a correct demand-driven query executor, and where does that abstraction expose or hide real CPU, memory, I/O, and cancellation costs?

## Why This Matters

A physical plan is useful only if an executor can run it. Hard-coding one procedure for every possible plan shape would make the engine unmaintainable. A uniform iterator interface lets scans, filters, projections, joins, aggregates, sorts, limits, and extensions form trees without each operator knowing the full query. The parent asks for a record; the child supplies one or reports exhaustion. This simple protocol localizes algorithm state and makes new physical alternatives composable.

The abstraction also shapes performance and failures. A filter can skip many child records inside one parent call. A nested-loop join can rescan its inner child repeatedly. A sort appears as one node but drains its entire input on first demand and may spill. A limit can stop a streaming scan after a few rows, yet it cannot undo work already performed by a blocking descendant. One slow root call may therefore represent millions of child calls, allocation, I/O, expression evaluation, and cancellation opportunities.

Tuple-at-a-time virtual dispatch was designed when storage costs often dominated. On modern processors, per-record calls, unpredictable branches, indirect function dispatch, poor instruction/data locality, and representation conversion can dominate analytical workloads. Vectorized engines amortize control over batches; push/data-centric compilation fuses loops across operators. These approaches change the control surface but retain the semantic obligations: correct multiplicity, expression behavior, ownership, blocking boundaries, resource governance, errors, and cancellation.

“Volcano” is sometimes used loosely as a synonym for any pull iterator. Graefe's Volcano system was broader: it emphasized extensible operators and support functions, separation of mechanism and policy, parallelism through exchange, dynamic plans, and resource allocation. This module uses *iterator* for the `open/next/close` protocol and *Volcano-style* for the family of composable demand-driven operator designs, while keeping historical product claims precise.

## Prerequisites and Retrieval

You should understand relational bags, logical and physical plans, schemas and tuple representations, predicates and expression evaluation, scans, nested-loop/hash/merge joins, aggregation, sorting/spill, transactions and snapshots, exceptions, resource ownership, cancellation, and basic CPU locality.

Retrieve: plan node, execution state, iterator, cursor, `open`, `next`, end-of-stream, `close`, rescan, mark/restore, demand pull, pipeline, pipeline breaker, materialization, support function, exchange, backpressure, tuple slot, borrowed/owned lifetime, selection, projection, volatile expression, cancellation point, inclusive/exclusive timing, row counter, batch, vector, push execution, and query compilation.

DBE-051 separated logical from physical plans. DBE-052 through DBE-057 supplied representative scan, join, aggregation, and sort operators. This module unifies their control interface. DBE-059 compares vectorized and pipeline-oriented execution, and DBE-060 develops measurement across the resulting operator graph.

## Learning Objectives

After this module, you can:

1. specify lifecycle, end-of-stream, error, schema, and ownership contracts for an iterator operator;
2. trace pull control through scan, filter, projection, limit, join, aggregation, and sort;
3. prove local operator correctness composes over a physical-plan tree under explicit assumptions;
4. distinguish streaming, bounded-state, blocking, and rewind/materialization behavior;
5. implement a finite pull executor and verify rows, counters, early stop, and closure;
6. reason about parameterized rescans, volatile expressions, snapshots, and borrowed tuple lifetimes;
7. design cancellation, exception unwinding, memory/spill ownership, and cleanup;
8. attribute inclusive/exclusive work and avoid misleading per-node metrics;
9. compare row iterators with batch/vector, push, compiled, and exchange-based execution; and
10. design conformance, metamorphic, fault-injection, resource, and performance tests for an extensible executor.

## Core Exposition

**Separate immutable plan from mutable execution.** A plan node records operator kind, child relationships, expressions, physical properties, and estimates. Execution state holds cursors, current rows, hash/sort structures, memory contexts, parameters, snapshot handles, instrumentation, and lifecycle status. Reusing one mutable state object across sessions or rescans invites races and stale results. An engine may cache or share an immutable prepared plan while instantiating state per execution, subject to schema/catalog invalidation rules.

**Define the interface precisely.** Conceptual `open` validates configuration, initializes local state, and opens children in a documented order. `next` returns one output occurrence or an end marker; errors travel through a separate error path. `close` releases local resources and closes initialized children even after partial open, error, or early stop. Implementations may combine initialization with first execution, use function pointers, coroutines, bytecode, or language iterators, but the observable lifecycle contract remains.

End-of-stream cannot be represented by an ordinary nullable column. A SQL row `(NULL)` is data. Use a tagged result, a slot with an explicit empty flag, an option type, status plus out parameter, or a protocol-specific sentinel that cannot be a legal row. Likewise, do not convert an exception, timeout, or cancellation into exhaustion: partial results and a successful end have different transaction and client meaning.

**Pull composes recursively.** A projection requests a child record, evaluates output expressions once under the expression contract, and returns a new or safely referenced record. A filter loops: request a child record; if exhausted, return exhaustion; evaluate the predicate; return the record only if SQL truth semantics accept it; otherwise continue. A limit forwards at most N qualifying child occurrences and can then return exhaustion without another child call.

A nested-loop join stores one current outer occurrence, opens or rescans the inner for that occurrence, and emits every qualifying pair before advancing the outer. A merge join coordinates two ordered cursors and duplicate bands. A hash join builds before probing. An aggregate may stream ordered groups or consume all groups. Uniform `next` signatures do not make algorithms equally lazy, memory-bounded, rewindable, or cancellable.

**Classify state and blocking boundaries.** A scan, filter, projection, or limit can usually stream with bounded per-record state. Merge join streams but may retain duplicate bands or require mark/restore. Nested loop can stream outputs while repeatedly rescanning/materializing its inner. Hash join blocks on build input before probe output. Full sort consumes all input before its first ordinary result. Hash aggregate can consume all input; ordered aggregate can finalize group by group. Window functions vary by frame and partition requirements.

The relevant question is not merely “blocking or not.” Ask: which input side, key group, partition, or frame must be complete; how much state can grow; whether spill is supported; whether output can begin; whether the operator can stop its child; and what rewind/random-access contract the parent needs. These properties influence plan enumeration and memory admission.

**Make record ownership explicit.** A child may reuse a tuple slot or vector buffer on its next call. A parent that needs the record later must copy/materialize the required fields or pin ownership according to the engine protocol. Storing a borrowed pointer in a hash table or duplicate band after advancing the child can silently replace earlier values. Projection can sometimes produce virtual references without copying, but their lifetime must extend through the consumer's use.

**Expressions are part of semantics.** Predicates observe SQL three-valued logic, collation, types, and errors. Volatile or effectful functions constrain reordering and duplicate evaluation. A filter loop must not reevaluate an expression because instrumentation, a retry, or a representation conversion requested the row again. Projection pruning is safe only for values whose evaluation is not semantically required. The physical executor follows contracts established by binding and optimization; it cannot assume every expression is pure.

**The executable exposes demand and a blocking boundary.** The finite plan is `Limit(Project(Sort(Filter(Scan))))`. Opening recursively records child-first initialization. On the first request, sort drains filter: five source rows are examined, three pass, and the source receives one additional call to observe end-of-stream. Sort orders by descending score. Limit consumes two results and then reports its own end without asking sort for the third buffered row. Closure records parent-first cleanup and reaches every node.

<!-- bijux-verify: {"id":"pull-iterator-lifecycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"result=((4, 90), (5, 80))\nscan_rows_examined=5\nscan_next_calls=6\nfilter_next_calls=4\nfilter_rows_passed=3\nsort_input_rows=3\nsort_next_calls=2\nproject_next_calls=2\nlimit_next_calls=3\nlimit_child_stopped_early=True\nopened=scan,filter,sort,project,limit\nclosed=limit,project,sort,filter,scan\nevidence=pull_lifecycle_and_blocking_boundary\n","stderr":""}} -->
```python
EOS = object()


def node(kind, name, child=None, **state):
    value = {
        "kind": kind,
        "name": name,
        "child": child,
        "started": False,
        "stopped": False,
        "next_calls": 0,
    }
    value.update(state)
    return value


def start(current, events):
    if current["started"]:
        raise RuntimeError("double start")
    if current["child"] is not None:
        start(current["child"], events)
    current["started"] = True
    events.append(f"open:{current['name']}")


def pull(current):
    if not current["started"] or current["stopped"]:
        raise RuntimeError("pull outside live lifecycle")
    current["next_calls"] += 1
    kind = current["kind"]
    if kind == "scan":
        if current["position"] == len(current["rows"]):
            return EOS
        row = current["rows"][current["position"]]
        current["position"] += 1
        return row
    if kind == "filter":
        while True:
            row = pull(current["child"])
            if row is EOS:
                return EOS
            if row[1] >= current["minimum"]:
                current["passed"] += 1
                return row
    if kind == "sort":
        if current["materialized"] is None:
            rows = []
            while True:
                row = pull(current["child"])
                if row is EOS:
                    break
                rows.append(row)
            current["materialized"] = tuple(
                sorted(rows, key=lambda value: (-value[1], value[0]))
            )
        if current["position"] == len(current["materialized"]):
            return EOS
        row = current["materialized"][current["position"]]
        current["position"] += 1
        return row
    if kind == "project":
        row = pull(current["child"])
        return EOS if row is EOS else (row[0], row[1] * 10)
    if kind == "limit":
        if current["emitted"] == current["count"]:
            return EOS
        row = pull(current["child"])
        if row is EOS:
            return EOS
        current["emitted"] += 1
        return row
    raise RuntimeError("unknown operator")


def stop(current, events):
    if current["stopped"]:
        return
    events.append(f"close:{current['name']}")
    current["stopped"] = True
    if current["child"] is not None:
        stop(current["child"], events)


events = []
scan = node(
    "scan",
    "scan",
    rows=((1, 4), (2, 7), (3, 2), (4, 9), (5, 8)),
    position=0,
)
filtered = node("filter", "filter", scan, minimum=7, passed=0)
ordered = node("sort", "sort", filtered, materialized=None, position=0)
projected = node("project", "project", ordered)
limited = node("limit", "limit", projected, count=2, emitted=0)

start(limited, events)
result = []
while True:
    row = pull(limited)
    if row is EOS:
        break
    result.append(row)
stop(limited, events)

opened = ",".join(item.split(":")[1] for item in events if item.startswith("open:"))
closed = ",".join(item.split(":")[1] for item in events if item.startswith("close:"))
print(f"result={tuple(result)}")
print(f"scan_rows_examined={scan['position']}")
print(f"scan_next_calls={scan['next_calls']}")
print(f"filter_next_calls={filtered['next_calls']}")
print(f"filter_rows_passed={filtered['passed']}")
print(f"sort_input_rows={len(ordered['materialized'])}")
print(f"sort_next_calls={ordered['next_calls']}")
print(f"project_next_calls={projected['next_calls']}")
print(f"limit_next_calls={limited['next_calls']}")
print(f"limit_child_stopped_early={ordered['position'] < len(ordered['materialized'])}")
print(f"opened={opened}")
print(f"closed={closed}")
print("evidence=pull_lifecycle_and_blocking_boundary")
```

This model deliberately excludes SQL NULL/three-valued logic, tuple-slot reuse, exceptions during partial open/close, rescan, parameters, snapshots, joins, spill, parallelism, asynchronous I/O, and timing. Python method dispatch is not a database CPU benchmark.

**Rescan is a new execution contract.** A nested-loop parent may change correlation parameters and ask the inner plan to restart. A scan might reset a cursor under the same snapshot; a sort might rewind retained output; a volatile function may need reexecution; a network source may be nonrewindable. `rescan` must specify parameter propagation, expression reevaluation, snapshot identity, state reset, instrumentation accumulation, and resource reuse. If those cannot be met, the optimizer must materialize or choose another plan.

Mark/restore and backward scan are stronger than restart. They require a child to preserve a position or provide random access. The parent cannot infer that capability from `next`. Physical-property and executor APIs must advertise it, and initialization flags may change the operator's storage strategy.

**Cancellation and errors cross recursion.** Long filter loops, hash builds, sorts, expression evaluation, scans, and device waits need cancellation points. Excessively frequent checks add overhead; rare checks violate latency objectives. Use bounded work units and interruptible I/O. On an error, unwind every successfully initialized node exactly once, preserving the primary error while reporting cleanup failures separately. Never return a partially valid row whose fields failed halfway unless the protocol explicitly supports per-field errors.

**Instrumentation must understand nesting.** Root elapsed time includes child time. A node's inclusive time includes recursive calls; exclusive/self time subtracts correctly attributed child work and instrumentation overhead. Row counters need clear meanings: calls received, input occurrences fetched, predicate evaluations, output occurrences, loops/rescans, rows removed, batches, and end calls are different. A filter can receive one call yet scan thousands of rows before producing a match. A sort's first call can contain nearly all its work.

Timing each tuple call can perturb a tight iterator loop. Sampling, coarse intervals, hardware counters, and batch accounting reduce overhead but need calibration. Profiles should retain plan and parameter identity, estimates versus actuals, first-row and total latency, memory/spill, I/O, cancellations, errors, and concurrency. Do not attribute all child time to the parent as “self,” and do not compare different semantics or cache states.

**Extensibility requires more than a function pointer.** A new operator must declare accepted child schemas and properties, output schema/properties, parameter and expression support, lifecycle and rescan abilities, state and memory ownership, spill behavior, parallel safety, cancellation, errors, instrumentation, and serialization/versioning where relevant. The optimizer needs cost and property rules; the executor needs initialization dispatch and cleanup; explain/profile needs stable naming; tests need reference semantics and adversarial cases.

PostgreSQL 18 currently describes its executor as demand-pull: each plan-node call returns one more row or exhaustion. Its source dispatches plan-state types through executor initialization and per-node procedures; its sort node consumes its outer plan before serving sorted tuples. This is evidence about that version, not proof that every PostgreSQL node or every database uses a textbook three-method object interface.

**Alternative engines expose the abstraction's cost.** SQLite compiles statements to VDBE bytecode; `sqlite3_step()` advances until a result row, completion, or error, and the `ResultRow` opcode suspends execution. DuckDB's current internals documentation describes push-based vectorized `DataChunk` flow. MonetDB/X100 demonstrated vectorized primitives; Neumann's data-centric compilation work fuses code around pipelines to improve locality and branch behavior. These systems differ in granularity and control direction, yet all need explicit state, blocking boundaries, ownership, and termination.

## Definitions and Notation

- **P**: immutable or logically immutable physical plan.
- **S(v)**: execution-local state for plan node v.
- **I(v)**: input bag/stream observed by node v under its child contract.
- **O(v)**: output occurrence sequence produced by node v.
- **`open(v)`**: establish valid execution state and initialized descendants.
- **`next(v)`**: produce one legal output occurrence or the explicit end marker.
- **`close(v)`**: release resources for v and all initialized descendants not otherwise owned.
- **EOS**: end-of-stream control value, disjoint from every legal SQL record.
- **Streaming operator**: can produce output after bounded input progress and retains bounded incremental state under stated width assumptions.
- **Blocking operator**: requires completion of a relevant input boundary before ordinary output.
- **Pipeline**: operators connected without full intermediate materialization.
- **Pipeline breaker**: operator boundary that materializes or completes an input region before downstream progress.
- **Inclusive work**: a node's work interval including descendant activity.
- **Exclusive work**: work attributed to the node after removing correctly nested descendant work.
- **Loop**: one execution or rescan instance recorded for a node.
- **Support function**: parameterized behavior such as comparison, hashing, predicate, projection, or type operation supplied to a generic operator.
- **Exchange**: mechanism that transfers records between workers/processes and can introduce partitioning, buffering, and parallel control.

For a finite tree, local correctness means each node transforms child outputs according to its physical specification. Composition additionally assumes compatible schemas/representations, one consistent snapshot/parameter environment, reliable control/error signaling, and correct lifecycle ownership.

## Mechanisms, Invariants, or Proof Structure

**Lifecycle state machine.** Model a node as `created -> open -> active/exhausted -> closed`, with error/cancellation transitions from open or active into cleanup then closed. `next` is legal only while active; after EOS, repeated behavior must be specified (commonly EOS again) or forbidden. `close` should tolerate partial initialization and repeated calls. A failed child open prevents parent activation but still requires cleanup for already opened siblings/resources.

**Structural correctness argument.** Base case: a scan emits exactly the occurrences selected from its source under the snapshot/access-path contract. Inductive step: assume each child sequence is correct. If the parent consumes those sequences according to its local physical semantics and emits exactly its specified transformation, its output is correct. Applying induction at the root establishes the plan result. This argument does not establish that the optimizer chose a logically equivalent plan or that operator implementations meet their local specifications; those are separate proofs/tests.

**Filter invariant.** At entry to each loop iteration, every previously consumed child occurrence has either been emitted exactly once because its predicate was TRUE or rejected because it was FALSE/UNKNOWN under SQL rules. The next child occurrence is evaluated once. EOS is returned only after child EOS. This proves ordered-subsequence behavior and multiplicity preservation for accepted occurrences.

**Limit invariant.** After e outputs, `0 <= e <= N`, and exactly the first e child outputs have been forwarded. If e=N, return EOS without another child request. Early closure must still propagate. Offset, ties, percent, or nondeterministic underlying order require different/extended semantics.

**Blocking-sort invariant.** Before first output, consume the complete child, build a bag-equivalent ordered representation, then return its elements in order. A root limit cannot save child work below this boundary, although a semantically valid bounded top-N sort could change the physical operator.

**Ownership invariant.** At every suspension point, each live cursor, buffer, record reference, memory allocation, file, and task has one accountable owner or an explicit shared-ownership protocol. Advancing a child invalidates borrowed state exactly as declared. Close releases all ownership not transferred to a longer-lived result/client layer.

**Cancellation bound.** If each loop performs at most W bounded-cost work between cancellation checks and each I/O is interruptible within L, response latency is bounded by roughly the current work slice plus I/O cancellation and cleanup, not merely root call count. The bound is conditional on scheduler/runtime behavior and must be measured.

**Evidence hierarchy.** The executable proves one finite lifecycle trace. Independent recomputation checks counters. Source review checks historical and current implementation claims. Symbolic review checks composition and invariants. Target-engine conformance, CPU profiling, concurrency, and fault tests remain necessary for deployment claims.

## Alternatives and Trade-Offs

**Tuple-at-a-time pull** offers a tiny compositional interface, natural early termination, and localized state. It pays frequent calls/branches, can obscure work inside one request, and often underuses SIMD/cache bandwidth.

**Batch or vector pull** returns multiple rows per call. It amortizes dispatch and enables columnar/vector primitives while retaining demand control. Batches need selection vectors, NULL masks, buffer lifetime rules, variable cardinality, and careful latency/cancellation policy.

**Push execution** has producers send rows or chunks to consumers. It can form explicit pipelines and work well with parallel scheduling, but early termination and backpressure require control channels; multi-input operators and resumable state can be harder to express.

**Data-centric compilation** generates fused loops for pipeline regions, improving instruction locality and eliminating generic dispatch. It adds compilation latency, code-cache management, deoptimization/fallback, security hardening, and debugging/observability complexity.

**Bytecode interpretation** compiles SQL into a database virtual-machine program. It centralizes control, can make suspension explicit, and avoids a deep object-call tree. Opcode dispatch remains interpretation overhead, and operator-level properties may be less visually direct.

**Materialization between operators** simplifies ownership, rescan, scheduling, and failure boundaries. It costs memory/I/O, copying, and latency. Selective materialization can be required for correctness or beneficial for reuse/adaptivity.

**Coroutines/language generators** express suspension directly and can make implementations readable. Runtime allocation, exception, stack, cancellation, and performance characteristics must still satisfy engine contracts.

**Parallel exchange** can turn an existing plan region into producer/consumer workers and hide parallelism from many operators, as Volcano explored. It introduces queues, partition correctness, serialization, backpressure, cancellation, skew, and failure coordination.

## Failure Modes and Misconceptions

1. **“`next` means cheap constant work.”** A call can scan many rejected rows, build a hash table, or perform an entire external sort.
2. **“Pull means streaming.”** Control direction and materialization behavior are different properties.
3. **“NULL can represent EOS.”** SQL NULL is data; use a disjoint tagged control result.
4. **“Closing is optional after limit.”** Early termination is exactly when descendants may still own substantial state.
5. **“An immutable plan can share its state.”** Share configuration only; cursors, parameters, counters, and buffers are execution-local unless synchronization is designed.
6. **“A child row stays valid.”** Slots/vectors are often reused; retain only under explicit ownership or copy/pin.
7. **“Rescan just resets a counter.”** Parameters, snapshots, volatile expressions, spill, and external sources determine validity.
8. **“Child error is end-of-stream.”** It changes transaction/client semantics and must propagate distinctly.
9. **“One predicate evaluation is harmless to repeat.”** Volatile functions, errors, and cost make evaluation count observable.
10. **“Root row counts explain performance.”** Hidden child calls, rejected rows, loops, blocking work, I/O, and representation costs matter.
11. **“Inclusive time is self time.”** Recursive child work must be attributed consistently.
12. **“Per-row tracing is free.”** It can dominate the execution being measured.
13. **“Uniform interface means uniform capabilities.”** Rewind, mark/restore, spill, parallelism, ordering, and random access require explicit properties.
14. **“Iterator execution is obsolete.”** Its compositional ideas remain valuable, while granularity and dispatch are design choices to measure.

## Worked Examples

### Example 1

**Situation:** A filter receives one parent request. Its first 999 child rows make the predicate FALSE; row 1,000 is TRUE. The filter returns one row after 1,000 scan calls. **Conclusion:** parent call count is not input work; record input, rejected, predicate, and output counts separately.

### Example 2

**Situation:** A row has one nullable column whose value is NULL. An API uses a null pointer to mean EOS and also represents the row with a null pointer. The consumer terminates early. A tagged result `{ROW, payload}` versus `{END}` distinguishes them. **Conclusion:** control state must be disjoint from legal SQL values.

### Example 3

**Situation:** `Limit(10, Filter(Scan))` finds ten matches in the first 100 records of a billion-row source. Limit returns EOS without an eleventh child call, then close cancels/tears down the scan. **Conclusion:** pull supports early stop when no blocking boundary below has already consumed the input.

### Example 4

**Situation:** `Limit(10, Sort(Scan))` has the same result request, but full sort's first call drains the billion rows before returning its minimum. A bounded top-N sort might avoid full ordering if semantics allow it. **Conclusion:** a limit cannot retroactively make a blocking child lazy.

### Example 5

**Situation:** Nested loop holds outer row A, opens the parameterized inner, emits three matches, then rescans inner for outer B. The inner source is a nonrewindable network stream. Materialization or a different join is required. **Conclusion:** rescan capability is a physical property, not implied by `next`.

### Example 6

**Situation:** A child reuses one tuple slot. Hash build stores pointers from three calls; after the third call, all pointers show the third row. Copying keys/payload into owned hash memory fixes it. **Conclusion:** advancement and retention require an explicit borrowed-versus-owned lifetime contract.

### Example 7

**Situation:** A predicate calls a volatile sequence function. Instrumentation evaluates it once to label the row and the filter evaluates it again, changing both result and sequence state. Instrumentation must observe the already computed outcome without reexecution. **Conclusion:** measurement cannot silently alter evaluation count.

### Example 8

**Situation:** Opening the left child succeeds; opening the right child fails. The join never becomes active, but must close the left child and local allocations exactly once while preserving the right-open error. **Conclusion:** partial initialization belongs in the lifecycle state machine and fault tests.

### Example 9

**Situation:** A node reports 120 ms inclusive time and its only child reports 100 ms. About 20 ms may be attributable to the node only if timers are correctly nested and overhead/parallel overlap is handled. Subtracting parallel child times mechanically can yield nonsense. **Conclusion:** define timing attribution before interpreting profiles.

### Example 10

**Situation:** A custom geospatial join implements `next` but declares neither output ordering nor rewind support. The optimizer assumes both, removes a sort, and places it inside nested loop. Results become unordered and rescan fails. **Conclusion:** an extension contract includes physical properties and lifecycle capabilities, not just row production.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies operational semantics, effects, exceptions, and observational equivalence for lifecycle protocols.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies channels, backpressure, cancellation, structured concurrency, task ownership, and race analysis.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) connects bytecode dispatch, interpretation, code generation, specialization, and deoptimization to query execution.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) contributes interface contracts, extension boundaries, dependency direction, and lifecycle ownership.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies model-based state-machine tests, metamorphic oracles, fault injection, and instrumentation validation.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains cache locality, branch prediction, SIMD, instruction dispatch, memory bandwidth, and NUMA costs.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies file/socket cursors, asynchronous I/O, resource cleanup, scheduling, cancellation, and process failure.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) extends local iterators into exchanges, partitioned streams, backpressure, retries, and partial failure.

## References

1. Goetz Graefe, [“Volcano—An Extensible and Parallel Query Evaluation System”](https://doi.org/10.1109/69.273032), *IEEE Transactions on Knowledge and Data Engineering* 6(1), 1994. Primary system paper on iterators, support functions, exchange, extensibility, and parallel execution.
2. Goetz Graefe, [“Query Evaluation Techniques for Large Databases”](https://web.stanford.edu/class/cs346/2014/graefe.pdf), *ACM Computing Surveys* 25(2), 1993. Primary survey of iterators, operator composition, materialization, and database algorithms.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Executor](https://www.postgresql.org/docs/18/executor.html), retrieved 2026-08-30. Current demand-pull plan-tree description and sort/merge-join trace.
4. PostgreSQL Global Development Group, [`execProcnode.c` source](https://doxygen.postgresql.org/execProcnode_8c_source.html), retrieved 2026-08-30. Current plan-state initialization, dispatch, execution, and cleanup structure.
5. PostgreSQL Global Development Group, [`nodeNestloop.c` source](https://doxygen.postgresql.org/nodeNestloop_8c_source.html), retrieved 2026-08-30. Current nested-loop state, inner rescan, qualification, and row-production implementation.
6. PostgreSQL Global Development Group, [`nodeSort.c` source](https://doxygen.postgresql.org/nodeSort_8c_source.html), retrieved 2026-08-30. Current blocking sort initialization, child draining, tuple retrieval, rescan, and cleanup.
7. SQLite Project, [The SQLite Bytecode Engine](https://sqlite.org/opcode.html), retrieved 2026-08-30. Current VDBE execution and `ResultRow` suspension behavior.
8. DuckDB Foundation, [Overview of DuckDB Internals](https://duckdb.org/docs/current/internals/overview), retrieved 2026-08-30. Current push-based vectorized `DataChunk` execution description.
9. Peter Boncz, Marcin Zukowski, and Niels Nes, [“MonetDB/X100: Hyper-Pipelining Query Execution”](https://www.cidrdb.org/cidr2005/papers/P19.pdf), CIDR 2005. Primary vectorized execution paper and CPU-efficiency study.
10. Thomas Neumann, [“Efficiently Compiling Efficient Query Plans for Modern Hardware”](https://www.vldb.org/pvldb/vol4/p539-neumann.pdf), *PVLDB* 4(9), 2011. Primary data-centric query compilation design and evaluation.

## Exercises

### Exercise 1

Define the minimum observable states and transitions for a safe iterator lifecycle, including partial initialization, EOS, error, early stop, and repeated close.

### Exercise 2

Trace child `next` calls for a filter over values `[1,2,3,4,5]` accepting even values, with a parent limit of one. Assume the consumer asks the limit once for a row and once for EOS. Then contrast behavior when a full sort sits between filter and limit.

### Exercise 3

Diagnose a plan where root output is only 100 rows but latency is high. The profile shows a filter with 50 million input rows, a sort below limit, two rescans, and inclusive times on every node. Specify the additional counters and attribution checks needed before changing the plan.

### Exercise 4

Compare tuple pull, vector pull, push/vector execution, and data-centric compilation for a scan-filter-project analytical pipeline and a latency-sensitive query that often stops after one row.

### Exercise 5

Design the executor contract for a third-party operator that reads a remote partitioned source and supports filtering. Include schemas/properties, state, row ownership, backpressure, cancellation, rescan, errors, parallelism, credentials, instrumentation, and conformance tests.

## Answers to the Exercises

### Answer 1

Use at least `created`, `opening`, `active`, `exhausted`, `closing`, and `closed`, with error/cancellation transitions from opening/active to cleanup. Successful open establishes children/local resources before active. Next is legal only when active and yields tagged ROW or EOS; error/cancellation is distinct. EOS moves to exhausted, whose repeated-next behavior is specified. Early stop invokes close from active. Partial open tracks exactly which resources/children succeeded so cleanup releases them once. Close is idempotent from every initialized state, preserves the primary failure, and finishes in closed; next after close is rejected.

### Answer 2

Without sort, the first limit request calls filter once; filter calls its child for 1 (reject) and 2 (accept), then returns 2. On the second limit request, the limit has emitted one and returns EOS without another filter/scan call. Thus scan next calls are two, filter calls one, and limit calls two before close. With full sort between them, sort's first call drains filter: filter produces 2, then 4, then EOS while scanning all five values plus one scan EOS call. Sort orders `[2,4]`, returns 2, and limit later returns EOS without requesting 4. The result matches, but work and retained state differ.

### Answer 3

Collect per-loop calls, input/output rows, rows removed, expression evaluations, sort input/output, method, memory, spill/run/pass/temp I/O, rescan parameter values, child EOS calls, first-row/total latency, waits, I/O, cancellations, and estimates versus actual rows/width. Establish whether the limit is above a semantically necessary full sort or a top-N/incremental/index order is legal. Check why two rescans occur and whether materialization would help. Verify timer nesting, parallel overlap, loops, and instrumentation overhead before subtracting inclusive times. Root output alone says nothing about 50 million filtered inputs or blocking work.

### Answer 4

Tuple pull is simple and permits immediate early stop but pays dispatch/branch overhead per occurrence. Vector pull amortizes calls and enables columnar/SIMD primitives, while batch fill can delay a one-row response and requires buffer/selection ownership. Push/vector execution naturally drives chunks through analytical pipelines and parallel schedulers, but needs backpressure and explicit early-stop propagation. Data-centric compilation can fuse scan/filter/project into cache-friendly code with minimal dispatch, at the cost of compilation latency, code cache, fallback, and observability complexity. For long analytical scans, measure vector/push/compiled routes; for frequent one-row stop, include startup/compile and overproduction, so tuple or small adaptive batches may win. Semantic equivalence and same cache/data conditions are prerequisites for comparison.

### Answer 5

Declare accepted partition metadata and input parameters, output schema/order/partitioning, predicate semantics, snapshot/consistency, and whether rows are copied, borrowed, or batch-owned. Instantiate per-execution cursors, credentials, buffers, retries, and counters; never share mutable state implicitly. Define bounded queues or demand credits for backpressure; propagate stop/cancellation to all remote requests and close handles idempotently. State whether rescan is unsupported, reissues against the same snapshot/token, or uses retained materialization. Distinguish EOS, transport retryable/nonretryable errors, data errors, authorization, timeout, and partial partition failure. Declare partition parallelism, ordering merge, skew, and resource limits. Keep credentials least-privilege and out of logs/spill. Instrument partitions, requests, bytes, rows before/after filter, retries, waits, first/total latency, cancellation, and cleanup. Test a reference finite source, duplicates/NULLs, partitions reordered or repeated/missing, short pages, token expiry, timeout, cancellation at every state, partial open, rescan rules, buffer lifetime, quota, and leak-free cleanup.
