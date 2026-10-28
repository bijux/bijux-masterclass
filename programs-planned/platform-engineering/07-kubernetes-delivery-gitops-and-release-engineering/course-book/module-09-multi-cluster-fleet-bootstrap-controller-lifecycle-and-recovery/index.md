# Module 9 — Multi-cluster delivery, bootstrap, controller lifecycle, and recovery

## Central question

**How can one delivery system govern many clusters without turning a single repository error, credential compromise, controller upgrade, or fleet selector into a platform-wide incident?**

Fleet delivery magnifies every earlier decision. A harmless-looking directory name may generate hundreds of Applications. A controller upgrade may change diff behavior across all clusters. A repository outage may prevent new cluster bootstrap. A cluster label mistake may route production desired state into a test environment.

## Fleet desired state

A fleet is not merely a list of clusters. Each cluster has:

- identity and ownership;
- environment and region classification;
- Kubernetes and API versions;
- installed controllers and CRDs;
- network and storage capabilities;
- policy profile;
- secret and workload identity authorities;
- desired revision;
- maintenance and recovery state.

Atlas stores this metadata in a governed cluster catalogue. Generators may read the catalogue; they may not infer production class from a mutable display name.

## Bootstrap chain

A new cluster needs enough initial authority to install the delivery system that will manage everything else. This creates a bootstrap chain:

```text
cloud and cluster creation
→ initial trust and identity
→ GitOps controller installation
→ source and destination credentials
→ platform prerequisites
→ workload desired state
```

The chain must be recoverable without granting permanent cluster-admin access to a CI job. Atlas uses a short-lived bootstrap identity, installs a pinned controller release, registers bounded source credentials, then transfers ongoing reconciliation to the controller ServiceAccounts.

Bootstrap evidence records which steps were external to GitOps. A cluster cannot create its first GitOps controller solely by reconciling a resource that does not yet have a reconciler.

## Hub-and-spoke versus per-cluster controllers

### Central controller

A central controller manages remote clusters. Operational visibility is concentrated, but credentials and network access have broad blast radius. A hub outage affects reconciliation for many clusters.

### Per-cluster controller

Each cluster pulls its own desired state. Credentials and failure are localized, but controller upgrades, configuration, and observability must be operated across the fleet.

### Hybrid

A management plane may generate or govern per-cluster resources while local controllers perform writes. Atlas prefers local reconciliation for production workloads and central fleet metadata, policy, and release orchestration. Course 10 will turn these capabilities into a platform product.

## Promotion waves across clusters

A fleet release should not change every cluster simultaneously. Atlas defines waves based on failure domains and learning value:

1. ephemeral validation cluster;
2. internal development clusters;
3. one staging cluster per topology class;
4. one low-risk production cell;
5. broader production waves;
6. exceptional or regulated clusters after explicit review.

A wave advances only when required observations from prior waves are complete. The plan accounts for correlated failure: deploying first to three clusters in the same region or provider does not test other topology classes.

## Cluster and controller version skew

Kubernetes versions, CRDs, admission policies, Gateway APIs, CSI drivers, and GitOps controllers may differ across clusters. A desired revision valid in one cluster may fail elsewhere.

Atlas records compatibility requirements for each release:

- minimum and maximum Kubernetes versions;
- required APIs and feature gates;
- renderer and controller versions;
- CRD schema versions;
- provider capabilities;
- policy versions.

Promotion checks the target cluster catalogue before reconciliation. A skipped compatibility check becomes a release defect, not a runtime surprise.

## Delivery-controller upgrades

Upgrading Argo CD or Flux changes the delivery system itself. The release may include:

- controller images;
- CRDs;
- RBAC;
- repository-server behavior;
- renderer versions;
- diff normalization;
- health rules;
- cache format;
- command-line clients.

The controller cannot be assumed to upgrade itself safely merely because it manages its own manifests. Atlas uses a dedicated platform-delivery application with staged rollout, compatibility tests, and an external recovery path.

Controller upgrades should test current Applications or Flux resources against the new version in a representative cluster. CRD conversion and rollback are particularly important: an older controller may not understand objects stored under a newer schema.

## Repository, registry, and identity outages

Fleet operation depends on several control-plane services.

### Repository outage

Clusters continue running last-known-good state. Reconciliation becomes stale. New promotions and bootstrap stop. The platform reports source age and does not prune.

### Registry outage

Existing Pods continue if images are present and healthy. New Pods or rollouts may fail. A delivery decision should consider image availability and node cache assumptions.

### Identity outage

Repository, OCI, secret, or cluster authentication can fail independently. Broad emergency credentials should not be the default recovery. Maintain tested, scoped recovery identities and procedures.

### GitOps controller outage

Kubernetes workload controllers continue managing existing objects. Drift correction and new desired revisions stop. Recovery should restore the controller without taking ownership of unrelated fields or deleting inventory.

## Disaster recovery of the delivery plane

Git is necessary but not sufficient. Recovery may require:

- repository mirrors or backups;
- protected branches and signatures;
- controller installation manifests and images;
- CRDs and version compatibility;
- repository credentials;
- cluster registrations or workload identity configuration;
- secret decryption keys or external-secret access;
- Application/Project or Flux resource definitions;
- release and promotion records;
- protected-resource and prune policy;
- controller-specific state where required.

