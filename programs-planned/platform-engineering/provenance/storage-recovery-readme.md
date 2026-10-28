# Platform Engineering

A cumulative ten-course program that follows one Atlas Developer Platform from Linux processes to a governed internal platform. The program introduces an abstraction only after the learner has studied the mechanism, failure model, and evidence hidden beneath it.

## Released courses

1. **Linux, Networking, and Cloud Systems Engineering** — understand and operate the substrate.
2. **Infrastructure as Code and Cloud Foundation Engineering** — codify cloud state and its change process.
3. **Container, OCI, and Software Supply Chain Engineering** — package workloads as immutable, policy-verifiable releases.
4. **Kubernetes Architecture and Workload Engineering** — reconcile the verified release through Kubernetes APIs and workload controllers.
5. **Kubernetes Networking, Gateway, and Service Connectivity Engineering** — make packet paths, discovery, policy, and exposure explicit.
6. **Kubernetes Storage, Stateful Workloads, and Data Resilience Engineering** — preserve data authority, recoverability, and workload correctness across Pod, Node, zone, and storage-system failure.

```text
operate the machine
→ codify the cloud
→ verify the workload artifact
→ reconcile the workload
→ connect it deliberately
→ persist and recover it safely
→ deliver it through GitOps
```

Course 6 exports an immutable data-plane handoff for Course 7, **Kubernetes Delivery, GitOps, and Release Engineering**.

Begin at [`program-book/start-here.md`](program-book/start-here.md).
