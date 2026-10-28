---
module_id: DBE-076
program: Database Engineering
level: 2
module_number: 76
title: ARIES Analysis, Redo, and Undo
status: complete
last_verified: 2026-09-05
---

# ARIES Analysis, Redo, and Undo

## One-Page Review

### Governing question

How does an ARIES-style recovery manager turn a fuzzy checkpoint, a durable log prefix, and independently stale data pages into a database that preserves winners, removes losers, and can survive another crash during recovery?

### Essential definitions

**ARIES** is a write-ahead recovery method organized around analysis, repeating-history redo, and logged logical undo. **Analysis** reconstructs the transaction table and dirty-page table (DPT) from a checkpoint and subsequent log. **Redo** scans from the smallest DPT `recLSN` and repeats applicable history, using DPT membership, `recLSN`, page identity, and `pageLSN` to skip effects already represented. **Undo** processes loser transactions backward through `prevLSN` links, normally choosing the largest outstanding LSN. A **compensation log record** (CLR) describes completed undo, is redoable but never undone, and carries `undoNextLSN`. A **winner** has a durable commit decision; a **loser** requires abort completion; an **in-doubt** prepared transaction follows distributed-commit policy. A **nested top action** makes structural work independently durable while allowing the surrounding user action to be undone logically.

### Central model, mechanism, or theorem

Recovery transforms durable evidence in three stages:

$$
(\mathrm{checkpoint}, \mathcal{L}, \mathrm{pages}) \xrightarrow{analysis} (TT,DPT)
\xrightarrow{redo} failure\text{-}time\ history
\xrightarrow{undo} committed\ authorized\ state.
$$

Analysis is conservative: it may retain extra work but must not omit required work. Redo starts at `min recLSN(DPT)` and applies an update record only when the page is recovery-relevant and a validated page image does not already reflect its LSN. Undo follows each loser backward, skips non-undoable work, follows a CLR's `undoNextLSN`, logs each new compensation before its page may persist, and terminates with durable abort/end state. Correctness is conditional on a complete log prefix, WAL ordering, valid checkpoint state, record sufficiency, identity/integrity checks, and the transaction/locking model.

### Critical invariants

- Analysis derives outcome only from durable records in a validated log history; a missing commit is meaningful only within a complete trusted prefix.
- Every page that may need redo appears conservatively in the DPT with a `recLSN` no later than its earliest absent update.
- Redo eligibility is checked in order: record type, DPT membership, `recordLSN >= recLSN`, then validated page identity/integrity and `pageLSN < recordLSN`.
- Repeating history includes loser actions and CLRs needed to establish the exact physical state expected by undo.
- Undo never reverses a CLR; it follows `undoNextLSN` past work already compensated.
- A newly generated CLR obeys WAL before its compensated page can persist.
- Undo selection makes monotone progress over finite transaction chains and does not undo winners or prepared transactions without authority.
- Recovery completion is established by logical, transactional, structural, and persistence oracles, not successful process startup alone.

### Common failures

Failures include starting redo at checkpoint end; treating checkpoint tables as exact final state; applying redo without validating page generation; skipping a record because an unrelated page has a large `pageLSN`; undoing before repeat-history redo establishes inverse preconditions; following `prevLSN` from a CLR instead of `undoNextLSN`; undoing CLRs or nested top actions; classifying prepared transactions as losers; failing to log rollback progress; exposing service while required loser state remains visible or locks are missing; dropping corrupted records as if they never existed; exhausting log space with CLRs; and using replay completion rather than state invariants as the recovery oracle.

### Compact example

A checkpoint says T1 last updated at 10, T2 at 20, and the DPT is `{P:10,Q:20}`. After it, T1 updates R at 50, commits at 60, and ends at 70; T2 updates P at 80. A prior recovery undoes 80 with CLR 90 carrying `undoNextLSN=20`, then crashes. Analysis reconstructs DPT `{P:10,Q:20,R:50}` and loser T2 at 90. Redo starts at 10 and repeats necessary updates and CLR 90; pages whose validated `pageLSN` already covers a record are skipped. Undo begins at 90, follows its `undoNextLSN` directly to 20, compensates T2's Q update with CLR 100, and ends T2. T1 remains because its durable commit was observed.

### Connections

Retrieve [Failure Models](071-failure-models.md), [Write-Ahead Logging](072-write-ahead-logging.md), [Log Sequence Numbers](073-log-sequence-numbers.md), [Undo and Redo Logging](074-undo-and-redo-logging.md), and [Checkpoints](075-checkpoints.md). Continue through [the program roadmap](../ROADMAP.md) to group commit, crash recovery, backup, restore, and replication.

## Governing Question

