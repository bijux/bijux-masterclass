---
module_id: DBE-080
program: Database Engineering
level: 2
module_number: 80
title: Point-in-Time Recovery and Restore Verification
status: complete
last_verified: 2026-09-05
---

# Point-in-Time Recovery and Restore Verification

## One-Page Review

### Governing question

How can engineers select an exact authorized recovery target, reconstruct it from a compatible backup and log history, prove the restored database is usable, and promote it without overwriting evidence or confusing a successful replay with business correctness?

### Essential definitions

**Point-in-time recovery** (PITR) restores a base and replays logged history to a declared target rather than necessarily to the latest available record. A **recovery target** can be a log position, named restore point, transaction boundary, timestamp interpreted under engine rules, or end of available history. **Inclusive** targeting may apply the named transaction/event; **exclusive** targeting stops before it. A **timeline** or **history branch** identifies one continuation after restore or promotion. **Restore verification** validates artifact integrity and lineage, engine recovery, structural state, transaction semantics, application invariants, security/configuration, and operational readiness. A **recovery point objective** (RPO) bounds tolerated loss under a named incident; a **recovery time objective** (RTO) bounds time to usable service. A **restore drill** executes the real acquisition, recovery, verification, and handoff path in an isolated environment.

### Central model, mechanism, or theorem

For target T, a valid restore needs a compatible base B whose consistent position is no later than T and a complete ordered log path on one valid history from B through T:

$$
Restore(T)=Recover(B,LogPath(H,L_B,T),Policy_T).
$$

Selection is safe only when database identity, history ancestry, format/tool compatibility, target semantics, log continuity, manifests, digests, keys, and recovery policy validate. Acceptance then requires a vector of postconditions—not one checksum or startup event—covering physical integrity, logical/transaction state, structural invariants, application reconciliation, security, and role-specific readiness.

### Critical invariants

- Translate human incident intent into an immutable engine-native target with explicit history and inclusive/exclusive semantics before replay.
- Never select a wall-clock target without documenting timestamp precision, time zone, ordering ambiguity, and the engine's transaction-boundary behavior.
- Restore into a new isolated authority; do not overwrite the only source backup, damaged primary, or forensic evidence.
- Verify every base, incremental, log segment, manifest, key, and tool-format dependency before or while consuming it.
- A missing or corrupt required middle log range blocks that target; later valid records cannot bridge the gap.
- Recovery stops at a transaction-consistent boundary defined by the engine, not an arbitrary byte in a record.
- Promotion creates a new fenced history/epoch and prevents the old authority from accepting conflicting writes.
- Declare success only after named integrity, structural, transaction, application, security, and operational gates pass.

### Common failures

Failures include restoring by a vague local timestamp; applying the destructive transaction because target inclusivity was misunderstood; choosing a backup from another system incarnation; following the wrong timeline after failover; ignoring a WAL/log gap; overwriting the primary during a trial; restoring data without roles, keys, extensions, configuration, or external objects; declaring success because the server started; trusting row counts without constraints/indexes/business reconciliation; measuring replay instead of full RTO; exposing a restore with production credentials/network access; and promoting without fencing the old writer or recording a new history.

### Compact example

An accidental deletion commits at LSN 760 with operation ID `delete-42`. The last verified base is consistent at 500, and archive history H contains complete log through 900. The requested state is immediately before the deletion, so engineers choose the engine-native exclusive transaction/restore-point boundary before 760—not the operator's imprecise 14:03 wall clock. They restore B500 into an isolated environment, verify manifests and WAL 500–760, replay to the declared boundary, confirm `delete-42` is absent while all earlier acknowledged operations exist, validate indexes/constraints and application totals, scan for unintended external connectivity, then fence the old authority and promote the restore as a new history branch.

### Connections

Retrieve [Failure Models](071-failure-models.md), [Log Sequence Numbers](073-log-sequence-numbers.md), [Crash Recovery](078-crash-recovery.md), and [Physical and Logical Backup](079-physical-and-logical-backup.md). Continue through [the program roadmap](../ROADMAP.md) to physical/logical replication, failover, sharding, distributed transactions, and consensus-backed databases.

