---
module_id: OS-029
program: Operating Systems
level: 1
module_number: 29
title: Local Sockets and Message Queues
status: complete
last_verified: 2026-09-04
---

# Local Sockets and Message Queues

## One-Page Review

### Governing question

How should local processes choose and operate socket or message-queue IPC while preserving framing, peer authority, resource bounds, lifecycle, ordering, backpressure, and failure meaning?

### Essential definitions

- A **local socket** is an endpoint in the local interprocess socket family, commonly called UNIX-domain or `AF_UNIX`.
- A **stream socket** provides an ordered byte stream without message boundaries.
- A **datagram socket** preserves individual datagram boundaries but can reject, truncate, or lose data under interface and resource conditions.
- A **sequenced-packet socket** provides connection-oriented record boundaries and ordered delivery where supported.
- A **POSIX message queue** is a named kernel object containing bounded priority-ordered messages.
- **ancillary data** is control information carried with a socket message, including file descriptors or credentials on supported systems.
- **backpressure** is the producer constraint caused by exhausted receiver, socket, queue, or application capacity.

### Central model, mechanism, or theorem

Model a channel by semantic vector `C=(F,O,R,A,L,B)`: framing `F`, ordering `O`, reliability scope `R`, peer authority `A`, lifetime `L`, and bounds `B`. A design is correct only when application assumptions are no stronger than every component of `C`.

For a message queue with maximum count `K`, maximum message size `S`, and queued messages `Q`, require `0<=|Q|<=K` and `len(m)<=S`. Priority chooses the highest-priority available message; equal-priority ordering follows the applicable contract. Bounded capacity means send can block, time out, or fail, so message ownership must remain explicit until acceptance.

### Critical invariants

- Stream users frame and parse arbitrary partial reads and writes; record users size receive buffers and detect truncation.
- Endpoint discovery and peer credentials authorize the exact operation rather than trusting a pathname or connection alone.
- Passed descriptors are validated as capabilities, use close-on-exec policy, and are closed exactly once on all error paths.
- Queue or socket capacity, per-peer admission, message size, wait time, and retry are bounded.
- Ordering and priority claims specify socket type, producer count, connection, queue, and implementation scope.
- Close, unlink, stale names, fork, exec, restart, half-close, notification, and peer death have defined transitions.
- Acknowledgment distinguishes local API acceptance, peer receipt, application processing, and durable commit.

### Common failures

Common mistakes are assuming streams preserve sends, silently accepting datagram truncation, trusting filesystem permissions as peer identity, leaking received file descriptors, forgetting ancillary-buffer truncation, allowing priority starvation, treating queue notification as one callback per message, retrying an uncertain request without identity, leaving stale pathname sockets, assuming unlink ends existing references, and benchmarking payload copy while ignoring synchronization and operations cost.

### Compact example

A privileged local broker creates a pathname socket in a protected directory, atomically uses close-on-exec flags, validates connecting peer credentials, parses bounded versioned frames, and receives descriptors only with sufficient control space and truncation checks. It validates each descriptor's type and rights before transferring ownership. Per-peer queues enforce byte and request limits; application acknowledgments carry request IDs; shutdown stops admission, drains or rejects work by policy, closes connections, and removes the owned socket name.

### Connections

[OS-026](026-pipes-and-byte-streams.md) supplies stream framing and descriptor lifetime; [OS-027](027-shared-memory.md) contrasts application-owned shared state; [OS-028](028-signals-and-notifications.md) distinguishes notification from queued work.

## Governing Question

Local IPC avoids network routing but does not eliminate protocol design. Streams need framing. Datagram and packet receivers need truncation policy. Named queues have finite count and size. Socket names and queue names need secure creation and cleanup. Peer identity can change across reconnect and restart.

The governing question is how to select semantics deliberately and then close every gap between kernel acceptance and application completion. The answer requires a channel contract, explicit authority, bounded ownership, and failure-aware lifecycle.

