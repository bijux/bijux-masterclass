# Program evidence ladder

The program separates document evidence, semantic evidence, local mechanism evidence, cluster evidence, storage-system evidence, cloud environment evidence, and operated evidence.

A semantic binder can prove that a `WaitForFirstConsumer` claim must not provision before a scheduling topology exists. A local filesystem test can prove atomic rename and directory synchronization on one filesystem. Neither proves that a CSI driver, cloud volume service, snapshot controller, database engine, or backup target provides the same guarantees under Node loss or regional failure.

Course 6 therefore labels every result by evidence class. Static manifests can reject unsafe reclaim policies. Local tests can prove fencing logic and restore verification. Cluster-backed tests can prove controller interactions. Storage-system-backed tests are required for attach, detach, snapshot, expansion, performance, and failure claims. Production durability requires operated evidence over time.
