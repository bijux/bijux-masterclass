# Module 8 — Edge, Data Protection, Backup, and Recovery

A public endpoint and an encrypted volume can make a diagram look complete. They do not establish availability, durability, or recoverability. This module follows two paths all the way to their owners:

1. the request path from DNS through TLS and the load balancer to Atlas;
2. the data path from an accepted job through persistent storage, backup, restoration, and integrity verification.

The governing question is not “did we enable a feature?” It is:

> Which failure does this mechanism contain, and which failure remains?

## Learning outcomes

You will be able to:

- trace a public request through DNS, certificate selection, listener, target group, security groups, health checks, and host sockets;
- distinguish edge availability from application readiness;
- reason about load-balancer connection draining and unhealthy-target behavior;
- explain the availability and durability properties of root volumes, EBS data volumes, snapshots, and object storage;
- define recovery point objective (RPO) and recovery time objective (RTO) as testable requirements;
- design backups that can be restored into an empty destination;
- distinguish encryption at rest, key availability, deletion protection, retention, and immutability;
- verify data-plane behavior after infrastructure apply;
- avoid claiming multi-zone or regional resilience from a single-zone teaching topology;
- write a recovery runbook that an operator can execute under pressure.

## The request path is a chain of independent decisions

For `https://atlas.example.test/jobs/123`, the client depends on:

```text
DNS answer
→ network reachability
→ load-balancer listener
→ certificate and hostname verification
→ listener rule
→ target group
→ target health
→ security-group path
→ Atlas edge socket
→ Atlas API readiness
```

A plan showing an ALB and a Route 53 record proves only that resources are proposed. It does not prove the certificate chain, DNS propagation, target registration, health behavior, or application response.

## DNS ownership

Atlas separates:

- **zone ownership:** who may change the authoritative namespace;
- **record ownership:** which deployment may publish the Atlas name;
- **certificate ownership:** which process requests and renews names;
- **application ownership:** which target may receive the traffic.

A wildcard certificate or broad DNS role can collapse these boundaries. The Course 2 baseline grants the release role authority only over the Atlas record set and certificate association needed for the environment.

DNS TTL is an operational parameter. A low TTL can help planned transitions but increases query volume and does not force every resolver to refresh instantly. A high TTL can make rollback slower. The release record includes the expected propagation and fallback behavior.

## TLS termination

The reference lane terminates TLS at the application load balancer and sends HTTP to the private Atlas host. This proves public certificate handling and edge routing but not encryption on the final hop.

The architecture record therefore says exactly:

```text
client → ALB: TLS authenticated by public/private managed certificate
ALB → Atlas host: private VPC HTTP in Course 2 baseline
```

Later courses can add end-to-end workload identity and transport protection. Course 2 does not call the final hop “mTLS” or “end-to-end encrypted.”

A certificate in the plan is not a usable certificate. Validate:

- requested names;
- validation status;
- listener attachment;
- selected certificate for the hostname;
- protocol and policy;
- expiry/renewal ownership;
- client hostname verification.

## Health checks choose routing behavior

A health check is an automated control loop. A badly chosen check can amplify an incident.

If `/ready` fails whenever an optional analytics sink is down, the load balancer may remove every otherwise usable target. If it checks only that the TCP port opens, it may route requests to an API that cannot read its durable spool.

Atlas defines:

- `/live`: process can execute a minimal self-check;
- `/ready`: API can accept and durably queue a job;
- `/edge-health`: narrow, inexpensive check used by the ALB.

The ALB check has thresholds and intervals. Those values determine detection and recovery delay. “Health check enabled” is not enough; compute the approximate time to unhealthy and healthy states.

## Draining and replacement

When a target is removed, existing connections may continue during a deregistration delay. New requests should go elsewhere. With a singleton target, “draining” can mean intentional unavailability unless the replacement overlaps safely.

Review:

- application shutdown grace period;
- load-balancer deregistration delay;
- client/request timeout;
- long-running response behavior;
- process termination timeout.

The outer layer must stop admitting work early enough for the inner layer to finish or reject it truthfully.

## Security-group path

The public ALB security group accepts only the declared public listener. The Atlas host security group accepts the application port only from the ALB security group—not from the whole VPC CIDR and not from the internet.

For administration, the baseline prefers a managed session path rather than public SSH. If SSH is enabled in a learner sandbox, it is an explicit temporary exception with a source prefix, expiry, and cleanup check.

## Availability is not durability

These terms answer different questions:

- **availability:** can the service be used now?
- **durability:** will acknowledged data survive expected failures over time?
- **recoverability:** can operators restore a usable service and prove data integrity?

An EBS volume can be durable within its service model and still be unavailable while attached to a failed instance or inaccessible in another zone. A snapshot can protect data and still have an RTO too long for the service objective.

## Atlas storage classes

### Root volume

Replaceable machine state. Encrypted, but not the authority for completed work. Deletion with the instance is acceptable after evidence is retained.

### Data volume

Holds the Atlas spool and results for the Course 2 singleton. Encrypted with the workload key, separately tagged, and protected from accidental deletion during normal replacement.

The reference baseline uses one availability zone. Therefore:

- the volume does not establish cross-zone failover;
- attachment location constrains replacement;
- a zonal failure requires snapshot-based or backup-based recovery elsewhere;
- recovery time includes volume creation and host bootstrap.

### Snapshot