## Why This Matters

Local sockets connect daemons, supervisors, desktop components, databases, containers, and language runtimes. They can carry credentials and file descriptors, enabling capability-oriented architecture. Message queues offer bounded records, priorities, and asynchronous producer-consumer decoupling.

These powers create sharp boundaries. Passing a descriptor transfers authority. A public socket path can be replaced or connected by the wrong principal. One high-priority producer can starve ordinary work. A queue can persist after all intended users exit. Oversized ancillary data can be truncated while payload appears valid.

Good IPC contracts support upgrades, overload, restart, and observability—not only the successful send and receive shown in a minimal example.

## Prerequisites and Retrieval

Recall descriptor and process inheritance from [OS-012](012-process-creation-and-program-loading.md), bounded waiting from [OS-015](015-process-states-and-wait-queues.md), pipe framing from [OS-026](026-pipes-and-byte-streams.md), and signal notification from [OS-028](028-signals-and-notifications.md).

Retrieve these distinctions:

- byte streams, datagrams, sequenced packets, and message queues have different framing;
- a filesystem socket entry, a bound socket, a connection, and peer process identity are separate objects;
- transport acceptance, delivery, processing, and durability are separate acknowledgment levels;
- descriptor numbers are process-local while passed open-file descriptions carry authority;
- priority is not fairness and bounded buffering is not durable storage;
- readiness indicates an operation may progress now, not a reservation;
- unlinking a name and destroying all extant references are different lifecycle events.

## Learning Objectives

After this module, you should be able to:

1. compare local stream, datagram, sequenced-packet, socket-pair, and POSIX message-queue semantics;
2. design framing, truncation, ordering, priority, timeout, and acknowledgment contracts;
3. secure endpoint naming and validate peer credentials and passed capabilities;
4. manage descriptors, ancillary data, fork, exec, close, unlink, and restart;
5. reason about bounded backpressure, fairness, notification races, and overload;
6. diagnose partial I/O, peer closure, queue persistence, stale names, and identity change;
7. produce platform-scoped performance and assurance evidence without overclaiming.

## Core Exposition

### Local socket types

Local sockets use the socket interface without an external network path. `SOCK_STREAM` gives connection-oriented bytes. `SOCK_DGRAM` preserves datagrams. `SOCK_SEQPACKET` gives connection-oriented ordered records where supported. `socketpair` creates an already-connected pair, useful before `fork` or for internal component wiring.

Choose type from protocol needs, not familiarity. A stream protocol owns framing. A datagram protocol owns maximum size and truncation. A packet protocol still owns versioning, authentication, resource limits, and application acknowledgment.

### Namespaces and discovery

Pathname sockets appear in the filesystem. Directory traversal permissions, socket entry ownership, mode, `umask`, labels, and race-resistant creation matter. A stale socket entry can survive process death and block a new bind.

Linux abstract socket names do not behave like filesystem paths, automatically disappear with references, and do not use pathname permissions; they are nonportable. Their convenience is not an authorization mechanism. POSIX message queues use names with their own persistence and permission rules.

### Bind, listen, connect, and accept

A server creates a socket, binds a controlled address, listens for a bounded backlog, and repeatedly accepts connections. Atomic nonblocking and close-on-exec creation flags avoid post-creation races in multithreaded programs where supported.

Accept success means a transport peer exists, not that it is authorized or speaks the protocol. Authenticate credentials, negotiate version and limits, and allocate per-peer resources only under admission policy.

### Stream framing

Local stream sends and receives can be partial. Calls do not preserve application record boundaries. Use fixed headers, bounded length prefixes, delimiters with escaping, or another incremental framing scheme.

Parsers reject overflow and lengths above configured limits before allocation. They distinguish incomplete frames, malformed frames, orderly end-of-stream, reset, timeout, and protocol shutdown. Output code retains unsent suffixes exactly once.

### Datagram and packet boundaries

