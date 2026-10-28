# Job retries and effect identity

Kubernetes Job semantics count successful Pod completions. They do not automatically make database writes, reports, uploads, or external calls exactly once.

A retry can occur after the external effect commits but before the Pod or Job status records success. Therefore every effectful task needs a logical identity independent of Pod UID or attempt number.

For an indexed Job:

```text
job logical identity + completion index + effect version
```

For a CronJob:

```text
schedule identity + intended schedule time + effect version
```

The effect store should accept the first commit, return the same result for an identical replay, and reject changed output under the same identity.

`backoffLimit` controls retry accounting, not business deduplication. `activeDeadlineSeconds` bounds runtime, not external side effects after cancellation. `ttlSecondsAfterFinished` removes completed Job objects, not business records.