## Governing Question

“Restore the database to just before the incident” sounds precise only to a human. The database needs an ordered history, a transaction boundary, and a target rule. An incident timestamp may reflect a log message written after commit, a client clock in another zone, or several commits sharing one clock tick. A named restore point may be logged inside or outside a transaction depending on the engine. An LSN identifies a history position only when system ID, timeline, and endpoint convention accompany it.

After target selection, replay success still does not prove usability. The restored instance may lack roles, encryption keys, extensions, configuration, external objects, or compatible application schema. An index can be damaged while row counts look right. A payment can exist in the database while an external processor has a different outcome. Restore verification therefore combines database mechanisms with incident intent and independent semantic evidence.

## Why This Matters

PITR is the primary defense against events that healthy replication faithfully propagates: accidental deletion, destructive deployment, ransomware encryption, or latent application corruption. It can also recover from media loss when a base plus archived history survives. Its granularity and retention depend on what the log records and archives, not merely backup frequency.

PITR also creates irreversible choices. Promoting a restored copy forks history; writes accepted on both old and new authorities need reconciliation and may violate uniqueness or external invariants. Restoring too far loses valid work; restoring too late includes the damaging transaction. An isolated rehearsal lets operators inspect several candidate targets before promotion.

Current PostgreSQL documentation supports targets by time, transaction ID, named restore point, LSN, or immediate consistency, with inclusive and post-recovery action settings and timeline selection. MySQL 8.4 documents binary-log position/time replay and cautions around event selection. Product semantics differ, so automation must preserve the exact tool/version target contract rather than invent a universal timestamp rule.

## Prerequisites and Retrieval

Retrieve these concepts:

- a base backup, incremental chain, required WAL/log range, manifest, key set, and compatible tools form a recovery chain;
- an LSN or position belongs to a database/system identity and timeline/history;
- commit record order is authoritative within its log, while wall clocks can be coarse, skewed, adjusted, or observed after commit;
- physical recovery reconstructs engine state; logical/application recovery may require selective replay or reconciliation;
- transaction atomicity means a target normally cannot expose half a transaction;
- checkpoints bound recovery work but do not replace the log needed to reach a later target;
- failover/promotion requires fencing and creates a new epoch/history branch;
- checksums support byte integrity but not completeness, provenance, semantic correctness, or readiness;
- external systems and secrets/configuration can be necessary to validate or serve the restored application.

DBE-079 established valid backup inputs. This module closes the recovery block by proving target selection, restoration, validation, and safe handoff.

## Learning Objectives

After completing this module, you should be able to:

1. translate an incident into an exact engine-native recovery target and stop rule;
2. validate base, incremental, log, history, format, manifest, and key compatibility;
3. reason about time, LSN, transaction, named-point, inclusive/exclusive, and latest-consistent targets;
4. execute restores in isolated immutable workspaces and preserve forensic evidence;
5. define layered physical, structural, transactional, application, security, and operational oracles;
6. measure actual RPO and end-to-end RTO from verified evidence;
7. promote/fence a restored authority and reconcile post-fork events safely;
8. design automated drills, target sampling, failure injection, canarying, and restoration rollback.

## Core Exposition

**Start with an incident predicate.** Define the desired state in domain terms: every acknowledged order before operation X, no effects of destructive deployment Y, or the latest consistent state before corruption first became durable. Record known-good and known-bad transaction IDs, operation IDs, audit events, commit positions, and evidence sources. The target is a hypothesis until these are mapped to database history.

Preserve the original primary, logs, backup catalog, application/audit logs, and control-plane evidence. Investigation may refine the target. Reusing or truncating them during a hurried restore destroys both recovery options and causality evidence.

**Prefer ordered engine-native markers.** A named restore point or exact LSN/transaction boundary in the correct history is normally more precise than time. A stable application operation ID stored transactionally can be mapped to its commit position or used as the restored-state predicate. Record whether the harmful transaction itself must be excluded or included.

Time targets require care. Convert to an absolute instant with recorded zone and precision, then inspect nearby transaction order. Client timestamps and log-line timestamps may not equal commit order. If two transactions share a timestamp, engine-specific inclusive behavior may not isolate them. Restore multiple candidates or use exact log inspection rather than guessing.

