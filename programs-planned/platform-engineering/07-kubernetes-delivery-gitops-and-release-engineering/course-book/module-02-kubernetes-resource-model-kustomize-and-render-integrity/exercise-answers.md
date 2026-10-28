# Worked answers — Kubernetes Resource Model, Kustomize, and render integrity

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why should a renderer be treated like a compiler?

It transforms reviewed source into the actual objects submitted to Kubernetes. Tool version, remote inputs, plugins, schemas, and environment variables can change output. Like a compiler, it therefore needs pinned identity, deterministic inputs, warnings, output artifacts, and reproducibility evidence. Reviewing only source ignores the executable result.

## 2. What fields form the logical identity of a Kubernetes resource for inventory purposes?

API group, kind, namespace, and name form the logical identity. Filename and document order do not. Resource version identifies an API schema version, not a different logical object. Stable identity is required for patches, inventories, ownership, drift, and prune decisions.

## 3. When is an environment overlay evidence that the base is defective?

When every overlay applies the same corrective patch or when production alone must repair a universal safety property such as non-root execution, valid probes, stable selectors, or secret handling. Those are workload invariants and belong in the base. An overlay should express a legitimate environmental difference, not conceal a broken shared contract.

## 4. Why can replacing a container array be dangerous?

Many patch formats replace arrays as a whole. A patch intended only to change one image may remove sidecars, ports, environment variables, or security settings. Ordered index patches also depend on array order. A schema-aware merge or explicit named target is safer when available, and the rendered diff must prove the complete result.

## 5. What does a content-hashed ConfigMap name accomplish?

It makes configuration identity part of the referenced object name. When content changes, the generated name and Pod template reference change, causing a new rollout and preventing a workload from silently consuming mixed configuration. It does not prove that the application reloads correctly or that the new configuration is valid.

## 6. Why is a remote base pinned to a branch incompatible with reproducible promotion?

The branch can resolve to different commits at different render times. Production may receive output that staging never exercised even though the local environment commit is identical. Promotion must identify the exact remote commit or vendored artifact and include it in render identity.

## 7. Which fields should be excluded from a desired-state render digest?

Fields not authored as desired state, such as `status`, server-assigned resourceVersion, UID, managedFields, and timestamps, should be excluded. The exact exclusion list must be explicit. Defaultable spec fields require care: removing an explicit default can change behavior across API versions, so canonicalization should not erase authored semantics.

## 8. Why is force-conflict in Server-Side Apply a migration rather than a routine flag?

Forcing conflicts transfers field ownership from another manager. That can be legitimate, but it changes authority and may erase an operator, autoscaler, or human-controlled value. The transferred field set, prior manager, new manager, compatibility, and rollback must be reviewed. Global force hides ownership defects.

## 9. What should a rendered-diff review show beyond ordinary text changes?

It should show resource identities added and removed, field-level changes, image and chart digests, API-version changes, protected-resource implications, ownership changes, policy results, and the canonical render digest. This lets reviewers reason about controller actions rather than formatting.

## 10. Why is base64-encoded Secret data still sensitive rendered output?

Base64 is reversible encoding, not encryption. Anyone who can read the repository, CI logs, rendered artifacts, or controller cache can recover the plaintext. Sensitive values require an explicit encryption or external-secret authority boundary, and rendered-output retention must be controlled.

## 11. How can two source commits legitimately share one render digest?

A commit may change comments, documentation, file ordering, or source structure without changing the canonical Kubernetes objects. Keeping both commit and render identities preserves review history while proving equivalent desired state. Collapsing them loses either causality or executable equivalence.

## 12. What is the minimum evidence for claiming a production render is deterministic?

Record immutable local and remote source identities, renderer and plugin versions, all variable inputs, schema profile, canonical output, and render digest. Re-run in a clean environment and obtain the same digest. A single successful render is not determinism evidence.
