# Module 6 — Identity, Secrets, Encryption, and Workload Authority

Cloud networks do not create authority. IAM does. A private instance with an administrator role can be more dangerous than a public instance with no useful credentials. This module builds the identity and key boundaries that let Atlas operate without embedding long-lived secrets in code, state, images, or user data.

## Learning outcomes

You will be able to:

- separate human, pipeline, workload, backup, and audit identities;
- read IAM trust and permission policies as different contracts;
- reason through SCPs, permissions boundaries, session policies, identity policies, resource policies, endpoint policies, and KMS key policies;
- use short-lived role sessions instead of static keys;
- attach least-privilege authority to EC2 through an instance profile;
- require and validate IMDSv2 behavior;
- keep secrets out of OpenTofu state where possible;
- distinguish KMS key administration, key use, grants, rotation, and deletion;
- design cross-account access and CI federation deliberately;
- prove denial paths rather than only successful access.

## Identity begins with the actor and purpose

Atlas defines these principal classes:

| Principal | Purpose | Explicitly not allowed |
|---|---|---|
| `foundation-plan` | read state/cloud and calculate plan | mutate foundation |
| `foundation-apply` | apply approved foundation plan | arbitrary organization admin |
| `workload-instance` | read declared configuration, write backup/result objects | change network/IAM/state |
| `backup-writer` | write/verify backup objects | read unrelated data or delete retention |
| `audit-reader` | inspect logs and evidence | mutate workload |
| `break-glass` | bounded emergency action | routine deployment |

Do not begin from a managed policy and ask where it can be attached. Begin from an action/resource/condition table derived from the workload.

## Trust policy and permission policy answer different questions

A role trust policy says **who may obtain the role**. Attached permission policies say **what the resulting session may do**.

For EC2, the trust principal includes the EC2 service. The role is placed in an instance profile attached at launch.

For CI, the trust policy validates an OIDC issuer and constrains subject, repository, branch/environment, and audience claims. A trust policy that accepts any subject from a large CI organization creates broad mutation authority even when the role’s action policy is narrow.

## IAM evaluation is layered

A useful mental model:

```text
organization ceiling (SCP)
        ∩
permissions boundary
        ∩
session policy
        ∩
identity/resource allows
        −
any explicit deny
```

KMS key policies and VPC endpoint policies add resource/service-specific gates. A role policy allowing `kms:Decrypt` is insufficient if the key policy does not allow the principal or delegation path.

Use the IAM policy simulator and real negative API calls in a sandbox, but remember that not every service condition or resource policy is fully modeled by one simulator.

## Least privilege includes resource and condition scope

Bad:

```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

Atlas workload needs a narrow set such as:

- `s3:PutObject` to one backup prefix;
- `s3:GetObject` only when restore behavior requires it;
- `kms:GenerateDataKey`/`kms:Decrypt` on one key with service/context conditions;
- selected SSM/Secrets Manager reads for named configuration paths;
- CloudWatch log/metric writes if used.

List and object actions often require different ARN forms. Test both expected allow and expected deny.

## Temporary credentials are not automatically safe

An EC2 role supplies temporary credentials through IMDS. Any compromised process able to reach IMDS may use the role’s authority. Least privilege, process isolation, metadata controls, and egress policy remain necessary.

Atlas launch configuration requires:

```text
HttpEndpoint: enabled
HttpTokens: required
HttpPutResponseHopLimit: 1 for direct host workload profile
InstanceMetadataTags: disabled unless explicitly needed
```

A containerized future profile may require a different hop limit. That decision belongs to Course 3/4 and must be justified, not copied blindly.

Do not store secrets in EC2 user data. Instance metadata/user data are accessible to software on the instance and are not a secret store.

## Provider credentials remain outside HCL

The AWS provider uses the standard credential chain and, for apply, assumes a named role. Configuration records the role ARN or account contract, not access keys.

```hcl
provider "aws" {
  region = var.region

  assume_role {
    role_arn     = var.apply_role_arn
    session_name = "atlas-foundation-apply"
  }
}
```

`apply_role_arn` is not secret. The credentials used to assume it are short-lived and external.

## Secret values and OpenTofu state

If a resource argument contains a secret, the provider may store it in state even when the variable is marked sensitive. Avoid generating or retrieving application secrets through ordinary resource/data-source attributes unless the provider supports write-only or ephemeral semantics and the lifecycle is understood.

Preferred pattern:

1. OpenTofu creates the secret container and access policy.
2. A dedicated secret-injection/rotation process writes the value.
3. The workload reads it at runtime with its identity.
4. Rotation does not require reapplying the whole foundation.

When OpenTofu must create an initial secret, record the state exposure and migration plan.

## Parameter Store versus Secrets Manager

Both can hold configuration; Secrets Manager provides secret-specific rotation integrations and pricing. Parameter Store supports hierarchical parameters and secure strings. The choice depends on rotation, size, access pattern, cost, and operational ownership.

Neither service removes the need for:

- resource policy/identity policy;
- KMS key policy;
- caching/refresh behavior;
- failure handling when the service is unavailable;
- redaction from logs;
- deletion/recovery policy.

## KMS establishes another authority graph

Separate:

- key administrators who change policy/rotation/deletion;
- key users who encrypt/decrypt or generate data keys;
- service principals that use the key on behalf of resources;
- auditors who inspect configuration and usage.

Key deletion has a waiting period but can still make data permanently unreadable. The plan policy rejects scheduled deletion and key replacement without a migration record.

Automatic rotation changes backing key material while preserving key identity for supported key types. It is not the same as changing application secrets or re-encrypting every object immediately.

## Encryption context and service conditions

KMS conditions can restrict use to a service, account, ARN pattern, or encryption context. These conditions can prevent a broadly usable decrypt permission from becoming a universal decryption oracle.

Be careful: a condition that does not match the service’s actual request context can cause runtime failure. Test with real service calls.

## Cross-account access

Cross-account S3/KMS access typically requires permission on both sides:

- source principal can assume/use a role or call the resource;
- destination resource/key policy trusts the principal/account;
- organization/SCP/boundary permits it;
- endpoint policy and network path permit it.

Atlas’s future central log archive and backup designs use delivery-only authority from workload accounts and separate read/admin authority in the destination account.

## CI federation

A pipeline should obtain short-lived credentials through OIDC, with trust conditions bound to:

- issuer;
- audience;
- repository/project;
- branch, tag, or protected environment;
- workflow identity where supported.

The apply role is not available to every pull request. Untrusted contributions can run static checks and perhaps read-only plans in a separate environment, but cannot mint production mutation credentials.

## Worked incident: secret copied into a variable

A module accepts `database_password`, marks it sensitive, and passes it to a resource. A learner sees no password in terminal output and concludes it is protected.

The value appears in state, plan, CI artifacts, crash logs, and possibly provider debug logs. The fix is architectural: create a secret container and workload permission; inject/rotate the secret outside the general foundation apply; scrub existing artifacts and rotate the credential.

## Atlas identity module

The module owns:

- EC2 workload role and instance profile;
- scoped backup/config permissions;
- optional permissions boundary attachment;
- policy documents generated from explicit resource ARNs;
- outputs containing role/profile identity, not credentials.

The root owns provider role assumption. The data-protection module owns key and bucket policies while accepting the workload principal as an input.

Policy rejects:

- wildcard administrative actions;
- IAM user access keys;
- secrets in variable defaults or user data;
- IMDSv1 allowance;
- workload permission to mutate state/network/IAM;
- KMS deletion without migration;
- unbounded CI trust subjects.

## Policy decision trace

Atlas worker calls:

```text
secretsmanager:GetSecretValue
arn:aws:secretsmanager:eu-central-1:100000000005:secret:atlas/dev/db
```

A complete decision can involve:

1. the instance profile's role trust allows EC2 to assume the role;
2. the role session is valid and not restricted by a session policy;
3. the identity policy allows the action on the dev secret ARN;
4. an applicable permission boundary permits it;
5. an organization SCP does not deny it;
6. the secret resource policy permits the principal if one is present;
7. the secret's KMS key policy and grant path permit decryption;
8. resource/condition tags match;
9. no explicit deny applies.

The course evaluator implements only a documented subset of identity-policy
logic. It is useful for positive and negative design vectors, but it cannot
replace AWS's policy simulator or live call evidence. The limitation is a
feature of honest teaching: learners see which layer the small model omits.

## Negative permissions define least privilege

A role is not demonstrated least-privilege because one required action works.
Atlas verifies adjacent denials:

```text
allowed
    read atlas/dev configuration
    read atlas/dev secret tagged dev
    write atlas/dev backup prefix
    use atlas/dev workload key

denied
    read atlas/prod configuration
    list all secrets
    write another backup prefix
    administer or delete the KMS key
    create IAM roles
    change routes or security groups
```

These negative vectors are retained with the release. When the workload gains a
new feature, the permission change is reviewed against both the required
positive vector and the expanded attack surface.

## CI OIDC trust is code execution authority

A CI trust policy that accepts any repository in an organization may allow a
less protected repository to assume the production apply role. Claims need to
bind the intended repository/project, branch or protected environment,
audience, and workflow context available from the provider.

The CI identity flow is:

```text
reviewed source
→ protected CI job
→ signed OIDC assertion
→ AWS role trust evaluation
→ short-lived role session
→ plan or apply permissions
```

The AWS role still needs narrow permissions, and the CI system itself becomes a
security dependency. Federation removes stored cloud keys; it does not make
untrusted pipeline code safe.

## Secret rotation without infrastructure replacement

A database password should rotate through the secret owner and application
reload/restart path, not require changing an OpenTofu variable that copies the
value into state.

A rotation design answers:

- how old and new values overlap;
- whether the consumer caches credentials;
- how the consumer detects a new version;
- how failure rolls back;
- which audit event identifies use;
- when the old value is revoked;
- whether backup or logs contain the old value.

OpenTofu may provision the secret container, access policy, and rotation
integration. It should not become the secret delivery channel.

## KMS recovery trap

Suppose the workload key is scheduled for deletion during cleanup while old
snapshots still depend on it. The backup objects remain, but recovery will fail
when the key is gone.

The data-retention and key-retention plans must be joined. Decommissioning
checks all encrypted dependents before key deletion, retains a cancellation
window, and records which recovery roles can decrypt. A key is not merely an
attribute of an encrypted resource; it is a long-lived authority dependency.

## Atlas capstone increment

Module 6 adds the identity module, KMS key profile, secret-container example, OIDC trust fixture, IMDS policy, IAM evaluator, and negative access vectors.

## Completion standard

You are ready for Module 7 when every Atlas API call can be traced to a principal, session source, policy path, resource scope, and expected denial—and no workload or pipeline secret must be embedded in configuration.
