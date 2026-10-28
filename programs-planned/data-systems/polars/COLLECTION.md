# Polars source collection

This planned collection preserves 12 source files in its current tree.
Its lessons, examples, toolchain and publication readiness still require review.
It remains outside supported-course CI, qualification input sets and the published
catalogue. Source manifests and verification claims are retained source documents;
they are not a new qualification of this collection.

The working rewrite is retained, including its untracked replacement chapters and tracked deletions. Inherited Make scaffolding is not a supported Polars verification route.

## Source preservation

[SOURCE.json](SOURCE.json) records original paths, content hashes, file modes,
source snapshots and explicit changes made for placement in this repository.
Original bytes remain available in the source snapshot commits:

- `4f4efac8ec7f4131768eb040bd6ec0ddba52dfb1`: 5 mapped source files.
- `5906d73843b20dbd72c181c2e4e304397d02a243`: 12 mapped source files.

For an original mapped file, run `git show <snapshot>:<collection-path>/<mapped-path>`.
Source snapshots are preservation records created during consolidation, rather than
a reconstruction of the original authoring chronology. Source reviews are retained
for reference and do not establish independent approval.

The original two-commit source history is also reachable from this branch.
The current tree preserves the working rewrite, while the original Git commits
retain both earlier authoring revisions.

## Promotion

Before promotion, establish the intended learner scope, reconcile source variants,
check references and relative links, qualify the actual supported commands and
toolchains, and register the accepted material with its supported owner. Keep
generated run output under the repository-root `artifacts/` directory.
