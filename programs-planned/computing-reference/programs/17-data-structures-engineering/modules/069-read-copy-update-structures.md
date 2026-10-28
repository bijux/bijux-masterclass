---
module_id: DSE-069
program: Data Structures Engineering
level: 2
module_number: 69
title: Read-Copy-Update Structures
status: complete
last_verified: 2026-08-30
---

# Read-Copy-Update Structures

## One-Page Review

### Governing question

How can read-copy-update give read-mostly structures extremely cheap concurrent reads while preserving publication, traversal, deletion, lifetime, update ordering, bounded backlog, and shutdown correctness?

### Essential definitions

- **read-copy-update (RCU)** is a family of synchronization/reclamation techniques in which readers execute in marked read-side critical sections while updaters publish a new view or unlink an old one, then defer reclamation until a grace period.
- A **read-side critical section** delimits references protected by an RCU domain.
- **publication** makes a fully initialized node/version reachable with required ordering; **subscription** safely obtains and consumes it.
- **removal** prevents new readers from acquiring an old object through the protected root/path.
- A **pre-existing reader** could have acquired the old object before removal.
- A **quiescent state** proves a participant no longer holds an earlier protected reference.
- A **grace period** ends after every relevant pre-existing reader has passed quiescence.
- **synchronous reclamation** waits for a grace period; **asynchronous reclamation** queues a callback for after one.
- **QSBR** relies on participants reporting quiescent states; **SRCU** provides separate domains with different read-side mechanics.
- A **weakly consistent traversal** may legally observe some overlapping insertions/removals; it is not a snapshot.

### Central model, mechanism, or theorem

A canonical replacement starts with root pointing to immutable/stable version V0. Writer constructs V1 privately, publishes root V1 with release-capable ordering, and retires V0. Readers enter the RCU domain, acquire/subscription-load root, use that version without escaping the critical section, and exit. Readers that begin after publication cannot newly acquire V0 through root. After every reader that could have acquired V0 before removal exits, a grace period permits V0's destruction/reuse.

Safety requires more than waiting: the published version must be fully initialized; readers must use the prescribed accessors/order; all acquisition paths must be updated; old nodes/links must remain traversable for pre-existing readers; fields read concurrently must be immutable or separately synchronized; and writers need their own serialization/linearization protocol. A grace period protects lifetime but does not turn a multi-node traversal into a transactional snapshot.

### Critical invariants

1. A reader enters the correct RCU domain before acquiring protected pointers and exits after its last access.
2. Protected references do not escape the read-side section without conversion to independent ownership.
3. A new node/version is fully initialized before release-capable publication.
4. Readers subscribe with the domain's prescribed dependency/acquire semantics before consuming fields.
5. Removal closes every protected acquisition path for future readers.
6. Pre-existing readers retain a valid old path/version through their section.
7. Reclamation/reuse occurs only after a grace period covering the removal.
8. Concurrent writers are serialized or composed by a separate correct update protocol.
9. Mutable fields use immutability, atomics, locks, sequence counters, or another explicit rule.
10. Callback backlog, quiescence lag, cancellation, CPU/thread/task lifecycle, and domain destruction are bounded and observable.

### Common failures

- Publishing a pointer before finishing initialization.
- Using an ordinary load/store where the RCU implementation requires accessors/order.
- Returning an RCU-protected pointer beyond the critical section.
- Reclaiming after unlink without waiting for pre-existing readers.
- Clearing old links that a paused reader still needs for traversal.
- Assuming readers see one coherent snapshot of all nodes/fields.
- Assuming RCU serializes competing writers.
- Mutating reader-visible fields in place without synchronization.
- Blocking indefinitely or reporting false quiescence while retaining pointers.
- Unloading code/domain while deferred callbacks can still execute.

### Compact example

Reader R enters and loads V0. Writer constructs V1, publishes it, and retires V0. A new reader sees V1, but V0 cannot be reclaimed while R is active. R continues safely on V0 and exits; the grace period completes and reclaims V0. The publication point orders versions, while the grace period establishes only lifetime eligibility.

### Connections

[DSE-068](068-hazard-pointers-and-epoch-reclamation.md) supplies grace and reclamation foundations. [DSE-067](067-aba-avoidance.md) supplies reuse/identity cautions. [DSE-064](064-concurrent-skip-lists.md) supplies weak traversal and logical removal. The [program roadmap](../ROADMAP.md) next develops linearizability testing before moving to external-memory structures.

## Governing Question

Under what representation, publication, reader-scope, update-serialization, grace-period, reclamation, and lifecycle assumptions does an RCU-protected list, tree, table, or snapshot implement its declared concurrent semantics?

## Why This Matters

