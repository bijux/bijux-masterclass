---
module_id: DBE-078
program: Database Engineering
level: 2
module_number: 78
title: Crash Recovery
status: complete
last_verified: 2026-09-05
---

# Crash Recovery

## One-Page Review

### Governing question

How should a database move from an unclean stop to an authoritative serving state while fencing stale writers, validating durable evidence, executing recovery, and refusing unsafe shortcuts when logs, pages, resources, or operator assumptions fail?

### Essential definitions

A **crash** is an unplanned loss of execution continuity; its durability effects depend on the declared process, kernel, host, power, storage, and failure-domain model. **Crash recovery** is the controlled lifecycle that validates identity and persistent state, reconstructs the database using its recovery algorithm, verifies postconditions, and gates service exposure. **Fencing** prevents an old or competing writer from continuing to mutate the same authority. A **recovery epoch** distinguishes one ownership/history incarnation from another. **Bootstrap metadata** identifies the database, format, checkpoint, log history, and recovery mode. A **recovery target** is the exact endpoint or condition to which history may be applied. **Recovery complete** means declared logical, transactional, structural, and persistence invariants hold—not merely that a process accepts connections. **Unknown outcome** means an observer cannot determine whether an operation committed and must query authoritative state rather than replay blindly.

### Central model, mechanism, or theorem

Treat restart as a monotone state machine:

$$
S_0 \rightarrow S_{fenced} \rightarrow S_{validated} \rightarrow S_{replayed}
\rightarrow S_{resolved} \rightarrow S_{verified} \rightarrow S_{serving}.
$$

Each transition has evidence and a failure policy. Recovery may advance only when the current database incarnation, log history, checkpoint, record/page formats, and durable prefix validate; the chosen recovery algorithm then reconstructs history and resolves transaction state. Service opens only after its declared gate passes. A crash during any transition restarts from durable evidence without assuming volatile progress.

### Critical invariants

- Exactly one authorized writer epoch can mutate a database authority; stale processes and mounts are fenced before recovery writes.
- Bootstrap metadata, checkpoint, log, and pages must belong to compatible database and history incarnations.
- Recovery consumes only a complete validated durable log prefix and never invents a missing commit decision.
- Every recovery write follows the same log-before-data and integrity rules required by the recovery algorithm.
- Repeated recovery crashes preserve a restart path; progress markers are durable, monotone, and replayable.
- Corruption, missing history, format incompatibility, and resource exhaustion produce explicit repair, restore, or fail-closed outcomes.
- Service exposure is tied to named recovery postconditions, not elapsed time or process liveness.
- Client requests with unknown pre-crash outcomes use stable identity and authoritative lookup.

### Common failures

Failures include restarting before fencing an old primary; using the newest-looking checkpoint without validating it; treating a clean-shutdown flag as proof of all storage; skipping damaged WAL; guessing that missing commit records mean abort when the tail is incomplete; opening read-only service with inconsistent indexes or visibility metadata; repeatedly killing loser rollback; restoring an older binary that cannot parse new durable formats; letting recovery fill the disk; promoting a stale replica by bare LSN comparison; acknowledging health before application invariants are checked; and retrying unknown payments without idempotency or status lookup.

### Compact example

A node crashes with control generation 42, checkpoint pointer 500, durable WAL through 900, and pages at mixed LSNs. A previous process may still hold a lease. Recovery first acquires writer epoch 43 and proves epoch 42 cannot write. It validates database identity, control checksum, checkpoint completeness, WAL continuity 500–900, record formats, and page repair options. Analysis/redo/undo reconstruct the authorized state; a crash during undo is safe through CLRs. Structural and transaction oracles pass, the durable recovery-complete marker is recorded where the design requires it, and only then does the node advertise serving. Requests whose responses were lost query operation IDs against recovered state.

### Connections

Retrieve [Failure Models](071-failure-models.md), [Write-Ahead Logging](072-write-ahead-logging.md), [Undo and Redo Logging](074-undo-and-redo-logging.md), [Checkpoints](075-checkpoints.md), [ARIES Analysis, Redo, and Undo](076-aries-analysis-redo-and-undo.md), and [Group Commit](077-group-commit.md). Continue through [the program roadmap](../ROADMAP.md) to physical/logical backup and verified point-in-time restore.

