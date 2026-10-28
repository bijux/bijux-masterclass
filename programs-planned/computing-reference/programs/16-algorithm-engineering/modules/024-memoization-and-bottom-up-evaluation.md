---
module_id: ALGE-024
program: Algorithm Engineering
level: 1
module_number: 24
title: Memoization and Bottom-Up Evaluation
status: complete
last_verified: 2026-09-04
---

# Memoization and Bottom-Up Evaluation

## One-Page Review

### Governing question

Given a correct dynamic-programming state recurrence, which evaluation schedule computes exactly the requested result with acceptable work, memory, stack depth, locality, reconstruction, and operational behavior?

### Essential definitions

- **Memoization** evaluates a state on demand and caches its result under a canonical key.
- **Bottom-up evaluation**, or **tabulation**, evaluates a predecessor-closed state domain in an order that makes every dependency available before use.
- A **dependency graph** has an edge $t\to s$ when evaluating $V(s)$ reads $V(t)$.
- The **ancestor closure** $R(q)$ of query state $q$ contains $q$ and every state transitively required by it.
- A **topological order** places every dependency before its consumer in an acyclic dependency graph.
- A **memo hit** reuses a completed entry; a **memo miss** evaluates a previously unseen key.
- A state may be **unseen**, **active**, or **done**; encountering an active dependency exposes a cycle.
- A **live frontier** is the set of previously computed values still needed by future states.
- **Rolling storage** reuses table locations after their values leave that frontier.
- A **single-flight** mechanism coordinates concurrent requests so at most one producer computes a key while waiters share its result.

### Central model, mechanism, or theorem

Let $B$ be base states and let each nonbase state have deterministic recurrence

$$
V(s)=F_s\left(\bigl(V(t)\bigr)_{t\in\operatorname{Pred}(s)}\right).
$$

Assume the dependency graph is finite and acyclic, bases and impossible values are defined, and $F_s$ has stable numeric and tie semantics. Memoized depth-first evaluation from query $q$ computes only $R(q)$. Bottom-up evaluation computes any chosen domain $T$ that contains $q$ and is closed under predecessors, in topological order. By induction on that order, both assign every common state the same unique recurrence value.

With constant expected cache operations and constant-time transitions, memoized work is $O(|R(q)|+|E_R|)$ and space is $O(|R(q)|+h)$, where $h$ is maximum active recursion depth. A direct bottom-up pass costs $O(|T|+|E_T|)$ work and $O(|T|)$ value space before liveness compression. Real bounds must also include key construction, hashing, transition cost, parent storage, allocation, and cache coordination.

### Critical invariants

- State semantics, bases, transitions, objective, and ties remain identical across evaluation strategies.
- Every cache key includes or is scoped by all inputs that determine the state value.
- Only a done entry may be returned as a hit; active and failed entries have explicit behavior.
- False, zero, empty, impossible, and null-like values are cached values, not evidence of absence.
- Every bottom-up read refers to an initialized predecessor in the declared order.
- The selected table domain is predecessor-closed, or missing dependencies are handled explicitly.
- Rolling storage retains a value until its final consumer and overwrites in a recurrence-safe direction.
- Reconstruction follows the same tie rule and retains, checkpoints, or recomputes enough information.
- Cache size, stack depth, table bytes, numeric range, and concurrent producers are bounded before execution.
- Measurements count distinct states, dependency attempts, hits, misses, live cells, bytes, and witness checks—not hit rate alone.

### Common failures

Common failures include memoizing an impure function; omitting instance or policy version from a key; using a process-global cache across tenants; treating a cached zero as absent; publishing a partially computed value; recursing through a cycle; overflowing the call stack on a long chain; swallowing exceptions into ordinary values; tabulating in consumer-before-dependency order; leaving cells uninitialized; allocating a dense table for sparse reachable states; looping capacities upward in 0/1 knapsack and thereby reusing one item; compressing rows needed for reconstruction; assuming a thread-safe map prevents duplicate computation; allowing eviction to invalidate a once-per-state work proof; and comparing strategies using a warm cache on one side only.

### Compact example

For Fibonacci values $F(0)=0$, $F(1)=1$, and $F(n)=F(n-1)+F(n-2)$, naive recursion makes 177 calls for $F(10)$. Memoization evaluates 11 distinct states and makes 19 total calls: 11 misses and 8 hits. Bottom-up evaluation computes the same 11 values in order $0,1,\ldots,10$. Because only the previous two values are live, value-only bottom-up storage can shrink from 11 cells to two. These are different evaluation and storage choices for the same recurrence.

### Connections

[ALGE-023](./023-dynamic-programming-state-design.md) proves the state recurrence, [ALGE-004](./004-inductive-correctness-proofs.md) supplies induction, [ALGE-005](./005-asymptotic-time-and-space.md) supplies cost models, and [ALGE-025](../ROADMAP.md) contrasts caching overlapping states with searching distinct partial assignments.

## Governing Question

How should a proven state recurrence be scheduled and stored so implementation cost matches the reachable dependency structure and the result remains exact?

State design answers what a subproblem means. Evaluation answers when to compute it, how to find its dependencies, where to retain its result, and how to recover the witness. Confusing those questions produces folklore such as “top-down is always slower” or “bottom-up always uses less memory.” Neither statement follows without a dependency domain, representation, workload, and output contract.

Memoization is demand-driven. It often mirrors the recurrence and avoids states outside the query's ancestor closure. Bottom-up evaluation makes order and storage explicit. It often removes call-stack risk, permits compact arrays and rolling frontiers, and exposes locality or parallel wavefronts. Both can be exact implementations of the same mathematics.

## Why This Matters

A recurrence with polynomially many states can still fail in production. Recursive depth can exceed the runtime stack. A global memo can return a value computed for an earlier dataset. A dense table can allocate gigabytes although only a narrow corridor is reachable. A one-row optimization can silently turn 0/1 choice into unbounded reuse. A synchronized cache can remain coherent yet calculate the same expensive state concurrently many times.

Evaluation choices also change evidence. Memo hit rate says little without miss cost and query scope. A tabulation benchmark may include millions of irrelevant cells. A warm-cache comparison may charge initialization to only one strategy. Parent pointers can dominate value memory. Persistent caches introduce versioning, authorization, invalidation, and privacy obligations absent from the recurrence proof.

