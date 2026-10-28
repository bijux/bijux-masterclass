---
module_id: OS-076
program: Operating Systems
level: 2
module_number: 76
title: Connection State Management
status: complete
last_verified: 2026-09-04
---

# Connection State Management

## One-Page Review

### Governing question

How should an operating system create, locate, evolve, time, expose, close, and reclaim transport connection state while preserving protocol sequence semantics, endpoint identity, resource bounds, concurrent lifetime, reset security, namespace isolation, and truthful application completion?

### Essential definitions

- A **transmission control block (TCB)** is the protocol state for one TCP connection, including tuple, sequence spaces, windows, options, timers, queues, errors, and ownership.
- A **connection tuple** identifies a transport association using namespace, address family, local and remote addresses, local and remote ports, and relevant interface or policy scope.
- A **request socket** or embryonic entry represents a passive handshake that has not yet become an accepted full endpoint.
- The **SYN backlog** holds incomplete passive opens; the **accept queue** holds completed connections awaiting application acceptance.
- A **sequence space** orders bytes and control flags modulo $2^{32}$; SYN and FIN each consume one sequence number.
- **SND.UNA** is the oldest unacknowledged send sequence, **SND.NXT** the next sequence to send, and **RCV.NXT** the next sequence expected.
- A **retransmission timer** drives recovery when acknowledgment does not arrive; it is distinct from delayed ACK, persist, keepalive, FIN-WAIT, and TIME-WAIT timers.
- **Half-close** means one direction has ended with FIN while the other direction can still carry data.
- **TIME-WAIT** retains enough state after active close to acknowledge a retransmitted FIN and protect a later incarnation from old segments.
- A **challenge ACK** is a guarded response used by modern TCP hardening for certain suspicious in-window reset or SYN conditions.

### Central model, mechanism, or theorem

Represent one connection as

$$
C=(K,Z,S,R,W,O,T,Q,E,A,L,G),
$$

where $K$ is the scoped tuple, $Z$ the protocol state, $S$ and $R$ the send and receive sequence spaces, $W$ negotiated windows and options, $O$ current ownership, $T$ timers, $Q$ packet and application queues, $E$ error state, $A$ hierarchical accounting, $L$ protected object lifetime, and $G$ generations for table membership and asynchronous work.

Every event—application call, incoming segment, timer expiry, memory pressure, policy change, or teardown—passes a guard based on the current state and validated sequence space. The transition publishes new state atomically with its queue, timer, wakeup, and ownership effects. A tuple match is not sufficient: the segment must belong to this incarnation and be acceptable for this state.

### Critical invariants

- Connection lookup includes namespace and full binding semantics, and its result remains lifetime-protected through use.
- Initial sequence numbers are hard to predict and tied to connection identity while still meeting protocol progression requirements.
- Segment sequence, acknowledgment, window, flags and option extent are validated before changing state or freeing acknowledged data.
- Passive-handshake state, completed-but-unaccepted state, and accepted endpoints have separate bounded accounting.
- No handshake completion enters the accept queue unless a live listener still authorizes and can account for it.
- Each timer carries a protected connection reference or validated generation; cancellation and callback cannot both retire it.
- FIN closes one byte stream direction, not necessarily the whole connection; unread data and pending output retain explicit semantics.
- RST is validated for the current state and sequence window before aborting a synchronized connection.
- TIME-WAIT tuple reuse never lets delayed segments from an old incarnation corrupt a new one.
- Final reclamation occurs only after hash membership, queues, timers, callbacks, users, protocol work, and deferred readers release ownership.

### Common failures

Common failures are using only a four-tuple across namespaces, treating a hash hit as a live connection, allocating full sockets for every SYN, conflating SYN backlog with accept queue, completing a handshake after listener close, using predictable initial sequence numbers, comparing wrapped sequence numbers as ordinary unsigned integers, freeing send data from an unacceptable ACK, treating FIN as reset, reporting `close()` as peer receipt, accepting any in-window RST without modern hardening, expiring TIME-WAIT merely to reduce counters, arming duplicate timers, racing callback with destruction, retaining unbounded out-of-order data, and hiding listener overload behind generic connection failure.

### Compact example

An active opener moves `CLOSED → SYN-SENT → ESTABLISHED → FIN-WAIT-1 → FIN-WAIT-2 → TIME-WAIT → CLOSED`. Each arrow needs more than the named event: the SYN-ACK must acknowledge the transmitted SYN and have an acceptable sequence; the ACK must cover the local FIN; the remote FIN is acknowledged; TIME-WAIT lasts for its specified protection interval and restarts for a retransmitted FIN where required. Application close does not mean peer receipt, and the object cannot be freed while timers or table readers retain it.

### Connections

[OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-071](071-socket-layer-architecture.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), and [OS-075](075-routing-and-neighbor-tables.md) connect connection state to lookup, buffers, timers, routes, queues, concurrency, and memory pressure.

