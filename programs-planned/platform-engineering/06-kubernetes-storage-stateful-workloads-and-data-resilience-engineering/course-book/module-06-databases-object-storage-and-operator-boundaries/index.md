# Module 06 — Databases, Object Storage, and Operator Boundaries

> **Governing question:** Which stateful capabilities should Kubernetes host directly, which should be external services, and which responsibilities may an operator safely automate?

## Why this module exists

The platform team deploys a database StatefulSet, a backup sidecar, and a shared RWX artifact volume. The service team assumes the platform owns database upgrades and restore. The platform assumes the service team owns schema compatibility. A routine version change produces a valid Pod rollout and an invalid database state.

This module does not begin with YAML. It begins by locating authority and the earliest missing transition. Kubernetes storage is a set of cooperating control loops around an external data system; the application still owns the meaning and correctness of the data.

## Learning outcomes

- compare managed services, operators, and manually managed StatefulSets
- separate transactional state from immutable object data
- define database ownership, replication, backup, and upgrade boundaries
- evaluate object-store consistency, identity, lifecycle, and egress requirements
- review operators as domain-specific control planes
- reject architectures that centralize all state in one shared filesystem

## A data service is more than a Pod plus PVC

A database includes on-disk format, transaction log, checkpointing, replication, membership, leader election, fencing, authentication, schema, backup protocol, upgrade rules, and client semantics. Kubernetes can run the processes and attach volumes. It does not supply those database-specific mechanisms. A StatefulSet manifest that starts PostgreSQL is not equivalent to an operated PostgreSQL service.

Before selecting a deployment model, enumerate the responsibilities: who upgrades the engine, tests extensions, rotates credentials, monitors lag, repairs replicas, runs vacuum or compaction, validates backups, and decides failover? If ownership is incomplete, the platform capability is not ready.
## Managed service, operator, or direct workload

A managed database transfers some infrastructure and control-plane work to a provider, but service owners still own schema, queries, client behavior, recovery requirements, and many security decisions. An operator embeds database knowledge in a Kubernetes controller and may manage clusters, replication, backups, and upgrades. Direct StatefulSets expose the most mechanism and the most operational burden.

The correct choice depends on required control, compliance, portability, team expertise, failure-domain needs, and cost. “Kubernetes-native” is not a sufficient reason to operate a database inside the cluster. Atlas uses a local single-writer ledger for learning and defines a managed-service comparison lane for production decisions.
## Transactional state and immutable artifacts want different interfaces

Transactional state benefits from conditional mutation, transactions, indexes, constraints, and a well-defined commit point. Artifacts are naturally immutable, content-addressed, and retrieved by identity. Forcing artifacts into database rows can make backup and transfer expensive. Forcing transactional metadata into object keys creates hidden locking and consistency protocols.

Atlas stores run state in a transactional service and published artifacts in object-style storage. The artifact record contains checksum, size, media type, creation generation, and retention class. Publication is atomic at the application layer: clients cannot observe a completed artifact before its bytes and metadata agree.
## Shared filesystems are not coordination services

RWX filesystems are valuable when multiple workloads truly require shared file semantics. They do not automatically provide record locking, transaction isolation, leader election, or safe concurrent update protocols. NFS client caching, rename semantics, lock recovery, and backend availability can alter application behavior. A directory convention is not a schema.

Course 6 allows shared filesystems for bounded cases such as read-mostly datasets or tool compatibility, but it requires a separate coordination contract. Atlas does not use a shared filesystem as its job queue, database, or source of truth.
## Operators own reconciliation, not business meaning

A database operator may create StatefulSets, Services, Secrets, backups, and failover actions. It should publish status that reflects database state rather than only Kubernetes object existence. It needs upgrade sequencing, compatibility checks, finalizers, and disaster procedures. Yet the operator cannot decide whether a business transaction may be lost or whether an application schema migration is reversible.

An operator review therefore covers both Kubernetes mechanics and domain boundaries. Atlas records which fields the platform owns, which the operator owns, and which remain with the application team. Course 10 will expose these capabilities through a platform API only after their authority is explicit.
## Network and storage contracts meet at the data service

Course 5 defined stable names, default-deny traffic, egress validation, and Gateway boundaries. Data services add controller endpoints, node-plugin sockets, database Services, object-storage endpoints, KMS, backup targets, and restore traffic. NetworkPolicy must allow required flows without making IP reachability the authorization mechanism.

The data service’s readiness also feeds network eligibility. A database can listen on a socket while replaying a log or lacking quorum. Object storage can accept requests while the intended bucket policy or encryption key is unavailable. Atlas health states report data capability, not merely TCP availability.

## Operators can automate unsafe decisions consistently

Automation increases repeatability, not correctness. An operator that promotes a replica based on incomplete health signals can cause split brain every time. An operator that deletes PVCs during cluster deletion can consistently destroy retained data. Review the operator’s state machine, defaults, finalizers, backup integration, and failure handling, not only its happy-path installation.

Atlas operator evaluations include planted Node partitions, stale leaders, failed backups, incompatible upgrades, and deletion with unavailable backends.


## Managed service does not remove platform integration

