---
module_id: CONPAR-062
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 62
title: Optimistic Concurrency and Validation
status: complete
last_verified: 2026-08-29
---

# Optimistic Concurrency and Validation

## One-Page Review

### Governing question

When concurrent work proceeds without excluding every potential conflict in advance, what exactly must validation establish before results can be published safely?

### Essential definitions

- **Optimistic concurrency control (OCC)** speculates that harmful interference will be uncommon and detects it before publication rather than preventing every overlap.
- A **dependency** is an observation whose continued validity matters to the proposed result, including values, absence, collection shape, predicates, versions, and object lifetime.
- A **read set** records dependencies; a **write set** records proposed changes.
- A **validation point** is when recorded evidence is checked against concurrent state.
- The **validation window** runs from the earliest relevant observation until publication becomes irrevocable.
- A **version** distinguishes logical states of an object; equality is useful only if wraparound and identity reuse cannot impersonate the observed state.
- **Certification** decides whether an operation can join the committed serialization using its dependency and conflict information.
- A **phantom** is a newly inserted, removed, or reclassified object that changes a predicate result without changing any individually recorded member.
- **False validation** accepts a proposal whose dependencies no longer hold; **false conflict** rejects a proposal that could have committed.
- A **fallback** is a coordinated pessimistic or serialized path for attempts that cannot profitably remain optimistic.

### Central model, mechanism, or theorem

An optimistic operation has read/speculative, validation, and publication phases. It observes state and records every semantic dependency, computes private changes, then establishes a serialization order by validating those dependencies while obtaining exclusive authority over its writes. Correctness requires closing the time-of-check/time-of-use gap: no relevant conflicting publication may slip between the final successful validation and this operation's publication. If any dependency is stale, the entire attempt is discarded and recomputed from fresh state.

### Critical invariants

Tentative results are private. Each accepted observation identifies one stable logical state and live object. The dependency set is semantically complete, including negative and predicate reads. Validation and write authority jointly cover the full validation window. Publication is all-or-nothing relative to observers. Version comparison cannot be fooled by wrap or reuse. Abort releases metadata and leaks no effects. Retry recomputes rather than merely revalidating an old decision. Plain accesses, reclamation, weak-memory ordering, cancellation, fallback, and shutdown obey the same serialization contract.

### Common failures

Implementations validate a value but not the object identity; record members but not the range predicate that selected them; check versions and then publish without locking or compare-exchange; trust a counter that wraps; mutate shared caches during speculation; reuse a computed result after failed validation; use wall-clock age as correctness evidence; omit write-write conflicts; deadlock while locking write sets; allow read-set validation to race reclamation; or retry indefinitely under adversarial contention.

### Compact example

A scheduler reads `alice.version=4` and `bob.version=7`, sees Alice has less load, and proposes assigning job J to Alice. Another operation increments Alice to version 5 before publication. Comparing only the proposed new count is insufficient: the choice depended on both loads. Complete validation rejects the stale choice and recomputes; otherwise OCC can publish a decision that was never justified by one state.

### Connections

[Software Transactional Memory](061-software-transactional-memory.md) introduces transactional state and opacity. [Linearizability Proofs](058-linearizability-proofs.md) supplies the abstract-history method. The following modules deepen transactional retry/composition and conflict policy.

## Governing Question

How can an optimistic implementation prove that a speculative result still corresponds to one legal state at its serialization point, including dependencies that are absent, derived, indirect, or vulnerable to reclamation?

Validation is not “check a timestamp.” It is a proof-producing protocol. Its evidence must match the abstract operation, and its final check must be connected atomically to publication.

## Why This Matters

Optimism appears in software transactional memory, databases, versioned documents, lock-free algorithms, caches, build systems, distributed APIs with entity tags, and parallel execution engines. It can remove lock hold time from expensive computation and allow disjoint operations to proceed concurrently. When conflicts are rare and attempts are inexpensive, this is powerful.

The tempting implementation—read, compute, check one version, write—often validates the wrong proposition. A decision may depend on several fields, on the absence of an entry, on all objects satisfying a predicate, or on the continued identity of a referenced object. A version check may pass before a conflicting writer publishes. A pointer can be freed while its version is examined. A compiler or processor can reorder metadata and data observations.

