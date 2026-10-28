---
module_id: DBE-029
program: Database Engineering
level: 1
module_number: 29
title: Checksums and Page Corruption
status: complete
last_verified: 2026-08-30
---

# Checksums and Page Corruption

## One-Page Review

### Governing question

How can a database detect, contain, diagnose, and recover from corrupted page state without mistaking one checksum for complete integrity or destroying the evidence needed to determine root cause?

### Essential definitions

**Physical corruption** means stored/transferred bytes differ from the intended page image. **Logical corruption** means bytes may be internally well formed yet violate database invariants. A **checksum** maps protected bytes and context to a compact value; verification detects a mismatch but normally neither localizes nor repairs it. A **torn write** contains parts from different page versions. A **misdirected write** stores valid bytes at the wrong address. **Latent corruption** remains undetected until read/scrub. **End-to-end integrity** protects identity, bytes, ordering, and meaning across memory, software, filesystem, controller, media, backup, and restore. **Scrubbing** proactively reads and verifies stored data. **Quarantine** prevents suspect state from silently serving or propagating.

### Central model, mechanism, or theorem

Integrity requires layers with independent failure coverage. A page checksum covers a precisely defined serialized image; incorporating page identity/address can detect some misplaced copies. Read verification catches covered byte changes before interpretation. Structural verifiers check relationships that a per-page digest cannot express. WAL/full-page images, doublewrite storage, replicas, backups, or erasure coding may provide repair candidates, but only if independently verified and consistent with the recovery point. Cryptographic authentication is required against an attacker who can rewrite data and checksum together.

### Critical invariants

- Checksum generation and verification cover the same canonical bytes, identity context, algorithm, seed, and excluded checksum field.
- A page is not interpreted or served after failed physical validation except through an explicit forensic/recovery path.
- Verification distinguishes never-initialized pages and sanctioned transitional states from corruption.
- Page identity, type, format version, bounds, LSN, and structure are checked in addition to checksum.
- Detection never implies a repair source exists; repair never overwrites the only evidence before capture.
- Replicas and backups are verified independently before use because corruption can propagate.
- Repair preserves transaction/recovery consistency, not merely local checksum validity.
- Alerts, affected scope, evidence, containment, repair, and post-repair verification are auditable.

### Common failures

Failures include hashing only payload while ignoring identity/header; accepting a valid page at the wrong block; verifying after parsing unsafe offsets; trusting a checksum copied with corrupted bytes; using a non-keyed checksum against adversarial modification; assuming collision impossibility; silently zeroing a bad page; rebuilding an index from a corrupt heap; copying corruption to replicas/backups; promoting an unchecked replica; running destructive repair before imaging evidence; disabling checksums to suppress alerts; treating a clean scrub as proof of absence; and ignoring RAM, DMA, decompression, encryption, firmware, or software-bug boundaries.

### Compact example

A digest over `(relation, block, payload)` verifies the intended page. One flipped bit and a half-old/half-new torn image fail. Moving the unchanged page from block 7 to block 8 also fails because address is bound; a payload-only digest would incorrectly pass. If an attacker or buggy component rewrites both bytes and digest, ordinary checksum verification passes. Two individually valid pages can still disagree about whether an index entry has a heap row. These cases show detection coverage rather than one universal integrity bit.

### Connections

This module extends [DBE-021](021-pages-blocks-and-database-files.md), [DBE-026](026-buffer-pools.md), and [DBE-028](028-dirty-pages-and-writeback.md). DBE-030 follows one row across these layers; DBE-072 through DBE-080 later develop logging, recovery, backup, and restore verification. Computer architecture supplies ECC and memory faults; operating systems/storage supply atomicity and barriers; security engineering supplies authenticated integrity and evidence handling.

## Governing Question

The governing question contains four separate obligations: what faults are detectable, where detection occurs, what happens after detection, and how a trusted replacement is established. A checksum answers only part of the first two. A production integrity design must state protected objects, failure/adversary model, verification occasions, false-negative/collision assumptions, containment policy, repair authority, and residual risk.

## Why This Matters

