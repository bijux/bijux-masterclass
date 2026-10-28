# Worked answers — Flux controller composition, sources, and image automation

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why is the source artifact status more important than the configured branch name?

The status identifies the exact commit or OCI digest consumed by downstream controllers. The branch is a mutable selection rule. Diagnosis and release evidence need the resolved immutable artifact revision and digest, especially when source observation occurs at different times.

## 2. What does Flux Kustomization `dependsOn` guarantee?

It delays reconciliation until the named dependency reports Ready according to the configured semantics. It does not create atomic rollback or combine both reconciliations into one transaction. Upstream changes remain if downstream work later fails.

## 3. Why must readiness expressions test observed generation?

Without generation awareness, a success condition from an older spec can satisfy the expression after a new desired change. Downstream reconciliation would begin using stale prerequisite state. The expression should bind status to the current generation and authoritative condition.

## 4. What release-identity problem is created by post-build substitution from a live ConfigMap?

Rendered output can change when the ConfigMap changes even though the Git source artifact is unchanged. The substitution object identity and content must enter the release record, or production loses reproducibility. For sensitive values, evidence should record a non-secret version identity rather than plaintext.

## 5. How does Flux HelmRelease differ from using Helm only as a renderer?

HelmRelease is reconciled by helm-controller and maintains Helm install, upgrade, test, remediation, and release-state behavior. Renderer-only use produces manifests that another controller owns directly. Failure, rollback, hooks, inventory, and history therefore differ.

## 6. Why is an ImagePolicy result only a candidate?

It applies a selection rule to registry metadata. It does not establish signature, provenance, vulnerability disposition, compatibility, environment fitness, or rollback safety. Those gates attach to the selected digest before promotion.

## 7. What permissions should ImageUpdateAutomation have?

Only the approved repository, path, and proposal branch; non-force updates; no destructive refspecs; and credentials unable to merge production unless explicitly authorized. Commits should identify old and new digests and remain reviewable.

## 8. How should a missed webhook affect Flux reconciliation?

It may delay immediate source refresh, but periodic reconciliation should eventually observe the change. Webhooks are accelerators, not the sole delivery guarantee. A missed event must not permanently lose the desired revision.

## 9. Why are controller and CRD upgrades one release?

New controller binaries may expect new schemas and new schemas may expose fields old controllers do not understand. Flux release notes can require CRD changes with controller changes. The upgrade must record compatibility, order, rollback, and observed readiness as one governed platform change.

## 10. How does controller decomposition improve diagnosis?

Each resource exposes a bounded transition: source acquisition, Kustomize apply, Helm release, image selection, or notification. The earliest non-Ready condition localizes the failure. The cost is a larger dependency graph whose status and generation semantics must be understood.

## 11. Why can tenant impersonation still be unsafe with shared controllers?

A Kustomization may apply as a scoped ServiceAccount, but shared controllers can read source artifacts, Secrets, and cluster-wide resources according to their own permissions. Cross-namespace references and privileged ServiceAccounts must be restricted at the platform boundary.

## 12. Which invariants must remain identical between Argo CD and Flux lanes?

Immutable source and artifact identity, deterministic render evidence, explicit inventory, protected-resource policy, bounded credentials, environment promotion rules, separate health/data gates, and categorical release decisions. Product-specific status and APIs may differ; safety guarantees must not.
