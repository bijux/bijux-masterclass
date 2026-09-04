---
module_id: OS-099
program: Operating Systems
level: 2
module_number: 99
title: Distributed and Network Operating-System Concepts
status: complete
last_verified: 2026-09-04
---

# Distributed and Network Operating-System Concepts

## One-Page Review

### Governing question

How should operating-system abstractions cross machine boundaries when latency, partial failure, replay, partitions, independent clocks, heterogeneous kernels and administrative domains make a remote resource fundamentally different from a local one?

### Essential definitions

- A **network operating system** exposes communication and remote services while machines remain visibly distinct.
- A **distributed operating system** coordinates multiple machines to present selected system abstractions as one managed environment.
- A **single-system image** makes resources such as processes, files or administration appear unified across nodes.
- **location transparency** lets a client name a resource without encoding its current host; **failure transparency** attempts to mask some failures.
- **remote procedure call** maps a local-looking invocation onto message encoding, transport, server dispatch and reply handling.
- A **stable operation identifier** distinguishes a logical request from retransmissions of that request.
- **at-most-once execution** means a logical operation is applied zero or one times; it does not guarantee completion.
- A **lease** grants time-bounded authority that expires unless renewed under explicit clock and failure assumptions.
- A **fencing token** is a monotonically ordered authority value checked by the resource so an older owner cannot act after replacement.
- An **epoch** identifies one incarnation of a server, membership view or ownership regime.
- **distributed shared memory** presents memory-like access across nodes while a protocol manages placement and coherence.
- A **multikernel** treats cores or nodes as an explicit distributed system and communicates through messages rather than assuming shared kernel state.

### Central model, mechanism, or theorem

A remote OS operation is a replicated state transition, not a transparent function call:

`resolve stable name -> authenticate principal -> obtain epoch/session -> send(op_id, precondition, payload) -> validate authority -> apply or find prior result -> durably record outcome -> reply -> reconcile timeout, retry, cancellation or failover`.

The client may observe a timeout after the server applied the operation but before the reply arrived. Safe retry requires operation identity and retained outcome or an intrinsically idempotent transition. Safe exclusive ownership requires more than failure detection: every side effect must reject stale fencing tokens. Transparency is acceptable only where this uncertainty and the system's recovery semantics remain observable enough for correctness.

### Critical invariants

- Names bind to stable resource identity separately from current location and transport address.
- Every mutating remote request has declared replay, duplicate, cancellation and uncertain-outcome semantics.
- Sessions and duplicate records are scoped by client identity, server epoch and retention lifetime.
- Cached file, memory and metadata state obeys a named consistency and invalidation contract.
- Exclusive owners carry monotonically ordered fencing authority checked at the final resource.
- Process, descriptor, credential and device migration either transfers each dependency or exposes what remains remote.
- Membership, clocks and failure detectors are treated as fallible evidence rather than truth oracles.
- Recovery preserves durable state, identity, authorization and externally visible ordering across node replacement.

### Common failures

Frequent failures are promising local semantics over an unreliable network, identifying resources by address, retrying mutations without stable IDs, calling a timeout a failure, calling an acknowledgment durable without defining the boundary, allowing old owners to write after failover, using leases without clock bounds, hiding cache staleness, migrating a process while leaving untracked dependencies, treating distributed shared memory like uniform RAM, assuming synchronized clocks establish causality, equating node liveness with service correctness, centralizing naming or scheduling without a partition policy, mixing incompatible protocol and kernel versions, delegating credentials without revocation, and declaring a single-system image simpler while its recovery state machine remains implicit.

### Compact example

Client A receives fencing token 41 and writes to shared storage. Its network path stalls. The coordinator expires A's lease and grants client B token 42. Storage accepts B's write and records 42 as the highest token. A later resumes and sends a delayed write with 41; storage rejects it because `41 < 42`. A lease alone could not stop the stale request after A resumed. The monotonic token works only because the side-effecting storage system validates it.

### Connections

Distributed OS concepts connect kernel IPC, network protocols, filesystems, process lifecycle, virtual memory, naming, clocks, authentication, storage fencing, cluster membership, observability, virtualization and distributed-systems consistency.

