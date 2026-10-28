---
module_id: DSE-099
program: Data Structures Engineering
level: 2
module_number: 99
title: Conflict-Free Replicated Data Types as Structures
status: complete
last_verified: 2026-08-30
---

# Conflict-Free Replicated Data Types as Structures

## One-Page Review

### Governing question

How can a replicated data type encode concurrency semantics, causal metadata, merge algebra, dissemination, compaction, authorization, and invariants so replicas converge without coordination while preserving the application's intended meaning?

### Essential definitions

A **CRDT** is a replicated abstract data type designed to converge under stated delivery and failure assumptions. A state-based CRDT (CvRDT) places states in a join-semilattice; local updates inflate state and merge computes least upper bound. Merge is associative, commutative, and idempotent, so duplicate/reordered state delivery is safe. An operation-based CRDT (CmRDT) broadcasts operations whose concurrent effects commute under a delivery contract, often causal and exactly-once or deduplicated.

Strong eventual consistency means replicas that have applied the same updates have equivalent state; it does not mean linearizability, immediate visibility, invariant preservation, authorization, or automatic semantic conflict resolution.

### Central model, mechanism, or theorem

A grow-only counter stores one nondecreasing component per replica and merges componentwise maximum; its value is the component sum. An observed-remove set assigns unique **dots** to adds. Remove records only dots it observed, so a concurrent unseen add remains live. Merge unions add dots and removal context; live membership means at least one add dot is not removed.

Convergence follows from join algebra, but bounded metadata and application validity require additional causal-context, garbage-collection, membership, and coordination design.

### Critical invariants

- Replica IDs, dot/counter allocation, schema, type semantics, and encoding are stable and unique in scope.
- State order and join are defined; every local state mutation is inflationary for CvRDTs.
- Merge is associative, commutative, idempotent, and preserves well-formedness.
- Operation-based delivery assumptions and deduplication/causal dependencies are explicit.
- Add/remove, assignment, sequence, map, and nested-type concurrency semantics are named and tested.
- Tombstone/context compaction never forgets information that a delayed replica can reintroduce.
- Application invariants requiring cross-object/exclusive decisions use coordination, escrow, or a proven invariant-confluent design.
- Authorization applies to operations/provenance, not merely the converged value.

### Common failures

Failures include calling last-write-wins a universal merge, using unsynchronized wall clocks, reusing replica IDs/counters, dropping tombstones before causal stability, merging only visible set elements, applying non-idempotent operations twice, assuming network retries satisfy exactly-once delivery, confusing convergence with invariant preservation, allowing unauthorized operations because their signatures vanish after merge, unbounded dots/tombstones/version vectors, incompatible schema upgrades, and claiming CRDT text/list behavior without specifying identifiers and interleaving semantics.

### Compact example

Replica A increments its G-Counter twice and B three times; componentwise-max merge yields `{A:2,B:3}` and value 5, unchanged by duplicate merge. For an OR-Set, both initially observe add dot `A:1` for `x`; during partition A removes it while B concurrently adds `B:1`. Merge records `A:1` removed but retains live `B:1`, so `x` is present. Merge law checks pass on the finite states.

### Connections

[DSE-098](098-distributed-hash-table-data-structures.md) supplies dissemination/replica placement boundaries; [DSE-095](095-dynamic-fenwick-and-segment-structures.md) supplies algebraic and persistence reasoning. The final module is [DSE-100, “Reviewing a Data Structure from Invariants, Workload, Hardware, and Failure”](../ROADMAP.md). Distributed systems, databases, collaborative software, formal methods, security, and data engineering own delivery, transactions, user intent, proofs, authorization, and lifecycle.

## Governing Question

Which algebra, concurrency semantics, causal/delivery assumptions, metadata lifecycle, and application constraints make a CRDT correct rather than merely deterministic after one merge?

## Why This Matters