Optimistic control therefore trades waiting before work for evidence and possible waste after work. It is appropriate only when the system can enumerate dependencies, keep speculative effects private, certify a serialization, contain retries, and measure when the optimism assumption stops holding.

## Prerequisites and Retrieval

Retrieve:

- abstract operations and histories from [Linearizability Proofs](058-linearizability-proofs.md);
- memory visibility from [Acquire and Release Ordering](027-acquire-and-release-ordering.md);
- ABA/identity reuse from [ABA Problems and Tagged References](054-aba-problems-and-tagged-references.md);
- object lifetime from [Hazard Pointers](055-hazard-pointers.md) and [Epoch-Based Reclamation](056-epoch-based-reclamation.md); and
- transaction metadata from [Software Transactional Memory](061-software-transactional-memory.md).

Retrieval prompt: an operation chooses the least-loaded eligible worker. List every observation that can change the answer even if the selected worker's record does not change.

## Learning Objectives

After completing this module, a learner can:

1. derive read, validation, and publication phases from an abstract operation;
2. enumerate value, identity, absence, predicate, range, and lifetime dependencies;
3. explain the validation-window and time-of-check/time-of-use obligation;
4. trace versioned validation with exclusive write authority;
5. compare incremental, commit-time, global, per-object, and multi-version validation;
6. distinguish false conflicts, false validation, and legitimate conservative rejection;
7. reason about version wrap, pointer reuse, weak memory, reclamation, and plain accesses;
8. design retry, fallback, admission, and observability policy;
9. review proofs and empirical evidence for an optimistic implementation; and
10. apply stronger review to high-consequence decisions.

## Core Exposition

### Start from the abstract decision

Suppose operation `assign(j)` selects an eligible worker with minimum load, breaks ties by identifier, and increments its load. The abstract read is not just the chosen worker's load. It includes the membership of the eligible set, every compared load and identifier, the job's unassigned status, and perhaps a capacity policy. These observations are semantic dependencies because changing any can change the legal result.

Define the operation's precondition, result, state transition, invariant, and failure. Then derive `R(T)` as the smallest evidence sufficient to justify the proposed transition. Recording less risks false validation. Recording more is safe only if conservative aborts are allowed, but creates false conflicts and reduces progress.

Dependencies can be direct values; object identity and generation; absence of a key; size or structural shape; aggregate values; predicate/range results; authorization or configuration version; and lifetime. Derived values do not replace their inputs unless the derived value itself is maintained as a versioned authoritative object.

### The optimistic phases

The classical shape has three phases:

1. **Read/speculate:** observe a snapshot or individually checked states, record dependencies, and compute tentative output privately.
2. **Validate/certify:** establish that the attempt can be ordered with relevant concurrent operations and that its dependencies still justify the output.
3. **Publish/write:** make the proposed state visible according to that established order.

These are logical phases. An implementation can validate incrementally during reads, lock write metadata before final validation, overlap certification among transactions, or publish through a single multiword descriptor. The proof must explain the actual transitions rather than force code into three superficial functions.

If validation fails, the result must be recomputed. Rechecking an unchanged selected record is not enough because the selection policy may now choose a different record. An attempt is evidence bound to observations, not a reusable command waiting for permission.

### Close the validation window

Assume T reads x at version 4, later validates that x remains 4, then writes y. If U can change x after T's check but before T's publication, T's result may be stale at every possible serialization point. This is a time-of-check/time-of-use gap.

Common closure techniques include acquiring write-set ownership before final read validation; atomically comparing and updating one versioned object; serializing certification plus publication; using a sequence counter whose odd/even protocol detects overlapping writers; or assigning timestamps and enforcing validation/order rules that make later conflicts abort or order correctly.

“Validate, then lock” is normally suspect. The lock acquisition itself creates a gap unless the validation evidence remains protected or is repeated after acquisition. “Lock, then validate” can work when locks cover every conflicting writer and acquisition cannot expose partial state. Canonical lock order or try-lock-and-abort prevents deadlock.

### Versioned-object pattern

A simple object contains immutable logical data plus a monotonically advancing version. A reader obtains a `(value,version)` pair that belongs together. A writer proposes a replacement and uses compare-exchange or a lock to require the observed version before installing a new pair. This linearizes a single-object conditional update.

Multi-object decisions need more. Lock or reserve the write set, validate all read dependencies after reservation, then publish the complete write set while readers follow a protocol that cannot accept a prefix. A global commit sequence can help order states but does not itself publish multiple words atomically. The data/metadata memory ordering must ensure an observer that accepts a new version also observes its data.

