# Lab — Module 03 lab — Optimize artifact retrieval without changing bytes

> **Module 03:** HTTP Efficiency and Representation Cost

## Objective

Compare full, conditional, ranged, compressed metadata, and streamed artifact paths while enforcing exact representation and authorization oracles.

## Why this lab matters

This lab turns the module’s governing question—**Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes?**—into a falsifiable experiment. Immutable content-addressed artifacts can use long freshness with immutable when authorization and URL design ensure that reuse cannot cross principals improperly. If an artifact URL is protected by bearer authorization, shared caching requires a deliberate design; public is not safe by default.

It advances the cumulative Analysis Runs Platform by requiring this result: **Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- artifact fixtures include small, medium, and large exact-byte objects
- authorized and unauthorized principals are available
- baseline uses the inherited full retrieval path
- memory and byte counters are enabled

## Hypothesis

The clean implementation should satisfy this claim: **304 sends no body and retains validator/cache metadata; 206 and 416 metadata matches exact bytes; reconstructed checksum equals the original; unauthorized access remains rejected before reuse; large object memory is bounded by configured chunks and concurrency; compression comparison includes CPU and byte savings.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Measure full authorized downloads for three object sizes.
2. Add or enable strong validators and repeat with matching `If-None-Match`.
3. Run prefix, open-ended, and suffix range vectors.
4. Reconstruct an object from sequential ranges and verify its checksum.
5. Test JSON compression above and below the threshold.
6. Run 100 concurrent streams and record peak application buffering.
7. Attempt cross-principal conditional and range access.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Compare full, conditional, ranged, compressed metadata, and streamed artifact paths while enforcing exact representation and authorization oracles**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **HTTP Efficiency and Representation Cost**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **HTTP Efficiency and Representation Cost**. A green command without the negative case and causal explanation does not satisfy this gate.
