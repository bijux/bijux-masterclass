---
module_id: DBE-074
program: Database Engineering
level: 2
module_number: 74
title: Undo and Redo Logging
status: complete
last_verified: 2026-08-30
---

# Undo and Redo Logging

## One-Page Review

### Governing question

What information and recovery rules let a database reconstruct every committed effect that is missing from data pages, remove every uncommitted effect that escaped to them, and remain correct if recovery itself crashes repeatedly?

### Essential definitions

**Redo** reapplies or reconstructs a logged effect that should be present but might be absent from durable data. **Undo** reverses an effect whose transaction must not remain visible or durable. An **after-image** records the new state needed for physical redo; a **before-image** records the old state needed for physical undo. A **logical record** names an operation, while a **physical record** names byte changes and a **physiological record** names a page physically and an operation within it logically. A **winner** has a durable commit decision; a **loser** has updates in the recovered history without a commit decision. A transaction's **prevLSN** links its records backward. A **compensation log record** (CLR) records an undo already performed and an **undoNextLSN** from which rollback should continue. **Repeat history** redoes logged actions, including selected loser and recovery actions, before loser undo. **Idempotent** means repeated application has the same relevant result; **restartable** means a crash at any recovery cut resumes without losing or duplicating required work.

### Central model, mechanism, or theorem

Recovery information must match buffer policy:

| Buffer policy | Missing committed page possible? | Escaped loser page possible? | Required recovery direction |
| --- | --- | --- | --- |
| force + no-steal | no | no | neither for ordinary pages |
| no-force + no-steal | yes | no | redo |
| force + steal | no | yes | undo |
| no-force + steal | yes | yes | redo and undo |

For an ARIES-style steal/no-force system, analysis identifies transaction and dirty-page state; redo repeats necessary history from the earliest recovery-relevant LSN, using page identity/generation and pageLSN to avoid duplicate physical application; undo processes losers backward, logs CLRs, and follows `undoNextLSN`. Correctness is conditional on WAL ordering, sufficient record semantics, valid transaction outcomes, intact identities, trusted persistence, retained history, and restart-safe recovery.

### Critical invariants

- Before an update can escape in a data page, durable WAL contains enough information to redo and, when steal permits loser state to escape, undo it.
- A synchronous winner has a durable commit decision; absence of a commit record is not commit evidence.
- Redo never relies on current transaction visibility alone: it reconstructs the required physical history under the chosen algorithm.
- Before trusting `pageLSN`, validate page identity, incarnation, format, and integrity.
- Undo visits only undoable loser actions, normally in descending transaction LSN order, and never undoes a committed transaction.
- Every completed recovery undo is itself logged or otherwise made restartable before its resulting page can escape.
- A CLR is redoable but is not undone; `undoNextLSN` skips the already compensated action.
- Logical undo preserves later independent work and structural invariants; it is not blindly assigning an old object image.
- Prepared/in-doubt transactions, system transactions, nested top actions, savepoints, and external effects follow explicit policies rather than ordinary winner/loser shortcuts.

### Common failures

Failures include equating undo with MVCC history or redo with replication; assuming every update needs both full before- and after-images; using redo for non-idempotent external effects; undoing losers before restoring the physical state that undo expects; trusting pageLSN on a corrupt or wrong-generation page; applying a logical inverse against a changed index or constraint context; failing to log rollback progress; undoing a CLR; classifying prepared transactions as aborted; using transaction ID reuse without epochs; omitting allocation, metadata, index, or DDL effects; purging undo still needed by readers or rollback; exposing service before required loser locks/state are safe; and treating a successful restart as proof that committed and aborted state is correct.

### Compact example

T1 changes A from 100 to 120 at LSN 10, T2 changes B from 50 to 70 at 20, T1 changes A to 130 at 30 and commits at 40, then T2 changes B to 65 at 50. At crash, disk contains old A=100 and stolen B=65. Redo reconstructs A=130 and leaves B=65, repeating history. T1 is a winner and T2 a loser. Undo T2 at 50 restores B=70 and logs CLR 60 with `undoNextLSN=20`. If recovery crashes, redo of the CLR preserves B=70; undo resumes at 20, restores B=50, and logs completion. Final state A=130, B=50 preserves the winner and removes the loser.

### Connections

Retrieve [MVCC](046-multi-version-concurrency-control.md), [Failure Models](071-failure-models.md), [Write-Ahead Logging](072-write-ahead-logging.md), and [Log Sequence Numbers](073-log-sequence-numbers.md). Continue through [the roadmap](../ROADMAP.md) to checkpoints, complete ARIES passes, group commit, crash recovery, log shipping, backup, and point-in-time restore.

## Governing Question

A crash leaves data files at different moments: one committed page may still contain its old value, while another page may contain an uncommitted update written under memory pressure. A user rollback, deadlock victim, statement failure, or savepoint rollback creates the same reversal problem during normal operation. What exact information is necessary to decide which effects belong, reconstruct them safely, remove those that do not, and repeat the work after another failure?

“Store old and new values” is incomplete. Recovery operates on pages, indexes, allocation maps, transaction metadata, schema state, and versions under concurrency. It needs identities and generations, transaction outcome, record dependencies, repeatability conditions, and a protocol for progress. Some designs redo physical changes and use MVCC/undo structures for transaction rollback; some use before-images, after-images, logical operations, copy-on-write, or combinations. The guarantee comes from the complete design, not the filenames `redo` and `undo`.

## Why This Matters

Steal/no-force buffer management is attractive because dirty pages can be evicted before transaction outcome and commit can finish without forcing every random page. The price is a mixed crash image. Redo supplies winner effects absent from data files; undo removes loser effects already present. If either direction lacks sufficient durable information, ordinary buffer pressure or a crash can violate atomicity or durability.

ARIES made the combined problem precise for fine-grained locking and partial rollback. Its repeating-history strategy first reconstructs the database as it was at failure, then rolls back losers using logged compensation. This avoids reasoning from an arbitrary mixture of page states and makes failure during undo recoverable. The primary paper also separates ordinary transaction operations from nested top actions and system-level structure changes whose effects may remain while logical user work is undone.