Version equality is not timeless truth. A fixed-width counter wraps; an address can be reused for a different object with the same apparent version; a replica can restart its counter; a file may be replaced while retaining a timestamp resolution. Use sufficiently wide generations with a proved non-wrap lifetime, unique identities, epochs, tagged references, or another protocol that prevents indistinguishable reuse.

### Executable validation trace

The following model records all worker versions used by a minimum-load decision. T's stale attempt is rejected even though its proposed worker still exists; retry recomputes and selects Bob. The code is deterministic and sequential. It does not implement atomic machine publication, concurrent memory ordering, reclamation, or distributed OCC.

<!-- bijux-verify: {"id":"optimistic-assignment-validation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first_choice=alice\nconcurrent_update=alice:3\nfirst_attempt=aborted\nretry_choice=bob\nretry_attempt=committed\nloads={'alice': 3, 'bob': 2}\nversions={'alice': 2, 'bob': 1}\n","stderr":""}} -->
```python
workers = {
    "alice": {"load": 1, "version": 1, "eligible": True},
    "bob": {"load": 1, "version": 0, "eligible": True},
}


def propose_assignment():
    reads = {name: record["version"] for name, record in workers.items()}
    eligible = [name for name, record in workers.items() if record["eligible"]]
    choice = min(eligible, key=lambda name: (workers[name]["load"], name))
    return {"reads": reads, "choice": choice}


def commit(proposal):
    valid = all(workers[name]["version"] == version for name, version in proposal["reads"].items())
    if not valid:
        return "aborted"
    record = workers[proposal["choice"]]
    record["load"] += 1
    record["version"] += 1
    return "committed"


first = propose_assignment()
print(f"first_choice={first['choice']}")
workers["alice"]["load"] = 3
workers["alice"]["version"] += 1
print(f"concurrent_update=alice:{workers['alice']['load']}")
print(f"first_attempt={commit(first)}")
retry = propose_assignment()
print(f"retry_choice={retry['choice']}")
print(f"retry_attempt={commit(retry)}")
print(f"loads={{'alice': {workers['alice']['load']}, 'bob': {workers['bob']['load']}}}")
print(f"versions={{'alice': {workers['alice']['version']}, 'bob': {workers['bob']['version']}}}")
```

In real concurrency the `commit` check and update need one protocol. Iterating a mutable mapping also does not validate membership; a production design needs a collection generation or predicate/range mechanism.

### Negative reads and phantoms

An insertion often depends on “key k is absent.” Recording no object records no evidence. Validate a bucket generation, index node, key-range lock/version, immutable root, or unique-key authority that changes when k can appear.

Predicates are broader. A transaction reads every order with `status=pending` and approves an aggregate. Another transaction inserts a new pending order. All recorded member versions remain unchanged, yet the predicate result is stale: the new row is a phantom. Protect or validate the index range, predicate token, collection root, or serialization mechanism that controls membership.

Checking collection size is not generally sufficient: removal plus insertion can preserve size while changing members. A global collection version is simple and conservative; partition or range versions reduce false conflicts but complicate boundary operations.

### Incremental versus final validation

Commit-time validation minimizes repeated checking, but speculative code can operate on mutually inconsistent observations before it reaches commit. Managed runtimes may sandbox some failures; unmanaged pointer traversal can access invalid memory. Opacity-oriented systems validate during reads or when a global sequence changes, use consistent snapshots, or constrain speculative operations.

Incremental validation can cost `O(|R|^2)` if every new read rescans all earlier reads. Global version filters can skip rescans when no writer committed, while per-object versions localize checks. NOrec-style designs use a small global sequence and value-based validation, trading centralized metadata and read-set scans against per-object ownership records.

Final validation is still necessary if later observations or writers can invalidate earlier checks. An optimization must preserve the proof: caching “validated” without a protecting epoch, sequence, lock, or snapshot is unsound.

### Validation order and write conflicts

Writers commonly acquire their write set before validating reads. Sorting stable ownership identities avoids cyclic waiting; alternatively failed try-lock acquisition aborts and releases all acquired metadata. Duplicate/aliased locations must collapse to one ownership record.

