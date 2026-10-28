# Worked Answers — State and Recovery

## 1. Backend bootstrap

Backend initialization happens before the normal resource graph is available. The backend must exist so OpenTofu can read state before planning resources. Use a separate bootstrap root with local or other pre-existing state, then migrate later roots to the created backend.

## 2. State-only information

State records remote IDs, address associations, provider-instance references, observed attributes, schema versions, deposed replacement instances, lineage, serial, and outputs. Names/tags are not always unique or sufficient to reconstruct these relationships.

## 3. Force-unlock evidence

Identify lock owner, command, creation time, pipeline/run, backend key, and whether any process or provider operation is still active. Preserve the lock record, inspect cloud activity, obtain approval, and plan again after unlock. Age alone is not evidence of abandonment.

## 4. Unsafe rollback

An older snapshot can omit resources created later or remember objects already changed/deleted. Restoring it may propose duplicates or destructive reconciliation. Restore to an isolated key, refresh, compare identities, and only replace authority after review.

## 5. Encryption layers

S3/KMS encrypts the stored backend object and relies on AWS storage/key controls. Native OpenTofu encryption encrypts content before backend storage and also applies to plans where configured. Both require access control and key recovery; neither prevents replay or data loss.

## 6. Sensitive output

`sensitive` suppresses routine display but the underlying value can remain in state and be available to state readers or remote-state consumers. Do not place long-lived secrets in state merely because output is marked sensitive.

## 7. State boundary

Split when owners, credentials, release cadence, or blast radius differ. Do not split when two resources must change atomically under one owner and cross-state coupling would replace a clear graph with fragile output choreography.

## 8. Workspace limits

Workspaces change state identity but not necessarily account, region, credentials, policy, backend access, approval path, or source configuration. A wrong profile can still apply production from the dev workspace or vice versa.

## 9. Remote-state access

The reader typically needs backend access to the full source state, not only the declared output, and sensitivity metadata does not enforce storage-layer isolation. Publish narrow values elsewhere where possible.

## 10. Orphan after partial apply

First stop writers and inspect the object. If it should be managed, write complete configuration and use a reviewed import block. If it should not exist, delete it deliberately with cloud evidence. Do not simply rerun creation.

## 11. Lineage and serial

Lineage identifies a state history. Serial orders snapshots within that history. A snapshot from another lineage is not comparable merely because its serial is larger.

A recovery decision should therefore compare lineage first, then serial and object version, and reject a foreign lineage unless a deliberate migration proves the relationship.

## 12. Recovery rehearsal

Copy a chosen version into a new backend key, verify checksum/lineage/serial, initialize a read-only/restricted root against it, run refresh-only and normal plans, compare with authoritative object identities, retain evidence, and delete the rehearsal key. Never overwrite authority during practice.
