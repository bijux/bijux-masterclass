# Checkpoint — Module 03: HTTP Efficiency and Representation Cost

## Required result

Optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory.

## Demonstrate

- explain the governing question: Where do HTTP connections, representations, compression, conditional requests, range delivery, and streaming consume time and bytes?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=03 TRACK=${TRACK:-python}
```

## Evidence to retain

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

## Defend the design

Answer without reading from the chapter:

1. What exact bytes does your ETag identify?
2. Why is a 304 not just an empty 200?
3. Which buffer dominates memory at your chosen concurrency?

## Continue only when

The module fails if any byte, validator, range, or authorization oracle changes to obtain better throughput.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that optimize artifact and metadata delivery while preserving authorization, ETags, ranges, and bounded memory.
