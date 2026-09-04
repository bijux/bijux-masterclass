---
module_id: OS-078
program: Operating Systems
level: 2
module_number: 78
title: Packet Filtering
status: complete
last_verified: 2026-09-04
---

# Packet Filtering

## One-Page Review

### Governing question

How should an operating system evaluate packet policy at multiple network-path hooks while preserving bounded parsing, deterministic rule semantics, namespace isolation, stateful-flow correctness, atomic ruleset replacement, safe offload, resource limits, and enough evidence to explain every verdict?

### Essential definitions

- A **hook** is a named point in ingress, local input, forwarding, local output, egress, bridge, socket, or device processing where policy can observe a specific packet representation.
- A **ruleset generation** is one immutable, internally consistent policy version visible to a packet evaluation.
- A **match** is a side-effect-free predicate over validated packet fields, metadata, context, or protected state.
- A **verdict** terminates or redirects evaluation, such as accept, drop, reject, queue, redirect, jump, return, or continue under the framework's semantics.
- A **base chain** attaches evaluation to a hook with family, priority, type, and default policy; an ordinary chain is reached through control flow.
- A **set** indexes many keys under one expression; a **map** associates keys with data or verdicts.
- **Connection tracking** classifies packets relative to a bidirectional flow record; it is distinct from the transport endpoint's own connection state.
- **NAT** transforms addresses or ports under a mapping and must update dependent checksums, routing, tuple state, and reply direction.
- A **stateless filter** decides from current packet and context; a **stateful filter** also consumes protected history.
- **Hardware offload** executes an eligible policy subset outside the ordinary software path while retaining semantic, lifecycle, counter, and fallback obligations.

### Central model, mechanism, or theorem

Represent filtering as

$$
F(G,H,P,C,S,B)\rightarrow(V,P',C',D),
$$

where $G$ is an immutable ruleset generation, $H$ the exact hook and priority, $P$ a validated packet view, $C$ namespace, device, route, socket, mark and security context, $S$ protected optional state such as connection tracking or rate limits, and $B$ execution, memory and response budgets. The outputs are verdict $V$, possibly transformed packet $P'$, updated state $C'$, and diagnostic attribution $D$.

One packet evaluation observes one coherent generation. Every field read has been proved present at that hook. Every state lookup includes namespace and direction. Every transformation invalidates or recomputes dependent metadata. “Accept” means only continue from this policy point; later hooks, routing, protocol processing, endpoint queues, or applications can still reject the packet.

### Critical invariants

- Rule input is limited to fields and metadata valid at the chosen hook; later-header assumptions cannot leak into earlier hooks.
- Each field access proves bounds across nonlinear buffers, fragments, tunnels, and variable headers before comparison.
- Chain traversal, jumps, expression work, set lookup, logging, queueing, and generated responses have explicit bounds.
- Rule order, priorities, family, chain control flow, default policy, set semantics, and verdict meaning are deterministic for one generation.
- Ruleset transactions validate all references and expressions before atomic publication; readers see all old or all new state.
- Connection tracking keys, zones, directions, timers, helpers, expectations, NAT mappings, and accounting are namespace-scoped and bounded.
- NAT occurs at defined stages and updates routes, checksums, hashes, offload metadata, reverse mappings, fragments, and ICMP quotations as required.
- Stateful decisions never label a packet authorized merely because a tuple resembles an established flow.
- Offloaded and software policy have stated semantic equivalence, counter behavior, generation lifetime, and failover.
- Every verdict is attributable without permitting unbounded logs, sensitive-data leakage, or a logging-induced denial of service.

### Common failures

Common failures are assuming all hooks see the same packet, reading ports from noninitial fragments, trusting cached offsets after NAT or decapsulation, interpreting connection-tracking `ESTABLISHED` as application authentication, forgetting reply direction, updating a live rule list in place, changing a set independently of rules that depend on it, creating unbounded per-source meters, allowing chain cycles or excessive jumps, rejecting all ICMPv6 and breaking path MTU discovery, applying IPv4 policy incompletely to IPv6, logging every hostile packet, accepting userspace verdicts after context teardown, counting only software packets after offload, and failing open when an offloaded rule is removed.

### Compact example

A first-match chain accepts tracked established traffic, drops a blocked source, accepts new TCP destination port 443, then defaults to drop. An established packet from any source hits the first rule. A new port-443 packet from the blocked source hits the earlier block rule and drops. A new DNS packet matches none and hits default drop. Reordering the block and established rules changes policy; it is not a performance-only edit. The packet's state label must also come from a live, directionally correct tracking record rather than its flags alone.