## Governing Question

A protocol state diagram shows legal abstract states, but a kernel must also manage objects. One logical connection can appear as a listener, incomplete request, established hash entry, accept-queue item, file-owned socket, orphan, retransmission owner, TIME-WAIT object, and deferred callback target during its lifetime. These representations overlap under concurrency.

The governing question is how to make every external event act on the correct connection incarnation and leave all representations coherent. Packets may be duplicated, delayed, reordered or forged. Applications can close concurrently with receive processing. Timers can expire as acknowledgments arrive. Namespaces and devices can disappear. Correctness depends on guarded transitions and explicit lifetime, not on state labels alone.

## Why This Matters

Connection tables are exposed to untrusted network traffic. A SYN flood tries to turn cheap packets into expensive state. An off-path attacker tries to predict sequence space or inject a reset. An established peer can create out-of-order memory, tiny-window work, or slow application queues. Every allocation and response must be bounded.

Connection state also defines application-visible behavior. Successful `connect()` means a transport association reached the local established condition, not that application data was accepted. A successful buffered send means the kernel accepted bytes, not that the peer application consumed them. Graceful close, abort, timeout, refusal and unreachable errors must remain distinguishable.

At scale, tuple hashes, listener selection, per-CPU processing, timers, retransmission queues, accept queues and TIME-WAIT objects dominate memory and cache behavior. Tuning one limit without understanding the entire admission chain simply moves overload to another queue.

## Prerequisites and Retrieval

Review [OS-007](007-kernel-data-structures.md), [OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), and [OS-075](075-routing-and-neighbor-tables.md).

Retrieve these distinctions:

- listening socket, handshake request, completed child, accepted file descriptor, orphan and TIME-WAIT object are different representations;
- SYN backlog, accept queue, receive queue, out-of-order queue, send queue and retransmission queue have different admission rules;
- local system-call completion, protocol acknowledgment, peer delivery and peer application consumption are different completion levels;
- tuple match, incarnation match, sequence acceptability, acknowledgment acceptability and application authorization are different checks;
- receive window, congestion window, advertised window, send buffer and bytes in flight are related but not synonymous;
- FIN, RST, timeout, local abort, process exit and namespace teardown have different peer and application semantics;
- retransmission, delayed ACK, persist, keepalive, FIN-WAIT and TIME-WAIT timers protect different invariants;
- RCU visibility, reference ownership, socket lock, callback generation and user file ownership cover different lifetime intervals;
- syncookies, backlog growth, admission control and load shedding solve different overload conditions;
- connection count, socket memory, packet truesize, pinned pages, timers and queued application data require separate accounting.

## Learning Objectives

After this module, you should be able to:

1. trace active and passive TCP open through lookup, sequence initialization, request state, established publication, accept admission and application notification;
2. validate sequence numbers, ACKs, windows, SYN, FIN, RST and options before changing a connection;
3. design connection hashes, listener selection, queues, timers and lifetime protocols for concurrent packet and application events;
4. preserve half-close, error, retransmission, TIME-WAIT and completion semantics through shutdown and teardown;
5. bound handshake, established, out-of-order, retransmission, accept, orphan and TIME-WAIT resources hierarchically;
6. reason about SYN floods, syncookies, reset attacks, tuple reuse, listener close, timer races and namespace destruction;
7. diagnose connection failures with state transitions, queue occupancy, timer events, sequence evidence, drops and application-visible errors.

## Core Exposition

### Key state by full connection context

Transport lookup begins only after network and transport headers are validated. A TCP established key includes network namespace, address family, local and remote addresses, local and remote ports, and any interface or binding scope required by the implementation. A listener key is less specific and follows wildcard, bound-device, reuse-group and policy precedence.

Hashing accelerates lookup but does not define semantics. The slow reference algorithm and fast tables must choose the same listener or connection. Protect a result with RCU plus the socket-specific reference or lock required to survive concurrent close; a bucket match alone is not a lifetime grant.

### Distinguish connection incarnations

The same tuple can be reused after close. Sequence numbers, timestamps where negotiated, TIME-WAIT rules and protocol quiet-time assumptions prevent old duplicate segments from entering a new byte stream. Store enough incarnation state to validate every control segment.

Initial sequence numbers must progress as TCP requires and resist prediction using connection-specific secret input. Random-looking output without uniqueness or time evolution can still collide; monotonic output without a secret enables spoofing.

### Process active open transactionally

An active open chooses and reserves a local endpoint, obtains a route, initializes the TCB and sequence state, queues a SYN for transmission, arms retransmission, and publishes lookup state. Order publication so an immediate reply can find a fully initialized object.

If routing, port selection, allocation or publication fails, release each resource once and return a precise error. If the application cancels while the SYN is in flight, timer and receive paths must observe the closing generation and cannot establish a now-unowned connection.

### Split passive open into admission stages

