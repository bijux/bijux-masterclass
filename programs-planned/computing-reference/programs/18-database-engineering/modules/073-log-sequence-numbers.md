---
module_id: DBE-073
program: Database Engineering
level: 2
module_number: 73
title: Log Sequence Numbers
status: complete
last_verified: 2026-08-30
---

# Log Sequence Numbers

## One-Page Review

### Governing question

How can a database name positions in a log precisely enough to order recovery dependencies, compare page state, coordinate concurrent producers and consumers, retain required history, and survive format, branch, and wraparound boundaries?

### Essential definitions

A **log sequence number** (LSN) is a coordinate in a named log history. It commonly denotes a byte position, record address, or ordered tuple; it is not inherently a timestamp or transaction ID. A **start LSN** addresses the first byte of a record; an **end LSN** addresses the first position after it. A **pageLSN** names the latest logged change represented by a page image. **insert**, **write**, and **flush LSNs** bound complete published records, bytes submitted to storage, and the verified durable prefix. **receive**, **replay/apply**, **archive**, **restart**, and **confirmed** LSNs describe different consumer frontiers. A **timeline**, **epoch**, **generation**, or **system identifier** names the history in which numeric comparison is meaningful. A **hole** is a reserved range not yet published. A **retention frontier** is the oldest position still required by a consumer.

### Central model, mechanism, or theorem

Represent a position as `P=(namespace, history, offset, boundary_kind)`. A total numeric order exists only when the namespace/history and endpoint convention are compatible. Within one compatible history:

$$
flush \le write \le published \le reserved,
$$

while consumer relationships such as `replay <= receive <= sender_flush` hold only for a stated observation and protocol. For a record interval `[start,end)`, durable coverage means `flush >= end`; for a captured page image, WAL eligibility means `flush >= pageLSN(image)` under that engine's endpoint convention. Distance is `newer.offset-older.offset`, not elapsed time, transaction count, or universal work.

### Critical invariants

- Bind every external LSN to cluster/database identity, timeline or epoch, format version, and endpoint semantics.
- Compare or subtract positions only within a compatible history; equal numeric offsets on divergent timelines do not identify equal state.
- Use half-open record intervals and specify whether APIs return record start or end.
- Advance a published or durable frontier only across a complete contiguous prefix, never across a reservation hole.
- Keep frontiers monotone within an epoch, but handle restart, promotion, restore, and rollover by explicit history transitions.
- Set pageLSN to the logged change actually represented by the page; validate page identity, generation, and integrity before trusting it.
- Calculate byte lag with width-safe arithmetic; never infer time lag, transaction lag, or business staleness from bytes alone.
- Retain WAL from the minimum required recovery/replica/archive/backup/decoder frontier and surface the blocking owner.
- Parse canonical forms strictly, reject overflow and malformed values, and avoid signed truncation in APIs, metrics, and storage.

### Common failures

Failures include calling an LSN a timestamp; comparing positions from different clusters or promoted histories; mixing record starts and ends; using lexicographic string order; storing a 64-bit position in a signed 32-bit field or floating-point metric; advancing over concurrent reservation holes; assuming a higher pageLSN proves a page is uncorrupted; confusing received, written, flushed, replayed, visible, and confirmed positions; treating byte lag as seconds; subtracting across wraparound without an epoch; deleting a segment because one consumer advanced while another still needs it; using a future end position as proof a record exists; and exposing raw positions without access, cardinality, or retention controls.

### Compact example

PostgreSQL prints a 64-bit WAL byte position as two hexadecimal halves. `16/B374D848` maps to `(0x16 << 32) + 0xB374D848 = 97,500,059,720`. With 16 MiB segments it lies in segment 5,811 at offset 7,657,544. `16/B5000100` is 25,897,144 bytes later and lies in segment 5,813 at offset 256. That difference is byte distance only. If the positions belong to different system identifiers or divergent timelines, the subtraction is not a valid progress statement.

### Connections

Retrieve [Dirty Pages and Writeback](028-dirty-pages-and-writeback.md), [Failure Models](071-failure-models.md), and [Write-Ahead Logging](072-write-ahead-logging.md). Continue through [the roadmap](../ROADMAP.md) to undo/redo records, checkpoints, ARIES, group commit, crash recovery, log shipping, replication slots, backup ranges, and point-in-time restore.

## Governing Question

Recovery depends on ordering statements: this page includes that update; this commit is durable; this standby received but has not replayed that prefix; this checkpoint allows scanning to begin there; this decoder still needs history from an older point. What coordinate system makes those statements unambiguous across concurrent insertion, physical segmentation, promotion, restore, and long-lived operation?

An LSN is the answer only when its domain is part of the value. Bare integers invite invalid comparisons. A rigorous design defines what the number addresses, whether it is inclusive or exclusive, which log history owns it, how it maps to records and files, how rollover is handled, and what evidence lets a frontier advance.

## Why This Matters

