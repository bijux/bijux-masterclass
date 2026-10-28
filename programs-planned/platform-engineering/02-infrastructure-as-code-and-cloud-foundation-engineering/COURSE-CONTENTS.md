# Course Contents

## Course 2 — Infrastructure as Code and Cloud Foundation Engineering

This course is a complete reader-first successor to **Linux, Networking, and Cloud Systems Engineering**. It consumes the exact Course 1 handoff and turns its host, network, storage, identity, and failure-domain requirements into **Atlas Cloud Foundation 1.0**.

The course book is the authoritative product. The OpenTofu configuration, semantic models, fixtures, tests, local Atlas runtime, and optional AWS lane exist to make the book’s claims falsifiable.

## Reader product

- **78 navigated course-book pages** and approximately **49,000 words**;
- one orientation module and ten complete teaching modules;
- **120 transfer exercises** with **120 matching worked answers**;
- ten full engineering laboratories plus the orientation laboratory;
- ten evidence checkpoints plus the orientation gate;
- a cumulative Atlas Cloud Foundation walkthrough;
- incident casebooks for concurrent state writers, egress failure, KMS recovery, and partial edge apply;
- guides for plan review, account safety, cost and quota control, and evidence journals;
- references for state recovery, CIDR design, IAM evaluation, module interfaces, migrations, provider comparison, and release review;
- instructor notes, assessment rubric, final defense, and misconception catalogue.

## Ten-module progression

1. **Declarative Infrastructure and the OpenTofu Execution Model** — configuration, graph, providers, unknown values, plans, applies, and data-plane proof.
2. **State, Backends, Locking, Encryption, and Recovery** — lineage, serials, native S3 lock files, version recovery, partial apply, and incident handling.
3. **Module Design, Interfaces, and Composition** — typed module APIs, provider ownership, flat composition, semantic versioning, and migration.
4. **Landing Zones, Accounts, Identity, and Guardrails** — account boundaries, organization policy, audit authority, plan/apply separation, quotas, and lifecycle.
5. **Network Foundation: Addressing, Routing, Egress, and DNS** — flow-first design, stable zone identity, NAT, endpoints, IPv4/IPv6, filtering, and DNS ownership.
6. **Identity, Secrets, Encryption, and Workload Authority** — trust policies, permission evaluation, temporary credentials, KMS authority, secret boundaries, and CI federation.
7. **Compute, Images, Bootstrap, and Replacement** — image acceptance, launch templates, IMDSv2, replacement, data attachment, patching, and readiness.
8. **Edge, Data Protection, Backup, and Recovery** — DNS/TLS/ALB request paths, health and draining, storage classes, RPO/RTO, backup manifests, and empty-target restore.
9. **Drift, Import, Refactoring, and Infrastructure Migrations** — difference classification, refresh-only review, import, moved addresses, state splits, provider upgrades, and expand–transition–contract changes.
10. **Delivery, Policy, Testing, and Cloud Foundation Release** — source-to-plan binding, federated CI, policy outcomes, cost/quota evidence, partial apply, release dossier, and Course 3 handoff.

## Executable product

The capstone contains:

- the immutable nine-file Course 1 predecessor handoff;
- Course 1’s Atlas API, worker, HTTPS edge, PKI fixtures, and durable spool runtime;
- a provider-neutral semantic model for plans, state, locks, modules, organizations, networks, IAM, compute, backup, drift, cost, quota, and release decisions;
- an AWS/OpenTofu reference lane pinned to OpenTofu 1.12.5 and AWS provider 6.58.0;
- remote-state bootstrap with KMS, S3 versioning, public-access blocking, TLS-only policy, lifecycle retention, and native lock-file profile;
- flat modules for naming, network, identity, audit, data protection, workload, and edge responsibilities;
- separate foundation and workload roots;
- stable availability-zone-ID mapping and semantic subnet identities;
- workload identity, KMS key, private compute, optional HTTPS edge, encrypted durable volume, versioned backup bucket, and account-local audit lane;
- deterministic plan/state/network/IAM/cost/release fixtures;
- import and moved-address migrations;
- accepted, rejected, review-required, and not-executed release candidates;
- ten planted infrastructure defects with named rejecting proofs;
- state, KMS, network, partial-apply, and recovery runbooks;
- a manifested thirteen-file handoff to Course 3.

## Proof routes

```bash
make doctor
make predecessor-proof
make test
make hcl-check
make links-proof
make capstone-tour
make core-proof
make manifest-proof
```

Environment-backed routes are deliberately separate:

```bash
make tofu-proof
make aws-preflight
make aws-plan-foundation
make aws-plan-workload
make docs-build
```

No default target creates cloud resources. AWS apply and destroy commands require explicit opt-in variables and a passing account/region preflight.

## Evidence classes

- **A — dependency-light semantic and static proof:** executed in the release environment;
- **B — native OpenTofu proof:** requires the pinned CLI and initialized provider dependencies;
- **C — AWS sandbox proof:** requires a disposable, budgeted account and creates billable resources;
- **D — organizational foundation proof:** requires multiple accounts, delegated administration, centralized evidence, and identity federation.

The verification record reports these classes separately. A Level A pass is never represented as proof that AWS accepted an API call or that a real data plane behaved correctly.
