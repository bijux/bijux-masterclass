# Kubernetes Architecture and Workload Engineering

Course 4 of the Platform Engineering program turns the verified Atlas OCI release into a Kubernetes workload without weakening its image, identity, filesystem, health, shutdown, or supply-chain contracts.

The governing question is:

> Which API object and controller own each workload transition, and what evidence proves convergence or explains why it stopped?

## Primary product

The course book is authoritative. It contains one orientation, ten deep modules, 120 exercises with worked answers, ten controlled laboratories, a casebook, reference material, and a final architecture defense.

Begin at [`course-book/start-here.md`](course-book/start-here.md).

## Executable support

The capstone includes:

- a deterministic Python model of API persistence, apply conflicts, finalizers, controllers, scheduling, lifecycle, disruption, and workload identity;
- a compiled Go reconciliation core for `AtlasWorkload`;
- production-intent Kubernetes manifests using exact Course 3 image digests;
- a separate optional kind observation lane;
- ten planted defects and categorical release candidates;
- exact Course 3 and Course 5 handoff manifests.

```bash
make help
make doctor
make predecessor-proof
make core-proof
make capstone-tour
make manifest-proof
```

`make kind-proof` is guarded and requires an isolated disposable cluster. Its output is local mechanics evidence, not production proof.

## Evidence boundary

The dependency-light release proves course semantics, static contracts, controller idempotency, and cross-implementation agreement. It does not claim managed-cluster availability, production CNI/CSI behavior, network reachability, persistent-volume durability, cloud identity, representative capacity, or fleet operation. Those responsibilities belong to later courses.
