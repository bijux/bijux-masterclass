---
module_id: SARCH-096
program: Software Engineering: Software Architecture
level: 2
module_number: 96
title: Architecture for Offline and Intermittently Connected Systems
status: complete
last_verified: 2026-09-06
---

# Architecture for Offline and Intermittently Connected Systems

## One-Page Review

### Governing question

How can a system keep useful local authority during hours or months without a reliable network, then exchange and reconcile work without inventing a global order, duplicating effects, concealing conflict, or violating safety and business invariants?

### Essential definitions

- **offline operation** is useful work performed without a currently reachable coordinating service; **intermittent connectivity** alternates connected and disconnected intervals with uncertain duration, capacity, and direction;
- a **local authority** is the component allowed to commit a declared class of decision while disconnected; a local replica is not necessarily authoritative for every decision;
- a **sync unit** is a durably identified operation or state fragment exchanged and acknowledged as one retryable item;
- **causal order** records that one event could have influenced another; **concurrency** means neither event is known to precede the other;
- **reconciliation** gives concurrent or disputed work domain meaning; **convergence** only means replicas eventually reach equal state under stated assumptions;
- an **escrow right** is a bounded portion of a global resource that a replica may consume without coordination;
- a **tombstone** is retained deletion evidence that prevents older state from resurrecting an item;
- a **sync epoch** fences an obsolete replica, credential, schema family, or authority grant;
- **local durability** means an accepted local action survives declared local faults; it does not mean a server has accepted it;
- **anti-entropy** compares replicas and exchanges missing information until they agree, assuming communication eventually recurs.

### Central model, mechanism, or theorem

An offline contract is

$$
O=(A,L,S,C,Q,U,P,E),
$$

where $A$ is local authority, $L$ local durability, $S$ synchronization protocol, $C$ conflict semantics, $Q$ capacity and quotas, $U$ user-visible states, $P$ security and privacy policy, and $E$ evolution rules. If any component is implicit, a network outage exposes accidental behavior.

For a local production rate $\lambda$ sync units/s, mean durable size $s$ bytes, and maximum planned isolation $T$, the raw lower bound is $B_{raw}=\lambda sT$. If reconnect service rate is $\mu>\lambda$ and backlog is $b$, idealized drain time is $t_d=b/(\mu-\lambda)$. When $\mu\le\lambda$, backlog cannot drain while production continues. Indexes, logs, encryption, compaction, bursts, failed uploads, and safety reserve make both equations optimistic.

For state-based replicas with merge $\sqcup$, duplicate, reordered exchange converges when merge is associative, commutative, and idempotent and every update eventually reaches every live replica. These algebraic properties prove replica convergence, not domain validity: two replicas can converge on an inventory count below zero unless the data type or authority allocation preserves the inventory invariant.

### Critical invariants

- every locally accepted action has stable identity, actor, device, authority epoch, schema, causal context, and durability outcome;
- the interface distinguishes local acceptance, pending exchange, remote acceptance, rejection, conflict, and final domain outcome;
- retry is idempotent at the declared sync-unit scope, while genuine repeated user intent remains distinguishable;
- clocks support display and bounded expiry only under explicit uncertainty; wall time never substitutes for causal order;
- commutative updates merge automatically only when their domain meaning also composes;
- invariant-sensitive work uses allocated rights, a single authority, reservation, or later human adjudication rather than blind last-writer-wins;
- deletion, consent withdrawal, credential revocation, and policy epochs are reconciled before ordinary stale work;
- a replica cannot silently resume after its supported schema, credential, retention horizon, or authority lease has expired;
- storage exhaustion has a defined admission and evidence-preservation policy;
- synchronization can resume after interruption and never interprets transport acknowledgement as business acceptance;
- every conflict has an owner, visible state, preserved evidence, and bounded resolution path;
- recovery and upgrade retain unsynchronized work or explicitly disclose its loss.

### Common failures

Common failures include treating a response cache as offline architecture; displaying “saved” before local durable commit; using device timestamps as last-writer authority; generating a new operation ID on every retry; applying a generic CRDT to a non-mergeable business rule; selling the same last item at two disconnected sites; hiding server rejection after optimistic UI; accepting an offline payment without a bounded risk grant; losing tombstones during compaction; relying on remote wipe for a stolen offline device; requiring online identity bootstrap after a cold restart; filling disk with bulk attachments before audit records; upgrading schema while old clients still emit legacy operations; reconnecting an entire fleet at once; and declaring success when replicas match but real-world effects disagree.

### Compact example

A field team records 40 inspections/hour, each averaging 30 KB including evidence, and must work for 72 hours. The raw bound is $40/3600\cdot30{,}000\cdot259{,}200=86.4$ MB. The design reserves 200 MB for work plus journal and indexes, stores each inspection transactionally with a stable ID, shows “saved on this device,” rejects new photographs before essential text when reserve is low, and uploads resumable content-addressed chunks. Server validation may accept, reject, or require review; transport success alone never changes the inspection to accepted.

### Connections

[SARCH-051](051-partial-failure-as-an-architectural-constraint.md) establishes ambiguous distributed outcomes, [SARCH-052](052-consistency-and-availability-trade-offs.md) establishes consistency trade-offs, [SARCH-059](059-edge-and-hybrid-architectures.md) allocates edge and physical control, [SARCH-073](073-versioned-contracts-and-compatibility.md) governs mixed versions, and [SARCH-076](076-data-migration-architecture.md) supplies reconciliation discipline. [SARCH-097](../ROADMAP.md) next addresses long-lived scientific systems. Distributed Systems owns replication algorithms in depth; this chapter owns the architectural contract that makes disconnected work safe and intelligible.