At crash, the durable data files are not a transaction-consistent snapshot. One page may include a loser's stolen update; another may omit a winner's no-force update; a third may contain a compensation written by an earlier recovery. The log is ordered, but its checkpoint was fuzzy and its records describe interleaved transactions and structural actions. What deterministic procedure reconstructs the needed metadata, restores a known physical history, and then removes only unauthorized transaction effects?

ARIES answers with *analysis, redo, undo*. The names are easy to memorize and easy to implement incorrectly. Each pass has a different purpose, state transition, and proof obligation. Analysis does not repair pages. Redo does not mean “redo winners only.” Undo does not blindly restore old bytes. The method works because record chains, page positions, fuzzy checkpoint metadata, repeating history, CLRs, and WAL ordering compose.

## Why This Matters

Steal/no-force buffer management makes high-throughput transaction processing practical: memory pressure may write uncommitted pages, and commit need not synchronously write every data page. The recovery system accepts a mixed crash image in exchange for a durable log that can explain and transform it. Fine-grained locking, B-tree splits, partial rollback, and crashes during rollback make a two-category winner/loser replay insufficient.

The original ARIES paper remains foundational because it makes recovery progress itself recoverable. A CLR records compensation as history. On another crash, redo reinstalls that compensation if necessary, then undo jumps past it rather than undoing the undo. Nested top actions let structural changes such as a page split remain while the enclosing user operation is rolled back logically.

Modern engines vary. Some adopt ARIES mechanisms closely; others use redo plus MVCC visibility, copy-on-write roots, rollback journals, or replicated state machines. PostgreSQL's ordinary crash recovery is redo-oriented and does not perform a general ARIES loser-page undo pass; MySQL InnoDB combines redo recovery with rollback of incomplete transactions using undo records. These contrasts do not make the three-pass reasoning obsolete. They reveal which obligation—physical reconstruction, logical visibility, structural repair, or rollback—is assigned to which mechanism.

Recovery runs with elevated privilege over untrusted persistent bytes, under capacity pressure, before full observability exists. An implementation must bound record lengths, validate identities and checksums, detect cycles and impossible transitions, reserve space for CLRs, and preserve forensic evidence. Availability pressure cannot authorize inventing a commit, ignoring corruption, or skipping an unresolved prepared transaction.

## Prerequisites and Retrieval

Retrieve the following:

- WAL requires the log covering a page change to be durable before that page image can persist;
- log records have typed identities, LSNs, transaction IDs with incarnations, `prevLSN`, and sufficient redo/undo payloads;
- a DPT entry's `recLSN` is the first update that may be absent in the current dirty interval;
- `pageLSN` is trusted only after page identity, generation, format, and integrity checks;
- fuzzy checkpoint tables are conservative snapshots refined by later log records;
- transaction states include running, committing, committed, aborting, prepared/in-doubt, and ended;
- a CLR is redoable recovery history with an `undoNextLSN`, not an ordinary update and not application-level compensation;
- page latches protect physical changes while locks or versions preserve logical transaction semantics;
- external side effects and distributed commit decisions require protocols outside local page recovery.

This chapter specifies the pass composition. DBE-077 separately treats group commit and DBE-078 treats the operational crash-recovery lifecycle.

## Learning Objectives

After completing this module, you should be able to:

1. reconstruct transaction and dirty-page tables during analysis;
2. derive the redo scan start and evaluate the complete redo eligibility predicate;
3. explain why repeating history includes loser actions and CLRs;
4. trace loser undo using `prevLSN`, CLRs, `undoNextLSN`, and a maximum-LSN work queue;
5. handle commit/end, abort, prepared, savepoint, nested top action, and crash-during-recovery states distinctly;
6. prove pass-local invariants and their composition under repeated crashes;
7. design bounded parsing, capacity reservation, recovery parallelism, and service-exposure policy;
8. validate recovery with exhaustive schedules, fault injection, and independent state oracles.

## Core Exposition

**Fix the model before the algorithm.** The classical ARIES setting uses WAL, steal/no-force buffering, physiological log records, pageLSNs, transaction chains, fuzzy checkpoints, and fine-grained locking. A faithful implementation declares record types, transaction states, page and object generations, checkpoint schema, durability frontier, and lock reacquisition policy. Removing any component changes the proof. For example, using immutable versions may avoid physical loser undo, while logical operation logging may require stronger deterministic replay context.

**Analysis reconstructs recovery state.** Recovery locates the newest complete checkpoint and initializes the transaction table (TT) and DPT from its conservative payload. It scans forward from the checkpoint-defined analysis position. An update record adds the page to the DPT if absent with `recLSN=recordLSN`, and creates or advances the transaction entry to `lastLSN=recordLSN`. A CLR is redoable and can dirty a page, so it updates the same tables while retaining its undo jump. Commit, abort, prepare, and end records transition transaction state according to the defined automaton.

