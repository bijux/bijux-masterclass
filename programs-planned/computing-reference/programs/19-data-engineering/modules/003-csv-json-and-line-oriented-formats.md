---
module_id: DE-003
program: Data Engineering
level: 1
module_number: 3
title: CSV, JSON, and Line-Oriented Formats
status: complete
last_verified: 2026-09-02
---

# CSV, JSON, and Line-Oriented Formats

## One-Page Review

### Governing question

How should a data engineer define, parse, validate, stream and reproduce text-encoded records when CSV dialects, JSON values and line-oriented framing have different rules and failure boundaries?

### Essential definitions

- A **text format contract** defines byte encoding, media type, compression, framing, grammar, schema, null semantics, limits, ordering and error policy.
- A **record boundary** identifies where one logical observation ends; a physical line is a record only when the format contract makes it so.
- A **CSV dialect** specifies delimiter, quote, quote escaping, line termination, header presence and related parsing behavior.
- A **CSV field** is an escaped or unescaped text token; apparent numeric or timestamp type is external metadata or inference.
- A **JSON text** is a serialized JSON value under the JSON grammar; it can represent an object, array, string, number, Boolean or null.
- **JSON Lines** or newline-delimited JSON uses one valid JSON value per line under a declared newline and blank-line policy.
- A **JSON text sequence** uses the ASCII record-separator byte before each JSON text and a line feed after it, providing explicit framing distinct from JSON Lines.
- **null**, **missing**, **empty string** and **empty collection** are separate states unless a boundary contract deliberately maps them.
- **semantic round trip** means decode followed by encode and decode preserves the declared data meaning; byte equality is a different property.
- A **quarantine record** preserves invalid input, provenance and error evidence outside accepted output for governed diagnosis and replay.

### Central model, mechanism, or theorem

Treat interchange as a composition

$$
bytes\xrightarrow{decode_E}text\xrightarrow{frame_F}records\xrightarrow{parse_G}values\xrightarrow{validate_S}accepted\cup quarantined,
$$

where encoding $E$, framing $F$, grammar or dialect $G$ and schema/semantic contract $S$ are independently versioned. Correct parsing at $G$ cannot prove encoding, record identity or domain validity. For accepted value $v$, semantic round-trip evidence requires $decode(encode(v))\equiv_S v$ under the declared equivalence, not merely that a parser returned something.

### Critical invariants

- Raw bytes are decoded with an explicit encoding and error policy before characters are parsed; replacement characters cannot silently become valid data.
- Record framing follows the chosen format: quoted newlines remain inside CSV fields, JSON Lines admits one JSON value per line, and JSON text sequences use record separators.
- CSV dialect, header mapping, column count, schema, null markers and formula-handling policy are explicit; guessing is quarantined or bounded.
- JSON duplicate-member policy, numeric range/precision, Unicode handling, top-level shape and missing/null semantics are declared and tested across consumers.
- Parsing is resource-bounded and preserves provenance, raw evidence and stable error classification; one malformed record cannot silently shift later boundaries.
- Serialization is deterministic where hashing or replay requires it, and round trips are tested against semantic rather than display equality.

### Common failures

Splitting CSV on commas; counting CSV lines as records; treating the first row as a header without contract; accepting ragged rows; mapping empty text to null everywhere; inferring identifiers as numbers; using locale-specific decimals; opening files with a default encoding; retaining a UTF-8 BOM in the first field; assuming JSON objects preserve semantic member order; accepting duplicate names differently across libraries; losing large integers through binary floating point; allowing NaN as JSON; pretty-printing JSON Lines; skipping malformed lines without evidence; splitting streams at arbitrary byte offsets; unbounded nesting or fields; spreadsheet formula injection; and treating successful parsing as trustworthy data.

### Compact example

A supplier labels a file `orders.csv`, but the contract additionally states UTF-8 without BOM, comma delimiter, CRLF or LF record endings, RFC-style double-quote escaping, header required, three columns, empty comment allowed but empty identifier forbidden, decimal point `.` and no spreadsheet formula prefixes. One comment contains an embedded newline, so a CSV parser yields two records from three physical data lines. A second feed uses JSON Lines: one compact UTF-8 JSON object per LF-terminated line, unique member names, integer identifiers represented as strings and blank lines rejected. The pipeline decodes strictly, parses with explicit modes, validates schemas, caps size and depth, writes invalid evidence to quarantine, and emits canonical accepted output with source digest, contract version and counts.

### Connections

