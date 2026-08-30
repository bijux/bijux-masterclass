---
module_id: DSE-056
program: Data Structures Engineering
level: 2
module_number: 56
title: Finger Trees
status: complete
last_verified: 2026-08-30
---

# Finger Trees

## One-Page Review

### Governing question

How can a persistent recursively nested 2–3 finger tree provide cheap access at both sequence ends, logarithmic concatenation and measured splitting, while preserving digit bounds, monoidal annotations, version isolation, strictness/laziness, and honest operational evidence?

### Essential definitions

- A **finger** is a position—here an end—kept near the top so operations close to it are cheap.
- A **finger tree** is `Empty`, `Single(x)`, or `Deep(measure,prefix,middle,suffix)`.
- A **digit** is a nonempty sequence of one to four elements at a `Deep` tree's left/right edge.
- A **2–3 node** groups two or three elements and carries their combined measure.
- The **middle tree** is itself a finger tree whose elements are 2–3 nodes from the level below.
- A **monoid** has an associative operation `⊕` and identity `ε`; annotations combine independent of grouping.
- A **measure** maps elements/nodes/trees into the monoid and is cached at constructed nodes/trees.
- A **view** decomposes a sequence into leftmost/rest or init/rightmost while rebuilding underfull edge structure.
- `app3(left,bridge,right)` concatenates two trees with a short bridge by packing adjacent boundary elements into 2–3 nodes and recursively joining the middles.
- A **split predicate** is normally monotone over accumulated measures so descent can choose one branch.

### Central model, mechanism, or theorem

`Deep(pr,m,sf)` denotes `flatten(pr) ++ flatten(m) ++ flatten(sf)`, where each middle element is a 2–3 node recursively flattened. Digits contain 1–4 elements and internal nodes 2–3. Adding at an end changes only its digit unless a full four-element digit overflows: keep two at the edge and push a `Node3` into the recursive middle. Because overflow recurses only after several operations at each level, end operations are amortized `O(1)` and persistent under the published analysis.

Concatenation keeps the left prefix and right suffix. It combines the left suffix, explicit bridge, and right prefix; packs this bounded boundary sequence into 2–3 nodes; recursively concatenates the middle trees. Recursion follows the logarithmic nesting depth, giving `O(log(min(n1,n2)))` under the standard model, while sharing much of both inputs.

Measurements generalize the tree. With element measure `1` and addition, annotations give sequence size and enable indexed split. With priority minimum, interval endpoints, text metrics, or other monoids, the same shape supports searches when a monotone predicate over prefix accumulation identifies a boundary. Associativity is essential because rotations/groupings change parentheses.

### Critical invariants

1. A published tree is exactly `Empty`, `Single`, or `Deep`; every `Deep` digit has 1–4 elements.
2. Every middle-tree element is a `Node2` or `Node3` of the immediately lower element type.
3. Flattening preserves logical left-to-right sequence across prefix, recursive middle nodes, and suffix.
4. Each node/tree annotation equals independent monoidal recomputation from its logical elements.
5. The measure operation is associative with identity and element measures are stable/immutable.
6. End insertion/view and concatenation preserve digit/node bounds and rebuild only changed paths/boundaries.
7. Measured split uses a predicate with the monotonicity/totality assumptions required by the search theorem.
8. Old roots/nodes/elements remain unchanged and sufficiently live; iterators and views pin their versions.
9. Size/measure overflow, lazy forcing, allocation failure, and serialization have explicit policies.
10. Performance claims state strictness, measure cost, operation mix, allocation, retention, runtime, and input shape.

### Common failures

- Allowing an empty or five-element digit in a published `Deep` node.
- Packing a boundary remainder into a singleton internal node rather than 2–3 nodes.
- Flattening middle nodes in the wrong order during views or concatenation.
- Copying stale size/priority/text annotations after reconstruction.
- Using a nonassociative combine function and expecting grouping-independent answers.
- Applying logarithmic split to a nonmonotone predicate.
- Treating a measured finger tree as a binary search tree without an ordering/search invariant.
- Implementing concatenation as repeated end insertion and claiming the paper's logarithmic bound.
- Assuming structural persistence provides deep immutability for mutable elements.
- Ignoring lazy thunk retention, integer overflow, collector pauses, or very long-lived versions.

### Compact example

Build left sequence `a..e` with costs `1..5` and right `f..j` with costs `6..10`. Concatenation yields `a..j` with measure `55`, retains the left outer prefix and right outer suffix by identity, and leaves both inputs unchanged. A cumulative-cost predicate `sum>15` splits before `f`: left `a..e` measures exactly 15, pivot `f`, right `g..j`. The executable implements real 2–3 digit overflow and recursive `app3`; its pedagogical split rebuilds from flattening and therefore does not prove logarithmic splitting.

### Connections

[DSE-015](015-doubly-and-intrusive-linked-lists.md), [DSE-018](018-deques.md), and [DSE-020](020-ropes-and-piece-tables.md) supply sequence/deque/text requirements. [DSE-037](037-fenwick-interval-and-segment-trees.md) supplies aggregates and prefix searches. [DSE-051](051-path-copying.md), [DSE-052](052-structural-sharing.md), and [DSE-053](053-persistent-lists-and-queues.md) supply persistence, sharing, and persistent amortization. The [program roadmap](../ROADMAP.md) proceeds to persistent union-find, fat nodes, vectors, snapshots, and concurrency.

## Governing Question

Which logical sequence operations, digit/node representation, monoidal annotation, view/concatenation/split algorithms, evaluation strategy, lifetime model, and evidence establish the desired persistent sequence guarantees for a concrete runtime?

## Why This Matters

Applications often need more than list or queue operations: prepend and append, inspect/remove both ends, concatenate sequences, split by index or aggregate, and preserve old versions. Ropes, editor histories, work deques, event batches, priority search sequences, interval collections, parsers, and functional language libraries all encounter this combination.