Datagram and sequenced-packet sockets preserve record boundaries, but the receiver must provide adequate payload and ancillary buffers. If a message is larger, APIs can truncate returned data or report flags and original length under specified options.

Treat truncation as a protocol outcome. Never parse a truncated authenticated or structured record as complete. Probe-style reads can race with another consumer; single-owner receive or explicit serialization is easier to reason about.

### Ordering and reliability scope

An ordered local stream orders bytes within one connection. It does not order actions across multiple connections or prove that the peer processed data. Datagram behavior and buffer failure rules differ. Reconnect creates a new ordering domain.

Use request IDs, sequence numbers, epochs, and application acknowledgments when retry or reconnect matters. Define whether duplicate requests are rejected, deduplicated, or idempotently replayed.

### Peer credentials

Local transports can expose peer credentials through platform-specific mechanisms. Linux pathname permissions control who may reach a socket path under local rules, while peer credential interfaces can identify the connected process or sender at a particular boundary.

Credentials are inputs to authorization, not the entire policy. Account for namespaces, privilege transitions, groups, security labels, brokered connections, and process lifecycle. Capture and validate identity at the correct time and bind it to the connection generation.

### Descriptor passing

UNIX-domain sockets can carry file descriptors through ancillary messages. The receiver obtains descriptors referring to open file descriptions, effectively receiving capabilities for files, sockets, devices, shared memory, or other objects.

Allocate enough control space, inspect every control header, detect `MSG_CTRUNC`, bound descriptor count, and close all unexpected or rejected descriptors. Apply close-on-exec atomically when supported. Validate object type, access mode, metadata, seals, and intended protocol before use.

### Ancillary data construction

`sendmsg` and `recvmsg` combine payload vectors, address, and control messages. Control buffers require alignment and length macros; manual pointer arithmetic is error-prone. Payload and ancillary data form one protocol event under the interface's conditions.

A receiver must not assume one expected control item means no extras. Iterate safely, reject malformed lengths and duplicates, and establish ownership before any later failure can leak a received descriptor.

### Half-close and peer termination

Stream `shutdown` can close one direction while retaining the other. Read EOF means the peer will send no more bytes after buffered data drains; it does not say the peer read, processed, or durably stored what this side sent.

A reset, broken-pipe error, or `SIGPIPE`-related outcome changes what can be sent but leaves earlier application acknowledgment uncertain. Protocols define terminal frames, half-close order, timeout, and duplicate handling.

### Backpressure and fairness

Socket buffers and message queues are bounded. Blocking send waits; nonblocking send can return partial progress for streams or unavailability according to type; timed queue operations can expire. Application queues add another bounded layer.

Bound bytes and messages per connection, peer, tenant, and service. Round-robin or deficit scheduling can protect fairness. A global FIFO alone permits one producer to monopolize memory and head-of-line block others.

### POSIX message-queue objects

`mq_open` creates or opens a named queue with maximum message count and size. `mq_send` transfers a whole message with priority or waits according to flags and timeout. `mq_receive` removes the highest-priority oldest applicable message and requires a buffer at least the configured maximum size under the interface contract.

Queue descriptors, open descriptions, names, and kernel objects have separate lifetimes. `mq_close` releases a descriptor; `mq_unlink` removes the name; existing open references can continue. Kernel persistence is not durable storage across reboot.

### Priority and starvation

Priority delivery is useful for urgent control traffic but can starve lower-priority work. It also reorders messages across priorities, so a lower-priority setup message must not be assumed to precede a higher-priority dependent message.

Use a small reviewed priority set, quotas or aging, independent queues, and dependency-aware protocol state. Measure latency by priority under sustained overload rather than only empty-queue behavior.

### Queue notification

`mq_notify` registration is generally one-shot and tied to a transition involving an empty queue under specified conditions. A consumer must register and drain in an order that does not miss work arriving around the transition.

