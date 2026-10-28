# Module 4 — Landing Zones, Accounts, Identity, and Guardrails

A cloud foundation is not a VPC with a naming convention. It is the boundary within which identities, audit evidence, policies, budgets, accounts, networks, and workloads can be created and changed without giving every workload authority over the organization.

This module moves Atlas from “a sandbox account exists” to an explicit landing-zone model. The course does not attempt to create an AWS Organization from the same account-local stack that deploys Atlas. Organizational control and workload delivery have different authorities and lifecycles.

## Learning outcomes

You will be able to:

- explain why cloud accounts are security, billing, quota, and failure boundaries;
- design a small multi-account structure without copying a large-enterprise diagram blindly;
- distinguish workforce identity, workload identity, organization policy, and resource policy;
- explain what service-control policies do and do not do;
- separate management, audit, log archive, shared services, sandbox, non-production, and production responsibilities;
- design centralized evidence without granting the log producer control over the archive;
- model account vending, quarantine, and retirement;
- place budgets, quotas, regions, tags, and ownership in the foundation rather than adding them after incidents;
- know which claims require an actual organizational environment.

## Why accounts are architectural boundaries

An AWS account provides independent namespaces and boundaries for many services, policies, quotas, billing records, and blast-radius controls. It is not a perfect security boundary by itself, but it is stronger than tagging every resource in one account and hoping all policies filter correctly.

Separate accounts help when:

- production and development need different change authority;
- security evidence must be protected from workload administrators;
- a compromised workload must not create organization-wide identities;
- quotas and costs need accountable ownership;
- data classification or regulatory policy differs;
- teams need independent release cadence;
- one environment must be suspended or closed.

Too many accounts also create cost, identity, DNS, network, and support overhead. The account model should follow ownership and policy, not an arbitrary “one microservice, one account” rule.

## A minimal Atlas organization

The reference architecture uses these account roles:

```text
Organization management
├── Security OU
│   ├── Log Archive
│   └── Audit / Security Tooling
├── Infrastructure OU
│   ├── Shared Services
│   └── Network (introduced only when central networking is justified)
├── Workloads OU
│   ├── Atlas Non-Production
│   └── Atlas Production
└── Sandbox OU
    └── Learner / Experiment account
```

The management account should perform organization administration and little else. Running ordinary workloads there increases the consequence of credential or policy mistakes.

The course’s executable AWS lane can run in one sandbox account. The organization diagram is a design and policy artifact unless the learner has a dedicated multi-account lab.

## Organization units express policy scope, not team charts

An OU groups accounts for policy application. An OU should represent a control boundary such as production, sandbox, suspended, or security—not necessarily mirror every reporting line.

Moving an account between OUs can change effective policy immediately. That movement is a production change and requires plan, review, and rollback reasoning.

## Service-control policies set a ceiling

An SCP limits which actions principals in member accounts can perform. It does not grant permissions. A principal needs an IAM allow and must not be blocked by an applicable SCP or other explicit deny.

A policy that denies disabling CloudTrail can protect audit continuity. A policy that denies all services not yet approved can also break recovery when an incident requires a new service or region. Guardrails need owners, test accounts, exceptions, and rollback.

Course 2’s policy examples focus on high-confidence controls:

- deny leaving the organization;
- restrict root-user actions in member accounts;
- deny disabling required audit services;
- deny unapproved regions with documented global-service exceptions;
- deny creation of long-lived IAM access keys where feasible;
- require selected encryption controls for high-risk resources.

The exact production policy is organization-specific. The course evaluator verifies policy intent and exception metadata, not every AWS IAM nuance.

## Workforce identity is not workload identity

### Workforce identity

Humans authenticate through IAM Identity Center or an external identity provider, then assume short-lived roles. Roles distinguish read, plan, apply, security audit, billing, and break-glass responsibilities.

### Workload identity

EC2 receives a role through an instance profile. CI receives a role through OIDC or another federated workload identity. Neither should reuse a human’s credentials.

### Break-glass identity

A tightly controlled emergency path with strong authentication, monitored use, short session duration, and post-use review. “AdministratorAccess in a shared password vault” is not a sufficient design.

## Plan and apply authority should differ

A plan job needs read access to state and cloud configuration plus the ability to calculate proposed changes. An apply job needs mutation authority. Separating them reduces the consequence of unreviewed pull-request code.

The release record binds approval to:

- source digest;
- plan digest;
- target account/region;
- apply role class;
- policy result.

The apply runner should not accept arbitrary source after plan approval.

## Centralized audit needs asymmetric authority

The workload account can produce CloudTrail and flow logs, but should not be able to delete or rewrite the central archive. A log-archive account, bucket policy, retention policy, and restricted KMS key establish a stronger boundary.

Centralization is not complete merely because a trail exists. Verify:

- all required regions and management/data events;
- delivery status;
- destination ownership;
- object-lock/retention decisions where required;
- key access;
- monitoring of trail changes;
- restore/query capability.

Course 2’s account-local baseline sends evidence to an account-local protected bucket because multi-account execution is optional. The architecture record clearly marks that limitation.

## Account vending is a lifecycle

Creating an account is the first transition, not the product.

