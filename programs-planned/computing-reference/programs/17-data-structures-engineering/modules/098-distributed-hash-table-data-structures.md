---
module_id: DSE-098
program: Data Structures Engineering
level: 2
module_number: 98
title: Distributed Hash-Table Data Structures
status: complete
last_verified: 2026-08-30
---

# Distributed Hash-Table Data Structures

## One-Page Review

### Governing question

How can a distributed hash table maintain enough structured, authenticated, failure-aware routing and replica state that lookups converge to the responsible live nodes despite churn, partial views, delay, and adversarial peers?

### Essential definitions

A **distributed hash table (DHT)** maps opaque keys and node identifiers into a shared space, distributes key/value or provider records, and routes lookups through an overlay rather than requiring every participant to know every node. A node stores a bounded routing table plus local records; a lookup repeatedly chooses contacts closer to the target under the protocol's metric.

Chord uses clockwise successor ownership and exponentially spaced fingers. Kademlia uses XOR distance and prefix-bucket contacts with parallel iterative lookup. Pastry routes by shared identifier prefixes with leaf sets and proximity-aware choices. CAN partitions a multidimensional coordinate space. Each has different invariants; “DHT” is a family, not one interoperable wire protocol.

### Central model, mechanism, or theorem

In an ideal stable Chord ring with correct successors and fingers, a lookup advances clockwise toward the key's successor, typically cutting remaining identifier distance exponentially and using (O(log N)) overlay hops/state with high probability under stated assumptions. Stabilization repairs successor/predecessor/finger state after joins and failures.

This routing result does not supply durable storage, replica agreement, membership authentication, Byzantine resistance, or Internet-path locality. A production DHT composes routing with record validation, expiration, replication, admission, failure detection, repair, and bounded resource use.

### Critical invariants

- Identifier/key derivation, bit width, metric, interval conventions, and protocol version are canonical.
- Node identities bind network endpoints through an authenticated or explicitly open-membership policy.
- Every forwarding step is valid under the metric and makes measurable progress or terminates with a justified closest/responsible set.
- Successor/leaf/bucket invariants retain enough live alternatives to route around failures.
- Stored records bind key, value/provider, publisher, sequence/expiration, and validation policy.
- Replication distinguishes placement, successful writes, repair, and read reconciliation.
- Join/leave/failure maintenance is idempotent, bounded, restartable, and observable.
- Parsers, routing tables, pending RPCs, records, and peer influence have quotas.

### Common failures

Failures include mixing circular and XOR distance, incorrect wrap intervals, forwarding to a nonprogressing contact, trusting self-asserted node IDs/endpoints, eclipse-prone buckets, unbounded parallel queries, stale records without expiration, treating nearest nodes as replicas already written, accepting values without key/publisher validation, deleting old copies before join repair, letting Sybils dominate a key neighborhood, confusing overlay hops with network latency, and claiming logarithmic routing during unconverged or adversarial churn.

### Compact example

On a 4-bit stable Chord ring with nodes `[1,4,8,12]`, node 1's fingers are `[4,4,8,12]`. Key 10 belongs to successor 12, and lookup from 1 follows `[1,8,12]`. Exhaustive routing from every node to all 16 keys reaches the correct successor. After node 10 joins an already repaired ideal snapshot, key 10 belongs to 10 and route `[1,8,10]` converges.

### Connections

[DSE-097](097-consistent-hash-rings.md) supplies placement and transition fundamentals; this chapter adds partial-view overlay routing and maintenance. [DSE-096](096-merkle-trees.md) supplies authenticated content/state ideas. The successor is [DSE-099, “Conflict-Free Replicated Data Types as Structures”](../ROADMAP.md). Networking, distributed systems, databases, cryptography, security, and SRE own transport, membership, records, consistency, identities, abuse resistance, and operations.

## Governing Question

What identifier geometry, routing state, lookup algorithm, maintenance protocol, record model, replication semantics, and threat controls make a DHT lookup correct and operationally defensible?

## Why This Matters

