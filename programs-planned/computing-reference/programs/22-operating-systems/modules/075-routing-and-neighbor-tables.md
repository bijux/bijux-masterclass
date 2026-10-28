---
module_id: OS-075
program: Operating Systems
level: 2
module_number: 75
title: Routing and Neighbor Tables
status: complete
last_verified: 2026-09-04
---

# Routing and Neighbor Tables

## One-Page Review

### Governing question

How should an operating system select a route and resolve its next hop at packet rate while preserving longest-prefix semantics, policy and namespace isolation, multipath stability, object lifetime, bounded unresolved traffic, neighbor reachability, secure updates, and coherent recovery from topology change?

### Essential definitions

- A **routing information base (RIB)** is control-plane reachability and policy information; a **forwarding information base (FIB)** is the lookup representation used to forward packets.
- **Longest-prefix match (LPM)** selects the matching address prefix with the greatest prefix length before applicable tie-breaking.
- A **policy rule** selects a routing table or action using context such as source, destination, mark, interface, priority, or namespace.
- A **route result** contains more than an output device: it can include route type, next hop, preferred source, MTU, scope, metrics, features, policy context, and lifetime.
- A **next hop** is the immediate network-layer destination used for forwarding; it may be the final destination on-link or a gateway.
- **ECMP** selects among equal-cost next hops, commonly with a stable flow hash rather than independently per packet.
- A **neighbor entry** maps an on-link network-layer address to link-layer reachability and addressing state.
- **Neighbor Unreachability Detection (NUD)** is IPv6's state machine for resolving and confirming neighbor reachability.
- An **unresolved queue** retains bounded packets while address resolution runs; it is not permission to buffer without limit.
- A **generation** or protected reference proves that a cached route, next-hop, device, or neighbor object remains valid during use.

### Central model, mechanism, or theorem

Model output selection as two joined state machines:

$$
R=L(n,s,d,m,i,t,p)\rightarrow(a,o,g,u,\mu,\gamma_R),
$$

$$
N=H(n,o,g,a)\rightarrow(\ell,z,Q,\tau,\gamma_N),
$$

where route lookup $L$ consumes namespace $n$, source $s$, destination $d$, mark $m$, ingress or bound interface $i$, traffic class $t$, and policy $p$. It returns action $a$, output interface $o$, gateway $g$, preferred source $u$, metrics $\mu$, and lifetime generation $\gamma_R$. Neighbor lookup $H$ resolves the effective next hop on interface $o$ to link address $\ell$, state $z$, unresolved queue $Q$, timer $\tau$, and generation $\gamma_N$.

LPM applies within the selected table, but policy can choose the table or a non-forwarding action first. A successful route does not imply a usable neighbor. Publication is safe only when the route result, next-hop object, device, neighbor state, packet metadata, and link header all belong to compatible live generations.

### Critical invariants

- Prefixes are canonical and bounded by address width; LPM precedes metric or multipath tie-breaking within one lookup domain.
- Policy rules execute in explicit priority order and cannot leak routes across namespaces or virtual routing domains.
- Route results distinguish unicast, local, unreachable, prohibit, blackhole, throw, multicast and broadcast semantics.
- An ECMP choice is stable for the ordering domain and excludes dead or administratively ineligible next hops.
- Cached decisions retain or validate route, next-hop, device and policy generations before use.
- Neighbor keys include namespace, protocol family, interface and on-link address; equal addresses on different links are distinct neighbors.
- Resolution updates validate message structure, target context, trust policy and state transition before replacing a link address.
- Packets awaiting resolution are charged before insertion and bounded by objects, bytes, time, neighbor and tenant.
- Reachability evidence has a defined source; mere receipt of an unsolicited message is not always positive forward-path confirmation.
- Route deletion, interface down, namespace teardown and neighbor failure drain or transfer every queued packet and reference exactly once.

### Common failures

Common failures are applying metric before prefix length, treating a default route as “no route,” caching only an output interface, hashing ECMP per packet, remapping every flow when one next hop changes, using a gateway that is not reachable under the route's recursive rules, sharing neighbor entries across interfaces, accepting unsolicited ARP or Neighbor Advertisement as unquestioned authority, keeping a neighbor permanently reachable, buffering unlimited packets during resolution, probing under memory pressure without a budget, waking after device removal, holding stale route or neighbor pointers across RCU grace periods, and reporting all failures as destination unreachable.

### Compact example

For destination `10.1.2.33`, routes `0.0.0.0/0`, `10.0.0.0/8`, and `10.1.2.0/24` all match. The `/24` wins even if the default has a lower metric. Its weighted ECMP group maps one stable flow to gateway `192.0.2.2`. The packet is still not transmit-ready: the stack must resolve `192.0.2.2` on the selected interface, retain the relevant generations, and either build a valid link header or admit the packet to a bounded unresolved queue.