A balanced binary sequence can provide logarithmic operations, but constant-time access at both ends and elegant concatenation need more structure. Finger trees keep small digits at the edges and recursively store groups in the middle. The recursive type bootstraps shallow end operations into a balanced nested sequence without embedding parent pointers or mutation.

The measure abstraction is the decisive generalization. The same underlying tree can act as a counted sequence, priority queue, interval search structure, ordered sequence under additional invariants, or text metric tree. This reuse is safe only when the annotation forms a valid monoid and the split predicate matches its semantics.

Production correctness exceeds the algebraic shape. Strict and lazy implementations have different amortization/forcing behavior. Cached sizes can overflow. Concatenation can retain large histories. Generic measures can throw, allocate, or expose mutable state. Serialized recursive graphs can be hostile. A graduate treatment must connect the elegant derivation to these lifecycle constraints.

## Prerequisites and Retrieval

Retrieve deque contracts and end-operation evidence from [DSE-018](018-deques.md), ropes/piece-table sequence editing from [DSE-020](020-ropes-and-piece-tables.md), and prefix/range aggregation from [DSE-037](037-fenwick-interval-and-segment-trees.md). Retrieve recursive invariants and cost models from [DSE-002](002-representation-invariants.md) and [DSE-004](004-time-space-and-allocation-cost.md).

Retrieve version construction, lifetime, concurrency, and serialization from [DSE-051](051-path-copying.md); physical sharing/reachability from [DSE-052](052-structural-sharing.md); and the interaction of persistence, amortization, laziness, and real-time scheduling from [DSE-053](053-persistent-lists-and-queues.md). You should be comfortable with recursive algebraic data types, induction, monoids, amortized analysis, and snapshot semantics.

## Learning Objectives

After completing this module, you can:

1. define the `Empty`/`Single`/`Deep` representation and recursive flattening;
2. prove digit/node arity and sequence-order invariants;
3. trace prepend, append, left/right views, and recursive overflow/underflow repair;
4. derive `app3` boundary packing and concatenation structure;
5. specify monoidal annotations and identify invalid measures;
6. derive measured splitting under a monotone accumulated predicate;
7. distinguish amortized end bounds, logarithmic concatenation/split, and runtime latency;
8. design persistence, iterator, failure, concurrency, serialization, and retention contracts;
9. validate every version, annotation, arity, flattening, and sharing promise; and
10. benchmark measure work, allocation, depth, forcing, locality, retention, and tail behavior.

## Core Exposition

**Specify the sequence first.** A finite sequence supports empty, singleton, prepend `<|`, append `|>`, left/right view, concatenation `><`, iteration/fold, equality, size, indexed access/update, and split. Some derived structures add priority, ordered search, interval queries, or text offsets. Each has additional measure and semantic invariants.

Persistent operations accept roots and return roots; any old root can branch. Logical equality compares element order, not shape or root identity. Element values need immutable/copy/persistent ownership for deep snapshots. A finger tree containing a mutable text buffer preserves only its spine unless the API says otherwise.

Empty-view behavior should be total (`None`) or a named exception. Indexed operations define negative/out-of-range behavior. Concatenation preserves all left elements followed by all right elements. Iteration order is deterministic logical sequence even if internal grouping differs.

**Define the recursive shape.** At a given element type `A`:

- `Empty` contains nothing.
- `Single(a)` contains one `A`.
- `Deep(v,pr,m,sf)` has prefix/suffix digits of 1–4 `A`, and middle `m` is a finger tree over `Node A`.
- `Node2(v,a,b)` and `Node3(v,a,b,c)` group 2 or 3 adjacent `A` values.

The recursion changes element type: middle level stores nodes, whose middle stores nodes of nodes. In languages requiring regular recursive types, wrappers or encoding techniques may be needed. Never erase levels so thoroughly that validators cannot know a node's expected contents.

Flatten recursively: `flatten(Empty)=[]`; `flatten(Single x)=flattenItem(x)`; and `flatten(Deep pr m sf)=flattenDigit(pr) ++ concatMap(flattenNode,flattenTreeItems(m)) ++ flattenDigit(sf)`. At the top, `flattenItem` yields an element; at middle levels it yields the grouped lower items.

Digits ensure direct access to ends. Internal 2–3 nodes ensure recursive middle height is logarithmic in logical elements. A `Deep` cannot expose an empty digit; views that consume the last digit element must borrow a node from the middle or rebuild from the opposite digit.

**End insertion overflows slowly.** Prepending to `Empty` yields `Single`; prepending `a` to `Single b` yields `Deep([a],Empty,[b])`. If a `Deep` prefix has fewer than four elements, prepend into it. If prefix is `[b,c,d,e]`, prepend `a`, keep digit `[a,b]`, package `[c,d,e]` as `Node3`, and recursively prepend that node to the middle.

Appending is symmetric: a full suffix `[a,b,c,d]` plus `e` keeps `[d,e]` and recursively appends `Node3(a,b,c)` to the middle. Constructed measures update at the affected edge and recursive path. Old digits/tree nodes remain immutable.

The recursion frequency decreases geometrically: middle overflow occurs only after multiple lower-level overflows. The standard analysis gives amortized constant end insertion. With suitable lazy evaluation, bounds can persist under sharing as analyzed by the original structure. A strict port must ensure its evaluation/credit proof matches actual reconstruction; source resemblance is insufficient.

Each public operation may allocate digit/tree wrappers and occasionally recursive nodes. Amortized `O(1)` is not zero allocation, worst-case wall-clock, or constant retained bytes. Copying element values/measures can dominate.

**Views repair an empty digit.** Viewing left of `Single x` returns `x,Empty`. For `Deep([a,...],m,sf)`, return `a`; if prefix retains elements, rebuild `Deep(rest,m,sf)`. If prefix was `[a]`, view left of `m`. If it yields `Node2/3`, expand that node into the new prefix. If middle is empty, convert `sf` (1–4 elements) into a small tree.

