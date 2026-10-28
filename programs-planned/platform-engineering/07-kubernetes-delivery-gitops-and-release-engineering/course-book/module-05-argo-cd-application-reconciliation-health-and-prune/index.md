# Module 5 — Argo CD application reconciliation, health, and prune

## Central question

**How should an application-centric GitOps controller compare, own, order, apply, assess, and delete Kubernetes resources without confusing synchronization with safety?**

Argo CD is the primary implementation lane in this course. It is not presented as the definition of GitOps. It is a concrete system whose APIs make several delivery concerns visible: source revision, destination, application inventory, project scope, synchronization, health, hooks, waves, prune, self-heal, and fleet generation.

## The control path

A simplified Argo CD path is:

```text
Application source reference
        ↓
repository and artifact retrieval
        ↓
manifest generation
        ↓
live-state comparison
        ↓
application-controller reconciliation
        ↓
Kubernetes API writes
        ↓
resource status and health assessment
```

Different components own different observations. Repository retrieval can succeed while manifest generation fails. Rendering can succeed while comparison fails because an API is absent. Apply can succeed while health remains progressing. Health can become degraded after the sync operation has completed.

A useful incident timeline records the earliest failed transition rather than starting with the final red application icon.

## Application as an ownership declaration

An Argo CD `Application` declares source, destination, project, and sync behavior. It also establishes an inventory boundary: these rendered resources are managed as one application.

A good application boundary has coherent lifecycle and ownership. Placing all cluster infrastructure and every workload into one Application creates broad blast radius and unreadable health. Splitting each YAML file into a separate Application creates ordering and coordination problems. Atlas separates platform controllers, shared infrastructure, data plane, and application workloads according to independent lifecycle and authority.

The Application should pin an immutable target revision for production. Tracking a branch can be appropriate for development; the controller status must still report the resolved commit.

## AppProject as a security and tenancy boundary

An `AppProject` can restrict source repositories, destination clusters and namespaces, and allowed resource kinds. Those rules are not mere organization. They constrain what an Application can cause the controller to write.

Atlas production projects:

- allow only the environment repository and approved OCI/chart sources;
- target only named clusters and namespaces;
- deny unexpected cluster-scoped resources;
- separate platform controller installation from application reconciliation;
- bind repository and destination credentials to the minimum required scope.

A project that allows any repository, any destination, and every cluster-scoped kind transfers too much authority to application authors and the GitOps controller.

## Sync state

Argo CD compares desired manifests with live resources and reports whether they are synchronized. Diff behavior includes normalization and ignore rules. Differences may arise from:

- defaulted fields;
- admission mutation;
- other field managers;
- controller-generated values;
- list ordering;
- API conversion;
- genuinely unauthorized drift.

Ignore rules must be narrow and justified. Ignoring an entire object or broad spec path can hide dangerous changes. Atlas records the owner, reason, expiry, and test for each ignore rule.

## Automated sync, self-heal, and prune

Automated sync can reduce manual delay and correct drift quickly. It also amplifies mistakes. The three important behaviors are distinct:

- **automated sync** applies a new desired revision;
- **self-heal** corrects live drift against the current revision;
- **prune** deletes managed resources absent from desired state.

Atlas enables them per application only after inventory, protected-resource, and rollback analysis. Data-plane Applications do not receive blanket prune authority. A resource can also carry an explicit retain or delete confirmation policy, but annotations are supporting evidence, not a substitute for correct application boundaries.

Prune order matters. Deleting a Service before draining traffic, a CRD before custom resources, or a recovery object before retention approval creates failure. Prune should be visible in the rendered diff and release review.

## Health assessment

Health is resource-specific. A Deployment can be Progressing until observed generation and available replicas satisfy expectations. A Job can be Healthy after completion. A custom resource needs meaningful status conditions or a custom health assessment.

A custom health rule must not declare success merely because the object exists. It should observe conditions owned by the authoritative controller and include observed generation where applicable. Stale status can otherwise make an old success appear current.

Atlas separates:

```text
Synced
Healthy
JourneyPassed
DataGatesPassed
```

The release decision requires all applicable gates, not only Argo CD health.

## Sync phases, hooks, and waves

Argo CD supports phases such as PreSync, Sync, and PostSync, with numeric waves to order resources. This is useful for CRDs before custom resources, namespaces before namespaced objects, and bounded verification Jobs after rollout.

Ordering hints do not create a distributed transaction. A later wave can fail after earlier resources have changed. A hook can run more than once. Hook deletion policy can remove evidence. A controller restart can resume from observed state. Every step must be idempotent or durably identified.

Atlas uses sync waves for declarative dependencies and uses the Course 6 release-order protocol for data migration. Migration phases have durable operation IDs and explicit completion records; they are not inferred from hook names.

## Resource hooks and lifecycle

Hooks are Kubernetes resources. Their health, retries, ServiceAccount, network access, cleanup, and evidence retention need review. A PreSync Job with broad database credentials is a privileged production component, not a convenient script.

A hook should have:

- immutable image digest;
- bounded permissions;
- idempotent operation identity;
- deadline and retry policy;
- observable outcome;
- cleanup that retains required evidence;
- compatibility with resume and rollback.

## ApplicationSet and fleet generation

ApplicationSet can generate Applications from clusters, Git directories, lists, pull requests, or combinations. It is powerful because one generator change can affect many destinations.

