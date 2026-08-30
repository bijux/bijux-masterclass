---
module_id: DSE-058
program: Data Structures Engineering
level: 2
module_number: 58
title: Fat Nodes and Partial Persistence
status: complete
last_verified: 2026-08-30
---

# Fat Nodes and Partial Persistence

## One-Page Review

### Governing question

How can a mutable pointer structure retain every historical version when updates are allowed only at the newest version, and which assumptions make fat nodes or node copying correct and efficient?

### Essential definitions

- An **ephemeral** structure exposes only its current state; an update destroys the previous state.
- A **version** is a logical state identified by an ordered, structure-local version handle—not necessarily a wall-clock timestamp.
- **Partial persistence** permits queries at every retained version but permits updates only from the latest version.
- A **fat node** retains the versioned history of each mutable field instead of overwriting its old value.
- A **modification record** contains at least a field identity, a version, and that field's new scalar or pointer value.
- A **versioned read** returns the field value belonging to the greatest version not exceeding the query version in a linear history.
- **Node copying** places a bounded number of modification records beside a node, then copies a full node and redirects its current incoming pointers.
- **in-degree** is the number of structure pointers that can point to a node; bounded in-degree is essential to the constant-overhead node-copying transformation.
- A **root directory** maps each version to the entry roots needed to reach that version's structure.
- A **publication point** makes all changes of one logical version visible atomically.

### Central model, mechanism, or theorem

For a linear version order `0 < 1 < ... < m`, replace each mutable field `f` by its initial value plus an ordered history `H_f=[(v_1,x_1),...]`. Reading `f` at version `q` chooses the record with maximum `v_i <= q`, or the initial value if none exists. An update appends records only for a new latest version. Induction on versions proves that every historical read simulates the corresponding ephemeral execution.

If histories use balanced search structures, the fat-node method uses constant additional space per primitive field change and takes `O(log h)` to select among `h` changes to that field—often stated more coarsely as `O(log m)` after `m` changes. It does not require bounded in-degree, but nodes may grow without bound and accesses slow as histories grow.

Driscoll, Sarnak, Sleator, and Tarjan's partial node-copying transformation assumes a pointer-machine structure with constant bounded in-degree. Each node has a constant number of extra modification slots. A change uses a free slot; when full, it copies the node's current contents and recursively redirects the current predecessors. A potential argument charges copying cascades to filled slots, giving `O(1)` amortized time and space per primitive update step and `O(1)` worst-case overhead per access step under that model.

### Critical invariants

1. Versions form one strictly ordered latest-only update history; rejected historical updates change nothing.
2. Every field history is ordered, contains an unambiguous value at each published version, and is owned by the correct structure.
3. A read at version `q` selects the greatest applicable record and follows every pointer at the same `q`.
4. All fields/root changes for a logical update become visible together or none do.
5. Historical records and nodes reachable from retained roots remain alive and immutable in their historical meaning.
6. Node copying reconstructs the full current node, not only the overflowing field.
7. Every current incoming pointer to a copied node is redirected exactly once; bounded in-degree and reverse-pointer accounting are explicit.
8. Root replacements are recorded in the version directory, including structures with multiple roots.
9. Complexity statements count primitive field accesses/changes, history search, redirections, allocation, and logical-operation size.
10. Validation compares every retained version with an independent model and checks histories, reachability, ownership, and publication recovery.

### Common failures

- Calling a snapshot copy or append-only log partially persistent without historical query semantics.
- Updating an old version and silently turning the version line into a tree.
- Reading one pointer at the requested version and subsequent pointers at the latest version.
- Using wall-clock time, allowing duplicate/out-of-order timestamps, or accepting a handle from another structure.
- Publishing a version number before all its field records are durable.
- Applying the node-copying bound to an unbounded-in-degree graph.
- Copying a node but omitting unchanged fields, root replacement, or one predecessor redirection.
- Treating `O(1)` per primitive change as `O(1)` per arbitrary high-level operation.
- Reclaiming old records while readers or serialized roots still name them.
- Trusting a deserialized history whose versions, pointers, or modification arrays were not validated.

### Compact example

A latest-only list starts at version 0 as `10 -> 20 -> 30`. Version 1 changes the middle payload to 25; version 2 changes the first node's `next` pointer to skip the middle node; version 3 changes the final payload to 35. Each field stores its own ordered changes. A query at version 0 still yields `10 -> 20 -> 30`, version 1 yields `10 -> 25 -> 30`, version 2 yields `10 -> 30`, and version 3 yields `10 -> 35`. Following every pointer at the query version is what preserves each historical list.

### Connections

[DSE-051](051-path-copying.md) introduces persistence levels and version roots; [DSE-052](052-structural-sharing.md) develops reachability and lifetime; [DSE-057](057-persistent-union-find-trade-offs.md) shows why mutation-heavy queries complicate persistence. [DSE-054](054-persistent-balanced-trees.md) provides an immutable alternative. The [program roadmap](../ROADMAP.md) next generalizes from a version line to full and confluent persistence.

## Governing Question

Given an ephemeral pointer structure, can we support exact queries of every past state while continuing to update only the newest state, without copying the entire structure—and can we state the simulation, cost, failure, lifetime, and security obligations precisely enough to trust the result?

## Why This Matters

Historical data is not a niche feature. Geometry algorithms sweep through ordered events and query earlier search trees. Editors preserve revisions. Databases expose snapshots. Configuration systems audit prior decisions. Incremental analyses compare states. Debuggers ask what a structure contained before a failure. These workloads need old-state queries, but many do not need to branch updates from the past. Partial persistence matches that asymmetry.

Naively copying an `n`-node structure for each of `m` updates can require `Theta(nm)` space even when an update changes one pointer. An append-only operation log uses little space, but replaying from the beginning makes old queries expensive and requires a deterministic, complete replay semantics. Fat nodes store changes at the node that owns each field, allowing navigation through an old logical graph without rebuilding the whole state.