Read-mostly structures occur everywhere: routing and policy tables, process registries, filesystem metadata, caches, configuration snapshots, network classifiers, subscriber lists, and service discovery. Reader-writer locks can make their lifetime proof straightforward, but every reader still touches shared lock state and can participate in contention, cache-line traffic, or writer delay. RCU moves much coordination to updates and reclamation so readers can be exceptionally light.

That benefit is bought with temporal coexistence. Old and new versions remain valid simultaneously. A writer's update is not complete operationally when it changes the root: it must preserve paths for readers already inside, arrange grace-period reclamation, and manage backlog. Readers do not automatically block writers; writers do not automatically serialize each other. RCU is as much a representation discipline as a primitive.

The name “read-copy-update” is a conceptual pattern, not a command to copy the whole structure for every mutation. A writer may replace one node, splice a list entry, publish a new immutable root with structural sharing, or build a full snapshot. The amount copied determines update cost and reader consistency. The stable theorem is that future readers cannot acquire the removed version through protected paths, while pre-existing readers may finish before reclamation.

Misuse tends to survive ordinary tests. A returned pointer works until memory is reused. A missing publication barrier appears only on weak hardware or compiler transformations. A list traversal seems snapshot-like until overlapping changes create a legal mixture. Deferred callbacks accumulate quietly until memory pressure or shutdown. Production-grade RCU therefore requires explicit semantic and operational contracts.

## Prerequisites and Retrieval

Retrieve atomic pointer publication, acquire/release, immutable data, linked traversal, linearization, progress classes, ABA, and reclamation. From [DSE-068](068-hazard-pointers-and-epoch-reclamation.md), retrieve removal-versus-reclamation, read-side intervals, quiescence, grace periods, callback/destructor cost, and stalled-reader retention. From [DSE-067](067-aba-avoidance.md), retrieve incarnation reuse and the fact that lifetime safety does not prove identity or unchanged membership.

Understand that RCU APIs and guarantees vary by domain: Linux classic/preemptible/SRCU, userspace QSBR, and standard-library domains have different nesting, blocking, scheduling, and ordering rules. Use a published implementation's exact contract. The executable artifact below is a bounded version-lifetime model, not an implementation of any RCU flavor.

## Learning Objectives

After completing this module, you can:

1. derive RCU replacement from an immutable versioned representation;
2. distinguish publication/subscription from grace-period ordering;
3. specify reader entry, pointer scope, and ownership escape rules;
4. identify update and reclamation linearization/lifetime events;
5. explain why weak traversal is not a snapshot;
6. design insert, delete, replace, and mutable-field policies;
7. compare classic, preemptible, QSBR, SRCU, and standard-library domains;
8. diagnose callback backlog, stalled readers, false quiescence, and unload races;
9. separate reader, updater, grace, callback, and memory progress; and
10. build litmus, history, lifetime, fault, and workload evidence.

## Core Exposition

**Start with a sequential contract.** For a map or list, specify lookup/traversal and insert/delete/replace results, uniqueness, order, and empty behavior. Then state the concurrent observation contract. A point lookup might be linearizable at a root/link load plus validation. An iteration might be weakly consistent: it need not duplicate elements and may see some but not all overlapping changes. If callers require a transactionally consistent snapshot across keys, basic RCU traversal is insufficient; publish an immutable whole snapshot/version or add version validation.

**Separate four jobs.** RCU design has at least four distinct mechanisms:

1. **reader delimitation** says which old references may exist;
2. **publication/subscription** orders initialization and pointer consumption;
3. **update synchronization** defines how writers preserve structure and abstract semantics;
4. **grace/reclamation** delays destruction/reuse.

An RCU read lock often is not mutual exclusion. A grace-period wait is not a publication barrier for incorrectly initialized nodes. A writer lock does not make old-reader lifetime safe after unlock unless deletion also waits/defers. Review each job independently.

**Derive copy-and-replace.** Root initially points to V0. Writer W allocates V1, copies or derives stable state from V0 under appropriate writer synchronization, applies changes privately, then publishes V1 in one atomic pointer update with release semantics prescribed by the domain. That pointer update is a natural linearization point for a whole-snapshot replace. W then retires V0 and either waits synchronously for a grace period or queues a callback.

Reader R enters, subscription-loads root, accesses immutable/stable fields, and exits. If R loads V0 before publication, it may continue on V0. If it loads V1 after publication, acquire/dependency ordering exposes V1's initialization. Once root no longer exposes V0, readers starting later cannot newly acquire it from root. The grace period waits only for readers that might already hold it; readers starting after removal need not delay V0.

**Do not overgeneralize pointer atomicity.** An atomic root update ensures readers get an old or new pointer value, not that the object graph behind it is consistent. Every field reachable from V1 must be initialized/published, and every retained shared child needs a valid lifetime. Structural sharing can reduce copy cost, but reclamation must account for shared ownership. If V1 points into mutable V0-owned storage that is freed with V0, the root theorem is false.