A managed database still needs private connectivity, DNS, workload identity, credentials, TLS, egress policy, observability, quotas, backup policy, and recovery evidence. It may improve operational depth while creating provider-specific dependencies. The platform should expose a stable capability without hiding provider limits that affect application design.

Course 2’s cloud foundation and Course 5’s connectivity plane therefore remain active inputs even when the database is outside Kubernetes.


## Artifact publication needs a commit protocol

An API may upload bytes while a worker writes metadata. If metadata becomes visible before the object is complete, clients can observe a corrupt artifact. If bytes exist without metadata, garbage collection may delete or leak them. Atlas stages content under a temporary identity, verifies checksum and size, atomically records the immutable object, then publishes metadata.

The protocol is idempotent: repeating publication of identical bytes returns the same content identity; conflicting bytes for one identity are rejected.


## Service catalogues must include recovery ownership

A platform catalogue entry for a database should list owner, engine, version, topology, storage classes, backup mechanism, last verified restore, RPO, RTO, encryption authority, upgrade window, and incident route. “Maintained by platform” is too broad.

Course 10 will turn this information into a platform product, but Course 6 defines the data-specific fields and proofs.

## Worked semantic example

```python
from atlas_data.architecture import DataServiceDecision

decision = DataServiceDecision.evaluate(
    workload="transactional-run-state",
    team_operational_expertise="limited",
    requires_custom_storage_engine=False,
    requires_cross_region_recovery=True,
)
assert decision.recommendation == "managed-service"
```

The example is intentionally small enough to inspect. It establishes one invariant in the dependency-light lane; it does not claim native Kubernetes or storage-system conformance.

## Production-intent API fragment

```yaml
apiVersion: v1
kind: Service
metadata:
  name: atlas-db
  namespace: atlas-system
spec:
  clusterIP: None
  selector:
    app.kubernetes.io/name: atlas-db
  ports:
    - name: database
      port: 5432
```

The manifest is a contract candidate. Its effect depends on admission, installed controllers, CSI capabilities, backend behavior, and application compatibility.

## Failure signatures

| Observation | Likely missing guarantee | Decisive evidence |
|---|---|---|
| operator ambiguity | no team owns upgrade or restore | responsibility matrix |
| RWX queue | filesystem races corrupt workflow | transactional coordination |
| managed-service assumption | provider backup does not meet app RPO | service-specific recovery proof |

## Atlas capstone increment

Atlas publishes an explicit data-service decision record, transactional-state contract, immutable-artifact contract, and operator responsibility matrix.

## Evidence boundary

The module’s Python and filesystem tests can falsify logical invariants and local durability mechanisms. Cluster controller behavior, CSI RPC behavior, snapshot semantics, cloud durability, and operated recovery require the corresponding native evidence lane. Record unavailable evidence as `not-executed`.

## Transition

Module 7 creates copies of those data sets without confusing crash consistency, application consistency, cloning, and backup.

## Advanced design review — choose the owner that understands the invariant

Generic Kubernetes controllers understand Pods and claims. A database operator understands engine members, replication, log positions, failover, backup hooks, and version skew. A managed service may own even more of that lifecycle. Put a transition under the component that can observe and enforce its invariant, then expose enough evidence for the platform and service owner to verify the result.

This principle prevents “operator-shaped shell scripts”: custom automation that restarts Pods or edits labels without understanding database history. It also prevents the opposite mistake of trusting an operator’s `Ready` condition for every service requirement. Compose operator status with service-specific RPO, tenant, schema, and workload evidence.

## Exit is part of the service contract

A data service decision is incomplete without an export and migration path. Record formats, extensions, keys, network dependencies, backup portability, transfer time, and cutover/fencing. Testing exit does not imply frequent migration; it limits the risk of discovering during an incident that the only usable restore path depends on the failed provider or controller.

## Operators create a second API surface

An operator’s custom resources are APIs consumed by platform teams and service owners. Their fields, defaults, status conditions, upgrade rules, and deletion behavior deserve the same scrutiny as a public API. A field named `instances: 3` may imply engine membership, Pod count, or desired replicas depending on the operator. Backup and failover fields can trigger external effects and need stable identity and idempotency.

Before platform adoption, inspect CRD schemas, status semantics, finalizers, child ownership, RBAC, webhooks, upgrade policy, backup formats, and recovery runbooks. Test deletion of a custom resource in a disposable environment and determine which PVCs, snapshots, and external copies survive. A platform template should expose only the subset it can support and should not pass arbitrary operator configuration directly to consumers.

## Managed service does not mean outsourced accountability

A provider can own infrastructure and engine operations while the organization remains accountable for access, schema, data quality, retention, residency, and recovery decisions. Service-level claims must be read carefully: multi-zone availability may not imply synchronous zero-loss failover; automatic backups may share an account or region; point-in-time recovery may have retention gaps; maintenance can introduce version changes.

The platform should normalize these facts into the same data-service profile used for in-cluster options. That enables an honest comparison and prevents architecture from being selected by organizational fashion. The output is a supported service, not merely a vendor resource.
## Choose the data service before choosing the workload controller

