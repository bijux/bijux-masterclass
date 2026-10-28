---
module_id: OS-077
program: Operating Systems
level: 2
module_number: 77
title: Congestion-Control Hooks
status: complete
last_verified: 2026-09-04
---

# Congestion-Control Hooks

## One-Page Review

### Governing question

How should an operating system expose pluggable congestion-control decisions while ensuring that every algorithm consumes truthful delivery, loss, ECN, RTT, application-limit, and flight-size signals and produces bounded congestion windows and pacing rates without violating transport correctness, kernel lifetime, fairness, or safe rollback?

### Essential definitions

- A **congestion window (`cwnd`)** limits sender bytes or segments outstanding in the network; it is distinct from the receiver-advertised window.
- A **slow-start threshold (`ssthresh`)** separates rapid startup growth from congestion avoidance and records a response to congestion.
- A **congestion-control hook** is a kernel callback invoked at a defined lifecycle or signal point to initialize state, process ACK-derived samples, choose a window or rate, react to loss or ECN, report diagnostics, or release state.
- A **rate sample** estimates newly delivered data over an observation interval and carries provenance such as prior flight, RTT, loss, ECN, retransmission, and application-limited status.
- **Pacing** schedules transmission over time to enforce a rate and burst bound instead of releasing an entire window at once.
- **Application-limited** means the sender lacked enough ready data to exercise its allowed flight; the resulting delivery sample may be a lower bound on path capacity.
- **ACK compression** bunches acknowledgments and can make a short-interval delivery estimate appear larger than the actual bottleneck rate.
- **ECN** conveys congestion through packet marking and transport feedback without requiring loss for every signal.
- **Recovery** governs transmission after detected loss; it is related to but not interchangeable with the steady congestion-control algorithm.
- **Algorithm-private state** is per-connection memory owned by the selected controller and initialized and released through its lifecycle contract.

### Central model, mechanism, or theorem

Represent a controller invocation as

$$
H(C,E,X)\rightarrow(c',s',p',X',D),
$$

where transport core state $C$ contains validated sequence, delivery, flight, receiver-window and timer facts; event $E$ identifies ACK, loss, ECN, idle restart, state change or transmit opportunity; private state $X$ belongs to the algorithm; and outputs are congestion window $c'$, slow-start threshold $s'$, pacing rate $p'$, new private state $X'$, and diagnostics $D$.

The transport core owns protocol truth and a safety envelope. The algorithm estimates and selects within that envelope. It cannot acknowledge bytes, invent delivery, exceed representable bounds, bypass receiver flow control, retain dead socket pointers, sleep in an atomic callback, or transmit directly around pacing and recovery. Invalid or unavailable algorithm output falls back to a known-safe controller without leaving partial private state.

### Critical invariants

- Hooks receive validated immutable event facts and mutate only fields authorized by the callback contract.
- Newly acknowledged bytes increase window at most once; duplicate, old, invalid, or split ACKs cannot manufacture growth.
- `cwnd`, `ssthresh`, pacing rate, burst size, and algorithm arithmetic remain positive, bounded, unit-consistent, and overflow-safe.
- Send eligibility respects the minimum of congestion, receiver, local, pacing, recovery, and policy constraints.
- Loss, ECN, timeout, reordering, route change, idle restart, and application limitation remain distinct signals.
- Rate and RTT samples record interval and provenance; invalid, zero-duration, retransmission-ambiguous, or compressed samples are rejected or handled conservatively.
- GSO aggregates, retransmissions, SACKed data, and packets in flight use the transport core's logical accounting rather than raw SKB count.
- Algorithm selection and replacement initialize new state before publication and keep old code and state alive until callbacks quiesce.
- Per-connection, cgroup, namespace, route and global policy cannot select an unregistered, incompatible, or unauthorized algorithm.
- Observability and experimentation never remove standards safety, resource bounds, rollback, or tenant isolation.

### Common failures

Common failures are treating `cwnd` as a sending command, confusing packets with bytes, growing once per ACK instead of newly acknowledged data, using receiver window as congestion evidence, interpreting every loss as congestion or every reordering event as loss, trusting an application-limited rate sample as capacity, dividing by a zero or tiny interval, allowing ACK compression to set an unbounded pace, counting a GSO aggregate as one wire packet, invoking a sleeping hook from deferred network context, switching algorithms without migrating or resetting private state, detaching code while sockets retain callbacks, exposing experimental defaults globally, and benchmarking only throughput on one clean path.

### Compact example

