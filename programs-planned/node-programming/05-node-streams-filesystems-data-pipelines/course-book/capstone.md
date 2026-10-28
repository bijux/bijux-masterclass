# FlowLedger Engineering Guide

FlowLedger is the cumulative Course 5 product: a bounded command-line data pipeline for newline-delimited JSON events. Its purpose is not to demonstrate how many Node.js stream classes can be connected. Its purpose is to make ten contracts coexist without contradiction:

1. byte ownership;
2. stream lifecycle;
3. backpressure;
4. cancellation;
5. incremental decoding and framing;
6. runtime validation;
7. representation-specific compression and hashing;
8. child-process supervision;
9. transactional file publication;
10. deterministic terminal reporting.

The implementation is standard-library-only. That keeps the important mechanisms visible rather than delegating them to a framework whose defaults would become part of the hidden curriculum.

## 1. Product boundary

FlowLedger accepts external files and process arguments, validates them through typed command and data boundaries, processes records incrementally, and either publishes one complete output file or leaves the previously visible destination authoritative.

The supported commands are:

```text
flowledger inspect <input> [--gzip-input]

flowledger normalize <input> <output>
  [--gzip-input]
  [--gzip-output]
  [--replace]

flowledger filter <input> <output>
  --kind <kind>
  [--gzip-input]
  [--gzip-output]
  [--replace]

flowledger verify <input> --sha256 <hex>

flowledger through <input> <output>
  [--replace]
  -- <program> [argument...]

flowledger help
flowledger version
```

`inspect` validates and counts records without publishing a new file. `normalize` validates and emits canonical NDJSON. `filter` performs the same validation and canonicalization but emits only records with the requested kind. `verify` checks the SHA-256 digest of the exact input bytes. `through` treats a directly spawned child process as a raw-byte filter and publishes its stdout only after stdio and child status agree on success.

## 2. Representation graph

The most important architecture artifact is the representation graph. Every arrow changes either ownership, interpretation, or both.

```text
host pathname
      ↓ open
raw file bytes
      ↓ optional gunzip
expanded source bytes
      ↓ fatal UTF-8 decoder
text fragments
      ↓ bounded line framer
physical NDJSON lines
      ↓ JSON.parse
unknown JavaScript values
      ↓ FlowEvent validator
trusted FlowEvent objects
      ↓ selector
emitted or filtered FlowEvent objects
      ↓ canonical encoder
canonical NDJSON bytes
      ↓ optional gzip
published output bytes
```

The graph has separate hash domains:

```text
raw input bytes       → sourceSha256
canonical NDJSON      → canonicalSha256
final output bytes    → outputSha256
```

Those names are not cosmetic. A gzip option changes `outputSha256` without changing `canonicalSha256`. Reordering object keys changes canonical bytes even when the parsed object has the same members. `verify` intentionally verifies raw file bytes because that command receives a pathname and an expected digest for the stored representation.

For `through`, the graph is different:

```text
raw input bytes
      ↓ child stdin
foreign process
      ↓ child stdout
raw candidate output bytes
      ↓ transactional sink
published output bytes
```

The child path does not claim FlowEvent validation. It is a generic byte filter with a stronger process-lifecycle contract.

## 3. Domain model

A valid FlowEvent has exactly four fields:

```ts
export interface FlowEvent {
  readonly id: string;
  readonly timestamp: string;
  readonly kind: string;
  readonly value: number;
}
```

The validator establishes all of the following:

- the value is a non-null, non-array object;
- no unknown keys are present;
- `id` is nonempty and within its UTF-8 byte limit;
- `kind` is nonempty and within its UTF-8 byte limit;
- `timestamp` is a canonical ISO instant rather than merely a date-like string;
- `value` is a finite number;
- the returned object is constructed from validated fields rather than reusing the untrusted object.

Canonical encoding writes keys in the fixed order `id`, `timestamp`, `kind`, `value` and terminates every record with `\n`. Canonical output is therefore independent of source key order and source chunking. It is not independent of the schema version: a future field or number-normalization policy would require an explicit compatibility decision.

## 4. Capacity model

Backpressure is necessary but insufficient. FlowLedger owns semantic limits that remain meaningful even when every stream queue respects its high-water mark.

