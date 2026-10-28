# Module 4 — Repository topology, artifact promotion, and environment lineage

## Central question

**How should source, artifacts, desired state, and environment approvals be arranged so that a promotion changes one reviewed fact instead of rebuilding or rediscovering the candidate?**

Repository topology is often treated as a matter of taste. It is actually an authority and failure-domain design. A repository boundary changes who can approve a revision, which credentials automation needs, how history is retained, how blast radius is limited, and whether a compromised build job can write directly to production desired state.

## Four different products

Atlas distinguishes four products even if a small organization initially hosts them in one Git service:

1. **application source** — code, tests, build definition, and developer review;
2. **artifact catalogue** — immutable image and chart digests plus supply-chain evidence;
3. **configuration source** — KRM, Kustomize overlays, Helm values, policy inputs, and environment references;
4. **release evidence** — promotion decision, render digest, test subjects, approvals, and runtime observations.

Combining these products is not automatically wrong. Failing to distinguish their authority is wrong. A build job that needs to push an image does not automatically need permission to merge production configuration. A GitOps controller that reads production configuration does not automatically need read access to application source or signing keys.

## Application repository and environment repository

A common design uses one repository for application code and another for environment desired state. The application repository publishes an immutable release proposal: image digest, chart digest, compatibility notes, and evidence references. The environment repository selects that proposal for dev, staging, or production.

This separation gives environment owners an independent review boundary. It also introduces coordination cost. If every development change needs synchronized pull requests across several repositories, teams may bypass the process. The answer is not necessarily to merge repositories; it is to automate candidate proposal and evidence propagation while preserving human-readable review.

A monorepository can preserve the same separation through paths, ownership rules, workflows, and credentials. Repository count is less important than authority and immutable identity.

## Environment-per-directory versus environment-per-branch

Both patterns are common.

### Environment directories

```text
environments/dev
environments/staging
environments/prod
```

One commit can change several environments, which is useful for atomic policy changes and dangerous for accidental broad promotion. History is easy to compare. Branch protection and path ownership must prevent a dev automation identity from modifying production.

### Environment branches

```text
dev
staging
production
```

Promotion can be represented as merge or cherry-pick across branches. The same path resolves differently by branch, which can complicate local review, automation, and GitOps source configuration. Long-lived branches drift and accumulate merge conflicts. A force push can rewrite release history unless prohibited.

Atlas uses environment directories in one configuration repository and represents promotion as a narrow change to an immutable release reference. The repository policy requires separate approval for production paths.

## Promotion is selection, not transformation

A correct promotion record states:

```text
candidate identity
source commit
image and chart digests
rendered-set digest for the target environment
required evidence
approver and policy result
time and predecessor release
```

Promotion may change environment-specific configuration, such as hostname or replica count, but it must not rebuild workload artifacts. If a different environment requires a different binary, the architecture has created environment-specific builds and must justify why. Configuration should be externalized enough that one artifact can move through the intended environments.

The phrase “promote the tag” is unsafe. A tag is a discovery label. The desired state must pin the digest observed during approval. Image automation may select a tag according to policy, but its Git commit should write the corresponding digest or an evidence record that binds tag to digest at selection time.

## Revision lineage

Every environment revision has a predecessor. Atlas records a release lineage graph rather than relying only on chronological Git history. The graph answers:

- which production revision followed which previous production revision;
- which candidate was rejected or superseded;
- whether a revert selected an earlier desired revision or created a new forward revision;
- which data migration phases were active;
- which artifact and render identities were retained.

A Git revert creates a new commit that applies inverse source changes. It is not the same commit as the earlier state, and it may render differently when external inputs or tool versions have changed. The release record therefore stores exact identities and does not assume that `git revert` reproduces prior bytes automatically.

## Pull requests as release evidence containers

A production promotion pull request should be reviewable without reconstructing evidence from several dashboards. Atlas generates a release summary containing:

- candidate and predecessor identities;
- source and rendered diffs;
- artifacts and signatures;
- policy decisions;
- schema and API compatibility;
- storage and migration phase;
- progressive-delivery plan;
- rollback and break-glass boundaries;
- unresolved `not-executed` evidence.

A reviewer should see what will change and what will not. Large generated diffs should be attached as artifacts and summarized by identity and risk, not dumped into an unreadable comment.

## Promotion gates and environments

Dev, staging, and production are not merely replica-count profiles. They have different evidence obligations.

Dev may accept a candidate after structural validation and basic runtime tests. Staging should exercise production-like identity, network, storage, migration, and telemetry paths. Production requires evidence from the same immutable subjects plus explicit approval and current recovery gates.

A staging pass expires when relevant facts change. Examples include:

- image or chart digest;
- render digest;
- policy version;
- migration set;
- secret authority;
- cluster API version;
- significant environment topology.

Evidence freshness is part of the policy. A six-month-old restore drill should not remain valid forever simply because the backup manifest path is unchanged.

## Automated image updates

Automation can scan registries, select versions, and propose Git changes. This is useful for dependency and security updates, but it changes the trust path.

The image automation identity should:

- read only approved repositories and metadata;
- select according to a declared policy;
- write only candidate paths or dedicated branches;
- create a reviewable commit with tag and digest;
- never bypass compatibility or production approval;
- record why a version was selected;
- avoid force updates and deletion refspecs.

