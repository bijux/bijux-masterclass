# Evidence rubric

Every submitted claim is scored on six dimensions: semantic precision, authoritative ownership, failure-window coverage, durable oracle, repeatability, and bounded uncertainty.

| Level | Description |
|---|---|
| 0 | Assertion or screenshot without an invariant or oracle |
| 1 | Correct happy path but no duplicate, crash, replay, or security boundary |
| 2 | Failure action and expected result named, but durable evidence is incomplete |
| 3 | Repeatable proof with explicit identity, transaction, and residual risk |
| 4 | Cross-language or live-dependency corroboration that does not overstate scope |

A module checkpoint requires level 3 for its central invariant. Level 4 cannot compensate for an incorrect semantic model.
