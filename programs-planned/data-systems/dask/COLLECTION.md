# Dask source collection

This planned collection preserves 12 source files in its current tree.
Its lessons, examples, toolchain and publication readiness still require review.
It remains outside supported-course CI, qualification input sets and the published
catalogue. Source manifests and verification claims are retained source documents;
they are not a new qualification of this collection.

The working rewrite is retained, including its untracked replacement chapters and tracked deletions. Inherited Make scaffolding is not a supported Dask verification route.

## Source preservation

[SOURCE.json](SOURCE.json) records original paths, content hashes, file modes,
source snapshots and explicit changes made for placement in this repository.
Original bytes remain available in the source snapshot commits:

- `9be89a36637f99965e3765cd082bac9689f40f43`: 5 mapped source files.
- `578660957986976d08d7bf497f526bd73fa21b08`: 12 mapped source files.

For an original mapped file, run `git show <snapshot>:<collection-path>/<mapped-path>`.
Source snapshots are preservation records created during consolidation, rather than
a reconstruction of the original authoring chronology. Source reviews are retained
for reference and do not establish independent approval.

The original two-commit source history is also reachable from this branch.
The current tree preserves the working rewrite, while the original Git commits
retain both earlier authoring revisions.

## Promotion

Dependency declarations receive security maintenance before course promotion.
Original source snapshots remain unchanged; `SOURCE.json` records the maintained
file hashes and the dependency changes separately from those original bytes.

Before promotion, establish the intended learner scope, reconcile source variants,
check references and relative links, qualify the actual supported commands and
toolchains, and register the accepted material with its supported owner. Keep
generated run output under the repository-root `artifacts/` directory.