A listener receiving a valid SYN first decides whether it can admit handshake work. A compact request object can retain tuple, initial sequence values, negotiated options, retransmission state, route or reply context, timer and listener relationship without allocating a full accepted socket.

The SYN backlog bounds incomplete requests. After a valid final ACK, create or promote a child, publish it in the established table, admit it to the accept queue, and wake the listener. These actions are transactional: if the listener closed or the accept queue cannot admit, do not leave a reachable unowned child.

### Treat syncookies as a constrained fallback

SYN cookies encode enough handshake state into the server's initial sequence number to validate a later ACK without retaining ordinary request state. They reduce memory amplification under SYN backlog pressure but constrain how much negotiated state can be recovered and consume CPU and response bandwidth.

They are not a substitute for capacity planning under legitimate connection load. Apply rate limits, authentication or upstream mitigation as appropriate, and monitor when the fallback activates, which options change, and whether the accept queue—not the SYN backlog—is the real bottleneck.

### Validate segment acceptability before state mutation

After lookup, validate checksum and header, then apply state-specific sequence tests in modular arithmetic. An empty segment and a data-bearing segment have different acceptable-window conditions. ACK validation ensures acknowledgments do not cover unsent sequence space before advancing SND.UNA or releasing retransmission data.

Process RST, SYN, ACK, data and FIN in the required order for the state. Do not update window, timers or queues from a segment that an earlier check rejects. Challenge responses themselves require rate limiting so hardening cannot become amplification.

### Compare wrapped sequence numbers correctly

TCP sequence space wraps at $2^{32}$. Implement comparisons with a defined modular ordering valid within the protocol's bounded window, not ordinary integer `<`. Ambiguity is avoided because valid windows and in-flight ranges remain smaller than half the sequence space.

SYN and FIN each occupy sequence space even without payload. Segment logical length is payload plus those control contributions. Forgetting them causes off-by-one ACK, retransmission and close transitions.

### Maintain send state as acknowledged ownership

The send queue contains application bytes accepted by the kernel; the retransmission structure retains transmitted bytes until cumulatively or selectively acknowledged under valid rules. Track SND.UNA, SND.NXT, maximum sent, advertised peer window, congestion state, timestamps and retransmission metadata coherently.

An ACK can release only covered data that was actually sent. Duplicate or stale ACKs may drive recovery algorithms but cannot free arbitrary buffers. Zero-copy application pages remain immutable and owned until the kernel's defined completion notification, which may outlast protocol acknowledgment processing.

### Maintain receive state and reassembly bounds

RCV.NXT identifies the next byte for contiguous receive. In-order bytes advance it and can enable application delivery. Out-of-order segments occupy an interval structure until gaps close. Duplicate and overlapping bytes follow TCP's data-consistency policy without being double charged or delivered.

Bound out-of-order objects and bytes by socket, cgroup, namespace and host. Memory pressure may collapse or drop queued ranges and rely on retransmission. Advertised receive window reflects admissible capacity, not simply free bytes at one instant.

### Keep flow control separate from congestion control

The peer's advertised window limits how far the sender may advance for receiver capacity. The congestion window limits network injection. Effective send opportunity is constrained by both plus bytes already in flight and local pacing or policy.

Window updates are validated against sequence and acknowledgment context so reordered old segments cannot shrink or expand current state incorrectly. Zero-window persist prevents deadlock through bounded probes without interpreting lack of window as ordinary congestion loss. OS-077 develops congestion-control hooks.

### Give every timer one invariant

The retransmission timer detects missing acknowledgment and computes bounded backoff. Delayed ACK timer bounds acknowledgment latency. Persist probes a zero window. Keepalive optionally tests long-idle connections under configured semantics. Handshake timers expire embryonic state. FIN-WAIT and orphan timers bound abandoned resources. TIME-WAIT protects old sequence space.

Represent each armed timer with deadline, purpose, generation and protected owner. Arm, replace and cancel under one state protocol. A callback validates generation after acquiring its reference; cancellation waits or arranges that exactly one path releases timer ownership.

### Handle half-close explicitly

Receiving FIN advances RCV.NXT and marks end-of-stream after preceding bytes. The local application can still send in CLOSE-WAIT until it closes its direction. Sending FIN does not discard pending receive data. Simultaneous close passes through CLOSING when both FINs cross before acknowledgment.

Expose EOF only after all preceding accepted bytes. Local `shutdown()` controls one or both directions according to API contract. Abortive close and unread-data policies can produce RST instead of a graceful FIN path; make that choice visible.

### Preserve TIME-WAIT safety

The active closer commonly enters TIME-WAIT after both directions finish. It acknowledges a retransmitted final FIN and prevents delayed segments from a previous incarnation contaminating a new one. Timer restart and tuple reuse follow protocol and negotiated timestamp constraints.