Good engineering preserves semantic equivalence while measuring the physical execution: evaluated states, dependency edges, lookup cost, live cells, stack depth, bytes, contention, recomputation, and witness validation.

## Prerequisites and Retrieval

Retrieve:

- state semantics, Bellman recurrences, bases, impossibility, rank, and deterministic ties from ALGE-023;
- induction over natural numbers and topological orders;
- directed acyclic graphs, predecessors, reachability, and depth-first traversal;
- arrays, maps, tuples, hashing, equality, mutability, and integer overflow;
- recursion, call stacks, exceptions, cancellation, threads, and synchronization;
- cache hit/miss terminology, bounded storage, eviction, and invalidation;
- working-set, locality, allocation, and benchmark controls;
- exhaustive small-instance oracles and witness replay.

You should be able to state exactly what $V(s)$ means and prove its recurrence before selecting either evaluator.

## Learning Objectives

After completing this module, you should be able to:

1. separate recurrence semantics from evaluation schedule and storage representation;
2. prove memoized and bottom-up evaluators equivalent on a finite acyclic dependency domain;
3. derive work and space from reached states, selected table states, dependency edges, and active depth;
4. implement cache membership, active-cycle detection, failure handling, and canonical keys correctly;
5. derive a bottom-up topological or coordinate order from recurrence dependencies;
6. compress storage from dependency liveness without changing update semantics;
7. preserve deterministic witness reconstruction under rolling or bounded storage;
8. diagnose cache contamination, stack overflow, wrong loop direction, and concurrency duplication;
9. select memoized, bottom-up, explicit-stack, or hybrid evaluation from workload evidence;
10. design bounded, reproducible tests and telemetry for correctness and performance claims.

## Core Exposition

### Freeze the recurrence before choosing an evaluator

Let $\mathcal S$ be a finite state set, $B\subseteq\mathcal S$ its bases, and $\operatorname{Pred}(s)$ the states whose values are read by $s$. Write

$$
V(s)=
\begin{cases}
b(s), & s\in B,\\
F_s\left(\bigl(V(t)\bigr)_{t\in\operatorname{Pred}(s)}\right), & s\notin B.
\end{cases}
$$

This specification fixes state meaning, legal dependencies, base and impossible values, arithmetic, aggregation, and ties. It does not demand recursion, a map, nested loops, or a rectangular table.

The dependency graph has edge $t\to s$ when $t\in\operatorname{Pred}(s)$. A rank $r$ satisfying $r(t)<r(s)$ on every edge proves acyclicity and suggests an order. If such an order does not exist because the model has genuine cycles, ordinary finite dynamic programming is not justified merely by adding a cache.

### Identify the query's ancestor closure

For query $q$, define $R(q)$ as the least set such that:

1. $q\in R(q)$;
2. if $s\in R(q)$, then every $t\in\operatorname{Pred}(s)$ named by its legal recurrence is in $R(q)$.

Memoized evaluation discovers this closure dynamically. A bottom-up implementation chooses some predecessor-closed $T$ with $R(q)\subseteq T\subseteq\mathcal S$. A carefully restricted table may make $T=R(q)$; a convenient dense rectangle may make $T$ much larger.

This distinction explains the most durable top-down advantage: it can avoid states not demanded by the query. It does not imply faster execution. Hashing, recursion, object allocation, branch behavior, and poor locality can outweigh avoided cells.

### Understand repeated recursion before caching

Without retention, a recursive evaluator follows a computation tree, not the quotient state DAG. The same state can occur once for every path reaching it. For Fibonacci call count $C(n)$,

$$
C(0)=C(1)=1,
\qquad
C(n)=1+C(n-1)+C(n-2).
$$

Thus $C(10)=177$, even though only states $0$ through $10$ exist. Memoization collapses repeated tree nodes with equal keys into one completed state computation.

Overlapping subproblems are necessary for this speedup. If every recursive state is unique, a memo adds storage and lookup without eliminating work. Measure duplicates rather than assuming them from the presence of recursion.

### Implement memoization as a state machine

A robust memo entry has at least three logical conditions:

- **unseen:** no evaluation has begun;
- **active:** this evaluation owns an unfinished computation;
- **done:** a complete value may be reused.

On an unseen state, mark active, evaluate dependencies, validate the result, then publish it as done. On done, return the stored value. Encountering active on the same dependency chain reveals a cycle or re-entrancy that requires an explicitly different algorithm.

Failure policy is part of the mechanism. If evaluation raises, is cancelled, times out, or exceeds a resource limit, remove the active entry or publish a typed failure according to the API contract. Never expose a partially initialized value as a successful hit.

Language helpers may hide this lifecycle. Understand whether they cache exceptions, admit re-entrant calls, retain arguments strongly, expose statistics, synchronize map mutations, or coordinate producers.

### Distinguish absence from every valid value

Zero, `False`, an empty tuple, an empty witness, and a tagged impossible result can all be legitimate cached values. A test equivalent to “if cache[key] is truthy” is therefore not a membership test.

Use explicit membership, a private missing sentinel, or a result variant such as `Missing | Active | Done(value) | Failed(error)`. If null is valid, it cannot double as missing. This is both a correctness issue and a performance issue: silently recomputing zero-valued states may preserve the final answer while destroying the advertised bound.

### Make cache identity match value identity

Memoization is sound only when equal keys imply equal results for the cache's lifetime. If $V(s)$ also depends on input array $x$, graph revision $g$, objective mode $m$, policy version $p$, or tenant $u$, either:

- include stable identities or content fingerprints for those inputs in the key; or
- scope the entire cache to the immutable evaluation instance that owns them.

Mutable objects are dangerous as keys even when a language permits them indirectly. Hash/equality must remain stable, aliases must not mutate inputs behind the evaluator, and identity reuse must not make a new object look like an old instance.

Cache keys are also security boundaries. Sharing by state coordinates alone can cross tenant, authorization, locale, or policy boundaries. Include the governing context or isolate the cache; do not rely on callers to remember manual invalidation.

### Require referential transparency or declare invalidation

A pure state evaluator returns the same value for the same complete key and has no externally visible effect. Such functions are natural memoization targets.

For time, randomness, I/O, mutable databases, feature flags, or permission checks, a coordinate-only cache freezes an observation. Correct use requires a snapshot, version, expiration policy, or explicit invalidation theorem tied to the desired semantics. Time-to-live is an operational policy, not proof that stale values are acceptable.