Read validation must treat locations also in the write set according to the algorithm: T's own lock should not look like a foreign conflict, yet the pre-lock version must still match when the operation depended on it. Blind writes that never read old state still conflict with other writers unless the abstract operation defines overwrite semantics that can be ordered safely.

Assigning a commit timestamp before a validation failure must not expose a committed transaction. Gaps in timestamps can be harmless, but status and visibility rules must be precise. A reader cannot interpret “high timestamp exists” as proof every lower transaction committed.

### Multi-version validation

Multi-version concurrency lets a reader select versions belonging to a snapshot rather than abort whenever a newer version exists. A writer still needs certification for write-write conflicts and invariants involving recent state. Snapshot isolation alone can allow write skew: two transactions read the same invariant, write disjoint objects, and both commit.

Serializable multi-version schemes track additional dependencies, validate dangerous structures, lock predicate/range authorities, or order transactions under stronger rules. Retaining versions changes abort pressure into memory and reclamation pressure. Snapshot age, oldest reader, and version bytes become safety/availability controls.

### Lifetime and weak memory

Reading a version does not protect the object containing it. Between locating an object and validating it, another thread can remove, free, and reuse the address. Hazard pointers, epochs, reference ownership, GC, immutable snapshots, or locked lookup must keep identity alive through validation. The lifetime protocol and OCC proof are inseparable.

Weak memory adds another pairing problem. Writers must publish data before releasing a metadata state that readers accept; readers acquire or otherwise order metadata before using data. Seqlock-style readers usually read sequence, copy data, then reread sequence, accepting only equal even values with specified barriers. Data races in the host language cannot be excused by a logically sound version algorithm.

### Effects, cancellation, and failure

Speculation must not leak irrevocable effects. Buffer output, emit a post-commit intent, or use an explicitly serialized irrevocable path. A retry after conflict recomputes from fresh dependencies; it cannot assume an external request was rolled back.

Cancellation before publication aborts and releases reservations. Cancellation after the serialization point may return an uncertain result: the operation could be committed even if the caller timed out. APIs need idempotency keys or status lookup where retrying the logical request could duplicate an effect.

Process failure distinguishes volatile and durable systems. A memory compare-exchange needs no recovery log for vanished process state; a database needs write-ahead logging, flush order, recovery, or another durability protocol. OCC is concurrency control, not durability by itself.

### When optimism fails operationally

Expected waste depends on conflict probability, attempt cost, and retry amplification. A 5% abort rate near transaction start differs from 5% after expensive computation. Record attempts per logical success, work lost by stage, dependency/write sizes, validation scan time, ownership failure, oldest attempt, abort cause, and fallback.

Hot keys, skew, synchronized retries, oversubscription, long readers, and adversarial input can invalidate a low-conflict assumption. Backoff can reduce collision but cannot create capacity or fairness. Partitioning, combining, queues, pessimistic locks, or serial fallback may be better. A starvation threshold can route one logical operation through a coordinated slow path; that path must exclude or order optimistic attempts correctly.

Use bounded retry/time budgets with semantics appropriate to the caller. Returning “conflict” can be valid for an editor API; silently dropping a financial update is not. Randomized delay is policy and must be reproducible or controlled in deterministic tests.

### Validation evidence

Write the sequential specification and dependency derivation. For each accepted read, prove identity, value/version pairing, and lifetime. For commit, prove exclusive authority, complete final validation, serialization point, and atomic abstract publication. For abort, prove no state/effect leakage and complete cleanup. For progress, state scheduler, contention, allocator, reclaimer, and fallback assumptions.

Test omitted-dependency mutants: skip one compared worker, one absence token, one range generation, or one alias and ensure histories fail. Use small-state model checking, adversarial barriers around every validation/publication boundary, differential execution against a serialized reference, wrap/reuse tests, weak-memory/race tools, fault and cancellation injection, and lifecycle tests.

Measure representative low-conflict, typical, skewed, saturated, overload, and fallback workloads. Compare identical semantics against competent pessimistic, partitioned, message-passing, and snapshot designs. Successful validation is evidence only for that attempt; it does not prove the validator itself correct.

## Definitions and Notation

