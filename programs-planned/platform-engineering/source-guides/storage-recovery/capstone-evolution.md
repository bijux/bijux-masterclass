# Atlas capstone evolution

```text
Course 1 — Atlas Host Runtime 1.0
Course 2 — Atlas Cloud Foundation 1.0
Course 3 — Atlas Workload Release 1.0
Course 4 — Atlas Kubernetes Workload 1.0
Course 5 — Atlas Connectivity Plane 1.0
Course 6 — Atlas Data Plane 1.0
Course 7 — Atlas Delivery Plane 1.0
```

Course 6 introduces three data authorities: transactional state, immutable artifacts, and recovery evidence. It separates them because they have different consistency, lifecycle, access, and restoration requirements. Kubernetes coordinates claims and workloads; it does not become the database, object store, backup repository, or application consistency protocol.