[DE-001](001-data-producers-consumers-and-lifecycle.md) supplies producer, consumer and lifecycle boundaries. [DE-002](002-rows-columns-records-and-events.md) supplies grain, record and event meaning. DE-004 adds schema-aware binary serialization; later modules develop validation, partitioning, ingestion, lineage and trustworthy replay.

## Governing Question

Given bytes described as CSV, JSON or “one record per line,” what additional contract is needed to recover exactly the intended records and values, reject ambiguity safely, and reproduce the interpretation later?

The format name is only one layer. CSV has dialects and no intrinsic field types. JSON has a defined grammar and value model but does not supply domain schema, record stream framing or universal number behavior. A plain line format may be easy to process only if values cannot contain its separator.

Data engineering must make every hidden convention explicit: encoding, framing, grammar, schema and operational policy. Otherwise two individually reasonable consumers can derive different datasets from identical bytes.

## Why This Matters

Text formats sit at durable and organizational boundaries. Spreadsheets, exports, logs, APIs and object-store drops remain common because they are inspectable and widely supported. That reach also exposes every undocumented convention to many implementations.

Boundary errors compound. A comma inside a quoted address can shift columns; a newline inside a CSV field can corrupt parallel splits; one duplicate JSON member can be interpreted as first-wins or last-wins; a large integer can lose identity precision in a consumer.

Streaming needs real framing. A complete JSON document may contain arbitrary whitespace and nested values, so newline alone is not automatically a separator. JSON Lines restricts each record to one line. JSON text sequences use a control character to mark starts and permit recovery after damage.

Operational safety matters as much as grammar. Attackers or accidents can produce gigantic fields, extreme nesting, invalid encodings and spreadsheet formulas. Parsers require bounds, isolation and downstream-context controls.

Reproducibility requires preserving the contract and evidence. A parser-library upgrade, dialect change or null rule can alter results without altering source bytes. Digests alone prove byte identity, not stable meaning.

## Prerequisites and Retrieval

Retrieve sample and adversarial source bytes; producer/export configuration; content type and content encoding; character encoding and BOM policy; compression; record framing; CSV dialect and header policy; JSON profile and top-level shape; schema, grain and identity; field types, units, time zones and null markers; ordering and duplicate policy; maximum file, record, field, nesting and collection sizes; malformed-record policy; spreadsheet or downstream rendering contexts; expected counts and digests; consumer parser/library versions; historical contracts; privacy classification; quarantine access/retention; and replay requirements.

Distinguish bytes from characters; encoding error from parse error; newline from record; delimiter from field content; header from data; empty field from missing column; textual number from domain number; JSON syntax from schema; object member from ordered tuple; absent member from null; one JSON document from a stream; JSON Lines from JSON text sequences; pretty printing from canonicalization; parser acceptance from interoperability; syntactic validity from domain truth; skipping from quarantine; byte round trip from semantic round trip; and file suffix from media type and contract.

## Learning Objectives

After completing this module, you should be able to:

1. specify the byte, text, framing, grammar, schema and operational layers of a text data boundary;
2. parse RFC-style CSV fields, quotes and embedded line endings without naive splitting;
3. define CSV dialect, headers, ragged-row, null, type and spreadsheet-safety policies;
4. explain JSON values, member names, number interoperability, Unicode and null/missing behavior;
5. distinguish complete JSON, JSON Lines, concatenated JSON and JSON text sequences;
6. design bounded streaming, parallel splitting, checkpoint and recovery behavior;
7. quarantine malformed input with provenance instead of silently losing or shifting data;
8. validate syntax, structure and domain meaning as separate gates;
9. test semantic round trips and deterministic encodings across implementations; and
10. select CSV, JSON or a line-oriented format from data shape and operational requirements.

## Core Exposition

### Start with bytes

Files and messages arrive as bytes. Character parsing is meaningful only after choosing an encoding and error policy.

Prefer an explicit boundary contract such as UTF-8. Strict decoding exposes invalid sequences; replacement decoding can turn corruption into plausible text and break identifiers.

Record compression separately. A `.csv.gz` suffix is a hint, not a trustworthy or complete protocol.

### Govern the byte-order mark

UTF-8 has no byte-order ambiguity, though some producers emit the UTF-8 BOM as a signature. Some consumers remove it; others expose U+FEFF in the first header.

State whether a BOM is forbidden, allowed and stripped, or retained by another protocol. Test the exact first field.

Do not heuristically remove U+FEFF from arbitrary positions; it may be data or evidence of malformed concatenation.

### Separate framing from parsing

Framing finds candidate record byte/text regions. Parsing interprets a candidate according to grammar or dialect.

CSV framing requires quote state because line endings can appear inside escaped fields. JSON document framing requires grammar depth and string escape state unless an external protocol supplies boundaries.