- `R(T)`: semantic dependencies recorded by attempt T.
- `W(T)`: tentative updates proposed by T.
- `obs_T(x)`: value, identity, and version T observed for dependency x.
- `cur(x)`: current validated identity/version of x.
- `V(T)`: predicate that every required dependency of T remains compatible with its serialization.
- `L(T)`: ownership or reservation protecting T's publication set.
- `sp(T)`: T's serialization point.
- `C(T,U)`: conflict relation under the abstract operations and implementation granularity.
- `A`: attempts per committed logical operation.
- `W_lost`: speculative work discarded by aborts.

The tempting predicate `V(T) = ∀x∈R(T): cur(x)=obs_T(x)` is sufficient only if R is complete, comparison captures identity and state, validation is properly ordered, and no conflicting change can escape between validation and publication.

## Mechanisms, Invariants, or Proof Structure

### Dependency completeness

For proposed result r and transition f, show that any concurrent state change capable of changing r, f, legality, or invariant satisfaction changes at least one recorded authority in `R(T)` or conflicts with `L(T)`. This is a semantic proof, not a field-count exercise. Negative and predicate reads need explicit authorities.

### Observation validity

For every x in `R(T)`, show the observed value, identity, and version came from one stable live object. If observations are individually stable but can form a fractured snapshot, show incremental validation, a snapshot timestamp, or sandboxing establishes the required consistency condition.

### Window closure

After the final successful validation, any U whose change would invalidate T must be unable to serialize before T while publishing first. Write reservation, certification ordering, compare-exchange, or another atomic protocol must establish this. Then assign `sp(T)` and show every observer orders before or after the entire abstract transition.

### Abort and liveness

Failure of validation publishes nothing, releases all partial reservations, discards private results, unregisters wait/lifetime state, and emits no unqualified success. Repeated attempts require a stated progress policy; absence of deadlock is not absence of starvation.

## Alternatives and Trade-Offs

| Approach | Advantage | Principal cost |
|---|---|---|
| Coarse pessimistic lock | direct exclusion and small proof | blocking and serialized unrelated work |
| Fine-grained locks | concurrent disjoint work | lock order and compositional complexity |
| Per-object versions | localized validation | metadata, false sharing, multi-object publication |
| Global sequence/version | cheap change filter | centralized contention and conservative rescans |
| Immutable root/snapshot | simple consistent read identity | copy and retained-version cost |
| Multi-version OCC | long readers avoid many aborts | certification and version reclamation |
| Compare-exchange one object | compact linearization | unsuitable for arbitrary multi-object invariants |
| Owner/message queue | explicit order and effects | queueing, owner availability, backpressure |
| Hybrid optimistic/fallback | fast common path and bounded retries | coordination proof and two operational paths |

Optimism is a workload hypothesis, not a virtue. Prefer it when conflicts are sufficiently rare, dependencies are enumerable, speculation is cheap and private, and fallback is coherent.

## Failure Modes and Misconceptions

- **“No lock means no synchronization.”** Validation metadata and publication still synchronize.
- **“One version check validates the operation.”** It validates only dependencies represented by that authority.
- **“Member versions cover a query.”** Inserts and removals can create phantoms.
- **“Same value means same state.”** Identity, generation, and hidden dependencies can differ.
- **“Validate then write is atomic.”** A conflicting change can enter the gap.
- **“Large counters never wrap.”** The proof needs a bound, not optimism.
- **“Retry the old proposal.”** Failed evidence requires recomputation.
- **“Read-only never conflicts.”** It can require snapshot consistency and version retention.
- **“False conflicts are correctness bugs.”** Conservative rejection is safe but may be operationally poor.
- **“Low average abort rate is enough.”** Tail starvation and expensive late aborts matter.
- **“Backoff guarantees progress.”** It is contention policy under scheduler assumptions.
- **“A version protects memory.”** Reclamation needs a lifetime protocol.
- **“Sequence logic overrides language races.”** Host-language memory rules still apply.
- **“Timeout means abort.”** Commitment may precede response.
- **“OCC gives durability.”** Recovery is a separate protocol.

## Worked Examples

### Example 1

**Single document.** Client reads document version 8, edits privately, and conditionally replaces `(content,8)` with `(new,9)`. If version is 9, it receives conflict and merges/recomputes. **Conclusion:** one-object compare-and-set closes validation and publication when identity/version pairing is sound.

### Example 2

**Incomplete minimum.** T reads only Alice, proposes her because load is 2, but never records Bob. U lowers Bob to 1. Alice remains version-stable, so incomplete validation accepts a result forbidden by the minimum rule. **Conclusion:** validate decision inputs, not merely output targets.

