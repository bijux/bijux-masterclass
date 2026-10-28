---
module_id: DBE-022
program: Database Engineering
level: 1
module_number: 22
title: Record and Tuple Layout
status: complete
last_verified: 2026-08-30
---

# Record and Tuple Layout

## One-Page Review

### Governing question

How does a storage engine turn a typed logical row into bytes that can be located, decoded, updated, versioned, and recovered without confusing SQL values with one engine's physical representation?

### Essential definitions

A **row** is a logical mapping from attributes to SQL values; a **tuple** or **record** is one physical encoding of a row or index entry. A record normally combines a header, null information, fixed-width fields, variable-width metadata and payload, alignment padding, and possibly transaction/version fields. A **null bitmap** records absence without storing a value payload. An **offset** or **length directory** locates variable fields. **Overflow** or **out-of-line storage** replaces a large inline value with a reference to separately stored bytes. A **tuple identifier** locates a physical version, not necessarily a permanent business entity.

### Central model, mechanism, or theorem

Given schema metadata, start at the aligned end of the tuple header. For each non-null attribute in physical order, round the current offset up to its alignment, store either its fixed representation, length-prefixed variable representation, or overflow reference, and advance by the stored length. Null attributes consume a bitmap bit but ordinarily no data bytes. Decoding must use the same format version, schema/type metadata, byte order, alignment, null convention, and overflow rules. Every computed interval must remain inside the record and page before bytes are interpreted.

### Critical invariants

- Logical type, physical encoding, and in-memory representation are distinct contracts.
- Header length, attribute count, flags, null map, offsets, lengths, and record boundary agree.
- Every non-null field is properly aligned, in bounds, non-overlapping, and decoded with authoritative schema metadata.
- A null has no value bytes; an empty string or zero-length binary value is present and distinct.
- Variable-length metadata cannot overflow arithmetic, point backward illegally, or exceed the containing record.
- An overflow reference is validated before following it, and the referenced value is bounded and owned by the correct record/database.
- Transaction/version metadata is interpreted by the engine's visibility rules, not as application data.
- Format changes require version-aware readers or governed rewrites; raw bytes are not portable across engines.

### Common failures

Common failures include estimating row size from declared SQL widths; assuming columns are stored in query order or without padding; confusing characters with encoded bytes; treating null as zero length; trusting corrupt offsets before bounds checks; decoding with the wrong schema after evolution; assuming a physical tuple ID is stable; forgetting hidden/version columns and secondary-index key copies; fetching every overflow value eagerly; publishing vendor-specific offsets as universal; and changing row format without measuring cache density, write amplification, recovery, replica, and backup effects.

### Compact example

In the chapter's pedagogical format, a 24-byte header plus a one-byte null map rounds to a 32-byte data start. Values `int32`, `bool`, `int64`, five UTF-8 bytes, and a 140-byte value produce aligned field offsets 32, 36, 40, 48, and 60. The short text occupies nine bytes including its length header; the large value becomes a 16-byte overflow reference. Final 8-byte rounding yields an 80-byte tuple. If both variable fields were inline, the tuple would be 208 bytes; physical design changes page density and I/O, not logical SQL meaning.

### Connections

[DBE-021](021-pages-blocks-and-database-files.md) establishes the page and file container. [DBE-023](../ROADMAP.md) adds slot directories and stable within-page indirection; [DBE-030](../ROADMAP.md) later traces a row through all physical layers.

## Governing Question

SQL exposes named, typed attributes and declarative operations. A storage engine must instead answer byte-level questions: where a tuple begins, which attributes are null, how long each variable value is, what alignment a fixed value needs, whether a large value is inline, and which transaction may see this physical version. The bridge is a format contract shared by writers, readers, recovery, replication, backup, verification, and upgrade code.

There is no universal row format. PostgreSQL heap rows use a fixed header, optional null bitmap, aligned schema-driven attributes, and possibly TOASTed variable-length values. SQLite records carry a header of serial-type codes that determines payload sizes and storage classes. InnoDB index records use row-format-specific headers, null and variable-length metadata, hidden fields, and possibly off-page column data. The durable lesson is how to derive and validate a representation, not memorize offsets outside their engine and version.

## Why This Matters

Tuple width determines how many records fit on a page, and therefore buffer-pool reach, scan I/O, index fanout, logging volume, cache pressure, and replication bandwidth. A logical schema with many nullable or wide attributes can be cheap when values are absent or out of line, yet expensive when updates repeatedly cross inline/overflow thresholds. Character encoding can make a declared character count a poor byte estimate.