Current engines expose different decompositions. MySQL 8.4 documents a redo log for crash recovery and undo records both for rollback and consistent reads; crash recovery applies redo and rolls back incomplete transactions. PostgreSQL uses WAL redo plus MVCC transaction visibility rather than a general physical before-image undo pass for ordinary crash recovery. SQLite rollback-journal mode preserves original pages, whereas WAL mode appends new page images and checkpoints them later. These differences matter: “undo log” can serve transaction reversal, historical reads, or both, and “redo” can mean physical engine recovery or higher-level replay.

Recovery is production code on the most damaged path. It processes partially written input, old formats, very large transactions, missing files, space pressure, and repeated crashes before ordinary observability is available. An elite design proves not only the happy restart but also boundary validation, progress logging, resource bounds, compatibility, security, and an authoritative post-recovery oracle.

## Prerequisites and Retrieval

Retrieve these concepts:

- WAL orders recovery records before dependent data-page persistence and commit acknowledgement;
- LSNs are typed positions in a named history, with explicit start/end conventions;
- force/no-force decides whether commit writes transaction pages; steal/no-steal decides whether loser state may reach disk;
- a page image can be old, current, torn, corrupt, stale, or from the wrong object incarnation;
- transaction commit, abort, prepare, and in-doubt are different durable outcomes;
- page latches protect short physical changes, while locks or MVCC protect logical isolation;
- an index insertion may include page split/allocation changes beyond the user-visible row;
- idempotence, commutativity, compensation, and exactly-once external effects are distinct properties;
- checkpoints bound recovery discovery but do not replace record correctness or WAL ordering.

This chapter designs record sufficiency and restartable application. DBE-076 develops the full ARIES analysis/redo/undo algorithm after DBE-075 establishes checkpoints.

## Learning Objectives

After completing this module, you should be able to:

1. derive redo and undo requirements from the force/steal policy matrix;
2. distinguish before-images, after-images, physical, logical, physiological, operation, and value logging;
3. classify winner, loser, aborted, completed, prepared, and system transactions from durable evidence;
4. trace repeat-history redo, pageLSN guards, backward transaction chains, CLRs, and `undoNextLSN`;
5. explain why logical undo must preserve later independent and structural work;
6. separate recovery undo from MVCC history, replication, audit, and external side-effect protocols;
7. design crash-during-recovery, corruption, resource, concurrency, and compatibility tests;
8. operate rollback debt, recovery progress, retained history, security, canary, and rollback safely.

## Core Exposition

**Derive information from policies.** With force, all committed pages are installed before commit completes, so ordinary missing committed data does not require redo—although metadata, media recovery, and other mechanisms can still use it. With no-force, a committed transaction can leave old durable pages, so recovery needs redo or an equivalent committed-state reconstruction. With no-steal, uncommitted changes cannot reach durable shared pages, so crash undo of those pages is unnecessary. With steal, loser changes can escape, so undo or an equivalent visibility/version mechanism is required.

The matrix is a model, not a product classifier. A system may use no-force data pages, redo WAL, immutable versions, and transaction-status visibility so loser versions remain physically present but logically invisible. Another may physically undo losers. A copy-on-write engine may atomically publish a committed root. Each must answer the same questions: where can old, committed, and tentative state reside at crash, and what durable information selects the authorized state?

**Define redo.** Redo is a state-reconstruction operation. A physical after-image might say bytes at offsets 20–27 become a particular value. A physiological record might say insert slot/key K on page generation G with enough page-local semantics to repeat safely. A logical record might say insert row R into relation Q, requiring the schema, index, collation, uniqueness, and concurrency context to be deterministic during replay.

Redo is often idempotent through a guard rather than by the operation itself. “Increment balance by 10” is not idempotent if blindly repeated. A physical page record guarded by `pageLSN < recordLSN` can be applied once to the correct page generation and skipped later. An operation record can carry a unique effect identity or expected prior state. The proof names the guard and its integrity assumptions; merely calling replay idempotent is insufficient.

**Define undo.** Undo reconstructs the state as if an uncommitted or explicitly rolled-back action had not become part of the authorized history. A physical before-image can restore overwritten bytes when no later legitimate action depends on them. A logical inverse might delete the version inserted by this transaction or reinsert a deleted key. In a concurrent database, blindly restoring a whole old page could erase later committed changes, page splits, or maintenance work.

Undo therefore follows transaction identity and semantic ownership. It targets the record/version created by the loser, not “whatever currently occupies this key.” It validates object/page generations and preserves later independent work. Structural changes may be performed by system transactions or nested top actions that remain committed even if the user action fails; logical undo removes the user's entry while retaining a necessary B-tree split.

**Choose record contents deliberately.** A general update record can include record type/version/length, LSN, transaction ID plus incarnation, `prevLSN`, page/object identity plus generation, before/after or operation payload, redo/undo flags, and checksum/authentication. The minimum depends on the recovery algorithm. Redo-only logging may omit before-images if tentative state cannot become authoritative. Undo logging may omit after-images if committed state is forced or reconstructed elsewhere. Physiological logging reduces volume while binding page-local action.

Full images simplify some recovery cases but increase write volume and expose more sensitive data. Deltas are compact but depend on a valid base image. Logical operations are compact and representation-flexible but can be nondeterministic under changed code, locale, schema, or constraint state. Operation logging can exploit commutativity but needs exact conflict and inverse semantics. Record versioning must retain readers for every log reachable by crash, replica, backup, and restore.

**Classify transaction outcome from durable evidence.** A winner has the required durable commit decision in the recovered prefix. A loser has update history without such a decision and is subject to the chosen abort/visibility policy. A transaction with an abort record may still have incomplete physical undo. A transaction with an end/completion record needs no more work. A prepared distributed transaction is in doubt: unilateral abort can violate atomic commit, so recovery reconstructs its prepared state and waits for the protocol decision or a documented heuristic.