### Connections

[OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-070](070-designing-an-i-o-path-for-latency-or-throughput.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), and [OS-074](074-protocol-processing.md) connect table lookup to concurrency, topology, timers, packets, sockets and pressure.

## Governing Question

Routing answers “what network-layer action should this context take?” Neighbor resolution answers “how can this selected on-link next hop be reached now?” Combining them too early hides distinct failure and lifetime domains. Separating them without a contract can transmit through a stale device, wrong namespace, obsolete gateway, or poisoned link address.

The governing question is therefore how to make both decisions fast and replaceable while a packet is using them. Routes change through configuration, dynamic routing, policy, address changes and device state. Neighbors change through discovery, reachability, movement, conflict and attack. Readers must see coherent immutable state or validate generations; writers must retire old state only after all users finish.

## Why This Matters

Every local output and forwarded packet depends on routing. Lookup cost, cache locality and multipath selection affect throughput and ordering. Route churn can be rare in a workstation and continuous in a router, container host or service mesh node. A design optimized only for a static table can stall during updates.

Neighbor tables sit directly on less-trusted local links. Spoofed ARP or Neighbor Discovery messages can redirect traffic. Unresolved destinations can allocate queues, timers and probes cheaply for an attacker. One interface failure can simultaneously invalidate thousands of routes, neighbors and packets.

Operationally, “network unreachable,” “neighbor unresolved,” “policy prohibited,” “blackholed,” “device down,” and “queue full” require different remedies. The subsystem must preserve those distinctions in counters, errors and traces.

## Prerequisites and Retrieval

Review [OS-007](007-kernel-data-structures.md), [OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-070](070-designing-an-i-o-path-for-latency-or-throughput.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), and [OS-074](074-protocol-processing.md).

Retrieve these distinctions:

- route installation, FIB publication, packet lookup, neighbor resolution, descriptor submission and wire transmission are different events;
- route prefix, route policy, next-hop group, next-hop member, output interface and neighbor entry are different objects;
- a route metric breaks ties under defined rules; it does not defeat a more-specific matching prefix;
- destination address, effective next hop and link-layer destination can be three different values;
- reachability, address resolution, liveness, authorization and path quality are different properties;
- RIB, FIB, route cache, flow cache and socket route reference have different invalidation contracts;
- namespace, VRF, routing table, policy-rule set, interface and link scope are separate isolation dimensions;
- ARP, IPv6 Neighbor Discovery, IPv6 router discovery and duplicate-address detection share messages but have distinct rules;
- unresolved, reachable, stale, delayed, probing and failed are state-machine meanings, not vague health labels;
- route miss, policy action, next-hop failure, neighbor queue overflow, probe exhaustion and device removal are separate errors.

## Learning Objectives

After this module, you should be able to:

1. derive a route from policy-rule selection, LPM, route type, metrics and multipath choice;
2. trace the selected next hop through ARP or IPv6 Neighbor Discovery, unresolved queuing, reachability confirmation and link-header construction;
3. design prefix and neighbor tables for read-mostly concurrency using immutable nodes, RCU, generations and explicit lifetime protection;
4. preserve namespace, interface, mark, source, MTU, preferred-source, next-hop and security context across caches and deferral;
5. bound multipath disruption, recursive lookup, unresolved packets, probes, timers, table growth and garbage collection;
6. handle route replacement, neighbor movement, device down, address conflict, namespace teardown and memory pressure safely;
7. diagnose forwarding decisions with reproducible lookups, table snapshots, neighbor state, probes, counters and packet evidence.

## Core Exposition

### Separate control state from forwarding state

Routing protocols and administrators produce candidate reachability in a RIB. The kernel or routing service validates, selects and publishes a FIB representation optimized for lookup. This separation permits rich control metadata without charging every packet for it.

Publication must be transactional from readers' perspective. Build replacement nodes off-path, validate prefixes and next-hop references, then publish one root or generation. Readers either see the old coherent FIB or the new coherent FIB. Partial multipath groups and half-installed routes are not valid intermediate views.

### Normalize route keys

For address width $W$, prefix length $p$ must satisfy $0\le p\le W$. Canonicalize a prefix by clearing all host bits. Reject or normalize inconsistent input at the ownership boundary so semantically equal prefixes cannot occupy ambiguous duplicates.

Lookup gathers routes whose significant prefix bits equal the destination and selects the greatest $p$. Only then do preference, metric, scope or protocol-specific tie-breakers apply. Policy routing can select a table or action before LPM; document that ordering explicitly.