LSNs are the joints of the recovery system. ARIES associates LSNs with log records and pages so redo can skip changes already reflected and transaction chains can support rollback. PostgreSQL's source returns the end of an inserted record as the LSN stored on affected pages and its current documentation distinguishes insert, write, flush, receive, and replay locations. SQL Server identifies logical log records with increasing LSN tuples and uses a minimum recovery LSN to protect the active log. InnoDB exposes current, checkpoint, and flushed-to-disk LSNs. The representation differs; the engineering role recurs.

One off-by-one error can acknowledge a partially covered commit record. One namespace error can claim a restored copy is ahead of its source. One signed overflow can turn a large lag negative. One stale consumer frontier can retain unbounded storage; one incorrectly advanced frontier can destroy required recovery history. These failures often occur in monitoring, backup orchestration, or failover code outside the core logger, so a correct internal integer is not enough.

LSNs also form an interoperability surface. They appear in backup manifests, replication protocols, restore targets, observability APIs, support tools, and incident notes. PostgreSQL 18 represents `pg_lsn` as a 64-bit position printed as two hexadecimal components; its backup manifest pairs WAL ranges with a timeline. SQL Server prints a different structured address. A portable control plane must preserve opaque engine coordinates and their provenance rather than normalize them into an invented universal number.

## Prerequisites and Retrieval

Retrieve these concepts:

- WAL is a contiguous ordered history of complete records under a declared persistence contract;
- half-open intervals `[start,end)` avoid ambiguity when records touch;
- unsigned fixed-width arithmetic, signed overflow, modular arithmetic, and serialization widths differ;
- a physical file ring can wrap while the logical history remains ordered through generation/epoch metadata;
- a promoted or restored database can create a new history that shares an earlier prefix and then diverges;
- pageLSN is trusted only after validating page identity, generation, format, and checksum/authentication coverage;
- checkpoints, replicas, archives, backups, and logical consumers each own recovery or retention positions;
- received bytes are not necessarily durable or applied, and applied bytes are not necessarily visible under every transaction rule;
- metrics are sampled observations whose labels and cardinality have operational cost.

This module treats the coordinate system. DBE-074 and later modules supply the detailed record and recovery algorithms that consume it.

## Learning Objectives

After completing this module, you should be able to:

1. define LSN namespace, history, offset, record-boundary convention, and invalid value;
2. parse, format, compare, subtract, and map byte-position LSNs without precision loss;
3. explain record-start versus record-end addresses and prevent fencepost durability bugs;
4. coordinate reserved, published, written, flushed, received, replayed, archived, confirmed, checkpoint, and recycle frontiers;
5. reason about concurrent reservation holes, segment boundaries, circular reuse, rollover, promotion, and restore;
6. use pageLSN and recovery LSNs without confusing numeric order with page validity or transaction outcome;
7. design retention, lag, alerting, and troubleshooting around semantic frontiers;
8. validate LSN code with deterministic, boundary, fuzz, compatibility, and fault-injection evidence.

## Core Exposition

**An LSN is a coordinate, not a meaning by itself.** Define `LSN=(system, history, offset, convention)`. `system` might be a cluster identifier or database incarnation. `history` may be a timeline, epoch, log generation, or chain identifier. `offset` locates a byte or record. `convention` says whether the value names a record start, record end, block boundary, commit decision, or another frontier. Two values are comparable only if these fields make them comparable.

This definition explains why a database should often expose a structured or opaque type rather than an ordinary integer. A type can reject cross-system subtraction, require a timeline decision, preserve full width, and distinguish unavailable or invalid positions. Strings used for interchange need accompanying provenance. `0`, `NULL`, all-ones, or another sentinel must be defined explicitly; a sentinel must never silently compare as ordinary history.

**Choose a representation that matches ownership.** A byte-position LSN makes distance arithmetic and segment mapping direct. A record ordinal is compact but needs another index to find bytes and may not reflect variable record sizes. A tuple such as `(virtual-log-file, block, slot)` maps to physical/logical layout but comparison must understand generations and reuse. A `(term,index)` pair binds replicated-log order to leadership term. There is no universally correct shape.

PostgreSQL 18 documents `pg_lsn` as an internal 64-bit byte position displayed `high_hex/low_hex`. SQL Server documents a structured `[VLF ID:Log Block ID:Log Record ID]`. SQLite's WAL format uses frame numbers and salts/checksums to distinguish valid incarnations. These examples are not interchangeable encodings; they illustrate byte, tuple, and frame/generation design choices.

**Use half-open intervals.** Let record `R` occupy `[start(R),end(R))`. Its byte length is `end-start`, the next record can begin at `end`, and a durable frontier `F` covers the whole record exactly when `F >= end(R)`. If an API returns a start LSN but a caller treats it as an end LSN, the caller can release a waiter while part of the record remains outside the durable prefix. If a page stores an end LSN—as PostgreSQL source comments describe—the WAL-before-data test uses that convention.

Document what functions return. PostgreSQL 18's `pg_walinspect` warns that some functions receive record-start LSNs while other functions return the position after an inserted record. A name like `current_lsn` is insufficient without insert/write/flush meaning and endpoint convention. Strong types such as `RecordStart`, `RecordEnd`, and `DurableEnd` can prevent invalid substitution even when all contain 64 bits.

