# Start here — Platform Engineering

Platform engineering is the design and operation of trusted capabilities that let other teams deliver and run software without rediscovering every systems problem. This program establishes lower-layer mechanisms before introducing the abstractions that hide them.

The first four stages are:

```text
Atlas Host Runtime 1.0
→ Atlas Cloud Foundation 1.0
→ Atlas Workload Release 1.0
→ Atlas Kubernetes Workload 1.0
```

Course 4 introduces an API-mediated control system. The API server persists admitted desired state. Controllers, scheduler, and kubelets act independently and report observations. Kubernetes receives a released artifact; it does not build the artifact, invent secret values, or turn ephemeral storage into durable storage.

For every object ask who owns desired state, which controller observes it, which identity survives replacement, which transition is retryable, and what evidence explains convergence or failure.

Begin Course 4 at `04-kubernetes-architecture-and-workload-engineering/course-book/start-here.md`.
