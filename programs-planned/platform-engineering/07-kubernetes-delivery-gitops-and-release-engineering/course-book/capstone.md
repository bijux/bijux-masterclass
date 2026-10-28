# Capstone — Atlas Delivery Plane 1.0

Atlas Delivery Plane receives immutable workload, networking, storage, and recovery contracts from Courses 3–6. It adds a governed path from a reviewed revision to running state without transferring data authority to the delivery controller.

```text
source commit and OCI subjects
        ↓
deterministic Kustomize or Helm rendering
        ↓
canonical rendered-set digest and policy evidence
        ↓
environment promotion record
        ↓
Argo CD or Flux reconciliation and inventory
        ↓
resource health and actual traffic exposure
        ↓
journey, data, restore, secret, and fleet gates
        ↓
categorical release dossier and incident recovery
```

## Capstone components

- `atlas_delivery/` — transparent Python model for canonicalization, rendering, inventory, reconciliation, health, promotion, progressive analysis, secrets, fleet compatibility, and release decisions;
- `gitopsprobe-go/` — independent Go implementation of canonical JSON digest and drift-set comparison;
- `repository/` — Kustomize bases and overlays, protected data inventory, and a versioned Helm chart;
- `controllers/` — Argo CD and Flux resources with bounded source, destination, prune, and automation policy;
- `secrets/` — SOPS and External Secrets teaching lanes using synthetic fixtures;
- `progressive/` — Argo Rollouts and Flagger resources plus data compatibility;
- `fleet/` — cluster profiles and promotion waves;
- `releases/` and `planted-defects/` — accepted, rejected, review-required, and not-executed evidence;
- `handoff/` — exact security, identity, policy, and multi-tenancy requirements for Course 8.

Read the [capstone architecture](capstone/architecture.md) before editing files. The [implementation map](capstone/implementation-map.md) links every conceptual mechanism to its code and native resource. The final outcome is not “Argo CD installed” or “Flux installed.” It is a release system whose authority, evidence, failure, and recovery can be defended.