### Treat route types as typed results

A lookup does not always return a forwarding next hop. Local results enter local delivery. Blackhole results consume silently. Unreachable and prohibit results have distinct local errors and possible control responses. Throw results can continue policy lookup. Broadcast and multicast have specialized semantics.

Represent these as a tagged result so a caller cannot mistake “matched non-forwarding action” for “no entry” or dereference a nonexistent gateway. Include output interface, next hop, preferred source, MTU, metrics and feature context only where meaningful.

### Compose policy with LPM

Policy rules can match source and destination prefixes, marks, interfaces, traffic class, user or tenant context, and other implementation fields. Evaluate rules by explicit priority. A rule can select a table, return a terminal action, or continue.

Bound rule traversal and prevent loops among recursive actions. A cache key must cover every input that can change the result. Caching only destination when marks or sources select tables is a cross-policy leak.

### Resolve next hops without recursive ambiguity

A route may be on-link or name a gateway. The gateway itself must be reachable through a valid relationship that cannot recurse indefinitely. Bound recursive next-hop resolution, detect cycles, and retain the final egress interface and on-link address as part of the result.

Interface state and address scope constrain validity. A syntactically correct gateway on the wrong link is not usable. When a device changes namespace, VRF, address or operational state, affected route generations become stale.

### Make multipath stable and explicit

Equal-cost routes form a next-hop group with member eligibility, weight and identity. Hash validated flow fields plus a controlled seed into the group. Choose fields that preserve required ordering and avoid attacker-controlled concentration where possible.

Simple modulo remaps many flows whenever membership changes. Indirection tables or resilient groups can limit disruption by moving buckets assigned to failed or added members. Stability is scoped: a seed rotation, group replacement or policy change can intentionally remap flows and should be observable.

### Protect fast lookup lifetime

Read-mostly prefix structures often use immutable tries with RCU publication. A reader obtains a route or next-hop object under the read-side contract, then either finishes use before leaving it or acquires a longer-lived reference. A raw pointer cannot escape because lookup was lockless.

Route caches store a generation for policy, FIB, device and next-hop state. Validate each dependency before reusing the result. Negative caches also need scope and expiration; an old “no route” must not survive a newly installed route indefinitely.

### Derive the neighbor key

After routing, compute the effective on-link next hop: destination for an on-link route or gateway for an indirect route. Neighbor identity includes network namespace, address family, interface and this address. The same IPv6 link-local address on two interfaces is not one neighbor.

Some links do not use ARP or Neighbor Discovery; represent link-specific output operations behind a typed interface. Do not manufacture an Ethernet address assumption in generic routing code.

### Resolve IPv4 addresses with ARP

ARP requests ask which link-layer address owns an IPv4 protocol address; replies provide a mapping. Validate hardware and protocol types, lengths, opcode and address fields before use. Tie learning behavior to interface and policy.

Unsolicited or gratuitous ARP can announce movement or conflict, but it is not universally trusted authority. Duplicate-address detection probes and announcements have their own timing and conflict semantics. Static or administratively managed entries should not be overwritten by ordinary dynamic learning.

### Implement IPv6 Neighbor Discovery statefully

IPv6 Neighbor Discovery uses ICMPv6 Neighbor Solicitation and Advertisement for address resolution and reachability, and Router Solicitation and Advertisement for first-hop information. Validate hop limit, checksum, source and destination constraints, options and message-specific rules before updating state.

NUD distinguishes INCOMPLETE, REACHABLE, STALE, DELAY and PROBE, with failure after bounded retransmission. REACHABLE ages to STALE. Sending through STALE can enter DELAY, allowing upper-layer confirmation before active probes. A successful solicited confirmation can restore REACHABLE under the specification's conditions.

### Bound unresolved traffic

When a neighbor lacks a usable link address, begin one resolution process and admit packets to a bounded per-neighbor queue. Charge packet truesize, objects and ancillary state before insertion. Apply per-interface, namespace and tenant limits so many fake destinations cannot allocate one queue each without a global bound.

Choose an overflow policy deliberately: drop newest, replace oldest, preserve control traffic, or fail immediately. Probe work is also bounded. Resolution success publishes the link address and drains packets through revalidation; failure releases the queue and reports protocol-appropriate errors.

### Interpret reachability evidence narrowly

A mapping says which link address to use; reachability says recent evidence supports the forward path. Upper-layer acknowledgements can confirm reachability without extra probes. An unsolicited advertisement can update a mapping under policy while leaving state stale rather than proving reachability.

Record evidence source and time. Randomize reachable timers where required to avoid synchronized probing. A permanent entry is an administrative promise, not a discovered proof, and still depends on a live device.

