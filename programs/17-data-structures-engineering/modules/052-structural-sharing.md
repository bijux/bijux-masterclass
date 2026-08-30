---
module_id: DSE-052
program: Data Structures Engineering
level: 2
module_number: 52
title: Structural Sharing
status: complete
last_verified: 2026-08-30
---

# Structural Sharing

## One-Page Review

### Governing question

How can immutable versions and values safely reuse common nodes as a directed acyclic graph while preserving logical equality, update isolation, hashes/metadata, bounded retention, concurrency, persistence, and honest space evidence?

### Essential definitions

- **structural sharing** reuses an immutable node/subgraph in multiple logical values or versions.
- A **sharing DAG** is the directed acyclic object graph reachable from one or more roots; fan-in greater than one records reuse.
- **hash-consing** canonicalizes nodes by content so equal node descriptors reuse one representative.
- **interning** maps a value/key to a shared canonical object, often with a process- or generation-local identity.
- **maximal sharing** reuses all equal substructures discoverable by a canonicalization scheme; persistence does not require maximal sharing.
- A **Merkle DAG** names immutable objects by cryptographic hashes of canonical content and child identifiers.
- **pointer equality shortcut** treats identical object identity as proof of equal immutable content, but unequal pointers do not prove unequal content.
- **sharing ratio** must state numerator/denominator, such as logical node occurrences divided by unique reachable nodes.
- A **weak interning table** permits canonical nodes to disappear when no external roots reference them; a strong table retains them.
- **retention dominator** is a root/cache/table whose reachability keeps a large shared subgraph alive.

### Central model, mechanism, or theorem

Structural sharing is sound when every shared node and all transitively reachable state are immutable for the lifetime of every root. Multiple incoming edges then observe identical stable content. Updating one logical value constructs replacement nodes for its changed frontier and reuses unchanged children; it never rewires a shared node. Logical values form trees conceptually, while physical storage forms a DAG.

Hash-consing computes a canonical descriptor `(tag,payload,child-identities-or-content-IDs)`, looks it up, and returns an existing node or inserts a new immutable one. This makes pointer equality imply descriptor equality within the table/generation. Correctness still requires collision-safe equality, canonical encoding, synchronized insertion, lifetime protection, and no mutable payload. Without global hash-consing, independent equal subtrees may have different objects.

Space depends on roots and sharing. For retained roots `R`, unique live nodes are `|union Reach(r)|`; logical unfolded occurrences are `sum` over paths/roots and can be much larger. Sharing reduces allocation and enables fast identity-based diffs/hashes, but one retained root or strong intern table may keep a large graph live. Reclamation and observability are therefore part of the representation.

### Critical invariants

1. Every published shared node, payload, child vector, hash, and metadata is immutable or uses explicitly isolated/versioned interior state.
2. The reachable physical graph is acyclic unless a separate cyclic-immutable representation and collector are specified.
3. Each root's logical unfolding satisfies the abstract data type even when physical nodes have multiple parents.
4. Update/rewrite creates new nodes at the changed frontier and never changes a node reachable from another root.
5. Cached hashes, sizes, depths, aggregates, and canonical descriptors derive only from immutable local payload and children.
6. Hash-cons equality confirms full canonical content after noncryptographic hash matches; cryptographic identity uses named canonical encoding/hash/collision policy.
7. Intern-table, root, iterator, cache, and reader references participate correctly in lifetime/reclamation and cannot resurrect freed nodes unsafely.
8. Serialization assigns stable object IDs/content hashes, preserves allowed sharing, validates acyclicity/references, and binds roots/schema.
9. Space/performance claims report logical occurrences, unique reachable/allocated/reclaimed nodes, table/cache retention, and exact roots/workloads.

### Common failures

- Sharing a node whose value, child array, cached lazy field, or referenced buffer remains mutable.
- Treating unequal pointers as proof of unequal logical content.
- Hash-consing on hash alone without full equality or collision-resistant content identity.
- Omitting type/schema/length boundaries from a canonical hash encoding.
- Using a strong intern table that retains every object indefinitely and calling the result memory-efficient.
- Adding parent pointers to a shared tree node and assuming one parent.
- Refcounting the DAG but forgetting roots, intern tables, iterators, caches, or cycles.
- Counting each version's logical size and reporting it as physical memory, or counting allocations without subtracting garbage.
- Persisting raw pointers or process-local intern IDs.
- Mutating through a “transient” owner token that does not actually prove uniqueness.

### Compact example

Expression `(x+y)*(x+y)+(x+y)` unfolds to eleven node occurrences. A hash-consing factory stores only `x`, `y`, `x+y`, the product, and the root: five unique objects. Building an alternate root `(x+y)*(x+y)+(x+z)` creates `z`, `x+z`, and one root, for eight unique objects across both roots. The roots share four objects—the product, `x+y`, `x`, and `y`. Evaluating with `x=2,y=1,z=4` gives 12 and 15; the original remains unchanged.

### Connections