The phrase “store old values” hides most engineering hazards. A traversal must use one version consistently. A multi-field operation must publish atomically. Versions must be ordered and scoped to one structure. Old nodes cannot be freed merely because the latest root no longer reaches them. If a node-copying optimization is used, every current predecessor must be found and redirected. Crash recovery must distinguish staged records from a committed version.

The celebrated asymptotic transformations are model-dependent. The pointer machine permits nodes with a constant number of fields and pointer traversal, not arbitrary array indexing or word tricks. Fat nodes tolerate unbounded in-degree but pay history-search costs. The constant-overhead node-copying result needs constant bounded in-degree. A graph hub with a million predecessors is not covered merely because each node has two outgoing pointers.

Partial persistence is also weaker than immutability and full persistence. Its implementation may mutate the physical histories of old nodes by appending new records, while preserving their old logical values. Only the latest logical version accepts updates. This distinction is often exactly what makes a compact implementation possible.

## Prerequisites and Retrieval

Retrieve pointer graphs, search-tree invariants, linked representations, amortized analysis, binary search, transactions, checksums, and reachability. From [DSE-051](051-path-copying.md), retrieve ephemeral, partial, full, confluent, and functional persistence plus version-root terminology. From [DSE-052](052-structural-sharing.md), retrieve logical versus physical identity, sharing, reclamation, and reader pinning.

From [DSE-054](054-persistent-balanced-trees.md), retrieve immutable path copying as a representation-specific alternative. From [DSE-057](057-persistent-union-find-trade-offs.md), retrieve the lesson that a nominal query can write and that complexity must include the persistent substrate. You should be able to prove an invariant by induction on updates and perform a potential-method amortized argument.

## Learning Objectives

After completing this module, you can:

1. distinguish partial persistence from snapshots, logs, rollback, full persistence, and functional immutability;
2. specify a linear version domain and latest-only update contract;
3. derive versioned-field lookup and the fat-node simulation invariant;
4. calculate field-history space and lookup costs without hiding high-level operation size;
5. explain the node-copying transformation and its bounded-in-degree assumption;
6. design version roots, transactions, handles, retention, and crash publication;
7. diagnose mixed-version traversal, duplicate stamps, incomplete copies, and predecessor failures;
8. choose among fat nodes, copying, path copying, logs, checkpoints, MVCC-like chains, and immutable structures;
9. validate historical semantics, structural invariants, and adversarial serialized histories; and
10. benchmark history skew, traversal length, copy cascades, retention, cache behavior, and tail latency.

## Core Exposition

**Begin with the contract.** Let an ephemeral structure have states `S_0,S_1,...`, where operation `U_i` transforms `S_(i-1)` into `S_i`. A partially persistent representation supports `query(i,...)` for every retained `i`, but the only legal update is `update(latest,...)`, which creates `latest+1`. The version genealogy is a line. Updating version 7 after version 12 either must fail or belongs to a full-persistence API that creates a branch.

Version IDs are logical sequence numbers scoped to one structure generation. Wall clocks can repeat, move backward, differ across hosts, or expose ordering before durability. They can be metadata, not the sole semantic order. A handle should carry structure identity/generation and version; validate `0 <= version <= publishedLatest`. If histories can be truncated or rebased, include an epoch so a stale integer cannot name a different state.

Separate a logical operation from a primitive update step. A tree rotation might write several child pointers, a parent pointer, a root, and metadata. Transformation theorems charge overhead to each primitive pointer-machine access/change. If the ephemeral operation performs `u` primitive steps, constant overhead per step yields `O(u)`, not necessarily `O(1)` per operation.

**Fat nodes retain field histories.** Suppose node `x` has fields `key`, `left`, `right`, and `color`. Instead of overwriting `right`, retain its initial value and append `(version,newRight)` whenever it changes. At query version `q`, read the record whose version is the greatest not exceeding `q`. Initial values conceptually have version 0 or negative infinity.

For one field with ordered changes `(v_1,a_1),...,(v_h,a_h)`, define:

`read(f,q) = a_j`, where `j=max{k | v_k <= q}`, falling back to the initial value.

Because partial updates arrive in increasing version order, appending is simple. Historical lookup can binary-search an array in `O(log h)`, use a balanced search tree, or use a more specialized predecessor structure under a different machine model. A current-value cache makes latest reads constant-time but does not remove old-read cost. Linear scanning is valid but `O(h)` and vulnerable to hot-field histories.

Every mutable scalar, pointer, tag, size, color, balance value, aggregate, and root that affects semantics must be versioned or proven derivable. Versioning only payloads while overwriting child pointers does not preserve old structures. A pointer record stores a node identity, but dereferencing that node must continue reading its fields at the same query version.

Fat nodes add one record per primitive field change, hence constant space per change when field identities, versions, and values occupy constant space. They do not need bounded in-degree because changing a node does not redirect its predecessors; an old or current pointer still names the same fat node. The price is unbounded node growth and predecessor queries within field histories.

The broad `O(log m)` lookup statement assumes at most `m` changes overall. The sharper cost is `O(log h_f)` for field `f` with `h_f` changes. Traversing `k` pointers costs the sum of their field lookup costs, not merely one binary search. Hot roots or counters can dominate while most nodes stay thin. Cache lines, allocation, compression, and branch prediction matter even when asymptotics look acceptable.

**Simulation gives correctness.** Map every ephemeral node identity to one fat node. Claim: for every published version `i`, reading each field of the reachable fat graph at `i` equals the corresponding field in `S_i`. Base version initializes equal fields. For the induction step, operation `U_i` appends records containing exactly the new values for precisely the fields the ephemeral execution changes; every other field's greatest applicable record remains its `S_(i-1)` value. Therefore the version-`i` graph simulates `S_i`, while queries at `j<i` ignore records stamped `i` and remain unchanged.