Storage corruption is dangerous when it is silent. A malformed header may crash loudly, but a plausible changed key can cause a wrong query result, a missing index entry, a broken recovery chain, or a poisoned backup. The longer detection is delayed, the more copies and recovery points may inherit the fault.

Database pages cross many boundaries: CPU cache and RAM, buffer manager, checksum/compression/encryption code, kernel cache, filesystem, volume manager, controller, device firmware/media, replication, backup, and restore. Each layer can detect or introduce errors. Device ECC does not validate database semantics; a database checksum does not prove the storage command reached stable media; a structural index check does not verify every media byte.

Checksums also create operational decisions. A mismatch during a read can abort one query, take a page/relation offline, trigger replica comparison, or stop the engine, depending on scope and policy. Availability pressure tempts operators to bypass validation or copy a page from somewhere convenient. That action can turn detectable damage into an internally consistent but transactionally wrong database.

Strong engineering therefore treats the first checksum error as an incident, not an isolated retry. Preserve logs and images, establish scope, stop suspect propagation, inspect storage and memory health, identify trustworthy recovery sources, repair through engine-aware procedures, and verify the full logical/recovery boundary afterward.

## Prerequisites and Retrieval

Retrieve page header/identity/layout invariants from [DBE-021](021-pages-blocks-and-database-files.md), frame and I/O publication rules from [DBE-026](026-buffer-pools.md), and immutable write image/WAL ordering from [DBE-028](028-dirty-pages-and-writeback.md). You should understand hashes/checksums, probability, filesystems, storage atomicity, redundancy, backups, transaction consistency, and incident response.

Before continuing, explain why a checksum mismatch proves that observed input and expected digest disagree but does not identify which is correct; why two valid page checksums do not prove a valid B+ tree; and why copying a page from a replica requires recovery-position and identity checks.

This chapter uses SHA-256 only for a transparent executable illustration, not as a recommendation for database page format, performance, or adversarial protocol. Real engines choose algorithms, widths, seeds, address binding, and compatibility rules under format and performance constraints.

## Learning Objectives

After completing this module, you should be able to:

1. classify physical, structural/logical, latent, misdirected, stale, torn, and adversarial corruption;
2. define an unambiguous checksum coverage and verification contract;
3. explain the detection limits of per-page checksums and collision probability;
4. compare checksums, ECC, authenticated tags, structural verifiers, scrubs, doublewrite, WAL, replicas, and backups;
5. design safe read/write verification ordering and error containment;
6. diagnose corruption without destroying evidence or spreading damage;
7. select and validate a transactionally appropriate repair source;
8. design fault injection, scrubbing, recovery drills, and observability; and
9. scope integrity claims to the tested failure and threat model.

## Core Exposition

A checksum contract begins with serialization. Specify the exact page length, byte order, format/version, checksum field treatment, padding, compression/encryption stage, and contextual seed. If the writer hashes plaintext but the reader hashes ciphertext, or one includes mutable padding that the other does not initialize, correct data will fail verification. The checksum field is normally zeroed/excluded during calculation.

Context matters. A digest over payload alone detects many bit changes but accepts the same valid bytes at another address. Including relation/tablespace identity and block number can detect some misdirected writes. It still may not detect a stale but once-valid image written back to the same address; monotonic page generation/LSN and recovery reasoning add coverage. Identity fields inside corrupted bytes are not equivalent to trusted expected context supplied by the caller.

Collision resistance is probabilistic. A `b`-bit idealized checksum has accidental random collision probability roughly `2^-b` for one independent corrupted image, but real faults are not necessarily uniform/independent, implementation bugs can create systematic blind spots, and fleet-scale repeated opportunities matter. A small fast CRC can be appropriate for accidental faults; it is not authentication. An attacker able to modify both page and checksum can recompute it unless a secret-key/MAC or authenticated encryption binds the data and context.

Verification should precede unsafe interpretation. The read path knows expected physical/logical identity and length, obtains a complete page image, validates transport/I/O results, checksum/authentication, header/version/type, offsets/counts/bounds, and then exposes it as valid. Parsing untrusted slot offsets before checksum/bounds validation can turn corruption into memory-safety or denial-of-service risk.