Offline and geo-replicated systems want local writes during delay or partition. Handwritten “merge JSON” code often loses updates or creates nondeterministic outcomes. CRDTs provide mathematical structure for convergence and explicit concurrent-update semantics.

But convergence is a narrow property. A converged shopping cart can violate inventory limits; a converged ACL can retain an unauthorized grant; a compacted set can resurrect deleted data. Production quality requires proof obligations from algebra through causal stability, storage, access control, schema evolution, and user-visible behavior.

## Prerequisites and Retrieval

Retrieve partial orders, lattices/join-semilattices, associativity/commutativity/idempotence, causality/happens-before, Lamport and vector clocks, unique event dots, reliable/causal broadcast, anti-entropy, eventual/strong eventual consistency, partitions, tombstones, snapshots, transactions, invariant confluence, escrow, and property/model testing.

This chapter uses logical events and explicit causal metadata. Physical timestamps may be useful metadata, but clock synchronization is not assumed and timestamp comparison alone does not recover causality.

## Learning Objectives

After this chapter, you should be able to:

1. define a state order, inflationary mutations, and least-upper-bound merge;
2. prove G-Counter and observed-remove-set convergence properties;
3. distinguish state-, delta-state-, and operation-based dissemination assumptions;
4. specify concurrent semantics for counters, registers, sets, maps, and sequences;
5. design causal stability, tombstone/context compaction, persistence, and membership safely;
6. identify invariants requiring coordination, escrow, or redesigned operations;
7. validate laws, traces, delayed replicas, schema upgrades, security, and metadata/performance curves.

## Core Exposition

### State-based semilattices

Let states form partial order (\sqsubseteq) and merge be join (\sqcup), the least state above both inputs. Local update must be inflationary: (s\sqsubseteq update(s)). Join is associative, commutative, and idempotent. If states/deltas eventually reach every replica, arbitrary duplication and reordering still converge to the join of all updates.

A G-Counter state maps replica IDs to natural numbers. Increment at replica (r) raises only component (r); merge takes pointwise maximum; query sums components. Component ownership/monotonicity is essential. A PN-Counter pairs two G-Counters for increments/decrements and subtracts sums, growing metadata while the visible value can fall.

Delta-state CRDTs emit smaller joinable fragments, but arbitrary isolated deltas may omit causal context needed by a type. Anti-entropy must satisfy the delta-interval/causal conditions of the design; “send changed fields” is not automatically a correct delta CRDT.

### Operation-based CRDTs

An operation-based design applies a prepared operation locally and delivers an effect to replicas. Concurrent effectors must commute; causally ordered operations may rely on causal delivery. Exactly-once is commonly simulated with unique operation IDs/deduplication, durable logs, acknowledgments, and replay—not promised by an ordinary network.

State and operation designs can implement similar abstract semantics with different metadata, bandwidth, persistence, and trust. Operation messages expose provenance/authorization opportunities but require delivery discipline; state merge tolerates duplicates but may send large state and obscure individual operations after compaction.

### Registers, sets, maps, and sequences

A multi-value register retains concurrent assignments and collapses values causally overwritten by later assignments. A last-write-wins register chooses a total timestamp/tie-break order, converging but discarding concurrent values according to clock/ID policy. This is one intentional semantic, not conflict disappearance.

Grow-only and two-phase sets are simple but cannot fully re-add after removal. Observed-remove sets tag adds uniquely; remove records currently observed dots. Add-wins arises because an unseen concurrent add is not removed. Remove-wins needs additional causal intent. Merging just visible elements loses the causal distinction.

Maps compose CRDT values only with a specified key-removal/nested-update policy. Sequences/text assign stable position/event identifiers and deterministically order concurrent insertions; deletion, move, formatting, cursor anchors, interleaving, and identifier growth are algorithm/application semantics. A generic array diff is not a CRDT proof.

### Causal context and compaction

