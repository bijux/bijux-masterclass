# Module 3 — Helm chart engineering, packaging, and upgrade semantics

## Central question

**How can a chart provide a reusable configuration API without hiding unsafe behavior behind templates, values, hooks, or release state?**

Helm is often introduced as “templates for Kubernetes YAML.” That description is too small. A chart is a versioned package, a configuration API, a renderer, and—when used with Helm's release engine—a lifecycle system with stored release state, upgrades, rollbacks, hooks, tests, and dependency resolution.

A chart should be reviewed like a library. Its values are public inputs. Its templates are implementation. Its rendered resources are executable output. Its upgrade behavior is a compatibility promise.

## Chart API versus application API

A chart's values are not the application's HTTP API, but they are still an API consumed by operators and automation. Renaming `resources.requests.cpu`, changing a boolean into an object, or changing the meaning of `persistence.enabled` can break environment repositories even if the Kubernetes workload remains compatible.

Atlas defines a small chart surface:

- immutable API and worker image digests;
- replica and resource profiles;
- hostnames and Gateway references;
- external Secret references;
- storage-class and claim references;
- feature flags whose ownership is explicit.

The chart does not expose every Kubernetes field. A values file that mirrors the entire Deployment spec transfers platform invariants to every consumer and makes safe upgrades difficult.

## Chart structure

A stable Helm chart contains:

```text
Chart.yaml
values.yaml
values.schema.json
templates/
charts/ or declared dependencies
README and upgrade notes
```

`Chart.yaml` identifies chart name, version, application version, dependencies, and chart type. Chart version identifies the package. Application version is informational and must not be used as the workload artifact identity. Atlas still pins image digests explicitly.

`values.schema.json` turns implicit assumptions into validation. It can require digest-shaped image references, constrain replica ranges, reject unknown keys, and make mutually exclusive modes visible before rendering. Schema validation does not prove semantic compatibility, but it prevents a large class of accidental misconfiguration.

## Values design

Good values express decisions, not raw implementation detail. Compare:

```yaml
availabilityTier: critical
```

with:

```yaml
podDisruptionBudget:
  minAvailable: 2
strategy:
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
replicas: 3
```

The first is concise but transfers hidden policy into the chart implementation. The second is explicit but exposes several coupled knobs that can produce impossible combinations. A mature chart may offer a small policy profile plus deliberate advanced overrides, with validation that preserves invariants.

Atlas keeps the invariant close to the implementation: production requires enough replicas and disruption allowance to satisfy its availability tier. An override that violates the invariant is rejected rather than accepted because the template language can render it.

## Template discipline

Templates should be deterministic, readable, and boring. Overuse of functions, nested conditionals, dynamic lookup, and string-generated YAML makes review harder. A template should not query live cluster state to decide production output; that makes render identity depend on the observation point.

Use helpers for stable names, labels, and repeated fragments. Avoid helpers that conceal whole resources or construct arbitrary snippets from untyped strings. Quote values according to their Kubernetes schema, not by habit. Render optional blocks only when the absence has defined semantics.

The chart test suite renders representative values combinations and validates the complete object set. It includes at least:

- minimal supported configuration;
- production profile;
- each optional capability;
- invalid combinations expected to fail;
- upgrade fixtures from the previous chart version.

## Dependencies and ownership

Chart dependencies can be convenient for a self-contained demonstration and dangerous for platform ownership. Bundling PostgreSQL, an ingress controller, and a monitoring stack into an application chart can make one application release own shared infrastructure and stateful lifecycle it should not control.

Atlas does not package the database or GitOps controller as an application dependency. Their lifecycles, recovery, and permissions differ. The chart may declare an external service contract, not create every dependency it uses.

Dependencies must be pinned by version and, where supported, immutable OCI digest. A mutable repository index or range can resolve differently across environments.

## CRDs

CustomResourceDefinitions have cluster-wide lifecycle and compatibility implications. Helm treats files under `crds/` differently from templates: they are installed before templates and are not upgraded or deleted by ordinary chart lifecycle. Templating CRDs can provide more control but introduces ordering and ownership hazards.

A chart that uses a CRD should state whether it owns installation, merely consumes an existing API, or delegates CRD lifecycle to a platform component. Atlas application charts consume platform APIs; they do not own shared CRDs.

## Hooks are not a transaction manager

Helm hooks can run before or after install, upgrade, rollback, and delete. They are useful for bounded checks and carefully designed jobs. They are dangerous when used as an implicit database migration engine.

A hook may be retried, left behind, deleted according to hook policy, or rerun during rollback. If the operation is not idempotent and durably identified, the hook can repeat side effects. If the hook succeeds but the main release fails, application and data state may diverge.

Course 6 already defines an expand/backfill/cutover/contract protocol. Helm may deploy the jobs and record their status; it may not collapse the protocol into one opaque `pre-upgrade` script.

## Install, upgrade, wait, and atomic

Flags such as `--wait` and `--atomic` are useful but bounded. Waiting uses resource-specific readiness and timeout behavior. Atomic upgrade can roll back Kubernetes resources when an upgrade fails. It cannot reverse an external side effect, a completed data migration, a revoked certificate, or an event emitted to another system.