Correctness also depends on layout. A malformed length can drive an unsafe parser outside the page. A schema mismatch can reinterpret payload bytes as another type. A stale tuple identifier can name a reused slot or obsolete version. Recovery that restores payload without required header/version state can expose the wrong row. Storage inspection therefore begins with identity, version, schema, and bounds—not with convenient casting of raw bytes.

Physical layout is an operational interface even when undocumented to applications. Schema changes, row-format conversions, major upgrades, compression, encryption, backup tools, change-data capture, and forensic utilities all depend on it. Production engineering must separate supported logical interfaces from internal formats and validate every format-dependent tool against exact versions.

## Prerequisites and Retrieval

Retrieve primitive binary encodings; signed integers; byte order; UTF-8 and character-versus-byte length; memory alignment and padding; arrays and bitmaps; records and pointers; SQL types and null; schemas and catalogs; page layout; transactions and multi-version concurrency control; checksums; compression; and overflow chains.

Before proceeding, distinguish logical row from physical tuple; declared maximum width from actual encoded width; null from empty; fixed logical type from fixed physical representation; record header from page header; tuple location from application identity; inline bytes from out-of-line ownership; transaction metadata from user columns; and parser acceptance from semantic validity.

## Learning Objectives

After this module, you should be able to:

1. derive a simplified tuple layout from header, null, alignment, and field rules;
2. explain fixed-width, variable-width, self-describing, and schema-driven encodings;
3. validate offsets and lengths with overflow-safe bounds checks;
4. distinguish null, empty, absent, defaulted, and dropped attributes;
5. explain inline, compressed, and out-of-line value trade-offs;
6. identify transaction, version, row, and index metadata stored beside user values;
7. estimate record density without treating estimates as observed storage;
8. reason about schema evolution and format-version compatibility;
9. design safe tuple inspection and corruption triage; and
10. evaluate row-layout decisions from measured workload evidence.

## Core Exposition

A logical row is an ordered value assignment under a schema. Physical storage may preserve schema order, use an engine-defined order, omit derivable values, add hidden fields, encode an index key instead of a table row, or store multiple row versions. “Column 3” is meaningful only with the catalog/schema snapshot and physical record kind used by the decoder.

A record header establishes how to interpret what follows. Depending on the engine and record kind, it can hold flags, header length, attribute count, null presence, transaction identifiers, visibility hints, a link to another version, row state, variable-length metadata, and record-chain information. The page already has its own header and slot/cell directory; neither should be mistaken for tuple metadata.

Header size can be fixed, variable, or a fixed prefix plus optional regions. Optional data avoids per-row costs when a feature is unused, but creates parsing branches. A trustworthy parser reads only a minimal fixed prefix, validates version and declared header length against the enclosing record, and only then accesses optional regions.

Null is an element of SQL semantics, not a zero-byte string. Many formats dedicate one bit per nullable or present attribute. Some use 1 for null; PostgreSQL's documented heap null bitmap uses 1 for not-null. A decoder must follow its exact convention. If no nulls occur, an engine may omit the bitmap and clear/set a header flag accordingly. Null attributes ordinarily consume no payload bytes, so later offsets depend on null state.

Fixed-width means the stored datum has a known byte length under one representation—for example, a four-byte integer—not that every SQL declaration or every engine uses the same format. Numeric/decimal, temporal, boolean, and character types have engine-specific encodings. In-memory executor representations may differ from on-disk representations due to endianness, pointer expansion, decompression, or vectorization.

Alignment places a datum at an offset divisible by a required power, commonly 1, 2, 4, or 8. For positive alignment `a`, `align(o,a)=ceil(o/a)*a`, equivalently `(o+a-1)//a*a` with checked arithmetic. Padding bytes between fields do not represent values. They still consume tuple space and must not be assumed initialized or stable unless the format says so.

Variable-width values need a boundary. Common choices include a length prefix adjacent to the value, a header directory of serial types/lengths, end offsets, delimiter/escaping schemes, or a pointer to another object. The choice trades metadata, random field access, update cost, maximum length, and parser complexity. Length prefixes must specify whether the length includes the prefix and in what units.