[DSE-051](051-path-copying.md) supplies one update mechanism and version-lifetime model. [DSE-020](020-ropes-and-piece-tables.md), [DSE-034](034-treaps.md), [DSE-044](044-tries.md), and [DSE-045](045-compressed-and-radix-tries.md) provide shareable sequence/tree examples. [DSE-021](021-hash-functions-and-distribution.md) through [DSE-030](030-engineering-a-memory-efficient-hash-map.md) supply hash-table/equality foundations. [DSE-050](050-choosing-representations-for-large-graphs-and-text.md) supplies byte/retention evidence discipline. The [program roadmap](../ROADMAP.md) proceeds to persistent balanced trees, HAMTs, vectors, and versioned storage.

## Governing Question

Which repeated substructures are safe and valuable to share, which canonicalization scope and equality/hash scheme should discover them, which roots/tables/readers own them, and how will updates, reclamation, concurrency, persistence, security, and measurements preserve the sharing contract?

## Why This Matters

Structural sharing is why persistent structures can preserve many versions without copying every element. It also powers compiler expression DAGs, common-subexpression representation, immutable syntax trees, ropes, HAMTs, persistent vectors, content-addressed stores, deduplicated configuration, version control, and incremental build graphs.

Sharing changes a tree into a DAG. Algorithms that assume one parent, destructive traversal, or unique ownership become wrong. One mutable payload corrupts multiple values. Reference counting must account for fan-in. A tiny retained root can dominate a large subgraph. Recursive serialization may duplicate shared nodes. Pointer equality becomes useful but only in one direction.

Canonical sharing is not free. Hash-consing computes hashes/descriptors, performs table lookups, stores table entries, synchronizes concurrent creators, and can worsen locality. Equal substructure frequency and size determine benefit. Random/high-entropy data may yield little reuse. Strong global interning can become a memory leak and cross-tenant side channel.

At storage scale, Merkle DAGs make sharing durable and verifiable, but demand canonical encoding, collision policy, object reachability GC, root manifests, and authenticated provenance. This module develops sharing as a full lifecycle contract rather than a visual trick.

## Prerequisites and Retrieval

Retrieve persistence levels, path-copy proofs, identity, lifetime, concurrency, serialization, and benchmarks from [DSE-051](051-path-copying.md). Retrieve invariants/failure from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), allocation/locality from [DSE-004](004-time-space-and-allocation-cost.md) and [DSE-006](006-memory-locality-and-cache-behavior.md), hashing/equality from [DSE-021](021-hash-functions-and-distribution.md), and testing/measurement from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical unfolding, physical DAG, allocation graph, and retained live graph;
2. prove sharing is safe under transitive immutability and root lifetime;
3. design collision-safe hash-consing and scoped interning;
4. use pointer identity and cached hashes as sound one-way equality/diff shortcuts;
5. maintain metadata and rewrites in DAGs without parent/unique-ownership assumptions;
6. choose strong/weak tables, tracing GC, reference counts, epochs, arenas, and root policies;
7. specify transient/edit-token uniqueness without mutating shared nodes;
8. serialize and validate ID-based or Merkle sharing graphs and roots;
9. prevent retention, hash-flooding, cross-tenant, and graph-parser abuse; and
10. measure logical/unique/allocated/reclaimed/retained nodes, sharing benefit, and overhead.

## Core Exposition

**Separate logical value from physical topology.** A mathematical expression is usually described as a tree: each occurrence has one parent. If the same subexpression occurs three times, the logical unfolding contains three occurrences. An immutable implementation can represent them with one node reached through three edges. The physical object graph is a DAG.

An ordered map/version similarly appears as a tree per root, while many roots share subtrees. A rope can reuse leaves/chunks. HAMTs share unchanged branches. A compiler DAG can reuse common pure expressions. A content-addressed store reuses objects with identical canonical bytes across commits.

Algorithms must choose their domain. Evaluating the expression visits occurrences unless memoizing by node; counting unique nodes visits objects once; rendering source may need unfold each incoming occurrence; serialization should often write each object once and root/edge IDs. A generic “node count” is ambiguous.

Define `Reach(r)` as unique physical nodes reachable from root `r`. For roots `R`, physical reachable set is their union. Logical unfolded occurrence count counts every path occurrence; with sharing it can be exponential in DAG nodes for certain constructions. Traversal APIs state whether they visit nodes or occurrences and how they handle cycles/malformed graphs.

Sharing is semantically invisible for pure immutable values: replacing several equal subtrees with one does not change outputs. It can be observable through pointer identity, timing, memory, weak-reference lifetime, caches, or debugging; keep those outside logical equality unless explicitly part of API.

**Transitive immutability is the safety proof.** A shared node's tag/payload/children cannot change. Neither can mutable objects referenced by payload unless they are copied, persistent, synchronized under weaker snapshot semantics, or excluded. “Final pointer” to a mutable list is not an immutable node.

Suppose roots `r1,r2` share node `s`. Any query reaching `s` observes the same stable content. Updating `r1` constructs a replacement frontier and may continue referencing `s` if unchanged; it never writes `s`, so `r2` remains unchanged. This is the core proof.

Lazy memo fields introduce interior mutation. A cached hash/value can be safe if computed deterministically from immutable content, published race-free, and logically invisible. It still complicates memory ordering, data races, serialization, and byte accounting. An error/partial cache state must not corrupt results. Eager precomputation is simpler.

