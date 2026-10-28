# Module 03 — HTTP Efficiency and Representation Cost

> **Program stage:** Course 5 of 10 — Sustain the promise under pressure.

> **Central question:** Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes?

## Where this module fits

Module 02 produced **Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons**. This module extends that result by asking: **Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes?**

The new capstone increment is **Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory**. It becomes the prerequisite for **PostgreSQL Query and Persistence Performance**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Separate resource state, selected representation, and transferred message.
- Measure bytes and buffering alongside latency.
- Apply strong and weak entity tags intentionally.
- Evaluate conditional requests in the correct precedence.
- Implement single byte-range requests and documented unsatisfied ranges.
- Stream large bodies with bounded memory.
- Choose compression from media type, size, CPU, and cache-key consequences.
- Design authorization-aware cache directives and `Vary` behavior.
- Reject optimizations that break checksums, ranges, or tenant isolation.

## Capstone increment

Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory.

## Core performance model

### 1. Representation cost is multi-dimensional


A response consumes server CPU, memory, storage reads, network bytes, client processing, and intermediary capacity. Reducing one dimension may increase another. Compression lowers network bytes but consumes CPU and can delay the first byte. Small chunks bound memory but increase syscall and framing overhead. Large chunks improve throughput but increase per-connection memory.

Measure at least:

```text
headers bytes
body bytes
time to first byte
time to completion
peak buffered bytes
storage bytes read
CPU time
status and validator outcome
```

For an artifact download, first-byte and completion latency answer different questions. For a metadata response, serialization and header overhead may dominate body transfer.


### 2. Validators and conditional requests


An entity tag identifies a selected representation. A **strong** validator can be used when byte-for-byte identity is required, including range combination. A **weak** validator signals semantic equivalence without byte identity and begins with `W/`.

Content-addressed artifacts already have a strong identity: the checksum of exact bytes. Metadata entities can use a version-derived strong tag when serialization is deterministic, or a weak tag when multiple byte encodings represent the same state.

For retrieval, `If-None-Match` can turn a full `200` transfer into `304 Not Modified` when the selected representation matches. The `304` response has no representation body, but must include relevant validator and caching metadata. Do not return `304` merely because the database row is unchanged when content negotiation would select different bytes.


### 3. Preconditions are not speed hints


Conditional headers define request semantics, not optional optimization. Mutation preconditions such as `If-Match` were implemented in Course 2 to prevent lost updates. Retrieval conditions such as `If-None-Match` avoid transferring an unchanged representation.

Precondition evaluation order and method semantics come from HTTP. A shortcut that checks `If-None-Match` after streaming half the body is wrong even if it saves some work. Select representation, compute or retrieve the validator, evaluate preconditions, then send the response.

The capstone helper parses comma-separated entity tags and wildcard behavior without accepting malformed tags as silent misses.


### 4. Byte ranges


A range request asks for selected bytes of a representation. Course 5 supports one `bytes` range:

```text
Range: bytes=0-999
Range: bytes=1000-
Range: bytes=-500
```

A satisfiable range returns `206 Partial Content` with `Content-Range` and the correct `Content-Length`. An unsatisfied range returns `416 Range Not Satisfiable` with `Content-Range: bytes */<complete-length>`.

The implementation rejects multi-range requests rather than pretending to support multipart ranges. `If-Range` requires validator-aware behavior: send the range only when the validator permits it; otherwise send the full representation. Range boundaries are inclusive.


### 5. Bounded streaming


Streaming means the application does not materialize the entire object in memory before sending it. It does not mean memory use is zero. Each connection holds buffers in the application, runtime, server, kernel, and potentially proxy.

Choose a chunk size through evidence. Track active download concurrency and calculate a conservative memory bound:

```text
application buffer ≈ active_streams × chunk_size × buffers_per_stream
```

The artifact adapter opens only authorized, validated paths and seeks to the selected range. It reads no more than the remaining range length per iteration. Client disconnect and cancellation close the file promptly.


