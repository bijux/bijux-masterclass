# Capstone proof map

| Claim | Dependency-light proof | Optional kind proof | Deferred proof |
|---|---|---|---|
| digest-pinned workload | manifest validator | admitted Pod template | registry/admission policy in Course 8 |
| idempotent reconciliation | semantic controller tests | controller child stability | operated controller SLO in Course 9 |
| rollout bounds | rollout model | Deployment status | production capacity in Course 5/9 |
| scheduling feasibility | semantic scheduler | scheduler events | managed-cluster topology/capacity |
| graceful termination | lifecycle model | Pod deletion observation | real workload drain under traffic |
| durable worker path interface | manifest/PVC reference | binding if storage exists | CSI/data resilience in Course 6 |
| service identity handoff | manifest and contract | ServiceAccount admission | cloud workload identity in Course 8 |