The wrong framer can corrupt every later record even when individual fragments sometimes parse.

### Understand RFC-style CSV

RFC 4180 documents a common CSV form: records separated by CRLF, fields separated by commas, an optional header, optional double quoting, doubled quotes inside quoted fields and permitted embedded commas or line breaks when quoted.

It is an informational description, not proof that a source follows it. Real exports vary in delimiter, newline, quoting, escaping and whitespace.

Use it as a named baseline and declare deviations explicitly.

### Define a CSV dialect

At minimum record delimiter, field delimiter, quote character, doubled-quote or escape behavior, header presence and encoding.

Also decide whitespace, comments, blank records, trailing delimiters, ragged rows and NUL/control characters. Parser defaults differ.

Version the dialect with the dataset contract. Never infer and persist a guessed dialect as if the producer declared it.

### Parse CSV with a state machine

An unquoted comma ends a field; a comma inside a quoted field is data. Two quotes inside a quoted field represent one quote under RFC-style rules.

An unquoted record ending ends a record; one inside a quoted field is data. Therefore `splitlines()` and `split(',')` are not CSV parsers.

Use a maintained parser in an explicitly configured mode, then validate its output.

### Govern headers

Declare header presence. If present, validate count, encoding, names, duplicates, normalization and mapping to stable field identifiers.

Human labels can change while semantic field identity remains stable. Avoid position-only evolution without a schema version.

A BOM, invisible whitespace or duplicate column title can produce distinct dictionary keys or overwrite one value.

### Handle ragged records

Compare every parsed row’s field count with the declared schema. Extra and missing fields require an explicit policy.

Do not pad or truncate silently. Padding can turn structural corruption into nulls; truncation discards facts.

Quarantine the record and preserve its logical record number, physical span and raw bytes when policy permits.

### Add types outside CSV

CSV fields are text. Boolean, integer, decimal, date, instant, unit, identifier and null semantics come from metadata or contract.

Avoid broad inference for durable ingestion. `00123` may be an identifier, `1-2` may be a code, and locale changes decimal interpretation.

Parse into exact domain types with range, precision, unit and time-zone rules after structural validation.

### Define null and empty

An empty CSV field is text of length zero at syntax level. A boundary may map it to null, but that destroys the ability to represent empty text unless another marker exists.

Declare per-field null markers and escaping. Ensure a literal equal to the marker remains representable.

Differentiate absent trailing fields from present empty fields; ragged input is not automatically null.

### Prevent spreadsheet injection

CSV opened in spreadsheet software can interpret leading characters as formulas. Valid CSV syntax does not make untrusted cell content safe for that consumer.

Define export and presentation policy based on destination. Preserve raw domain data separately from escaped display exports.

Do not claim universal safety from prefixing alone; spreadsheet behaviors and downstream transformations differ.

### Understand the JSON data model

JSON values are objects, arrays, numbers, strings, `true`, `false` and `null`. A JSON text serializes one value.

JSON object member names are strings. The model does not provide schema, identity, units, timestamp semantics or reference integrity.

A top-level array or scalar can be valid JSON even if a local API requires an object.

### Enforce JSON grammar

JSON strings use double quotes and defined escapes. Comments, single-quoted strings and trailing commas are not JSON grammar.

JSON numbers do not include NaN or infinities. Leading zeros and incomplete exponent forms are invalid.

Reject extensions at boundaries unless a separately named profile explicitly permits and normalizes them.

### Handle duplicate object names

JSON grammar permits object syntax whose names need not be unique, but behavior across implementations is unpredictable: consumers may report last, first, all or fail.

Require unique names for interoperable ingestion and configure a parser hook or pre-validation to detect duplicates.

Never rely on member order or duplicate order to encode repeated facts; use an array with explicit identity.

### Preserve numeric meaning

JSON’s grammar allows arbitrary-length decimal digit sequences, while implementations use different numeric ranges and precision.

Interoperable profiles often constrain integers to exactly representable ranges. Large identifiers should usually be strings, not arithmetic values.

Parse money and precise measurements into decimal or integer minor units under schema. Round-trip across every important consumer.

### Handle Unicode correctly

JSON exchanged across systems is normally UTF-8. Escape sequences and literal characters can denote the same Unicode string.

Unicode equality, normalization and visual similarity are separate from parser equality. Apply normalization only under domain policy.

Reject or govern unpaired surrogate escapes and control characters according to the required interoperability profile.

### Separate missing and null in JSON

An absent object member differs from a member with value `null`. Empty string, empty array and empty object are values.