Parent pointers conflict with multiple parents. Store no parent, keep traversal stacks, maintain version-local external parent maps, or explicitly represent parent sets with update/lifetime costs. Algorithms using parent for balance/navigation should copy/recompute external context rather than overwrite a shared child.

Sharing mutable synchronization primitives/loggers/counters can also leak between versions. Per-node reference counts are lifecycle state with careful atomic semantics; query statistics belong outside logical nodes. Tenant-sensitive cache state can create side channels.

**Path copying creates history-based sharing.** DSE-051 copies update frontiers and reuses untouched children by identity. Sharing occurs because a new version descends from an old one. Equal subtrees built independently need not share. This local scheme avoids a global canonical table and preserves update complexity.

Maximal/canonical sharing tries to merge independently equal subgraphs. Hash-consing is one technique. It can reduce more memory and make identity-based equality powerful, but adds hashing/table/lifetime contention. The best scope may be one build, compiler function, tenant, document, generation, thread, or process rather than global.

Hybrid schemes path-copy normally and hash-cons during batch compaction/serialization. This moves canonicalization off the update latency path and can improve locality. A persistent file content-addresses nodes while in-memory hot structures share only by history.

Sharing granularity matters. Interning individual tiny integers/strings can cost more table/header memory than saved. Sharing large repeated subtrees/chunks/pages has greater benefit. Page-level copy-on-write duplicates an entire page for one changed byte but keeps storage/recovery manageable. Measure bytes and churn.

**Hash-consing canonicalizes descriptors.** Define a node descriptor including type/domain tag, payload/key/value, arity/length, and ordered child canonical identities. Compute a table hash, look up candidates, and compare full descriptor equality. If equal, return existing immutable node; otherwise allocate/insert one.

Noncryptographic hash collisions are routine and handled by equality. Never equate on hash alone. The equality comparison must be pure, bounded under threat model, and include schema/type boundaries. Child identity works only because children are already canonical in the same table; alternatively compare child content IDs.

Bottom-up construction naturally canonicalizes children before parents. Cyclic graphs cannot use this simple DAG recursion. Mutually recursive structures need a different fixed-point/cycle representation. Detect cycles in imported graphs.

Concurrent `intern(descriptor)` must return one representative if canonical identity promises it. Use a locked table, per-bucket locks, atomic insertion with winner/loser cleanup, or tolerate duplicates and weaken maximal identity. A check-then-insert race creates two equal nodes. Logical correctness can remain, but pointer-equality/maximal-sharing claims fail.

Factory publication initializes node fully before table/root readers see it. The table's key must not borrow temporary/mutable buffers. Removing a weak table entry races acquisition/reclamation; managed weak references or protected upgrade protocols are required.

Hash flooding/adversarial equality can make interning quadratic or contentious. Use keyed hashes where appropriate, bounds, tenant scopes, and fallback. A cryptographic content hash has different cost/threat properties and still needs canonical bytes.

**Canonical identity changes equality and diff, carefully.** If two references are identical, immutable content is equal. Return immediately from equality, diff, hash, or merge. If references differ, content may still be equal unless maximal canonicalization under the same live table/schema is guaranteed.

Cached structural hashes can reject equality when hashes differ. Equal hashes require recursive/full equality unless collision-resistant content identity is accepted under policy. Store domain-separated hash of tag, lengths, canonical payload, and ordered child hashes. An unordered map/set needs canonical child ordering or commutative canonical encoding.

Diff of versions walks corresponding nodes. Identity skips shared subtrees; hash equality may skip content-equal independently allocated subtrees under cryptographic policy; otherwise recurse. Output complexity depends on changed frontier plus emitted differences when structures align, but adversarial shapes/equal-content-different-layout can cause more work.

Memoizing evaluation by node identity changes work from logical occurrences toward unique nodes and is valid for pure context-independent functions. Context-dependent evaluation, occurrence position, environments, short-circuit effects, or resource accounting may require per-occurrence work/cache keys including context.

Pointer addresses are process-local and can be reused after reclamation. Never persist or expose them as stable content/version IDs. Debug identities should include generation or opaque tokens.

**Metadata belongs to the node descriptor.** Subtree size, height, hash, bounds, aggregate, leaf count, and balance derive from children/payload. If they affect semantics/validation, compute deterministically and include/verify them. Two content-equal nodes with different stale metadata must not be canonicalized as equal while queries use metadata.

Some metadata is a cache and excluded from content identity. Specify recomputation, publication, and validation. Weak caches referencing parents/other nodes can create retention/cycles. Store large indexes externally keyed by content/generation when appropriate.

Augmented persistent updates construct changed nodes with new metadata. Shared children retain valid metadata because immutable. Hash-consing can reuse a node only after all descriptor fields normalize. Floating aggregates may be order-dependent; canonical tree shape/order is needed for deterministic content identity.

Node arity/order is important. A rope concatenation tree with equal flattened text but different balancing is logically equal as text yet structurally different. Hash-consing raw nodes will not merge the roots. Canonical rebalancing or content chunking can deduplicate more but costs. Define structural versus extensional equality.

HAMT collision nodes and bitmap-indexed child arrays have canonical ordering/bitmap rules; otherwise equal maps can have different nodes. Persistent vectors have branching/tail and shape rules. Subsequent modules deepen these formats.