Release engineers should know which resources Helm tracks, what rollback revision contains, and which state exists outside Helm. In a GitOps system, the desired-state controller may also reapply the Git revision after an imperative Helm rollback, creating competing control loops. The durable rollback is a reviewed desired-state change.

## Chart tests

Helm test hooks can verify in-cluster behavior after installation. They are useful for protocol and connectivity checks but have their own identity, cleanup, and failure semantics. A passing test is one evidence source, not proof of all user journeys.

Atlas chart tests are bounded and non-destructive. They verify service reachability, version reporting, and dependency contracts without modifying authoritative data.

## OCI charts and immutable distribution

Helm charts can be stored as OCI artifacts. The release record should include the chart digest, not only `name:version`. A version is a human-facing compatibility label; a digest identifies bytes.

Promotion must reuse the same chart digest. Repackaging an identical chart source can change archive bytes and digest. If the chart digest changes, re-run the appropriate evidence even when templates render the same set.

The relationship among identities is:

```text
chart source commit
chart package digest
values revision
renderer version
rendered-set digest
```

Each answers a different question.

## Helm 4 considerations

Helm 4 is the current major release in the reference lane. Course 7 uses stable chart API conventions and avoids making the course dependent on optional plugin runtimes. Teams migrating from Helm 3 must test chart rendering, plugins, SDK integrations, storage behavior, and CI scripts against both the current and target versions. The chart contract is more stable than the surrounding toolchain only when compatibility is tested deliberately.

## GitOps integration

Argo CD and Flux can render Helm charts declaratively. In that mode, the GitOps controller—not a human running `helm upgrade`—owns reconciliation. Helm release-state semantics may differ depending on the integration:

- Argo CD commonly uses Helm as a template renderer and owns Kubernetes resources as an Application;
- Flux `HelmRelease` uses the Helm controller and preserves Helm release behavior.

This difference matters for hooks, rollback, tests, inventory, drift, and stored release history. “We use Helm” is not enough information to diagnose the system.

## Atlas chart contract

Atlas adopts these rules:

1. values are a small, versioned API with schema validation;
2. images and charts are selected by immutable digest;
3. shared infrastructure and CRDs are not silently owned by the application chart;
4. dynamic live-cluster lookups are forbidden in production rendering;
5. hooks cannot bypass the Course 6 migration protocol;
6. chart tests are bounded, non-destructive evidence;
7. upgrade fixtures test compatibility from the previous accepted chart;
8. GitOps integration mode is recorded because renderer-only and Helm-release behavior differ.

Module 4 places Kustomize and Helm artifacts into a complete repository and promotion model. The central question moves from “Can we render it?” to “How does the same candidate move through environments without mutation?”

## Deep-dive practicum

### A chart is a versioned API offered to operators

A Helm chart is not merely a folder of templates. Its values, generated resource identities, labels, hooks, ownership annotations, and upgrade behavior form an API. Renaming a value, changing its type, moving a resource between templates, or altering a default can break consumers even when the rendered Kubernetes objects remain valid.

Treat the chart as two contracts:

- **input contract** — values schema, defaults, supported combinations, and deprecations;
- **rendered contract** — object identities, selectors, immutable fields, ownership, hooks, and lifecycle.

The input contract is where `values.schema.json` earns its value. It rejects misspelled keys and mutable image references before rendering. It cannot express every cross-field invariant; for example, enabling persistence may require a StorageClass and a retention policy. Those checks belong in chart tests or policy.

### Upgrade safety is historical

`helm template` validates one desired snapshot. `helm upgrade` must reconcile that snapshot with release history and live objects. Risks include immutable field changes, resource renames, hook replay, ownership adoption, and CRD ordering. A chart can render correctly from an empty cluster and still fail as an upgrade.

A serious chart test matrix includes:

1. install from empty state;
2. upgrade from every supported predecessor version;
3. rollback within the declared frontier;
4. failure during a hook and safe retry;
5. uninstall behavior for retained and shared resources;
6. rendering with minimal, default, and production values;
7. absence of cluster lookups in reproducible release rendering unless explicitly governed.

### Hooks are jobs with hidden coupling

Helm hooks have weights and lifecycle annotations, but they do not create distributed transactions. If a pre-upgrade hook migrates a database and the Deployment fails, Helm can report a failed release while the database has already changed. A retry may rerun the migration. A rollback may select a binary that cannot read the new state.

Atlas therefore uses hooks only for bounded verification or idempotent operations whose durable identity and replay semantics are explicit. Long-lived migrations are modeled as data releases with their own ledger, not hidden in chart lifecycle.

### Library charts and abstraction pressure

Library charts can reduce repeated labels or security context fragments. They can also create a private template language that reviewers cannot reason about. Extract a helper only when it has a stable semantic responsibility and tests. Do not abstract merely to reduce line count. A visible 20-line Deployment security context may be easier to audit than a one-line include whose behavior changes across dozens of charts.

### Packaging and provenance

Chart version, application version, repository URL, and archive digest are distinct identities. Promotion should bind the exact chart archive digest and image digests. Repackaging the same chart source can change archive bytes; changing an index can retarget a version. The release dossier should record the registry or repository subject actually fetched by the controller.

The final design review should answer: which chart changes are additive, which require a major chart API version, which require data compatibility work, and which require a new Kubernetes resource identity? If those categories are not explicit, chart version numbers are decorative.
