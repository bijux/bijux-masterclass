> Planned source collection. See [collection status](COLLECTION.md) for preservation and qualification limits.

# Platform Engineering

Platform Engineering is a cumulative ten-course program that follows one **Atlas Developer Platform** from Linux processes to a governed internal platform. An abstraction is introduced only after the learner has studied the mechanism, failure model, authority boundary, and evidence that the abstraction hides.

## Released courses

1. **Linux, Networking, and Cloud Systems Engineering** — understand and operate the substrate.
2. **Infrastructure as Code and Cloud Foundation Engineering** — codify cloud state and govern infrastructure change.
3. **Container, OCI, and Software Supply Chain Engineering** — package workloads as immutable, policy-verifiable releases.
4. **Kubernetes Architecture and Workload Engineering** — reconcile verified workloads through Kubernetes APIs and controllers.
5. **Kubernetes Networking, Gateway, and Service Connectivity Engineering** — make packet paths, discovery, policy, and exposure explicit.
6. **Kubernetes Storage, Stateful Workloads, and Data Resilience Engineering** — preserve data authority and recoverability across failure domains.
7. **Kubernetes Delivery, GitOps, and Release Engineering** — turn reviewed revisions into observable, reversible desired state without weakening data or security guarantees.

```text
operate the machine
→ codify the cloud
→ verify the workload artifact
→ reconcile the workload
→ connect it deliberately
→ persist and recover it safely
→ deliver it through governed reconciliation
→ defend the platform and its tenants
```

Course 7 publishes an immutable delivery-plane handoff for Course 8, **Platform Security, Identity, Policy, and Multi-Tenancy Engineering**.

Begin at [`program-book/start-here.md`](program-book/start-here.md).
