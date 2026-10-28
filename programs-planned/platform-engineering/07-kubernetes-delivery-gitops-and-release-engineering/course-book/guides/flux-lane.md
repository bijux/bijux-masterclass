# Guide — Flux native lane

Trace Flux through its custom-resource graph rather than treating it as one controller.

Begin with `GitRepository` or `OCIRepository` and capture the resolved artifact revision and digest. Then inspect each `Kustomization` or `HelmRelease`, its source reference, dependency, ServiceAccount, health checks, decryption, prune, interval, timeout, and observed generation.

For image automation, separate registry reflection, selection policy, and Git mutation. The selected tag is not approval. The Git commit must write or bind the digest and remain within a bounded repository path.

When diagnosis reaches a failed workload, walk backward to the earliest non-Ready source or reconciler. A stale dependency condition, substitution input, or chart source can explain the failure more accurately than the final Pod status.

## Extended reader notes

Follow the Flux object chain rather than treating Flux as one controller. Verify GitRepository revision and artifact, Kustomization source reference and inventory, HelmRelease history and remediation, image discovery and policy, automation write target, and notification behavior.

Exercise a missed webhook and prove interval reconciliation still observes the commit. Break the source and verify downstream objects report stale or failed source without deleting live inventory. Make an image candidate available and prove automation writes only the candidate branch. Review the RBAC and repository credentials of each controller family.

The comparison with Argo CD should end in a common release dossier, not a winner.