Automatic production merge is appropriate only when the policy, test coverage, rollback boundary, and impact class support it. “Patch version” is not itself a low-risk proof.

## Repository availability and cluster continuity

A GitOps controller may continue serving the last applied state during a repository outage. That is a valuable property. It also means the repository is not the runtime data plane. The platform should define:

- how long reconciliation may remain stale;
- how stale desired state is reported;
- whether new cluster bootstrap is possible during the outage;
- how repository credentials are recovered;
- whether source artifacts are cached and integrity-checked;
- which emergency actions are allowed.

A repository outage should not trigger automatic deletion or replacement of known-good workloads. “Cannot fetch desired state” is not evidence that desired state is empty.

## Signed commits and review identity

Commit signatures can strengthen identity evidence, but signatures do not prove that the content is safe or that the signer was authorized for the target environment. Atlas separates:

- cryptographic commit identity;
- repository account and branch protection;
- code-owner approval;
- policy evaluation;
- artifact and render evidence;
- environment authorization.

A valid signature from the wrong actor is still unauthorized. An unsigned emergency commit may be acceptable only under an explicit incident policy and must be remediated afterward.

## Repository topology anti-patterns

### Production desired state generated only in CI

If the exact production render exists only as an ephemeral CI artifact, the controller cannot independently reproduce or verify it. Store an immutable rendered artifact or all immutable render inputs and a deterministic toolchain.

### One mutable values file per environment with unbounded overrides

This makes environment behavior opaque and difficult to compare. Values should be schema-validated and the rendered diff should remain small and intentional.

### Cluster credentials in the application pipeline

This bypasses the pull reconciler, expands credential distribution, and makes observed state depend on pipeline availability. The pipeline should publish candidates; the in-environment controller should reconcile them.

### Git history as the only release database

Git preserves revisions, but release decisions, evidence expiry, runtime observations, and incident state require structured records linked to commits.

## Atlas promotion contract

Atlas Delivery Plane requires:

1. artifact build and environment promotion are separate authorities;
2. production references immutable image and chart digests;
3. each promotion has a predecessor and evidence subject set;
4. render inputs and tool versions are recorded;
5. environment path ownership is explicit;
6. automation proposes or performs only policy-authorized changes;
7. repository outage preserves last-known-good runtime state and reports staleness;
8. reverts create new release records and re-evaluate compatibility.

Module 5 gives these repository and promotion records to the primary reconciliation engine: Argo CD. The new question is how application inventory, health, synchronization, ordering, and prune policy behave once a controller continuously observes the source.

## Deep-dive practicum

### Repository shape follows authority and failure containment

There is no universally correct “app repo versus config repo” answer. Repository boundaries should make decision authority and blast radius visible. Atlas conceptually separates application source, immutable artifact publication, and environment desired state. A small organization may store them in one repository with protected paths and distinct workflows; a larger organization may use separate repositories. The invariant is that a source-code merge cannot silently become production desired state without the promotion gates.

A repository topology should make these questions cheap to answer:

- Which commit selected the production artifact?
- Which evidence subject was reviewed?
- Which environments inherit the same base?
- Which actor can change a production destination or controller scope?
- Which commit reverts a failed selection?
- Which external dependencies can alter rendering without a local diff?

If the answers require reconstructing CI logs that may expire, the repository is not carrying enough release lineage.

### Promote subjects, not recipes

Rebuilding in each environment tests the recipe repeatedly but loses artifact identity. Atlas promotes an artifact set: API image digest, worker image digest, chart or source artifact digest, and policy evidence subjects. Environment-specific rendering may differ in replicas, hostname, or resource class; the workload bytes do not.

This separation lets the release record say:

```text
artifact set X
was rendered by renderer Y version Z
with environment input E
into desired-set digest D
```

A changed artifact set is a new candidate, even if the semantic version remains the same.

### Pull requests are evidence containers, not gates by themselves

A pull request records discussion and approval, but its usefulness depends on the generated evidence. For a production promotion, the review should include:

- predecessor and candidate identities;
- exact artifact-set equality with the tested environment;
- rendered diff and object inventory;
- policy and schema results;
- data compatibility phase;
- restore and secret-adoption gates;
- target fleet compatibility;
- rollback frontier and abort owner.

A reviewer should not need to trust a bot’s “all checks passed” summary without inspectable subjects and results.

### Merge, rebase, and environment lineage

Environment branches often drift because hotfixes, automated image updates, and manual cherry-picks create unrelated histories. Atlas prefers a monotonic promotion record rather than assuming branch ancestry alone proves environment order. The record links candidate to predecessor and lists the unchanged artifact set.

When a production incident requires a revert, create a new commit that selects the prior safe desired state. Do not rewrite production history. The revert preserves the failed decision and the recovery sequence. If data crossed the rollback frontier, select a forward-fix candidate instead and record why the prior revision is no longer safe.

### Repository outage and last-known-good state

The controller should continue serving the last reconciled workload when the source is temporarily unavailable. Automation that generates target lists or prunes inventory must distinguish “source unavailable” from “source contains no targets.” A mirror or cached source can improve availability, but failover must preserve commit identity and trust policy.

A repository is part of the platform’s control plane. Its backup, recovery, key rotation, protected-branch configuration, audit retention, and incident ownership deserve the same rigor as a Kubernetes component.