Notification means “inspect the queue,” not “exactly one message arrived.” Drain until unavailable, rearm according to the API, and handle competing receivers and receiver death. A dedicated blocking receiver can be simpler.

### Timeouts and clocks

Timed operations require explicit clock and deadline semantics. Relative retry loops can extend the total bound after interruptions or spurious readiness. Convert service budgets to an absolute deadline and preserve it across retries.

Timeout transfers ownership according to policy: caller retry, durable outbox, rejection, or ambiguous-result resolution. Never silently free a request whose acceptance may already have occurred.

### Fork and exec

Descriptors can be inherited across `fork`; message-queue descriptors may share open-description flags under the platform contract. Unintended inheritance delays endpoint closure and transfers authority. Establish close-on-exec atomically.

After fork, close unused ends in every process. Exec protocols deliberately preserve only descriptors the new image owns, often using a constrained bootstrap channel and explicit descriptor inventory.

### Restart and stale state

A pathname or named queue can outlive its intended server. Startup must distinguish its own stale object from a live or hostile owner. Blind unlink can disrupt another instance or cross a namespace boundary.

Use protected directories, exclusive creation, locks or supervisor ownership, identity metadata, and generation handshakes. Clients reconnect under bounded backoff and reject replies from a prior session epoch.

### Resource accounting

Account for descriptors, connection backlog, socket-buffer memory, pending accepts, queued messages, bytes, ancillary descriptors in flight, application buffers, and per-user queue limits. Privilege may change ceilings but does not remove physical bounds.

Reject before expensive allocation, shed low-value work, and reserve capacity for control paths. Descriptor passing can exhaust receiver tables even when payload bytes are small.

### Observability

Record accepts, authenticated identity, negotiated version, bytes and records, truncation flags, parse failures, queue depth, message priority, wait duration, timeouts, retries, descriptor transfers and closures, EOF, reset, stale cleanup, and generation.

Avoid payload and descriptor-path secrets. Correlate transport calls with request IDs while distinguishing accepted, received, processed, and committed stages.

### Security and assurance

Treat local peers as untrusted unless isolation proves otherwise. Validate all lengths, ancillary headers, credentials, labels, passed objects, queue attributes, and state transitions. Apply least privilege and per-peer quotas.

Safety-relevant IPC needs bounded failure, overload, upgrade, and restart behavior plus independent review. A successful loopback benchmark or toy priority queue does not certify the endpoint, kernel, protocol, or deployment.

## Definitions and Notation

Let channel semantics be `C=(F,O,R,A,L,B)`, covering framing, ordering, reliability scope, authority, lifetime, and resource bounds. Application requirement vector `X` is supportable only when every required property is provided by the channel or a stated higher-layer mechanism.

For a message queue, `K` is maximum message count, `S` maximum message size, and `Q` the ordered multiset of messages `(priority,arrival,id,payload)`. Safety requires `0<=|Q|<=K` and `len(payload)<=S`. Selection is maximal priority then applicable arrival order.

For connection generation `g`, request identifier `r` is unique within a stated scope. Acknowledgment levels are `accepted`, `received`, `processed`, and `committed`; a protocol names exactly which level a response proves.

## Mechanisms, Invariants, or Proof Structure

A reviewable local IPC design follows nine obligations:

1. Select stream, datagram, packet, pair, or queue from an explicit semantic vector.
2. Define framing, maximum sizes, truncation, versioning, ordering, and acknowledgment.
3. Secure naming and bind authenticated peer authority to a connection or queue generation.
4. Validate ancillary data and transfer descriptor ownership without leaks or confused authority.
5. Bound buffers, messages, descriptors, priorities, waits, retries, peers, and tenants.
6. Preserve partial progress and ambiguous outcomes through IDs and idempotency.
7. Define close, half-close, unlink, stale cleanup, fork, exec, restart, and migration.
8. Make notification advisory and drain authoritative state without races.
9. Test failure and overload while labeling portable, platform-specific, and empirical claims.

