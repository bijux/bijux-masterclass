# Case 1 — GitOps pruned the recovery copy

A snapshot-content manifest was removed during repository cleanup. Automated prune deleted the Kubernetes object and the storage provider then removed the snapshot. The application remained Healthy, so the release dashboard stayed green.

The failure began at ownership: the application inventory had been allowed to own a data-retention object whose lifecycle belonged to the data owner. Absence from Git was mistaken for retirement authorization.

The repair adds a protected-resource policy, separate recovery inventory, data-owner retirement record, and release gate that enumerates every prune candidate. The incident demonstrates why synchronization and health cannot substitute for recovery evidence.

## Extended reader notes

### Timeline

At 10:02 a cleanup commit removed an apparently unused snapshot-content manifest. At 10:04 automated sync calculated one prune. At 10:05 the Kubernetes object disappeared. At 10:11 the storage controller completed backend deletion. Application health never changed. At 13:40 a restore drill discovered the missing recovery point.

### Why ordinary controls missed it

Schema validation, sync, health, and smoke tests all passed because the application workload was unaffected. The deleted object belonged to the recovery plane, not the serving path. The missing control was lifecycle authority in the inventory and a restore gate bound to the candidate.

### Durable correction

The recovery inventory is separated, prune defaults to false, protected kinds and annotations are policy-blocked, and retirement requires a data-owner record. Release review enumerates every deletion. A periodic restore test detects recovery-set loss independently of application health.