## Governing Question

Connectivity is not a Boolean infrastructure property. A device may receive but not send, resolve a name but not complete authentication, exchange small messages but not attachments, or reconnect briefly after weeks away. A request timeout cannot tell whether the server committed an operation. A cold device may lack current time, credentials, configuration, or enough local state to start.

The architectural problem is therefore not “add synchronization.” It is to decide which work may proceed, what local commitment means, how identity and causality survive retry, which concurrent work composes, how scarce rights remain bounded, what the person sees, and when an old replica must stop. The goal is useful autonomy with honest limits.

## Why This Matters

Offline systems support disaster response, aviation, shipping, mines, clinics, farms, warehouses, retail, field maintenance, and ordinary mobile work. In these settings an unavailable screen can halt physical work, but unsafe autonomy can sell unavailable inventory, issue incompatible treatment, disclose private records, or execute a revoked command.

Disconnected work creates multiple legitimate histories. Reconnection does not make one history retrospectively false. Architecture must preserve enough intent and provenance to merge compatible histories, reject invalid work, and route irreducible disputes to accountable people. Coda demonstrated deliberate disconnected operation in a file system, while Bayou exposed application-specific dependency checks and merge procedures for weak connectivity [1], [2]. Local-first work later emphasized immediate local interaction and user control, but those ideals do not remove business authority, security, or lifecycle constraints [5].

## Prerequisites and Retrieval

Retrieve replica, operation log, snapshot, transaction, durable commit, idempotency, deduplication, causal order, version vector, conflict, merge, commutativity, associativity, idempotence, invariant, escrow, lease, epoch, tombstone, anti-entropy, backpressure, retention, checkpoint, schema compatibility, encryption, revocation, attestation, recovery point objective, and user-visible state.

From SARCH-044 retrieve messaging semantics; SARCH-047 supplies cache boundaries; SARCH-051 supplies partial failure; SARCH-052 supplies consistency; SARCH-053 supplies data placement; SARCH-057 supplies queue capacity; SARCH-059 supplies device and site topology; SARCH-073 supplies versioned contracts; and SARCH-076 supplies movement, reconciliation, and cutover evidence.

## Learning Objectives

After completing this module, you should be able to:

1. define an explicit offline contract and distinguish cache, replica, and local authority;
2. model local commit, synchronization, acceptance, conflict, and real-world outcome separately;
3. select operation, state, or hybrid synchronization with stable identity and causal context;
4. prove convergence conditions for a simple merge without confusing convergence with validity;
5. allocate scarce rights so disconnected actions preserve a global bound;
6. size local retention and reconnect drain while stating model limits;
7. design user-visible pending, rejected, and conflicted states;
8. preserve security, privacy, deletion, and revocation under long disconnection;
9. evolve schemas and protocols across replicas that skip many releases;
10. test cold start, long partition, retry, conflict, exhaustion, compromise, recovery, and reconnection.

## Core Exposition

**Start with the offline contract.** Inventory every action and query. For each action, state whether it is available disconnected, the local authority that may accept it, what is durably recorded, which invariants must hold immediately, what remote validation remains, maximum isolation, maximum pending age, rejection behavior, and final owner. For each query, state the data version, freshness evidence, and whether it is authoritative, advisory, or merely cached.

A read cache that displays old catalog data is not an offline write architecture. A full local replica still grants no authority unless policy says its decisions count. Conversely, a device can have narrow authority without a full replica—for example, consuming ten preallocated voucher numbers. Separate data presence from decision rights.

**Define commitment vocabulary.** “Saved” is dangerously overloaded. A local transaction may be durable on one device but not backed up. A sync gateway may durably receive bytes but reject the business action. A server may accept an action but a later physical effect may fail. Name states such as editing, locally committed, queued, transmitting, server received, accepted, rejected, conflicted, superseded, and externally completed.

Expose the state relevant to the user’s decision. A technician leaving a remote site must know whether evidence exists only on one tablet. A cashier must know whether a payment is finally authorized or only accepted under a local risk limit. Do not turn eventual consistency into eventual surprise.

**Make local durability real.** Store an accepted operation and its queue metadata in one local transaction where practical. A UI confirmation before durable commit creates phantom work after process or power failure. The local store needs integrity checking, crash recovery, encryption appropriate to the threat, and tested backup or device-to-device transfer where the loss model requires it.

SQLite currently documents serializable transactions by serialized writes and snapshot isolation in WAL mode; it also warns that a WAL file is part of persistent state and must stay with the database when copied [10], [11]. Those are implementation facts checked 2026-09-06, not a universal endorsement. The architecture must record the actual engine, journal mode, filesystem, sync policy, device guarantees, and tested failure envelope.

**Give every sync unit durable identity.** Generate identity before local commit and retain it across transport retries. RFC 9562, published May 2024, defines current UUID formats and obsoletes RFC 4122 [8]. UUIDs can supply decentralized identifiers, but uniqueness probability or construction does not define business idempotency. Scope identity to a declared intent such as `submit-inspection`, not an arbitrary HTTP attempt.

Record actor and device identity, authority epoch, operation kind, target identity, schema version, causal context, payload digest, local sequence, local commit evidence, and dependencies. A repeated operation ID is a transport replay; two distinct IDs may still represent an accidental double click and need product-level prevention. Deduplication retention must exceed the maximum supported replay age or an old retry can become new again.