This proof assumes complete instrumentation, total order, no ambiguous duplicate record for a field/version, correct root selection, and atomic publication. It proves semantic simulation, not memory safety, crash durability, concurrency, or claimed asymptotic data structures for record lookup.

Multiple writes to the same field inside one logical operation require a policy. The safest transaction stages ephemeral execution, coalesces the final value of each changed field, validates the resulting structure, appends records stamped with one new version, then publishes that version. Alternatively, primitive subversions can be internal and only the final subversion published. Readers must never observe an intermediate rotation as a valid public tree.

**Root directories are fields too.** A root can change even when no existing node field does. Retain `(version,root)` history for each named entry point, or store a root array indexed by version. A forest, graph service, or multi-index structure may have several roots; their changes must share the transaction. `null` is a legitimate versioned pointer value, not absence of a record.

Nodes created at version `b` have a birth version. Queries before `b` must not reach or read them; a direct node handle should reject such access. Deletion usually means no retained root reaches the node in later logical versions. The node remains physically necessary if an older retained version reaches it. Reusing its address or numeric ID can corrupt old pointers unless identities include generations and retention proves safety.

**Node copying bounds access histories.** Pure fat nodes let histories grow forever. The partial node-copying method gives each node a fixed number of modification slots. If a slot is free, record the changed field/version there. A versioned field read examines the base field plus a constant number of slots, so access overhead is constant.

When no slot is free, allocate a fresh copy containing the node's complete latest field values with the requested modification applied and empty modification slots. The old physical node continues serving old versions. For the new latest version, every predecessor that currently points to the old node must be changed to point to the copy. If a predecessor has a free slot, record the redirected pointer there. If it is full, copy that predecessor too. The cascade can reach a root, whose latest root entry then changes.

This is why constant bounded in-degree matters. With at most `p=O(1)` incoming pointers, copying a node triggers only a constant number of predecessor changes. Reverse pointers or another exact predecessor mechanism are needed for current-version incoming edges; scanning the entire heap would destroy the bound. Out-degree and node-field count also belong to the fixed pointer-machine representation.

An amortized potential counts filled modification capacity. Ordinary modifications fill slots and raise stored potential. Copying consumes accumulated fullness while creating nodes with free capacity; with enough slots relative to the in-degree, the released potential pays for recursive copying and redirection. The result is constant amortized time and space per primitive update step and constant worst-case access-step overhead under the theorem's assumptions.

Do not convert this sketch into a numeric slot formula without following the exact construction and potential proof. Slot capacity, predecessor representation, root handling, and postprocessing interact. A production implementation must document which published transformation it implements or supply its own proof.

The original result is amortized: one update may cascade through many nodes even though a sequence is cheap. Brodal later gave a bounded-degree partial-persistence construction with worst-case constant update time in the pointer-machine model. That stronger result is a separate mechanism, not a property obtained by relabeling the basic copying scheme.

**The pointer-machine boundary matters.** A node has constant-sized scalar/pointer fields; computation follows pointers and updates fields. A variable-sized array stored inside one “node,” unbounded adjacency vector, hash table resize, or arbitrary RAM indexing can perform work not represented by a constant pointer step. First expose the actual representation and primitive steps. High in-degree can sometimes be reduced through indirection nodes, but that changes traversal, space, lifetime, and invariants.

A rooted tree naturally has in-degree one except for root-directory references, so copying is attractive. A DAG may have bounded or unbounded sharing. A doubly linked list has bounded in-degree when all structural pointers are accounted for. An adjacency-list graph can have a hub pointed to by arbitrarily many edges; the general copying theorem does not cover it directly.

Parent pointers and backreferences increase in-degree and must be included. External raw node handles behave like additional predecessors if clients expect them to follow the latest copy. Prefer version-qualified opaque handles resolved through a directory, or specify that handles identify historical physical nodes rather than latest logical nodes.

**Queries must remain version-consistent.** Start by resolving the root at version `q`. Every field read, comparison metadata access, pointer selection, and aggregate uses `q`. Caching the current child inside a node is safe only for latest queries; an old query must not accidentally use it. Passing an implicit thread-local “current version” makes reentrancy and nested queries dangerous; pass an explicit validated view object.

A historical iterator pins its version and retention epoch. It must not switch to latest after yielding one element. Equality needs a contract: physical node identity, logical object identity, `(structure,version,node)` identity, or value equality differ. Hashing a mutable fat node by latest contents breaks historical map keys.

**Atomic publication creates a trustworthy history.** A logical update enters a staging state, reserves a new version, allocates/copies nodes and records, validates local invariants, persists required bytes, and finally publishes the root-directory entry/latest version. If any prior step fails, the unpublished records are unreachable garbage or are rolled back. Publication is the linearization/durability point.

Under concurrent readers and one writer, immutable historical entries can be read without locks only if memory publication ensures complete initialization and lifetime protection. Appending to resizable arrays can move storage while readers binary-search it. Use immutable chunks, copy-on-write history indexes, locks, epochs, or another proved synchronization scheme. “Old values never change” does not make the mutable container race-free.

Multiple writers require serialization or a consensus/compare-and-swap protocol for the one latest version. If two writers both derive version 42 from 41, partial persistence cannot publish both as successors without choosing one, retrying, or becoming a branching model. Reserve identifiers without exposing holes as valid committed states.

On durable storage, write records/nodes, checksums, and commit metadata in an order that recovery can interpret. A write-ahead log can redo a committed version or discard an incomplete one. Root-directory publication must not point to missing records. Validate monotonic commit sequence and graph reachability during recovery.

**Retention is semantic policy.** Keeping every past version means reachable old records accumulate at least with change volume. Product requirements often retain only a window, milestones, or legal snapshots. Removing a prefix is not just deleting early history entries: each surviving field needs a correct base value at the new oldest version, roots need rebasing, and nodes reachable only from deleted versions can then be reclaimed.