A governed account lifecycle includes:

1. request and accountable owner;
2. account email and identity setup;
3. OU placement and inherited policies;
4. logging, security tooling, and cost controls;
5. network/DNS integration;
6. baseline roles;
7. workload onboarding;
8. quarantine when ownership or security fails;
9. data/resource cleanup;
10. closure and retained evidence.

A platform that creates accounts but cannot quarantine or retire them accumulates unmanaged authority.

## Region policy and global services

Restricting regions can reduce data-placement risk and operational surface. Some services are global or use region-specific control endpoints. A naïve deny can block IAM, Route 53, CloudFront, support, or organization functions unexpectedly.

Model region policy from documented service behavior, test in a sandbox OU, and retain an explicit exception list. “Deny all regions except eu-central-1” is not production-ready by itself.

## Ownership tags are useful but not authority

Atlas requires tags such as:

```text
atlas:owner
atlas:environment
atlas:system
atlas:managed-by
atlas:data-classification
atlas:cost-center
```

Tags support inventory, cost allocation, policy conditions, and incident routing. Tags can be missing, wrong, or changed. Do not rely on them as the only tenant or security boundary.

A tag policy can standardize keys/values, but enforcement and remediation differ by service. The course checks required tags in planned resources and separately verifies remote inventory in Level C.

## Budgets and quotas belong in the foundation

A budget is not a hard spending limit, but it creates visibility and escalation. Atlas uses low sandbox thresholds and environment-specific ownership.

Quota evidence includes:

- current limit;
- current use;
- required headroom for replacement;
- request lead time;
- fallback resource/region strategy.

A rollback that requires temporarily running old and new generations needs double capacity. If the quota permits only one, `create_before_destroy` cannot deliver the intended safety.

## Provider aliases and organizational authority

An organization root may use multiple AWS provider aliases for management, log archive, audit, and workload accounts. This is powerful and dangerous.

```hcl
provider "aws" {
  alias  = "workload"
  region = var.region

  assume_role {
    role_arn = var.workload_apply_role_arn
  }
}
```

Every module call receives the intended provider explicitly. A default provider accidentally pointing at the management account is unacceptable.

Atlas Course 2 separates organization-design artifacts from account-local execution so the common learner path cannot mutate Organizations.

## Worked decision: one account or three?

A small team proposes one account for dev, prod, and logs to reduce overhead.

Questions:

- Can dev administrators alter production IAM?
- Can a compromised prod role delete its own audit logs?
- Can a runaway dev load exhaust production quotas?
- Can billing identify ownership?
- Can production policy be stricter without blocking dev experimentation?

If the answers require fragile tag conditions and broad shared roles, separate accounts are justified. If the team cannot yet operate multiple accounts, the honest interim design records the shared blast radius and a migration trigger rather than claiming equivalent isolation.

## Compromise exercise: production role becomes administrator

Assume the Atlas production instance role is accidentally changed to
`AdministratorAccess` and the process is compromised.

In a one-account design, the attacker may reach:

- production data and network resources;
- development resources and credentials;
- audit trails and their destination;
- IAM roles used by deployers;
- account-level security tooling;
- quota-consuming resources.

In the Atlas multi-account design, the role remains dangerous inside the
production workload account, but organization policy, independent audit data,
and other workload accounts remain under different authorities. The account
boundary does not eliminate the incident; it contains it and preserves evidence
needed for response.

Now ask a harder question: can the production administrator assume a role in
the log archive? If cross-account trust is broad, the diagram's separation is
illusory. Account design and trust policies must be reviewed together.

## Policy staging

An SCP can prevent recovery just as effectively as it prevents misuse. Atlas
uses a policy-staging OU/account for changes with broad effect.

A policy promotion record includes:

1. intended risk addressed;
2. exact policy digest;
3. affected OUs/accounts;
4. allowed/denied action vectors;
5. global-service and recovery exceptions;
6. staging evidence;
7. monitoring and rollback;
8. accountable approver.

The tests include positive vectors because a policy that denies the bad action
and every legitimate action is not successful.

## The minimum viable landing zone depends on operation

A two-person project may not be able to operate seven accounts immediately.
The honest design can begin with:

```text
management (no workloads)
security/log archive
sandbox/non-production
production
```

and add specialized accounts when ownership or scale justifies them. The
important properties are:

- no ordinary workload in management;
- audit authority separated from the workload it observes;
- production change authority separated from experimentation;
- an account lifecycle and quarantine path;
- centralized identity with short-lived roles;
- explicit migration triggers for the interim compromises.

Copying a large enterprise OU tree without people to operate it creates
abandoned controls. A smaller governed structure is more mature than a larger
fiction.

## Atlas capstone increment

Module 4 adds:

- `organization-model.json` with account/OU ownership;
- provider-alias and role-assumption profiles;
- mandatory tag and budget policy;
- account preflight checks;
- audit-destination ownership model;
- accepted and rejected SCP fixtures;
- account lifecycle runbook;
- a sandbox root that refuses management-account execution.

## Completion standard

You can continue when you can trace a human plan, approved apply, workload API call, log delivery, security audit, and emergency action to different identities and authorities—and state which parts remain unproven without a multi-account environment.