**Choose operation, state, or hybrid exchange.** Operation synchronization preserves intent and can be compact, but receivers must understand historical operations and required order. State synchronization can recover from lost intermediate messages and works well with mergeable state, but can send more data and hide intent. A hybrid commonly exchanges operation logs while recent, then a versioned snapshot plus causal summary after compaction.

The choice depends on audit, privacy, schema evolution, bandwidth, and conflict semantics. A medical correction may require immutable intent history. A large derived thumbnail can be regenerated from content-addressed source. Never compact away information still needed to reject replay, propagate deletion, explain a decision, or support an old replica within the promised horizon.

**Synchronize as a resumable protocol.** A robust session authenticates both sides, negotiates protocol and schema, exchanges replica identity and epochs, communicates causal or sequence summaries, transfers bounded batches, verifies content, applies idempotently, returns per-unit business outcomes, downloads missing work, and checkpoints only durable progress. Attachment chunks and metadata may have different priority and retry units.

Treat each acknowledgement precisely. TCP receipt is not durable storage; durable inbox receipt is not schema validation; schema validation is not business acceptance; business acceptance is not external completion. Resume from the last mutually evidenced checkpoint after interruption. Rate limit and randomize reconnect so a fleet does not overwhelm its service after a regional outage.

**Represent causality instead of trusting clocks.** If operation $y$ was created after observing $x$, then $x\rightarrow y$. Device wall times cannot establish this relation reliably because clocks drift, reset, and can be changed. Per-replica sequence numbers and version vectors represent partial order; compact dotted or bounded summaries trade precision and metadata.

Wall time remains useful for display, physical event analysis, retention, and expiry under stated uncertainty. RFC 3339 timestamp syntax is updated by RFC 9557 for additional time information [9]. A serialized timestamp still does not prove clock accuracy. Preserve device time, offset or zone when meaningful, clock source, uncertainty, local monotonic duration where available, and server receipt time rather than collapsing them into one “timestamp.”

**Classify concurrent work by semantics.** Some operations commute: adding two independently identified observations can preserve both. Some state has a deterministic merge: a grow-only set can use union. Some conflicts are resolvable with application semantics: a calendar may preserve both proposals and request a choice. Some cannot be auto-merged safely: allocating the same serial number, approving incompatible medication, or consuming the final item.

Last-writer-wins is a policy, not a law. With unsynchronized clocks it may choose the wrong “last” writer; even with trusted ordering it discards intent. Use it only where loss is acceptable and the winner order is defined. Field-wise merge can construct a combination no person ever reviewed. Preserve concurrent versions and route them when the domain cannot justify an automatic result.

**Use algebra carefully.** A state-based CRDT merge is designed so delivery duplication and order do not affect the final result. Associativity lets grouping vary, commutativity lets order vary, and idempotence makes duplicates harmless [4]. Operation-based CRDTs need different delivery assumptions, often causal delivery or commutative concurrent operations.

Strong eventual consistency says replicas that have received the same updates reach equivalent state. It does not say the state is authorized, safe, private, understandable, compact, or free of malicious input. A set union converges even if an attacker inserted a forbidden member. Validate identity, authority, schema, and domain invariants before admitting an update to the merge domain.

**Preserve global bounds with rights.** A disconnected replica cannot ask whether another replica consumed the same scarce resource. Allocate non-overlapping rights before separation: units of inventory, voucher ranges, monetary risk capacity, reservation slots, or energy budgets. A local transaction may consume only its current rights; transfer of rights is itself a coordinated, auditable operation.

If total rights never exceed global capacity and consumption cannot exceed locally held rights, disconnected consumption preserves the global upper bound. The cost is stranded capacity: one site may reject work while another holds unused rights. Emergency override must be a separately authorized and observable policy, not silent negative inventory.

**Separate reversible and irreversible effects.** Editing a draft can be reconciled. Dispensing medicine, opening a gate, charging a card, or promising inventory may not be undone by a database merge. For each offline action state the external effect, compensation limits, evidence, risk owner, and whether local authority is adequate.

Use bounded grants, offline-capable secure devices, deferred execution, or explicit manual procedure where appropriate. “We will resolve it later” is not a control for irreversible harm. Reconciliation must compare digital histories with receipts, sensors, people, and partner records when the real world can diverge.

**Budget storage and admission.** Size operation log, current state, tombstones, indexes, journal, attachments, encryption overhead, diagnostics, upgrade reserve, and emergency evidence. Model ordinary and burst rates, longest isolation, largest item, compaction, media endurance, and corruption reserve. Monitor time-to-full at current rate.

Define degradation order. Preserve safety events, authority evidence, pending business work, and deletion/revocation metadata before replaceable caches or media. Reject an operation before pretending to save it. Let users export or transfer critical pending work through an authorized path. Never compact solely by age when a replica may legally return after a longer interval.

**Plan drain and backpressure.** New work continues when connectivity returns. If useful upload capacity does not exceed new production, old backlog grows. Reserve bandwidth for policy, revocation, outcomes, and interactive work before bulk history. Use resumable batches, checksums, prioritization, adaptive concurrency, server admission control, and fleet jitter.

The simple $b/(\mu-\lambda)$ model assumes constant rates and no failures. Real plans include handshake cost, retries, downloads, validation, conflict work, radio energy, server write amplification, and peak concurrency. Measure production-shaped workloads and specify a maximum recovery objective for pending work.

**Make conflict a first-class workflow.** A conflict record retains all contenders, causal context, relevant prior state, policy version, detection reason, risk, owner, deadline, and resolution operation. Resolution is new auditable intent, not an in-place erasure. Replicas must later learn that a candidate was accepted, transformed, rejected, or superseded.