Side effects are another trap. A memoized function may emit an audit event on a miss but not on a hit, changing observable behavior. Separate pure value computation from required per-request effects.

### Bound memoized work and space honestly

Let $E_R$ be dependency edges examined while evaluating $R(q)$. With constant-time transitions and expected $O(1)$ map operations,

$$
T_{\mathrm{memo}}(q)=O(|R(q)|+|E_R|).
$$

More generally,

$$
T_{\mathrm{memo}}(q)=
O\left(
\operatorname{key}(q)+\operatorname{lookup}(q)
+
\sum_{s\in R(q)}
\left(
\operatorname{evaluate}(s)
+\sum_{t\in\operatorname{Pred}(s)}
\left(
\operatorname{transition}(t,s)
+\operatorname{key}(t)
+\operatorname{lookup}(t)
\right)
\right)
\right).
$$

Hash operations are expected rather than universal constant time unless stronger map guarantees apply. Copying a subset into a key, comparing a long string, or materializing all transitions can dominate recurrence arithmetic.

If $h$ is maximum active dependency depth, ordinary recursive memoization uses

$$
O(|R(q)|+h)
$$

stored values plus call frames, excluding key, parent, allocator, and runtime overhead. A chain can have $|R(q)|=h$ and no repeated states, making recursion all risk and no reuse benefit.

### Interpret hits and misses in context

For one cold query with entries retained indefinitely, misses often equal distinct evaluated states. Hits count repeated requests for already done states. The ratio

$$
\rho=\frac{H}{H+M}
$$

is descriptive, not an objective. A zero-hit calculation may be optimal if only a small ancestor closure is needed. A 99% hit rate may still be slow if each lookup serializes a large key or waits on a remote cache.

Report misses, hits, dependency attempts, miss cost, lookup latency, key bytes, entry bytes, evictions, recomputations, active depth, and query result. State whether the cache was cold, warm, shared, or prepopulated.

### Derive a bottom-up dependency order

Bottom-up evaluation chooses a predecessor-closed domain $T$ and orders it as $s_1,\ldots,s_k$ so

$$
t\in\operatorname{Pred}(s_i)
\Longrightarrow
t=s_j\text{ for some }j<i.
$$

Coordinate recurrences often make the order obvious: increasing prefix length, increasing interval length, increasing subset cardinality, or decreasing remaining position. For an irregular DAG, compute or receive a topological order. Kahn's indegree process is one standard method; ALGE-033 develops topological ordering fully.

Initialize every base before its first consumer. Use a distinct uninitialized marker during testing so a wrong order cannot masquerade as a numeric zero. Assertions that every predecessor is ready turn a silent table-order bug into a local failure.

### Bound bottom-up work by the selected domain

Let $E_T$ be dependency edges enumerated within $T$. A direct pass has

$$
T_{\mathrm{tab}}=O(|T|+|E_T|)
$$

under constant-time representation assumptions. A rectangular loop may enumerate invalid or unreachable coordinates and then discard them, so report visited cells, valid cells, dependency attempts, and useful cells separately.

Array tabulation often has lower constants than map-based memoization: compact values, no recursive calls, predictable traversal, fewer allocations, and better spatial locality. These are implementation hypotheses to measure on representative workloads, not consequences of dynamic-programming correctness.

### Compress storage from value liveness

Full tabulation stores all $|T|$ values. That is unnecessary when future states depend only on a narrow frontier. If row $i$ reads only row $i-1$, two rows suffice for values. If each scalar reads only the previous two scalars, two scalar registers suffice.

The proof obligation is liveness:

> A location may be reused only after every future consumer of its old value has executed.

This is stronger than noticing a visually repetitive table. Dependencies determine the required frontier, and traversal order determines when values die.

### Respect in-place update direction

One-dimensional compression can change the recurrence if a just-written value is read as though it came from the previous logical layer. For 0/1 knapsack item $(w,v)$,

$$
\mathrm{dp}[b]\leftarrow
\max\{\mathrm{dp}[b],v+\mathrm{dp}[b-w]\}.
$$

Processing $b$ downward ensures $dp[b-w]$ still represents the preceding item layer. Processing upward permits the same item to update $dp[w]$, then lets that new value update $dp[2w]$, silently implementing unbounded reuse.

For unbounded knapsack, ascending order is intentional. Loop direction is part of semantics, not a micro-optimization.

### Preserve reconstruction under compression

Value-only rolling storage may discard the choices needed to recover a witness. Options include:

- keep parent/action metadata even when values roll;
- checkpoint selected layers and recompute between them;
- rerun recurrence comparisons with identical numeric and tie rules;
- use a problem-specific divide-and-recompute method.

Hirschberg's longest-common-subsequence method is a classic example of retaining linear-space score frontiers while recursively choosing split points. It demonstrates a time-space-reconstruction design, not a universal permission to drop parents.

Always replay the recovered witness against original identities and constraints, then recompute its objective independently.

### Convert top-down recurrence to bottom-up deliberately

Use this conversion sequence:

1. preserve the exact state sentence and recurrence;
2. orient every dependency and identify bases;
3. derive a rank or topological order;
4. choose a predecessor-closed table domain;
5. map state keys to safe indices and allocate with checked arithmetic;
6. initialize bases and impossible/uninitialized markers distinctly;
7. translate each recursive call into a read of an earlier state;
8. preserve branch legality, arithmetic, and total tie order;
9. compare every small state, not only the final query, with the memoized version;
10. compress storage only after dependency liveness is proven.

Conversion is not “replace recursion with loops” mechanically. Reversing an index, merging two logical layers, or choosing an overly broad domain can change behavior or cost.

### Use explicit stacks and hybrids when appropriate

Memoization does not require the language call stack. An explicit frame can record state, next dependency, partial aggregation, and parent. This preserves demand-driven reachability while bounding memory in a controlled heap structure and exposing cancellation points.

A hybrid can discover reachable states top-down, then evaluate the induced DAG bottom-up; tabulate dense interiors while memoizing sparse boundary queries; precompute stable bases and memoize rare extensions; or switch representation after measured frontier density crosses a validated threshold.

Each hybrid needs one semantic recurrence and an explicit ownership boundary. A value computed by one route must have the same key, numeric behavior, tie order, and witness meaning as a value computed by another.