### Update mappings without races

A validated message may confirm the existing address, propose a new address, or conflict with protected state. Serialize state transition, link-address replacement, probe cancellation and queue drain. Packets built with the old link header must not be published after the new generation becomes mandatory.

Replacement may require accepting mobility while resisting spoofing. Use protocol flags, solicited context, security mechanisms and local policy rather than a universal “last reply wins” rule. Log changes with bounded rate and enough interface context to investigate.

### Revalidate after deferral

A packet can wait during policy verdict, route lookup retry, qdisc scheduling or neighbor resolution. During the wait, routes, MTU, device state or neighbor address can change. Define which properties are snapshots and which require revalidation.

Before draining an unresolved queue, confirm the route and neighbor relationship is still compatible. A route may now choose another device or gateway. Re-running lookup can be safer than forcing an old packet through a resolved neighbor that is no longer its next hop.

### Garbage-collect without deleting live state

Neighbor tables and route caches need thresholds, aging and reclamation. Prefer evicting failed, old and unreferenced dynamic entries before active reachable ones. Hash membership, timers, queued packets, device references and external pointers must retire under one ownership protocol.

Memory pressure can accelerate collection, but reclaim must make forward progress without depending on new allocations. Reserve narrowly scoped resources for teardown, probe completion and administrative recovery.

### Tear down in dependency order

On interface down or namespace destruction, stop new lookup publication, mark routes and neighbors unusable, prevent new probes, synchronize readers and callbacks, drain unresolved queues, cancel timers, release next-hop and device references, and only then free tables.

Removing the neighbor hash entry is insufficient while a timer, queued packet, cached route or RCU reader retains it. Late advertisements and probe completions must observe a dead generation and release safely.

### Observe each decision layer

Expose rule hits, table selection, prefix length, route type, metric, next-hop group and bucket, member eligibility, cache hit and invalidation, neighbor state transition, mapping change, queue admission and drop, probes, resolution latency, failure, garbage collection and teardown.

Use reproducible diagnostic lookups with full namespace, source, destination, mark, interface and traffic class. A routing-table dump alone cannot reproduce policy lookup. A neighbor dump alone cannot show which route selected that neighbor.

### Test churn, not only steady state

Generate overlapping prefixes from `/0` through host routes, equal metrics, conflicting rules, recursive gateways, dead members, hash collisions and rapid replacements. Compare a fast lookup with a simple reference LPM and policy interpreter.

Race lookup with route deletion, group replacement, neighbor update, timer expiry, device down, CPU hotplug and namespace teardown. Flood unique unresolved addresses under low memory. Assert bounded queues, stable intended flows, no stale device use, no cross-namespace result, no double release and eventual reclamation.

## Definitions and Notation

For address $x$ of width $W$ and canonical prefix $(p,k)$, where $0\le k\le W$, define match as

$$
\operatorname{match}(x,p,k) \iff (x\land M_k)=p,
$$

where $M_k$ contains $k$ leading one bits. Within selected table $T$, LPM chooses

$$
r^*=\arg\max_{r\in T,\operatorname{match}(d,r.p,r.k)} r.k,
$$

then applies defined tie-breakers among routes with the same prefix length.

Let a policy program be ordered rules $\rho_1,\ldots,\rho_m$. Each returns `continue`, a table identifier, or a terminal typed action. Evaluation is bounded by $m$ plus an explicit recursion depth; cycles are rejected.

For next-hop group members $j$ with positive weights $w_j$, let $W_g=\sum_j w_j$. A basic weighted selection maps stable flow hash $h$ into $h\bmod W_g$. A resilient indirection table instead maps buckets to member identities so membership changes need not remap unrelated buckets.

Let neighbor entry

$$
e=(n,f,i,a,\ell,z,r,Q,t,g),
$$

contain namespace, family, interface, protocol address, link address, state, reachability evidence, unresolved queue, timer and generation. Require

$$
|Q|\le C_e,\qquad \sum_{p\in Q}\operatorname{charge}(p)\le B_e,
$$

plus aggregate interface, namespace and tenant bounds.

A cached route is reusable only when all captured generations agree:

$$
g_{policy}=g'_{policy}\land g_{fib}=g'_{fib}\land g_{nh}=g'_{nh}\land g_{dev}=g'_{dev}.
$$

## Mechanisms, Invariants, or Proof Structure

Review the subsystem with these obligations.