## Governing Question

Database recovery is often described as an automatic scan performed when a server starts. That description hides the hardest decisions. Which process owns the files? Which log history is authoritative after failover or restore? Is the newest checkpoint complete? Does the durable prefix end at a record boundary? Can the current binary interpret every reachable format? Are pages old, torn, corrupt, or from a different incarnation? When is it safe to expose reads, writes, replication, and background maintenance?

A production recovery design answers these questions as a lifecycle with explicit evidence. Its inner algorithm may be ARIES, redo plus MVCC visibility, copy-on-write root selection, rollback-journal restoration, or another proven method. The lifecycle surrounds that algorithm with fencing, bootstrap validation, resource controls, health gates, client semantics, and escalation paths.

## Why This Matters

The recovery path runs when normal assumptions are least trustworthy. The preceding process may have died mid-write, the filesystem may have remounted, storage may have returned errors, the host clock may have jumped, an operator may have copied partial files, and another node may still believe it is primary. Recovery also runs with elevated access before ordinary monitoring and configuration services are available.

Fast recovery is valuable, but a fast incorrect restart can acknowledge divergent writes, expose aborted data, omit committed rows, or corrupt indexes further. Recovery-time objectives are therefore conditional distributions over failure type, data/log volume, hardware, cache warmth, loser debt, repair needs, and resource availability. They cannot be established by one clean restart benchmark.

Current PostgreSQL documentation describes WAL replay from the last checkpoint and distinguishes crash recovery, archive recovery, restartpoints, and recovery targets. MySQL 8.4 documents InnoDB redo application and rollback of incomplete transactions, including operational force-recovery modes that can sacrifice normal guarantees and are intended for emergency data extraction. SQLite's atomic-commit analysis makes filesystem and power-loss assumptions explicit. These product mechanisms differ, but all require honest boundaries between ordinary recovery, degraded extraction, media repair, and restore.

## Prerequisites and Retrieval

Retrieve these concepts:

- process crash, kernel panic, host loss, power loss, storage loss, corruption, and region loss affect different volatile/durable boundaries;
- WAL positions are comparable only within compatible database and history incarnations;
- a checkpoint is a validated recovery summary and can point to a redo horizon older than its own record;
- ARIES-style analysis/redo/undo uses DPT/TT state, pageLSN guards, and CLRs;
- a successful write call, cache submission, device completion, and durable ordered persistence are distinct;
- locks, leases, epochs, quorum terms, and storage reservations can fence old writers only under explicit failure assumptions;
- replicas, archives, backups, and decoders may own log-retention frontiers;
- transaction commit and client knowledge are separate; response loss creates an unknown outcome;
- restoration changes provenance and often creates a new database or log-history incarnation.

This module integrates recovery into an operational lifecycle. DBE-079 separates physical and logical backup, and DBE-080 develops point-in-time recovery and restore verification.

## Learning Objectives

After completing this module, you should be able to:

1. define crash recovery as a fenced, validated, restartable state machine;
2. classify failures and choose local recovery, replica failover, media repair, restore, or fail-closed handling;
3. validate bootstrap, checkpoint, log, page, and binary-format compatibility before replay;
4. derive service-exposure gates for read, write, replication, and maintenance roles;
5. handle repeated crashes, prepared transactions, unknown client outcomes, and degraded recovery safely;
6. budget log, scratch, page, memory, CPU, and time resources for recovery;
7. design recovery telemetry, RTO evidence, drills, canaries, and rollback constraints;
8. validate recovered logical and structural state with independent oracles.

## Core Exposition

**Classify the failure before selecting the path.** A process crash with intact storage may need ordinary log recovery. A host or power loss additionally tests device-cache and filesystem assumptions. Missing or corrupt media needs repair or restore, not ordinary redo over absent evidence. Loss of a failure domain may require fenced replica promotion. A human copying files from different times creates an inconsistent backup even if every file parses.

The classifier is evidence-based. Examine storage errors, checksums, control generations, log continuity, replication terms, and backup provenance. Do not decide “ordinary crash” merely because the daemon exited unexpectedly. Escalate when the required premises fail.