Writes calculate integrity metadata from a stable image after all covered transformations are finalized. Compression and encryption complicate placement: an authenticated encryption tag may protect ciphertext and associated identity, while an internal checksum may protect the database page before encryption. Each catches faults in different segments and needs explicit key/version/nonce handling. Re-dirty concurrency from DBE-028 still applies.

A torn page combines sectors/chunks from old and new versions when page size exceeds the atomic-write guarantee or the stack violates it. A checksum usually detects the mixture, but detection alone cannot reconstruct either full version. Recovery can use a full-page WAL image, a doublewrite copy, an atomic-write facility, shadow/copy-on-write protocol, or verified redundant copy. Each mechanism has ordering and its own corruption/failure domain.

MySQL documents InnoDB's doublewrite buffer: pages are first written to a separate area and then to their data-file positions; crash recovery can use the good copy for incomplete writes. PostgreSQL uses page checksums and recovery mechanisms including full-page images under its WAL configuration. These implementations are different; “has WAL” does not automatically mean arbitrary torn pages are repairable under every setting and failure.

Physical validity does not imply logical validity. An index page can be well-formed and correctly checksummed yet omit a heap tuple because buggy maintenance wrote a self-consistent wrong state. A catalog row can reference a missing object. Sibling pointers can form the wrong topology while every individual page digest matches. Structural tools traverse cross-page/heap-index invariants and complement physical checks.

PostgreSQL's `amcheck` documentation explicitly distinguishes structural checks from data checksums and warns that verification can use cached pages rather than reread the filesystem. It also states that clean results cannot prove corruption absence. That is a general lesson: every verifier has coverage, sampling/caching, concurrency, permissions, and trusted-code limitations.

Scrubbing reduces detection latency by reading cold data proactively. A scrub schedule considers dataset size, media error rates, I/O budget, backup retention, recovery-point lifetime, replicas, tenant priorities, and the window before all good copies may age out. Scrubs should force the intended storage path when the goal is media verification and record bytes/objects actually examined. Aggressive scrubbing can harm workload latency or accelerate marginal hardware; pace and isolate it.

On detection, avoid automatic destructive “repair.” First classify evidence: exact object/page/address, expected/actual checksum, header/type/LSN, read path and replica, timestamps, storage/kernel/controller errors, recent maintenance/upgrades, memory telemetry, and backup/scrub history. Capture raw page and surrounding metadata through supported forensic procedures with access controls because pages contain sensitive data.

Containment depends on scope. Stop serving the bad page/result; pause processes that might rewrite or replicate it; prevent suspect backups from expiring known-good generations; consider isolating the host/device/replica; and avoid failover until the target is checked. Retrying a read may distinguish transient transport behavior but must not erase the original error or make the retry result proof of correctness.

Repair source selection is consistency-aware. A replica page must match object incarnation, block, format, encryption key, timeline/term, and a recovery point compatible with surrounding database state. A backup may require WAL replay to a coherent point. Rebuilding an index can be safe only if the heap and comparison semantics are trusted. Restoring one heap page can break transaction visibility or cross-page structures. Prefer documented engine procedures and named database/storage experts.

After repair, verify more than the checksum: page format, relation/index invariants, catalog dependencies, relevant query results, WAL/recovery ability, replicas, backups, and storage/memory health. Otherwise the symptom is hidden while the cause remains. Root cause can be media, cable/controller, firmware, RAM/DMA, filesystem, unsafe storage acknowledgement, software bug, misconfiguration, backup tool, manual file copy, or faulty repair.

Integrity observability includes checksum failures by object/block/read source, structural-check failures, read/I/O errors, corrected/uncorrected device and ECC events, scrub coverage/age/rate, repair source and verification, replica divergence, backup verification age, restore drills, firmware/device identity, and propagation scope. Cardinality/privacy controls matter: logging raw page content is usually unsafe.

Testing should inject single/multi-bit flips, zeroed sectors, torn combinations at every cut, duplicated/misdirected/stale pages, truncated/short reads, wrong length/type/version, malformed offsets/counts, decompression/authentication failures, corrupted checksum metadata, RAM-side changes, and logically inconsistent but correctly checksummed structures. Crash/power-cut campaigns and storage fault injection supplement deterministic models. Always preserve a control and validate the detector itself.

