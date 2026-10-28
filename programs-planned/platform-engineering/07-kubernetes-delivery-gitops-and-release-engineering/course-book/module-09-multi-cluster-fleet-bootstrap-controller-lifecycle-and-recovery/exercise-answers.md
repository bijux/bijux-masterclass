# Worked answers — Multi-cluster delivery, bootstrap, controller lifecycle, and recovery

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why is a cluster name insufficient fleet identity?

Names can be mutable, reused, or ambiguous. Fleet identity should include canonical ID, owner, environment, region, topology, Kubernetes version, capabilities, and lifecycle. Generators and release policy should use governed fields rather than display names.

## 2. What is the bootstrap paradox of GitOps?

The controller that reconciles Git-managed resources does not exist on a new cluster yet. An external bootstrap path must create initial trust, install the controller, and configure source access. That authority should be short-lived and handed off to bounded in-cluster identities.

## 3. What is the main trade-off between central and per-cluster reconcilers?

Central reconcilers concentrate visibility and management but also credentials, network reach, and blast radius. Per-cluster reconcilers localize failure and authority but require fleet-wide controller lifecycle and observability. Hybrid designs can centralize metadata while keeping writes local.

## 4. Why should release waves represent topology classes?

Several clusters in one provider or region may share the same failure mode. A wave should learn across relevant Kubernetes versions, network, storage, policy, and provider classes before broad promotion. Cluster count alone does not measure diversity.

## 5. What compatibility facts should be checked before a cluster receives a revision?

Kubernetes and API versions, CRDs, GitOps controller and renderer versions, admission policy, Gateway and CSI capabilities, required feature gates, and provider-specific dependencies. The exact set depends on the revision’s resources and behavior.

## 6. Why is upgrading the GitOps controller itself a special release?

It changes the system that renders, compares, applies, and reports every other release. CRDs, RBAC, caches, health rules, and embedded renderers may change. It needs staged validation and an external recovery path rather than blind self-management.

## 7. How should a repository outage be represented?

As source unavailable or stale while preserving the last-known-good desired state. Running workloads continue. New promotion and bootstrap stop. Empty output or deletion must never be inferred from fetch failure.

## 8. Why is Git alone insufficient for delivery-plane disaster recovery?

Controller installation, CRDs, credentials, cluster registrations, decryption authority, release records, inventory, and protected-resource policy may live outside the repository or require external bootstrap. Recovery needs a documented chain for all of them.

## 9. Why must a generator distinguish missing observation from retirement?

A catalogue outage or selector error can temporarily omit a cluster. Treating omission as retirement could delete Applications and resources. Retirement requires an explicit owner-approved record with data and credential disposition.

## 10. What should happen to existing workloads during a GitOps-controller outage?

Kubernetes workload controllers continue managing existing objects. No new desired revision or drift repair occurs. The platform reports stale reconciliation and restores the controller without using the outage as a reason to replace or delete workloads.

## 11. Why are universal fleet credentials dangerous?

One compromise crosses environment, tenant, and cluster boundaries. Credentials should be scoped by source, destination, environment, and function, with separate recovery identities. Fleet automation must not depend on one permanent cluster-admin secret.

## 12. What does a fleet dashboard need beyond a green cluster count?

Desired and resolved revisions, render digest, sync and health, controller/CRD versions, source age, last reconciliation, suspension or break-glass state, wave, and evidence completeness. Each aggregate must drill into the first failed transition.
