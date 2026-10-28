# Module 10 — Delivery, Policy, Testing, and Cloud-Foundation Release

The final module turns a set of HCL files into an operated infrastructure product. A foundation is trustworthy only when changes can be proposed, reviewed, tested, applied with the intended authority, verified in the data plane, recovered when they fail, and handed to the next course without losing the meaning of its guarantees.

The governing question is:

> Can another engineer reproduce, review, release, recover, and extend Atlas Cloud Foundation without depending on the original author’s memory or cloud-console history?

## Learning outcomes

You will be able to:

- design a CI/CD path that separates source validation, plan authority, approval, apply authority, and post-apply proof;
- bind an approved saved plan to source, dependency lock, target, policy, and evidence;
- use short-lived federated CI identity rather than stored cloud access keys;
- build policy checks that reject high-confidence hazards without pretending to replace architecture review;
- combine static validation, module tests, plan tests, integration tests, and data-plane tests;
- manage provider locks, module versions, release records, and reproducibility evidence;
- reason about cost estimation and quota checks as release inputs;
- handle partial apply, failed verification, rollback, and roll-forward honestly;
- produce a Course 2 final defense and exact Course 3 handoff;
- distinguish dependency-light, local, and real-cloud evidence in the final claim.

## The release pipeline is an authority pipeline

A typical infrastructure pipeline is described as stages:

```text
format → validate → plan → approve → apply
```

The more important view is authority:

```text
untrusted change author
    can propose source

validation runner
    can read source and run local checks

plan runner
    can read target state and remote configuration

reviewer/policy
    can approve a specific proposal

apply runner
    can mutate one declared target using the approved proposal

verification runner
    can exercise the resulting data plane with bounded credentials
```

A single administrator credential used for every stage destroys this separation even if the CI interface shows multiple jobs.

## Source-to-apply binding

An approved plan is meaningful only for a specific context. Atlas records:

- source commit/digest;
- module package digests;
- provider lock digest;
- OpenTofu version;
- backend/state identity and serial;
- target account and region;
- variable-set digest excluding secret values;
- saved plan digest;
- policy result;
- reviewer identity;
- approval time and expiry;
- apply role class.

The apply job accepts that saved plan. It does not rerun `plan` after approval against potentially changed source or dependencies.

A saved plan can still become stale if remote state changes. Locking and serial checks constrain this risk, and the apply result must be handled as a new fact rather than assumed from the earlier plan.

## Federated CI identity

The preferred Course 2 AWS lane uses workload federation from the CI system to AWS. The trust policy restricts repository/project, branch or environment, audience, and other available claims. The session is short-lived and tagged for audit.

Separate roles support:

- read/plan;
- apply to non-production;
- apply to production;
- verification;
- emergency recovery.

A repository secret containing a long-lived AWS access key is a rejected candidate.

The exact federation implementation depends on the CI provider. The course models trust claims and permissions separately so that GitHub Actions, GitLab CI, or another runner can be mapped without changing the core argument.

## What belongs in validation

### Formatting and syntax

Fast, deterministic checks catch parse and style failures. They provide no cloud behavior evidence.

### Initialization and dependency lock

`tofu init` resolves providers/modules according to constraints and the lock file. The lock file is reviewed and committed. A provider checksum change is a supply-chain event, not noise.

### Static policy

Atlas rejects or reviews plans with conditions such as:

- public SSH without a bounded exception;
- wildcard actions/resources in high-risk IAM statements;
- unencrypted state or data storage;
- deletion of the state backend, audit destination, or protected data;
- metadata tokens optional;
- workload in a management account;
- missing ownership/cost tags;
- route to the internet from a data-only subnet;
- replacement of a critical resource without a migration record;
- unbounded retention or missing cleanup owner.

Policy checks are strongest for explicit, machine-readable invariants. They are weaker for questions such as whether one account is the right business boundary or whether a NAT design is worth its cost. Those remain architecture decisions.

### Module tests

OpenTofu tests can instantiate modules with test variables and assert outputs or plan properties. Course 2 also uses dependency-light Python tests for the conceptual models so learners can run useful proofs without a cloud account.

Module tests should cover:

- valid baseline;
- invalid CIDRs;
- duplicate subnet identities;
- forbidden public routes;
- missing tags;
- policy boundaries;
- optional feature combinations;
- moved/import compatibility fixtures.

### Plan tests

A plan is evaluated for action classes, replacements, sensitive changes, cost-affecting resources, and policy. Golden plan snapshots are used sparingly because provider normalization can make them brittle. Prefer semantic assertions over complete text comparison.

### Integration tests

A disposable environment validates provider behavior, permissions, and resource relationships. It needs a budget, lease/TTL, owner, isolated state, and cleanup proof.

### Data-plane tests

These verify DNS, TLS, routing, job acceptance, worker completion, backup, and restore. They are the closest Course 2 evidence to the service the foundation exists to support.

## Policy outcome vocabulary

Atlas uses four outcomes:

```text
pass
    evidence establishes the rule

review
    change may be valid but requires an accountable decision

fail
    high-confidence rule violation blocks release

not-executed
    required evidence was unavailable; never converted to pass
```

A percentage score cannot compensate for a failed state-protection or public-ingress rule.

## Cost and quota as release evidence

A plan can be secure and still be unaffordable or impossible to apply.

The pipeline records:

