# Module 10 checkpoint — Performance Regression and Release Engineering

## Required result

- [ ] all ten module checkpoints pass
- [ ] performance profile 1.0 validates
- [ ] release vectors agree across languages
- [ ] accepted dossier contains complete identities and evidence
- [ ] faster invalid candidate is rejected
- [ ] inconclusive candidate is not misreported
- [ ] final handoff is sanitized and manifested

## Defend the design

Answer without reading from the chapter:

1. Why is your accepted candidate actually comparable?
2. Which earlier gate rejects the fastest invalid candidate?
3. What exact condition triggers remeasurement or rollback?

## Demonstrate

- explain the governing question: How does a performance change become a reproducible release decision rather than a favorable chart?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=10 TRACK=${TRACK:-python}
```

## Continue only when

The course fails if a faster incorrect candidate can pass, if a baseline is overwritten without lineage, or if inconclusive evidence is reported as a performance win.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that build correctness-first regression gates, environment comparability, accepted/rejected/inconclusive candidates, and a performance dossier.