TIME-WAIT objects can be compact, but prematurely destroying them changes correctness, not merely memory use. Bound total state with capacity planning and safe reuse rules; do not “fix” a high count by weakening sequence protection.

### Harden reset and synchronized-state handling

A RST must pass state-specific sequence validation before aborting a connection. Modern challenge-ACK behavior strengthens handling of certain in-window reset and SYN attacks. Rate-limit challenges globally and per context without making legitimate recovery impossible.

Do not reveal more connection existence or sequence information than the protocol requires. Authenticate stronger environments with appropriate protocol mechanisms rather than assuming tuple secrecy.

### Publish state and wakeups coherently

Connection state, queue insertion, error visibility and waiter notification form one synchronization contract. Publish data or terminal state before wakeup; waiters test the predicate under the matching lock or memory-order rule. A wake without visible state can be lost.

Exclusive ownership by a socket lock simplifies transitions but can create contention. Per-CPU processing and lockless reads improve locality only when cross-CPU enqueue, application syscalls, timers and teardown have explicit ordering.

### Account every representation

Charge request objects, full sockets, packet truesize, out-of-order ranges, retransmission buffers, accept-queue membership, timers, route references, zero-copy pins and ancillary data. Enforce listener, user, cgroup, namespace, protocol and host limits before allocation or insertion.

Count both objects and bytes. Tiny packets can retain large allocations; one established socket can retain megabytes. Reserve limited resources for ACK, RST, close, error reporting and reclamation so pressure does not prevent release.

### Make teardown a state transition

Process exit, socket close, listener close, namespace destruction and protocol shutdown begin by blocking new ownership. Unhash or mark unavailable, cancel new timer arming, wake users with defined results, drain packet and application queues, synchronize callbacks and RCU readers, release routes and pages, then reclaim.

Listener teardown also handles pending requests and completed children. A child already accepted belongs to its own file; a child merely queued for accept still depends on listener ownership under the kernel contract. Late final ACKs must not resurrect a closed listener generation.

### Observe the whole admission chain

Record active-open attempts and failures, SYN admissions, cookie activation, request retransmissions, handshake expiry, established promotions, accept-queue occupancy and overflow, lookup misses, invalid sequences and ACKs, challenge ACKs, RST outcomes, out-of-order memory, retransmissions, timer firings, closes, orphans and TIME-WAIT retirement.

Correlate state transitions with tuple, namespace, listener, CPU and generation while controlling sensitive data and cardinality. A packet trace alone cannot see application accept delay or internal queue pressure; socket dumps alone can miss rejected segments and destroyed requests.

### Test events and races, not just states

Generate active, passive and simultaneous opens; duplicate SYNs; lost SYN-ACKs; reordered final ACKs; ACKs beyond sent data; zero windows; wrap-adjacent sequence numbers; out-of-order ranges; duplicate FINs; simultaneous closes; valid and invalid RSTs; and tuple reuse with delayed old segments.

Race receive with close, final ACK with listener destruction, ACK with retransmission timeout, FIN with application send, timer migration with CPU hotplug, and namespace teardown with every callback. Inject allocation and queue failures. Assert one state transition, one queue ownership, bounded memory, no stale lookup, no double timer release and eventual reclamation.

## Definitions and Notation

Let TCP sequence values lie in $\mathbb{Z}_{2^{32}}$. Define “before” for differences within half the space:

$$
a \prec b \iff 0 < (b-a)\bmod 2^{32} < 2^{31}.
$$

Use this relation only where protocol bounds exclude ambiguous half-space distances.

For segment starting at `SEG.SEQ` with payload length $d$, flags $s,f\in\{0,1\}$ for SYN and FIN, define sequence length

$$
L=d+s+f.
$$

An ACK can advance acknowledged state only if

$$
\mathrm{SND.UNA}\preceq \mathrm{SEG.ACK}\preceq \mathrm{SND.NXT}.
$$

Let receive window begin at $r=\mathrm{RCV.NXT}$ with width $w$. A nonempty segment is acceptable only if at least one occupied sequence position intersects the current window under the protocol's modular rule. Empty segments use the specified boundary rule.

Let listener capacities be incomplete requests $B_s$, completed children $B_a$, and accounted bytes $M_l$:

$$
0\le N_{syn}\le B_s,\qquad 0\le N_{accept}\le B_a,\qquad 0\le A_l\le M_l.
$$

Let lifetime ownership be reference sum

$$
R=R_{hash}+R_{file}+R_{timer}+R_{queue}+R_{worker}+R_{protocol}.
$$

Reclamation requires $R=0$ after new acquisition is impossible and the required grace periods complete.

For timer $t=(p,d,g)$ with purpose $p$, deadline $d$, and generation $g$, a callback may transition $C$ only when $g=g_C$ and the purpose remains armed.

## Mechanisms, Invariants, or Proof Structure

Review connection management through these obligations.