Dots pair replica ID with monotonic counter. Version vectors compact contiguous observed prefixes; dotted vectors represent one event plus context. Gaps and exceptions may require additional sets. Replica-ID reuse or counter rollback makes distinct events indistinguishable and can lose updates.

Tombstones/context prevent delayed pre-removal adds from resurrecting. They can be discarded only when the system establishes causal stability: every replica that could send the old event has observed its removal or is permanently retired under an epoch/membership protocol. Offline clients make this a product retention decision. Forced retirement needs resynchronization rules that reject stale state.

Snapshots bind CRDT schema, replica/membership epoch, causal context, payload, compaction watermark, and checksum. Publication is atomic; recovery restores state and durable next-dot allocation without counter reuse. Log truncation waits until snapshot/context dominates every retained operation needed for peers.

### Invariants and coordination

CRDT convergence preserves the data type's algebra, not arbitrary application invariants. Two replicas can each reserve the last seat or withdraw under a limit while partitioned; merging produces an invalid total. Invariant-confluence analysis asks whether independently valid states merge to a valid state. If not, coordinate, partition rights via escrow, serialize a subset, or weaken/redesign the invariant.

Referential integrity across separately replicated objects, unique usernames, bounded counters, ACL revocation, and workflow state transitions need explicit analysis. Transactions can group local CRDT operations atomically, but global invariant enforcement still depends on isolation/coordination or rights allocation.

### Security and multi-tenant operation

Convergence accepts mathematically valid updates regardless of authorization unless provenance is retained/verified. Authenticate replica/user operations, namespace and schema, dot ownership, causal claims, and membership epoch. A malicious replica can invent large counters, forge dots, replay old signed operations, or inflate metadata. Signatures do not ensure semantic authorization or causal honesty without protocol checks.

Bound state, dots, exceptions, tombstones, operation logs, pending dependencies, merge CPU, recursion, document size, peers, and offline age. Per-tenant quotas, admission, rate limits, compaction, and abuse evidence are required. Encrypting transport/state does not hide metadata access patterns or solve merge authorization.

### Testing and bounded executable evidence

Law tests generate well-formed states and verify join associativity, commutativity, idempotence, inflation, and query equivalence. Trace/model tests enumerate operation orders, duplication, loss followed by anti-entropy, partitions, restart, late replicas, membership retirement, schema upgrades, and compaction. A plain centralized oracle is useful only after concurrent semantics are defined.

Benchmark local updates, merge/delta/log/snapshot bytes and CPU, anti-entropy convergence, offline catch-up, metadata per logical item/history, tombstone/context stability, compaction pause/amplification, persistence/recovery, and user-visible latency under realistic collaboration/churn.

The finite model below implements one G-Counter and simplified tombstone OR-Set. Its unique string dots are fixture data; it does not implement durable allocation or safe compaction.