**Fence before recovery writes.** An old primary can resume after a network partition or delayed process pause. A lock file on shared storage is useful only if its atomicity and failure semantics cover the threat. Stronger designs use leases backed by a quorum clock assumption, monotonically increasing epochs embedded in writes, storage reservations, or consensus ownership. Recovery obtains a new writer epoch and proves older epochs cannot commit accepted mutations.

Fencing is not leader election alone. Election chooses an owner; fencing prevents the former owner from continuing. Every write path and durable record that depends on leadership must reject stale epochs, or the database can diverge while both processes appear healthy.

**Bootstrap from a minimal trusted surface.** Read redundant control records containing magic, database/system identifier, format versions, page size, checksum algorithm, encryption/key identifiers, log-history/timeline, checkpoint pointer, and clean/unclean state. Validate sizes before allocation, checksums before fields, generations before freshness, and compatibility before interpretation. Select the newest valid compatible generation, not the largest unvalidated number.

A clean-shutdown flag can permit a shorter path only if its publication protocol proves all required log/pages/metadata durable first and if storage has not changed unexpectedly. It is a hint backed by an ordering proof, not a universal bypass.

**Validate the recovery history.** Locate a complete checkpoint, derive the analysis and redo positions, and verify WAL continuity through the chosen target. Each record must pass bounds, version, identity, LSN ordering, checksum/authentication, and type-specific validation. The durable tail ends at a complete record boundary under the logger's torn-tail protocol. A checksum failure in the middle of required history cannot be reinterpreted as the end.

After restore or promotion, history can branch. Bind positions to system ID and timeline/term ancestry. A numerically larger LSN on an unrelated history does not make a replica safer. Recovery target selection must specify inclusive/exclusive endpoint semantics and transaction consistency.

**Validate pages before trusting recovery guards.** Page identity, relation/file incarnation, generation, format, checksum/authentication, and encryption context precede pageLSN comparison. A page with a large corrupt pageLSN cannot authorize skipping redo. Repair may use a logged full-page image, validated replica, checksum-aware backup, parity, or media recovery. If no sound source exists, ordinary recovery stops.

**Execute the engine's recovery algorithm.** In an ARIES-style engine, analysis reconstructs DPT/TT, redo repeats required history, and undo resolves losers using CLRs. In a redo-plus-MVCC engine, WAL replay reconstructs physical state while transaction status makes aborted versions invisible and later maintenance reclaims them. Copy-on-write selects a valid committed root and reclaims unreachable objects later. The outer lifecycle must not assume the wrong mechanism's postconditions.

Prepared transactions remain in doubt unless their distributed decision is recovered. External messages, payments, files, or devices are outside local WAL unless a durable integration protocol says otherwise. Reconciliation and idempotent workflow state follow database recovery.

**Make recovery itself restartable.** Crash after every recovery log append, log flush, page write, metadata change, file create/delete/rename, checkpoint/restartpoint, and service-state publication. Durable progress must be replayable or safely ignored. ARIES CLRs make undo progress restartable. A copy-on-write repair may publish a new root only after all referenced objects are durable. Temporary files use generation and atomic-publication rules.

Never depend on volatile “already repaired” sets for correctness. On restart, reconstruct progress from durable records. Bounded repeated work is a performance objective; a sound restart path is the correctness requirement.

**Control resources.** Recovery needs memory for tables/queues, I/O bandwidth, log space for CLRs, scratch space for repair, file descriptors, CPU, and sometimes network/archive capacity. Large losers can pin old WAL while generating new CLRs. A full disk can prevent the very recovery needed to release space. Reserve emergency capacity and reject unsafe admission during normal operation.

Spill large recovery structures using checksummed, generation-bound files. Bound record lengths and table entries to resist corruption and denial of service. Throttle parallel workers against storage queues; recovery that saturates the device can delay itself and damage other services.

**Choose service gates by invariant.** A conservative system remains offline until all required recovery and verification completes. Another may expose restricted reads after redo if transaction visibility, indexes, schemas, locks, and prepared state are safe while background loser cleanup continues. The gate is product-specific and must list exactly which operations are allowed.