## Governing Question

Local kernel abstractions rely on shared memory, one failure domain, low-latency calls and authoritative scheduler state. Crossing a network removes those assumptions. A request can arrive twice, a reply can vanish, two nodes can disagree about membership, and an isolated owner can continue issuing device commands.

The governing question is how much distribution the OS should expose or mask. A useful design gives applications stable names and reusable abstractions while preserving the failure distinctions needed to avoid duplicate effects, stale authority, silent inconsistency and unsafe recovery.

## Why This Matters

Remote files, process launch, cluster schedulers, network block devices, disaggregated memory and system-management planes all extend OS responsibilities beyond one kernel. Their failures cross protection and durability boundaries. A hidden retry can charge a payment twice; an unfenced node can corrupt a shared filesystem.

Transparency can reduce application complexity during normal operation. It can also transform an obvious network failure into a long blocked system call or a plausible stale read. Operators need to know which node, epoch, credential, cache and operation produced a result.

The right goal is selective transparency with explicit contracts. Location can often be hidden behind stable naming. Latency and uncertain outcomes usually cannot. Recovery must converge physical resources and logical ownership before service resumes.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain processes, address spaces, descriptors, filesystems and device ownership;
- distinguish messages, streams, RPCs and shared-memory IPC;
- reason about crashes, timeouts, retries, idempotency and durable writes;
- explain cache coherence, consistency and virtual-memory faults;
- distinguish identity, authentication, authorization and delegation.

Retrieve node and failure-domain topology; stable node, boot, client and resource identities; protocol and schema versions; name-service data; session and epoch rules; request IDs and duplicate-retention windows; authentication and authorization mappings; transport settings; RPC timeouts and retransmissions; clock source, uncertainty and monotonic behavior; membership and failure-detector outputs; process and resource placement; migration dependencies; remote mounts, cache and delegation modes; data and metadata durability boundaries; leases and fencing-token enforcement; shared-storage ownership; network partitions and loss; kernel and firmware versions; upgrade compatibility; traces correlated by operation; recovery logs; fault-injection results; and rollback state.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish network, distributed, single-system-image and multikernel designs;
2. explain which local OS assumptions fail across a network;
3. design stable naming independent of location and incarnation;
4. specify RPC retry and uncertain-outcome semantics;
5. reason about remote file, process, memory and device abstractions;
6. prevent stale owners from acting with resource-validated fencing;
7. assess leases, clocks, membership and failure detectors conservatively;
8. design cross-node recovery, observability and compatible upgrades;
9. choose selective transparency by correctness and operational needs;
10. test distributed OS mechanisms under partitions, replay and partial recovery.

## Core Exposition

### Distinguish architectural goals

A network OS makes remote access explicit: log into another host, mount a remote filesystem or call a network service. A distributed OS may unify names, processes, files or administration so placement is less visible.

A single-system image is a property, not one fixed architecture. Systems can unify a namespace while exposing process placement, or unify process management while retaining separate storage. State precisely which abstraction is transparent.

### Preserve stable identity

An IP address, socket or path identifies a current route, not necessarily a durable resource. Reuse after reboot or reassignment can bind old state to a new actor.

Use stable resource IDs plus incarnation or epoch where required. Resolve identity to current location through a versioned naming service. Cache bindings with bounded validity and invalidate them after movement or replacement.

### Treat naming as a consistency problem

A global namespace needs rules for creation, deletion, rename, mount, delegation and concurrent update. Namespace partitions can be autonomous or coordinated, but clients must know which view they observed.

Plan 9 demonstrates a compositional approach in which resources are represented through per-process file namespaces and accessed by a common protocol. Uniform naming reduces interface variety; it does not remove network latency, authentication or server failure.

### Model RPC as messages

RPC stubs encode procedure, arguments and identity into a message; transports deliver requests and replies; a server decodes, authorizes and dispatches. Interface definition and external data representation isolate language and machine ABI differences.

Local calls normally return once or fault synchronously. An RPC can time out while the request is queued, executing, committed or already replied. APIs must surface this uncertainty instead of inventing a reliable call stack.

### Define retry semantics