A point-in-time block-storage recovery artifact. Snapshots need ownership, encryption, retention, inventory, and restore tests. “Snapshot completed” does not prove the application can use the restored filesystem.

### Object backup

The course exports a small, canonical Atlas backup manifest and result objects to an encrypted, versioned S3 bucket. This provides a separately addressable recovery path and integrity hashes. It is not a substitute for application-consistent database backup in later stateful systems.

## RPO and RTO

### Recovery point objective

The maximum acceptable amount of data loss, measured in time or committed operations. If snapshots run every 24 hours, the design cannot claim an RPO of one hour.

### Recovery time objective

The target duration to restore useful service. It includes detection, decision, artifact retrieval, resource creation, data restoration, validation, and traffic return—not only the cloud API’s volume-creation time.

Atlas declares separate objectives:

```text
host replacement in same zone
    RPO: 0 for separately attached data volume
    RTO: bounded by replacement and readiness

zone-loss recovery from latest protected snapshot/object backup
    RPO: backup interval plus application consistency limit
    RTO: restore, bootstrap, integrity check, and DNS/traffic return
```

These are hypotheses until a real recovery drill measures them.

## Backup is a workflow

A dependable backup process answers:

1. what is included;
2. what consistency point is captured;
3. who can initiate it;
4. where the artifact is stored;
5. who can delete it;
6. which key decrypts it;
7. how integrity is recorded;
8. how retention is enforced;
9. how an empty environment restores it;
10. how success is measured.

Atlas generates a manifest containing version, source release, snapshot/object identifiers, creation time, file list, and SHA-256 digests.

## Restore into an empty destination

The strongest Course 2 recovery exercise does not overwrite the working environment. It restores into a new volume and a clean directory, then verifies:

- expected files exist;
- unexpected files do not appear;
- hashes match;
- ownership and modes are correct;
- the API can read completed results;
- the worker does not replay already completed work;
- the restored environment has a new machine identity but preserves workload facts.

Restoring over the source can hide missing dependencies and create irreversible damage.

## Encryption and key ownership

Encryption at rest needs more than `encrypted = true`.

Trace:

- which KMS key is used;
- who administers the key;
- who can encrypt, decrypt, create grants, disable, or schedule deletion;
- whether snapshots retain the correct key relationship;
- whether the recovery role can decrypt;
- how cross-account copies would be authorized;
- what happens if the key is unavailable.

A backup encrypted by a key that the recovery environment cannot use is not recoverable.

Course 2 uses separate key intents for state and workload data. The optional AWS baseline may collapse them in a cost-constrained sandbox only if the limitation is explicit.

## Deletion protection, retention, and immutability

These mechanisms are related but distinct:

- **deletion protection** blocks a normal delete API until disabled;
- **versioning** retains prior object versions;
- **retention/lifecycle** removes or transitions data under policy;
- **object lock/WORM controls** constrain deletion or modification for a retention period;
- **cross-account ownership** limits which compromised account can alter evidence.

Every protection also affects legitimate cleanup, privacy deletion, cost, and incident response. The course does not enable indefinite retention by default.

## Post-apply data-plane checks

After apply, Atlas verifies:

- DNS resolves to the intended edge;
- TLS hostname validation succeeds;
- an incorrect hostname fails;
- ALB target health becomes healthy;
- direct public access to the host is unavailable;
- a job is durably accepted;
- the worker completes it;
- the result hash is recorded;
- backup is created;
- restoration into an empty destination reproduces the hash.

These checks are outside OpenTofu’s state model. They are still part of the release.

## Failure exercise: the healthy but unusable target

Suppose the edge health path returns `200`, but the data volume is mounted read-only. The ALB routes traffic, and Atlas cannot accept durable jobs.

The diagnosis requires both edge and application evidence. The remedy may be to make the narrow edge check include a bounded spool-write/read/delete probe, or to stop the service before reporting readiness. The correct choice balances false positives, health-check cost, and failure containment.

## Application consistency versus filesystem consistency

The local Atlas spool can be backed up after the API and worker stop at a known
completed-job boundary. A database or continuously written filesystem may need
a snapshot API, write freeze, transaction log, or application-native backup.

Course 2's backup manifest records its consistency point explicitly. It does
not generalize a stopped-process file copy into a universal cloud backup method.
This prepares the learner for stateful systems and Kubernetes storage later in
the program, where crash consistency and application consistency must be
distinguished rigorously.

## Recovery authority during an incident

The normal runtime role may write backups but should not delete or broadly read
them. A recovery role can list/select versions and decrypt under controlled
conditions. The role is more powerful, so its sessions are monitored and used
only through the runbook.

This asymmetry matters when the workload is compromised: the attacker should
not be able to destroy the recovery path using the same credential that writes
new results.

## Atlas capstone increment

Module 8 adds:

- DNS, certificate, ALB, listener, target group, and edge security groups;
- explicit TLS-termination record;
- health thresholds and deregistration policy;
- encrypted data volume and workload key policy;
- snapshot and object-backup policy;
- backup manifest with digests;
- restore-to-empty workflow;
- RPO/RTO hypotheses;
- post-apply request and recovery checks;
- runbooks for target failure, volume loss, and restore.

## Completion standard

You may continue when you can trace one public request and one restored result end to end, identify every authority and failure boundary, and distinguish measured recovery evidence from diagram-level aspiration.
