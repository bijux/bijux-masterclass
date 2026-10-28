# Checkpoint — Event Platform Governance, Release, and Final Defense

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Explain the distinct responsibilities of AsyncAPI, event catalogue, consumer catalogue, and broker configuration.
- Describe producer and consumer release gates.
- Define deprecation/retirement in the presence of retained history.
- Trace one event and one failure across the complete architecture.

## Required result

- `work/module-10/release-dossier/decision.json`
- `work/module-10/release-dossier/trace.md`
- `work/module-10/planted-defect-matrix.json`
- `work/module-10/tabletop-report.md`
- `work/module-10/handoff-proof.json`

## Commands

```bash
make release-proof
make planted-defect-proof
make handoff-proof
make core-proof
make manifest-proof
```

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

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
