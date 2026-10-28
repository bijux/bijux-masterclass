---
module_id: ALGE-032
program: Algorithm Engineering
level: 1
module_number: 32
title: Depth-First Search
status: complete
last_verified: 2026-09-05
---

# Depth-First Search

## One-Page Review

### Governing question

How do we preserve depth-first search's nested exploration, discovery and finish events, ancestor structure, and edge semantics while choosing recursion or explicit frames, controlling depth and memory, and operating on deterministic, implicit, mutable, or parallel graph representations?

### Essential definitions

- A **DFS forest** contains a tree for each root selected by the outer vertex order.
- A vertex is **white** before discovery, **gray** while its adjacency remains active, and **black** after all outgoing edges have been examined.
- The **discovery time** $d(v)$ records the transition from white to gray.
- The **finish time** $f(v)$ records the transition from gray to black.
- A **DFS frame** stores an active vertex and the position of its next neighbor.
- A **tree edge** first discovers its head.
- A **back edge** points from a vertex to an active ancestor, including a self-loop.
- A **forward edge** is a non-tree edge to a proper descendant.
- A **cross edge** joins vertices with disjoint DFS intervals.
- The **parenthesis property** says any two DFS intervals are nested or disjoint.
- A **preorder** sorts vertices by discovery time; a **postorder** sorts them by finish time.
- A **complete traversal** has finished every requested root and edge; early exit leaves an explicitly incomplete forest or trace.

### Central model, mechanism, or theorem

For a finite directed graph $G=(V,E)$ and declared root and neighbor orders, DFS discovers a white vertex $u$, keeps it gray while examining each outgoing neighbor in order, recursively explores every white neighbor to completion, and then finishes $u$.

The active calls or explicit frames form a root-to-current path. Each vertex receives one interval

$$
I(v)=[d(v),f(v)].
$$

For distinct vertices $u$ and $v$, exactly one of these relations holds:

$$
I(u)\cap I(v)=\varnothing,\qquad
I(u)\subset I(v),\qquad
I(v)\subset I(u).
$$

Moreover, $u$ is a proper ancestor of $v$ in the DFS forest exactly when

$$
d(u)<d(v)<f(v)<f(u).
$$

This nesting turns traversal events into structural evidence. In a directed graph, a cycle exists exactly when a complete DFS encounters a back edge. Reverse finish order is a topological order exactly when no back edge exists. Low-link, component, bridge, articulation, and planarity algorithms refine the same active-path machinery.

### Critical invariants

- Graph, root order, neighbor order, edge identity, filters, and snapshot are fixed for the traversal.
- A vertex changes color only white to gray to black for the current search.
- A vertex is claimed and timestamped before its frame becomes visible.
- The explicit frame at stack position $i$ retains the next unexamined adjacency position; it is not merely a vertex name.
- Gray vertices are exactly the active parent chain.
- Every tree edge records the parent before the child is explored.
- A vertex finishes only after every outgoing adjacency entry has produced its required event and every tree child has finished.
- The logical clock advances once at each discovery and once at each finish, without collision or overflow.
- Recursive and iterative implementations agree only when their neighbor-resumption and event contracts agree.
- Directed and undirected edge classification use different logical-edge rules.
- A Boolean visited flag cannot replace gray-versus-black state when active-ancestor or cycle semantics matter.
- Cancellation, callback failure, stack exhaustion, missing adjacency, or graph-version change prevents a complete-traversal claim.

### Common failures

Frequent failures include marking only on pop and pushing a vertex many times; using a vertex-only stack that cannot resume the correct neighbor; reversing a neighbor list without proving event equivalence; turning gray vertices black too early; classifying any edge to a visited vertex as a cycle; treating a directed edge to a black vertex as a back edge; counting the mirrored storage record of an undirected tree edge as a cycle; forgetting disconnected roots; assuming DFS finds a shortest path; overflowing the language call stack on a long path; raising the recursion limit without a memory argument; using one global visited set in depth-limited search and pruning a later shallower arrival; running callbacks with undocumented reentrancy; stopping at a target and publishing finish times; mixing graph snapshots; and parallelizing subtrees while still promising the sequential discovery order.

### Compact example

With sorted adjacency

$$
a:(b,c),\quad b:(d),\quad c:(d),\quad d:(b),
$$

DFS from $a$ discovers $a,b,d$, sees $d\to b$ while $b$ is gray, finishes $d$ and $b$, and then discovers $c$. Edge $d\to b$ is a back edge and certifies cycle $b\to d\to b$. When $c\to d$ is examined, $d$ is black and its interval is disjoint from $c$'s, so that edge is cross, not back.

The same destination can therefore mean “active ancestor” or “completed earlier branch.” A one-bit visited set cannot distinguish the cases.

### Connections

[ALGE-003](./003-loop-invariants-for-algorithm-correctness.md) supplies invariant discipline, [ALGE-005](./005-asymptotic-time-and-space.md) supplies cost analysis, [ALGE-021](./021-divide-and-conquer.md) supplies recursive structure, [ALGE-025](./025-backtracking.md) supplies explicit choice-stack reasoning, [ALGE-030](./030-selecting-a-design-paradigm-from-problem-structure.md) supplies paradigm selection, and [ALGE-031](./031-breadth-first-search.md) provides the contrasting level-order traversal.

## Governing Question

How can an implementation follow one branch completely, resume every suspended adjacency iterator exactly, and expose trustworthy ancestor, completion, and edge-classification evidence without assuming the runtime call stack or incidental container order is safe?

DFS is often summarized as “replace the BFS queue with a stack.” That slogan is adequate only for a narrow reachability result. Full DFS semantics include when a vertex becomes active, the order in which each edge is examined, when a child returns, and when a vertex finishes. Algorithms for cycles, topological ordering, strong or biconnected components, bridges, articulation points, and other graph structure depend on those events.

Engineering choices are visible. Recursive code mirrors the proof but can overflow. An explicit stack avoids call-stack dependence but must store neighbor progress. Root and adjacency order determine the forest and timestamps. Parallel execution changes active-path semantics. Depth limits change completeness. Visitor exceptions change finish events. The right implementation begins from the required output and evidence.

## Why This Matters

DFS exposes graph structure that reachability alone does not. The active gray path distinguishes a return to an ancestor from an edge into completed work. Nested discovery-finish intervals answer ancestor queries. Postorder supports dependency ordering. Low-link summaries compress information about escape from a subtree. These are not accidental artifacts; they are the reason DFS is a foundation for many linear-time graph algorithms.

The tiny recursive specification also hides a potentially linear-depth call stack. A graph that is one path of ten million vertices has trivial branching and dangerous recursion. Explicit frames move that storage into a controlled data structure, where capacity, byte width, checkpoints, and cancellation can be governed.

DFS is common in implicit state spaces, parsers, filesystems, dependency graphs, static analysis, and search. Those environments introduce cycles, aliases, generated neighbors, permissions, remote errors, and mutation. An unavailable directory is not empty. Two serialized states that compare equal may or may not denote the same search state. A callback can invalidate an iterator. Correctness therefore spans the effective graph and its lifecycle.

## Prerequisites and Retrieval

Retrieve:

- directed and undirected graphs, paths, reachability, cycles, trees, forests, ancestors, and descendants;
- recursion, induction, loop invariants, stacks, iterators, and state machines;
- arrays, maps, sets, adjacency lists, matrices, and compressed graph representations;
- preorders, postorders, partial orders, intervals, and total tie orders;
- asymptotic work, auxiliary space, recursion depth, amortized allocation, and cache behavior;
- atomic claims, work stealing, deterministic reductions, snapshot isolation, cancellation, and restart;
- callbacks, exceptions, resource ownership, reentrancy, and event logs;
- differential, metamorphic, property, adversarial, and fault-injection testing.

You should be able to explain why “visited” and “currently on the active recursion path” are different predicates.

## Learning Objectives

After completing this module, you should be able to:

1. specify DFS over an effective directed or undirected graph with explicit root, neighbor, identity, event, and failure semantics;
2. derive the white-gray-black recursive mechanism and its explicit-frame equivalent;
3. prove forest coverage, active-path behavior, and the discovery-finish parenthesis theorem;
4. classify directed tree, back, forward, and cross edges and handle undirected mirrored adjacency correctly;
5. derive directed cycle detection and reverse-finish topological ordering from DFS invariants;
6. calculate work, graph-representation cost, explicit-stack bytes, recursion risk, and output cost;
7. design correct early exit, depth-limited, iterative-deepening, and implicit-state variants;
8. govern callbacks, cancellation, snapshots, checkpoints, and deterministic output;
9. validate forest, timestamps, intervals, classifications, and exact ordered traces independently;
10. decide when DFS, BFS, iterative deepening, or a specialized structural algorithm fits the contract.