| Retained state | Unit | Bound or policy |
|---|---|---|
| raw source representation | bytes accepted during one operation | `maxSourceBytes` |
| raw stream queues | bytes | Node stream thresholds; treated as tuning, not a total memory proof |
| decompressed expansion | bytes | `maxExpandedBytes` |
| unfinished NDJSON line | UTF-8 bytes | `maxLineBytes` |
| validated records | records inspected during one operation | `maxEvents` |
| identifier | UTF-8 bytes | `maxIdBytes` |
| kind | UTF-8 bytes | `maxKindBytes` |
| final output representation | bytes accepted for publication | `maxOutputBytes` |
| child stdout representation | bytes accepted from one child | `maxChildOutputBytes` |
| child stderr excerpt | bytes retained | `maxChildStderrBytes` |
| child processes | processes per `through` command | exactly one direct child |
| staged output | bytes on disk | bounded by input/product policy, not retained in JavaScript memory |

The raw-source limit is checked before decompression or child stdin. The expanded-byte limit is checked after decompression and before parsing. The unfinished-line limit is independent because a single line can grow without a delimiter. Event-count limits prevent valid small records from creating an unlimited operation. Final output and child stdout have separate byte bounds because a transform can expand data even when its input is bounded. Diagnostic excerpts have their own retention bound because errors are another potential memory channel.

A truthful memory statement is therefore narrower than “streaming uses constant memory.” FlowLedger avoids retaining the complete input and regulates connected queues, but native zlib state, stream buffers, one unfinished line, child-process pipe buffers, and bounded diagnostics still exist.

## 5. Resource ownership

Each operation creates one resource tree. The application function owns the tree; individual helpers own only the resources they create beneath it.

### Record pipeline owner

```text
transformFile / inspectFile
├── input ReadStream
├── optional Gunzip
├── raw ByteTap
├── ExpandedByteLimiter
├── FlowEventDecoder
├── EventSelector
├── EventEncoder
├── canonical ByteTap
├── optional Gzip
├── output ByteTap
└── transactional candidate WriteStream
```

One `pipeline(...)` promise owns pressure, stream errors, destruction, and completion for the connected graph. The transactional wrapper owns the stage pathname, synchronization, destination policy, rename, and pre-commit cleanup. The operation report is constructed only after both levels succeed.

### Child-process owner

```text
throughChild
├── child process
├── input ReadStream → source ByteLimit → input ByteTap → child stdin pipeline
├── child stdout → child-output ByteLimit → output ByteTap → candidate sink pipeline
├── bounded stderr collector
├── child close promise
└── transactional candidate publication
```

Spawn success is observed before starting asynchronous collectors whose rejection would otherwise lack an owner. Stdin, stdout, and stderr progress concurrently. On any branch failure the child is terminated if still live. The function then waits for the owned terminal work rather than treating `kill()` as completion.

## 6. Stream and backpressure policy

FlowLedger uses byte-mode streams until NDJSON records become trusted objects. The decoder’s writable side accepts bytes and its readable side emits `FlowEvent` objects in object mode. The selector remains object mode on both sides. The encoder converts trusted objects back to bytes.

Linear graphs use `node:stream/promises.pipeline` because it provides one operation promise, preserves pressure between stages, and tears down the connected graph on failure. Custom manual writing is reserved for the independent backpressure and fan-out laboratories, where the protocol itself is the teaching target.

No stage attaches a competing `data` listener to a source consumed by pipeline. Hash and count observation is implemented through transparent Transform stages so observation participates in the same lifecycle. A tap updates its state before forwarding the exact chunk and exposes its digest only after flush.

## 7. Incremental decoder contract

`FlowEventDecoder` maintains three pieces of state:

- a bounded pending byte buffer for the current physical line;
- the current physical line number;
- the number of successfully validated events.

NDJSON uses the ASCII LF byte as its frame delimiter, so FlowLedger frames bytes before converting a complete line to text. For each source chunk, the decoder:

1. copies the visible byte window into bounded decoder-owned state;
2. finds every complete LF-delimited frame;
3. removes a terminal `\r` for CRLF input;
4. checks the encoded byte length before decoding or retaining more data;
5. decodes the complete line with fatal UTF-8 validation;
6. parses JSON into `unknown`;
7. validates the FlowEvent shape and domain limits;
8. increments record accounting only after successful validation.

At stream end, a final nonempty unterminated frame is accepted and processed under the same bound and validation rules. Empty physical lines are ignored by current V1 policy; changing that behavior would be a format-compatibility decision. Byte-first framing prevents replacement decoding from erasing malformed-input evidence and makes the line bound independent of JavaScript string code-unit length.