Readers, iterators, exports, backups, replication, audits, and legal holds can pin versions. Track pins by structure generation and use epochs, reference counts, tracing, arenas, or storage-level leases. A compacting rewrite creates a new physical representation that must preserve every retained logical query. Compare all retained versions or use hashes plus sampled/full semantic validation before retiring the old representation.

**Serialization is a graph protocol.** A logical export may serialize each requested version independently: simple but duplication-heavy. A physical export can serialize nodes, initial fields, modification histories, roots, births, and version metadata compactly, but couples readers to format and invariants. Assign stable object IDs; never serialize process pointers.

Validate schema/version, integer ranges, monotone histories, at most one final record per field/version, field type, pointer target existence, birth-version ordering, allowed cycles, roots, reachability budgets, and checksums before publishing an import. Parse into a quarantine arena. A malicious cycle can make traversal nonterminating; use step/depth/visited limits appropriate to the structure.

**Evidence must test time, not only latest state.** Maintain an independent ephemeral/reference snapshot for every test version. After each generated update, compare queries at all retained versions or a reproducible sample. Check the latest structure's ordinary invariants and each old version's logical invariants. Test fields updated many times, pointers set to null and restored, root changes, node births/deaths, duplicate values, and no-op updates.

Metamorphic properties help: appending version `i` cannot change any answer at `j<i`; serializing/reloading preserves all retained queries; compaction/rebasing preserves the retained suffix; failed publication exposes neither version nor partial changes; an update attempted at an old version leaves all bytes/logical answers unchanged.

For node copying, instrument slot occupancy, copy cascades, predecessor redirections, root replacements, allocated bytes, and maximum/percentile cascade length. Adversarial patterns should repeatedly modify hot nodes and force cascading full predecessors. Verify every latest incoming edge resolves to the right logical copy and every old version still reaches the old physical representation.

Benchmark separately: latest versus old queries, version age, history length/skew, path length, update field count, node in-degree, copy frequency, retention window, cache misses, allocations, GC/reclamation, serialization, recovery, and concurrency. Report medians and tails plus memory per logical change. A four-version demonstration is correctness evidence for a finite trace, not a throughput or theorem benchmark.

## Definitions and Notation

- `S_i`: the ephemeral logical state after published operation `i`.
- `V={0,...,m}`: one structure generation's totally ordered retained version domain.
- `latest=m`: the only logical version from which partial-persistence updates are accepted.
- `N`: logical node identities; a logical node can have several physical copies under node copying.
- `F(x)`: the constant set of fields of logical node `x` in the pointer-machine model.
- `b_x`: birth version of node `x`; it is invalid before `b_x`.
- `H_(x,f)`: ordered modification history for field `f` of fat node `x`.
- `h_(x,f)=|H_(x,f)|`: number of retained changes to that field.
- `value(x,f,q)`: initial value or value in the greatest record of `H_(x,f)` stamped at most `q`.
- `R_q`: root/entry directory for version `q`.
- `u`: number of primitive field-access/change steps made by one ephemeral operation.
- `p`: maximum current in-degree assumed by a bounded-degree copying transformation.
- `e`: constant extra modification capacity per physical node in a particular copying construction.
- **logical node**: the object in the simulated versioned structure.
- **physical node**: one allocated fat node or copy implementing a logical node over some versions.
- **history skew**: concentration of changes in a small subset of fields/nodes.
- **version-consistent traversal**: every read follows the same query version.
- **rebase**: materialize a retained version as a new base and discard an older prefix after proving no pin needs it.

For an array-backed field history with ordered distinct versions, predecessor search takes `O(log h_(x,f))`; append takes amortized `O(1)` at the container level unless allocation/durability changes the model. A traversal reading fields `f_1,...,f_k` costs `sum O(log(h_i+1))` plus application work. State the representation used for the `h=0` case.

## Mechanisms, Invariants, or Proof Structure

**Fat-node algorithm.** Initialize every field and root at version 0. To create version `q=latest+1`, execute the logical operation in a staging transaction, collect final changed fields, validate them, append one ordered record per changed field/root stamped `q`, then atomically publish `q`. To query `q`, validate its handle, resolve `R_q`, and use predecessor lookup at `q` for every field encountered.

**Simulation proof.** Induct on published `q`. Version 0 matches initialization. Assume every read at `q-1` matches `S_(q-1)`. The staged execution computes exactly the ephemeral operation's changes. Appended records override exactly those fields at `q`; unchanged fields inherit their greatest earlier record. Thus reads at `q` match `S_q`. For any `j<q`, predecessor lookup excludes stamp `q`, so its view is unchanged. Atomic publication excludes partial states.

**History invariants.** Within a field, record versions are strictly increasing after transaction coalescing; all values have the declared type; pointer targets exist and are born no later than the version where referenced; initial value is defined; the latest cache equals predecessor lookup at `latest`; and histories belong to one structure generation.

**Graph invariants.** Roots are valid for their versions. Each query follows versioned pointers consistently. Structure-specific properties—BST order, heap order, acyclicity, sizes, colors, balance, parent/child agreement—hold in every retained logical version. Physical cycles or sharing are acceptable only if the decoder/read algorithm cannot confuse them with forbidden logical cycles.

**Node-copying mechanism.** Read a physical node's base field plus its constant modification slots at `q`. For a latest change, use a free slot. On overflow, materialize a complete latest copy with the change, locate all current predecessors through bounded reverse pointers, and recursively install redirects; if no predecessor remains, update the relevant root. Preserve old nodes/slots for old queries.

**Copying obligations.** The mapping from `(logical node,version)` to a physical representative is total and unambiguous. Copies contain all latest fields. Every current incoming pointer and root is redirected. Old-version pointer resolution stays with historical representatives. Reverse pointers describe current logical incoming edges, not stale historical edges. Capacity and in-degree satisfy the selected theorem.

**Amortized proof shape.** Define potential proportional to filled modification capacity in current representatives. A cheap update adds bounded actual cost and potential. Overflow copying does more actual work but empties capacity in new representatives and consumes enough stored potential—given bounded predecessors and sufficient slots—to pay the cascade. Sum `amortized=actual+Delta potential` over a sequence; initial/final potential is nonnegative, yielding linear total overhead in primitive changes. Cite the exact construction for constants.

