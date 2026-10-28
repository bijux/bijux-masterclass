# Platform Engineering source collection

This planned collection preserves 1,839 source files in its current tree.
Its lessons, examples, toolchain and publication readiness still require review.
It remains outside supported-course CI, qualification input sets and the published
catalogue. Source manifests and verification claims are retained source documents;
they are not a new qualification of this collection.

Seven source courses are retained. The GitOps guide owns program-book; other guide contexts remain under source-guides. Root Make currently selects the GitOps course only; full program qualification remains pending.

## Source preservation

[SOURCE.json](SOURCE.json) records original paths, content hashes, file modes,
source snapshots and explicit changes made for placement in this repository.
Original bytes remain available in the source snapshot commits:

- `ce71ed56180ef2413dd4aa152c7264d10eb62350`: 1,839 mapped source files.

For an original mapped file, run `git show <snapshot>:<collection-path>/<mapped-path>`.
Source snapshots are preservation records created during consolidation, rather than
a reconstruction of the original authoring chronology. Source reviews are retained
for reference and do not establish independent approval.

## Promotion

Dependency declarations receive security maintenance before course promotion.
Original source snapshots remain unchanged; `SOURCE.json` records the maintained
file hashes and the dependency changes separately from those original bytes.

Before promotion, establish the intended learner scope, reconcile source variants,
check references and relative links, qualify the actual supported commands and
toolchains, and register the accepted material with its supported owner. Keep
generated run output under the repository-root `artifacts/` directory.
