---
module_id: OS-074
program: Operating Systems
level: 2
module_number: 74
title: Protocol Processing
status: complete
last_verified: 2026-09-04
---

# Protocol Processing

## One-Page Review

### Governing question

How should an operating system turn an untrusted packet into a local delivery, forwarded packet, control response, or attributable drop while preserving bounds, protocol semantics, namespace and policy context, checksum meaning, resource limits, concurrency, and error causality?

### Essential definitions

- **Demultiplexing** selects the next protocol or endpoint from a validated protocol identifier and context.
- A **parse cursor** is a checked offset into packet data together with the remaining validated extent; it is safer than a persistent raw pointer into movable or fragmented storage.
- A **protocol control block** stores per-protocol or per-endpoint state used after packet classification.
- **Reassembly** combines fragments of one original IP datagram under a bounded key, timer, byte budget, and overlap policy.
- A **pseudo-header checksum** covers selected network-layer fields in addition to a transport header and payload.
- **Local delivery** hands a packet addressed to this host to an upper-layer protocol; **forwarding** sends a packet through another interface after router processing.
- **ICMP** reports Internet-layer errors and control information, but an ICMP error is itself subject to suppression, quoting, routing, policy, and rate limits.
- A **hook** is a defined interception point at which policy may accept, drop, transform, queue, or redirect traffic.
- **Softirq or deferred processing** performs bounded network work outside the immediate device interrupt while still imposing restrictions on blocking and allocation.
- **Offload metadata** represents work already verified or deferred; it is valid only for the exact bytes, layers, and device path that established it.

### Central model, mechanism, or theorem

Represent one processing attempt as

$$
P=(b,c,e,n,h,v,f,r,k,s,q,a),
$$

where $b$ is the packet backing, $c$ a checked cursor, $e$ the validated extent, $n$ the network namespace, $h$ the protocol-header chain, $v$ checksum and semantic validity, $f$ fragment state, $r$ route decision, $k$ hook and policy context, $s$ protocol or socket state, $q$ queue and execution context, and $a$ accounting. A transition may consume only fields already proved by an earlier stage. Any byte or metadata transformation invalidates every dependent proof unless the implementation updates it by a proved rule.

The safe pipeline is classify, bound, copy or make accessible, validate fixed fields, validate declared variable lengths, authenticate checksum meaning, apply namespace and hooks, resolve fragments, choose local or forwarding behavior, demultiplex to an upper protocol, enqueue under bounded accounting, and transfer ownership once. Reject early enough to bound cost, but retain enough stage information to explain the rejection.

### Critical invariants

- Every header access proves `offset + required <= validated_extent` with overflow-safe arithmetic before dereference.
- Variable-length chains have independent byte, element, nesting, and work budgets; a packet cannot force unbounded parsing.
- Fragment queues use a complete key, reject prohibited overlaps, cap fragments and bytes, expire on a timer, and charge memory before insertion.
- Checksum state names the verified layer and coverage; transformations update or invalidate it before later code relies on it.
- Namespace, device, mark, security label, hook result, and route context remain attached to the packet across deferral and reinjection.
- Local delivery, forwarding, multicast, broadcast, raw observation, and control-error generation are explicit branches with distinct policy.
- No transport lookup uses ports, flags, sequence numbers, or payload until the entire required transport header is accessible and validated.
- Per-CPU batching and lockless lookup preserve endpoint lifetime through references, RCU, or another stated protocol.
- Drops, errors, retries, and generated control traffic are bounded and attributed to one processing stage.
- Completion of protocol processing transfers or releases the packet exactly once, including every hook, clone, fragment, and error path.

### Common failures

Common failures are checking captured bytes but not the protocol-declared length, retaining pointers across pull or linearization, walking extension headers without a budget, dispatching on an unvalidated next-header value, accepting contradictory IPv4 lengths, treating checksum-offload state as a universal trust bit, reassembling fragments under an incomplete key, accepting prohibited overlaps, allocating fragment state before charging it, applying policy only before reassembly when rules require the final datagram, generating recursive ICMP errors, performing socket lookup in the wrong namespace, racing endpoint destruction, changing packet bytes without invalidating flow hashes and checksums, silently dropping under backlog pressure, and measuring only final socket delivery.

### Compact example

Three non-overlapping fragment ranges arrive for a 24-byte payload: $[0,8)$, $[16,24)$, and $[8,16)$. The reassembly tracker reports 16, then 8, then 0 missing bytes. Completion at zero still does not authorize delivery: the implementation must retain a valid first-fragment header, rebuild consistent lengths, verify the reassembled upper-layer checksum where required, apply the correct post-reassembly policy, and transfer the assembled packet once.

### Connections

[OS-024](024-atomic-operations.md), [OS-038](038-memory-mapped-files.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), and [OS-073](073-network-buffers.md) connect protocol processing to memory, concurrency, queues, buffers, sockets, and timers.

## Governing Question

A received frame is only evidence that some bytes arrived. It is not yet evidence that those bytes form a legal IP datagram, belong to this namespace, contain a complete transport header, pass policy, identify a live endpoint, or can be admitted to that endpoint's queue. Protocol processing builds those conclusions one bounded proof at a time.