1. **Identity obligation:** lookup keys include namespace, tuple, binding scope and enough incarnation evidence to reject old traffic.
2. **Lookup-lifetime obligation:** listener, request, established and TIME-WAIT results remain protected through every dereference.
3. **Admission obligation:** request, child, accept, packet, byte, timer and pin resources are charged before state becomes externally reachable.
4. **Sequence obligation:** modular sequence, ACK, window and control-flag acceptability precede mutation or buffer release.
5. **Handshake obligation:** SYN state and negotiated options are consistent from initial response through final ACK and listener promotion.
6. **Queue obligation:** send, retransmission, receive, out-of-order and accept queues have one owner, explicit bounds and ordered wakeups.
7. **Timer obligation:** each timer has one purpose, deadline, generation and release path; callback and cancellation cannot both own completion.
8. **Close obligation:** FIN, half-close, simultaneous close, abort and errors preserve directional stream and application semantics.
9. **Reset obligation:** RST or unexpected SYN is statefully validated and challenge responses are bounded.
10. **TIME-WAIT obligation:** retained state protects retransmitted final control and tuple reincarnation for the required interval.
11. **Completion obligation:** local acceptance, transport ACK, peer stack delivery and peer application consumption are never conflated.
12. **Teardown obligation:** new lookup and callback ownership stop before tables, queues, timers, routes, pages and the object retire once.

An inductive argument starts with a uniquely owned initialized TCB or request. Each accepted event proves identity, lifetime and state guard before changing sequence, queues or timers. Publication makes all effects visible atomically; failure keeps the prior valid state or enters one terminal owned path. Therefore no unvalidated segment can advance the incarnation, and no object can be reclaimed while a declared owner remains—provided every implementation transition satisfies the obligations.

This is a proof framework, not a proof of a TCP stack. Real evidence needs specification review, model and property testing, packet fuzzing, sanitizers, lock and RCU diagnostics, timer fault injection, memory pressure, namespace teardown, cross-implementation tests and production-scale measurement.

## Alternatives and Trade-Offs

- **Full socket per SYN versus compact request:** full objects simplify promotion; compact requests reduce amplification but duplicate selected state.
- **Retained requests versus SYN cookies:** retained state supports richer negotiation; cookies save memory while constraining encoded information.
- **One connection hash versus namespace-owned tables:** sharing saves memory; separate tables improve isolation and NUMA placement.
- **Socket lock versus finer-grained synchronization:** one lock simplifies transitions; finer ownership can reduce contention and multiply races.
- **Per-CPU timers versus global wheel:** locality improves common paths; migration and teardown become more complex.
- **Immediate ACK versus delayed ACK:** immediate feedback reduces latency; delay reduces packet rate but adds timing interactions.
- **Large receive window versus bounded memory:** large windows support high bandwidth-delay products; advertised capacity can invite more retained data.
- **Aggressive out-of-order retention versus drop:** retention avoids retransmission; dropping limits memory during reordering or attack.
- **Copy send buffers versus zero copy:** copying simplifies application reuse; pinning saves bandwidth and extends completion ownership.
- **Fine-grained errors versus compatibility masking:** precise errors aid diagnosis; some APIs intentionally collapse asynchronous network outcomes.
- **Early child promotion versus late allocation:** early promotion reduces final-ACK latency; late allocation resists incomplete-handshake pressure.
- **Strict TIME-WAIT retention versus safe reuse heuristics:** retention is simple and robust; reuse can reduce port pressure with more conditions.
- **Challenge ACKs versus silent drops:** challenges help resynchronize and resist injection; they consume bounded response capacity.
- **Keepalive versus application liveness:** kernel probes find some dead paths; application protocols understand semantic health better.
- **Cached route versus fresh route:** caching lowers send cost; path and policy generations require revalidation.
- **Rich per-connection tracing versus sampling:** full history diagnoses races; sampling controls overhead and sensitive cardinality.

## Failure Modes and Misconceptions

