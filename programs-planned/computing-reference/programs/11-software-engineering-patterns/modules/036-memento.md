---
module_id: SEPAT-036
program: Software Engineering: Patterns
level: 1
module_number: 36
title: Memento
status: complete
last_verified: 2026-08-28
---

# Memento

## One-Page Review

### Governing question

How can an object's meaningful state be captured and later restored without exposing its representation, while identity, compatibility, history branching, external effects, confidentiality, durability, and recovery limits remain explicit?

### Essential definitions

- The **originator** owns state and alone creates/interprets its mementos.
- A **memento** is an opaque state capture sufficient for a declared restoration contract.
- The **caretaker** stores/selects mementos but does not inspect or mutate their encapsulated representation.
- A **snapshot** records state at a logical point; a **delta** records a change relative to a base.
- **undo** restores a prior application state under declared assumptions; **redo** reapplies a branch retained after undo.
- **observational equivalence** means restored state behaves the same for specified observations, not necessarily that its bytes/object addresses match.
- A **checkpoint** is a durable recovery point coordinated with persistence/log boundaries.
- **compensation** is a new action that addresses an already observed external effect; it is not memento restoration.

### Central model, mechanism, or theorem

Let capture $C_v:S_v\to M_v$, restore $R_{v\to w}:S_w\times M_v\to S_w\cup Error$, and observables (Obs). Under ownership, integrity, compatibility, and invariant assumptions,

$$
Obs(R(C(s)))=Obs(s).
$$

This round-trip law is scoped to the captured state and supported observables. It does not reverse external messages, payments, physical actions, elapsed time, concurrent writes, or data that was intentionally excluded.

### Critical invariants

- Only the originator defines capture/restore representation and validates restored state.
- A memento binds originator identity/type, schema version, logical revision/base, and integrity/provenance as required.
- Captured mutable state is owned/immutable or structurally shared under a proven lifetime discipline; no accidental alias mutates history.
- Restore is atomic for the originator's invariant or fails without partial application.
- Undo/redo cursor and branch semantics are explicit; a new edit after undo handles the abandoned future deliberately.
- External effects, authority, and concurrent state are reconciled or compensated, never claimed rolled back by local restoration.
- Durable captures are crash-consistent with logs/references and have tested migration/recovery paths.
- Sensitive mementos are minimized, access-controlled, integrity-protected, encrypted where required, retained, and destroyed by policy.

### Common failures

Common failures include exposing all private fields, shallow-copy aliases, capturing caches/locks/sockets, restoring a memento into the wrong object, ignoring schema/code version, accepting untrusted serialized classes, partial restore before validation, unbounded history, redo surviving a divergent edit accidentally, calling compensation rollback, overwriting concurrent work, storing plaintext secrets, using snapshots as an audit log, assuming an in-memory memento survives a crash, mismatching checkpoint and write-ahead log, and treating one process snapshot as a consistent distributed state.

### Compact example

A text editor captures immutable owner/schema/revision/text/cursor state before each edit. Two undos restore revisions one and zero; redo restores revision one; a new edit clears the abandoned redo branch. The caretaker never reads the text/cursor representation directly.

### Connections