**Transactional invariants.** Published versions are contiguous or holes are explicitly invalid. A reader sees either the old latest or the fully initialized new version. Allocation failure, cancellation, validation failure, or crash before publication leaves no visible version. Recovery accepts a commit only when referenced records/nodes and checksums exist.

**Lifetime invariants.** A physical node/history record is reclaimed only if no retained root, reader pin, iterator, export, backup, replica, or recovery record can require it. Rebase records the logical base version and invalidates stale pre-rebase handles by epoch. Object IDs are not reused within an observable generation without a generation tag.

**Concurrency invariants.** One total publication order defines versions. Histories are safely published under the language memory model. Readers pin both version and storage lifetime. Writers do not mutate containers concurrently without synchronization. A failed competing writer retries from the actual latest or fails; it does not create an undeclared branch.

**Verification layers.** Structural parsing checks chapter/metadata shape. Executable finite traces compare all versions with independent expected sequences. Property tests compare randomized updates/queries with full ephemeral snapshots. Model checking can cover small histories, failures, and interleavings. Proof review checks simulation and amortization assumptions. Fault testing covers allocation/write/crash points. Benchmarks assess operational costs but do not prove semantics.

## Alternatives and Trade-Offs

| Design | Historical query | Update topology | Access/update character | Main obligation |
|---|---|---|---|---|
| Full snapshot copy | Direct | Usually linear | Simple query; `Theta(n)` copy | atomic snapshot and lifetime |
| Operation log/replay | Replay/checkpoint | Linear | cheap append; age-dependent query | deterministic complete replay |
| Unlimited fat nodes | Per-field predecessor | Latest only | `O(log h)` historical field access | ordered complete histories |
| Bounded-slot node copying | Constant slot scan | Latest only | constant access overhead; amortized copying | bounded in-degree and redirects |
| Immutable path copying | Direct from root | Naturally branching | copies changed frontier | representation-specific sharing proof |
| MVCC-style version chains | Visible-version selection | transaction-defined | chain/index dependent | isolation and reclamation |
| Rollback/undo | Current plus LIFO restore | One mutable timeline | cheap DFS/backtracking | complete reverse log |
| Periodic checkpoint plus deltas | Replay bounded by interval | Linear | tunable read/write/storage | checkpoint consistency |

Snapshot copying is ideal for small states, infrequent updates, or strongest implementation simplicity. A log is ideal when audit/replay is primary and queries can tolerate checkpoints. Fat nodes suit pointer structures, historical locality, and moderate per-field histories. Node copying suits bounded-degree structures when constant access overhead justifies greater implementation/proof complexity.

Immutable path copying may be easier in functional systems and already supports updates from old roots. It can copy `O(height)` nodes in a tree, which may be entirely acceptable. A general transformation is not automatically better than a data-structure-specific persistent representation.

MVCC resembles fat fields because versions retain older values, but database visibility can depend on transaction IDs, snapshots, commits, aborts, and isolation rather than a simple integer predecessor. Do not claim database MVCC correctness from this chapter's linear single-writer model.

Checkpoints plus deltas bound replay and support storage compaction. They move cost into checkpoint creation and require an atomic link between base and deltas. Hybrid fat histories can keep recent changes inline, spill immutable chunks, index old chunks, and rebase hot nodes; each layer adds recovery and validation obligations.

Choose using: need to branch, node degree, field count, hot-field skew, latest/old query ratio, acceptable tail updates, runtime memory model, persistence/durability requirements, retention, external handles, concurrency, and team ability to maintain the proof. The simplest design meeting measured requirements is often superior to the strongest theorem.

## Failure Modes and Misconceptions

- **“Any timestamp works.”** Version order must be total, unambiguous, scoped, and coupled to publication; wall clocks do not supply that automatically.
- **“Append-only means immutable.”** Appending physically mutates a fat node/history container even though old logical values remain stable.
- **“One binary search per query.”** A traversal may perform a predecessor lookup for every field along its path.
- **“Current pointers can be followed normally.”** A historical traversal must resolve every pointer at its requested version.
- **“Payload history is enough.”** Structural pointers, roots, tags, and metadata affect semantics and must also be preserved.
- **“Latest-only is a convention.”** It is the defining topology and part of the proof; an old update must be rejected atomically.
- **“A copied node inherits omitted fields.”** The new physical node must materialize the complete latest logical state.
- **“Out-degree two implies bounded degree.”** The theorem needs bounded incoming pointers; a shared child may have enormous in-degree.
- **“Reverse pointers are optional bookkeeping.”** Without an exact bounded way to find current predecessors, redirecting copies can scan the heap or miss edges.
- **“The theorem covers arrays and hash tables.”** Only after their primitive representation fits the stated pointer-machine assumptions.
- **“Constant overhead means constant operation time.”** It multiplies the ephemeral operation's primitive steps.
- **“Amortized means every update is fast.”** A copying cascade can be long; tail latency requires measurement or a worst-case construction.
- **“Old nodes are garbage after deletion.”** Retained old roots may still reach them.
- **“Readers need no synchronization.”** History containers, root directories, and reclamation are mutable physical state.
- **“A reserved version is a committed version.”** Only atomic publication creates a queryable logical state.
- **“Compaction is semantics-free.”** Rebasing must preserve every retained answer and invalidate/rewrite handles safely.
- **“Serialization can dump pointers.”** Stable IDs, schema, validation, quotas, and recovery rules are required.
- **“Passing latest-state tests proves persistence.”** The defining evidence is unchanged, correct behavior at every old version.

## Worked Examples

### Example 1

**Situation.** A counter has initial value 7 and changes at versions 2, 5, and 9 to 11, 4, and 12. What does a fat-field read return at versions 0, 2, 4, 5, 8, and 9?