Right view is symmetric. The conversion of a digit to a tree must preserve order and digit bounds. Borrowed middle nodes are expanded exactly one level; flattening them as opaque elements corrupts logical type/order. Measures recompute from new prefix/middle/suffix.

Repeated views are amortized constant under the published model. Iterator implementations can repeatedly view, or traverse with an explicit stack for lower allocation. A persistent iterator pins one root and returns a stable snapshot but can retain the entire sequence/history.

**Concatenation uses bounded boundary packing.** Directly appending every right element to left is semantically correct but linear in right length. Finger-tree concatenation uses `app3(left,xs,right)`, where `xs` is a short sequence of bridge elements at the current level.

Base cases fold bridge elements into the nonempty side and handle `Single`. For two `Deep` trees, preserve left prefix and right suffix. Concatenate `left.suffix ++ xs ++ right.prefix`. This boundary has bounded length in the ordinary top call and recursively produced calls. Partition it into `Node2`/`Node3` groups—never singleton—then recursively `app3(left.middle,nodes,right.middle)`. Return `Deep(left.prefix,newMiddle,right.suffix)`.

Any integer length at least two can be partitioned into 2s and 3s. A practical grouping rule uses `3`s until remainder `2` or `3`, but handles remainder `4` as `2+2`; a naïve all-3 greedy can leave forbidden remainder `1`. Preserve order inside/across nodes.

Recursion depth is logarithmic in the smaller tree under the standard analysis, producing the cited logarithmic concatenation bound. The result structurally shares outer digits and many subtrees, but newly packs the boundary and reconstructs recursive spines. Exact allocation depends on sizes/shapes/laziness.

Concatenation can combine version histories (confluent persistence in a broad operational sense). Repeated self-concatenation may create logical exponential size and overflow cached counts even if structural sharing limits immediate allocation. Define maximum logical size and overflow policy.

**Measures turn shape into searchable structure.** Let `(V,⊕,ε)` be a monoid and `measure:A→V`. Node/digit/tree measure folds elements in logical order. Require identity and associativity:

`ε⊕x=x=x⊕ε` and `(x⊕y)⊕z=x⊕(y⊕z)`.

Grouping changes during overflow, views, and concatenation. Associativity ensures cached measure is independent of parentheses. Commutativity is not required: text/layout summaries can be order-sensitive. Measure elements must be stable; mutable measured fields corrupt all shared annotations.

Counting uses natural-number addition and `measure(element)=1`. Cached total size enables bounds and index search. A priority sequence uses `min` with infinity identity, then searches for the first prefix meeting a priority condition. Interval structures can measure maximum endpoint. Text sequences can combine character/line metrics; order-sensitive monoids may track first/last boundary state.

Floating-point addition is not mathematically associative due to rounding. Using it as a measure can make grouping-dependent results. Either accept/document approximate shape dependence, use exact/fixed arithmetic with overflow policy, or choose a domain-specific associative summary.

**Splitting descends by accumulated measure.** Given initial accumulator `i` and predicate `p`, find the first element where `p(i⊕prefixMeasure)` becomes true. For logarithmic search, `p` must be monotone along the logical prefix sequence: once true, it remains true for subsequent prefixes (under the intended domain).

At `Deep`, test accumulated prefix measure. If target lies there, scan at most four digit elements. Otherwise add prefix measure and test through middle; recursively split middle by node measures, then scan the selected 2–3 node to locate the element. Otherwise scan suffix. Reconstruct left/right trees with helper constructors that tolerate temporarily empty edge pieces and borrow from middle.

For indexing, `V` is size and predicate `count>index`; validate nonnegative index and total size. For priority minimum, a predicate based on whether accumulated minimum meets threshold can be monotone under the chosen ordering. A predicate like “prefix sum is even” is not monotone; logarithmic branch choice is invalid.

Split returns `(left,pivot,right)` or a no-match result. Define whether pivot belongs to either side for higher-level APIs. Indexed update splits, replaces pivot, and concatenates; theoretical/constant factors depend on implementation.

**Applications add domain invariants.** A deque needs only sequence order. A counted sequence uses size measures. A priority queue finds/removes a minimum but may not preserve sorted iteration. An ordered sequence/set requires the logical elements themselves remain sorted and insertion uses measured search or another ordering scheme. Finger-tree shape alone is not a search tree.

Interval trees need interval validity and a max-end measure; query pruning uses that measure plus ordering assumptions. A rope needs chunk/text metrics, chunk-size policy, Unicode coordinate semantics, and rebalancing/compaction. Event logs need logical-size/retention constraints and durable storage beyond in-memory values.

Finger trees are general but not automatically optimal. Persistent vectors often provide better indexed constants/locality; HAMTs are better unordered maps; ropes specialize text; balanced trees specialize ordered maps. Generic node/wrapper overhead can be significant.

**Metadata and strictness are correctness concerns.** Every `Node2/3` and `Deep` cached measure derives from its immediate contents. Use trusted smart constructors across insertion, view, app3, split reconstruction, deserialization, and transformations. Validators recompute without trusting cached values.

Strict annotations avoid retaining chains of unevaluated arithmetic and ensure queries do not encounter surprising work. Lazy middle trees can support persistence-aware amortization but retain thunks/environments and shift exceptions to later operations. State which fields are strict, what forcing a view/split performs, and whether memoization is thread-safe.

Count measures use bounded machine integers in many libraries. Concatenation/replication can overflow. Silent wrap can route index split incorrectly and violate memory safety in lower-level code. Reject overflow, use wider/arbitrary integers with cost, or document a hard maximum and enforce it.

Cached hash measures need canonical element hashing and collision policy; they can speed equality/diff but do not prove equality under ordinary hashes. Pointer identity can skip shared subtrees only under immutable nodes/elements.

**Lifetime and failure follow sharing.** Tracing GC sees roots, iterators, lazy thunks, caches, and in-flight operations. Reference counting on an acyclic spine is possible but middle/digit fan-in and payload cycles/caches complicate it; destruction of deep unique structures may need iteration/deferred work. Arenas can amplify retention across shared versions.