### Connections

[OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), [OS-075](075-routing-and-neighbor-tables.md), [OS-076](076-connection-state-management.md), and [OS-077](077-congestion-control-hooks.md) connect filtering to parsing, state, routes, namespaces, timers, concurrency, sockets, and overload.

## Governing Question

A packet can be filtered before an SKB exists, after device metadata is attached, before or after routing, before or after reassembly, on a bridge, at a traffic-control point, at a socket, and after transformations. Each hook has different valid fields, ownership, timing, and possible actions. “The firewall saw the packet” is therefore incomplete.

The governing question is how to express policy against an explicit packet view and publish it without a transient protection gap. Filtering must remain fast under normal traffic and bounded under adversarial traffic. Stateful conveniences such as connection tracking, NAT, dynamic sets, meters, asynchronous verdicts, and hardware offload add memory and lifetime graphs that must be governed independently from rule evaluation.

## Why This Matters

Packet filters enforce host, tenant and network boundaries inside the kernel. A parser bug, namespace leak, stale set, skipped fragment, mismatched offload, or ruleset replacement gap can bypass a security policy before applications see traffic.

Overly broad blocking can be equally destructive. IPv6 depends on selected ICMPv6 messages for Neighbor Discovery and path MTU behavior. Tunnels create inner and outer policy contexts. Stateful filters can drop valid failover or long-idle flows if timeout assumptions are wrong.

Filtering also sits on a denial-of-service boundary. Attackers choose packet diversity and rate. Per-flow state, logs, user queues, counters and helper parsing can consume more resources than the incoming bytes. Every optional feature needs precharged limits and a pressure policy.

## Prerequisites and Retrieval

Review [OS-007](007-kernel-data-structures.md), [OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), [OS-075](075-routing-and-neighbor-tables.md), [OS-076](076-connection-state-management.md), and [OS-077](077-congestion-control-hooks.md).

Retrieve these distinctions:

- device ingress, XDP, traffic control, bridge, prerouting, local input, forwarding, local output, postrouting and socket filters see different state;
- packet bytes, validated parse results, device metadata, route metadata, socket metadata and security labels have different trust origins;
- accept, continue, return, jump, goto, redirect, queue, drop, reject and application delivery are different outcomes;
- a rule, chain, table, set, map, stateful object and generation have different ownership and update semantics;
- transport connection state and firewall connection-tracking state are different objects with different timers and truth;
- original direction, reply direction, pre-NAT tuple and post-NAT tuple are separate views;
- fragment filtering, reassembly, extension-header parsing, tunnel decapsulation and transport matching occur in an explicit order;
- packet counter, byte counter, log record, trace event, hardware statistic and application outcome observe different populations;
- verifier memory safety, rule type safety, policy correctness and security completeness are different claims;
- fail-open, fail-closed, rollback, bypass and emergency management access are separate operational choices.

## Learning Objectives

After this module, you should be able to:

1. place filtering at hooks whose packet and context view matches the intended policy;
2. construct bounded, fragment-aware, tunnel-aware stateless matches and deterministic chain control flow;
3. design atomic ruleset transactions with immutable generations, validated references and safe reader lifetime;
4. reason about connection tracking, helpers, expectations, timers, NAT, reply direction and resource exhaustion;
5. preserve dual-stack, ICMP, path MTU, Neighbor Discovery, routing, namespace and application semantics;
6. validate software, verified-program and hardware-offloaded policy for semantic equivalence and safe fallback;
7. diagnose verdicts with generation, hook, rule, set, state, transformation, counter and trace evidence.

## Core Exposition

### Start with the enforcement objective

State which boundary is protected, which principals exist, what traffic is permitted, what must remain operational, and which failure mode is preferred. “Block port 22” is not enough: direction, namespace, interface, address family, fragments, tunnels, local services, replies and management recovery change its meaning.

Translate the objective into invariants before syntax. For example: only workload namespace A can initiate TCP to service B on 443; replies belonging to admitted flows may return; unrelated inbound traffic drops; required ICMP errors pass under validation; policy replacement never exposes a wider generation.

### Choose hooks by packet view

Early device hooks can drop cheaply before allocation or protocol work but may lack routes, sockets, reassembly, connection state or a conventional SKB. Later hooks provide richer context at higher cost. Bridge hooks see link forwarding that IP router hooks may not.

Document bytes and metadata available at each hook, whether fragments are reassembled, which address view applies around NAT, and which operations are legal. Do not copy a predicate among hooks merely because field names look similar.