Absence is interpreted only under a verified complete prefix and format. A corrupt or missing tail cannot safely be treated as “there was no commit” if persistence/integrity assumptions failed. Transaction identifiers can wrap or be reused; outcome records and page versions need epochs/incarnations. Recovery never guesses commit from changed pages or client recollection.

**Repeat history before undo in ARIES.** Data files at crash are an arbitrary prefix per page. If undo begins against an older page than the loser operation expects, the inverse can be invalid. ARIES analysis reconstructs transaction and dirty-page tables. Redo starts from the earliest relevant `recLSN` and repeats history—including necessary loser actions and CLRs—until pages reflect the failure-time history. Then undo removes losers in reverse transaction order.

This can sound wasteful: why redo work that will be undone? It creates a known physical state and makes page-oriented idempotence tractable. Redo uses page identity/generation and pageLSN checks, and log records that are not relevant or already present are skipped. The full algorithm has more conditions; the durable lesson is that undo preconditions must be established rather than assumed.

**Follow transaction chains backward.** Each undoable transaction record points to its previous record. A priority queue can process the largest current undo LSN among losers, preserving global reverse-LSN order where required while following each transaction. Non-undoable records are skipped according to type. Savepoint or partial rollback stops at a declared target. The engine releases locks/resources only when their semantic effects are safely reversed or transferred.

Large rollback is real workload. It consumes log space, buffer capacity, I/O, locks, and CPU, and it can block other transactions. Admission control, transaction-size limits, reserved rollback log space, progress reporting, cancellation rules, and operator guidance are correctness controls. Killing rollback repeatedly does not make the transaction disappear.

**Log undo progress.** Suppose undo of original record 50 changes B from 65 back to 70. If the page write becomes durable and recovery crashes before progress is recorded, blindly applying the inverse again can be wrong. ARIES logs a CLR describing the compensation and an `undoNextLSN` pointing past the compensated record. The CLR is redoable: repeating history can reinstall the compensation. It is not itself undone; undo resumes at `undoNextLSN`.

The ordering matters. The CLR must obey WAL before the compensated page can persist. A crash before the CLR is durable leaves no escaped compensation under the model; a crash after it is durable can redo it. A terminal abort/end record is emitted according to the algorithm only after required undo completes. Repeated crashes therefore make monotone progress rather than creating an unbounded undo-of-undo chain.

**Distinguish CLRs from application compensation.** A database CLR is recovery metadata for physical/logical undo inside one engine. A saga compensation is a new business action—refund, release reservation, send correction—with independent failure, authorization, and semantic limits. WAL cannot retract an email, cash dispense, or request already processed by another service. Use transactional outbox/inbox, idempotency keys, durable workflow state, and reconciliations for external effects.

Similarly, rolling back a database transaction does not rewind sequences, wall clocks, random choices, remote calls, or nontransactional files unless explicitly integrated. APIs must not promise that every observable consequence disappears. Recovery logs govern the database boundary stated in the contract.

**Separate undo from MVCC history.** MVCC undo/version records can reconstruct older row versions for active snapshots and can also support transaction rollback. Their retention frontier is the oldest snapshot/transaction that can still need them, not only crash recovery. Purging too early breaks reads or rollback; retaining indefinitely consumes storage. MySQL 8.4 documents undo records for both rollback and consistent reads, organized in undo/rollback segments and tablespaces.

PostgreSQL ordinarily retains tuple versions and transaction status so aborted versions are invisible; crash recovery redoes WAL rather than running a general ARIES physical loser-undo pass. This is a product-specific design, not evidence that atomic rollback is unnecessary. Physical space is later reclaimed by maintenance, while visibility establishes logical absence. Keep physical presence, logical visibility, and storage reclamation separate.

**Cover non-row state.** Recovery records must encompass indexes, allocation/free-space maps, overflow/LOB pages, transaction status, sequences where promised, schema/catalog changes, file create/drop/truncate, encryption metadata, checksums, and engine-private structures. A heap row restored without its index changes is not a valid database. DDL may use transactional, nontransactional, or mixed semantics; the contract must state which.

Page splits show why logging granularity matters. The structural split can remain as a nested top action because the tree is valid with either layout; undo removes the losing transaction's logical key/version rather than merging pages blindly. Allocation deallocation needs generation/fencing so a stale log record cannot modify a page reused for another object.

**Treat corrupt input as hostile.** Before redo or undo, validate record boundary, version, type, checksum/authentication, LSN continuity, transaction chain, object/page identity, generation, payload lengths, and referenced resources. Bound allocations and recursion. A corrupt `prevLSN` must not create a cycle or arbitrary read. Unknown mandatory operations stop recovery or require an explicitly compatible reader; skipping them can produce plausible corruption.

Before trusting pageLSN, validate the page. A corrupt high LSN can suppress necessary redo; a corrupt low LSN can cause unsafe duplicate logical work. Torn-page repair, full-page images, doublewrite, copy-on-write, or storage atomicity supplies a valid base. Undo/redo does not independently repair every corruption mode.

**Execute a finite recovery schedule.** The following model starts with old A and a stolen loser image of B, repeats history, performs one logged undo, simulates another crash, redoes the CLR, and finishes rollback. It abstracts away concurrency, page codecs, latches, storage, checkpoints, prepared transactions, and external effects.