The executable model demonstrates detection boundaries on tiny byte strings. It binds relation and block as trusted context, then separately tests content-only verification, a torn mixture, a recomputed malicious/buggy rewrite, and a cross-page logical invariant. It does not model page formats, collision rates, storage, concurrency, recovery, or authentication.

<!-- bijux-verify: {"id":"page-integrity-boundaries","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid_page=True\nbit_flip_detected=True\ntorn_write_detected=True\nmisdirected_detected_with_address=True\nmisdirected_detected_without_address=False\nrecomputed_corruption_detected=False\nlogical_mismatch_detected_by_checksum=False\nlogical_mismatch_detected_by_invariant=True\n","stderr":""}} -->
```python
import hashlib


def digest(relation: str, block: int, payload: bytes) -> bytes:
    context = relation.encode("utf-8") + b"|" + str(block).encode("ascii") + b"|"
    return hashlib.sha256(context + payload).digest()


def content_digest(payload: bytes) -> bytes:
    return hashlib.sha256(payload).digest()


old_payload = b"row=42;balance=0900;state=old"
new_payload = b"row=42;balance=1000;state=new"
expected = digest("accounts", 7, new_payload)
valid_page = digest("accounts", 7, new_payload) == expected

bit_flipped = bytes((new_payload[0] ^ 1,)) + new_payload[1:]
bit_flip_detected = digest("accounts", 7, bit_flipped) != expected

cut = len(new_payload) // 2
torn = new_payload[:cut] + old_payload[cut:]
torn_write_detected = digest("accounts", 7, torn) != expected

misdirected_with_address = digest("accounts", 8, new_payload) != expected
payload_only_expected = content_digest(new_payload)
misdirected_without_address = content_digest(new_payload) != payload_only_expected

rewritten = b"row=42;balance=0000;state=new"
rewritten_checksum = digest("accounts", 7, rewritten)
recomputed_corruption_detected = digest("accounts", 7, rewritten) != rewritten_checksum

heap_payload = b"heap_ids=42"
index_payload = b"index_ids=42,99"
heap_valid = digest("heap", 3, heap_payload) == digest("heap", 3, heap_payload)
index_valid = digest("index", 5, index_payload) == digest("index", 5, index_payload)
logical_mismatch_detected_by_checksum = not (heap_valid and index_valid)
logical_mismatch_detected_by_invariant = b"99" in index_payload and b"99" not in heap_payload

print(f"valid_page={valid_page}")
print(f"bit_flip_detected={bit_flip_detected}")
print(f"torn_write_detected={torn_write_detected}")
print(f"misdirected_detected_with_address={misdirected_with_address}")
print(f"misdirected_detected_without_address={misdirected_without_address}")
print(f"recomputed_corruption_detected={recomputed_corruption_detected}")
print(f"logical_mismatch_detected_by_checksum={logical_mismatch_detected_by_checksum}")
print(f"logical_mismatch_detected_by_invariant={logical_mismatch_detected_by_invariant}")
```

The two `False` detection results are deliberate. The content-only digest cannot distinguish address 7 from 8, and a recomputed unkeyed digest accepts rewritten content. The two self-checksummed logical pages both pass locally while a cross-page invariant detects the phantom index identifier.

## Definitions and Notation

Let canonical serialized page image be `P`, trusted expected identity/address context be `A`, checksum algorithm/version and seed be `K`, and stored checksum be `c`. Generation is `c := C_K(A || P_without_c)`. Verification accepts exactly when recomputation equals `c`, after required length/I/O checks.

For an idealized `b`-bit output and an independent random erroneous image, collision probability is `2^-b`; after `n` independent opportunities, a union upper bound is `n*2^-b`, capped at one. This is not a field-failure estimator without justified independence and fault distribution.

Detection latency is time from corruption occurrence to trustworthy alert. Exposure is the set of live/replica/backup states that might contain or derive from suspect data. Recovery point identifies a transactionally coherent state, not merely a page timestamp. **False negative** here includes covered corruption that verifies due to collision/bug, corruption outside coverage, and logical corruption the physical checksum was never designed to detect.