Design for people who may be offline too. A conflict queue needs triage, privacy boundaries, bulk safety, escalation, and metrics. Some outcomes can be accepted with a warning; some require a supervisor; some demand suspension of further local authority. Track conflict age and recurrence, not only count.

**Reconcile user experience with truth.** Optimistic interaction should not misrepresent authority. Show local and shared state separately when it changes decisions. Preserve edits after server rejection and explain a repair path. Avoid endlessly spinning “syncing” indicators that conceal a permanent schema or authorization failure.

Conflict presentation should use domain language. “Your dosage conflicts with a newer prescription” is more actionable than “HTTP 409.” Accessibility and translation must work offline. Ensure status, error help, and critical policy are packaged locally, and test screen-reader and low-power behavior without network dependencies.

**Secure an offline replica as a data-bearing authority.** Minimize locally stored data, encrypt under a key custody model, use scoped device and user credentials, lock sensitive operations, and preserve tamper-evident evidence where warranted. NIST SP 800-124 Rev. 2, current final publication checked 2026-09-06, covers mobile-device lifecycle, centralized management, endpoint protection, encryption, and disposal [7]. Apply its controls according to risk rather than assuming a managed device remains online.

Remote wipe and rapid revocation may not reach a stolen device. Limit credential lifetime and local capability while balancing mission duration; bind sensitive data to device protection; require renewed presence or supervision for high-risk action; and enforce server-side epoch rejection on reconnect. A device can continue only the authority intentionally cached for its isolation contract.

**Order security-critical reconciliation.** On reconnect, authenticate current device identity and compare device, user, authority, consent, deletion, and policy epochs before admitting ordinary operations. A revoked device may be allowed to upload encrypted recovery evidence without regaining normal read or command authority. A deletion tombstone must dominate older replicated content according to the declared policy.

Security policy itself can conflict with availability. A credential that expires after eight hours cannot support a seven-day mission unless there is bounded offline renewal, preauthorization, or a manual fallback. Extending all credentials to seven days enlarges theft exposure. Record the trade-off, high-risk exceptions, and containment boundary.

**Evolve across skipped releases.** A replica may return after dozens of server deployments. Define a supported offline horizon and protocol compatibility matrix. Prefer tolerant readers, explicit versions, stable identifiers, and additive evolution before retirement. An old operation can be translated only if its original semantics remain known.

Schema migration must preserve pending work. Upgrade local storage transactionally or retain a verified rollback/forward-repair path. Test old-client/new-server, new-client/old-server where applicable, interrupted upgrade, full disk, corrupted journal, and operation replay after transformation. Beyond the supported horizon, quarantine and export evidence rather than guessing.

**Bootstrap without hidden online dependencies.** Test power loss and cold start while disconnected. The device needs local trust roots, usable identity, protected keys, compatible configuration, schema, time policy, essential reference data, and recovery instructions. A warm process surviving network loss is weak evidence for a device rebooted in the field.

Activation and first login may legitimately require connectivity, but state that constraint. For mission systems, provision and exercise offline accounts and emergency roles before departure. Prevent stale images from silently cloning replica identity or restoring already-consumed rights.

**Observe local and fleet state.** Locally record replica and boot epoch, software/schema/protocol version, last successful sync, causal frontier, pending units and bytes by priority, oldest age, dedup horizon, tombstones, conflicts, rejections, storage reserve, clock status, credential and policy expiry, retries, and integrity results.

Fleet views must distinguish silence, declared disconnection, power loss, retirement, and compromise; absence of telemetry is not health. Measure acceptance latency separately from transfer latency. Sample payloads only under privacy rules and prefer metadata and invariant evidence where content would be excessive.

**Test histories, not happy-path requests.** Generate concurrent operations, duplicate and reorder delivery, truncate sessions, reset clocks, reuse stale images, fill disk, crash around commit, corrupt queue metadata, revoke credentials, delete data, skip versions, restore backup, reconnect a fleet, and fail midway through conflict resolution. Assert user-visible states and domain invariants after every prefix of the history.

Model-based and property-based tests can check merge algebra, deduplication, rights conservation, and convergence. Deterministic simulations explore many schedules; device tests expose filesystem, power, radio, and secure-storage behavior. Field exercises expose human workarounds. Each evidence type supports only its tested environment and assumptions.

## Definitions and Notation

Let:

- $R$ be the set of replicas and $r\in R$ one replica;
- $o=(id,actor,r,e,k,p,c,v)$ be a sync operation with stable identity, actor, replica, authority epoch, kind, payload, causal context, and schema version;
- $x\rightarrow y$ mean operation $x$ causally precedes operation $y$;
- $x\parallel y$ mean $x$ and $y$ are concurrent;
- $\sqcup$ be a deterministic state merge;
- $X_r$ be replica $r$'s current mergeable state;
- $Q$ be a globally bounded resource and $q_r$ rights held by replica $r$;
- $u_r$ be resource units consumed locally at $r$;
- $\lambda$ be local sync-unit production rate and $s$ mean durable bytes/unit;
- $T$ be the planned disconnected duration;
- $b$ be backlog bytes or units at reconnect, consistently measured;
- $\mu$ be sustained reconnect processing rate in the same units as $\lambda$;
- $H$ be the maximum supported replay and offline horizon;
- $e$ be the current authority or synchronization epoch.

A version vector $V_r$ maps replica identity to the greatest contiguous sequence observed from that replica. $V_x\le V_y$ component-wise means $y$ includes every event summarized by $x$. Incomparable vectors imply possible concurrency, not necessarily a business conflict.

