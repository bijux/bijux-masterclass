# Program evidence ladder

Every platform claim names its evidence class.

1. **Reasoned** — a claim derived from a documented model and assumptions.
2. **Static** — parsing, rendering, schema, compatibility, or policy evidence.
3. **Local executable** — deterministic code, process, filesystem, socket, or Git evidence.
4. **Cluster-backed** — evidence from Kubernetes admission, controllers, storage, networking, or delivery tools in a bounded cluster.
5. **Cloud- or system-backed** — evidence from real IAM, load balancers, KMS, CSI drivers, registries, repositories, and managed services.
6. **Operated** — evidence accumulated under representative traffic, incidents, upgrades, recovery exercises, and organizational ownership.

Evidence strength depends on relevance as well as environment. A real cluster test against a different image digest cannot support the candidate under review. A native Helm render proves chart behavior but not upgrade safety. Argo CD `Synced` proves a bounded live comparison, not user or data correctness. Course 7 therefore binds every observation to source, artifact, renderer, environment, and release subjects.

The release must preserve `not-executed` when required infrastructure is absent. Missing evidence is not transformed into success merely because a semantic model passed.
