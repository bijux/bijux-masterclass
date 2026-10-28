---
module_id: DBE-030
program: Database Engineering
level: 1
module_number: 30
title: Tracing a Record from Logical Row to Persistent Bytes
status: complete
last_verified: 2026-08-30
---

# Tracing a Record from Logical Row to Persistent Bytes

## One-Page Review

### Governing question

What exact chain of contracts turns one typed logical row into addressable, recoverable persistent bytes—and reconstructs a transactionally visible row without confusing a teaching trace with any vendor's private format?

### Essential definitions

A **logical row** is a schema-interpreted tuple of values, not a byte string. A **tuple descriptor** supplies column order, types, lengths, alignment, nullability, collation, storage policy, and schema-version context. **Serialization** converts values into a canonical record representation with header, null/presence metadata, fixed/variable fields, alignment, and possibly overflow references. A **slot identifier** locates an item within a page; a **record identifier** combines page/block and slot. The **heap/access method** selects a page using free-space and placement policy. The **buffer manager** owns the mutable in-memory page. **WAL/writeback** orders recovery evidence before data persistence. A **physical address** resolves tablespace/database/relation incarnation/fork/segment/block/offset. A **checksum** validates covered bytes and trusted address context.

### Central model, mechanism, or theorem

The path is a composition of partial functions with proof obligations: SQL values are validated and normalized under a catalog snapshot; encoded under a declared tuple format; placed through an item directory without breaking page bounds; published through buffer identity, pin, latch, and dirty-generation protocols; described by recovery log; persisted only after WAL ordering; protected by integrity metadata; and resolved to the correct file offset/incarnation. Reading reverses the physical transformations but also applies snapshot visibility, schema interpretation, overflow reconstruction, decompression/decryption, and type decoding. Bytes alone do not identify their meaning.

### Critical invariants

- The schema/catalog version used to encode or decode is compatible with the row representation.
- Each non-null field has the required width, byte order, alignment, and bounds; null fields consume representation-defined metadata/space only.
- Tuple and overflow references belong to the same object incarnation and form bounded valid chains.
- Slot offset/length is within the page item region and does not overlap header, directory, free, special, or another live item.
- Page tag, relation/fork/block identity, buffer frame, record identifier, WAL pageLSN, and file address agree.
- No page image persists before WAL through its captured pageLSN is durable.
- Completion clears dirty only for the written generation; checksum covers the final stable image and trusted address context.
- Decoding never exposes a row version that fails physical validation, structural validation, or visibility rules.

### Common failures

Failures include assuming SQL text is stored; using application field order instead of catalog order; treating character count as byte count; omitting null bitmap/alignment/varlen headers; following corrupt overflow pointers; interpreting bytes with the current schema after incompatible evolution; assuming row ID is a permanent key; confusing logical table OID with physical file incarnation; deriving paths by hand across tablespaces/segments; writing a buffer before its WAL; hashing before final page mutation; clearing a re-dirtied page; reading cached bytes when intending media verification; and claiming one engine's heap layout applies to clustered-index or B-tree table storage.

### Compact example

An illustrative row `(42,"ada@example.org",12345,NULL)` is encoded under a declared four-column descriptor. An 8-byte tuple header carries format/null/transaction context; the integer occupies bytes 8–11, a 2-byte text length precedes 15 UTF-8 bytes, 3 zero alignment bytes lead to an 8-byte balance at offset 32, and NULL note has no payload. The 40-byte tuple is placed at offset 88 in a 128-byte page; a 4-byte slot at page offset 24 points to it. `lower=28`, `upper=88`, and free space is 60 bytes. Block 9 maps to byte offset 1,152 in segment 0. WAL through pageLSN 75 permits write, and an address-bound checksum plus decode verifies the trace.

### Connections

