# Exercises — Identity and Secrets

## 1. Trust versus permission

Distinguish a role trust policy from a permission policy.

## 2. Temporary credential risk

Why can temporary EC2 credentials still be dangerous?

## 3. Policy layers

Explain the relationship among SCP, boundary, session policy, and identity policy.

## 4. Role separation

Why should plan and apply use different roles?

## 5. Backup writer

Give a least-privilege permission set for writing backups to one S3 prefix.

## 6. Sensitive marking

Why is `sensitive = true` not a state-secrecy control?

## 7. Secret lifecycle

Design a secret lifecycle that does not require OpenTofu to hold the value.

## 8. IMDSv2 scope

What do IMDSv2 token requirements protect, and what do they not protect?

## 9. KMS roles

Separate KMS key administrator and key user responsibilities.

## 10. KMS failure

Why can `kms:Decrypt` in an IAM policy still fail?

## 11. CI trust claims

What claims should constrain a CI OIDC trust policy?

## 12. Negative matrix

Design a negative-test matrix for the Atlas workload role.