Health endpoints should distinguish process alive, storage accessible, recovery validating, replaying, undoing, repairing, verifying, read-safe, and write-safe. Load balancers and orchestrators must not equate a listening socket with readiness. Replicas should not stream from a node before its history and role are authoritative.

**Handle unknown client outcomes.** A transaction can become durable before the crash while its success response never reaches the client. After recovery, the client uses a stable operation key and authoritative status endpoint. Retrying a non-idempotent operation without that identity can duplicate effects. Conversely, absence of an operation record is decisive only when the lookup covers the authoritative recovered database and retention policy.

**Separate ordinary, degraded, and forensic modes.** Emergency options that ignore corrupt pages, skip redo, disable consistency checks, or permit read-only extraction change guarantees. Name the mode prominently, prevent ordinary writes, copy evidence first, extract to a new clean authority, and require reconciliation. Do not call a server “recovered” after a force option merely made some rows readable.

**Decide local recovery versus failover.** Failover can reduce outage only if the candidate is fenced, has compatible history, covers the required durability policy, and can be promoted without losing acknowledged commits beyond contract. Local recovery may preserve more recent state but take longer. Evaluate recovery/failover time distributions, data-loss objective, network/quorum condition, cache state, replica lag, and repair risk.

Failing over does not remove recovery: the replica may need replay/restart recovery and the old primary later needs rejoin or rebuild. Avoid oscillation by recording decision epochs and requiring explicit evidence for re-promotion.

**Verify the recovered state.** Structural checks cover page identity, checksums, allocation ownership, free-space maps, index order/reachability, and catalog-to-file agreement. Transaction checks cover winners, losers, prepared work, visibility, constraints, and sequence promises. Application checks cover selected business invariants and reconciliation totals. Verification can be risk-based online work after a minimum safety gate, but claims must state what was checked.

**Measure recovery honestly.** Record failure classification, data/log versions, start checkpoint/horizon, target, bytes and records scanned/applied, pages read/written/repaired, transaction counts/states, CLR volume, worker concurrency, storage errors, phase timings, resource peaks, verification results, service gates, and exact environment. RTO distributions include detection, fencing, orchestration, recovery, verification, and traffic restoration—not replay alone.

The executable state machine below demonstrates legal lifecycle transitions and rejection of premature serving. It does not emulate a database, storage, fencing service, or recovery algorithm.

<!-- bijux-verify: {"id":"finite-crash-recovery-lifecycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial=stopped\nepoch=43\npath=fenced,validated,replayed,resolved,verified,serving\npremature_serving_rejected=true\nmissing_history_rejected=true\nfinal=serving\nall_required_gates=true\nevidence=finite_crash_recovery_lifecycle\n","stderr":""}} -->
```python
transitions = {
    "stopped": "fenced",
    "fenced": "validated",
    "validated": "replayed",
    "replayed": "resolved",
    "resolved": "verified",
    "verified": "serving",
}

def advance(state: str, evidence: dict[str, bool]) -> str:
    required = {
        "fenced": "old_writer_excluded",
        "validated": "history_complete",
        "replayed": "replay_complete",
        "resolved": "transactions_resolved",
        "verified": "oracles_passed",
        "serving": "readiness_authorized",
    }
    target = transitions[state]
    if not evidence.get(required[target], False):
        raise ValueError(f"missing evidence for {target}")
    return target

evidence = {
    "old_writer_excluded": True,
    "history_complete": True,
    "replay_complete": True,
    "transactions_resolved": True,
    "oracles_passed": True,
    "readiness_authorized": True,
}

state = "stopped"
path = []
while state != "serving":
    state = advance(state, evidence)
    path.append(state)

try:
    advance("validated", {"readiness_authorized": True})
    premature_rejected = False
except ValueError:
    premature_rejected = True

try:
    advance("fenced", {"history_complete": False})
    missing_history_rejected = False
except ValueError:
    missing_history_rejected = True

print("initial=stopped")
print("epoch=43")
print("path=" + ",".join(path))
print(f"premature_serving_rejected={str(premature_rejected).lower()}")
print(f"missing_history_rejected={str(missing_history_rejected).lower()}")
print(f"final={state}")
print(f"all_required_gates={str(all(evidence.values())).lower()}")
print("evidence=finite_crash_recovery_lifecycle")
```