Schema and evolution policy decide whether absence means default, unknown, not applicable or old producer.

Do not recursively delete nulls to “clean” data; that changes the information model.

### Distinguish order guarantees

Array order is part of the JSON value. Object member order should not carry domain semantics.

Parsers may preserve insertion order for convenience, but interoperable equality treats an object as name/value associations under the profile.

For deterministic hashing, define a canonical serialization or hash a normalized typed model—not incidental pretty output.

### Frame JSON Lines

JSON Lines convention uses UTF-8, one valid JSON value per line and line terminators; a BOM is forbidden by the convention and JSON rules.

Because each value occupies one line, embedded newlines in strings must be escaped. Pretty-printed multi-line objects violate the framing.

Declare whether blank lines are invalid, skipped or meaningful. JSON `null` is a value; a blank line is not.

### Understand JSON text sequences

RFC 7464 defines a sequence using ASCII record separator `0x1E` before each JSON text and LF after. This makes record starts explicit.

The format can continue after an incomplete or invalid element under its processing model. Producers must still emit valid elements.

It differs from JSON Lines and cannot be selected merely by a `.jsonl` suffix.

### Treat plain line formats deliberately

TSV, key-value logs and custom line protocols need escaping or restrictions for tabs, newlines, backslashes and control bytes.

If a value can contain the separator without a reversible escape, the format is ambiguous.

Write a grammar and property tests. “It looks readable” is not a framing specification.

### Design bounded streaming

Stream decoders and parsers to bound memory, but impose maximum record, field, string, nesting and collection sizes.

For JSON Lines, a line can still be arbitrarily large. For CSV, an embedded-newline field can span many physical lines.

Track byte and logical record offsets, source identity and digest so errors can be reproduced.

### Split safely for parallel work

JSON Lines can split on confirmed line boundaries outside corrupt oversized records. CSV cannot generally split on arbitrary newlines without quote-state knowledge.

Compressed streams may not support arbitrary seeking. Use splittable containers, indexed boundaries or upstream partitions when scale requires it.

Validate partition concatenation against a single-parser baseline before trusting distributed ingestion.

### Checkpoint and resume

A checkpoint identifies immutable source version, parser/contract version, safe record boundary and accepted/quarantined counts.

Byte offsets become invalid if the object changes, encoding normalization occurs or decompression state is missing.

Use idempotent record identity and atomic publication so retry does not duplicate accepted facts.

### Quarantine with evidence

Classify decode, framing, syntax, structure, type and domain errors separately. Preserve raw bytes only under security and privacy policy.

Record source, digest, byte span, logical position, contract version and stable error code. Redact secrets from broad operational views.

Never silently skip malformed input when completeness matters. Quarantine is a governed state, not a forgotten directory.

### Validate in layers

First validate decoding and framing, then grammar/dialect, structure/schema, field types, domain constraints and cross-record invariants.

Successful syntax does not establish truthful timestamps, authorized identity or referential integrity.

Report counts at every layer so accepted plus rejected reconciles to framed input.

### Serialize deliberately

For CSV, use the exact dialect and write through a library that quotes delimiters, quotes and line endings. Preserve column order and null mappings.

For JSON, choose compact or human-readable output, Unicode escaping, number rendering and ordering under the contract. Reject non-finite numbers.

Atomic writes and checksums protect publication. Neither makes semantics correct without validation.

### Test round trips and consumers

Build fixtures for delimiters, quotes, CRLF/LF, embedded newlines, BOM, non-ASCII, empty/null/missing, duplicate names, numeric boundaries and malformed truncation.

Test producer-to-every-critical-consumer paths, not only a library against itself. Same-library round trips can share one defect or extension.

Compare typed semantic values, field identities and record counts; compare bytes only when canonical encoding is promised.

### Choose the format by evidence

CSV fits flat, schema-aligned tables and broad spreadsheet/tool exchange when dialect and metadata are controlled.

JSON fits nested heterogeneous values and web/tool ecosystems, but complete documents are poor append streams without external framing.

JSON Lines fits independently processable one-line JSON records. Use schema-aware formats when evolution, types, compactness or cross-language guarantees exceed text conventions.

## Definitions and Notation

Let source bytes be $B$, encoding $E$, framing rule $F$, grammar/dialect $G$ and semantic schema $S$. The ingestion composition is

$$
I_{E,F,G,S}(B)=validate_S(parse_G(frame_F(decode_E(B)))).
$$

Let framed record $r_i$ have source byte span $[a_i,b_i)$, logical index $i$, raw digest $h_i$ and outcome $o_i\in\{accepted,quarantined\}$. Reconciliation for a fixed immutable source requires every framed record receive exactly one outcome, while source-level failure before framing is reported separately.