Central directories simplify lookup but create scaling, trust, and availability concentration. Flooding every query is decentralized but expensive. DHTs seek logarithmic routing and bounded per-node state while members join, leave, and fail.

The elegant diagrams assume stable, honest participants with compatible identifiers. Real overlays face NAT, asymmetric latency, stale contacts, correlated failure, malicious IDs, spam records, partitions, and software upgrades. The data structure spans local tables, distributed invariants, network protocols, and lifecycle policies; verifying only the ideal routing loop is inadequate.

## Prerequisites and Retrieval

Retrieve consistent hashing, circular intervals, XOR/prefix metrics, binary search, tries, randomized identifiers, routing tables, UDP/stream transports, timeouts, retries, parallel RPCs, failure detectors, replication, quorums, signatures/MACs, capability/admission systems, NAT traversal, and distributed tracing.

This chapter separates **routing ownership** (which nodes should be queried), **record placement** (where copies should live), and **record truth** (which values are valid/current). A DHT can route correctly to invalid or unavailable records if those layers are underspecified.

## Learning Objectives

After this chapter, you should be able to:

1. derive Chord successor/finger lookup and circular progress invariants;
2. derive Kademlia XOR buckets and iterative parallel lookup behavior;
3. compare Chord, Kademlia, Pastry, and CAN metrics/state/maintenance;
4. specify signed/versioned/expiring record and replica semantics;
5. design bootstrap, join, stabilization, failure, partition, and recovery behavior;
6. analyze Sybil, eclipse, poisoning, amplification, and resource-exhaustion threats;
7. validate convergence, hop/latency distributions, correctness, repair, and adversarial resilience.

## Core Exposition

### Identifier geometry and responsibility

Canonical bytes map keys and nodes into an (m)-bit space. Chord assigns key (k) to the first live node clockwise at or after (k), with one exact modular interval convention. Kademlia defines distance (d(x,y)=x\oplus y); closer means numerically smaller XOR, and buckets group contacts by the most significant differing bit. Pastry uses prefix digits plus a numeric leaf set. CAN assigns coordinate zones and routes geometrically.

The metric determines progress and routing-table structure. Circular clockwise order is not XOR closeness: applying one protocol's “closest” choice inside another can loop or miss the responsible node. Identifier collision, endpoint changes, bit width, hash algorithm, namespace, and tie-breaking are protocol fields.

### Chord routing and stabilization

For node (n), finger (i) targets the successor of (n+2^i) modulo (2^m). To find successor of (k), return the immediate successor when (k\in(n,successor]); otherwise forward to the closest known finger strictly inside clockwise interval ((n,k)), falling back to a live successor. A correct step advances without overshooting the target under the modular order.

The successor pointer is the safety-critical route; fingers accelerate. A successor list supplies alternatives under adjacent failures. Stabilization asks successors about predecessors, adopts a closer valid node, notifies, refreshes fingers, and checks liveness. Joins initialize through a known bootstrap node and transfer/replicate affected records only after routing state supports them.

Ideal (O(log N)) results assume suitably distributed IDs and sufficiently correct tables. During churn, stale fingers may add hops while correct successors preserve reachability; broken successor cycles/partitions violate lookup correctness. Maintenance rate must dominate relevant churn and correlated failures.

### Kademlia lookup and buckets

Kademlia stores contacts in (k)-buckets for XOR-distance ranges. A target lookup begins with the closest known contacts, sends up to (alpha) parallel queries, incorporates returned closer contacts, and continues until the closest candidate set no longer improves and required responses complete. Parallelism masks slow/failed peers but consumes bandwidth/state.

XOR is symmetric and unidirectional for a fixed displacement. Bucket diversity across prefix regions provides reach. Least-recently-seen eviction policies exploit stable contacts under the original availability model, but modern deployments must test whether this improves resilience or preserves attacker-controlled incumbents. Lookup termination must define queried/unresponsive sets, closest-live result count, duplicate endpoints/IDs, and cancellation.

Records are usually stored at the (k) closest nodes, refreshed/republished, and expired. “Closest” is a placement target, not evidence that every node accepted/durably stored the record. Provider records, mutable signed records, and immutable content records need different validation and conflict policies.