<!-- bijux-verify: {"id":"state-crdt-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"gcounter_a={'A': 2}\ngcounter_b={'B': 3}\ngcounter_merged={'A': 2, 'B': 3}\ngcounter_value=5\ngcounter_idempotent=True\norset_a=[]\norset_b=['x']\norset_merged=['x']\norset_removed_dots=['A:1']\norset_live_dots=['B:1']\nmerge_commutative=True\nmerge_associative=True\nmerge_idempotent=True\nvalid=True\nevidence=bounded_state_crdt_model\n","stderr":""}} -->
```python
class GCounter:
    def __init__(self, components=None):
        self.components = dict(components or {})

    def increment(self, replica, amount=1):
        assert amount >= 0
        self.components[replica] = self.components.get(replica, 0) + amount

    def merge(self, other):
        return GCounter({
            replica: max(
                self.components.get(replica, 0),
                other.components.get(replica, 0),
            )
            for replica in sorted(self.components.keys() | other.components.keys())
        })

    def value(self):
        return sum(self.components.values())


class ORSet:
    def __init__(self, adds=None, removed=None):
        self.adds = {
            element: set(dots) for element, dots in (adds or {}).items()
        }
        self.removed = set(removed or set())

    def add(self, element, dot):
        self.adds.setdefault(element, set()).add(dot)

    def discard_observed(self, element):
        self.removed |= self.adds.get(element, set()) - self.removed

    def value(self):
        return sorted(
            element for element, dots in self.adds.items()
            if dots - self.removed
        )

    def merge(self, other):
        adds = {
            element: self.adds.get(element, set()) | other.adds.get(element, set())
            for element in sorted(self.adds.keys() | other.adds.keys())
        }
        return ORSet(adds, self.removed | other.removed)

    def normalized(self):
        return (
            tuple(
                (element, tuple(sorted(dots)))
                for element, dots in sorted(self.adds.items())
            ),
            tuple(sorted(self.removed)),
        )


counter_a = GCounter()
counter_b = GCounter()
counter_a.increment("A", 2)
counter_b.increment("B", 3)
counter_merged = counter_a.merge(counter_b)

set_a = ORSet()
set_a.add("x", "A:1")
set_b = ORSet(set_a.adds, set_a.removed)
set_a.discard_observed("x")
set_b.add("x", "B:1")
set_merged = set_a.merge(set_b)
set_c = ORSet()
set_c.add("y", "C:1")

commutative = set_a.merge(set_b).normalized() == set_b.merge(set_a).normalized()
associative = (
    set_a.merge(set_b).merge(set_c).normalized()
    == set_a.merge(set_b.merge(set_c)).normalized()
)
idempotent = set_merged.merge(set_merged).normalized() == set_merged.normalized()

print(f"gcounter_a={counter_a.components}")
print(f"gcounter_b={counter_b.components}")
print(f"gcounter_merged={counter_merged.components}")
print(f"gcounter_value={counter_merged.value()}")
print(f"gcounter_idempotent={counter_merged.merge(counter_merged).components == counter_merged.components}")
print(f"orset_a={set_a.value()}")
print(f"orset_b={set_b.value()}")
print(f"orset_merged={set_merged.value()}")
print(f"orset_removed_dots={sorted(set_merged.removed)}")
print(f"orset_live_dots={sorted(set_merged.adds['x'] - set_merged.removed)}")
print(f"merge_commutative={commutative}")
print(f"merge_associative={associative}")
print(f"merge_idempotent={idempotent}")
print(f"valid={counter_merged.value() == 5 and set_merged.value() == ['x'] and commutative and associative and idempotent}")
print("evidence=bounded_state_crdt_model")
```

The OR-Set retains removed dots forever and therefore demonstrates correctness pressure rather than a bounded production representation. Real optimized OR-Sets compress causal context and prove compaction safety.

## Definitions and Notation

- A partial order (\sqsubseteq) relates states by information content; (\sqcup) is least upper bound/join.
- A **CvRDT** is state-based with inflationary updates and semilattice merge.
- A **CmRDT** disseminates operations whose concurrent effects commute under its delivery contract.
- A **delta-state** is a joinable state fragment produced under delta-CRDT anti-entropy conditions.
- A **dot** is a unique event identifier, normally `(replica_id,counter)`.
- A **causal context** compactly records observed dots; a **tombstone** records removal/invalidated history.
- **Causal stability** means an event/context is known to all replicas that could later affect its visibility under the membership model.
- **Strong eventual consistency** combines eventual delivery/termination with convergence for equal update sets.
- **Invariant confluence** means independently valid reachable states merge to a valid state under the invariant.
- **Escrow/rights allocation** partitions bounded authority so local updates preserve a global limit.

## Mechanisms, Invariants, or Proof Structure

### G-Counter semilattice

Order component maps pointwise. Increment raises one owned component, so it is inflationary. Pointwise maximum is least above both maps and inherits associativity, commutativity, and idempotence from scalar maximum. When replicas have received the same increments, each component maximum agrees and the sum query agrees.

### Observed-remove semantics

Each add creates a unique dot. Remove adds precisely currently observed live dots to removal context. Merge unions adds and removals. Therefore a causally prior observed add is removed everywhere after delivery, while an unseen concurrent add dot survives. Set union gives merge laws; query is a deterministic projection. Optimized variants must preserve the same causal knowledge while compacting.

### Operation delivery proof obligation

For CmRDTs, effectors for concurrent operations commute; causally related operations arrive in the required order or carry enough context to delay/transform safely. Duplicate effects must be idempotent or deduplicated durably. Network retry alone proves none of these assumptions.

### Compaction safety

A removed dot can be forgotten only if no valid delayed state/operation can reintroduce it without accompanying dominating context. Establishing that fact requires acknowledgments/stability across current and retired replicas, epochs, and offline-retention rules. Local elapsed time is not a proof.

### Evidence ladder

The model checks selected merge laws and concurrent OR-Set meaning. Stronger evidence enumerates well-formed states and traces, proves algebra/type composition, model-checks delivery/compaction/membership schedules, differentially tests independent replicas, injects crash/replay/upgrade, and measures history-dependent metadata. Random final-value equality without causal histories is weak evidence.

## Alternatives and Trade-Offs

**Consensus/serializable transactions.** Coordinate to choose one order and enforce broad invariants, sacrificing some partition availability/latency. Often correct for scarce resources or security-critical transitions.

**Last-write-wins replication.** Compact and deterministic with a total timestamp/tie-break order, but silently discards concurrency according to clock policy. Appropriate only when this is intentional semantics.

**State-based CRDTs.** Duplicate/reorder-tolerant anti-entropy and simple join reasoning; full state/context can grow or cost bandwidth.

**Delta-state CRDTs.** Joinable incremental dissemination reduces bytes while retaining state-style tolerance under stricter causal delta-interval protocols.

**Operation-based CRDTs.** Small operations and provenance, but require causal/reliable/deduplicated delivery conditions and durable logs.

**OT/central collaboration.** Operational transformation with a server/total order can provide mature text-editing semantics under a different architecture and proof model.

**Application-specific merge/workflow.** Surface conflicts to users or domain resolvers instead of encoding an arbitrary automatic winner. This may best preserve intent.

**Escrow/rights CRDTs.** Partition consumable rights to preserve numeric bounds locally, adding rights-transfer and recovery complexity.

## Failure Modes and Misconceptions

1. Merge is deterministic but not associative, commutative, or idempotent.
2. A CvRDT local mutation decreases information order.
3. Visible values are merged without causal metadata.
4. Wall-clock LWW is presented as causal or semantically neutral.
5. Replica ID/counter restarts reuse dots.
6. Operation retries double-apply a non-idempotent effect.
7. Causal dependencies are delivered out of order without buffering/context.
8. Delta fragments are sent independently despite missing causal intervals.
9. Remove semantics do not specify concurrent add behavior.
10. Map key removal races with nested updates without a policy.
11. Sequence insertion ordering/interleaving is undocumented.
12. Tombstones are expired by age without causal stability.
13. Offline/retired replicas rejoin with obsolete state and resurrect data.
14. Version-vector membership grows forever without epoch policy.
15. Convergence is confused with linearizability or immediate visibility.
16. Global uniqueness/bounds/referential integrity are assumed preserved.
17. Signatures are discarded so converged state loses authorization provenance.
18. Malicious replicas forge counters/dots or inflate metadata.
19. Schema versions merge states with different semantics.
20. Small friendly histories justify bounded metadata or good user experience.

## Worked Examples

### Example 1

A increments component A from 0 to 2; B increments B to 3. Pointwise-max merge is `{A:2,B:3}`, value 5. Reapplying either state changes nothing.

### Example 2

A PN-Counter stores positive `{A:5}` and negative `{A:2}`; query is 3. Merge independently maxes positive and negative components, never the visible difference.

### Example 3

A and B concurrently assign `red` and `blue` to a multi-value register. Neither context dominates the other, so query returns both. A later assignment observing both replaces both dots.

### Example 4

An LWW register chooses `blue` because its `(logical_time,replica_id)` is larger. It converges but intentionally loses `red`; physical-clock skew could select a surprising winner.

### Example 5

Both replicas know `x@A:1`. A removes observed `A:1`; B concurrently adds `x@B:1`. Merge removes only `A:1`, leaving `B:1`, so add wins this concurrency.

### Example 6

If storage retains only visible `{x}` and then A's empty set overwrites B's `{x}`, it cannot distinguish causal removal from missing delivery. Dots/context carry the needed history.

### Example 7

A tombstone for `A:1` is deleted before offline C returns with the original add. C's merge can resurrect `x`. A stability proof or forced full resync is required before compaction.

### Example 8

Two partitions each sell the final seat based on local counter value. A convergent counter correctly totals two sales but violates capacity one. Coordinate or distribute one escrow right.

### Example 9

A signed add is authorized at creation, then the user is revoked. Whether later replay/merge remains valid depends on epoch/revocation semantics; mathematical join alone cannot answer.

### Example 10

Schema v1 defines concurrent set add/remove as add-wins; v2 defines remove-wins. Merging without a typed migration combines incompatible algebras even if bytes parse. Upgrade the state/protocol explicitly.

## Cross-Program Connections

- **Distributed Systems:** causality, anti-entropy, partitions, delivery, membership, and stability.
- **Database Engineering:** isolation, transactions, materialized views, indexes, constraints, repair, and durability.
- **Collaborative Software:** user intent, presence, undo, text interleaving, cursors, and offline UX.
- **Formal Methods:** semilattices, refinement, invariant confluence, model checking, and property testing.
- **Security:** operation authorization, provenance, revocation, malicious replicas, metadata DoS, and privacy.
- **Data Engineering:** schema evolution, replay, event logs, compaction, lineage, and backfills.

## References

1. Marc Shapiro et al., [“Conflict-Free Replicated Data Types”](https://perso.lip6.fr/Marc.Shapiro/papers/2011/CRDTs_SSS-2011.pdf), *SSS*, 2011. Author-hosted foundational state/operation CRDT paper.
2. Marc Shapiro et al., [INRIA Research Report RR-7687](https://hal.inria.fr/inria-00609399/document), 2011. Full formal CRDT report with proofs and data types.
3. Paulo Sérgio Almeida, Ali Shoker, and Carlos Baquero, [“Delta State Replicated Data Types”](https://arxiv.org/abs/1603.01529), 2018. Primary delta-state framework and anti-entropy conditions.
4. Annette Bieniusa et al., [“An Optimized Conflict-free Replicated Set”](https://arxiv.org/abs/1210.3368), 2012. Primary optimized observed-remove set work.
5. Nuno Preguiça, Carlos Baquero, and Marc Shapiro, [“Conflict-Free Replicated Data Types: An Overview”](https://arxiv.org/abs/1806.10254), 2018. Developer/system/type-design overview.
6. Carlos Baquero et al., [“Composition in State-based Replicated Data Types”](https://bulletin.eatcs.org/index.php/beatcs/article/view/507), *BEATCS*, 2020. Semilattice composition and practice.
7. Martin Kleppmann et al., [“Local-First Software”](https://www.inkandswitch.com/essay/local-first/local-first.pdf), *Onward!*, 2019. Primary local-first collaboration context and practical boundaries.

## Exercises

### Exercise 1

Given G-Counter states A=`{A:4,B:1}`, B=`{A:2,B:5,C:1}`, and C=`{C:3}`, compute both parenthesizations of the join, prove equality, and give the query value.

### Exercise 2

Construct an OR-Set trace with two concurrent adds, one remove observing only one add, duplicate/reordered state delivery, and a later re-add. Show add/removal dots, visible values, and all merge-law obligations.

### Exercise 3

Design an operation-based multi-value register. Specify prepare/effect, dot/context, causal broadcast/dedup assumptions, concurrent semantics, persistence, retry, and compaction.

### Exercise 4

Design bounded tombstone/context collection for devices that may be offline 30 days and can be permanently retired. Define epochs, acknowledgments/stability, snapshot/resync, counter allocation, crash recovery, and stale-device rejection.

### Exercise 5

Analyze a replicated inventory with stock 100, returns, orders, cancellation, and regional offline operation. Identify which invariants are merge-closed and design coordination/escrow plus a validation campaign.

## Answers to the Exercises

### Answer 1

Pointwise max of A and B is `{A:4,B:5,C:1}`; joining C raises C to 3, yielding `{A:4,B:5,C:3}`. Joining B and C first gives `{A:2,B:5,C:3}`, then A again yields `{A:4,B:5,C:3}`. Both equal because scalar max is associative componentwise; value is (4+5+3=12). Commutativity/idempotence follow componentwise as well.

### Answer 2

A creates `x@A:1`; B concurrently creates `x@B:1`. C receives only A's state and removes x, recording removed `{A:1}`. Merge B/C has adds `{A:1,B:1}` and removed `{A:1}`, so x remains via B:1. Duplicate/reordered merges do not change unions. After all replicas converge, A re-adds `x@A:2`; adds gain A:2 and x remains. Verify union merge associativity/commutativity/idempotence, local add/remove inflation of information state, unique dots, and query equivalence for every delivery order. A remove after observing all three live dots would record each; it must not invent removal of unseen future dots.

### Answer 3

Prepare assignment creates durable unique dot `(replica,next_counter)`, value, and current causal context; persist counter allocation before emission. Effect retains the new dotted value, removes values whose dots are dominated by its context, and retains concurrent values. Delivery must preserve causal predecessors or buffer until context is satisfied; unique operation IDs and durable seen/context state deduplicate retries. Local apply uses the same effect. Snapshot binds schema, values, causal context, membership epoch, and next counter; recovery cannot reuse dots. Compact dominated dots into version-vector prefixes only after every retained delivery/replay path is covered; retired replicas must resync. Query returns the deterministic set of concurrent values, not an arbitrary winner.

### Answer 4

Assign stable replica IDs and durable monotonic counters within membership epoch. Each active replica acknowledges causal version-vector frontiers through anti-entropy. A dot/tombstone is stable only when every active member's acknowledged frontier dominates it and no retained log/snapshot can emit an undominated copy. Keep at least the 30-day offline window; permanent retirement is a committed epoch change that excludes the ID and sets a minimum accepted snapshot/frontier. Returning retired/stale devices cannot merge old state: they fetch an authenticated compacted snapshot, receive a new identity/epoch, and rebase/re-author local user work through explicit operations. Publish snapshots and compaction watermarks atomically; persist counters before use; recovery verifies schema/epoch/context and resumes above the durable high-water mark.

### Answer 5

Nonnegative grow-only totals and append-only audit events merge naturally. Stock bound `accepted_orders - cancellations <= initial + accepted_returns` is not preserved when regions independently spend the same availability. Allocate escrow rights totaling available stock; a region accepts orders only by consuming local rights, returns/cancellations replenish rights under idempotent event IDs, and rights transfers require a protocol preventing duplication. Coordinate SKU creation/unique identifiers and policies whose transitions are non-confluent. Test all small concurrent traces/model-check the bound, duplicate/reorder/loss plus anti-entropy, partition/offline/restart, transfer crash, cancellation/return races, malicious/duplicate events, epoch retirement, compaction, and schema upgrades. Differentially recompute from the immutable authorized event ledger and measure rights starvation, coordination latency, metadata, convergence, and repair.