### Example 3

**Absent key.** Two operations see coupon C absent and both insert it under different records. No absent object has a version. A unique-key/index bucket authority must serialize the claim. **Conclusion:** absence is a dependency requiring positive evidence.

### Example 4

**Phantom capacity.** T counts active jobs in range `[team=A,status=active]` as nine under limit ten. U inserts another matching job; member versions T saw do not change. Range/index generation validation or predicate locking is required. **Conclusion:** collection membership belongs to predicate validation.

### Example 5

**TOCTOU gap.** T validates stock version 4, U sells and advances it to 5, then T writes its sale. Without reservation or atomic compare-update, both can oversell. **Conclusion:** successful checking must be indivisible from publication relative to conflicts.

### Example 6

**Version wrap.** A two-bit version cycles `0,1,2,3,0` while T pauses. Equality with T's old zero does not mean unchanged state. Use a non-wrap bound, wider generation, epoch/identity, or retain history. **Conclusion:** version domains are proof parameters.

### Example 7

**Reused address.** T records pointer P/version 6. The object is removed, freed, and a new object at P starts version 6. Validation passes syntactically. Lifetime protection plus generation identity prevents the ABA-like substitution. **Conclusion:** validation depends on reclamation.

### Example 8

**Write skew.** Doctors A and B are both on call. T sees B on call and removes A; U sees A and removes B. Disjoint writes can both pass snapshot write-write checks, violating “at least one.” Validate/lock the invariant authority or use serializable certification. **Conclusion:** multi-version snapshots alone need not preserve predicates.

### Example 9

**Fallback coordination.** After five aborts, T takes a global fallback lock, but optimistic transactions ignore it. T still conflicts. Optimistic begin/commit must subscribe to the lock or use a shared epoch that orders paths. **Conclusion:** fallback belongs to one serialization protocol.

### Example 10

**Aircraft maintenance release.** A release decision depends on component status, signed inspections, configuration, deferred defects, software load, and authorization. Validating only the aircraft record misses revoked credentials or a newly applicable directive. The system needs versioned authorities for every approved dependency, durable evidence, explicit uncertain-result handling, and named aviation safety, maintenance-domain, security, formal-methods, data/runtime, human-factors, quality/regulatory, and operations review; none is claimed here. **Conclusion:** high-consequence validation must trace the complete safety argument, not a convenient row version.

## Cross-Program Connections

- **Databases:** OCC, predicate validation, phantoms, write skew, and recovery distinguish isolation levels.
- **Programming languages:** effect systems, exceptions, data races, and lifetime types constrain speculation.
- **Formal methods:** dependency completeness and window closure are refinement obligations.
- **Distributed systems:** conditional requests, fencing tokens, replica versions, and uncertain outcomes require scoped authority.
- **Security:** stale authorization and adversarial conflict can turn false validation or retry into vulnerabilities.
- **Performance engineering:** conflict topology and wasted work determine whether optimism pays.
- **Safety engineering:** evidence versions and named review connect technical validation to controlled decisions.

## References

1. H. T. Kung and John T. Robinson, “On Optimistic Methods for Concurrency Control,” *ACM TODS* 6(2), 1981. <https://doi.org/10.1145/319566.319567>
2. Dave Dice, Ori Shalev, and Nir Shavit, “Transactional Locking II,” DISC 2006. <https://doi.org/10.1007/11864219_14>
3. Luke Dalessandro, Michael F. Spear, and Michael L. Scott, “NOrec: Streamlining STM by Abolishing Ownership Records,” PPoPP 2010. <https://doi.org/10.1145/1693453.1693464>
4. Rachid Guerraoui and Michal Kapalka, “On the Correctness of Transactional Memory,” PPoPP 2008. <https://doi.org/10.1145/1345206.1345233>
5. Stephen Tu, Wenting Zheng, Eddie Kohler, Barbara Liskov, and Samuel Madden, “Speedy Transactions in Multicore In-Memory Databases,” SOSP 2013. <https://doi.org/10.1145/2517349.2522713>
6. Atul Adya, *Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions*, MIT PhD thesis, 1999. <https://hdl.handle.net/1721.1/9333>
7. Maurice Herlihy and Nir Shavit, *The Art of Multiprocessor Programming*, revised first edition, 2012. <https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-397337-5>
8. ISO C++ working draft, atomic operations and memory order, continuously maintained; retrieved 2026-08-29. <https://eel.is/c++draft/atomics>
9. PostgreSQL Global Development Group, “Transaction Isolation,” PostgreSQL 18 documentation; retrieved 2026-08-29. <https://www.postgresql.org/docs/18/transaction-iso.html>
10. HTTP Semantics, RFC 9110, conditional requests and validators, June 2022. <https://www.rfc-editor.org/rfc/rfc9110>

