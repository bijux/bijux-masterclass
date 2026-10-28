---
module_id: DSE-097
program: Data Structures Engineering
level: 2
module_number: 97
title: Consistent-Hash Rings
status: complete
last_verified: 2026-08-30
---

# Consistent-Hash Rings

## One-Page Review

### Governing question

How should a consistent-hash ring translate keys, weighted physical members, replicas, membership epochs, and failure-domain policy into deterministic placement with measured balance and bounded remapping?

### Essential definitions

A ring maps keys and member **tokens** into a fixed circular hash space. A key's primary owner is normally the first token clockwise from its position. Adding a token steals only the preceding arc; removing one transfers its arc to the next token. This is the local movement property, not a complete storage protocol.

Physical members usually own many virtual nodes/tokens to reduce variance and approximate weights. A replica preference list walks clockwise while skipping repeated physical members and enforcing zones/racks. All participants must share hash algorithm, byte encoding, token map, epoch, tie-breaking, and eligibility state.

### Central model, mechanism, or theorem

With independently uniform key and token positions, expected owned load follows arc length. On a single-token-per-member ring, arc variance is high; multiple well-distributed tokens smooth it at metadata and rebalancing cost. When one member is removed, keys it owned move to successors while keys owned elsewhere remain placed under the same ring snapshot.

The theorem concerns placement under fixed views. Real correctness also requires membership agreement, handoff, replication, read/write routing, anti-entropy, and fencing so old and new owners do not lose or ambiguously accept data.

### Critical invariants

- Hash algorithm, seed, key/member canonical bytes, token width, ring direction, and tie-breaking are versioned.
- Tokens are uniquely ordered; each maps to exactly one physical member with declared capacity/failure domain.
- Lookup wraps at the ring end and uses one exact equality convention.
- Preference lists contain distinct eligible physical members and satisfy replication/failure-domain policy where possible.
- Placement uses one immutable membership epoch; handoff binds source, destination, range, epoch, and progress.
- Removal/addition moves only mathematically affected primary ranges, though replica and policy changes may move more.
- Balance, churn, hot-key load, metadata, repair, and recovery are measured separately.

### Common failures

Failures include language-dependent hashing, inconsistent string encoding, signed/unsigned token ordering, duplicate tokens, off-by-one range ownership, missing wraparound, equating tokens with machines during replication, proportional-token rounding that starves small members, treating uniform keys as uniform traffic, routing with mixed epochs, deleting a source before verified handoff, marking failed nodes absent on transient suspicion, and claiming minimal movement while changing hash/seed/token generation simultaneously.

### Compact example

On a 16-bit ring, nodes A/B/C each own two fixed tokens. Eight SHA-256-derived fixture keys map deterministically. Removing B moves only `gamma`, whose prior primary was B, to C; all keys previously owned by A or C keep their primary. `alpha`'s two-distinct-member preference list is `[A,B]` before removal.

### Connections

[DSE-096](096-merkle-trees.md) covers authenticated state and immutable publication. [DSE-083](083-cuckoo-and-quotient-filters.md) and [DSE-089](089-locality-sensitive-hashing.md) show that different hash structures own different guarantees. The successor is [DSE-098, “Distributed Hash-Table Data Structures”](../ROADMAP.md). Distributed systems, databases, storage, networking, SRE, and security own membership, replication, repair, routing, capacity, observability, and adversarial keys.

## Governing Question

What exact placement function, membership model, replica policy, transition protocol, and evidence make a consistent-hash ring safe and useful under capacity changes, failures, skew, and incompatible clients?

## Why This Matters

Modulo sharding remaps most keys when shard count changes. A consistent ring can limit placement churn, distribute a large keyspace, and compute owners locally. It supports caches, stateful services, object stores, and partitioned databases.

Minimal remapping is only one objective. Poor token placement overloads members; one hot key overloads its replicas; divergent membership causes inconsistent routes; unsafe handoff loses writes. Production engineering treats the ring as a versioned placement plan embedded in a data-movement and consistency protocol.