**Reasoning.** The history is `[(2,11),(5,4),(9,12)]` with initial 7. Predecessor lookup finds no record at 0, version 2 at queries 2 and 4, version 5 at 5 and 8, and version 9 at 9. Results are `7,11,11,4,4,12`. The values are not monotone; only record versions are.

**Conclusion.** Historical lookup selects the latest applicable stamp, not the numerically greatest stored value or the closest wall-clock time.

### Example 2

**Situation.** Version 6 of a tree rotation must change `x.right`, `y.left`, two parent pointers, the root, and subtree sizes. Allocation fails after three records are appended.

**Reasoning.** If version 6 were already visible, a reader could see a graph that is neither version 5 nor the completed rotation. Stage records in unreachable storage or tag them uncommitted, validate the final graph, then publish the version-6 root/latest marker. Recovery ignores or reclaims the incomplete staged transaction. If histories are appended in place, their visibility predicate must exclude uncommitted records.

**Conclusion.** One logical version needs an atomic publication point across every field and root change.

### Example 3

**Situation.** A version-3 binary-search query resolves the root at version 3, but its helper reads child pointers through a latest-value cache at version 8.

**Reasoning.** A node that existed at version 3 may have had its right child replaced at version 6. Following the cached right child enters the version-8 graph and can return a key absent at version 3 or violate the old search path. Resolve each `left`, `right`, color, and aggregate using the same explicit view `q=3`.

**Conclusion.** A historical query is a version-consistent traversal, not a historical root followed by current pointers.

### Example 4

**Situation.** A graph node has two outgoing fields but can be referenced by every one of a million vertices. Can the basic bounded-degree node-copying theorem promise constant work when it is copied?

**Reasoning.** Out-degree is two, but in-degree is one million. The latest incoming pointers must be redirected or mediated. Direct redirection is not constant. An indirection tree could bound physical in-degree, but adds nodes/traversals and needs a new analysis. Unlimited fat nodes avoid predecessor redirection but pay history lookup.

**Conclusion.** Bounded out-degree does not substitute for the theorem's bounded-in-degree assumption.

### Example 5

**Situation.** One field changes 1,024 times while every other field changes once. Compare linear and binary history lookup.

**Reasoning.** A linear scan may inspect 1,024 records for an old query. Binary search needs at most about `log2(1024)=10` comparison levels, subject to exact implementation. A traversal of 40 such hot fields can still require about 400 comparison levels. A latest cache helps only latest queries.

**Conclusion.** Fat-node cost depends on per-field history skew and path length; averages over all nodes can hide the hot path.

### Example 6

**Situation.** Reproduce four versions of a linked list and prove old observations do not change after newer records are appended.

**Reasoning.** The program implements initial field values plus sorted latest-only modification histories. It independently checks the expected sequence for every version, rejects an attempted historical update, verifies ordered histories and birth constraints, and emits exact finite evidence.