### Treat concurrency as more than map coherence

A cache can protect its internal dictionary and still evaluate the same missing key twice. Two threads may both observe absence, compute, and then publish equivalent results. That can be correct for a pure function yet unacceptable for expensive work or external effects.

Single-flight coordination associates an in-progress promise or condition with a key. It must define producer failure, waiter cancellation, timeout, retry, recursion, and cleanup. Holding a broad lock while recursively requesting dependencies can deadlock. Publishing active markers without ownership rules can make unrelated callers mistake temporary state for a cycle.

Per-request caches are simpler and isolate inputs. Shared caches can reuse across queries but require versioned identity, bounded retention, authorization isolation, contention metrics, and invalidation semantics.

### Account for eviction and persistence

An unbounded memo can exhaust memory or retain sensitive input identities. A bounded cache evicts entries, preserving result correctness for pure deterministic computation but permitting recomputation. Therefore the standard once-per-state work bound no longer holds without an eviction-aware analysis.

Persistent or remote memo stores add serialization, schema version, network failure, atomic publication, corruption detection, expiry, and deployment compatibility. Store only when cross-query reuse exceeds these costs and when the result may safely outlive the request.

### Select from structure and workload evidence

Prefer memoized demand-driven evaluation when query closures are small or irregular, state enumeration is difficult, and active depth is safe or explicitly managed. Prefer bottom-up evaluation when most candidate states are needed, an order is simple, arrays are compact, recursion depth is hazardous, locality matters, or wavefront scheduling is useful.

Benchmark both only after making semantics and evidence comparable:

- identical state recurrence, numeric type, ties, witness contract, and validation;
- cold-versus-warm conditions declared;
- initialization and table clearing charged consistently;
- representative query batches and density distributions;
- peak resident bytes, stack, parent storage, and allocator effects measured;
- correctness checked on every shared state and reconstructed witness.

An algorithm portfolio may select by input shape, but thresholds must be derived from held-out workload evidence and guarded by deterministic fallbacks and resource limits.

### Validate evaluation, not merely the final answer

Build three independent views:

1. a small-instance solution oracle that does not reuse the same dynamic recurrence;
2. memoized and bottom-up evaluators instrumented per state;
3. a replay checker for the chosen witness.

Compare all common state values, ties, impossible states, and parent decisions. Perturb enumeration order, input identity, cache warmth, storage layout, and concurrency schedule. Inject cycles, cancellation, exceptions, eviction, allocation rejection, and stack limits. A final value can remain correct while cache isolation, complexity, or witness behavior is wrong.

### Preserve correspondence in executable evidence

The following finite DAG has two source components. Query vertex 7 depends only on vertices 0 through 7; vertices 8 through 11 are valid table states but irrelevant to that query. Equal-cost paths to vertex 3 exercise the shared lexicographic tie rule.

