# Reference Answers — Module 03: Module 03 exercise answers — HTTP Efficiency and Representation Cost

Read after attempting all twelve HTTP Efficiency and Representation Cost exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. For a 1,000-byte object, normalize `bytes=100-199`.

The selected bytes are 100 through 199 inclusive: start 100, internal end-exclusive 200, length 100, and `Content-Range: bytes 100-199/1000`.

## 2. Normalize `bytes=-200` for a 1,000-byte object.

A suffix range selects the final 200 bytes: start 800, end-exclusive 1000, `Content-Range: bytes 800-999/1000`. A suffix length larger than the object selects the whole object.

## 3. What response should `bytes=1500-` receive for a 1,000-byte object?

The start is beyond the current selected representation, so return 416 with `Content-Range: bytes */1000`. The profile does not silently return an empty 206.

## 4. Why can a content hash be a strong ETag for an artifact?

When the hash covers the exact selected bytes and collision-resistant encoding is used, equal tags imply byte identity for practical purposes. If content coding changes the bytes, the encoded representation needs its own tag or identity encoding must be selected.

## 5. When is `Cache-Control: no-cache` different from `no-store`?

`no-cache` allows storage but requires validation before reuse. `no-store` instructs caches not to store the response. The correct choice depends on sensitivity and reuse design; `no-cache` does not mean ‘do not cache’.

## 6. Why may `Vary: Authorization` be insufficient as a shared-cache security design?

It creates a key per credential value and may expose sensitive credential material to cache metadata or produce unbounded cardinality. Many shared caches also treat authenticated responses specially. Prefer private caching or a trusted tenant/principal partition designed explicitly.

## 7. Calculate application buffer for 200 streams, 64 KiB chunks, and two buffers per stream.

`200 × 64 KiB × 2 = 25,600 KiB`, or 25 MiB of application-level buffers, before runtime, kernel, proxy, and TLS buffers. This is a lower-bound component, not total memory.

## 8. A 900-byte JSON response compresses to 600 bytes but costs 1.5 ms CPU. Should it be compressed?

There is no universal answer. Compare network conditions, request rate, CPU budget, and latency. For a local or CPU-saturated service the 300-byte saving may not justify 1.5 ms. Use a size/media-type threshold derived from evidence.

## 9. What must remain true when replacing a full download with ranges?

Authorization, selected representation, ETag, checksum, content type, complete length, inclusive boundaries, 206/416 semantics, cancellation cleanup, and byte reconstruction must remain correct.

## 10. Why measure storage reads for a 304 response?

A validator design that requires reading the full artifact to compute the tag saves network bytes but not storage I/O. A content-addressed metadata record should allow validation without rereading the object.

## 11. Can a weak ETag satisfy `If-Range` in this course profile?

No. Range combination requires byte-level confidence. The profile uses strong validators for `If-Range`; otherwise it sends the full representation.

## 12. Design an experiment for chunk size.

Hold workload, object distribution, concurrency, and environment fixed. Test several chunk sizes; measure TTFB, completion throughput, CPU, peak memory, syscalls if available, and cancellation cleanup. Select a size within memory and tail-latency budgets, not simply maximum throughput.