- “A five-tuple is globally unique.” Network namespaces and binding scope can repeat it.
- “A hash lookup pins the socket.” Lifetime protection must explicitly extend through use.
- “SYN-RECEIVED is already an accepted connection.” It is incomplete handshake state.
- “SYN backlog and accept backlog are one queue.” They represent different admission stages.
- “Increasing the SYN backlog fixes accept stalls.” A saturated accept queue or application can remain the bottleneck.
- “SYN cookies increase server capacity.” They protect handshake memory under specific pressure and have trade-offs.
- “A random ISN is automatically safe.” Generation also needs tuple binding and progression properties.
- “Sequence integers compare normally.” Wrap requires protocol-defined modular ordering.
- “SYN and FIN carry no data, so consume no sequence.” Each consumes one sequence number.
- “Any ACK advances the sender.” It must acknowledge sent, acceptable sequence space.
- “Checksum-valid means connection-valid.” Tuple, incarnation, state and sequence checks still apply.
- “Any in-window reset should abort immediately.” Modern validation and challenge rules narrow spoofing exposure.
- “FIN closes both directions.” TCP streams close independently.
- “EOF can precede queued bytes.” Receive exposes preceding accepted bytes before FIN end-of-stream.
- “Successful send means the peer read data.” It can mean only local kernel acceptance.
- “Transport ACK means peer application consumption.” It generally confirms peer transport processing, not application use.
- “Retransmission timeout and keepalive are equivalent.” They protect different states and evidence.
- “Canceling a timer means its callback never started.” Cancellation must synchronize with an already-running callback.
- “One timer reference covers all rearming.” Generations distinguish obsolete callbacks.
- “TIME-WAIT is leaked established state.” It deliberately protects tuple and final-FIN semantics.
- “Destroying TIME-WAIT early only saves memory.” It can admit delayed old segments into a new incarnation.
- “Out-of-order data is bounded by advertised payload.” Backing allocation and fragment metadata require real accounting.
- “Process exit immediately frees every socket.” Orphaned protocol state may remain for close and retransmission.
- “Listener close cannot race final ACK.” Packet processing and application teardown run concurrently.
- “Socket count measures TCP memory.” Queues, fragments, timers, pins and ancillary objects can dominate.

## Worked Examples

### Example 1

A listener allows 1,024 incomplete requests but only 128 completed unaccepted children. SYN cookies keep the request count low during legitimate load, yet the accept queue fills because the application is stalled.

Cookie activation cannot solve this bottleneck. The service must diagnose acceptance latency and completed-queue overflow separately.

### Example 2

The following executable toy checks a guarded active-close path. It models no packets, modular sequence validation, retransmission, timers, kernel sockets, peer, or concurrency.

