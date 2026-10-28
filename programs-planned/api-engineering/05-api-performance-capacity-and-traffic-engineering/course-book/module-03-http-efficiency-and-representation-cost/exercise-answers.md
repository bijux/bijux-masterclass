# Worked Answers — Module 03: HTTP Efficiency and Representation Cost

Use these solutions to audit your reasoning for **HTTP Efficiency and Representation Cost**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. For a 1,000-byte object, normalize `bytes=100-199`.

The selected bytes are 100 through 199 inclusive: start 100, internal end-exclusive 200, length 100, and `Content-Range: bytes 100-199/1000`.

The chapter’s decisive distinction is this: The parser converts the HTTP inclusive end into one internal half-open interval and rejects multiple ranges. The streaming iterator accepts start, length, and chunk size and never reads beyond the selected bytes.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 2. Normalize `bytes=-200` for a 1,000-byte object.

A suffix range selects the final 200 bytes: start 800, end-exclusive 1000, `Content-Range: bytes 800-999/1000`. A suffix length larger than the object selects the whole object.

In the cumulative capstone, the rule becomes concrete: The implementation rejects multi-range requests rather than pretending to support multipart ranges. If-Range requires validator-aware behavior: send the range only when the validator permits it; otherwise send the full representation. Range boundaries are inclusive.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 3. What response should `bytes=1500-` receive for a 1,000-byte object?

The start is beyond the current selected representation, so return 416 with `Content-Range: bytes */1000`. The profile does not silently return an empty 206.

A useful way to reason about the boundary is: An entity tag identifies a selected representation. A strong validator can be used when byte-for-byte identity is required, including range combination. A weak validator signals semantic equivalence without byte identity and begins with W/.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 4. Why can a content hash be a strong ETag for an artifact?

When the hash covers the exact selected bytes and collision-resistant encoding is used, equal tags imply byte identity for practical purposes. If content coding changes the bytes, the encoded representation needs its own tag or identity encoding must be selected.

The implementation consequence is: Content-addressed artifacts already have a strong identity: the checksum of exact bytes. Metadata entities can use a version-derived strong tag when serialization is deterministic, or a weak tag when multiple byte encodings represent the same state.

## 5. When is `Cache-Control: no-cache` different from `no-store`?

`no-cache` allows storage but requires validation before reuse. `no-store` instructs caches not to store the response. The correct choice depends on sensitivity and reuse design; `no-cache` does not mean ‘do not cache’.

The important nuance is: HTTP caching is not an in-process dictionary. A response’s policy declares whether and how clients or shared caches may reuse it. Authorization-sensitive metadata defaults to Cache-Control: private, no-cache: a private cache may store it but must validate before reuse. Highly sensitive or non-reusable responses may use no-store.

## 6. Why may `Vary: Authorization` be insufficient as a shared-cache security design?

It creates a key per credential value and may expose sensitive credential material to cache metadata or produce unbounded cardinality. Many shared caches also treat authenticated responses specially. Prefer private caching or a trusted tenant/principal partition designed explicitly.

Under concurrency or failure, the distinction becomes: Immutable content-addressed artifacts can use long freshness with immutable when authorization and URL design ensure that reuse cannot cross principals improperly. If an artifact URL is protected by bearer authorization, shared caching requires a deliberate design; public is not safe by default.

## 7. Calculate application buffer for 200 streams, 64 KiB chunks, and two buffers per stream.

`200 × 64 KiB × 2 = 25,600 KiB`, or 25 MiB of application-level buffers, before runtime, kernel, proxy, and TLS buffers. This is a lower-bound component, not total memory.

The design remains honest only if: Streaming means the application does not materialize the entire object in memory before sending it. It does not mean memory use is zero. Each connection holds buffers in the application, runtime, server, kernel, and potentially proxy.

## 8. A 900-byte JSON response compresses to 600 bytes but costs 1.5 ms CPU. Should it be compressed?

There is no universal answer. Compare network conditions, request rate, CPU budget, and latency. For a local or CPU-saturated service the 300-byte saving may not justify 1.5 ms. Use a size/media-type threshold derived from evidence.

The consumer-facing consequence is: For the capstone, JSON above a threshold may use gzip when accepted. Binary artifacts default to identity unless their media type and measured ratio justify precompressed or stored encodings. Range requests operate on the selected representation; dynamically compressed range semantics are deliberately avoided.

## 9. What must remain true when replacing a full download with ranges?

Authorization, selected representation, ETag, checksum, content type, complete length, inclusive boundaries, 206/416 semantics, cancellation cleanup, and byte reconstruction must remain correct.

The operational consequence is: The artifact adapter opens only authorized, validated paths and seeks to the selected range. It reads no more than the remaining range length per iteration. Client disconnect and cancellation close the file promptly.

**Evidence.** Use a correctness-gated baseline/candidate comparison that attributes CPU, wall time, allocations, event-loop delay, and downstream work to one hypothesis.

## 10. Why measure storage reads for a 304 response?

A validator design that requires reading the full artifact to compute the tag saves network bytes but not storage I/O. A content-addressed metadata record should allow validation without rereading the object.

The strongest engineering interpretation is: A response consumes server CPU, memory, storage reads, network bytes, client processing, and intermediary capacity. Reducing one dimension may increase another. Compression lowers network bytes but consumes CPU and can delay the first byte. Small chunks bound memory but increase syscall and framing overhead. Large chunks improve throughput but increase per-connection memory.

## 11. Can a weak ETag satisfy `If-Range` in this course profile?

No. Range combination requires byte-level confidence. The profile uses strong validators for `If-Range`; otherwise it sends the full representation.

The defect-oriented view is: An entity tag identifies a selected representation. A strong validator can be used when byte-for-byte identity is required, including range combination. A weak validator signals semantic equivalence without byte identity and begins with W/.

**Evidence.** Vary tenant, principal, representation, source version, mutation, concurrent miss, and cache failure while asserting correctness before hit rate.

## 12. Design an experiment for chunk size.

Hold workload, object distribution, concurrency, and environment fixed. Test several chunk sizes; measure TTFB, completion throughput, CPU, peak memory, syscalls if available, and cancellation cleanup. Select a size within memory and tail-latency budgets, not simply maximum throughput.

Across the Python and TypeScript tracks, the invariant is: Precondition evaluation order and method semantics come from HTTP. A shortcut that checks If-None-Match after streaming half the body is wrong even if it saves some work. Select representation, compute or retrieve the validator, evaluate preconditions, then send the response.