**Publish and subscribe correctly.** In Linux terminology, publication and dereference accessors encode compiler and hardware requirements in addition to pointer atomicity. In a language library, release store/CAS and acquire load may provide the corresponding edge. Do not replace a domain accessor with a plain/relaxed operation because it looks equivalent on one architecture. Likewise, do not infer that a grace-period API publishes earlier ordinary writes unless its contract says so.

Initialization must finish before publication. After publication, fields promised immutable cannot be mutated in place. Reader-visible mutable fields need atomics, a lock, a sequence counter, or a replace-with-new-version rule. RCU prevents the object's storage from disappearing; it does not make data races or torn compound state legal.

**Insert into a linked structure.** Initialize new N, including its successor link, before publishing the predecessor/root link to N. Readers that see N must also see initialized fields and a valid continuation. The publish link can linearize insertion if writer coordination ensures it connects to the correct current predecessor and satisfies uniqueness/order. A writer mutex is common and compatible with lockless RCU readers; “RCU” does not imply lock-free writers.

**Delete from a linked structure.** Writer first logically removes/unlinks D so future readers following protected links cannot acquire D. The unlink can linearize deletion. But a pre-existing reader may be at D or its predecessor and still traverse links from the old path. Keep D and any required continuation state valid until a covering grace period. Then reclaim or schedule destruction. Some RCU list primitives deliberately preserve traversal-relevant links; generic pointer-clearing after unlink can break paused readers.

Deletion semantics for an iterator are contract-specific. Linux's RCU list documentation describes which pre-existing elements are guaranteed and allows overlapping changes to be seen or not seen. Never infer a universal iteration guarantee from lifetime safety. Duplicates, omissions, ordering, and replacement visibility must be proved from the exact update primitives.

**Replace one node.** Construct N with the desired stable fields and appropriate links. Atomically replace the protected link from old O to N. A reader may see O or N depending on its timing. If the update primitive guarantees a reader sees exactly one of old/new at that position, document it; otherwise validate. O remains intact until grace. For identity-sensitive lookup, key fields should usually be immutable; otherwise readers can find an object whose key changed under them despite safe lifetime.

**Serialize writers.** Two writers copying from V0 can each publish derived V1/V2 and lose one change if they use plain stores. Use a writer mutex, CAS retry against the current root, serialized update queue, transaction/merge logic, or another proven scheme. The publication order supplies whole-version linearization only if each version derives from the state it validly replaces. Writer lock ordering, allocation failure, and cancellation before/after publication need policy.

Readers may be extremely scalable while updates are expensive. Copy cost can be `O(n)`, a grace wait can be long, and queued callbacks can grow. This is often acceptable for read-mostly workloads; it is not a universal replacement for a concurrent mutable structure.

**Understand grace-period logic.** A grace period associated with removal at time `t_r` must cover every read-side critical section that began early enough to have acquired the old path and had not ended by the grace start/observation rules. It does not require the system to have no readers at one instant. Readers can overlap continuously if the implementation can establish that each old reader individually quiesced.

Different implementations recognize quiescence differently: context switches/user-kernel transitions, explicit QSBR reports, per-thread counters/generations, or domain-specific tracking. Preemptible RCU accounts for readers suspended in a critical section. QSBR can make read paths minimal but requires trustworthy periodic reports and forbids retaining protected pointers across reported quiescence. SRCU permits sleepable read-side sections under its exact domain rules at higher tracking cost. Names do not substitute for API documentation.

**Synchronous versus asynchronous reclamation.** A synchronous wait such as a grace-period synchronize call blocks the updater until coverage completes, then it may destroy old storage. It must not be invoked in contexts where sleeping/deadlock is forbidden, and waiting from within a read-side section of the same domain can be impossible: the caller waits for itself to exit.

Asynchronous retirement queues a callback after grace, allowing the updater to return sooner. Callback execution is part of resource behavior. Backlog consumes memory; callback batches and destructors cause tail spikes; callbacks may run in constrained contexts. On module/plugin/domain unload, wait not only for grace periods but for queued callbacks whose code/data must remain loaded. A barrier/drain primitive has a different purpose from a normal grace wait.

**Keep protected pointers scoped.** A pointer loaded inside a read-side section cannot be cached globally, returned to an unguarded caller, captured by an asynchronous callback, or used after unlock. Convert to independent ownership while protected—perhaps increment a reference count only if nonzero and then validate identity—or copy stable data. The conversion protocol needs its own race proof.