### Validate before matching

A match is safe only after proving every requested byte. Check network version, declared length, header chain, fragmentation and transport extent using checked arithmetic and fragment-aware access. A verifier can prove a program checked `data_end` before direct access, but it cannot prove that a byte sequence is semantically the intended header.

Cached offsets and protocol identifiers are proof certificates tied to current bytes. NAT, encapsulation, decapsulation, reassembly, pull, trim or linearization can invalidate them. Recompute or clear dependent metadata centrally.

### Give chains explicit control flow

Base chains attach to hook and priority and define a terminal default. Ordinary chains encapsulate reusable evaluation. Specify first-match, continue, return, jump and goto semantics precisely. Reject cycles or bound traversal so a ruleset cannot create unbounded recursion.

Counters and logs are expressions with side effects, not verdicts. Their position matters. A counter before a later drop counts attempted traffic; a counter after an earlier terminal verdict never runs.

### Use sets and maps without changing meaning

Sets replace many repetitive equality rules with one lookup. Interval sets represent ranges; concatenated keys represent tuples; maps return data or verdicts. Validate key width, family, byte order, interval normalization, timeout and element type.

Dynamic elements, per-key counters and meters create state. Bound cardinality and memory before insertion. Expiry and garbage collection must retire timer, key, counter and references exactly once.

### Publish rulesets transactionally

Parse and type-check the whole candidate transaction, resolve chain and set references, detect cycles, validate hook priorities and resource quotas, compile representations, then publish one generation. Readers see either old or new roots under RCU or an equivalent lifetime protocol.

If any operation fails, publish none of the candidate. Deleting an object referenced within the same transaction is legal only if the final graph is valid. Keep old generation data alive until software readers, queued verdicts and offload instances quiesce.

### Keep namespaces and tenants in every key

Rulesets, connection state, sets, quotas, logs and user queues belong to an explicit namespace or other policy domain. A numeric table or zone identifier is not globally unique. Kernel objects cannot retain a raw namespace or device pointer beyond its lifetime.

Administrative authorization distinguishes who can modify policy from who sends packets through it. Delegating one namespace must not permit attaching hooks to another namespace's device or consuming unbounded host-wide state.

### Define connection tracking narrowly

Connection tracking maps an original and reply tuple plus zone and protocol-specific state to a bounded record. It can label packets new, established, related, invalid, or untracked under framework semantics. That label describes tracking history, not user authentication or guaranteed endpoint existence.

Validate transport state transitions enough to resist trivial spoofing, but do not claim equivalence to the endpoint TCP implementation. UDP tracking commonly uses observed request/reply and timeouts rather than a transport connection. ICMP errors can be related by safely parsing their quoted packet.

### Bound state and timers before creation

Charge each tracking entry, extension, helper, expectation, NAT mapping, timer and counter to zone, namespace, tenant and host before publication. Limit total entries, per-source creation, helper expectations, unresolved fragments and teardown work.

Under pressure, reject new state or use an explicitly safe stateless path; do not evict active records arbitrarily if that converts established traffic into an unintended new-policy path. Reserve resources for expiry, deletion and administrative recovery.

### Treat helpers as parsers with authority

Some protocols negotiate secondary flows in payload. A helper may parse control traffic and create bounded expectations. It consumes hostile application bytes and can widen future policy, so enable it explicitly, scope it to ports and zones, and bound depth, length, expectations and lifetime.

Encrypted payloads and evolving protocols limit helper visibility. Do not infer authorization from a heuristic parser. Prefer application-aware gateways when semantic identity is required.

### Make NAT a reversible state transition

NAT chooses a mapping for an eligible flow and records original and reply directions. Rewrite addresses or ports at defined hooks, update network and transport checksums, invalidate route and flow hashes where required, and handle ICMP quotations and fragments consistently.

Mapping allocation is bounded shared state. Port exhaustion, collision, endpoint dependence, hairpinning and timeout are explicit outcomes. NAT is not a firewall: address translation alone does not define an allow policy.

### Handle fragments and extension headers explicitly

Noninitial IP fragments may lack transport ports. Decide whether policy runs before reassembly, after reassembly, or both, and prevent fragments from taking a weaker path. IPv6 first fragments must contain the entire header chain under current requirements, but implementations still validate and bound it.

Connection tracking can associate later fragments only through a protected fragment subsystem. Overlap, timeout and memory rules from protocol processing still apply. Never invent zero ports for absent headers and let them match ordinary rules.

### Preserve essential control traffic