With sender MSS 1,200 bytes, `cwnd=4,800`, and `ssthresh=9,600`, three ACK events newly acknowledge 1,200, 1,200, and 2,400 bytes. A byte-counted slow-start hook increases by `min(acked, MSS)` per event, producing windows 6,000, 7,200, and 8,400 rather than granting two increments for the last cumulative ACK. A congestion event halves the window subject to a two-MSS floor, setting both threshold and current window to 4,200. This toy does not decide whether the signal was valid loss, which recovery packets may send, or how pacing should change.

### Connections

[OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), [OS-075](075-routing-and-neighbor-tables.md), and [OS-076](076-connection-state-management.md) connect hooks to packet truth, timers, connection state, scheduling, concurrency and evidence.

## Governing Question

Congestion control is transport policy executed inside a correctness-critical data path. The kernel knows which sequence ranges were sent, delivered, declared lost, retransmitted or ECN-marked. An algorithm turns those facts into an allowed flight and pacing rate. A clean interface must preserve this ownership boundary.

The governing question is how to permit algorithm innovation without giving plugins undefined access to protocol state or system lifetime. A controller can execute once per ACK at millions of events per second. It can amplify bad samples into bursts, starve other flows, overflow arithmetic, retain resources after detach, or make a namespace-wide outage. Extensibility therefore requires a narrow ABI, verification, safety clamps, staged rollout, and a trustworthy fallback.

## Why This Matters

No one congestion algorithm is ideal for every path. High-bandwidth long-delay links, shallow data-center queues, wireless loss, satellite delay, low-rate interactive traffic and application-limited RPCs produce different observations. Pluggability lets operators and researchers match control to evidence without rebuilding the whole transport stack.

The cost of a mistake is shared. Excess sending raises queue delay and loss for unrelated traffic. Excess caution wastes capacity. An algorithm that performs well in isolation can be unfair beside deployed Reno or CUBIC flows, unstable under delayed ACKs, or unsafe when offloads change event granularity.

Kernel hooks also become a software supply and compatibility boundary. Built-in modules, loadable modules and verified runtime programs have different update and lifetime mechanics, but all execute with kernel state. Selection, attachment and rollback need the same discipline as any other privileged production policy.

## Prerequisites and Retrieval

Review [OS-007](007-kernel-data-structures.md), [OS-024](024-atomic-operations.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-054](054-kernel-read-copy-update.md), [OS-055](055-numa-memory-placement.md), [OS-058](058-timer-and-interrupt-scalability.md), [OS-071](071-socket-layer-architecture.md), [OS-072](072-packet-reception-and-transmission.md), [OS-073](073-network-buffers.md), [OS-074](074-protocol-processing.md), [OS-075](075-routing-and-neighbor-tables.md), and [OS-076](076-connection-state-management.md).

Retrieve these distinctions:

- congestion window, receiver window, bytes in flight, send-buffer bytes, pacing budget and qdisc occupancy are different constraints;
- ACK arrival, new delivery, SACK information, declared loss, retransmission, ECN feedback and timeout are different signals;
- packet count, segment count, bytes, GSO aggregates and wire packets are different units;
- RTT sample, smoothed RTT, minimum RTT, ACK interval and delivery-rate interval have different provenance;
- path capacity, available bandwidth, bottleneck bandwidth, sending rate, delivery rate and goodput are not synonymous;
- application-limited, receiver-limited, congestion-limited, pacing-limited and CPU-limited transfers provide different evidence;
- congestion control, loss detection, loss recovery, retransmission timing, flow control and packet scheduling are coupled but separately owned;
- algorithm registration, default selection, per-route choice, per-socket choice, initialization, switching and release are different lifecycle events;
- built-in code, loadable kernel modules and verified runtime hooks have different compatibility and revocation contracts;
- a passing benchmark, fairness claim, safety claim and Internet-wide deployment approval require different evidence.

## Learning Objectives

After this module, you should be able to:

1. define a congestion-control hook contract with lifecycle, ACK, delivery, loss, ECN, state, idle and diagnostic events;
2. separate transport-core truth from algorithm estimates and enforce a bounded output safety envelope;
3. reason about `cwnd`, `ssthresh`, receiver window, flight, pacing, recovery, GSO, delayed ACKs and application limitation;
4. design safe registration, per-socket selection, algorithm switching, code lifetime, private-state migration and fallback;
5. evaluate Reno-like, CUBIC-like, delay-, ECN-, or model-based controllers without conflating their signal assumptions;
6. protect callback latency, arithmetic, memory, namespace policy and observability under adversarial ACK and loss patterns;
7. validate new controllers with models, emulation, coexistence, path diversity, fault injection, canaries and rollback criteria.

## Core Exposition

### Put protocol facts in the core