**Space accounting must include the table and retention.** Let logical occurrences be 1,000,000 and unique nodes 100,000; occurrence/unique sharing factor is 10. This does not mean 90% total bytes saved. Add node sizes, edges, payloads, intern-table buckets/keys/weak wrappers, hashes, allocators, roots, caches, GC/refcounts, fragmentation, and temporary construction.

Report allocated cumulative nodes, currently reachable unique nodes, garbage waiting for GC/epoch, reclaimed nodes, table entries/capacity, logical occurrences, roots, and bytes. A factory that allocated losing race candidates has more allocations than unique nodes. A tracing heap includes unreachable until collection.

Retention attribution is difficult because shared nodes have many owners. Dominator analysis can identify roots/tables whose removal frees nodes, but with multiple roots no single one dominates shared nodes. Measure marginal retained bytes per root/set, root ages, readers, cache owners, and generation DAG.

A strong intern table itself is a root and prevents collection, even after all logical versions release. Use bounded/evicting tables, weak entries, generation-local tables destroyed together, or explicit compaction. Eviction only reduces future canonical reuse; it cannot free nodes still referenced elsewhere.

Weak interning allows table entries to vanish. Later equal construction may produce a new canonical object, so canonical pointer identity is temporal, not global forever. Equality code must remain correct. Concurrent weak upgrade must prevent returning a node being finalized.

**Reclamation handles DAG fan-in.** Tracing GC naturally marks from all roots and collects unmarked DAG nodes/cycles, with pause/throughput/heap trade-offs. Reference counting stores incoming-reference count from nodes plus roots/readers/tables. Removing an edge/root decrements and recursively frees at zero. DAG fan-in is supported, cycles are not.

Hash-cons tables complicate refcounts: a strong table adds a reference; weak table needs safe nonowning reference. Atomic refcounts add contention; batching/deferred destruction helps. Counts can overflow under extreme fan-in/version creation; define saturation/error.

Epoch/RCU protects readers of published roots/tables, but deciding which shared nodes are no longer referenced across newer roots still needs tracing/refcounts/arena ownership. Arena generations are efficient when sharing stays within/ancestry-tracked arenas; cross-arena edges create dependency DAGs and coarse retention.

Content-addressed stores perform reachability GC from retained root manifests. Concurrent writers/readers and distributed replicas require mark roots/snapshots, grace periods, tombstones, and race-safe sweep. Missing a root deletes live history; retaining every root leaks storage.

Reclamation work can be unbounded when releasing a root makes a huge unique subgraph unreachable. Defer/incrementalize destruction and include tail latency. Recursive free on deep DAG paths risks stack overflow.

**Transients exploit uniqueness but must not break sharing.** A transient builder may mutate a node if it knows no immutable root or other transient references it and its edit token/owner matches. Otherwise copy. Hash-consed nodes are generally shared/immutable and never editable in place merely because a language reference count appears one—the intern table/weak races and canonical identity matter.

Freeze validates, revokes edit token, and optionally interns/canonicalizes nodes. If interning replaces a transient node with an existing canonical node, parent construction uses returned representative. After freeze, transient methods fail and no editable aliases remain.

Reference-count uniqueness optimizations are race-sensitive and can be invalid with weak/untracked raw references. Type/ownership systems can enforce uniqueness better, but interior mutability, foreign code, and unsafe paths need audit. Thread confinement or synchronized handoff is explicit.

Batch hash-consing may build in a private table, then publish root/table generation. On failure/cancel, discard private graph. Merging canonical tables across tenants/generations can reveal equality and complicate lifetime; often avoid.

**Concurrency favors immutable nodes, not necessarily canonical tables.** Read-only traversal is race-free after safe root/node publication and lifetime pinning. Multiple roots can publish atomically. Writers build private nodes and CAS/lock root registries as in DSE-051.

The intern table is mutable shared state. A global lock serializes creation; striped locks reduce contention; concurrent maps still need canonical winner handling and safe reclamation. Duplicate-tolerant interning may improve throughput and retain logical correctness while reducing identity shortcuts. State the guarantee.

Cached hashes/lazy values need once/publication semantics. Two threads redundantly computing the same pure cache is logically okay only without data races and with safe value publication. Error caching and cancellation rules matter.

Cross-tenant global canonical nodes can leak equality through timing, reference counts, memory, cache effects, or content IDs. Scope tables/keys by tenant/security domain, salt hashes, or accept/document threat. Shared public constants differ from secret content.

Lock-free table algorithms depend on memory reclamation; a bucket can point to a removed/reused node. Managed GC, hazards, epochs, or tagged protocols are required. Hash-consing throughput benchmarks include creator contention and readers, not just lookup.

**Merkle DAGs make sharing durable.** Canonically encode `(domain/schema,tag,payload lengths/bytes,ordered child content IDs)`, hash it, store object under hash, and root manifests name content IDs. Equal encoded objects deduplicate across versions/stores. Child IDs make object immutable; changing one leaf creates new hashes on ancestors, sharing untouched objects.

Cryptographic hashes make accidental/malicious substitution detectable under named assumptions, but collision risk is a policy, not mathematical impossibility. Domain separation prevents a blob/node ambiguity. Canonical serialization must define integers, Unicode/bytes, ordering, maps, floats/NaNs, versions, and extensions.

