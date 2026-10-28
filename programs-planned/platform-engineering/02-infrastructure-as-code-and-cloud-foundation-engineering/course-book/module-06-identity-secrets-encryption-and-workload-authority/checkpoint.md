# Checkpoint — Identity, Secrets, and Encryption

## Required evidence

Retain:

- principal-to-role and role-to-resource matrix;
- trust-policy and permission-policy analysis;
- organization, boundary, session, resource, endpoint, and key-policy applicability table;
- successful required workload calls;
- denied adjacent and administrative calls;
- IMDSv2 launch evidence;
- secret lifecycle with value ownership outside OpenTofu state;
- KMS administration/use/recovery split;
- CI OIDC claim constraints;
- repository, user-data, plan/state-facing input, and evidence secret scan;
- cleanup of temporary sessions and test material.

## Decision defense

Trace one allowed and one denied request through every applicable policy layer. Explain why temporary credentials can still be dangerous, why KMS permission does not imply access to ciphertext, and why a policy that denies everything is not least privilege.

## Progression gate

You pass only when humans, CI jobs, and workloads obtain authority through explicit, short-lived trust paths and the Atlas runtime can perform all required actions while every adjacent foundation-mutating action fails.