For typed value $v$, encoder $enc$ and decoder $dec$, semantic round trip is $dec(enc(v))\equiv_S v$. Byte canonicality additionally requires $enc(dec(x))=x$ for already canonical $x$, a stronger and often unnecessary property.

## Mechanisms, Invariants, or Proof Structure

### Twelve-step text-ingestion mechanism

1. Identify immutable source, content encoding, compression, media type and contract version.
2. Decode bytes strictly under the declared character encoding and BOM policy.
3. Frame records using CSV quote state, JSON document grammar or declared line protocol.
4. Parse using an explicit CSV dialect or standards-conforming JSON profile.
5. Validate header, shape, duplicate names, field count and top-level requirements.
6. Convert types with declared null, numeric, time, unit and Unicode semantics.
7. Apply domain and cross-record constraints while preserving record identity.
8. Bound resource consumption and isolate malicious or malformed inputs.
9. Reconcile accepted and quarantined evidence with stable error classification.
10. Serialize accepted data deterministically where replay or hashing requires it.
11. Test semantic round trips and every critical producer-consumer combination.
12. Publish counts, digests, contract/parser versions, lineage and limitations atomically.

### Encoding invariant

Every accepted character derives from a declared byte encoding without silent replacement, and BOM handling follows the boundary contract.

### Framing invariant

Each logical record has one unambiguous boundary under its format; embedded delimiters and newlines cannot shift neighboring record identity.

### Structure invariant

CSV rows map to the declared header and field count; JSON values meet top-level and unique-member policy before type/domain conversion.

### Semantic invariant

Null, missing, empty, numeric precision, units, time and identifiers preserve their declared meaning across parse and serialization.

### Reconciliation invariant

Every successfully framed input record is accepted exactly once or quarantined exactly once with provenance; nothing is silently skipped or duplicated.

### Resource-safety invariant

File, record, field, string, nesting, collection and error volumes have enforced bounds, and downstream formula or rendering contexts receive separate controls.

### Proof sketch: a file extension cannot determine a unique interpretation

Construct two valid producer contracts for bytes named `data.csv`: one uses comma, header and UTF-8; the other uses semicolon, no header and a legacy encoding. The suffix is identical while records and characters differ. Therefore a file extension alone cannot determine interpretation; encoding, dialect/framing and schema evidence are necessary.

### Executable format audit

The synthetic audit parses RFC-style CSV with an embedded newline, a JSON object and two JSON Lines records, then checks a JSON semantic round trip. It illustrates library behavior under explicit inputs, not universal dialect or interoperability proof.

