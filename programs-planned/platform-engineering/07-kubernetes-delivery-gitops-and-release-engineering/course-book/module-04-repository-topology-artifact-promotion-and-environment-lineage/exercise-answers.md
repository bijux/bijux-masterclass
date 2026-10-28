# Worked answers — Repository topology, artifact promotion, and environment lineage

These answers are reference reasoning, not phrases to memorize. A different answer is acceptable only when it preserves the same ownership, compatibility, and evidence constraints.

## 1. Why is repository count less important than authority separation?

A monorepo can enforce strong separation through paths, code ownership, credentials, and workflows, while several repositories can still share one overpowered automation identity. The design goal is to control who can change application source, artifact metadata, environment desired state, and release decisions. Repository count is an implementation choice serving those boundaries.

## 2. Why does Atlas use environment directories rather than long-lived environment branches?

Directories make cross-environment comparison straightforward and avoid persistent branch divergence and merge conflict. They also permit one repository-level reconciliation and structured path ownership. The trade-off is that a single commit can touch several environments, so production paths require distinct approval and automation scopes.

## 3. What is the difference between promotion and rebuild?

Promotion selects the same immutable artifact identity for a more demanding environment. Rebuild creates new bytes and therefore a new evidence subject. Even if source and semantic version are unchanged, a rebuild can change dependencies, base image, compiler, or metadata and must be evaluated as a new candidate.

## 4. Why should a release lineage record a predecessor explicitly?

Chronological Git history includes unrelated commits, failed proposals, and reverts. An explicit predecessor identifies the release state that a candidate replaces, enabling compatibility, rollback, migration-phase, and incident reasoning. It also distinguishes a forward corrective release from a selection of a prior desired state.

## 5. What evidence becomes stale when only the policy version changes?

A candidate previously accepted under another policy may no longer satisfy current requirements. The artifact bytes have not changed, but the decision rule has. Release status must record the policy version, and the candidate must be re-evaluated. Evidence can remain usable while the policy result changes.

## 6. Why should image automation write a digest in addition to a tag?

The tag can move between selection and reconciliation. The digest binds the proposed update to exact bytes and lets reviewers compare it with signatures, provenance, and test evidence. The tag remains useful for human version selection, but the desired state should pin the digest.

## 7. How should a repository outage affect running workloads?

Existing last-known-good workloads should continue unless another failure requires action. The controller should report source staleness and stop applying unverified changes. Failure to fetch is not an empty desired state and must never trigger prune. Bootstrap and new promotion may be unavailable until source integrity is restored.

## 8. What does a signed commit prove?

It proves possession of a signing credential associated with the signature and that the signed content was not modified afterward. It does not prove the signer was authorized for production, that review occurred, that the artifacts are trustworthy, or that the change is compatible. Those require independent repository and release policy evidence.

## 9. Why can `git revert` fail to reproduce a previous deployment?

It creates a new commit and may run under different renderer versions, remote dependencies, policies, or defaults. External artifacts may have moved if they were not digest-pinned. The new release must be rendered and evaluated explicitly rather than assumed identical to the earlier environment state.

## 10. What should a production promotion pull request summarize?

Candidate and predecessor identities, artifact and render digests, source and rendered diffs, compatibility, policy results, migration phase, recovery gates, progressive-delivery plan, rollback boundaries, approvals, and missing evidence. The summary should make risk review possible without hiding detail in external dashboards.

## 11. When is automated production promotion defensible?

Only when the change class, immutable identity, evidence freshness, compatibility, policy, rollback boundary, monitoring, and incident controls are strong enough that no human judgment is required. A semantic version label alone is not sufficient. The automation must remain bounded to approved paths and subjects.

## 12. Why is Git not a complete release database?

Git records file revisions and authorship history. It does not natively model evidence expiry, environment observations, progressive-delivery metrics, approvals from external systems, incident state, or runtime outcome populations. Structured release records should link those facts to immutable commits.