## Mechanisms, Invariants, or Proof Structure

**State convergence proposition.** Suppose merge $\sqcup$ is associative, commutative, and idempotent; every local state evolves monotonically in the merge order; and every update from a live replica is eventually delivered to every other live replica. Then replicas that have received the same updates converge. Associativity removes grouping dependence, commutativity removes delivery-order dependence, and idempotence removes duplicate dependence. The eventual-delivery premise supplies the same update set. This is a proof sketch of convergence, not of authorization or domain validity [4].

**Rights-conservation proof.** Assume initially $\sum_{r\in R}q_r\le Q$. A local consumption is admitted only when $0\le u_r\le q_r$ and atomically replaces $q_r$ by $q_r-u_r$. A transfer of $d$ rights atomically subtracts $d$ from one replica and adds $d$ to another, preserving the sum. Therefore cumulative admitted consumption plus remaining rights never exceeds $Q$. The proof fails if a backup clones rights, transfer can be applied twice, or emergency override bypasses accounting.

**Capacity derivation.** Raw production over isolation is $B_{raw}=\lambda sT$. At reconnect, idealized backlog rate is $db/dt=\lambda-\mu$. For $\mu>\lambda$, integration from $b(0)=b_0$ to zero gives $t_d=b_0/(\mu-\lambda)$. When $\mu\le\lambda$, the derivative is nonnegative and backlog cannot clear under continuing production. Bursts, metadata, retry, compression variability, downloads, and validation require measured margin.

**Executable admission model.** The following finite model classifies an incoming offline operation. Its rule order deliberately fences revoked epochs before deduplication, then checks schema, stable identity, local rights, and domain conflict. It demonstrates six outcomes; production systems need durable atomic storage, authentication, concurrency control, and richer policy.