<!-- bijux-verify: {"id":"text-format-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"csv_records=2\ncsv_note_lines=2\njson_keys=3\njson_integer_exact=True\njsonl_records=2\njsonl_ids=1,2\nround_trip=True\n"}} -->
```python
csv_text = 'id,note\r\n1,"first line\nsecond line"\r\n2,"said ""ok"""\r\n'


def parse_csv(text):
    records, record, field = [], [], []
    quoted, index = False, 0
    while index < len(text):
        char = text[index]
        if quoted:
            if char == '"' and index + 1 < len(text) and text[index + 1] == '"':
                field.append('"')
                index += 1
            elif char == '"':
                quoted = False
            else:
                field.append(char)
        elif char == '"' and not field:
            quoted = True
        elif char == ',':
            record.append(''.join(field))
            field = []
        elif char in ('\r', '\n'):
            if char == '\r' and index + 1 < len(text) and text[index + 1] == '\n':
                index += 1
            record.append(''.join(field))
            records.append(record)
            record, field = [], []
        else:
            field.append(char)
        index += 1
    if quoted:
        raise ValueError("unterminated CSV quote")
    if field or record:
        record.append(''.join(field))
        records.append(record)
    return records


def parse_json(text):
    index = 0

    def skip_space():
        nonlocal index
        while index < len(text) and text[index].isspace():
            index += 1

    def value():
        nonlocal index
        skip_space()
        if index >= len(text):
            raise ValueError("missing JSON value")
        if text[index] == '"':
            index += 1
            characters = []
            while index < len(text) and text[index] != '"':
                if text[index] == '\\':
                    index += 1
                    escapes = {'"': '"', '\\': '\\', 'n': '\n', 'r': '\r', 't': '\t'}
                    if index >= len(text) or text[index] not in escapes:
                        raise ValueError("unsupported JSON escape")
                    characters.append(escapes[text[index]])
                else:
                    characters.append(text[index])
                index += 1
            if index >= len(text):
                raise ValueError("unterminated JSON string")
            index += 1
            return ''.join(characters)
        if text[index] == '{':
            index += 1
            result = {}
            skip_space()
            while index < len(text) and text[index] != '}':
                key = value()
                skip_space()
                if index >= len(text) or text[index] != ':':
                    raise ValueError("missing JSON name separator")
                index += 1
                result[key] = value()
                skip_space()
                if index < len(text) and text[index] == ',':
                    index += 1
                    skip_space()
                elif index >= len(text) or text[index] != '}':
                    raise ValueError("missing JSON value separator")
            if index >= len(text):
                raise ValueError("unterminated JSON object")
            index += 1
            return result
        for token, parsed in (("true", True), ("false", False), ("null", None)):
            if text[index:index + len(token)] == token:
                index += len(token)
                return parsed
        start = index
        if text[index] == '-':
            index += 1
        while index < len(text) and text[index].isdigit():
            index += 1
        if start == index:
            raise ValueError("unsupported JSON value")
        return int(text[start:index])

    parsed = value()
    skip_space()
    if index != len(text):
        raise ValueError("trailing JSON data")
    return parsed


csv_matrix = parse_csv(csv_text)
header, csv_values = csv_matrix[0], csv_matrix[1:]
csv_rows = [dict(zip(header, values)) for values in csv_values]
document = parse_json('{"id":"001","count":9007199254740991,"active":true}')
jsonl = '{"id":1,"value":"alpha"}\n{"id":2,"value":"beta"}\n'
line_values = [parse_json(line) for line in jsonl.splitlines()]
encoded = '{"active":true,"count":9007199254740991,"id":"001"}'

print(f"csv_records={len(csv_rows)}")
print(f"csv_note_lines={len(csv_rows[0]['note'].splitlines())}")
print(f"json_keys={len(document)}")
print(f"json_integer_exact={document['count'] == 9007199254740991}")
print(f"jsonl_records={len(line_values)}")
print(f"jsonl_ids={','.join(str(value['id']) for value in line_values)}")
print(f"round_trip={parse_json(encoded) == document}")
```

### Verification strategy

Inspect raw bytes and media metadata; test strict decoding and BOM cases; parse CSV fixtures with commas, quotes, embedded CR/LF and ragged rows; detect duplicate headers and JSON names; exercise numeric and Unicode boundaries across languages; compare full and partitioned parses; truncate every framing position; fuzz depth, length and escapes under resource limits; reconcile accepted/quarantined counts and byte spans; test spreadsheet exports in destination context; verify checkpoints against immutable source digests; and run cross-implementation semantic round trips rather than only same-library tests.

## Alternatives and Trade-Offs

1. CSV is compact and ubiquitous for flat tables but carries little intrinsic type or schema information.
2. JSON represents nesting naturally but repeats names and can obscure numeric interoperability.
3. JSON Lines streams independent values simply but forbids pretty multi-line records.
4. JSON text sequences provide explicit recovery framing but have weaker everyday tool support.
5. Strict rejection preserves contract clarity but can halt useful ingestion for one bad record.
6. Quarantine sustains throughput but adds governance, privacy and replay obligations.
7. Dialect inference helps exploratory access but can turn ambiguity into silent production interpretation.
8. Producer-declared dialects improve reproducibility but require coordination and versioning.
9. UTF-8 without BOM interoperates broadly but may confuse legacy spreadsheet workflows.
10. BOM-tolerant ingestion accepts common exports but needs exact first-field handling.
11. Empty-as-null is convenient but loses distinction from legitimate empty text.
12. Explicit null markers preserve meaning but need escaping when marker text is legitimate.
13. Numeric JSON values support arithmetic directly but expose cross-language range and precision differences.
14. String-encoded identifiers preserve digits but require schema-guided conversion where arithmetic is real.
15. Whole-document JSON supports one atomic value but impedes incremental append and partial recovery.
16. Line framing supports streaming and concatenation but needs record-size bounds and newline restrictions.
17. Canonical output enables stable hashes but costs processing and may discard source presentation.
18. Source-byte retention improves diagnosis but increases sensitive-data and retention risk.

## Failure Modes and Misconceptions

1. “CSV means split on comma” ignores quoting and dialects.
2. “One line is one CSV record” fails on embedded newlines.
3. “The first row is always a header” treats data as names.
4. “Every CSV row has the same width” must be validated, not assumed.
5. “Empty CSV means null” erases empty text.
6. “CSV types infer reliably” corrupts identifiers, decimals and dates.
7. “Whitespace is harmless” may be field data or dialect-specific.
8. “UTF-8 always has no BOM” confuses common practice with received bytes.
9. “Replacement decoding is robust” can silently change keys.
10. “Valid CSV is safe in spreadsheets” ignores formula interpretation.
11. “JSON is always an object” excludes valid top-level values.
12. “JSON supports comments” confuses extensions with the grammar.
13. “Trailing commas are portable” many conforming parsers reject them.
14. “NaN is JSON” non-finite values are outside JSON number grammar.
15. “JSON numbers have universal precision” implementations differ.
16. “Large numeric IDs are safe” floating consumers may round them.
17. “Object member order carries meaning” uses a nonportable model.
18. “Duplicate JSON names have obvious meaning” consumers disagree.
19. “Null and missing are equivalent” breaks evolution and domain meaning.
20. “Escaped and literal Unicode are different strings” confuses encoding with value.
21. “JSON is a streaming format” one JSON text has no multi-record framing.
22. “JSON Lines can be pretty printed” breaks one-value-per-line framing.
23. “Blank JSONL lines mean null” blank text is not JSON `null`.
24. “JSON Lines and JSON sequences are identical” their framing bytes differ.
25. “Any newline is a safe split point” fails for CSV and custom protocols.
26. “Streaming automatically bounds memory” one record may be enormous.
27. “Skipping bad records is resilient” destroys completeness evidence.
28. “A parser success proves schema” syntax is only one gate.
29. “Round trip means identical bytes” semantic and canonical properties differ.
30. “The extension defines the format” omits every essential boundary contract.

## Worked Examples

### Example 1

`"Smith, Ana",42` contains two CSV fields, not three. A configured parser preserves the comma inside quotes.

### Example 2

A comment field contains LF between opening and closing quotes. Physical line count exceeds logical record count, invalidating naive partitioning.

### Example 3

A UTF-8 BOM becomes part of `customer_id` in one consumer. The contract allows and strips it only at byte offset zero.

### Example 4

An empty CSV cell means empty display name, while `\N` means unknown. Per-field null policy preserves both values.

### Example 5

Identifier `00123` becomes integer 123 under inference. Schema-guided text parsing preserves its identity.

### Example 6

Two JSON consumers receive duplicate `status` names; one keeps first and one keeps last. Unique-name rejection removes the ambiguity.

### Example 7

A 20-digit JSON integer rounds in a floating-point consumer. The boundary changes the identifier to a validated decimal string.

### Example 8

Pretty-printed objects are appended to a `.jsonl` file. Line parsing fails because one record spans several lines; compact serialization repairs the producer.

### Example 9

A parallel CSV reader begins at an embedded field newline and invents a record. Quote-aware indexed boundaries replace arbitrary byte chunks.

### Example 10

One malformed JSONL line is quarantined with digest and offset. Accepted plus quarantined counts reconcile, allowing corrected replay without duplicating accepted IDs.

## Cross-Program Connections

- Programming Languages contributes lexical grammars, Unicode strings and parser state machines.
- Data Structures contributes buffers, streaming iterators, nesting and bounded resource use.
- Database Engineering contributes types, nulls, keys, constraints and bulk loading.
- API Engineering contributes media types, JSON profiles, compatibility and error contracts.
- Security Engineering contributes untrusted-input limits, injection controls and evidence handling.
- Distributed Systems contributes framing, partial delivery, retries, checkpoints and idempotence.
- Software Testing contributes fixtures, property tests, fuzzing and cross-implementation conformance.
- Data Governance contributes schema ownership, privacy, retention, quarantine and lineage.
- Observability contributes stable error taxonomies, counts and replay evidence.
- Systems Engineering contributes layered contracts, boundaries and failure containment.

## References

1. IETF. [RFC 4180: Common Format and MIME Type for Comma-Separated Values Files](https://www.rfc-editor.org/rfc/rfc4180.html). Retrieved 2026-09-02.
2. IETF. [RFC 7111: URI Fragment Identifiers for the text/csv Media Type](https://www.rfc-editor.org/rfc/rfc7111.html). Retrieved 2026-09-02.
3. W3C. [Model for Tabular Data and Metadata on the Web](https://www.w3.org/TR/tabular-data-model/). Retrieved 2026-09-02.
4. W3C. [Metadata Vocabulary for Tabular Data](https://www.w3.org/TR/tabular-metadata/). Retrieved 2026-09-02.
5. IETF. [RFC 8259: The JavaScript Object Notation Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259.html). Retrieved 2026-09-02.
6. Ecma International. [ECMA-404: The JSON Data Interchange Syntax](https://ecma-international.org/publications-and-standards/standards/ecma-404/). Retrieved 2026-09-02.
7. IETF. [RFC 7493: The I-JSON Message Format](https://www.rfc-editor.org/rfc/rfc7493.html). Retrieved 2026-09-02.
8. IETF. [RFC 7464: JavaScript Object Notation Text Sequences](https://www.rfc-editor.org/rfc/rfc7464.html). Retrieved 2026-09-02.
9. JSON Lines. [JSON Lines Format](https://jsonlines.org/). Retrieved 2026-09-02.
10. Unicode Consortium. [UTF and Byte Order Mark FAQ](https://www.unicode.org/faq/utf_bom.html). Retrieved 2026-09-02.
11. Unicode Consortium. [Unicode 17.0 Core Specification, Chapter 5](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-5/). Retrieved 2026-09-02.
12. IANA. [Media Type: text/csv](https://www.iana.org/assignments/media-types/text/csv). Retrieved 2026-09-02.
13. Python. [csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html). Retrieved 2026-09-02.
14. Python. [json — JSON Encoder and Decoder](https://docs.python.org/3/library/json.html). Retrieved 2026-09-02.
15. OWASP. [CSV Injection](https://owasp.org/www-community/attacks/CSV_Injection). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Parse the conceptual CSV record `7,"north, west","line one\nline two"` and explain why delimiter and line splitting fail.

### Exercise 2

Design a CSV boundary for customer identifiers, optional display names, decimal balances and timestamps. Include null and BOM policy.

### Exercise 3

A JSON object contains duplicate names, a 20-digit identifier, `NaN`, a missing field and a null field. Define an interoperable ingestion decision for each.

### Exercise 4

Compare whole-document JSON, JSON Lines and RFC 7464 JSON text sequences for a continuously appended event export.

### Exercise 5

Design a parallel, resumable ingestion and quarantine protocol for 500 GB of supplier text data whose CSV dialect is documented but sometimes violated.

## Answers to the Exercises

### Answer 1

Under comma delimiter and RFC-style quoting, the record has three fields: unquoted `7`, quoted `north, west`, and quoted text containing an embedded newline. The comma inside the second field and newline inside the third are data because quote state is active.

Splitting on comma creates four fragments; splitting on newline creates two apparent records. A CSV parser tracks quoted/unquoted state, doubled quotes and record endings. The producer contract must also specify whether the shown `\n` denotes an actual LF byte or two literal characters.

### Answer 2

Declare UTF-8, forbid or explicitly strip one BOM at offset zero, choose comma/quote/doubled-quote behavior, allow CRLF and LF record ends, require a unique four-column header and reject ragged rows. Keep `customer_id` as constrained string so leading zeros survive. Allow empty display name as value.

Choose a reserved escaped null marker for optional display name only, while identifiers and balance cannot be null. Parse balance as bounded decimal with specified currency and scale, and timestamp as RFC-defined instant with offset policy. State formula-safe presentation export separately from raw data, plus size limits, quarantine and round-trip fixtures.

### Answer 3

Reject duplicate names because consumer behavior is not interoperable. Treat the 20-digit identifier as a string under schema; if the producer sent a number, either reject or accept only after proving exactness across all consumers. Reject `NaN` because it is not a JSON number.

Preserve the distinction between missing and explicit `null`. Apply the schema: missing may select a versioned default or mean old producer; null is allowed only if that state has declared meaning. Do not “clean” either into the other. Preserve raw evidence and stable error classification in quarantine.

### Answer 4

A whole-document array is atomic and widely parseable but rewriting or incomplete tails complicate continuous append and recovery. JSON Lines supports append, concatenation and record-at-a-time processing with common tools, provided every JSON value is compact on one UTF-8 line and record sizes are bounded.

RFC 7464 explicitly marks each record start with RS and ends with LF, supporting recovery after damaged elements and clearer framing for arbitrary JSON texts, but tool support is less common. Select from consumer support and recovery requirements; version the choice rather than calling every option `.jsonl`.

### Answer 5

Land immutable objects with size and digest, producer/contract version and encoding. Validate strict decoding and dialect on samples plus adversarial fixtures. Because CSV newlines may occur inside fields, use upstream file partitions or a quote-aware indexing pass to create verified safe byte ranges; validate distributed counts/digests against a single-stream baseline.

Checkpoint object digest, parser version and last complete logical record boundary. Enforce file/field/record limits. Give each framed record stable source identity; publish accepted partitions atomically and quarantine invalid records with raw byte span, error code and protected provenance. Reconcile accepted plus quarantined to framed count, review dialect violations, and replay corrected records idempotently without rereading a mutable source.