The question “Should PostgreSQL run in Kubernetes?” is too broad. A responsible decision compares service requirements, team capability, failure domains, recovery objectives, compliance, cost, and operational ownership. Kubernetes can schedule and restart a database process; it does not automatically provide database replication, point-in-time recovery, corruption detection, major-version upgrades, or expert incident response.

A useful decision matrix compares three lanes:

| Lane | Strength | Hidden responsibility |
|---|---|---|
| managed database | provider operates much of the data plane | network integration, IAM, parameter policy, backup verification, provider limits |
| operator-managed database in Kubernetes | declarative lifecycle close to workloads | operator quality, cluster/storage coupling, upgrade and recovery competence |
| manually managed in Kubernetes | maximum direct control | nearly every lifecycle and correctness responsibility remains yours |

The recommendation should be explicit about what is outsourced and what is retained. “Managed” never means “no operational work.”

### Operators encode one product’s operational model

A database operator is a controller with domain-specific knowledge. It may create StatefulSets, Services, Secrets, backup jobs, replication configuration, and status conditions. Its custom resource becomes a platform API. That API deserves the same scrutiny as any other contract:

- Which fields are stable?
- What does `Ready` mean?
- Which transitions are automated?
- Which failures stop reconciliation?
- How are credentials rotated?
- How are backups and restores represented?
- How are major upgrades performed?
- Which resources may users modify directly?
- What happens when the operator itself is unavailable?
- Can a newer operator reconcile an older custom resource safely?

A controller that continuously rewrites application state can make manual recovery harder. The runbook must explain when to pause reconciliation, which fields remain authoritative, and how to resume without undoing a repair.

### Replication is not backup

Database replicas usually share logical history and can reproduce corruption, accidental deletion, or malicious writes. They improve availability and may reduce data loss under specific failures. Backups preserve selected historical recovery points and should survive a different failure boundary. Both are needed when the recovery objectives require them.

For Atlas transactional state:

- replication protects against an individual process, Pod, or Node failure;
- fencing prevents two primaries from writing divergent histories;
- write-ahead logs support point-in-time recovery;
- backups protect historical states outside the primary failure boundary;
- restore drills prove the backup chain and keys are usable.

The platform should never report “protected” without naming which mechanism covers which failure.

### Object storage is not a mounted filesystem

Atlas artifacts are immutable and content-addressed, making object storage a natural fit. Object stores expose key-based operations, conditional requests, versioning, retention, and multipart upload rather than POSIX rename, directory, or locking semantics. Mounting an object store through a filesystem adapter can hide these differences and encourage unsafe assumptions about atomicity and consistency.

A correct artifact publication flow is designed for object semantics:

```text
stream bytes while computing digest
→ publish under an immutable digest identity
→ verify length and checksum
→ commit authoritative metadata
→ make the artifact discoverable
```

Retries use the same digest and are idempotent. Readers verify identity. Deletion follows retention policy. A mutable “latest” alias may exist, but it is not the release identity.

### Database readiness must describe service semantics

A database process accepting TCP does not prove it can serve the application. A replica may be in recovery, far behind, or unable to satisfy writes. A primary may have lost quorum or durable storage. Readiness should reflect the role and operation the application needs.

Examples:

- write endpoint requires current primary authority and accepted fencing generation;
- strongly consistent read requires primary or sufficiently synchronized replica;
- eventual read can accept a bounded lag;
- maintenance jobs may require exclusive migration ownership;
- restore validation requires isolated access before normal traffic.

Avoid liveness checks that restart a healthy database because a remote dependency or quorum is unavailable. Restarting can lengthen recovery or remove useful evidence.

### Operator and platform ownership boundaries

The platform team may provide supported data-service classes, storage, identity, network policy, monitoring, and backup integration. The service team owns schema, query behavior, consistency needs, migration logic, and business-level restoration validation. A database team may own engine configuration and recovery. The operator vendor or project owns controller code and documented lifecycle behavior.

Write these boundaries into the service catalogue. During an incident, “database problem” is not a sufficient assignment. The earliest failed transition determines the owner:

```text
claim provisioning
→ volume attachment
→ database process start
→ replication membership
→ primary election
→ schema readiness
→ application query
```

### Managed-service connectivity is still part of the platform

When the database runs outside the cluster, Course 5’s connectivity guarantees remain active. Private DNS, routes, egress, identity federation, TLS, connection pools, and failure handling must be explicit. A managed service can reduce storage lifecycle work while increasing dependence on cloud network and IAM control planes.

The Course 6 release dossier records both the data service and the path to it. Recovery exercises include credential rotation, DNS or endpoint changes, and restoration into a new service instance—not merely restarting Pods.

### Decision defense for Atlas

Atlas uses three deliberately different models:

- transactional run state: database semantics, one authoritative history, fencing and point-in-time recovery;
- immutable artifacts: object semantics, content identity, independent retention and verification;
- worker scratch: local ephemeral storage, bounded and fully recomputable.

This separation is more important than whether a particular database is managed or in-cluster. Each data class has an interface aligned with its semantics, an owner, a recovery path, and evidence strong enough for its claim.