This chapter integrates [DBE-021](021-pages-blocks-and-database-files.md) through [DBE-029](029-checksums-and-page-corruption.md). It closes the storage/buffer block and prepares index, query execution, concurrency, logging/recovery, replication, and operations chapters. Data structures supplies directories/maps; programming languages supplies representation and ABI reasoning; operating systems supplies virtual/file/device I/O; security supplies validation and authenticated boundaries.

## Governing Question

The governing question is not “where is my row on disk?” as if there were one stable offset. It asks which version, access path, schema snapshot, engine, table access method, partition, relation incarnation, fork, page, slot, overflow objects, buffer state, log state, filesystem mapping, and recovery point make that question meaningful. Compaction, update/versioning, vacuum, clustering, online rewrite, partition movement, compression, encryption, and replication can change physical placement while logical identity remains.

An auditable trace therefore records transformations and evidence at each boundary. It does not open a live database file and guess. It uses supported catalogs/inspection tools, quiescent or transactionally defined observations, engine source/documentation for the exact version, safe copies for low-level parsing, and an explicit statement of what may change concurrently.

## Why This Matters

Abstraction is essential: applications should not depend on tuple headers or file offsets. But engineers diagnosing corruption, space amplification, write latency, cache behavior, row-size limits, overflow I/O, recovery, or forensic incidents must cross layers correctly. A wrong mental model leads to dangerous actions such as raw-copying a block, trusting a stale file path, or interpreting encrypted/compressed bytes as a heap tuple.

The trace also explains performance. A 15-byte string can require a length prefix and alignment; one logical row update can create a new version, index work, WAL, dirty pages, overflow changes, checksums, and later background I/O. Conversely, repeated logical updates can coalesce into fewer data-page writes while producing multiple log records. Logical operation count, buffer changes, log bytes, and storage I/O are different metrics.

Correctness depends on composition. A perfect serializer placed into the wrong relation block is corruption. A valid page written before its WAL violates recovery. A durable checksummed page can encode a logically invisible or inconsistent row. A structurally valid tuple decoded with the wrong collation/type/schema can yield wrong meaning. Every layer supplies assumptions consumed by the next.

## Prerequisites and Retrieval

Retrieve fixed pages/files/blocks and address arithmetic from [DBE-021](021-pages-blocks-and-database-files.md); tuple headers, nulls, alignment, and variable fields from [DBE-022](022-record-and-tuple-layout.md); directory stability from [DBE-023](023-slotted-pages.md); heap organization from [DBE-024](024-heap-files.md); placement summaries from [DBE-025](025-database-page-free-space-management.md); buffer lifecycle from [DBE-026](026-buffer-pools.md); replacement from [DBE-027](027-buffer-pool-page-replacement.md); WAL-ordered versioned writeback from [DBE-028](028-dirty-pages-and-writeback.md); and integrity boundaries from [DBE-029](029-checksums-and-page-corruption.md).

You should understand schemas/types, byte order, alignment, transactions/MVCC, latches, filesystems, WAL, checksums, compression/encryption, and failure domains. Before continuing, derive `segment=floor(block/blocks_per_segment)` and `offset=(block mod blocks_per_segment)*page_size`, and explain why that arithmetic still does not identify tablespace, relation incarnation, or fork.

## Learning Objectives

After completing this module, you should be able to:

1. narrate and audit the complete write and read paths for one row version;
2. distinguish logical values, catalog metadata, encoded tuple, page item, buffer, WAL, file address, and durable image;
3. compute field offsets, tuple size, slot/page bounds, free space, segment, and file offset under a declared format;
4. identify where nulls, alignment, varlen headers, overflow, MVCC, compression, encryption, and checksums enter;
5. explain why PostgreSQL heap, InnoDB clustered-index, and SQLite B-tree record paths differ;
6. locate concurrency/recovery/integrity proof obligations at layer boundaries;
7. design safe tracing instrumentation and low-level inspection procedures;
8. diagnose cross-layer failures without unsupported raw modification; and
9. state exactly what an executable miniature proves and omits.

## Core Exposition

