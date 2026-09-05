---
module_id: ALGE-034
program: Algorithm Engineering
level: 1
module_number: 34
title: Strongly Connected Components
status: complete
last_verified: 2026-09-05
---

# Strongly Connected Components

## One-Page Review

### Governing question

How can we partition a directed graph into its maximal mutually reachable regions, prove that the quotient is acyclic, and implement the partition with trustworthy stack, transpose, identity, and snapshot semantics?

### Essential definitions

- Vertices $u$ and $v$ are **strongly connected** when each is reachable from the other.
- A **strongly connected component** (SCC) is a maximal set of pairwise strongly connected vertices.
- A one-vertex SCC needs no self-loop: length-zero reachability makes its vertex reachable from itself.
- The **condensation graph** contracts each SCC to one component vertex and retains edges between distinct components.
- The **transpose** $G^T$ reverses every directed edge while preserving all vertices.
- **Kosaraju–Sharir** uses DFS finish order and a second traversal on the transpose.
- **Tarjan's algorithm** uses one DFS, discovery indices, low-link values, and a stack of vertices not yet assigned to a component.
- A vertex is **on stack** only while its final SCC is unresolved; it may already be black in ordinary DFS terms.
- A **component map** assigns every vertex exactly one component identifier.
- A **component certificate** includes the partition, intercomponent edges, graph identity, and validation evidence.

### Central model, mechanism, or theorem

Mutual reachability is an equivalence relation, so its equivalence classes uniquely partition a finite directed graph. Contracting them yields a DAG. If the condensation had a cycle of distinct components

$$
C_0\to C_1\to\cdots\to C_{k-1}\to C_0,
$$

then every vertex in those components could reach every other through internal paths and cycle edges. Their union would be strongly connected, contradicting maximality.

Tarjan assigns each discovered vertex an index $\operatorname{idx}(v)$. For an unresolved vertex $v$, $\operatorname{low}(v)$ summarizes the earliest indexed unresolved vertex reachable through the explored DFS subtree under the algorithm's recurrence. After all outgoing edges of $v$ are processed,

$$
\operatorname{low}(v)=\operatorname{idx}(v)
$$

exactly when $v$ roots the next SCC to pop from the unresolved stack.

With adjacency lists, Kosaraju–Sharir, Tarjan, and Gabow-style path algorithms all achieve $\Theta(|V|+|E|)$ work and $\Theta(|V|)$ auxiliary state beyond the stored graph, subject to representation and transpose choices.

### Critical invariants

- The graph is directed, finite, and fixed to one snapshot throughout discovery, extraction, and validation.
- The declared vertex universe includes isolated, target-only, and source-only vertices.
- Every vertex belongs to exactly one output component; component labels themselves have no mathematical meaning.
- Every output component is internally mutually reachable and maximal.
- Transposition reverses every logical edge exactly once and preserves every vertex.
- Tarjan indices are unique and strictly increase at discovery.
- Tarjan's unresolved stack contains discovered vertices not yet assigned to a completed SCC.
- `on_stack` membership, not merely DFS color, governs non-tree low-link updates.
- A parent incorporates a tree child's low-link only after that child returns; if the child has already closed, its low-link cannot lower the parent's earlier index.
- When a root is detected, popping continues through that root, and every popped vertex is marked resolved exactly once.
- Condensation edges omit intra-component edges and use the same vertex-to-component map as the partition.
- Success is published only after partition and quotient validation; cancellation or snapshot change yields an incomplete result.

### Common failures

Frequent failures include computing undirected connected components; omitting isolated vertices; requiring singleton SCCs to have self-loops; confusing a DFS tree with mutual reachability; using discovery index instead of low-link at root tests; updating low-link through an edge to an already completed component; removing a vertex from the unresolved stack when its DFS call finishes; transposing endpoints without preserving vertices or edge identity; assuming numeric component labels are stable or topologically ordered; treating every residual cycle vertex as one component; recursively overflowing on a long path; mixing graph revisions; and declaring a partition correct because every vertex appears once without checking mutual reachability or maximality.

### Compact example

For edges

$$
a\to b,\ b\to a,\ b\to c,\ c\to d,\ d\to c,\ d\to e,
$$

the SCCs are $\{a,b\}$, $\{c,d\}$, and $\{e\}$. The condensation has edges $\{a,b\}\to\{c,d\}\to\{e\}$ and is acyclic. Vertex $e$ forms an SCC even without a self-loop. Adding $e\to a$ makes every component reachable around a cycle, so all five vertices merge into one SCC.

### Connections

[ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies invariant proof discipline, [ALGE-005](./005-asymptotic-time-and-space.md) supplies cost analysis, [ALGE-032](./032-depth-first-search.md) supplies discovery, finish, frame, and back-edge semantics, and [ALGE-033](./033-topological-ordering.md) supplies the DAG order used by condensation. [ALGE-035](../ROADMAP.md#block-04--graph-algorithms) next moves to minimum spanning structure in undirected weighted graphs, whose connectivity model is deliberately different.

## Governing Question

How do we find the unique maximal regions of mutual reachability in a directed graph, expose their acyclic dependency structure, and provide enough evidence to trust the result on deep, large, duplicated, mutable, or externally stored inputs?

Ordinary reachability answers a question from one source. Weak connectivity ignores edge direction. Strong connectivity requires paths both ways and therefore describes where directed cycles can circulate. A compiler control-flow graph, call graph, package dependency graph, state machine, or replication topology often becomes easier to reason about once every mutually reachable region is collapsed to one vertex.

The partition is mathematically unique, but its presentation is not. Component numbers, vertex order within a component, and component emission order depend on traversal and policy. A stable API must distinguish the invariant partition from its chosen serialization.

Three classic linear-time mechanisms deserve understanding. Kosaraju–Sharir is conceptually direct and naturally connects finish order to the transpose. Tarjan's algorithm performs one DFS and compresses reachability evidence into low-link values plus an unresolved stack. Gabow's path-based method replaces low links with two stacks. The best engineering choice depends on graph representation, recursion safety, transpose cost, streaming needs, and the evidence a caller requires.

## Why This Matters

Cycles are rarely all alike. A graph can contain thousands of unrelated cyclic regions joined by one-way dependencies. Returning only “cycle exists” loses the structure needed for diagnosis or downstream processing. SCC decomposition separates mutually dependent regions and turns the remaining global relation into a DAG, enabling topological evaluation, parallel planning, and localized repair.

Applications include recursive procedure groups, compiler data-flow iteration, module dependency diagnosis, model checking, dead-state analysis, web and citation structure, graph databases, build cycles, workflow validation, and decomposition before expensive graph algorithms. In a one-vertex component, a self-loop distinguishes a cyclic vertex from an acyclic singleton when that detail matters; SCC membership alone deliberately does not.

Linear asymptotic time does not settle implementation safety. A path with millions of vertices can overflow a language call stack. Building a transpose can double edge storage temporarily. Component labels can change after harmless input reordering. A live graph can mutate between passes. These are observable contract and lifecycle concerns, not footnotes to the theorem.

Modern libraries expose different choices. NetworkX 3.6.1 documents a nonrecursive Tarjan algorithm with Nuutila modifications and yields sets; Boost.Graph 1.92.0 documents Tarjan-based `strong_components`, writable component maps, vertex-index requirements for defaults, and $O(V+E)$ time. Such version-sensitive API facts must be checked separately from durable SCC theory.

## Prerequisites and Retrieval

Retrieve:

- finite directed graphs, paths, reachability, cycles, self-loops, parallel edges, subgraphs, and graph reversal;
- equivalence relations, partitions, quotient structures, partial orders, and proof by contradiction;
- DFS forests, root and neighbor order, discovery and finish times, tree edges, back edges, explicit frames, and recursion depth;
- adjacency lists, reverse adjacency, stacks, arrays, maps, sets, iterators, and stable identifiers;
- loop invariants, induction over recursive return, asymptotic work, auxiliary space, and output cost;
- topological ordering, rank maps, cycle witnesses, and DAG validation;
- immutable snapshots, graph revisions, counter width, memory budgets, cancellation, checkpoints, and atomic publication;
- property, differential, metamorphic, exhaustive, adversarial, and fault-injection testing.

You should be able to explain why “$u$ reaches $v$” is not symmetric and why adding the reverse reachability condition creates an equivalence relation.

## Learning Objectives

After completing this module, you should be able to:

1. define strong connectivity, SCC maximality, component maps, transpose graphs, and condensation graphs precisely;
2. prove that mutual reachability partitions the vertex set and that condensation is acyclic;
3. derive Kosaraju–Sharir from DFS finish-time behavior across components;
4. derive Tarjan's index, low-link, unresolved-stack, and root-pop invariants;
5. explain why edges to completed components do not update Tarjan low links;
6. compare two-pass, low-link, and path-based mechanisms and their representation costs;
7. implement deterministic, recursion-safe SCC extraction and condensation construction;
8. validate partition coverage, internal mutual reachability, maximality, quotient edges, and quotient acyclicity;
9. handle isolated vertices, self-loops, duplicates, deep paths, snapshot changes, cancellation, and unstable labels;
10. connect the decomposition to dependency diagnosis and production execution without overclaiming what SCC evidence proves.

## Core Exposition

### Specify the effective directed graph

Declare $V$ separately from $E$. An edge list cannot represent an isolated vertex. Define vertex identity, endpoint validation, self-loop policy, parallel-edge semantics, filters, and the graph revision. If edges come from several owners, decide whether duplicate records are one logical edge or separately auditable facts. The SCC partition is unchanged by duplicate parallel edges, but work, storage, diagnostics, and provenance are not.

Decide what output is required:

- a component ID for every vertex;
- explicit sets of vertices;
- a Boolean “whole graph is strongly connected” result;
- one largest component;
- condensation vertices and edges;
- a topological order of components;
- cyclic components only;
- witness paths within components;
- stable serialization across repeated runs.

These outputs require different evidence. A partition does not automatically include paths proving mutual reachability. An arbitrary integer label does not encode topological order. A singleton component does not reveal whether it has a self-loop. Stable component IDs require a policy such as the least stable vertex identifier or a content digest; traversal counters are insufficient.

### Prove that SCCs form a unique partition

Define $u\sim v$ exactly when $u$ reaches $v$ and $v$ reaches $u$.

- **Reflexive:** the length-zero path lets $u$ reach itself.
- **Symmetric:** the definition explicitly requires reachability in both directions.
- **Transitive:** if $u\sim v$ and $v\sim w$, concatenate paths $u\leadsto v\leadsto w$ and $w\leadsto v\leadsto u$ to obtain $u\sim w$.

Therefore $\sim$ is an equivalence relation. Its equivalence classes are disjoint, cover $V$, and are unique. Each class is strongly connected. It is maximal because any outside vertex mutually reachable with a member would be equivalent to every member and already belong to the class.

This proof prevents a common modeling error: SCCs are not arbitrary groups selected by an algorithm. Algorithms discover a canonical partition; only labels and enumeration order vary.

### Derive the condensation DAG

Let $\mathcal C$ be the SCC partition. The condensation $G^{\mathrm{SCC}}$ has one vertex for each $C\in\mathcal C$ and edge $C\to D$ when $C\ne D$ and some original edge crosses from a vertex in $C$ to a vertex in $D$.

Suppose the condensation contains a directed cycle of distinct components. Every component is internally strongly connected, and the crossing edges let one traverse the whole cycle. Hence any vertex in any cycle component reaches every other and can return. Their union is strongly connected, contradicting that the components are distinct maximal equivalence classes. Thus the condensation is a DAG.

The condensation is the finest acyclic contraction: splitting an SCC leaves mutually reachable quotient pieces and therefore a quotient cycle, while merging components can remain acyclic but discards structure. This property lets downstream algorithms operate on a smaller DAG without pretending that internal cyclic dependencies have vanished.

### Derive Kosaraju–Sharir

Let $G^T=(V,\{(v,u):(u,v)\in E\})$. Reversal preserves SCC membership: $u$ reaches $v$ in $G$ exactly when $v$ reaches $u$ in $G^T$, so mutual reachability is unchanged.

One standard variant performs:

1. a complete DFS of $G$ and records vertices by finish time;
2. a complete DFS of $G^T$ in decreasing finish time from the first pass;
3. one output component for each second-pass DFS tree.

Consider two distinct SCCs $C\to D$ in the condensation. If the first DFS reaches $C$ before either component is complete, it may enter $D$, but $D$ must finish before the call in $C$ can finish; no path returns from $D$ to $C$. More generally, the maximum finish time of $C$ exceeds that of $D$ for a sourceward component selected by decreasing finish time. In $G^T$, that selected component has no outgoing edge to another unassigned component, so the second DFS cannot escape it. Internal strong connectivity ensures it reaches all of it. Repeating extracts every SCC.

Equivalent presentations run the first pass on $G^T$ and the second on $G$, changing component emission direction. State the variant rather than memorizing “reverse something twice.”

### Implement a deterministic, recursion-safe two-pass algorithm

The implementation below coalesces parallel records, retains isolated vertices, uses explicit DFS frames, produces deterministic component serialization, builds the condensation, and independently checks the result on the example graph.

<!-- bijux-verify: {"id":"iterative-kosaraju-condensation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"components=(('i',), ('a', 'b', 'c'), ('d', 'e'), ('f', 'g'), ('h',))\nlabels=(('a', 1), ('b', 1), ('c', 1), ('d', 2), ('e', 2), ('f', 3), ('g', 3), ('h', 4), ('i', 0))\ncondensation=((1, 2), (2, 3), (3, 4))\nvalid=True\n","stderr":""}} -->
```python
def normalize(vertices, edges):
    vertices = set(vertices)
    graph = {vertex: set() for vertex in vertices}
    for tail, head in edges:
        if tail not in vertices or head not in vertices:
            raise ValueError(f"unknown endpoint: {(tail, head)}")
        graph[tail].add(head)
    return {vertex: tuple(sorted(heads)) for vertex, heads in graph.items()}


def transpose(graph):
    reversed_graph = {vertex: [] for vertex in graph}
    for tail, heads in graph.items():
        for head in heads:
            reversed_graph[head].append(tail)
    return {vertex: tuple(sorted(tails))
            for vertex, tails in reversed_graph.items()}


def finish_order(graph):
    visited = set()
    finished = []
    for root in sorted(graph):
        if root in visited:
            continue
        visited.add(root)
        stack = [(root, 0)]
        while stack:
            vertex, index = stack[-1]
            if index == len(graph[vertex]):
                finished.append(vertex)
                stack.pop()
                continue
            head = graph[vertex][index]
            stack[-1] = (vertex, index + 1)
            if head not in visited:
                visited.add(head)
                stack.append((head, 0))
    return tuple(finished)


def strongly_connected_components(vertices, edges):
    graph = normalize(vertices, edges)
    reversed_graph = transpose(graph)
    assigned = set()
    components = []
    for root in reversed(finish_order(graph)):
        if root in assigned:
            continue
        assigned.add(root)
        component = []
        stack = [root]
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for head in reversed(reversed_graph[vertex]):
                if head not in assigned:
                    assigned.add(head)
                    stack.append(head)
        components.append(tuple(sorted(component)))
    return tuple(components), graph


def component_map(components):
    return {vertex: number
            for number, component in enumerate(components)
            for vertex in component}


def condensation(graph, labels):
    return tuple(sorted({
        (labels[tail], labels[head])
        for tail, heads in graph.items()
        for head in heads
        if labels[tail] != labels[head]
    }))


def reaches(graph, source):
    seen = {source}
    stack = [source]
    while stack:
        vertex = stack.pop()
        for head in graph[vertex]:
            if head not in seen:
                seen.add(head)
                stack.append(head)
    return seen


def validate_partition(graph, components):
    flattened = [vertex for component in components for vertex in component]
    if len(flattened) != len(graph) or set(flattened) != set(graph):
        return False
    labels = component_map(components)
    closure = {vertex: reaches(graph, vertex) for vertex in graph}
    for left in graph:
        for right in graph:
            mutually_reachable = (
                right in closure[left] and left in closure[right]
            )
            if mutually_reachable != (labels[left] == labels[right]):
                return False
    quotient = condensation(graph, labels)
    return all(tail < head for tail, head in quotient)


vertices = set("abcdefghi")
edges = {
    ("a", "b"), ("b", "c"), ("c", "a"), ("c", "d"),
    ("d", "e"), ("e", "d"), ("e", "f"),
    ("f", "g"), ("g", "f"), ("g", "h"), ("h", "h"),
}
components, graph = strongly_connected_components(vertices, edges)
labels = component_map(components)
print(f"components={components}")
print(f"labels={tuple(sorted(labels.items()))}")
print(f"condensation={condensation(graph, labels)}")
print(f"valid={validate_partition(graph, components)}")
```

The validator computes transitive reachability only for this bounded example; using it on a production graph would cost far more than the SCC algorithm. Production validation can combine partition coverage, induced forward and reverse spanning trees per component, quotient-edge reconstruction, and condensation acyclicity for linear-size evidence.

The numeric labels follow second-pass discovery order and are not durable identities. The explicit sorted output is deterministic only because vertex keys and collation are stable in this example.

### Derive Tarjan's low-link method

Tarjan performs one DFS. At discovery, assign

$$
\operatorname{idx}(v)=\operatorname{low}(v)=t,
$$

increment $t$, push $v$ on the unresolved stack $S$, and set `on_stack(v)`.

For each edge $v\to w$:

- if $w$ is undiscovered, recursively explore it and, after return, set $\operatorname{low}(v)=\min(\operatorname{low}(v),\operatorname{low}(w))$;
- if $w$ is already on $S$, set $\operatorname{low}(v)=\min(\operatorname{low}(v),\operatorname{idx}(w))$;
- if $w$ has been assigned to a completed SCC, do not lower through it.

After all edges, if $\operatorname{low}(v)=\operatorname{idx}(v)$, pop $S$ until and including $v$. Those popped vertices form one SCC.

The key distinction is between the DFS activation stack and the unresolved-component stack. A descendant's recursive call can finish while the vertex remains on $S$ awaiting an ancestor's component. Ordinary black color therefore does not mean “ignore”; `on_stack` does. Conversely, an edge to a previously completed SCC must not lower the current root candidate even if that target has a small discovery index.

One useful interpretation is that low-link identifies the earliest unresolved DFS position the explored region can return to without passing through a completed component. When a vertex cannot return above its own index, it closes the unresolved suffix rooted there. This sentence is intuition; correctness rests on the precise recurrence and stack invariant.

### Prove the Tarjan pop rule

Maintain that $S$ contains exactly discovered vertices not yet assigned to an output component, in discovery order with interleaved completed calls removed only by SCC suffix pops. Before $v$ is popped as a root, every unresolved descendant $w$ with $\operatorname{low}(w)$ reaching $v$ has a path back to $v$ through explored unresolved structure, while DFS tree paths give $v\leadsto w$. Thus the popped suffix is mutually reachable.

If $\operatorname{low}(v)<\operatorname{idx}(v)$, explored evidence reaches an earlier unresolved root candidate, so $v$ cannot close a maximal component yet. If equality holds after complete adjacency processing, no popped suffix vertex can reach an earlier unresolved vertex in a way represented by the recurrence; otherwise low-link would be smaller. The suffix is therefore maximal at that moment.

After it is popped, future DFS work cannot make it strongly connected with an unassigned vertex. Such mutual reachability would require a return path that DFS would have exposed before the root closed. Each vertex is pushed and popped once; each edge causes constant recurrence work, yielding $\Theta(n+m)$ time.

### Avoid the completed-component low-link defect

Consider a completed SCC $A$ with small discovery indices and a later SCC $B$ having an edge $B\to A$ but no path from $A$ back to $B$. If the algorithm updates $\operatorname{low}(B)$ from `idx(A)` regardless of stack membership, $B$ appears to reach an earlier unresolved ancestor and may never pop at its true root or may merge incorrectly.

The edge is real, but it is one-way between components. `on_stack(A) == false` records that $A$ has already closed and cannot participate in the current unresolved SCC. Ignoring the edge for low-link does not ignore it globally; it becomes a condensation edge.

Some pseudocode formulations update a parent with every tree child's low-link without a separate post-return stack test because the surrounding proof and pop timing make it safe. Others state the unresolved condition explicitly. Do not combine lines from different variants without carrying their invariants.

### Compare Gabow's path-based method

Gabow-style path-based DFS maintains a stack $S$ of unassigned vertices and a stack $P$ of candidate component roots. Discovery pushes a vertex on both. An edge to an unresolved earlier vertex removes candidate roots from $P$ until the top is no earlier than the target. When finishing a vertex equal to the top of $P$, pop one component suffix from $S$ and remove that root from $P$.

This approach avoids explicit low-link numbers while retaining linear time and arrays/stacks. It can offer a simpler operational story for some implementations, but it still requires exact discovery order, unresolved membership, adjacency resumption, and suffix-pop correctness. “Two stacks” is not a proof.

Kosaraju–Sharir often wins on clarity and easy iteration. Tarjan avoids constructing or traversing a transpose and can emit components during one pass. Gabow offers a path-oriented alternative. Measure actual memory traffic and implementation risk on the intended representation rather than treating one linear-time algorithm as universally faster.

### Build and use condensation safely

Given `component[v]`, scan every logical edge $u\to v$. If labels differ, add component edge `component[u] -> component[v]`; coalesce duplicates if the quotient is a simple graph. Preserve provenance separately when callers need to know which original constraints created the edge.

Validate that the quotient is acyclic. A topological order of components enables source-to-sink evaluation. Some SCC algorithms emit reverse topological order under particular variants, but label order is not a portable guarantee. Compute or validate the order explicitly unless the implementation contract proves it.

Within a component, a topological order of individual vertices does not exist when it contains a directed cycle. A downstream planner must choose a component-level policy: reject, solve a simultaneous fixed point, iterate to convergence, break an allowed constraint, or invoke domain-specific cycle handling. Condensation exposes the boundary; it does not choose the policy.

### Validate the partition and evidence

A basic structural check ensures that components are nonempty, disjoint, contain only declared vertices, and cover $V$. That is necessary but not sufficient: any arbitrary partition passes it.

To certify internal strong connectivity of component $C$, select representative $r$. A traversal restricted to $C$ must reach every vertex from $r$ in $G[C]$, and another restricted traversal in $G^T[C]$ must reach every vertex from $r$. These two spanning reachability trees prove $r\leadsto v$ and $v\leadsto r$ for every $v$, hence pairwise mutual reachability through $r$.

To establish maximality, reconstruct every intercomponent edge and prove the condensation acyclic. If two distinct components were mutually reachable, the quotient would contain a directed cycle. Thus internal certificates plus an acyclic quotient establish the SCC partition.

Also check:

1. graph revision and normalization match;
2. every original edge is either internal or maps to the correct quotient edge;
3. every quotient edge has at least one original witness edge;
4. self-loop and parallel-edge policy is preserved in metadata;
5. stable component identities follow the declared rule;
6. success, cancellation, resource exhaustion, and input failure are distinct statuses.

### Engineer deep and large traversals

Recursive specifications mirror proofs but a directed path has DFS depth $n$. Do not raise a recursion limit without bounding native and language frame memory. Use explicit frames that retain vertex, next-neighbor position, and algorithm-specific return state. For Tarjan, child return must update the correct parent before the parent can close.

Kosaraju–Sharir needs access to both orientations. Options include storing outgoing and incoming adjacency, constructing a transpose, using a database index over edge heads, externally sorting reversed edge pairs, or reading a bidirectional graph interface. “Transpose is free” is a representation assumption, not an algorithm theorem.

Budget arrays for discovery indices, low links or assignment state, explicit frames, unresolved stacks, component labels, and validation ranks. Use widths that can represent all vertices and edges. Detect overflow before assignment. Component output itself is $\Theta(n)$.

For external memory, record I/O passes, sort volume, partition skew, and checkpoint boundaries. Tarjan's DFS access pattern can be less sequential than two-pass methods. The right choice may trade another edge scan for predictable bulk I/O.

### Preserve snapshots, cancellation, and recovery

SCC claims concern one edge relation. An edge added between passes can merge components; a removed edge can split one. Bind all traversals, transpose data, indices, stacks, labels, quotient edges, and validators to one immutable snapshot or transactionally consistent revision.

Cancellation leaves partial DFS trees and unresolved stacks. It proves neither a complete partition nor maximality. Return an incomplete status and discard or clearly quarantine partial labels. A checkpoint for iterative Kosaraju includes graph identity, current pass, finish sequence, assigned set, component under construction, explicit frames, and output position. A Tarjan checkpoint additionally includes indices, low links, unresolved stack, membership bits, counter, and child-return state.

Persist checkpoint state atomically. On resume, validate graph identity, stack membership consistency, unique indices, frame cursors, and completed-component coverage. Otherwise restart. Publishing a partial component as final can be especially misleading because later edges may merge it with unresolved vertices.

### Test and operate the decomposition

For small graphs, independently compute transitive closure and group vertices by mutual reachability. Compare the partition as a set of frozensets, not by numeric labels. Enumerate all directed graphs through a bounded size to test singleton, cyclic, disconnected, and dense cases.

Metamorphic properties include:

- bijective vertex renaming preserves the mapped partition;
- transposing the whole graph preserves every SCC;
- permuting input vertices or edges changes no component sets;
- duplicating an edge changes no component sets under simple-graph semantics;
- adding an internal edge cannot split a component;
- removing an intercomponent edge cannot split an existing component;
- adding an isolated vertex adds exactly one singleton component;
- adding a self-loop changes no partition, though it changes cyclicity metadata;
- contracting the reported components yields an acyclic graph;
- adding an edge from a later condensation component back to an earlier one merges exactly the components on mutually reachable quotient paths, possibly more than its endpoints.

Inject unknown endpoints, iterator failure, allocation failure, counter overflow, corrupt transpose entries, cancellation at every DFS event, callback failure, snapshot replacement, checkpoint corruption, and output failure. Differentially compare Kosaraju–Sharir, Tarjan, Gabow, and a transitive-closure oracle on bounded inputs.

Observe vertices, logical and physical edge records, component count, singleton and self-loop counts, largest component, condensation edges, maximum DFS depth, explicit-frame bytes, unresolved-stack peak, transpose bytes and time, pass I/O, label serialization, validation time, cancellations, snapshot age, and publication outcome. A large SCC may reflect legitimate recursion or a dependency design failure; interpretation belongs to the domain owner.

## Definitions and Notation

Let $G=(V,E)$ be a finite directed graph, $n=|V|$, and $m=|E|$ under the declared logical-edge policy.

- $u\leadsto v$ means a directed path, including a length-zero path when $u=v$.
- $u\sim v$ means $u\leadsto v$ and $v\leadsto u$.
- An **SCC** is one equivalence class of $\sim$, equivalently a maximal strongly connected vertex set.
- $G[C]$ is the subgraph induced by vertex set $C$.
- The **transpose** $G^T=(V,E^T)$ has $E^T=\{(v,u):(u,v)\in E\}$.
- The **condensation** $G^{\mathrm{SCC}}$ contracts each SCC to one vertex and retains crossing edges.
- $\operatorname{idx}(v)$ is Tarjan's unique discovery index.
- $\operatorname{low}(v)$ is Tarjan's root-candidate summary under its precise recurrence.
- $S$ is Tarjan's stack of discovered vertices not yet assigned to a completed component.
- `on_stack(v)` is membership in $S$, not ordinary DFS gray color.
- A **component map** $c:V\to\{0,\ldots,k-1\}$ labels the $k$ output components.
- A **crossing edge** satisfies $c(u)\ne c(v)$.
- A **cyclic singleton** is a one-vertex SCC with a self-loop; an acyclic singleton lacks one.
- A **component root** is the DFS vertex whose completed root condition triggers a suffix pop; it is not necessarily a stable component representative.
- A **partition certificate** establishes coverage, disjointness, internal mutual reachability, maximality, and snapshot identity.

Component equality is independent of labels:

$$
\mathcal C_1=\mathcal C_2
\quad\Longleftrightarrow\quad
\{\operatorname{frozenset}(C):C\in\mathcal C_1\}
=
\{\operatorname{frozenset}(C):C\in\mathcal C_2\}.
$$

## Mechanisms, Invariants, or Proof Structure

### Equivalence and quotient obligations

Prove reflexivity using zero-length paths, symmetry from the definition, and transitivity by path concatenation. Equivalence classes give coverage, disjointness, and maximality. Prove condensation acyclicity by expanding any supposed quotient cycle into mutual reachability across its component union.

### Kosaraju–Sharir obligations

The first pass must finish every declared vertex on one graph orientation. The second pass must use the exact transpose and exact decreasing finish order. Before each second-pass root, all previously assigned components are complete; the chosen root belongs to a source component among the unassigned condensation under this variant, and transpose traversal cannot escape it. Internal reachability in the transpose covers the entire component.

### Tarjan obligations

At every event:

1. each discovered vertex has one unique index;
2. $S$ contains exactly discovered but unassigned vertices;
3. stack order follows discovery order after completed suffixes are removed;
4. low-link updates use only the declared tree-child and on-stack-edge cases;
5. completed-component edges never lower a current candidate;
6. a root test occurs only after all outgoing edges and child returns are processed;
7. a root pop removes one nonempty suffix through the root and assigns each vertex exactly once;
8. assigned components never reenter $S$.

The variant “undiscovered vertex count” proves termination: each DFS discovery decreases it. Each adjacency position advances once, and each vertex is pushed and popped once.

### Certificate obligations

For each component representative, forward and transpose restricted trees prove mutual reachability. Reconstructed quotient edges plus a valid topological order prove no distinct components are mutually reachable. Coverage and disjointness then prove the output equals the unique SCC partition.

## Alternatives and Trade-Offs

### Kosaraju–Sharir versus Tarjan

Kosaraju–Sharir offers a short proof, simple iterative traversals, and easy differential checking. It requires two full passes and transpose access. Tarjan uses one DFS pass and no explicit transpose but has subtler low-link, stack, and child-return invariants. Both are linear in an adjacency-list model.

### Tarjan versus Gabow

Tarjan stores indices and low links; Gabow stores unresolved vertices and candidate roots on two stacks. Gabow avoids low-link arithmetic, while Tarjan is widely documented and implemented. Implementation clarity, memory layout, and existing traversal infrastructure matter more than slogans about one stack versus two.

### Recursive versus explicit frames

Recursion closely matches the proof and can be appropriate under a proven depth bound. Explicit frames govern memory and enable checkpoints but must faithfully preserve next-neighbor position and post-child actions. A vertex-only stack is insufficient for exact Tarjan semantics.

### Materialized versus virtual transpose

Materialization makes the second pass simple and sequential but costs edge storage and construction I/O. A reverse-adjacency index or adapter avoids copying when the representation already supports incoming edges. Repeatedly scanning all edges to discover predecessors destroys linear time.

### Arbitrary versus stable component identity

Traversal labels are cheap and valid within one result. Stable IDs based on minimum canonical vertex keys or component content help diffs and references but require deterministic identity, sorting or reduction, and collision policy. Any graph update can merge or split components, so durable external references need versioning.

### Full decomposition versus targeted reachability

If the only question is whether one pair is mutually reachable, two targeted traversals may be cheaper. If many queries, condensation, or all cycles matter, full SCC decomposition amortizes better. A largest-component request can consume a streaming component iterator without sorting every component.

## Failure Modes and Misconceptions

- **Weak instead of strong connectivity:** ignoring directions merges vertices connected only one way.
- **Singleton self-loop requirement:** every isolated or acyclic vertex is still an SCC by length-zero reachability.
- **Cycle equals component:** overlapping directed cycles can belong to one SCC; distinct cycles can remain separate.
- **DFS tree equals component:** tree ancestry proves reachability downward, not a path back.
- **Wrong transpose:** dropping isolated vertices or reversing only selected edges changes the problem.
- **Wrong pass order:** combining finish order and graph orientation from different Kosaraju variants can merge or split results.
- **Low-link/index confusion:** child propagation and on-stack edges use different summaries.
- **DFS-color confusion:** a black vertex can remain unresolved on Tarjan's component stack.
- **Completed-edge lowering:** using an edge into a popped component corrupts the current low-link root.
- **Early stack removal:** finishing a recursive call does not necessarily finish its SCC.
- **Premature root test:** a later child can lower the candidate; test only after complete adjacency.
- **Label semantics:** numeric IDs are not stable, size ordered, or topological unless explicitly produced that way.
- **Residual maximality assumption:** coverage alone does not show internal mutual reachability or maximality.
- **Recursive safety assumption:** $O(n)$ stack depth can exhaust runtime stack on a path.
- **Free-transpose assumption:** reverse access may duplicate storage or require external sorting.
- **Mixed snapshots:** an edge change can merge or split components between passes.
- **Partial publication:** cancelled low-link state is not a valid partial partition.
- **Condensation solves cycles:** contraction exposes cyclic regions; domain policy must still handle their internals.
- **Disjoint-set substitution:** union-find models undirected equivalence under edge insertion, not directed mutual reachability.
- **Linear means cheap:** edge volume, random access, transpose I/O, output, and validation can dominate.

## Worked Examples

### Example 1

**Situation.** For edges $a\to b$, $b\to a$, $b\to c$, $c\to d$, and $d\to c$, derive the SCC partition from mutual reachability.

Vertices $a$ and $b$ reach one another directly, so $a\sim b$. Vertices $c$ and $d$ likewise reach one another. From $a$ or $b$, edge $b\to c$ reaches the second pair. No edge returns from $\{c,d\}$ to $\{a,b\}$, so cross-pair mutual reachability fails. Transitivity within each pair gives the classes $\{a,b\}$ and $\{c,d\}$.

**Conclusion.** SCC membership follows bidirectional path evidence, not the presence of an edge between groups; the one-way crossing becomes a condensation edge.

### Example 2

**Situation.** Graph $V=\{x,y\}$ has only self-loop $x\to x$.

Length-zero paths make $x\sim x$ and $y\sim y$. Neither vertex reaches the other, so the partition is $\{x\},\{y\}$. The self-loop makes $x$ cyclic, whereas $y$ is an acyclic singleton, but both sets are SCCs. The condensation has two vertices and no crossing edge because self-loops remain internal.

**Conclusion.** Component size and cyclicity are different outputs; singleton SCCs do not require self-loops.

### Example 3

**Situation.** Trace Kosaraju–Sharir on SCC chain $A=\{a,b\}\to C=\{c\}\to D=\{d,e\}$ with internal edges $a\leftrightarrow b$ and $d\leftrightarrow e$.

A first DFS from $a$ can enter $b,c,d,e$. Because no condensation edge returns, $d,e$ finish before $c$, and $c$ finishes before $a,b$ complete. The maximum finish time lies in $A$. In the transpose, the crossing edges point $D\to C\to A$. Starting the second pass at a maximum-finish vertex in $A$ cannot escape $A$ in the transpose, so it extracts $A$. The next unassigned maximum extracts $C$, then $D$.

**Conclusion.** Finish order selects a source component of the remaining condensation, and transposition prevents the second traversal from crossing forward out of it.

### Example 4

**Situation.** Trace Tarjan on $a\to b$, $b\to c$, $c\to a$, and $c\to d$, using indices $0,1,2,3$.

Discovery pushes $a,b,c$. Edge $c\to a$ sees on-stack index zero, so `low(c)=0`. Discover $d$ with `idx(d)=low(d)=3`; it has no outgoing edge, so it is a root and pops alone. Returning to $c$ does not merge completed $d$. Propagation gives `low(b)=0` and `low(a)=0`. At $a$, equality `low(a)=idx(a)=0` pops $c,b,a$ as one SCC.

**Conclusion.** The algorithm emits $\{d\}$ and $\{a,b,c\}$; a descendant can complete separately while its ancestors remain unresolved.

### Example 5

**Situation.** Explain why an edge from later vertex $x$ to already completed vertex $a$ must not lower `low(x)`.

Suppose $a$ was popped as singleton SCC with index zero. Later DFS discovers $x$ at index five and sees $x\to a$, but no path returns from $a$ to $x$. If code applies `low(x)=min(5,idx(a))`, it obtains zero and suppresses the valid root test at $x$. Since `on_stack(a)` is false, the precise recurrence ignores the edge for low-link. The edge is recorded later as component $X\to A$.

**Conclusion.** Low-link summarizes reachability within unresolved structure; edges to resolved components affect condensation, not component merging.

### Example 6

**Situation.** Prove that condensation vertices $A,B,C$ with edges $A\to B$, $B\to C$, and $C\to A$ cannot be three distinct SCCs.

Choose any $a\in A$, $b\in B$, and $c\in C$. Internal paths reach each crossing-edge tail and return from each head. Traversing the quotient cycle gives $a\leadsto b\leadsto c\leadsto a$; the same cycle with internal paths establishes mutual reachability for every pair across $A\cup B\cup C$. That union is strongly connected, contradicting maximal distinct components.

**Conclusion.** Every valid SCC condensation is acyclic; a quotient cycle is a checkable certificate that the partition is too fine or incorrectly labeled.

### Example 7

**Situation.** Existing condensation is $A\to B\to C\to D$. Add edge $D\to B$.

Before insertion no component can return to an earlier one. The new edge creates cycle $B\to C\to D\to B$. Therefore $B,C,D$ become mutually reachable and merge. Component $A$ reaches the merged component but receives no return path, so it remains separate. Merging only edge endpoints $B,D$ would be wrong because $C$ lies on the return structure.

**Conclusion.** A back edge in condensation can merge every component on the induced cycle, not merely its endpoints; dynamic maintenance needs reachability evidence.

### Example 8

**Situation.** Estimate explicit transpose storage for $m=600{,}000{,}000$ edges represented by two unsigned 64-bit endpoint IDs per edge, excluding offsets and allocator overhead.

Each record uses $16$ bytes, so the edge-pair array requires

$$
600{,}000{,}000\times16=9{,}600{,}000{,}000\text{ bytes}.
$$

That is $9{,}600{,}000{,}000/2^{30}\approx8.94$ GiB. Holding original and transpose pair arrays simultaneously consumes about $17.88$ GiB before adjacency offsets, sorting workspace, labels, and frames.

**Conclusion.** Kosaraju–Sharir remains linear, but transpose materialization can dominate memory; reverse indexes or external sorting may be necessary.

### Example 9

**Situation.** Validate reported components $\{a,b\}$ and $\{c\}$ for edges $a\to b$, $b\to a$, $b\to c$, and $c\to a$.

Coverage and disjointness pass. Internal mutual reachability also passes. However quotient edges are $AB\to C$ from $b\to c$ and $C\to AB$ from $c\to a$, forming a two-cycle. Expanding it shows $a,b,c$ are mutually reachable. The reported partition violates maximality and must be merged.

**Conclusion.** Internally strong groups are not necessarily maximal; condensation acyclicity completes the certificate.

### Example 10

**Situation.** A two-pass service computes finish order on graph revision 70. Before its transpose traversal, edge $z\to a$ is added in revision 71 and closes a path from a downstream component back to the source.

The finish order describes revision 70 while second-pass reachability describes revision 71. Components can be merged or split relative to either real snapshot, so the hybrid result has no theorem behind it. A correct service pins revision 70 for both passes and validation, then evaluates revision 71 separately.

**Conclusion.** Multi-pass algorithms require snapshot identity as part of correctness; “eventually consistent edges” do not define one SCC problem.

## Cross-Program Connections

- Data Structures Engineering owns adjacency, stack, map, and compact-index representation invariants; Algorithm Engineering owns SCC mechanisms, proof, and measured selection.
- Theory of Computation uses SCCs in automata and transition-system analysis but owns the language and complexity consequences.
- Programming Languages and Semantics uses SCCs for mutually recursive definitions and fixed-point ordering.
- Compiler Engineering applies SCC decomposition to call graphs, control-flow analyses, and iterative data-flow solving.
- Software Architecture uses SCCs to locate mutually dependent components; whether the cycle is acceptable is an architectural judgment.
- Software Delivery and Reliability Engineering applies SCC diagnostics to builds and deployment graphs, adding artifact, failure, and rollback semantics.
- Database and Data Engineering use SCCs in dependency and lineage graphs, where snapshot consistency and incomplete metadata are first-class risks.
- Distributed Systems adds partitioned graph ownership, duplicate delivery, durable checkpoints, and termination detection; sequential DFS order generally does not distribute directly.
- [ALGE-032](./032-depth-first-search.md) supplies the traversal invariants and [ALGE-033](./033-topological-ordering.md) supplies quotient ordering. [ALGE-035](../ROADMAP.md#block-04--graph-algorithms) contrasts directed mutual reachability with undirected weighted connectivity.

## References

1. Robert E. Tarjan, “Depth-First Search and Linear Graph Algorithms,” *SIAM Journal on Computing* 1(2), 146–160, 1972, DOI [10.1137/0201010](https://doi.org/10.1137/0201010). Primary source for the low-link SCC algorithm; publisher record checked 2026-09-05.
2. Micha Sharir, “A Strong-Connectivity Algorithm and Its Applications in Data Flow Analysis,” *Computers & Mathematics with Applications* 7(1), 67–72, 1981, DOI [10.1016/0898-1221(81)90008-0](https://doi.org/10.1016/0898-1221(81)90008-0). Primary published source for the two-pass method commonly associated with Kosaraju and Sharir; record checked 2026-09-05.
3. Harold N. Gabow, “Path-Based Depth-First Search for Strong and Biconnected Components,” *Information Processing Letters* 74(3–4), 107–114, 2000, DOI [10.1016/S0020-0190(00)00051-X](https://doi.org/10.1016/S0020-0190(00)00051-X). Primary source for the path-based two-stack presentation; checked 2026-09-05.
4. Robert E. Tarjan and Uri Zwick, “Finding Strong Components Using Depth-First Search,” *Journal of Computer and System Sciences* 136, 194–206, 2023, DOI [10.1016/j.jcss.2023.03.001](https://doi.org/10.1016/j.jcss.2023.03.001). Modern survey of DFS-based mechanisms; checked 2026-09-05.
5. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022, §§20.5 and 22.5. [Official publisher record](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), checked 2026-09-05.
6. Jeff Erickson, *Algorithms*, 1st ed., 2019, graph-search chapter. [Author-hosted book](https://jeffe.cs.illinois.edu/teaching/algorithms/), checked 2026-09-05.
7. NetworkX developers, “Strongly Connected Components,” NetworkX 3.6.1 documentation. [Official API documentation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.strongly_connected_components.html), checked 2026-09-05.
8. Boost C++ Libraries, “Strongly Connected Components,” Boost.Graph 1.92.0 documentation. [Official algorithm documentation](https://www.boost.org/latest/libs/graph/doc/strong_components.html), checked 2026-09-05.
9. Jørgen Bang-Jensen and Gregory Gutin, *Digraphs: Theory, Algorithms and Applications*, 2nd ed., Springer, 2009. [Official DOI record](https://doi.org/10.1007/978-1-84800-998-1), checked 2026-09-05.

## Exercises

### Exercise 1

For $V=\{a,b,c,d,e,f\}$ and edges $a\to b$, $b\to a$, $b\to c$, $c\to d$, $d\to c$, $d\to e$, and $e\to f$, identify every SCC, the cyclic singleton status, and all condensation edges.

### Exercise 2

Prove that transposing a directed graph preserves its SCC partition. Then explain why this fact alone is insufficient to justify Kosaraju–Sharir's ordering of second-pass roots.

### Exercise 3

Tarjan code updates `low(v)` with `idx(w)` for every edge $v\to w$ whose head was previously discovered, without checking whether $w$ remains on the unresolved stack. Construct a small counterexample, trace the corruption, and state the correct rule.

### Exercise 4

Choose between iterative Kosaraju–Sharir, iterative Tarjan, and Gabow's path-based method for a 700-million-edge graph stored as outgoing compressed adjacency on local NVMe. Incoming adjacency is unavailable, recursion is prohibited, memory is constrained, and a verifiable condensation is required. Give a defensible design and evidence plan.

### Exercise 5

A service receives versioned dependency edges from several teams, must expose stable component references, and incrementally receives insertions and deletions. Design an honest SCC publication protocol. Address snapshot identity, duplicate edges, stable IDs, recomputation versus dynamic maintenance, merge/split behavior, certificates, cancellation, and consumer migration.

## Answers to the Exercises

### Answer 1

Mutual edges make $\{a,b\}$ one SCC. Paths $c\to d$ and $d\to c$ make $\{c,d\}$ another. Vertex $e$ reaches $f$ but receives no path back, so $\{e\}$ and $\{f\}$ are separate singleton SCCs. Neither singleton is cyclic because neither has a self-loop.

Let component names be $A=\{a,b\}$, $C=\{c,d\}$, $E=\{e\}$, and $F=\{f\}$. Crossing edges are $A\to C$ from $b\to c$, $C\to E$ from $d\to e$, and $E\to F$ from $e\to f$. Internal pair edges disappear from the simple condensation. The quotient is the DAG chain $A\to C\to E\to F$.

### Answer 2

If $u\leadsto v$ in $G$, reversing every edge of that path gives $v\leadsto u$ in $G^T$. Therefore

$$
u\leadsto_G v\ \land\ v\leadsto_G u
$$

holds exactly when

$$
v\leadsto_{G^T} u\ \land\ u\leadsto_{G^T} v.
$$

The same vertex pairs are mutually reachable, so the equivalence classes—and hence SCC partition—are identical.

This does not justify arbitrary second-pass roots. A traversal of $G^T$ starting in one SCC can cross into another along a reversed condensation edge and merge DFS-tree output incorrectly. Finish order from the first pass selects a component with the required source/sink position among the unassigned quotient so that the chosen second-pass orientation cannot escape it. Transpose preservation explains what the components are; the finish-time theorem explains how one traversal isolates them.

### Answer 3

Use vertices $a,x$ with one edge $x\to a$, and choose root order $a$ then $x$. DFS discovers $a$ with index zero and, because it has no outgoing edge, pops completed SCC $\{a\}$. It later discovers $x$ with index one. The defective rule sees previously discovered $a$ and sets `low(x)=min(1,0)=0`. Then `low(x) != idx(x)`, so $x$ is never popped at its proper root even though no path returns from $a$ to $x$.

The correct non-tree rule lowers from `idx(w)` only when `on_stack(w)` is true. Since $a$ was assigned and removed, edge $x\to a$ is an intercomponent edge and must not influence the unresolved root candidate. With the correct rule, `low(x)=idx(x)=1` and $x$ pops as its own SCC.

### Answer 4

Start with an explicit-frame Tarjan or Gabow implementation because outgoing adjacency is available, recursion is forbidden, and materializing 700 million reversed edges may exceed memory. Tarjan needs index, low-link, component, membership, frame, and unresolved-stack storage; Gabow substitutes a candidate-root stack for low-link state. Select between them through prototype clarity, peak-byte calculation, sequential versus random I/O measurement, and differential tests—not asymptotic time, which is linear for both.

If an external sort can cheaply construct a disk-backed transpose and two sequential scans outperform irregular DFS reads, iterative Kosaraju–Sharir remains a valid alternative. Measure it rather than rejecting it categorically. In every design, pin one graph snapshot, use wide indices, checkpoint explicit frames atomically, and separate duplicate logical-edge policy from physical records.

Produce a component map, scan original edges to reconstruct deduplicated quotient edges with provenance, and topologically validate the quotient. For each component, retain or reconstruct forward and reverse restricted spanning trees as sampled or full certificates according to risk. Test against a closure oracle on bounded graphs, differentially compare algorithms, and inject deep paths, skewed components, self-loops, iterator/I/O failure, cancellation, and checkpoint corruption. Record edge bytes, auxiliary bytes, maximum depth and stack, I/O volume, runtime, component distribution, quotient size, and validation outcome.

### Answer 5

Create each published decomposition from an immutable, complete graph revision. Give every source record a stable owner and edge identity; normalize duplicates according to whether repeated records are the same fact or independent provenance. The result records the graph digest, normalization policy, algorithm version, component map, condensation, validation certificate, and completion status.

Stable component references can derive from a collision-checked digest of sorted canonical member IDs plus graph revision, or from a registry that explicitly records lineage. A member-derived ID changes on merge or split, which is honest; a registry ID needs versioned predecessor/successor relations and cannot pretend continuity where semantics changed.

Prefer full recomputation until measured graph size, update rate, and latency justify a proven dynamic algorithm. Insertions can merge all SCCs on new quotient cycles; deletions can split an SCC and therefore are not handled by union-find. Batch changes into a new snapshot, recompute or apply a verified dynamic transition, and never mutate a published partition in place.

On cancellation or evidence failure, publish no complete decomposition for the new revision; retain the previous revision with explicit staleness. Validate coverage, internal forward/reverse reachability evidence, every quotient edge, quotient acyclicity, and stable-ID collision policy. Atomically publish the new version and a migration map describing unchanged, merged, split, added, and removed components so consumers can move deliberately.