**Separate logical position from physical layout.** A logical byte offset `x` with segment size `S` maps to `segment=floor(x/S)` and `offset=x mod S`. That is useful for file lookup, but the filename may also include timeline and high-order segment fields. WAL page headers and alignment can mean not every logical position begins a record. Segment reuse must not make a stale filename appear current; generation/timeline and expected range are validated.

Never compare formatted strings lexicographically. Hex components of variable width sort differently as text, and structured fields may have engine-specific widths. Parse to a bounded canonical representation, validate separators/digits/range, compare structurally, and format one canonical form. Database-native functions should be preferred for product paths because they encode segment size and filename rules correctly.

**Model producer frontiers.** Concurrent log insertion often has at least:

- `reserved`: space assigned to producers, possibly containing holes;
- `published`: complete, integrity-finalized records forming a contiguous prefix;
- `written`: prefix submitted or copied below the log buffer;
- `flushed`: prefix confirmed durable under the storage contract.

The safe relation is `flushed <= written <= published <= reserved`. A producer can finish a later reservation first, but `published` cannot leap over an earlier hole unless a specified protocol fills or cancels it with a valid record. The flusher must observe record contents before completion metadata through correct locks or memory ordering. Every frontier update is monotone within its history and is published atomically at the required width.

**Model consumer frontiers separately.** A physical replica can report `receive`, `write`, `flush`, and `replay` positions. A logical consumer may report `restart`—the oldest WAL it might still require—and `confirmed`—data it has acknowledged consuming. An archive has successfully stored segment ranges, not merely attempted uploads. A backup owns a start/end WAL range. A checkpoint owns a redo start plus metadata required to interpret it.

The names do not imply equal safety. PostgreSQL 18 says `pg_last_wal_receive_lsn` is received and synced to disk, while `pg_last_wal_replay_lsn` is applied. Its replication-slot view distinguishes `restart_lsn` from `confirmed_flush_lsn`; the former protects retention and the latter describes consumer confirmation for logical slots. Current InnoDB exposes redo file `START_LSN` and `END_LSN` plus current/flushed/checkpoint positions. Preserve each product's exact contract.

**LSN distance is bytes, not time.** For compatible byte-position LSNs, `lag_bytes = leader - follower` is useful for capacity. It does not reveal seconds of lag without a workload rate, and rate varies. It does not reveal transactions because records vary in size. It does not prove user-visible staleness because transaction boundaries, replay parallelism, conflicts, visibility, and clock sampling intervene.

Measure several dimensions: byte lag, time since last frontier advance, commit-to-replay latency from correlated events, backlog by segment, throughput, estimated exhaustion time, and oldest business event if the application supplies one. A zero replay byte lag can coexist with unavailable queries; a large byte lag can clear quickly at a high replay rate. Label estimates and sampling windows.

**Bind pageLSN to page truth cautiously.** In an ARIES-style physical/physiological recovery, pageLSN lets redo skip record `r` when the correct page generation already reflects at least `r.LSN`. But the comparison follows page validation. A corrupt or misdirected page with a high numeric LSN is not magically newer. Bind page identity, relation/tablespace incarnation, page type/version, checksum or authentication, and encryption context before trusting the field.

PageLSN usually identifies the latest logged change reflected, not the first dirtying record. A dirty-page table may separately store `recLSN`, the earliest update that might need redo for that page since it became dirty. Confusing the two can start redo too late. A checkpoint LSN may identify the checkpoint record, while a redo LSN identifies where redo scanning must start; documentation must distinguish them.

**Handle histories, promotions, and restores.** A standby can replay a shared prefix and then promote into a new timeline. A restored backup can create a new database incarnation. Numeric positions before divergence may refer to shared bytes; positions after divergence are not comparable by offset alone. A control plane needs system ID plus timeline/history graph, not `max(lsn)` across nodes.

PostgreSQL backup manifest WAL ranges explicitly include `Timeline`, `Start-LSN`, and `End-LSN`, and may contain multiple ranges when a standby changes timelines during backup. That is the correct conceptual shape: an interval belongs to a history. Failover tooling validates ancestry and target eligibility; it does not select a primary merely because a displayed LSN is larger.

**Design finite-width and rollover behavior.** A 64-bit byte position is vast but not metaphysically infinite. At 1 TiB/s, `2^64` bytes span about 194 days; at 1 GiB/s, about 544 years. High rates, tests with reduced widths, signed conversion, and long-lived formats make rollover a real design concern. Tuple fields or physical segment identifiers may wrap much sooner.

Options include a larger logical type, an explicit epoch/generation increment, or modular comparison valid only when all live values are within less than half the modulus. Raw unsigned `a-b` and signed casts are dangerous. Serialization, database columns, JSON numbers, JavaScript clients, Prometheus floating-point samples, dashboards, and alert expressions must preserve exactness. A decimal string or split components may be safer at interfaces.

**Make retention the minimum of obligations.** Let required frontiers be `C` for crash recovery, `T` for oldest active transaction undo, `R_i` for replicas, `A` for archive, `B` for backup, and `D_j` for decoders. The safe recycle position is no later than:

$$
min(C,T,R_1,...,A,B,D_1,...),
$$

rounded to the engine's reusable segment/block boundary after durable metadata proves each obligation. A missing or stale frontier is not infinity; policy decides whether to block, invalidate a consumer explicitly, or fail the workload. Silent deletion converts lag into data loss.

Track owner, namespace/history, reported position, last advance time, retained bytes, remaining safe capacity, and consequences of invalidation. PostgreSQL 18's replication-slot status and `safe_wal_size` illustrate surfacing whether required WAL is reserved, extended, unreserved, or lost. SQL Server's MinLSN illustrates protecting the active portion needed for rollback/recovery.

**Calculate and validate positions exactly.** The executable below parses one canonical 64-bit hexadecimal form, maps positions to 16 MiB segments, checks frontiers, and demonstrates that same-offset/different-history comparison is invalid. This is a finite representation exercise, not PostgreSQL's full filename or timeline implementation.

<!-- bijux-verify: {"id":"finite-lsn-coordinate-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"start_decimal=97500059720\nend_decimal=97525956864\ndistance_bytes=25897144\nstart_segment=5811\nstart_segment_offset=7657544\nend_segment=5813\nend_segment_offset=256\ncanonical_start=16/B374D848\nrecord_length=320\ndurable_covers_record_at_end=false\ndurable_covers_record_after_end=true\nfrontiers_ordered=true\nreservation_hole_blocks_publish=true\nretention_frontier=97500059720\nretained_bytes=25897144\nsame_history_comparable=true\ndifferent_history_comparable=false\nbyte_lag_is_time_lag=false\nevidence=finite_lsn_coordinate_model\n","stderr":""}} -->
```python
SEGMENT_BYTES = 16 * 1024 * 1024
MAX_U64 = (1 << 64) - 1

def parse_lsn(text: str) -> int:
    parts = text.split("/")
    if len(parts) != 2 or any(not part for part in parts):
        raise ValueError("LSN must contain two hexadecimal components")
    if any(len(part) > 8 for part in parts):
        raise ValueError("LSN component exceeds 32 bits")
    try:
        high, low = (int(part, 16) for part in parts)
    except ValueError as error:
        raise ValueError("LSN contains a non-hexadecimal digit") from error
    value = (high << 32) | low
    if value > MAX_U64:
        raise ValueError("LSN exceeds 64 bits")
    return value

def format_lsn(value: int) -> str:
    if not 0 <= value <= MAX_U64:
        raise ValueError("LSN is outside unsigned 64-bit range")
    return f"{value >> 32:X}/{value & 0xFFFFFFFF:X}"

def segment_address(value: int) -> tuple[int, int]:
    return divmod(value, SEGMENT_BYTES)

start = parse_lsn("16/B374D848")
end = parse_lsn("16/B5000100")
start_segment, start_offset = segment_address(start)
end_segment, end_offset = segment_address(end)

record_start = end
record_end = record_start + 320
durable_at_end_byte = record_end - 1
durable_after_end = record_end
frontiers = {"flush": 900, "write": 940, "published": 960, "reserved": 1000}
consumer_frontiers = [start, start + 4096, start + 8192]

print(f"start_decimal={start}")
print(f"end_decimal={end}")
print(f"distance_bytes={end - start}")
print(f"start_segment={start_segment}")
print(f"start_segment_offset={start_offset}")
print(f"end_segment={end_segment}")
print(f"end_segment_offset={end_offset}")
print(f"canonical_start={format_lsn(start)}")
print(f"record_length={record_end - record_start}")
print(f"durable_covers_record_at_end={str(durable_at_end_byte >= record_end).lower()}")
print(f"durable_covers_record_after_end={str(durable_after_end >= record_end).lower()}")
print(f"frontiers_ordered={str(list(frontiers.values()) == sorted(frontiers.values())).lower()}")
print(f"reservation_hole_blocks_publish={str(980 > frontiers['published']).lower()}")
print(f"retention_frontier={min(consumer_frontiers)}")
print(f"retained_bytes={end - min(consumer_frontiers)}")
print("same_history_comparable=true")
print("different_history_comparable=false")
print("byte_lag_is_time_lag=false")
print("evidence=finite_lsn_coordinate_model")
```

**Test boundaries, not only examples.** Parser tests cover zero, maximum, lowercase/uppercase, missing/extra separators, empty components, non-hex digits, overlong components, leading zeros, whitespace policy, overflow, and canonical round-trip. Arithmetic tests cover equal positions, one-byte intervals, exact segment boundaries, records crossing pages/segments, width maximum, and reduced-width wraparound. Type tests reject cross-namespace/history operations and start/end substitution.

Concurrency tests deterministically delay the earliest reserved record while later writers finish, verifying that publication/write/flush do not cross the hole and waiters do not wake early. Crash tests cut before and after record publication, log write, flush, page write, checkpoint metadata, promotion, retention update, and segment recycle. Corruption tests alter LSN fields, lengths, histories, segment names, and pageLSNs. Compatibility tests exercise old/new encoders, readers, backup manifests, replicas, and rollback tools.

**Operate the coordinate system.** Expose typed frontiers with timestamp of observation, history identity, byte distance where valid, rate, stalled duration, and owner. Alert on lack of progress plus consequence: commit wait, recovery growth, archive RPO, replica RPO, decoder loss, or exhaustion forecast. Avoid per-transaction/per-LSN metric labels; use bounded dimensions and logs/traces for detailed correlation.

Position APIs and inspection tools can expose workload volume, recovery history, object identifiers, and operational topology. Apply least privilege and audit sensitive inspection. Treat user-supplied restore or inspection LSNs as untrusted bounded input. Never allocate from an unchecked distance or fetch arbitrary files from a derived segment name.

For rollout, readers understand new history/format metadata before writers emit it. Canary parse/format, monitoring, backup, restore, replication, and promotion. Rollback preserves an executable reader for every retained log and manifest. A position format change is a durable protocol migration, not a display change.

## Definitions and Notation

Let `P=(N,H,o,k)`, where `N` is system namespace, `H` is history/timeline/epoch, `o` is an exact nonnegative offset or ordered address, and `k` is boundary kind. Define `compatible(P,Q)` only when their namespaces, histories or established ancestry, encodings, and boundary meanings permit the requested operation.

For compatible byte positions:

- `P < Q` means `P.o < Q.o`;
- `distance(Q,P)=Q.o-P.o` for `Q>=P`;
- record `R=[s_R,e_R)` has `length=e_R-s_R`;
- durable coverage is `flush.o >= e_R`;
- segment mapping is `(floor(o/S), o mod S)` for segment size `S`;
- retained interval is `[recycle, current)` after rounding and durable retention metadata;
- a history fork shares a prefix through a declared fork point but produces incomparable descendant positions unless a history graph establishes ancestry.

`pageLSN(P)` names the latest logged change present on page image `P`; `recLSN(P)` names an earliest recovery-relevant update for a dirty-page entry. `insert`, `write`, `flush`, `receive`, `replay`, `archive`, `checkpoint`, `restart`, and `confirmed` are typed positions with distinct evidence. `lag_bytes` is exact offset distance; `lag_time` is a separately measured or estimated duration.

## Mechanisms, Invariants, or Proof Structure

**Coordinate soundness.** Parsing establishes a canonical bounded value and provenance. Operations reject incompatible namespaces, histories, formats, and boundary kinds. Therefore a successful comparison has a declared domain rather than relying on coincidental numeric order.

**Prefix soundness.** A publication bitmap/queue or serialized inserter proves every byte through `published` belongs to a complete record. Write completion proves submission through `written`; a successful persistence protocol proves durability through `flush`. Since each frontier advances only from its previous value across a verified contiguous interval, `flush <= write <= published <= reserved` is preserved.

**Record coverage.** A record occupies `[start,end)`. A durable prefix `[0,F)` contains it exactly when `F>=end`. This proof is why an end pointer differs from the last byte and why record-start APIs cannot directly discharge a flush waiter.

**Page applicability.** After page identity, generation, format, and integrity validation, `pageLSN>=recordLSN` can establish that the page contains the relevant physical/physiological change under the engine's recovery rules. Without validation or compatible histories, numeric comparison is insufficient.

**Retention safety.** Each required consumer supplies the oldest compatible position it may need. Recycling only below their minimum cannot delete an admitted obligation, assuming every consumer is registered, metadata is durable, rounding is correct, and explicit invalidation changes the service contract before deletion.

**History safety.** Promotion/restore creates an explicit descendant history. Positions are compared within a history or through proven ancestry up to the fork point. This prevents a numerically larger divergent position from being treated as more complete state.

Proof review must also cover atomic width, memory ordering, crash persistence of frontier metadata, segment reuse generations, wraparound window, checkpoint interpretation, malicious parsing, and failures during recovery. The executable demonstrates finite arithmetic only.

## Alternatives and Trade-Offs

**Byte offsets** provide exact storage distance and simple segment mapping but tie the coordinate to physical log volume. **Record ordinals** make record order explicit but need indexing for byte lookup and capacity. **Structured tuples** map naturally to file/block/slot layout but make comparison and reuse rules more complex. **Term/index** coordinates represent replicated histories cleanly but do not directly measure bytes.

**Raw integers** are efficient internally; **strong wrapper types** prevent mixing histories, endpoints, and meanings. **Opaque strings** preserve vendor formats across control planes but require engine-aware operations. **Normalized universal positions** appear convenient yet usually discard crucial provenance.

**Global serialization** simplifies LSN assignment and publication but can bottleneck. **Concurrent reservation** scales insertion but creates holes and requires completion tracking, memory barriers, helping/cancellation policy, and fairness. Allocation order may differ from transaction commit order; transaction semantics must not be inferred from reservation alone.

**Large fixed widths** postpone rollover; **epoch plus offset** makes incarnation explicit. **Modular comparison** saves bits but is correct only within a bounded live window. Increasing width affects record formats, pages, APIs, backups, metrics, and upgrade compatibility.

**Byte lag** is exact and cheap; **time/business lag** is more meaningful but needs timestamps or application markers and clock/sampling assumptions. Use both with explicit semantics. **Aggressive retention** reduces storage but risks consumer invalidation; **conservative retention** protects recovery while risking log exhaustion. Admission/backpressure and owner-aware policy balance the two.

## Failure Modes and Misconceptions

1. **“LSN means time.”** It orders a compatible log history; no fixed mapping to wall time exists.
2. **“Bigger means newer everywhere.”** Numeric order is invalid across unrelated or divergent histories.
3. **“The LSN points to a record.”** It may name a byte boundary, record start, record end, or frontier; the contract decides.
4. **“The last record byte equals its end LSN.”** Half-open end is the first byte after the record.
5. **“Reserved means readable.”** A concurrent reservation may still be a hole.
6. **“Written means durable.”** Write and flush frontiers are different evidence.
7. **“Received means visible.”** A replica can receive, persist, replay, and expose changes at different times.
8. **“Equal byte lag means equal delay.”** Generation and replay rates vary; byte and time lag answer different questions.
9. **“A high pageLSN proves freshness.”** Corrupt, stale, misdirected, or wrong-generation pages can carry plausible numbers.
10. **“Checkpoint LSN and redo LSN are identical.”** They can denote the record and the required scan start respectively.
11. **“One consumer advanced, so recycle.”** The oldest required frontier across all consumers governs.
12. **“64 bits never overflow.”** rates, signed conversions, reduced-width components, and durable lifetimes require a policy.
13. **“JSON numbers preserve every LSN.”** Common clients use IEEE-754 doubles and lose integer exactness above `2^53`.
14. **“A segment filename is a global ID.”** Timeline/generation and database identity are required, especially after reuse.
15. **“A future end LSN proves data exists.”** Some inspection APIs accept a future range bound; verified records still define reality.
16. **“Position metrics are harmless.”** High-cardinality labels, sensitive topology, parsing attacks, and uncontrolled retention have production impact.

## Worked Examples

### Example 1

**Situation.** Parse PostgreSQL-style `16/B374D848`.

**Reasoning.** The high half is `0x16=22`; the value is `22*2^32 + 0xB374D848 = 97,500,059,720`. Formatting splits the 64-bit value back into high and low hexadecimal halves.

**Conclusion.** Parse numerically and round-trip canonically; do not sort the string.

### Example 2

**Situation.** A record occupies `[1000,1320)`. The durable frontier is 1319.

**Reasoning.** The prefix `[0,1319)` does not cover byte 1319 and certainly not the complete record. Even interpreting 1319 as last durable byte, the required end frontier is 1320.

**Conclusion.** Release the record's waiter only when the endpoint convention proves `flush>=1320`.

### Example 3

**Situation.** Reservations are `[0,100)`, `[100,180)`, and `[180,260)`. First and third records finish; the second stalls.

**Reasoning.** Published state must be parseable from zero. The third record cannot join the prefix across the hole even though its bytes are complete.

**Conclusion.** `published=100`; completion tracking waits, helps, or safely cancels/fills the second range under an explicit protocol.

### Example 4

**Situation.** Positions 97,500,059,720 and 97,525,956,864 use 16 MiB segments.

**Reasoning.** `divmod` yields segment/offset `(5811,7,657,544)` and `(5813,256)`; distance is 25,897,144 bytes. Crossing two segment numbers does not mean two full segments of payload remain because both endpoints are interior.

**Conclusion.** Compute from exact offsets and configured segment size, not filenames or segment-count intuition.

### Example 5

**Situation.** Primary history A and promoted history B both report numeric LSN 5000, then each appends different records.

**Reasoning.** They share an ancestor only through the fork. The equal number after divergence can identify different bytes and transaction outcomes.

**Conclusion.** Require system ID plus history ancestry; equality of offsets is not equality of state.

### Example 6

**Situation.** Sender flush is 900 MiB, replica receive is 850 MiB, replay is 700 MiB.

**Reasoning.** Transport/durable receive lag is 50 MiB; apply lag from sender is 200 MiB; local receive-to-replay backlog is 150 MiB. None supplies seconds without rate/timing evidence.

**Conclusion.** Report all frontiers and named gaps; “replica lag=200” is dimensionally incomplete.

### Example 7

**Situation.** A page passes checksum and identity validation with pageLSN 420; redo record 400 targets the same generation.

**Reasoning.** Under the stated physical recovery rule, the page already reflects at least the record and redo may skip it. If validation failed, the numeric comparison would not be trusted.

**Conclusion.** pageLSN is an idempotence guard after integrity and identity, not before.

### Example 8

**Situation.** Recovery needs 100, a replica 130, archive 90, backup 120, and decoder 80; current is 200.

**Reasoning.** The minimum required position is 80. Recycling to 90 because the archive advanced would delete decoder history. Retained distance is 120 units before segment rounding.

**Conclusion.** The decoder owns the recycle constraint until explicitly advanced or invalidated.

### Example 9

**Situation.** An LSN `9,007,199,254,740,993` (`2^53+1`) is sent as a JSON number to a double-based client.

**Reasoning.** IEEE-754 binary64 cannot represent every integer above `2^53`; the value may round to its neighbor, corrupting equality, difference, and file mapping.

**Conclusion.** Serialize exact large positions as validated strings or split integer fields with an explicit schema.

### Example 10

**Situation.** A 16-bit test logger has current 65,530 and new position 8 after rollover.

**Reasoning.** Raw comparison says 8 is older. Modular ordering can say it is 14 bytes ahead only if every live position is within less than half of 65,536 and history generation is controlled. Otherwise order is ambiguous.

**Conclusion.** Prefer explicit epoch plus offset; if modular comparison is used, prove and enforce its live-window assumption.

## Cross-Program Connections

- **Data Structures Engineering:** ring buffers, interval maps, ordered sets, heaps, and generation-tagged slots implement frontiers and retention efficiently.
- **Data Engineering:** offsets and watermarks resemble LSNs, but event time, processing time, consumer acknowledgement, and business completeness remain distinct.
- **Data Architecture Engineering:** backup lineage, restore targets, CDC contracts, retention, and sovereignty require position provenance and history graphs.
- **API and Service Engineering:** typed cursors, idempotency status, pagination tokens, and versioned opaque coordinates share the same namespace and compatibility concerns.
- **Platform Engineering:** storage sizing, metrics precision, failover orchestration, volume snapshots, and rollout determine whether positions remain usable operationally.
- **Concurrent Programming:** reservation, publication, atomic-width reads, memory barriers, and monotone wakeups are happens-before problems.
- **Functional Programming:** immutable history and algebraic data types support explicit `Start`, `End`, `Unknown`, and `DifferentHistory` cases.
- **Object-Oriented Programming:** value objects can enforce namespace, endpoint, width, and comparison invariants at API boundaries.
- **Security Engineering:** restore targets and WAL inspection are privileged inputs; parser bounds, provenance, least privilege, and audit prevent abuse.

## References

1. C. Mohan et al., “ARIES: A Transaction Recovery Method Supporting Fine-Granularity Locking and Partial Rollbacks Using Write-Ahead Logging,” *ACM TODS* 17(1), 1992. Primary LSN, pageLSN, transaction-chain, and recovery paper.
2. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_lsn` Type](https://www.postgresql.org/docs/18/datatype-pg-lsn.html), reviewed 2026-08-30. Official 64-bit representation, formatting, comparison, and difference semantics.
3. PostgreSQL Global Development Group, [PostgreSQL 18: System Administration Functions](https://www.postgresql.org/docs/18/functions-admin.html), reviewed 2026-08-30. Official insert, write, flush, receive, replay, file mapping, and LSN difference functions.
4. PostgreSQL Global Development Group, [PostgreSQL 18: WAL Internals](https://www.postgresql.org/docs/18/wal-internals.html), reviewed 2026-08-30. Official record/page/segment organization.
5. PostgreSQL Global Development Group, [PostgreSQL 18: `pg_replication_slots`](https://www.postgresql.org/docs/18/view-pg-replication-slots.html), reviewed 2026-08-30. Official restart, confirmed, status, and safe-capacity positions.
6. PostgreSQL Global Development Group, [PostgreSQL 18: Monitoring Database Activity](https://www.postgresql.org/docs/18/monitoring-stats.html), reviewed 2026-08-30. Official replication sender/receiver and WAL statistics frontiers.
7. PostgreSQL Global Development Group, [PostgreSQL 18: Backup Manifest WAL Range](https://www.postgresql.org/docs/18/backup-manifest-wal-ranges.html), reviewed 2026-08-30. Official timeline-bound start/end ranges.
8. PostgreSQL Global Development Group, [`xlogrecord.h`](https://github.com/postgres/postgres/blob/master/src/include/access/xlogrecord.h), source reviewed 2026-08-30. Current record length, previous pointer, resource manager, and CRC layout.
9. PostgreSQL Global Development Group, [`bufpage.h`](https://github.com/postgres/postgres/blob/master/src/include/storage/bufpage.h), source reviewed 2026-08-30. Current pageLSN representation and semantics.
10. Microsoft, [SQL Server Transaction Log Architecture and Management Guide](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-log-architecture-and-management-guide?view=sql-server-ver17), reviewed 2026-08-30. Official structured LSN, logical order, MinLSN, and circular log behavior.
11. Oracle, [MySQL 8.4: `innodb_redo_log_files`](https://dev.mysql.com/doc/refman/8.4/en/performance-schema-innodb-redo-log-files-table.html), reviewed 2026-08-30. Official redo file start/end LSN metadata.
12. Oracle, [MySQL 8.4: InnoDB Checkpoints](https://dev.mysql.com/doc/refman/8.4/en/innodb-checkpoints.html), reviewed 2026-08-30. Official fuzzy checkpoint and recovery scan relationship.
13. SQLite Project, [WAL-Mode File Format](https://www.sqlite.org/walformat.html), reviewed 2026-08-30. Official frame, read-mark, salt, checksum, and checkpoint-sequence design.

## Exercises

### Exercise 1

Define the four components of a rigorous LSN value and explain why a bare integer cannot safely support every comparison.

### Exercise 2

For a 64-bit byte-position format `high/low`, parse `2/A0000100`, map it to 16 MiB segment and offset, then calculate the distance from `2/9FFFFF00`. State all compatibility assumptions.

### Exercise 3

Design a concurrent reservation/publication algorithm for three producers in which the middle producer stalls. Specify data structures, memory ordering, frontier advancement, cancellation or failure behavior, and waiter correctness.

### Exercise 4

Design an observability and retention model for one primary, two physical replicas, an archive, a backup, and two logical consumers. Distinguish byte/time/apply lag and calculate the recycle owner.

### Exercise 5

An unfamiliar engine uses 32-bit physical offsets in a circular log and is adding online promotion plus long-lived backup manifests. Propose a durable successor coordinate, migration, validation, canary, and rollback strategy.

## Answers to the Exercises

### Answer 1

Use `(namespace, history, offset, boundary_kind)`. Namespace identifies the database/cluster incarnation; history identifies a timeline, term, epoch, or generation; offset is the exact ordered address; boundary kind distinguishes record start, record end, durable frontier, checkpoint, and similar meanings. A bare integer loses provenance, so unrelated clusters, divergent promotions, or reused rings can produce equal or ordered-looking values for different state. It also permits start/end substitution, signed truncation, and invalid sentinel comparison. Safe operations validate compatibility first and return a typed incomparable/error result when the domain is not shared.

### Answer 2

`2/A0000100 = (2 << 32) + 0xA0000100 = 11,274,289,408`. With `S=16,777,216`, `divmod` gives segment 672 and offset 256. `2/9FFFFF00 = 11,274,288,896`, so the distance is 512 bytes. The calculation assumes both are exact unsigned 64-bit byte positions, in the same system and history, using the same encoding and endpoint convention, with the latter no earlier than the former as stated. It says nothing about time, transactions, durability, or record existence. Engine-native filename mapping may additionally incorporate timeline and engine-specific segment rules.

### Answer 3

Maintain an atomic reservation tail, immutable reservation descriptors `(start,end,owner,state)`, completion bits or an ordered completion queue, and a contiguous published frontier. Each producer atomically reserves a nonoverlapping interval, fully writes record bytes and integrity metadata, then release-publishes `complete`. A coordinator/acquiring producer scans from the current frontier and advances only across consecutive complete descriptors using compare-and-swap under a lock or proven lock-free protocol. The third producer may complete, but the frontier stops before the stalled middle range. Flush reads only through published, and waiters wake only after the typed write/flush frontier covers their record end.

Cancellation cannot create an unparseable hole: a helper finishes the record, or the owner installs a valid padding/abort record under exclusive state transition, or the logger fails closed. Process death, timeout, and storage errors wake affected waiters with failure, not success. Tests delay each publication instruction and verify memory visibility, no overlap, no leap, monotonicity, fairness, width-atomic observation, and crash recovery of any persistent reservation metadata.

### Answer 4

Record for every actor: system/history, semantic frontier, exact byte position, observation time, last-advance time, rate, retained bytes, health, and owner. The primary exposes insert/write/flush. Each physical replica exposes receive-durable and replay/apply separately; calculate sender-flush minus receive and sender-flush minus replay. The archive exposes last continuously verified stored segment/end, not last attempted upload. The backup owns its required start until its manifest/data and ending WAL are complete and verified. Each logical consumer exposes restart and confirmed positions; restart governs retention, confirmed governs consumption progress.

Time lag comes from correlated commit/replay or event markers and stated clocks, not byte subtraction. Alert on stalled duration, byte growth, apply gap, archive RPO, and exhaustion forecast. The recycle owner is the actor with the minimum required compatible position after including crash-recovery/checkpoint and active-transaction obligations; round down to a safely reusable segment only after durable metadata. If a consumer is abandoned, explicitly invalidate it and record the service/RPO consequence before allowing recycle.

### Answer 5

Introduce a value object such as `(system_id, history_epoch, logical_u64_or_u128_offset, boundary_kind, format_version)`. Keep physical ring location derived as `(generation, offset mod ring_size)` and validate segment headers against expected generation. Promotion creates a child history with an ancestry/fork record; backup manifests store system ID, history ranges, start/end kinds, format version, and checksums. Never compare two positions without compatibility/ancestry logic.

Ship readers first: new binaries read legacy 32-bit manifests/records and the successor format, while writers remain legacy. Inventory every API, database column, JSON client, metric, backup, restore tool, replica, and offline recovery binary for exact width. Then dual-record or emit upgrade metadata at a durable gate, canary on a replica or bounded tenant, test wrap with reduced widths, promote/fork, restore across the fork, corrupt generations, exhaust the ring, and crash at every metadata transition. Enable new writers only when every retained recovery/rollback path understands them. Rollback before emission uses old writers; after emission it uses a retained compatible reader and a documented format gate, never an old binary that truncates or ignores the new coordinate.