The governing question is how to build a fast path whose shortcuts never outrun their proofs. Parsing, checksum offload, reassembly, flow caches, per-CPU batching, hooks, routing, and socket lookup all save work or add policy, but each also creates state that can become stale under mutation, timeout, migration, teardown, or adversarial input.

## Why This Matters

Protocol code consumes hostile lengths, offsets, flags, identifiers, and checksums at high packet rates. One unchecked addition can become an out-of-bounds read. One unbounded fragment table can become a memory attack. One stale endpoint pointer can become a use-after-free. These are operating-system integrity problems, not merely malformed-traffic problems.

Correct protocol processing also determines interoperability. Hosts must tolerate loss, duplication, reorder, varying MTUs, optional headers, delayed fragments, and control messages while implementing precise standards behavior. An optimization that changes externally visible acceptance, ordering, checksum, or error semantics is not transparent.

Finally, this path is a major performance boundary. Cache misses, fragment access, hash lookup, hooks, route lookup, lock contention, timer work, and socket queuing all multiply by packet rate. The design must bound worst-case work and expose where CPU and memory were spent.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-007](007-kernel-data-structures.md), [OS-024](024-atomic-operations.md), [OS-038](038-memory-mapped-files.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-063](063-direct-memory-access.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), and [OS-073](073-network-buffers.md).

Retrieve these distinctions:

- frame length, network-layer declared length, fragment length, transport length, and backing capacity are different bounds;
- packet bytes, device metadata, buffer metadata, cached parse results, and protocol state have different trust origins;
- hardware checksum result, software checksum result, partial checksum, pseudo-header coverage, and absent checksum are different states;
- IP options, IPv6 extension headers, encapsulation headers, transport options, and application framing use different grammars;
- fragment reception, reassembly completion, validation, policy acceptance, and endpoint delivery are different events;
- local address, route result, namespace, interface, mark, security label, and socket binding jointly affect delivery;
- raw sockets, packet taps, protocol handlers, established sockets, listeners, multicast groups, and error queues are different consumers;
- a softirq, worker, timer, process context, and device interrupt permit different operations;
- ICMP generation, ICMP reception, local errors, asynchronous socket errors, and application-visible failure are not synonymous;
- packet drop, policy rejection, checksum failure, no route, no endpoint, queue overflow, and memory exhaustion identify different stages.

## Learning Objectives

After this module, you should be able to:

1. trace IPv4 and IPv6 receive processing from network-header validation through hooks, reassembly, local or forwarding selection, transport demultiplexing, and socket admission;
2. design cursor-based parsing for fixed headers, options, extension chains, encapsulation, fragments, and nonlinear buffers;
3. preserve checksum, length, namespace, route, security, mark, hash, timestamp, and offload semantics through transformations;
4. bound reassembly memory, parser work, hook behavior, control-message generation, per-CPU backlogs, and endpoint queues;
5. reason about RCU lookups, references, per-CPU processing, timers, reinjection, endpoint teardown, and CPU migration;
6. distinguish local delivery, forwarding, multicast, raw observation, control traffic, and rejection paths;
7. diagnose protocol drops and latency with stage-specific counters, traces, packet evidence, state snapshots, and scoped experiments.

## Core Exposition

### Build trust monotonically

Begin with the smallest trusted fact: the buffer exposes a reported number of bytes. A parser may then prove a version-specific fixed header, a declared datagram extent, a bounded chain of optional headers, and finally an upper-layer header. Each proof has a scope. Validation of the outer IPv6 header does not validate an extension header; validation of an extension chain does not validate TCP options.

Store offsets and validated extents rather than raw pointers when a buffer may be pulled, copied, linearized, reassembled, or transformed. Reacquire an address after any operation that can relocate storage. A safe helper returns failure without leaving a partially trusted cursor.

### Establish the actual datagram extent

The backing allocation can exceed the packet, and the received frame can include link padding. IPv4 supplies an Internet Header Length and Total Length. The processor checks version, minimum and maximum header length, total length at least header length, and total length no greater than available bytes before trimming padding or reading options.

IPv6 has a fixed 40-byte base header and a Payload Length, with separately specified handling for exceptional forms such as jumbograms. The parser computes the claimed end with checked arithmetic and never silently substitutes backing capacity for the declared extent. An encapsulated inner packet establishes a new bounded extent within the outer one.

### Walk variable headers with explicit budgets

IPv4 options and IPv6 extension headers are typed variable-length grammars. For each element, validate the bytes needed to learn its length, validate its format-specific minimum and alignment, then prove the full element lies within the current extent. Unknown options follow the protocol's required action rather than a universal skip rule.

Use several budgets: maximum parsed bytes, number of headers, nesting depth, and CPU work. A byte bound alone may not constrain a pathological chain of minimum-sized elements. Record why parsing ended: upper protocol found, no-next-header, unsupported element, malformed length, policy limit, or truncation.

### Treat cached parse metadata as a proof certificate