Start with the statement and transaction context. Parsing produces a syntax tree; binding resolves relation/column identifiers under namespaces and privileges; planning chooses an operation; execution evaluates expressions, defaults, generated values, casts, domains, constraints, triggers, policies, and partition routing. The resulting datum vector is already more precise than the user's SQL text. Session encoding, collation, timezone, numeric semantics, and transaction snapshot can affect values or behavior.

The tuple descriptor is essential. It fixes physical attribute order and provides type identity, fixed/variable length, by-value/reference semantics, alignment, storage/compression policy, nullability, dropped/missing/generated-column behavior, and format/version information. In PostgreSQL, catalog fields such as `attlen` and `attalign` participate in heap attribute interpretation. A raw tuple is not self-describing enough to decode safely without compatible catalog metadata.

Serialization builds one row version. A fixed header commonly carries transaction/version/flags/navigation metadata. A null bitmap avoids storing absent payloads while preserving column positions. Fixed-width values use declared byte order and representation; variable-width values need length/type metadata. Alignment can insert padding that must be deterministic or excluded/initialized for integrity. Character length differs from encoded byte length. Numeric/decimal, timestamp, UUID, array, collation key, and user-defined types have format-specific rules.

Large values may be compressed or stored out of line. PostgreSQL TOAST can represent variable-length values inline, compressed, or external because heap tuples do not span pages. InnoDB row format and page pressure determine prefixes or off-page columns in overflow pages. SQLite B-tree cells store local payload and overflow remainder according to page formulas. The main record contains a reference/descriptor, not the logical value bytes, so reading may touch multiple pages and failure domains.

Placement asks the access method for a target. A heap can consult a free-space summary, validate the selected page under latch, and retry if stale. A clustered-index table descends a B-tree and may split pages; it is not a heap append. Partitioning/sharding may route before local placement. The record may be rejected for size, redirected to overflow, or cause compaction/split. Placement summaries are advisory; page-local bounds decide.

In a slotted page, directory entries grow from one boundary and items from another. The slot stores offset/length/state; `(block,slot)` can remain stable while compaction moves bytes inside the page. Stability is engine/protocol-specific: updates can create new versions and redirect/chain identifiers. A physical record identifier is not an application primary key and may be reused after lifecycle transitions.

The buffer manager fetches or creates the page through a complete tag: tablespace/database/relation incarnation/fork/block or the engine's equivalent. The caller pins it, acquires content protection, validates page/type/identity, modifies bytes and page metadata, emits/links recovery information, sets pageLSN, marks dirty generation, and releases protection. Publication ordering prevents another thread from seeing changed bytes with stale descriptor state.

Index maintenance, constraint effects, visibility maps, free-space maps, undo/version stores, and toast/overflow pages mean one logical row can change multiple pages. Their ordering and atomicity come from transaction/recovery protocols, not physical adjacency. A trace that follows only the heap page is deliberately incomplete for indexed, versioned, or overflowed data.

WAL decouples commit from data-page force in a no-force/steal engine. The captured page image cannot become persistent before durable WAL covers its pageLSN. Writeback may occur due to eviction, background cleaning, checkpoint, or administration. If the page is re-dirtied while an older image is in flight, only the captured generation is persisted; newer state remains dirty. Successful write completion and power-loss durability are separate storage contracts.

Before a final page image is written, integrity metadata is calculated over its specified canonical form and trusted context. Compression/encryption/checksum ordering must match the format. An address-bound checksum can detect some misdirected pages, but it does not prove logical consistency or recovery compatibility. Read verification must happen before unsafe offset interpretation.

Logical block mapping reaches files. A relation locator and fork choose an object; block number selects a segment and page offset. PostgreSQL documents main, free-space, visibility, and initialization forks plus segment files and tablespaces. File identifiers can change under rewrite operations while logical object identifiers remain. Use supported mapping functions for a running version; do not hard-code paths from an example.