ICMP and ICMPv6 include diagnostics and protocol machinery. IPv6 Neighbor Discovery and Packet Too Big behavior are essential to connectivity. Filter by validated type, code, scope, direction, quoted packet relationship and rate rather than dropping the entire protocol.

Reject responses themselves consume bandwidth and can reveal policy or amplify traffic. Generate them only where permitted, initialize bounded quotations, rate-limit, and attribute response failure separately from the original verdict.

### Apply source validation at the right boundary

Ingress filtering checks whether a source is plausible for the interface and policy domain. Strict reverse-path tests work in symmetric simple networks; loose or feasible-path modes better tolerate multihoming and asymmetric routing. Choose based on topology rather than habit.

Egress filters prevent internal sources from emitting addresses they do not own. Tunnel endpoints apply policy to outer and inner source domains at the corresponding boundaries.

### Protect asynchronous userspace verdicts

Queueing a packet for userspace defers ownership and pins context. Bound queued packets, bytes, time and per-client outstanding work before insertion. Authenticate the verdict source and include ruleset, namespace and continuation generations.

On timeout, process death, ruleset replacement, device removal or namespace teardown, apply the configured fail behavior and release once. A late verdict for an obsolete generation cannot be applied to current policy.

### Offload only what can be proved equivalent

Hardware may offload eligible matches and actions with different parser depth, table size, priorities, counters and update mechanics. Compile only a declared subset. Reject or retain software processing when semantics cannot be preserved.

Program replacement transactionally across software and hardware. Define whether software is authoritative during transition, how packets in flight are handled, and how counters combine without double counting. Device reset or rule eviction must fail to the chosen safe policy, not silently bypass.

### Make verified programs policy components

BPF verification can establish bounded control flow, permitted memory and helper access, and packet bounds along accepted paths. Attachment type defines hook and context. Maps provide shared state with their own lifetime, size and synchronization.

Verification does not establish that allow rules implement intent, that IPv4 and IPv6 are symmetric, that helpers are secure, or that two attachment points do not conflict. Review semantics and generation rollout separately.

### Bound observability

Every rule and terminal policy should expose packet and byte counters, but counters need generation, hook, chain and direction context. Rate-limit logs and cap captured bytes. Redact addresses, ports, identifiers or payload according to policy.

Tracing can record hook, generation, rule handle, set result, tracking state, NAT tuple view and verdict for sampled flows. Do not enable full per-packet tracing on hostile line-rate traffic without an independent budget.

### Test semantic matrices and replacement races

Generate both IP families, every hook direction, fragments, extension headers, tunnels, multicast, required ICMP, original and reply flows, invalid states, NAT collisions, helper limits, set expiry and default fallthrough. Compare behavior with a simple reference policy.

Race evaluation with transaction commit, set replacement, tracker expiry, userspace verdict, offload reset, device detach and namespace destruction. Assert one generation per evaluation, no bypass window, bounded memory, exact ownership, consistent software/offload verdicts and eventual reclamation.

## Definitions and Notation

Let hook context be $h=(f,k,d,r,n)$ for address family, hook kind, direction, routing stage and namespace. Let packet view $P_h$ contain only fields validated and meaningful at $h$.

A rule is $r_i=(m_i,a_i)$ with predicate $m_i(P_h,C,S)\in\{0,1\}$ and action $a_i$. For a first-terminal chain, evaluation selects the least index whose match is true and action terminates; otherwise it returns chain policy $\pi$.

Let ruleset generation graph be $G=(T,C,R,S,O,E)$. Publication requires all references in edge set $E$ resolve, all control-flow cycles are rejected or statically bounded, all object types agree, and total charged memory is within quota.

For tracked flow key

$$
K=(n,z,f,p,s_a,s_p,d_a,d_p),
$$

include namespace $n$, zone $z$, family $f$, protocol $p$, addresses and ports. Reply direction uses an explicit inverse or translated tuple, never an unordered comparison.

Let dynamic state counts and bytes satisfy

$$
N_{ct}\le C_{ct},\quad N_{set}\le C_{set},\quad N_{queue}\le C_q,\quad A_{total}\le B_n,
$$

with lower per-tenant and per-source bounds where policy requires isolation.

Let software verdict $V_s$ and offloaded verdict $V_h$ be equivalent for eligible domain $D$ only when

$$
\forall x\in D:\ V_s(x,G)=V_h(x,G)
$$

under the same packet view and generation. Testing samples this property; it does not prove the universal claim.

## Mechanisms, Invariants, or Proof Structure

Review filtering with these obligations.