Header offsets, protocol identifiers, flow hashes, checksum states, route caches, and offload flags save repeated parsing. They are valid only for the bytes and context that produced them. Pulling a header, decapsulating a tunnel, rewriting an address, reassembling fragments, changing namespace, or selecting another output device can invalidate some or all of them.

Define invalidation centrally. A transformation either updates dependent metadata through a proved incremental rule or clears it so the next consumer recomputes. Stale metadata is more dangerous than absent metadata because it can bypass work.

### Validate checksums at the correct layer

IPv4 includes a header checksum; transport protocols may cover their header, payload, and a pseudo-header derived from IP addresses, protocol, and length. IPv6 does not have a base-header checksum. UDP checksum rules differ by IP version and context. ICMP and ICMPv6 have their own coverage.

Offload metadata says which checksum work hardware or earlier software performed. The processor verifies that metadata matches device capability, encapsulation depth, checksum level, and current header offsets. A checksum proves accidental-corruption detection over covered fields; it does not authenticate a sender or authorize a packet.

### Make fragmentation a bounded subsystem

Fragments arrive independently and may be duplicated, reordered, inconsistent, overlapping, or never completed. Key a reassembly queue with every field required by the protocol and namespace. Preserve the necessary unfragmentable or first-fragment header, validate offsets and lengths, and apply the standard's overlap rules. IPv6 requires discarding a datagram when fragments overlap.

Charge memory before queue insertion. Bound bytes, queues, fragments per queue, source contribution, and lifetime. Use timer and memory-pressure eviction that removes hash membership, timers, fragments, accounting, and references exactly once. Reassembly completion proves byte coverage; it does not replace upper-layer checksum or policy validation.

### Order hooks and transformations deliberately

Packet hooks expose defined points before or after routing, local delivery, forwarding, and output. A hook can clone, queue, redirect, translate, or reinject a packet. The implementation must define whether a policy sees fragments or reassembled datagrams, outer or inner headers, original or translated addresses, and pre- or post-route context.

Reinjection is a state transition, not an arbitrary jump to a function label. Carry a generation or continuation describing which stages already ran, prevent accidental recursion, restore execution context, and validate any userspace or asynchronous verdict before use. A queued verdict cannot retain an unprotected namespace, device, route, or socket pointer.

### Decide local delivery versus forwarding

After valid network-layer processing and the applicable early hooks, the stack decides whether the destination is local, forwarded, multicast, broadcast, or rejected. Local delivery and forwarding share parsing but differ in hop-limit or TTL changes, routing, redirects, output policy, fragmentation, and error generation.

Forwarding decrements TTL or hop limit under the protocol rule, applies routing and policy, enforces output MTU, and never treats a host-only assumption as router behavior. Local delivery preserves the transport context needed for endpoint lookup. OS-075 develops route and neighbor data structures; this module focuses on their typed results and failure handling.

### Demultiplex to the upper protocol

Dispatch only after the next-protocol identifier and required header bytes are valid. A protocol registry must define lookup lifetime, module removal, namespace scope, raw observers, and unknown-protocol behavior. Delivering to a raw observer may require a clone or shared read-only reference; it must not steal the packet from the normal handler accidentally.

For UDP, validate header availability and datagram length before endpoint lookup and checksum decisions. For TCP, validate the fixed header, data offset, flags and option extent before consulting sequence or connection state. OS-076 develops connection-state machinery; here the essential rule is that malformed segments never reach state transitions as if their fields were trustworthy.

### Perform endpoint lookup in the full context

An endpoint key can include namespace, address family, protocol, local and remote addresses, ports, bound interface, wildcard rules, device, transparent-proxy state, mark, cgroup or security policy, and reuse group. A fast hash must implement the same precedence as the slow semantic lookup.

Protect the result through RCU, a reference, a lock, or a generation validation that spans every dereference. A successful hash match followed by endpoint destruction is not successful delivery. Listener selection and established-flow selection may use different tables and load-distribution rules.

### Admit work to bounded queues

Before queueing to a socket or protocol worker, charge the packet's actual accounted memory and any ancillary state. Enforce object and byte limits. Wakeups occur only after the item is visible, and consumers recheck the predicate under the synchronization contract so a wake cannot be lost.

Backpressure depends on protocol. A reliable transport can advertise less receive space and eventually reject new work; UDP may drop a datagram. The stack records the exact queue and reason. Unbounded deferral merely moves overload from CPU to memory.

### Constrain deferred execution

Network receive work often runs in a deferred interrupt context where sleeping is forbidden and CPU time must be shared. Budget packets, bytes, time, or all three. Large reassembly, expensive options, policy hooks, cryptography, and error processing cannot monopolize one poll cycle.

Per-CPU queues improve locality but require explicit behavior for CPU hotplug, flow migration, remote enqueue, and timer execution. Receive steering can move protocol work away from the device CPU, adding an inter-processor queue and ordering boundary.

### Generate control errors without amplification

An error path may generate ICMP or ICMPv6 with a quote of the triggering packet. Check whether the triggering packet is eligible for an error, select a valid source, bound and initialize the quote, route the response, apply policy, rate-limit it, and account allocation. Do not emit an ICMP error in response to classes for which the specification forbids it.