## Mechanisms, Invariants, or Proof Structure

A defensible integrity workflow is:

1. Define protected objects and accidental/adversarial failure model.
2. Canonicalize page image and bind trusted identity, format, and transformation context.
3. Generate integrity metadata from one stable write image.
4. Preserve DBE-028 WAL, write-order, generation, and durability invariants.
5. On read, validate exact length/I/O result and physical integrity before unsafe parsing.
6. Validate header/type/identity/format/offset bounds and then access-method/logical invariants.
7. Quarantine a failure, preserve evidence, and establish affected propagation scope.
8. Select a recovery source independently verified for identity and recovery consistency.
9. Repair through an engine-aware method, then verify page, structure, recovery, replicas, and backups.
10. Investigate root cause and improve scrubbing, redundancy, alerts, or procedures.

Checksum soundness is conditional: if canonicalization is identical, expected context is trustworthy, the stored digest is itself covered appropriately, algorithm implementation is correct, and no collision occurs, a changed covered input is rejected. None of those premises proves semantic correctness or supplies repair.

Operational safety requires fail-closed interpretation with a controlled exception for forensic recovery. Availability may require serving unaffected ranges, but every bypass must be scoped, observable, time-bounded, and approved. A global “ignore checksum failures” switch is not a repair.

## Alternatives and Trade-Offs

CRC/fletcher-style checksums are fast and target accidental errors; wider cryptographic hashes reduce accidental collision probability at CPU/storage cost; MACs/authenticated encryption resist unauthorized recomputation but add key/nonce lifecycle and do not validate database semantics. ECC corrects/detects at memory/media units but may not cover software, DMA, addressing, or end-to-end transformations.

Inline read verification detects access-time faults cheaply but leaves cold data latent. Background scrubbing improves coverage at I/O cost. Offline whole-cluster verification offers a stable scan boundary but needs downtime/coordination and still samples a moment. Structural verification finds logical/access-method faults but consumes CPU/I/O/locks and trusts comparison/parser code.

Doublewrite/full-page-image/shadow mechanisms supply potential torn-write recovery with extra writes/log space/complexity. Replication improves availability but can rapidly reproduce logical corruption; backups give history but can be stale or corrupted. Erasure coding repairs some shard/media losses but not valid-looking application mistakes. Diversity of failure domain and verification matters more than copy count alone.

## Failure Modes and Misconceptions

- “A valid checksum proves the page is correct.” It proves only equality under a bounded checksum contract.
- “Checksums repair corruption.” They detect covered mismatches; another trustworthy source/mechanism repairs.
- “SHA means authenticated.” An unkeyed hash can be recomputed by an attacker who can alter metadata.
- “Storage ECC makes database checksums redundant.” Coverage boundaries and identities differ.
- “WAL always repairs a torn page.” Required images/settings/records may not exist or remain retained.
- “A replica is a clean copy.” It may share the fault, hardware class, software bug, or propagated write.
- “Retry success means false alarm.” Transient paths/caches can return different bytes; preserve both observations.
- “Reindex repairs corruption.” It is unsafe if source heap/collation/comparison state is not trusted.
- “A clean verifier proves absence.” Coverage, cache path, concurrency, sampling, collisions, and verifier bugs remain.
- “Zeroing the page restores service.” It destroys unknown data and recovery evidence and may break structures.
- “Disable validation during incidents.” Bypass can amplify damage; use controlled forensic paths.
- “More copies mean safe.” Correlated failure and silent propagation can invalidate every copy.
- “Checksum overhead is the only cost.” Scrub I/O, incident handling, format compatibility, and key lifecycle matter.
- “Corruption is only a disk problem.” RAM, DMA, firmware, software, tools, humans, and recovery paths participate.

## Worked Examples

### Example 1

A page for block 12 is copied intact to block 13. Its payload checksum passes, but an address-bound checksum using trusted expected block 13 rejects it. Storing the block number only inside the copied page would not supply independent expected context.

### Example 2

An 8 KiB page write leaves the first 4 KiB new and second 4 KiB old after power loss. Recomputed checksum mismatches, detecting the tear. Recovery still needs a full valid image from WAL/doublewrite/replica/backup; detection is not reconstruction.