[SEPAT-035](035-mediator.md) coordinates stateful collaborators; [SEPAT-037](../ROADMAP.md) distributes change notifications. Memento connects to [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

Which state is necessary and sufficient to restore a meaningful prior behavior, who may interpret it, and what cannot be reversed because it lies outside the originator's state boundary?

Memento preserves encapsulation by moving state through an opaque value. The difficult work is not copying fields; it is defining the recovery boundary, compatibility, history algebra, resource/security policy, and honest treatment of the outside world.

## Why This Matters

Editors, games, planners, simulations, optimizers, transactional objects, debuggers, and workflow tools need undo, trial branches, or checkpoints. Reconstructing state through public operations may be slow or impossible; exposing internals to history managers makes representation changes dangerous.

Snapshots also amplify risk. They can retain secrets and large object graphs, resurrect invalid old assumptions, pin storage versions, conflict with concurrent work, and create false confidence about durable recovery. A precise memento is a contract, not a universal time machine.

## Prerequisites and Retrieval

You should understand encapsulation, object identity, invariants, immutable values, copying/aliasing, serialization, transactions, logs, concurrency control, encryption, and recovery. Retrieve these facts:

1. Object representation can differ while specified observable behavior remains equivalent.
2. A shallow copy duplicates references, not the referenced mutable objects.
3. Restoring one object cannot erase effects already observed by another authority.
4. Undo/redo is a branching history, not merely two stacks without semantics.
5. Durable recovery needs an atomic relationship among checkpoint, log, metadata, and acknowledged writes.
6. A consistent global state in a distributed system cannot be inferred from unrelated local snapshots.

## Learning Objectives

After completing this module, you should be able to:

- define originator, memento, caretaker, and restoration observables;
- design opaque immutable captures without representation leakage;
- compare full snapshots, deltas, commands, event logs, and persistent structures;
- specify undo/redo branching and capacity policy;
- validate owner, revision, schema, integrity, and invariants before atomic restore;
- separate local restoration from concurrency resolution and external compensation;
- design durable, secure, migratable checkpoint/recovery mechanisms;
- test round trips, aliasing, history, migration, crash, corruption, and resource bounds.

## Core Exposition

### Define the restoration contract first

List the observations that must be restored: rendered document and cursor, game board and deterministic generator state, optimizer search frontier, or transaction-local aggregate values. Exclude derived caches that can be recomputed and runtime resources that cannot be meaningfully serialized.

Byte-for-byte reconstruction is often unnecessary and brittle. A restored hash table may use different bucket layout yet answer the same specified queries. State observational equivalence and any identity/reference guarantees explicitly.

### Keep representation with the originator

The originator creates a private/opaque memento and validates it on restoration. The caretaker stores labels, timestamps, storage handles, or user-facing descriptions but should not edit the captured internals.

Language access control may be imperfect; module/package boundaries, unexported types, capability tokens, authenticated envelopes, and disciplined interfaces preserve the ownership intention. Do not serialize arbitrary runtime class names and reflectively reconstruct them from untrusted data.

### Capture necessary and sufficient state

Capture too little and restored behavior diverges: cursor, selection, mode, random-generator state, normalization/version flags, or stable IDs may matter. Capture too much and history retains caches, credentials, file handles, locks, observers, sessions, and unrelated aggregates.

Treat clock, randomness, and external query results explicitly when deterministic replay matters. A reference to “current rate” does not restore the historical rate unless the version/value is captured under policy.

### Eliminate accidental aliasing

If a memento holds the originator's mutable list, later edits mutate the past. Deep copy supplies isolation but can be expensive and mishandle identity/cycles. Immutable values and persistent data structures share unchanged structure safely when their immutability/lifetime invariants hold.

Copy-on-write needs exclusive ownership detection and correct reference accounting. A mutable element inside an immutable outer tuple is still an alias risk.

### Bind identity and compatibility

Include stable originator identity/type, memento schema version, source revision/base, feature/config version where behavior depends on it, and integrity metadata for durable/untrusted storage. Reject a document A memento applied to document B.

Restore old schema through an allowlisted migration chain with retained fixtures. Never guess missing semantics or silently drop fields affecting invariants. Sometimes the safe behavior is “unsupported history version.”

### Validate before atomic application

Parse and bound the envelope; verify integrity/provenance, owner/type, schema, base/conflict policy, all field types/ranges, cross-field invariants, and resource sizes into temporary owned state. Only then swap/commit the new state.

If validation mutates the live object incrementally, failure can leave a hybrid. Construct-then-swap or transactional update provides failure atomicity inside the declared boundary.

### Specify undo and redo as history

Before an edit, save the current memento on undo and clear redo. Undo pushes current state to redo and restores the newest prior state. Redo pushes current state to undo and restores the newest future state.

After undo, a new edit normally creates a branch and discards redo, but advanced tools may preserve a history DAG. Define grouping/coalescing, maximum entries/bytes/time, saved-document markers, irreversible barriers, and what happens when a capture fails.

### Choose snapshot, delta, or command history

Full snapshots make restore fast and simple but cost space/copy time. Deltas/commands reduce storage when changes are small but depend on bases, invertibility, deterministic application, and longer chains. Periodic snapshots plus deltas bound replay.

Command undo can store inverse data rather than all state, but inverses are context-dependent: deleting text must retain the text/location, and intervening edits can invalidate assumptions. Event sourcing stores the authoritative sequence of facts and rebuilds state; a memento is usually a derived acceleration/recovery artifact, not the audit truth.

### Handle concurrency explicitly

A memento from revision 10 restored over current revision 15 may erase another user's changes. Options include exclusive editing, expected-version rejection, branch/fork, three-way merge, operational transformation/CRDT semantics, or domain-specific reconciliation.

Never call last-write-wins “undo” without informing the user. Restoration authorization and conflict policy are current decisions, not frozen inside an old capture.

### Separate state reversal from effects

Restoring an order object does not un-send an email, un-charge a card, revoke a shipped parcel, or reverse physical motion. Those effects require new authorized compensating commands, reconciliation, and audit; some are irreversible.

If replaying/restoring would normally emit effects, suppress them through an explicit replay mode/gateway or derive new effects from a controlled reconciliation process. Hidden callbacks during restore are dangerous.

### Make checkpoints crash-consistent

An in-memory memento provides no crash recovery. A durable checkpoint needs atomic publication: write new data completely, verify it, synchronize according to the storage guarantee, atomically update a pointer/manifest, and retain the previous usable generation until the new one is committed.

For log-based systems, record the exact log position/epoch included. Recovery loads a valid compatible checkpoint then replays strictly later committed records. Test power loss/corruption at every write/rename/sync boundary on the real storage stack rather than inferring durability from an API return.

### Do not confuse local and distributed snapshots

Independent snapshots of services A and B can represent an impossible combination if messages were in flight. Distributed snapshot algorithms record process/channel state under communication assumptions to capture a consistent cut; database transactions or coordinated epochs provide other mechanisms.

A collection of mementos has no global consistency property by itself. State the snapshot protocol, membership, channels, failure model, and restoration coordination.

### Protect snapshot data

Mementos often contain more historical sensitive data than current state. Minimize fields; classify data; authorize creation/read/restore/delete separately; encrypt at rest and in transit where required; authenticate integrity; manage keys independently; redact logs; and enforce retention/legal-hold/deletion policy.

Compression before authenticated encryption can be acceptable for stored blobs under a reviewed design; do not invent cryptography. Limit size, nesting, decompression ratio, object count, migrations, and restore CPU to resist hostile captures.

### Operate bounded history

Track entries and bytes per object/user/tenant, capture/restore latency, deduplication ratio, checkpoint age, migration failures, corrupt/rejected captures, recovery point/time, pinned-version storage, and restore outcomes. Apply quotas and compaction without deleting required audit/backup evidence accidentally.

History eviction should preserve the current state and clear user expectations. Backups need independent copies, access controls, integrity checks, restoration drills, and failure-domain separation; an undo stack is not a backup.

### Test evidence at each boundary

Property-test capture/restore observational round trips across generated valid states. Mutate live state after capture to detect aliases. Test wrong owner/type, stale base, every schema version/migration, corrupt/truncated/oversized data, invalid invariants, partial restore failure, history branch behavior, and memory limits.

For durability, fault-inject every checkpoint/log boundary, corrupt latest generation, restore prior generation, and measure RPO/RTO. For external/distributed systems, test suppressed replay effects, compensation failure, concurrent conflicts, inconsistent local snapshots, partitions, and recovery authorization.

## Definitions and Notation

Let (S_v) be valid originator states under schema (v), and (M_v) the corresponding mementos. Capture $C_v:S_v\to M_v$. Restore/migrate $R_{v\to w}:S_w\times M_v\to S_w\cup Error$.

For observable functions (O=\{o_1,...,o_k\}), define

$$
s\equiv_O s'\iff \forall o\in O:o(s)=o(s').
$$