## Core Exposition

### Specify the effective graph and trace

Define the vertex universe, directedness, logical edge identities, self-loops, parallel edges, root order, neighbor order, filters, and snapshot. For implicit graphs, define successor generation and state equality. For filesystems or remote stores, distinguish empty adjacency from failed or unauthorized enumeration.

DFS outputs can include:

- reachable vertex set;
- one path to each discovered vertex;
- a single-source tree or full forest;
- discovery preorder;
- finish postorder;
- discovery and finish timestamps;
- edge events and classifications;
- a target witness;
- a depth-bounded result;
- summaries such as low-link values built by a client algorithm.

These outputs require different state. Reachability needs one claimed bit. Directed cycle detection needs active-versus-finished state. A deterministic trace needs stable root and neighbor order. Exact recursive visitor events need resumable adjacency positions. A completed postorder cannot be returned after abrupt target exit unless the remaining traversal is completed or the status says partial.

An ordinary vertex traversal may coalesce parallel adjacency entries. An edge-classification or visitor contract may not: each logical edge identity needs its own examine and finish behavior. In undirected storage, two directed-looking records can represent one logical edge, so carry edge identity or a deliberate parent-edge rule.

### Define the recursive specification

Initialize every vertex white and a logical clock to zero. Visit roots in the declared order. When visiting white $u$:

1. change $u$ to gray;
2. increment the clock and assign $d(u)$;
3. emit the discovery event;
4. examine outgoing adjacency entries in order;
5. for a white head $v$, record tree edge and parent $p(v)=u$, then visit $v$ completely;
6. for a gray or black head, emit the appropriate non-tree event;
7. after every adjacency entry completes, change $u$ to black;
8. increment the clock and assign $f(u)$;
9. emit the finish event.

The outer root loop turns a single-source traversal into a forest. Starting with a preferred root and then continuing across all white vertices gives that root's tree first without losing disconnected coverage.

The recursive call itself stores $u$, its next-neighbor position, local summary state, and the return continuation. Any iterative replacement must preserve the pieces that downstream logic uses.

### Build explicit frames, not a bag of vertices

A faithful frame is approximately

$$
\operatorname{Frame}(u,i,\sigma),
$$

where $u$ is active, $i$ identifies the next adjacency entry, and $\sigma$ contains client state that must survive child traversal. The top frame advances one neighbor at a time. On a white neighbor, it saves its advanced position and pushes the new child frame. Only a frame whose adjacency is exhausted may finish and pop.

A common reachability-only variant pushes all neighbors at once, perhaps in reverse order. It can reproduce a particular preorder when claims and reversal are carefully arranged, but it does not automatically reproduce edge-examine, tree-edge, finish-edge, and finish-vertex events. Duplicate pushes and when vertices are marked further change behavior. Name it a different traversal contract unless equivalence is proved.

An explicit frame stack makes memory visible and controllable. It can reserve capacity, reject impossible indices, spill or checkpoint under a designed protocol, and unwind on cancellation. It still has $\Theta(h)$ frames for forest height $h$, which can be $\Theta(|V|)$.

### Execute deterministic iterative DFS

The following implementation uses sorted roots and neighbors, retains the next-neighbor index in every active frame, assigns exact discovery and finish times, and classifies directed edges after the forest is complete.