## Definitions and Notation

- `E`: authorized writer/recovery epoch.
- `H`: database and log-history identity/ancestry.
- `C`: newest complete compatible checkpoint selected for bootstrap.
- `F_durable`: greatest complete validated durable log frontier.
- `T`: requested recovery target, if recovery is intentionally bounded.
- `S_x`: lifecycle state with named entry evidence and exit postconditions.
- **Ordinary recovery:** recovery under all normal correctness premises.
- **Media recovery:** reconstruction when durable database media is missing or damaged.
- **Degraded extraction:** explicitly weakened mode for salvaging data, not normal service.
- **Fencing token:** unforgeable or monotonically ordered authority checked by all relevant writers.
- **Readiness gate:** evidence predicate authorizing a particular service role.
- **Recovery drill:** controlled execution of the real recovery workflow with recorded evidence.
- **Recovery oracle:** independent expected-state or invariant mechanism used to evaluate the result.

## Mechanisms, Invariants, or Proof Structure

**Single-writer safety.** If every accepted mutation carries epoch E and storage/replication rejects epochs older than the greatest authorized epoch, acquiring E+1 and publishing it before recovery writes prevents an old writer at E from committing new accepted state. A lease without enforceable write rejection does not establish the premise.

**Bootstrap safety.** Redundant control metadata is useful only when selection validates checksum, bounds, database incarnation, log history, format support, and referenced checkpoint completeness before generation comparison. Under payload-before-pointer publication, falling back to an older valid checkpoint increases work without losing required history.

**Monotone lifecycle.** Every transition requires evidence whose durable prerequisites remain true across a crash or can be reconstructed. Volatile phase labels do not authorize skipping. If a repeated crash removes volatile progress, recovery re-enters from fenced/validated durable facts and safely repeats idempotent work.

**Service safety.** Define predicate G_role over page/log integrity, transaction resolution/visibility, structural state, schema/catalog state, ownership epoch, and operational limits. Advertising role is safe only after G_role passes. A process-health predicate is strictly weaker and cannot substitute.

**RTO scope.** Let total recovery time include detection, fencing, orchestration, bootstrap/validation, replay/resolution, verification, and traffic restoration. Measuring only replay supplies a lower component, not the end-to-end objective.

## Alternatives and Trade-Offs

| Choice | Advantage | Risk or cost | Required evidence |
| --- | --- | --- | --- |
| Local crash recovery | retains newest local history | damaged media or long replay | log/page validation and RTO drills |
| Replica failover | may reduce outage | stale/divergent candidate, split brain | fencing, history ancestry, durability coverage |
| Media repair | preserves local lineage | repair source may be stale/wrong | identity, checksum, page-level provenance |
| Full restore | clean known base | longer RTO and possible data loss to target | backup/WAL lineage and restore verification |
| Offline full gate | simplest exposure proof | longer unavailability | complete recovery/oracle results |
| Restricted early reads | earlier partial availability | subtle visibility/index/schema hazards | precise role predicate and tests |
| Parallel recovery | potential lower replay time | dependency and error complexity | serial equivalence and fault schedules |
| Degraded extraction | salvage from damaged state | weakened or unknown consistency | isolation, labels, reconciliation, rebuild |

## Failure Modes and Misconceptions

1. **“Restarting the daemon is recovery.”** Ownership, durable evidence, state reconstruction, and gates are required.
2. **“Election fences the old primary.”** Every relevant write target must enforce the new epoch.
3. **“Newest generation wins.”** Integrity, compatibility, identity, and referenced payload validate first.
4. **“Missing commit means abort.”** Only a complete trusted prefix supports that inference.
5. **“A large pageLSN proves freshness.”** Corrupt or wrong-generation pages invalidate comparison.
6. **“Skipping one bad WAL record is acceptable.”** Later history may depend on it; repair or fail closed.
7. **“Read-only is always safe during recovery.”** Visibility, indexes, catalogs, and prepared locks may be incomplete.
8. **“Fast replay meets RTO.”** Detection, fencing, verification, and traffic restoration also count.
9. **“Failover avoids recovery.”** A promoted replica still replays, fences, verifies, and establishes a new history.
10. **“Force-recovery mode restores correctness.”** It may only permit degraded extraction with lost guarantees.
11. **“Old binaries are a rollback plan.”** Durable format changes can make downgrade unsafe.
12. **“Killing slow rollback helps.”** It preserves or increases recovery debt.
13. **“Healthy storage yesterday proves flush today.”** Persistence claims are environment- and failure-specific.
14. **“Successful startup proves the data.”** Logical and structural oracles must agree.
15. **“Client retry resolves uncertainty.”** Stable identity and authoritative lookup are needed.
16. **“One recovery drill establishes the objective.”** Evidence is bounded by failure, workload, data, version, and environment.

