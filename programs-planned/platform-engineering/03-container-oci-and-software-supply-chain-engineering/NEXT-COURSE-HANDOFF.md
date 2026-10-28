# Course 4 successor handoff

Course 4—Kubernetes Architecture and Workload Engineering—receives a workload release, not a repository of build internals.

The handoff identifies:

- API and worker images by immutable digest;
- supported operating-system and architecture pairs;
- process user and group;
- entry points and listening ports;
- liveness, readiness, and worker-heartbeat semantics;
- durable, ephemeral, and configuration mount classes;
- termination grace period;
- read-only root filesystem and capability policy;
- resource hypotheses and their evidence class;
- SBOM, provenance, signer, and verification policy;
- risks that Kubernetes must not hide.

Kubernetes may reconcile this contract. It may not rebuild the image at startup, substitute a tag for a digest, bake environment secrets into a layer, or redefine readiness as process existence.