The round-trip obligation is $R_{v\to v}(s',C_v(s))\equiv_O s$ for compatible owner/base and successful validation, independent of interim state (s').

History state (H=(U,c,R)) contains undo stack (U), current state (c), and redo stack (R). New edit maps $(U,c,R)\to(U\mathbin{+}[C(c)],edit(c),[])$. Undo and redo move captures between stacks without exposing their contents.

## Mechanisms, Invariants, or Proof Structure

### Memento design procedure

1. Define originator boundary and observable restoration contract.
2. Select necessary state; exclude derived caches, resources, and unrelated authorities.
3. Create immutable/owned opaque capture with owner, schema, revision, and integrity metadata.
4. Validate/migrate into temporary state, then restore atomically.
5. Define undo/redo branching, grouping, limits, and failure behavior.
6. Specify concurrency conflict and external effect/compensation policy.
7. For durability, align checkpoint generation with committed log position and secure retention.
8. Test round trips, aliasing, migration, corruption, crashes, conflicts, effects, and recovery drills.

### Executable mechanism

This text editor uses immutable tuple mementos. The caretaker stores opaque values, moves them between undo/redo stacks, and clears redo after a divergent edit. It does not model concurrent editing, durable serialization, encryption, external effects, or crash recovery.

<!-- bijux-verify: {"id":"memento-editor-history","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"current=alpha-beta-gamma revision=2\nundo1=alpha-beta revision=1\nundo2=alpha revision=0\nredo=alpha-beta revision=1\nbranch=alpha-beta-delta revision=2 redo=0\n","stderr":""}} -->
```python
class Editor:
    def __init__(self, document_id, text):
        self.document_id = document_id
        self.text = text
        self.cursor = len(text)
        self.revision = 0

    def capture(self):
        return ("editor-v1", self.document_id, self.revision, self.text, self.cursor)

    def restore(self, memento):
        schema, owner, revision, text, cursor = memento
        if schema != "editor-v1" or owner != self.document_id:
            raise ValueError("incompatible memento")
        if cursor < 0 or cursor > len(text) or revision < 0:
            raise ValueError("invalid memento")
        self.revision, self.text, self.cursor = revision, text, cursor

    def append_text(self, suffix):
        self.text = self.text + suffix
        self.cursor = len(self.text)
        self.revision += 1


class History:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def edit(self, editor, suffix):
        self.undo_stack.append(editor.capture())
        self.redo_stack = []
        editor.append_text(suffix)

    def undo(self, editor):
        self.redo_stack.append(editor.capture())
        editor.restore(self.undo_stack.pop())

    def redo(self, editor):
        self.undo_stack.append(editor.capture())
        editor.restore(self.redo_stack.pop())


editor = Editor("doc-7", "alpha")
history = History()
history.edit(editor, "-beta")
history.edit(editor, "-gamma")
print(f"current={editor.text} revision={editor.revision}")
history.undo(editor)
print(f"undo1={editor.text} revision={editor.revision}")
history.undo(editor)
print(f"undo2={editor.text} revision={editor.revision}")
history.redo(editor)
print(f"redo={editor.text} revision={editor.revision}")
history.edit(editor, "-delta")
print(f"branch={editor.text} revision={editor.revision} redo={len(history.redo_stack)}")
```

### Round-trip argument

For a valid captured tuple, restore checks schema/owner and cursor/revision bounds before one tuple assignment. It assigns exactly captured revision, text, and cursor, so each observable projection equals its captured value. Tuple immutability prevents later editor field assignment from altering the memento.

This argument assumes tuple elements are immutable scalars/strings, no concurrent mutation, sufficient memory, correct language assignment semantics, and no failure after validation. It does not prove durability or restore external state.

### Recovery review layers

Review local observational equivalence, alias/lifetime safety, history algebra, migration/invariant validation, durable checkpoint/log consistency, security/retention, and distributed/external-effect recovery independently. Passing one layer is not evidence for another.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Full memento | Fast simple restore | Copy/storage cost | State is bounded and restore frequent |
| Delta/inverse command | Compact for small edits | Base chains and inverse assumptions | Changes are small and well-defined |
| Persistent data structure | Cheap immutable branching | Structural/GC complexity | Many related versions in memory |
| Event sourcing | Authoritative history and replay | Schema/code/effect replay complexity | Complete change history is a core requirement |
| Database transaction/savepoint | Strong storage-scoped rollback | Limited to one transaction/authority | Short-lived database work |
| Durable checkpoint plus log | Fast crash recovery | Atomic publication and migration work | Large state rebuilt from an ordered log |
| Backup | Independent disaster recovery copy | Restore time and operational cost | Failure-domain recovery/compliance |
| Compensation | Addresses observed external effects | New action can fail and is not erasure | Irreversible/cross-authority effects exist |

## Failure Modes and Misconceptions

- **“A memento is a deep copy.”** It is an opaque sufficient state representation; copying strategy is an implementation choice.
- **“Private means secure.”** Language visibility does not provide storage confidentiality, integrity, or authorization.
- **“Restore means byte identity.”** Observational equivalence is often the durable requirement.
- **“Undo reverses the world.”** It restores scoped internal state; external effects need compensation/reconciliation.
- **“Redo is always available.”** A divergent edit normally invalidates the abandoned linear future unless history branches are retained.
- **“Snapshots are audit logs.”** They omit how/why state changed and can be overwritten; audit has separate provenance/integrity needs.
- **“Latest capture can overwrite current.”** Concurrent changes need expected-version conflict or merge policy.
- **“Serialization preserves meaning forever.”** Schema, code, configuration, and dependencies evolve.
- **“Atomic file replacement guarantees durability.”** Storage/filesystem sync and crash semantics must be established and tested.
- **“Local snapshots compose globally.”** In-flight messages can make their combination inconsistent.
- **“Encrypted history needs no access policy.”** Keys, metadata, restore authority, retention, and deletion remain critical.
- **“A passing round trip proves recovery.”** Corruption, crash windows, scale, migration, and external dependencies remain.

## Worked Examples

### Example 1

A shallow memento stores a mutable list reference; appending after capture changes both live state and “history.” Capturing an immutable tuple or persistent version isolates it. **Conclusion:** Historical state must not alias later mutation.

### Example 2

A hash table restores with different bucket capacity but identical `get`, membership, and iteration-order contract. Byte inequality is irrelevant to specified behavior. **Conclusion:** Define restoration through observables, not incidental representation.

### Example 3

Document A's syntactically valid memento is applied to document B. Binding/checking stable owner ID rejects it before mutation. **Conclusion:** Schema validity alone does not establish capture identity.

### Example 4

The user undoes twice, redoes once, then types new text. Clearing redo avoids presenting an obsolete linear future; a history-DAG editor could preserve it as another branch. **Conclusion:** Redo policy is a branching decision.

### Example 5

Revision-10 state is restored over collaborative revision 15. Expected-version rejection prompts merge/fork instead of erasing five revisions. **Conclusion:** Restoration is a concurrency-controlled write.

### Example 6

Restoring an order to “unpaid” does not reverse a completed card charge. A separately authorized refund command records a new fact and may fail. **Conclusion:** Compensation is not rollback or erasure.

### Example 7

A checkpoint includes log records through 800 but metadata says 850; recovery skips 801–850 and loses committed state. Publishing data and exact log position atomically prevents the mismatch. **Conclusion:** Durable checkpoints are protocols, not files.

### Example 8

Service A snapshots after sending a debit message while B snapshots before receiving it; combined balances invent money unless channel/in-flight state is included. **Conclusion:** Independent local mementos do not form a consistent distributed cut.

### Example 9

An undo history retains deleted access tokens and personal text indefinitely. Field minimization, encryption, access separation, byte/time quotas, retention, deletion, and audit reduce exposure. **Conclusion:** Historical copies expand the security/privacy surface.

### Example 10

A flight-control simulation captures software variables but omits hardware state, clock synchronization, actuator position, and environment. Restore tests cannot establish safe real-system recovery. **Conclusion:** High-stakes restoration requires system-level state and safety evidence.

## Cross-Program Connections

- **Object-Oriented Programming:** encapsulation, identity, copying, ownership, and object graphs shape captures.
- **Functional Programming:** immutability, persistent structures, lenses, and pure state transitions support history.
- **Data Structures Engineering:** structural sharing, copy-on-write, DAGs, and memory accounting determine cost.
- **Database Engineering:** transactions, savepoints, MVCC, write-ahead logs, checkpoints, and recovery formalize durability.
- **Distributed Systems Engineering:** consistent cuts, in-flight messages, epochs, replication, and partial failure constrain global restore.
- **Security Engineering:** confidentiality, authenticated integrity, key management, deserialization, retention, and restore authorization apply.
- **Testing and Quality:** property tests, corruption/fault injection, migration fixtures, and recovery drills produce evidence.
- **Software Design and Domain Modeling:** aggregate boundaries and external effects define what one originator can restore.
- **Cloud and Platform Engineering:** backup generations, object versioning, quotas, RPO/RTO, and disaster recovery operationalize captures.
- **Systems Engineering:** safety-critical recovery needs hazard analysis, physical-state modeling, and independent controls.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Memento intent, structure, applicability, and consequences.
2. Chris Okasaki, *Purely Functional Data Structures*, Cambridge University Press, 1998, ISBN 978-0-521-66350-2. Provides persistence and structural-sharing foundations for immutable versions.
3. K. Mani Chandy and Leslie Lamport, [“Distributed Snapshots: Determining Global States of Distributed Systems”](https://lamport.azurewebsites.net/pubs/chandy.pdf), *ACM Transactions on Computer Systems* 3(1), 1985. Primary consistent distributed-snapshot algorithm and assumptions.
4. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1992, ISBN 978-1-55860-190-1. Provides logging, checkpoint, transaction, and recovery foundations.
5. Martin Fowler, [“Event Sourcing”](https://martinfowler.com/eaaDev/EventSourcing.html), 2005. Distinguishes authoritative event history, state rebuild, snapshots, reversal, and external replay effects; explicitly presented by its author as draft material.
6. SQLite Project, [Atomic Commit in SQLite](https://www.sqlite.org/atomiccommit.html), accessed 2026-08-28. Provides a concrete storage-engine account of journals, synchronization assumptions, atomic commit, and recovery.
7. NIST, [SP 800-209: Security Guidelines for Storage Infrastructure](https://doi.org/10.6028/NIST.SP.800-209), 2020. Provides storage confidentiality, integrity, availability, isolation, restoration, and monitoring guidance.
8. OWASP Foundation, [Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html), accessed 2026-08-28. Provides data-minimization, algorithm/key, random-generation, and defense-in-depth guidance.

## Exercises

### Exercise 1

Trace the executable history and prove the observational round trip and branch behavior under its assumptions.

### Exercise 2

Design a memento for a graph editor with shared nodes, selection, viewport, caches, and file/network resources.

### Exercise 3

Specify secure versioned restoration for mementos stored for five years across application schema changes.

### Exercise 4

Compare mementos, inverse commands, event sourcing, database savepoints, checkpoints, and backups for an editing service.

### Exercise 5

Review a proposed distributed “rollback” based on simultaneous service snapshots after an externally visible transaction.

## Answers to the Exercises

### Answer 1

Initial current state is `alpha` revision zero. First edit pushes its capture and produces `alpha-beta` revision one; second pushes that capture and produces `alpha-beta-gamma` revision two. First undo pushes current revision two to redo and restores revision one; second pushes revision one and restores revision zero. Redo pushes revision zero to undo and restores revision one. The new delta edit first captures revision one, clears redo, and yields `alpha-beta-delta` revision two, so redo length is zero.

For any valid same-owner tuple, restore validates before assigning exactly captured revision, text, and cursor; projections therefore equal captured projections. Tuple and string immutability prevent subsequent editor assignments from modifying the capture. The argument excludes concurrency, deep mutable elements, memory failure, durability, external effects, and malicious runtime compromise.

### Answer 2

Define observables as graph nodes/edges/attributes with stable IDs, selection IDs, viewport transform, tool/mode, and document revision. Exclude render caches, spatial indexes, open file/socket handles, locks, observers, undo manager, and derived layout that can be recomputed unless deterministic layout state is a requirement. Represent graph through immutable node/edge maps or a persistent structure so captures share unchanged subgraphs without mutable aliasing; validate referential integrity, unique IDs, edge endpoints, attribute limits, selection membership, and finite viewport values.

Bind document ID, schema, source revision, feature/config version, and integrity metadata. Restore builds temporary graph/indexes, then atomically swaps. Reopen external resources through explicit capabilities after authorization rather than capturing handles. Apply expected-version conflict for collaborative edits. Test cycles, shared nodes, deleted selection, huge/corrupt graph, alias mutation, migration, missing plugins/fonts, failed cache rebuild, concurrent edits, and exact observable round trips.

### Answer 3

Define a stable envelope containing record ID, owner/type, capture schema, application semantic/config version, source revision, creation/expiry/retention class, payload digest/authenticated metadata, encryption/key identifier, and provenance. Use allowlisted non-executable formats with byte/depth/count/decompression limits. Encrypt sensitive payloads using reviewed authenticated encryption and independently managed rotated keys; authorize capture, read, restore, migration, export, and deletion separately, with audited current identity/tenant policy.

Maintain explicit migration chains with immutable original bytes, golden fixtures for every supported version, semantic round-trip expectations, and rollback of migration tooling. Validate/migrate into temporary current state, check all invariants and conflicts, then atomically restore. Quarantine corrupt/unsupported captures rather than guessing. Test old-to-current paths, missing/retired keys, tamper/truncation, malicious sizes, authorization revocation, tenant separation, clock/expiry, deletion/legal hold, disaster recovery, and restore drills. Retention support is a product/operations commitment, not guaranteed by serialization.

### Answer 4

Use in-memory immutable mementos for responsive short editing history and branch previews. Use inverse commands when edits are compact and inverse context can be captured reliably; periodic full captures bound inverse-chain recovery. Use event sourcing only when the complete accepted change sequence and temporal reconstruction are first-class system-of-record requirements, with explicit replay/effect/version semantics. Database savepoints handle short-lived rollback inside one transaction but are not user history or crash backup.

Use durable checkpoints aligned to an authoritative log to reduce restart time, retaining generation/log-position metadata and testing crash recovery. Use independent encrypted/versioned backups for infrastructure disaster, deletion, or corruption recovery across failure domains, with RPO/RTO and restoration drills. These mechanisms can coexist because they answer different questions; calling the undo stack a backup or an event log a compensation mechanism creates dangerous gaps.

### Answer 5

First reject the claim that clock-simultaneous local snapshots define one global state: clocks differ, messages/effects are in flight, services may have different commit points, and external observers cannot be rewound. Inventory every authority, local state/log position, channel, transaction identity, external effect, isolation/version, and acknowledgement. Determine whether a consistent-cut algorithm, transaction protocol, coordinated epoch, or source-of-truth replay can establish a recoverable internal state under stated membership/channel/failure assumptions.

For an already visible transaction, restoration normally creates a new recovery workflow: fence further writes, establish current facts, reconcile each idempotent/effect-queryable step, issue authorized compensations where valid, preserve audit, and surface irreversible/indeterminate outcomes. Test duplicates/reorder/partitions, snapshots before/after send/receive/commit/ack, crash during restore, concurrent new work, compensation failure, stale authority, and external-provider reconciliation. A collection of mementos proves neither global consistency nor business/legal erasure; named domain, data, distributed-systems, security, operations, and assurance reviewers must approve the recovery claim.