## Worked Examples

### Example 1

**Situation.** A network partition ends, and both the former primary and a promoted replica can reach shared storage.

**Reasoning.** Promotion alone does not stop the former primary. The replica obtains epoch 43 from the authority and storage rejects writes bearing 42. Recovery and new commits carry 43. If storage does not check epochs, a quorum lease or reservation must enforce equivalent exclusion before either node writes.

**Conclusion.** Recovery starts only after stale-writer exclusion is enforceable at the mutation boundary.

### Example 2

**Situation.** Control slot A has generation 9 and valid checksum; slot B has generation 10 but a torn checksum.

**Reasoning.** Validate before comparing freshness. Slot B is unusable. Slot A's database ID, history, format, and checkpoint reference also validate, so recovery uses A and scans additional WAL. Choosing B because 10 is larger would trust corrupt metadata.

**Conclusion.** Older valid bootstrap state is safer than newer unvalidated state.

### Example 3

**Situation.** WAL has valid records through 800, corruption at 820, and another valid-looking record at 850.

**Reasoning.** A middle gap breaks the required history. Record 850 can depend on 820 and its apparent checksum does not reconstruct the missing semantics. Obtain the missing segment from archive/replica or restore from a verified base. Treating 820 as an end-of-log torn tail is valid only if the logger protocol and physical position prove it is the terminal boundary.

**Conclusion.** Required middle-history corruption blocks ordinary recovery; later parseability is not continuity.

### Example 4

**Situation.** A page has pageLSN 900 but a checksum failure and an object generation older than the catalog.

**Reasoning.** The pageLSN belongs to untrusted/wrong-incarnation bytes. Redo cannot safely skip records below 900 or apply current deltas to the stale page. Recover a compatible full-page image or validated page copy, verify identity and format, then resume record application.

**Conclusion.** Page integrity and identity are preconditions for recovery-position comparison.

### Example 5

**Situation.** Recovery crashes after undo writes CLR 950 durably but before the compensated page reaches disk.

**Reasoning.** On restart, redo sees CLR 950 and applies the compensation if the pageLSN guard requires it. Undo follows CLR `undoNextLSN` past the already completed original action. If the page had reached disk first, WAL ordering would have been violated.

**Conclusion.** Durable CLR-before-page ordering makes crash-during-undo restartable.

### Example 6

**Situation.** A server finishes redo but retains an in-doubt prepared payment transaction.

**Reasoning.** Absence of a commit record does not authorize abort after a durable prepare/vote. Reconstruct its prepared state and locks or equivalent exclusion, query the distributed decision, and gate conflicting service. A read-only mode is safe only if visibility and conflict policy explicitly cover prepared effects.

**Conclusion.** Redo completion does not resolve distributed transaction authority.

### Example 7

**Situation.** The disk has 30 GiB free, but loser undo may emit 80 GiB of CLRs before old WAL can be recycled.

**Reasoning.** Recovery risks capacity deadlock. Use pre-reserved emergency space, attach additional verified capacity, or choose a restore/failover path that preserves the durability contract. Deleting required WAL or suppressing CLRs would destroy restart safety.

**Conclusion.** Recovery-space sufficiency is a correctness precondition, not merely a performance preference.

### Example 8

**Situation.** A replica can be promoted in 40 seconds but lacks the last acknowledged local commit; local recovery is estimated at four minutes.

**Reasoning.** If the contract promises that acknowledged commit across this failure, promotion would violate durability despite the better outage time. Seek a candidate covering the required frontier or recover locally. If the contract explicitly allowed that loss window, promotion may be valid, but the loss and client reconciliation must be reported.

