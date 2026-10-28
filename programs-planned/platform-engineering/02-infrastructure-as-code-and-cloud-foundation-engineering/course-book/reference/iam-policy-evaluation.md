# Reference — IAM Policy Evaluation

Authorization in AWS is not determined by finding one `Allow` statement. A request is evaluated through the principal’s ability to obtain a session and through every applicable policy boundary.

## Two separate questions

### Can the caller obtain the identity?

Role trust and federation answer this question. Relevant evidence can include:

- trusted principal or identity provider;
- OIDC issuer, audience, subject, repository, branch, or environment claims;
- service principal for EC2;
- session duration;
- external ID or source identity;
- MFA or assurance conditions;
- organization/account restrictions.

A narrow permission policy is irrelevant if an untrusted actor can assume the role.

### What may the resulting session do?

The effective authorization can involve:

- organization service-control policy;
- resource-control policy where used;
- identity policy;
- permissions boundary;
- session policy;
- resource policy;
- VPC endpoint policy;
- KMS key policy or grant;
- service-specific ownership and condition rules.

An explicit deny dominates. In the absence of a decisive deny, the request still needs the relevant allow across the required policy types.

## A practical decision trace

For a request such as `s3:PutObject` to the Atlas backup prefix:

1. **Session validity** — did the instance obtain the intended runtime role?
2. **Organization ceiling** — is the action allowed by organization policy?
3. **Boundary/session limits** — do a permissions boundary or session policy exclude it?
4. **Identity policy** — does the role allow `PutObject` on the exact result prefix?
5. **Bucket policy** — is the principal admitted and is TLS required?
6. **KMS policy** — when SSE-KMS is used, may the principal generate a data key under the required context?
7. **Endpoint policy** — if traffic uses a VPC endpoint, does that policy admit the bucket/action?
8. **Service conditions** — do account, region, tags, encryption headers, or source constraints match?

The denial record should identify the decisive explicit deny or missing permission. “IAM denied it” is too vague to repair safely.

## Least privilege requires positive and negative proof

A policy that denies everything is not useful. Test adjacent actions:

| Request | Expected |
|---|---|
| write result object to `results/` | allow |
| abort its multipart upload | allow |
| list every bucket | deny |
| delete backup bucket | deny |
| read another environment’s secret | deny |
| schedule KMS key deletion | deny |
| mutate state backend | deny |

The negative cases should be close enough to the required capability to expose wildcard resources, broad prefixes, or service-wide permissions.

## Resource and condition scope

Action names are only one dimension. Least privilege also constrains:

- exact resource ARN or prefix;
- account and region;
- principal tags or session claims;
- source identity;
- transport security;
- encryption key and context;
- source VPC endpoint or service;
- request tags where safely controlled.

Do not rely on a tag for authority when the same principal can change the tag and escape the boundary.

## KMS is a separate authority graph

An IAM allow for `kms:Decrypt` can still fail because the key policy does not enable IAM delegation, a grant or context is missing, or the ciphertext was encrypted under another key. Conversely, key permission does not grant access to the S3 object or EBS volume containing ciphertext.

Separate:

- key administration: policy changes, grants, rotation configuration, deletion scheduling;
- key use: encrypt, decrypt, re-encrypt, data-key generation;
- recovery: controlled access when the ordinary platform path is unavailable.

The workload should use the key but not administer or delete it.

## Plan and apply identities

A planning identity usually needs read access to existing objects and data sources. An apply identity needs controlled mutation. Separate them so a review can bind the proposal to a target and so untrusted pull-request code cannot silently gain apply authority.

CI trust should constrain issuer, audience, repository, branch/environment, workflow identity, and—when supported—source identity. Avoid broad subjects that allow forks or arbitrary branches to assume the role.

## Course evaluator boundary

The Python evaluator in this course models only the action/resource/condition features used by Atlas fixtures. It is an executable explanation and regression oracle, not a replacement for AWS policy simulation or real API tests. Real-cloud evidence must exercise successful and denied calls with the actual identities and policies.

## Final rule

For every powerful identity, be able to state:

```text
who can obtain it
for how long
from which context
which resources it can change
which adjacent actions are denied
who can revoke or recover it
which logs prove its use
```

If one answer is missing, the authority boundary is incomplete.