### Pastry, CAN, and design families

Pastry routing tables increase shared prefix digits per hop; a leaf set handles numerically nearby destinations, and proximity metrics can choose among equivalent-prefix routes. CAN routes across neighboring coordinate zones in a (d)-dimensional torus/space, trading dimensions, path length, and neighbor state. These families show that routing geometry, locality, and maintenance are coupled design choices.

Structured overlays differ from unstructured gossip/flood search. DHTs excel at exact opaque-key lookup, not semantic/range/full-text queries without secondary structures. Gateway caches, recursive versus iterative routing, and hierarchical/federated designs may fit operational trust boundaries better than a fully open flat overlay.

### Records, replicas, and consistency

A record schema binds namespace, key, value/provider endpoints, publisher identity, sequence/version, validity interval/TTL, signature or content digest, and size limits. Immutable values can validate against content-derived keys. Mutable records need authorization and deterministic freshness/conflict rules; wall-clock timestamps alone are fragile.

Replica factor names intended target nodes. A PUT protocol reports which peers acknowledged what bytes/version and whether durability is promised. GET queries enough candidates, validates every response, and reconciles or returns conflicts. Repair reestablishes desired copies after membership change; expiration/republication bounds stale state. The routing layer does not automatically provide read/write quorums or linearizability.

Partitions can yield divergent mutable records. Policies may prefer signed monotonic sequence numbers, application merges, consensus within a replica group, or immutable append-only versions. The choice belongs in the record contract, not an undocumented “last write wins” in routing code.

### Membership, bootstrap, and network reality

Bootstrap contacts introduce the node to one overlay view. Multiple independently configured seeds, cached validated peers, DNS/service discovery, or authenticated rendezvous reduce one-point eclipse. A join validates protocol/network/identity compatibility before admitting contacts and gradually warms routing state.

Node IDs may be random, derived from public keys, or authority-assigned. Self-certifying IDs bind identity but do not limit how many identities an attacker creates. Proof-of-work/stake, admission authorities, rate/reputation diversity, network-prefix constraints, and peer sampling impose different decentralization/security costs.

Transport endpoints change; node identity must not silently equal an IP:port unless specified. NAT traversal, relays, address validation, amplification-safe request/response sizes, MTU, retransmission, timeouts, and connection limits materially affect lookup availability and latency.

### Security, persistence, and operations

Sybil attackers create identities; eclipse attackers fill a victim's useful routing regions; poisoning returns malicious contacts/records. Defenses combine identity cost/admission, diverse bucket selection, independently sourced contacts, response validation, iterative queries to multiple paths, quotas, and monitoring. No routing-table heuristic alone proves Byzantine safety.

Persist canonical peer IDs, validated endpoints, last-success/failure evidence, bucket/finger positions, record versions/expiry, and protocol epoch only when safe to reuse. On restart, persisted contacts are hints—not live facts—and must be revalidated. Corrupt or attacker-injected state cannot bypass normal admission.

Bound peer/table size, RPC concurrency, response contacts, record bytes/count/TTL, per-publisher storage, refresh work, recursion, redirects, and logs. Observe lookup success, correctness probes, overlay/network hops, latency, timeouts, bucket diversity, routing churn, record availability, repair backlog, rejection reasons, traffic amplification, and resource use.

The executable model below constructs an ideal static Chord snapshot. It validates local circular routing mechanics, not asynchronous stabilization or a distributed network.