Nesting must be supported explicitly; only the outermost exit should end protection. Task migration, coroutine suspension, signals/interrupts, and CPU hotplug depend on the RCU flavor. A userspace library may require registration tied to OS threads. Never assume a guard can cross `await`, fork, or FFI boundaries.

**RCU is not a snapshot by default.** During a list traversal, reader can observe predecessor relationships from different update moments. Lifetime remains safe, but a compound invariant may not hold. If a financial report needs all fields from one commit, publish a versioned immutable root and keep the root/version guard, or retry using a sequence/version check. If a lookup needs only one matching immutable record, weak traversal may be sufficient.

Also distinguish **existence** from **state**. RCU can guarantee a node's type/storage stays valid; it does not guarantee its status field, reference count, or external resource remains active. Acquire a stronger reference/lock and revalidate where required.

**Analyze progress and memory.** Reader overhead can be tiny, but its formal progress depends on the implementation and context. Writer publication may be lock-based. Synchronous grace waiting can block behind a stalled pre-existing reader. Callback reclamation can lag. If retired byte rate is `λ` and effective grace/backlog delay is `T`, retained exposure is roughly `λT` plus batches and live/copy memory; no finite bound follows if T is unbounded.

Copy-based updates temporarily require both old and new versions. Full `n`-byte snapshots may approach `2n` live version memory plus outstanding generations; multiple rapid updates can retain more than two versions. Admission, coalescing, backpressure, callback limits, and memory alarms are production requirements.

**Choose the right RCU shape.** Whole immutable snapshots give strong per-reader consistency and simple read paths at copy/memory cost. Path copying/structural sharing reduces writes but complicates shared lifetime. RCU lists support cheap weak traversal. Hash tables can replace buckets/tables and defer old arrays, but resize/version semantics need proof. Trees require rotations/path changes that preserve every old traversal path or use copy-on-write roots.

Use reader-writer locks when updates are frequent, snapshots/capacity/shutdown dominate, or the environment lacks mature RCU. Hazard pointers can precisely protect a few nodes under stalled readers. Epoch schemes generalize interval protection. Reference counting permits references to escape but adds atomic traffic and safe-acquisition complexity.

**Use a finite artifact honestly.** The model records reader R on V0, publishes V1, retires V0, and refuses grace while R is active. A later reader sees V1. After R exits, V0 becomes reclaimable.