Failure to allocate or route a control response does not resurrect the original packet. Control-message generation is secondary bounded work. Record the original processing error separately from response-generation failure.

### Process output as another validation pipeline

Locally generated and forwarded packets need valid lengths, headers, checksums, routes, MTUs, hooks, transformations, and device features. Transport construction may leave a partial checksum or segmentation request, but the final path verifies that the chosen device supports it or performs software fallback.

Path MTU information is cached with scope and lifetime, not treated as immutable truth. IPv6 routers do not fragment forwarded packets; sources respond to Packet Too Big information and perform source fragmentation when appropriate. IPv4 handling depends on size, Don't Fragment, path policy, and host or router role.

### Observe stages, not one aggregate outcome

Maintain counters for version rejection, fixed-header length, declared-length conflict, option or extension failure, checksum state, fragment insertion and eviction, hook verdict, local-address decision, TTL or hop-limit expiry, route failure, unknown protocol, transport length, endpoint miss, socket admission, backlog overflow, ICMP suppression, and response failure.

Counters need namespace, CPU, interface, protocol, hook, route, and endpoint context where feasible without unbounded cardinality. Sampled traces join packet identity and stage transitions. Packet capture at one observer proves only the bytes visible at that point; offloads and transformations may make another observer see different bytes.

### Test the state graph under faults

Generate truncated headers at every byte, contradictory declared lengths, maximum option chains, unknown next-header values, nesting limits, checksum variants, fragments in all orders, duplicates, overlaps, gaps, timeouts, memory pressure, and hash collisions. Inject allocation and queue-admission failure at each state transition.

Race fragment expiry with completion, endpoint lookup with close, hook queueing with namespace teardown, timer work with CPU hotplug, and route invalidation with output. Assert no packet is delivered twice, leaked, used after release, or charged after final destruction. Differential tests against an independent parser help expose shared assumptions.

## Definitions and Notation

Let packet storage expose an accessible extent $E$ bytes and let the protocol declare an extent $D$. A parse of $n$ bytes at offset $o$ is permitted only when

$$
0 \le o \le D \le E
\quad\text{and}\quad
0 \le n \le D-o.
$$

The subtraction form avoids accepting a wrapped sum $o+n$. For nested protocol $i$, let $[b_i,e_i)$ be its proved extent. Then

$$
b_i \le b_{i+1} \le e_{i+1} \le e_i.
$$

Let a parser budget be $B=(B_b,B_h,B_d,B_w)$ for bytes, headers, nesting depth, and abstract work. Every loop iteration decreases at least one finite component and never increases another without an explicit replenishment rule.

For a fragment with byte range $I_j=[a_j,b_j)$, valid coverage requires $0\le a_j<b_j\le M$, where $M$ is the established final payload end. Let $U=\bigcup_j I_j$. Reassembly is complete when

$$
U=[0,M)
$$

and all required first-fragment and consistency conditions hold. Completeness alone does not decide overlap legality.

Let endpoint lookup be

$$
L(n,p,s_a,d_a,s_p,d_p,i,m,\sigma)\rightarrow (x,g),
$$

where $n$ is namespace, $p$ protocol, addresses and ports form the flow, $i$ is ingress or bound interface, $m$ is mark or policy context, $\sigma$ is security context, $x$ is an endpoint, and $g$ its protected lifetime token or generation.

For processing queue $q$, require both object and byte bounds:

$$
0\le N_q\le C_q,
\qquad
0\le A_q=\sum_{p\in q}\operatorname{charge}(p)\le M_q.
$$

Let $V_j$ be a validation certificate such as header extent, checksum coverage, flow hash, or route. A transformation $T$ preserves $V_j$ only if its contract proves

$$
V_j(b,c) \Rightarrow V_j(T(b),T(c));
$$

otherwise $T$ clears $V_j$ before publication.

## Mechanisms, Invariants, or Proof Structure

Use these obligations to review a protocol path.

1. **Backing obligation:** the packet backing and reported receive length remain owned and accessible throughout parsing.
2. **Extent obligation:** every layer derives a declared extent within its parent's validated extent with overflow-safe arithmetic.
3. **Cursor obligation:** every fixed and variable header access proves coverage before reading even the field that describes further length.
4. **Budget obligation:** extension, option, encapsulation, fragment, hook, and deferred-work loops have finite independent limits.
5. **Checksum obligation:** checksum metadata identifies exact coverage and is updated or invalidated after dependent bytes change.
6. **Fragment obligation:** queue keys are complete; ranges, consistency and overlap rules are enforced; memory and timers are bounded.
7. **Context obligation:** namespace, device, mark, label, hook continuation and route meaning survive every deferral or reinjection.
8. **Branch obligation:** local, forward, multicast, raw, unknown-protocol, control-error and drop paths have explicit ownership outcomes.
9. **Lookup obligation:** upper-protocol and endpoint tables implement semantic precedence and protect result lifetime through use.
10. **Admission obligation:** protocol and socket queues charge actual resources before insertion and preserve wakeup ordering.
11. **Error obligation:** generated control traffic is standards-eligible, initialized, routed, policy-checked, rate-limited and independently accounted.
12. **Release obligation:** success and every failure path transfer, clone, queue or destroy the packet exactly once and retire all dependent state.