<!-- bijux-verify: {"id":"guarded-connection-transitions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"active_open: CLOSED -> SYN-SENT\nvalid_syn_ack: SYN-SENT -> ESTABLISHED\napplication_close: ESTABLISHED -> FIN-WAIT-1\nfin_acknowledged: FIN-WAIT-1 -> FIN-WAIT-2\npeer_fin: FIN-WAIT-2 -> TIME-WAIT\ntime_wait_expired: TIME-WAIT -> CLOSED\nfinal=CLOSED\n","stderr":""}} -->
```python
state = "CLOSED"
transitions = [
    ("active_open", "CLOSED", "SYN-SENT"),
    ("valid_syn_ack", "SYN-SENT", "ESTABLISHED"),
    ("application_close", "ESTABLISHED", "FIN-WAIT-1"),
    ("fin_acknowledged", "FIN-WAIT-1", "FIN-WAIT-2"),
    ("peer_fin", "FIN-WAIT-2", "TIME-WAIT"),
    ("time_wait_expired", "TIME-WAIT", "CLOSED"),
]

for event, required, result in transitions:
    if state != required:
        raise RuntimeError(f"{event} invalid in {state}")
    print(f"{event}: {state} -> {result}")
    state = result

print(f"final={state}")
```

### Example 3

SND.UNA is 1,000, SND.NXT is 1,500, and a segment ACKs 1,800. Even with a valid checksum and tuple, the ACK cannot free send buffers because it covers unsent sequence space.

The stack applies state-specific response rules and retains its retransmission ownership.

### Example 4

RCV.NXT is near $2^{32}$ and a valid segment begins after numerical wrap. An ordinary unsigned comparison calls it “smaller” and drops it. Modular comparison within the bounded receive window orders it correctly.

### Example 5

A final handshake ACK races listener close. The receive path holds a protected listener generation, but close invalidates admission before promotion. The ACK cannot publish a child onto a dead accept queue.

Request, route, timer and packet resources retire once through the losing path.

### Example 6

An application calls `shutdown(write)` after all queued bytes are segmentized. The stack sends FIN and enters FIN-WAIT-1, but it continues receiving. Peer data remains deliverable until the peer's FIN establishes EOF.

Half-close preserves the opposite stream direction.

### Example 7

An acceptable remote FIN arrives and is ACKed, but the final ACK is lost. The peer retransmits FIN while this endpoint is in TIME-WAIT. The endpoint ACKs again and restarts the required protection timer.

Deleting state after the first ACK would leave the peer unable to complete gracefully.

### Example 8

A forged RST has the right tuple but an unacceptable sequence. The synchronized connection does not abort. Under applicable modern behavior, an in-window but non-exact suspicious reset can elicit a rate-limited challenge ACK.

Tuple knowledge alone is not abort authority.

### Example 9

One socket retains 64 KiB of useful out-of-order payload in many 2 KiB buffers plus metadata. Payload-only accounting underestimates memory substantially. Charging truesize and objects triggers bounded pruning before host pressure becomes global.

### Example 10

Clients report connection timeouts. Device, route and SYN backlog counters are normal; request promotion succeeds; accept-queue overflow rises and application accept latency spikes.

The evidence identifies server admission after handshake, not packet loss or SYN flood, as the current failure stage.

## Cross-Program Connections

- **Network engineering:** TCP sequence space, handshake, options, retransmission, flow control and close define interoperable state.
- **Data structures engineering:** tuple hashes, interval trees, queues, timer wheels, reference counts and RCU organize connection objects.
- **Security engineering:** SYN floods, ISN prediction, reset injection, namespace isolation and resource accounting define attack resistance.
- **Distributed systems:** partial failure, delayed messages, incarnation identity, acknowledgments, leases and failure detectors recur in connections.
- **Performance engineering:** cache locality, queue depth, batch size, timers, zero copy, contention and memory pressure determine scale.
- **API and service engineering:** connect, accept, send, receive, half-close, deadlines and errors expose kernel state to applications.
- **Platform engineering:** listener backlog, namespaces, cgroups, observability, load balancing and graceful shutdown operationalize connections.
- **Formal methods:** guarded state machines, modular arithmetic, ownership, temporal timers and refinement make transitions reviewable.
- **Reliability engineering:** retransmission, retry budgets, timeout, failover, orphan cleanup and teardown cover recovery.
- **Privacy engineering:** tuple logs, payload tracing, timing data and per-connection identifiers require controlled observability.

## References

1. IETF, [RFC 9293: Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc9293.html), current base TCP state machine, sequence variables, segment processing, open, close, reset and user events; retrieved 2026-09-04.
2. IETF, [RFC 5961: Improving TCP's Robustness to Blind In-Window Attacks](https://www.rfc-editor.org/rfc/rfc5961.html), challenge ACKs and hardened RST, SYN and ACK handling; retrieved 2026-09-04.
3. IETF, [RFC 6528: Defending against Sequence Number Attacks](https://www.rfc-editor.org/rfc/rfc6528.html), connection-specific initial sequence number generation; retrieved 2026-09-04.
4. IETF, [RFC 7323: TCP Extensions for High Performance](https://www.rfc-editor.org/rfc/rfc7323.html), window scaling, timestamps, protection against wrapped sequences and option negotiation; retrieved 2026-09-04.
5. IETF, [RFC 6298: Computing TCP's Retransmission Timer](https://www.rfc-editor.org/rfc/rfc6298.html), RTT measurement, retransmission timeout and backoff; retrieved 2026-09-04.
6. IETF, [RFC 5681: TCP Congestion Control](https://www.rfc-editor.org/rfc/rfc5681.html), congestion window, acknowledgments, loss response and interaction with connection state; retrieved 2026-09-04.
7. IETF, [RFC 4987: TCP SYN Flooding Attacks and Common Mitigations](https://www.rfc-editor.org/rfc/rfc4987.html), backlog exhaustion, SYN caches, cookies, filtering and operational trade-offs; retrieved 2026-09-04.
8. IETF, [RFC 1337: TIME-WAIT Assassination Hazards in TCP](https://www.rfc-editor.org/rfc/rfc1337.html), TIME-WAIT failure modes and old duplicate protection; retrieved 2026-09-04.
9. IETF, [RFC 6191: Reducing the TIME-WAIT State Using TCP Timestamps](https://www.rfc-editor.org/rfc/rfc6191.html), constrained tuple reuse and timestamp conditions; retrieved 2026-09-04.
10. Linux Kernel Documentation, [IP Sysctl](https://docs.kernel.org/networking/ip-sysctl.html), listen backlog, SYN requests, syncookies, TIME-WAIT, orphan and TCP memory controls; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design a passive-open path from validated SYN through request admission, SYN-ACK retransmission, final ACK, established publication and application accept. Include overload, listener close, option state and ownership.

### Exercise 2

Given wrap-adjacent send and receive sequence spaces, specify safe tests for segment data, ACK, SYN, FIN and RST before state mutation. Explain the half-space assumption.

### Exercise 3

Design timer ownership for retransmission, delayed ACK, persist, keepalive, handshake, FIN-WAIT and TIME-WAIT under concurrent packet receipt, application close, CPU migration and namespace teardown.

### Exercise 4

Design hierarchical resource controls for a public TCP service exposed to SYN floods, legitimate bursts, slow accept, out-of-order data, zero-copy sends, orphans and TIME-WAIT pressure.

### Exercise 5

Construct a test and observability plan for connection lookup, state transitions, reset hardening, half-close, tuple reuse and teardown. State what passing evidence cannot prove.

## Answers to the Exercises

### Answer 1

After header, checksum and route-context validation, look up the listener using namespace, family, addresses, ports, bound interface, mark and listener precedence. Protect its lifetime and verify LISTEN state. Check per-listener and hierarchical request limits before allocating a compact request; if pressure policy selects a cookie, encode only supported state and record fallback activation.

Choose a connection-specific unpredictable ISN, capture the client sequence, negotiated MSS, window scale, timestamps and other permitted options, retain reply route context, publish request lookup, transmit SYN-ACK, and arm one request timer generation. Duplicate SYNs find the same incarnation and trigger defined retransmission rather than duplicate state.

The final ACK must match tuple, listener generation, request incarnation, server SYN and acceptable client sequence. Before promotion, reserve full socket memory, established-hash membership and accept-queue capacity. Construct the child completely, publish it, enqueue it, then wake the listener. If close wins, queue admission fails or allocation fails, do not publish a partial child; remove request state, cancel or synchronize its timer, release packet and route ownership once, and apply the protocol's response policy.

### Answer 2

Represent differences modulo $2^{32}$ and define before or after only for distances less than $2^{31}$. TCP's legal windows and outstanding data must stay within that half-space so ordering is unambiguous. Never cast to a wider ordinary timeline without a proven unwrapping reference.

Compute segment sequence length as payload plus one for SYN plus one for FIN. Apply the state's receive-window rule, including special handling for zero-length segments and zero windows. Validate ACK within the sent interval from SND.UNA through SND.NXT before advancing or releasing bytes. Window updates also compare the segment and ACK that last updated the window.

SYN is acceptable only in the states and sequence context allowed by the current specification; synchronized-state unexpected SYN follows hardened challenge behavior where implemented. FIN is processed only after preceding sequence data and advances RCV.NXT once. RST validation is state-specific: SYN-SENT ties it to acknowledgment of the SYN, while synchronized states validate sequence and applicable challenge rules. Any rejected earlier guard prevents later mutation.

### Answer 3

Give every timer a purpose, connection reference, deadline, CPU ownership and generation. Keep at most the contractually permitted timer instance per purpose. Arming publishes the deadline and generation before the timer becomes callable. Rearming invalidates the old generation. A callback acquires or already owns a protected reference, locks or otherwise serializes the connection, and rechecks purpose, generation and state before transition.

Cancellation changes armed state under the same protocol and synchronizes with an executing callback or transfers the final reference to it. An ACK can cancel retransmission and arm a later timer without letting the old callback back off the new state. Data arrival can cancel delayed ACK; window update can stop persist; close can stop keepalive; handshake promotion retires the request timer; retransmitted FIN can restart TIME-WAIT.

CPU migration first prevents local execution, transfers or cancels timer ownership, and publishes the new target before resuming. Namespace teardown blocks new arming, unhashes connections, synchronously drains or invalidates callbacks, then drops timer references. Tests race every cancel, expiry and rearm boundary and assert exactly one release.

### Answer 4

Limit incomplete requests and their bytes per listener, source policy, cgroup, namespace and host. Separately cap completed accept-queue children and measure application accept delay. Use compact requests, bounded retransmission and carefully monitored cookies only for backlog pressure. Rate-limit challenge ACKs and other control output independently.

For established sockets, charge object state, packet truesize, send and retransmission bytes, out-of-order buffers, ancillary data, timers, route references and pinned zero-copy pages. Enforce socket send and receive bounds, user locked-memory limits, cgroup memory, namespace TCP pressure and host reserves before admission. Bound orphans, FIN-WAIT and TIME-WAIT objects with protocol-safe policies rather than unsafe early deletion.

Reserve narrow capacity for ACKs, RSTs, close, notification draining and reclaim. Under pressure, prune out-of-order data, reduce advertised windows, reject new requests, shed before full child allocation, or fail application sends according to explicit semantics. Never use payload-only accounting. Attribute every rejection to SYN admission, promotion, accept, established memory, pins, orphan or TIME-WAIT stage.

### Answer 5

Generate active, passive and simultaneous opens; all losses and duplicates in the handshake; option combinations; sequence wrap; ACKs below and above valid bounds; zero windows; reordered and overlapping data; FIN in every legal state; simultaneous close; retransmitted FIN; valid, invalid and challenge RST cases; and delayed old segments after tuple reuse. Differentially compare transitions with a reviewed model where feasible.

Race lookup with close, final ACK with listener teardown, ACK with retransmission expiry, receive with half-close, callbacks with cancellation, CPU hotplug and namespace destruction. Inject allocation, route, hash and queue failure at every transition. Apply memory, bounds, leak, lock, RCU and reference diagnostics.

Record tuple with privacy controls, namespace, connection generation, old and new state, event, sequence-window decision, queue sizes, memory charge, timer purpose and generation, challenge outcome, error, CPU and latency. Combine packet capture, internal transition traces, socket snapshots, listener metrics and application timestamps.

Finite tests cannot prove every modular-arithmetic case or interleaving. A model can share specification errors. Packet capture may observe offload-altered representations. Loopback omits real loss, path changes and devices. Passing state tests does not prove performance, SYN-flood capacity, off-path resistance, privacy or cross-implementation conformance. State these limits.