The executable model demonstrates priority selection and stable order among equal-priority messages under a bounded queue contract.

<!-- bijux-verify: {"id":"toy-priority-queue","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=4\ndelivery=shutdown|alert|batch-a|batch-b\nremaining=0\n","stderr":""}} -->
```python
capacity = 4
messages = []
for arrival, priority, body in [
    (0, 1, "batch-a"),
    (1, 3, "alert"),
    (2, 1, "batch-b"),
    (3, 5, "shutdown"),
]:
    assert len(messages) < capacity
    messages.append((priority, arrival, body))

delivery = []
while messages:
    index = max(range(len(messages)), key=lambda i: (messages[i][0], -messages[i][1]))
    chosen = messages.pop(index)
    delivery.append(chosen[2])

print(f"accepted={len(delivery)}")
print("delivery=" + "|".join(delivery))
print(f"remaining={len(messages)}")
```

The toy uses a sequential list and fixed trusted values. It omits kernel queues, blocking, limits, clocks, processes, notification, permissions, failure, and starvation.

## Alternatives and Trade-Offs

- Stream sockets handle arbitrary byte volume but require framing and partial-I/O state.
- Datagram sockets preserve records but require size and truncation policy.
- Sequenced packets combine connection and records but have narrower portability.
- Socket pairs avoid public names but require ancestry or descriptor transfer.
- Pathname sockets use filesystem controls but need protected creation and stale-entry cleanup.
- Descriptor passing enables least-authority composition but expands validation and leak risk.
- POSIX queues provide bounded priority records but introduce persistent names and priority starvation.
- Blocking operations simplify control flow but can tie up threads and participate in deadlock.
- Shared memory can reduce copying while local sockets improve isolation, framing choices, and capability transfer.

## Failure Modes and Misconceptions

1. **“One stream send is one receive.”** stream call boundaries are not records.
2. **“Datagrams cannot be partial.”** receive buffers and flags can expose truncation.
3. **“Local means trusted.”** peers can cross users, namespaces, or compromised components.
4. **“Socket-path permissions prove current identity.”** connection credentials and lifecycle still matter.
5. **“A received descriptor is safe data.”** it is authority requiring validation and ownership.
6. **“Ignoring `MSG_CTRUNC` is harmless.”** missing control data can invalidate the entire message.
7. **“EOF means the request was processed.”** it only describes the sending direction's transport state.
8. **“Priority preserves global FIFO.”** higher priority deliberately reorders and may starve.
9. **“Queue notification counts messages.”** notification is advisory and often one-shot.
10. **“Close deletes a named queue.”** descriptor close and unlink are separate.
11. **“Unlink disconnects current users.”** open references can outlive the name.
12. **“Readiness reserves capacity.”** another actor can consume the opportunity.
13. **“Retry after reconnect is always safe.”** the old peer may have processed the request.
14. **“Loopback speed decides IPC choice.”** security, lifecycle, overload, and operations also dominate.

## Worked Examples

### Example 1

A stream client sends header and payload in two calls; the server receives half a header, then the remainder plus payload. An incremental bounded parser succeeds while a receive-call parser corrupts framing.

### Example 2

A datagram receiver supplies 1 KiB for a 4 KiB record and ignores truncation. It authenticates and processes a prefix. Correct code rejects the marked truncated record and records the configured maximum mismatch.

### Example 3

A public temporary directory contains a replaced socket entry. A client connects to an attacker. A protected directory, ownership checks, and authenticated peer credentials close the naming gap.

### Example 4

A broker expects one descriptor but its ancillary buffer truncates three. It checks `MSG_CTRUNC`, closes every descriptor actually delivered, rejects the message, and does not interpret the payload.

### Example 5

Urgent messages arrive continuously at priority 5; priority-1 maintenance never runs. Quotas, aging, or a separate control queue supply a bounded fairness policy.

### Example 6

