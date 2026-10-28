---
module_id: DSE-068
program: Data Structures Engineering
level: 2
module_number: 68
title: Hazard Pointers and Epoch Reclamation
status: complete
last_verified: 2026-08-30
---

# Hazard Pointers and Epoch Reclamation

## One-Page Review

### Governing question

How can a nonblocking data structure reclaim removed nodes without freeing storage that a delayed participant may still dereference, and when should engineers choose precise hazard announcements versus coarse epoch/grace-period protection?

### Essential definitions

- **logical removal** makes a node absent from the abstract data structure; **physical unlinking** removes a traversal path; **reclamation** destroys or reuses storage only after no eligible observer can access it.
- A **retired node** is removed but not yet reclaimable.
- A **hazard pointer** is a shared announcement of a node one participant may dereference or use in an ABA-sensitive comparison.
- **protect-then-validate** loads a candidate, publishes it as hazardous, and reloads its source before dereferencing.
- A **retire list** holds removed nodes pending a scan of hazard announcements.
- An **epoch** is a logical generation used to group read-side participation and retirements.
- **pinning** announces that a participant may hold references protected by an epoch.
- A **quiescent state** is a point after which the participant retains no reference from the earlier protected interval.
- A **grace period** has elapsed when every participant that could hold a pre-retirement reference has quiesced.
- **reclamation progress** concerns when memory becomes reusable; it is distinct from operation progress.

### Central model, mechanism, or theorem

Hazard pointers protect named nodes. A reader loads A, publishes A, validates the shared source still identifies A, then dereferences while keeping the hazard set. A remover retires A. A scan reclaims A only if no relevant hazard slot contains A. This tolerates unrelated stalled participants but charges readers atomic publication and reclaimers scanning/threshold work.

Epoch-based reclamation protects intervals. A reader pins before loading shared nodes and unpins only after its final dependent access. A remover records a retirement generation. The node becomes safe only after every participant that could have entered before retirement passes through quiescence. Reads can be cheap and reclamation batched, but one stalled pinned participant can retain a large cohort.

For either scheme, safety theorem is conditional: every possible dereference is protected, publication/entry ordering is correct, removal goes through retirement, all reuse paths respect eligibility, participant lifecycle is sound, and destruction waits for global quiescence. Neither scheme by itself proves the data structure linearizable or the complete API lock-free.

### Critical invariants

1. A node is reclaimed only when no participant can legally retain a reference to its current incarnation.
2. Removal always transitions `live → retired`; no path directly frees a shared node.
3. Hazard readers publish then validate before dereference; validation failure prevents access and retries.
4. A hazard remains active through the final dependent read or CAS.
5. Scans use a coherent-enough view required by the hazard algorithm and never reclaim a matching retired node.
6. Epoch readers pin before loading and unpin after releasing every protected reference.
7. A retired epoch node waits for every potentially earlier reader to quiesce.
8. Protected references cannot escape their hazard/epoch guard or enter unintegrated callbacks.
9. Thread registration, nesting, cancellation, panic/exception, exit, and shutdown preserve announcements.
10. Retire lists, records, deferred callbacks, retained bytes, and reclamation work have explicit bounds/policies.

### Common failures

- Freeing immediately after a successful unlink CAS.
- Publishing a hazard after dereference or omitting source validation.
- Protecting only the first of several simultaneously accessed nodes.
- Clearing protection before the final CAS/callback access.
- Reusing through a pool that bypasses retirement scans.
- Treating an unpinned epoch pointer as valid.
- Pinning across blocking I/O, user callbacks, or indefinite waits.
- Forcibly dropping a stalled participant's protection while it may resume.
- Claiming operation lock-freedom bounds retired memory.
- Batch-reclaiming without measuring destructor and allocator latency.

### Compact example

P loads and hazard-protects A, then validates. Q unlinks and retires A. A scan sees P's hazard and reclaims zero nodes. After P's final access and clear, the next scan reclaims A. Separately, P pins generation 0; Q retires B at generation 0. B is unsafe while P remains pinned and safe only after P quiesces. The protocols reach the same lifetime result through per-node versus per-interval evidence.

### Connections

[DSE-065](065-lock-free-stack-structure-and-invariants.md) and [DSE-066](066-michael-scott-queues.md) provide structures needing reclamation. [DSE-067](067-aba-avoidance.md) distinguishes lifetime from identity/version. The [program roadmap](../ROADMAP.md) next studies RCU and linearizability testing.

## Governing Question

What complete protocol—from first load through retirement, protection release, reuse, participant exit, and object destruction—makes dynamic-memory access safe in a nonblocking structure while preserving the required progress and memory bounds?

## Why This Matters

