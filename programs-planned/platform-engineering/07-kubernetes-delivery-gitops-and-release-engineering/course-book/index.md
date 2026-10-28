# Kubernetes Delivery, GitOps, and Release Engineering

A Kubernetes cluster can converge perfectly on the wrong revision. A reviewed repository can select an untested artifact. A controller can report `Synced` while a migration is irreversible, a Secret is undecryptable, a canary receives no traffic, or a recovery object is about to be pruned.

Course 7 studies delivery as a control system with explicit subjects, authorities, inventories, observations, and recovery paths. You will follow one Atlas release from immutable source and OCI artifacts through rendering, promotion, reconciliation, health, progressive exposure, fleet rollout, and incident recovery.

## What you will be able to do

By the final defense you will be able to:

- distinguish source identity, artifact identity, rendered identity, live state, health, journey correctness, and data correctness;
- design a repository and promotion model that moves the same tested artifacts through environments;
- evaluate Kustomize patches and Helm chart APIs as versioned release interfaces;
- scope Argo CD and Flux source, destination, inventory, field, prune, and automation authority;
- prevent ordinary GitOps reconciliation from deleting protected data and recovery resources;
- evaluate secret delivery through source, materialization, adoption, and revocation;
- design canary evidence that handles sample size, segments, telemetry delay, and missing data honestly;
- operate multi-cluster promotion and recover the delivery control plane without losing lineage;
- publish a categorical release dossier and select reconcile, revert, forward fix, or retirement deliberately.

## Reader path

Begin with [Start here](start-here.md), then complete the [orientation](module-00-orientation/index.md). Follow the ten modules in order. Use the [incident casebook](casebook/case-01-gitops-pruned-recovery.md) after Module 4 and the [capstone manual](capstone/architecture.md) when implementing Atlas Delivery Plane 1.0.

The course book is the authoritative product. The capstone code and manifests exist to make claims falsifiable, not to hide explanations behind tooling.