### 6. Compression policy


Compression is representation selection. The response varies by content coding, so caches and validators must account for it. `Vary: Accept-Encoding` tells caches that request header participates in selection.

Do not compress already compressed formats blindly. Do not compress tiny responses when headers and CPU exceed byte savings. Avoid dynamic compression of secret-bearing responses in contexts where attacker-controlled input and secrets share a compression context; security policy takes precedence.

For the capstone, JSON above a threshold may use gzip when accepted. Binary artifacts default to identity unless their media type and measured ratio justify precompressed or stored encodings. Range requests operate on the selected representation; dynamically compressed range semantics are deliberately avoided.


### 7. Caching policy at the HTTP boundary


HTTP caching is not an in-process dictionary. A response’s policy declares whether and how clients or shared caches may reuse it. Authorization-sensitive metadata defaults to `Cache-Control: private, no-cache`: a private cache may store it but must validate before reuse. Highly sensitive or non-reusable responses may use `no-store`.

Immutable content-addressed artifacts can use long freshness with `immutable` when authorization and URL design ensure that reuse cannot cross principals improperly. If an artifact URL is protected by bearer authorization, shared caching requires a deliberate design; `public` is not safe by default.

`Vary` affects cache keys. Varying on high-cardinality or unstable headers can destroy hit rate. Omitting a selection header can return the wrong representation.

## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Validators representation-aware | ETag identifies the selected representation and encoding. | 304 or range combines different bytes. | Conditional vector tests |
| Conditional before body | Preconditions are evaluated before streaming or serialization cost where possible. | Body work occurs for not-modified response. | Server trace and test |
| Range exactness | Inclusive boundaries, lengths, and 206/416 metadata are correct. | Corrupt or extra bytes are returned. | Byte vectors and checksum |
| Bounded streaming | Large artifacts are read in bounded chunks and file handles close on cancellation. | Memory scales with object size or leaks descriptors. | Memory/cancellation test |
| Compression deliberate | Policy accounts for media type, threshold, CPU, security, and `Vary`. | Bytes shrink while CPU or semantics regress. | Compression experiment |
| Cache policy authorization-aware | Private and shared reuse reflect tenant and credential boundaries. | Cross-tenant response reuse. | Security and cache tests |
| Metrics separate TTFB/completion | First byte and full completion are measured separately. | Streaming appears fast while completion stalls. | HTTP envelope |
| Correctness exact bytes | Checksum and range reconstruction pass for candidate. | Fast path changes artifact contents. | Artifact oracle |

## Worked failures

### Case 1 — The universal public cache

**Initial condition.** Project metadata responses are marked `public, max-age=300` to reduce database reads.

**Analysis.** The representation is owner-specific and bearer-authenticated. A shared cache can reuse it for another caller unless the design provides a safe partition.

**Correct response.** Use private validation or an explicitly tenant-partitioned trusted cache; retain authorization at reuse.

**Lesson.** Cacheability is part of the security boundary.

### Case 2 — The bodyless 304 with missing validator

**Initial condition.** The server returns 304 but omits ETag and cache policy.

**Analysis.** The client cannot reliably update stored metadata and future validation behavior.

**Correct response.** Return the relevant selected-representation metadata required by the cache policy.

**Lesson.** 304 is a semantic response, not merely an empty 200.

### Case 3 — The off-by-one range

**Initial condition.** `bytes=0-9` returns eleven bytes because end is treated as exclusive in one layer and inclusive in another.

**Analysis.** HTTP byte-range end positions are inclusive.

**Correct response.** Normalize to an internal half-open interval `[start, end_exclusive)` once, and verify `Content-Range: bytes 0-9/length` plus ten bytes.

**Lesson.** Boundary conversion must be centralized.

### Case 4 — The compressed range confusion

**Initial condition.** The server advertises the checksum of uncompressed bytes but applies dynamic gzip before satisfying a byte range.

**Analysis.** The range now refers to a different selected representation and the validator/content-length relationship is ambiguous.

