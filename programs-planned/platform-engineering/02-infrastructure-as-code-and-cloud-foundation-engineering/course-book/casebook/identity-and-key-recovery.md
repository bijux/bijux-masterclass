# Casebook — The Backup Exists but the Key Is Gone

Six months after a development environment is retired, an audit asks for one
Atlas result. The backup bucket still contains the object and prior versions.
The workload KMS key was scheduled for deletion during cleanup and is now gone.

## What the controls did prove

- S3 versioning retained the object.
- The object was encrypted at rest.
- The manifest checksum still identifies the expected ciphertext/object.

## What they did not prove

- retained decryption authority;
- key lifecycle aligned with data retention;
- recovery role access;
- successful restore after environment retirement.

The backup is durable but unusable.

## Design correction

Data and key retirement must be one dependency graph. Before key deletion:

1. inventory encrypted volumes, snapshots, objects, and state versions;
2. determine retention and legal obligations;
3. re-encrypt or copy retained artifacts under a surviving key where policy
   allows;
4. run a recovery test with the recovery role;
5. record artifact/key mappings;
6. wait through the key deletion window with alerts;
7. delete only after recovery responsibility has ended.

## Authority correction

The normal runtime role should not administer the key. A separate data-protection
owner controls key lifecycle, and a monitored recovery role can decrypt retained
backups. This reduces the chance that workload cleanup or compromise destroys
recovery authority.

## Lesson

Encryption creates a new dependency. A protected byte is not recoverable unless
the key, policy, identity, and procedure survive for the same retention period.
