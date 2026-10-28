# Atlas Data Plane architecture

Atlas separates five responsibilities:

```text
application semantics
→ Kubernetes storage intent
→ CSI lifecycle
→ backend data service
→ independent recovery plane
```

The application owns commit, schema, logical identity, consistency, and fencing. Kubernetes owns claims, desired attachment, workload placement, and lifecycle objects. CSI components own translation between Kubernetes intent and storage/backend operations. The backend owns physical persistence and provider-specific replication. Recovery tooling owns independent copy inventory, keys, restore orchestration, and evidence.

## Data classes

- **Transactional state** uses one authoritative history and rejects stale writer generations.
- **Immutable artifacts** use content-addressed identity and atomic publication.
- **Scratch data** is Pod-scoped, bounded, and recomputable.
- **Recovery evidence** is retained separately from the primary cluster.

## Trust boundaries

Node CSI plugins are privileged host components. Controller plugins and sidecars may hold powerful backend credentials. Backup systems can read all protected data. GitOps may manage declarative resources but does not automatically own data deletion or restoration.

## Course boundary

The dependency-light implementation proves semantic mechanisms. Native Kubernetes, CSI, storage-backend, multi-zone, and operated recovery claims require stronger evidence lanes and remain explicitly classified.
