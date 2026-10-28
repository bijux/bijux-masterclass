# Module 6 — Flux controller composition, sources, and image automation

## Central question

**How does a GitOps system behave when source acquisition, rendering, Helm lifecycle, notification, and image updates are separate controllers connected by Kubernetes APIs?**

Flux exposes GitOps as a toolkit of controllers rather than one application object. This architecture makes the reconciliation graph explicit. It also means that readiness, dependency, versioning, and failure must be reasoned about across several custom resources.

## Source artifacts are first-class

The source-controller reconciles Git repositories, OCI repositories, Helm repositories, buckets, and related sources into immutable artifacts. Downstream controllers consume the artifact identified in status, not an abstract repository name.

A source object records:

- URL and authentication reference;
- revision selector;
- reconciliation interval;
- verification policy where configured;
- produced artifact revision and digest;
- readiness and failure conditions.

A Git branch may be the selection policy, but the artifact status should expose the resolved commit. OCI sources can be pinned by digest. If the source is not Ready, downstream reconciliation should not interpret the desired state as empty.

## Kustomization as reconciliation unit

Flux `Kustomization` refers to a source artifact and path, then builds and applies Kubernetes resources. It has its own interval, timeout, prune, target namespace, health checks, dependencies, decryption, and ServiceAccount impersonation.

This makes several policies explicit per reconciliation unit. Atlas uses separate Kustomizations for platform prerequisites, data-plane resources, and Atlas workloads. `dependsOn` expresses that one unit should become Ready before another begins.

Dependencies must remain acyclic. A dependency graph is not a transaction. If downstream application reconciliation fails after infrastructure becomes Ready, the upstream state remains.

## Health and readiness expressions

Flux can assess health for named resources and supports expressions for dependency readiness in current releases. A readiness expression is code. It must use current generation and authoritative conditions rather than matching a vague status string.

Atlas tests readiness expressions against success, progress, failure, and stale-status fixtures. An expression that returns Ready for a stale observed generation is rejected.

## Post-build substitution

Flux supports post-build variable substitution for Kustomizations. This can make environment configuration convenient and render identity difficult. Substitution values may come from ConfigMaps and Secrets, meaning output depends on live cluster objects rather than only source artifacts.

Atlas prohibits unrecorded production substitution. If substitution is used, the exact values source, resource version or digest, and rendered output become part of the release identity. Secrets should not be exposed in rendered evidence.

## HelmRelease

Flux `HelmRelease` is reconciled by helm-controller. Unlike Argo CD's common renderer-only Helm use, this path preserves Helm release semantics, remediation, tests, and stored release state.

A HelmRelease specifies chart source, version or digest policy, values, interval, install and upgrade behavior, tests, drift detection, and remediation. Atlas pins chart identity and distinguishes install failure, upgrade failure, test failure, and health failure.

Remediation settings can retry, uninstall, or roll back. Those actions remain bounded by the same data and side-effect constraints studied in Module 3. A rollback cannot reverse an irreversible migration merely because helm-controller restored older manifests.

## OCIRepository and artifact composition

OCI sources allow desired state and charts to be distributed as immutable artifacts. This can improve reproducibility and decouple reconciliation from a large Git checkout. It also shifts review and promotion into the artifact publication path.

Atlas uses Git as the human review ledger and permits OCI desired-state artifacts only when their provenance links back to the reviewed commit and their digest is recorded in the environment revision.

## Notification and event handling

Flux notification-controller can publish events and receive external triggers. Events provide useful feedback but should not become the sole release database. Reconciliation is still interval- and source-driven; a missed webhook should delay observation, not permanently lose the change.

Alert routing must avoid leaking secret values or full rendered manifests. Event metadata should include source revision, object identity, reason, and controller, with bounded cardinality.

## Image reflection and policy

Flux image-reflector-controller scans registries and records image metadata. `ImagePolicy` selects a candidate according to semantic version, alphabetical, or numerical rules. Selection is not release approval. It is one automated proposal mechanism.

Atlas policies select only digests from approved registries and require the image's supply-chain evidence from Course 3. A version range can identify a candidate; signatures, provenance, compatibility, and environment policy decide whether it may progress.

## ImageUpdateAutomation

Image automation can edit files in a Git repository and push commits. This is powerful because it closes the loop from registry observation to desired-state proposal.

The automation identity should be constrained to:

- one repository and path;
- one branch or proposal branch;
- non-force updates;
- no deletion refspecs;
- deterministic commit messages containing old and new digest;
- signed commits where available;
- no direct production merge unless policy explicitly permits it.

The controller must handle concurrent human changes. A failed push should rebase or retry safely, not overwrite history.

## Controller composition and failure isolation

Flux controllers communicate through Kubernetes resources and status. This creates observable boundaries:

```text
GitRepository Ready
        ↓ artifact revision
Kustomization Ready
        ↓ applied inventory
HelmRelease Ready
        ↓ release outcome
Alert event
```

A source-controller outage can leave existing Kustomizations on their last artifact. A kustomize-controller outage stops apply but not source acquisition. A notification-controller outage loses feedback but not reconciliation. Diagnosis should identify the first non-Ready resource in the dependency graph.

## Multi-tenancy and impersonation

