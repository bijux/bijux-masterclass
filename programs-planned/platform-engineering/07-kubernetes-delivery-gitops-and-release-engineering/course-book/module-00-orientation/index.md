# Orientation — lock the predecessor and build the delivery laboratory

Course 7 begins with a refusal: you are not allowed to improve delivery by weakening the guarantees inherited from Course 6. The predecessor handoff is therefore not background reading. It is an input contract.

Atlas Data Plane 1.0 identifies resources that ordinary prune logic may not delete, release phases that automation may not reorder, recovery evidence that promotion may not ignore, and credentials that delivery controllers may not acquire. Before you create an Argo CD `Application`, a Flux `Kustomization`, a Helm chart, or a promotion workflow, verify the handoff byte-for-byte:

```bash
make predecessor-proof
```

A GitOps controller has broad write authority over Kubernetes resources. That authority is useful only when its boundary is narrower than the failure it is meant to prevent. Course 7 therefore separates five identities:

1. **source revision identity** — the Git commit, OCI artifact digest, chart digest, and referenced workload image digests;
2. **render identity** — the exact set of canonical Kubernetes objects produced by a named renderer version and input set;
3. **delivery application identity** — the inventory owner, destination, sync policy, and permissions under which reconciliation occurs;
4. **observed cluster identity** — the actual object UIDs, generations, managed fields, status, and controller-generated mutations;
5. **release decision identity** — the evidence bundle and approval that allowed one desired revision into one environment.

When those identities are collapsed into “the version,” diagnosis becomes guesswork. A source commit can render differently after a remote base moves. Two commits can render the same set. A cluster can be synchronized to a rendered set whose image tag later resolves to different bytes. A resource can be healthy while a migration is not backward compatible. A release can be technically successful and still violate the data-owner contract.

## The mandatory local lane

The dependency-light laboratory uses tools already present in a normal development environment:

- Git for immutable local history;
- Python for deterministic render, inventory, promotion, and release models;
- Go for a small compiled drift and inventory probe;
- YAML and JSON for desired-state and evidence documents.

This lane does not emulate every Helm, Argo CD, or Flux behavior. It isolates the invariants that those tools must preserve. Native lanes add evidence when the relevant binaries and clusters are available.

## The Atlas repositories

The capstone uses three logical repositories even when they are represented as directories in one teaching archive:

```text
atlas-source
    application source and tests

atlas-artifacts
    immutable OCI images, charts, and evidence subjects

atlas-environments
    reviewed desired state for dev, staging, and production
```

Course 7 never rebuilds an application during promotion. A production promotion changes the environment repository so that production references the same immutable image and chart subjects already exercised in staging. If bytes change, the result is a new candidate and must repeat the required evidence.

## Native tool lanes

The pinned reference lane uses Kubernetes 1.36.2, Helm 4.2.3, Kustomize 5.8.1, Argo CD 3.5.0, Flux 2.9.4, Argo Rollouts 1.9.1, SOPS 3.13.3, and External Secrets 2.9.0. A learner may use later supported patch versions, but must record the exact versions and re-run compatibility checks.

Argo CD is the primary implementation lane because its `Application`, `AppProject`, health, sync, and fleet concepts make application ownership visible. Flux is the comparative lane because its separate source, Kustomize, Helm, notification, and image controllers make the reconciliation graph visible. Neither tool defines GitOps by itself.

## Your first evidence dossier

Before Module 1, create `reports/orientation.json` containing:

- predecessor manifest digest;
- local Git version;
- available native tools;
- selected primary lane;
- selected environment evidence class;
- exact course version pins;
- unresolved limitations.

A missing native tool is not a failure. Hiding that it is missing is a failure.

## The evidence ledger you will maintain

Before the first module, create one release ledger rather than ten unrelated lab notes. Each row describes a transition in the same Atlas release. Record the subject that changed, the authority that approved it, the controller or tool that acted, the observation that followed, and the claim that observation can support. For example, a Kustomize render can support a claim about the exact desired resource set; it cannot support a claim that a Pod became Ready. An Argo CD health observation can support a claim about Kubernetes resource conditions; it cannot support a claim that a restored database contains the right rows.

Use five evidence classes throughout the course:

1. **reasoned** — derived from a documented model without executing the mechanism;
2. **static** — obtained from parsing, rendering, schema validation, or policy evaluation;
3. **local executable** — obtained from the deterministic Python and Go reference lanes;
4. **cluster-backed** — obtained from real Kubernetes controllers in a bounded cluster;
5. **operated** — obtained from the organization’s actual repositories, identity systems, clusters, telemetry, and incident process.

A stronger class is not automatically better for every question. A cluster run can still be irrelevant if it observes a different artifact digest or ignores the data migration. The discipline is to match the evidence to the claim.

## A release is a graph, not a button

The object you will manage is a graph of immutable subjects and observations:

```text
source commit
  ├── image digests
  ├── chart or Kustomize source digest
  └── policy and test evidence
          ↓
rendered resource-set digest
          ↓
controller inventory and sync result
          ↓
resource health and actual traffic
          ↓
journey, data, restore, and security gates
          ↓
release decision
```

Every edge needs an owner. If an image automation controller proposes a newer image, it has created a candidate edge; it has not acquired production promotion authority. If a GitOps controller removes a resource from its inventory, it has observed a desired-set change; it has not acquired the data owner’s authority to destroy a retained recovery object. This graph becomes the connective tissue of every chapter and the final defense.

## How to study the two controller families

Argo CD and Flux are both present because their architectures expose different lessons. Argo CD presents an application-oriented view with explicit sync and health. Flux decomposes source, Kustomize, Helm, image, and notification concerns into collaborating controllers. Do not copy every example twice. Study the common invariant first, then use the second implementation to test whether your reasoning depended on one product’s vocabulary.

Select one primary lane for the full capstone. In the comparative lane, complete the design reviews and at least one failure laboratory. The objective is not product certification. It is the ability to identify source identity, rendered identity, inventory, field authority, health, prune scope, secret custody, promotion authority, and recovery behavior regardless of controller choice.

## Completion standard

You are ready to begin Module 1 only when you can state, without using the word “deploy” as a shortcut, how a Course 6 workload digest becomes an environment revision and which facts remain outside GitOps authority. You must also be able to verify the predecessor handoff, identify every protected resource class, and explain why an unavailable desired-state source is not an empty desired-state source.