**Model target semantics.** Let the ordered committed events on history H be `e_1,...,e_n`. An exclusive target at event k yields the prefix through `e_{k-1}`; inclusive yields through `e_k`, subject to the engine's exact definition. Targeting an internal LSN may cause recovery to stop at a consistent transaction boundary rather than exposing a partial record. Document whether the target position names record start, record end, or a commit decision.

**Select a compatible base.** Choose a complete verified base with position no later than T and the same database incarnation or a documented ancestor. Newer is not always better: a newer base may already contain the damaging transaction and cannot be undone by forward replay. An older base requires more log and time but may be the only valid choice.

For an incremental chain, validate every parent ID, changed-page map/range, digest, history, and format. Ensure the restore tool understands all page/log versions and extensions. Recover encryption keys and credentials from an independent path before declaring the chain usable.

**Construct one complete log path.** Verify continuous segments/records from the base's required start through the target on a valid timeline ancestry. A promotion can fork histories sharing a prefix. Select the branch containing the authoritative desired event sequence, not simply the highest numeric LSN or newest file timestamp.

Required middle corruption or absence blocks the target. Later segments cannot infer lost operations. Seek another archive/replica, another base after the gap but before the incident if logically possible, or a different recovery method. Any data-loss choice is explicit and reconciled.

**Restore into isolation.** Create a new destination with validated capacity, supported ownership/permissions, no accidental production endpoints, and separate credentials. Fetch immutable artifacts read-only. Verify manifests, sizes, digests, signatures/authentication, key IDs, and decompression before consumption or incrementally with fail-closed behavior. Record exact commands, versions, environment, and inputs.

Block outbound jobs, email, payments, CDC, scheduled tasks, and replica registration. A restored database can replay old outbox rows or credentials and cause real external effects. Use network isolation and inert substitutes until promotion authorization.

**Replay with explicit configuration.** Write recovery configuration from the immutable target specification. Log the selected base, history/timeline, start, target, inclusive rule, and action on target—pause, shutdown, or promote. Prefer pause/shutdown for inspection. Protect recovery against missing-log polling loops and accidental fallback to an unintended history.

Monitor segments requested/fetched, replay LSN, target distance, errors, restartpoints, I/O, and resource use. Do not change target interactively without creating a new recorded attempt; otherwise evidence no longer matches configuration.

**Verify physical and structural integrity.** Check backup manifest again after materialization, database control identity, page checksums, catalog-to-file/tablespace mapping, relation sizes, allocation/free-space ownership, index order and reachability, and extension/object compatibility. Run engine-native consistency tools where supported, recording scope and limitations.

A full scan may be expensive; define mandatory gates plus risk-based expansion. A single corruption suggests a broader class and expands sampling or blocks promotion. Rebuilding an index is acceptable only after proving base rows and semantics, and the rebuild becomes part of the restoration evidence.

**Verify transactions and target semantics.** Prove known-good transactions/operations before T exist, known-bad transaction at/after T is absent as intended, no partial transaction is visible, prepared/in-doubt state has a policy, and constraints/visibility match. Inspect a window around the target, not only the destructive row. The target may exclude legitimate commits that occurred concurrently before human detection.

Use invariant queries with stable expected results: counts by partition, uniqueness, referential integrity, ledger balance, inventory conservation, sequence lower bounds, and audit-chain continuity. Row counts alone can agree while values, ownership, or indexes are wrong.

**Reconcile application and external state.** Database PITR does not rewind messages already delivered, payments executed, files written, caches, search indexes, object stores, or downstream warehouses. Classify events after T: replay idempotently, compensate, discard derived state and rebuild, or investigate. Stable operation IDs and outbox/inbox histories help map database and external outcomes.

Do not connect the isolated restore to external services merely to “see what happens.” Export a reconciliation plan, obtain authorization, and execute through controlled workflows after authority is established.

**Verify security and operability.** Restore roles, ownership, grants, row-level policies, audit settings, encryption keys, certificates, extensions, locale/collation, configuration, and secrets through approved paths. Rotate credentials copied from a compromised environment. Check application migration compatibility, connection behavior, query plans for critical operations, monitoring, backup jobs, log archiving, and capacity.

