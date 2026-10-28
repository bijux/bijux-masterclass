# Checkpoint — Event-Time Stream Processing, Windows, Watermarks, and Corrections

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Distinguish event, ingestion, processing, and observation time.
- Define watermark and allowed lateness without claiming certainty.
- Explain how one late event revises a published result.
- Describe durable checkpoint and output atomicity.

## Required result

- `work/module-07/expected-windows.json`
- `work/module-07/window-results.json`
- `work/module-07/late-events.json`
- `work/module-07/checkpoint-design.md`
- `work/module-07/residual-risk.md`

## Commands

```bash
make stream-proof
make vector-proof
make module-proof MODULE=07 TRACK=$TRACK
```

## Defend the design

- Show ordered and shuffled inputs converging.
- Demonstrate duplicate suppression and late revision separately.
- Explain why processing time is wrong for replayed business facts.
- Defend the state-retention budget.

## Continue only when

- Window time source or boundary is implicit.
- Late events are silently dropped or overwrite output without revision.
- Duplicate identity is timestamp/payload based.
- The dependency-light in-memory model is claimed as durable.

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine.