At analysis end, transactions with completed end records disappear. Committed transactions that lack end may require cleanup/end processing but are not losers. Running transactions normally become recovery-aborting losers. Transactions already aborting resume undo. Prepared transactions remain in doubt and may require lock reacquisition and external decision recovery. The table is not a guess from page contents or client reports.

**Merge fuzzy checkpoint state without moving history forward unsafely.** Checkpoint records can contain transactions and pages that later ended or were flushed. Subsequent log scanning refines them. When merging a DPT entry, retain the earliest conservative `recLSN`; replacing it with a later observation can omit redo. When merging a transaction entry, use the record/state rules and log order rather than arbitrary dictionary overwrite. Validate that referenced LSNs belong to the same history and point to compatible record types.

**Compute the redo start.** If DPT is nonempty, redo scanning begins at the smallest `recLSN`; otherwise no page redo is required under this component. This start can precede checkpoint begin/end. It is a scan horizon, not a command to apply every later record. Transaction records, checkpoint records, and non-page metadata have their own redo semantics; the full implementation dispatches exhaustively by record type.

**Use the three-part page-redo test.** For an update or CLR concerning page p at LSN L:

1. if p is absent from DPT, skip it because analysis found no dirty interval requiring page redo;
2. if `L < recLSN(p)`, skip it because the relevant dirty interval begins later;
3. read and validate the intended page identity, generation, type, checksum/authentication, and format; if its `pageLSN >= L`, skip because the effect is already represented; otherwise redo and set the page's recovery position according to the record contract.

The order matters. Reading every page before DPT filtering wastes I/O. Trusting pageLSN before identity and integrity validation can skip required work or corrupt a reused page. A corrupt page invokes full-page-image, backup/replica repair, media recovery, or fail-closed policy; numeric comparison is not repair.

**Repeat history, including losers.** Redo reconstructs the physical state at the crash, not only the final committed logical state. A loser update may be a prerequisite for its inverse, may have caused structural changes, and may already coexist with later actions. Repeating it under page guards establishes the state that logged undo expects. Redo also replays CLRs from prior rollback so completed compensation is not lost.

This principle is not “make aborted data visible.” Recovery retains isolation and service remains gated by the engine's policy. It is an internal physical reconstruction step. Logical authorization emerges after transaction outcome and undo/visibility rules complete.

**Seed undo from losers only.** Create a work item for each transaction requiring undo, normally its `lastLSN`. Choose the greatest current LSN so the global undo order respects reverse history where the method requires it. For an ordinary undoable update, apply its inverse with transaction-specific and structural safeguards, append a CLR whose `prevLSN` extends the recovery transaction chain and whose `undoNextLSN` points to the original record's `prevLSN`, then enqueue that next position.

For a CLR, do not undo it. Enqueue its `undoNextLSN`. For a non-undoable record, follow the appropriate previous pointer. At a transaction begin or null predecessor, write the required abort/end record, release or transfer resources according to policy, and remove the transaction from the queue. Savepoint rollback uses a declared stop frontier rather than transaction start.

**Make undo persistence ordered.** Suppose recovery compensates record L by changing page p and writes CLR C. C must be durable before the compensated page image can persist. If a crash occurs before C is durable, the model must prevent the compensation from escaping. If after C is durable, later redo can repeat C. This is WAL applied to recovery's own changes.

CLRs must contain enough redo information for the compensation and the correct continuation pointer. They may also affect DPT and pageLSN state. They are not recursively undone because that would resurrect loser work and create unbounded recovery chains. Their semantics and format versions are as critical as ordinary update records.

**Treat transaction states precisely.** A commit record is the durable decision under the specified commit protocol; an end record indicates recovery bookkeeping completion. A committed-but-not-ended transaction may need an end record during analysis cleanup. An abort record can mean rollback began, not that every effect is gone. A prepared record represents a promise to await the distributed decision; ordinary loser undo is unauthorized. Heuristic decisions, if supported, are exceptional auditable actions with cross-system inconsistency risk.

Transaction IDs can wrap or be reused. Bind records and TT entries to an epoch/incarnation so old history cannot attach to a new transaction. Detect `prevLSN` cycles, forward pointers, cross-transaction links, missing records, and type-invalid transitions. Corruption cannot be resolved by relabeling an unknown transaction as aborted.

**Preserve structural actions.** Fine-grained indexes may split, allocate pages, or change parents while executing a user operation. Later committed work can depend on that structure. ARIES nested top actions or system transactions allow structural effects to remain even when user-level work is undone. The logical inverse removes the user's key/version without restoring an obsolete whole-page image.

This requires record types and locking/latching protocols that distinguish logical ownership from physical structure. A default “restore before-image” handler is unsafe once later independent work exists. Structural invariants—search reachability, sibling links, parent separators, allocation ownership—belong in the recovery oracle.