1. **Objective obligation:** rules trace to an explicit principal, boundary, allowed behavior and failure policy.
2. **Hook obligation:** each match consumes only packet and context fields valid at the selected attachment point.
3. **Parser obligation:** bounds, fragments, extensions, tunnels and transformations preserve or invalidate field proofs correctly.
4. **Control-flow obligation:** priorities, chains, jumps, returns, defaults and terminal verdicts are deterministic and bounded.
5. **Transaction obligation:** the complete object graph validates before one atomic generation publishes.
6. **Isolation obligation:** rules, sets, state, queues, counters and administration are scoped to the correct namespace and tenant.
7. **State obligation:** tracking direction, protocol state, timer, helper, expectation and NAT mapping are validated and precharged.
8. **Transformation obligation:** NAT or redirect updates bytes, checksums, routes, hashes, metadata and reverse semantics together.
9. **Control-traffic obligation:** essential ICMP and discovery remain functional under precise validation and rate limits.
10. **Deferral obligation:** queued packets retain bounded ownership and apply only an authenticated current-generation continuation.
11. **Offload obligation:** eligible semantics, counters, transition authority, device failure and fallback are explicit.
12. **Evidence obligation:** each verdict is attributable under bounded privacy-aware counters, logs and traces.

The safety argument composes parsing, policy, state and lifetime. Parsing proves a hook-specific view. One immutable generation deterministically maps that view and protected state to a verdict. State mutation charges and publishes atomically. Lifetime keeps packet, namespace, ruleset and optional tracker alive through completion. A valid implementation satisfying all four layers cannot read unproved fields, mix generations, cross policy domains, or lose packet ownership.

This is not a proof that a ruleset expresses organizational intent. That requires threat modeling, policy review, reachability tests, dual-stack analysis, change review, attack simulation and independent operational evidence.

## Alternatives and Trade-Offs

- **Early hooks versus rich context:** early drop saves work; later hooks know routes, sockets, reassembly and tracking state.
- **Stateless versus stateful filtering:** stateless policy is bounded and transparent; stateful policy expresses replies and relationships at memory and timer cost.
- **Ordered rules versus sets and maps:** lists are readable for small policy; indexed objects scale but hide precedence unless designed carefully.
- **Default deny versus default allow:** deny limits unknown exposure; allow can preserve connectivity during incomplete migrations and widens risk.
- **In-place edits versus immutable transactions:** edits reduce replacement allocation; generations eliminate partial-reader states.
- **Pre-reassembly versus post-reassembly policy:** early filtering bounds fragment cost; final semantics may require complete headers.
- **Strict reverse-path filtering versus feasible-path validation:** strict mode blocks more spoofing; asymmetric routing can make it reject legitimate traffic.
- **Reject versus silent drop:** rejection improves diagnosis; silence reduces information and response amplification.
- **Kernel-only verdict versus userspace queue:** kernel evaluation is bounded and fast; userspace enables richer policy while pinning packets and context.
- **Generic tracking versus protocol helpers:** generic tuples reduce parser risk; helpers express related flows and expand authority.
- **NAT-integrated policy versus separate translation:** integration sees mapping state; separation makes authorization independent of address rewriting.
- **Software evaluation versus hardware offload:** software supports full semantics; hardware reduces CPU with capability and counter differences.
- **Per-rule counters versus aggregated telemetry:** per-rule evidence is precise; high cardinality raises memory and read cost.
- **Full logs versus sampled events:** full logs seem complete and enable DoS; bounded samples preserve system availability.
- **One dual-stack policy versus separate families:** unified intent reduces drift; protocol-specific control messages still require distinct rules.
- **Automatic rollback versus manual containment:** automation closes exposure quickly; a misleading metric can remove legitimate access.

## Failure Modes and Misconceptions

