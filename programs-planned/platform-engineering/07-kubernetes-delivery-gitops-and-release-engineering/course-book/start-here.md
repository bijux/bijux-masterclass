# Start here

## Entry contract

This course assumes that you can explain Kubernetes desired and observed state, Deployment and StatefulSet behavior, immutable image digests, Service and Gateway paths, PersistentVolume lifecycles, snapshots, backups, fencing, and the difference between application rollback and data recovery. Course 7 consumes those guarantees rather than weakening them for deployment convenience.

Run the predecessor proof before reading further:

```bash
make doctor
make predecessor-proof
```

Then open the [Course 6 handoff bridge](../PREDECESSOR-HANDOFF.md) and identify the protected-resource list, data-release order, restore gates, and evidence limitations.

## Choose a primary controller lane

Select one primary native lane:

- **Argo CD** for application-oriented inventory, sync, health, Projects, Applications, hooks, waves, and ApplicationSet;
- **Flux** for source artifacts, controller composition, Kustomizations, HelmReleases, image automation, and dependency graphs.

You must understand both architectures, but duplicating every command is not the goal. The dependency-light Python model isolates the common invariants. The Go probe supplies an independent canonicalization and drift implementation. Native tools add implementation evidence when available.

## How to use each module

1. Read the chapter without editing code.
2. Write your answers to the twelve exercises.
3. Compare reasoning with the worked answers.
4. State the lab hypothesis before running commands.
5. Collect machine-readable evidence, not only screenshots.
6. Complete the checkpoint and defend the claim boundary.

A checkpoint is not complete because a controller is green. It is complete when the required evidence supports the exact claim and names what remains unproven.

## First complete run

```bash
make capstone-tour
make core-proof
```

The tour demonstrates deterministic rendering, convergence, field ownership, protected prune, source-outage behavior, progressive analysis, artifact promotion, fleet compatibility, and bounded health. Continue to the [ten-day study plan](study-plan.md).