Atlas treats generator inputs as a fleet API. Cluster labels and directory names influence deployment scope and must be governed. A malformed selector should not promote production configuration into a test cluster. Generated Application diffs and destination changes require review.

Course 9 will operate fleets deeply. In Course 7, the focus is release topology and blast radius.

## Multiple sources

An Application can combine multiple sources, such as a chart from one repository and values from another. This can reduce duplication but complicates identity and causality. The release record must include every source revision and define precedence. A change in any source produces a new desired revision.

Atlas prefers one environment source that pins external artifacts by digest. Multi-source configuration is used only when ownership and promotion remain explicit.

## Orphaned resources and unmanaged state

Resources may exist in an application namespace without belonging to the Application inventory. Orphan monitoring can reveal manual or legacy objects. It does not prove they are safe to adopt or delete.

Adoption is an ownership transfer. Before adding a live resource to Git, capture its current fields, managers, consumers, lifecycle, and data. Before deletion, identify the owner and recovery path.

## Repository and controller failure

If Argo CD cannot fetch a repository, the correct state is source error or unknown, not empty desired state. Running workloads should continue. If the controller is unavailable, Kubernetes workload controllers continue reconciling their existing objects, but no new desired revision or drift correction occurs.

Recovery needs:

- controller installation and configuration source;
- repository credentials;
- Application and Project definitions;
- destination credentials or cluster registration;
- known desired revision;
- inventory and comparison recovery;
- protected-resource policy.

The Git repository alone may not contain all of those secrets and bootstrap dependencies.

## Atlas Argo CD profile

Atlas adopts these Argo CD rules:

1. Applications align with lifecycle and ownership boundaries;
2. production resolves immutable source revisions;
3. AppProjects restrict sources, destinations, and resource kinds;
4. automated sync, self-heal, and prune are separate policy decisions;
5. protected resources are excluded from ordinary prune;
6. ignore rules are narrow, owned, tested, and expiring;
7. health is separate from journey and data gates;
8. hooks are idempotent, least-privileged resources with durable outcomes;
9. waves order dependencies but do not claim transactionality;
10. ApplicationSet generator changes are fleet-scope release changes.

Module 6 examines Flux. The comparison is not a contest. It reveals which concepts belong to GitOps and which belong to one implementation architecture.

## Deep-dive practicum

### An Application is an inventory and authority boundary

The most important Argo CD design decision is not the repository URL. It is which resources share one inventory, sync lifecycle, health summary, prune scope, destination, and delegated authority. An Application that combines a stateless API, retained database PVCs, cluster-scoped CRDs, and another team’s namespace makes a single sync action responsible for unrelated lifecycles.

Atlas keeps protected data-plane objects outside the ordinary application inventory. The AppProject also blacklists PVC and snapshot resources from the application path. This is defense in depth, not a replacement for data-owner policy: an administrator could still change the project. The release dossier binds both project policy and rendered inventory.

### Sync status is a comparison result

Argo CD computes desired state from source and compares it with live resources using Kubernetes-aware normalization. `Synced` means the compared fields match for that revision. It does not mean all controllers observed the current generation, all hooks completed durably, or user journeys passed.

When sync seems wrong, inspect four identities:

1. source revision Argo CD fetched;
2. renderer and plugin version actually used;
3. desired object identity and normalized fields;
4. live object managers and ignored paths.

Many “Argo CD drift bugs” are ownership or normalization disagreements.

### Ignore differences as a temporary ownership specification

The production example ignores `/spec/replicas` for one Deployment because an autoscaling lane may own it. A safe ignore rule is narrow in group, kind, namespace, name, and pointer. It has an owner, reason, test, and review date. It does not ignore the full `spec` or every Deployment.

Even a correct ignore rule creates an observability duty. If Git does not own replicas, the autoscaler’s desired and observed behavior must be visible elsewhere. Ignoring a field in one control plane does not make the field unimportant.

### Hooks and sync waves under failure

Assume a PreSync verification Job passes, the Deployment applies, and a PostSync smoke Job fails. Earlier writes remain. Re-running the sync may recreate hooks depending on deletion policy. If the hook performs an external side effect without a stable operation key, each retry can duplicate it.

Atlas’s reference hook is read-only and verifies a named data phase. It uses immutable code, bounded retries, and least privilege. The actual schema migration remains owned by the Course 6 data-release process. This separation keeps hook failure from becoming ambiguous data authority.

### ApplicationSet as a fleet compiler

An ApplicationSet generator compiles catalogue inputs into Applications. A selector change can remove dozens of targets. If the catalogue source is unavailable, the generator must not interpret the result as zero clusters. Review should show the generated Application set before and after, including destinations and revisions.

For production, Atlas treats generator changes like platform releases. They require compatibility and recovery evidence, not just template syntax validation.

### Incident sequence

If Argo CD is repeatedly restoring an unsafe revision:

1. identify and suspend the smallest Application or automated action;
2. preserve source, render, diff, and live evidence;
3. establish whether the repository revision or live drift is unsafe;
4. apply a bounded mitigation with incident authority;
5. create a reviewed desired-state change or revert;
6. resume reconciliation and confirm no hidden inventory deletion;
7. retain the incident fork and merge evidence.

Deleting the Application or turning off the controller cluster-wide is rarely the first correct action.