<!-- bijux-verify: {"id":"chord-overlay-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=[1, 4, 8, 12]\nfingers_1=[4, 4, 8, 12]\nkey=10\nowner_10=12\nroute_1_to_10=[1, 8, 12]\nall_routes_valid=True\njoined_node=10\nafter_nodes=[1, 4, 8, 10, 12]\nafter_owner_10=10\nafter_route_1_to_10=[1, 8, 10]\nvalid=True\nevidence=bounded_chord_overlay_model\n","stderr":""}} -->
```python
import bisect


SPACE = 16
NODES = [1, 4, 8, 12]


def successor(identifier, nodes):
    index = bisect.bisect_left(nodes, identifier) % len(nodes)
    return nodes[index]


def clockwise_inside(value, left, right, include_right=True):
    if left < right:
        return left < value <= right if include_right else left < value < right
    if include_right:
        return value > left or value <= right
    return value > left or value < right


def fingers(node, nodes):
    return [
        successor((node + (1 << bit)) % SPACE, nodes)
        for bit in range(4)
    ]


def route(start, key, nodes):
    path = [start]
    current = start
    for _ in range(len(nodes) + 2):
        immediate = successor((current + 1) % SPACE, nodes)
        if clockwise_inside(key, current, immediate):
            path.append(immediate)
            return path
        candidates = [
            contact for contact in fingers(current, nodes)
            if clockwise_inside(contact, current, key, include_right=False)
        ]
        next_node = candidates[-1] if candidates else immediate
        assert next_node != current and next_node not in path
        path.append(next_node)
        current = next_node
    raise AssertionError("routing failed to converge")


all_valid = all(
    route(start, key, NODES)[-1] == successor(key, NODES)
    for start in NODES
    for key in range(SPACE)
)
after_nodes = sorted(NODES + [10])

print(f"nodes={NODES}")
print(f"fingers_1={fingers(1, NODES)}")
print("key=10")
print(f"owner_10={successor(10, NODES)}")
print(f"route_1_to_10={route(1, 10, NODES)}")
print(f"all_routes_valid={all_valid}")
print("joined_node=10")
print(f"after_nodes={after_nodes}")
print(f"after_owner_10={successor(10, after_nodes)}")
print(f"after_route_1_to_10={route(1, 10, after_nodes)}")
print(f"valid={all_valid and route(1, 10, after_nodes)[-1] == 10}")
print("evidence=bounded_chord_overlay_model")
```

The assertion rejects repeated nodes in this fixture route, but a real implementation needs protocol-aware loop detection, visited/request IDs, TTL/hop budgets, stale-contact fallback, and concurrent cancellation.

## Definitions and Notation

- (m) is identifier width and (2^m) the identifier-space size.
- (successor(k)) is the first live Chord node clockwise at or after key (k).
- A **finger table** contains exponentially offset Chord successors; a **successor list** contains adjacent fallback nodes.
- (d(x,y)=x\oplus y) is Kademlia's XOR distance interpreted as an unsigned integer.
- A **k-bucket** stores bounded contacts for one XOR-distance/prefix region; (alpha) bounds parallel lookup queries.
- A **routing-table invariant** is a condition on contacts sufficient for progress/reachability under named failures.
- **Iterative routing** lets the origin query contacts; **recursive routing** delegates forwarding to overlay peers.
- A **record** is validated key/value/provider metadata with ownership, version/freshness, and expiration semantics.
- **Churn** is membership change over time; **stabilization/refresh** repairs routing and record state.
- A **Sybil** is one of many attacker-controlled identities; an **eclipse** isolates a victim's useful view.

## Mechanisms, Invariants, or Proof Structure

### Chord progress

If successor pointers form the correct live ring, the immediate-successor fallback always advances clockwise and eventually reaches (successor(k)) in finitely many nodes. A valid closest-preceding finger lies strictly between current and key and therefore advances without passing the target. Ideal exponentially spaced fingers shrink expected remaining distance and yield logarithmic hops under the paper's distribution/stability assumptions.

### XOR progress

Kademlia candidates are ordered by unsigned XOR distance to the target. Iterative lookup only expands unqueried candidates and records responses; termination occurs when the closest required live set has been queried with no closer discoveries. Bucket coverage across differing-prefix regions supplies progressively closer candidates under the protocol assumptions. Parallelism affects latency/fault tolerance, not the definition of distance.

### Record correctness

Routing proof establishes a target node set, not value truth. Record acceptance separately checks canonical key binding, publisher authorization or content digest, namespace, version/sequence, expiration, size, and signature. Read reconciliation considers only validated records; replication success requires actual acknowledgments and later repair evidence.