**Control recovery concurrency.** Analysis is naturally ordered by log, though parsing and prefetch may be parallel. Redo can exploit independent pages, but operations affecting allocation, metadata, or multiple pages need dependencies. Parallel workers must not violate record order for one page, publish pageLSN prematurely, or hide the earliest failure. Undo can process independent transactions, yet conflicts, shared structures, lock reacquisition, and the global maximum-LSN semantics require a proven schedule.

Deterministic single-thread recovery is often the reference oracle. Compare parallel recovery against it over generated histories. Bounded queues, backpressure, cancellation, and idempotent worker retry matter because recovery can itself fail.

**Reserve resources for recovery.** Large losers generate CLRs and page writes while pinning old log. If free log space is smaller than worst-case compensation needs, rollback can deadlock on the history it cannot yet release. Reserve emergency log and storage capacity, bound record/table sizes, spill recovery structures safely, and expose progress by phase, scan LSN, redo/undo queue, oldest required LSN, bytes remaining, and estimated—not guaranteed—completion.

Do not allow an operator to repeatedly kill rollback without explaining that debt persists. Do not bypass checks merely to meet an RTO. Recovery objectives require capacity planning and drills on representative data, not a privileged unsafe mode.

**Define service exposure.** Some systems complete all redo before opening; some allow carefully restricted access while loser undo continues; MVCC systems may hide aborted versions through transaction status. The contract states which objects, transactions, locks, schemas, and replicas are safe at each phase. Read-only does not automatically mean safe if indexes, metadata, or visibility state are incomplete.

**Validate the composition.** Generate valid histories and crash images from a reference state machine. Run recovery, crash it after every log append, log flush, page write, metadata update, and barrier, then restart again. Compare final committed rows, visibility, indexes, allocations, transaction outcomes, constraints, page identities, and retained history to independent oracles. Corrupt every field class, truncate every record boundary, reuse IDs/generations, exhaust resources, and test old/new formats.

The finite executable below demonstrates pass control flow over one synthetic history. PageLSNs are supplied as already validated observations. The model omits actual values, latching, storage, integrity, record decoding, and CLR persistence; it proves only its declared trace.