Flux Kustomizations and HelmReleases can reconcile under specified ServiceAccounts. This helps separate tenant authority. The source-controller and other shared controllers still have their own cluster permissions and cached content.

Course 8 will deepen multi-tenancy. In Course 7, Atlas ensures that reconciliation units target explicit namespaces and use bounded ServiceAccounts. A tenant source cannot reference a cluster-admin ServiceAccount or cross-namespace Secret without platform consent.

## Argo CD and Flux comparison

The useful comparison is conceptual:

| Concern | Argo CD tendency | Flux tendency |
|---|---|---|
| primary unit | Application | controller-specific custom resources |
| source and apply | combined in application view | explicit source artifact and reconciler |
| Helm | often renderer-only | HelmRelease lifecycle |
| fleet | ApplicationSet | Kustomization/HelmRelease topology and automation |
| feedback | application status and notifications | Kubernetes conditions and events |
| image automation | external or ecosystem integration | first-class Flux controllers |

Both can implement sound or unsound systems. Atlas preserves the same identities, promotion rules, protected resources, and evidence gates in both lanes.

## Flux failure patterns

### Dependency says Ready too early

A weak expression observes a stale condition and starts a downstream migration before the prerequisite generation is active.

### Substitution changes output without source change

A live ConfigMap changes, the Kustomization re-renders, and production output changes without an environment-repository commit.

### Image automation bypasses approval

A semver policy writes directly to production and a controller applies the candidate before compatibility evidence exists.

### Helm remediation repeats side effects

A retry or uninstall policy reruns a hook whose operation identity is not durable.

### Controller upgrade changes behavior

CRDs or rendering behavior change during Flux upgrade. Controller and CRD versions must move together, and the upgrade is itself a platform release.

## Atlas Flux profile

Atlas adopts these rules:

1. downstream reconciliation consumes immutable source artifacts;
2. every source status reports the resolved revision and digest;
3. Kustomization dependencies are acyclic and generation-aware;
4. production substitution inputs are explicit release subjects;
5. HelmRelease remediation cannot bypass data compatibility;
6. image policy proposes candidates but does not prove release eligibility;
7. image automation writes bounded, reviewable, non-destructive Git commits;
8. tenant reconciliation uses scoped ServiceAccounts;
9. controller and CRD upgrades are versioned platform releases;
10. diagnosis begins with the earliest failed resource in the controller graph.

Module 7 turns to the most sensitive inputs in the delivery graph: repository credentials, decryption keys, Secret material, artifact trust, and policy gates.

## Deep-dive practicum

### Flux exposes the control graph

Flux’s source-controller, kustomize-controller, helm-controller, image-reflector-controller, image-automation-controller, and notification-controller make ownership explicit. This decomposition is educationally valuable: a GitRepository can be Ready while a Kustomization fails; an ImagePolicy can select a candidate while no repository write occurs; a Receiver can miss a webhook while interval reconciliation still succeeds.

Diagnose the earliest unready artifact in the chain:

```text
source artifact
  → rendered artifact
  → applied inventory
  → health result
  → image candidate
  → proposed Git update
```

Do not jump directly to Pod logs when the source artifact never became available.

### Source artifacts are controller-produced release inputs

A Flux GitRepository produces a revisioned artifact. Downstream reconcilers consume that artifact, not a magical live Git tree. The source status therefore needs the resolved revision, digest, verification result, and last successful observation. An unavailable new revision should not erase the last successful artifact.

Atlas pins a commit in the reference GitRepository to make the course evidence deterministic. Branch tracking may be acceptable in development, but the resulting commit still becomes the observed source identity.

### Kustomization dependencies and readiness

`dependsOn` orders reconciliation readiness between Flux Kustomizations. It does not create a cross-resource transaction. If infrastructure became Ready and the application later failed, the infrastructure remains. Recovery must be safe from that partial state.

Health checks should name resources whose status represents the Kustomization’s purpose. Waiting for every object can make a controller block on resources that intentionally remain progressing. Waiting for none can report success before endpoints exist. Choose the health population deliberately.

### HelmRelease owns more than rendering

A Flux HelmRelease drives install and upgrade state using Helm semantics. Its remediation strategy can retry, rollback, or uninstall. Those actions interact with hooks, retained resources, and data compatibility. The same chart API and upgrade-history concerns from Module 3 still apply; placing Helm behind a controller does not remove them.

### Image automation is candidate generation

ImageRepository discovers available tags and digests. ImagePolicy chooses according to a policy. ImageUpdateAutomation writes a proposed configuration change. None of these observations prove production safety.

Atlas constrains automation to a staging candidate branch. A pull request then binds the selected digest to supply-chain evidence and environment gates. Direct production writes would combine discovery, selection, and promotion authority in one credential.

### Webhooks are latency optimizations

A Receiver can trigger faster source reconciliation. The interval remains the reliability path. Missing a webhook should delay observation, not permanently suppress it. Replaying a webhook should be harmless. This is the same design principle as event-driven systems: notification and authoritative state are separate.

### Comparative review

Map an Argo CD Application and a Flux Kustomization into the common Atlas model. Both need source identity, rendered set, inventory, field authority, health, prune policy, and recovery. The product-specific status objects differ. The release claim does not.