Schema-driven formats can avoid repeating type identifiers in every row: the catalog supplies type length, alignment, storage policy, and decoder. This is compact but couples interpretation to the correct schema metadata. Self-describing records repeat type/size codes, easing heterogeneous values and some evolution at metadata cost. SQLite's serial types are a concrete self-describing example, though table meaning still depends on schema and record context.

PostgreSQL documents a heap tuple fixed header of 23 bytes on most machines, followed by an optional null bitmap and user data beginning at an aligned `t_hoff`. Attributes are visited in order using catalog values such as `attlen` and `attalign`; variable-length `varlena` values carry header/flag information and may be inline, compressed, or external. These are PostgreSQL 18 facts, not constants for other engines or future builds.

SQLite describes each record as a header followed by a body. The header contains its own length and one serial-type varint per value; each serial type determines storage class and body byte length. Integer encodings use different widths, text/blob lengths derive from the serial type, and body values follow header order. This compactness means a safe reader must validate varints, serial codes, cumulative lengths, text encoding, and enclosing cell payload.

InnoDB stores table rows as clustered-index records and secondary entries as index columns plus primary-key columns needed to locate clustered records. Its `COMPACT` family includes a fixed record header preceded by variable metadata, a null bit vector for nullable columns, and lengths for variable fields. Hidden row ID and transaction/rollback fields may exist depending on index and schema. Row format determines how long values move to overflow pages.

Large values force a policy choice. Keeping them inline gives locality when selected but reduces page density and makes unrelated scans carry more bytes. Moving them out of line leaves a compact reference and preserves density, but adds indirection, extra I/O, failure surfaces, and ownership/reclamation work. Compression may avoid overflow but costs CPU and complicates corruption limits. Engines generally choose using value type, page constraints, storage policy, and row format rather than an application-controlled pointer.

An overflow reference is not an ordinary process pointer. It is a persistent, engine-defined locator and metadata record. Validation must bound the referenced logical length, authenticate/check ownership where supported, detect cycles or excessive chains, limit allocation/decompression, and treat missing pages as corruption. Readers should avoid fetching out-of-line values when a query does not need them.

Tuple headers may carry concurrency state. PostgreSQL heap versions include inserting/deleting transaction identifiers and a tuple link; InnoDB clustered records include transaction and rollback information. These fields participate in visibility and recovery. A hex dump cannot decide whether a tuple is visible without transaction status, snapshot, undo/log, and engine rules. “Present on disk” does not imply “returned by SQL.”

Updates can be in-place, create a new row version, move a record, or change overflow representation. The logical primary key may stay constant while physical location changes. A physical tuple identifier is therefore a diagnostic or internal locator with engine-specific stability. Application references should use declared keys, not page/slot addresses.

Indexes have record layouts too. A clustered index can contain the complete row; a secondary record can repeat the primary key or a row locator. Null ordering, collation keys, prefix compression, included columns, and MVCC metadata affect physical size. Estimating table bytes while ignoring index-entry records—especially duplicated wide keys—can be dramatically wrong.

Record density is bounded by both tuple bytes and per-record page metadata. Under a simplified page with usable bytes `U`, slot bytes `S`, and fixed tuple bytes `T`, at most `floor(U/(S+T))` records fit. Real density also depends on fill factor, variable widths, free-space policy, dead versions, fragmentation, compression, page special space, and minimum/maximum inline payload. Treat the formula as a capacity bound, then measure actual distributions.

Column order can change padding in schema-ordered formats, but changing order solely to save a few bytes can damage clarity, compatibility, or access patterns and may require a rewrite. Some engines optimize or abstract layout. Measure with the actual engine/version and realistic null/width distribution. Never promise a byte saving from a source-language struct rule or another database's format.

Schema evolution is a reader/writer compatibility problem. Adding an attribute may permit old records to omit trailing bytes and synthesize a default; dropping a column may leave catalog or physical remnants until rewrite; changing a type can require reinterpretation or full conversion. Correct decoding needs the schema generation or engine rules that were valid for that record. Online DDL also needs concurrency, log, replica, backup, cancellation, and disk-headroom plans.

Checksums and encryption usually protect pages or storage units, not individual SQL values, and their coverage varies. A valid page checksum does not prove tuple offsets, type semantics, ownership, visibility, or schema match. Authenticated encryption validates its cryptographic envelope only under correct keys/nonces/associated data. Tuple validation remains necessary after integrity checks.

