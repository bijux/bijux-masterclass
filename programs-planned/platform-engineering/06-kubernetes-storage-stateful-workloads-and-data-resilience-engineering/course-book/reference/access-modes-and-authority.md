# Access modes and writer authority

Kubernetes access modes constrain how a volume may be presented; they do not implement locking, consensus, transaction isolation, or stale-writer rejection.

| Access mode | Kubernetes-level intent | Common misreading |
|---|---|---|
| `ReadWriteOnce` | writable from one Node at a time | “only one Pod can write” |
| `ReadOnlyMany` | read-only from multiple Nodes | “all readers see one strongly consistent view” |
| `ReadWriteMany` | writable from multiple Nodes | “concurrent writes are safe” |
| `ReadWriteOncePod` | writable by one Pod cluster-wide when the CSI stack supports it | “split brain is impossible” |

The application still needs an authority model. For a database, this may be a consensus term or primary-generation token. For a worker, it may be a lease generation stored with the job. For a filesystem workflow, it may be compare-and-swap against an authoritative manifest. The authority must be enforced at the same boundary as the protected write.

## Review sequence

1. Identify the logical data set and authoritative writer.
2. Determine whether the access mode is implemented by the selected driver and volume type.
3. Describe Node loss, network partition, force detach, and delayed process shutdown.
4. State how a replacement writer receives a newer generation.
5. Prove that the stale generation is rejected.
6. Record whether the evidence came from a semantic model, Kubernetes, the CSI driver, or the actual data service.

## Atlas decision

Atlas uses access modes to narrow exposure and durable fencing to protect single-writer history. A release is rejected when it relies on attachment state alone to guarantee writer exclusivity.
