# Analysis-run state machine

```text
queued ──poll──> running ──poll──> completed
  |                 |
  +──cancel────────>canceled
                    |
                    +──failure boundary──> failed
```

| Current state | Action | Result |
|---|---|---|
| `queued` | retrieve | `running`, progress 50 |
| `running` | retrieve | `completed`, progress 100, artifact created |
| `queued` | cancel | `canceled` |
| `running` | cancel | `canceled` |
| terminal | cancel | `409` Problem Details |
| incomplete | list artifacts | `409` Problem Details |
| completed | list artifacts | artifact page |

The deterministic polling transition is not presented as a production queue implementation. It exists so every learner and CI run can prove asynchronous HTTP semantics without time-sensitive background jobs.

## Invariants

- progress is between 0 and 100;
- terminal states do not transition again;
- `completedAt` is non-null only for a completed run;
- artifacts appear only after completion;
- a run's project and dataset must share an owner and relationship;
- an idempotent replay never advances or duplicates state;
- canceling a run never creates an artifact.
