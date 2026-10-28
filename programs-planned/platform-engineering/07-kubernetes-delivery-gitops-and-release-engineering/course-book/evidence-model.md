# Evidence model

Course 7 uses five evidence classes. Each class answers a different question and must be bound to the same release subject.

## E0 — reasoned and structural

The model is explicit; files parse; schemas, policies, and deterministic semantic code evaluate selected invariants. E0 can reject duplicate identities, mutable images, unsafe prune, invalid release gates, and inconsistent analysis inputs. It does not prove native renderer or controller behavior.

## E1 — native local

The pinned renderer or CLI executes against local inputs: `kustomize build`, `helm lint`, chart rendering, controller diff, SOPS decryption with synthetic keys, or policy engines. E1 adds tool behavior but not a live reconciliation path.

## E2 — disposable cluster

A real controller observes source, renders, applies, inventories, reports status, and recovers from controlled failure in kind or another disposable cluster. E2 can prove bounded integration and reveal API defaulting or CRD behavior. It does not prove managed identity, cloud load balancers, fleet scale, or production key custody.

## E3 — cloud or organizational integration

Real repository permissions, OCI registries, secret authorities, admission controls, workload identity, cluster access, and fleet catalogues participate. E3 supports claims about integration boundaries but may still use non-representative traffic and recovery conditions.

## E4 — operated evidence

The release system is exercised under representative traffic, incidents, controller upgrades, repository outages, key rotation, restore drills, and organizational ownership over time.

A higher class cannot repair a subject mismatch. A live cluster test against digest `A` cannot approve digest `B`. A controller health result cannot approve data rollback. Record subject, environment, tool version, time, and limitation with every evidence item. See the [evidence dossier](capstone/evidence-dossier.md).