1. **Canonical-prefix obligation:** address width, prefix length and host-bit normalization are validated at insertion.
2. **Policy-order obligation:** lookup inputs are complete, rule priority is deterministic, recursion is bounded and namespace isolation holds.
3. **LPM obligation:** maximum matching prefix length is chosen before same-prefix metrics or next-hop selection.
4. **Typed-result obligation:** local, forward, reject, blackhole, throw, multicast and broadcast outcomes cannot be confused.
5. **Next-hop obligation:** gateway recursion terminates and returns a live compatible output interface and on-link address.
6. **Multipath obligation:** eligible membership, weight, hash fields, seed and remapping semantics preserve the intended ordering domain.
7. **Lifetime obligation:** policy, route, next-hop, device and neighbor generations or references remain valid through use.
8. **Neighbor-key obligation:** family, namespace, interface and on-link address uniquely scope a mapping.
9. **Update obligation:** ARP or ND input is fully validated and authorized for the exact state transition it performs.
10. **Queue obligation:** unresolved packets and probe work are charged and bounded hierarchically before admission.
11. **Revalidation obligation:** packets crossing asynchronous boundaries recheck every dependency that is not a promised snapshot.
12. **Teardown obligation:** publication stops before readers, timers, probes, queues and references drain, and each resource retires once.

The safety proof composes two results. Route lookup proves a typed network-layer action and a live effective next hop under captured generations. Neighbor lookup proves a link-layer destination or bounded pending state for that exact next hop and device. Only the conjunction authorizes link-header publication. Failure of either proof produces an attributable owned error, not a partially valid transmit.

This is a review structure, not a formal proof of a kernel. Assurance requires reference-model differential tests, protocol conformance, sanitizers, RCU and lock diagnostics, timer fault injection, table churn, packet generators, namespace teardown, link failure and deployed-topology measurement.

## Alternatives and Trade-Offs

- **Trie versus hash:** tries naturally implement LPM; hashes accelerate exact prefixes but need multiple probes or auxiliary ordering.
- **Mutable nodes versus immutable publication:** in-place changes save allocation; immutable roots simplify reader coherence and reclamation.
- **Per-packet lookup versus flow cache:** fresh lookup follows changes; caching saves CPU but expands keys and invalidation.
- **One table versus policy-selected tables:** one table is simple; multiple tables express tenants and source policy with rule-walk cost.
- **Recursive gateways versus resolved next-hop objects:** recursion is flexible; resolved objects bound packet work but need dependency tracking.
- **Modulo ECMP versus resilient groups:** modulo is compact; resilient indirection reduces churn at greater state and rebalance complexity.
- **Per-packet ECMP versus per-flow ECMP:** packet spreading balances finely but reorders; flow selection preserves order but can skew elephant flows.
- **Eager neighbor creation versus on-demand:** eager entries reduce first-packet delay; on-demand state bounds idle memory but exposes resolution latency.
- **Queue while resolving versus fail immediately:** queuing hides ordinary discovery latency; immediate failure resists memory attacks but harms usability.
- **Retain packet pages versus copy pending bytes:** retention saves copying; a small pending packet can pin a large backing allocation.
- **Passive confirmation versus active probes:** passive evidence saves traffic; active probes detect silent failure more directly at a cost.
- **Aggressive learning versus protected updates:** mobility converges faster with learning; stricter policy reduces spoofing and may delay legitimate moves.
- **Timer wheel versus per-entry timers:** shared wheels scale expiry; precise timers simplify individual timing at high overhead.
- **Global garbage collection versus sharded collection:** global policy sees total pressure; sharding reduces contention but can leave imbalance.
- **Rich route dumps versus sampled tracing:** dumps reveal state snapshots; traces reveal decisions but can add hot-path cost.
- **Fail open versus fail closed on stale state:** reuse can preserve traffic during churn; rejection better protects isolation and correctness.

## Failure Modes and Misconceptions