**Conclusion.** RTO cannot silently override the declared recovery-point/durability objective.

### Example 9

**Situation.** An emergency force mode starts the engine and returns rows from a table with a damaged secondary index.

**Reasoning.** Isolate the source, prevent normal writes, preserve forensic copies, extract base rows with provenance, rebuild into a new clean database, recreate constraints/indexes, and reconcile totals/business invariants. The original instance remains degraded and is not promoted to ordinary service.

**Conclusion.** Data extraction from damaged state is a salvage workflow, not proof of recovery.

### Example 10

**Situation.** A payment committed before crash, but its response was lost; the client retries after recovery.

**Reasoning.** The client submits the same operation ID. Recovered authoritative state contains that ID and result under a uniqueness constraint, so the service returns the existing result. A new ID would represent a new requested operation. If status lookup is unavailable while verification is incomplete, return unavailable/unknown rather than executing again.

**Conclusion.** Stable identity converts transport ambiguity into an authoritative lookup after recovery.

## Cross-Program Connections

- **Operating Systems:** process death, filesystem ordering, fsync, device caches, mount state, and storage errors define crash cuts.
- **Distributed Systems:** epochs, leases, consensus, promotion, prepared transactions, and history ancestry establish authority.
- **Platform Engineering:** orchestration, readiness, storage qualification, capacity reserves, drills, and incident controls operationalize recovery.
- **API and Service Engineering:** idempotency, unknown outcomes, health contracts, retries, and degraded-mode responses protect clients.
- **Security Engineering:** privileged parsing, encryption keys, integrity, salvage isolation, and denial-of-service bounds secure the path.
- **Data Architecture Engineering:** backup lineage, recovery objectives, retention, reconciliation, and evidence govern restore decisions.
- **Software Testing and Quality Engineering:** model-based histories, crash injection, corruption campaigns, and independent oracles establish evidence.
- **Concurrent and Parallel Programming:** recovery workers, phase publication, cancellation, and dependency ordering require happens-before proofs.

## References

