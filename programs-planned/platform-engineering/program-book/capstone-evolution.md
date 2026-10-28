# Atlas capstone evolution

The program uses one cumulative system rather than ten disconnected demonstrations.

```text
Course 1  Atlas Host Runtime
          processes, identity, files, sockets, TLS, supervision

Course 2  Atlas Cloud Foundation
          networks, IAM, remote state, compute, edge, recovery

Course 3  Atlas Workload Release
          OCI images, digests, runtime contracts, SBOM, provenance

Course 4  Atlas Kubernetes Runtime
          API objects, controllers, scheduling, lifecycle, CRDs

Course 5  Atlas Connectivity Plane
          CNI, Services, DNS, policy, Gateway, TLS, egress

Course 6  Atlas Data Plane
          CSI, stateful identity, fencing, snapshots, backup, restore

Course 7  Atlas Delivery Plane
          rendering, promotion, GitOps, secrets, canaries, fleet release
```

Each course consumes an exact predecessor handoff and publishes a bounded successor handoff. The handoff preserves guarantees already earned and names evidence that remains environment-backed. Course 7’s security handoff freezes controller identities, repository authority, secret-delivery lanes, artifact trust, tenant boundaries, protected prune, and known risks for Course 8.