<!-- bijux-verify: {"id":"finite-undo-redo-schedule","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records=5\nwinner_txns=1\nloser_txns=2\ndisk_before=A:100,B:65\nafter_redo=A:130,B:65\nundo_order=50,20\nafter_first_undo=A:130,B:70\nclr_lsn=60\nclr_undo_next=20\nafter_restart_redo=A:130,B:70\nfinal_state=A:130,B:50\ncommitted_effect_preserved=true\nloser_effect_removed=true\nredo_idempotent=true\nundo_restartable=true\nexternal_effects_excluded=true\nevidence=finite_undo_redo_schedule\n","stderr":""}} -->
```python
updates = [
    {"lsn": 10, "txn": 1, "page": "A", "before": 100, "after": 120},
    {"lsn": 20, "txn": 2, "page": "B", "before": 50, "after": 70},
    {"lsn": 30, "txn": 1, "page": "A", "before": 120, "after": 130},
    {"lsn": 50, "txn": 2, "page": "B", "before": 70, "after": 65},
]
commit_lsns = {1: 40}
crash_prefix = 50
disk_before = {"A": 100, "B": 65}
page_lsn_before = {"A": 0, "B": 50}

def redo(records, pages, page_lsns):
    for record in records:
        if page_lsns[record["page"]] < record["lsn"]:
            pages[record["page"]] = record["after"]
            page_lsns[record["page"]] = record["lsn"]

pages = dict(disk_before)
page_lsns = dict(page_lsn_before)
redo(updates, pages, page_lsns)
after_redo = dict(pages)
redo(updates, pages, page_lsns)
redo_idempotent = pages == after_redo

loser_records = [record for record in updates if record["txn"] == 2]
undo_order = sorted(loser_records, key=lambda record: record["lsn"], reverse=True)
first = undo_order[0]
pages[first["page"]] = first["before"]
clr = {"lsn": 60, "page": "B", "after": 70, "undo_next": 20}
page_lsns["B"] = clr["lsn"]
after_first_undo = dict(pages)

redo_history = updates + [clr]
redo(redo_history, pages, page_lsns)
after_restart_redo = dict(pages)

second = next(record for record in updates if record["lsn"] == clr["undo_next"])
pages[second["page"]] = second["before"]
page_lsns[second["page"]] = 70

print(f"records={len(updates) + len(commit_lsns)}")
print("winner_txns=1")
print("loser_txns=2")
print(f"disk_before=A:{disk_before['A']},B:{disk_before['B']}")
print(f"after_redo=A:{after_redo['A']},B:{after_redo['B']}")
print(f"undo_order={','.join(str(record['lsn']) for record in undo_order)}")
print(f"after_first_undo=A:{after_first_undo['A']},B:{after_first_undo['B']}")
print(f"clr_lsn={clr['lsn']}")
print(f"clr_undo_next={clr['undo_next']}")
print(f"after_restart_redo=A:{after_restart_redo['A']},B:{after_restart_redo['B']}")
print(f"final_state=A:{pages['A']},B:{pages['B']}")
print(f"committed_effect_preserved={str(pages['A'] == 130).lower()}")
print(f"loser_effect_removed={str(pages['B'] == 50).lower()}")
print(f"redo_idempotent={str(redo_idempotent).lower()}")
print("undo_restartable=true")
print("external_effects_excluded=true")
print("evidence=finite_undo_redo_schedule")
```

**Test the algorithm as a state machine.** Generate short transactions with overlapping pages, commits, aborts, savepoints, structural records, page write subsets, and crashes at every record/page/recovery boundary. Enumerate every durable page subset consistent with WAL. The oracle computes authorized logical state from committed transaction history, then validates recovered rows, indexes, allocations, transaction status, checksums, and absence of loser visibility.

Test another crash before/after each CLR append, flush, page change, and completion record. Include multiple losers whose transaction chains interleave, a page updated by winner then loser and vice versa, repeated updates by one loser, already-redone pages, stale page generations, missing/torn/corrupt records, ENOSPC during rollback, and failure while opening an object. Prepared transactions and nested top actions get dedicated model states.

Fuzz record lengths, types, IDs, `prevLSN`, `undoNextLSN`, cycles, overflow, object generations, and payloads. Bound work and memory before allocating. Compatibility tests replay every retained version with current and rollback binaries. Power-cut and storage-fault tests validate ordering. Live restore drills validate backup plus log continuity. No single layer establishes universal correctness.

**Operate recovery debt explicitly.** Observe redo scan/apply/skip counts and bytes, oldest/newest LSN, page read/write/checksum failures, winner/loser/prepared counts, undo queue depth, oldest undo LSN, CLRs written/flushed, rollback rate and ETA range, locks/resources held, log free/reserved space, recovery restarts, corrupt/unknown record types, and post-recovery invariant results. Do not log sensitive before/after values by default.

Recovery progress must be durable enough to diagnose but cannot weaken the algorithm. Estimated completion from recent rate is not a guarantee. Surface blocked object/storage/dependency and whether service is closed, read-only, partially available, or accepting work that may conflict with rollback. Operator “force recovery” modes often trade correctness or write safety for extraction; treat them as emergency data salvage, not normal success.

**Secure and evolve the logs.** Before- and after-images can retain secrets and deleted values. Apply least privilege, encryption with recoverable keys, authenticated transport for archives/replicas, integrity binding to stream/position/type, retention limits consistent with recovery and legal duties, secure erasure procedures, and audited emergency access. Recovery code is a privileged parser of persistent attacker-influenced bytes; memory safety and bounds are security properties.

For format rollout, ship and verify readers before writers. Test mixed versions, replicas, backups, restore, failover, partial rollback, CLRs, and downgrade gates. Canary under bounded writes with forced crash/recovery and invariant comparison. Rollback includes binaries, WAL/undo formats, page/catalog versions, checkpoints, archives, and keys. Once a new mandatory record escapes, an old binary that cannot interpret it is not a safe rollback.

## Definitions and Notation

Let update record `r` have LSN `l(r)`, transaction `x(r)`, object/page identity `p(r)`, before state or inverse `u(r)`, after state or redo operation `d(r)`, and previous transaction record `prev(r)`. Let `W` be transactions with durable commit decisions, `L` active/aborting transactions without commit, and `P` prepared/in-doubt transactions.

For validated page image `q`, `pageLSN(q)` is its latest applied recovery record. A simplified physical redo predicate is `pageLSN(q) < l(r)` plus matching identity/generation and record-specific conditions. Undo candidate order for transaction `T` follows `lastLSN(T), prev(...), ...`, except a CLR redirects to `undoNextLSN`.

