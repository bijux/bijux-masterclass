# Checkpoint — Module 10: Event Platform Governance, Release, and Final Defense

## Required result

Publish the catalogue, consumer declarations, accepted/rejected release candidates, final defense, and Course 7 handoff.

## Demonstrate

- Explain the distinct responsibilities of AsyncAPI, event catalogue, consumer catalogue, and broker configuration.
- Describe producer and consumer release gates.
- Define deprecation/retirement in the presence of retained history.
- Trace one event and one failure across the complete architecture.

## Commands

```bash
make release-proof
make planted-defect-proof
make handoff-proof
make core-proof
make manifest-proof
```

## Evidence to retain

- `work/module-10/release-dossier/decision.json`
- `work/module-10/release-dossier/trace.md`
- final catalogue and consumer inventory
- candidate comparison reports
- planted-defect matrix
- tabletop timeline and reconciliation
- handoff manifest and secret-scan result
- output from `make core-proof` and `make manifest-proof`

## Defend the design

- Defend the accepted release and two rejections.
- Show a complete completion-event durability and effect trace.
- Respond to one selected failure without relying on broker magic.
- Explain exactly which live/environment-backed claims remain unexecuted.

## Continue only when

- Any public message or consumer is unowned or uncatalogued.
- A breaking, replay-unsafe, or unauthorized candidate is accepted.
- A partition/retention change lacks migration evidence.
- The handoff contains secrets, private incident data, or manifest drift.

The **Event Platform Governance, Release, and Final Defense** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