- “All filter hooks see the same packet.” Representation and metadata change across the path.
- “A port rule is safe on every fragment.” Noninitial fragments may not contain transport headers.
- “The verifier understands firewall intent.” It checks defined program properties, not organizational policy.
- “Accept means delivered.” It means continue from one policy point.
- “Drop and reject are identical.” Reject generates a controlled response and different external behavior.
- “Connection tracking is TCP state.” It is a separate middlebox-oriented approximation and resource.
- “Tracked established means authenticated.” It says nothing about application identity.
- “UDP cannot be tracked.” Frameworks can retain tuple observations and timeouts without a transport handshake.
- “NAT is a security policy.” Translation does not define authorization.
- “The same tuple applies before and after NAT.” Original, translated and reply directions differ.
- “Rule order is only an optimization.” First-match and side effects make order semantic.
- “A set update cannot affect ruleset coherence.” Rules may depend on set membership in the same generation contract.
- “Atomic syntax upload guarantees valid references.” The kernel must validate the final graph before publication.
- “RCU means old rules can be freed immediately.” Existing readers and queued continuations retain them.
- “One connection limit bounds state.” Sets, timers, expectations, fragments, queues and logs also allocate.
- “Dropping all ICMP improves security.” It can break diagnosis and path MTU behavior.
- “IPv4 rules automatically protect IPv6.” Families and required control protocols differ.
- “Extension headers are always malicious.” Policy must distinguish supported uses from prohibited forms.
- “Reverse-path strict mode fits every network.” Multihoming and asymmetry can require feasible-path logic.
- “Userspace verdicts can arrive whenever.” Generation, namespace, device and timeout determine validity.
- “Offloaded traffic still hits software counters.” Counter ownership depends on the offload contract.
- “Hardware rejection of a rule means software will cover it.” Fallback must be explicitly installed and ordered.
- “Logging every drop improves evidence.” It lets hostile traffic consume CPU, storage and sensitive data.
- “A ruleset dump explains a historical verdict.” Generation and dynamic-state snapshots are also needed.
- “A passing connectivity test proves default-deny completeness.” It samples a few intended paths, not all unintended ones.

## Worked Examples

### Example 1

An ingress XDP filter can reject a source prefix before SKB allocation. It cannot match a later socket identity or assume fragments have been reassembled. A local-input filter can use richer context at higher cost.

### Example 2

The following executable model shows first-match order and default policy. Its `state` field is trusted input to the toy; it models no parser, tracker, namespace, kernel, rule transaction, NAT, or packets.