### Example 3

One bit flips in RAM after read verification but before query interpretation. A disk checksum verified only on input cannot detect it. ECC, protected memory paths, revalidation at transformations, assertions, and structural checks address additional boundaries without giving absolute protection.

### Example 4

Every B+ tree page has a valid checksum, but a collation change invalidates key ordering. Physical checks pass while a structural verifier finds out-of-order keys. Rebuilding is considered only after comparison semantics and heap correctness are established.

### Example 5

Primary storage reports a mismatch. The standby has the same bad page because physical replication copied it. An older verified backup plus retained WAL may be a better recovery source. Copy count did not equal independence.

### Example 6

A scrub processes 20 TiB at 100 MiB/s. Ignoring contention, it needs `20*1024*1024/100=209,715.2` seconds, about 58.25 hours. A weekly target is feasible nominally, but production needs throttling, retries, coverage accounting, and headroom.

### Example 7

A checksum mismatch is followed by a successful reread. The system records both images and paths, quarantines the suspect device/cache route, and verifies replicas/backups. It does not erase the first alert or call the page healthy from one retry.

### Example 8

An operator copies a raw page from another node at a later timeline. The checksum and block identity pass, but transaction visibility and neighboring structures are incompatible. Engine-aware point-in-time recovery was required; local validity was insufficient.

### Example 9

An attacker changes a balance and recomputes an unkeyed SHA-256. Verification passes. A MAC or authenticated encryption with protected keys could detect unauthorized change, while authorization/audit controls and logical reconciliation remain necessary.

### Example 10

A canary firmware cohort shows rising corrected media errors without checksum failures. Waiting for database corruption wastes early warning. The team drains the cohort, preserves metrics, verifies pages/backups, and investigates the correlated hardware boundary.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hashes, Merkle structures, trees, and invariants.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies filesystems, atomic writes, caches, and error propagation.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies ECC, memory hierarchy, DMA, controllers, and media faults.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies MACs, authenticated encryption, key management, forensics, and adversaries.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies scrubbing, observability, incident containment, fault injection, and recovery drills.

## References