The transport core validates ACK sequence space, updates SACK state, identifies newly delivered data, detects or declares loss, tracks retransmission ambiguity, computes flight, and timestamps delivery. A congestion hook consumes these facts after their ownership is settled.

Do not ask every algorithm to parse ACKs or infer whether bytes were previously acknowledged. Duplicate implementations drift and expose security-sensitive sequence logic. Supply a stable event object whose fields, units, validity flags and lifetime are explicit.

### Define a lifecycle, not only an ACK callback

A controller needs initialization after transport basics exist, event callbacks, optional state-change notification, output queries, diagnostics and release. Initialization can reject incompatible connection features. Release runs exactly once after callbacks quiesce.

State changes include open, disorder, recovery, timeout loss, congestion-window reduction, idle restart, route change and close as supported by the host interface. Absence of a callback is not permission to retain stale assumptions; the core establishes defaults.

### Keep the safety envelope outside the plugin

The core enforces minimum and maximum windows, representable pacing rates, receiver window, unsent data, recovery rules, amplification limits, path MTU and device constraints. It validates plugin output before publication and falls back on invalid values.

This envelope cannot prove fairness or performance. It prevents local structural failures such as zero progress, overflow, sending beyond acknowledged protocol state, or bypassing flow control. Network safety still depends on algorithm design and evaluation.

### Make units impossible to confuse

Some specifications express windows in sender maximum segment units; implementations often store bytes or packets. Offloads combine multiple logical segments into one buffer. Declare the unit of every field and convert with checked arithmetic at one boundary.

When MSS changes after path discovery, preserve byte or segment semantics according to the algorithm contract. A raw `cwnd=10` is meaningless without units and current MSS. Count logical wire segments for algorithms whose equations require them, not SKB objects.

### Grow only for new delivery

ACK division can produce many acknowledgments for one segment. ACK compression can bunch legitimate acknowledgments. Window growth is tied to newly acknowledged bytes or the algorithm's rigorously defined delivery event, never the number of packets carrying ACK flags alone.

Appropriate byte counting caps growth per event where required. SACK information can establish delivered ranges without advancing the cumulative ACK; the core ensures a byte contributes to delivered accounting once.

### Interpret loss through provenance

Loss can be declared by duplicate ACK or SACK evidence, time threshold, packet threshold, retransmission timeout, local qdisc drop, device error, or another transport mechanism. Reordering can resemble loss. Corruption and policy drop can also remove packets.

Pass event type and confidence or provenance rather than one Boolean. The controller applies the response required by its protocol, while loss recovery owns which bytes to retransmit. Undo mechanisms require evidence that the congestion inference was spurious; they cannot arbitrarily restore an old window.

### Treat ECN as a counted signal

ECN-capable packets can arrive with congestion experienced marking, and transport feedback returns that information. Validate negotiation and feedback semantics before exposing counts. Avoid treating one sticky flag as the entire marking fraction.

An ECN-aware controller maintains counters across a defined observation window and reduces or adjusts according to its specification. Persistent marking must continue to reduce sending where required. Non-ECN controllers still need core-standard behavior rather than ignoring negotiated congestion feedback.

### Build rate samples from delivered data

A delivery-rate sample needs delivered bytes, a nonzero interval, timestamp provenance, prior in-flight state, retransmission and application-limit flags, RTT evidence, loss and ECN counts. Use the larger or otherwise specified send and acknowledgment interval to resist artifacts in one clock.

Reject negative, overflowed, zero-duration or otherwise invalid samples. ACK compression can still inflate a short sample; filters, bounds and multi-round evidence reduce damage. A sample during application limitation does not prove the path could not deliver faster.

### Couple windows to pacing deliberately

A window bounds volume in flight; pacing bounds release over time. Without pacing, a large window can emerge as a burst after wakeup, idle, ACK compression or timer delay. Derive rate from controller state using a declared gain and minimum RTT or other approved time basis.

The scheduler enforces pacing and a maximum burst even if callbacks arrive late. Pacing queues interact with qdiscs and NIC offloads; measure the actual wire or device release rather than assuming a configured rate became a smooth path rate.

### Handle startup, steady state and recovery separately

Startup probes an unknown path and can grow rapidly. Congestion avoidance seeks additional capacity around an operating point. Recovery responds to loss or marking while preserving an ACK clock and retransmitting missing data. Timeout loss has weaker evidence of viable flight and generally requires stronger reduction.

A plugin's internal modes must map to transport-core recovery states without contradicting them. Exiting recovery needs a clear event and cannot forget losses still outstanding.

### Recognize application and receiver limitation