## Exercises

### Exercise 1

Define semantic dependency, false validation, false conflict, validation window, and phantom. Explain why recording more fields can improve safety yet harm progress.

### Exercise 2

T reads x version 3 and y version 8, proposes writing z, validates both, then U changes y before T writes z. Trace the failure and give two valid window-closing protocols.

### Exercise 3

An API creates a username after listing current users and validates only list length. Diagnose absence, replacement, and ABA risks; design appropriate validation authorities.

### Exercise 4

Design OCC for reserving seats satisfying `(carriage=A, accessible=true, free=true)`. Cover predicate membership, selection order, multi-seat atomicity, cancellation, retries, and fallback.

### Exercise 5

A hospital deploys optimistic validation for medication orders against allergies, interactions, lab results, formulary, and clinician authority. Specify proof obligations, failure semantics, operational evidence, and required human review.

## Answers to the Exercises

### Answer 1

A semantic dependency is any observation whose change can alter the result, legality, transition, or invariant. False validation accepts despite a stale dependency; false conflict rejects a serialization that could be legal. The validation window spans relevant observation through irrevocable publication. A phantom changes a predicate result through membership without changing recorded members. Recording a conservative global generation can cover omitted changes and improve safety, but unrelated updates also change it, causing unnecessary aborts, wasted work, and starvation. Refine authorities only with a proof that every semantic change still touches one.

### Answer 2

T's check is true at one instant, but U's y update enters before T publishes z. If z's value depended on y=version 8, no serialization after U justifies it; ordering T before U is also invalid if z publishes after U in a way visible to observers. One protocol reserves/locks z and every authority whose writer could invalidate T, then revalidates x and y before publishing and releases after publication. Another performs certification and publication under a serialization mechanism/global commit lock. For a single combined immutable state, atomic compare-exchange of the observed root to a new root also closes the window.

### Answer 3

List length does not prove a name is absent: one removal and insertion preserves length, and replacement can change membership. A reused bucket/node/version can impersonate old evidence. Use a unique-key index authority: lock/conditionally update the target key or validate a bucket/range generation changed on every membership transition. Pair logical collection identity with a nonreused generation and protect nodes through lookup/validation using ownership, epoch, hazard, or GC rules. Recheck normalization rules (case/Unicode), authorization, and uniqueness under the same serialization; publish one insert or return conflict, then recompute.

### Answer 4

Define a seat-index snapshot or range authority covering every matching seat, including inserts, accessibility/free changes, and carriage movement. Record the selection rule and versions for chosen seats; reserve all selected seat authorities in canonical order, revalidate predicate/index and chosen versions, then publish the full reservation atomically. On failure release every reservation and recompute; do not reuse the old seats. Cancellation before serialization aborts, after serialization returns committed/uncertain and uses reservation ID lookup. Bound attempts and route hot requests through a fallback that optimistic commits observe. Test phantoms, ties, partial multi-seat availability, wrap/reuse, timeout, overload, and shutdown.

### Answer 5

The abstract state includes normalized order, patient identity, active allergies, medications, dose/route, time-scoped labs, formulary/rules, clinician authorization, overrides, and audit intent. Derive a versioned authority for every dependency and prove stable identity/lifetime, consistent observation, complete validation, closed validation-publication window, one serialization point, atomic durable order/audit publication, and no speculative external dispensing. Conflicts recompute or return an explicit unresolved state; timeout cannot imply abort after commitment. Evidence includes formal/invariant review, dependency-omission mutants, bounded histories, race/weak-memory and identity-reuse tests, rule/version rollover, fault/recovery, security, representative contention, alerting, fallback, and rollback. Named pharmacy, clinical safety, prescribing, informatics, formal-methods, security/privacy, human-factors, runtime/database, operations, quality/regulatory, and independent assurance reviewers must approve requirements, evidence, overrides, fallback, and residual risk. Internal tests or this answer are not clinical approval.