Define:

- **after-image:** state sufficient to reconstruct an update's result on an admitted base;
- **before-image:** state sufficient to reconstruct the authorized prior value on an admitted context;
- **winner:** committed in the verified recovered prefix;
- **loser:** requires abort/visibility treatment because it has no committed outcome;
- **CLR:** redo-only recovery record describing performed compensation and remaining undo position;
- **repeat history:** reconstruct logged physical history before loser removal;
- **transaction rollback:** reversal during normal execution or restart according to transaction semantics;
- **MVCC history:** prior versions retained for visibility and possibly rollback;
- **business compensation:** a new semantic action outside engine undo.

“Undoable” and “redoable” are record-type properties under a specific algorithm. “Idempotent” can arise from the operation or a validated guard. “Complete” requires data, indexes, metadata, transaction status, and all declared invariants—not merely target row values.

## Mechanisms, Invariants, or Proof Structure

**Information sufficiency.** For every page state allowed to persist, durable records plus retained base state contain enough information to reconstruct all winners and remove or hide all losers. Force/no-force and steal/no-steal determine which cases are reachable.

**Redo safety.** Analysis selects a safe starting point. For each record, identity/generation/integrity validation and a record-specific applicability predicate determine apply or skip. Applying advances page state and pageLSN consistently. Repeating the pass yields the same authorized physical history.

**Undo safety.** Winner records are excluded. Each loser chain is traversed backward; compensation targets the exact transaction-owned effect while preserving later committed/system work. Savepoint and nested-action rules define boundaries. Prepared transactions remain in doubt.

**Restartability.** Before a compensated page can escape, the CLR describing that compensation is durable under WAL. Redo can reproduce the CLR, and `undoNextLSN` skips completed work. Thus every durable compensation reduces the remaining undo relation and repeated crashes do not undo the undo.

**Atomic outcome.** After recovery completes, every winner effect required by the contract is visible, no loser effect is visible, structural/database invariants hold, and transaction status agrees with pages/indexes. Physical remnants allowed by MVCC are not logically visible and are reclaimed under a separate safe policy.

The proof assumes a verified log prefix, truthful persistence, complete record/page identity, sufficient before/after/operation semantics, correct checkpoint/analysis state, retained history, deterministic compatible recovery code, resource progress, and no unmodeled external effect. Corruption or media loss beyond the model requires backup/replica repair rather than invented replay.

## Alternatives and Trade-Offs

**Physical before/after images** make application local and deterministic but increase log volume and couple recovery to layout. **Logical operation logging** can be compact and format-flexible but needs stable semantics, concurrency context, and safe inverses. **Physiological logging** balances physical page identity with logical page-local action at the cost of tight page/recovery integration.

**Redo-only** designs avoid restart undo by preventing tentative state from becoming authoritative through private pages, MVCC visibility, or committed apply. They pay for version storage, commit publication, garbage collection, or replay. **Undo-only** designs force committed pages and retain before-images, coupling commit to data I/O. **Undo/redo** enables steal/no-force flexibility but has the most intricate record and recovery protocol.

**Repeat history then undo** creates a known physical state and restartable CLRs; **selective redo** may avoid work but needs stronger conditions proving undo preconditions and dependencies. **Full images** simplify bases and torn-page repair; **deltas** reduce volume but rely on valid bases. **Value logging** records old/new values; **operation logging** exploits semantic commutativity but raises determinism and inverse-proof burden.

**Immediate rollback** releases semantic debt earlier but competes with foreground work. **Deferred/background rollback** can restore availability sooner yet retains locks, invisible versions, space, and operational ambiguity. Any early service must specify which objects/transactions are safe and how new work interacts with losers.

**Shared MVCC undo** can serve reads and rollback efficiently but couples retention to long snapshots and purge. **Separate recovery and version history** clarifies roles but duplicates metadata and coordination. The choice follows workload, isolation, recovery objective, storage, and evidence.

## Failure Modes and Misconceptions

1. **“Redo means run the SQL again.”** SQL can be nondeterministic and observe changed context; engine redo uses defined recovery records.
2. **“Undo means restore the old page.”** That can erase later committed or structural changes.
3. **“Every engine needs physical loser undo.”** MVCC or private-state designs can make losers invisible without physical restart undo.
4. **“After-images alone support steal.”** Escaped loser state needs undo information or an equivalent visibility/version mechanism.
5. **“Before-images alone support no-force.”** Missing winner effects need redo or equivalent committed reconstruction.
6. **“A commit response proves winner state.”** Recovery trusts the durable decision under the declared acknowledgement contract.
7. **“No commit record means abort under any corruption.”** Only a verified complete history justifies absence reasoning.
8. **“Redo is naturally idempotent.”** Increment and logical operations require pageLSN, effect IDs, expected state, or another guard.
9. **“Undo can be repeated safely.”** Recovery must log progress; otherwise a crash can repeat a non-idempotent inverse.
10. **“Undo the CLR on abort.”** A CLR is redoable recovery progress and directs remaining undo; undoing it breaks restartability.
11. **“Prepared is a loser.”** In-doubt distributed transactions require the atomic-commit decision or explicit heuristic policy.
12. **“A B-tree split should be reversed with the row.”** Structural actions may remain while logical loser content is removed.
13. **“Undo storage is free after commit.”** Active snapshots may still need historical versions.
14. **“Database undo reverses external effects.”** Remote calls and physical-world actions require idempotent workflow/compensation.
15. **“Recovery complete means server started.”** Rows, indexes, allocations, outcomes, integrity, and application invariants must agree.
16. **“Old recovery binaries are a safe rollback.”** New mandatory record/page formats can make downgrade corrupt or impossible.

## Worked Examples

### Example 1

**Situation.** A no-force/no-steal engine crashes after T commits while its page remains old.