### Maintenance safety

Join and stabilization must preserve at least one correct successor/near-target route while replacing stale state. Data transfer retains old copies until new placement is acknowledged and repair/cutover policy permits deletion. Under partitions or Byzantine behavior, stronger availability/consistency conclusions require additional assumptions and protocols.

### Evidence ladder

The model exhaustively checks one ideal 4-bit Chord snapshot. Stronger evidence adds independent protocol oracles, exhaustive small topologies, asynchronous schedule simulation/model checking, property/fuzz tests, churn/failure/partition injection, cross-version wire tests, Sybil/eclipse experiments, record-conflict/expiry tests, Internet/NAT trials, and measured routing/repair/resource distributions. Stable simulations do not prove adversarial or production behavior.

## Alternatives and Trade-Offs

**Central directory/metadata quorum.** Simple authoritative placement and rich queries, but concentrated availability/trust and metadata scaling. Often preferable inside one operated database.

**Gossip membership plus full maps.** Every node eventually learns all members and performs local placement. This avoids overlay routing for modest clusters but uses (O(N)) membership state/traffic.

**Chord.** Simple ring ownership, successor safety path, and logarithmic fingers. Locality and highly concurrent correctness require careful maintenance.

**Kademlia.** Symmetric XOR metric, parallel iterative queries, and organically learned contacts suit open networks. Bucket/admission diversity and record validation dominate security.

**Pastry/Tapestry.** Prefix routing and proximity choices improve locality opportunities at more structured state/maintenance complexity.

**CAN.** Multidimensional zones and neighbor routing offer different state/path tradeoffs and geometric partition maintenance.

**Unstructured search/gossip.** Supports discovery without exact-key placement but consumes more messages and provides probabilistic coverage.

**Federated/hierarchical routing.** Administrative domains retain control and exchange summaries/gateways, trading global flatness for policy, abuse handling, and operability.

## Failure Modes and Misconceptions

1. Circular interval wrap/equality is inconsistent among peers.
2. XOR and clockwise/numeric closeness are interchanged.
3. A forwarding choice does not strictly progress and loops.
4. A stale finger is treated as authoritative despite a live successor fallback.
5. Too few successor/leaf alternatives survive correlated failure.
6. Node ID is not bound to endpoint/identity or collision policy.
7. Bootstrap from one malicious peer produces an eclipse.
8. Unlimited Sybils capture target neighborhoods.
9. Routing tables accept unvalidated contacts returned by one peer.
10. Lookup parallelism, responses, retries, or pending state is unbounded.
11. Nearest-node selection is reported as successful durable replication.
12. Values are accepted without content/publisher/key validation.
13. Mutable versions use ambiguous wall-clock last-write-wins.
14. TTL expiry is omitted, allowing permanent stale/spam records.
15. Join/failure deletes old replicas before verified repair.
16. Partitioned writes diverge without surfaced conflicts/merge protocol.
17. Persisted contacts are assumed live after restart.
18. Overlay hop count is presented as end-to-end network latency.
19. Stable honest simulations justify claims under churn/adversaries.
20. A DHT is claimed to provide consensus, semantic search, confidentiality, or authorization automatically.

## Worked Examples

### Example 1

On nodes `[1,4,8,12]`, key 0 wraps to successor 1, key 4 belongs to node 4, and key 10 belongs to 12. Equality and wrap are part of the protocol.

### Example 2

Node 1's 4-bit fingers start at 2, 3, 5, and 9, whose successors are `[4,4,8,12]`. Duplicate physical contacts are valid table entries for different starts.

### Example 3

For key 10, node 1 chooses finger 8 strictly within `(1,10)`; node 8's successor 12 covers `(8,12]`, so route `[1,8,12]` terminates.

### Example 4

A stale long finger may time out. Falling back through a correct successor list can preserve lookup with more hops. If successor pointers split into disjoint cycles, fingers alone do not prove reachability.

### Example 5