A safe tuple inspector accepts an immutable copy or supported engine interface; records engine/build, relation/index, page type, page and slot identity, schema/catalog snapshot, byte order, format version, checksum/encryption/compression state; validates the page first; then validates tuple header and every cumulative offset before decoding. It must cap lengths and recursion and preserve raw hashes plus structured output.

Corruption response prioritizes preservation. Stop unsafe mutation, capture exact errors and storage logs, protect original data/log/control/catalog files, work on verified copies, and use version-matched supported tools. One malformed tuple may indicate wider memory, device, filesystem, firmware, or software damage. Recover from known-good replicas/backups plus logs, then reconcile constraints and application invariants.

Operational evidence should include actual/percentile tuple widths, null fractions, inline/overflow rates, compression ratios, rows per page, page splits, dead/versioned bytes, update amplification, buffer misses, overflow fetch latency, index entry size, rewrite duration/space, replication lag, and backup/restore results. Sample distributions rather than relying only on averages; tail-width rows often govern failure and page-split behavior.

The following executable model is intentionally pedagogical. It models checked alignment, one null bit per nullable field, a four-byte variable-length header, a 16-byte overflow reference, and final 8-byte rounding. It is not PostgreSQL, SQLite, InnoDB, an ABI, a parser, or a recommended on-disk format.

