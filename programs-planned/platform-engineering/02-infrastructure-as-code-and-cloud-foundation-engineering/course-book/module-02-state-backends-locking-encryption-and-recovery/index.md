# Module 2 — State, Backends, Locking, Encryption, and Recovery

State is the operational memory of an OpenTofu configuration. Treating it as disposable generated output is one of the fastest ways to turn routine changes into accidental recreation, data loss, or two teams believing they own the same object.

This module treats state as a small but critical distributed-systems problem: there are writers, locks, versions, sensitive values, partial failures, backups, restoration choices, and lineage.

## Learning outcomes

You will be able to:

- explain why state exists and what information it owns;
- bootstrap a remote backend without pretending the bootstrap paradox does not exist;
- distinguish backend encryption, OpenTofu native encryption, access control, and version recovery;
- reason about lock acquisition, stale locks, and safe force-unlock decisions;
- choose state boundaries based on ownership and lifecycle rather than convenience;
- recover from partial apply, lost state, wrong backend, and stale snapshot incidents;
- avoid leaking sensitive data through outputs and remote-state consumers;
- design a state service that another operator can safely continue using.

## State is more than an inventory

A state snapshot records, among other things:

- state lineage and serial;
- resource and module addresses;
- provider associations;
- remote object identities;
- last observed attributes;
- dependencies and deposed instances during replacement;
- output values;
- schema-version information needed by providers.

Some values are sensitive even when configuration marks them `sensitive`; that annotation mainly controls display. State can still contain the value. Treat the entire state as sensitive.

## Why configuration cannot replace state

A cloud API may have many objects with the same tags or names. Some resources have generated identifiers. Provider defaults and normalized values matter on later plans. OpenTofu needs a durable record that says:

```text
resource address A
was managed by provider configuration P
and corresponds to remote object R
last observed with attributes X
```

Reconstructing that association by guessing after every run would be unsafe.

## The bootstrap paradox

A remote backend such as S3 must already exist before the root configuration can initialize against it. The backend cannot create itself while it is being used.

Atlas uses a separate `bootstrap/` root with local state to create:

- an S3 state bucket;
- versioning;
- public-access blocking;
- a KMS key and alias;
- bucket policy;
- optional audit notifications.

After bootstrap, the foundation root is initialized with an S3 backend configuration:

```hcl
terraform {
  backend "s3" {}
}
```

and external `backend.hcl` values:

```hcl
bucket       = "atlas-tofu-state-123456789012-eu-central-1"
key          = "platform/foundation/terraform.tfstate"
region       = "eu-central-1"
encrypt      = true
kms_key_id   = "alias/atlas-tofu-state"
use_lockfile = true
```

Backend configuration is deliberately separate from ordinary variables. Backend initialization happens before normal expression evaluation.

## Native S3 lock files

The OpenTofu S3 backend can use conditional object writes for locking with `use_lockfile = true`. The lock reduces simultaneous writers. It does not prove that the writer has the correct source, account, inputs, or approval.

A lock failure is useful evidence: another writer may be active, a previous process may have crashed, or the backend path may be shared unintentionally.

Do not force-unlock because a pipeline is slow. Before force-unlock:

1. identify the lock owner and operation;
2. confirm no process is still applying;
3. preserve the lock information;
4. check the provider/cloud activity for in-flight operations;
5. obtain incident-level approval;
6. recalculate a plan after unlock.

## Versioning is a recovery tool, not automatic correctness

S3 versioning lets operators retrieve an earlier state object after accidental overwrite or deletion. An older snapshot may not match the current cloud. Restoring it blindly can make OpenTofu propose recreation of resources created after that snapshot or forget destructive changes already completed.

A safe recovery restores the candidate to a separate backend key first, inspects lineage and serial, compares resource identities with the cloud, and calculates a plan before replacing the authoritative key.

## Encryption has layers

### Backend/server-side encryption

S3 can encrypt objects with a KMS key. This protects stored objects according to AWS storage and key-access controls.

### OpenTofu state and plan encryption

OpenTofu can encrypt state and plan contents before backend storage. The course includes an AWS KMS encryption profile, but does not enable it automatically. Losing or misconfiguring the encryption key can make state unrecoverable. The encryption metadata and key-provider names also become part of the recovery contract.

### Transport encryption

Backend requests use TLS. This is distinct from at-rest encryption.

### Access control

Encryption does not stop an authorized `tofu` process from seeing decrypted values. Restrict who can run plans, read state, decrypt state, or change the key.

### Replay and loss

Encryption does not prevent restoring an old state snapshot, nor does it recover a corrupted/deleted snapshot. Versioning, lineage checks, and recovery procedures remain necessary.

## State boundaries are ownership boundaries

A single state file for an entire organization creates a large blast radius, slow plans, broad credentials, and coupled release schedules. Hundreds of tiny states create dependency sprawl and difficult discovery.

Choose boundaries around:

- one accountable owner;
- one change lifecycle;
- one credential scope;
- bounded failure and lock contention;
- outputs that can be published through a deliberate interface.

Atlas uses separate states for:

```text
bootstrap
foundation
workload-dev
workload-prod
```

The bootstrap changes rarely and owns the backend. The foundation owns account-local network, audit, keys, and shared edge resources. Workload states own environment-specific compute and data resources.

## Workspaces are not full environment isolation

Workspaces provide multiple state instances for one root configuration. They do not automatically provide different accounts, credentials, backend policies, variable review, or lifecycle. Atlas uses separate root stacks and backend keys for dev and prod because the isolation and release evidence should be explicit.

Workspaces remain useful for bounded cases, but “workspace name equals production safety” is not an acceptable control.