<!-- bijux-verify: {"id":"ordered-filter-verdicts","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"packet=1 rule=established verdict=accept\npacket=2 rule=blocked_source verdict=drop\npacket=3 rule=default verdict=drop\naccept=1 drop=2\n","stderr":""}} -->
```python
packets = [
    {"state": "established", "source": "203.0.113.8", "port": 22},
    {"state": "new", "source": "198.51.100.7", "port": 443},
    {"state": "new", "source": "192.0.2.9", "port": 53},
]
blocked = {"198.51.100.7"}
counts = {"accept": 0, "drop": 0}

for number, packet in enumerate(packets, 1):
    if packet["state"] == "established":
        rule, verdict = "established", "accept"
    elif packet["source"] in blocked:
        rule, verdict = "blocked_source", "drop"
    elif packet["port"] == 443:
        rule, verdict = "https", "accept"
    else:
        rule, verdict = "default", "drop"
    counts[verdict] += 1
    print(f"packet={number} rule={rule} verdict={verdict}")

print(f"accept={counts['accept']} drop={counts['drop']}")
```

### Example 3

A noninitial IPv4 fragment lacks TCP ports. The pre-reassembly hook applies fragment policy but does not substitute zero and match a generic non-HTTPS drop. Post-reassembly policy evaluates the complete transport header.

### Example 4

A ruleset transaction adds a chain that references a new set and deletes the old chain and set. Allocation of one new set element fails. The whole candidate aborts; readers continue using the complete old generation.

### Example 5

A tracked TCP packet matches the reply tuple but has an impossible reset sequence. Tracking can label direction, while transport validation or stricter firewall state still rejects the control effect. `ESTABLISHED` is not blind trust.

### Example 6

Source NAT allocates a public port, rewrites the packet, updates checksums, invalidates the old route, and records the inverse reply mapping. If port allocation fails, the packet drops with NAT-exhaustion attribution, not generic policy denial.

### Example 7

An IPv6 policy permits echo selectively but also permits validated Packet Too Big and required local Neighbor Discovery types. A blanket ICMPv6 drop would make some paths stall and local address resolution fail.

### Example 8

A userspace inspection queue reaches its byte bound. New packets take the configured fail-closed verdict immediately. A verdict arriving after ruleset replacement carries the old generation and is discarded without reinjection.

### Example 9

A NIC offloads four allow rules but cannot offload a stateful rate limit. Software remains authoritative for that chain, and counters identify which packets bypassed software. Device reset installs the safe fallback before offload state disappears.

### Example 10

An incident shows application timeouts but firewall accept counters are high. Later-hook traces show accepted packets, route counters are normal, and socket receive queues overflow. Filter acceptance did not establish endpoint admission; the bottleneck lies later.

## Cross-Program Connections

- **Security engineering:** threat models, default policy, spoofing, state exhaustion, least privilege and audit define filtering intent.
- **Network engineering:** hooks, fragments, ICMP, tunnels, NAT, routes, multicast and dual-stack behavior define packet semantics.
- **Data structures engineering:** immutable graphs, tries, hash sets, interval maps, counters, timers and RCU implement rulesets.
- **Formal methods:** typed expressions, control-flow termination, generation consistency and refinement connect rules to proofs.
- **Performance engineering:** early drop, cache locality, set lookup, per-CPU counters, batching, logging and offload determine cost.
- **Platform engineering:** namespaces, cgroups, network policy, runtime programs, device offload and rollout operationalize enforcement.
- **API and service engineering:** connection direction, load balancers, service ports, health checks and retries define allowed flows.
- **Distributed systems:** replicated policy, versioning, delayed verdicts, convergence and partial failure recur in ruleset deployment.
- **Privacy engineering:** packet logs, addresses, ports, payload capture, retention and access control constrain observability.
- **Reliability engineering:** transactional replacement, fallback, management access, resource reserves and rollback prevent lockout.

## References

1. Linux Kernel Documentation, [nftables Netlink Specification](https://docs.kernel.org/netlink/specs/nftables.html), tables, chains, rules, sets, expressions, hooks, state objects, NAT, counters and transactions; retrieved 2026-09-04.
2. Netfilter Project, [`nft` Manual](https://netfilter.org/projects/nftables/manpage.html), current nftables ruleset syntax, evaluation, stateful objects, transactions, tracing and operations; retrieved 2026-09-04.
3. Linux Kernel Documentation, [eBPF Verifier](https://docs.kernel.org/bpf/verifier.html), bounded control flow, pointer tracking and direct packet-access proofs; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Linux Socket Filtering](https://docs.kernel.org/networking/filter.html), classic and extended BPF attachment, socket-filter behavior and kernel checking; retrieved 2026-09-04.
5. IETF, [RFC 3704: Ingress Filtering for Multihomed Networks](https://www.rfc-editor.org/rfc/rfc3704.html), strict, loose and feasible-path source validation; retrieved 2026-09-04.
6. IETF, [RFC 4890: Recommendations for Filtering ICMPv6 Messages](https://www.rfc-editor.org/rfc/rfc4890.html), required control traffic, security balance, message classes and stateful correlation; retrieved 2026-09-04.
7. IETF, [RFC 6092: Recommended Simple Security Capabilities in Customer Premises Equipment for Providing Residential IPv6 Internet Service](https://www.rfc-editor.org/rfc/rfc6092.html), stateful filtering, inbound defaults and IPv6 control traffic; retrieved 2026-09-04.
8. IETF, [RFC 7112: Implications of Oversized IPv6 Header Chains](https://www.rfc-editor.org/rfc/rfc7112.html), first-fragment header-chain requirements and filtering implications; retrieved 2026-09-04.
9. IETF, [RFC 9099: Operational Security Considerations for IPv6 Networks](https://www.rfc-editor.org/rfc/rfc9099.html), dual-stack policy, extension headers, ingress filtering, ICMPv6 and monitoring; retrieved 2026-09-04.
10. IETF, [RFC 2979: Behavior of and Requirements for Internet Firewalls](https://www.rfc-editor.org/rfc/rfc2979.html), transparency, application behavior, path MTU and firewall requirements; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design a dual-stack host policy across early ingress, local input and local output hooks. Permit a public HTTPS service, established replies, management from one subnet and required control traffic; state packet-view and default semantics.

### Exercise 2

Design an atomic ruleset transaction system with chains, interval sets, verdict maps, counters, dynamic timeouts and RCU readers. Cover validation, failure, generations and reclamation.

### Exercise 3

Trace a TCP flow through connection tracking and source NAT in original and reply directions, including retransmission, fragments, ICMP error quotation, mapping expiry and port exhaustion.

### Exercise 4

Defend the filtering subsystem against unique-flow floods, dynamic-set cardinality, helper expectations, userspace queue saturation, reject amplification and logging denial of service.

### Exercise 5

Construct a semantic validation and observability plan for a ruleset partly offloaded to hardware and partly implemented by verified programs. State evidence limits.

## Answers to the Exercises

### Answer 1

At early ingress, validate only available outer network fields and cheaply drop impossible source ranges under topology-aware source validation. Do not match ports on noninitial fragments or assume reassembly. Attach namespace and ingress device explicitly. Preserve packets needing later header or state evaluation.

At local input after the chosen reassembly and tracking point, accept validated required ICMPv6 and IPv4 control messages by type, code, scope and quoted-flow relationship. Accept established reply-direction traffic under tracking plus protocol-validity policy. Accept new TCP destination 443 to the service addresses. Accept management only from its source prefix, interface and authenticated higher-layer boundary; filtering alone is not authentication. Default drop with bounded counters.

At local output, permit service replies, required control traffic and explicitly authorized initiations. Apply egress source validation. Use one dual-stack intent model but compile protocol-specific ICMP and address rules. Document hook priorities relative to NAT and routing. Transactionally publish all chains and sets, retain an independent recovery channel, and test fragments, tunnels, both families, route change and namespace isolation.

### Answer 2

Represent the candidate as an immutable graph of tables, base and ordinary chains, typed expressions, sets, maps and state objects. Parse all messages into private objects, enforce namespace quota, normalize intervals, validate key and value widths, resolve references, reject dangling edges and cycles, and compute bounded traversal.

Create counters and dynamic timeout state with explicit ownership. A transaction may refer to objects by temporary IDs, but all must resolve in the final graph. Compile optimized lookup structures before publication. If any allocation, type, capability or reference check fails, destroy the candidate and leave the active root unchanged.

Publish one root and generation atomically. Readers hold RCU or equivalent protection for the whole evaluation. Dynamic elements use separately synchronized versioned state only if the contract permits changes within a ruleset generation. Retire old roots after readers, queued continuations and offloads quiesce; cancel timers and release counters once. Preserve a rollback root until the new generation passes health gates.

### Answer 3

The first valid outbound SYN creates or finds a tracker keyed by namespace, zone, family and original tuple. Precharge entry, protocol extension, timer and mapping. Source NAT selects an available external address and port, records original-to-translated and inverse reply tuples, rewrites bytes, updates checksum state, invalidates route and flow metadata as needed, and transmits under the current route.

Retransmissions reuse the mapping and do not create state or consume another port. Later fragments associate through bounded protected fragment state; absent ports are never parsed. A validated ICMP error quotation is matched against the relevant original or translated tuple according to hook view and its inner quotation is rewritten consistently if the implementation supports it.

Reply packets match the inverse translated tuple, enter reply direction, reverse NAT, update checksums and route context, then continue policy. On mapping timeout, stop new acquisition, remove both direction keys, synchronize readers and timers, and release the port once. Port exhaustion rejects new mappings with a specific counter; it does not steal an active mapping or bypass NAT policy.

### Answer 4

Precharge tracker entries, set elements, timers, helper expectations, NAT mappings, queued packets, log buffers and counter objects to source, tenant, namespace and host. Bound new-state rate and total cardinality independently. Use protocol-aware timeouts and prefer expiring failed old unreferenced state under pressure.

Helpers are explicitly enabled and limited by parser bytes, nesting, expected-flow count, lifetime and parent flow. Userspace queues have packet, byte, client and time bounds with authenticated generation-tagged verdicts. Reject responses have per-source, per-type and global token buckets. Logging is sampled or token-bucketed, caps snapshot length, redacts sensitive fields and never blocks packet progress.

Reserve memory and CPU for expiry, transaction rollback, device failure and management. Define fail-open or fail-closed per hook and policy rather than allowing allocation failure to decide implicitly. Monitor allocation rejection, cardinality, timer backlog, queue age, response suppression, log loss and reclaim progress.

### Answer 5

Build a canonical test matrix from policy intent: both IP families, hooks, interfaces, namespaces, sources, destinations, protocols, ports, fragments, extensions, tunnels, connection directions, tracking states, NAT views, required ICMP, set boundaries and defaults. Evaluate it against a simple reference interpreter, software rules, verified program and hardware subset.

Verify program bounds and helper access, then separately review semantic fields and attachment order. Query hardware capabilities and reject unsupported compilation rather than approximating. Race generation replacement, map update, tracker expiry, device reset and namespace teardown. Confirm software authority and safe fallback before old hardware rules disappear.

Record generation, hook, rule handle, set key result, tracking direction and state, tuple view, offload location, verdict and counter source. Reconcile software and hardware counters with known ownership and in-flight transitions. Use sampled traces and packet observations before and after transformations.

Finite matrices cannot prove absence of unintended reachability. Verifier success does not prove policy correctness. Hardware tests cover one firmware and capability set. Packet capture can miss offloaded paths. Counters can lose attribution during defined transitions. Passing tests do not prove resistance to every parser, state-exhaustion or operational error. State those limits and require staged rollout.