If an application did not fill the available window, delivered rate underestimates possible capacity. Mark samples application-limited until delivery passes the boundary that began the limited period. Similarly, a small receiver window constrains flight independently of congestion.

Idle restart prevents a stale large window from releasing a path-sized burst after the ACK clock disappeared. Controllers may preserve learned models, but the core still applies restart and burst safety required by the selected protocol behavior.

### Specify private-state ownership

Allocate algorithm-private state within a fixed per-connection budget or through charged bounded allocation. Zero it before initialization. Only the selected algorithm may interpret it. Diagnostic export copies a versioned snapshot rather than exposing a live pointer.

On release, cancel algorithm-owned deferred work, detach external references, publish unavailability and wait for callbacks before freeing code or state. A runtime program or module remains pinned while any socket can invoke it.

### Switch algorithms transactionally

Switching an established connection is not name replacement. Old state can include bandwidth, minimum RTT, epochs, loss history and mode. Define whether the new algorithm initializes from safe core state, imports a versioned compatible snapshot, or rejects live switching.

Allocate and initialize replacement state first. Serialize with ACK and timer callbacks, publish the new operations and state together, then quiesce and release the old implementation. On failure, retain the old valid algorithm. Clamp carried `cwnd` and pace under new rules.

### Scope selection policy

Algorithm availability is a registry concern; default selection is a namespace or host policy; route and per-socket choices may override within authorization. Resolve the name to a pinned implementation before accepting the setting.

Tenant policy can restrict experimental algorithms, maximum pace or diagnostic access. One namespace changing its default must not mutate existing or future sockets in another namespace. Record which policy layer selected the final controller.

### Constrain runtime hooks

Callbacks execute in hot network contexts and must not block, recurse without bound, allocate unpredictably, or access unprotected memory. A verifier can prove instruction, pointer and helper constraints for a runtime program, but cannot by itself prove congestion fairness or Internet safety.

Bound callback time and detect invalid output. Provide only helpers with clear context and lifetime. Version structural interfaces through type information and feature checks; kernel internal layouts are not an eternal ABI.

### Handle arithmetic as adversarial input

ACKed bytes, intervals, windows, bandwidth products and gains can approach integer bounds. Use widened checked multiplication and division, saturating clamps where specified, and explicit fixed-point scale. Check denominators before division.

Order operations to retain precision without overflow. A controller that wraps pacing rate to a small value can stall; one that wraps `cwnd` upward can burst catastrophically. Both require fallback and telemetry.

### Measure coexistence and externalities

Throughput alone rewards aggressive algorithms. Measure completion time, goodput, queue delay, loss, ECN marking, retransmission, burstiness, fairness within and across RTTs, response after path change, short-flow impact and CPU cost.

Test alongside deployed Reno, CUBIC and other relevant flows, plus nonresponsive traffic. A lab bottleneck, emulator and production canary answer different questions. Document topology, queue, AQM, RTT, bandwidth, loss model, offloads, receiver behavior and workload.

### Roll out with a kill path

Registration does not authorize default use. Progress from model and unit tests to network emulation, isolated hosts, opt-in sockets, low-risk namespaces and bounded canaries. Define abort thresholds for loss, latency, fairness, retransmission, CPU, invalid samples and fallback.

Keep a known-safe implementation resident and selectable without depending on the failing hook. Detach prevents new selection, migrates or drains existing sockets under policy, waits for callbacks, then releases code. Preserve diagnostics for the rejected generation.

## Definitions and Notation

Let congestion window be $c$, receiver window $r$, current flight $f$, local unsent readiness $u$, and pacing credit $b$. A send is eligible only within

$$
x\le \min(\max(0,c-f),\max(0,r-f),u,b).
$$

Let $a$ be newly acknowledged bytes and $M$ sender MSS. One Reno-style slow-start bound is

$$
c'\le c+\min(a,M).
$$

This is a specific event rule, not a universal formula for every controller.

For a delivery sample with newly delivered bytes $d$ over valid interval $\Delta t>0$,

$$
\hat{R}=\frac{d}{\Delta t}.
$$

Attach flags $q=(q_{app},q_{retx},q_{delay},q_{valid})$ and never interpret $\hat{R}$ without them.

Let paced rate $P$ be computed from controller bandwidth estimate $B$ and gain $g$ using widened arithmetic:

$$
P=\operatorname{clamp}(gB,P_{min},P_{max}).
$$

Let algorithm lifecycle be

$$
U\xrightarrow{init}I\xrightarrow{publish}A\xrightarrow{detach}Q\xrightarrow{release}D,
$$

for uninitialized, initialized, active, quiescing and dead. Only $A$ accepts event callbacks.

