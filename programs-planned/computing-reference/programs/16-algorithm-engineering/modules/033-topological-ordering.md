---
module_id: ALGE-033
program: Algorithm Engineering
level: 1
module_number: 33
title: Topological Ordering
status: complete
last_verified: 2026-09-05
---

# Topological Ordering

## One-Page Review

### Governing question

Given directed precedence constraints, how can we either produce a linear order that respects every constraint or return trustworthy evidence that no such order exists, while making tie-breaking, graph identity, failure, and execution semantics explicit?

### Essential definitions

- A **directed acyclic graph** (DAG) is a finite directed graph with no directed cycle.
- A **topological order** is a permutation of all vertices in which every edge $u\to v$ places $u$ before $v$.
- A **linear extension** is a total order consistent with a partial order; a topological order linearly extends the reachability relation of a DAG.
- A vertex is **ready** when its current number of unprocessed predecessors is zero.
- **Kahn's algorithm** repeatedly removes a ready vertex and decreases the remaining indegree of its successors.
- The **DFS method** emits vertices in decreasing finish time after certifying that no back edge exists.
- A **tie policy** chooses among simultaneously ready vertices; it affects reproducibility but not validity.
- A **cycle witness** is a directed closed walk, preferably reduced to a simple directed cycle, whose edges can be checked against the input.
- A **rank map** sends each vertex to its position in the returned order.
- A **ready batch** is an antichain of vertices whose declared predecessors have all completed at the moment the batch is released.

### Central model, mechanism, or theorem

For a finite directed graph $G=(V,E)$, a topological order exists if and only if $G$ is acyclic.

Kahn's invariant partitions vertices into emitted $P$, ready $R$, and blocked $B$. For every unprocessed vertex $v$,

$$
d^-_{\mathrm{rem}}(v)=|\{u\in V\setminus P:(u,v)\in E\}|.
$$

Thus $R=\{v\in V\setminus P:d^-_{\mathrm{rem}}(v)=0\}$. Emitting any $v\in R$ is safe because every predecessor is already in $P$. If all vertices are emitted, the result is valid. If unprocessed vertices remain and $R$ is empty, their induced subgraph has minimum indegree at least one; repeatedly following predecessors in this finite subgraph must revisit a vertex and therefore exposes a directed cycle.

With adjacency lists, exact vertex membership, and each logical edge processed once, construction and ordering take $\Theta(|V|+|E|)$ work. A binary heap adds deterministic minimum-key selection at $O((|V|+|E|)\log |V|)$ worst-case time; an ordered integer bucket or specialized queue may give other bounds.

### Critical invariants

- The graph is directed, finite, and bound to one immutable or versioned snapshot.
- Every edge endpoint belongs to the declared vertex universe; isolated vertices are included.
- Parallel input records are either distinct constraints or deliberately coalesced before indegree is counted.
- Remaining indegree equals the number of incoming edges from unprocessed vertices.
- A vertex enters the ready set exactly when that count reaches zero and is emitted exactly once.
- Every emitted vertex has all declared predecessors earlier in the output.
- The output is complete only when it contains every vertex exactly once.
- Failure returns verifiable residual or cycle evidence, not a partial order mislabeled as success.
- Tie-breaking, edge orientation, self-loop policy, and graph version are part of the observable contract.
- Ready-for-ordering is not the same as safe-to-execute when resources, failures, side effects, or undeclared dependencies exist.

### Common failures

Frequent failures include reversing dependency edges; omitting isolated or predecessor-only vertices; counting a duplicated edge twice but decrementing once; using an unordered set while promising reproducibility; confusing one valid order with the unique order; publishing a prefix after a cycle; treating a self-loop as harmless; mutating dependencies during traversal; overflowing a narrow indegree counter; deriving execution batches by merely slicing a sequential order; releasing successors when work is dispatched rather than completed; interpreting ordering as a schedule with resource guarantees; and deleting a dependency solely to make a cycle disappear.

### Compact example

Let $V=\{a,b,c,d\}$ and $E=\{a\to c,b\to c,c\to d\}$. Initially $a$ and $b$ are ready. Choosing $a$ then $b$ yields $(a,b,c,d)$; choosing $b$ then $a$ yields $(b,a,c,d)$. Both are valid because neither $a$ nor $b$ reaches the other. Adding $d\to a$ blocks every vertex after no initial emission and gives the checkable cycle $a\to c\to d\to a$.

### Connections