A useful safety argument is inductive. Initially only backing extent and ingress context are trusted. Each stage consumes previously proved facts and either adds a narrower certificate or terminates with an owned drop. Transformations explicitly invalidate dependent certificates. Therefore no later stage can legally consume an unproved byte, stale context, or dead object if every transition satisfies its obligation.

This is a proof structure, not a proof of an implementation. Real assurance also needs standards conformance, code review, sanitizers, lock and RCU diagnostics, packet generators, fuzzing, fault injection, reference tracking, namespace teardown tests, device offload coverage, and measurements on the deployed kernel and hardware.

## Alternatives and Trade-Offs

- **Linearize early versus parse fragments:** linearization simplifies parsers but copies bytes and can fail; fragment-aware reads preserve zero copy but expand boundary cases.
- **Strict layering versus shared metadata:** strict layers isolate reasoning; cached cross-layer metadata saves work but enlarges invalidation contracts.
- **Drop unknown extensions versus follow standards actions:** dropping is operationally simple but may break extensibility; correct action bits preserve interoperability and require careful policy.
- **Reassemble before policy versus inspect fragments:** reassembly exposes final semantics but costs memory; early fragment policy bounds attack surface but cannot always see upper headers.
- **Global reassembly limits versus per-tenant limits:** global limits are simple but allow one tenant to evict another; hierarchical limits improve isolation with more accounting.
- **Copy fragments versus retain references:** copying simplifies lifetime and compaction; retaining pages saves bandwidth but pins large backing for small useful ranges.
- **Software checksums versus hardware offload:** software gives a direct evidence point and costs CPU; offload saves work but depends on truthful scoped metadata.
- **One shared protocol queue versus per-CPU queues:** sharing simplifies ordering and accounting; per-CPU queues improve locality but complicate migration and global fairness.
- **Locked endpoint tables versus RCU lookup:** locks simplify lifetime reasoning and contend on fast paths; RCU accelerates reads but requires disciplined removal and deferred reclamation.
- **Cache route and parse results versus recompute:** caches reduce repeated work; mutation and policy changes demand precise generations and invalidation.
- **Inline hooks versus asynchronous verdicts:** inline hooks reduce lifetime complexity; asynchronous policy permits richer decisions while pinning packet and context state.
- **Rich tracing versus minimal overhead:** detailed events localize failures; high-cardinality tracing can perturb the exact packet path under study.
- **Large processing batches versus short latency:** batching amortizes overhead; large batches delay other flows, timers and control work.
- **Generate detailed errors versus suppress aggressively:** errors aid diagnosis and protocol adaptation; quotes and responses consume bandwidth and can amplify attacks.
- **Fail closed versus compatibility fallback:** strict rejection limits ambiguity; fallback can preserve legacy connectivity but must never bypass security or bounds.
- **Generic protocol framework versus specialized fast paths:** generic dispatch reduces duplication; specialized paths improve locality but risk semantic drift.

## Failure Modes and Misconceptions

- “The DMA length makes every header safe.” It bounds received bytes, not protocol-declared structure.
- “A packet is linear because the fixed IP header is linear.” Options, extensions, transport headers, and payload can cross fragments.
- “Checking `offset + length` is sufficient.” The addition itself may overflow; use checked arithmetic or subtraction bounds.
- “IPv6 has no checksum.” The base header lacks one, while upper protocols and ICMPv6 have their own checksum rules.
- “Checksum verified means authentic.” A checksum detects covered corruption; it does not establish identity or policy authorization.
- “All fragments carry the transport header.” Later fragments generally do not, so transport policy cannot assume ports are present.
- “Coverage without gaps is valid reassembly.” Overlap, key, consistency, first-header, size, and timeout rules also matter.
- “Duplicate fragments are free.” They still consume parsing, lookup and comparison work and can become an attack.
- “A fragment timeout only deletes a hash entry.” Timers, charges, pages, references and optional control responses also require retirement.
- “Extension headers can be followed until the packet ends.” A valid packet still needs implementation work and nesting limits.
- “Unknown protocol means malformed.” It may be valid but unsupported, requiring defined raw delivery or control behavior.
- “Hooks see one canonical packet.” Hook position determines fragment, translation, encapsulation, route and checksum view.
- “Reinjection can restart anywhere.” Skipping or repeating stages can bypass policy, recurse, or double-transform bytes.
- “The route decides the namespace.” Namespace and policy context precede and constrain route lookup.
- “A hash match is a live socket.” Endpoint lifetime must remain protected after lookup.
- “Wildcard binding precedence is an optimization detail.” Fast and slow paths must implement identical externally visible selection.
- “Socket queue length counts memory.” One object can retain far more allocation than its payload; byte accounting is also required.
- “UDP overload creates backpressure.” Datagram delivery commonly drops; applications need explicit loss and capacity semantics.
- “Forwarding is local delivery plus another output call.” TTL, routing, MTU, redirects, hooks and error rules differ.
- “ICMP can report every failure.” Specifications suppress several cases, and rate limits prevent reflection and amplification.
- “Packet Too Big proves a permanent MTU.” Path information has validation, scope, aging and attack considerations.
- “Per-CPU processing has no shared state.” routes, fragments, endpoints, policy and timers cross CPUs and lifetimes.
- “Dropping early is always cheaper.” A sophisticated early policy can cost more than a bounded parse and simple later rejection.
- “One final drop counter is enough.” It cannot separate malformed input, policy, routing, reassembly, endpoint and capacity failures.
- “A passing loopback test covers the path.” Loopback omits physical DMA, many offloads, device queues, MTU differences and real topology.