Measure root count, logical total, unique live/allocated/reclaimed nodes/bytes, node/digit arity distributions, recursive depth, sharing fan-in, thunk/forced state, oldest reader/root, allocator/GC pauses, and retention owner. Current sequence length and sum of version lengths are both insufficient physical-memory metrics.

Construct results privately. Element/measure combine, allocation, bridge grouping, recursion, or validation can fail. Release partial nodes and preserve all inputs. Publish roots last. Lazy exceptions need memoize/retry/poison semantics. Cancellation of parallel map/concatenation/build must clean partial branches.

**Concurrency separates immutable roots from services.** Safely published roots are read-only snapshots; readers need lifetime protection. Independent writers can branch. A latest-root variable needs a lock/CAS/transaction; lost-update, retry, merge, and ABA/reclamation policies remain.

Concatenating branches does not semantically merge edits: it sequences entire left then right values and may duplicate common history. Application-level three-way merge requires stable element identities/operations and conflict policy. Do not infer collaborative editing semantics from structural concatenation.

Lazy measures/middles forced concurrently need safe once-publication. Pure recomputation can be repeated only if bounded/acceptable and exception/timing semantics permit. A mutable transient optimization—if provided—needs exclusive ownership/freeze like other persistent structures and is not a concurrent sequence.

Parallel map/fold/split can exploit recursive structure, but ordered combination and monoid associativity must hold. Deterministic results require deterministic element functions and order. Cutoffs, allocation, and GC can erase benefits.

**Serialization should preserve logical meaning.** The simplest durable format writes elements in order plus schema and rebuilds under the current implementation. It discards internal grouping/sharing and process-local laziness, which improves portability. Record measure semantics/version; recompute rather than trusting stored annotations.

A structural graph format for many roots assigns IDs/content hashes to nodes, digits, and trees. Validate tags, digit 1–4, node 2–3, recursive level/type, acyclicity, order, annotations, total size, roots, references, and quotas. Do not persist pointers, closures, thunks, locks, refcounts, or runtime type erasure.

Content addressing needs canonical encoding and may conflict with multiple valid finger-tree shapes for the same sequence. Hash logical elements for canonical sequence identity or define canonical structural construction; never assume insertion histories converge structurally. Write children before parent/root manifests, then provide checksums, flush, recovery, and reachability GC.

Element/measure schema changes require logical rebuild. Old readers/roots retain old schema until retired. Authorization applies per root/history; concatenation and old snapshots can preserve deleted/sensitive elements.

**Security and resource controls are explicit.** Bound logical size, roots/branches/readers, element bytes, measure cost/size, recursive/node count, concatenation bridge and result size, split/output, lazy thunk depth/work, serialized graph, and operation time. Reject overflow before construction/publication.

Malicious measures can be nonassociative, expensive, stateful, throwing, or huge. Restrict generic callbacks across trust boundaries or meter/isolate them. A malicious split predicate can violate monotonicity or consume unbounded time; logarithmic correctness then fails.

Hostile structural input may use empty/five-element digits, singleton internal nodes, wrong recursive levels, cycles, enormous measures, forged sizes, and duplicate references. Validate iteratively with quotas before callbacks when possible. Fuzz the decoder/invariant checker.

Timing of lazy force, shape-dependent iteration, measures, pointer sharing, and historical roots can leak activity. Do not expose internal shapes/addresses or cross-tenant shared nodes casually. Reclaim old sensitive roots according to policy.

**Evidence must cover shape transitions and measures.** Maintain an independent array/list snapshot per root. Generate prepend, append, left/right view, concatenate, branch, split/index/update, and domain searches. Compare every retained root after every operation.

Exhaust small trees to force `Empty↔Single↔Deep`, digit sizes 1–4, prefix/suffix overflow, recursive middle overflow, borrowing middle `Node2/3`, middle-empty digit conversion, and every app3 boundary length/grouping. Include concatenation with empty/single/deep, skewed sizes, self/related roots, and repeated concatenations up to limits.

Validate recursively: tags, digit/node arity, recursive level, flatten order, cached measure, total size/overflow, acyclicity, and element policy. Across roots validate old-node immutability, expected shared prefixes/suffixes/subtrees, no invalid changed-node sharing, iterator retention, and reachability accounting.

Test measures with noncommutative associative monoids, identity elements, sizes, priorities, intervals, text summaries, and deliberately invalid nonassociative/nonmonotone cases that the API rejects/documents. For split, compare all prefix accumulations with a linear oracle.

Metamorphic relations include prepend/view-left inverse, append/view-right inverse, concatenation identity/associativity by logical equality, flatten(concat)=flatten(left)++flatten(right), measure(concat)=measure(left)⊕measure(right), split-recombine restoration, index/update behavior, branch isolation, serialization rebuild equality, and compaction preservation.

Fault-inject element measure, `⊕`, predicate, every node/tree allocation, overflow, app3 grouping, split reconstruction, root CAS, serialization write/flush/publication, and reclamation. Concurrent tests race readers/writers/lazy force/release and validate the stated publication model.

Benchmarks vary size, end/view/concat/split/index/search/update mix, size skew, measure cost/width, strict/lazy policy, branch history/readers, element size, runtime/allocator/GC/refcount, threads, serialization, and comparison structures. Report latency quantiles, measure/predicate calls, recursive depth, node/digit allocations/arity, copied bytes, live/retained/reclaimed bytes, sharing, cache/TLB/branches, forcing, GC pauses, CAS retries, and validation.

The executable implements immutable generic `Empty`/`Single`/`Deep`, 1–4 digits, `Node2/3`, measured end insertion/views, and recursive `app3` concatenation. It verifies order, cost measure, shape, persistence, and outer sharing. Its split deliberately flattens/rebuilds to provide finite semantic evidence, so it does not prove the logarithmic measured-split algorithm or production amortized/runtime bounds.

