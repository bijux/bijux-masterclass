# Laboratory 7 — Compressed Digest Pipeline

**Module 47: Transform Pipelines: Compression, Hashing, and Integrity**

## Product

Build a gzip pipeline that records source, canonical, and compressed byte counts, computes explicitly named SHA-256 digests, rejects corrupt input, enforces an expanded-byte limit, and publishes metadata only after successful completion.

This is an independent mechanism study. It deliberately excludes FlowLedger’s other stages so failures can be attributed to one contract.

## Governing question

> How do compression, decompression, hashing, and format transforms compose without confusing data representation, integrity evidence, security, and resource amplification?

## Public surface

- `gzipWithDigests(source)` returns source and compressed counts, two named digests, and compressed bytes.

- `gunzipBounded(input, maxExpandedBytes)` rejects output beyond the declared limit.

- `DigestLabel` in the starter makes representation part of the type vocabulary.

## Required invariants

- Hash taps pass bytes through unchanged.

- Source and compressed digests are computed over explicitly different edges.

- Digests are unavailable before the associated stream completes.

- Corrupt compressed input fails with its causal zlib error.

- Expanded output is bounded independently of compressed input.

## Implementation sequence

1. Build the byte-counting SHA-256 tap.

2. Compose source tap, gzip, compressed tap, and sink.

3. Gate digest retrieval on finalization.

4. Add round-trip verification.

5. Add bounded decompression and corruption tests.

6. Write a representation graph labeling every count and digest.

Do not begin by reading the reference. The starter defines the vocabulary and a baseline, not the final design.

## Adversarial cases

- empty source;

- many tiny source chunks;

- incompressible and highly compressible input;

- corruption at the header, body, and trailer;

- expanded bytes exactly at and above the limit;

- digest access before completion;

- different gzip settings producing different compressed digests;

Add cases in the smallest order that falsifies an incorrect model. Avoid arbitrary sleeps; use exact chunks, counters, injected callbacks, or explicit state transitions.

## Prohibited shortcuts

- naming every digest `sha256` without a representation;

- calling a hash authentication;

- limiting compressed input but not expansion;

- collecting unbounded expanded output;

- publishing metadata before output completion;

A shortcut is prohibited because it removes the mechanism the laboratory exists to teach, not because one implementation style is preferred.

## Completion evidence

1. a labeled representation graph;

2. round-trip and corruption tests;

3. exact expanded-limit tests;

4. a test proving taps do not change bytes;

5. a written integrity-versus-authenticity statement;

## Independent transfer

Design a backup verifier for compressed archives. Decide which digests are stored, which representation each covers, and how an expansion limit is enforced during verification.

Your transfer design must reconstruct the module ledger for the new domain. Renaming the laboratory types is not transfer.

## Representation report

Run one logical record set through four observation points: canonical uncompressed bytes, compressed bytes, decompressed bytes, and parsed records. Record byte count and SHA-256 at each byte representation. The canonical and decompressed digests should agree when decompression restores exactly the canonical byte stream; the compressed digest generally differs because it identifies a different representation.

Repeat with two chunkings and verify that each representation's digest is chunk-independent. Then corrupt one compressed byte and classify the resulting failure: framing, decompression, integrity comparison, or domain parsing. Do not use one generic “verification failed” label. State what a bare SHA-256 digest proves and what it does not: it can detect accidental mismatch against a trusted expected value, but it does not authenticate an attacker-controlled file and attacker-controlled digest. The completed laboratory must include a diagram naming the exact byte domain consumed by every transform, counter, and digest tap.

## Comparing with the reference

After your tests pass, inspect `reference/` and locate the first meaningful difference. Adopt it only when it proves an invariant your design misses; otherwise retain the simpler design.