## Cross-state data sharing

`terraform_remote_state` can read root outputs from another state, but the reader generally needs access to the whole state object and sensitivity markings do not constrain backend access. OpenTofu documentation warns that remote-state data sources do not preserve the source state’s sensitivity boundary.

Prefer publishing required values through a narrower store or service where possible: parameter store, DNS, resource tags/data sources, or a platform catalog. If remote state is used, expose minimal root outputs, restrict backend access, and version the output contract.

## Partial apply and state write failure

An apply can create a remote resource and then fail before state is written. On the next plan, OpenTofu may propose creating it again. The response is not to rerun blindly.

Investigate provider/cloud activity. If the object exists and should be managed, add complete configuration and import it. If it is safe to delete, remove it deliberately and record the action.

A state write can also fail after remote operations. OpenTofu may write a local recovery state file. That file is sensitive incident evidence. Preserve it, stop writers, and reconcile it with the backend and cloud before pushing anything.

## State lineage and serial

Lineage distinguishes independent state histories. Serial increases as snapshots are written. A snapshot with a higher serial but wrong lineage is not a newer version of the same state.

The course model refuses to apply a saved plan when lineage or serial differs. Real OpenTofu also protects state consistency, but the operational process must preserve identity in evidence and recovery.

## Worked incident: the wrong backend key

An operator copies a stack directory and changes variables but forgets to change the backend key. Planning the new environment refreshes the old environment’s state and proposes broad replacement.

The plan’s resource count may look plausible. The decisive evidence is backend identity and state lineage, not the directory name.

Controls:

- backend configuration generated from an explicit environment record;
- preflight account/region/backend allowlist;
- state lineage and key printed in plan evidence;
- distinct apply roles;
- policy that rejects cross-environment resource tags and backend identity.

## Backup and restore rehearsal

State backup is only credible when restored and used to calculate a safe plan.

The Atlas rehearsal:

1. creates a new isolated backend key;
2. restores one historical object version to that key;
3. verifies checksum, lineage, and serial;
4. runs refresh-only planning;
5. compares object identities with the authoritative state;
6. deletes the rehearsal key after evidence is retained.

Do not practice by overwriting the authoritative production key.

## Incident reconstruction: two pipelines, two locks

A team migrates from DynamoDB locking to native S3 lock files. One developer
updates the backend configuration to `use_lockfile = true`; an older pipeline
still uses only the DynamoDB table. Both believe they hold the authoritative
lock and write the same state object.

This is not a theoretical “eventual consistency” problem. It is a coordination
contract split across versions of the backend configuration.

A safe migration has an overlap phase:

```text
old clients: DynamoDB lock
transition clients: S3 lock + DynamoDB lock
new clients: S3 lock
```

During overlap, a transition client acquires both mechanisms. Once every
writer uses the transition configuration and a baking period shows no old
client, the DynamoDB setting can be removed. The migration record identifies
all writers—not only repositories, but scheduled drift jobs, local operators,
and recovery tooling.

The lesson generalizes: changing a coordination protocol requires inventory of
participants and a mixed-version strategy. Editing one backend block does not
change every writer atomically.

## A state recovery decision tree

When a state incident occurs, the first question is not “which command repairs
it?” It is “which fact is uncertain?”

### Backend selection uncertain

Verify account, region, bucket, key, workspace prefix, and assumed role. A
perfect state file in the wrong backend is still the wrong state.

### Lock ownership uncertain

Identify the lock holder and process. A force-unlock can create a concurrent
writer. Terminate or confirm the original operation before clearing its lock.

### Lineage uncertain

Do not merge or push. Isolate both histories, compare remote IDs and backend
versions, and determine which lineage has authority. The course model rejects a
foreign lineage before serial comparison.

### Serial or latest write uncertain

Use versioned state objects and apply logs to reconstruct the sequence. A larger
serial is suggestive but does not automatically prove correctness if a wrong
lineage or target wrote it.

### Resource binding uncertain

Compare configuration addresses, state addresses, and remote IDs with a
read-only cloud inventory. Repair the binding only after the intended owner is
known.

### Sensitive material exposed

Treat the incident as credential exposure as well as state recovery. Rotate
secrets that appeared in state, review access logs, and reduce future state
content.

This decision tree is more valuable than memorizing `state push`, because the
same command can repair one incident and destroy evidence in another.

## Native encryption and recoverability

OpenTofu's native state encryption can protect local and remote state payloads
before backend storage. Backend-side KMS encryption protects the S3 object at
the storage service. They address different boundaries and can be combined.

Whichever profile is used, the recovery path must retain:

- encryption-method metadata;
- key-provider configuration;
- access to current and retired decryption keys for retained state versions;
- a tested transition path during key/provider rotation.

Rotating a key without retaining the ability to read older backend versions can
silently defeat the versioning strategy. Encryption configuration is therefore
part of state schema and recovery, not a decorative security option.

The dependency-light course checks the profile and transition records. It does
not claim compatibility with OpenTofu's encrypted-state wire format; the real
tool must perform that proof in the provisioned lane.

## Atlas capstone increment

Module 2 adds:

- a backend bootstrap stack;
- a state-lock simulator with owner and expiry evidence;
- versioned state fixtures;
- an encryption example using AWS KMS;
- restore and stale-lock runbooks;
- policy that rejects unversioned/unlocked backend profiles;
- tests for wrong lineage, stale serial, and lost-update scenarios.

## Completion standard

You are ready for Module 3 when you can explain who owns each Atlas state, which identity writes it, how it is locked, how it is encrypted, how it is restored, and which consumers can access its outputs.