[ALGE-002](./002-preconditions-postconditions-and-correctness.md) supplies contract reasoning, [ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies invariant proofs, [ALGE-005](./005-asymptotic-time-and-space.md) supplies cost analysis, [ALGE-031](./031-breadth-first-search.md) supplies queue-frontier reasoning, and [ALGE-032](./032-depth-first-search.md) supplies colors, finish times, and back-edge cycle evidence. [ALGE-034](../ROADMAP.md#block-04--graph-algorithms) next turns ordering failures into strongly connected components.

## Governing Question

How should an algorithm transform a set of directed precedence constraints into a complete, deterministic, auditable order—or prove that this is impossible—without confusing a graph order with a production execution schedule?

The mathematical problem is compact. Input is a finite directed graph. Output is a permutation that places every tail before every head, or evidence that a directed cycle prevents such a permutation. The engineering problem is wider: callers disagree about whether an edge means “depends on,” “must precede,” or “is consumed by”; graph containers may omit isolated vertices; duplicates can corrupt counts; multiple valid answers complicate builds and tests; and a useful failure must identify constraints that people can repair.

Topological ordering is not numerical sorting. Vertex names need no natural order for validity. A secondary order is a policy for choosing among incomparable vertices. Nor is topological order automatically a schedule. It expresses logical precedence, not duration, worker capacity, locks, memory, deadlines, retries, or side-effect safety.

## Why This Matters

Dependency order appears in compilation, package installation, database migration, spreadsheet recalculation, workflow engines, configuration rollout, static initialization, course prerequisites, build systems, and data pipelines. In each case, consuming an artifact before its prerequisite can produce failure or, worse, a plausible but stale result.

The theorem “a finite digraph is topologically orderable exactly when it is acyclic” gives both an algorithm and a diagnostic boundary. A successful order is a compact certificate checked in one edge scan. A rejected graph should carry a cycle witness, because “processed 8,431 of 8,500 nodes” does not identify the contradictory constraints.

Multiple valid orders are often desirable: they expose concurrency. They also create nondeterminism unless a tie policy is specified. Reproducible tools commonly select the least stable identifier, preserve manifest insertion order, or return ready batches. Each policy changes the exact result and sometimes cost, but never the defining edge constraint.

The foundational algorithms remain stable. What changes in current libraries is lifecycle behavior. Python 3.14's `graphlib.TopologicalSorter`, for example, accepts a predecessor mapping, exposes ready/done batches for parallel coordination, documents insertion-sensitive ordering, and now permits repeated `prepare()` calls before sorting starts. These are API facts, not new graph theorems.

## Prerequisites and Retrieval

Retrieve:

- finite directed graphs, vertices, edges, paths, directed cycles, self-loops, and induced subgraphs;
- adjacency lists, reverse adjacency, indegree, queues, stacks, heaps, maps, sets, and integer counters;
- permutations, total orders, partial orders, antichains, and reachability;
- loop invariants, induction, proof by contradiction, and the pigeonhole principle;
- asymptotic work and space, sparse versus dense representations, and output-sensitive cost;
- DFS discovery and finish events, gray ancestors, back edges, and reverse postorder;
- immutable snapshots, stable identifiers, overflow checks, cancellation, atomic publication, and error witnesses;
- task dispatch, task completion, resource scheduling, retries, idempotence, and failure propagation.

You should be able to distinguish an edge $u\to v$ from the statement “$u$ stores $v$ as a predecessor.” Many real defects begin by silently reversing that interpretation.

## Learning Objectives

After completing this module, you should be able to:

1. specify the vertex universe, edge orientation, multiplicity, tie policy, snapshot, output, and failure evidence for a topological-ordering contract;
2. prove that a finite digraph admits a topological order exactly when it is acyclic;
3. derive Kahn's remaining-indegree invariant and its success and failure conditions;
4. derive the DFS reverse-finish method and explain why a back edge invalidates its output;
5. implement deterministic ordering, rank validation, ready batches, and cycle-witness extraction;
6. analyze adjacency-list, matrix, heap, output, and counter-storage costs;
7. characterize uniqueness and show why one moment with multiple choices certifies non-uniqueness;
8. handle isolated vertices, self-loops, parallel records, disconnected components, cancellation, and mutation;
9. separate logical precedence from execution readiness, resource feasibility, and operational success;
10. design property, differential, metamorphic, and fault-injection tests for an ordering service.

## Core Exposition

### Specify the effective precedence graph

Declare the complete vertex set $V$ independently of edges. An edge list alone cannot represent an isolated vertex. Decide whether an edge $u\to v$ means “$u$ must precede $v$” or whether the input maps each task to its predecessors. Normalize exactly once at the boundary and use one internal orientation.

Also declare:

- whether parallel edge records are meaningful constraints or duplicate data;
- whether self-loops are permitted as input and, if so, reported as one-edge cycles;
- whether unknown endpoints are rejected or implicitly create vertices;
- how vertex identity and stable tie keys are computed;
- whether ordering covers the whole graph or a named induced subgraph;
- which immutable snapshot or graph revision is being ordered;
- whether failure returns one cycle, all cyclic components, or only residual vertices;
- whether the caller needs one order, a canonical order, all orders, ranks, or ready batches.

“Dependency graph” is ambiguous. Suppose a mapping contains `deploy: {package}`. Its natural meaning is predecessor `package` with precedence edge `package -> deploy`. Feeding the mapping as outgoing adjacency reverses the constraint. Name APIs `predecessors_by_task` or `successors_by_task`, not merely `graph`.

### Establish the existence theorem

**Theorem.** A finite directed graph has a topological order if and only if it has no directed cycle.

For the forward direction, assume positions $r(v)$ form a topological order. Every cycle edge requires a strict increase:

$$
r(v_0)<r(v_1)<\cdots<r(v_{k-1})<r(v_0),
$$

which is impossible. Therefore an order excludes cycles.

For the reverse direction, first prove a lemma: every finite DAG has a vertex of indegree zero. If every vertex had a predecessor, start at any vertex and repeatedly choose a predecessor. Finiteness forces a repeated vertex, and the edges followed between repetitions form a directed cycle, contradicting acyclicity. Remove one zero-indegree vertex. Removing vertices and incident edges cannot create a cycle, so the remaining graph is a DAG. Induction on $|V|$ produces an order; prepend the removed vertex.

This proof already contains Kahn's mechanism. It also identifies where finiteness matters. An infinite acyclic graph can have every vertex possess a predecessor—for example integers with edge $i-1\to i$—and need not have a first element in the desired order.

### Derive Kahn's algorithm

Compute initial indegree for every vertex, including zeros. Put every zero-indegree vertex into a ready container. Repeatedly:

1. choose and remove one ready vertex $u$;
2. append $u$ to the output;
3. for each outgoing logical edge $u\to v$, decrement $v$'s remaining indegree;
4. when the count becomes zero, insert $v$ into the ready container.

If the output contains $|V|$ vertices, return it. Otherwise reject the graph as cyclic and extract a witness from the unprocessed subgraph.

The ready container implements policy:

- a FIFO queue gives linear work and order determined by initial and adjacency insertion order;
- a LIFO stack gives another valid order;
- a min-heap gives the lexicographically least topological order under the declared key;
- a batch set exposes all currently ready work but needs a stable order for deterministic serialization;
- a priority queue can encode legitimate business priority, provided precedence still dominates it.

The lexicographically least claim follows greedily. At the first position where another valid order differs, it selects some ready key $y$ while the heap algorithm selects the smaller ready key $x$. Since $x$ was ready, selecting it cannot violate any constraint; replacing $y$ with $x$ gives a smaller valid prefix. Thus no valid order is lexicographically smaller.

### Maintain the remaining-indegree invariant

Let $P$ be the emitted set. Define

$$
\operatorname{rem}(v)=|\{(u,v)\in E:u\notin P\}|,
\qquad v\notin P.
$$

Initially $P=\varnothing$, so counted indegree equals `rem`. When $u$ is emitted, exactly its outgoing edges cease to originate outside $P$; decrementing each corresponding successor once restores the equation. No other count changes. By induction, the invariant holds at every iteration.

If `rem(v) = 0`, every predecessor of $v$ is in $P$, so appending $v$ preserves every edge constraint. A vertex is enqueued only on the transition from one to zero, so exact edge accounting yields at-most-once readiness. Popping once yields at-most-once emission.

If the algorithm stops with unprocessed set $U$, every $v\in U$ has positive indegree within $G[U]$. Repeatedly following an incoming edge in $U$ must revisit a vertex, producing a cycle. The entire residual is not necessarily cyclic: vertices downstream of a cycle also remain blocked. Therefore return residual membership as diagnostic context, not as a claim that every residual vertex lies on a cycle.

### Implement deterministic ordering and cycle evidence

This implementation accepts a complete vertex iterable and precedence-oriented edges, coalesces duplicate records, uses a heap for stable minimum-key choices, validates successful ranks, and extracts a deterministic cycle from Kahn's residual graph.

<!-- bijux-verify: {"id":"deterministic-topological-order","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"order=('docs', 'fetch', 'lint', 'parse', 'compile', 'package', 'deploy')\nlayers=(('docs', 'fetch', 'lint'), ('parse',), ('compile',), ('package',), ('deploy',))\nvalid=True\ncycle=('a', 'b', 'c', 'a')\n","stderr":""}} -->
```python
from dataclasses import dataclass
import heapq


@dataclass(frozen=True)
class CycleDetected(ValueError):
    witness: tuple[str, ...]


def normalize(vertices, edges):
    vertices = set(vertices)
    successors = {vertex: set() for vertex in vertices}
    for tail, head in edges:
        if tail not in vertices or head not in vertices:
            raise ValueError(f"unknown endpoint: {(tail, head)}")
        successors[tail].add(head)
    return {vertex: tuple(sorted(heads))
            for vertex, heads in successors.items()}


def find_cycle(successors, residual):
    color = {vertex: 0 for vertex in residual}
    parent = {}
    for root in sorted(residual):
        if color[root] != 0:
            continue
        color[root] = 1
        stack = [(root, 0)]
        while stack:
            vertex, index = stack[-1]
            neighbors = tuple(
                head for head in successors[vertex] if head in residual
            )
            if index == len(neighbors):
                color[vertex] = 2
                stack.pop()
                continue
            head = neighbors[index]
            stack[-1] = (vertex, index + 1)
            if color[head] == 0:
                parent[head] = vertex
                color[head] = 1
                stack.append((head, 0))
            elif color[head] == 1:
                path = [vertex]
                while path[-1] != head:
                    path.append(parent[path[-1]])
                return tuple(reversed(path)) + (head,)
    raise AssertionError("a finite blocked residual must contain a cycle")


def topological_order(vertices, edges):
    successors = normalize(vertices, edges)
    indegree = {vertex: 0 for vertex in successors}
    for heads in successors.values():
        for head in heads:
            indegree[head] += 1
    ready = [vertex for vertex, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        vertex = heapq.heappop(ready)
        order.append(vertex)
        for head in successors[vertex]:
            indegree[head] -= 1
            if indegree[head] == 0:
                heapq.heappush(ready, head)
    if len(order) != len(successors):
        residual = {vertex for vertex, degree in indegree.items() if degree > 0}
        raise CycleDetected(find_cycle(successors, residual))
    return tuple(order)


def ready_layers(vertices, edges):
    successors = normalize(vertices, edges)
    indegree = {vertex: 0 for vertex in successors}
    for heads in successors.values():
        for head in heads:
            indegree[head] += 1
    ready = tuple(sorted(v for v, degree in indegree.items() if degree == 0))
    layers = []
    emitted = 0
    while ready:
        layers.append(ready)
        emitted += len(ready)
        newly_ready = []
        for vertex in ready:
            for head in successors[vertex]:
                indegree[head] -= 1
                if indegree[head] == 0:
                    newly_ready.append(head)
        ready = tuple(sorted(newly_ready))
    if emitted != len(successors):
        residual = {vertex for vertex, degree in indegree.items() if degree > 0}
        raise CycleDetected(find_cycle(successors, residual))
    return tuple(layers)


def valid_order(vertices, edges, order):
    vertices = set(vertices)
    if len(order) != len(vertices) or set(order) != vertices:
        return False
    rank = {vertex: index for index, vertex in enumerate(order)}
    return all(rank[tail] < rank[head] for tail, head in set(edges))


vertices = {"fetch", "parse", "compile", "lint", "package", "deploy", "docs"}
edges = {
    ("fetch", "parse"),
    ("parse", "compile"),
    ("compile", "package"),
    ("lint", "package"),
    ("package", "deploy"),
}
order = topological_order(vertices, edges)
print(f"order={order}")
print(f"layers={ready_layers(vertices, edges)}")
print(f"valid={valid_order(vertices, edges, order)}")

try:
    topological_order({"a", "b", "c", "tail"},
                      {("a", "b"), ("b", "c"), ("c", "a"), ("c", "tail")})
except CycleDetected as error:
    print(f"cycle={error.witness}")
```

The code's coalescing policy is intentional: duplicate edge records denote one logical constraint. A system in which parallel edges are separately owned obligations may retain multiplicity, but then every retained record must increment and later decrement exactly once. The cycle extractor traverses only the residual and returns consecutive input edges with the first vertex repeated.

### Derive the DFS method

Run a complete DFS with white, gray, and black states. Encountering an edge to a gray ancestor produces a directed cycle witness, so reject. Otherwise prepend each vertex when it finishes, or reverse the final finish list.

For every edge $u\to v$ in a DAG, $f(u)>f(v)$. If DFS discovers $v$ from $u$, $v$ finishes before $u$. If $v$ was already discovered, it cannot be gray because that would make $u\to v$ a back edge and a cycle; if black, it already finished. Therefore decreasing finish time places $u$ before $v$.

DFS and Kahn both take $\Theta(n+m)$ work with adjacency lists. Their evidence differs. DFS naturally returns a back-edge cycle and postorder. Kahn naturally exposes ready sets, ranks, processed prefixes, and a blocked residual. Recursive DFS risks call-stack overflow; explicit DFS frames avoid that risk but must preserve neighbor position and color semantics. Kahn stores indegrees and a ready container.

Do not reverse DFS finish times unless cycle detection completed successfully. Reverse postorder of a cyclic graph is a permutation, but it violates at least one edge and is not a topological order.

### Validate an order independently

Given candidate sequence $L$, check:

1. `len(L) == |V|`;
2. every declared vertex appears exactly once;
3. no unknown vertex appears;
4. construct rank $r(L_i)=i$;
5. verify $r(u)<r(v)$ for every logical edge $u\to v$.

This costs $\Theta(n+m)$ time and $\Theta(n)$ rank space. Validation should use the same normalized edge semantics and snapshot identifier as generation, but an independently implemented parser or representation catches more defect classes.

A valid order certifies acyclicity: a cycle would imply a strict rank increase back to its starting vertex. It does not prove that the graph contains every dependency the domain requires. Missing constraints are a data-quality problem outside the graph theorem.

For a failure witness $(v_0,v_1,\ldots,v_k)$, check $k\ge1$, $v_0=v_k$, and $(v_i,v_{i+1})\in E$ for every $0\le i<k$. Remove repeated interior segments if the contract promises a simple cycle. Bind the witness to the graph digest or revision.

### Determine whether the order is unique

A finite DAG has a unique topological order exactly when Kahn's ready set has size one at every step. If two distinct vertices $a$ and $b$ are ready together, choosing $a$ first or $b$ first yields two valid completions, so uniqueness fails. Conversely, one choice at every step forces every position.

Equivalently, a returned order $(v_1,\ldots,v_n)$ is unique exactly when every consecutive pair has edge $v_i\to v_{i+1}$. If that edge is missing, the pair is incomparable at the relevant point and can be swapped in some linear extension. This criterion is about logical edges, not merely transitive reachability data that was omitted from storage.

Uniqueness is rarely necessary for execution. A non-unique order may be a useful signal that work can proceed concurrently. Requiring uniqueness can also reveal an under-specified policy when a pipeline expected a single canonical sequence.

### Produce ready batches without inventing precedence

Kahn's current ready set is an antichain: no ready vertex can reach another ready vertex, because a path into the latter would leave an unprocessed predecessor. Removing an entire ready set at once produces layers. Each layer can begin only after all prior layers have logically completed.

These layers are not necessarily a minimum-time schedule under varied durations or bounded workers. They ignore CPU, memory, licenses, locks, locality, affinity, deadlines, and preemption. They also impose a barrier between layers: a successor of a fast task in one batch might be ready before an unrelated slow task in the same batch finishes. An asynchronous ready/done coordinator exposes more concurrency.

Crucially, decrement successors on **completion**, not dispatch, if edges mean “requires successful result.” On failure, apply an explicit policy: block descendants, retry, substitute a cached result, or compensate. Topological logic alone does not define that policy.

### Account for representation and cost

Let $n=|V|$ and $m=|E|$ after normalization.

- Adjacency lists: indegree construction plus traversal is $\Theta(n+m)$ work and $\Theta(n+m)$ graph storage.
- Adjacency matrix: scanning successors of every emitted vertex costs $\Theta(n^2)$ even when few edges exist.
- FIFO ready queue: $\Theta(n+m)$ total work.
- Binary heap: $O((n+m)\log n)$ worst-case work under a simple bound, with at most one insertion per vertex after exact coalescing.
- Rank validation: $\Theta(n+m)$ work and $\Theta(n)$ auxiliary storage.
- Emitting every order: necessarily output-sensitive and potentially exponential in $n$.

Use counters wide enough for maximum normalized indegree. If there may be more incoming records than the counter represents, reject before overflow. Underflow during decrement proves mismatched edge accounting or duplicate emission. Treat it as corruption, not as readiness.

For external graphs, indegree aggregation may require partitioned counting, sorting, or durable key-value state. The graph theorem is unchanged, but I/O, recovery, duplicate delivery, and checkpoint protocols dominate. Exactly-once logical decrement can be implemented using idempotent edge identities or replayable state transitions; merely assuming exactly-once messaging is unsafe.

### Preserve determinism and identity

Validity allows any ready choice. Reproducibility requires more:

- stable vertex identifiers independent of memory addresses and hash randomization;
- a total, versioned tie key with explicit collation and byte encoding;
- normalized logical edges and endpoint identity;
- stable input snapshot and filter configuration;
- defined treatment of equal business priorities;
- recorded algorithm and policy version.

Insertion order is deterministic only if upstream construction order is deterministic and contractual. Lexicographic order is deterministic only if normalization, case folding, locale, and tie resolution are fixed. When identifiers can collide, compare a stable composite key or reject the input.

Canonical ordering can improve cache reuse, diff stability, and incident reproduction, but a heap adds cost. If consumers only need a valid rank, a queue may be preferable. Separate correctness from convenience: the edge validator accepts either.

### Handle change, cancellation, and publication

The proof concerns one graph. Adding an incoming edge after a vertex is emitted can invalidate the prefix; removing an edge can leave a vertex blocked after it should be ready. Bind vertex enumeration, edge enumeration, indegrees, ready state, output, and witness to one immutable snapshot or transactionally consistent revision.

General fully dynamic topological ordering is a different problem. For a small batch of changes, recomputing may be simpler and safer than maintaining ranks incrementally. An insertion $u\to v$ is immediately compatible when current $r(u)<r(v)$; otherwise it requires reachability and reordering work and may create a cycle. Do not patch ranks locally without a proved dynamic algorithm.

Cancellation yields a partial prefix, not a completed order and not cycle evidence. Record a distinct cancelled status and graph revision. A resumable checkpoint needs normalized graph identity, indegrees or processed set, ready-container contents with its ordering policy, output prefix, counter widths, and output sink position. Validate it before resuming.

Publish result status, order or witness, counts, tie policy, graph digest, and validation result atomically. Do not expose a “success” file before its rank certificate and metadata are durable.

### Test and operate the implementation

For small $n$, enumerate all permutations and compare the implementation with an independent edge predicate. Enumerate directed graphs through a bounded size and compare success with an independent cycle oracle. For successful cases, validate every edge. For rejected cases, validate every witness edge.

Useful metamorphic properties include:

- bijective vertex renaming preserves validity after mapping back;
- adding an isolated vertex adds one unconstrained position but changes no old edge relation;
- duplicating a record changes nothing under coalescing semantics;
- adding an edge already implied by reachability preserves the set of valid orders;
- adding a self-loop forces rejection with an immediate witness;
- reversing every edge reverses any valid order;
- permuting input records changes no canonical heap result;
- adding a new source can never make an existing DAG cyclic unless an edge returns to it.

Inject unknown endpoints, duplicate identities, counter overflow, underflow, iterator failure, allocation failure, cancellation after each emission, snapshot replacement, corrupt checkpoint state, and output failure. Differentially compare heap-Kahn, queue-Kahn, and DFS methods for validity, not exact equality unless tie policies match.

Observe vertex and normalized-edge counts, initial and maximum ready width, maximum indegree, heap or queue operations, residual size, witness length, normalization time, ordering time, validation time, memory, spill I/O, snapshot age, cancellations, retries, and publication failure. Large ready width suggests potential concurrency; it does not guarantee resource-feasible speedup.

## Definitions and Notation

Let $G=(V,E)$ be a finite directed graph, $n=|V|$, and $m=|E|$ after the declared normalization.

- A **directed path** is a sequence $(v_0,\ldots,v_k)$ with $(v_i,v_{i+1})\in E$.
- A **directed cycle** is a directed path with $k\ge1$, $v_0=v_k$, and no repeated interior vertex when simplicity is required.
- A **DAG** is a finite directed graph without a directed cycle.
- The **indegree** $d^-(v)$ is the number of incoming logical edges under the multiplicity policy.
- The **outdegree** $d^+(v)$ is the number of outgoing logical edges.
- A **topological order** $L=(v_1,\ldots,v_n)$ is a permutation of $V$ satisfying $(v_i,v_j)\in E\Rightarrow i<j$.
- A **rank map** $r:V\to\{0,\ldots,n-1\}$ is the inverse position map of $L$.
- The **processed prefix** $P$ is the set already emitted by Kahn's algorithm.
- The **remaining indegree** is $d^-_{\mathrm{rem}}(v)=|\{u\notin P:(u,v)\in E\}|$.
- The **ready set** is $R=\{v\notin P:d^-_{\mathrm{rem}}(v)=0\}$.
- The **residual** is the subgraph induced by $V\setminus P$ when progress stops.
- A **source** has indegree zero; a **sink** has outdegree zero.
- An **antichain** contains pairwise incomparable vertices under reachability.
- A **linear extension** is a total order that respects a partial order.
- A **tie policy** is the declared selection rule over $R$.
- A **canonical order** is the unique output chosen by a deterministic policy, not necessarily the DAG's unique topological order.
- A **cycle witness** is a checkable sequence of vertices and input edges proving impossibility.
- A **ready/done protocol** releases vertices only after all predecessors have been reported complete.
- A **snapshot binding** identifies the exact vertex and edge relation used by generation and validation.

The reachability relation $u\preceq v$ defined by $u=v$ or a directed path from $u$ to $v$ is a partial order exactly when the graph is acyclic: reflexivity and transitivity follow by construction, and antisymmetry fails precisely when distinct vertices reach one another.

## Mechanisms, Invariants, or Proof Structure

### Kahn loop obligations

Maintain these assertions before each selection:

1. `order` contains each vertex in $P$ exactly once.
2. Every edge whose head is in $P$ has its tail earlier in `order`.
3. For every $v\notin P$, the stored counter equals $d^-_{\mathrm{rem}}(v)$.
4. The ready container contains exactly the vertices outside $P$ with zero remaining indegree, subject to its documented returned/in-flight state.
5. No processed vertex remains ready and no vertex is emitted twice.
6. Graph identity, normalization, and tie policy remain unchanged.

Initialization follows from full indegree counting. Preservation follows because selecting a ready $u$ violates no incoming constraint and only edges out of $u$ change the remaining graph. The variant $n-|P|$ decreases by one, proving termination. At termination, $|P|=n$ proves success; otherwise an empty ready set plus the counter invariant proves a cyclic residual.

### DFS proof obligations

Maintain white-gray-black transitions, an exact active ancestor stack, complete adjacency processing, and finish timestamps. Reject on an edge to gray. If no such edge exists, prove $f(u)>f(v)$ for each edge $u\to v$; sorting by decreasing finish time then satisfies all ranks. Termination follows from finite vertices, one discovery per vertex, and finite adjacency.

### Certificate obligations

A success certificate contains every vertex once and satisfies every rank inequality. A failure certificate contains a closed directed sequence whose consecutive edges exist in the normalized input. These certificates are asymmetric: a rank map is globally linear-sized but simple to check; one cycle can be much smaller than the residual. Neither certifies that upstream dependency discovery was complete.

### Uniqueness obligations

Record ready-set cardinality before every selection. Cardinality greater than one supplies two distinct safe choices and hence two extensions. Cardinality exactly one throughout forces the emitted vertex at each position. Do not infer uniqueness merely because two implementations happened to return the same order.

## Alternatives and Trade-Offs

### Kahn versus DFS

Choose Kahn when clients need indegrees, ready batches, streaming prefixes, lexicographic selection, or completion coordination. Choose DFS when a traversal framework already produces reliable finish times and back-edge witnesses. Both are linear with adjacency lists absent ordered-selection overhead. Kahn avoids depth proportional call stacks; DFS avoids explicit reverse adjacency counts if outgoing adjacency already exists.

### FIFO versus heap versus batches

A FIFO queue minimizes overhead and preserves a documented discovery order. A heap provides a canonical least-key order at logarithmic selection cost. Ready batches expose concurrency and layered structure but may impose barriers if executed literally. A priority queue can incorporate policy, but priorities must never bypass incoming constraints.

### One order versus all orders

One order is linear-sized and enough for most consumers. Counting or enumerating all linear extensions is fundamentally different and can be intractable; output alone may be exponential. Avoid an API option such as `all=True` unless budgets, cancellation, and output semantics are explicit.

### Recompute versus dynamic maintenance

Recomputation is simple, independently verifiable, and often fast on moderate sparse graphs. Dynamic maintenance can reduce repeated work but adds complicated rank repair, reachability, concurrency, and recovery invariants. Choose it only from measured update rates and latency needs, not because recomputation seems inelegant.

### Canonicality versus throughput

Global least-key selection serializes a policy decision and can require coordination in distributed settings. Unordered ready batches permit throughput but make exact traces schedule-dependent. A practical system may store a valid rank plus stable per-batch ordering, or reserve canonical ordering for publication and use a separate runtime scheduler.

### Logical order versus scheduling

Topological ordering solves precedence feasibility. Critical-path scheduling adds durations; resource-constrained scheduling adds capacities; workflow execution adds failure and side-effect semantics. Keep these responsibilities separate. An excellent topological order can still be a poor schedule.

## Failure Modes and Misconceptions

- **Reversed edges:** interpreting `task -> prerequisites` as outgoing precedence runs dependents first. Normalize and test a two-vertex graph.
- **Missing vertices:** edge-derived enumeration drops isolated tasks. Accept a separate vertex universe.
- **Duplicate-accounting mismatch:** incrementing twice and decrementing once leaves a false cycle; coalesce or preserve multiplicity consistently.
- **Self-loop blindness:** $v\to v$ is a directed cycle and prevents any strict rank.
- **Prefix-as-success:** Kahn can emit acyclic vertices before reaching a blocked residual. The prefix is partial evidence, not a whole-graph order.
- **Residual-as-cycle:** vertices downstream of a cycle can be residual without belonging to any cycle. Extract actual witness edges.
- **Reverse-postorder without detection:** every digraph has a DFS finish sequence; only an acyclic one makes its reverse topological.
- **Assumed uniqueness:** deterministic output does not imply a unique mathematical order.
- **Hash-order determinism:** current iteration behavior is not a stable tie contract across construction paths, versions, or processes.
- **Rank-only validation:** checking edges without permutation completeness can accept an order that omits a difficult component.
- **Overflow and underflow:** narrow or corrupt counters can create premature readiness. Check bounds and decrement invariants.
- **Mutable snapshot:** concurrent edge insertion can invalidate an already published prefix.
- **Dispatch-as-completion:** releasing successors when a prerequisite merely starts violates result dependency.
- **Order-as-schedule:** precedence does not account for workers, memory, locks, durations, deadlines, or failures.
- **Cycle deletion as repair:** removing an edge restores acyclicity only if domain semantics allow that constraint to disappear.
- **All-orders surprise:** enumeration can produce exponential output and must be a separate budgeted operation.
- **Infinite-graph extrapolation:** the zero-indegree lemma and finite permutation contract rely on finiteness.
- **Opaque failure:** returning only `cycle detected` shifts graph forensics to the caller; return a verifiable witness and snapshot.

## Worked Examples

### Example 1

**Situation.** Order $V=\{a,b,c,d\}$ with edges $a\to c$, $b\to c$, and $c\to d$ using minimum-letter tie-breaking.

Initial indegrees are $d^-(a)=0$, $d^-(b)=0$, $d^-(c)=2$, and $d^-(d)=1$, so the heap contains $a,b$. Emit $a$; $c$ drops to one. Emit $b$; $c$ drops to zero. Emit $c$; $d$ becomes ready. Emit $d$. The rank inequalities are $0<2$, $1<2$, and $2<3$.

**Conclusion.** $(a,b,c,d)$ is the canonical minimum-letter order; $(b,a,c,d)$ is also valid, proving the DAG's order is not unique.

### Example 2

**Situation.** A course catalog contains courses `intro`, `systems`, and isolated `ethics`; the only constraint is `intro -> systems`. An implementation constructs vertices only from adjacency-map keys, where only `intro` is a key.

That representation emits `intro`, perhaps `systems` if heads are added implicitly, but cannot discover `ethics`. Even though its edge inequality passes, the output is not a permutation of the declared catalog. Supplying $V=\{\text{intro},\text{systems},\text{ethics}\}$ gives initial ready set `{ethics, intro}` and a complete three-course order.

**Conclusion.** Vertex completeness is independent of edge validity; accept or derive a declared universe that includes isolated and predecessor-only vertices.

### Example 3

**Situation.** Records contain the same logical constraint $a\to b$ twice. Indegree construction counts both records, but the successor container is a set and therefore decrements only once.

The stored initial indegree of $b$ is two. After emitting $a$, it becomes one, never enters ready state, and the algorithm falsely reports a cycle although the normalized graph is acyclic. Coalescing before both phases gives indegree one and one decrement. Preserving two parallel obligations also works if adjacency retains two identities and performs two decrements.

**Conclusion.** Multiplicity is a contract decision; increment and decrement must use the identical logical-edge representation.

### Example 4

**Situation.** Kahn's algorithm processes source $s$ in a graph with $a\to b$, $b\to c$, $c\to a$, and $c\to t$. It then stops with residual $\{a,b,c,t\}$.

Vertex $t$ is blocked because its predecessor $c$ remains, but $t$ has no path back to itself and is not on a cycle. DFS restricted to the residual discovers gray-edge $c\to a$ along active path $a,b,c$, yielding $a\to b\to c\to a$.

**Conclusion.** The residual localizes blocked work; the three-edge witness, not residual membership, proves the contradictory constraints.

### Example 5

**Situation.** DFS on edges $p\to r$, $q\to r$, and $r\to s$ explores roots in order $p,q,r,s$. It finishes $s$, then $r$, then $p$, and later finishes $q$.

One valid finish sequence is $(s,r,p,q)$, so decreasing finish time is $(q,p,r,s)$. Check: ranks satisfy $q<r$, $p<r$, and $r<s$. If edge $s\to p$ is added, DFS from $p$ sees gray ancestor $p$ from $s$; reverse finish output must be rejected.

**Conclusion.** Reverse finish time is a topological mechanism only when the same complete DFS certifies absence of back edges.

### Example 6

**Situation.** Decide whether edges $a\to c$, $b\to c$, and $c\to d$ have a unique topological order.

At the first Kahn step, ready set is $\{a,b\}$. Both choices are safe, giving prefixes $(a,b)$ and $(b,a)$ and complete orders $(a,b,c,d)$ and $(b,a,c,d)$. Adding $a\to b$ leaves only $a$ ready, then only $b$, $c$, and $d$. Every consecutive pair in $(a,b,c,d)$ now has a direct edge.

**Conclusion.** Multiple simultaneous ready vertices certify non-uniqueness; singleton readiness throughout certifies uniqueness.

### Example 7

**Situation.** Estimate storage for $n=50{,}000{,}000$ vertices when indegree uses unsigned 64-bit counters and rank uses unsigned 64-bit positions, excluding container overhead and adjacency.

Each array requires

$$
50{,}000{,}000\times 8=400{,}000{,}000\text{ bytes}.
$$

Together they require $800{,}000{,}000$ bytes, about $762.94$ MiB because $800{,}000{,}000/2^{20}\approx762.94$. A one-byte processed state adds $50{,}000{,}000$ bytes, for $850{,}000{,}000$ bytes before alignment and allocator overhead.

**Conclusion.** Linear auxiliary space can be operationally large; width, identifier layout, spill strategy, and whether ranks are retained deserve explicit budgets.

### Example 8

**Situation.** Tasks `compile` and `lint` are initially ready; `package` depends on both. A coordinator dispatches both, immediately marks both done, and releases `package`. Compilation then fails.

The produced dispatch order respects graph ranks, but execution violates the intended “requires successful output” semantics. Correct coordination records `compile` and `lint` as in flight, calls `done` only after success, and applies a failure policy to `package`. A topological sorter cannot infer retry or compensation behavior.

**Conclusion.** Logical readiness follows predecessor completion under the declared domain contract, not merely predecessor dispatch.

### Example 9

**Situation.** Validate candidate $(a,c,b)$ for $V=\{a,b,c\}$ and edges $a\to b$, $b\to c$.

Permutation checks pass: length is three and the set matches $V$. Ranks are $r(a)=0$, $r(c)=1$, $r(b)=2$. Edge $a\to b$ passes because $0<2$, but $b\to c$ fails because $2\not<1$. Candidate $(a,b,c)$ passes both. Candidate $(a,b)$ fails before edge scanning because it omits $c$.

**Conclusion.** Independent validation requires both permutation completeness and every edge inequality.

### Example 10

**Situation.** A migration plan has $A\to B$ and $B\to C$. While ordering snapshot 41, another transaction inserts $C\to A$ into revision 42. The service returns $(A,B,C)$ without recording a revision.

The order is valid for revision 41 and invalid for revision 42. Rechecking against “current” data produces inconsistent conclusions depending on timing. Snapshot-bound generation and validation would publish graph revision 41 with the order; revision 42 would separately return cycle $A\to B\to C\to A$.

**Conclusion.** Mutation does not make the theorem unreliable; it makes an unversioned result ambiguous. Bind every order or witness to one graph snapshot.

## Cross-Program Connections

- Data Structures Engineering owns queue, heap, adjacency, and counter representation invariants; Algorithm Engineering owns how these support ordering correctness and cost.
- Theory of Computation owns broader complexity classes and counting hardness; this module uses only the finite DAG existence theorem and output-sensitive warning.
- Software Architecture uses dependency directions and cycle diagnostics to reason about component boundaries, but architectural desirability is not implied by acyclicity.
- Software Delivery and Reliability Engineering applies ready/done graphs to builds and deployments, adding hermeticity, retries, rollout safety, and artifact identity.
- Database Engineering uses dependency orders for migrations and recovery actions, where transactions and snapshot rules define the effective graph.
- Data Engineering applies ordering to pipelines but must add data freshness, partition completion, backfills, and partial-failure semantics.
- Concurrent and Parallel Programming turns ready antichains into potential work, while synchronization and memory visibility determine safe execution.
- Distributed Systems adds partitioned ownership, duplicate delivery, durable completion, termination detection, and recovery.
- [ALGE-032](./032-depth-first-search.md) supplies DFS finish and back-edge mechanisms; [ALGE-034](../ROADMAP.md#block-04--graph-algorithms) will compress mutually reachable cyclic regions into strongly connected components for deeper diagnostics.

## References

1. A. B. Kahn, “Topological Sorting of Large Networks,” *Communications of the ACM* 5(11), 558–562, 1962, DOI [10.1145/368996.369025](https://doi.org/10.1145/368996.369025). Primary source for the removal-based method; publisher record checked 2026-09-05.
2. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, chapters 20–22. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
3. Robert Sedgewick and Kevin Wayne, *Algorithms*, 4th ed., Addison-Wesley, 2011, §4.2. [Author-maintained directed-graph material](https://algs4.cs.princeton.edu/42digraph/) and [topological API record](https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/Topological.html), checked 2026-09-05.
4. Jeff Erickson, *Algorithms*, 1st ed., 2019, graph-search chapters. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
5. Python Software Foundation, “`graphlib` — Functionality to operate with graph-like structures,” Python 3.14.7 documentation. [Official documentation](https://docs.python.org/3.14/library/graphlib.html), updated 2026-09-04 and checked 2026-09-05.
6. IEEE and The Open Group, *POSIX.1-2024*, `tsort` utility. [Official specification](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/tsort.html), checked 2026-09-05.
7. Donald E. Knuth, *The Art of Computer Programming, Volume 1: Fundamental Algorithms*, 3rd ed., Addison-Wesley, 1997, §2.2.3. [Official publisher record](https://www.informit.com/store/art-of-computer-programming-volume-1-fundamental-algorithms-9780201896831), checked 2026-09-05.
8. Jørgen Bang-Jensen and Gregory Gutin, *Digraphs: Theory, Algorithms and Applications*, 2nd ed., Springer, 2009. [Official DOI record](https://doi.org/10.1007/978-1-84800-998-1), checked 2026-09-05.

## Exercises

### Exercise 1

For $V=\{a,b,c,d,e\}$ and $E=\{a\to c,b\to c,b\to d,c\to e,d\to e\}$, list the initial indegrees, run minimum-letter Kahn ordering, and state whether the topological order is unique.

### Exercise 2

Prove that if a DAG has exactly one topological order $(v_1,\ldots,v_n)$, then every consecutive pair has edge $v_i\to v_{i+1}$. Prove the converse.

### Exercise 3

An implementation initializes indegree from a list containing two copies of $x\to y$, stores successors in a set, and reports a cycle after emitting $x$. Diagnose the violated invariant and give two correct representation policies.

### Exercise 4

Compare queue-based Kahn, heap-based Kahn, and explicit-frame DFS for a reproducible build planner with 20 million tasks, sparse edges, stable task IDs, a need for ready batches, and a requirement to return a cycle witness. Recommend a design and identify validation and memory evidence.

### Exercise 5

A distributed workflow snapshot contains tasks owned by several services. Dependencies may arrive twice, workers fail after completing side effects, and the graph can change between runs. Design an ordering and execution protocol that uses topological reasoning honestly. Specify graph identity, edge identity, readiness, completion, failure, recovery, certificate, and publication behavior.

## Answers to the Exercises

### Answer 1

Initial indegrees are

$$
d^-(a)=0,\quad d^-(b)=0,\quad d^-(c)=2,\quad d^-(d)=1,\quad d^-(e)=2.
$$

Ready heap begins $(a,b)$. Emit $a$, reducing $c$ to one. Emit $b$, reducing $c$ and $d$ to zero; heap now contains $c,d$. Emit $c$, reducing $e$ to one. Emit $d$, reducing $e$ to zero. Emit $e$. The minimum-letter result is $(a,b,c,d,e)$.

The order is not unique because the initial ready set contains both $a$ and $b$; $(b,a,c,d,e)$ is also valid. There is another choice between $c$ and $d$ after $b$, producing additional valid orders such as $(a,b,d,c,e)$.

### Answer 2

Assume the unique order is $(v_1,\ldots,v_n)$ and suppose some consecutive pair lacks edge $v_i\to v_{i+1}$. An edge $v_{i+1}\to v_i$ is impossible because it would contradict the given order. No path can run from $v_i$ to $v_{i+1}$ through another vertex, because every interior vertex of such a path would need a rank strictly between consecutive positions. Thus the pair is incomparable and swapping them preserves every edge constraint, producing a second topological order—a contradiction. Hence every consecutive edge exists.

Conversely, suppose every $v_i\to v_{i+1}$ exists. Transitivity gives a directed path from every earlier vertex to every later one. Any topological order must place $v_i$ before $v_{i+1}$ for each consecutive edge, forcing the entire sequence. Therefore the order is unique.

### Answer 3

Indegree says two unprocessed logical edges enter $y$, while successor traversal contains only one edge to remove. After $x$ is emitted, stored count becomes one although no unprocessed predecessor remains. This violates

$$
d^-_{\mathrm{rem}}(y)=|\{u\notin P:(u,y)\in E\}|.
$$

Policy one treats duplicate records as one constraint: coalesce the edge list before both indegree construction and adjacency construction. Policy two treats them as two owned obligations: retain both edge identities in adjacency, count both, and decrement both exactly once. In either policy, use the same normalized representation in generation and validation and treat counter underflow as corruption.

### Answer 4

Use Kahn's method because ready batches are a primary output. A FIFO queue minimizes work but does not guarantee a canonical result unless insertion and adjacency orders are stable. A heap keyed by stable task ID gives reproducible within-batch choices at logarithmic cost; for throughput, a hybrid can sort each newly ready batch while maintaining linear edge processing. Explicit-frame DFS can return a back-edge witness and valid reverse finish order, but it does not naturally drive the ready/done execution protocol.

The design should store compact wide indegrees, sparse outgoing adjacency, processed or in-flight state, and stable IDs; budget each array and container using measured width rather than only asymptotics. On blockage, run explicit DFS over the residual to extract a cycle. Validate successful output with permutation and rank-edge checks and validate every witness edge. Test duplicate semantics, isolated vertices, self-loops, counter bounds, record-order permutations, cancellation, and snapshot changes. Record graph digest, tie policy, task and edge counts, maximum ready width, peak bytes, runtime, and certificate result. A valid order does not by itself validate build hermeticity or worker scheduling.

### Answer 5

Take a transactionally consistent dependency snapshot and publish its revision or content digest. Give every task and logical dependency a stable identity; deduplicate repeated delivery by edge identity before indegree aggregation. Partition outgoing edges and counts durably, and make decrements idempotent with a processed-edge or committed predecessor-completion record.

Release a task only after all predecessor **success** records for that snapshot are durable. Dispatch changes it to in flight, not done. A worker uses an idempotency key or transactional side-effect protocol; after a crash, the coordinator reconciles the effect before retrying. Failure blocks descendants unless a versioned retry, substitute, skip, or compensation policy says otherwise. Checkpoints include graph revision, normalized counts, ready and in-flight tasks, completions, output ranks, and policy version.

If ordering blocks, extract and validate a cycle in the residual. If ordering succeeds, validate vertex completeness and every rank inequality. Execution produces a separate outcome ledger because successful ordering does not imply successful tasks. Atomically publish snapshot identity, ordering status, rank certificate or cycle witness, execution status, and limitations. A later graph revision gets a new run; it never silently changes the meaning of the existing certificate.