1. C. Mohan, D. Haderle, B. Lindsay, H. Pirahesh, and P. Schwarz, “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM Transactions on Database Systems* 17(1), 1992. Primary restartable recovery paper; [IBM Research record](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging), reviewed 2026-09-05.
2. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Durable treatment of failure models, logging, recovery, media failure, and operational transaction processing.
3. PostgreSQL Global Development Group, [PostgreSQL 18: WAL Configuration](https://www.postgresql.org/docs/18/wal-configuration.html), reviewed 2026-09-05. Official checkpoint, crash/archive recovery, redo-point, and restartpoint behavior.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Continuous Archiving and Point-in-Time Recovery](https://www.postgresql.org/docs/18/continuous-archiving.html), reviewed 2026-09-05. Official recovery history, archive, target, and timeline behavior.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Recovery Target Settings](https://www.postgresql.org/docs/18/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY-TARGET), reviewed 2026-09-05. Official target types and inclusive/action semantics.
6. PostgreSQL Global Development Group, [PostgreSQL 18: Reliability and the Write-Ahead Log](https://www.postgresql.org/docs/18/wal-reliability.html), reviewed 2026-09-05. Official storage-persistence assumptions.
7. Oracle, [MySQL 8.4 Reference Manual: InnoDB Recovery](https://dev.mysql.com/doc/refman/8.4/en/innodb-recovery.html), reviewed 2026-09-05. Official redo and incomplete-transaction recovery behavior.
8. Oracle, [MySQL 8.4 Reference Manual: Forcing InnoDB Recovery](https://dev.mysql.com/doc/refman/8.4/en/forcing-innodb-recovery.html), reviewed 2026-09-05. Official warnings and limitations for emergency force-recovery levels.
9. SQLite Project, [Atomic Commit in SQLite](https://www.sqlite.org/atomiccommit.html), reviewed 2026-09-05. Official crash/power-loss and filesystem-assumption analysis.
10. SQLite Project, [How To Corrupt An SQLite Database File](https://www.sqlite.org/howtocorrupt.html), reviewed 2026-09-05. Official operational corruption modes and unsafe file-access patterns.

## Exercises

### Exercise 1

Define the crash-recovery lifecycle states and the evidence required to enter serving state. Explain why process liveness is insufficient.

### Exercise 2

A candidate has writer epoch 12, checkpoint 400, WAL through 900, page P with invalid checksum/pageLSN 850, and a prepared transaction at 700. Derive the safe decisions for fencing, replay, page handling, transaction handling, and service exposure.

### Exercise 3

Design a versioned bootstrap and WAL-validation implementation. Cover redundant controls, generations, checksums, history identity, record bounds, torn tail, middle corruption, encryption keys, and downgrade compatibility.

### Exercise 4

Compare local recovery, replica failover, page/media repair, and full restore for a system promising zero loss of acknowledged payments and a five-minute RTO. State required evidence and conflicts.

### Exercise 5

Design a full recovery drill and readiness review for an unfamiliar database. Include failure classes, repeated crashes, resource exhaustion, prepared/external work, oracles, observability, degraded modes, canarying, and rollback.

## Answers to the Exercises

### Answer 1

A sound sequence is stopped, fenced, validated, replayed, transaction-resolved, verified, then role-specific serving. Fenced requires enforceable exclusion of stale writers and a new authority epoch. Validated requires compatible database/history identity, formats, checkpoint, complete WAL prefix, pages/repair sources, keys, and resources. Replayed/resolved require the engine algorithm and prepared-state policy to reach their postconditions. Verified requires logical, transaction, structural, integrity, and selected application oracles. Serving requires an explicit readiness authorization for reads/writes/replication. A live process proves only execution; it does not prove authority, recovered state, or safe visibility.

### Answer 2

Acquire epoch 13 and prove every write target rejects epoch 12 before recovery writes. Validate checkpoint 400 and WAL continuity/format through 900. P's checksum failure invalidates pageLSN 850; do not skip redo or apply deltas until a compatible full-page image, replica/backup page, or other validated repair re-establishes identity and integrity. Preserve the prepared transaction and recover its distributed decision; do not ordinary-loser undo it. Service remains offline or explicitly restricted until P is repaired, replay completes, prepared conflicts are safely represented, and role-specific oracles pass. Bare LSNs and elapsed time cannot weaken these decisions.

### Answer 3

Use two or more fixed control slots with magic, length, supported version, database/system ID, page parameters, encryption/key ID, log history/timeline, checkpoint pointer, clean-state protocol, generation, and checksum/authentication. Validate bounds/integrity/identity/format before selecting the highest compatible generation. Validate the referenced checkpoint and scan WAL records with overflow-safe lengths, history/LSN ordering, checksums, exhaustive types, and key availability. The terminal torn-tail rule applies only at the physical end under the logger protocol; corruption inside required history is repair/restore, not truncation. Retain older readers/writers or explicit migration metadata for reachable formats; refuse downgrade when an older binary cannot interpret durable state.

### Answer 4

Local recovery is valid if local durable history covers every acknowledged payment and can be verified within five minutes; measure the full distribution. Replica failover is valid only when the candidate's fenced compatible history covers the promised acknowledgement frontier. Page repair is valid when damage is localized and each replacement has matching identity/generation/history provenance. Full restore requires a verified base plus complete WAL through the promised frontier. If no path both preserves zero acknowledged loss and meets five minutes, the requirements conflict under the observed failure; do not silently choose RTO. Improve replica durability, recovery parallelism, repair sources, capacity, or the stated contract before claiming both.

### Answer 5

Exercise process, kernel, power, storage, corruption, host, network, region, operator-copy, and upgrade/downgrade failures against production-like data. Crash at every bootstrap, log/page, recovery-progress, verification, and readiness transition, including repeated crashes during redo/undo. Inject missing/corrupt history, torn controls/pages, stale epochs, missing keys, full disk, huge losers/tables, worker death, prepared transactions, response loss, and external-workflow backlog. Verify rows, winners/losers/prepared visibility, indexes, allocations, catalogs, constraints, checksums, history, acknowledged operations, and selected business totals with independent oracles. Record full RTO/RPO components and resources. Clearly isolate salvage modes. Canary compatible binaries/policies on rehearsed copies or safe replicas; retain validated restore/rebuild paths, and roll back only when old software can read all durable formats and authority epochs safely.
