# Module 03 lab — Optimize artifact retrieval without changing bytes

## Objective

Compare full, conditional, ranged, compressed metadata, and streamed artifact paths while enforcing exact representation and authorization oracles.

## Setup conditions

- artifact fixtures include small, medium, and large exact-byte objects
- authorized and unauthorized principals are available
- baseline uses the inherited full retrieval path
- memory and byte counters are enabled

## Failure action and investigation


1. Measure full authorized downloads for three object sizes.
2. Add or enable strong validators and repeat with matching `If-None-Match`.
3. Run prefix, open-ended, and suffix range vectors.
4. Reconstruct an object from sequential ranges and verify its checksum.
5. Test JSON compression above and below the threshold.
6. Run 100 concurrent streams and record peak application buffering.
7. Attempt cross-principal conditional and range access.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory. A passing command without this causal explanation is insufficient.

## Operational oracle

- 304 sends no body and retains validator/cache metadata
- 206 and 416 metadata matches exact bytes
- reconstructed checksum equals the original
- unauthorized access remains rejected before reuse
- large object memory is bounded by configured chunks and concurrency
- compression comparison includes CPU and byte savings

## Required evidence

Create:

```text
work/module-03/
├── http-policy.yaml
├── full-baseline.json
├── conditional.json
├── range-vectors.json
├── reconstruction.sha256
├── compression.json
├── memory.json
└── decision.md
```

The decision must distinguish metadata and artifact policy and state which evidence comes from pure vectors versus a local socket experiment.

## Cleanup and reset

Close clients, verify no artifact file descriptor remains open, remove only generated response captures, and restore default compression/range configuration.

## Completion gate

- [ ] conditional retrieval semantics pass
- [ ] all single-range vectors pass
- [ ] multi-range requests are rejected explicitly
- [ ] large artifact delivery is bounded
- [ ] authorization is preserved for every path
- [ ] candidate explains CPU/byte/memory trade-off

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.
