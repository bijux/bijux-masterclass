# Kubernetes Architecture and Workload Engineering

Kubernetes is best understood as an API-mediated control system. Users and automation write desired state. Independent controllers observe selected objects, compare current state with intent, create or modify dependent resources, and report observations. Schedulers choose feasible Nodes. Kubelets realize bound Pods through container runtimes and local operating-system mechanisms. The system is useful precisely because no human has to coordinate every transition manually—but that division of responsibility becomes dangerous when ownership is vague.

This course develops one practical skill across ten modules:

> Given a desired workload state and an observed failure, identify the owning object, controlling component, missing transition, decisive evidence, safe repair, and residual risk.

That skill is more durable than memorizing Kubernetes object templates.

## Place in the Platform Engineering program

The first three courses established the substrate and release being orchestrated:

```text
Course 1 — Linux, Networking, and Cloud Systems Engineering
    process, identity, filesystems, sockets, TLS, supervision, host recovery

Course 2 — Infrastructure as Code and Cloud Foundation Engineering
    cloud state, identity, networks, compute, encryption, recovery, IaC release

Course 3 — Container, OCI, and Software Supply Chain Engineering
    immutable image subjects, runtime constraints, registry publication,
    SBOM, provenance, signatures, workload-release policy

Course 4 — Kubernetes Architecture and Workload Engineering
    API objects, field ownership, controllers, scheduling, lifecycle,
    rollout, disruption, stable identity, and custom control loops
```

Atlas Workload Release 1.0 enters this course with exact image digests, non-root runtime identity, a read-only root filesystem, declared writable paths, health semantics, shutdown expectations, and supply-chain evidence. Kubernetes may operationalize those requirements. It may not weaken them.

## What the course builds

The capstone is **Atlas Kubernetes Runtime 1.0**. Its production-intent model contains:

- three replaceable Atlas API replicas managed by a Deployment;
- one Atlas worker replica managed by a Deployment while storage concurrency remains unproven;
- exact Course 3 image subjects;
- ServiceAccounts with deliberate token projection;
- configuration projection;
- a persistent-volume interface for inherited durable paths;
- readiness, liveness, startup, and termination behavior;
- a PodDisruptionBudget;
- Job, CronJob, DaemonSet, and StatefulSet teaching workloads;
- an `AtlasWorkload` custom resource and compiled Go controller;
- an exact networking handoff for Course 5.

Networking data planes, persistent-storage implementation, GitOps, security policy, fleet operation, and self-service platform APIs remain later-course responsibilities. Course 4 names those boundaries rather than pretending that a Service or PVC proves them.

## How the book is organized

Each numbered module has five learner-facing artifacts:

1. **Chapter** — the complete conceptual and practical explanation;
2. **Exercises** — twelve transfer problems that require reasoning beyond recall;
3. **Worked answers** — matching solutions that expose assumptions and evidence;
4. **Laboratory** — one bounded failure investigation;
5. **Checkpoint** — evidence that must exist before progression.

Supporting guides teach object reading, debugging, evidence capture, and local-cluster discipline. The casebook follows failures across module boundaries. Reference pages keep calculations and review criteria close at hand.

## Learning outcomes

After completing the course, you should be able to:

- explain the responsibilities of the API server, etcd, scheduler, controllers, kubelets, runtimes, and extension components;
- distinguish persistence, reconciliation, placement, realization, readiness, availability, and reachability;
- use UID, resource version, generation, owner references, managed fields, finalizers, and conditions correctly;
- design Pod templates that preserve the inherited OCI runtime contract;
- select Deployment, Job, CronJob, DaemonSet, StatefulSet, or custom controller from workload invariants;
- calculate rollout and disruption populations;
- explain every failed scheduler predicate rather than guessing at capacity;
- design probes whose repair actions match their questions;
- write an idempotent custom reconciler with stable status and bounded cleanup;
- defend what the evidence proves and what remains unexecuted.

Begin with [Start here](start-here.md), then complete the [Orientation](module-00-orientation/index.md).