Read-only or idempotent operations may tolerate replay, but even reads can consume cursors or change audit state. Mutations need a stable operation ID and server-side duplicate detection or an application precondition.

Duplicate caches have retention limits. Scope keys by authenticated client and server epoch, persist them to the required durability level, and say what happens after eviction or restart. At-most-once is different from exactly-once completion.

### Separate acknowledgment from durability

A reply can mean received, accepted, replicated, committed to stable media or externally applied. Clients cannot infer one boundary from another.

Document failure atomicity and recovery. If a client retries after an uncertain commit, the new server must find the prior outcome or reject ambiguity. Downstream side effects need the same operation identity or compensating semantics.

### Make cancellation a protocol

Canceling a local blocked thread can stop waiting without undoing kernel state. Canceling an RPC does not recall a packet or reverse a committed operation.

Represent cancellation as another ordered request with an acknowledgment and race semantics. State whether cancellation prevents start, requests cooperative abort, or only abandons the reply. Preserve the final outcome for reconciliation.

### Design remote process creation

Remote spawn transfers executable identity, arguments, environment, credentials, limits, namespace bindings and placement policy. The launcher must distinguish “not started,” “started with identity,” “exited” and “outcome unknown.”

Return a stable process handle scoped by node incarnation, not a reusable numeric PID alone. Define signal, wait, exit-status, orphan and node-failure behavior.

### Bound process migration

Migration may transfer registers, memory, threads, signals, timers, credentials and scheduler state. Open files, sockets, devices, shared mappings and kernel objects may move, be proxied, be reconnected or block migration.

Quiescing every thread gives a coherent checkpoint but increases pause. Pre-copy reduces pause and can fail to converge under heavy writes. After cutover, fence the source before the destination performs externally visible effects.

### Treat descriptors as capabilities with location

A file descriptor names kernel state in one process table. Moving it across nodes requires a protocol reference, delegated capability or proxy. The remote endpoint can disappear independently of the local integer.

Preserve access mode, offset-sharing, locks, credentials, revocation and close semantics. Do not serialize raw kernel addresses or assume descriptor numbers are globally meaningful.

### Specify remote filesystem consistency

Network filesystems cache data, attributes, directory entries and sometimes write authority. Close-to-open, session, lease, callback and delegation mechanisms trade communication against freshness.

Define when writes become visible, what `fsync` means across client/server/storage layers, how rename and locks behave, and what clients do when callbacks fail or leases expire. Disconnected operation needs explicit conflict semantics.

### Recover stateful file protocols

Stateful protocols track opens, locks, layouts and delegations. Server reboot or failover creates a new epoch and a recovery window in which clients reclaim valid state.

Reclaim must not resurrect revoked or conflicting authority. Stable client identity prevents a rebooted client from impersonating its prior incarnation accidentally. Record recovery success and unresolved state before ordinary I/O resumes.

### Understand distributed shared memory

Distributed shared memory maps remote data into an address-space abstraction and moves pages or objects on faults. A coherence protocol controls ownership, replication and invalidation.

Page granularity creates false sharing when nodes write different words on one page. Network faults can turn an ordinary load into an indefinitely delayed or failed operation. Synchronization and memory-model rules must include protocol messages and node failure.

### Separate shared address from shared truth

Mapping the same virtual range on several nodes does not by itself define consistency. Sequential, release, causal or weaker models permit different observations and optimizations.

Tie publication to explicit synchronization. Recovery after an owner's crash must reconstruct or invalidate dirty state. Never assume hardware cache coherence extends across a network unless the platform provides and specifies it.

### Manage remote devices explicitly

Remote block, GPU, accelerator or sensor access crosses queue, DMA, interrupt and reset boundaries. A client timeout does not prove the device stopped. Device firmware may continue acting after the controlling node is isolated.

Use queue epochs, request IDs and fencing at the device, controller or storage target. Define reset ownership, completion replay, data-buffer lifetime and how a new owner proves the old path cannot issue effects.

### Use leases with clock assumptions

A lease grants authority until a time boundary. The grantor can wait for expiry before reassigning, but safe interpretation requires bounded clock behavior, communication assumptions or server-relative enforcement.