<!-- bijux-verify: {"id":"classify-offline-operation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"stale-epoch\nduplicate\nunsupported-schema\nrights-exhausted\nneeds-review\naccepted\nremaining-rights=3\n","stderr":""}} -->
```python
def classify(op, *, epoch, seen, schemas, rights):
    if op["epoch"] != epoch:
        return "stale-epoch"
    if op["id"] in seen:
        return "duplicate"
    if op["schema"] not in schemas:
        return "unsupported-schema"
    if op["kind"] == "allocate" and op["units"] > rights["units"]:
        return "rights-exhausted"
    if op["concurrent_exclusive_change"]:
        return "needs-review"
    seen.add(op["id"])
    if op["kind"] == "allocate":
        rights["units"] -= op["units"]
    return "accepted"

base = {
    "id": "op-1", "epoch": 7, "schema": 3, "kind": "note",
    "units": 0, "concurrent_exclusive_change": False,
}
seen = {"already-seen"}
rights = {"units": 5}
cases = [
    base | {"epoch": 6},
    base | {"id": "already-seen"},
    base | {"schema": 1},
    base | {"kind": "allocate", "units": 6},
    base | {"concurrent_exclusive_change": True},
    base | {"kind": "allocate", "units": 2},
]
for case in cases:
    print(classify(case, epoch=7, seen=seen, schemas={2, 3}, rights=rights))
print(f"remaining-rights={rights['units']}")
```

**Sync checkpoint invariant.** A sender may discard or compact operation $o$ only after retention policy and durable evidence establish that every required receiver can recover its effect from either acknowledged operation history or a causally covering snapshot. A transport acknowledgement alone is insufficient. This invariant couples compaction, replay horizon, offline support promise, backup, and replica retirement.

## Alternatives and Trade-Offs

**Online-only, cache-assisted, and offline-authoritative.** Online-only minimizes divergent authority and local sensitive data, but halts work. Cache-assisted reads improve availability without accepting writes. Offline-authoritative systems maximize autonomy but require local durability, reconciliation, security, and honest pending states. Different actions in one product can choose different points.

**Single writer, leader per object, and multi-writer.** A single reachable writer simplifies invariants but defeats disconnected writes. Preassigned ownership lets one replica edit an object during an epoch, reducing conflicts but limiting collaboration and requiring handoff. Multi-writer improves autonomy and requires causal metadata plus domain-specific merge or adjudication.

**Operation logs versus state merge.** Logs preserve intent and audit but grow, expose historic schema, and need ordering and compaction. State merge tolerates missing intermediate transfers and can be algebraically robust, but may carry large payloads and erase why. Hybrid snapshots plus retained recent operations balance recovery and explainability at a more complex boundary.

**CRDT versus application conflict workflow.** CRDTs are excellent where a data type’s merge matches domain meaning. A grow-only observation set or increment-only counter is natural. Exclusive decisions and scarce resources need rights, coordination, or review. A deterministic winner is cheap but may be semantically destructive.

**Long grants versus frequent renewal.** Long-lived credentials, policy, and rights support longer missions but enlarge theft and staleness exposure. Short grants contain risk but can strand legitimate users. Risk-tiered capabilities, protected keys, local supervision, and emergency procedure are often better than one universal duration.

**Immediate media upload versus deferred evidence.** Immediate upload reduces single-device loss when bandwidth exists. Deferred, resumable upload protects interactive traffic and power. Content-addressed chunks deduplicate and resume but reveal equality patterns unless designed carefully. Text and safety evidence may deserve priority over replaceable high-resolution media.

**Automatic resolution versus human adjudication.** Automatic merge reduces delay and workload when semantics are sound. Human review handles context but creates queues, privacy exposure, inconsistency, and delay. Systems should minimize irreducible conflicts through authority design, then support the remaining queue as a real operational capability.

## Failure Modes and Misconceptions

- **“Offline means cache the API.”** Cached reads neither provide local write authority nor durable intent.
- **“A green check means synchronized.”** It may mean only local commit or byte receipt; label the exact outcome.
- **“Exactly once prevents duplicate business actions.”** Retry identity can deduplicate one intent, but two independently created intents remain two.
- **“Latest timestamp wins.”** Device time may be wrong, and later time does not imply legitimate authority.
- **“A CRDT resolves conflict.”** It resolves a convergence problem under a particular data type; domain disagreement can remain.
- **“All fields can merge independently.”** Field-wise winners can create an invalid combination never authored together.
- **“Eventual consistency eventually succeeds.”** Delivery can reveal permanent authorization, schema, or invariant rejection.
- **“The cloud copy backs up the device.”** Unsynchronized work exists only locally; recovery point and transfer must be explicit.
- **“Remote wipe protects a lost offline device.”** It may never arrive; minimize data and scope authority before loss.
- **“Expired credentials can simply fail closed.”** That may violate the mission availability requirement; design bounded offline authority deliberately.
- **“More retention is always safer.”** It increases privacy exposure and storage pressure; retain causal and legal evidence under explicit horizons.
- **“Compaction is internal.”** It can destroy tombstones, deduplication, audit, or support for returning replicas.
- **“Warm offline tests prove resilience.”** Cold start can require unavailable identity, time, configuration, keys, or migration.
- **“Reconnect restores order.”** Reconnect creates load and exposes divergent histories; it does not manufacture a global past.
- **“Equal replicas mean correct reality.”** Both replicas can agree on a state inconsistent with inventory, a physical act, or an external partner.

## Worked Examples

### Example 1

**Concurrent note edits without silent loss.**

Two clinicians edit different sentences of the same discharge note while disconnected. A record-level last-writer policy keeps only the device with the larger timestamp, even though its clock is seven minutes fast. That policy loses a legitimate edit and gives clock error semantic power. The system instead stores paragraph operations with stable IDs and causal context. Nonoverlapping insertions compose; concurrent changes to the dosage sentence produce two preserved candidates and a clinical-review conflict. The displayed shared note remains explicitly pending until reviewed. **Conclusion:** merge granularity may preserve independent intent, but safety-sensitive semantic overlap still requires accountable adjudication.

### Example 2

**Field inspection with resumable evidence.**

A tablet records 40 inspections/hour at a 30 KB mean for 72 disconnected hours. The raw bound is $40\cdot30{,}000\cdot72=86.4$ MB. The team provisions 200 MB after measuring journal, index, retry, and photo variance. Metadata and mandatory readings commit transactionally first; photographs use content-addressed chunks. At 20 inspections/hour of new production and 80 inspections/hour of sustained upload-equivalent capacity, a 2,880-inspection backlog ideally drains in $2{,}880/(80-20)=48$ hours. Retries and downloads lengthen it. **Conclusion:** storage and reconnect are separate capacity obligations, and resumable evidence prevents one large attachment from blocking every result.

### Example 3

**Preserving the last five inventory units.**

Three disconnected depots share a global stock of 12 kits. Before isolation they hold rights of 5, 4, and 3, whose sum is 12. Depot A sells five and rejects a sixth even though B may still have unused rights. No site can drive global admitted sales above 12 because it can consume only its allocation. When connectivity returns, B transfers two unused rights to A through one idempotent transfer operation; duplicate delivery cannot create rights. **Conclusion:** escrow sacrifices some utilization during partition to preserve a hard inventory bound.

### Example 4

**Offline payment under bounded risk.**

A ferry terminal may lose connectivity for four hours. Allowing arbitrary card charges would turn availability into unbounded fraud and credit risk. The acquirer grants the terminal a protected offline risk budget of €2,000, a €100 per-transaction ceiling, an expiry, device epoch, and merchant scope. Each accepted transaction atomically consumes budget and prints a receipt marked “offline accepted; settlement pending.” A stolen terminal cannot exceed the remaining grant, and reconnect submits stable transaction identities before accepting a new grant. **Conclusion:** offline payment is a delegated risk decision with explicit bounds, not a queued ordinary API call.

### Example 5

**Patient assignment conflict.**

Two emergency coordinators, both offline, assign the same specialist to different critical transfers. A set union converges by retaining both assignments, but the specialist cannot be in two ambulances. Last-writer-wins hides one promise. The architecture treats specialist availability as exclusive authority: only the coordinator holding the current assignment token can make a final allocation; the other may create a request marked provisional. On reconnect, the provisional request enters escalation with timestamps as evidence, not authority. **Conclusion:** convergence of records cannot preserve a real-world exclusivity invariant without rights or coordination.

### Example 6

**Revoking a stolen device that remains offline.**

A survey tablet containing private records is stolen and never receives remote wipe. Its device certificate is valid for another day, but locally cached policy allows only reading its assigned cases and creating observations—never downloading new cases or exporting plaintext. The server advances the device epoch immediately. If the tablet reconnects, it may upload encrypted recovery records to a quarantine endpoint but cannot regain reads or submit ordinary operations. Disk encryption and local authentication reduce offline disclosure; neither proves erasure. **Conclusion:** containment comes from prior minimization and scoped authority plus server-side fencing, not hope that a command reaches the device.

### Example 7

**A clock moves backward.**

Device R records operation `r:108` at displayed 14:05, then reboots with its clock at 13:42 and records `r:109`. Device S has concurrently recorded `s:77`. Sorting by wall time would place `r:109` before its cause and cannot order it against `s:77`. Replica sequence proves $r{:}108\rightarrow r{:}109$; version summaries show $s{:}77\parallel r{:}109$. The UI retains both physical/display time and server receipt time, while merge uses causal identity. **Conclusion:** clock metadata supports diagnosis and domain time, while causal metadata supports synchronization order.

### Example 8

**Storage approaches exhaustion.**

A wildlife sensor hub has 500 MB free, with safety alarms, signed custody events, raw images, and a replaceable map cache competing for space. Policy reserves 100 MB for journal, upgrade, and critical evidence. At the threshold it evicts the map cache, then reduces ordinary image resolution, while retaining alarm and custody events losslessly. Once only the reserve remains, it refuses new bulk capture and visibly reports degraded acquisition rather than claiming success. **Conclusion:** priority and admission must be defined before disk pressure; filesystem failure is too late to choose what mattered.

### Example 9

**A replica skips six schema releases.**

An agricultural tablet returns after nine months with schema 3 while the server supports schemas 7 and 8 for direct admission. Its pending schema-3 pesticide operation uses a unit whose historical meaning is still documented, so a quarantined transformer converts it to schema 8, preserves original payload and transform digest, and requests review because the current policy needs a field absent in schema 3. A second unknown operation is exported for manual recovery rather than dropped. The device must upgrade before receiving new authority. **Conclusion:** version compatibility includes operation meaning and policy evidence; unsupported does not justify silent loss or guessed defaults.

### Example 10

**Disaster response across independent organizations.**

After a storm, municipal, hospital, and volunteer teams operate isolated. Person records cannot be indiscriminately replicated across privacy boundaries, and two teams may issue overlapping shelter or transport promises. Each organization keeps its own authoritative case log and shares minimal, purpose-bound offers and requests with stable identities. Shelter beds use allocated rights; free-text observations preserve provenance; identity matches remain tentative until evidence supports linkage. Reconnection first exchanges revocation and consent epochs, then resource outcomes, then bulk evidence. Disputes retain all signed claims for a joint review. **Conclusion:** a multi-party offline design needs federated authority, minimization, and reconciliation governance—not one globally writable database.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) explains races, atomicity, and synchronization inside a node.
- [Software Engineering: Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns deployment, operational recovery, and reliability practice.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns transaction, storage-engine, and replication implementation details.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns causal order, replication protocols, consensus, and CRDT algorithms in depth.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns credential, device, cryptographic, and adversarial mechanisms.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns physical mission, human procedure, and lifecycle integration.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns sync protocol contracts, idempotency interfaces, and compatibility at service boundaries.
- [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) owns fleet infrastructure and hosted implementation detail.

## References

1. James J. Kistler and M. Satyanarayanan, “Disconnected Operation in the Coda File System,” *ACM Transactions on Computer Systems* 10(1), 1992. [Coda publication record and paper](https://www.cs.cmu.edu/~coda/docs-coda.html).
2. Douglas B. Terry et al., “Managing Update Conflicts in Bayou, a Weakly Connected Replicated Storage System,” *SOSP ’95*, 1995. [ACM DOI record](https://doi.org/10.1145/224056.224070).
3. Alan Demers et al., “Epidemic Algorithms for Replicated Database Maintenance,” *PODC ’87*, 1987. [ACM DOI record](https://doi.org/10.1145/41840.41841).
4. Marc Shapiro, Nuno Preguiça, Carlos Baquero, and Marek Zawirski, “Conflict-Free Replicated Data Types,” INRIA Research Report RR-7687 / SSS, 2011. [INRIA author publication record and preprint](https://perso.lip6.fr/Marc.Shapiro/papers/2011/CRDTs_SSS-2011.pdf).
5. Martin Kleppmann, Adam Wiggins, Peter van Hardenberg, and Mark McGranaghan, “Local-First Software: You Own Your Data, in spite of the Cloud,” *Onward! ’19*, 2019. [DOI-linked author publication](https://www.inkandswitch.com/essay/local-first/).
6. Martin Kleppmann and Chris Riccomini, *Designing Data-Intensive Applications*, 2nd ed., O’Reilly Media, February 2026. [Publisher record](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/).
7. NIST, *SP 800-124 Rev. 2: Guidelines for Managing the Security of Mobile Devices in the Enterprise*, May 2023. [Final publication](https://csrc.nist.gov/pubs/sp/800/124/r2/final). Current final status checked 2026-09-06.
8. IETF, *RFC 9562: Universally Unique IDentifiers (UUIDs)*, May 2024. [RFC Editor record](https://www.rfc-editor.org/info/rfc9562/). Current status and obsolescence of RFC 4122 checked 2026-09-06.
9. IETF, *RFC 3339: Date and Time on the Internet: Timestamps*, July 2002, as updated by *RFC 9557*, April 2024. [RFC 3339 record](https://www.rfc-editor.org/info/rfc3339/) and [RFC 9557 record](https://www.rfc-editor.org/info/rfc9557/). Update status checked 2026-09-06.
10. SQLite Project, “Isolation In SQLite.” [Official documentation](https://www.sqlite.org/isolation.html). Implementation behavior checked 2026-09-06.
11. SQLite Project, “Write-Ahead Logging.” [Official documentation](https://www.sqlite.org/wal.html). WAL persistence and recovery cautions checked 2026-09-06.
12. Pat Helland and David Campbell, “Building on Quicksand,” *CIDR 2009*. [CIDR proceedings paper](https://www.cidrdb.org/cidr2009/Papers/CIDR09_Paper29.pdf).

## Exercises

### Exercise 1

**Distinguish outcomes.**

A mobile form displays “saved” immediately after updating an in-memory model, later writes to a local database, uploads after reconnection, and requires supervisor approval on the server. Name the distinct outcomes that the interface and evidence model should represent, and explain which one permits the worker to power off safely.

### Exercise 2

**Prove and limit a merge.**

Two replicas hold grow-only sets $A=\{a,b\}$ and $B=\{b,c\}$ and merge by union. Show duplicate and reversed delivery produce the same result. Then give one domain rule for which convergence by union is insufficient.

### Exercise 3

**Diagnose a reconnect backlog.**

A device produces 12 MB/hour while disconnected and reconnects with 360 MB queued. The link provides 20 MB/hour of sustained application-level upload while new work continues. Compute idealized drain time. Diagnose the result if validation and retries reduce effective upload to 10 MB/hour, and propose two architectural controls.

### Exercise 4

**Design bounded offline allocation.**

Design offline allocation for 200 emergency meal vouchers across four shelters. State the rights invariant, transfer identity, backup/restore rule, user-visible states, and what happens when one shelter exhausts rights while another remains disconnected with unused rights.

### Exercise 5

**Transfer to wildfire response.**

Design the offline contract for a multi-agency wildfire application that records crew locations, assigns scarce evacuation vehicles, stores medical notes, and shares closure notices. Cover authority, local durability, synchronization, conflict classes, user-visible states, capacity, security/revocation, schema evolution, and cold-start testing. Identify at least two actions that must not use generic last-writer-wins.

## Answers to the Exercises

### Answer 1

The outcomes are editing/in-memory only, locally durably committed, queued for transfer, transport received, server validated, supervisor accepted or rejected, and any later external effect. Only a successful local durable transaction under the declared crash and storage assumptions permits an ordinary safe power-off; even then, the work may exist on one device and needs a loss warning if no local redundancy exists. “Saved on this device; approval pending” is accurate after local commit. An upload acknowledgement should not imply approval. Evidence should retain stable operation ID, local commit result, transfer checkpoint, server outcome, and approval identity.

### Answer 2

$A\cup B=\{a,b,c\}$. Reversing delivery gives $B\cup A=\{a,b,c\}$ by commutativity. Receiving $B$ twice gives $(A\cup B)\cup B=\{a,b,c\}$ by associativity and idempotence. Thus order and duplicate delivery do not change the result. Union is insufficient if the set represents simultaneous assignments of one exclusive vehicle: retaining both assignments converges but violates physical exclusivity. A right/token, single authority epoch, or explicit conflict workflow is required. Credit requires both the algebra and a domain counterexample.

### Answer 3

With $b=360$ MB, $\lambda=12$ MB/hour, and $\mu=20$ MB/hour, net drain is 8 MB/hour and idealized time is $360/8=45$ hours. At effective $\mu=10$, production exceeds drain capacity by 2 MB/hour, so backlog grows and no finite drain time exists while production continues. Controls include reserving more application-level bandwidth or a scheduled higher-capacity transfer, and reducing admitted bulk production while preserving critical records. Prioritization, compression with measured semantics, or physical authorized export are acceptable additions. Merely retrying faster is not a solution.

### Answer 4

Allocate nonnegative rights such as 50 vouchers per shelter so $\sum q_r\le200$. Each issue atomically consumes one local right and creates a stable voucher identity bound to shelter, rights epoch, recipient policy, and issuance evidence. A transfer has one stable ID and atomically subtracts from the donor before adding at the receiver; retry is deduplicated. Backup restore must never clone unconsumed rights: restored state reuses the replica identity only after fencing the old instance, or starts a new epoch with rights reissued by authority. The UI distinguishes locally issued, submitted, accepted, rejected, and disputed. An exhausted shelter rejects final issuance or invokes a separately audited emergency override; it cannot assume another disconnected shelter’s rights. This preserves the bound at the cost of stranded capacity.

### Answer 5

One sound design gives each agency authority over its personnel observations and medical records, while a joint incident authority allocates vehicle rights and closure epochs. Crew positions commit locally with stable observation identity, device sequence, physical time and uncertainty; they append rather than overwrite. Vehicle assignment consumes a preallocated exclusive token, so concurrent generic last-writer-wins is forbidden. Medical-note amendments preserve authorship and causal context; conflicting dosage or allergy edits require clinical review, another case where last-writer-wins is forbidden. Closure notices carry geographic scope, issuing authority, validity, and revocation epoch.

Each operation and queue record commits transactionally to encrypted local storage. The interface labels local, pending, shared, rejected, conflicted, and expired states. Sync authenticates agencies, exchanges current consent/revocation and authority epochs first, negotiates schema, transfers bounded idempotent batches, and returns per-operation outcomes. Critical alerts, rights, and medical evidence outrank imagery under storage and bandwidth pressure. Lost devices are contained by scoped data, protected keys, short high-risk grants, and server-side fencing; remote wipe is supplementary. Protocols support a declared offline horizon and quarantine older operations with original evidence for transformation or review. Tests include cold boot without network or trusted wall time, 72-hour partitions, duplicate/reordered delivery, disk full, stolen-device epoch, skipped releases, fleet reconnect, concurrent vehicle claims, and comparison with physical vehicle and patient outcomes. A complete answer must preserve federated privacy boundaries and real-world exclusivity, not merely describe data replication.
