# Standards and reference implementations

The vendor-neutral foundation is the OpenGitOps principles: desired state is declarative, versioned and immutable, pulled automatically, and continuously reconciled. These principles define properties, not a repository layout or product.

The Kubernetes Resource Model supplies object identity, API semantics, managed fields, status, conditions, ownership, and reconciliation boundaries. Kustomize is the template-free composition lane. Helm is the chart and package lane. Argo CD is the primary GitOps implementation; Flux is the comparative controller-oriented implementation. Argo Rollouts is the primary progressive-delivery example, with Flagger used for comparison. SOPS and External Secrets model two secret-delivery custody patterns.

The reference release pins Kubernetes 1.36.2, Kustomize 5.8.1, Helm 4.2.3, Argo CD 3.5.0, Flux 2.9.4, Argo Rollouts 1.9.1, SOPS 3.13.3, and External Secrets 2.9.0. Pins are evidence anchors, not permanent recommendations. A real platform may choose another supported patch release after compatibility, upgrade, rollback, and recovery proof.

Keep version axes separate: source commit; OCI and chart digest; renderer version; controller version; Kubernetes version; environment release; Atlas delivery profile; and Course 6 data phase. “Version 1.7” alone is not a release identity.