<!-- bijux-verify: {"id":"bounded-tuple-layout","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"header_bytes=32\nnull_bitmap=0b00\nfields=(('id', 32, 4, 'inline'), ('active', 36, 1, 'inline'), ('balance', 40, 8, 'inline'), ('nickname', 48, 9, 'inline'), ('bio', 60, 16, 'overflow'))\ntuple_bytes=80\nlogical_value_bytes=158\noverflow=(('bio', 140, 16),)\nnull_case=(1, 64)\ninline_wide_tuple_bytes=208\npage_density=(97, 38)\ninvariants=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Field:
    name: str
    alignment: int
    fixed_bytes: int | None
    nullable: bool
    value_bytes: int | None


def align(offset: int, boundary: int) -> int:
    assert boundary > 0 and boundary & (boundary - 1) == 0
    return (offset + boundary - 1) // boundary * boundary


def layout(fields: tuple[Field, ...], overflow_limit: int) -> tuple:
    nullable_count = sum(field.nullable for field in fields)
    header = align(24 + (nullable_count + 7) // 8, 8)
    offset = header
    null_bitmap = 0
    placed = []
    overflow = []
    logical_bytes = 0
    nullable_index = 0
    for field in fields:
        bit = nullable_index
        nullable_index += field.nullable
        if field.value_bytes is None:
            assert field.nullable
            null_bitmap |= 1 << bit
            continue
        logical_bytes += field.fixed_bytes or field.value_bytes
        offset = align(offset, field.alignment)
        if field.fixed_bytes is not None:
            stored = field.fixed_bytes
            mode = "inline"
        elif field.value_bytes > overflow_limit:
            stored = 16
            mode = "overflow"
            overflow.append((field.name, field.value_bytes, stored))
        else:
            stored = 4 + field.value_bytes
            mode = "inline"
        placed.append((field.name, offset, stored, mode))
        offset += stored
    total = align(offset, 8)
    valid = total >= header and all(
        start >= header and start + size <= total for _, start, size, _ in placed
    )
    return header, null_bitmap, tuple(placed), total, logical_bytes, tuple(overflow), valid


row = (
    Field("id", 4, 4, False, 4),
    Field("active", 1, 1, False, 1),
    Field("balance", 8, 8, False, 8),
    Field("nickname", 4, None, True, 5),
    Field("bio", 4, None, True, 140),
)
normal = layout(row, overflow_limit=64)
null_row = row[:3] + (
    Field("nickname", 4, None, True, None),
    Field("bio", 4, None, True, 12),
)
null_case = layout(null_row, overflow_limit=64)
inline_wide = layout(row, overflow_limit=1024)
usable_page = 8192 - 24

print(f"header_bytes={normal[0]}")
print(f"null_bitmap=0b{normal[1]:02b}")
print(f"fields={normal[2]}")
print(f"tuple_bytes={normal[3]}")
print(f"logical_value_bytes={normal[4]}")
print(f"overflow={normal[5]}")
print(f"null_case={(null_case[1], null_case[3])}")
print(f"inline_wide_tuple_bytes={inline_wide[3]}")
print(f"page_density={(usable_page // (4 + normal[3]), usable_page // (4 + inline_wide[3]))}")
print(f"invariants={normal[6] and null_case[6] and inline_wide[6]}")
```

The exact output verifies only this finite model. It does not verify vendor offsets, overflow ownership, catalog interpretation, visibility, corruption recovery, or production density.

## Definitions and Notation

Let `H` be the fixed header bytes, `N` the number of nullable attributes, `B=ceil(N/8)` the model's bitmap bytes, and `A_h` the required data-start alignment. Then `D=align(H+B,A_h)` is the first possible datum offset. For each non-null attribute `i` in physical order:

- `a_i` is its required alignment;
- `o_i=align(e_(i-1),a_i)` is its start;
- `s_i` is its stored inline length or reference length;
- `e_i=o_i+s_i` is its exclusive end.

Null attributes set the format-defined bitmap state and do not advance the payload cursor. A tuple with record alignment `A_r` has `T=align(max(D,e_last),A_r)`. Validity requires checked arithmetic and `D<=o_i<=e_i<=T<=record_limit`, with no interval overlap except where a documented union overlays header fields. Logical value length, stored length, and external referenced length are separate quantities.

## Mechanisms, Invariants, or Proof Structure

A defensible tuple-layout derivation proceeds as follows:

1. Identify engine/build, relation or index kind, page type, row format, schema/catalog generation, and byte order.
2. Establish the enclosing page/slot/cell bounds before touching tuple bytes.
3. Read the minimal header prefix; validate flags, version, attribute count, and declared header length.
4. Determine whether null, variable-length, transaction, and optional metadata regions exist and bound each one.
5. Walk attributes under the authoritative physical order, type length, alignment, and storage policy.
6. For each field, perform checked alignment/addition before accessing bytes; distinguish null, inline, compressed, and external forms.
7. Validate external locators and cap chain length, decompression output, allocation, and recursion before retrieval.
8. Interpret transaction/version fields only through the engine's snapshot and recovery rules.
9. Cross-check decoded values with SQL-level queries, constraints, indexes, logs, replicas, and backups where safe.
10. Preserve byte hashes, tool/version/schema identity, limitations, and reproducible commands.

The simplified offset recurrence is proven by induction. `D` is aligned and inside the validated header boundary. Assuming the previous exclusive end is valid, checked `align` produces the smallest permitted start no earlier than that end. Checked addition yields the next exclusive end. Thus fields are ordered, aligned, and non-overlapping. The proof says nothing about whether schema metadata, bytes, visibility, or overflow targets are authentic; those are separate premises to verify.

## Alternatives and Trade-Offs

Schema-driven records reduce repeated metadata but demand the correct catalog. Self-describing records spend bytes on type/length codes but support heterogeneous values and some evolution more naturally. Fixed offsets make random access cheap but waste space for nulls and variable data; sequential parsing is compact but makes late-field access depend on earlier fields.

Inline values improve locality for selected columns but reduce density and amplify scans/updates. Out-of-line values keep primary pages compact but add pointer validation, I/O, caching, recovery, and reclamation. Compression trades CPU and bounded decompression risk for space/I/O. Prefix or dictionary compression can raise index fanout but complicates local decoding and damage containment.

Bitmaps are compact for many nullable fields; per-field tags can be simpler for sparse/self-describing records. Offset tables support direct variable-field access but grow with field count. Length prefixes are local and streamable but require walking. Stable logical row IDs add storage and an indirection contract; physical page/slot locators are smaller/faster internally but change as storage evolves.

## Failure Modes and Misconceptions

- “The SQL declaration is the byte width.” Encoding, headers, alignment, nulls, compression, versions, and overflow intervene.
- “Null and empty occupy the same representation.” Null is absence marked by metadata; empty is a present value.
- “Fields are packed with no gaps.” Alignment and row-format rules can insert padding.
- “A character is one byte.” Encoded byte length depends on character and encoding.
- “The record explains itself.” Schema-driven formats require exact catalog/type metadata; self-describing formats still need context.
- “A valid checksum makes offsets safe.” Page integrity and tuple semantic/bounds validation are separate.
- “An overflow pointer can be followed immediately.” Validate ownership, bounds, chain, allocation, and integrity first.
- “Tuple IDs are durable application IDs.” Updates, compaction, rewrite, vacuum, and recovery may change/reuse locations.
- “Rows and secondary-index entries cost the same.” Index records can repeat keys, locators, included columns, and metadata.
- “Average row size predicts capacity.” Tail widths, null distribution, versions, fragmentation, fill policy, and index amplification matter.

## Worked Examples

### Example 1

The model has a 24-byte fixed header and two nullable attributes. The bitmap needs `ceil(2/8)=1` byte, so the aligned data start is `align(25,8)=32`. Seven bytes are padding/unused header tail, demonstrating why adding field payload sizes alone underestimates a tuple.

### Example 2

Starting at 32, `id` occupies `[32,36)`, `active` `[36,37)`, and `balance` needs 8-byte alignment, so bytes `[37,40)` are padding and balance occupies `[40,48)`. The invariant is exclusive-end arithmetic: adjacent or padded intervals never overlap.

### Example 3

The five-byte nickname is stored as a four-byte length plus five payload bytes at `[48,57)`. The next 4-aligned field begins at 60, leaving three padding bytes. A decoder that treats the prefix as payload returns nine bytes of corrupted text; a decoder that forgets it starts the next field too early.

### Example 4

The 140-byte biography exceeds the model's 64-byte inline limit and becomes a 16-byte reference, producing an 80-byte tuple. Raising the threshold so it remains inline produces 208 bytes. On an 8168-byte usable page with four slot bytes per record, the simplified capacities are 97 versus 38 records; the real engine must be measured.

### Example 5

When nickname is null, bitmap bit zero is set and no nickname payload or alignment is consumed. A present 12-byte biography uses a four-byte length and 12 data bytes; the tuple ends at 64. An empty nickname would instead be present with a four-byte length prefix and must not decode as null.

### Example 6

A corrupt variable-length prefix claims 4 GiB while only 40 bytes remain. Safe code checks that the prefix is legal, computes the exclusive end without integer wraparound, and rejects it before allocation or read. Allocating first turns storage corruption into denial of service or memory unsafety.

### Example 7

A schema change adds a trailing column with a default, while old records contain fewer physical attributes. A version-aware engine may synthesize the value using catalog rules. A raw decoder that assumes every record has the newest physical field reads beyond the tuple and falsely reports corruption.

### Example 8

A heap update creates a new version at another slot and links concurrency metadata. The old bytes remain on disk until cleanup but may be invisible to the current snapshot. Counting recognizable payloads in a page is therefore not a valid SQL row count.

### Example 9

A wide natural primary key appears once in each clustered row and is copied into several secondary-index records in an InnoDB-style organization. Shortening only non-key columns barely changes total bytes. Capacity work must measure every index record and write/rebuild cost, not just base-row width.

### Example 10

An inspector sees an impossible offset after a checksum-clean page read. It records engine/build, object/page/slot, schema snapshot, raw hash, header, and failed bound; stops dereferencing; checks supported engine diagnostics and replicas/backups; and investigates software, memory, and storage paths. It does not rewrite the length or checksum on the only copy.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies bitmaps, packed records, offsets, indirection, and external-memory cost models.
- [Programming Languages — Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) supplies representations, alignment, checked arithmetic, parsing, and memory safety.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) explains byte order, alignment, caches, and machine representations.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies pages, files, memory mapping, I/O, and corruption containment.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) contributes hostile-input parsing, authenticated integrity, encryption, and forensic evidence handling.

## References

1. PostgreSQL Global Development Group, [Database Page Layout](https://www.postgresql.org/docs/18/storage-page-layout.html), PostgreSQL 18 heap tuple header and table-row layout documentation.
2. PostgreSQL Global Development Group, [TOAST](https://www.postgresql.org/docs/18/storage-toast.html), PostgreSQL 18 variable-length compression and out-of-line storage documentation.
3. PostgreSQL Global Development Group, [`pg_attribute`](https://www.postgresql.org/docs/18/catalog-pg-attribute.html), PostgreSQL 18 catalog fields for physical attribute length, alignment, storage, and compression.
4. SQLite Project, [Database File Format](https://www.sqlite.org/fileformat.html#record_format), record headers, serial types, payload, and overflow documentation for SQLite 3.
5. SQLite Project, [Datatypes in SQLite](https://www.sqlite.org/datatype3.html), storage classes, type affinity, and encoding documentation.
6. Oracle, [InnoDB Row Formats](https://dev.mysql.com/doc/refman/8.4/en/innodb-row-format.html), MySQL 8.4 compact headers, null metadata, hidden fields, and off-page values.
7. Oracle, [Data Type Storage Requirements](https://dev.mysql.com/doc/refman/8.4/en/storage-requirements.html), MySQL 8.4 type and engine storage requirements.
8. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, chapters on data storage and file organization.
9. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008, storage and record-layout foundations.

## Exercises

### Exercise 1

In the pedagogical format, use a 24-byte header, five nullable attributes, 8-byte data alignment, and fields `(int32 align4, int16 align2, int64 align8)`, all present. Derive bitmap bytes, data start, field intervals, final 8-aligned tuple size, and padding.

### Exercise 2

A record's validated boundary is `[100,180)`. Its header ends at 124, and three non-null variable fields claim lengths 8, 20, and 40 with 4-byte alignment. Derive their intervals and decide whether the record is valid. State the safe parser behavior.

### Exercise 3

Design a decoder-validation order for a schema-driven record containing a null bitmap, fixed and variable fields, a compressed value, and an overflow reference. Include hostile lengths and schema/version mismatch.

### Exercise 4

Compare inline and out-of-line storage for a workload that scans identifiers/status for every row but reads a 20 KiB document for 2% of rows and updates it frequently. Cover density, I/O, CPU/compression, logging, locality, reclamation, and failure handling.

### Exercise 5

Plan evidence for an online row-format/schema rewrite on a replicated production database. Include compatibility, capacity, workload baselines, correctness, cancellation, backup/restore, replicas, observability, security, and rollback/forward recovery.

## Answers to the Exercises

### Answer 1

Five nullable attributes require `ceil(5/8)=1` bitmap byte even though all are present. The data start is `align(24+1,8)=32`, giving seven header-tail padding bytes. `int32` occupies `[32,36)`, `int16` `[36,38)`, then two bytes pad to the 8-byte boundary and `int64` occupies `[40,48)`. Final tuple size is 48. Total padding beyond the 24-byte fixed header is nine bytes: seven before data and two before `int64`; the bitmap itself is metadata, not padding.

### Answer 2

The first field starts at `align(124,4)=124` and occupies `[124,132)`. The second occupies `[132,152)`. The third begins at `align(152,4)=152` and would occupy `[152,192)`, beyond the exclusive record end 180. The record is invalid. The parser must reject before reading or allocating the third field, record the failed bound and context, and avoid attempting recovery by truncating the claimed value.

### Answer 3

First authenticate identity: engine/build, record/page type, format version, relation/index, and matching schema generation. Validate the enclosing page, slot, and minimal record header before optional metadata. Bound header length, attribute count, bitmap bytes, and variable directory. For each attribute, consult authoritative physical type/alignment/storage metadata; inspect null state; perform checked alignment and addition; and validate the interval before access. Validate compression kind and cap compressed input, output, ratio, CPU, and nesting before decompression. Validate overflow locator kind, owner, logical length, target bounds/integrity, chain length, and cycle freedom before fetch. Reject unknown flags/types/versions and schema mismatch; preserve evidence rather than guessing.

### Answer 4

Keeping 20 KiB documents inline would sharply reduce primary-page density, make identifier/status scans read irrelevant bytes, enlarge dirty/log units, and increase split/fragmentation pressure. Out-of-line storage fits the 98% non-document path: primary records retain bounded references and document I/O occurs on demand. Costs are extra indirection and cache misses for the 2%, overflow allocation/reclamation, recovery ownership, and more complex damage handling. Compression can reduce I/O when documents compress well but consumes CPU and needs decompression bounds. Measure size distributions, scan bytes, overflow fetch latency, update/log amplification, cache hit behavior, garbage/reclamation, backup/restore, and corruption faults; choose engine-supported policy rather than application pointers.

### Answer 5

Record exact source/target engine versions, row formats, schema/catalog rules, page/checksum/encryption/compression modes, client and replica compatibility, and unsupported downgrade boundaries. Measure row/null/overflow/index size distributions, page density, update and read latency, log volume, replica lag, growth, rewrite throughput, lock time, and temporary plus rollback headroom. Rehearse on production-shaped copies with concurrent reads/writes, constraints, checksums, row counts, aggregates, application invariants, cancellation at critical points, crash recovery, and old/new reader coexistence. Take governed backups including logs and keys and prove isolated restore. Define throttling, pause/cancel semantics, replica rollout/failover, access control and evidence protection, alert thresholds, cutover fencing, rollback while compatible, and forward repair after the irreversible boundary.
