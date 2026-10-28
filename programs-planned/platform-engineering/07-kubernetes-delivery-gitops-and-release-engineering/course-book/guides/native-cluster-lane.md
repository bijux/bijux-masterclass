# Guide — Native disposable-cluster lane

The native lane uses a disposable cluster and synthetic credentials. Never point the course targets at a shared cluster.

Install only pinned controller versions. Record Kubernetes, CRD, renderer, Helm, Argo CD, Flux, and Rollouts versions. Use a local or disposable Git/OCI source whose complete history can be destroyed after the exercise.

The lane should execute at least:

- deterministic render and diff;
- one successful sync;
- unauthorized drift and self-heal;
- protected prune rejection;
- repository outage;
- one canary abort;
- controller restart;
- complete cleanup.

Classify the evidence as E2 local-cluster evidence. Do not convert it into a claim about managed identity, multi-zone availability, hosted Git reliability, or production traffic.

## Extended reader notes

The native lane uses a disposable cluster only after dependency-light proof passes. Install pinned CRDs and controllers, record every binary or image digest, and keep the cluster disposable. Apply the course manifests in a dedicated namespace and avoid cloud credentials or real secrets.

Capture native render output, API admission, controller status, Events, managed fields, inventory, health, and cleanup. Run repository outage, drift, protected-prune, secret-source failure, and canary-abort experiments. Remove all cluster-scoped resources during cleanup.

A local cluster establishes bounded integration evidence. It does not support claims about managed IAM, cloud load balancers, multi-region fleets, operated key custody, or production scale.