## Prerequisites and Retrieval

Retrieve uniform hashing, order statistics, probability, variance, binary search, circular intervals, virtual nodes, weighted capacity, replication, quorums, failure detectors, epochs, fencing, hinted handoff, anti-entropy, backpressure, and deterministic serialization.

The chapter uses half-open clockwise ownership `(previous_token, token]`: equality belongs to the token at that position. Another convention is valid if every producer, router, storage node, range scan, and handoff uses it consistently.

## Learning Objectives

After this chapter, you should be able to:

1. implement deterministic successor lookup with equality and wraparound;
2. derive which primary ranges move on token addition/removal;
3. design virtual-node and weighted placement from measured capacity/load goals;
4. construct distinct-member, failure-domain-aware preference lists;
5. specify epoch transitions, streaming, dual routing, fencing, and recovery;
6. compare ring, rendezvous, jump, bounded-load, and centralized placement;
7. validate balance, churn, replica diversity, compatibility, and operational cost.

## Core Exposition

### Deterministic ring function

Canonicalize a key into bytes, hash with the exact algorithm/seed, and interpret a fixed-width unsigned token in fixed endianness. Sort unique member tokens. Binary search finds the first token greater than or equal to the key token; if none, wrap to index zero. The physical owner attached to that token owns `(previous, token]`.

Every detail is protocol: normalization, tenant prefix, hash version, truncation, signedness, token collision resolution, and member identity. Built-in language hashes are often randomized or version-dependent and are unsuitable for cross-process durable placement.

### Movement and balance

Adding token (t) between predecessor (p) and successor (s) transfers range `(p,t]` from (s) to the new owner. Removing (t) transfers `(p,t]` to its successor. Other primary arcs are unchanged under the identical snapshot. Adding/removing a physical member with many tokens applies this argument to each token, with adjacent ranges merging.

Uniform random token gaps have variance. Many virtual tokens make each physical share a sum of smaller arcs, usually improving balance. More tokens increase membership size, lookup/cache cost, streaming fragments, replica transitions, and repair scheduling. Deterministic evenly spaced tokens can reduce variance but complicate weighted change and membership autonomy.

Token share approximates storage/throughput weight only if key bytes and request sizes/rates match the model. Capacity dimensions differ: bytes, requests, CPU, bandwidth, and tail latency may disagree. Weighted tokens need minimum allocations, stable rounding, hysteresis, and rate-limited change.

### Replication preference lists

Starting at the primary token, walk clockwise and collect distinct eligible physical members. Skip additional tokens belonging to a collected member. Apply zone/rack constraints before accepting candidates, with a documented fallback if topology lacks diversity. The preference list is a placement plan; quorum semantics determine how reads/writes use it.

Removing or adding one member can change replica placement for keys it did not primarily own, because preference-list successors change. Therefore “only 1/N keys move” may describe primaries but understate replica copying. Measure primary churn, replica churn, bytes, and network paths separately.

Transient health should not rewrite durable ownership on every suspicion. Separate placement membership from routing eligibility: a failed primary may be bypassed/hinted while its durable ownership remains until a controlled epoch change. Otherwise failure-detector flapping creates data storms.

### Membership epochs and handoff

Publish an immutable sorted token map with epoch, members, weights, zones, states, hash protocol, and checksum/signature as needed. Routers attach/observe epochs. A transition computes exact gained/lost ranges and replicas, streams a snapshot, forwards/captures concurrent writes, verifies counts/digests, catches up a log, then fences and activates ownership.

Strategies include stop-the-world transfer, source forwarding, dual writes, change-log replay, or quorum overlap. Each needs a linearization point and idempotent restart. The source does not delete until the destination is verified and rollback/retention policy permits it. A stale client is redirected or rejected with a newer epoch rather than silently writing to an abandoned owner.

Concurrent membership changes should serialize or compose through planned epochs. Tokens cannot be independently edited while transfers from an older plan are unresolved without a reconciliation model. Persist transition state so restart knows ranges, source/destination generations, high-water marks, and cleanup eligibility.