Git object storage and IPFS-style Merkle DAGs illustrate content-addressed objects and roots, but their exact object/domain/trust/lifetime semantics differ. Do not infer application authorization, confidentiality, transactional atomicity, or GC automatically.

Write child objects before/root manifests; verify hashes on load; authenticate/authorize roots; validate object types, arity, sizes, DAG acyclicity/depth/work, and semantic invariants. A valid hash graph can encode an invalid BST/expression/schema.

Garbage collection starts from retained/leased roots, traverses IDs, and deletes unmarked objects only under race-safe generation protocol. Distributed GC must account for replicas/in-flight roots. Pin legal/audit/backup roots explicitly and measure storage.

Graph serialization without content hashes can assign sequential IDs once per object, write records, then roots. It preserves sharing but not canonical identity across files. Validate references and reject cycles/duplicates/schema mismatches. Logical per-version serialization is simpler but duplicates content.

**Ropes, HAMTs, vectors, and compilers reveal different sharing.** A rope shares immutable text leaves and concatenation subtrees across edits/slices. Rebalancing may copy/reshape nodes while leaves share. Tiny slice retaining a huge backing buffer is a retention hazard; substring/view policy matters.

HAMTs share all branches outside hash-fragment path. Bitmap-indexed nodes pack sparse children; hash collisions require explicit nodes/equality. Canonical shape depends on hash/equality and insertion/collision rules. Bagwell's ideal hash trees and modern implementations illustrate the trade-offs.

Persistent vectors share wide tree prefixes/branches and use a tail. An append normally copies a shallow path and possibly promotes tail; transient edit tokens batch efficiently. Branching factor trades path depth, copied node width, cache, and wasted slots. Clojure's implementation provides one concrete contract.

Compiler expression DAGs hash-cons pure typed nodes. Source locations/debug occurrence metadata often cannot live in the shared semantic node because identical expressions occur at different places; store occurrence annotations externally. Effectful or exception-order expressions cannot be merged solely by syntax.

Build systems and version control share content-addressed file/tree objects. Environment/tool/configuration belongs in action/object identity; omitting it incorrectly reuses stale output. Sharing is sound only when descriptor includes every semantic dependency.

**Security and reliability constrain canonicalization.** Untrusted data can create enormous DAG fan-in/depth, many near-equal nodes, hash collisions, expensive equality, table churn, or root retention. Bound nodes, arity, payload, depth, roots, table capacity/load, construction work, equality bytes, versions, reader age, and serialized expansion.

Hash-consing sensitive content globally leaks equality. Content hashes reveal dictionary-guessable content. Use security-domain scoping, keyed/encrypted identifiers, access controls, and threat review. Encryption can defeat cross-object deduplication or introduce convergent-encryption leakage.

Canonical parsers validate length/overflow before allocation, object/hash/reference counts, cycles, decompression, and semantics. Avoid recursive traversal of hostile depth. Limit diagnostics and never print secret DAG content/IDs indiscriminately.

Hash collision attacks on noncryptographic tables use keyed/randomized hashes and bounded fallback. Cryptographic hash algorithm migration needs versioned IDs and dual/rebuild strategy. Do not reinterpret old IDs under a new canonical encoding.

Root deletion is destructive even if objects are immutable. Retention policy, authorization, grace/backup, audit, and recoverable manifests apply. Memory pressure must not silently drop durable user versions.

**Evidence measures both semantics and sharing.** Compare each root's logical unfolded value to an independent nonsharing reference. Generate branching histories/expressions, rewrites, equal independent construction, insertion orders, and release sequences. Old roots must remain unchanged.

Validate DAG globally: node immutability/type, acyclicity, child IDs/objects, metadata/hashes, logical invariants, root reachability, and table descriptor equality. White-box tests verify expected identity reuse where guaranteed, while logical tests never require maximal sharing unless API promises it.

For hash-consing, force hash collisions, concurrent same-descriptor creation, losing-candidate cleanup, weak entry collection/recreation, table resize/eviction, and payload/schema distinctions. Differentially compare canonical and duplicate-tolerant modes. Verify pointer shortcuts never cause false equality.

For lifetime, release every combination of roots/readers/caches/tables; compare tracing/reference counts/reachable oracle; test cycles if supported/rejected; stalled readers; deep destruction; counter overflow; arena dependencies; and root GC races. Use sanitizers/leak tools.

Metamorphic properties include unfolding shared versus duplicated DAG yields equal results; intern twice returns same object within guarantee scope; dropping maximal sharing preserves logic; rewrite one root leaves sibling; content-addressed encode/decode preserves ID; order-independent canonical map encoding; compaction preserves roots; and diff/apply round trip.

Fault-inject node/table/hash/cache/refcount/root/file/object/manifest allocations and writes. Crash-inject child-before-root and GC phases. Concurrency histories cover publication, intern races, weak reclamation, cache once, and root release/acquisition.

Benchmarks vary repetition, subtree size, DAG fan-in/depth, roots/history/branching, update locality, values, table scope/load, hash/equality, weak/strong, GC/refcount/arena, threads, transients, serialization, and retention. Measure logical/unique/allocated/reclaimed/table/cache/retained bytes and nodes; sharing ratios; hashes/equality/table probes; copied nodes; latency quantiles; allocator/cache/TLB/GC/reclamation; contention; serialize/load/GC; and failure cleanup.

