# Checkpoint — Schema Evolution, Compatibility, Replay, and Historical Truth

Do not progress because the chapter has been read. Progress when the following evidence can be reproduced from a clean working tree.

## Demonstrate

- Explain directional compatibility for new producers, current consumers, and retained records.
- Give an example of semantically breaking but structurally compatible change.
- Distinguish upcasting from rewriting history.
- Describe a safe projection rebuild and live catch-up.

## Required result

- `work/module-05/compatibility-report.json`
- `work/module-05/semantic-review.md`
- `work/module-05/replay-plan.yaml`
- `work/module-05/replay-results.json`
- `work/module-05/residual-risk.md`

## Commands

```bash
make evolution-proof
make replay-proof
make release-proof
make module-proof MODULE=05 TRACK=$TRACK
```

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

The checkpoint is complete only when all commands pass, all artifacts are reviewable, and each oral-defense question can be answered without appealing to a broker feature as magic.