<!-- bijux-verify: {"id":"deterministic-iterative-dfs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"preorder=('a', 'b', 'd', 'e', 'c', 'x', 'y')\npostorder=('e', 'd', 'b', 'c', 'a', 'y', 'x')\ntimes=(('a', 1, 10), ('b', 2, 7), ('c', 8, 9), ('d', 3, 6), ('e', 4, 5), ('x', 11, 14), ('y', 12, 13))\nparents=(('a', None), ('b', 'a'), ('c', 'a'), ('d', 'b'), ('e', 'd'), ('x', None), ('y', 'x'))\nedges=(('a', 'b', 'tree'), ('a', 'c', 'tree'), ('a', 'e', 'forward'), ('b', 'd', 'tree'), ('c', 'd', 'cross'), ('c', 'e', 'cross'), ('d', 'b', 'back'), ('d', 'e', 'tree'), ('x', 'y', 'tree'), ('y', 'x', 'back'))\nback_edges=(('d', 'b'), ('y', 'x')) cycle=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Forest:
    parent: dict[str, str | None]
    discover: dict[str, int]
    finish: dict[str, int]
    preorder: tuple[str, ...]
    postorder: tuple[str, ...]
    edges: tuple[tuple[str, str, str], ...]


def normalize(graph):
    vertices = set(graph)
    normalized = {}
    for vertex, neighbors in graph.items():
        if any(neighbor not in vertices for neighbor in neighbors):
            raise ValueError(f"unknown neighbor from {vertex}")
        normalized[vertex] = tuple(sorted(set(neighbors)))
    return normalized


def depth_first(graph):
    graph = normalize(graph)
    color = {vertex: "white" for vertex in graph}
    parent = {}
    discover = {}
    finish = {}
    preorder = []
    postorder = []
    clock = 0

    for root in sorted(graph):
        if color[root] != "white":
            continue
        parent[root] = None
        color[root] = "gray"
        clock += 1
        discover[root] = clock
        preorder.append(root)
        stack = [(root, 0)]

        while stack:
            vertex, next_index = stack[-1]
            if next_index == len(graph[vertex]):
                color[vertex] = "black"
                clock += 1
                finish[vertex] = clock
                postorder.append(vertex)
                stack.pop()
                continue

            neighbor = graph[vertex][next_index]
            stack[-1] = (vertex, next_index + 1)
            if color[neighbor] == "white":
                parent[neighbor] = vertex
                color[neighbor] = "gray"
                clock += 1
                discover[neighbor] = clock
                preorder.append(neighbor)
                stack.append((neighbor, 0))

    classified = []
    for tail in sorted(graph):
        for head in graph[tail]:
            if parent.get(head) == tail:
                kind = "tree"
            elif tail == head or (
                discover[head] < discover[tail]
                and finish[tail] < finish[head]
            ):
                kind = "back"
            elif (
                discover[tail] < discover[head]
                and finish[head] < finish[tail]
            ):
                kind = "forward"
            else:
                kind = "cross"
            classified.append((tail, head, kind))

    return Forest(
        parent,
        discover,
        finish,
        tuple(preorder),
        tuple(postorder),
        tuple(classified),
    )


def validate(graph, forest):
    vertices = set(graph)
    assert set(forest.parent) == vertices
    assert set(forest.discover) == vertices
    assert set(forest.finish) == vertices
    assert set(forest.discover.values()) | set(forest.finish.values()) == set(
        range(1, 2 * len(vertices) + 1)
    )
    for vertex in vertices:
        assert forest.discover[vertex] < forest.finish[vertex]
        predecessor = forest.parent[vertex]
        if predecessor is not None:
            assert vertex in graph[predecessor]
            assert (
                forest.discover[predecessor] < forest.discover[vertex]
                < forest.finish[vertex] < forest.finish[predecessor]
            )
    for left in vertices:
        for right in vertices - {left}:
            left_interval = (
                forest.discover[left],
                forest.finish[left],
            )
            right_interval = (
                forest.discover[right],
                forest.finish[right],
            )
            disjoint = (
                left_interval[1] < right_interval[0]
                or right_interval[1] < left_interval[0]
            )
            nested = (
                left_interval[0] < right_interval[0]
                < right_interval[1] < left_interval[1]
                or right_interval[0] < left_interval[0]
                < left_interval[1] < right_interval[1]
            )
            assert disjoint or nested


graph = normalize({
    "a": ("e", "c", "b"),
    "b": ("d",),
    "c": ("e", "d"),
    "d": ("e", "b"),
    "e": (),
    "x": ("y",),
    "y": ("x",),
})
forest = depth_first(graph)
validate(graph, forest)

print(f"preorder={forest.preorder}")
print(f"postorder={forest.postorder}")
print(
    "times="
    + str(tuple(
        (vertex, forest.discover[vertex], forest.finish[vertex])
        for vertex in sorted(graph)
    ))
)
print(f"parents={tuple(sorted(forest.parent.items()))}")
print(f"edges={forest.edges}")
back_edges = tuple((tail, head) for tail, head, kind in forest.edges
                   if kind == "back")
print(f"back_edges={back_edges} cycle={bool(back_edges)}")
```

The post-classification uses finished intervals, making the categories easy to audit. An online visitor can classify edges from colors, but a black head may need timestamp or ancestor information to separate forward from cross. The normalization coalesces parallel entries only because this executable's contract is vertex structure rather than per-edge events.

### Prove forest coverage

Each root or tree edge discovers only a white vertex, so every vertex receives at most one parent and one discovery. A tree edge connects a discovered vertex to a newly discovered child, and parent pointers cannot cycle because discovery time strictly increases down the tree.

If the outer loop scans every vertex, any still-white vertex becomes a root. Recursive or explicit-frame exploration terminates on a finite graph because each frame advances a finite adjacency iterator and each white vertex is pushed at most once. Therefore every vertex eventually becomes black.

For a single root $s$, every discovered vertex has a parent path from $s$, so it is reachable. Conversely, take a reachable but undiscovered vertex and choose the first such vertex on a path from $s$. Its predecessor is discovered and eventually has every outgoing edge examined, so the edge to the supposedly undiscovered vertex would discover it. This contradiction proves exact reachable-set coverage.

### Prove the active-path invariant

Immediately after discovery, a vertex is gray and owns the top frame. It stays gray while each tree child is explored to completion. Pushing a child extends the parent chain by one. Popping a finished child restores its parent's frame and next adjacency position. No nonancestor remains gray because a child subtree finishes before a sibling begins.

Thus the gray vertices are exactly the vertices represented by the frame stack, in root-to-current order. An edge to gray therefore targets an ancestor or the vertex itself. This is why tricolor state certifies a directed back edge.

In an asynchronous or parallel traversal, active tasks may form several paths rather than one. The sequential color proof no longer transfers automatically; cycle algorithms need a concurrency-specific invariant or a different method.

### Prove the parenthesis theorem

When $u$ is discovered, its interval opens. DFS cannot finish $u$ until every tree child and descendant finishes. Therefore if $v$ is discovered while $u$ is gray, then

$$
d(u)<d(v)<f(v)<f(u).
$$

If $v$ is not discovered during $u$'s active interval, it is either already black before $d(u)$ or remains white until after $f(u)$. The intervals are then disjoint. Partial overlap is impossible because DFS completes the active descendant before resuming an ancestor or starting another root.

Consequently,

$$
u\text{ is an ancestor of }v
\Longleftrightarrow
d(u)\le d(v)<f(v)\le f(u),
$$

with equality only when $u=v$. This constant-time ancestor test is valid only for timestamps from the same completed forest and clock domain.

### Use the white-path theorem

At discovery of $u$, consider paths beginning at $u$ whose other vertices are white at that moment. Every vertex reachable by such a white path becomes a descendant of $u$: induction along the path shows each next white vertex is discovered within the still-active subtree, perhaps through an earlier branch.

Conversely, each descendant is reached through tree edges to vertices that were white when first traversed. This characterizes a DFS subtree independently of the exact moment each tree edge is chosen and supports many structural proofs.

The theorem's time reference matters. A vertex black before $u$ is discovered can be reachable from $u$ without becoming its descendant; an edge from $u$ to that vertex is cross.

### Classify directed edges

After a complete directed DFS:

- $(u,v)$ is **tree** when $p(v)=u$ and that logical edge made $v$ white to gray;
- it is **back** when $v=u$ or $v$ is a proper ancestor of $u$;
- it is **forward** when $v$ is a proper descendant of $u$ but the edge is not the tree edge;
- it is **cross** when the intervals of $u$ and $v$ are disjoint.

The timestamp tests are:

$$
\begin{aligned}
\text{back: }&
d(v)<d(u)<f(u)<f(v),\\
\text{forward: }&
d(u)<d(v)<f(v)<f(u),\\
\text{cross: }&
f(v)<d(u)\ \text{or}\ f(u)<d(v),
\end{aligned}
$$

with self-loops handled explicitly as back edges and tree identity checked before forward classification.

For online classification, a white head yields a tree edge, a gray head yields a back edge, and a black head yields forward or cross. If the client does not need to distinguish the last two, that event contract is simpler.

### Handle undirected logical edges

In an undirected DFS, every non-tree logical edge joins a vertex to an ancestor. If it joined two different completed branches, whichever branch was explored first would have traversed the edge and discovered the other endpoint, so they would not be different branches.

Storage complicates events. A tree edge $\{u,v\}$ may appear as $u\to v$ and $v\to u$. The reverse record seen at $v$ points to gray parent $u$, but it is the same logical tree edge, not an independent cycle witness. Track edge identity or skip exactly the parent edge identity. With parallel edges, only one identity is the tree edge; a second edge to the parent is a genuine non-tree edge and can form a length-two cycle in a multigraph contract.

Do not reuse directed forward/cross labels casually for undirected storage records. Define categories over logical edges.

### Derive cycle detection and topological order

If DFS sees back edge $(u,v)$ to an ancestor $v$, tree edges give a path $v\leadsto u$ and the back edge closes a directed cycle.

Conversely, suppose a directed cycle exists. Let $v$ be the first cycle vertex discovered. While $v$ remains gray, DFS follows white cycle vertices as descendants until an edge returns to an already discovered cycle vertex. The earliest such target is gray on the active ancestor path, yielding a back edge. Therefore:

$$
G\text{ has a directed cycle}
\Longleftrightarrow
\text{DFS has a back edge}.
$$

If no back edge exists, for every edge $(u,v)$, $f(u)>f(v)$. Tree and forward heads finish inside $u$; cross heads were already finished. Sorting vertices by decreasing finish time therefore places $u$ before $v$, producing a topological order. If a back edge exists, no topological order exists. The next module develops the full ordering contract.

### Separate reachability paths from shortest paths

Parent pointers construct one path from a root to every discovered vertex. DFS makes no minimum-length promise. If adjacency from $s$ explores a chain of one thousand edges before direct edge $(s,t)$, DFS can first reach $t$ along the chain. BFS would give hop distance one.

DFS is preferable when active ancestry, completion order, low-link structure, exhaustive backtracking, or low frontier width is central. BFS is preferable for unit-edge distances. A target search with a strong heuristic may favor another strategy. Select from the output contract.

### Control recursion depth deliberately

Recursive DFS mirrors the inductive proof and lets local variables naturally survive child calls. Its depth is forest height $h$, up to $|V|$. Runtime frames can contain return addresses, saved registers, exceptions, debugging metadata, and client locals, so stack bytes are not merely one vertex identifier.

Language recursion limits or native stack limits are operational guards. Increasing a limit does not reduce frame bytes and can turn a handled recursion exception into process stack exhaustion. Measure safe depth on the deployed runtime only as a guardrail; use explicit frames when input can form deep paths.

An explicit stack also needs a budget. If each frame uses $b_f$ bytes, peak frame payload is approximately

$$
h\,b_f,
$$

plus capacity slack and referenced iterator state. Check index width, multiplication overflow, allocator failure, and cancellation. A failed stack allocation returns incomplete or error, never “acyclic” or “unreachable.”

### Preserve recursive event order iteratively

To compare recursive and iterative implementations, define an event alphabet such as:

$$
\operatorname{discover}(u),\
\operatorname{examine}(u,v),\
\operatorname{tree}(u,v),\
\operatorname{back}(u,v),\
\operatorname{finishEdge}(u,v),\
\operatorname{finish}(u).
$$

Run bounded graphs through both implementations and compare the full event sequence, not only visited sets. The frame must remember whether a child edge awaits its finish-edge callback. Exceptions and early stops need an unwind policy: are active frames abandoned, sent cancellation events, or deterministically closed?

Visitor state may be passed by value, reference, handle, or closure depending on the library. Verify ownership. A copied visitor can make observed counters appear unchanged. A visitor that mutates the graph may invalidate the active adjacency iterator. Unless explicitly supported with a snapshot or mutation protocol, forbid structural mutation and reentrant traversal.

### Design depth-limited search carefully

A semantic depth limit $L$ explores paths containing at most $L$ edges. It can be complete for “find a witness within depth $L$” while incomplete for unrestricted reachability. Record cutoff separately from dead-end failure.

In graph search, one global visited bit can be unsound with a limit. Suppose DFS first reaches $v$ at depth $L$ and cannot expand it, then later reaches $v$ at depth $L-1$ along a shorter prefix. Skipping the second occurrence loses one unit of remaining budget and may miss a target child. Safe policies include:

- remember the greatest remaining depth with which each state has been explored and revisit only on improvement;
- use path-local cycle checks for a tree-search contract, accepting repeated state work;
- formulate a state as `(vertex, remaining budget)` and prove its dominance rule.

Iterative deepening runs depth limits $0,1,\ldots,D$ until a target is found. It combines DFS-like memory with minimum-depth discovery in a tree or correctly managed graph state. It repeats shallow work; in an ideal branching tree with $b>1$, total work remains $\Theta(b^D)$ because the deepest level dominates. On graphs with duplicates or expensive successor generation, measure the repetition and use a sound transposition policy.

### Account for graph and event cost

With adjacency lists and a full forest, DFS claims each vertex once and examines each stored adjacency entry once:

$$
T=\Theta(|V|+|E|).
$$

Single-root work can be stated over the reachable subgraph, plus any whole-universe initialization. An adjacency matrix requires scanning $|V|$ candidate heads for every expanded vertex, giving $\Theta(|V|^2)$ for a full forest.

Auxiliary color, parent, and timestamps use $\Theta(|V|)$ storage. The active frame stack uses $\Theta(h)$. Recording every edge event adds $\Theta(|E|)$ output; streaming events avoids retaining them but makes callback and sink cost part of traversal. Sorting adjacency adds construction cost. Hash-based state identity adds hashing and equality cost.

For implicit state spaces,

$$
T
=
\Theta(|V_R|)
+
\sum_{u\in V_R}\sum_{v\in N^+(u)}\Theta(g(u,v)),
$$

where $g$ includes successor generation, canonicalization, validation, and lookup. A nominal linear traversal can still be infeasible when reachable state grows exponentially in problem depth.

### Engineer representation and locality

CSR gives compact sequential scans within one vertex but a deep DFS jumps among adjacency segments as it follows edges. Returning to a parent requires its frame index, not rescanning from the start. Pointer-rich lists can make every frame and neighbor access a cache miss. Relabeling or layout by expected traversal can help but changes stable identities and costs preprocessing.

For filesystems, databases, object graphs, and remote APIs, open adjacency iterators may own descriptors, transactions, pages, or streams. Keeping one per active frame can exhaust resources on deep paths. A frame may instead store a stable cursor token, materialize bounded adjacency, or reopen under snapshot and idempotence guarantees. Include those costs and failure modes.

External-memory DFS is sensitive to random root-to-leaf movement. Blocking, graph separators, buffered traversals, or a different algorithm may improve I/O for a specific structural task. RAM-model $\Theta(V+E)$ does not imply scan-efficient external behavior.

### Treat parallel DFS as a changed contract

Exact deterministic DFS order has a long dependence chain: a parent does not continue to its next neighbor until the chosen child subtree finishes. Parallelizing sibling subtrees changes discovery and finish order and can race for vertices reachable from both.

Useful parallelism can still exist:

- traverse known-disjoint components independently;
- split an implicit search tree whose states have path-local identity;
- use work stealing for unordered reachability or backtracking;
- apply a parallel algorithm designed for the downstream property rather than parallelize sequential DFS literally.

Define ownership and duplicate claims. If two tasks reach the same white vertex, a global atomic winner changes forest structure by schedule. That may satisfy unordered reachability but not a canonical DFS forest, parenthesis trace, or sequential edge classification. Postprocessing arbitrary timestamps does not reconstruct the promised sequential traversal.

Distributed DFS additionally needs termination, active-work transfer, snapshot access, and recovery of suspended iterators. It is often a poor fit for high-latency partitioned graphs compared with frontier algorithms. Choose it only when the structural output or search behavior justifies the coordination.

### Preserve snapshots, cancellation, and checkpoints

DFS proofs concern one graph. Bind colors, frames, timestamps, parents, edge events, roots, filters, and neighbor ordering to a graph revision. If adjacency changes during traversal, a vertex can finish before a newly added outgoing edge appears, or an edge can vanish after becoming a recorded parent.

Cancellation leaves gray frames and unfinished intervals. Expose status and either retain a partial trace with explicitly open intervals or discard it. Do not fabricate finish timestamps during cleanup unless the contract defines cancellation events distinct from semantic finishes.

A resumable checkpoint contains graph and ordering versions, logical clock, completed roots, colors or claimed state, parents, timestamps, the ordered frame stack with next-neighbor positions, client summaries, and output sink position. Persist it atomically. On resume, verify every cursor can be reconstructed against the same snapshot. Otherwise restart or fail.

### Validate structure and exact traces

A completed structural certificate should check:

1. every requested vertex is exactly one root or has exactly one parent;
2. every parent is a logical graph edge;
3. parent pointers form a forest;
4. discovery and finish values are distinct and cover the promised clock domain;
5. $d(v)<f(v)$ for each vertex;
6. parent intervals strictly contain child intervals;
7. every pair of intervals is nested or disjoint;
8. edge classifications match parent and interval relations;
9. every back edge closes a replayable cycle;
10. graph, roots, neighbor order, filters, edge identities, and implementation versions match.

These conditions establish a structurally coherent DFS forest, but an exact deterministic event contract should also replay the algorithm over ordered adjacency and compare all events. Several DFS forests can be structurally valid for one graph.

For bounded graphs, compare recursive and explicit-frame event traces. Independently enumerate reachability and directed simple cycles. Metamorphic tests can relabel vertices bijectively; add isolated vertices; duplicate a logical edge under a multiplicity-insensitive contract; add a self-loop and require a back edge; and reorder adjacency, expecting structure to change only when order is not canonicalized.

Inject a path deeper than the recursive guard, invalid neighbors, callback exceptions at every event type, iterator invalidation, allocation failure, cancellation at every frame depth, checkpoint corruption, and snapshot replacement. Complete publication requires successful validation.

### Measure and operate the traversal

Record vertices and logical edges examined; roots; maximum frame depth and bytes; discovery and finish counts; edge-class counts; duplicate claim attempts; adjacency-generation time; sorting and normalization; callback time; cache and I/O behavior; allocation; cancellation; checkpoint; validation; and output time.

Use graph families that expose different risks: long paths, stars, balanced trees, dense digraphs, DAGs with cross edges, one large cycle, self-loops, parallel edges, disconnected graphs, deep implicit trees, and production snapshots. Compare like contracts. A reachability-only vertex stack is not a fair replacement for a timestamped edge-event DFS.

Before deployment, publish the root and neighbor ordering, recursion or explicit-frame policy, maximum depth or memory budget, mutation rule, callback ownership, failure status, validator, and snapshot binding. Reevaluate when graph depth, degree distribution, representation, runtime frame size, callback behavior, mutation rate, or output contract changes.

## Definitions and Notation

Let $G=(V,E)$ be a finite directed graph unless an undirected contract is stated. Let $n=|V|$ and $m=|E|$. Root order $\prec_V$ and each adjacency order $\prec_u$ together define one deterministic traversal.

- The **effective graph** is the snapshot-visible, filtered vertex and logical-edge relation actually traversed.
- A **DFS forest** $F$ is the parent relation created by a full outer root loop.
- A **root** has no parent in $F$; every other vertex has one tree-edge parent.
- A vertex is **white** if unclaimed, **gray** if active with unfinished adjacency, and **black** if finished.
- The **active path** is the ordered sequence of gray vertices represented by recursive calls or explicit frames.
- A **frame** stores an active vertex, its next adjacency position, and any suspended client state.
- Discovery time $d(v)$ is the clock value when $v$ becomes gray.
- Finish time $f(v)$ is the clock value when $v$ becomes black.
- The **DFS interval** $I(v)$ is $[d(v),f(v)]$.
- Vertex $u$ is an **ancestor** of $v$ when repeated parent links from $v$ reach $u$; it is a proper ancestor when $u\ne v$.
- The **preorder** is increasing discovery time.
- The **postorder** is increasing finish time; **reverse postorder** is decreasing finish time.
- A **tree edge** is the logical edge whose examination claims a white head.
- A **back edge** points to the same vertex or a proper active ancestor.
- A **forward edge** is a non-tree edge to a proper descendant.
- A **cross edge** has endpoints in disjoint DFS intervals.
- Forest height $h$ is the maximum number of vertices on a root-to-vertex parent path.
- A **visitor** is client behavior attached to declared traversal events.
- A **depth limit** $L$ bounds tree-path edges explored by one depth-limited invocation.
- A **cutoff** reports that a depth boundary, rather than exhaustive failure, stopped a branch.
- **Iterative deepening** repeats depth-limited search with increasing $L$.
- A **structural certificate** records enough forest, timestamp, edge, and version evidence to validate a completed result.
- An **exact trace contract** additionally fixes root, neighbor, logical-edge, callback, and error order.

For a vertex $u$, let $\operatorname{Adj}(u)$ be its ordered outgoing logical-edge sequence. Let $\operatorname{color}_t(u)$ be its color at event time $t$. The clock domain for a full forest with conventional discovery and finish events is

$$
\{1,2,\ldots,2n\}.
$$

If only a reachable component is requested, replace $n$ with the number of discovered vertices and state that the outer forest is not complete.

## Mechanisms, Invariants, or Proof Structure

### Color-transition invariant

Every vertex follows exactly one monotone state path:

$$
\text{white}\longrightarrow\text{gray}\longrightarrow\text{black}.
$$

White-to-gray occurs once, before parent or root discovery is published. Gray-to-black occurs once, after the final adjacency entry and every tree child complete. No ordinary completed DFS returns a vertex to white or gray.

This establishes at-most-once discovery and finish. It does not by itself establish depth-first order; the frame-resumption invariant supplies that.

### Frame-resumption invariant

For every active frame $(u,i,\sigma)$:

- adjacency positions below $i$ have completed their required examine and child-return behavior;
- position $i$ is the next unexamined entry, or $i=|\operatorname{Adj}(u)|$;
- any active child frame lies immediately above its parent;
- $u$ remains gray until $i=|\operatorname{Adj}(u)|$ and all child frames have popped.

Advancing $i$ before pushing a child ensures the edge is not repeated on return. Keeping the frame ensures later siblings are not lost. Finishing only at exhaustion gives the same nesting as recursion.

### Active-path theorem

The gray vertices are exactly one parent path in sequential DFS. Initially a new root is the only gray vertex. A tree edge pushes a white child whose parent is the previous top, extending the path. Finishing can pop only the top frame, shortening the path. No other transition creates gray state.

Therefore an edge examined toward gray state points to an ancestor or self. This theorem underlies online directed cycle detection and low-link updates.

### Parenthesis theorem

For any vertices $u,v$, their intervals are nested when one is an ancestor of the other and disjoint otherwise. The proper-ancestor test is

$$
u\text{ proper ancestor of }v
\Longleftrightarrow
d(u)<d(v)<f(v)<f(u).
$$

Proof follows from exclusive control of the active frame: once $v$ is discovered under gray $u$, $v$ must finish before $u$ resumes and finishes. A vertex not discovered during $u$'s active interval can only finish before $u$ opens or begin after $u$ closes.

The theorem forbids crossing timestamp pairs such as

$$
d(u)<d(v)<f(u)<f(v).
$$

One such pattern invalidates the trace or indicates incomparable clocks.

### White-path theorem

At the moment $u$ is discovered, vertex $v$ becomes a descendant of $u$ exactly when a path from $u$ to $v$ exists whose vertices after $u$ are white at that moment.

For the forward direction, tree edges on the parent path encountered white heads. For the reverse direction, choose the first vertex on a white path not made a descendant. Its predecessor is a descendant and cannot finish before examining the edge, which would discover or encounter the next vertex inside the subtree. Either way the alleged first outsider cannot remain outside.

This time-indexed theorem explains why a reachable black vertex can remain outside a later subtree.

### Edge-partition theorem

With logical edge identities, every directed edge belongs to exactly one of tree, back, forward, or cross:

1. The discovering edge is tree.
2. A non-tree edge whose head interval contains its tail interval is back.
3. A non-tree edge whose tail interval contains its head interval is forward.
4. Otherwise the intervals are disjoint and the edge is cross.

Nested-or-disjoint intervals make the cases exhaustive. Tree identity is tested before the general descendant relation because a tree edge also points forward to a descendant.

Self-loops are back by definition. In a simple undirected graph, every non-tree logical edge joins ancestor and descendant, so it is represented once as a back relation. Mirrored adjacency records do not create extra logical classes.

### Directed-cycle theorem

A back edge $(u,v)$ combines with the parent path $v\leadsto u$ to form a cycle. Conversely, choose the first discovered vertex on any directed cycle. DFS cannot finish it before following the cycle through white descendants or reaching an already active cycle vertex. The closing edge targets gray state and is back.

Thus a complete, snapshot-consistent directed DFS has

$$
\text{cycle exists}
\Longleftrightarrow
\text{back-edge set is nonempty}.
$$

A stopped or failed traversal can report a found cycle witness, but absence of a seen back edge before completion does not prove acyclicity.

### Reverse-finish ordering theorem

In a graph without back edges, every edge $(u,v)$ satisfies $f(u)>f(v)$. If $v$ is a descendant, it finishes before $u$. If it is not, it must have finished before $u$ discovered or examined the cross edge. Therefore decreasing finish time puts $u$ before $v$ for every edge.

If a back edge exists, its ancestor head finishes after its tail, and the graph is cyclic. Reverse finish order is then merely a vertex order, not a topological certificate.

### Recursive-to-iterative simulation

Map each recursive activation to one explicit frame containing the same vertex, next adjacency position, and suspended client state. Discovery maps to frame creation; recursive child call maps to child-frame push; return maps to child pop and parent resumption; function exit maps to finish and frame pop.

Induction on events proves a bijection between stacks and produces identical colors, parents, times, and callbacks. A vertex-only stack lacks enough state for this simulation. It may satisfy a weaker preorder or reachability contract but cannot claim full event equivalence without additional encoding.

### Depth-limited dominance invariant

For state $v$ reached with remaining allowance $r$, an earlier exploration with allowance $r'\ge r$ dominates the new occurrence only if successor semantics depend solely on $v$ and the earlier exploration completed. Store

$$
R(v)=\max\{\text{completed remaining allowance at }v\}.
$$

Skip a later occurrence only when $R(v)\ge r$. A Boolean visited bit collapses different remaining allowances and can be unsound. Path-dependent constraints require richer state than $(v,r)$.

### Work and storage theorem

Under constant-time color access and explicit adjacency lists, every vertex changes color twice and every stored directed adjacency entry is examined once. A full forest therefore uses

$$
\Theta(n+m)
$$

work and $\Theta(n+h)$ auxiliary metadata and active-frame entries, simplified to $\Theta(n)$. Event materialization can add $\Theta(n+m)$ output storage. Whole-universe initialization may dominate a small single-root reachable set.

Recursive and iterative variants have the same asymptotic active depth but different constants and failure modes. Matrix representation changes edge enumeration to $\Theta(n^2)$.

### Completion and publication invariant

A complete record binds:

$$
(r,\prec_V,\{\prec_u\},F,d,f,C,\text{status},E_{\mathrm{validation}}),
$$

where $r$ is graph/filter revision and $C$ is the logical edge classification or client summary. Every requested frame has closed, every edge event has completed, the clock and output sink reconcile, and validation passed.

Open frames, callback error, unavailable adjacency, cancellation, overflow, or revision mismatch yield an incomplete or failed record. A locally found cycle can be a complete positive witness even when full classification is incomplete; acyclicity still requires full coverage.

## Alternatives and Trade-Offs

| Approach | Best fit | Principal advantage | Principal obligation or cost |
|---|---|---|---|
| Recursive DFS | Trusted shallow graphs and simple visitors | Mirrors inductive specification | Runtime call-stack depth and unwind behavior |
| Explicit-frame DFS | Untrusted or deep graphs | Governed memory and exact resumption | Frame design and event simulation |
| Vertex-only iterative traversal | Reachability or selected preorder | Compact simple loop | Usually not full recursive DFS semantics |
| Full forest | Whole-graph classification | Covers disconnected vertices | Root order and full initialization |
| Single-root DFS | One reachable region | Avoids unrelated components | Cannot claim full graph properties |
| Tricolor state | Cycles, timestamps, low links | Distinguishes active ancestors | More state than a claimed bit |
| Boolean visited state | Plain reachability | Minimal metadata | Cannot classify active versus finished edges |
| Stable sorted adjacency | Reproducible forest and trace | Deterministic output | Sort/build cost and identity policy |
| Stored adjacency order | Source-order semantics | Avoids sorting | Order may be unstable across builds |
| Depth-limited DFS | Bounded witness search | Explicit semantic radius | Cutoff and revisit-state correctness |
| Iterative deepening | Unknown minimum tree depth | DFS-like path memory | Repeated generation and graph duplicates |
| BFS | Minimum unit-edge depth | Exact hop distances | Frontier memory and no DFS interval structure |
| Bidirectional or heuristic search | One target | May reduce explored state | Additional proof and representation |
| Edge-event streaming | Large traces | Avoids retaining all events | Sink cost, backpressure, and partial output |
| Timestamp materialization | Ancestor and order queries | Constant-time interval tests | Two counters per vertex and completion requirement |
| Work-stealing search | Unordered implicit exploration | Parallelism across branches | Schedule-dependent tree and duplicate ownership |
| External-memory traversal | Graph exceeds RAM | Controlled bulk storage | DFS locality and cursor persistence |
| Specialized SCC or bridge algorithm | Structural decomposition | Uses DFS summaries directly | Summary-specific stack and low-link invariants |

Choose recursive DFS when depth is tightly bounded below a measured safe guard and its event structure improves clarity. Choose explicit frames when graph depth is data dependent, cancellation or checkpointing matters, or runtime stack failure is unacceptable. Choose a weaker vertex-stack traversal only when its weaker output is the actual contract.

Choose BFS for shortest unit-edge paths. Choose iterative deepening for a minimum-depth target in an implicit tree when frontier memory is the constraint and repeated work is acceptable. Choose a dedicated parallel or distributed structural algorithm when exact sequential DFS ordering would serialize the workload.

## Failure Modes and Misconceptions

1. **Stack slogan:** replacing a queue with any stack is called equivalent recursive DFS.
2. **Mark on pop:** duplicate vertices accumulate and parent choice shifts.
3. **Lost neighbor position:** returning from a child restarts or skips parent adjacency.
4. **Premature black:** a vertex finishes before a child or edge callback completes.
5. **Missing finish:** a popped vertex never receives its postorder event.
6. **Clock collision:** discovery and finish events reuse timestamps.
7. **Clock overflow:** a narrow counter wraps within one forest.
8. **Visited means active:** every edge to any discovered vertex is labeled back.
9. **Black means forward:** a black head in an earlier branch is mislabeled descendant.
10. **Tree identity lost:** a tree edge is classified only by endpoint intervals.
11. **Self-loop omitted:** a one-vertex directed cycle is missed.
12. **Undirected mirror cycle:** the reverse storage record of a tree edge is called back.
13. **Parallel-edge collapse:** per-edge events disappear under endpoint deduplication.
14. **Directed-undirected confusion:** a theorem for logical undirected edges is applied to arcs.
15. **Single-root acyclicity:** unvisited components are ignored in a whole-graph claim.
16. **DFS shortest-path claim:** first discovery is mistaken for minimum hop count.
17. **Postorder after target exit:** unfinished gray frames receive authoritative finish order.
18. **Cycle absence before completion:** no observed back edge becomes an acyclic claim.
19. **Recursion-limit remedy:** a larger limit is assumed to reduce stack bytes.
20. **Explicit-stack amnesia:** container allocation can still fail or exceed budget.
21. **Frame-byte undercount:** iterators, capacity slack, and client summary state are omitted.
22. **Global depth-limit visited:** a deep first arrival prunes a useful shallow revisit.
23. **Cutoff as failure:** reaching the semantic depth boundary is called exhaustive absence.
24. **Path-local state omitted:** a vertex key merges histories with different legal continuations.
25. **Infinite successor stream:** one adjacency iterator prevents progress or cancellation.
26. **Unlawful state identity:** hash or equality merges distinct implicit states.
27. **Mutable adjacency:** a visitor invalidates the iterator currently held by a frame.
28. **Reentrant visitor:** callback recursion corrupts shared color, clock, or stack state.
29. **Copied visitor state:** results are written to an unobserved visitor copy.
30. **Callback exception erasure:** partial events are treated as a complete trace.
31. **Open-resource depth:** every frame retains a file, cursor, transaction, or network stream.
32. **Unavailable means empty:** an I/O or permission failure becomes a leaf.
33. **Snapshot mixture:** parent edges and timestamps describe different graph revisions.
34. **Unsafe checkpoint:** stack vertices are saved without next-neighbor positions.
35. **Parallel order promise:** work stealing returns a schedule-dependent forest under a canonical API.
36. **Racing claims:** parallel branches both publish one vertex or lose its client summary.
37. **Local completion:** distributed workers finish without global in-flight-work accounting.
38. **Matrix cost blindness:** neighbor enumeration scans all possible vertices.
39. **Trace-output blindness:** per-edge logging dominates the traversal.
40. **Structural-only validation:** a coherent forest is accepted as the exact declared ordered trace without replay.

## Worked Examples

### Example 1

**Question:** Interpret the executable forest's first component.

**Reasoning:** DFS opens $a$ at time 1, then follows $a\to b\to d\to e$. It closes $e,d,b$ at times 5, 6, and 7. It next opens and closes $c$ at 8 and 9, then closes $a$ at 10. Thus

$$
I(a)=[1,10],\
I(b)=[2,7],\
I(d)=[3,6],\
I(e)=[4,5],\
I(c)=[8,9].
$$

The second root $x$ and child $y$ use times 11 through 14.

**Engineering conclusion:** The explicit next-neighbor index lets $a$ resume at $c$ only after $b$'s entire subtree closes, matching recursive events.

### Example 2

**Question:** What do intervals $I(u)=[4,15]$, $I(v)=[7,10]$, and $I(w)=[16,19]$ prove?

**Reasoning:** Interval $v$ lies strictly inside $u$, so $u$ is a proper ancestor of $v$. Interval $w$ is disjoint from both and belongs to a completed earlier or later branch or root. It cannot be a descendant of either.

The proposed interval $I(x)=[9,17]$ would partially cross $u$ because $4<9<15<17$. No completed sequential DFS forest can contain both.

**Engineering conclusion:** Interval queries are constant time, but only after validating that all timestamps share one complete clock domain.

### Example 3

**Question:** Why are $d\to b$ and $c\to d$ different in the executable even though both heads were previously discovered?

**Reasoning:** When $d\to b$ is examined, $b$ is gray and its interval will contain $d$; the edge returns to an active ancestor and is back. When $c\to d$ is examined, $d$ is already black and $I(d)=[3,6]$ is disjoint from $I(c)=[8,9]$; the edge is cross.

**Engineering conclusion:** A visited bit answers reachability deduplication but cannot implement directed cycle or full edge classification.

### Example 4

**Question:** In an undirected multigraph, vertex $u$ is discovered from $p$ through edge identity $e_1$, and another parallel edge $e_2$ also joins $p$ and $u$. How should the records be treated?

**Reasoning:** The $u$-to-$p$ storage mirror of $e_1$ is the same logical tree edge and is skipped as a non-tree cycle witness. Edge $e_2$ is a different logical edge. Together $e_1$ and $e_2$ form a two-edge multigraph cycle, so $e_2$ is a non-tree ancestor connection.

**Engineering conclusion:** Skipping every edge whose endpoint equals the parent would incorrectly erase $e_2$. Use logical edge identity when multiplicity matters.

### Example 5

**Question:** Can DFS find a 101-edge path to $t$ before direct edge $(s,t)$?

**Reasoning:** Yes. If the first neighbor of $s$ begins a chain of 100 more edges ending at $t$, DFS explores that chain fully and claims $t$. Only after returning does it examine direct edge $(s,t)$. Its tree path has 101 edges although the minimum hop distance is 1.

**Engineering conclusion:** The path is a valid reachability witness. It is not a BFS distance certificate.

### Example 6

**Question:** Estimate active-stack payload on a path of five million vertices if an explicit frame is 24 bytes. Compare a hypothetical measured recursive frame of 160 bytes.

**Reasoning:** Explicit frame payload is

$$
5{,}000{,}000\cdot24
=120{,}000{,}000\text{ bytes}
\approx114.4\text{ MiB}.
$$

The hypothetical recursive payload is

$$
5{,}000{,}000\cdot160
=800{,}000{,}000\text{ bytes}
\approx762.9\text{ MiB}.
$$

Both omit allocator, capacity, runtime, and graph metadata.

**Engineering conclusion:** Explicit frames expose a smaller governable representation, but they do not make linear depth free.

### Example 7

**Question:** Why can a global visited bit break depth-limited DFS with limit 3 on edges $s\to a\to x\to v\to t$ and $s\to b\to v$, when $a$ precedes $b$?

**Reasoning:** The first branch reaches $v$ at depth 3, marks it, and cannot expand $v\to t$ without exceeding the limit. The later branch reaches $v$ at depth 2, from which $t$ is reachable at depth 3, but a global bit skips $v$ and misses the valid witness.

**Engineering conclusion:** Record the greatest completed remaining allowance for $v$, or include remaining budget in the state. Ordinary unbounded DFS's visited rule does not transfer unchanged.

### Example 8

**Question:** A DAG has edges $a\to c$, $b\to c$, and $c\to d$, with root order $a,b,c,d$. What reverse finish order can DFS produce?

**Reasoning:** DFS from $a$ visits and finishes $d$, then $c$, then $a$. Root $b$ finishes afterward. Increasing finish order is $d,c,a,b$, so reverse finish order is $b,a,c,d$. Every edge points left to right in that order.

Adding edge $d\to a$ makes $d$ see gray ancestor $a$, producing cycle $a\to c\to d\to a$.

**Engineering conclusion:** Reverse postorder is topological only after complete no-back-edge evidence.

### Example 9

**Question:** What is the payload of emitting one 24-byte event for each of two billion examined adjacency entries?

**Reasoning:**

$$
2{,}000{,}000{,}000\cdot24
=48{,}000{,}000{,}000\text{ bytes},
$$

or 48 GB decimal, about 44.7 GiB, before framing, indexes, or replication.

**Engineering conclusion:** An $\Theta(V+E)$ traversal can be output-bound. Stream with backpressure, aggregate counters, sample under an explicit diagnostic contract, or budget the complete trace.

### Example 10

**Question:** A remote directory DFS has opened a frame for directory $u$, read two of five pages of children, and then receives an unavailable response. May it finish $u$ and call the unseen pages empty?

**Reasoning:** No. Finishing asserts every effective outgoing entry was examined. The frame must remain resumable with its page cursor, retry under the same snapshot, or cause incomplete failure. Fabricating $f(u)$ would invalidate postorder, cycle absence, and coverage.

**Engineering conclusion:** Remote availability is part of the traversal proof. Empty and unavailable need distinct result states.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) connects DFS to reachability, state-space search, reductions, and graph-property certificates.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns stacks, iterators, graph layouts, visited maps, cursor invalidation, and compressed adjacency.
- [Programming Languages — Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md) supplies visitor dispatch, callback ownership, reentrancy, and object-graph identity.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies work stealing, atomic claims, deterministic scheduling, memory visibility, and cancellation.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies recursive graph queries, snapshot isolation, external operators, and cursor restart.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies process stack limits, virtual memory, filesystems, descriptors, and fault behavior.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns global termination, work transfer, checkpoint consistency, snapshot versions, and publication.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns authorization-filtered traversal, symbolic-link policy, adversarial depth, resource caps, and fail-closed results.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Authoritative DFS forest, timestamp, parenthesis, edge-classification, and topological-order foundations.
2. Jeff Erickson. [*Algorithms*](https://jeffe.cs.illinois.edu/teaching/algorithms/), self-published open textbook, 2019. Proof-oriented graph traversal, reachability, and structural algorithms.
3. Robert E. Tarjan. [“Depth-First Search and Linear Graph Algorithms”](https://doi.org/10.1137/0201010), *SIAM Journal on Computing* 1(2), 1972, pp. 146–160. Primary DFS treatment for biconnected and strongly connected components.
4. John Hopcroft and Robert Tarjan. [“Efficient Planarity Testing”](https://doi.org/10.1145/321850.321852), *Journal of the ACM* 21(4), 1974, pp. 549–568. Primary demonstration of DFS structure in a linear-time graph algorithm.
5. Robert E. Tarjan and Uri Zwick. [“Finding Strong Components Using Depth-First Search”](https://doi.org/10.1016/j.ejc.2023.103815), *European Journal of Combinatorics* 119, 2024, 103815. Current derivation, comparison, and nonrecursive treatment of DFS-based strong-component algorithms.
6. Boost Contributors. [“Depth-First Search”](https://www.boost.org/doc/libs/latest/libs/graph/doc/html/graph/algorithms/traversal/depth_first_search.html), Boost.Graph documentation, consulted 2026-09-05. Current generic color-map, root, visitor-event, and complexity contract.
7. NetworkX Developers. [“Traversal: Depth First Search”](https://networkx.org/documentation/stable/reference/algorithms/traversal.html), NetworkX 3.6.1 documentation, consulted 2026-09-05. Current preorder, postorder, predecessor, tree, labeled-edge, and depth-limit interfaces.
8. Python Software Foundation. [“System-Specific Parameters and Functions”](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit), Python 3.14 documentation, consulted 2026-09-05. Official recursion-limit purpose and stack-safety warning.
9. Robert Sedgewick and Kevin Wayne. [*Algorithms, fourth edition: Undirected Graphs*](https://algs4.cs.princeton.edu/41graph/), Princeton author site, 2011. Implementations and applications of DFS over explicit graph representations.
10. Steven S. Skiena. [*The Algorithm Design Manual*, third edition](https://doi.org/10.1007/978-3-030-54256-6), Springer, 2020. Practical graph traversal, representation, implementation, and algorithm-engineering guidance.

## Exercises

### Exercise 1

Run a complete directed DFS with root order $r,a,b,c,d,e$ and alphabetical adjacency over edges

$$
(r,a),(r,b),(a,c),(b,c),(b,e),(c,a),(c,d),(e,b).
$$

Give preorder, postorder, parents, discovery and finish times, and every edge class. Identify cycle witnesses and a valid reverse finish order, then explain whether that order is topological.

### Exercise 2

Prove the parenthesis theorem from the active-frame invariant. Then prove the directed-cycle theorem in both directions. Explain precisely why “an edge to any visited vertex proves a cycle” is false, using a three- or four-vertex counterexample.

### Exercise 3

Consider this iterative routine: pop a vertex; if unseen, mark and emit discovery; push every neighbor in forward adjacency order; immediately emit finish. Diagnose its differences from recursive DFS for reachability, preorder, parent choice, finish order, edge events, duplicate work, and cycle classification. Design the minimal explicit frame needed to simulate recursion exactly.

### Exercise 4

An implicit tree has branching factor 4 and its shallowest goal is at depth 10. Assume no duplicate states and 64 bytes for either one queued state or one active DFS frame. Compute:

- the number of nodes through depth 10;
- the depth-10 frontier bytes for BFS;
- the active frame bytes for depth-first traversal;
- the total node expansions for iterative deepening limits 0 through 10 if every tree node within a limit is expanded.

Compare the algorithms and list the assumptions that keep the arithmetic valid.

### Exercise 5

Transfer DFS to an unfamiliar constraint. An immutable object-store namespace contains 300 million directory and object identities. Directory pages contain stable child-edge identities; hard links and symbolic links can create aliases or cycles. The required output is a deterministic postorder of every identity reachable from a declared root, suitable as a deletion-plan candidate but not itself authorization. RAM is limited to 256 MiB. Pages are remote, paginated, and can be temporarily unavailable. A run must be resumable and may never publish a complete plan from mixed snapshots or missing pages.

Select and justify a traversal and state representation. Compare recursion, BFS, and an explicit external DFS. Define identity and link policy, ordering, cursor storage, cycle handling, event output, validation, checkpoints, failure behavior, metrics, and atomic publication.

## Answers to the Exercises

### Answer 1

Alphabetical adjacency is:

$$
r:(a,b),\quad
a:(c),\quad
b:(c,e),\quad
c:(a,d),\quad
d:(),\quad
e:(b).
$$

Start at $r$. The traversal follows $r,a,c$, sees $c\to a$ as a back edge, visits and finishes $d$, then finishes $c$ and $a$. It resumes $r$, visits $b$, sees completed $c$ through a cross edge, visits $e$, sees $e\to b$ as a back edge, and finishes $e,b,r$.

The preorder is

$$
(r,a,c,d,b,e),
$$

and the postorder is

$$
(d,c,a,e,b,r).
$$

Times and parents are:

| Vertex | Discover | Finish | Parent |
|---|---:|---:|---|
| $r$ | 1 | 12 | root |
| $a$ | 2 | 7 | $r$ |
| $c$ | 3 | 6 | $a$ |
| $d$ | 4 | 5 | $c$ |
| $b$ | 8 | 11 | $r$ |
| $e$ | 9 | 10 | $b$ |

Edge classes are:

| Edge | Class | Reason |
|---|---|---|
| $(r,a)$ | tree | discovers $a$ |
| $(r,b)$ | tree | discovers $b$ after $a$ closes |
| $(a,c)$ | tree | discovers $c$ |
| $(b,c)$ | cross | $I(c)=[3,6]$ precedes $I(b)=[8,11]$ |
| $(b,e)$ | tree | discovers $e$ |
| $(c,a)$ | back | $a$ is an active ancestor |
| $(c,d)$ | tree | discovers $d$ |
| $(e,b)$ | back | $b$ is an active ancestor |

Back edges yield cycles $a\to c\to a$ and $b\to e\to b$. Reverse finish order is $(r,b,e,a,c,d)$. It is a valid total vertex order but not a topological order because the cyclic graph has no topological order; for example, edge $c\to a$ points backward in it.

### Answer 2

The active-frame invariant says gray frames form one parent path and a parent frame cannot finish while a child frame remains. If $u$ is an ancestor of $v$, $u$ is discovered before $v$ and cannot finish until $v$ finishes:

$$
d(u)<d(v)<f(v)<f(u).
$$

If neither is ancestor of the other, whichever is discovered first completes before the other can be discovered. Otherwise the later vertex would be discovered inside the first vertex's active subtree and become its descendant. Their intervals are disjoint. These are the only cases, proving nested-or-disjoint parentheses.

For one direction of the cycle theorem, a back edge $(u,v)$ has ancestor head $v$. Tree edges give directed path $v\leadsto u$, and $(u,v)$ closes a directed cycle.

For the converse, select the first discovered vertex $v$ on a directed cycle. While $v$ is active, DFS follows white cycle vertices as descendants whenever it reaches them. Before $v$ can finish, some cycle edge points from a descendant to a cycle vertex already on the active path. That edge targets gray ancestor state and is back. A self-loop is the one-vertex case.

The claim about any visited target is false on DAG

$$
a\to b,\quad a\to c,\quad c\to b
$$

with adjacency $a:(b,c)$. DFS finishes $b$, then visits $c$ and examines $c\to b$. Vertex $b$ is visited but black; intervals $I(b)$ and $I(c)$ are disjoint, so the edge is cross. The graph is acyclic.

### Answer 3

Pushing neighbors in forward order makes the last neighbor pop first, reversing the recursive preference. Marking only after pop permits several parents to push the same vertex; the eventual winner depends on stack order, and queue or stack space can grow. Marking before push can remove duplicates, but assigning all children at once still makes them discovered before recursive DFS would reach them.

Immediate finish is fundamentally wrong. A recursive vertex stays gray while all descendants run and finishes after them. The routine gives parents intervals that close before child intervals open, so it loses the parenthesis property, postorder, active-ancestor detection, and correct tree-edge return events. A one-bit seen set cannot distinguish back from forward or cross edges. It may still enumerate the reachable set if every valid neighbor is eventually pushed and resource limits do not fail; that is a weaker contract.

The minimal ordinary frame is

$$
(u,i),
$$

where $u$ is gray and $i$ is the next adjacency index. If visitor logic needs edge-finish callbacks or local summaries, add the suspended edge identity and summary $\sigma$.

The loop examines adjacency $i$, increments the saved index, and:

- if the head is white, records the tree edge, discovers it, and pushes child frame $(v,0)$;
- otherwise emits the correct gray or black edge event;
- if $i=|\operatorname{Adj}(u)|$, emits finish, makes $u$ black, and pops.

Claim the child on push. With the same root and neighbor orders, induction over these transitions reproduces recursive preorder, parents, event sequence, and postorder.

### Answer 4

The complete tree through depth 10 contains

$$
\sum_{i=0}^{10}4^i
=\frac{4^{11}-1}{3}
=1{,}398{,}101
$$

nodes. The depth-10 frontier has $4^{10}=1{,}048{,}576$ states, so its payload is

$$
1{,}048{,}576\cdot64
=67{,}108{,}864\text{ bytes}
=64\text{ MiB}.
$$

One active root-to-depth-10 path has 11 frames:

$$
11\cdot64=704\text{ bytes}.
$$

For iterative deepening, a depth-$i$ node is expanded once for every limit from $i$ through 10. Total expansions are

$$
\sum_{i=0}^{10}(11-i)4^i
=1{,}864{,}131.
$$

That is about $4/3$ of the one-pass full-tree node count. The deepest level dominates because the branching factor exceeds one.

The comparison assumes a tree with no duplicate states, uniform branching exactly 4, unit generation cost, the goal only after all earlier depth-10 ordering positions relevant to the worst case, frames and queue records both exactly 64 bytes, and no retained global visited map. BFS can stop earlier within the goal level. DFS may retain path-local state beyond frames. A graph transposition table, variable degree, expensive generation, ordering, or repeated states changes both time and memory.

### Answer 5

Use explicit-frame DFS over one immutable namespace snapshot, with traversal state and output stored externally. Recursive DFS is inadmissible because depth is untrusted, runtime frames are not checkpointable in a portable way, and each open paginated iterator could retain a remote resource. BFS does not directly produce child-before-parent postorder and may require a very wide frontier; it can establish reachability but would need a second dependency ordering step. An explicit DFS directly implements the required nested completion.

First define identity and edges. Use stable object identity, not display path, because hard links alias paths. Decide whether symbolic links are leaves, followed only within an allowed namespace, or followed under a separate target identity; bind that policy and authorization filter to the snapshot. Carry logical child-edge identities so duplicates and link provenance are auditable. Sort children by a canonical bytewise identity or externally sort each directory's child stream; locale-dependent display order is unsuitable.

A frame contains:

$$
(\text{vertex ID},\text{page token},\text{offset in page},
\text{pending child edge},\text{status}).
$$

Keep only a bounded top segment in RAM and persist older immutable frame segments in an append-only stack store. Colors or discovery states live in an external exact key-value structure bound to the snapshot. A white target is claimed and pushed; a gray target is a link to an active ancestor and supplies cycle evidence; a black target is already complete. Whether repeated identities appear once or once per path is fixed by the output contract; “every identity” means once.

Emit a postorder record only after the final page is received, every child occurrence is classified, all tree children have emitted, and the directory frame finishes. Stream records to an immutable candidate object with sequence number and checksum. The deletion service must reauthorize against its own policy and must not treat traversal output as deletion permission.

Temporary page unavailability leaves the frame open. Retry under bounded policy and the same snapshot; if availability cannot be restored, mark the run incomplete. Empty-page and unavailable-page responses are different. Cursor tokens must be stable for the snapshot. If the remote API cannot resume them, persist the last canonical edge identity and restart the directory scan with deduplication, or reject resumability.

Checkpoint atomically at safe event boundaries. Include snapshot and policy digests, root, canonical order version, clock or sequence, external color-store generation, output length and checksum, the entire logical frame stack with cursor state, and all pending child-return events. On recovery, validate these bindings before resuming.

Validation includes:

1. every emitted identity belongs to the snapshot and appears once;
2. every nonroot discovery has a valid child-edge parent;
3. every parent is emitted after every tree child;
4. timestamps or nested event intervals satisfy the parenthesis property if retained;
5. every reachable edge was enumerated or classified under the link policy;
6. every gray edge yields a replayable alias or cycle relation;
7. external state counts and checksums reconcile with output and checkpoints;
8. no frame remains open and no page request remains unresolved;
9. bounded fixtures match an independent in-memory traversal under the same canonical order.

Measure reached identities, logical edges, maximum depth, in-RAM and external frame bytes, page requests, retry and cache rates, sort bytes, visited-store operations, cycle and alias counts, event sink throughput, checkpoint time, restart work, validation, and end-to-end latency. Retain unavailable and cancelled runs.

Publish a new plan generation atomically only after terminal empty stack, complete page coverage, exact snapshot match, checksum reconciliation, and validation. Preserve the prior generation on any failure. The result is a deterministic candidate order for that snapshot and policy, not authorization and not evidence about a later namespace revision.