Atlas performs a clean-cluster reconstruction exercise using synthetic credentials and verifies that the recovered controller selects the same desired revision and inventory. It does not claim that this proves cloud-provider or regional disaster recovery.

## Fleet generators and deletion

A generator that stops emitting one cluster's Application may cause deletion. The absence can result from a catalogue outage, label typo, or intended decommissioning. Atlas separates **missing observation** from **retirement intent**.

Cluster retirement requires an explicit record with owner, final desired state, data disposition, credential revocation, and evidence retention. A generator empty result never authorizes deletion by itself.

## Multi-cluster secrets

Secrets and repository credentials should not be copied identically across the fleet without need. Environment and tenant boundaries may require separate keys, secret stores, and controller identities. Rotation should proceed in waves and retain recovery access.

Course 8 will formalize identity and multi-tenancy. Course 7 records the authority graph and ensures that fleet convenience does not force one universal credential.

## Fleet observability

A fleet view should distinguish:

- desired revision by cluster;
- resolved source artifact;
- render digest;
- sync and health;
- controller and CRD version;
- source age;
- last successful reconciliation;
- active suspension or break-glass state;
- release wave;
- evidence completeness.

Aggregates are useful, but every red or stale cluster must be drillable to the first failed transition.

## Fleet failure patterns

### Label-driven accidental promotion

A cluster is relabelled `environment=production` and receives production Applications. Labels affecting authority require governed ownership and review.

### Empty generator result prunes fleet state

A catalogue or API failure returns no clusters. The generator interprets this as desired deletion. The correct state is unknown or source error.

### Controller upgrade changes rendering

A new embedded Helm or Kustomize version produces a different rendered set from the same source. Renderer identity and pre-upgrade diffs are mandatory.

### Recovery uses broad static credentials

The emergency path restores service but leaves cluster-admin or repository-write credentials distributed permanently. Recovery credentials need expiry and cleanup evidence.

## Atlas fleet-delivery contract

Atlas requires:

1. clusters have canonical catalogue identities and owners;
2. bootstrap authority is short-lived and recorded;
3. production reconciliation is localized where practical;
4. fleet generators cannot convert missing observation into deletion;
5. promotions proceed through topology-aware waves;
6. target compatibility is checked before apply;
7. GitOps controller and CRD upgrades are platform releases;
8. repository, registry, identity, and controller outages have distinct runbooks;
9. delivery-plane recovery includes credentials, CRDs, inventory, and policy—not Git alone;
10. fleet convenience never requires one universal secret or cluster credential.

Module 10 integrates the entire course into a release and incident operating model. The final defense asks not whether the tools work on a good day, but whether the delivery plane remains understandable and recoverable when its own control path fails.

## Deep-dive practicum

### A fleet is a set of different failure domains, not a loop over contexts

Clusters differ in Kubernetes version, installed CRDs, controller version, storage classes, network implementation, identity integration, region, capacity, and maintenance state. Treating them as homogeneous targets causes releases to fail only after reaching the incompatible cluster.

Atlas maintains a cluster profile and release requirements. Target generation filters by lifecycle and environment, then compatibility checks evaluate version and capabilities. An unavailable catalogue returns “unknown,” not an empty target set. This distinction prevents a source outage from being interpreted as a request to retire every Application.

### Bootstrap dependency and the self-hosting paradox

A GitOps controller often manages its own configuration or even its own Deployment. Self-management is useful but creates a bootstrap dependency: if the controller, repository credential, or CRD is broken, the mechanism that would repair it may also be broken.

A recovery design identifies a minimal seed layer that can be installed or restored independently. It includes controller namespace, CRDs, ServiceAccounts, repository trust, and the source of desired state. The seed should be small, pinned, auditable, and tested. Copying a current cluster’s entire state is not a bootstrap strategy.

### Controller upgrades are platform releases

Upgrading Argo CD or Flux can change rendering, normalization, health, inventory, API versions, or credential behavior. Before upgrading a fleet:

1. render representative applications with the new version;
2. compare diffs and health classifications;
3. verify CRD conversion and rollback boundaries;
4. upgrade a canary cluster from each topology class;
5. observe controller resource use and reconciliation lag;
6. retain a supported downgrade or forward-recovery path.

The controller is part of the release compiler and runtime. Its version belongs in every environment revision.

### Promotion waves and correlated risk

Promoting one cluster per topology class provides more information than promoting the first alphabetical cluster. Atlas chooses canaries across single-zone and multi-zone classes before expanding. Additional dimensions may include cloud provider, region, identity integration, and CNI.

A wave should have an entry gate, observation window, stop condition, and recovery owner. “Ten clusters at a time” is not a strategy unless those clusters represent bounded and diverse risk.

### Disaster recovery of the delivery plane

During a regional outage, workloads may fail over while the desired-state repository or controller remains in the failed region. Recovery must preserve source lineage and avoid two active controllers fighting over the same cluster. Decide:

- repository replication and failover authority;
- controller active/standby or independent ownership;
- credential and key availability;
- last-known-good artifact retention;
- cluster registration and revocation;
- post-recovery reconciliation of divergent changes.

The delivery plane needs its own RPO and RTO. These are distinct from application data objectives.