<!-- bijux-verify: {"id":"fat-node-partial-list","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"v0=10->20->30\nv1=10->25->30\nv2=10->30\nv3=10->35\nlatest=3\nold_update_rejected=True\nold_versions_unchanged=True\nordered_histories=True\nbirth_constraints=True\nversion_consistent=True\nall_invariants=True\nevidence=finite_fat_node_partial_history\n","stderr":""}} -->
```python
from bisect import bisect_right
from dataclasses import dataclass, field


@dataclass
class FatNode:
    born: int
    initial: dict[str, object]
    changes: dict[str, list[tuple[int, object]]] = field(default_factory=dict)

    def read(self, name: str, version: int) -> object:
        if version < self.born:
            raise ValueError("node did not exist")
        history = self.changes.get(name, [])
        stamps = [stamp for stamp, _ in history]
        position = bisect_right(stamps, version) - 1
        return history[position][1] if position >= 0 else self.initial[name]

    def append(self, name: str, version: int, value: object) -> None:
        history = self.changes.setdefault(name, [])
        if history and history[-1][0] >= version:
            raise ValueError("versions must increase")
        history.append((version, value))


class PartialList:
    def __init__(self) -> None:
        self.latest = 0
        self.nodes = [
            FatNode(0, {"value": 10, "next": 1}),
            FatNode(0, {"value": 20, "next": 2}),
            FatNode(0, {"value": 30, "next": None}),
        ]

    def update(self, base: int, node: int, field_name: str, value: object) -> int:
        if base != self.latest:
            raise ValueError("partial persistence updates latest only")
        version = self.latest + 1
        self.nodes[node].append(field_name, version, value)
        self.latest = version
        return version

    def values(self, version: int) -> tuple[int, ...]:
        if not 0 <= version <= self.latest:
            raise ValueError("unknown version")
        result: list[int] = []
        seen: set[int] = set()
        current: int | None = 0
        while current is not None:
            if current in seen or not 0 <= current < len(self.nodes):
                raise ValueError("invalid list")
            seen.add(current)
            node = self.nodes[current]
            result.append(int(node.read("value", version)))
            next_node = node.read("next", version)
            current = None if next_node is None else int(next_node)
        return tuple(result)

    def invariants(self) -> tuple[bool, bool]:
        ordered = all(
            all(a[0] < b[0] for a, b in zip(history, history[1:]))
            for node in self.nodes
            for history in node.changes.values()
        )
        births = all(
            node.born <= stamp
            for node in self.nodes
            for history in node.changes.values()
            for stamp, _ in history
        )
        return ordered, births


history = PartialList()
expected = [(10, 20, 30)]
history.update(0, 1, "value", 25)
expected.append((10, 25, 30))
history.update(1, 0, "next", 2)
expected.append((10, 30))
history.update(2, 2, "value", 35)
expected.append((10, 35))

before_rejection = [history.values(v) for v in range(4)]
try:
    history.update(1, 0, "value", 99)
    rejected = False
except ValueError:
    rejected = True
after_rejection = [history.values(v) for v in range(4)]
ordered, births = history.invariants()
consistent = after_rejection == expected

for version, values in enumerate(after_rejection):
    print(f"v{version}=" + "->".join(map(str, values)))
print(f"latest={history.latest}")
print(f"old_update_rejected={rejected}")
print(f"old_versions_unchanged={before_rejection == after_rejection}")
print(f"ordered_histories={ordered}")
print(f"birth_constraints={births}")
print(f"version_consistent={consistent}")
print(f"all_invariants={ordered and births and consistent and rejected}")
print("evidence=finite_fat_node_partial_history")
```

The implementation intentionally has one writer, one-field logical updates, a fixed root/universe, unlimited histories, and no durability. It is evidence for the finite trace and rejection rule, not the node-copying theorem or production performance.

**Conclusion.** Versioned fields preserve all four list states when every dereference uses the same version and old updates are rejected before mutation.

### Example 7

**Situation.** A node with full modification slots is copied, but the implementation copies only the field being changed and its child pointers, omitting its cached subtree size and color.

**Reasoning.** The new physical node represents the current logical node, so every semantic field must equal its current value before applying the requested change. Omitting size/color may break rank/select or balancing immediately. Materialize each field through latest-version lookup, apply the change, validate, then redirect predecessors/root.

**Conclusion.** Overflow copying reconstructs a complete current node; it is not a partial patch object.

### Example 8

**Situation.** Retention deletes versions 0–99 and keeps 100–200. A field's initial value was `A`; records are `(20,B),(80,C),(150,D)`.

**Reasoning.** Simply deleting records before 100 would expose initial `A` at version 100, but the correct value is `C`. Rebase the field's new initial/base value to its predecessor value at 100, namely `C`, retain `(150,D)`, and record the new oldest version/epoch. Do this consistently for roots/nodes before reclaiming data reachable only from removed versions.

**Conclusion.** Prefix truncation requires semantic rebasing, not blind history deletion.

### Example 9

**Situation.** Two writers read latest version 12 and independently prepare successors 13 with different updates.

**Reasoning.** Publishing both would create two children of 12, which is full persistence, not one partial history. Serialize writers or use compare-and-swap on the latest commit: one publishes 13; the loser discards/rebases its staging work and retries from 13, or returns a conflict. Reserved IDs must not make the losing version queryable.

**Conclusion.** Concurrent partial persistence still needs one total committed successor order.

### Example 10

**Situation.** A team reports “constant-time persistent updates” after measuring a bounded-degree copied tree.

**Reasoning.** Audit the claim: was time per primitive change or full tree operation? Was it amortized or worst-case? Were predecessor redirects, allocation, root updates, reclamation, and synchronization included? Was in-degree actually bounded after parent pointers/external handles? Were cascade tails measured? The defensible statement may be the theorem's amortized constant overhead per primitive pointer-machine update step plus measured distribution under a named workload.

**Conclusion.** Complexity claims must name the model, unit, assumptions, and amortized/worst-case status; measurements must name the workload and included costs.

## Cross-Program Connections

- **Database Engineering:** MVCC, undo chains, snapshots, visibility, vacuum, and transaction commit share version-selection and retention concerns, but database isolation has additional semantics.
- **Data Engineering:** incremental pipelines and slowly changing dimensions preserve historical views; publication and backfill policy define which timeline is authoritative.
- **Software Engineering Patterns:** event sourcing, mementos, immutable aggregates, and copy-on-write encode different replay/query/update contracts.
- **Programming Languages:** persistent values may use mutation internally; observational equivalence, ownership, and effects determine whether that implementation is sound.
- **Concurrent and Parallel Programming:** safe publication, reader pinning, epochs, and writer serialization govern physical histories shared across threads.
- **Distributed Systems:** replicated logs establish a total order and durable commit point; forks/conflicts change the topology beyond simple partial persistence.
- **Security Engineering:** historical roots and serialized graphs expand confidentiality, integrity, denial-of-service, and deletion obligations.
- **Formal Methods:** refinement maps physical nodes/histories/copies to an abstract sequence of ephemeral states; induction and amortized potentials prove different properties.

## References

1. James R. Driscoll, Neil Sarnak, Daniel D. Sleator, and Robert E. Tarjan, [“Making Data Structures Persistent”](https://www.cs.cmu.edu/~sleator/papers/making-data-structures-persistent.pdf), *Journal of Computer and System Sciences* 38(1), 1989, pp. 86–124. Primary definitions, fat-node, node-copying, node-splitting, simulation, and overhead results.
2. Neil Sarnak and Robert E. Tarjan, [“Planar Point Location Using Persistent Search Trees”](https://www.cs.princeton.edu/techreports/1985/005.pdf), Princeton technical report TR-005-85, 1985. Primary application of partially persistent search trees.
3. MIT 6.854, [“Persistent Data Structures”](https://courses.csail.mit.edu/6.854/21/Notes/n02-persistent.html), course notes, 2021. Graduate derivation of fat nodes, copying, and persistence models.
4. MIT OpenCourseWare 6.851, [Lecture 1 student notes](https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/708883381ebad263ee5de4a2faa64cf8_MIT6_851S12_L1.pdf), 2012. Pointer-machine and bounded-degree transformation exposition.
5. MIT 6.851, [Lecture 1: Persistent Data Structures](https://classes.csail.mit.edu/6.851/spring21/lectures/L01.html), 2021. Current graduate lecture synopsis and theorem scope.
6. Gerth Stølting Brodal, [“Partially Persistent Data Structures of Bounded Degree with Constant Update Time”](https://pure.au.dk/portal/en/publications/partially-persistent-data-structures-of-bounded-degree-with-const), *Nordic Journal of Computing* 3(3), 1996, pp. 238–255. Author-institution record for the worst-case bounded-degree result.
7. Princeton Computer Science, [technical-report record for “Planar Point Location Using Persistent Search Trees”](https://www.cs.princeton.edu/research/techreps/533), report metadata and abstract. Official institutional record.

## Exercises

### Exercise 1

A field has initial value `P` and history `[(3,Q),(7,R),(12,S)]`. Give its values at versions `0,3,6,7,11,12,20`. State the validity condition needed before answering version 20.

### Exercise 2

Prove by induction that appending complete, ordered fat-node records for operation `i` preserves every query answer at versions less than `i` and simulates the ephemeral state at `i`. Identify at least four assumptions the proof needs.

### Exercise 3

A copied-node implementation passes latest-state tests but fails old queries after overflow. Its steps are: copy the changed node, redirect its parent, free the old node, and update the root only when the changed node was initially the root. Diagnose at least four defects and propose focused tests.

### Exercise 4

Choose a design for a 10-million-node tree with bounded in-degree, 99% latest queries, occasional audits of milestone versions, strict 20 ms update-tail requirement, and 90-day retention. Compare unlimited fat nodes, basic node copying, full snapshot copies, and checkpoint-plus-delta histories. Give an evidence plan.

### Exercise 5

Design a crash-consistent, single-writer/many-reader partially persistent configuration graph imported from untrusted files. Specify handles, transaction/publication order, history representation, reader lifetime, retention/rebase, validation/quotas, recovery, and verification. Explain what would have to change to permit updates from old versions.

## Answers to the Exercises

### Answer 1

Predecessor selection yields `P,Q,Q,R,R,S,S` at versions `0,3,6,7,11,12,20`, respectively, assuming 20 is a valid published retained version in the same structure generation. If latest is below 20, version 20 must be rejected rather than treated as “latest.” A query system may define an explicit clamp policy, but that is a different contract and should not happen silently.

### Answer 2

Let invariant `I(i)` say every field reachable from each root at version `j<=i`, when read at `j`, equals the corresponding ephemeral state `S_j`. Base `I(0)` holds by initialization. Assume `I(i-1)`. Execute the same ephemeral operation from the latest logical view and append at stamp `i` the final values of exactly all changed fields/roots. At query `i`, changed fields select their new records and unchanged fields select their previous values, so the graph equals `S_i`. At any `j<i`, predecessor lookup excludes stamp `i`, so `S_j` is unchanged. Atomic publication makes only the complete endpoint visible.

Required assumptions include: (1) strictly ordered, unambiguous structure-local versions; (2) updates only from latest; (3) complete instrumentation of every semantic field/root; (4) every traversal read uses its query version; (5) initial values/births are correct; (6) one final value per field/version or deterministic coalescing; and (7) atomic publication/lifetime safety. The induction proves logical simulation, not concurrency, durability, or time bounds.

### Answer 3

First, freeing the old node destroys versions that still reach it. Second, redirecting only “its parent” assumes in-degree one and may miss other current predecessors. Third, copying only the changed content may omit current unchanged fields/modification-slot effects. Fourth, root handling must update whichever copy cascade reaches any current named root, not merely when the originally requested node was root. Further risks include stale reverse pointers, external handles, birth/version mapping, and failure mid-cascade.

Tests should force overflow at leaves/internal/root nodes; use two or more predecessors up to the bound; compare all historical versions after every cascade; inspect complete copied fields; force recursive predecessor overflow; inject allocation failure at each copy/redirect/root step; retain/pin old iterators; validate current reverse edges; and run reclamation only after proving old roots are gone.

### Answer 4

Full copies are likely infeasible: one small update can copy ten million nodes. Unlimited fat nodes make implementation simpler and old milestone queries possible, but hot paths may accumulate long histories and latest reads need caches. Basic node copying gives constant access overhead under bounded in-degree, but only amortized update overhead; an adversarial cascade can violate the strict 20 ms tail. Checkpoint plus deltas/fat histories around selected milestones offers tunable retention and audit access, though reconstruction and checkpoint publication grow more complex.

A defensible design might keep immutable milestone checkpoints, a bounded recent fat/delta window, and scheduled rebasing outside the update critical path. If direct historical traversal latency is strict, evaluate Brodal's worst-case construction or a representation-specific immutable tree rather than assuming basic copying meets it. Evidence includes reference snapshots at milestones, failure/recovery tests, rebasing equivalence, pin/reclamation tests, hot-root/history-skew workloads, cascade and checkpoint tails, memory per change, 90-day expiry, cache misses, and production-shaped audit traces.

### Answer 5

Use opaque `(graph-id,generation,version)` handles and reject foreign, stale, future, or expired versions. A single writer reads the published latest, builds changes in a quarantine/staging arena, coalesces each field, validates the complete graph, writes nodes/history chunks and checksums, fsyncs as required, appends a commit/root record, and atomically publishes latest. Readers acquire a version view and epoch pin, resolve all roots/fields at that version through immutable chunks/indexes, then release the pin.

Retain versions by explicit window/milestone/legal-hold policy. Rebase at the oldest retained version by materializing correct base fields/roots into a new generation, compare retained queries/hashes, atomically switch generations, and reclaim only after old readers/backups/replicas release pins. Imports parse into bounded quarantine storage and validate schema, counts, sizes, version monotonicity, duplicate stamps, types, birth rules, target IDs, roots, allowed cycles, traversal depth, total records/bytes, checksums, and structure-specific invariants.

Recovery scans authenticated commit records, selects the latest commit whose referenced chunks are complete/checksummed, ignores incomplete staging, and verifies roots before service. Verification uses exhaustive small-model histories, randomized comparison with full snapshots, rejected-old-update noninterference, fault injection at every publication step, malformed imports, concurrency/read-reclamation stress, and retention/rebase equivalence.

Permitting updates from old versions changes the version line into a tree: handles need ancestry-aware version identity/order, field selection cannot use simple numeric `<=` without an ancestry labeling mechanism, root directories branch, conflict/merge semantics must be defined, retention becomes graph reachability, and the implementation/proof must be replaced by a full-persistence design. That change cannot be introduced as a flag on this partial-persistence protocol.