Use monotonic clocks for intervals and account for uncertainty. A client should stop before the grantor might consider authority expired. Clock synchronization improves estimates but does not establish event causality.

### Fence every exclusive side effect

Failure detection can suspect a healthy but partitioned owner. Granting a replacement creates two actors unless the old one's authority is rejected downstream.

Issue monotonically increasing fencing tokens and require the final resource to reject operations older than its highest accepted token. Putting the token only in the coordinator log does not protect a storage device that never checks it.

### Treat membership as a view

Membership services assemble heartbeats, leases, administrative actions and consensus or quorum decisions into a view. During partitions, different nodes may have incomplete observations.

Bind work to a view or epoch. Do not let a local timeout alone authorize destructive recovery. Define quorum loss, minority behavior, rejoin and stale-message rejection.

### Design cluster scheduling conservatively

A distributed scheduler allocates CPUs, memory, devices and placement constraints across nodes. Offers or reservations can become stale before use; concurrent schedulers can overcommit the same resource.

Use versioned allocations, admission at the owning node and reclaim after failed launch. Preserve capacity for system daemons and recovery. Resource availability is not task correctness or data locality.

### Expose topology and locality

Hiding location can simplify naming but prevent applications from controlling network, NUMA, storage and failure-domain costs. Make locality discoverable without making physical addresses permanent identity.

Placement APIs should express preferences and constraints, then report effective placement and movement. Replication across one rack is not failure-domain diversity merely because nodes differ.

### Understand multikernel reasoning

A multikernel models a multicore machine as a network of independent cores communicating with explicit messages and replicated state. This makes topology, ownership and update protocols architectural concerns.

The model can improve scalability reasoning and hardware diversity, but messages inside one machine still require ordering, failure and lifecycle contracts. It is an OS design lens, not proof that all distributed protocols transfer unchanged.

### Support heterogeneity and evolution

Nodes may differ in architecture, byte order, word size, page size, accelerators and kernel capability. External representations must define field sizes, alignment, unknown fields and validation.

Negotiate protocol versions and features. Rolling upgrades create mixed-version periods; test old-new interactions, downgrade resistance and state written by each version. Never deserialize untrusted kernel objects directly.

### Map identity across nodes

Numeric user and group IDs can mean different principals in different domains. Authenticate stable principals and apply explicit mapping at the resource owner.

Delegation should be narrow in resource, action, audience and lifetime. Preserve the initiating principal through proxies for authorization and audit. Revocation must reach cached capabilities and disconnected clients under declared rules.

### Protect distributed kernel surfaces

Kernel network protocols parse attacker-controlled lengths, offsets, handles and state transitions. Validate before allocation or pointer use, cap resource consumption, authenticate peers and separate tenants.

Remote administration and process control deserve stronger isolation than data access. Rate-limit creation, retries and recovery claims so a peer cannot exhaust memory or duplicate tables.

### Observe one logical operation

Assign an operation ID at the first stable boundary and carry it through name resolution, RPC attempts, server dispatch, storage commit and reply. Add node, boot, process, session, epoch and fencing identifiers.

Use monotonic durations locally and clock-uncertainty-aware wall time across nodes. A trace missing one side does not prove the event did not occur. Retain raw retry and duplicate decisions.

### Recover by reconciliation

After partition or restart, compare durable operations, resource epochs, leases, locks, dirty caches and external effects. Reject stale actors before enabling new writes.

Recovery must be idempotent and restartable. Prefer a conservative unavailable state over two writers. Declare completion only when logical ownership, physical fencing, durable data and namespace visibility agree.

### Govern transparency

For each abstraction, decide whether to hide location, migration, replication, concurrency, latency and failure. Make the choice from correctness and operator needs, not aesthetic uniformity.

Expose uncertain outcomes, stale reads, degraded replicas and recovery epochs where applications must react. A smaller honest abstraction often composes better than a perfect local illusion with undocumented exceptions.

## Definitions and Notation