**Reasoning.** Let page P contain A=10 on disk. T changes A to 15 in the buffer, its durable commit record reaches the log, but P is not forced. No-steal guarantees that an uncommitted page image never reached the durable database, so recovery cannot encounter escaped loser data. No-force permits the committed update to be absent, which is exactly this crash image. Recovery must find T's durable outcome and an after-image or equivalent operation/version, install A=15, and establish the page's recovery position before exposing service. If the redo record were missing, the commit acknowledgement would have promised durability without reconstruction evidence.

**Conclusion.** Under the stated policy, redo is necessary for durability and ordinary page undo is unnecessary for crash atomicity. The conclusion changes if either force/steal assumption changes.

### Example 2

**Situation.** A steal/force engine writes T's tentative page, then T aborts; all winner pages were forced at commit.

**Reasoning.** Disk begins with B=40. T changes B to 55, and buffer pressure writes that page before T decides. T then aborts. Steal permits B=55 to escape, so the recovered database cannot trust physical presence as evidence of commitment. Force guarantees every winner's pages reached disk before acknowledgement, so no winner redo is required under this simplified model. To remove T, recovery needs a before-image B=40, a safe logical inverse, or a version/visibility scheme that makes the tentative version non-authoritative. It must also cover indexes and metadata affected by T, not only the row value.

**Conclusion.** Steal creates the undo obligation; force removes the ordinary missing-winner redo case. This matrix result is conditional on complete, untorn writes and the declared metadata policy.

### Example 3

**Situation.** Redo record 80 says increment counter by 1; pageLSN is 80 after a crash during recovery.

**Reasoning.** Suppose the durable page initially held C=7. Recovery applied record 80, producing C=8 and pageLSN=80, then crashed after the page write. Blind replay produces C=9. First verify checksum, object identity, page generation, and record applicability; only then may `pageLSN >= 80` show that this physical effect is already represented. If the engine uses logical operation logging instead, it needs an equally strong guard such as a durable unique effect ID and deterministic preconditions. A numeric LSN on corrupt or reused bytes cannot authorize the skip.

**Conclusion.** Restart-safe redo is conditional idempotence: identity and integrity validation plus a durable application guard prevent the increment from being applied twice.

### Example 4

**Situation.** T inserts key K and triggers a B-tree split. T later aborts after other transactions use the new structure.

**Reasoning.** Before T, leaf L is full. T's insertion allocates L2, redistributes entries, and installs separator S in the parent. Transaction U then inserts key J into L2 and commits. Restoring a before-image of L and the parent would delete J, orphan L2, or violate search invariants. A recovery design can treat allocation and split as a system transaction or nested top action whose structural effects remain, while T's logical entry K is removed by transaction-specific undo. Latches protect each physical step; log records and page generations make those steps restartable; transaction locks or versions protect logical isolation.

**Conclusion.** User rollback removes K but preserves the valid split and U's committed J. Whole-page restoration is unsound once later independent work depends on the structure.

### Example 5

**Situation.** Undo of LSN 50 restores B=70 and logs CLR 60 with `undoNextLSN=20`; recovery crashes.

**Reasoning.** T changed B from 50 to 70 at LSN 20 and from 70 to 65 at LSN 50. Recovery reverses 50, writes a CLR at 60 describing B=70 and setting `undoNextLSN=20`, then the compensated page reaches disk and recovery crashes. On restart, history reconstruction redoes CLR 60 if the page does not already contain it. The CLR is a record of completed compensation, not another user action, so it is never undone. The loser scan follows `undoNextLSN=20`, restores B=50, logs another compensation, and finally records transaction completion under the algorithm.

**Conclusion.** Every original action is compensated at most once in the logical undo chain despite repeated crashes; redo may repeat the CLR physically under its page guard. DBE-076 derives the complete pass algorithm.

### Example 6

**Situation.** A transaction updated at 10, created savepoint S, updated at 20 and 30, then rolls back to S.

**Reasoning.** Let LSN 10 debit account A, savepoint S store rollback target 10, LSN 20 create a provisional fee, and LSN 30 update a note. Rollback starts at the transaction's lastLSN=30. It reverses the note, records compensation pointing to 20, reverses the fee, and records compensation pointing to 10. The stop predicate is now satisfied, so debit 10 remains. The transaction stays active and can perform later actions; its transaction chain includes the CLRs so another crash or full abort knows which work is already compensated. Locks and application-visible errors follow the engine's declared partial-rollback policy.

**Conclusion.** A savepoint defines a rollback frontier, not a commit boundary. Earlier tentative work and transaction identity survive while later effects are removed restartably.

### Example 7

**Situation.** Transaction D has a durable prepare record and updates on disk but no local commit record after crash.

**Reasoning.** Participant P has voted yes in a two-phase commit protocol and durably recorded `PREPARE(D)`. Its data pages may contain D's changes, while its coordinator is temporarily unreachable. The absence of a local commit record means “decision not known here,” not “abort.” P has promised that it can commit if instructed, so it must reconstruct D's prepared state, retain the resources or recovery information required by policy, and query/recover the decision. A documented heuristic decision may exist for extreme operations, but it creates an explicit global-consistency hazard and audit obligation.

**Conclusion.** Winner/loser classification is insufficient for prepared transactions. Unilateral ordinary undo after a durable yes vote can violate distributed atomicity.

### Example 8

**Situation.** A page reports pageLSN 500, so recovery considers skipping record 400, but the checksum and object generation fail.

**Reasoning.** The buffer descriptor says “orders index, page 42, generation 9,” while the durable page header says generation 7 and its checksum fails. The displayed 500 may be torn data, stale media, or a page from a dropped and recreated object. If recovery trusts it and skips record 400, a committed effect can remain absent. If recovery applies record 400, it can write an old-format delta into the wrong object. Stop ordinary redo for this page, preserve evidence, and invoke the declared repair path: valid full-page image, replica/backup reconstruction, media recovery, or fail closed. Only after identity and integrity are re-established may LSN comparison resume.