A client times out after sending but before seeing a reply. The server may have committed. The client reconnects with the same request ID and queries or safely deduplicates rather than replaying blindly.

### Example 7

A queue notification fires once while ten messages arrive. The consumer drains all ten, rearms with the required race-aware ordering, then checks again. It does not await nine more notifications.

### Example 8

A server crashes and leaves a pathname entry. Startup validates ownership and supervisor lock before removing it. Blind unlink might delete a live replacement server's endpoint.

### Example 9

A child inherits a listening descriptor across exec and keeps the service address alive. Atomic close-on-exec plus explicit descriptor inventory prevents the authority leak.

### Example 10

A peer half-closes after sending a request. The server reads EOF after the request but can still send its response. Treating read EOF as full connection death loses the valid reply path.

## Cross-Program Connections

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames credentials, names, labels, descriptor capabilities, and confused-deputy risk. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity, overload, observability, and assurance reasoning.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) generalizes acknowledgment levels, epochs, retry, idempotency, and partial failure. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects local framing to versioned request and error contracts.

Within this program, [OS-026](026-pipes-and-byte-streams.md), [OS-027](027-shared-memory.md), [OS-028](028-signals-and-notifications.md), and [OS-030](../ROADMAP.md) support explicit IPC selection.

## References

- Linux man-pages project, [unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html), current page checked 2026-09-04. Local socket types, addresses, permissions, abstract namespace, credentials, descriptors, truncation, and errors.
- Linux man-pages project, [socket(2)](https://man7.org/linux/man-pages/man2/socket.2.html), current page checked 2026-09-04. Endpoint creation, types, atomic flags, errors, and standards.
- Linux man-pages project, [socketpair(2)](https://man7.org/linux/man-pages/man2/socketpair.2.html), current page checked 2026-09-04. Connected pairs, flags, return semantics, portability, and errors.
- Linux man-pages project, [sendmsg(2)](https://man7.org/linux/man-pages/man2/sendmsg.2.html), current page checked 2026-09-04. Message vectors, ancillary data, partial send, flags, SIGPIPE suppression, and errors.
- Linux man-pages project, [recvmsg(2)](https://man7.org/linux/man-pages/man2/recvmsg.2.html), current page checked 2026-09-04. Payload and control receipt, truncation flags, close-on-exec for descriptors, and errors.
- Linux man-pages project, [cmsg(3)](https://man7.org/linux/man-pages/man3/cmsg.3.html), current page checked 2026-09-04. Ancillary-data alignment, sizing, iteration, construction, and examples.
- Linux man-pages project, [mq_overview(7)](https://man7.org/linux/man-pages/man7/mq_overview.7.html), current page checked 2026-09-04. POSIX queue naming, priority, persistence, limits, descriptors, namespaces, and Linux details.
- Linux man-pages project, [mq_open(3)](https://man7.org/linux/man-pages/man3/mq_open.3.html), current page checked 2026-09-04. Creation, attributes, permissions, exclusive open, nonblocking mode, and errors.
- Linux man-pages project, [mq_send(3)](https://man7.org/linux/man-pages/man3/mq_send.3.html), current page checked 2026-09-04. Whole-message sends, priorities, blocking, absolute timeout, limits, and errors.
- Linux man-pages project, [mq_receive(3)](https://man7.org/linux/man-pages/man3/mq_receive.3.html), current page checked 2026-09-04. Priority receive, buffer sizing, blocking, timeout, interruption, and errors.
- Linux man-pages project, [mq_notify(3)](https://man7.org/linux/man-pages/man3/mq_notify.3.html), current page checked 2026-09-04. One-shot registration, empty-queue transitions, competing receivers, notification modes, and races.

## Exercises

### Exercise 1

Choose IPC for a local broker that carries 1 MiB payloads, request metadata, peer identity, and occasional file descriptors. Compare stream, packet, queue, and shared-memory designs.

### Exercise 2

Design a secure descriptor-passing protocol. Cover framing, control buffers, truncation, type and rights validation, close-on-exec, rejection, and ownership transfer.

### Exercise 3

Specify a priority message queue with bounded fairness, notification, timeout, overload, restart, and stale-name cleanup.

### Exercise 4

Design application acknowledgment and retry across local-socket disconnect. Include request IDs, epochs, partial writes, half-close, ambiguous commit, and deduplication.

### Exercise 5

Construct an assurance plan for a privileged local control socket. Cover naming, credentials, namespaces, capabilities, resource exhaustion, upgrades, and evidence.

## Answers to the Exercises

### Answer 1

Use a local stream or sequenced-packet control connection for versioned metadata, peer authentication, request IDs, and descriptor passing. Stream is broadly available but requires incremental framing; sequenced packet preserves records where supported but still caps record size and handles truncation. POSIX queues provide bounded priority records but typical message-size limits and no portable descriptor passing make 1 MiB payloads awkward.

For large payloads, pass a sealed or otherwise constrained shared-memory or file descriptor after validating type, size, access, and generation. The control protocol owns authorization, completion, timeout, and cleanup. Benchmark end-to-end copy, page faults, descriptor overhead, contention, and tail latency; select a fallback for platforms lacking required packet or sealing behavior.

### Answer 2

Define a bounded frame with version, operation, request ID, expected descriptor count, descriptor roles, and metadata. Receive with payload and control buffers sized using platform macros. Iterate all control messages, reject malformed lengths, duplicates, unexpected types, count mismatch, `MSG_CTRUNC`, or payload truncation. Immediately place every received descriptor under an ownership guard.

Apply close-on-exec at receipt where supported. Inspect each descriptor's object type, access mode, metadata, size, seals, and allowed operation; never trust the sender's textual description. On rejection close them all exactly once. On acceptance transfer ownership to named protocol components and acknowledge only the intended processing level. Bound in-flight descriptor count per peer.

### Answer 3

Create exclusively under restrictive permissions with reviewed `mq_maxmsg` and `mq_msgsize`. Use a small priority vocabulary, per-priority admission, and either aging or service quotas so urgent traffic cannot starve maintenance indefinitely. Senders retain ownership until successful whole-message acceptance or resolve timeout under request IDs and retry policy.

A single consumer can block directly or use one-shot notification. In the latter case, register and drain under the API's race-aware sequence, then recheck until empty. Startup validates ownership and a supervisor generation before removing a stale name; shutdown stops admission, drains or rejects under a deadline, closes descriptors, and unlinks only the owned generation. Monitor depth, bytes, age, priority, failures, and system limits.

### Answer 4

Frame each request with connection epoch, stable request ID, operation, length, and idempotency semantics. Preserve exact partial-write progress on one connection. A response states whether it proves receipt, processing, or durable commit. Read EOF and reset do not by themselves reveal the last completed level.

After disconnect, reconnect into a new epoch and query the prior request ID or resend only through server deduplication or an idempotent operation. The server retains outcomes for a stated window and binds identity to both sessions. Half-close indicates no more request bytes while permitting response bytes. Absolute deadlines bound resolution; unresolved non-idempotent requests return an explicit ambiguous result rather than silent replay.

### Answer 5

Place the pathname in a protected service-owned directory, create with atomic close-on-exec behavior, verify stale cleanup through supervisor ownership, and reject abstract namespace use if filesystem permissions are required. Authenticate peer credentials and security labels under namespace-aware policy; authorize every operation. Treat received descriptors as capabilities and validate and bound them.

Fault tests cover path replacement, wrong user, namespace confusion, malformed and oversized frames, ancillary truncation, descriptor exhaustion, slow peers, full buffers, restart, upgrade, half-close, and ambiguous requests. Preserve kernel, mount, namespace, policy, workload, and raw evidence. Named IPC, OS, security, operations, performance, safety, and independent-verification reviewers assess residual risk. A local transport alone is not an authentication or certification claim.