The executable below hash-conses immutable expression tuples by full descriptors. It compares logical unfolded occurrences with unique objects, builds an alternate root sharing the product subtree, evaluates both, and validates acyclicity, factory canonicality, and exact hashes/descriptors. It does not prove memory reclamation, weak tables, concurrency, cryptographic identity, persistence, transient uniqueness, security, or production performance.

<!-- bijux-verify: {"id":"structural-sharing-dag-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unique_base_nodes=5\nunfolded_base_occurrences=11\nshared_xy_refs=3\nintern_reuses_xy=True\nbase_value=12\nalternate_value=15\nbase_unchanged=True\nbase_alt_share_mul=True\nroots=2\nunique_across_roots=8\nunfolded_across_roots=22\nobjects_in_both_roots=4\nall_invariants=True\nevidence=finite_structural_sharing_dag_trace\n","stderr":""}} -->
```python
table = {}


def intern(tag, payload=None, children=()):
    descriptor = (tag, payload, children)
    existing = table.get(descriptor)
    if existing is not None:
        return existing
    table[descriptor] = descriptor
    return descriptor


def variable(name):
    return intern("var", name)


def binary(operator, left, right):
    return intern(operator, None, (left, right))


def evaluate(root, environment):
    tag, payload, children = root
    if tag == "var":
        return environment[payload]
    left = evaluate(children[0], environment)
    right = evaluate(children[1], environment)
    return left + right if tag == "+" else left * right


def occurrence_count(root):
    return 1 + sum(occurrence_count(child) for child in root[2])


def occurrence_refs(root, counts):
    counts[id(root)] = counts.get(id(root), 0) + 1
    for child in root[2]:
        occurrence_refs(child, counts)


def reachable(root):
    found = {}
    stack = [root]
    while stack:
        current = stack.pop()
        if id(current) in found:
            continue
        found[id(current)] = current
        stack.extend(current[2])
    return found


x = variable("x")
y = variable("y")
xy = binary("+", x, y)
product = binary("*", xy, xy)
base = binary("+", product, xy)
base_nodes = reachable(base)
base_refs = {}
occurrence_refs(base, base_refs)

z = variable("z")
xz = binary("+", x, z)
alternate = binary("+", product, xz)
alternate_nodes = reachable(alternate)
all_nodes = dict(base_nodes)
all_nodes.update(alternate_nodes)


def validate(roots):
    visiting = {}
    visited = {}

    def visit(current):
        identity = id(current)
        if identity in visiting:
            return False
        if identity in visited:
            return True
        visiting[identity] = True
        tag, payload, children = current
        if tag == "var":
            valid_local = isinstance(payload, str) and children == ()
        else:
            valid_local = tag in {"+", "*"} and payload is None and len(children) == 2
        if not valid_local or table.get(current) is not current:
            return False
        if not all(visit(child) for child in children):
            return False
        del visiting[identity]
        visited[identity] = True
        return True

    return all(visit(root) for root in roots)


environment = {"x": 2, "y": 1, "z": 4}
print(f"unique_base_nodes={len(base_nodes)}")
print(f"unfolded_base_occurrences={occurrence_count(base)}")
print(f"shared_xy_refs={base_refs[id(xy)]}")
print(f"intern_reuses_xy={binary('+', x, y) is xy}")
print(f"base_value={evaluate(base, environment)}")
print(f"alternate_value={evaluate(alternate, environment)}")
print(f"base_unchanged={evaluate(base, environment) == 12}")
print(f"base_alt_share_mul={base[2][0] is alternate[2][0]}")
print("roots=2")
print(f"unique_across_roots={len(all_nodes)}")
print(f"unfolded_across_roots={occurrence_count(base) + occurrence_count(alternate)}")
print(f"objects_in_both_roots={len(set(base_nodes) & set(alternate_nodes))}")
print(f"all_invariants={validate([base, alternate])}")
print("evidence=finite_structural_sharing_dag_trace")
```

## Definitions and Notation

For root `r`, `Reach(r)` is its unique physical reachable nodes. For roots `R`, live union `U=union Reach(r)`. `Occ(r)` is logical unfolded occurrences, counting a shared node once per path occurrence. Sharing factor may be `sum Occ(r)/|U|`; report node/byte variant and root set. Fan-in is incoming physical references.

A node descriptor is canonical `(domain,schema,tag,payload,arity,ordered child identities/IDs)`. Structural equality compares descriptor graphs; extensional equality may ignore shape (for example rope text). An intern scope/generation defines the pointer-canonical guarantee. A Merkle content ID hashes canonical bytes, not runtime addresses.

## Mechanisms, Invariants, or Proof Structure

Sharing safety is transitive immutability plus lifetime. Logical correctness unfolds the DAG into the expected ADT tree/value. Hash-cons correctness proves descriptor equality and synchronized representative insertion; hashes are only filters/IDs under collision policy. Metadata correctness follows immutable children. Memory correctness traces all roots/tables/readers/caches and reclaims only outside their union.