A successful deletion CAS does not imply exclusive ownership of the removed node. Another participant can have loaded its address earlier and be paused before reading a field or attempting a CAS. Immediate `free` changes a correct abstract removal into use-after-free; prompt reuse can also create ABA. This gap exists in lock-free updates, optimistic lock-free reads over locked structures, caches, registries, routing tables, and intrusive pools.

Garbage-collected languages hide much physical reclamation but do not remove all logical ABA, resource finalization, off-heap, FFI, or latency concerns. Native systems must supply a protocol. Hazard pointers and epoch-based reclamation (EBR) are foundational because they expose opposite trade-offs. Hazards describe exactly which objects matter now. Epochs describe which time interval may still contain old observations.

These methods are part of the algorithm, not interchangeable allocator plugins. Hazard pointers can be difficult where an operation needs an unbounded or data-dependent set of simultaneous references. Epochs are easy to compose across traversals but a paused reader can delay all nodes in a cohort. Both need atomic ordering, record registration, cancellation cleanup, thread reuse, shutdown, and metrics.

The production question is larger than safety. A scheme may preserve dereference safety while retaining unbounded memory, producing latency spikes during scans/destructors, or narrowing the data structure's progress guarantee. Graduate-level design separates safety, ABA resistance, reclamation progress, memory bounds, operation progress, and empirical performance.

## Prerequisites and Retrieval

Retrieve singly linked reachability, allocation/reuse, atomic load/CAS, acquire/release, linearizability, progress classes, ABA, and participant lifecycle. From [DSE-065](065-lock-free-stack-structure-and-invariants.md), retrieve the load-dereference-CAS window. From [DSE-066](066-michael-scott-queues.md), retrieve old-dummy retirement. From [DSE-067](067-aba-avoidance.md), retrieve incarnation identity, load-publish-validate, and the fact that a rejecting tagged CAS cannot repair an earlier invalid dereference.

The legacy materials reinforce the decision boundary—mature reclamation or a simpler bounded/locked design—but provide no reusable complete reclamation implementation. The repository's executable verifier excludes runtime threading primitives, so the artifact is a bounded eligibility model rather than an implementation of hazards or EBR.

## Learning Objectives

After completing this module, you can:

1. separate abstract deletion, unlinking, retirement, reclamation, and reuse;
2. derive a hazard-pointer protect-validate-access-retire-scan protocol;
3. derive an epoch pin-access-retire-quiesce-grace protocol;
4. state safety invariants and operation/reclamation progress separately;
5. calculate hazard scan thresholds and conservative retention bounds;
6. diagnose stalled, crashed, cancelled, nested, and escaping participants;
7. integrate allocators, destructors, pools, callbacks, and shutdown safely;
8. compare hazards, epochs, reference counting, RCU, GC, and locks;
9. design forced-schedule, sanitizer, bounded-model, and lifecycle evidence; and
10. choose a scheme using workload topology, latency, and memory telemetry.

## Core Exposition

**Specify the lifetime problem.** Let node A be reachable and reader P load its address. Remover Q unlinks A and returns. Abstract correctness may allow Q to finish immediately. Physical safety cannot free A until P's last possible dereference. The earliest safe point is not “after unlink”; it is “after every observer that could have acquired A before unlink has become unable to use it.” A reclamation scheme provides evidence for that statement.

Use explicit lifecycle states:

- `private`: initialized but unreachable and owned by one operation;
- `live`: reachable under the structure's traversal rules;
- `logically removed`: excluded from the abstract set but perhaps still linked/helpable;
- `retired`: no new protected traversal should acquire it, but old observers may remain;
- `reclaimable`: the scheme proves no eligible observer remains;
- `reused`: storage begins a new incarnation only after reclamation.

Some algorithms mark then unlink. Retirement must occur at the point their traversal/protection proof permits, not mechanically at the linearization point. A logically removed node may still be needed for helping or navigation.

**Derive hazard protection.** Assume a fixed small number of hazard slots per participant. To read a shared pointer `source` safely:

1. load candidate A from `source`;
2. atomically publish A in an owned hazard slot with the scheme's required ordering;
3. reload/validate `source` still identifies A;
4. if validation fails, clear/update the slot and retry without dereferencing A;
5. otherwise dereference A while the slot remains A;
6. clear only after the last dependent access.

Why validate? Q can unlink, scan, and reclaim A between P's initial load and hazard publication. If P publishes too late then dereferences, the announcement cannot resurrect A. Validation ensures either A remained obtainable while protection became visible, or P abandons it without access. Exact source and validation rules can be more complex for marked/tagged links, helping, or multiple fields.

