# Course 6 successor handoff

Course 6 exports `capstone/handoff/` to Course 7. The package defines the storage classes, stateful workloads, recovery gates, migration order, backup evidence, and immutable data-plane release subjects that GitOps must reconcile safely.

Course 7 may automate promotion and rollback. It may not weaken reclaim policy, bypass restore gates, mutate retained snapshots, or order application rollout independently of schema and data migration safety.