Concurrency adds safe publication, canonical-table race semantics, and reclamation. Persistence adds canonical encoding/content IDs or object IDs, acyclicity/reference/semantic validation, child-before-root commit, and root-based GC. Measurements separate logical, unique, allocation, garbage, table, and retained costs.

## Alternatives and Trade-Offs

| Sharing method | Strength | Principal cost/restriction |
|---|---|---|
| history/path sharing | low update overhead/local reasoning | misses independently equal subtrees |
| strong hash-consing | maximal scoped identity reuse | table contention and permanent retention |
| weak hash-consing | reuse without table-owned lifetime | weak acquisition/recreation complexity |
| batch canonicalization | off hot path and compact output | temporary duplicate graph/rebuild work |
| content-addressed Merkle DAG | durable dedup/integrity | canonical encoding/hash/object GC |
| copy-on-write pages/chunks | coarse operational sharing | write amplification for small changes |
| no canonical sharing | simple ownership/locality | duplicate equal content and slower diffs |

Choose based on repetition/granularity, equality/diff needs, update/build path, security domain, lifetime, concurrency, serialization, locality, and measured table overhead.

## Failure Modes and Misconceptions

- A logical tree can be a physical DAG; algorithms must state node versus occurrence traversal.
- Persistence does not require maximal sharing, and maximal sharing is not always cheaper.
- Pointer equality proves equality only for immutable objects; pointer inequality usually proves nothing.
- Hash equality is not full equality unless a named cryptographic content-ID policy accepts collision risk.
- Shared node immutability includes payloads, child containers, and logically visible caches.
- Strong canonical tables are hidden roots and can dominate retention.
- Refcount/GC/epoch/arena correctness depends on all incoming roots and cycles.
- Structural equality differs from extensional equality for ropes/maps with alternate shapes.
- Content addressing provides integrity/dedup, not authorization/confidentiality/transactions automatically.
- Finite sharing ratios do not establish net byte or production-latency benefit.

## Worked Examples

### Example 1

Three occurrences of `x+y` share one node, but an evaluator without memoization visits it three times because logical occurrences matter. A pure memoized evaluator computes it once.

### Example 2

Two independently built equal BST subtrees may have different pointers under path copying. Equality cannot return false solely from pointer difference; recursive/content comparison is needed.

### Example 3

A hash-cons table sees the same `(+,x,y)` descriptor twice and returns one object. A forced table-hash collision with `(+,x,z)` must perform full descriptor comparison and keep both.

### Example 4

A strong table retaining one million nodes reports no external roots but frees nothing. Weak/generation-local/bounded tables change retention at the cost of canonical identity continuity.

### Example 5

A rope slice sharing one small leaf may also retain a huge backing buffer or arena. Logical slice bytes and retained physical bytes diverge; copying the slice can reduce retention.

### Example 6

A cached subtree hash excludes source-location metadata in a shared compiler expression. Occurrence locations live externally; otherwise identical pure expressions at different source spans cannot share.

### Example 7

Two threads concurrently intern one descriptor. If both publish separate nodes, logical values remain correct but maximal pointer canonicality fails. A winner protocol and loser cleanup uphold the stronger contract.

### Example 8

Releasing one version root may reclaim nothing because a sibling root reaches all its nodes. Marginal/root-dominator measurements explain retention better than dividing nodes evenly among versions.

### Example 9

A Merkle node hash includes domain, type, payload lengths/bytes, and ordered child hashes. Omitting lengths can make different concatenations encode identically; omitting schema permits reinterpretation.

### Example 10

A valid content hash proves object bytes match the ID, but a malicious DAG may be cyclic, enormous, or violate BST order. Semantic and resource validation remains mandatory.

## Cross-Program Connections

- **Functional programming:** persistent collections, immutable values, hash-consing, memoization, transients, and structural equality rely on sharing.
- **Compilers:** AST/IR DAGs, common subexpressions, occurrence annotations, incremental recomputation, and typed hash-consing are direct uses.
- **Storage/version control:** copy-on-write pages, Merkle trees/DAGs, commits/roots, deduplication, reachability GC, and crash publication extend sharing durably.
- **Concurrent programming:** immutable readers, intern-table races, cached hashes, weak references, ABA, refcounts/epochs, and stalled roots shape safety.
- **Security engineering:** hash flooding/collisions, cross-tenant equality leaks, content-ID guessing, DAG bombs, provenance, and root deletion matter.
- **Performance engineering:** sharing granularity, table probes, allocator/locality, retained bytes, GC/reclamation, and occurrence-versus-node work determine value.
- **Testing/reliability:** unfolded references, collision forcing, root-release matrices, canonical encode/decode, crash/GC races, and exact evidence labels are reusable.

## References