### Hot keys, adversaries, and bounded load

Uniform placement balances key counts in expectation, not traffic. A single viral key remains one primary placement and limited replicas. Request coalescing, caching, adaptive replication, key splitting, admission control, and load-aware routing address hot keys. Large objects and correlated prefixes likewise need byte/work metrics.

Adversaries may choose keys after learning an unkeyed hash to target one arc. A secret keyed placement hash can resist deliberate targeting but complicates interoperability, rotation, debugging, and clients; access control and quotas remain necessary. Collision flooding, oversized membership maps, and rebalance amplification require resource bounds.

Bounded-load variants reject assignments beyond capacity and search alternatives, trading additional movement/state for maximum-load control. They implement a different placement function whose consistency and overload behavior must be tested, not assumed from ordinary ring theory.

### Persistence and evaluation

Serialize canonical token integers, member IDs, weights, zones, states, epoch, and hash parameters. Reject duplicates, unsorted/noncanonical maps, impossible weights, insufficient distinct replicas, unknown algorithms, overflow, and stale signatures. Atomically publish validated snapshots and retain enough history for in-flight requests/transfers.

Differential testing compares binary-search lookup to a linear successor oracle for exact tokens, gaps, zero, maximum, and wrap. Property tests add/remove tokens and prove unaffected primary owners remain. Replica tests cover repeated virtual nodes, zone shortages, down/excluded members, and deterministic ties.

Benchmark lookup, snapshot load, membership update, balance by keys/bytes/requests, max/mean and percentiles, primary/replica churn, transfer bytes/time, foreground latency, recovery, metadata, and convergence. Use uniform, Zipf, hot-key, large-object, adversarial, heterogeneous-capacity, zone-loss, and flapping traces.

The executable model fixes a small ring and SHA-256 truncation. It proves only deterministic fixture lookup and the primary-removal locality property.