The OS/filesystem maps file offset to cached pages/extents/device requests. Sparse allocation, copy-on-write, RAID, volume managers, encryption, compression, cloud virtualization, and device remapping mean “disk sector” is not derivable from database offset. A database page may be in database buffer, kernel cache, controller cache, and media at different versions. Persistence claims require the configured flush/barrier/failure contract.

The read path reverses only some operations. Resolve relation/access path and snapshot; fetch correct block into buffer; validate I/O length, checksum/authentication, page identity/version, and structural bounds; locate slot; check row-version visibility; reconstruct overflow/compression; decode attributes with compatible descriptor; apply missing/dropped column semantics; and produce logical datums. Index access may yield a primary-key/record locator and require heap/clustered fetch. Predicate/projection can avoid decoding every field.

PostgreSQL's documented heap page has a general header, four-byte item identifiers, free space, items, and optional special space; heap tuples have an MVCC header, optional null bitmap, aligned data, and possible TOAST representations. InnoDB documents complete rows in clustered-index records and primary-key suffixes in secondary indexes, with row-format-dependent off-page values. SQLite documents table B-tree leaf cells with rowid and record-format payload, serial types, and overflow. These comparisons reveal common obligations without inventing a common binary format.

Safe inspection starts with exact engine/build/version, page size, schema/catalog snapshot, object incarnation, tablespace/fork, transaction/recovery point, encryption/compression/checksum settings, and whether the observation comes from shared buffer, filesystem, snapshot, replica, or backup. Use official inspectors where possible. Copy a quiescent/consistent image before custom parsing; sandbox parser input; never mutate live files.

Instrumentation can correlate query/transaction ID, relation/partition, row/version ID, buffer tag/frame, page/slot, WAL begin/end/pageLSN/durable position, dirty/write generation, checksum result, file/segment/offset, I/O request/completion, and storage latency. Sampling/redaction is necessary: values and raw pages contain sensitive data, high-cardinality identifiers cost memory, and instrumentation changes timing.

The executable model below declares a deliberately small big-endian teaching format. It encodes one row, places it in one slotted page, calculates an address-bound digest, checks WAL eligibility and file arithmetic, then decodes the tuple. It is not PostgreSQL, InnoDB, SQLite, an MVCC engine, or a durable storage test.

