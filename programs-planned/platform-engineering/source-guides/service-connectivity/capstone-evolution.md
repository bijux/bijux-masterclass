# Atlas capstone evolution

```text
Course 1 — Atlas Host Runtime 1.0
Course 2 — Atlas Cloud Foundation 1.0
Course 3 — Atlas Workload Release 1.0
Course 4 — Atlas Kubernetes Workload 1.0
Course 5 — Atlas Connectivity Plane 1.0
Course 6 — Atlas Data Plane 1.0
```

Each transition preserves the previous contract while moving a new responsibility into a governed control plane. Course 5 does not own durable data. It defines which names, ports, address families, failure semantics, policies, and topology assumptions the storage layer must honor.
