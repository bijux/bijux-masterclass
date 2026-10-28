# Data migration review

A migration dossier identifies source, target, authoritative generation, compatibility window, copy mechanism, verification, cutover, rollback boundary, and retirement policy.

## Separate dimensions

Do not hide several changes inside one phrase. List changes to:

- application schema and data representation;
- database engine or version;
- filesystem or block format;
- StorageClass, CSI driver, or backend;
- region, zone, account, or encryption key;
- backup and restore tooling;
- service endpoint and client routing.

## Authority sequence

State exactly when the target becomes authoritative. Before that point, rollback may discard the target. After target writes begin, rollback requires reverse replication or an explicit data-loss decision. Record fencing or write-freeze evidence.

## Verification

Use checksums, counts, log positions, schema checks, referential integrity, representative reads/writes, tenant boundaries, and restore evidence. The verification should detect failures specific to the copy method.

## Automation boundary

GitOps can reconcile surrounding resources, but one-shot data transitions require stable operation identity, explicit completion state, and protection against automatic replay or pruning.