Errors preserve the physical line and causal phase. Malformed UTF-8, over-limit framing, invalid JSON, and invalid event shape are not collapsed into one anonymous parse error.

## 8. Transactional output protocol

FlowLedger never opens the final destination for truncating output. `withTransactionalOutput` performs this sequence:

```text
choose unique stage beside destination
      ↓
create stage exclusively
      ↓
run complete output operation into stage
      ↓
finish stream graph
      ↓
open completed stage and fsync it
      ↓
close file handle
      ↓
apply replace/no-replace destination policy
      ↓
rename stage to destination
      ↓
return committed report
```

Before rename, failure removes the stage best-effort and preserves the old visible destination. Rename is the publication point. The current implementation deliberately does not claim:

- cross-process writer exclusion;
- an atomic no-overwrite primitive across every platform;
- parent-directory synchronization;
- universal power-loss durability;
- safety against an adversary changing directory entries concurrently;
- atomic publication of several unrelated paths.

Those are product boundaries, not hidden omissions. A stronger production design can add a lock or versioned bundle protocol after stating the target platform and failure model.

## 9. Child-process protocol

`through` defaults to direct invocation:

```ts
spawn(program, args, { shell: false, stdio: ['pipe', 'pipe', 'pipe'] })
```

The command parser requires `--` before the program. Everything afterward remains an argument vector; no shell command string is constructed.

The operation succeeds only when all of these facts hold:

- the process spawned;
- input remained within `maxSourceBytes`;
- input streaming to stdin completed or the child closed it under an accepted policy;
- stdout remained within `maxChildOutputBytes` and streamed to the staged destination completely;
- stderr was fully drained while retained content stayed bounded;
- the child closed without signal termination;
- the exit code was zero;
- the candidate synchronized and renamed successfully.

A nonzero child can produce useful stdout, but that stdout is not published because the child’s protocol says failure. Input and output taps report the exact byte count and SHA-256 for the two representations when the operation succeeds. The bounded stderr excerpt is included in the causal error. `stderrBytes` records total observed diagnostic bytes while `stderrTruncated` states whether the retained text is incomplete. Every stdin, stdout, stderr, process-error, and close branch is awaited before the transactional owner decides whether the stage may be published.

## 10. Error model

FlowLedger errors carry stable categories rather than leaking every internal exception directly to the CLI. The categories distinguish:

| Category | Meaning |
|---|---|
| command | invalid CLI grammar, missing option, or invalid digest syntax |
| input | unreadable source, cancellation, or `maxSourceBytes` failure |
| framing | malformed UTF-8, over-limit line, or line-state failure |
| validation | invalid JSON value or invalid FlowEvent domain state |
| compression | gzip/gunzip corruption or transform failure |
| output | canonical, compressed, or child output exceeds its declared byte bound |
| child | spawn, stdio, signal, nonzero status, or cancellation failure |
| digest | expected and actual raw-byte digest differ |
| commit | candidate, synchronization, destination policy, or rename failure |

Wrapping preserves the original cause where the language/runtime supports it. A CLI error message gives enough context to act without dumping unbounded input or stderr. Exit status remains stable: success is zero, user/input/product failure is nonzero, and usage errors are distinguished from unexpected internal failures.

## 11. Determinism and accounting

For the same logical valid input and options:

- canonical NDJSON records are byte-identical;
- filtering preserves source record order;
- report fields appear in a stable order;
- counts do not depend on source chunk boundaries;
- canonical digest does not depend on source object key order;
- gzip output may depend on selected compression settings and library behavior, so its digest identifies the actual output representation rather than a language-level canonical gzip format.

Record accounting satisfies:

```text
inspected = emitted + filtered
```

for successful normalize/filter operations. Invalid records are fatal in V1 and therefore do not enter a successful terminal category. The independent rejects-bundle extension changes this equation and must introduce a `rejected` category deliberately.

Byte accounting remains representation-specific. Raw input, expanded input, canonical output, and final compressed output cannot be added into one conservation equation because transforms legitimately change byte counts.

## 12. Module-by-module construction

### Module 41 — byte ownership

Introduce `maxSourceBytes`, copy-safe helper boundaries, and the first source hash tap. Prove that a small returned result does not accidentally alias a mutable input unless the API explicitly says so.

### Module 42 — stream roles

Name byte-mode and object-mode edges. Add transparent taps and identify the single promise that owns each linear graph. Build event traces for understanding, but do not use trace order as the success predicate.