<!-- bijux-verify: {"id":"memoized-and-bottom-up-dag","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"target=7\nmemoized cost=8 path=(0, 1, 3, 6, 7) states=8 hits=3 misses=8\nbottom_up cost=8 path=(0, 1, 3, 6, 7) table_states=12 transitions=14\nsame=True skipped_by_memo=(8, 9, 10, 11)\n","stderr":""}} -->
~~~python
from functools import cache


nodes = tuple(range(12))
edges = (
    (0, 1, 2),
    (0, 2, 2),
    (1, 3, 1),
    (1, 4, 6),
    (2, 3, 1),
    (2, 5, 5),
    (3, 6, 2),
    (4, 6, 1),
    (5, 6, 1),
    (6, 7, 3),
    (8, 9, 1),
    (8, 10, 4),
    (9, 11, 1),
    (10, 11, 1),
)
sources = frozenset((0, 8))
predecessors = {node: [] for node in nodes}
for left, right, weight in edges:
    predecessors[right].append((left, weight))


@cache
def memoized(vertex):
    if vertex in sources:
        return 0, (vertex,)
    candidates = []
    for parent, weight in predecessors[vertex]:
        prefix_cost, prefix_path = memoized(parent)
        candidates.append((prefix_cost + weight, prefix_path + (vertex,)))
    if not candidates:
        raise ValueError(f"unreachable vertex: {vertex}")
    return min(candidates)


def bottom_up():
    table = {}
    transition_count = 0
    for vertex in nodes:
        if vertex in sources:
            table[vertex] = 0, (vertex,)
            continue
        candidates = []
        for parent, weight in predecessors[vertex]:
            transition_count += 1
            if parent in table:
                prefix_cost, prefix_path = table[parent]
                candidates.append((prefix_cost + weight, prefix_path + (vertex,)))
        if candidates:
            table[vertex] = min(candidates)
    return table, transition_count


def ancestor_closure(query):
    reached = set()
    pending = [query]
    while pending:
        vertex = pending.pop()
        if vertex not in reached:
            reached.add(vertex)
            pending.extend(parent for parent, _weight in predecessors[vertex])
    return frozenset(reached)


target = 7
memo_result = memoized(target)
cache_info = memoized.cache_info()
table, transition_count = bottom_up()
table_result = table[target]
memoized_nodes = ancestor_closure(target)
skipped = tuple(node for node in table if node not in memoized_nodes)

print(f"target={target}")
print(
    "memoized "
    f"cost={memo_result[0]} path={memo_result[1]} "
    f"states={cache_info.currsize} hits={cache_info.hits} misses={cache_info.misses}"
)
print(
    "bottom_up "
    f"cost={table_result[0]} path={table_result[1]} "
    f"table_states={len(table)} transitions={transition_count}"
)
print(f"same={memo_result == table_result} skipped_by_memo={skipped}")
~~~

The `min` comparison orders first by cost and then by the complete path tuple, so both evaluators select the same witness. The reported cache statistics come from the runtime, while the skipped set is derived from the graph's known ancestor closure.

**Reasoning:** Memoization evaluates eight query ancestors and reuses three completed predecessors. The full bottom-up pass evaluates twelve states and all fourteen declared edges.

**Conclusion:** The run demonstrates value and tie correspondence on one finite graph plus a reachability difference; it does not prove arbitrary-DAG correctness, hash bounds, stack safety, or production performance.

## Definitions and Notation

- $\mathcal S$: finite set of recurrence states.
- $B\subseteq\mathcal S$: base states with directly defined values $b(s)$.
- $V(s)$: complete recurrence value of state $s$.
- $F_s$: deterministic combiner for state $s$, including arithmetic and ties.
- $\operatorname{Pred}(s)$: states whose values $V(s)$ directly reads.
- $D=(\mathcal S,E)$: dependency graph with $t\to s$ when $t\in\operatorname{Pred}(s)$.
- $q$: requested query state.
- $R(q)$: ancestor closure required to evaluate $q$.
- $T$: chosen predecessor-closed bottom-up table domain.
- $E_R,E_T$: dependency edges examined within $R(q)$ and $T$.
- $r(s)$: rank that increases from dependencies to consumers.
- $h$: maximum number of simultaneously active recursive states.
- $M,H$: memo misses and hits under a declared cache condition.
- $\rho=H/(H+M)$: observed hit ratio when at least one lookup occurs.
- **Cache scope:** inputs, callers, and lifetime among which entries may be reused.
- **Canonical key:** stable representation whose equality matches value identity.
- **Uninitialized:** table storage whose recurrence value has not been computed.
- **Impossible:** a computed state value representing no feasible completion.
- **Live value:** a completed value with at least one future consumer.
- **Witness metadata:** parent, action, or checkpoint information used to recover a solution.
- **Cold cache:** no applicable entries exist before measurement.
- **Warm cache:** applicable entries predate the measured query.
- **Eviction:** removal of a completed entry, possibly causing later recomputation.
- **Single-flight:** per-key coordination of concurrent producers and waiters.

Uninitialized, impossible, failed, and ordinary zero are different semantic states even when a language offers only one null-like sentinel. Tabulation describes scheduled evaluation, while memoization describes demand-driven reuse; both are dynamic programming when they evaluate the proven recurrence.

## Mechanisms, Invariants, or Proof Structure

Use this evaluator-design and review worksheet.

1. **Freeze semantics.** Record state sentence, recurrence, bases, impossibility, numeric type, and total tie rule.
2. **Orient dependencies.** Draw $t\to s$ exactly when $V(s)$ reads $V(t)$.
3. **Prove well-foundedness.** Supply a rank or topological-order argument; reject unexplained cycles.
4. **Define workload.** Identify query states, batches, cache lifetime, and whether inputs are immutable snapshots.
5. **Determine domains.** Derive $R(q)$ and candidate bottom-up domain $T$; quantify their density and variability.
6. **Choose keys.** Include or scope every value-determining input, version, mode, tenant, and numeric policy.
7. **Define entry lifecycle.** Separate unseen, active, done, failed, cancelled, evicted, and expired conditions as applicable.
8. **Choose order.** For bottom-up evaluation, prove every read precedes its consumer; for memoization, bound active depth or use explicit frames.
9. **Choose representation.** Compare arrays, maps, bitsets, packed values, parents, and allocation overhead under checked sizes.
10. **Prove correspondence.** Induct on rank or topological position to show each evaluator assigns the recurrence value.
11. **Analyze liveness.** Determine the final consumer of every stored layer before rolling or overwriting it.
12. **Preserve witnesses.** Store, checkpoint, or recompute decisions with identical ties and global identities.
13. **Specify failures.** Define cycle, exception, cancellation, timeout, overflow, allocation, and impossible-state behavior.
14. **Specify concurrency.** Decide cache isolation, single-flight ownership, locks, publication, waiters, retries, and invalidation.
15. **Bound cost.** Count states, dependency attempts, key/lookup/transition work, active frames, live values, parent bytes, and recomputation.
16. **Build independent evidence.** Exhaust small instances, compare all shared states, replay witnesses, inject failures, and benchmark controlled cold/warm workloads.

The correspondence proof is compact. Order the finite dependency DAG topologically. Bases agree by definition. Assume both evaluators agree on every predecessor of state $s$. Both then apply the same deterministic $F_s$ to the same predecessor-labeled values under the same numeric and tie semantics, so they agree on $V(s)$. Induction proves equality wherever both evaluate.

This proof does not prove that a proposed key is sufficient, that $T$ contains every dependency, that runtime arithmetic matches the mathematical domain, or that compressed storage preserves inputs. Those are separate obligations.

## Alternatives and Trade-Offs

- **Recursive memoization versus explicit frames:** recursion mirrors the proof; explicit frames control depth, cancellation, and memory accounting.
- **Memoized demand versus dense tabulation:** demand skips irrelevant states; dense arrays reduce lookup and layout overhead when occupancy is high.
- **Sparse map versus indexed array:** maps admit irregular keys and closures; arrays require indexing but improve compactness and locality.
- **Cold per-query cache versus shared warm cache:** isolation simplifies correctness; sharing can amortize work but adds identity, retention, and invalidation obligations.
- **Unbounded versus evicting memo:** retention supports once-per-state analysis; eviction bounds memory but can repeat work.
- **Single-flight versus duplicate pure work:** coordination saves expensive misses; synchronization can add latency, deadlock risk, and failure coupling.
- **Full table versus rolling frontier:** full values simplify debugging and reconstruction; rolling values minimize storage when liveness permits.
- **Parents versus recomputation:** parent metadata speeds witness recovery; recomputation or checkpointing trades extra work for space.
- **Static coordinate order versus computed topological order:** loops are cheap when structure is regular; explicit ordering supports irregular DAGs at preprocessing cost.
- **Scalar order versus wavefront parallelism:** a simple order minimizes coordination; independent ranks can expose parallel work but require deterministic aggregation.
- **Exact array size versus overallocated rectangle:** exact domains save cells; simple rectangles can make indexing and vectorization cheaper.
- **Precompute versus lazy extension:** precomputation makes query latency predictable; lazy computation avoids work before demand is known.
- **Local versus remote memo:** local lookup is fast and process-scoped; remote reuse adds network, schema, authorization, and failure costs.
- **One evaluator versus measured portfolio:** one path is easier to verify; a portfolio can fit varied densities if selection and fallback remain governed.
- **Value equality versus witness equality:** several optimal witnesses may share a value; APIs demanding determinism require a common total tie order.

## Failure Modes and Misconceptions

1. **Cache defines DP:** storing results is mistaken for designing a sufficient state recurrence.
2. **Recurrence drift:** top-down and bottom-up branches, bases, or ties differ subtly.
3. **Truthy membership:** zero, false, empty, or impossible results are repeatedly evaluated.
4. **Null collision:** missing, impossible, and a valid null result share one sentinel.
5. **Incomplete key:** graph, data version, mode, locale, tenant, or objective is omitted.
6. **Mutable key:** equality or hash changes after insertion, or aliased input mutates behind the cache.
7. **Identity reuse:** an address or short identifier denotes a different input later.
8. **Impure memo target:** time, randomness, I/O, state mutation, or per-call effects are frozen or skipped.
9. **Partial publication:** another caller reads a value before all dependencies and validation complete.
10. **Cached transient failure:** timeout or cancellation becomes a durable domain answer.
11. **Unmarked recursion:** a dependency cycle recurses until stack exhaustion.
12. **Long-chain stack:** an acyclic recurrence has depth beyond runtime limits.
13. **Wrong table order:** a consumer reads an uninitialized or stale predecessor.
14. **Zero initialization mask:** default numeric zero hides order or base errors.
15. **Nonclosed domain:** a restricted table excludes a required predecessor.
16. **Dense sparse-workload table:** most allocated and evaluated cells never contribute to a query.
17. **Sparse high-overhead map:** nearly every state is needed, but hashing and allocation dominate.
18. **Ascending 0/1 update:** a newly written capacity value reuses the same item.
19. **Descending unbounded update:** legal repeated use is accidentally prevented.
20. **Unproved rolling window:** an overwritten layer still has a future consumer.
21. **Lost witness:** compressed values cannot reproduce required actions or identities.
22. **Tie drift:** reconstruction chooses a different equal branch from evaluation.
23. **Hit-rate worship:** a ratio is optimized without miss cost, query latency, or useful-state coverage.
24. **Warm/cold asymmetry:** one implementation receives precomputed entries in a benchmark.
25. **Eviction-blind bound:** once-per-state complexity is claimed for a cache that discards states.
26. **Thread-safe means single-flight:** coherent map updates are assumed to prevent duplicate function calls.
27. **Lock-held recursion:** dependency evaluation under a broad cache lock deadlocks or serializes all keys.
28. **Cross-boundary reuse:** shared results leak data or decisions across authorization contexts.
29. **Unchecked allocation:** dimension products overflow or exceed process/tenant memory.
30. **Remote cache fantasy:** serialization, network, corruption, and version migration are treated as free.
31. **Oracle echo:** the test oracle repeats the same recurrence and order.
32. **Final-answer-only testing:** internal state, parents, cache isolation, and complexity regress while one output remains correct.

## Worked Examples

### Example 1

**Question:** How much repeated work does naive Fibonacci recursion perform at $n=10$?

**Reasoning:** The call recurrence is $C(0)=C(1)=1$ and $C(n)=1+C(n-1)+C(n-2)$. It yields $C(2)=3$, $C(3)=5$, $C(4)=9$, $C(5)=15$, and eventually $C(10)=177$. Memoization has 11 misses for states 0 through 10 and eight hits among 19 calls.

**Conclusion:** Memoization collapses repeated computation-tree nodes into recurrence states; it does not change Fibonacci semantics.

### Example 2

**Question:** Why does the executable memo evaluate eight states while tabulation evaluates twelve?

**Reasoning:** Vertex 7's transitive predecessors are exactly 0 through 7. The second source component, vertices 8 through 11, belongs to the declared bottom-up domain but has no path into 7. Demand follows only query dependencies; the full pass visits every declared vertex.

**Conclusion:** Work depends on $R(q)$ versus $T$, not on the labels “top-down” and “bottom-up” alone.

### Example 3

**Question:** What is wrong with returning a cached value only when it is truthy?

**Reasoning:** Suppose a minimization state has exact value zero. A lookup finds zero, treats it as absence, and recomputes the entire descendant closure. The final value may remain correct, hiding the broken once-per-state bound. If false or empty is a meaningful witness, behavior can also change.

**Conclusion:** Test membership or a private missing sentinel, never the truth value of cached data.

### Example 4

**Question:** Can two immutable problem instances share a memo keyed only by $(i,b)$?

**Reasoning:** Instance X may have item $i$ worth 10 while instance Y has it worth 2. Their coordinates collide but their recurrence values differ. A cache owned by each immutable instance is sound; a shared cache needs an instance/content version in the key.

**Conclusion:** A state coordinate is not automatically a complete cross-instance cache identity.

### Example 5

**Question:** Which order evaluates edit-distance state $D(i,j)$ from prefix bases?

**Reasoning:** Each interior cell reads $(i-1,j)$, $(i,j-1)$, and $(i-1,j-1)$. Increasing rows with an inner increasing-column loop places all three predecessors before $(i,j)$. Increasing $i+j$ wavefronts also work and expose independent cells on one diagonal.

**Conclusion:** A valid order comes from dependencies; several schedules can satisfy the same partial order.

### Example 6

**Question:** Why does capacity direction matter in one-row 0/1 knapsack?

**Reasoning:** Start $dp[0..4]=0$ and process one item of weight 2 and value 3. Ascending capacity writes $dp[2]=3$, then reads that new value to set $dp[4]=6$, using the item twice. Descending capacity sets $dp[4]=3$ from the old $dp[2]=0$, then $dp[2]=3$.

**Conclusion:** Descending capacity preserves the previous logical item layer; ascending capacity implements a different recurrence.

### Example 7

**Question:** Can edit-distance values use two rows while still returning an edit script?

**Reasoning:** Two rows preserve the dependencies needed for the distance value, but discarded cells no longer reveal the complete predecessor chain. Store parents, recompute selected regions, checkpoint, or use a justified divide-and-recompute construction.

**Conclusion:** Value liveness and witness liveness are different; the output contract determines usable compression.

### Example 8

**Question:** Is memoization safe for an acyclic chain of one million states?

**Reasoning:** It evaluates only one million required states, but ordinary recursive evaluation also creates active depth near one million. Caching eliminates no work because every state has one consumer, and the language stack will usually fail long before completion.

**Conclusion:** Use bottom-up order or an explicit heap-backed frame stack; state count alone does not bound call-stack safety.

### Example 9

**Question:** Does a thread-safe cache guarantee one computation for an expensive missing key?

**Reasoning:** Two threads can both miss before either publishes. Internal map invariants remain safe, yet the function runs twice. Current Python documentation, for example, explicitly permits this behavior for its cache wrapper.

**Conclusion:** Use per-key single-flight only when duplicate work matters, and specify failure/cancellation semantics for waiters.

### Example 10

**Question:** How should a service choose between a sparse memo and dense table?

**Reasoning:** Measure ancestor-closure density, query reuse, active depth, key/entry bytes, table bytes, miss and lookup costs, locality, witness storage, and cold/warm latency on representative batches. Validate both results and define hard allocation/stack limits before fitting a threshold.

**Conclusion:** Strategy selection is a governed workload decision, with an exact fallback—not a slogan about recursion versus loops.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns recursion, stack behavior, equality/hash contracts, purity, effects, exceptions, and runtime concurrency semantics.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns hash tables, arrays, bitsets, compact parents, cache policies, and representation overhead.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns memo groups, materialization, snapshot identity, invalidation, and property-aware plan caches.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns single-flight across workers, duplicate execution, distributed invalidation, consistency, and partial failure.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache locality, layout, bandwidth, vectorization, branch behavior, and working-set effects.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) owns thread stacks, virtual memory, allocation failure, synchronization, and process resource limits.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns cross-tenant isolation, cache poisoning, resource exhaustion, sensitive retention, and authorization-context keys.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns differential oracles, concurrency schedules, fault injection, benchmark fairness, and regression evidence.