In Kademlia, target `1000` and contacts `0001`, `1010`, `1111` have XOR distances `1001`, `0010`, `0111`; `1010` is closest, independent of ordinary numeric/circular order.

### Example 6

An iterative Kademlia lookup queries three candidates concurrently. Two time out and one returns closer contacts; the origin incorporates only validated unique contacts, cancels obsolete work, and continues within total RPC/hop/deadline budgets.

### Example 7

An immutable value stored under its content digest is rejected when bytes do not rehash to the key. A mutable provider record additionally needs authorized signature, sequence, expiration, and namespace checks.

### Example 8

Selecting the five closest peers is only desired placement. If two reject and one times out, a write has two acknowledgments, not replication factor five; repair/backfill must be scheduled and reported.

### Example 9

A victim whose buckets are filled with attacker IDs receives only attacker referrals. Diverse bootstrap, identity costs, network/authority diversity, and independent query paths reduce this eclipse risk but do not create Byzantine consensus.

### Example 10

After node 10 joins the ideal fixture, owner of key 10 changes from 12 to 10 and the repaired route becomes `[1,8,10]`. During real stabilization, old/new nodes retain/forward records until routing and replica repair establish cutover.

## Cross-Program Connections

- **Distributed Systems:** membership, failure detection, stabilization, partitions, replication, and convergence.
- **Networking:** UDP/streams, NAT/relays, MTU, retransmission, topology/locality, and amplification.
- **Database Engineering:** record versions, quorums, repair, durability, conflicts, and range-query limitations.
- **Cryptography/Security:** self-certifying IDs, signatures, Sybil cost, eclipse resistance, poisoning, quotas, and privacy.
- **SRE:** bootstrap, rollout compatibility, capacity, tracing, churn, repair backlog, and incident containment.
- **Performance Engineering:** overlay versus network hops, fanout, timeouts, caches, routing-state size, and tails.

## References