- `op_id`: stable identifier for one logical remote operation and all its retries.
- `client_id`: authenticated stable client identity.
- `boot_id`: identity of one node incarnation.
- `epoch`: ordered identifier for one server, membership or ownership regime.
- `f`: fencing token attached to an exclusive operation.
- `f_max`: highest fencing token accepted by a resource.
- **acceptance rule:** accept an exclusive effect only if its token is at least the resource's required current value under the specified protocol.
- **uncertain outcome:** the client cannot distinguish nonexecution from execution whose reply was lost.
- **duplicate table:** mapping from scoped operation IDs to in-progress or completed outcomes.
- **reclaim:** restoration of valid client protocol state after server restart or failover.
- **proxy:** component that retains a resource locally while forwarding operations for a migrated client.
- **delegation:** time- or recall-bounded authority granted to a client to act or cache without synchronous server checks.
- **view:** named membership configuration against which operations are interpreted.
- **location transparency:** stable access without embedding current placement in the name.
- **failure transparency:** masking a defined set of failures while preserving specified outcomes.

## Mechanisms, Invariants, or Proof Structure

1. **Abstraction claim:** name exactly which local-looking property is exported across nodes.
2. **Identity invariant:** separate stable resource and principal identity from address and incarnation.
3. **Protocol invariant:** version and validate every message and state transition.
4. **Operation invariant:** scope mutation IDs by client and epoch and retain authoritative outcomes.
5. **Durability claim:** define what each acknowledgment proves at server, replica, storage and external-effect boundaries.
6. **Cache invariant:** name consistency, ownership, invalidation and disconnected behavior.
7. **Authority invariant:** final resources reject stale epochs and fencing tokens.
8. **Migration invariant:** transfer, proxy or reject every process, descriptor, memory and device dependency.
9. **Time claim:** state monotonicity, synchronization and uncertainty assumptions for leases and diagnostics.
10. **Membership claim:** bind authority to an agreed view and define partition and rejoin behavior.
11. **Security invariant:** preserve authenticated principal, delegation scope and revocation across proxies.
12. **Recovery invariant:** replay and reconciliation are idempotent and converge durable state with physical ownership.
13. **Observability invariant:** correlate every attempt and outcome by operation, node, boot, session, epoch and token.
14. **Evolution invariant:** mixed versions negotiate features and preserve downgrade-safe state.
15. **Assurance claim:** test replay, partitions, reboot, stale owners, migration and partial recovery independently.

## Alternatives and Trade-Offs

- **Network OS versus distributed OS:** explicit hosts expose failure and placement; unified abstractions reduce routine coordination.
- **Location transparency versus locality control:** stable names ease movement; visible topology enables performance and failure-domain choices.
- **Stateless versus stateful protocol:** stateless requests simplify restart; stateful sessions enable locks, delegation and efficiency.
- **Retry versus surface uncertainty:** retries improve availability; surfacing ambiguity prevents hidden duplicate effects.
- **Idempotent operation versus duplicate table:** idempotency simplifies replay; duplicate records support non-idempotent results and need retention.
- **Lease versus synchronous authorization:** leases reduce coordination; synchronous checks improve revocation freshness.
- **Cache versus freshness:** caching lowers latency and load; invalidation and conflict semantics grow.
- **Migration versus restart:** migration preserves in-memory progress; restart reduces transferred hidden dependencies.
- **Move resource versus proxy it:** moving removes indirection; proxies preserve compatibility and add latency and failure dependence.
- **Distributed shared memory versus messages:** DSM offers familiar access; messages make ownership and failure boundaries explicit.
- **Central scheduler versus distributed admission:** central control simplifies policy; local admission scales and needs stale-allocation handling.
- **Shared storage versus replicated local storage:** shared storage simplifies one data view; replicated storage can isolate failures and adds reconciliation.
- **Synchronized clocks versus logical ordering:** physical time supports leases and audit; logical order better represents causality.
- **Single version versus rolling upgrade:** homogeneous versions simplify reasoning; rolling change preserves availability and creates mixed semantics.
- **Failure masking versus fail-fast:** masking handles transient faults; fail-fast exposes uncertainty before hidden stalls or stale state spread.

## Failure Modes and Misconceptions