## Worked Examples

### Example 1

An IPv4 receive buffer exposes 1,514 bytes after its link header. The IP header claims IHL 24 bytes and Total Length 1,480. The processor validates 24 within the fixed bounds, validates 1,480 at least 24 and no more than 1,514, then trims 34 bytes of link padding before upper processing.

Using 1,514 as transport coverage would let padding influence parsing or checksum decisions.

### Example 2

The following executable model admits three fragment ranges and reports uncovered bytes. It demonstrates checked, non-overlapping interval coverage, not an IP implementation.

<!-- bijux-verify: {"id":"bounded-fragment-coverage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"range=[0,8) missing=16\nrange=[16,24) missing=8\nrange=[8,16) missing=0\ncomplete=True\n","stderr":""}} -->
```python
total = 24
fragments = [(0, 8), (16, 24), (8, 16)]
covered = []

for start, end in fragments:
    if not (0 <= start < end <= total):
        raise ValueError("range")
    if any(start < old_end and old_start < end for old_start, old_end in covered):
        raise ValueError("overlap")
    covered.append((start, end))
    covered.sort()
    merged = []
    for left, right in covered:
        if merged and left == merged[-1][1]:
            merged[-1] = (merged[-1][0], right)
        else:
            merged.append((left, right))
    present = sum(right - left for left, right in merged)
    print(f"range=[{start},{end}) missing={total - present}")

print(f"complete={covered[0][0] == 0 and sum(b - a for a, b in covered) == total}")
```

Production reassembly additionally validates keys, alignment, final length, header consistency, overlap policy, memory, timers, checksums and ownership.

### Example 3

An IPv6 packet contains four extension headers whose total size is valid, but policy permits at most three headers. The parser stops with a distinct budget-exceeded reason rather than reading a fourth header or reporting truncation.

Operators can then distinguish implementation policy from malformed bytes and tune only with security and workload evidence.

### Example 4

A tunnel decapsulator removes an outer IPv4 and UDP header. The old flow hash, route, network offsets and checksum-level metadata described the encapsulated packet. The decapsulator resets inner offsets and invalidates or adjusts each dependent field before reinjection.

Leaving the outer flow hash could steer the inner flow inconsistently or select the wrong endpoint cache entry.

### Example 5

Two IPv6 fragments overlap by eight bytes. Even if the overlapping bytes are identical and total coverage would be complete, the receiver discards the entire datagram under the IPv6 fragmentation rule and retires the queue once.

“Identical overlap” is not a local compatibility exemption.

### Example 6

A UDP datagram declares length 48, but the reassembled IP payload is 40 bytes. The processor rejects it before endpoint lookup. It does not clamp the UDP length to available bytes or deliver a short message.

The stage counter records transport-length failure, not no-listener or socket overflow.

### Example 7

An established-socket hash lookup finds an endpoint while another CPU begins close. RCU protects the table node, but the receive path also needs the socket-specific lifetime or validation contract before queueing.

RCU visibility alone does not guarantee that the endpoint still accepts new packets.

### Example 8

A hook queues a packet for an asynchronous verdict. Before the verdict returns, its namespace is dismantled. The queued object holds defined references and teardown cancels or drains it; reinjection validates the continuation generation.

Storing only a raw hook index and device pointer would create stale-context use.

### Example 9

A router receives an IPv6 packet larger than the output MTU. It does not fragment the packet. It drops under the forwarding rule and attempts a rate-limited ICMPv6 Packet Too Big response with a properly bounded quote.

Failure to allocate that response is recorded separately and cannot retain the original packet.

### Example 10

Application receive latency increases. Device and NAPI counters are normal; extension-header budget drops rise on one namespace; fragment and checksum counters are flat; socket queues are short.

The evidence localizes the symptom to protocol parsing policy. Increasing receive rings would add latency without addressing the rejection source.

## Cross-Program Connections

- **Network engineering:** IP versions, extensions, fragmentation, ICMP, MTU, transport checksums, forwarding and interoperability define external semantics.
- **Security engineering:** hostile parsing, algorithmic complexity, overlapping fragments, namespace isolation, hooks, raw sockets and control amplification define attack surfaces.
- **Data structures engineering:** cursors, interval sets, hash tables, radix structures, queues, timers, reference counts and RCU organize the path.
- **Distributed systems:** loss, duplication, reorder, unreliable datagrams, endpoint identity, control feedback and partial failure begin at protocol processing.
- **Performance engineering:** batching, cache locality, per-CPU queues, offloads, hook cost, parsing budgets and observer effect shape packet-rate capacity.
- **API and service engineering:** socket selection, datagram boundaries, stream segments, asynchronous errors, queue admission and backpressure become application behavior.
- **Platform engineering:** namespaces, cgroups, policy hooks, telemetry, kernel configuration, offload rollout and incident isolation operationalize the subsystem.
- **Formal methods:** parser totality, refinement of untrusted bytes, transition invariants, resource bounds and lifetime proofs make acceptance reviewable.
- **Reliability engineering:** timer expiry, memory pressure, endpoint close, CPU hotplug, namespace teardown and fault injection expose recovery correctness.
- **Computer architecture:** byte order, alignment, cache lines, NUMA, DMA and memory ordering constrain how protocol fields can be accessed efficiently.

## References

1. IETF, [RFC 1122: Requirements for Internet Hosts—Communication Layers](https://www.rfc-editor.org/rfc/rfc1122.html), host IP and transport processing, validation, reassembly, ICMP, robustness and implementation requirements; retrieved 2026-09-04.
2. IETF, [RFC 8200: Internet Protocol, Version 6 Specification](https://www.rfc-editor.org/rfc/rfc8200.html), IPv6 headers, extension processing, payload length, fragmentation, reassembly and forwarding; retrieved 2026-09-04.
3. IETF, [RFC 9293: Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293.html), TCP header, options, state variables, segment processing, checksums and errors; retrieved 2026-09-04.
4. IETF, [RFC 768: User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768.html), UDP header, length, checksum, pseudo-header and delivery interface; retrieved 2026-09-04.
5. IETF, [RFC 4443: Internet Control Message Protocol for IPv6](https://www.rfc-editor.org/rfc/rfc4443.html), ICMPv6 errors, informational messages, checksum, suppression, quoting and rate limiting; retrieved 2026-09-04.
6. IETF, [RFC 6864: Updated Specification of the IPv4 ID Field](https://www.rfc-editor.org/rfc/rfc6864.html), IPv4 identification semantics for atomic and non-atomic datagrams; retrieved 2026-09-04.
7. IETF, [RFC 8900: IP Fragmentation Considered Fragile](https://www.rfc-editor.org/rfc/rfc8900.html), fragmentation failure modes, middleboxes, resource costs and operational guidance; retrieved 2026-09-04.
8. IETF, [RFC 8201: Path MTU Discovery for IP version 6](https://www.rfc-editor.org/rfc/rfc8201.html), Packet Too Big validation, path MTU state, source behavior and robustness; retrieved 2026-09-04.
9. IETF, [RFC 1191: Path MTU Discovery](https://www.rfc-editor.org/rfc/rfc1191.html), IPv4 Don't Fragment, ICMP feedback, cached MTU and timer behavior; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html), receive protocol-processing placement, RPS/RFS, per-CPU backlog, flow ordering and CPU selection; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design a parser for an IPv6 packet containing a base header, a bounded extension chain, a transport header that may cross fragments, and optional tunnel decapsulation. State cursor, length, budget, metadata-invalidation, checksum and failure-ownership rules.

### Exercise 2

Trace three fragments $[0,1024)$, $[1536,2048)$ and $[1024,1536)$ through a reassembly subsystem. Include keying, charging, overlap policy, timer concurrency, completion, policy, checksum and final release. Then analyze an overlapping fourth fragment.

### Exercise 3

Specify a namespace-aware UDP endpoint lookup and admission path supporting exact bindings, wildcard bindings, interface binding, reuse groups, raw observers, concurrent close and bounded receive queues.

### Exercise 4

Design error handling for a router that receives expired TTL or hop limit, an output-MTU failure, an unsupported upper protocol, and malformed fragments under a packet flood. Separate original failure from control-response outcome.

### Exercise 5

Construct a validation and observability plan for a protocol processor using checksum offload, RPS, per-CPU backlogs, fragment reassembly, policy hooks and asynchronous reinjection. State what the tests cannot prove.

## Answers to the Exercises

### Answer 1

Initialize the outer cursor with offset zero and an extent no larger than received bytes. Copy the 40-byte IPv6 base header through a fragment-aware bounded helper. Validate version and payload-length arithmetic, then set the declared extent. Do not retain the returned pointer across any buffer operation.

For each extension, first fetch only the fixed bytes needed to identify type and encoded length. Convert that length with checked arithmetic, enforce format minimum and alignment, prove it within the declared extent, and decrement independent byte, header, depth and work budgets. Apply the standard action for an unknown option. Record a precise stop reason. Before transport dispatch, make the entire required fixed header accessible and validate its own length field or data offset.

For decapsulation, validate the outer protocol and full removable range before mutation. Establish an inner extent within the authenticated outer extent, acquire write authority, remove or advance past the outer headers, and reacquire locations. Reset network and transport offsets. Invalidate outer route, flow hash, checksum level, security and offload metadata unless a proved mapping preserves them. Reinjection carries namespace, device, mark, policy continuation and a nesting generation.

Checksum processing verifies exactly the claimed layer and pseudo-header. If hardware metadata does not match current offsets, encapsulation or device capability, fall back to software or reject according to the interface. Every malformed, unsupported, budget, allocation and policy failure leaves one owner that drops and accounts once; successful decapsulation transfers the same packet once to the next stage.

### Answer 2

Construct a queue key from namespace, IP version, source, destination, protocol, fragment identification and any other implementation context required to prevent cross-domain mixing. Validate each fragment's header, offset units, non-final alignment, computed end and datagram maximum before allocation. Charge its retained memory before inserting it into a bounded interval structure.

After $[0,1024)$ the known covered prefix is 1024. After $[1536,2048)$ a gap remains. Inserting $[1024,1536)$ closes the gap and establishes coverage $[0,2048)$, assuming the final fragment established 2048 as the final end and all header-consistency rules hold. Preserve the required first-fragment header and rebuild declared lengths. Remove the queue from lookup and cancel or synchronize its timer under one state transition so completion and expiry cannot both free it.

Completion creates one valid packet, releases fragment-specific references and transfers aggregate accounting rather than losing it. Apply policy at the specified post-reassembly hook, validate the transport header and checksum, then deliver or drop once. If an overlapping fourth fragment arrives before completion, follow the IP-version rule; for IPv6, discard the entire datagram. A duplicate or overlap after completion belongs to a new or absent queue according to key lifetime and cannot mutate the delivered packet.

### Answer 3

Parse and validate the entire UDP header first. Prove UDP length is at least the header and no greater than the validated IP payload; apply version-specific checksum rules. Build the lookup key from namespace, address family, protocol, local and remote addresses and ports, ingress interface, mark and security or transparent-proxy context.

Lookup exact connected bindings before less-specific local bindings according to the implementation's published semantics. Interface-bound endpoints must match the correct device context. Reuse-group selection uses a stable flow hash over validated fields and a membership generation; it does not silently change wildcard precedence. Raw observers receive explicit clones or protected shared references and do not consume the UDP handler's ownership.

Protect the selected endpoint with the table's RCU read-side protocol plus the socket-specific acquire or validation needed to cross concurrent close. Recheck state if the lifetime contract requires it. Charge SKB truesize and ancillary data to the socket, cgroup and protocol before insertion. Enforce object and byte bounds, publish the queue entry before wakeup, and record no-endpoint separately from queue overflow, policy rejection and checksum failure. Every unsuccessful branch releases the packet once.

### Answer 4

Classify the original failure first. Expired TTL or hop limit, output MTU, unknown upper protocol and malformed fragments increment separate counters with namespace, interface, address family and stage context. Drop or retain the original only as required while constructing a quote; never transfer original ownership implicitly to the response path.

For an eligible TTL or hop-limit expiry, build Time Exceeded. For IPv6 output-MTU failure, build Packet Too Big with the valid next-hop MTU; IPv4 behavior depends on Don't Fragment and fragmentation rules. Unknown protocol may generate the specified unreachable or parameter response only when allowed. Malformed or overlapping fragments often suppress error generation, especially when required identifying material is unavailable or the triggering packet is itself an error.

Before response allocation, apply global, per-source, per-namespace and message-type rate limits. Bound and initialize the quote, select a legal source address, compute the correct checksum, route, apply output policy and account all memory. Allocation, source selection, policy, route and transmit failures each get response-path counters. A suppressed or failed response does not change the already recorded original failure and never triggers recursive error generation.

### Answer 5

Generate every truncation boundary for IPv4, IPv6, extension, UDP, TCP and ICMP headers; contradictory lengths; overflow-adjacent offsets; unknown options; maximum chains; nesting limits; checksum states; and nonlinear layouts. Compare accepted fields with an independent parser. Run offload enabled, disabled, falsely advertised and invalidated after transformation.

Generate fragments in order, reverse order and random order, plus duplicates, gaps, conflicting finals, prohibited overlaps, queue-hash collisions, timeout races and memory-pressure eviction. Verify hierarchical limits and exact charge retirement. Exercise hooks that accept, drop, clone, transform, queue and reinject, with invalid verdicts, repeated continuations, endpoint close, namespace teardown and route change.

Vary RPS CPU maps, remote backlog saturation, CPU hotplug, flow migration and batch budgets. Race endpoint table removal, listener group changes, timer expiry and socket admission. Inject allocation failure at each point. Use memory, bounds, leak, lock, RCU and reference diagnostics; packet capture before and after transformations; and stage-specific counters and sampled traces.

Measure packets, bytes, cycles, cache misses, remote enqueues, parser depth, fragment occupancy, hook delay, lookup collisions, queue charge, drops and latency percentiles by namespace and CPU. Record kernel, configuration, hardware, device features, topology, traffic, faults and instrumentation. Finite tests cannot prove all hostile grammars or interleavings; loopback cannot prove physical-device offloads; a reference parser can share specification mistakes; passing throughput cannot prove standards conformance, security or safe teardown. State those limits.