<!-- bijux-verify: {"id":"consistent-hash-ring-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"positions={'alpha': 36563, 'beta': 62542, 'gamma': 48797, 'delta': 20298, 'epsilon': 28351, 'zeta': 23745, 'eta': 25495, 'theta': 38718}\nbefore={'alpha': 'A', 'beta': 'A', 'gamma': 'B', 'delta': 'C', 'epsilon': 'C', 'zeta': 'C', 'eta': 'C', 'theta': 'A'}\nreplicas_alpha=['A', 'B']\nremoved_node=B\nafter={'alpha': 'A', 'beta': 'A', 'gamma': 'C', 'delta': 'C', 'epsilon': 'C', 'zeta': 'C', 'eta': 'C', 'theta': 'A'}\nmoved=['gamma']\nmoved_owned_by_removed=True\nunchanged_nonowners=True\nvalid=True\nevidence=bounded_consistent_hash_ring_model\n","stderr":""}} -->
```python
import bisect
import hashlib


TOKENS = [
    (10000, "A"), (20000, "B"), (30000, "C"),
    (40000, "A"), (50000, "B"), (60000, "C"),
]
KEYS = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]


def position(key):
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:2], "big")


def owner(key, tokens):
    positions = [token for token, _ in tokens]
    index = bisect.bisect_left(positions, position(key)) % len(tokens)
    return tokens[index][1]


def replicas(key, tokens, factor):
    positions = [token for token, _ in tokens]
    start = bisect.bisect_left(positions, position(key)) % len(tokens)
    result = []
    for distance in range(len(tokens)):
        member = tokens[(start + distance) % len(tokens)][1]
        if member not in result:
            result.append(member)
        if len(result) == factor:
            return result
    raise ValueError("insufficient distinct members")


before = {key: owner(key, TOKENS) for key in KEYS}
after_tokens = [entry for entry in TOKENS if entry[1] != "B"]
after = {key: owner(key, after_tokens) for key in KEYS}
moved = [key for key in KEYS if before[key] != after[key]]
local = all(before[key] == "B" for key in moved)
stable = all(after[key] == before[key] for key in KEYS if before[key] != "B")

print(f"positions={{{', '.join(repr(key) + ': ' + str(position(key)) for key in KEYS)}}}")
print(f"before={before}")
print(f"replicas_alpha={replicas('alpha', TOKENS, 2)}")
print("removed_node=B")
print(f"after={after}")
print(f"moved={moved}")
print(f"moved_owned_by_removed={local}")
print(f"unchanged_nonowners={stable}")
print(f"valid={local and stable and moved == ['gamma']}")
print("evidence=bounded_consistent_hash_ring_model")
```

The fixed tokens are not statistically calibrated virtual nodes, and eight keys cannot establish balance or expected churn. The model omits weights, zones, epoch transitions, replicas after removal, handoff, quorums, failures, and durability.

## Definitions and Notation

- The ring is an unsigned circular space ([0,M)); tokens and key positions lie in it.
- A token's primary range is `(predecessor, token]` under this chapter's equality convention.
- A **physical member** is a failure/capacity unit; a **virtual node** is one of its token positions.
- A **preference list** is an ordered list of distinct eligible physical replica members.
- A **membership epoch** identifies one immutable placement snapshot.
- **Primary churn** and **replica churn** count changed placements; **transfer cost** counts actual bytes/work.
- **Balance** compares assigned keys, bytes, requests, or work across members under a named workload.
- **Handoff** transfers an owned range between epoch plans while preserving concurrent operations.
- **Fencing** prevents an obsolete owner/epoch from accepting authoritative operations.

## Mechanisms, Invariants, or Proof Structure

### Successor and movement proof

Successor lookup partitions the circle into disjoint predecessor-token arcs. Inserting (t) only subdivides its successor's prior arc, so other successors remain unchanged. Removing (t) merges its arc into the next successor's. Applying this per token proves primary locality for a fixed protocol/snapshot; it says nothing about replicas or transfer safety.

### Probabilistic balance

Under independent uniform hashing, expected arc share per physical member follows its token share. Finite random gaps create variance, reduced by summing more virtual-token arcs. A production claim needs probability bounds or measured distributions for its actual deterministic generator, member count, weights, and keys.

### Preference correctness

Clockwise scanning establishes deterministic candidate order. Deduplicating physical IDs prevents two virtual nodes from masquerading as two replicas. Accepting only candidates satisfying topology policy establishes diversity when enough eligible domains exist; otherwise the explicit fallback determines availability versus durability.

### Transition correctness

A safe handoff establishes snapshot coverage, captures every later write until a cutover point, verifies replay through that point, publishes/fences the new epoch, then retires the source after grace. This is a protocol obligation, not a consequence of hashing.

## Alternatives and Trade-Offs

**Modulo/range sharding:** simple and compact but membership-count changes cause broad remapping; controlled range splits can be excellent under centralized metadata.

**Rendezvous (highest-random-weight) hashing:** scores each key/member and selects the highest, naturally producing ordered replicas and easy member changes. Naive lookup evaluates every member; optimized/weighted variants add complexity.

**Jump consistent hash:** constant-memory fast placement with sequential bucket identifiers and minimal movement. Arbitrary member removal, weights, replica topology, and stable identities require surrounding indirection.

**Bounded-load consistent hashing:** adds capacity constraints to control maximum load, accepting more state/movement and a different proof/implementation.

**Centralized placement tables:** an allocator can use measured bytes/load/zones and move explicit ranges optimally. Routers must distribute/version metadata, but operational control can outweigh ring elegance.

**DHT routing overlays:** Chord-like structures combine placement with decentralized routing tables and membership protocols. A local ring lookup alone is not a distributed hash table.

## Failure Modes and Misconceptions

1. Built-in/process-random hash causes cross-client disagreement.
2. UTF-8, normalization, namespace, or composite-key framing differs.
3. Signed and unsigned token comparisons disagree near the high bit.
4. Exact-token equality belongs to different adjacent owners.
5. Lookup fails to wrap beyond the maximum token.
6. Duplicate token resolution is nondeterministic.
7. Virtual nodes are counted as distinct failure replicas.
8. Zone diversity is asserted when topology lacks enough zones.
9. Weight rounding yields zero tokens or oscillating ownership.
10. Uniform key counts are reported as uniform bytes/requests.
11. Hot keys are expected to disappear through ring balance.
12. Replica churn is omitted from a minimal-movement claim.
13. Mixed epochs route reads/writes without redirects or fencing.
14. Failure suspicion immediately mutates durable placement.
15. Source data is deleted before snapshot/replay verification.
16. Concurrent membership plans overlap without composition.
17. Hash/seed/token regeneration is called a small member change.
18. Transfer bandwidth overwhelms foreground traffic.
19. Stale snapshots load after restart without monotonic epoch checks.
20. Ring placement is claimed to provide replication, quorum consistency, repair, or consensus by itself.

## Worked Examples

### Example 1

Tokens at 10, 40, and 80 own `(80,10]`, `(10,40]`, and `(40,80]`. Key position 90 wraps to token 10; position 10 belongs to token 10 under the declared convention.

### Example 2

Insert token 25 between 10 and 40. Only `(10,25]` transfers from owner 40 to the new token; `(25,40]` remains with 40 and other arcs remain unchanged.

### Example 3

Remove token 40. Its `(25,40]` arc transfers to successor 80. If the physical member owns another token, only the removed token's arc changes.

### Example 4

One token per member can leave a member with half the circle. Many independently spread virtual tokens make its share a sum of smaller arcs, reducing variance but fragmenting transfer ranges.

### Example 5

Members A/A/B/C appear clockwise as virtual tokens. Replication factor three yields `[A,B,C]`, not `[A,A,B]`; deduplication is by physical member.

### Example 6

Zones contain A/z1, B/z1, C/z2. A two-zone replica policy starting at A skips B until C is selected. A third replica may fall back to B only under the declared shortage rule.

### Example 7

A stale epoch-7 router sends a write to old owner A after epoch 8 cutover to B. B's activation and A's fencing/redirect prevent two authoritative histories.

### Example 8

Removing B in the executable fixture changes only `gamma`'s primary. Replica lists for other keys may still change because B can appear later in their preference order.

### Example 9

A million uniformly distributed cold keys cannot offset one key producing 40% of requests. Adaptive replicas/caching or key partitioning address traffic skew; extra virtual tokens do not split one key.

### Example 10

Changing SHA-256 truncation to another hash while adding one node may remap nearly everything. Hash migration is a full placement migration with versioned dual routing, not evidence about consistent-hash member churn.

## Cross-Program Connections

- **Distributed Systems:** membership, failure detection, epochs, quorums, handoff, anti-entropy, and consensus.
- **Database Engineering:** partitions, replicas, MVCC/fencing, range scans, repair, and metadata transactions.
- **Storage Engineering:** bytes/capacity, streaming, throttling, retention, restart, and checksums.
- **Networking/SRE:** topology, locality, health, backpressure, hot spots, rollout, and observability.
- **Security:** keyed placement, hostile keys, snapshot authentication, downgrade, and tenant quotas.
- **Performance Engineering:** lookup locality, metadata size, max/mean load, transfer amplification, and tails.

## References

1. David Karger et al., [“Consistent Hashing and Random Trees”](https://people.csail.mit.edu/karger/Papers/web.pdf), *STOC*, 1997. Author-hosted foundational paper.
2. Giuseppe DeCandia et al., [“Dynamo: Amazon's Highly Available Key-value Store”](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf), *SOSP*, 2007. Primary production design using consistent hashing, virtual nodes, replication, and handoff.
3. John Lamping and Eric Veach, [“A Fast, Minimal Memory, Consistent Hash Algorithm”](https://arxiv.org/abs/1406.2294), 2014. Primary Jump Consistent Hash paper.
4. Thaler and Ravishankar, [“Using Name-Based Mappings to Increase Hit Rates”](https://www.eecs.umich.edu/techreports/cse/96/CSE-TR-316-96.pdf), 1996. Primary rendezvous/highest-random-weight work.
5. Vahab Mirrokni, Mikkel Thorup, and Morteza Zadimoghaddam, [“Consistent Hashing with Bounded Loads”](https://arxiv.org/abs/1608.01350), 2016. Primary bounded-load variant.
6. Ion Stoica et al., [“Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications”](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf), *SIGCOMM*, 2001. Primary DHT ring/routing paper.
7. Envoy project, [Ring Hash Load Balancing](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers#ring-hash), official documentation. Operational ring configuration and locality context.

## Exercises

### Exercise 1

For tokens `10:A, 25:B, 40:C, 70:A`, determine owners for positions 0, 10, 11, 25, 69, 70, and 99; then remove B and list changed owners under `(previous,token]`.

### Exercise 2

Prove the single-token insertion/removal primary-locality property and explain why it does not bound replica churn, transfer bytes, or client-visible inconsistency.

### Exercise 3

Design deterministic weighted virtual-token allocation for capacities A:1, B:2, C:5 across three zones. State rounding, minimums, collision resolution, stability, and validation metrics.

### Exercise 4

Design a crash-safe epoch transition adding a node to a replicated database. Specify planning, streaming, concurrent writes, verification, cutover, fencing, rollback, restart, and cleanup.

### Exercise 5

Design a campaign comparing a ring, rendezvous hashing, jump hashing with indirection, and centralized ranges under heterogeneous capacity, Zipf traffic, zone failure, and churn.

## Answers to the Exercises

### Answer 1

Owners are 0→A at token 10, 10→A, 11→B, 25→B, 69→A at 70, 70→A, and 99→A after wrap to 10. Removing token 25 transfers `(10,25]` to C at 40, so positions 11 and 25 change from B to C; the listed others remain A.

### Answer 2

Insertion subdivides only the successor's predecessor arc; all other key positions still have the same first clockwise token. Removal merges only the removed token's arc into its successor. Replica walks can include the changed member after another primary, so more preference lists change. Actual bytes depend on object sizes/replicas, and mixed epochs/handoff determine availability and consistency; none follows from the geometric proof.

### Answer 3

Choose a versioned total token budget large enough for granularity, give every eligible member a minimum, and apportion remaining tokens by stable largest-remainder weights 1:2:5. Generate positions with a domain-separated hash of `(ring version, member ID, ordinal)`, resolving collisions by deterministic rehash counters. Preserve existing tokens when weights change and add/remove a rate-limited delta with hysteresis. Validate token counts, unique ordering, arc/key/byte/request shares, max/mean and percentiles, zone preference diversity, churn, metadata, and transfer fragments across repeated deterministic builds.

### Answer 4

Publish epoch E+1 plan from E, compute gained primary/replica ranges, pin source snapshots, stream idempotent chunks under bandwidth limits, and record per-range progress. Capture/forward writes after snapshot in an ordered log; destination verifies counts/digests and replays through a committed high-water mark. Atomically activate E+1 and fence E writes, redirect stale clients, retain source data for rollback/grace, then clean after readers/transfers/repair agree. Persist plan, snapshot IDs, offsets, replay marks, verification, and cutover state so restart resumes rather than guesses.

### Answer 5

Use identical canonical keys/members and independent placement oracles. Vary members, weights, zones, key/object sizes, uniform/Zipf/hot/adversarial traffic, sequential/arbitrary removal, and failure flapping. Measure lookup CPU/cache/metadata, key/byte/request balance, max/mean and tails, primary/replica churn, zone diversity, transfer bytes/fragments/time, foreground latency, convergence, and recovery. Ring favors arbitrary stable members and clockwise replicas; rendezvous favors simple ranked candidates; jump favors sequential buckets plus indirection; centralized ranges favor measured control. Select only after correctness under snapshots/transitions and service limits passes.
