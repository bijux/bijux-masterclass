# Capstone implementation map

The Python package maps course concepts to executable modules: canonicalization, Kustomize-style composition, Helm values validation, Git identity, inventory, reconciliation, health, ordering, promotion, secrets, progressive exposure, fleet recovery, and release policy.

The Go probe independently calculates resource identity, manifest digest, and desired/live drift for shared fixtures. Native Argo CD and Flux resources map the same invariants to real controller APIs.

## Extended reader notes

Use the Python semantic lane to study invariants and deterministic failure cases. Use the Go probe to confirm that a second implementation produces stable digest and diff behavior. Use native tools for full syntax, schema, and controller semantics.

Kustomize examples map to `kustomize_model.py`; Helm values and chart API map to `helm_model.py`; Argo CD and Flux resources map to the common reconciler and inventory; Rollouts and Flagger map to `progressive.py`; cluster catalogues map to `fleet.py`; candidate dossiers map to `models.py`, `promotion.py`, and `release.py`.

When native and semantic results differ, document the exact feature outside the bounded model. Never change the model silently to force agreement.