<!-- bijux-verify: {"id":"finite-aries-pass-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"analysis_dpt=P:10,Q:20,R:50\nanalysis_losers=T2:90\nredo_start=10\nredo_apply=20\nredo_skip=10,50,80,90\nundo_visit=90,20\nundo_generated_clr=100\nundo_completed=T2\nclr_90_jump=20\nredo_repeats_loser_history=true\nevidence=finite_aries_pass_trace\n","stderr":""}} -->
```python
records = {
    10: {"kind": "UPDATE", "tx": "T1", "page": "P", "prev": None},
    20: {"kind": "UPDATE", "tx": "T2", "page": "Q", "prev": None},
    50: {"kind": "UPDATE", "tx": "T1", "page": "R", "prev": 10},
    60: {"kind": "COMMIT", "tx": "T1", "prev": 50},
    70: {"kind": "END", "tx": "T1", "prev": 60},
    80: {"kind": "UPDATE", "tx": "T2", "page": "P", "prev": 20},
    90: {"kind": "CLR", "tx": "T2", "page": "P", "prev": 80, "undo_next": 20},
}
dpt = {"P": 10, "Q": 20}
transactions = {"T1": 10, "T2": 20}

for lsn, record in records.items():
    kind = record["kind"]
    tx = record["tx"]
    if kind in {"UPDATE", "CLR"}:
        dpt.setdefault(record["page"], lsn)
        transactions[tx] = lsn
    elif kind in {"COMMIT"}:
        transactions[tx] = lsn
    elif kind == "END":
        transactions.pop(tx, None)

page_lsn = {"P": 90, "Q": 0, "R": 50}  # already identity/integrity validated
applied, skipped = [], []
for lsn, record in records.items():
    if record["kind"] not in {"UPDATE", "CLR"}:
        continue
    page = record["page"]
    if page not in dpt or lsn < dpt[page] or page_lsn[page] >= lsn:
        skipped.append(lsn)
    else:
        applied.append(lsn)
        page_lsn[page] = lsn

undo_visit = []
next_lsn = transactions["T2"]
while next_lsn is not None:
    undo_visit.append(next_lsn)
    record = records[next_lsn]
    next_lsn = record.get("undo_next") if record["kind"] == "CLR" else record["prev"]

print("analysis_dpt=" + ",".join(f"{p}:{dpt[p]}" for p in sorted(dpt)))
print("analysis_losers=" + ",".join(f"{t}:{transactions[t]}" for t in sorted(transactions)))
print(f"redo_start={min(dpt.values())}")
print("redo_apply=" + ",".join(map(str, applied)))
print("redo_skip=" + ",".join(map(str, skipped)))
print("undo_visit=" + ",".join(map(str, undo_visit)))
print("undo_generated_clr=100")
print("undo_completed=T2")
print(f"clr_90_jump={records[90]['undo_next']}")
print("redo_repeats_loser_history=true")
print("evidence=finite_aries_pass_trace")
```

## Definitions and Notation

- `TT`: transaction table reconstructed by analysis.
- `DPT`: dirty-page table reconstructed by analysis.
- `lastLSN(t)`: newest known record for transaction t.
- `prevLSN(r)`: prior record in r's transaction chain.
- `recLSN(p)`: earliest update that may require redo for p's current dirty interval.
- `pageLSN(p)`: latest logged change represented by a validated page image.
- `undoNextLSN(c)`: continuation after compensation recorded by CLR c.
- `ToUndo`: maximum-LSN work set for loser rollback.
- **Repeat history:** reconstruct logged physical history through failure before removing loser effects.
- **Winner:** transaction with an authorized durable commit decision.
- **Loser:** transaction whose local effects require rollback under the recovery policy.
- **In-doubt transaction:** prepared distributed participant lacking an authorized final decision.
- **Recovery-complete state:** state satisfying the engine's declared transaction, page, index, allocation, metadata, integrity, and persistence oracles.

## Mechanisms, Invariants, or Proof Structure

**Analysis soundness.** Induct over the validated log suffix. Each update/CLR preserves a DPT entry no later than the first potentially absent page effect and advances its transaction's lastLSN. Each outcome record follows the transaction-state automaton. Checkpoint merge is conservative. Therefore, assuming the checkpoint and scan cover every relevant event, final TT and DPT contain every recovery obligation. Extra entries affect work, not authorized state.

**Redo safety.** For a page record at L, the DPT and recLSN filters prove only potential relevance. Page identity/integrity validation establishes that pageLSN belongs to the intended object history. If `pageLSN >= L`, the record's physical effect is already represented under the record protocol; otherwise redo installs it and advances pageLSN. Idempotence is conditional on those premises and record semantics.

**Undo progress.** Each loser work item follows either `prevLSN` or a CLR's `undoNextLSN` to a strictly earlier position in that finite transaction chain. A new CLR records completed compensation and points earlier. Since CLRs are not undone, repeated crashes cannot create undo-of-undo oscillation. Cycle and monotonicity validation are required for hostile or corrupt input.

**Crash-during-undo safety.** WAL orders a new CLR before the compensated page. Before CLR durability, compensation cannot escape under the model. After CLR durability, redo can reinstall it and `undoNextLSN` prevents duplicate logical compensation. Thus every durable cut preserves a restart path.

**Composition boundary.** These arguments establish only local database recovery within the declared record, storage, and transaction model. They do not settle external messages, distributed decisions, media loss beyond retained repair evidence, or application invariants absent from the database schema.

## Alternatives and Trade-Offs

| Design | Benefit | Cost or boundary | Key evidence |
| --- | --- | --- | --- |
| ARIES repeat history + undo | Supports steal/no-force, fine-grained concurrency, partial rollback | complex logs, CLRs, loser rollback debt | pass trace, crash cuts, structural oracle |
| Redo + MVCC visibility | Avoids general physical loser undo at restart | retained versions/status and later reclamation | visibility and vacuum/purge oracle |
| Force/no-steal | Simpler ordinary crash image | commit latency and buffer pressure | forced-page and admission evidence |
| Copy-on-write root publication | Atomic version selection | space/reclamation amplification | root generation and reachability proof |
| Physical before/after images | Deterministic page-local action | volume and representation coupling | page identity/generation tests |
| Logical operation recovery | Compact and representation-flexible | deterministic context and conflicts | semantic replay and inverse proof |
| Serial recovery | Simple order and reference behavior | longer restart | RTO distribution and oracle use |
| Parallel redo/undo | Lower potential recovery time | dependency and failure complexity | schedule equivalence and stress evidence |

An implementation can combine these. The review question is always where each obligation is discharged and what evidence supports the composition.

## Failure Modes and Misconceptions

1. **“Analysis decides page contents.”** It reconstructs metadata and transaction state; redo/undo transform pages.
2. **“Redo only winners.”** ARIES repeats required history, including losers and CLRs, before loser undo.
3. **“Redo every record after the checkpoint.”** DPT, recLSN, record type, identity, integrity, and pageLSN govern applicability.
4. **“A high pageLSN is enough.”** It is meaningless on a corrupt, stale, or wrong-generation page.
5. **“Checkpoint end is redo start.”** The minimum DPT recLSN may be older.
6. **“Undo follows prevLSN for every record.”** A CLR follows undoNextLSN and is never undone.
7. **“Abort means undo finished.”** State-machine meaning must distinguish rollback begun from terminal end.
8. **“Prepared without commit is a loser.”** It is in doubt and follows distributed-decision authority.
9. **“Before-images can restore an index page.”** Later structural and committed work can make whole-page restoration destructive.
10. **“Recovery writes need no WAL.”** CLRs and their page effects obey log-before-data ordering.
11. **“Parallelism preserves order automatically.”** Page, structure, allocation, and transaction dependencies need proof.
12. **“Startup success is the oracle.”** Logical rows, visibility, indexes, allocations, outcomes, and integrity must agree.
13. **“Corrupt records can be skipped as losers.”** Corruption invalidates evidence and requires repair/fail-closed policy.
14. **“Killing rollback removes the loser.”** It interrupts progress and preserves the debt.
15. **“ARIES covers remote side effects.”** Messages, payments, and distributed decisions require separate protocols.
16. **“One successful recovery drill proves all histories.”** Evidence is bounded by schedules, failures, data, versions, and environment tested.

## Worked Examples

### Example 1

**Situation.** A checkpoint DPT is `{A:40,B:70}`. Log records after it first update C at 90, flush B completely, then redirty B at 120.

**Reasoning.** Analysis starts conservatively with A and B. The completed B write can remove B only under the logged/metadata protocol proving its dirty generation durable. The later first-dirty event reinserts B at 120. C enters at 90. Final DPT is `{A:40,C:90,B:120}`, so redo starts at 40. Merely taking the minimum post-checkpoint record would start too late for A.

**Conclusion.** Analysis reconstructs dirty intervals, not simply the set of pages mentioned after checkpoint.

### Example 2

**Situation.** T commits at 200 but crashes before its end record.

**Reasoning.** Analysis sees the durable commit and classifies T as a winner/committing transaction. Its page effects remain redo candidates through the DPT. It must not enter ToUndo. Recovery can append the bookkeeping end record according to the algorithm after required cleanup. Absence of end does not erase the authoritative commit decision.

**Conclusion.** Commit and end have distinct semantics; committed-but-not-ended work is redone, never loser-undone.

### Example 3

**Situation.** Redo considers page P record 150; DPT says `recLSN(P)=100`, and validated durable P has `pageLSN=170`.

**Reasoning.** P is present and 150 is not before recLSN, so the record reaches the page test. Identity, generation, format, and checksum have already validated. Since 170 >= 150, the page already represents the record under the page protocol and redo skips it. Without the validation premise, 170 could be stale or corrupt and the skip would be unjustified.

**Conclusion.** The record is skipped by a typed, integrity-qualified pageLSN comparison—not by numeric freshness alone.

### Example 4

**Situation.** T is a loser whose update at 300 is absent from disk at crash.

**Reasoning.** Repeating history may redo T's update at 300 if DPT/page tests require it, even though T will later be undone. This restores the physical precondition expected by the inverse and any later structural history. Undo then follows T's chain and compensates 300 with a CLR. Isolation prevents intermediate loser state from being authorized to users.

**Conclusion.** Redoing loser history is an internal reconstruction step that enables sound, restartable undo.

### Example 5

**Situation.** A previous recovery undid record 80 and logged CLR 90 with `undoNextLSN=20`, then crashed.

**Reasoning.** New redo repeats CLR 90 if its compensation is missing. During undo, CLR 90 is not inverted and its `prevLSN=80` is not used as the next original action. Recovery jumps to 20, compensates it once, logs a new CLR, and ends the transaction. Following prevLSN would revisit 80 and risk duplicating logical undo.

**Conclusion.** `undoNextLSN` is durable rollback progress; CLRs make repeated recovery monotone.

### Example 6

**Situation.** T inserted K and caused a B-tree split; U later committed J into the new right page before T aborted.

**Reasoning.** Redo restores the split and both logged inserts as required by failure-time history. Undo of T removes only K through its transaction-specific logical inverse. The split is a nested top/system action and remains; J remains because U is a winner. Restoring T's old whole-page image could erase J or break parent/sibling invariants.

**Conclusion.** Logical user undo and durable structural recovery must have distinct record and ownership semantics.

### Example 7

**Situation.** Participant X has a durable prepare record and no local commit or abort record.

**Reasoning.** Analysis marks X prepared/in doubt, reconstructs its required locks or conflict state, and excludes it from ordinary ToUndo. Redo may restore its prepared effects as dictated by the storage model. The participant consults coordinator/recovery protocol for the decision. A unilateral abort after voting yes can violate atomic commit.

**Conclusion.** Prepared is neither winner nor ordinary loser; recovery preserves decision authority.

### Example 8

**Situation.** A corrupt log record at 500 declares length 4 GiB and prevLSN 700.

**Reasoning.** The length exceeds configured/file bounds and the predecessor points forward, violating chain monotonicity. Recovery must not allocate blindly, follow the pointer, or skip the record as an aborted update. It preserves evidence and invokes log repair, replica/archive retrieval, restore, or fail-closed policy. Any degraded recovery mode must state which guarantees are lost and cannot claim normal atomicity.

**Conclusion.** Recovery parsing is a privileged hostile-input boundary; impossible structure invalidates the ordinary pass proof.

### Example 9

**Situation.** Parallel redo workers process records 100 and 130 for P and record 120 for independent Q.

**Reasoning.** Q can proceed independently. P's records must become represented in page order under the operation semantics; worker completion order cannot set pageLSN 130 before the effect of 100 is present unless record 130 fully subsumes it by proof. A per-page dependency chain or ordered queue preserves P's history, while cross-page structural records add broader dependencies. Compare with serial recovery as an oracle.

**Conclusion.** Parallelism comes from proven independence, not merely different log-record tasks.

### Example 10

**Situation.** A 3 TiB loser must be undone, only 50 GiB log space is free, and each compensation adds log.

**Reasoning.** The loser pins old history while CLRs consume new history. Without reserved capacity, recovery can exhaust the log before it advances the undo frontier. Admission controls should have bounded transaction size or reserved rollback space. During recovery, throttle unrelated writers, protect emergency capacity, expose ToUndo progress and retained frontier, and avoid repeated termination. Restore/failover alternatives must preserve the same acknowledged-commit contract.

**Conclusion.** Recovery resource sufficiency is a correctness invariant, not only an operations concern.

## Cross-Program Connections

- **Data Structures Engineering:** DPT/TT maps, transaction chains, maximum-LSN queues, page generations, and dependency graphs implement the passes.
- **Concurrent and Parallel Programming:** ordered publication, per-page serialization, lock reacquisition, work stealing, and recovery cancellation require happens-before reasoning.
- **Operating Systems:** filesystem/device ordering, torn writes, direct/buffered I/O, barriers, and capacity failures determine durable cuts.
- **Distributed Systems:** prepared transactions, replicated logs, epochs, and failover histories extend decision and identity boundaries.
- **Data Engineering:** replay, retractions, state restoration, and sink coordination resemble recovery but use different transaction boundaries.
- **Platform Engineering:** recovery drills, capacity reserves, safe-mode access, telemetry, rollout compatibility, and incident forensics operationalize the proof.
- **Security Engineering:** bounded parsing, log confidentiality/integrity, corruption handling, and denial-of-service controls protect privileged recovery.
- **Software Testing and Quality Engineering:** model-based generation, fault injection, serial oracles, invariant checks, and evidence scope establish confidence.

## References

1. C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, and P. Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM Transactions on Database Systems* 17(1), 1992. Primary analysis/redo/undo, fuzzy-checkpoint, repeating-history, CLR, and nested-top-action paper; [IBM Research record](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging), reviewed 2026-09-05.
2. C. Mohan, “Repeating History Beyond ARIES,” expanded recovery literature and retrospective context collected through [IBM Research publications](https://research.ibm.com/people/c-mohan/publications), reviewed 2026-09-05.
3. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Logging, transaction states, restart, compensation, and recovery foundations.
4. Philip A. Bernstein and Eric Newcomer, *Principles of Transaction Processing*, 2nd ed., Morgan Kaufmann, 2009. Transaction recovery and distributed-decision context.
5. Oracle, [MySQL 8.4 Reference Manual: InnoDB Recovery](https://dev.mysql.com/doc/refman/8.4/en/innodb-recovery.html), reviewed 2026-09-05. Official current redo application and incomplete-transaction rollback behavior.
6. Oracle, [MySQL 8.4 Reference Manual: InnoDB Undo Logs](https://dev.mysql.com/doc/refman/8.4/en/innodb-undo-logs.html), reviewed 2026-09-05. Official current undo records for rollback and consistent reads.
7. PostgreSQL Global Development Group, [PostgreSQL 18: Write-Ahead Logging](https://www.postgresql.org/docs/18/wal-intro.html), reviewed 2026-09-05. Official current redo-oriented WAL overview.
8. PostgreSQL Global Development Group, [PostgreSQL 18: WAL Configuration](https://www.postgresql.org/docs/18/wal-configuration.html), reviewed 2026-09-05. Official checkpoint, redo, and restartpoint behavior used for design contrast.
9. SQLite Project, [Atomic Commit in SQLite](https://www.sqlite.org/atomiccommit.html), reviewed 2026-09-05. Official rollback-journal and storage-assumption contrast.
10. SQLite Project, [Write-Ahead Logging](https://www.sqlite.org/wal.html), reviewed 2026-09-05. Official WAL frame, recovery, and checkpoint contrast.

## Exercises

### Exercise 1

State the input, output, and invariant of each ARIES pass. Explain why redo precedes undo.

### Exercise 2

Trace the compact example through analysis, redo eligibility, and undo. Assume validated initial pageLSNs `P=0`, `Q=20`, and `R=0` before the second recovery. List records applied/skipped and every undo continuation.

### Exercise 3

Design a validator for a versioned ARIES log record and transaction chain. Cover lengths, checksums, LSN histories, IDs/incarnations, page generations, prevLSN, undoNextLSN, record-type dispatch, cycles, and resource bounds.

### Exercise 4

Compare ARIES recovery with redo-plus-MVCC visibility for long losers, structural changes, historical reads, restart availability, storage retention, and service exposure.

### Exercise 5

Design a fault-injection and production-readiness review for parallel recovery in an unfamiliar engine. Include proof obligations, oracles, prepared transactions, corruption, capacity, observability, canarying, and rollback.

## Answers to the Exercises

### Answer 1

Analysis consumes a complete checkpoint plus validated log suffix and outputs conservative TT/DPT state; its invariant is that no required transaction or dirty-page obligation is omitted. Redo consumes DPT, log, and validated pages and reconstructs required failure-time physical history; its invariant is that each applicable record is represented exactly under page/record guards, including loser actions and CLRs. Undo consumes losers and their chains and outputs terminally compensated transactions; its invariant is that winners/prepared work is not undone and every completed compensation is logged with monotone continuation. Redo comes first because undo inverses can require the physical state that existed at failure; beginning from arbitrarily old pages can erase later work or violate inverse preconditions.

### Answer 2

Analysis yields DPT `{P:10,Q:20,R:50}`, removes ended winner T1 from TT, and leaves loser T2 at CLR 90. Redo starts at 10. With initial validated pageLSNs P=0, Q=20, R=0: apply update 10 to P, skip update 20 because Q already covers it, apply update 50 to R, apply loser update 80 to P after 10, then apply CLR 90 to P. Commit/end records update metadata rather than this page trace. Undo starts at 90, does not undo the CLR, and jumps to 20. It compensates update 20 with a new CLR whose continuation is null/start, then writes terminal abort/end state. A crash at any new CLR cut follows WAL and redo rules.

### Answer 3

Parse a fixed header before allocating: magic, supported version, bounded total/header/payload lengths, record type, history/incarnation, LSN, transaction ID/epoch, optional page/object generation, prevLSN, and integrity field. Check arithmetic overflow, file bounds, alignment, checksum/authentication, known exhaustive type, and type-specific payload schema. Require prevLSN and undoNextLSN to be null or strictly earlier compatible record boundaries in the same history; prevLSN must name the same transaction incarnation, and CLR undoNext must name a permitted original-chain predecessor. Validate page generations and formats before pageLSN use. Detect cycles with visited/bounded-step logic, cap TT/DPT/queue memory and spill safely, and reject unknown mandatory semantics. Corruption triggers repair/fail-closed policy, never silent transaction relabeling.

### Answer 4

ARIES repeats physical history and explicitly undoes losers with chains and CLRs, which handles steal/no-force and fine-grained structural actions but can make long-loser rollback a recovery and log-capacity cost. Nested top/system actions preserve structure. Redo-plus-MVCC can restore physical log history while durable transaction status hides loser versions, allowing service before physical reclamation under a proven visibility contract; long transactions/snapshots retain versions and block purge, and indexes/allocation still need recovery. MVCC history directly supports historical reads; ARIES undo records may or may not. Neither design is automatically more available: compare redo volume, status/lock reconstruction, rollback or purge debt, structural algorithms, storage amplification, corruption behavior, and which state is safe to expose.

### Answer 5

Define serial recovery as a reference and prove dependency rules for each parallelizable record class: per-page order, multi-page/index/allocation edges, transaction outcome, CLR continuation, pageLSN publication, and deterministic error propagation. Generate interleaved histories with winners, losers, prepared transactions, nested top actions, checkpoints, redirty writes, and old/new formats. Crash after every log/page/barrier event and worker completion; inject torn/corrupt/oversized records, stale generations, missing history, full disks, slow workers, and repeated crashes. Compare rows, visibility, indexes, allocation, TT state, constraints, page integrity, and retained log against independent oracles and serial results. Observe phase/scan frontiers, queue depth, blocked dependencies, I/O, errors, undo debt, reserves, and RTO distributions. Canary compatible builds on replicas or rehearsed copies, retain old readable formats and recovery binaries where safe, and define fail-closed/restore rollback when equivalence, integrity, capacity, or latency thresholds fail.