**Retire and scan.** Q does not free an unlinked node. It appends A to a retire list. When a threshold is reached, a scanner obtains the relevant hazard announcements, constructs a protected-address set, partitions retired nodes, reclaims those absent, and keeps matches. Michael's hazard-pointer analysis chooses thresholds relative to the number of hazard records so amortized work and unreclaimed-node bounds can be reasoned about under its assumptions.

Scanning is not merely `if address not found now`. The memory-order protocol must ensure a valid reader's publication is visible in the way the proof requires. Record acquisition/release and reuse cannot let two participants own one slot. A reclaimer cannot infer a dead thread from timeout alone and clear its hazard while it may resume.

**Protect multiple nodes.** A list operation may need predecessor, current, and successor simultaneously. Each dereference/conditional update needs coverage, and movement commonly follows a hand-over-hand sequence: protect next, validate the link from a still-protected current, then release current when no longer needed. If the number of live references is unbounded, fixed hazard slots may not fit without algorithm redesign, restartable traversal, reference counting, or another scheme.

Hazards can aid ABA avoidance by forbidding reuse of protected addresses, but only for algorithms safe when physical identities are stable. They do not prevent a still-live node from being removed, mutated, and reinserted. Structural validation remains necessary.

**Derive epoch protection.** Epoch schemes replace per-node announcements with read-side intervals. A participant registers and pins/announces active before loading shared pointers. Every pointer loaded and kept within that interval is protected under the scheme. A remover associates retired nodes with a current generation. Advancement/grace logic establishes that all participants who could have observed those nodes have unpinned or moved beyond the relevant generation; only then does it run deferred destruction.

Many practical EBR schemes use a small cyclic epoch space and require multiple advances before reclaiming, but exact numbers and comparisons are implementation-specific. Do not transplant “three epochs” into a different scheme without its wrap, announcement, and grace proof. The durable invariant is: no node is reclaimed until every reader capable of holding a pre-retirement reference has quiesced.

**Keep references scoped.** An epoch-protected pointer must not escape beyond its guard: do not store it in a long-lived object, return it without ownership conversion, schedule a callback carrying it, or unpin before the final CAS/read. Nesting must prevent an inner unpin from ending an outer protection interval. Async tasks are especially dangerous if thread-local pinning and task migration/suspension do not match; use a library with an explicit supported model.

**Analyze stalled participants.** Hazard pointers are precise: a stalled participant generally retains the finite nodes in its slots, though it may also block algorithm-specific cleanup. Other retired nodes can be scanned and reclaimed. Classic EBR is coarse: one participant pinned in an old generation can prevent a grace period and retain every subsequently retired node covered by it. Structural operations may remain lock-free while memory use grows without bound.

This is not automatically a safety defect; it is a resource/progress defect that can become availability failure. Bound critical-section duration by design where possible, prohibit blocking/callbacks while pinned, monitor oldest pin age and retired bytes, and define overload/fail-safe policy. Declaring a participant dead and ignoring it is safe only when the runtime guarantees it cannot resume with old references.

**Separate progress properties.** A Treiber stack using hazard pointers can have:

- lock-free push/pop structural transitions;
- hazard-slot acquisition that blocks or fails if records are exhausted;
- scans whose work grows with registered slots and retire batch;
- safe but not prompt reclamation when hazards stay set;
- destructors/allocators that lock or execute unbounded work.

State a progress property for each operation and subsystem. “The queue is lock-free” should specify whether allocation, protection registration, retirement, scan, deferred destructor, and shutdown are included. A bounded wait-free reclamation claim requires a substantially stronger algorithm and proof.

**Integrate allocation and destruction.** Reclaimed storage may return to a local pool, global allocator, or OS. Reuse must occur after eligibility, not simply after logical delete. Destructors may call user code, acquire locks, throw/panic, or take long; batch execution can create tail spikes. Separate payload disposal from node-storage reuse only if ownership and access proofs allow it. If destructors must run on a designated thread, deferred work queues inherit their own capacity and shutdown obligations.

An allocator can cache freed addresses, making forced-reuse ABA tests important. Pool shutdown must stop new acquisitions, wait for active operations/guards, drain retire lists, reach grace/scan, invoke destructors exactly once, and free registration records. Fork, dynamic library unload, thread-local destructor order, and process-abort behavior need platform policy.

**Estimate hazard costs and bounds.** Suppose at most `P` participants own `K` hazard slots, so at most `H=PK` addresses are announced at one instant. A scan reads up to H slots and examines R retired nodes. With a hash/set representation, expected scan work is `O(H+R)`; sorting hazards yields `O(H log H + R log H)` or related implementation costs. Michael's threshold choices derive bounded unreclaimed counts under registered-thread and slot assumptions.

These are algorithmic models, not latency guarantees. Cache misses, slot layout, false sharing, registry churn, memory ordering, destructors, and allocator batches matter. If participants can register without bound, H and retention bounds are not constants.