1. [James Driscoll, Neil Sarnak, Daniel Sleator, and Robert Tarjan, *Making Data Structures Persistent*](https://www.cs.cmu.edu/~sleator/papers/making-data-structures-persistent.pdf).
2. [Chris Okasaki, *Purely Functional Data Structures* thesis](https://www.cs.cmu.edu/~rwh/students/okasaki.pdf).
3. [Phil Bagwell, *Ideal Hash Trees*](https://lampwww.epfl.ch/papers/idealhashtrees.pdf).
4. [Hans-J. Boehm, Russ Atkinson, and Michael Plass, *Ropes: An Alternative to Strings*](https://www.cs.tufts.edu/~nr/cs257/archive/hans-boehm/ropes.pdf).
5. [Git, *Git Objects*](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects).
6. [IPFS documentation, *Merkle DAGs*](https://docs.ipfs.tech/concepts/merkle-dag/).
7. [Rust `im` crate documentation](https://docs.rs/im/latest/im/).
8. [Clojure, maintained `PersistentVector` implementation](https://github.com/clojure/clojure/blob/master/src/jvm/clojure/lang/PersistentVector.java).

## Exercises

### Exercise 1

For expression `(a+b)*(a+b)+(a+b)*(a+c)`, draw the maximally hash-consed DAG, count unfolded occurrences and unique nodes, and identify nodes shared between the two product subexpressions.

### Exercise 2

Prove collision-safe bottom-up hash-consing yields one representative per descriptor within one locked table scope. State why it does not necessarily yield one representative per extensional logical value.

### Exercise 3

Design retention/reclamation for a multi-threaded version DAG with strong/weak intern tables, iterators, caches, and content-addressed persisted roots. Include observability and quotas.

### Exercise 4

Specify canonical Merkle encoding and validation for an immutable typed expression DAG with maps, byte strings, integers, and optional source annotations.

### Exercise 5

Design evidence and benchmarks comparing history-only sharing, weak hash-consing, strong hash-consing, and batch content-addressed canonicalization. State prohibited conclusions.

## Answers to the Exercises

### Answer 1

Unique leaves are `a,b,c`. Unique additions are `ab=(a+b)` and `ac=(a+c)`. Products are `p1=ab*ab` and `p2=ab*ac`; root is `p1+p2`: eight unique nodes. Unfolded occurrence count: root one; two products two; their four add occurrences (`ab` appears three, `ac` once); each add has two leaves, eight leaf occurrences—total `1+2+4+8=15`. Nodes `ab` and `a` are shared across both product subgraphs; within `p1`, `ab` (and its a/b descendants) appears twice. Physical fan-in counts differ from logical occurrences.

### Answer 2

Induct bottom-up. Leaves have complete canonical descriptors; under one locked lookup/insert, the first equal descriptor inserts and every later full-equal descriptor finds/returns it. For internal nodes, children are already canonical by induction, so equal ordered descriptors contain identical child representatives; collision-safe table lookup compares tag/payload/arity/children fully and one locked insertion chooses one representative. Hash collisions with unequal descriptors remain separate. The result is descriptor canonicality, not extensional value canonicality: different balanced rope shapes can flatten to the same text, different map shapes/orders can denote the same mapping, and metadata intentionally included in descriptors can distinguish otherwise equal values.

### Answer 3

Treat version roots, active iterators/readers, caches, strong tables, and persisted-root leases as explicit owners. Immutable node edges use tracing GC or atomic refcounts; weak tables use runtime weak references/protected upgrade, never raw unprotected pointers. Strong tables are bounded/generation-scoped and counted as retention roots. Epochs protect concurrent root/table acquisition and defer reclamation; node reachability still uses tracing/refcounts or arena dependency DAGs. Persisted Merkle objects GC by mark from committed/backup/legal/reader roots under generation/grace protocol. Expose roots by owner/age, unique/live/garbage/table/cache/arena bytes, sharing/fan-in, oldest reader, reclamation backlog and marginal/dominator estimates. Quota tenants for roots, versions, nodes/bytes, table entries, readers/age, diffs/output, and builds; authenticate deletion and retain rollback.

### Answer 4

Prefix every object with domain/schema/type. Encode integers in one minimal signed/unsigned format, byte strings with checked lengths, arrays with element count/order, and maps as entries sorted by canonical encoded key with duplicate rejection. An expression node encodes operator/type/payload, arity, and ordered child content hashes. Source annotations either participate through an explicit annotation-node/domain or remain in a separate occurrence map keyed by `(root,path/occurrence ID)`; do not ambiguously omit them. Hash exact canonical bytes with named algorithm/version/domain separation. Loader bounds bytes/nodes/depth/arity, verifies hashes, detects cycles, validates type/operator/child schemas and semantic invariants, authorizes/authenticates roots, and rejects unknown incompatible versions. Child objects become durable before root manifest; GC traces retained roots.

### Answer 5

Generate controlled DAGs varying repeated-subtree probability/size, granularity, entropy, fan-in/depth, roots/branches/updates, equal-content alternate shapes, tenant scopes, and release patterns. Compare every root with an unfolded nonsharing reference; force hash collisions, same-descriptor races, weak collection/recreation, table resize/eviction, allocation/crash failures, and Merkle corruption/GC races. Measure logical occurrences; unique/allocated/reclaimed/garbage/table/cache/retained nodes and bytes; hashes/equality/probes; copied nodes; build/update/query/diff/serialize/load/GC quantiles; allocator/cache/GC/contention; root release and peak memory. Test single/multi-thread and transients. Results support only measured descriptors, table/lifetime/runtime, platform, and workloads; they do not prove universal memory savings, collision/security certification, lock freedom, durable correctness, external review, or production fitness.
