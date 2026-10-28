# Exercises — Databases, Object Storage, and Operator Boundaries

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Choose managed service or in-cluster operator

Atlas needs PostgreSQL, the team has limited database operations expertise, and cross-region recovery matters. Which default is more defensible and why?

## 2. Draw the responsibility boundary

For an operator-managed PostgreSQL cluster, assign responsibility for Pod placement, PVCs, database replication, schema, backups, restore, and application correctness.

## 3. Choose object storage for artifacts

Why are immutable Atlas result artifacts usually better represented in object storage than on the database PVC?

## 4. Evaluate an operator status condition

An operator reports `Ready=True`, but replication lag is beyond the application’s RPO. Is the service ready?

## 5. Keep database credentials out of the storage layer

Which identities should access the database, backup repository, CSI backend, and KMS?

## 6. Plan an operator upgrade

What must be proven before upgrading a database operator and its CRDs?

## 7. Reject a false HA claim

A chart deploys three PostgreSQL Pods and a headless Service. Why is “highly available” unproven?

## 8. Compare filesystem and object semantics

A legacy tool expects rename, directory listing, and file locking. Can object storage replace its RWX filesystem transparently?

## 9. Design a database backup oracle

What should a backup test verify beyond the operator’s completed Job status?

## 10. Plan service exit and portability

How should Atlas avoid treating a managed database as an irreversible platform dependency?

## 11. Handle an operator outage

The database continues serving while its operator is down. Which functions are affected, and should the database be restarted?

## 12. Produce a data-service decision record

What must a decision record contain when choosing managed PostgreSQL over an in-cluster operator?