1. Ion Stoica et al., [“Chord: A Scalable Peer-to-peer Lookup Protocol for Internet Applications”](https://people.csail.mit.edu/dln/papers/chord/abstract.html), *IEEE/ACM TON*, 2003. Author-hosted final protocol page and paper.
2. Petar Maymounkov and David Mazières, [“Kademlia: A Peer-to-peer Information System Based on the XOR Metric”](https://pdos.csail.mit.edu/~petar/papers/maymounkov-kademlia-lncs.pdf), 2002. Author/CSAIL-hosted primary paper.
3. Antony Rowstron and Peter Druschel, [“Pastry: Scalable, Distributed Object Location and Routing”](https://www.microsoft.com/en-us/research/publication/pastry-scalable-distributed-object-location-and-routing-for-large-scale-peer-to-peer-systems/), 2001. Official author/employer publication page.
4. Sylvia Ratnasamy et al., [“A Scalable Content-Addressable Network”](https://www.cl.cam.ac.uk/~ey204/teaching/ACS/R212_2013_2014/papers/ratnasamy_sigcomm_2001.pdf), *SIGCOMM*, 2001. University-hosted copy of the primary CAN paper.
5. Giuseppe DeCandia et al., [“Dynamo: Amazon's Highly Available Key-value Store”](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf), *SOSP*, 2007. Production composition of partitioning, replication, versioning, and repair.
6. Pamela Zave, [“Reasoning about Identifier Spaces: How to Make Chord Correct”](https://arxiv.org/abs/1610.01140), 2016. Formal correction/invariant analysis for Chord.
7. libp2p, [Kademlia DHT specification](https://github.com/libp2p/specs/tree/master/kad-dht), official protocol specification repository. Contemporary wire/behavior context.

## Exercises

### Exercise 1

For a 5-bit Chord ring with nodes `[2,7,14,21,29]`, compute node 2's five fingers, owners of keys 0, 2, 8, 20, 31, and ideal routes from 2 to keys 20 and 31.

### Exercise 2

Prove ideal Chord successor-fallback termination and finger progress. State assumptions needed for logarithmic expected hops and explain what fails under a broken successor cycle.

### Exercise 3

For 8-bit Kademlia, place six contacts into XOR-distance buckets relative to one node, then design an (alpha=3), (k=4) iterative lookup state machine with exact progress, timeout, duplicate, cancellation, and termination rules.

### Exercise 4

Design a mutable signed provider-record protocol over an open DHT. Specify encoding, key binding, identity/admission, sequence/conflicts, expiry/republication, replicas, reads/writes, repair, quotas, and abuse handling.

### Exercise 5

Design a correctness/performance/security campaign comparing Chord and Kademlia under stable scale, churn, correlated loss, NAT/relay latency, Sybil/eclipse attempts, poisoned contacts, and record spam.

## Answers to the Exercises

### Answer 1

Finger starts from node 2 are 3, 4, 6, 10, and 18; successors are `[7,7,7,14,21]`. Owners: 0→2 after wrap, 2→2, 8→14, 20→21, and 31→2. For key 20, node 2 chooses 14 then successor 21, route `[2,14,21]`. For key 31, it can choose 21 then 29 then successor 2, route `[2,21,29,2]`; route representations must allow final wrap to the starting owner without mistaking it for a forwarding loop.

### Answer 2

With a correct live successor cycle containing every node once, immediate successors strictly advance in finite clockwise order and eventually reach the first node at/after the key. A closest-preceding finger lies strictly inside the remaining interval, so it also progresses without overshoot; fallback preserves safety. Expected logarithmic hops needs sufficiently uniform identifiers, stable/correct exponentially spaced fingers, and the paper's probabilistic model. A broken successor cycle may exclude the true owner; forwarding can terminate at a wrong component or loop, so no finger acceleration restores the missing global invariant reliably.

### Answer 3

Bucket index is the position of the most significant set bit in `self XOR contact`; equal IDs are not contacts. Store bounded validated unique contacts per index. Maintain candidate priority by `(xor_distance, peer_id)`, queried/in-flight/responded/failed sets, best (k), deadline, RPC cap, and request ID. Launch up to three closest unqueried candidates, validate each response and bounded contact list, merge unique contacts, and continue when slots open. Ignore late/wrong-request responses, penalize timeouts by policy, cancel farther requests once the closest four live candidates have all responded and no unqueried candidate is closer, or terminate on deadline/budget with an explicitly partial result. No-response peers are not counted as live results.

### Answer 4

Canonical record binds protocol/namespace, lookup key, publisher public key/ID, provider endpoints/capabilities, monotonically scoped sequence, issued/expiry bounds, payload digest/length, and signature. Derive or validate lookup key from namespace/publisher/content policy. Limit identity creation through the chosen admission/cost model and enforce per-peer/publisher/prefix quotas. Accept only authorized signatures, bounded future times, nonexpired records, and higher sequences; equal-sequence differing payloads surface equivocation/conflict rather than arbitrary overwrite. PUT targets the closest eligible replicas and reports actual acknowledgments; GET queries several, validates independently, returns highest valid sequence plus conflicts, and schedules repair. Republishing refreshes before expiry; tombstones need signed sequence/retention. Rate-limit messages/bytes, diversify paths, reject private/invalid endpoints as policy requires, and retain abuse evidence without permanent unbounded records.

### Answer 5

Use independent ideal oracles for stable ownership/distance and a deterministic event simulator for joins, leaves, failures, messages, and maintenance. Vary (N), ID distributions, churn/maintenance ratios, adjacent/correlated loss, bootstrap diversity, latency/loss/NAT/relays, and record workloads. Inject Sybil neighborhoods, bucket flooding, false referrals, duplicate IDs/endpoints, oversized responses, invalid signatures/versions, and spam. Measure correct lookup fraction, false termination/loops, overlay/network hops, latency/timeouts/RPC bytes, routing-state/diversity, convergence, record availability/freshness, replica/repair lag, amplification, CPU/memory, and honest-node impact. Cross-check small schedules exhaustively/model-check invariants, fuzz parsers/wire compatibility, and require bounded resources and recovery. Claims remain scoped to tested admission, topology, timing, maintenance, and adversary models.