## References

1. Richard Bellman. [“On the Theory of Dynamic Programming”](https://doi.org/10.1073/pnas.38.8.716), *Proceedings of the National Academy of Sciences* 38(8), 1952, pp. 716–719. Primary recurrence and multistage-decision foundation.
2. Donald Michie. [“‘Memo’ Functions and Machine Learning”](https://doi.org/10.1038/218306c0), *Nature* 218, 1968, p. 306. Primary historical memo-function source.
3. Richard S. Bird. [“Tabulation Techniques for Recursive Programs”](https://doi.org/10.1145/356827.356831), *ACM Computing Surveys* 12(4), 1980, pp. 403–417. Systematic tabulation of recursive programs.
4. Arthur B. Kahn. [“Topological Sorting of Large Networks”](https://doi.org/10.1145/368996.369025), *Communications of the ACM* 5(11), 1962, pp. 558–562. Primary topological-ordering method.
5. Daniel S. Hirschberg. [“A Linear Space Algorithm for Computing Maximal Common Subsequences”](https://doi.org/10.1145/360825.360861), *Communications of the ACM* 18(6), 1975, pp. 341–343. Primary linear-space value and reconstruction trade-off.
6. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Dynamic-programming evaluation, reconstruction, and complexity foundations.
7. Python Software Foundation. [`functools` — Higher-order functions and operations on callable objects](https://docs.python.org/3/library/functools.html#functools.cache), Python 3.14 documentation; consulted 2026-09-04. Current documented cache retention, statistics, thread coherence, and possible duplicate calls.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/algorithms-and-complexity/), endorsed 2024; consulted 2026-09-04. Current curricular scope for dynamic programming, implementation, and evaluation.

## Exercises

### Exercise 1

Let $V(0)=0$, $V(1)=1$, and for $n\ge2$ let $V(n)=\min\{V(n-1)+2,V(n-2)+3\}$, breaking equal values in favor of the smaller predecessor index. Compute $V(0)$ through $V(5)$, trace a cold memoized query for $V(5)$, give misses, hits, and dependency attempts, and give a bottom-up order and correspondence argument.

### Exercise 2

A robot moves only right or down through cell-cost grid

$$
\begin{pmatrix}
1&4&2\\
3&\bot&1\\
5&2&1
\end{pmatrix},
$$

where $\bot$ is blocked and the start cell is charged. Define the minimum-cost recurrence, evaluate the table and one deterministic path using “top predecessor before left” on equal costs, specify a valid order, derive work and full value/parent space, and determine what rolling storage preserves or loses.

### Exercise 3

Diagnose and repair three independent implementation defects: a memo tests `if cache.get(state)` before reuse; a process-global cache key is only `(index, budget)` although item data and pricing policy can change; and one-row 0/1 knapsack scans capacity upward. State whether each defect threatens value correctness, complexity, isolation, or several of them, and give targeted tests.

### Exercise 4

A cold query has $|R(q)|=24{,}000$ states and 72,000 dependency edges. A dense predecessor-closed table has $|T|=2{,}000{,}000$ states and 6,000,000 edges. Model memo cost as 40 units per evaluated state plus 10 per examined edge and bottom-up cost as 5 per table state plus 3 per edge. A memo entry occupies 96 bytes; a dense value cell occupies 8 bytes, excluding equal witness storage. Compute work and value-storage estimates for the cold query. Then recompute the comparison when a query batch eventually reaches every table state and explain which unmodeled evidence can reverse the decision.

### Exercise 5

Design evaluation for an authorization-rule DAG used by a multi-tenant service. Rules depend on tenant, subject attributes, resource revision, policy revision, and request time bucket; a decision must return a deterministic explanation path. Specify recurrence/evaluation separation, keys and cache scope, cycle/failure/cancellation behavior, single-flight policy, bottom-up opportunity, witness retention, resource/security limits, telemetry, differential tests, and rollout criteria.

## Answers to the Exercises

### Answer 1

The values are

$$
\begin{aligned}
V(0)&=0,\\
V(1)&=1,\\
V(2)&=\min\{1+2,0+3\}=3,\\
V(3)&=\min\{3+2,1+3\}=4,\\
V(4)&=\min\{4+2,3+3\}=6,\\
V(5)&=\min\{6+2,4+3\}=7.
\end{aligned}
$$

At $V(2)$ and $V(4)$ the values tie, so the smaller predecessor indices 0 and 2 win respectively. A cold depth-first call to 5 reaches each state 0 through 5 once: six misses. Each nonbase state 2 through 5 examines two dependencies, so there are eight dependency attempts. Total memo calls are the initial call plus those attempts, nine; therefore hits are $9-6=3$.

The increasing order $0,1,2,3,4,5$ is bottom-up valid because every predecessor index is smaller. Bases agree. Assuming both evaluators agree below $n$, they pass the same two values to the same `min` and tie rule, so induction establishes equality through 5.

Value-only bottom-up storage needs the previous two values. Reconstructing the predecessor sequence requires parents, checkpoints, or deterministic recomputation.

### Answer 2

Let $c_{ij}$ be the cost of nonblocked cell $(i,j)$, and let $P(i,j)$ be minimum total cell cost from $(0,0)$ to $(i,j)$. Define $P(0,0)=c_{00}=1$, blocked or out-of-grid predecessors as $+\infty$, and otherwise

$$
P(i,j)=c_{ij}+\min\{P(i-1,j),P(i,j-1)\}.
$$

Use the stated top-before-left tie order. Increasing row then increasing column is valid. The table is

$$
\begin{pmatrix}
1&5&7\\
4&+\infty&8\\
9&11&9
\end{pmatrix}.
$$

The target cost is 9. Its parent is $(1,2)$, whose parent is $(0,2)$, then $(0,1)$, then $(0,0)$. Thus one path is

$$
(0,0),(0,1),(0,2),(1,2),(2,2).
$$

Every legal path to a nonstart cell ends from top or left, and replacing a nonminimum prefix preserves the final move, proving the recurrence. There are at most $mn$ states and two transitions per cell, so work is $O(mn)$. Full values and parents use $O(mn)$ cells.

Two value rows suffice because row $i$ reads only the current row's left cell and preceding row. One row can suffice with a carefully defined update and blocked sentinel. Neither retains the complete parent chain. For a path result, store parents, checkpoint/recompute, or use another proven reconstruction method; replay the path and sum original cell costs.

### Answer 3

The truthy lookup conflates absence with cached zero, false, or empty results. Repair it with membership, a private missing object, or a typed entry. It always threatens the once-per-state complexity claim and can threaten correctness if a falsey result carries meaning beyond recomputation. Test states whose valid results are zero, false, empty, and impossible; assert both answers and evaluation counts across repeat calls.

The coordinate-only global key conflates distinct inputs and policies. Scope a cache to one immutable item/policy snapshot or include stable dataset and policy revisions plus every other value-determining mode. This threatens correctness, tenant isolation, privacy, and determinism. Test identical coordinates across two datasets, two policy versions, tenants, mutation attempts, and deliberately reordered request sequences.

The ascending 0/1 scan reads values written for the current item and permits reuse. Scan capacity from $B$ down to $w_i$. This changes value correctness, not merely speed. A single item $(w=2,v=3)$ at capacity 4 is a minimal regression: correct 0/1 value is 3, while the faulty ascending pass returns 6. Also compare every small instance with subset enumeration.

### Answer 4

For the sparse cold query, modeled memo work is

$$
24{,}000\cdot40+72{,}000\cdot10
=960{,}000+720{,}000
=1{,}680{,}000
$$

units. Dense bottom-up work is

$$
2{,}000{,}000\cdot5+6{,}000{,}000\cdot3
=10{,}000{,}000+18{,}000{,}000
=28{,}000{,}000
$$

units. Memo value storage is

$$
24{,}000\cdot96=2{,}304{,}000\text{ bytes},
$$

while dense values occupy

$$
2{,}000{,}000\cdot8=16{,}000{,}000\text{ bytes}.
$$

Under this model, memoization wins the cold sparse query.

If the batch eventually reaches every table state and the memo retains them, modeled memo work becomes

$$
2{,}000{,}000\cdot40+6{,}000{,}000\cdot10
=140{,}000{,}000
$$

units and entries occupy 192,000,000 bytes. The dense pass remains 28,000,000 units and 16,000,000 value bytes, so tabulation wins this saturated model.

The decision can reverse with cache reuse, eviction/recomputation, initialization frequency, irregular transition cost, key size, hash collisions, array index mapping, parent bytes, rolling storage, active stack, locality, parallelism, allocation overhead, remote lookups, and latency distributions. Benchmark equivalent semantics under declared cold/warm query batches and verify every result.

### Answer 5

Define the rule recurrence independently of evaluation: each rule combines typed predecessor decisions into allow, deny, or not-applicable plus a deterministically ordered explanation choice. Reject policy graphs with cycles at publication, and retain an active marker as defense during demand evaluation.

Use a per-request memo for request-specific values. A complete key includes tenant, canonical rule identity, subject-attribute snapshot or revision, resource identity and revision, policy revision, time bucket with declared boundary semantics, evaluation mode, and any feature/configuration version. Do not place raw secrets in observable keys or logs. Cross-request reuse is allowed only for inputs whose snapshots and authorization scope match exactly, with bounded retention and version-driven invalidation.

On a miss, publish a per-key in-progress handle without holding a broad lock during dependency evaluation. One producer computes; compatible waiters share success. Producer exception, timeout, cancellation, and resource rejection become typed evaluation failures, wake waiters, and remove or expire the active handle according to retry policy. One waiter's cancellation does not cancel a producer still needed by others unless ownership rules explicitly permit it.

Bottom-up evaluation is attractive when a published policy revision is an immutable DAG and a batch evaluates many roots or subjects. Precompute a topological rule order, but do not precompute subject/resource-dependent decisions without their complete context. A hybrid can validate/order the static graph once and memoize request-specific values on demand.

Store the chosen predecessor/action or a compact explanation node with stable global identities and the same tie order as the value. Replay the explanation against the exact policy and attribute revisions before returning it. Limit graph nodes, fan-out, depth, key/entry bytes, explanation length, concurrent producers, total work, and tenant cache share. Use checked counters and privacy-safe telemetry.

Record misses, hits, duplicate producers prevented, waits, wait latency, evaluated rules, dependency attempts, maximum depth, cycles rejected, cancellations, failures by type, evictions, bytes, policy/input revisions, decision latency, and replay failures. Never log protected attribute values indiscriminately.

Differential tests enumerate small rule DAGs and attribute assignments with an independent direct interpreter, then compare memoized and topological values and explanations under permuted dependency order. Add cross-tenant collision tests, revision changes, time-bucket boundaries, cycles, producer failure, waiter cancellation, eviction, concurrency schedules, overflow/resource limits, and stale-entry injection.

Roll out in shadow mode against the existing evaluator on versioned snapshots, require zero unexplained decision or witness mismatches, enforce latency/memory/error budgets, canary by tenant cohort, and keep a deterministic rollback. Performance improvement alone cannot authorize release when isolation or decision correspondence is unproven.
