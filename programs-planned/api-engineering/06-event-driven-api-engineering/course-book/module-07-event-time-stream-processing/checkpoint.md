# Checkpoint — Module 07: Event-Time Stream Processing, Windows, Watermarks, and Corrections

## Required result

Implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine.

## Demonstrate

- Distinguish event, ingestion, processing, and observation time.
- Define watermark and allowed lateness without claiming certainty.
- Explain how one late event revises a published result.
- Describe durable checkpoint and output atomicity.

## Commands

```bash
make stream-proof
make vector-proof
make module-proof MODULE=07 TRACK=$TRACK
```

## Evidence to retain

- `work/module-07/expected-windows.json`
- ordered and shuffled processing reports
- watermark and revision trace
- late-event records
- planted-defect failures
- checkpoint/output failure-window design
- output from `make stream-proof`

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

The **Event-Time Stream Processing, Windows, Watermarks, and Corrections** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that implement windowed analysis metrics, watermark progression, late-event correction revisions, and quarantine.