**Correct response.** Use identity encoding for range requests in this profile or maintain distinct stored encoded representations and validators.

**Lesson.** Compression, ranges, and validators must share one representation model.

## Python implementation

### Mechanism

The Python HTTP module implements strict entity-tag parsing, conditional matching, single-range normalization, compression selection, and a bounded iterator over byte sources.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/http_efficiency.py`
- `capstone/tracks/python-fastapi/src/api_performance/streaming.py`
- `capstone/tracks/python-fastapi/tests_performance/test_http_efficiency.py`

### Focused example

```python
from api_performance.http_efficiency import parse_single_range

selection = parse_single_range("bytes=0-999", complete_length=10_000)
assert selection.start == 0
assert selection.end_exclusive == 1_000
assert selection.content_range == "bytes 0-999/10000"
```

The parser converts the HTTP inclusive end into one internal half-open interval and rejects multiple ranges. The streaming iterator accepts start, length, and chunk size and never reads beyond the selected bytes.

### Python-specific failure to avoid

A synchronous file read inside an async route can block the event loop. Use the framework’s file-response mechanism, a bounded thread offload, or an async storage adapter, and measure the chosen boundary.

## TypeScript implementation

### Mechanism

The TypeScript module uses bigint-safe length parsing, strict tag matching, and an async iterable for bounded range reads. The Fastify adapter remains separate from pure HTTP calculations.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/http-efficiency.ts`
- `capstone/tracks/typescript-fastify/src/performance/streaming.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/http-efficiency.test.mjs`

### Focused example

```typescript
const selection = parseSingleRange("bytes=0-999", 10_000n);
if (selection.start !== 0n || selection.endExclusive !== 1_000n) {
  throw new Error("incorrect range");
}
if (selection.contentRange !== "bytes 0-999/10000") {
  throw new Error("incorrect Content-Range");
}
```

Lengths use bigint because artifact size is an external integer. The adapter converts only bounded chunk lengths to number for buffer allocation.

### TypeScript-specific failure to avoid

Do not call `readFile` for large artifacts; it materializes the whole object. Avoid converting complete object lengths to `number` before range validation.

## Cross-language invariant

Both tracks agree on tag lists, wildcard matching, range normalization, 416 decisions, compression eligibility, and chunk boundaries for every shared vector.

## Failure patterns

- **Validator over resource not representation.** Different encodings share one strong ETag. **Decisive check:** conditional and encoding vectors.
- **Whole-body buffering.** Memory grows with artifact size. **Decisive check:** peak-memory and chunk trace.
- **Unsafe shared reuse.** Authorization is absent from reuse decision. **Decisive check:** cross-principal test.
- **Range off-by-one.** Content-Range and bytes disagree. **Decisive check:** reconstruction checksum.
- **Compression by habit.** CPU rises more than network benefit. **Decisive check:** paired CPU/byte report.
- **TTFB-only success.** First byte is fast but connection occupies resources too long. **Decisive check:** completion latency and active streams.

## Evidence and design review

Before accepting the module increment, answer:

1. Which exact bytes does the ETag identify?
2. Does a 304 preserve the metadata needed for future validation?
3. Can a range response be reconstructed into the original checksum?
4. What is the maximum application buffer at the configured concurrency?
5. Which responses may be stored by a shared cache and why?
6. Did byte reduction increase CPU or tail completion latency beyond budget?

## Module synthesis

You are ready to leave this module when you can **separate resource state, selected representation, and transferred message, measure bytes and buffering alongside latency, and apply strong and weak entity tags intentionally** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **the lab introduces its declared planted defect** and requiring the following oracle: **304 sends no body and retains validator/cache metadata; 206 and 416 metadata matches exact bytes; reconstructed checksum equals the original; unauthorized access remains rejected before reuse.**

The cumulative platform now includes **Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [PostgreSQL Query and Persistence Performance](../module-04-postgresql-query-and-persistence-performance/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