Let callback generation $g_h$ and socket algorithm generation $g_s$ authorize mutation only when $g_h=g_s$ and the implementation reference remains pinned.

## Mechanisms, Invariants, or Proof Structure

Review a congestion-hook system with these obligations.

1. **Signal obligation:** transport core validates delivery, ACK, loss, ECN, RTT, flight and limitation facts before callback.
2. **Unit obligation:** every window, rate, time, packet, segment and byte value has explicit units and checked conversion.
3. **Growth obligation:** each newly delivered byte contributes at most as allowed; duplicate or divided ACKs cannot double-count.
4. **Safety-envelope obligation:** core clamps outputs and enforces flow control, recovery, pacing, burst and representable bounds.
5. **Sample obligation:** rate and delay samples carry validity, interval, retransmission, ACK and application-limit provenance.
6. **State obligation:** startup, avoidance, recovery, timeout, ECN, idle and route-change events have explicit transition meaning.
7. **Callback obligation:** hooks are bounded, nonblocking, nonrecursive, context-safe and unable to retain unprotected pointers.
8. **Private-state obligation:** memory is initialized, charged, versioned for export and released once after callbacks quiesce.
9. **Selection obligation:** registry, namespace, route and socket policy resolve to an authorized pinned compatible implementation.
10. **Switch obligation:** new state and operations publish atomically; failed migration keeps old state; old code retires after grace.
11. **Evaluation obligation:** evidence covers utilization, delay, loss, fairness, stability, CPU, path diversity and coexistence.
12. **Rollback obligation:** invalid output or rollout threshold activates an independent safe fallback and preserves diagnostics.

The proof boundary is deliberate. The core proves protocol and memory safety for any accepted plugin output within its envelope. An algorithm separately argues that its state updates satisfy congestion response and performance goals under stated signals. Deployment evidence then tests whether those signal assumptions hold on target paths. None of the three proofs substitutes for the others.

This framework does not prove an algorithm safe for the Internet. Such a claim needs standards analysis, extensive simulation and experiments, coexistence study, security review, implementation verification, operational canaries and independent scrutiny.

## Alternatives and Trade-Offs

- **Fixed built-in algorithm versus plugins:** fixed code narrows attack surface; plugins enable workload adaptation and experimentation.
- **Window-based versus rate-based control:** windows naturally bind flight; rates pair with pacing but depend heavily on time samples.
- **Loss-based versus delay-based signals:** loss is widely available but reactive; delay can respond earlier and is sensitive to baseline estimation.
- **ECN response versus loss-only fallback:** ECN can signal before drops; it requires valid negotiation, marking and feedback.
- **ACK callback versus batched delivery event:** per-ACK updates react quickly; batching reduces CPU and changes granularity.
- **Packets versus bytes:** packet units mirror some equations; byte units handle changing MSS and require careful conversion.
- **Algorithm-owned loss detection versus core-owned detection:** ownership can co-design recovery; central detection prevents semantic duplication.
- **Pacing in controller versus scheduler:** integrated logic sees model state; central scheduling enforces common timing and burst limits.
- **Fixed private state versus dynamic allocation:** fixed storage bounds cost; dynamic state permits richer models and expands failure paths.
- **Live migration versus new-connections-only:** migration accelerates rollout; new-only selection avoids incompatible state transfer.
- **Per-socket choice versus namespace default:** per-socket control supports experiments; defaults simplify governance and comparability.
- **Kernel module versus verified runtime program:** modules have broad implementation freedom; verification constrains memory and execution but not network behavior.
- **Strict output rejection versus clamping:** rejection surfaces bugs; clamping preserves availability and can conceal poor algorithms without telemetry.
- **Fast sampling versus filtered estimation:** fast signals adapt quickly and amplify noise; filtering stabilizes at the cost of lag.
- **Aggressive probing versus conservative growth:** probing discovers capacity; caution protects queues and competing flows.
- **Automatic rollback versus operator decision:** automation limits blast radius; complex metrics can trigger on benign workload shifts.

## Failure Modes and Misconceptions