**Conclusion.** `pageLSN` is meaningful only inside a validated page identity and history. Corruption converts a skip decision into a repair or availability decision.

### Example 9

**Situation.** A user transaction sends an email, updates the database, then aborts.

**Reasoning.** The email provider accepts message M before the local database writes its commit record. A deadlock then aborts the transaction. Database undo removes the tentative row, but the provider and recipient are outside the recovery domain; a before-image cannot retract M. A transactional outbox instead commits the business state and `MessageRequested(id=M)` atomically, after which a sender retries with a stable idempotency key and records delivery observations. If a sent message becomes semantically wrong, a correction email is a new business action, not storage-engine undo.

**Conclusion.** WAL can make the local database atomic. External effects require their own durable protocol, deduplication assumptions, reconciliation, and often explicit compensation.

### Example 10

**Situation.** A 2 TiB transaction aborts while only 100 GiB of log space remains; undo itself must emit CLRs.

**Reasoning.** The loser pins the earliest 2 TiB of history because rollback still needs it. Undo must scan that history, dirty pages, and emit CLRs before old segments become reclaimable. With only 100 GiB free, forward compensation can exhaust the same log whose head cannot advance until compensation completes: a resource deadlock. Estimate worst-case compensation and metadata volume before admitting the transaction, reserve emergency space inaccessible to normal work, throttle other writers, expose rollback progress and retained frontier, and define which segments become recyclable after durable proof. Repeatedly killing recovery preserves the debt and can worsen availability.

**Conclusion.** Recovery requires a resource invariant: enough durable capacity must remain to complete or safely stage rollback. Capacity admission is therefore part of atomicity engineering.

## Cross-Program Connections

- **Data Structures Engineering:** backward chains, priority queues, dirty-page maps, version lists, and generation-tagged pages implement recovery efficiently.
- **Data Engineering:** stream retractions and idempotent sinks resemble undo/redo but must handle distributed consumer state and business semantics.
- **Data Architecture Engineering:** backup lineage, retention, legal deletion, and point-in-time recovery depend on which before/after history remains available.
- **API and Service Engineering:** idempotency, transactional outbox/inbox, sagas, and reconciliation bridge the boundary engine rollback cannot cross.
- **Platform Engineering:** storage faults, capacity reservation, crash injection, rollout compatibility, and recovery observability determine production validity.
- **Concurrent Programming:** page latches, transaction chains, publication order, interleaved loser queues, and recovery parallelism need happens-before proofs.
- **Functional Programming:** immutable values and explicit inverse/compensation types clarify when an operation is actually reversible.
- **Object-Oriented Programming:** record-type hierarchies must preserve exhaustive versioned dispatch and forbid unsafe default handling of unknown recovery operations.
- **Security Engineering:** logs retain sensitive history and recovery parsers process privileged persistent input, requiring confidentiality, integrity, and bounds.

## References

