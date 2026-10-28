# Runbook — progressive release abort

1. Freeze further traffic steps.
2. Confirm actual router allocation and candidate request count.
3. Return new traffic to stable and observe connection drain.
4. Stop candidate-only side effects or prove idempotency.
5. Check the data compatibility phase before selecting an older desired revision.
6. Commit or record the rollback desired state so GitOps will not restore the candidate.