**Estimate epoch retention.** If retirement rate is `λ` bytes/second and oldest blocking pin lasts `T`, a first-order retained-byte exposure is at least roughly `λT`, plus batches already pending and live structure memory. It is not an upper bound unless rate, pin duration, batching, and participant behavior are bounded. Track bytes, not only node count, because payload sizes differ.

**Choose based on access topology.** Hazards suit algorithms with a small known set of independently protected nodes, where stalled readers should not stop unrelated reclamation. EBR suits short, well-scoped read intervals and workloads favoring very cheap repeated loads. RCU variants optimize read-mostly cases with explicit grace mechanisms. Atomic/reference counting suits shared ownership but safe acquisition and decrement/reclaim races are hard. A mutex or reader-writer lock can make lifetime proof simpler and bound shutdown at the cost of blocking.

Use mature implementations whose supported thread/task/lifecycle model matches the product. Current C++ draft safe-reclamation facilities and the Crossbeam epoch API demonstrate that reclamation is becoming an explicit library surface, but an API cannot prove a caller's guards cover every access.

**Use a finite model honestly.** The artifact models one hazard-protected retirement and one epoch-protected retirement. It shows A retained while named by a hazard then reclaimed after clear; B retained while a generation-0 reader is active then safe after quiescence.

<!-- bijux-verify: {"id":"hazard-epoch-eligibility-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"hazard_retired=A\nhazard_scan_while_protected=0\nhazard_scan_after_clear=1\nepoch_retired=B@0\nepoch_safe_while_pinned=False\nepoch_safe_after_quiescence=True\nreclaimed=A,B\nstalled_reader_blocks_epoch=True\nuse_after_free_prevented=True\nall_invariants=True\nevidence=finite_reclamation_protocol_model\n","stderr":""}} -->
```python
class HazardDomain:
    def __init__(self):
        self.hazards = {}
        self.retired = []
        self.reclaimed = []

    def protect(self, participant, node):
        self.hazards[participant] = node

    def clear(self, participant):
        self.hazards.pop(participant, None)

    def retire(self, node):
        self.retired.append(node)

    def scan(self):
        protected = set(self.hazards.values())
        safe = [node for node in self.retired if node not in protected]
        self.retired = [node for node in self.retired if node in protected]
        self.reclaimed.extend(safe)
        return len(safe)


class EpochDomain:
    def __init__(self):
        self.generation = 0
        self.active = {}
        self.retired = []
        self.reclaimed = []

    def pin(self, participant):
        self.active[participant] = self.generation

    def unpin(self, participant):
        self.active.pop(participant, None)

    def retire(self, node):
        self.retired.append((node, self.generation))

    def safe(self, retirement_generation):
        return all(entry > retirement_generation for entry in self.active.values())

    def reclaim_safe(self):
        keep = []
        for node, retired_at in self.retired:
            if self.safe(retired_at):
                self.reclaimed.append(node)
            else:
                keep.append((node, retired_at))
        self.retired = keep


hazard = HazardDomain()
hazard.protect("P", "A")
hazard.retire("A")
protected_scan = hazard.scan()
hazard.clear("P")
cleared_scan = hazard.scan()

epoch = EpochDomain()
epoch.pin("P")
epoch.retire("B")
safe_while_pinned = epoch.safe(0)
stalled_reader_blocks_epoch = not safe_while_pinned
epoch.unpin("P")
safe_after_quiescence = epoch.safe(0)
epoch.reclaim_safe()

reclaimed = hazard.reclaimed + epoch.reclaimed
use_after_free_prevented = protected_scan == 0 and not safe_while_pinned
all_invariants = (
    hazard.retired == []
    and epoch.retired == []
    and reclaimed == ["A", "B"]
    and cleared_scan == 1
    and safe_after_quiescence
    and use_after_free_prevented
)

print("hazard_retired=A")
print(f"hazard_scan_while_protected={protected_scan}")
print(f"hazard_scan_after_clear={cleared_scan}")
print("epoch_retired=B@0")
print(f"epoch_safe_while_pinned={safe_while_pinned}")
print(f"epoch_safe_after_quiescence={safe_after_quiescence}")
print("reclaimed=" + ",".join(reclaimed))
print(f"stalled_reader_blocks_epoch={stalled_reader_blocks_epoch}")
print(f"use_after_free_prevented={use_after_free_prevented}")
print(f"all_invariants={all_invariants}")
print("evidence=finite_reclamation_protocol_model")
```

The model assumes publication and validation already succeeded, represents participants as trusted dictionary entries, and uses a simplified quiescence predicate rather than a cyclic production EBR algorithm. It does not execute threads, atomics, allocators, destructors, weak memory, registration races, arbitrary schedules, ABA, progress, or performance.

**Test safety and resource behavior.** Force a reader to pause after initial load, after hazard publication, after validation, after pin, before unpin, and during shutdown. Force unlink and allocator reuse around every pause. Verify no destructor/reuse occurs early and every eligible node is eventually destroyed exactly once after release. Test multiple protected nodes, slot exhaustion, nested guards, registration reuse, thread exit, panic/exception, cancellation, callback escape, and object destruction.

Use bounded model checking for small participant/node counts, history checking for the host structure, and race/use-after-free sanitizers where supported. Instrument retire age/bytes, hazard slot occupancy, scan work, epoch advances, oldest pin, deferred destructor time, allocation/reuse, and failures. Stress tests are evidence about exercised schedules, not universal proofs.

Benchmark end-to-end against garbage collection, reference counting, and correct locks using equal semantics. Vary read/write ratio, traversal length, simultaneous references, participants, oversubscription, NUMA, retire rate, object size, allocator, destructor cost, and stalled readers. Report throughput and latency percentiles alongside peak/steady retained bytes and per-participant fairness. The fastest operation path can be unacceptable if memory or cleanup latency is unbounded.

## Definitions and Notation

Let node states be private `P`, live `L`, logically removed `M`, retired `R`, reclaimable `C`, and reused incarnation `P'`. Valid reclamation path is `L→M→R→C→P'`, with algorithm-specific possible overlap between M and reachable helping links. `Access(p,x,t)` means participant p may legally dereference incarnation x at time t.

Hazard slots are `HP[p,k]`; protected set at scan observation is `H={x | ∃p,k: HP[p,k]=x}`. A retired node x is eligible only under the scheme's visibility proof when `x∉H`. Let registered participants be P and slots per participant K; `|H|≤PK` under fixed registration.

Epoch participant state is inactive or active with entry generation `E_p`. Node x retired in generation `r(x)` is eligible only after a grace predicate `G(x)` proves all participants capable of holding x from before retirement have quiesced. The chapter's finite model uses `G(x) ≡ ∀p active: E_p>r(x)` solely as a simple interval model, not a universal EBR implementation.

Let R be retire-batch size, `λ_n` nodes/second and `λ_b` bytes/second retired, `T_old` oldest blocking protection age, `B_r` retired bytes, `S` scan time, and `D` deferred-destruction time. These are workload observations; bounds require enforced assumptions.

## Mechanisms, Invariants, or Proof Structure

### Hazard-pointer safety proof

1. Participant loads candidate, publishes it in an exclusively owned slot, and validates the acquisition source.
2. Validation failure causes retry without candidate dereference; success establishes protected access under the publication/scan ordering.
3. Removers retire rather than free; scanners exclude every address visible in relevant hazard slots.
4. Protection remains until the final dependent access, so no eligible scan overlaps a legal dereference.
5. Reuse occurs only after an excluding scan; therefore a protected incarnation cannot be freed/reused.

### Epoch safety proof

1. Participant pins/announces active before loading shared candidates.
2. Removal records retirement within the generation/grace protocol.
3. A node waits until every participant that might hold a pre-retirement reference has passed quiescence.
4. Protected pointers do not escape, and unpin follows the last dependent access.
5. Therefore an eligible node has no legal observer and can be reclaimed/reused.

### Progress and bound proof obligations

1. State operation, registration, protection, retire, scan, advance, destructor, and shutdown progress independently.
2. Bound registered participants, hazard slots, retire thresholds, and scan work for hazard memory/work claims.
3. Bound pin duration and retire rate—or reject a bounded-retention claim—for classic EBR.
4. Include thread failure, cancellation, nesting, allocator/destructor behavior, and overload.
5. Measure retention and tails without treating measurements as universal liveness proofs.

### Evidence ladder

1. Lifecycle and ownership specification for each node/incarnation.
2. Minimal paused-reader/use-after-free counterexample.
3. Finite hazard/epoch eligibility model and arithmetic recomputation.
4. Controlled publication, validation, pin, unlink, scan, grace, and reuse schedules.
5. Host-structure linearizability plus target memory/race/use-after-free/model evidence.
6. Registration, exhaustion, cancellation, thread exit, stall, callback, and shutdown faults.
7. Production-shaped retire rate, retention, scan/grace/destructor latency, throughput, and fairness telemetry.

## Alternatives and Trade-Offs

| Scheme | Protection granularity | Primary strength | Principal cost/risk |
|---|---|---|---|
| Hazard pointers | named nodes | stalled reader retains limited named nodes | per-access publication, slots/scans |
| Epoch reclamation | read interval/cohort | cheap repeated protected loads | stalled pin blocks cohort reclamation |
| RCU/QSBR | read interval plus grace | very cheap read-mostly paths | quiescence/update complexity |
| Atomic reference count | individual object ownership | prompt local lifetime when count reaches zero | safe acquisition, atomic traffic, cycles |
| Tracing GC | reachable object graph | automatic physical lifetime | pauses/throughput, logical ABA, off-heap |
| Tagged pointer only | compared generation | detects ABA at update | no dereference lifetime; wrap/width |
| Never reclaim until shutdown | process/object lifetime | simplest concurrent access | unbounded/peak memory |
| Mutex/RW lock | critical section | simple lifetime and shutdown proof | blocking, convoy, lock ordering |
| Immutable snapshots | whole version ownership | simple readers and rollback | copy/update/reclamation cost |

Hybrid schemes exist, but composing two incomplete protocols does not automatically produce a complete one. A tagged hazard-protected pointer may address version and lifetime; each mechanism still needs its own proof. Choose a mature implementation and smallest semantic surface meeting the product requirement.

## Failure Modes and Misconceptions

- **“Unlinked means unreachable by everyone.”** Local registers can retain old pointers.
- **“Retired means free.”** Retirement begins deferred eligibility checking.
- **“Publish after reading fields.”** The node can be reclaimed before publication.
- **“Publish is enough.”** Reload/validate closes the load-to-publication race.
- **“One hazard protects the traversal.”** Every simultaneously dependent node/link needs coverage.
- **“A current scan saw no hazard, so an earlier load is impossible.”** Only the full publication/validation ordering supports that inference.
- **“Pinned pointers can be returned normally.”** They cannot outlive the guard without ownership conversion.
- **“Epoch advance is a timer.”** Safety depends on participant quiescence, not elapsed wall time.
- **“A timeout proves a thread dead.”** It may resume; forced reclamation can cause use-after-free.
- **“Lock-free operations imply lock-free allocator/reclaimer.”** These are separate subsystems.
- **“EBR memory is bounded because live structure size is bounded.”** a stalled pin can retain removed cohorts.
- **“Hazards always bound memory by slot count.”** retire thresholds, registry size, algorithm links, and stalled cleanup also matter.
- **“Batch freeing is invisible.”** destructors and allocator interaction can create latency spikes.
- **“GC solves off-heap pointers.”** unmanaged resources still need explicit lifetime integration.
- **“Passing sanitizers proves reclamation.”** They cover exercised schedules and tool semantics only.

## Worked Examples

### Example 1

**Situation.** P loads A; Q unlinks and frees A; P reads `A.next`.

**Reasoning.** Q's successful structural CAS proves abstract removal, not absence of local observers. P dereferences freed storage. Reclamation must wait for evidence excluding P.

**Conclusion.** Linearization and reclamation are distinct events.

### Example 2

**Situation.** P loads A, publishes hazard A, validates the source, and pauses. Q retires A and scans.

**Reasoning.** The scan includes A in the protected set and retains it. After P's last access and clear, a later scan can reclaim A.

**Conclusion.** Hazard eligibility is node-specific and changes after protection release.

### Example 3

**Situation.** P loads A and reads a field before publishing its hazard, then validates successfully because A's address was reused.

**Reasoning.** The field read already raced with free/reuse. Later publication and address validation cannot retroactively make it safe; protection precedes dereference and needs incarnation/ABA support.

**Conclusion.** Protect-then-validate ordering is non-negotiable.

### Example 4

**Situation.** A list deletion needs predecessor P, current C, and successor S, but the participant owns two hazard slots.

**Reasoning.** Reusing a slot may expose a still-needed node. Redesign traversal/validation to need at most two, acquire more bounded slots, use epochs, or choose another algorithm; do not silently dereference the third unprotected node.

**Conclusion.** Hazard-slot cardinality is an algorithm precondition.

### Example 5

**Situation.** Reader R pins epoch 7, server performs blocking I/O for 30 seconds, writers retire 50 MB/s.

**Reasoning.** R may block the relevant grace period; first-order exposure is at least about `50×30=1,500 MB`, plus batches/live memory. Move I/O outside the pin or choose a scheme tolerating stalls.

**Conclusion.** Short read intervals are a resource invariant, not style advice.

### Example 6

**Situation.** An async task pins a thread-local epoch guard, awaits, and resumes on another worker.

**Reasoning.** The library may associate participation with the original thread and forbid guard migration/await. The task can retain memory or violate safety. Use an async-aware supported API or end protection before suspension.

**Conclusion.** Execution topology must match participant identity.

### Example 7

**Situation.** A cancelled operation exits through an exception without clearing hazard slot A.

**Reasoning.** Safety remains conservative—A is not freed—but memory can leak indefinitely. Structured guard cleanup and thread-exit transfer/deregistration are required; forcibly clearing is safe only after proving no resume/access.

**Conclusion.** Cleanup defects can preserve safety while breaking reclamation progress.

### Example 8

**Situation.** A scan reclaims 100,000 nodes whose destructors each update a locked registry.

**Reasoning.** Structural calls may experience a massive latency spike or deadlock/reentrancy. Bound batches, move destruction to a controlled executor with capacity/shutdown policy, or redesign payload ownership.

**Conclusion.** Eligible does not mean unbounded synchronous destruction is operationally safe.

### Example 9

**Situation.** Stack nodes retire through hazards, but a fast internal freelist immediately recycles nodes popped during shutdown.

**Reasoning.** The alternate reuse path bypasses scans and invalidates both lifetime and ABA premises. All reuse—including pools and shutdown drains—must enter after eligibility.

**Conclusion.** Reclamation owns the entire incarnation boundary.

### Example 10

**Situation.** EBR wins throughput benchmarks, while production alerts show old pins and monotonically growing retired bytes.

**Reasoning.** Cheap reads improved operation throughput but reclamation progress failed under the real scheduling/callback mix. Bound pins, add diagnostics/fail-safe policy, or move to hazards/another scheme after comparable tests.

**Conclusion.** Throughput and bounded memory are independent adoption gates.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** atomics, happens-before, progress, cancellation, task migration, and model checking define protocol execution.
- **Operating Systems:** preemption, signals, thread exit, TLS destruction, NUMA, and allocators control grace and retention.
- **Systems Programming:** raw pointer provenance, ownership conversion, destructors, FFI, and unsafe abstraction boundaries govern implementation soundness.
- **Database Engineering:** epochs resemble transaction/snapshot generations; oldest readers delay vacuum/version cleanup and create analogous retention pressure.
- **Security Engineering:** use-after-free, stale-pointer reuse, malicious pinned readers, registry exhaustion, and destructor amplification are attack surfaces.
- **Performance Engineering:** protected-load cost, scans, grace lag, retained bytes, allocator batching, cache layout, and tails must be measured together.

## References

1. Maged M. Michael, [“Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects”](https://www.eecg.utoronto.ca/~amza/ece1747h/papers/hazard_pointers.pdf), *IEEE TPDS* 15(6), 2004. Primary hazard-pointer algorithm, safety, ABA, progress, and bounded-resource analysis.
2. Keir Fraser, [“Practical Lock-Freedom”](https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-579.pdf), University of Cambridge Technical Report UCAM-CL-TR-579, 2004. Primary epoch-based reclamation and practical nonblocking design account.
3. Trevor Brown, [“Reclaiming Memory for Lock-Free Data Structures: There Has to Be a Better Way”](https://www.cs.toronto.edu/~tabrown/debra/fullpaper.pdf), PODC 2015/full version. Primary EBR stall/retention analysis and distributed reclamation alternative.
4. Maged M. Michael and Michael L. Scott, [“Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms”](https://www.cs.rochester.edu/u/scott/papers/1996_PODC_queues.pdf), PODC 1996. Primary queue retirement, counted-pointer, and allocator context.
5. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary correctness framework used to separate abstract effects from reclamation.
6. ISO C++ working draft, [Safe reclamation and hazard pointers](https://eel.is/c++draft/hazard.pointer.syn), current draft accessed 2026-08-30. Primary current standard-library hazard-pointer surface.
7. Maged Michael et al., [“Hazard Pointers for C++26”](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2530r3.pdf), WG21 P2530R3, 2023. Primary rationale and proposed interface history for the standardized facility.
8. Crossbeam project, [`crossbeam::epoch`](https://docs.rs/crossbeam/latest/crossbeam/epoch/index.html), crossbeam-epoch 0.9.20 documentation, accessed 2026-08-30. Maintainer documentation for a current production EBR API and pin/defer model.

## Exercises

### Exercise 1

Define logical removal, unlinking, retirement, reclamation, reuse, hazard pointer, protect-validate, pinning, quiescent state, grace period, and reclamation progress. State the central lifetime invariant.

### Exercise 2

Trace a Treiber pop where P pauses after initial load, Q pops/retires the node, and a scan runs. Give outcomes when P has not published, has published but not validated, has validated, and has cleared.

### Exercise 3

A service has 64 registered participants, two hazard slots each, scan threshold 256 nodes, and average node size 192 bytes. Compute slot count and nominal retired-batch bytes, then explain why these do not constitute a total memory or latency bound.

### Exercise 4

Design an epoch protocol for a read-mostly map used by synchronous request threads. Specify entry/exit, retirement, advancement/grace, nesting, blocking/callback policy, cancellation/exit, shutdown, retention alarms, and progress claims.

### Exercise 5

A low-latency native service must choose hazards, EBR, reference counting, or a reader-writer lock for a linked index. Readers traverse 2–20 nodes, updates are 5%, threads can be preempted for seconds, and memory is strictly capped. Make and defend a choice with verification and rollout evidence.

## Answers to the Exercises

### Answer 1

Logical removal changes abstract membership; unlinking removes a traversal edge; retirement records that a removed node may still have observers; reclamation proves destruction/reuse eligibility; reuse begins a new incarnation. A hazard pointer names a possibly accessed node; protect-validate loads, announces, then confirms the acquisition source before access. Pinning announces an epoch-protected interval; quiescence ends old-reference eligibility; a grace period excludes all earlier readers. Reclamation progress describes when retired storage becomes reusable, separate from data-structure operation progress.

Central invariant: storage is destroyed or reused only after the selected protocol proves that no participant can legally retain or later dereference a reference to that incarnation. Every acquisition, escape, removal, reuse path, and lifecycle exit must participate.

### Answer 2

P initially loads A but has no right to dereference yet. Q can pop and retire A. If a scan runs before P publishes, it may reclaim A; P must publish then validate the source before any dereference, and validation will fail if top changed. If P published A but has not validated, the scan conservatively retains A; P still cannot dereference until validation succeeds. If P validates top remains A, its hazard establishes a protected access window; a later Q retirement/scan retains A. After P's final dependent access and clear, a scan can reclaim A.

If address reuse can make validation compare equal, the algorithm also needs the hazard method's no-reuse guarantee to begin before reuse or another ABA/version rule. Publication ordering and scanner visibility must follow the chosen implementation, not an informal set snapshot.

### Answer 3

Hazard capacity is `64×2=128` slots. A threshold batch of 256 nodes averaging 192 bytes contains `256×192=49,152` bytes, or 48 KiB of node storage. A simple scan may examine 128 announcements and 256 retired nodes.

This omits per-participant retire lists, multiple simultaneous batches, live nodes, payload allocations, record/registry/set memory, allocator fragmentation/caches, nodes retained across scans, participant churn, algorithm-specific marked/helping nodes, and objects larger than average. It also does not bound cache misses, atomic loads, set construction, destructor work, allocator locks, or scheduling latency. Total bounds require maximum participants/slots/node bytes/batches and exact implementation behavior.

### Answer 4

Register each request worker. Enter a nest-aware guard before the first map pointer load; outermost entry announces active/current generation, and outermost exit clears only after the final pointer/callback use. Updates logically remove/unlink then append `(node,generation)` to a retire batch. Advancement periodically checks every registered active participant according to the published cyclic-epoch algorithm; nodes are reclaimed only after its required grace generations prove all pre-retirement readers quiesced.

No blocking I/O, waits, user callbacks, or pointer escape is allowed while pinned; copy/retain owned data then exit first. Cancellation/finally paths unpin; thread exit safely transfers batches and deregisters only after inactive. Shutdown closes admission, waits for active guards and updates, completes grace periods, drains batches/destructors, then frees registry/map. Monitor oldest pin, pinned count, generation age, retire nodes/bytes, batch/destructor latency, and memory cap; alert/reject work before exhaustion. Map operations may retain their structural progress property, but registration, allocation, grace completion, destructors, shutdown, and reclamation under stalled readers have separate non-lock-free or conditional claims.

### Answer 5

Strict memory caps plus seconds-long preemption make classic EBR risky because one pinned reader can retain all update cohorts. Traversals need up to 20 nodes but may require only a small moving window if the published linked-index algorithm can validate hand-over-hand; in that case hazard pointers are a strong candidate because a stalled reader retains its fixed protected set rather than all future retirements. If the algorithm truly needs many simultaneous pointers or strict tail simplicity, a reader-writer lock may be better despite blocking. Atomic reference counting adds per-edge traffic and requires a safe initial acquisition protocol; it is not automatically simpler.

Prototype hazards and the correct RW-lock baseline behind one API. Prove required slot count, protect/validate traversal, mutation/retirement, ABA, memory order, cancellation/exit, pool integration, capacity, and shutdown. Force pauses at every protection boundary and allocator reuse; run linearizability, race/use-after-free, bounded-model, exhaustion, and destructor tests. Benchmark actual 2–20-node reads, 5% writes, seconds-long stalls, NUMA, maximum threads, and payload sizes; report tails, throughput, retry/scan, registry cost, retired bytes, and fairness. Canary with strict retention/latency alarms and rollback. Prefer the lock if hazards cannot meet a proven slot/memory bound or show material measured benefit.