- “The lowest metric always wins.” A longer matching prefix is selected before same-domain metric tie-breaking.
- “A default route means the table was empty.” It is a real `/0` match with explicit semantics.
- “No gateway means no next hop.” On-link routes use the destination itself as effective next hop.
- “A gateway route can recurse forever.” Implementations must bound recursion and reject cycles.
- “An output interface is a complete route result.” Source, MTU, action, next hop, metrics, policy and lifetime also matter.
- “Destination-only cache keys are enough.” Source, mark, namespace, interface and traffic class can change lookup.
- “RCU lookup makes a route immortal.” Protection must cover the entire dereference and any escaped result.
- “Negative route caches need no invalidation.” A newly installed route must supersede an old miss.
- “Equal-cost means select a random member per packet.” That can reorder one flow.
- “Adding an ECMP member should remap every flow.” Resilient designs can limit disruption.
- “ARP and ND prove identity.” Without additional protections, they mainly support local address resolution and reachability.
- “One IP address has one neighbor entry.” Interface, family and namespace are part of identity.
- “An unsolicited advertisement proves reachability.” It may update mapping while leaving reachability stale.
- “REACHABLE means permanently healthy.” Reachability evidence ages.
- “STALE means unusable.” It can be used while delayed confirmation begins under NUD.
- “Permanent neighbor entries survive device removal.” They still depend on device lifetime.
- “Only packets consume resolution resources.” Entries, hashes, timers, probes and logs also cost resources.
- “One per-neighbor queue limit prevents flooding.” Many unique fake neighbors require aggregate limits.
- “Resolution success can drain blindly.” Route, device and policy may have changed while packets waited.
- “A timer callback owns the entry because it found it.” Hash removal or teardown may race; lifetime protocol decides ownership.
- “Deleting a route instantly frees it.” Readers, caches and next-hop groups can retain protected references.
- “Interface down is just a failed probe.” It invalidates routes, neighbors, queues and callbacks as a coordinated event.
- “A route dump reproduces lookup.” It omits rule inputs and packet context.
- “A neighbor entry explains the selected path.” It does not show which policy and route chose it.
- “Ping proves multipath correctness.” One flow may exercise one member and avoid churn, policy and failure cases.

## Worked Examples

### Example 1

Tables contain `10.0.0.0/8` metric 10 and `10.1.0.0/16` metric 500. Destination `10.1.2.3` selects the `/16`. The lower metric on `/8` cannot defeat greater specificity.

### Example 2

This executable toy performs LPM, same-prefix metric selection, and one weighted stable next-hop choice. It does not implement policy routing, a kernel FIB, ECMP resilience or neighbor discovery.