1. **“A distributed OS is just a local OS with sockets.”** remote failure changes every blocking state transition.
2. **“Transparency is always simpler.”** hidden latency and uncertainty can make recovery less understandable.
3. **“An address is stable identity.”** addresses are reused and resources move.
4. **“A global path has one current meaning.”** namespace replicas and caches can observe versions.
5. **“RPC has local call semantics.”** requests and replies fail independently.
6. **“A timeout means the server did nothing.”** execution may have committed before reply loss.
7. **“TCP prevents duplicate operations.”** application reconnect and retry can replay logical requests.
8. **“At-most-once means the operation completes.”** zero executions remain permitted.
9. **“Exactly-once is a transport property.”** effects, durable outcome and retry scope must compose.
10. **“Canceling the caller cancels the server.”** cancellation is a separate racing protocol.
11. **“A PID identifies a remote process.”** it needs node incarnation and stable handle context.
12. **“Migration copies memory and is done.”** descriptors, devices, credentials and external effects remain.
13. **“A descriptor integer is portable.”** it indexes local kernel state.
14. **“Remote `fsync` has obvious durability.”** client, server, replicas and devices define distinct boundaries.
15. **“Leases solve stale ownership.”** a partitioned former owner can keep acting unless effects are fenced.
16. **“A coordinator-side token fences storage.”** the final resource must validate it.
17. **“Synchronized clocks prove causality.”** bounded wall-time error does not order all events.
18. **“A heartbeat proves the service is correct.”** a live node can be stalled or corrupt.
19. **“Quorum loss is a reason to pick one writer locally.”** unilateral recovery can create split brain.
20. **“DSM behaves like uniform local RAM.”** faults, false sharing and node loss are observable.
21. **“Single-system image removes topology.”** physical placement still determines latency and failure.
22. **“Resource offers remain accurate until used.”** concurrent change requires owner-side admission.
23. **“Numeric user IDs identify principals globally.”** administrative domains can map them differently.
24. **“A rolling upgrade exercises one protocol.”** old-new pairs and stored states multiply combinations.
25. **“One trace timestamp orders the cluster.”** clock uncertainty and missing events remain.
26. **“Recovery ends when a node reboots.”** fencing, state reconciliation and namespace visibility must converge.

## Worked Examples

### Example 1

A stable service name resolves to a new server after failover. Clients discard cached sessions from the prior epoch rather than sending valid-looking handles to the replacement.

### Example 2

A create request commits and its reply is lost. The client retries with the same `op_id`; the server returns the stored object identity rather than creating another object.

### Example 3

A cancellation reaches the server after an operation commits. The reply reports “too late” with the committed outcome; it does not pretend the client-side wait reversed the effect.

### Example 4

A migrated process retains a socket through a proxy on its source node. Location transparency works until the source fails, so the migration contract records the residual dependency.

### Example 5

Two clients write separate words on one DSM page. Page ownership bounces on every update, demonstrating false sharing even though application data does not conflict.

### Example 6

An NFS client holds delegated write authority while callbacks fail. Lease recovery and recall rules determine when another client can safely receive conflicting access.

### Example 7

Client A with fencing token 41 resumes after B has written with 42. Storage rejects 41, preventing the old owner from corrupting the new epoch.

### Example 8

A central scheduler offers a GPU that fails before launch. Node-side versioned admission rejects the stale offer, and the scheduler resubmits rather than overcommitting a replacement.

### Example 9

During a rolling upgrade, a new node writes an optional field that an old node preserves but ignores. Feature negotiation prevents the new operation from depending on that field until every owner supports it.

### Example 10

Cross-node traces disagree by 30 milliseconds. Operation IDs and local monotonic spans reconstruct request order without claiming wall-clock timestamps establish causality.

## Cross-Program Connections

- **Networking:** framing, loss, congestion, authentication and transport lifecycle carry remote operations.
- **Distributed systems:** consensus, replication, logical time and partitions support OS-wide state.
- **Storage engineering:** durability, cache consistency, fencing and recovery protect shared data.
- **Security engineering:** stable principals, capabilities, delegation, revocation and parser hardening cross nodes.
- **Virtualization:** live migration, virtual devices and remote memory expose similar dependency problems.
- **Programming languages:** interface definitions, serialization and effect semantics shape RPC safety.
- **Concurrency:** operation IDs, epochs and ownership extend local state-machine reasoning across messages.
- **Platform engineering:** cluster scheduling, rollout, topology and observability operationalize the abstractions.
- **Reliability engineering:** fault injection and reconciliation validate partial-failure behavior.
- **Systems engineering:** selective transparency and residual dependencies must trace to stakeholder requirements.

