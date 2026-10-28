# Module 03 checkpoint — HTTP Efficiency and Representation Cost

## Required result

- [ ] HTTP vectors pass in both tracks
- [ ] ETag meaning is documented per representation
- [ ] 304/206/416 behavior is correct
- [ ] range reconstruction checksum passes
- [ ] peak buffer calculation and measurement exist
- [ ] cache directives are reviewed against authorization

## Defend the design

Answer without reading from the chapter:

1. What exact bytes does your ETag identify?
2. Why is a 304 not just an empty 200?
3. Which buffer dominates memory at your chosen concurrency?

## Demonstrate

- explain the governing question: Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=03 TRACK=${TRACK:-python}
```

## Continue only when

The module fails if any byte, validator, range, or authorization oracle changes to obtain better throughput.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory.
