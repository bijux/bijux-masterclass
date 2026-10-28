# API Engineering source collection

This planned collection preserves 3,552 source files in its current tree.
Its lessons, examples, toolchain and publication readiness still require review.
It remains outside supported-course CI, qualification input sets and the published
catalogue. Source manifests and verification claims are retained source documents;
they are not a new qualification of this collection.

Both source editions survive in Git history, including the five files unique to the earlier edition. Handoff OpenAPI fixtures under dist are maintained inputs and are retained.

## Source preservation

[SOURCE.json](SOURCE.json) records original paths, content hashes, file modes,
source snapshots and explicit changes made for placement in this repository.
Original bytes remain available in the source snapshot commits:

- `3a6a670a0b676f6937a625fa280751dcd3cb0078`: 3,529 mapped source files.
- `54eea52b73f106c0090f2fa068ca19807f834138`: 3,552 mapped source files.

For an original mapped file, run `git show <snapshot>:<collection-path>/<mapped-path>`.
Source snapshots are preservation records created during consolidation, rather than
a reconstruction of the original authoring chronology. Source reviews are retained
for reference and do not establish independent approval.

## Promotion

Before promotion, establish the intended learner scope, reconcile source variants,
check references and relative links, qualify the actual supported commands and
toolchains, and register the accepted material with its supported owner. Keep
generated run output under the repository-root `artifacts/` directory.