## References

1. Bell Labs, [The Plan 9 Operating System](https://9p.io/sys/doc/9.html), per-process namespaces, file-oriented resources and distributed system structure; retrieved 2026-09-04.
2. Plan 9 Foundation, [Plan 9 Manual Section 5](https://9p.io/sys/man/5/INDEX.html), 9P message, file, authentication and protocol formats; retrieved 2026-09-04.
3. IETF, [RFC 5531: Remote Procedure Call Protocol Version 2](https://www.rfc-editor.org/rfc/rfc5531.html), RPC messages, authentication, transport and reply semantics; retrieved 2026-09-04.
4. IETF, [RFC 8881: Network File System Version 4 Minor Version 1 Protocol](https://www.rfc-editor.org/rfc/rfc8881.html), sessions, state, recovery, leases, callbacks and exactly-once sequencing; retrieved 2026-09-04.
5. IETF, [RFC 7862: Network File System Version 4 Minor Version 2 Protocol](https://www.rfc-editor.org/rfc/rfc7862.html), extension and interoperability of stateful remote filesystem operations; retrieved 2026-09-04.
6. IETF, [RFC 5905: Network Time Protocol Version 4](https://www.rfc-editor.org/rfc/rfc5905.html), clock offset, delay, synchronization and error considerations; retrieved 2026-09-04.
7. Microsoft Research, [The Multikernel: A New OS Architecture for Scalable Multicore Systems](https://www.microsoft.com/en-us/research/publication/the-multikernel-a-new-os-architecture-for-scalable-multicore-systems/), explicit communication and replicated OS state; retrieved 2026-09-04.
8. Linux Kernel Documentation, [NFS](https://docs.kernel.org/filesystems/nfs/index.html), Linux NFS client, server, identifier and protocol documentation; retrieved 2026-09-04.
9. Linux Kernel Documentation, [Network Filesystem Helper Library](https://docs.kernel.org/filesystems/netfs_library.html), buffered I/O, caching, subrequests and network-filesystem integration; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Ceph Distributed File System Client](https://docs.kernel.org/filesystems/ceph.html), kernel client mounting, authentication, caches and recovery options; retrieved 2026-09-04.
11. Linux Kernel Documentation, [The 9P Filesystem Protocol](https://docs.kernel.org/filesystems/9p.html), Linux 9P transports, cache modes, security and mount behavior; retrieved 2026-09-04.

## Exercises

### Exercise 1

Specify a remote process-launch API that remains unambiguous across request loss, reply loss, node reboot, PID reuse, cancellation and client restart. Include identity, outcomes and retention.

### Exercise 2

Simulate two owners of shared storage. Owner A has fencing token 41; owner B receives 42 after A is suspected. Show that B's write is accepted and A's later delayed write is rejected, then state the assumptions.

### Exercise 3

Design migration for a multithreaded process with anonymous memory, a shared mapping, two files, a TCP connection, a local accelerator queue, timers and credentials. Classify every dependency as moved, reconnected, proxied or unsupported.

### Exercise 4

Compare a network filesystem's close-to-open cache policy with strict synchronous visibility for source builds and collaborative document editing. Cover correctness, latency, disconnected behavior and recovery.

### Exercise 5

Construct a validation matrix for a mixed-version cluster OS upgrade. Include RPC replay, server epochs, namespace changes, credentials, caches, leases, partitions, fencing, process recovery and observability.

## Answers to the Exercises

### Answer 1

The client chooses a stable authenticated `client_id` and random `op_id`, then sends executable digest, arguments, credential delegation, limits and placement preconditions. The server records `not_started`, `starting`, `running(process_handle)` or `finished(status)` durably enough for the promised behavior. The handle contains stable node and boot identity plus a nonreused process instance ID; the numeric PID is diagnostic only.

Retries with the same scoped ID return the stored state. A timeout yields `unknown`, never `not_started`. Cancellation is a separate idempotent request whose result is prevented, cooperatively stopping, too late with outcome, or unknown. Duplicate and outcome retention exceeds the documented client retry/recovery window; after expiry the server rejects ambiguous old IDs instead of silently treating them as new. Client restart recovers its stable identity and operation log before issuing new launches.

### Answer 2

The storage target records the highest accepted fencing token. B's token 42 advances that value and its write applies. A's delayed request carries 41, so the target rejects it as stale and leaves B's value intact.

<!-- bijux-verify: {"id":"storage-fencing-token","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"owner_a token=41 result=accepted value=before-partition\nowner_b token=42 result=accepted value=new-owner\nowner_a token=41 result=rejected-stale value=new-owner\nhighest_token=42\n"}} -->
```python
class FencedRegister:
    def __init__(self):
        self.highest_token = 0
        self.value = None

    def write(self, owner, token, value):
        if token < self.highest_token:
            result = "rejected-stale"
        else:
            self.highest_token = token
            self.value = value
            result = "accepted"
        print(f"{owner} token={token} result={result} value={self.value}")


storage = FencedRegister()
storage.write("owner_a", 41, "before-partition")
storage.write("owner_b", 42, "new-owner")
storage.write("owner_a", 41, "delayed-old-owner")
print(f"highest_token={storage.highest_token}")
```

Tokens must be monotonically ordered within the resource's authority domain, cannot be reused after coordinator loss, and must accompany every side effect. The storage target must authenticate requests and preserve the highest accepted token across the failures covered by the guarantee. This toy does not implement consensus, token issuance, durable media, concurrency or a real device protocol.

### Answer 3

Stop all threads at a coherent checkpoint while recording signals and timers. Pre-copy anonymous and eligible shared memory, then transfer final dirty state; reconnect the shared mapping through its distributed owner and preserve its consistency epoch. Reopen files by stable file handles with offsets, locks and credentials, or retain explicit proxies when server semantics do not permit reconstruction. Reconnect the TCP flow only if a transport migration protocol and peer support it; otherwise proxy through the source or mark migration unsupported.

Drain and fence the accelerator queue before cutover. If the device cannot transfer queue state or reject source commands, block migration. Recreate timers against monotonic remaining intervals with documented drift. Delegate narrow credentials to the destination and revoke source authority. Fence all external effects, publish destination identity, then release the source. A proxy leaves source-node availability as a recorded dependency.

### Answer 4

Close-to-open consistency can let one client cache between open and close while checking freshness at later opens. It lowers metadata and data traffic and may support bounded disconnected work, but simultaneous editors can observe stale bases and need conflict detection. Source builds often tolerate cached immutable inputs when generated outputs and rename visibility obey the toolchain's assumptions; strict visibility may be required for shared lock or generated-state coordination.

Collaborative editing should use an application-level operation or version protocol rather than assume filesystem open/close defines merge semantics. Strict synchronous visibility simplifies a narrow read-after-write claim but raises latency and reduces partition availability. For both workloads, specify writeback, `fsync`, rename, lock, callback failure, lease expiry, server reboot, conflict and stale-read reporting. Test packet loss and failover rather than inferring semantics from a local mount.

### Answer 5

Test every supported old/new client-server pair plus state written before, during and after the upgrade. Replay mutations before and after duplicate-record eviction; lose requests and replies; restart servers into new epochs; reuse addresses while preserving stable identity; and exercise namespace create, rename, deletion and stale binding caches. Cross principal mappings, delegation, revocation and downgraded authentication.

Test cached data and metadata, recalls, lease expiry, reclaim, disconnected clients, dirty writes and server failover. Partition owners and coordinators, issue a higher fencing token, then deliver delayed old writes to the final resource. Recover processes with lost launch replies, PID reuse and cancellation races. Verify feature negotiation and downgrade resistance, raw operation correlation by node/boot/session/epoch/token, lost-event indicators, rollback of stored formats and conservative behavior when quorum or compatibility is absent.