Readiness is role-specific. A database can be structurally valid yet not production-safe because audit export, keys, fencing, or backups are absent. Record each gate and responsible reviewer without claiming external review that did not occur.

**Measure RPO and RTO from the result.** Actual RPO is the distance between the last desired/acknowledged state and the verified restored target under the incident, expressed in transactions/business effects as well as time where possible. Actual RTO includes detection, decision, credential/key recovery, artifact transfer, reconstruction, replay, verification, reconciliation, fencing, promotion, application validation, and traffic restoration.

One drill gives one observation. Maintain distributions by data size, archive distance, region, cache state, and failure class. Track the latest target that has actually restored and passed gates, not only the newest backup timestamp.

**Promote as a new history.** Before accepting writes, fence the old primary and competing restore attempts, assign a new writer epoch/timeline, record parent history and fork point, enable log archival/backups, and validate replica seeding. Preserve the pre-promotion snapshot so rollback means a governed switch/reconciliation, not pretending new writes never happened.

After promotion, events accepted on any divergent authority need explicit reconciliation. Never merge physical WAL from sibling histories by numeric order. Logical conflict resolution uses domain policy and audit evidence.

**Automate drills, not just commands.** Schedule isolated restores selecting recent and older generations, different incremental lengths, target types, regions, keys, versions, and data classes. Inject missing segments, corruption, expired credentials, wrong timeline, low disk, slow network, tool incompatibility, and verification failures. The automation should refuse promotion by default and retain reproducible reports under governed storage.

The executable model below selects exact committed prefixes for inclusive and exclusive targets and rejects a gap. It models a finite ordered event list only; it does not implement a database restore, timestamps, WAL parsing, or transaction recovery.