1. PostgreSQL Global Development Group, [Data Checksums](https://www.postgresql.org/docs/current/checksums.html), current page-checksum coverage and offline verification behavior.
2. PostgreSQL Global Development Group, [amcheck](https://www.postgresql.org/docs/current/amcheck.html), current heap/index structural verification, limits, and repair cautions.
3. PostgreSQL Global Development Group, [pg_checksums](https://www.postgresql.org/docs/current/app-pgchecksums.html), current offline checksum enable/disable/check workflow and synchronization cautions.
4. Oracle, [InnoDB Doublewrite Buffer](https://dev.mysql.com/doc/refman/8.4/en/innodb-doublewrite-buffer.html), MySQL 8.4 incomplete-page detection and recovery design.
5. SQLite Project, [Atomic Commit](https://www.sqlite.org/atomiccommit.html), official sector atomicity, powersafe overwrite, flush, and corruption assumptions.
6. Bianca Schroeder and Garth A. Gibson, [Disk Failures in the Real World: What Does an MTTF of 1,000,000 Hours Mean to You?](https://www.usenix.org/legacy/events/fast07/tech/schroeder/schroeder.pdf), FAST 2007 empirical disk-failure study.
7. Lakshmi N. Bairavasundaram et al., [An Analysis of Data Corruption in the Storage Stack](https://www.usenix.org/legacy/events/fast08/tech/full_papers/bairavasundaram/bairavasundaram.pdf), FAST 2008 empirical storage-stack corruption study.
8. OpenZFS Project, [Checksums and Their Use in ZFS](https://openzfs.github.io/openzfs-docs/Basic%20Concepts/Data%20Storage/Checksums.html), official end-to-end checksum, redundancy repair, and scrubbing documentation.
9. C. Mohan et al., [ARIES](https://web.stanford.edu/class/cs345d-01/rl/aries.pdf), recovery and page-oriented WAL foundations.
10. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, storage and recovery foundations.

## Exercises

### Exercise 1

Define a checksum contract for 16 KiB pages with relation UUID, block number, format version, checksum field, compression, and encryption. State generation/verification order and failure coverage.

### Exercise 2

For a 32-bit ideal checksum and one billion independent random corrupted-page verification opportunities, compute the union upper bound and explain why it is not a real fleet-risk estimate. Compare 64 and 256 bits.

### Exercise 3

Design a fault-injection matrix for bit flips, torn, zeroed, duplicated, misdirected, stale, truncated, maliciously recomputed, and logically inconsistent pages across RAM, kernel, device, replica, backup, and restore.

### Exercise 4

A primary reports one checksum failure; one replica matches the bad bytes, another has an older good image, and backups span three recovery points. Write a safe incident/repair decision process.

### Exercise 5

Design a production integrity program with inline verification, structural checks, scrub cadence, telemetry, alerting, evidence controls, recovery drills, canaries, and explicit residual claims.

## Answers to the Exercises

### Answer 1

Define canonical plaintext page bytes with initialized padding and checksum field zeroed, plus trusted associated context `(relation_uuid, block, format_version)`. If compression precedes encryption, decide whether the database checksum covers canonical plaintext/compressed bytes; then use authenticated encryption over ciphertext with context as associated data and unique key-version/nonce rules. On write, freeze image, finalize header/LSN, compute checksum at its defined layer, compress/encrypt, and preserve DBE-028 ordering. On read, validate length/I/O, authenticate ciphertext/context before decryption, decompress with bounds, recompute checksum over canonical input, then validate header/identity/offsets. It detects covered accidental changes/misdirection and authenticated tampering, not logical correctness, key compromise, all RAM faults, or rollback unless version/freshness is bound.

### Answer 2

The union bound is `min(1,10^9/2^32)`, approximately 0.233 or 23.3%. For 64 bits it is about `5.42*10^-11`; for 256 bits about `8.64*10^-69`. These assume ideal uniform outputs and independent random corruptions/opportunities. Real workload count, correlated fault patterns, algorithm structure, implementation defects, uncovered fields, and adversarial recomputation invalidate a direct fleet prediction. Wider output addresses collision probability, not semantics or repair.

### Answer 3

Generate known page identities/versions and inject each fault before checksum generation, after generation in RAM, during serialization, at kernel/device boundaries, in persisted sectors, and while copying to replica/backup/restore. Assert which layer detects: ECC/transport, address-bound checksum, authentication, header/bounds parser, LSN/version, structural heap-index/tree checker, recovery replay, or replica/backup comparison. Include old/new sector cuts, valid-page duplication to wrong address, same-address rollback, checksum-plus-content rewrite, corrupted integrity metadata, short reads, and self-consistent logical omissions. Preserve negative controls, exact seeds/cuts, and evidence; verify containment and repair, not only alarm count.

### Answer 4

Stop serving/rewriting the page and pause suspect propagation/retention expiry; preserve raw images, identifiers, LSN/timeline, errors, topology, and storage/memory evidence with access control. Determine whether both matching nodes share lineage/fault and verify the older replica plus backups independently. Establish a transactionally coherent target recovery point and required WAL, surrounding pages, heap/index/catalog relationships, encryption/format identity, and recovery procedure. Prefer documented restore/replay or rebuild only from a trusted source; do not raw-copy solely because a checksum passes. Repair in isolation, verify physical and structural state, recovery/startup, queries, replicas/backups, then investigate root cause before returning capacity.

### Answer 5

Enable format-supported inline physical validation and safe fail-closed handling; schedule forced-path scrubs with byte/object coverage and age; run heap/index/catalog structural checks at controlled load; retain multiple independently verified recovery points and perform restores. Collect checksum/structure/I/O/ECC/device/firmware/replica divergence and scrub metrics without leaking page contents. Alert on first physical mismatch and trend precursors; provide an evidence-preserving runbook, named database/storage/security owners, quarantine authority, and tested repair/escalation. Inject faults and power cuts in nonproduction, canary firmware/settings, and drill recovery. Claim only detection for defined covered bytes/faults and demonstrated restore for tested points; do not claim absence of corruption, perfect hardware, adversarial integrity without keys, or universal recovery.
