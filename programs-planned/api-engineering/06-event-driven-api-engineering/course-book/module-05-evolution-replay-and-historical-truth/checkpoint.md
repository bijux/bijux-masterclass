# Checkpoint — Module 05: Schema Evolution, Compatibility, Replay, and Historical Truth

## Required result

Classify compatibility, add upcasters, preserve source bytes, define retention, and run bounded dry-run replay.

## Demonstrate

- Explain directional compatibility for new producers, current consumers, and retained records.
- Give an example of semantically breaking but structurally compatible change.
- Distinguish upcasting from rewriting history.
- Describe a safe projection rebuild and live catch-up.

## Commands

```bash
make evolution-proof
make replay-proof
make release-proof
make module-proof MODULE=05 TRACK=$TRACK
```

## Evidence to retain

- `work/module-05/compatibility-report.json`
- `work/module-05/semantic-review.md`
- `work/module-05/replay-plan.yaml`
- dry-run and apply reports
- v1/v2 projection comparison
- side-effect denial evidence
- output from `make evolution-proof` and `make replay-proof`

## Defend the design

- Defend one accepted additive change.
- Show why one rejected change breaks retained history.
- Demonstrate that replay creates no external side effects.
- Explain how correction facts preserve historical truth.

## Continue only when

- Any retained event is rewritten.
- Replay is unbounded or writes directly into an unprotected live target.
- Semantic changes rely only on JSON Schema comparison.
- Effect versions share or delete deduplication evidence.

The **Schema Evolution, Compatibility, Replay, and Historical Truth** checkpoint is complete only when the commands pass, the retained artifacts explain the event-system state, and you can defend the result without treating broker delivery, ordering, or replay as magic.