<!-- bijux-verify: {"id":"measured-finger-tree-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"left=a,b,c,d,e\nright=f,g,h,i,j\njoined=a,b,c,d,e,f,g,h,i,j\njoined_measure=55\nleft_unchanged=True\nright_unchanged=True\njoined_shares_left_prefix=True\njoined_shares_right_suffix=True\nview_left=a\nview_left_rest=b,c,d,e,f,g,h,i,j\nview_right=j\nview_right_rest=a,b,c,d,e,f,g,h,i\nsplit_left=a,b,c,d,e\nsplit_pivot=f\nsplit_right=g,h,i,j\nall_invariants=True\nevidence=finite_measured_finger_tree_trace\n","stderr":""}} -->
```python
EMPTY = ("empty",)


def item_measure(item):
    return item[1]


def node(items):
    if len(items) not in (2, 3):
        raise ValueError("internal node must contain two or three items")
    return ("node", sum(item_measure(item) for item in items), tuple(items))


def tree_measure(tree):
    if tree[0] == "empty":
        return 0
    if tree[0] == "single":
        return item_measure(tree[2])
    return tree[1]


def deep(prefix, middle, suffix):
    total = (
        sum(item_measure(item) for item in prefix)
        + tree_measure(middle)
        + sum(item_measure(item) for item in suffix)
    )
    return ("deep", total, tuple(prefix), middle, tuple(suffix))


def single(item):
    return ("single", item_measure(item), item)


def push_left(item, tree):
    if tree[0] == "empty":
        return single(item)
    if tree[0] == "single":
        return deep((item,), EMPTY, (tree[2],))
    prefix, middle, suffix = tree[2], tree[3], tree[4]
    if len(prefix) < 4:
        return deep((item,) + prefix, middle, suffix)
    a, b, c, d = prefix
    return deep((item, a), push_left(node((b, c, d)), middle), suffix)


def push_right(tree, item):
    if tree[0] == "empty":
        return single(item)
    if tree[0] == "single":
        return deep((tree[2],), EMPTY, (item,))
    prefix, middle, suffix = tree[2], tree[3], tree[4]
    if len(suffix) < 4:
        return deep(prefix, middle, suffix + (item,))
    a, b, c, d = suffix
    return deep(prefix, push_right(middle, node((a, b, c))), (d, item))


def from_items(items):
    tree = EMPTY
    for item in items:
        tree = push_right(tree, item)
    return tree


def digit_tree(items):
    return from_items(items)


def view_left(tree):
    if tree[0] == "empty":
        return None
    if tree[0] == "single":
        return tree[2], EMPTY
    prefix, middle, suffix = tree[2], tree[3], tree[4]
    first = prefix[0]
    if len(prefix) > 1:
        return first, deep(prefix[1:], middle, suffix)
    middle_view = view_left(middle)
    if middle_view is None:
        return first, digit_tree(suffix)
    borrowed, new_middle = middle_view
    return first, deep(borrowed[2], new_middle, suffix)


def view_right(tree):
    if tree[0] == "empty":
        return None
    if tree[0] == "single":
        return tree[2], EMPTY
    prefix, middle, suffix = tree[2], tree[3], tree[4]
    last = suffix[-1]
    if len(suffix) > 1:
        return last, deep(prefix, middle, suffix[:-1])
    middle_view = view_right(middle)
    if middle_view is None:
        return last, digit_tree(prefix)
    borrowed, new_middle = middle_view
    return last, deep(prefix, new_middle, borrowed[2])


def pack_nodes(items):
    result = []
    position = 0
    while position < len(items):
        remaining = len(items) - position
        if remaining in (2, 3):
            width = remaining
        elif remaining == 4:
            width = 2
        else:
            width = 3
        result.append(node(items[position : position + width]))
        position += width
    return tuple(result)


def app3(left, bridge, right):
    if left[0] == "empty":
        result = right
        for item in reversed(bridge):
            result = push_left(item, result)
        return result
    if right[0] == "empty":
        result = left
        for item in bridge:
            result = push_right(result, item)
        return result
    if left[0] == "single":
        return push_left(left[2], app3(EMPTY, bridge, right))
    if right[0] == "single":
        return push_right(app3(left, bridge, EMPTY), right[2])
    boundary = left[4] + tuple(bridge) + right[2]
    middle = app3(left[3], pack_nodes(boundary), right[3])
    return deep(left[2], middle, right[4])


def concatenate(left, right):
    return app3(left, (), right)


def flatten_item(item):
    if item[0] == "node":
        result = ()
        for child in item[2]:
            result += flatten_item(child)
        return result
    return (item,)


def flatten(tree):
    if tree[0] == "empty":
        return ()
    if tree[0] == "single":
        return flatten_item(tree[2])
    result = ()
    for item in tree[2]:
        result += flatten_item(item)
    for middle_item in flatten_raw(tree[3]):
        result += flatten_item(middle_item)
    for item in tree[4]:
        result += flatten_item(item)
    return result


def flatten_raw(tree):
    if tree[0] == "empty":
        return ()
    if tree[0] == "single":
        return (tree[2],)
    result = tuple(tree[2])
    for middle_item in flatten_raw(tree[3]):
        result += tuple(middle_item[2])
    return result + tuple(tree[4])


def valid_item(item):
    if item[0] != "node":
        return len(item) == 3 and isinstance(item[1], int)
    return (
        len(item[2]) in (2, 3)
        and item[1] == sum(item_measure(child) for child in item[2])
        and all(valid_item(child) for child in item[2])
    )


def valid(tree):
    if tree[0] == "empty":
        return True
    if tree[0] == "single":
        return valid_item(tree[2]) and tree[1] == item_measure(tree[2])
    prefix, middle, suffix = tree[2], tree[3], tree[4]
    arity = 1 <= len(prefix) <= 4 and 1 <= len(suffix) <= 4
    middle_nodes = all(item[0] == "node" for item in flatten_raw(middle))
    measured = tree[1] == sum(item_measure(item) for item in flatten_raw(tree))
    return (
        arity
        and middle_nodes
        and all(valid_item(item) for item in prefix + suffix)
        and valid(middle)
        and measured
        and tree[1] == sum(item[1] for item in flatten(tree))
    )


def split_flat(tree, predicate):
    accumulated = 0
    values = flatten(tree)
    for index, item in enumerate(values):
        accumulated += item[1]
        if predicate(accumulated):
            return from_items(values[:index]), item, from_items(values[index + 1 :])
    return tree, None, EMPTY


def labels(tree):
    return ",".join(item[2] for item in flatten(tree))


items = tuple(("value", cost, label) for cost, label in enumerate("abcdefghij", 1))
left = from_items(items[:5])
right = from_items(items[5:])
joined = concatenate(left, right)
left_item, left_rest = view_left(joined)
right_item, right_rest = view_right(joined)
split_left, pivot, split_right = split_flat(joined, lambda total: total > 15)
trees = (left, right, joined, left_rest, right_rest, split_left, split_right)

print("left=" + labels(left))
print("right=" + labels(right))
print("joined=" + labels(joined))
print("joined_measure=" + str(tree_measure(joined)))
print("left_unchanged=" + str(labels(left) == "a,b,c,d,e"))
print("right_unchanged=" + str(labels(right) == "f,g,h,i,j"))
print("joined_shares_left_prefix=" + str(joined[2] is left[2]))
print("joined_shares_right_suffix=" + str(joined[4] is right[4]))
print("view_left=" + left_item[2])
print("view_left_rest=" + labels(left_rest))
print("view_right=" + right_item[2])
print("view_right_rest=" + labels(right_rest))
print("split_left=" + labels(split_left))
print("split_pivot=" + pivot[2])
print("split_right=" + labels(split_right))
print("all_invariants=" + str(all(valid(tree) for tree in trees)))
print("evidence=finite_measured_finger_tree_trace")
```

## Definitions and Notation

- `FT A = Empty | Single A | Deep(V,Digit A,FT(Node A),Digit A)`.
- `Digit A` contains one, two, three, or four ordered `A` values.
- `Node A = Node2(V,A,A) | Node3(V,A,A,A)`.
- `flatten(t)` is the top-level logical element sequence obtained by recursively expanding nodes.
- `pr` and `sf` are prefix/suffix digits; `m` is the recursively typed middle tree.
- `<|` prepends, `|>` appends, `viewL/viewR` expose ends, and `><` concatenates.
- `(V,⊕,ε)` is the annotation monoid; `μ(a)` is an element measure.
- `μ(Node/Tree)` is the ordered fold of descendant measures and is cached.
- `app3(l,xs,r)` concatenates trees around a bounded bridge at the current element level.
- `p` is a split predicate over accumulated measures; monotonicity means false-to-true changes at most once along prefixes.
- `split(p,i,t)` seeks the first element whose inclusive accumulated prefix satisfies `p`.
- **Logical size** counts flattened elements; **structural depth** counts recursive middle levels.
- A **view** result is optional `(element,remainder)`; remainder is a new persistent root.
- Retained roots, iterators, caches, thunks, and readers determine physical reachability/lifetime.

## Mechanisms, Invariants, or Proof Structure

**Flattening invariant.** Induct on tree shape. `Empty`/`Single` are direct. `Deep` concatenates digit order, recursively flattens each middle node, and suffix order. Node2/3 preserve their local order. Every operation is proved against this abstraction.

**Arity invariant.** Published digits are 1–4; nodes are 2–3. End overflow turns five edge candidates into a two-element digit plus Node3. Views borrow Node2/3 into a digit or rebuild from the opposite digit. App3 packing partitions boundary lengths into only 2/3 groups.

**Measure invariant.** Smart constructors set cached measure to the ordered monoidal fold of immediate contents. By associativity/identity and induction, it equals the flattened fold independent of recursive grouping. Every reconstruction and deserializer uses these constructors or equivalent verified logic.

**End-operation amortization.** Most operations edit one digit. Full-digit overflow recurses one level; an appropriate potential/credit counts spare digit capacity across levels. Recursive events become geometrically rarer. The proof must match persistent/lazy/strict evaluation semantics and actual views.

**Concatenation proof.** App3 base cases preserve order. Deep/deep keeps left prefix/right suffix; boundary order is left suffix, bridge, right prefix; 2–3 packing preserves it; inductive middle app3 preserves grouped order. Nesting depth bounds recursion and yields the standard logarithmic size-skew bound.

**Split proof.** Maintain accumulated measure before the current region. Use cached prefix/middle/suffix measures to identify the first region where monotone `p` becomes true, recurse/scan bounded digit/node, then reconstruct. Monotonicity makes skipped regions safe; without it, the branch decision is invalid.

**Persistence/lifetime proof.** Nodes, digits, measures, and elements are immutable under the contract. Rebuild changed edges/spines and reuse untouched pieces. Publication is last. Reclamation follows all roots/readers/thunks, not only the latest sequence.

**Evidence separation.** Sequence/order, arity/recursive type, cached measures, persistence/sharing, amortized/logarithmic complexity, laziness, reclamation, concurrency, durability, security, and production performance are independently evidenced.

## Alternatives and Trade-Offs

| Structure | Strength | Limitation relative to finger trees |
|---|---|---|
| Immutable cons list | Minimal, constant front | Linear rear/concat/index |
| Two-list persistent queue | Excellent FIFO | No general split/index/concat guarantees |
| Persistent vector/RRB tree | Strong indexing/locality; RRB concat | End/view/measure trade-offs differ |
| Rope/piece tree | Specialized text editing/chunks | Domain-specific metadata/operations |
| Balanced ordered tree | Ordered lookup/range | Sequence ends/concatenation need augmentation |
| Finger tree | General ends, concat, measured split | Generic wrapper/node overhead and complex invariants |
| Flat immutable array | Excellent traversal/locality | `Theta(n)` update/concat copying |
| Mutable deque/vector | Low constants for one current state | No cheap persistent roots without another mechanism |

Choose by actual operation mix and existing verified library support. Generality is valuable only when the application uses the measure and sequence operations.

## Failure Modes and Misconceptions

1. **Finger means arbitrary cursor:** this structure places fingers at ends; arbitrary finger-search guarantees require other invariants.
2. **Any annotation works:** nonassociative/stateful measures break grouping independence.
3. **Any predicate splits logarithmically:** nonmonotone predicates invalidate pruning.
4. **Digit/node arity is cosmetic:** empty/five digits or singleton nodes break repair/amortization.
5. **Middle items are ordinary elements:** failing to expand exactly one recursive node level corrupts sequence/type.
6. **Repeated append is logarithmic concat:** it can be linear in appended elements and does not implement app3.
7. **Cached count cannot fail:** bounded integer overflow misroutes indexed operations.
8. **Persistence covers payloads:** mutable elements/measures can change all versions.
9. **Immutable roots merge edits:** concatenation sequences branches; it is not semantic conflict resolution.
10. **Amortized equals latency SLA:** allocation, laziness, GC/refcount, and callbacks can pause.
11. **One shape per sequence:** different histories may yield logically equal but structurally different trees.
12. **Stored measures validate themselves:** independent recomputation is mandatory.

## Worked Examples

### Example 1

**Prefix overflow.** Prepend `a` to prefix `[b,c,d,e]`. New prefix is `[a,b]`; `Node3(c,d,e)` is prepended to middle. Flattened order remains `a,b,c,d,e,...`. Conclusion: five candidates become legal digit two plus legal internal node three.

### Example 2

**Suffix overflow.** Append `e` to suffix `[a,b,c,d]`. Append `Node3(a,b,c)` to middle and keep suffix `[d,e]`. Conclusion: symmetry preserves order and prevents a five-element digit.

### Example 3

**Borrow on left view.** `Deep([a], middle starting Node3(b,c,d), [e])` views `a`; middle loses that node and prefix becomes `[b,c,d]`. Conclusion: expanding the borrowed node maintains a nonempty digit and logical order.

### Example 4

**Middle-empty view.** `Deep([a],Empty,[b,c,d])` views `a`. Convert suffix into a small tree denoting `[b,c,d]`; do not publish `Deep([],Empty,[b,c,d])`. Conclusion: helper reconstruction enforces the digit invariant at boundaries.

### Example 5

**Boundary packing.** An app3 boundary has seven items. Pack `3+2+2` or `2+2+3`, preserving order. Greedy `3+3` leaves illegal singleton one. Conclusion: grouping must cover the entire boundary with only Node2/3.

### Example 6

**Counted split.** Costs/sizes are all one and index is four. Predicate `count>4` is false through four elements and true at the fifth. Split returns first four, pivot fifth, remainder. Conclusion: strict-greater predicate maps zero-based index to inclusive prefix count.

### Example 7

**Nonmonotone predicate counterexample.** Prefix sums `1,2,3,4`; predicate “sum is even” is false,true,false,true. Skipping a region because its total endpoint is false can miss an earlier true. Conclusion: cached aggregate descent cannot implement arbitrary predicate search.

### Example 8

**Noncommutative measure.** Measure each text chunk as `(length,first,last,boundaryBreaks)` and combine left-to-right. Reversing operands changes result, but associativity can still hold. Conclusion: finger-tree measures need associativity/identity, not commutativity.

### Example 9

**Persistent concatenation retention.** `C=A><B` shares outer/subtrees. Releasing `A` and `B` may not reclaim them because `C` reaches most nodes; an iterator on `A` may retain nodes no longer reached by `C`. Conclusion: logical result size and root ownership do not directly determine physical reclamation.

### Example 10

**Representation choice.** An editor needs chunk concatenation, split by UTF coordinate, line counts, and snapshots. A measured finger tree/rope can fit if the Unicode-coordinate monoid and chunk policy are proven. If workload is mostly indexed point updates, an RRB vector may offer better constants. Conclusion: choose through domain measure, operations, and benchmarks—not generality alone.

## Cross-Program Connections

- Programming languages: recursive/nested algebraic types, laziness, monoids, smart constructors, and parametric measures connect type design to cost semantics.
- Algorithm engineering: amortized end operations, logarithmic app3/split, work/span, and exact allocation require proof-aligned implementation.
- Software engineering: immutable editor/event/configuration sequences need stable element identity, snapshots, diffs, and migrations.
- Concurrent programming: immutable readers, root CAS, lazy once-publication, reader retention, and parallel folds need publication/lifetime/progress contracts.
- Database/data engineering: measured logs, ordered batches, snapshots, root manifests, and GC connect sequence structure to storage lifecycle.
- Security engineering: measure callbacks, size overflow, version pinning, hostile graph encodings, and shape/timing leakage require quotas and isolation.
- Formal methods: arity-indexed shapes, monoid laws, flattening refinement, and verified Isabelle/Coq implementations provide proof routes.
- Performance engineering: generic nodes, cached annotations, locality, allocation, laziness, GC, and size-skewed concat determine real suitability.

## References

1. Ralf Hinze and Ross Paterson, “Finger Trees: A Simple General-Purpose Data Structure,” *Journal of Functional Programming* 16(2), 2006. https://www.cs.ox.ac.uk/ralf.hinze/publications/FingerTrees.pdf
2. Cambridge University Press, publication record for Hinze and Paterson's finger-tree paper. https://www.cambridge.org/core/journals/journal-of-functional-programming/article/finger-trees-a-simple-generalpurpose-data-structure/BF419BCA07292DCAAF2A946E6BDF573B
3. Archive of Formal Proofs, “Finger Trees,” current Isabelle/HOL proof document. https://www.isa-afp.org/browser_info/current/AFP/Finger-Trees/document.pdf
4. Matthieu Sozeau, “Program-ing Finger Trees in Coq,” ICFP, 2007. https://sozeau.gitlabpages.inria.fr/www/research/publications/Program-ing_Finger_Trees_in_Coq.pdf
5. Haskell `containers`, `Data.Sequence.Internal`, current implementation source, retrieved 2026-08-30. https://github.com/haskell/containers/blob/master/containers/src/Data/Sequence/Internal.hs
6. Haskell `containers`, current immutable-collection documentation, retrieved 2026-08-30. https://haskell-containers.readthedocs.io/en/latest/intro.html
7. Clojure, `data.finger-tree`, current official repository, retrieved 2026-08-30. https://github.com/clojure/data.finger-tree
8. Clojure, `clojure.data.finger-tree` API documentation. https://clojure.github.io/data.finger-tree/index.html

## Exercises

### Exercise 1

**Trace edge operations.** Starting from an empty tree, append `a,b,c,d,e,f`, then prepend `z`. Give the first structural overflows and final logical sequence; identify which old roots remain valid/shared.

### Exercise 2

**Pack app3 boundaries.** Give a deterministic order-preserving grouping into Node2/3 for every boundary length from 2 through 12. Explain why these cover the ordinary digit-plus-bridge cases.

### Exercise 3

**Design a measured split.** Define a monoid and split predicate for locating a byte offset in immutable text chunks. State Unicode/coordinate assumptions, monotonicity, overflow, and validator/oracle evidence.

### Exercise 4

**Compare persistent sequences.** Choose among a finger tree, RRB/persistent vector, rope/piece tree, and strict two-list queue for (a) work FIFO; (b) indexed application state; (c) snapshot text editing; and (d) size-skewed concatenated batches. Give conditional decisions and benchmarks.

### Exercise 5

**Transfer to a concurrent durable event sequence.** Design how finger-tree snapshots could serve readers while commits are stored durably. Include root publication, element IDs, crash recovery, reader retention, compaction, measure migration, conflicts, and verification; distinguish what the finger tree does not provide.

## Answers to the Exercises

### Answer 1

Appending `a` gives `Single(a)`; `b` gives `Deep([a],Empty,[b])`; `c,d,e` extend suffix through `[b,c,d,e]`. Appending `f` overflows: middle receives `Node3(b,c,d)` and suffix becomes `[e,f]`, while prefix remains `[a]`. Prepending `z` makes prefix `[z,a]` without recursive overflow. Logical sequence is `z,a,b,c,d,e,f`.

Each operation returns a new root; all prior roots still flatten to their earlier sequences. The `f` version reuses the old prefix element/node values but reconstructs the outer tree and packs former suffix elements into a new Node3; the `z` version reuses the `f` version's middle and suffix by identity. Exact wrapper/tuple sharing is implementation-specific and must be measured, while immutability of old logical roots is mandatory.

### Answer 2

One deterministic grouping is: `2=2`, `3=3`, `4=2+2`, `5=3+2`, `6=3+3`, `7=3+2+2`, `8=3+3+2`, `9=3+3+3`, `10=3+3+2+2`, `11=3+3+3+2`, and `12=3+3+3+3`. Consume groups left-to-right so order is unchanged. The sum of two digits is 2–8; recursive app3 bridges can add a small Node2/3 sequence, yielding the larger bounded range. More generally, every integer at least two is a sum of 2s and 3s; handling remainder four as 2+2 prevents singleton remainder one.

### Answer 3

Choose exact nonnegative byte length with monoid `(N,+,0)` and chunk measure equal to encoded byte count. To locate zero-based byte offset `i`, require `0<=i<total` and use monotone predicate `accumulatedBytes>i`; the pivot is the chunk containing the byte, with residual offset `i-leftMeasure`. UTF-8 byte offsets may land inside a code point; either API explicitly permits bytes and validates continuation boundaries, or use a richer associative text summary for scalar/grapheme coordinates with a named Unicode version and boundary state.

Use overflow-checked wide counts and reject excessive chunks/text. Independently concatenate chunk bytes, enumerate every prefix count, and compare linear pivot/residual with tree split. Test empty/zero-length policy, multibyte code points across chunk boundaries, combining/ZWJ cases if graphemes, every digit/node transition, concatenation, branches, invalid predicates, measure exceptions, serialization rebuild, and overflow. Recompute every cached measure and validate split-recombine equality.

### Answer 4

For FIFO work, a strict two-list or proven real-time persistent queue is simpler; finger-tree generality is unnecessary unless both ends/concat/split are used. For indexed application state, a persistent vector/RRB tree usually offers better indexing/locality; benchmark update/concat needs. For snapshot text editing, a rope/piece tree or finger tree measured by text coordinates fits, contingent on chunk/Unicode measures and compaction evidence.

For size-skewed concatenated batches with later splits, finger trees provide an attractive logarithmic concat/measured split contract; an RRB vector may win if indexed traversal/locality dominates. Benchmark target size skew and operation mix, element/measure cost, allocations/copied bytes, depth, live/retained memory, cache/GC, iterator behavior, and latency quantiles. Prefer a mature verified library and do not generalize one runtime's result.

### Answer 5

Give events stable IDs and immutable canonical payloads. A writer builds a candidate persistent sequence from a committed root; a transaction/consensus/log protocol—not the finger tree—orders/conflict-checks commits. Durable storage writes canonical event records and immutable structural/logical records with checksums, children before root, then atomically publishes a commit manifest containing root, parent/version, schema, measure definition, and provenance. Recovery selects a fully valid committed root and rejects/tolerates orphan/torn data by policy.

Readers pin commit roots through leases/epochs/transactions; compaction/checkpoints rebuild equivalent sequences and retain old roots until every reader, backup, replica, and legal hold releases them. A measure/schema/Unicode change rebuilds a new generation and verifies logical events plus recomputed annotations. Reclamation traces all retained manifests. Validate arities, recursive levels, order, IDs, measures, counts, hashes, reachability, and quotas; fault-inject every write/flush/root swap and test corrupt graphs, stalled readers, authorization, cancellation, and GC interruption. The finger tree supplies immutable sequence values and efficient operations; it does not supply consensus, durability, delivery, exactly-once effects, access control, or semantic merge.