- resources that have recurring cost;
- expected class of cost, not a fabricated exact bill;
- environment budget;
- quota current use and limit;
- temporary replacement headroom;
- NAT, ALB, data transfer, storage, backup, and logging effects;
- cleanup owner and TTL for ephemeral environments.

Provider price changes and usage patterns make static cost estimates uncertain. The release decision marks the evidence class and assumptions.

## Apply concurrency and environment leases

Only one apply may mutate a state at a time. Backend locks protect state operations, but the pipeline also serializes environment releases and records an owner.

Ephemeral environments receive:

- unique identity;
- creation time;
- owner;
- maximum lifetime;
- budget;
- cleanup job;
- exceptions for retained forensic evidence.

A cleanup system must not destroy an environment still used by an active test or incident. Lease extension is explicit and audited.

## Partial apply and failed verification

An apply can fail after creating some resources. A successful apply can be followed by failed data-plane verification.

The incident flow is:

1. stop automatic promotion;
2. retain state/backend version and apply log;
3. inventory actual resources;
4. classify whether the environment is safe, degraded, or exposed;
5. contain urgent risk;
6. plan from current reality;
7. choose roll-forward, targeted restoration, or controlled rollback;
8. rerun complete verification;
9. record the final state and cleanup.

Blindly rerunning apply may be correct for an idempotent transient failure, but it is a decision, not the default answer.

## Rollback is not always inverse apply

Infrastructure changes may be irreversible or stateful:

- data deleted;
- key rotation changed decryption authority;
- DNS cached;
- provider schema upgraded;
- resource replacement changed identity;
- a new module wrote data;
- consumers adopted a new endpoint.

A release record distinguishes:

- **configuration rollback:** deploy prior declared configuration;
- **application rollback:** send traffic to prior workload release;
- **data recovery:** restore state/data from protected evidence;
- **roll-forward:** fix current generation;
- **containment:** reduce exposure while deciding.

The correct action depends on the mechanism and facts.

## Foundation release contents

Atlas Cloud Foundation 1.0 is not “the repo at a commit.” It is a manifested release containing:

- version ledger;
- foundation requirements inherited from Course 1;
- architecture decisions;
- module and root-stack source digests;
- provider lock digest;
- backend identity and recovery procedure;
- accepted plan and policy report;
- account/region target;
- image and launch contract;
- request-path proof;
- backup/restore proof;
- known limitations;
- cleanup and ownership records;
- Course 3 handoff.

## Final architecture defense

The learner must defend ten decisions:

1. Why is each state boundary separate?
2. Why are accounts/roles divided as shown?
3. How does a packet reach Atlas and leave it?
4. Which identity can read each secret and why?
5. How is a host replaced?
6. How is acknowledged data restored?
7. Which changes are blocked automatically and which require review?
8. How is drift classified and reconciled?
9. What does the release prove in a sandbox, and what remains unproved?
10. Which exact artifacts does Course 3 receive?

The defense is successful only when answers cite evidence, not slogans.

## Course 3 handoff

Course 3 studies OCI containers and software supply chain. It receives a bounded handoff rather than the entire Course 2 repository.

The handoff includes:

- Atlas application/runtime inventory;
- host process and port contract;
- filesystem and volume contract;
- runtime identities and required cloud permissions;
- network ingress/egress contract;
- image-release and bootstrap boundary;
- secret-source contract;
- logging/health contract;
- supported architectures;
- artifact and release requirements;
- known host-to-container migration risks;
- version ledger and manifest.

Course 3 must preserve the cloud foundation’s identity, data, network, and evidence boundaries while changing the packaging/runtime abstraction.

## Release evidence as a graph

The final dossier can be read as dependencies:

```text
source and dependency identities
        ↓
state and target identity
        ↓
saved plan
        ↓
policy, cost, quota, and approval
        ↓
apply result or explicit not-executed status
        ↓
data-plane and recovery evidence
        ↓
release claim
        ↓
Course 3 handoff
```

If one node changes, downstream evidence may no longer apply. A new provider
lock invalidates the old plan. A new plan invalidates policy approval tied to
the previous digest. A different account invalidates network and IAM evidence.
This graph prevents the final report from becoming a folder of unrelated green
files.

## The final claim

A dependency-light completion can truthfully say:

> Atlas Cloud Foundation 1.0 has a validated architecture, deterministic
> semantic proofs, tested local workload/recovery mechanisms, reviewed HCL,
> and a complete Course 3 handoff. AWS control-plane and data-plane execution
> remain not executed in this environment.

An AWS-backed completion may add the exact applied target and observed
behaviors. Neither route may claim multi-account containment, zone failure, or
regional recovery unless those experiments were actually run.

## Atlas capstone final result

Course 2 finishes with:

```text
Atlas Cloud Foundation 1.0
├── bootstrap state foundation
├── account and authority model
├── VPC and subnet architecture
├── DNS and public edge
├── workload identity and KMS boundaries
├── replaceable Atlas host
├── durable data and recovery path
├── CI/policy/release model
├── migration and incident runbooks
└── exact Course 3 handoff
```

## Completion standard

You complete the course when a clean checkout can reproduce the dependency-light proofs; a provisioned sandbox can produce a reviewed plan and, when authorized, an applied/verified foundation; the final release states every unexecuted proof honestly; and another learner can begin Course 3 without reconstructing hidden decisions.
