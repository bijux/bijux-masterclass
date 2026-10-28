# Worked Answers — Identity and Secrets

## 1. Trust versus permission

The trust policy controls which principal/service/federated identity may assume the role. Permission policies control actions the resulting session may perform. Both must be correct; broad trust can expose a narrow role to unintended callers.

## 2. Temporary credential risk

Any compromised process with metadata access can obtain and use them until expiry. Temporary lifetime reduces persistence but does not replace least privilege, metadata protection, process isolation, and monitoring.

The correct question is not whether credentials expire, but which actions and resources a stolen session can reach before expiry and how quickly misuse is detected.

## 3. Policy layers

SCP and permissions boundary cap possible authority; session policy can further restrict one session; identity/resource policies supply allows; any applicable explicit deny wins. Service-specific key/endpoint policies can add gates.

A defensible authorization trace lists every applicable layer for one concrete request and identifies the exact allow or deny that determines the outcome.

## 4. Role separation

Plan can run with read-oriented access on untrusted proposed source. Apply mutation authority is issued only for an approved plan/source digest. This reduces pull-request code’s ability to change infrastructure.

The release record must bind the apply session to the reviewed plan digest and target account so that approval cannot be replayed for different infrastructure.

## 5. Backup writer

Allow required object write/multipart actions to `arn:aws:s3:::bucket/atlas-backups/*`, perhaps bucket-location/list limited to the prefix, and KMS data-key/encrypt operations on one key under S3/context conditions. Deny deletion/retention changes.

Test both the intended upload and forbidden read, delete, cross-prefix, and key operations with the actual runtime identity.

## 6. Sensitive marking

It hides routine display but does not guarantee the provider omits the value from state/plan. State readers and artifacts may still expose it.

The decisive proof is to inspect the machine-readable plan and resulting state under the exact provider version, not rely on terminal redaction.

## 7. Secret lifecycle

OpenTofu creates secret container, KMS policy, and workload access. A dedicated rotation process writes versions. The workload reads current value at runtime and refreshes safely. Foundation state never contains the secret value.

## 8. IMDSv2 scope

Session tokens and request mechanics reduce certain SSRF/proxy paths and can enforce v2-only access. They do not authenticate individual host processes or make an overprivileged instance role safe.

A negative test should show that IMDSv1 is rejected while an authorized process can still obtain a v2 token and use only the role’s narrow permissions.

## 9. KMS roles

Administrators manage policy, rotation, alias, and lifecycle. Users perform bounded cryptographic operations. Audit principals read configuration/events. Deletion authority is tightly separated and reviewed.

Recovery evidence must also prove that a surviving role can decrypt backups before a deletion window closes; a key that no one can administer is not resilience.

## 10. KMS failure

The key policy may not trust the principal, an SCP/boundary may deny it, the encryption context or service condition may not match, the key may be disabled, or cross-account resource policy may be absent.

## 11. CI trust claims

Issuer, audience, repository/project, protected branch/tag/environment, workflow identity, and possibly actor/ref conditions. Avoid wildcard subjects that include forks or arbitrary pull requests.

Evaluate an allowed protected-branch token and denied fork, unprotected branch, wrong audience, and alternate workflow tokens against the trust policy.

## 12. Negative matrix

Prove the workload cannot mutate IAM, network, state bucket, KMS policy, or other backup prefixes; cannot use IMDSv1; cannot read unrelated secrets; cannot delete backup objects; and cannot assume the foundation apply role.