<!-- bijux-verify: {"id":"rcu-version-grace-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"reader_R=V0:alpha\npublished=V1:beta\nreader_N=V1:beta\nretired=V0\ngrace_while_R_active=False\nold_version_still_live=True\ngrace_after_R_exit=True\nreclaimed=V0\ncurrent=V1\nreader_views_valid=True\nall_invariants=True\nevidence=finite_rcu_version_grace_model\n","stderr":""}} -->
```python
class RcuVersionModel:
    def __init__(self):
        self.versions = {"V0": "alpha"}
        self.current = "V0"
        self.readers = {}
        self.retired = []
        self.reclaimed = []

    def enter(self, reader):
        version = self.current
        self.readers[reader] = version
        return version, self.versions[version]

    def exit(self, reader):
        self.readers.pop(reader)

    def publish(self, version, value):
        assert version not in self.versions
        old = self.current
        self.versions[version] = value
        self.current = version
        self.retired.append(old)
        return old

    def grace_for(self, version):
        return version not in self.readers.values()

    def reclaim(self, version):
        assert version in self.retired and self.grace_for(version)
        self.retired = [item for item in self.retired if item != version]
        self.reclaimed.append(version)
        del self.versions[version]


model = RcuVersionModel()
old_reader = model.enter("R")
retired = model.publish("V1", "beta")
new_reader = model.enter("N")
grace_while_active = model.grace_for(retired)
old_still_live = retired in model.versions
model.exit("R")
grace_after_exit = model.grace_for(retired)
model.reclaim(retired)
reader_views_valid = old_reader == ("V0", "alpha") and new_reader == ("V1", "beta")
all_invariants = (
    not grace_while_active
    and old_still_live
    and grace_after_exit
    and model.current == "V1"
    and model.reclaimed == ["V0"]
    and reader_views_valid
)

print(f"reader_R={old_reader[0]}:{old_reader[1]}")
print(f"published=V1:{model.versions['V1']}")
print(f"reader_N={new_reader[0]}:{new_reader[1]}")
print(f"retired={retired}")
print(f"grace_while_R_active={grace_while_active}")
print(f"old_version_still_live={old_still_live}")
print(f"grace_after_R_exit={grace_after_exit}")
print("reclaimed=" + ",".join(model.reclaimed))
print(f"current={model.current}")
print(f"reader_views_valid={reader_views_valid}")
print(f"all_invariants={all_invariants}")
print("evidence=finite_rcu_version_grace_model")
```

The model gives each reader one immutable whole-version snapshot and treats method calls as indivisible. Its grace predicate tracks versions directly, unlike real RCU implementations that track read-side intervals/quiescence without knowing each pointer. It does not run threads, implement atomics/barriers/domains, model linked traversal, writer races, callbacks, arbitrary schedules, progress, or performance.

**Build evidence in layers.** Test sequential version/update semantics, then deterministic readers paused before/after subscription, writer publication, unlink, grace start/end, callback queue, and shutdown. Test multiple writers, failed allocation, cancellation before/after publication, nested readers, pointer escape, false quiescence, thread/task exit, callback reentrancy, and unload. Use target litmus/memory-model tools for publication and dependency/acquire paths.

Record invocation/response histories for operations that claim linearizability. For weak iteration, build an independent acceptability oracle matching the documented semantics rather than forcing snapshot linearizability. Use race/use-after-free sanitizers and bounded model checking, while recognizing coverage limits.

Benchmark against reader-writer locks, immutable reference-counted snapshots, hazard/epoch structures, and mature platform RCU. Vary read/write ratio, traversal length, copy depth, participants, preemption, NUMA, version size, mutation burst, grace lag, callback/destructor cost, and memory cap. Report reader/update latency percentiles, throughput, publication retries/lock time, grace duration, oldest reader, queued callbacks/bytes, peak coexisting versions, allocator cost, and fairness.

## Definitions and Notation

Let atomic protected root be `R`. Version `V_i` is fully initialized before publication. A reader interval is `[enter_p,exit_p]`; `View(p)` is the version/path acquired using prescribed subscription within it. Update publication `pub_i` replaces an acquisition path to old `V_o` with new `V_i`; retirement `ret_o` follows removal.

Pre-existing reader set for a removal is `P_o={p | p may have acquired V_o before removal and has not quiesced under the domain's rules}`. Grace predicate is `G_o ≡ P_o=∅`. Only when `G_o` holds may storage exclusively owned by V_o be destroyed/reused. New readers that cannot acquire V_o are not members merely because they overlap the wait.

For whole immutable versions, abstract state can linearize at `pub_i`. For a linked structure, `lp(op)` is the operation-specific publish/unlink/CAS/lock-protected event, not the grace period. Grace is a lifetime event without abstract insertion/deletion effect.

Let retired rate be `λ_n` nodes/s or `λ_b` bytes/s, grace/callback delay `T_g`, queued bytes `B_q`, coexisting versions `K_v`, reader latency `L_r`, update latency `L_u`, and callback/destructor time `D_c`. These are empirical unless bounded assumptions make them formal limits.

## Mechanisms, Invariants, or Proof Structure

### Reader/publication proof

1. Writer fully initializes a private new node/version and all owned reachable state.
2. Prescribed release-capable publication makes it reachable in one valid structural transition.
3. Reader enters before prescribed subscription and consumes fields only after the corresponding acquire/dependency guarantee.
4. Stable fields remain immutable or use separate synchronization.
5. Reader releases every protected reference before exit or converts it through a proved ownership protocol.

### Removal/grace proof

1. Writer closes every protected acquisition path to old O in a structurally valid update.
2. Readers beginning after removal cannot newly acquire O through those paths.
3. O and traversal-required links remain valid for pre-existing readers.
4. Grace completion proves every such reader passed quiescence.
5. Only then do destructor/reuse and callback/code unload become eligible.

### Abstract-correctness proof

1. Define operation-specific points at publication/unlink, not at grace.
2. Serialize or CAS-compose concurrent writers so each update derives from a valid current state.
3. Prove lookup/iteration visibility from exact link/version rules.
4. State weak consistency where a mixed traversal is legal; require version/snapshot mechanisms otherwise.
5. Separately prove mutable-field, identity, and ownership conversions.

### Evidence ladder

1. Sequential and concurrent observation contract, including iteration.
2. Publication/subscription and immutable-reachability proof.
3. Finite old/new reader and grace eligibility model.
4. Controlled update, reader, grace, callback, and writer-race schedules.
5. Target memory litmus, history/model, race, and lifetime tools.
6. Nesting, escape, false quiescence, preemption, cancellation, failure, unload, and memory-pressure faults.
7. Production-shaped reader/update tails, grace lag, backlog bytes, versions, fairness, and rollback evidence.

## Alternatives and Trade-Offs

| Design | Reader model | Main advantage | Principal cost/risk |
|---|---|---|---|
| Whole-snapshot RCU | one immutable root/version | strong per-reader version consistency | copy and coexisting-version memory |
| Path-copy RCU tree | immutable changed paths | less copying | shared-subtree lifetime complexity |
| RCU linked list | protected weak traversal | very cheap read-mostly iteration | mixed views, careful links/deletion |
| QSBR userspace RCU | explicit quiescent reports | minimal read overhead | false/missing reports and stalls |
| Preemptible RCU | tracked suspended readers | fits preemptive environments | implementation complexity |
| SRCU/domain RCU | domain-specific sleepable readers | flexible read contexts | greater read/domain overhead |
| Hazard pointers | named-node guards | stalls retain fewer unrelated nodes | publications, slots, scans |
| Atomic shared/reference count | escaping owned references | natural lifetime transfer | count traffic, acquisition/cycles |
| Reader-writer lock | mutual exclusion | simple snapshot/update/shutdown | reader shared state and blocking |
| Sequence lock | retrying snapshot-like readers | cheap writer/consistent copies | reader retries, no pointer lifetime alone |

RCU excels when reads dominate, readers can remain scoped, and update/copy/backlog costs fit explicit bounds. It is a poor default when writes dominate, readers must retain arbitrary pointers, strong multi-object snapshots are required, or no mature domain matches the scheduler/lifecycle.

## Failure Modes and Misconceptions

- **“RCU is just delayed free.”** It also requires read-side delimitation and publication/subscription ordering.
- **“The name requires copying the whole structure.”** replacement granularity is design-specific.
- **“Atomic pointer store publishes every field.”** only with the required memory-order/accessor chain.
- **“Read lock excludes writers.”** RCU readers and writers normally overlap.
- **“RCU serializes writers.”** use a writer lock, CAS retry, or another update protocol.
- **“Grace period is the update's linearization point.”** abstract effect usually occurs at publish/unlink.
- **“A grace wait requires zero readers simultaneously.”** it needs all relevant pre-existing readers to quiesce.
- **“Lifetime safety gives a snapshot.”** linked traversals can observe legal mixed states.
- **“Old node fields can be cleared after unlink.”** paused readers may still follow/read them.
- **“Protected pointer can be returned.”** it expires at read-side exit absent ownership conversion.
- **“Mutable fields are safe because the node lives.”** lifetime does not prevent data races or semantic inconsistency.
- **“QSBR timeout permits forced quiescence.”** a paused participant may resume with old pointers.
- **“Asynchronous callbacks make updates free.”** backlog, destruction, context, and unload remain.
- **“One grace wait drains all callbacks.”** callback barriers/drains have distinct contracts.
- **“Fast readers imply bounded memory.”** grace/backlog delay can retain arbitrarily many versions/nodes.

## Worked Examples

### Example 1

**Situation.** Writer initializes V1 payload after publishing root V1.

**Reasoning.** A reader can subscribe to V1 before initialization completes and observe partial/default state. Build privately, then release-publish; consume through the domain accessor/acquire path.

**Conclusion.** Publication ordering is part of RCU safety, not an optimization.

### Example 2

**Situation.** R holds V0, W publishes V1 and immediately frees V0.

**Reasoning.** Publication prevents new root acquisitions of V0 but does not revoke R's local reference. W must retire and wait/defer through a grace period covering R.

**Conclusion.** Removal closes future acquisition; grace excludes earlier acquisition.

### Example 3

**Situation.** Two writers both copy V0; one adds A and publishes V1, the other adds B and stores V2.

**Reasoning.** V2 derived from stale V0 and can erase A. Serialize writers or CAS root expected V0; on CAS failure, rebuild/merge from current V1.

**Conclusion.** Reader safety does not prevent lost writer updates.

### Example 4

**Situation.** A reader iterates an RCU list while writers replace X and insert Y.

**Reasoning.** Depending on exact primitives/timing, reader may see old or new X and may or may not see Y. Lifetime can be safe without a single-time list snapshot. Validate against the declared weak contract.

**Conclusion.** RCU iteration semantics must be stated independently from reclamation.

### Example 5

**Situation.** Delete unlinks D then sets `D.next=null` before grace.

**Reasoning.** A pre-existing reader positioned at D may need the old next link to continue. Clearing it changes that reader's path. Preserve traversal-required fields until grace or use a proved update primitive.

**Conclusion.** Retired nodes can remain semantically useful to old readers.

### Example 6

**Situation.** Lookup returns raw pointer P after leaving the RCU read section.

**Reasoning.** Updater can complete grace and free P immediately after exit. Copy stable data or acquire an independent reference while protected and validate the conversion.

**Conclusion.** RCU pointer lifetime is guard-scoped.

### Example 7

**Situation.** A QSBR participant reports quiescence but keeps a cached node pointer for its next request.

**Reasoning.** Reclaimer may free the node because the report asserted no old references. The next request dereferences freed storage. Cache owned data/reference or do not report until release.

**Conclusion.** Quiescence is a semantic promise, not a heartbeat.

### Example 8

**Situation.** Updater calls synchronous grace wait from inside a read-side section of the same non-recursive domain.

**Reasoning.** The wait needs the caller's pre-existing section to end, but caller cannot exit until wait returns: self-deadlock or prohibited use. Retire asynchronously or exit before waiting per API.

**Conclusion.** Grace waits have context and nesting restrictions.

### Example 9

**Situation.** Plugin unload waits for one grace period but leaves queued callbacks pointing into plugin code.

**Reasoning.** A callback can execute after code unload. Use the domain's callback barrier/drain, stop new retirement, and prove no callback/object/domain reference remains.

**Conclusion.** Grace coverage and callback-queue drainage are different lifecycle gates.

### Example 10

**Situation.** Whole-snapshot RCU publishes 4 GiB versions every second; grace delay reaches five seconds.

**Reasoning.** Multiple 4 GiB old versions plus the current build can coexist, exceeding a simple two-version assumption. Coalesce/rate-limit, path-copy safely, cap backlog, or select locks/different storage.

**Conclusion.** Copy and grace lag must fit a byte-level admission policy.

## Cross-Program Connections

- **Concurrent and Parallel Programming:** memory ordering, quiescence, scheduler/preemption, writer serialization, and progress establish the execution model.
- **Operating Systems:** kernel RCU, CPU idle/hotplug, interrupts, preemption, module unload, and deferred callbacks are core applications.
- **Database Engineering:** MVCC readers and vacuum resemble coexisting versions and oldest-reader retention, though transaction snapshots add different semantics.
- **Distributed Systems:** immutable configuration/routing snapshots and grace/drain deployment resemble version publication, but network consensus is separate.
- **Security Engineering:** use-after-free, stale identity, false quiescence, backlog exhaustion, callback-after-unload, and malformed mutable fields are attack surfaces.
- **Performance Engineering:** copy depth, reader cache traffic, update serialization, grace tails, backlog bytes, destructor batching, and NUMA determine value.

## References

1. Paul E. McKenney and John D. Slingwine, [“Read-Copy Update: Using Execution History to Solve Concurrency Problems”](https://www.cse.iitd.ac.in/~sbansal/os/previous_years/2011/bib/mckenney01read.pdf), PDCS 1998. Foundational RCU paper lineage and execution-history reasoning.
2. Linux Kernel Project, [“What is RCU? — Read, Copy, Update”](https://www.kernel.org/doc/html/next/RCU/whatisRCU.html), current kernel documentation accessed 2026-08-30. Official overview, core API, removal/reclamation, publication, and reference analogy.
3. Linux Kernel Project, [“A Tour Through RCU's Requirements”](https://www.kernel.org/doc/html/latest/RCU/Design/Requirements/Requirements.html), current documentation accessed 2026-08-30. Official grace-period, publish/subscribe, barrier, and context requirements.
4. Linux Kernel Project, [“Using RCU to Protect Read-Mostly Linked Lists”](https://cdn.kernel.org/doc/html/latest/RCU/listRCU.html), current documentation accessed 2026-08-30. Official list update and weak traversal semantics.
5. ISO C++ working draft, [RCU safe reclamation](https://eel.is/c++draft/saferecl.rcu.base), current draft accessed 2026-08-30. Primary current standard-library RCU domain/object surface.
6. Maged Michael et al., [“Read-Copy Update (RCU) for C++26”](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2545r2.pdf), WG21 P2545R2, 2023. Primary standardization rationale and interface history.
7. Paul E. McKenney, [*Is Parallel Programming Hard, And, If So, What Can You Do About It?*](https://www.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook-e1-rc2.pdf), 2023 edition candidate. Detailed RCU structures, replacement examples, and engineering context.
8. Maurice P. Herlihy and Jeannette M. Wing, [“Linearizability: A Correctness Condition for Concurrent Objects”](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf), *ACM TOPLAS* 12(3), 1990. Primary correctness framework for separating abstract effects from grace/reclamation.

## Exercises

### Exercise 1

Define RCU, read-side critical section, publication, subscription, removal, pre-existing reader, quiescent state, grace period, synchronous/asynchronous reclamation, QSBR, and weak traversal. State the central lifetime invariant.

### Exercise 2

Trace readers R1/R2 and writer W: R1 enters/loads V0; W publishes V1 and starts grace; R2 enters/loads V1; R1 exits; R3 enters; grace completes. State which readers grace waits for, legal views, abstract point, and reclamation time.

### Exercise 3

Review an RCU list whose writer publishes a half-initialized node, clears removed links immediately, allows two unsynchronized writers, mutates keys in place, and returns raw pointers. Diagnose and repair each issue.

### Exercise 4

Design a read-mostly configuration service using whole immutable RCU snapshots. Specify update serialization, publication, reader API, errors/cancellation, grace/callback policy, rate/memory bounds, metrics, and shutdown/unload.

### Exercise 5

A mutable tree requires linearizable point lookup, range snapshots, frequent updates, and references retained by asynchronous tasks. Decide whether basic RCU is suitable; propose a design and verification/rollout plan.

## Answers to the Exercises

### Answer 1

RCU permits marked readers to overlap publication/removal and defers destruction until pre-existing readers quiesce. A read-side critical section scopes protected references. Publication makes initialized state reachable with ordering; subscription obtains/consumes it safely. Removal closes future protected acquisition paths. A pre-existing reader might already hold the old object. Quiescence ends that eligibility; a grace period covers all such readers. Synchronous reclamation waits; asynchronous queues post-grace work. QSBR uses explicit quiescent reports. Weak traversal accepts defined mixtures of overlapping changes rather than a snapshot.

Central invariant: every old node/version and traversal-required field remains valid until removal has prevented new acquisition and a covering grace period proves all possible earlier readers released their references; reuse/destruction follows only then.

### Answer 2

R1 can hold V0 because it subscribed before publication. W's root publication linearizes the whole-version update to V1 and retires V0. R2 enters after publication and acquires V1; it cannot acquire V0 from root, so it need not delay V0's grace. R1 is pre-existing and must exit. R3 also starts after removal and sees V1; depending on the implementation it may overlap the grace without delaying V0.

When R1 exits and every other qualifying pre-existing reader has quiesced, grace can complete even if R2/R3 remain active on V1. Then V0 can be destroyed/reused. Legal views are R1=V0 and R2/R3=V1. The grace completion is a lifetime event, not the abstract update point.

### Answer 3

Half initialization violates publish/subscribe: initialize all fields/links privately then release-publish and use prescribed subscription. Clearing removed links can break pre-existing traversal; retain required fields through grace. Two writers can lose updates or corrupt links; serialize with a writer mutex or CAS/rebuild protocol and assign operation points. Mutable keys break lookup invariants and may race; make identity/key immutable, replace the node, or protect mutation with separately proved synchronization/validation. Raw pointers expire at read exit; copy stable values or acquire an independent reference while protected with nonzero/identity validation.

Then retire rather than free, wait/defer a covering grace period, and integrate callback drain/shutdown. Test publication litmus, writer races, paused traversal, pointer conversion, grace eligibility, allocation failure, cancellation, and lifetime tools.

### Answer 4

Expose `withSnapshot(fn)` or a non-escaping guard-bound view; each reader enters, acquire/subscription-loads one immutable root, reads only that version, and exits in structured cleanup. A single update mutex/queue loads current V, validates an input transaction, builds V′ privately, enforces size/version policy, and release-publishes root; publication linearizes success. Allocation/validation failure before publication leaves state unchanged. Cancellation after publication reports/records the committed version rather than pretending rollback.

Retire old V asynchronously to avoid updater waits, with bounded callback batches and controlled destructors; optionally provide an administrative synchronous drain. Enforce maximum snapshot bytes, update rate/in-flight generations, and admission/coalescing when retired bytes approach cap. Measure current/build/retired bytes, coexisting versions, oldest reader/grace, callback count/age/time, update/read tails, failures, and version IDs. Shutdown stops admission, resolves in-flight writer, waits for reader/domain quiescence, drains callbacks, disposes current root, and only then unloads code/domain. The reader path may have the domain's strong progress, while allocation, writer mutex, callbacks, drain, and shutdown are separately classified.

### Answer 5

Basic linked-tree RCU alone does not meet all requirements. It provides lifetime, not a range snapshot; frequent updates can create copy/backlog cost; async tasks cannot retain guard-scoped pointers. One design is an immutable persistent balanced tree published as a versioned atomic root, with reference-counted/epoch-managed snapshot handles that asynchronous tasks may own. Point lookup reads one immutable root and is linearizable at root acquisition relative to whole-root commits. Range queries retain one version handle and therefore see a consistent version. Writers serialize or CAS/rebase transactions and structurally share immutable subtrees with exact reference/reclamation accounting.

Alternatively use an MVCC/versioned lock-based tree/database index if update and retention complexity demands it. Specify snapshot expiration/admission so slow tasks cannot violate memory caps. Verify persistent-tree invariants, root/version points, writer conflicts, ownership counts/epochs, cancellation, task escape, range consistency, reclamation, and shutdown with model/history/race/lifetime tests. Benchmark read/range/update mix, retained snapshot age/bytes, copy depth, contention, tails, and NUMA against an RW-lock/MVCC baseline. Canary behind one API, monitor version/backlog/memory, and retain rollback for any consistency, memory, lifecycle, fairness, or latency regression.