- “`cwnd` is the number of packets to send now.” It bounds flight and still interacts with receiver window, data, pacing and recovery.
- “One SKB is one packet.” GSO can represent many logical or wire segments.
- “Every ACK proves new delivery.” Duplicate, stale or split ACKs may acknowledge no new byte.
- “More ACKs justify faster growth.” ACK division is not additional path capacity.
- “A delivery-rate sample equals bottleneck bandwidth.” It can reflect ACK timing, limitation, retransmission and measurement artifacts.
- “Application-limited samples prove low capacity.” The application did not test the available capacity.
- “Loss always means congestion.” Reordering, corruption, policy and device failure can cause loss-like evidence.
- “Reordering means loss recovery should never start.” Excessive delay waiting for certainty also harms correctness and performance.
- “ECN is a Boolean.” Counts and observation intervals often matter.
- “Receiver window is a congestion window.” It represents endpoint flow-control capacity.
- “Pacing makes windows unnecessary.” Flight bounds and burst/rate scheduling solve different constraints.
- “A configured pacing rate is the wire rate.” qdiscs, offloads, scheduler delay and device queues alter release.
- “Idle connections can reuse the old window instantly.” The ACK clock and path conditions may be stale.
- “Changing MSS leaves a segment-count window unchanged in bytes.” Unit conversion changes actual flight.
- “An algorithm can parse ACKs itself for flexibility.” That duplicates validated transport truth and security logic.
- “Verifier acceptance proves congestion safety.” It proves only specified program properties, not fairness or stability.
- “A callback may block because it is short on average.” Context rules apply to worst-case execution.
- “Private state dies when the algorithm is deselected.” Callbacks and code references must first quiesce.
- “Switching controllers only changes a function pointer.” Private state, windows, pace, modes and code lifetime also change.
- “Global default changes only new sockets everywhere.” Namespace and existing-socket semantics must be explicit.
- “Highest throughput wins.” Queue delay, loss, fairness, CPU and short flows are externalities.
- “One RTT and bandwidth pair represents the Internet.” Paths vary in queues, cross traffic, loss and feedback.
- “Emulation proves production behavior.” Models and timing differ from real hardware and workloads.
- “A canary with no alerts proves fairness.” Instrumentation may omit affected competing traffic.
- “Rollback can call the experimental hook.” A failed hook cannot be the sole path to its own containment.

## Worked Examples

### Example 1

A TCP socket has `cwnd=120,000` bytes, receiver window 80,000, and 70,000 bytes in flight. Congestion space is 50,000 but receiver space is only 10,000, so flow control is currently tighter. The controller cannot authorize more than 10,000 before pacing and local data limits.

### Example 2

This executable toy applies bounded newly-acknowledged growth and a multiplicative loss response. It models no transport, loss detector, recovery, RTT, pacing, ECN, network or fairness.

<!-- bijux-verify: {"id":"bounded-congestion-hook","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ack=1200 cwnd=6000\nack=1200 cwnd=7200\nack=2400 cwnd=8400\nloss ssthresh=4200 cwnd=4200\nmode=avoidance\n","stderr":""}} -->
```python
mss = 1200
cwnd = 4800
ssthresh = 9600

for newly_acked in (1200, 1200, 2400):
    cwnd += min(newly_acked, mss)
    print(f"ack={newly_acked} cwnd={cwnd}")

ssthresh = max(cwnd // 2, 2 * mss)
cwnd = ssthresh
print(f"loss ssthresh={ssthresh} cwnd={cwnd}")
print(f"mode={'slow_start' if cwnd < ssthresh else 'avoidance'}")
```

### Example 3

One cumulative ACK newly acknowledges 24,000 bytes after delayed processing. A naive per-byte unbounded update creates a large instant window jump. The core supplies one delivery event and the algorithm applies its specified cap and pacing.

### Example 4

A GSO buffer contains 32 logical TCP segments. Counting one SKB as one packet understates flight and loss. The transport core reports logical bytes and segments using metadata validated before the hook runs.

### Example 5

A rate sample reports 2 MiB delivered over zero microseconds because two timestamps collapsed to one clock tick. The hook rejects the sample instead of dividing or clamping an infinite estimate to the maximum pace.

### Example 6

An RPC sends 8 KiB then waits for an application dependency. Its measured delivery rate is low and marked application-limited. A bandwidth model does not reduce its capacity estimate solely from this sample.

### Example 7

ECN marking rises for one round without packet loss. An ECN-aware controller reduces according to the marked fraction and observation window. A loss-recovery module does not invent retransmissions because no bytes were declared lost.

### Example 8

An administrator switches a live socket from algorithm A to B. B rejects A's private snapshot version. The transaction retains A, reports incompatibility and changes no operations pointer or pace.

### Example 9

A runtime controller returns `cwnd=0` after arithmetic underflow. The core rejects the output, activates the safe fallback, records algorithm generation and sample inputs, and preserves minimum forward progress.

### Example 10

A canary improves bulk throughput 15 percent but doubles p99 latency for competing RPCs and increases retransmission. The rollout abort threshold fires even though the canary flow's own completion time improved.

## Cross-Program Connections