<!-- bijux-verify: {"id":"finite-pitr-target-selector","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"history=H7\nbase_lsn=500\ntarget_lsn=760\nexclusive_events=create-40,update-41\ninclusive_events=create-40,update-41,delete-42\nexclusive_excludes_delete=true\ninclusive_includes_delete=true\ncontinuous_path=true\ngapped_path_rejected=true\nlatest_verified_target=760\nevidence=finite_pitr_target_selector\n","stderr":""}} -->
```python
events = [
    (620, "create-40"),
    (700, "update-41"),
    (760, "delete-42"),
    (820, "update-43"),
]
base_lsn = 500
target_lsn = 760

def select(target: int, inclusive: bool) -> list[str]:
    return [name for lsn, name in events if lsn < target or (inclusive and lsn == target)]

def continuous(segments: list[tuple[int, int]], start: int, end: int) -> bool:
    cursor = start
    for lower, upper in sorted(segments):
        if lower > cursor:
            return False
        cursor = max(cursor, upper)
        if cursor >= end:
            return True
    return cursor >= end

exclusive = select(target_lsn, False)
inclusive = select(target_lsn, True)
complete_segments = [(500, 650), (650, 760)]
gapped_segments = [(500, 650), (700, 760)]

print("history=H7")
print(f"base_lsn={base_lsn}")
print(f"target_lsn={target_lsn}")
print("exclusive_events=" + ",".join(exclusive))
print("inclusive_events=" + ",".join(inclusive))
print(f"exclusive_excludes_delete={str('delete-42' not in exclusive).lower()}")
print(f"inclusive_includes_delete={str('delete-42' in inclusive).lower()}")
print(f"continuous_path={str(continuous(complete_segments, base_lsn, target_lsn)).lower()}")
print(f"gapped_path_rejected={str(not continuous(gapped_segments, base_lsn, target_lsn)).lower()}")
print(f"latest_verified_target={target_lsn}")
print("evidence=finite_pitr_target_selector")
```

## Definitions and Notation

- `B`: selected base or completed incremental chain.
- `L_B`: base's engine-defined consistent/recovery start position.
- `T`: immutable recovery target with history and stop semantics.
- `H`: selected log timeline/history and ancestry path.
- `LogPath(H,L_B,T)`: complete ordered compatible log needed from base through target.
- `Policy_T`: inclusive/exclusive, transaction-boundary, timeline, and target-action rules.
- **Known-good marker:** transaction/operation that must exist in the accepted restore.
- **Known-bad marker:** transaction/operation that must be absent under the chosen target.
- **Candidate restore:** isolated reconstruction not yet authorized for service.
- **Promotion:** fenced transition that makes a candidate an authoritative writable history.
- **Verification vector:** collection of physical, structural, transactional, semantic, security, and operational results.
- **Observed recoverable point:** newest target actually restored and accepted under defined gates.

## Mechanisms, Invariants, or Proof Structure

**Target-prefix argument.** Given a totally ordered commit history H and exact event boundary k, exclusive recovery returns the authorized prefix before k and inclusive recovery returns the prefix through k, under the engine's transaction stop rule. A timestamp maps safely only if it identifies the intended boundary without unresolved ordering ambiguity.

**Chain sufficiency.** If B is valid at/before T, every incremental dependency validates, and `LogPath(H,L_B,T)` is complete and compatible, the engine has the declared evidence needed to reconstruct T. This is a necessary recovery-input claim; post-recovery correctness still depends on algorithms, storage, and verification.

**Gap impossibility.** If a required interval contains an unknown record range, later log does not in general determine the missing transaction and page effects. Continuing ordinary physical replay cannot preserve its correctness proof. Repair, a different base that bypasses the gap legitimately, logical recovery, or explicit loss/reconciliation is required.

**Acceptance predicate.** Let verification vector V include integrity, structure, transactions, application, security, and operations. Promotion is authorized only if every mandatory component passes and every exception has explicit authority. Process startup or one component cannot imply the conjunction.

**History-fork invariant.** Promotion records a new epoch/history with parent and fork point, and fencing prevents writes on the old authority. Positions on sibling histories are not ordered by bare LSN; reconciliation is logical and policy-driven.

## Alternatives and Trade-Offs

| Choice | Strength | Risk or limitation | Evidence |
| --- | --- | --- | --- |
| Exact LSN/transaction target | precise log order | requires trustworthy mapping from incident | nearby record inspection |
| Named restore point | human/domain-readable marker | placement and engine semantics matter | durable marker and history identity |
| Time target | easy incident correlation | precision, zone, skew, ordering ambiguity | transaction window comparison |
| Latest consistent end | maximizes recovered history | includes propagated logical damage | known-bad predicate |
| Physical PITR | efficient whole-database history | not selective; version dependent | chain and engine verification |
| Logical selective recovery | excludes chosen damage/tenant scope | slow and dependency complex | reconciliation and import proof |
| Offline full verification | stronger gate | longer RTO | complete reports |
| Staged/risk-based verification | faster partial readiness | residual undetected defects | explicit mandatory gates and expansion rules |

## Failure Modes and Misconceptions

1. **“Point in time means wall-clock timestamp.”** Native positions, transactions, or restore points may be more precise.
2. **“14:03 identifies one commit.”** precision, skew, zones, and concurrent commits make this uncertain.
3. **“Inclusive is obvious.”** Engine target semantics must be recorded and tested.
4. **“Newest base is best.”** It may already contain the incident.
5. **“Any log with a larger LSN continues the base.”** System ID and timeline ancestry must match.
6. **“Later WAL repairs a middle gap.”** Missing required effects are not derivable in general.
7. **“Restore in place saves time.”** It destroys rollback, evidence, and alternative-target options.
8. **“Server startup proves restore success.”** Integrity, structure, semantics, security, and operations remain.
9. **“Row counts prove correctness.”** values, ownership, indexes, constraints, and business totals can disagree.
10. **“PITR rewinds external services.”** messages, payments, objects, and downstream data need reconciliation.
11. **“Read-only inspection is harmless.”** restored credentials/jobs can contact production unless isolated.
12. **“Replay time is RTO.”** acquisition, decisions, keys, verification, fencing, and traffic count too.
13. **“Promotion resumes the old history.”** It creates a new authority branch/epoch.
14. **“Rollback means re-enable the old primary.”** divergent writes and fencing require governed reconciliation.
15. **“One drill proves the retention window.”** sample generation, target, failure, version, and region vary.
16. **“A checksum proves semantic correctness.”** it establishes only defined-byte integrity under its assumptions.

## Worked Examples

### Example 1

**Situation.** Destructive transaction D commits at LSN 760; desired state is immediately before D.

**Reasoning.** Map D's stable operation/transaction ID to the authoritative history and commit boundary. Configure an exclusive target before D under the engine's semantics. Verify the last known-good transaction before 760 exists and D is absent. A time from an alert after D is less precise.

**Conclusion.** Use an exact exclusive transaction boundary, not an approximate detection timestamp.

### Example 2

**Situation.** Two commits share timestamp 14:03:00.000; one is valid and the next is destructive.

**Reasoning.** A time target at that precision cannot distinguish their order and inclusive behavior may include both. Inspect WAL/binlog/audit mappings to find transaction IDs, LSNs, or insert a prior named marker. If exact separation is unavailable, restore candidate variants and reconcile logically.

**Conclusion.** Equal/coarse timestamps make time-only targeting underdetermined.

### Example 3

**Situation.** Base B is on timeline 4 at 500; histories 5 and 6 fork at 650, and the desired operation exists only on 6.

**Reasoning.** Validate that B is an ancestor of 6, acquire timeline-history metadata, and replay the path from 4 through the fork onto 6. A segment on 5 with the same numeric positions is a sibling, not a substitute. Bind every archive object to timeline and system ID.

**Conclusion.** PITR follows an ancestry path, not the numerically greatest LSN files.

### Example 4

**Situation.** The archive contains 500–650 and 700–900; target is 760.

**Reasoning.** The required interval 650–700 is absent. Records after 700 can depend on missing page/transaction state. Retrieve the exact gap, choose a compatible base after 700 that predates the incident if one exists, or use another recovery/reconciliation method. Do not declare physical PITR continuous.

**Conclusion.** A required middle gap blocks the target even when later log exists.

### Example 5

**Situation.** A candidate starts and row counts match, but index validation finds missing entries.

**Reasoning.** Startup and counts prove neither structural reachability nor query correctness. Preserve evidence, validate base rows/checksums, determine whether the index can be safely rebuilt, rebuild in isolation, and re-run referential, uniqueness, query, and application checks. Expand sampling for related indexes/pages.

**Conclusion.** One structural failure blocks promotion and broadens verification.

### Example 6

**Situation.** The restored outbox contains messages committed before T that production already delivered.

**Reasoning.** Starting workers in isolation could resend them. Keep outbound networking disabled, compare stable message IDs with inbox/provider evidence, mark already delivered effects or rely on receiver idempotency, and plan reconciliation for messages after T whose database records were removed.

**Conclusion.** Database time travel requires external-effect reconciliation before workers resume.

### Example 7

**Situation.** A drill restores data but cannot decrypt one tablespace because the old key version expired.

**Reasoning.** The recovery chain is unusable for its declared scope despite valid ciphertext digests. Restore key escrow/version material through the independent disaster path and repeat. Update latest verified recoverable point and alert; a green backup job did not establish key recoverability.

**Conclusion.** Key-version availability is a mandatory restore dependency and RPO/RTO component.

### Example 8

**Situation.** Replay takes 35 minutes against a one-hour RTO, but total service restoration takes 95 minutes.

**Reasoning.** Detection used 10 minutes, approval/key retrieval 15, transfer 20, replay 35, verification 10, and fencing/traffic 5, totaling 95. The objective is missed even though replay alone fits. Optimize the actual critical path and rehearse dependencies.

**Conclusion.** End-to-end RTO is 95 minutes for this observation, not 35.

### Example 9

**Situation.** After candidate promotion, the old primary accepted three isolated writes before fencing completed.

**Reasoning.** Physical histories are siblings after the fork and cannot be concatenated. Freeze both, identify operations by stable IDs, apply business conflict policy, compensate or migrate authorized effects logically, and audit decisions. Repair fencing before returning to normal automation.

**Conclusion.** Split-history reconciliation is a domain operation, not WAL-file sorting.

### Example 10

**Situation.** Monthly drills always restore yesterday's full backup to the same region and latest end.

**Reasoning.** The sample omits older retention, incrementals, time/LSN/named targets, alternate regions, cold caches, key versions, network loss, missing segments, corruption, and version upgrades. Rotate a risk-based matrix and record exact targets/gates; expand when any defect suggests a class.

**Conclusion.** Repeatedly testing one easy path supplies narrow evidence, not corpus-wide recoverability.

## Cross-Program Connections

- **Data Architecture Engineering:** lineage, RPO/RTO, retention, sovereignty, reconciliation, and recovery authorities govern targets.
- **Distributed Systems:** timeline ancestry, fencing, promotion, quorum durability, and split-history reconciliation establish authority.
- **Platform Engineering:** isolated environments, artifact transfer, keys, automation, readiness, drills, and traffic restoration determine RTO.
- **Security Engineering:** ransomware response, credentials, key escrow, network isolation, integrity, and forensic preservation constrain restoration.
- **API and Service Engineering:** operation IDs, unknown outcomes, outbox/inbox state, and idempotent reconciliation connect clients/external effects.
- **Data Engineering:** CDC offsets, downstream rebuilds, schema compatibility, and replay of derived systems follow the selected database target.
- **Software Testing and Quality Engineering:** target matrices, mutation/fault injection, invariant oracles, and evidence scope make restore claims testable.
- **Operating Systems:** storage snapshots, sparse files, page caches, I/O errors, and filesystem/device semantics affect reconstruction.

## References

1. PostgreSQL Global Development Group, [PostgreSQL 18: Continuous Archiving and Point-in-Time Recovery](https://www.postgresql.org/docs/18/continuous-archiving.html), reviewed 2026-09-05. Official base/WAL recovery, archive, timeline, and history behavior.
2. PostgreSQL Global Development Group, [PostgreSQL 18: Recovery Target Settings](https://www.postgresql.org/docs/18/runtime-config-wal.html#RUNTIME-CONFIG-WAL-RECOVERY-TARGET), reviewed 2026-09-05. Official time, transaction, restore-point, LSN, immediate, inclusive, timeline, and target-action semantics.
3. PostgreSQL Global Development Group, [PostgreSQL 18: Backup Manifest WAL Ranges](https://www.postgresql.org/docs/18/backup-manifest-wal-ranges.html), reviewed 2026-09-05. Official timeline-bound start/end range semantics.
4. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_verifybackup`](https://www.postgresql.org/docs/18/app-pgverifybackup.html), reviewed 2026-09-05. Official manifest and required-WAL verification scope and limitations.
5. Oracle, [MySQL 8.4 Reference Manual: Point-in-Time Recovery Using Binary Log](https://dev.mysql.com/doc/refman/8.4/en/point-in-time-recovery.html), reviewed 2026-09-05. Official binary-log position/time recovery workflow.
6. Oracle, [MySQL 8.4 Reference Manual: `mysqlbinlog` Backup](https://dev.mysql.com/doc/refman/8.4/en/mysqlbinlog-backup.html), reviewed 2026-09-05. Official continuous binary-log backup considerations.
7. NIST, [SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems](https://csrc.nist.gov/pubs/sp/800/34/r1/final), 2010, reviewed 2026-09-05. Authoritative contingency recovery, testing, and maintenance guidance.
8. Google, [Site Reliability Engineering: Data Integrity—What You Read Is What You Wrote](https://sre.google/sre-book/data-integrity/), reviewed 2026-09-05. Operational recovery, human error, corruption, and validation guidance.
9. C. Mohan et al., “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM TODS* 17(1), 1992. Primary recovery correctness foundation; [IBM Research record](https://research.ibm.com/publications/aries-a-transaction-recovery-method-supporting-fine-granularity-locking-and-partial-rollbacks-using-write-ahead-logging), reviewed 2026-09-05.
10. Jim Gray and Andreas Reuter, *Transaction Processing: Concepts and Techniques*, Morgan Kaufmann, 1993. Durable transaction, logging, media-recovery, and operational verification foundations.

## Exercises

### Exercise 1

Define recovery target, inclusive/exclusive stop, history/timeline, recovery chain, candidate restore, verification vector, promotion, RPO, and RTO. Explain which are evidence versus objectives.

### Exercise 2

A harmful transaction H commits at LSN 900 on timeline 7 at a timestamp shared with valid transaction G at 880. Base B is at 500; WAL 500–760 and 800–1,000 exists. Derive valid and invalid target strategies and the smallest missing evidence.

### Exercise 3

Design an immutable PITR executor that validates base/incremental/log/key/tool inputs, target semantics, isolation, replay, repeated failures, and evidence recording.

### Exercise 4

Compare physical PITR, logical selective recovery, latest replica failover, and application compensation after an accidental tenant deletion that has propagated everywhere online.

### Exercise 5

Design a milestone restore drill and promotion review for a regulated payment database. Include target mapping, external effects, security, structural/business oracles, RPO/RTO, failure injection, canarying, and rollback/reconciliation.

## Answers to the Exercises

### Answer 1

A recovery target is the exact engine-native boundary/condition desired. Inclusive/exclusive controls whether the named transaction/event is applied. History/timeline identifies the ordered branch. A recovery chain is the compatible base, increments, log path, manifests, keys, and tools required. A candidate is an isolated reconstruction without authority. A verification vector records physical, structural, transaction, application, security, and operational outcomes. Promotion fences competitors and creates an authoritative new branch. RPO and RTO are objectives; observed loss/time and the verified chain/vector are evidence. Target and policy are specifications; manifests, logs, reports, and oracle results support them.

### Answer 2

The shared timestamp cannot distinguish G and H, so time-only targeting is invalid without finer engine evidence. Exact exclusive targeting at H's transaction/commit boundary would retain G and exclude H if the engine maps both identities on timeline 7. However the log path has a required gap 760–800, so physical PITR from B500 is currently invalid for either target beyond the gap. The smallest missing evidence is the exact compatible WAL/log interval 760–800 plus authoritative mapping of H/G to their positions and stop semantics. A different complete base after 800 but before H could legitimately bypass the gap. Later WAL or a larger LSN cannot repair it.

### Answer 3

Accept a signed immutable request containing incident ID, database/system ID, history ancestry, base/parent IDs, target type/value, inclusive rule, target action, expected known-good/bad markers, and verification policy. Resolve immutable artifacts read-only; validate manifests, sizes/digests, parent graph, continuous log path, versions/platform/extensions, keys, and tool compatibility. Create a fresh network-isolated destination with capacity and inert external integrations. Generate configuration rather than accepting interactive edits, pause at target, and record every segment, command, version, result, timing, and resource. Make attempts uniquely identified and restartable; a failure never mutates source or promotes a partial candidate. Run the verification vector and require explicit authority/fencing for promotion.

### Answer 4

Latest replica failover is ineffective because deletion propagated. Physical PITR restores the whole database before deletion and is efficient at scale but loses/confronts all later valid changes and needs external reconciliation. Logical selective recovery can restore only the tenant from a pre-deletion dump/candidate, preserving unrelated later transactions, but dependencies and merge conflicts require careful identity/constraint checks. Application compensation can recreate deleted state from audit/events without changing authority, but only if the history is complete and inverse semantics are sound. Often combine physical PITR into isolation with logical extraction/merge of the tenant, then reconcile external effects by stable IDs.

### Answer 5

Map the harmful operation and adjacent acknowledged payments to exact history/LSN boundaries and record inclusive semantics. Restore an independently protected chain with escrowed keys into an isolated region, outbound payments disabled. Inject missing/corrupt segments, wrong timeline, key/credential failure, ENOSPC, slow transfer, worker crash, repeated recovery failure, and verification defects. Verify manifests/pages/checksums, indexes/allocations/constraints/prepared transactions, known-good/bad operations, double-entry totals, uniqueness, audit continuity, roles/policies, and external processor/outbox outcomes. Measure detection through traffic as RTO and quantify lost/retained payments as RPO. Promotion requires security/operations/business authorization, old-writer fencing, a new epoch/history, backups/archiving, and limited canary traffic. Preserve the candidate and old authority; rollback is a fenced switch plus reconciliation of post-fork operations, never physical concatenation or silent data loss.