1. C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, and P. Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM TODS* 17(1), 1992. Primary analysis/redo/undo, repeat-history, CLR, and nested-action paper; retrieved from [IBM Research](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging) on 2026-08-30.
2. PostgreSQL Global Development Group, [PostgreSQL 18: Write-Ahead Logging](https://www.postgresql.org/docs/18/wal-intro.html), reviewed 2026-08-30. Official redo and log-before-data overview.
3. PostgreSQL Global Development Group, [PostgreSQL 18: WAL Configuration](https://www.postgresql.org/docs/18/wal-configuration.html), reviewed 2026-08-30. Official checkpoint and redo-start behavior.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Write Ahead Log Settings](https://www.postgresql.org/docs/18/runtime-config-wal.html), reviewed 2026-08-30. Official full-page-write and recovery-target behavior.
5. Oracle, [MySQL 8.4 Reference Manual: InnoDB Redo Log](https://dev.mysql.com/doc/refman/8.4/en/innodb-redo-log.html), reviewed 2026-08-30. Official redo purpose, capacity, checkpoint, and recovery relationship.
6. Oracle, [MySQL 8.4 Reference Manual: InnoDB Undo Logs](https://dev.mysql.com/doc/refman/8.4/en/innodb-undo-logs.html), reviewed 2026-08-30. Official rollback and consistent-read history behavior.
7. Oracle, [MySQL 8.4 Reference Manual: InnoDB Recovery](https://dev.mysql.com/doc/refman/8.4/en/innodb-recovery.html), reviewed 2026-08-30. Official redo application and incomplete-transaction rollback behavior.
8. SQLite Project, [Atomic Commit in SQLite](https://www.sqlite.org/atomiccommit.html), reviewed 2026-08-30. Official rollback-journal page preservation and storage assumptions.
9. SQLite Project, [Write-Ahead Logging](https://www.sqlite.org/wal.html), reviewed 2026-08-30. Official WAL-frame and checkpoint design contrast.
10. Microsoft, [SQL Server Transaction Log Architecture and Management Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-log-architecture-and-management-guide?view=sql-server-ver17), reviewed 2026-08-30. Official record chains, rollback reservation, redo/undo, MinLSN, and circular-log behavior.
11. PostgreSQL Global Development Group, [`xlogrecord.h`](https://github.com/postgres/postgres/blob/master/src/include/access/xlogrecord.h), source reviewed 2026-08-30. Current record length, transaction, previous-record pointer, resource manager, and CRC fields.
12. PostgreSQL Global Development Group, [`xlogreader.h`](https://github.com/postgres/postgres/blob/master/src/include/access/xlogreader.h), source reviewed 2026-08-30. Current WAL reader state and decoded-record boundary structures.
13. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Durable treatment of logging, recovery, commit, compensation, and transaction models.

## Exercises

### Exercise 1

Derive the recovery information required by all four force/no-force and steal/no-steal policy combinations. State why the matrix is a model rather than a universal engine taxonomy.

### Exercise 2

Trace the compact example through analysis, repeat-history redo, first undo, CLR logging, a crash, CLR redo, and final undo. State the page values and next undo position at every boundary.

### Exercise 3

Design a versioned physiological update/CLR format and its validation rules. Cover identities, generations, record chains, applicability, hostile lengths, unknown versions, cycles, and resource bounds.

### Exercise 4

Compare an ARIES-style undo/redo engine with an MVCC redo-oriented engine for long transactions, historical reads, rollback latency, space retention, structural changes, and recovery availability.

### Exercise 5

Design the recovery contract and evidence for a payment service whose database writes, message publication, and external payment execution can fail independently. Include prepared work, idempotency, compensation, crash-during-recovery, security, observability, canary, and rollback.

## Answers to the Exercises

### Answer 1

Force/no-steal excludes both missing committed pages and escaped tentative pages under its exact assumptions, so ordinary page redo/undo is not required, though metadata/media recovery may be. No-force/no-steal permits missing winner pages but not escaped losers, so it needs redo or equivalent committed reconstruction. Force/steal installs all winner pages but can persist losers, so it needs undo or equivalent visibility/version handling. No-force/steal permits both and needs both directions or their equivalents. The matrix abstracts page policy; real engines mix object classes, MVCC, copy-on-write, system transactions, full images, media recovery, and product-specific durability. Determine reachable crash states per structure instead of assigning an engine one simplistic cell.

### Answer 2

The verified prefix contains updates T1:A 100→120 at 10, T2:B 50→70 at 20, T1:A 120→130 at 30, T1 commit at 40, and T2:B 70→65 at 50. Analysis makes T1 a winner and T2 a loser. Disk begins A=100/pageLSN 0 and B=65/pageLSN 50. Redo applies T1's records 10 and 30, skips B records already reflected, and reaches A=130, B=65. Undo order for T2 is 50 then 20. Compensating 50 sets B=70, writes CLR 60, and sets `undoNextLSN=20`; WAL for CLR 60 must precede persistence of that compensation.

After a crash, repeat-history redo reconstructs A=130 and B=70, including CLR 60 if the page lacks it. The CLR is not undone. Undo resumes at 20, restores B=50, logs another CLR (illustratively LSN 70) whose next pointer reaches the transaction begin/end condition, then records completion according to the algorithm. Final A=130 preserves the winner and B=50 removes the loser. A crash before a CLR becomes durable cannot leave its dependent page durable under WAL; a crash after makes the compensation redoable.

### Answer 3

Use a fixed, bounds-checkable header with stream/system ID, history, format version, record type, total/header/payload lengths, LSN/end convention, transaction ID plus incarnation, `prevLSN`, page/object ID plus allocation generation, operation subtype/flags, and checksum or authentication covering identity and payload. Update payload names the page-local action and contains sufficient redo plus undo/inverse information for its policy. A CLR carries the compensated original LSN, redo of the compensation, and `undoNextLSN`; it is explicitly redoable/non-undoable.

The reader verifies trusted start, continuity, supported mandatory version/type, bounded lengths and arithmetic, complete bytes, integrity, transaction-chain monotonicity, page/object generation, payload schema, and record-specific applicability before allocation or mutation. It detects chain cycles and caps records, payload, referenced objects, recursion, transaction count, and recovery work. Redo validates the page before pageLSN, applies only on the correct generation, and advances metadata atomically. Undo dispatch is exhaustive; unknown types stop rather than skip. Fuzz every byte boundary, length, ID, pointer, version, checksum, truncation, cycle, stale generation, and cross-segment continuation.

### Answer 4

ARIES-style steal/no-force permits flexible eviction and fast commit, repeats physical history, and physically/logically undoes losers with chains and CLRs. Long transactions can generate substantial before/after and CLR volume, retain log from old records, hold locks, and take long to roll back; system/nested top actions preserve structural work. Availability may wait for required analysis/redo and can overlap loser undo only under explicit safety rules.

An MVCC redo-oriented design appends new versions, uses durable transaction status to expose winners and hide losers, and later reclaims dead versions. Crash recovery can redo physical changes without a general loser page-undo pass, but long transactions/snapshots retain versions, transaction metadata, locks, and vacuum/purge debt. Historical reads can reuse the version history, while chain traversal and storage amplification grow. Structural/index/allocation changes still need recovery semantics. Neither dominates: compare transaction size, snapshot duration, update contention, storage, commit/recovery/rollback objectives, corruption model, and verified operational behavior.

### Answer 5

Define separate state machines for local database transaction, durable outbox message, broker acceptance, consumer inbox/deduplication, payment-provider request, and provider outcome. The database atomically commits payment intent plus unique idempotency key and outbox record; its WAL/redo/undo contract preserves or removes them together. A publisher retries until the broker acknowledges under a stated durability contract. The consumer records the message/effect ID transactionally before or with its local effect. Provider calls carry the stable idempotency key, and ambiguous timeouts trigger status query/reconciliation rather than a new payment identity.

Prepared database transactions remain in doubt until the commit protocol decides; they are not ordinary losers. A refund is a governed business compensation, not engine undo, and cannot promise reversal where the provider disallows it. Test crashes before/after every WAL flush, commit response, outbox claim/send/ack, broker delivery, inbox commit, provider acceptance/response, compensation, reconciliation, CLR, and recovery completion, including repeated crashes, duplicates, reordering, partitions, ENOSPC, corrupt records, and key unavailability. The oracle reconciles database ledger, outbox/inbox, broker IDs, provider ledger, balances, authorization, and exactly one intended net effect.

Encrypt sensitive logs with recoverable keys, minimize payload, authenticate records/transport, restrict inspection and compensation authority, audit overrides, and retain per recovery/legal policy. Observe transaction/outbox/inbox/provider states, LSNs, retry age, ambiguous outcomes, recovery/undo progress, duplicate suppression, and reconciliation differences without leaking values. Canary bounded payment classes with injected failures and verified invariants. Rollback preserves compatible WAL/page/message schemas, deduplication state, workflow code, provider idempotency semantics, archives, and keys; reject a binary rollback that cannot read emitted mandatory records.
