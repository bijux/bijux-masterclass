# Worked answers — Helm chart engineering, packaging, and upgrade semantics

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why are Helm values a public API?

Environment repositories, automation, and operators depend on their names, types, defaults, and meaning. Changing those inputs can break consumers even if templates still render valid Kubernetes objects. Values therefore need schema, versioning, deprecation, upgrade notes, and compatibility tests like any other interface.

## 2. Why should a chart not expose the complete Deployment spec as values?

It transfers platform invariants and implementation details to every consumer, makes validation difficult, and prevents safe evolution. A chart should expose decisions consumers legitimately own while keeping security, lifecycle, selector, and availability invariants inside a reviewed implementation. Advanced escape hatches should be narrow and policy-gated.

## 3. What does `values.schema.json` prove and not prove?

It proves that values satisfy declared structural and selected semantic constraints before rendering. It can reject unknown keys, wrong types, invalid ranges, and malformed digests. It does not prove that rendered resources are valid for the target cluster, that an upgrade is compatible, or that the workload behaves correctly.

## 4. Why are live-cluster lookups in a production template problematic?

They make output depend on the cluster observation point rather than only immutable release inputs. The same source can render differently in CI, staging, and production, undermining review and reproducibility. If discovered state is required, it should enter as an explicit, versioned input or be handled by a controller with clear ownership.

## 5. Why should a database not usually be a dependency of an application chart?

The database has independent data authority, backup, restore, upgrade, credential, and availability lifecycles. Coupling it to application install or delete grants the application chart destructive ownership and makes rollback ambiguous. The application chart should consume a declared service contract unless the package is deliberately a single-owner appliance.

## 6. What special lifecycle issue do CRDs create?

They are cluster-scoped APIs consumed by multiple resources and possibly multiple teams. Helm’s `crds/` installation path does not perform ordinary upgrades or deletion, while templated CRDs create ordering and ownership risks. The chart must state who owns CRD installation, conversion, upgrade, and retirement.

## 7. Why is a pre-upgrade hook an unsafe place for an opaque migration?

Hooks can retry, rerun on rollback, outlive failed releases, and execute outside a transaction with the main workload. A non-idempotent migration may repeat or commit while the application upgrade fails. Durable migration identity, phase ordering, compatibility, and recovery must exist independently of hook convenience.

## 8. What can `--atomic` roll back, and what can it not roll back?

It can request rollback of Helm-managed Kubernetes release resources when install or upgrade fails. It cannot undo external side effects, data transformations, emitted events, credential revocation, or state owned by another controller. In GitOps, an imperative rollback may also be overwritten by the desired revision unless Git changes.

## 9. Why should promotion record both chart digest and rendered-set digest?

The chart digest identifies the package bytes; the render digest identifies output for a specific values set and renderer. One chart can render many outputs, and different packages can theoretically render the same output. Both identities are needed for provenance, review, and diagnosis.

## 10. How does Argo CD Helm integration differ conceptually from Flux HelmRelease?

Argo CD commonly uses Helm to render manifests and then owns them through the Application inventory. Flux HelmRelease delegates to helm-controller and preserves Helm release lifecycle and state. Hooks, tests, rollback, inventory, and drift semantics therefore differ. The integration mode must be recorded.

## 11. What should an upgrade fixture contain?

It should include the prior accepted chart and values, target chart and values, rendered diffs, changed value API, immutable-field checks, data compatibility requirements, hook behavior, and expected rollout. It should test both default and production profiles and identify any manual migration.

## 12. Why can a repackaged chart with unchanged templates require new evidence?

Archive metadata or dependency content can change the package digest. The production subject is therefore different even if the rendered set currently matches. Supply-chain, signature, provenance, and reproducibility evidence attach to the package bytes and must be refreshed for the new subject.
