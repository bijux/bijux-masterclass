# Guide — Local Git delivery laboratory

The local Git lane exists to make revision identity and promotion visible without depending on a hosted provider. It uses one bare repository as the remote and separate working copies for application automation, environment review, and recovery.

## Required structure

```text
remote.git
candidate-worktree
review-worktree
recovery-worktree
```

Configure a synthetic identity and disable credential helpers. Protect the laboratory by creating it under a temporary directory and never adding a real remote URL.

A useful exercise creates three commits:

1. the accepted production revision;
2. a candidate that changes an immutable image digest;
3. a documentation-only commit that leaves the rendered set unchanged.

Record both commit and render identities. The exercise demonstrates that Git causality and executable desired state are related but not interchangeable.

## Simulating review

Use branches only as workflow pointers. The promotion record should contain the exact candidate commit. Create a proposal branch, merge it without rewriting history, and record the merge or fast-forward result. Then attempt a force push in the semantic policy model and verify rejection.

## Simulating outage

Rename or remove access to the bare repository while the semantic cluster retains its last applied inventory. The expected outcome is source-unavailable status, not empty desired state. Restore the repository and prove that reconciliation resumes from the exact commit.

## Evidence

Retain `git log --graph --decorate --all`, exact commit IDs, render digests, promotion records, and cleanup output. Do not retain synthetic credentials or temporary repository internals in the course manifest.

## Extended reader notes

Use a disposable repository with configured course identity. Create a baseline environment commit, a candidate commit selecting the same immutable artifact set, a deliberately unsafe change, and an explicit revert. Record commit objects rather than branch names. Inspect the graph and show that a revert creates new history rather than deleting the failed decision.

Add branch-like refs for `candidates/staging` and `production` only after the lineage is visible. Simulate an automation bot writing a candidate and a release owner promoting it. The bot must not have the credential used for production. Finally, make the repository temporarily unavailable and verify that the semantic reconciler retains last-known-good state instead of pruning.

The lab proves Git lineage and authority mechanics. It does not prove hosted branch protection, signed commits, repository disaster recovery, or identity integration.
