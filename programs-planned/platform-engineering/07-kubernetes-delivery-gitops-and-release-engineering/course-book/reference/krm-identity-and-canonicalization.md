# Reference — KRM identity and canonicalization

Logical identity is group, kind, namespace, and name. Canonical rendering rejects duplicate YAML keys and duplicate logical identities, removes server-owned metadata and status, preserves authored scalar types, orders resources by identity, and emits deterministic JSON.

The canonicalizer must record its schema and version. It should not erase explicit defaults whose semantics may change across Kubernetes versions. A render digest proves equivalence only under the declared profile.

## Extended reader notes

Kubernetes resource identity is the tuple `(API group, kind, namespace, name)`. Version is deliberately not part of identity because versions can represent the same logical resource through conversion. Namespace is empty for cluster-scoped objects. A render containing duplicate identities is rejected before policy evaluation because precedence would otherwise depend on ordering or tool behavior.

Canonicalization is claim-specific. Atlas removes `status` and server-generated metadata before computing a desired-set digest, but preserves scalar types, explicit fields, annotations, and user-owned values. Omitting `replicas` and declaring `replicas: 1` are not treated as identical, because they express different ownership even if server defaulting later yields the same live value.

A canonical digest proves only the normalized desired collection. It does not prove schema validity, admission success, live convergence, health, or correctness. Record the canonicalization profile and renderer version with the digest. Changing that profile is a release-toolchain change and may invalidate comparisons with older dossiers.