<!-- bijux-verify: {"id":"row-to-page-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"logical=(42, 'ada@example.org', 12345, None)\nencoded_offsets=(('customer_id', 8, 4), ('email', 14, 15), ('balance_cents', 32, 8), ('note', None, 0))\ntuple_bytes=40\nslot=(offset=88,length=40)\npage_free=(lower=28,upper=88,bytes=60)\ntid=(block=9,slot=1)\nwal=(page_lsn=75,durable_lsn=75,write_allowed=True)\nfile=(segment=0,offset=1152)\nchecksum_valid=True\nround_trip=True\n","stderr":""}} -->
```python
import hashlib


PAGE_SIZE = 128
BLOCKS_PER_SEGMENT = 8_388_608
RELATION = "customer-main-incarnation-3"
BLOCK = 9
PAGE_LSN = 75
DURABLE_LSN = 75
logical = (42, "ada@example.org", 12_345, None)


email_bytes = logical[1].encode("utf-8")
tuple_header = b"R1" + bytes((0b00001000, 4)) + (51).to_bytes(4, "big")
customer_id = logical[0].to_bytes(4, "big")
email_length = len(email_bytes).to_bytes(2, "big")
before_balance = tuple_header + customer_id + email_length + email_bytes
padding = b"\x00" * ((8 - (len(before_balance) % 8)) % 8)
balance = logical[2].to_bytes(8, "big", signed=True)
encoded = before_balance + padding + balance
encoded_offsets = (
    ("customer_id", 8, 4),
    ("email", 14, len(email_bytes)),
    ("balance_cents", len(before_balance) + len(padding), 8),
    ("note", None, 0),
)

page_upper = PAGE_SIZE - len(encoded)
page_lower = 24 + 4
header = (
    b"PG01"
    + PAGE_LSN.to_bytes(8, "big")
    + page_lower.to_bytes(2, "big")
    + page_upper.to_bytes(2, "big")
    + b"\x00" * 8
)
slot = page_upper.to_bytes(2, "big") + len(encoded).to_bytes(2, "big")
page = bytearray(PAGE_SIZE)
page[0:24] = header
page[24:28] = slot
page[page_upper:PAGE_SIZE] = encoded


def page_digest(image: bytes) -> bytes:
    context = RELATION.encode("utf-8") + b"|" + str(BLOCK).encode("ascii") + b"|"
    checksum_zeroed = image[:16] + b"\x00\x00\x00\x00" + image[20:]
    return hashlib.sha256(context + checksum_zeroed).digest()[:4]


page[16:20] = page_digest(bytes(page))
checksum_valid = page[16:20] == page_digest(bytes(page))
stored_offset = int.from_bytes(page[24:26], "big")
stored_length = int.from_bytes(page[26:28], "big")
stored = bytes(page[stored_offset:stored_offset + stored_length])
identifier = int.from_bytes(stored[8:12], "big")
text_length = int.from_bytes(stored[12:14], "big")
email = stored[14:14 + text_length].decode("utf-8")
balance_offset = encoded_offsets[2][1]
stored_balance = int.from_bytes(stored[balance_offset:balance_offset + 8], "big", signed=True)
decoded = (identifier, email, stored_balance, None)
segment = BLOCK // BLOCKS_PER_SEGMENT
file_offset = (BLOCK % BLOCKS_PER_SEGMENT) * PAGE_SIZE

print(f"logical={logical}")
print(f"encoded_offsets={encoded_offsets}")
print(f"tuple_bytes={len(encoded)}")
print(f"slot=(offset={stored_offset},length={stored_length})")
print(f"page_free=(lower={page_lower},upper={page_upper},bytes={page_upper - page_lower})")
print(f"tid=(block={BLOCK},slot=1)")
print(f"wal=(page_lsn={PAGE_LSN},durable_lsn={DURABLE_LSN},write_allowed={DURABLE_LSN >= PAGE_LSN})")
print(f"file=(segment={segment},offset={file_offset})")
print(f"checksum_valid={checksum_valid}")
print(f"round_trip={decoded == logical}")
```

All offsets are relative to the teaching tuple or page as printed. `BLOCKS_PER_SEGMENT` is illustrative and produces segment 0 here; it is not a PostgreSQL runtime/build claim. The page digest's four stored bytes intentionally make collisions plausible and are not a production algorithm recommendation.

## Definitions and Notation

Let logical row under schema snapshot `S` be `R=(v_1,...,v_n)`. Tuple encoding is `E_S(R)=T`, a partial function because values, constraints, size, or format may reject. Placement `P(page,T)` yields a new page image and slot `s` if space/structure permit. Buffer tag `B=(tablespace,database,relation_incarnation,fork,block)` names the page.

Let captured page generation be `g`, page log position `L_p`, durable log position `L_w`, and address-bound integrity value `C(B,page)`. Data write requires `L_w>=L_p`; completion clears dirty only if identity/generation still match. Segment mapping for a fixed segment capacity `Q` blocks is `segment=floor(block/Q)` and `offset=(block mod Q)*page_size` within that segment.

Decoding `D_S(T)` may return a row only after physical/structural validity, compatible schema, overflow reconstruction, and visibility. `D_S(E_S(R))=R` is a round-trip property for values in the declared format domain; it does not establish transaction durability or query correctness.

## Mechanisms, Invariants, or Proof Structure

A defensible trace follows this order:

1. Record statement, transaction/snapshot, engine/version, schema/catalog descriptor, partition and access method.
2. Record evaluated typed values after defaults/casts/generated values/policies/triggers.
3. Encode a row version with exact null, length, alignment, MVCC, compression and overflow decisions.
4. Select and revalidate page free space; place item and update slot/header bounds atomically.
5. Record all companion page changes: indexes, overflow, free/visibility maps, undo/version stores.
6. Bind complete buffer identities, pins/latches, dirty generations, and pageLSNs.
7. Bind WAL/log evidence and require captured image LSN no greater than durable WAL before data persistence.
8. Finalize integrity/encryption/compression in the specified order and submit stable images.
9. Resolve relation incarnation/fork/block to segment/file offset through supported metadata.
10. On read, validate physical bytes and structure before visibility/decoding; prove round trip only within declared assumptions.

The composition proof is conditional at every arrow. Serialization preserves values only over its domain. Placement preserves tuple bytes only if page bounds/non-overlap hold. Buffer publication preserves identity only under concurrent protocol. Recovery preserves committed effects only under log assumptions. Storage preserves bytes only under durability/integrity assumptions. The end claim is no stronger than the weakest unverified premise.

## Alternatives and Trade-Offs

Heap storage gives flexible placement and stable slot indirection but needs separate indexes and cleanup. Clustered-index storage co-locates rows by key and accelerates ranges but makes key/order/page splits central. B-tree table storage combines key and record cells. Log-structured/columnar engines create different paths involving memtables, segments, row groups, dictionaries, and compaction.

Fixed-width encoding simplifies offsets but wastes space; variable/bit-packed formats save I/O/cache at CPU/branch complexity. Inline values reduce extra reads; overflow increases fit but adds indirection and lifecycle consistency. Compression saves bytes but changes random access, update cost, failure boundary, and checksum/encryption order.

Stable logical identifiers decouple applications from movement; physical identifiers aid engine access but can be invalidated/reused. Buffered I/O leverages OS caching; direct/asynchronous I/O increases control with alignment/queue complexity. Rich tracing accelerates diagnosis but adds overhead, sensitive data exposure, and timing perturbation.

## Failure Modes and Misconceptions

- “The database stores SQL rows as text.” It stores engine-specific typed binary representations and metadata.
- “Column order in my object is physical order.” The compatible catalog/descriptor governs.
- “VARCHAR(20) consumes 20 bytes.” Encoding, length header, actual value, alignment, compression, and overflow decide.
- “NULL is an empty value.” It is represented by null metadata and has different semantics.
- “One INSERT writes one page.” Indexes, overflow, maps, WAL, undo/version state, and splits may change too.
- “The TID is a permanent business identifier.” It is a physical/version locator under lifecycle rules.
- “Free-space map guarantees fit.” It is advisory; the latched page is authoritative.
- “Dirty means on disk soon.” Scheduling and WAL eligibility decide; commit/data force differ.
- “Write completion means durable.” The storage flush/failure contract determines that claim.
- “A valid checksum means a visible correct row.” Integrity, structure, recovery, visibility, and semantics differ.
- “File offset identifies a disk sector.” Filesystem/volume/device mappings intervene.
- “OID always equals filename.” Physical incarnation/filenode can change independently.
- “A raw page dump is self-describing.” Version, build, catalogs, encryption/compression, and context are required.
- “One engine trace generalizes.” Heap, clustered-index, B-tree, columnar, and log-structured paths differ.

## Worked Examples

### Example 1

The UTF-8 value `é` has one character but two bytes. A serializer using character count as byte length causes every following offset to shift and can make a valid logical row structurally corrupt. Encode first, then length the actual bytes.

### Example 2

Columns `(smallint,text,bigint)` cannot generally be located by summing declared widths. The text is variable and the bigint may need alignment padding. Sequential descriptor-driven decoding or stored offsets is required.

### Example 3

A large JSON value is externalized. The heap tuple contains an overflow descriptor; fetching the row touches heap plus overflow pages. The descriptor and chain must share object incarnation, bounds, ownership, and recovery consistency.

### Example 4

The free-space map says page 12 has 300 bytes, but a concurrent insert consumes them. Under the page latch only 80 remain, so a 120-byte tuple retries another page. The summary produced a candidate, not a reservation.

### Example 5

Compaction moves tuple bytes from offset 7000 to 6500 while slot 4 is updated. `(block 12,slot 4)` remains the locator under the protocol. A cached raw byte offset would become stale.

### Example 6

An UPDATE creates a new row version, modifies two indexes, changes free-space metadata, emits WAL, and dirties several pages. Commit may force log only; page writes occur later. “One row” spans transactional and physical objects.

### Example 7

A page with pageLSN 900 is selected for write while WAL is durable through 880. The physical offset is known and checksum can be calculated, but persistence is forbidden until WAL reaches 900. Address correctness does not satisfy recovery ordering.

### Example 8

`TRUNCATE` preserves a logical table identity but creates a new physical relation incarnation in an engine that uses filenode replacement. A completion or forensic path tied only to the old number can target stale storage. Generation/incarnation is part of identity.

### Example 9

An inspector reads a page already cached before a media fault. It verifies the cached image and incorrectly claims the device was scrubbed. Evidence must state the read path and force the intended layer when testing media.

### Example 10

PostgreSQL heap, InnoDB clustered-index, and SQLite table B-tree each store the same logical customer differently. A valid cross-engine migration compares logical values, constraints, ordering/collation, transaction point, and counts—not binary pages.

## Cross-Program Connections

- [Programming Languages — Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) supplies representation, alignment, endianness, and safe parsing.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies slotted arrays, maps, B-trees, chains, and invariants.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies virtual memory, page cache, filesystems, asynchronous I/O, and persistence.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache lines, alignment, byte order, ECC, DMA, and devices.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies input validation, encryption, authentication, sensitive evidence, and forensic boundaries.

## References

1. PostgreSQL Global Development Group, [Database Page Layout](https://www.postgresql.org/docs/current/storage-page-layout.html), current heap page, item identifier, tuple header, null, alignment, and attribute interpretation documentation.
2. PostgreSQL Global Development Group, [Database File Layout](https://www.postgresql.org/docs/current/storage-file-layout.html), current relation forks, filenodes, segments, tablespaces, and TOAST relation mapping.
3. PostgreSQL Global Development Group, [TOAST](https://www.postgresql.org/docs/current/storage-toast.html), current variable-length compression and out-of-line representation.
4. PostgreSQL Global Development Group, [pg_attribute](https://www.postgresql.org/docs/current/catalog-pg-attribute.html), current column descriptor metadata.
5. PostgreSQL Global Development Group, [pageinspect](https://www.postgresql.org/docs/current/pageinspect.html), supported low-level page inspection interfaces and fields.
6. PostgreSQL Global Development Group, [Buffer Manager README](https://github.com/postgres/postgres/blob/master/src/backend/storage/buffer/README), buffer identity, pins, content locks, I/O, replacement, and dirty-write source design.
7. Oracle, [InnoDB Row Formats](https://dev.mysql.com/doc/refman/8.4/en/innodb-row-format.html), current MySQL 8.4 clustered/secondary records and overflow behavior.
8. SQLite Project, [Database File Format](https://www.sqlite.org/fileformat.html), official pages, B-tree cells, record serial types, and overflow format.
9. C. Mohan et al., [ARIES](https://web.stanford.edu/class/cs345d-01/rl/aries.pdf), page-oriented write-ahead recovery foundations.
10. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, record, page, file, buffer, index, and recovery foundations.

## Exercises

### Exercise 1

Encode `(7,"naïve",NULL,9000000000)` under the chapter's teaching rules: 8-byte header, 4-byte ID, 2-byte UTF-8 length plus bytes, align the final 8-byte integer to 8, and no payload for NULL. Give offsets, padding, bitmap, and total size.

### Exercise 2

Place the Exercise 1 tuple in a 256-byte page with 24-byte header, two existing 4-byte slots, and `upper=180`. Determine new slot, tuple offset, lower/upper/free bounds, or reject it. State non-overlap checks.

### Exercise 3

Trace an UPDATE of a row with a large external value and two secondary indexes through transaction, tuple versions, heap/clustered page, overflow, indexes, free-space metadata, buffer, WAL, checksum, writeback, and visibility.

### Exercise 4

Design a safe diagnostic trace for a suspected wrong-row result. Include snapshot/schema, access path, cache/media distinction, physical integrity, structural checks, recovery/replica context, privacy, and non-destructive evidence.

### Exercise 5

Compare the trace for PostgreSQL heap, InnoDB clustered index, and SQLite table B-tree. Identify common contracts and nonportable layout assumptions, then define a logically valid migration verification plan.

## Answers to the Exercises

### Answer 1

`naïve` is six UTF-8 bytes (`ï` is two). Header bytes 0–7 carry format, bitmap, count, and transaction context; with the third column NULL, the teaching bitmap sets bit 2 (`0b00000100`). ID is offset 8 length 4. Text length is offsets 12–13 and text is offset 14 length 6, ending at 20. The final integer needs 8-byte alignment, so offsets 20–23 are four zero padding bytes and the integer is offset 24 length 8. NULL consumes no payload. Total tuple size is 32 bytes. This derives only the declared teaching format.

### Answer 2

Two existing slots make current lower `24+2*4=32`. Adding the third slot makes new lower 36. A 32-byte tuple allocated backward from existing upper 180 begins at 148, so new upper is 148 and contiguous free space is `148-36=112`. Accept only if existing live items are outside `[148,180)`, the current upper truly bounds the item area, slot count/header arithmetic is valid, no special space conflicts, and the page remains the same latched identity. The new slot stores `(148,32)`.

### Answer 3

Bind/update under one transaction/snapshot and compatible descriptor. Encode a new row version; decide inline prefix/external representation and update overflow ownership/chain. Place the new heap tuple or clustered record, link old/new version semantics, update both secondary indexes and any free/visibility summaries. Pin/latch every page under documented ordering; emit WAL/undo/redo for all atomic effects, set pageLSNs, and mark dirty generations. Commit durability follows the engine's log policy, not page force. Writeback captures each page, forces WAL through its pageLSN, finalizes checksum/encryption, and preserves re-dirty. Reads validate pages/chains and choose the visible version. Fault handling must not expose an index entry whose referenced version/overflow is unrecoverable.

### Answer 4

Capture exact query/parameters, transaction isolation/snapshot, schema/catalog/collation/type versions, plan/access path, engine/build/settings, object incarnation/partition, and result evidence with redaction. Reproduce on an isolated consistent snapshot. Compare index versus base-table path and run supported structural verification. Identify buffer tag/page/slot and whether bytes came from shared cache, filesystem cache, direct media, replica, or backup; use supported inspectors and immutable copies. Validate checksum/authentication, header/bounds, tuple/overflow, visibility and recovery LSN/timeline. Preserve raw evidence securely, stop propagation/destructive repair, compare independently verified recovery sources, and involve database/storage/security owners. A successful retry or one valid page does not close the incident.

### Answer 5

Common contracts are typed schema interpretation, deterministic encoding, bounded page/cell placement, stable-enough record navigation, complete physical identity, concurrency ownership, recovery ordering, integrity validation, and consistent decode/visibility. Nonportable assumptions include heap versus clustered organization, tuple/MVCC header, rowid/primary-key locator, null/serial types, slot/cell format, page size, overflow threshold/pointers, secondary-index payload, WAL/journal/undo, forks/files, checksums, compression, and encryption. Migrate at a defined transaction point using logical schema/type/collation mappings; validate constraints, generated/default semantics, row/value aggregates and targeted full comparisons, keys/order, large/binary/time/numeric/null edge cases, indexes, sequences/identities, and application queries. Perform restart/restore and rollback drills; never compare raw pages across engines.