### Module 43 — pressure and teardown

Connect source, transforms, and destination through `pipeline`. Verify slow destinations, transform failure, and AbortSignal behavior. Add capacity notes for state not controlled by high-water marks.

### Module 44 — sequence adapters

Use async generators for record-level selection where they improve clarity, but retain one explicit adapter boundary. Test early return and upstream cleanup rather than converting between Node and Web streams gratuitously.

### Module 45 — file publication

Add stage ownership, synchronization, overwrite policy, rename, and cleanup. Test preservation of an existing destination after parsing or transform failure.

### Module 46 — trust transition

Add incremental UTF-8, line framing, JSON parsing, FlowEvent validation, physical diagnostics, and canonical serialization. Generate chunk partitions around UTF-8 and delimiter boundaries.

### Module 47 — representation-specific transforms

Add optional gunzip/gzip and taps around the precise byte domains. Enforce expanded and final-output byte limits, and keep source, canonical, and published-output digest names unambiguous.

### Module 48 — foreign process stage

Add direct spawn, concurrent stdio, bounded source and child-output representations, bounded retained stderr, exit/signal interpretation, complete branch joining, and transaction coordination. Test ENOENT, nonzero exit after partial stdout, and cancellation.

### Module 49 — accounting and publication policy

Finalize terminal record counts and output reports. Document why V1 commits one path and how a future required multi-file product would use an immutable bundle or manifest authority.

### Module 50 — integrated proof

Run complete process-level scenarios, regenerate architecture ledgers, inject failures at exact stage counts, and perform an independent cross-layer extension without weakening earlier contracts.

## 13. Testing strategy

The capstone test suite is layered by claim.

### Domain tests

- exact object shape;
- UTF-8 byte limits for identifiers and kinds;
- finite numeric values;
- canonical timestamps;
- deterministic field order;
- unknown-key rejection.

### Decoder tests

- one-byte chunks;
- all split positions around multibyte UTF-8;
- LF and CRLF;
- final unterminated line;
- malformed UTF-8;
- exact and over-limit pending lines;
- invalid JSON and invalid object shape after earlier valid lines.

### Pipeline tests

- inspect counts;
- normalize and filter output;
- source/canonical/output digest domains;
- gzip input and output;
- corruption and expanded-byte failure;
- destination preservation on pre-commit failure;
- existing destination policy.

### Child tests

- direct argument preservation;
- successful stdout publication;
- bounded stderr;
- spawn failure;
- nonzero exit after stdout;
- signal termination;
- cancellation while stdio is active.

### Process tests

- help and version;
- invalid command grammar;
- stable exit status;
- deterministic JSON report;
- no partial final output after failure.

A later hardening pass should add an injectable filesystem boundary for deterministic sync and rename failures. The current tests exercise observable pre-commit preservation and real filesystem behavior without claiming every platform failure can be induced portably.

## 14. Final independent extension — rejects bundle

Add:

```text
--rejects <path>
```

to `normalize` and `filter`.

Framing and JSON syntax errors remain fatal because record boundaries or syntax cannot be trusted. Domain-invalid objects become typed reject records containing:

- physical line number;
- stable rejection code;
- bounded source excerpt;
- causal message;
- no unbounded original value.

The extension changes the conservation equation:

```text
inspected = emitted + filtered + rejected
```

It also introduces a required second output. Do not rename the two staged files sequentially and call the result atomic. Choose and document one protocol:

1. immutable version directory plus one committed pointer;
2. immutable data/reject files plus a manifest published last;
3. independent commits with explicit partial-visibility recovery.

Update command grammar, reports, limits, errors, staging, tests, help, and compatibility behavior. The supplied capstone is complete without this extension; implementing it is the final proof that the reader can change a stream architecture rather than merely reproduce it.

## 15. Completion standard

FlowLedger is complete when you can answer, without reading the implementation:

1. Which allocation owns every returned Buffer?
2. Which byte representation does every digest identify?
3. Where is backpressure preserved?
4. Which retained states require semantic limits beyond high-water marks?
5. What closes each stream, handle, iterator, and child process?
6. What happens when cancellation arrives at every blocking edge?
7. Which errors occur before publication and which can occur after it?
8. Why can invalid input never change the final destination?
9. Why can nonzero child stdout never commit?
10. Which guarantees does FlowLedger explicitly decline to make?

A passing test suite is necessary. The ability to reconstruct these contracts is the evidence that the system is understood rather than merely assembled.
