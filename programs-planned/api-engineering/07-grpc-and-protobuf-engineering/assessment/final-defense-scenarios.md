# Final defense scenarios

The examiner selects at least six:

- post-commit CreateRun response loss;
- reused request identifier with changed input;
- unknown enum value from a newer provider;
- TypeScript revision above `Number.MAX_SAFE_INTEGER`;
- upload data before metadata;
- slow WatchRun consumer;
- expired observation resume position;
- worker result from stale lease generation;
- delegated user with correct scope but wrong tenant;
- server drain with active upload and worker streams;
- descriptor/reflection mismatch;
- public HTTP cutover followed by rollback.

For each scenario, the learner must name the authoritative state, expected status, retry or reconciliation behavior, evidence, and residual limitation.