<!-- bijux-verify: {"id":"route-and-next-hop-selection","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"route=10.1.2.0/24 metric=100\nnext_hop=192.0.2.2 flow_hash=5\nneighbor_required=True\n","stderr":""}} -->
```python
def address_value(text):
    value = 0
    for part in text.split("."):
        value = value * 256 + int(part)
    return value


destination = address_value("10.1.2.33")
routes = [
    ("0.0.0.0/0", address_value("0.0.0.0"), 0, 1),
    ("10.0.0.0/8", address_value("10.0.0.0"), 8, 10),
    ("10.1.2.0/24", address_value("10.1.2.0"), 24, 100),
]
matches = []
for route in routes:
    name, network, prefix_length, metric = route
    mask = 0 if prefix_length == 0 else ((1 << 32) - (1 << (32 - prefix_length)))
    if destination & mask == network:
        matches.append(route)
name, network, prefix_length, metric = max(matches, key=lambda route: (route[2], -route[3]))

weighted_next_hops = ["192.0.2.1", "192.0.2.1", "192.0.2.2"]
flow_hash = 5
next_hop = weighted_next_hops[flow_hash % len(weighted_next_hops)]

print(f"route={name} metric={metric}")
print(f"next_hop={next_hop} flow_hash={flow_hash}")
print(f"neighbor_required={next_hop is not None}")
```

### Example 3

A packet mark selects table 200, which has a prohibit route for the destination. The main table has a unicast default, but it is never consulted after the terminal policy result.

Caching by destination alone could incorrectly reuse the main-table route for marked traffic.

### Example 4

A four-member ECMP group loses one member. Simple modulo selection remaps flows whose modulo changes as well as flows on the failed member. A resilient bucket table primarily reassigns buckets owned by the failed member.

The rollout records group generation so cached selections cannot silently use removed membership.

### Example 5

Two interfaces both have an IPv6 link-local neighbor `fe80::1`. Each has a different link-layer address. Neighbor lookup includes interface identity, so packets never reuse the other link's entry.

### Example 6

An IPv6 neighbor ages from REACHABLE to STALE. The first new packet may use the cached link address and enter DELAY. An upper-layer acknowledgement confirms reachability before the timer, avoiding an active probe.

STALE did not mean “drop,” and packet receipt alone was not the only possible confirmation.

### Example 7

An attacker targets 100,000 nonexistent on-link addresses. A per-neighbor queue limit of three still permits 300,000 retained packets without aggregate bounds. Interface and namespace byte limits reject new state early.

Counters distinguish neighbor-entry admission from per-entry queue overflow.

### Example 8

ARP announces a new link address for a dynamic mapping while packets await resolution. The update is validated and published with a new generation; the drain path builds headers only after observing it.

A protected static entry rejects the ordinary dynamic overwrite and records the conflict.

### Example 9

A queued packet resolved gateway A, but policy now chooses gateway B on another interface. Drain re-runs or validates route selection and sends the packet through B rather than forcing the stale A neighbor.

Resolution completion is not authority to bypass current routing.

### Example 10

Connections fail intermittently after a route change. Rule and LPM traces select the expected group; failures correlate with one member's neighbor entering PROBE and then FAILED; unresolved queue drops rise only for its buckets.

The evidence localizes failure below ECMP selection and above device transmission.

## Cross-Program Connections

- **Network engineering:** CIDR, routers, ECMP, ARP, IPv6 ND, first-hop selection and MTU define external behavior.
- **Data structures engineering:** tries, prefix compression, hashes, indirection tables, queues, timer wheels and immutable roots determine cost.
- **Security engineering:** route policy, namespace isolation, spoofed resolution, redirect trust, tenant limits and audit context define exposure.
- **Distributed systems:** replicated control state, convergence, stale reads, consistent hashing, failure detection and partial reachability recur here.
- **Performance engineering:** lookup depth, cache misses, RCU, batching, flow skew, churn, probe rate and unresolved memory drive capacity.
- **Platform engineering:** namespaces, VRFs, interfaces, CNI routes, service next hops, observability and rollout safety operationalize tables.
- **API and service engineering:** connection ordering, source selection, path changes, timeouts and unreachable errors affect clients and servers.
- **Reliability engineering:** failover, graceful route replacement, neighbor aging, device loss, pressure and teardown determine recovery.
- **Formal methods:** LPM ordering, typed results, generation validation, state machines and resource bounds support precise invariants.
- **Computer architecture:** NUMA placement, per-CPU caches, atomic publication and memory reclamation shape scalable lookup.

## References

1. IETF, [RFC 1812: Requirements for IP Version 4 Routers](https://www.rfc-editor.org/rfc/rfc1812.html), CIDR, longest-prefix lookup, forwarding, routing information and router behavior; retrieved 2026-09-04.
2. IETF, [RFC 8200: Internet Protocol, Version 6 Specification](https://www.rfc-editor.org/rfc/rfc8200.html), IPv6 forwarding, hop limit, addressing and packet-size behavior; retrieved 2026-09-04.
3. IETF, [RFC 4861: Neighbor Discovery for IP version 6](https://www.rfc-editor.org/rfc/rfc4861.html), router discovery, address resolution, NUD states, messages, timers and validation; retrieved 2026-09-04.
4. IETF, [RFC 826: An Ethernet Address Resolution Protocol](https://www.rfc-editor.org/rfc/rfc826.html), ARP fields, requests, replies, address merging and byte representation; retrieved 2026-09-04.
5. IETF, [RFC 5227: IPv4 Address Conflict Detection](https://www.rfc-editor.org/rfc/rfc5227.html), ARP probes, announcements, conflicts, defense and timing; retrieved 2026-09-04.
6. IETF, [RFC 4191: Default Router Preferences and More-Specific Routes](https://www.rfc-editor.org/rfc/rfc4191.html), IPv6 router preference, route information and host selection; retrieved 2026-09-04.
7. IETF, [RFC 6724: Default Address Selection for IPv6](https://www.rfc-editor.org/rfc/rfc6724.html), source and destination address selection, scope, labels and precedence; retrieved 2026-09-04.
8. IETF, [RFC 8028: First-Hop Router Selection by Hosts in a Multi-Prefix Network](https://www.rfc-editor.org/rfc/rfc8028.html), source-aware default-router and next-hop selection; retrieved 2026-09-04.
9. Linux Kernel Documentation, [Resilient Next-hop Groups](https://docs.kernel.org/networking/nexthop-group-resilient.html), bucket indirection, member changes, idle timers and rebalancing; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Route Netlink Specification](https://docs.kernel.org/netlink/specs/rt-route.html), route messages, attributes, next hops, metrics and table operations; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design an IPv4 and IPv6 FIB supporting policy rules, LPM, typed route outcomes, recursive gateways and lockless packet lookup. State insertion, publication, cache and reclamation invariants.

### Exercise 2

Design a weighted ECMP group that minimizes flow remapping when members are added, removed or marked unhealthy. Cover hash inputs, ordering, weights, generations, churn and observability.

### Exercise 3

Trace an IPv6 neighbor from absent through INCOMPLETE, REACHABLE, STALE, DELAY, PROBE and failure. Include queues, evidence, timers, update validation, accounting and races.

### Exercise 4

Defend a multi-tenant host against ARP or ND spoofing and a flood of unique unresolved destinations without breaking legitimate mobility or first-packet delivery.

### Exercise 5

Construct a test and diagnosis plan for intermittent failures during simultaneous route replacement, ECMP-member loss, neighbor movement, interface flap and namespace teardown. State evidence limits.

## Answers to the Exercises

### Answer 1

Validate address family, width, prefix length and canonical host bits at insertion. Represent policy rules as immutable priority-ordered programs whose actions are terminal, table lookup or continue; bound recursion and reject cycles. Build table roots and referenced next-hop objects off-path, then atomically publish a new generation.

Within a selected table, match prefixes and choose maximum length before metrics. Return a tagged local, unicast, reject, blackhole, throw, multicast or broadcast result. Bound gateway recursion, prove gateway reachability, and capture output interface, effective next hop, preferred source, MTU, metrics and relevant generations.

Readers use RCU through traversal and either finish before unlock or acquire references to escaped objects. Cache keys cover namespace, family, source, destination, mark, interface, traffic class and every policy input. Reuse validates policy, FIB, next-hop and device generations. Negative entries expire and invalidate on publication. Writers unlink old roots, wait for readers, then release next hops and devices once.

### Answer 2

Give each member a durable identity, positive weight, eligibility state and generation. Hash validated flow fields plus a managed seed; include enough tuple information to distribute flows while keeping packets in the required ordering domain together. Avoid fields that are absent in fragments unless a stable fallback exists.

Use a fixed indirection bucket table larger than the member count. Allocate buckets approximately by weight. On removal, reassign buckets owned by the failed member; on addition, move a controlled subset from overrepresented members. Delay rebalance for recently used buckets when policy values flow stability, while bounding convergence time. Never select an ineligible member even to preserve stability.

Publish group and bucket changes atomically. Cached choices carry group and member generations. Record bucket ownership, flow distribution, moved buckets, member health, rebalance reason, queue load, reorder and failover time. Test adversarial hashes, weight extremes, rapid flaps, simultaneous changes and seed rotation.

### Answer 3

The first packet creates or finds a neighbor keyed by namespace, family, interface and on-link address. Charge the entry and packet before admitting it to bounded unresolved queues, enter INCOMPLETE, and schedule a bounded solicitation with randomized or specified timing. A valid solicited advertisement installs the link address, establishes REACHABLE when its flags and context support confirmation, cancels resolution work and drains packets after route revalidation.

After reachable time, state becomes STALE. The next use can send using the cached address and enter DELAY. Valid upper-layer reachability evidence during DELAY restores REACHABLE. Otherwise the delay timer enters PROBE and sends bounded unicast solicitations. Valid confirmation restores REACHABLE; probe exhaustion enters failure, drops queued packets, reports errors and schedules eligible reclamation.

Timer, advertisement, upper-layer confirmation, device down and garbage collection serialize through one transition protocol. Every callback owns a reference or generation. Unsolicited mapping changes follow override and trust rules and need not prove reachability. Queue bytes, objects, probes, timer state and references retire exactly once.

### Answer 4

Validate every ARP or ND field, ICMPv6 checksum, hop limit, address scope, option length, interface and message-specific constraint before learning. Separate dynamic, static, protected and proxy entries. Apply solicited and override semantics, conflict detection, link security features and administrative policy rather than accepting the last message blindly. Rate-limit change logs without hiding counters.

Charge entries, packet truesize, timers and probes hierarchically before allocation. Set per-neighbor packet and byte limits plus aggregate interface, namespace, tenant and host limits. Bound simultaneous INCOMPLETE entries, probe rate and lifetime. Prefer reclaiming failed old dynamic state. Reserve limited recovery capacity for gateways, control traffic and management.

Legitimate mobility can update eligible dynamic mappings after protocol validation, publish a new generation, and drain only after route revalidation. First packets may queue within small limits or receive explicit failure. Monitor mapping churn, source, override result, conflicts, unresolved cardinality, queue charge, probe outcomes and tenant drops.

### Answer 5

Capture policy rules and full lookup inputs, FIB generations, prefix and typed result, group and bucket, member eligibility, effective next hop, device generation, neighbor state and generation, unresolved queue, probe events, link notifications and packet-stage counters. Timestamp them on a common clock and correlate by namespace and flow.

Use a reference policy/LPM interpreter during rapid route replacement. Replay stable flows through member removal and addition and measure remapping and reorder. Move neighbor link addresses during queued resolution. Flap each interface at every state. Destroy a namespace while lookups, timers, probes and queue drains run. Inject allocation failures and low memory.

Enable memory, bounds, lock, RCU, leak and reference diagnostics. Assert no cross-namespace result, stale device submission, dead member selection, unbounded queue, double release or surviving timer after teardown. Verify eventual reclamation after grace periods.

A table dump is only a snapshot; packet traces can miss offloaded traffic; ping samples few flows; loopback omits neighbor discovery; fault injection covers finite interleavings; a reference model can share policy misunderstandings. Passing tests does not prove spoof resistance, standards conformance, all churn schedules or production performance. Record those limits.
