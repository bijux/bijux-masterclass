# Computing reference preservation

This collection retains source from `bijux/bijux-courses`, branch `master`, at
commit `71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c`. Its 1,486 original commits are ancestors of
this repository. Their identities, authors, parent relationships and original paths
are unchanged.

All captured source history has been imported. Remote source retirement still requires
verification against the accepted default branch in a fresh GitHub clone.

Of the 2,962 tracked source files at this revision, 2,961 are
retained verbatim under this directory. The production backlog `TODO.md` remains
recoverable in original history instead of becoming a product backlog.
[SOURCE.json](SOURCE.json) accounts for the source paths, Git blobs, modes and
destinations.

The original manifest labels 1,442 entries complete and 1,558 planned.
These are preserved source claims, not a new assessment of correctness or
publication readiness. The collection remains outside supported-course CI,
qualification inputs and the published catalogue.

## Inspecting original history

Run from the repository root:

```sh
git merge-base --is-ancestor 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c HEAD
git show 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c:README.md
git show 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c:TODO.md
git log 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c -- manifests/modules.csv
```

Earlier commits use the original paths. A log filtered only by the new directory
may stop at an import boundary; use the original commit and path for older changes.

## Local-only material

The untracked SDRE-055 chapter is preserved verbatim as a draft; its manifest row
remains planned. Twelve original local Git blobs without known paths are retained
in an ancestor recovery commit. `SOURCE.json` records their object IDs and recovery
paths without inventing filenames or original development history.

The complete original local working tree, including ignored outputs, caches and
downloaded references, was captured and hash-verified under the repository-root
`artifacts/course-consolidation/` directory. Those recovery files are local and are
not tracked or published as curriculum source. Their archive checksum is recorded
in `SOURCE.json`.