- **Network engineering:** congestion, queueing, ECN, RTT, loss, reordering and path diversity define controller signals.
- **Control theory:** feedback delay, gain, stability, noise, filtering, operating points and saturation structure algorithm behavior.
- **Performance engineering:** pacing, offload, CPU, cache, goodput, latency percentiles and experimental design determine evidence.
- **Distributed systems:** delayed feedback, partial observation, adaptive retry, fairness and shared bottlenecks recur at larger scales.
- **Security engineering:** adversarial ACK patterns, arithmetic, privileged hooks, tenant policy and safe fallback define attack boundaries.
- **Data structures engineering:** per-connection state, registries, callback tables, rate filters, timers and immutable publication implement hooks.
- **Platform engineering:** namespace defaults, cgroup policy, runtime programs, canaries, telemetry and rollback operationalize selection.
- **API and service engineering:** short flows, application limitation, streaming, deadlines and connection reuse shape workload demand.
- **Formal methods:** contracts, safety envelopes, transition systems, bounded arithmetic and lifecycle proofs separate responsibilities.
- **Reliability engineering:** fallback, quiescence, fault injection, blast-radius limits and rollback make experimental policy survivable.

## References

1. IETF, [RFC 5681: TCP Congestion Control](https://www.rfc-editor.org/rfc/rfc5681.html), slow start, congestion avoidance, fast retransmit, fast recovery, ACK behavior and idle restart; retrieved 2026-09-04.
2. IETF, [RFC 9438: CUBIC for Fast and Long-Distance Networks](https://www.rfc-editor.org/rfc/rfc9438.html), current CUBIC window growth, decrease, Reno friendliness and safety behavior; retrieved 2026-09-04.
3. IETF, [RFC 5033: Specifying New Congestion Control Algorithms](https://www.rfc-editor.org/rfc/rfc5033.html), evaluation, fairness, safety, deployment and standards guidance; retrieved 2026-09-04.
4. IETF, [RFC 3168: The Addition of Explicit Congestion Notification to IP](https://www.rfc-editor.org/rfc/rfc3168.html), ECN negotiation, marking, feedback and congestion response; retrieved 2026-09-04.
5. IETF, [RFC 6937: Proportional Rate Reduction for TCP](https://www.rfc-editor.org/rfc/rfc6937.html), bounded sending during loss recovery; retrieved 2026-09-04.
6. IETF, [RFC 9406: HyStart++](https://www.rfc-editor.org/rfc/rfc9406.html), delay-based slow-start exit, limited slow start and implementation considerations; retrieved 2026-09-04.
7. IETF, [RFC 7661: Updating TCP to Support Rate-Limited Traffic](https://www.rfc-editor.org/rfc/rfc7661.html), congestion-window validation, application limitation and restart; retrieved 2026-09-04.
8. IETF, [RFC 9002: QUIC Loss Detection and Congestion Control](https://www.rfc-editor.org/rfc/rfc9002.html), delivery signals, recovery, persistent congestion and pacing architecture; retrieved 2026-09-04.
9. IETF, [RFC 8985: The RACK-TLP Loss Detection Algorithm for TCP](https://www.rfc-editor.org/rfc/rfc8985.html), time-based loss evidence, reordering and tail-loss probes; retrieved 2026-09-04.
10. Linux Kernel Documentation, [IP Sysctl](https://docs.kernel.org/networking/ip-sysctl.html), available and allowed TCP congestion algorithms, default selection, ECN and pacing-related controls; retrieved 2026-09-04.

## Exercises

### Exercise 1

Design a kernel congestion-control hook interface covering initialization, ACK and rate samples, loss, ECN, state changes, pacing, diagnostics and release. Divide responsibilities between core and plugin.

### Exercise 2

Given delayed ACKs, ACK compression, GSO, retransmissions, application-limited intervals and an MSS change, specify unit-safe delivery samples and window updates.

### Exercise 3

Design a transactional live switch between two incompatible controllers implemented as runtime hooks. Include policy, private state, callbacks, output clamps, failure and code lifetime.

### Exercise 4

Build an evaluation and rollout plan for a controller intended for mixed bulk transfers and latency-sensitive RPCs across data-center and wide-area paths.

### Exercise 5

Construct adversarial and fault tests for hook arithmetic, callback context, signal validation, namespace isolation, detachment and fallback. State evidence limits.

## Answers to the Exercises

### Answer 1

Have the transport core own sequence validation, newly delivered ranges, SACK interpretation, loss declaration, retransmission state, flight, receiver window, timestamps, ECN negotiation and socket lifetime. Supply immutable versioned event records with bytes, logical segments, interval, RTT, loss, ECN, prior flight, retransmission, delayed-ACK, application-limited and validity fields.

Expose bounded `init`, `on_delivery`, `on_loss`, `on_ecn`, `on_state`, `ssthresh`, `pace`, `diagnostics` and `release` operations as appropriate. Specify execution context, permitted fields, units, maximum runtime, allocation rules and call ordering. Private state is zeroed, charged and pinned to the implementation.

The plugin estimates and returns window, threshold, pace and diagnostics. The core checks overflow, minimum and maximum, receiver window, recovery, available data, pacing and burst safety before publication. Invalid return selects a resident fallback. Release begins after selection stops and all callbacks quiesce. The plugin never directly sends, frees transport queues or retains an unprotected socket pointer.

### Answer 2

Count newly delivered bytes once in the transport core even when cumulative and selective ACK information overlap. Preserve logical segment count separately from SKB count so GSO does not collapse flight. Rate samples include delivered bytes and the valid maximum or specified composition of send and acknowledgment intervals; reject zero or negative duration.

Mark retransmitted delivery and ambiguity, ACK-likely-delayed, ECN and application-limited provenance. Filter or cap compressed ACK samples rather than treating a short burst as immediate capacity. An application-limited sample may confirm a lower bound but should not reduce a maximum estimate under an algorithm that excludes it.

Express the hook boundary in bytes and microseconds or another single declared unit. Convert equations defined in segments with current MSS using widened checked arithmetic. On MSS change, preserve the specification's byte or segment intent and clamp resulting flight. Window growth consumes newly acknowledged bytes with the algorithm's per-event and per-round bounds; retransmission delivery is never counted twice.

### Answer 3

Authorize algorithm B under socket, cgroup and namespace policy and pin its verified program and operation type. Allocate zeroed B state within the configured budget. Under the socket's transition serialization, snapshot safe core facts and an optional versioned A export. Let B import only a recognized schema or initialize from core state.

Validate B's initial `cwnd`, threshold and pace against receiver window, flight, recovery state, arithmetic bounds and burst policy. Publish B operations, private-state pointer and a new algorithm generation atomically. New callbacks use B; already-entered A callbacks finish under A's program reference and cannot publish after generation validation fails.

After a grace or callback drain, invoke A release and drop its program reference. If any preparation or import fails, publish nothing and retain A. Detach B first prevents new choices, migrates or drains existing sockets under policy, waits for callback references, then unpins code. The fallback implementation is independent and resident.

### Answer 4

Start with equation review, fixed-point and overflow tests, event-sequence model tests, deterministic network simulation and coexistence analysis against Reno and CUBIC. Use emulation matrices for bandwidth, RTT, queue size, AQM, ECN, random and burst loss, reordering, ACK delay and compression, reverse-path congestion, path changes and application limitation.

Workloads include short RPCs, sparse requests, long bulk flows, mixed RTTs, many flows, incast, asymmetric paths and nonresponsive cross traffic. Measure goodput, completion-time distribution, standing and p99 queue delay, loss, marking, retransmission, burst, fairness, CPU, callback time and memory. Record offloads, qdisc, NIC, kernel and exact controller generation.

Roll out to opt-in sockets in an isolated namespace, then low-risk host canaries and a bounded fraction of traffic. Compare both selected and competing flows. Abort on explicit latency, loss, fairness, CPU, invalid-sample or fallback thresholds. Keep per-socket selection and immediate known-safe fallback. Expand only after stable observation across representative path regimes.

### Answer 5

Fuzz ACK counts, delivery bytes, intervals, RTT, loss, ECN, flight, MSS and gains at zero, one, maximum and overflow-adjacent values. Inject duplicate delivery, ACK division, compression, reordering, retransmission ambiguity, zero intervals, clock reversal, application limitation, GSO size changes and invalid flags. Assert positive bounded outputs and no double growth.

Measure worst-case callback instructions and duration. Attempt blocking, recursion, forbidden helpers, stale pointers and unbounded allocation; require verifier or interface rejection. Race selection and switching with ACK, timeout, close, CPU migration and detach. Change namespace defaults concurrently and prove existing selection semantics and cross-namespace isolation.

Force initialization, state import, callback and diagnostic-export errors. Return zero, negative-equivalent, maximum and wrapped windows or rates. Confirm the core rejects output, preserves protocol queues, selects an independent fallback, records the generation and eventually releases all private and program references.

Sanitizers, lock/RCU diagnostics, program verification, emulation and canaries prove only their covered executions and constraints. They do not prove Internet fairness, novel-path stability, signal truth on every device, absence of shared model errors or safe interaction with all controllers. State topology, workloads, competing traffic, instrumentation and those limits.
