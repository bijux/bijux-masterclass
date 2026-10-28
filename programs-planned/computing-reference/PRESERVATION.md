# Computing reference preservation

This collection retains source from `bijux/bijux-courses`, branch `master`, at
commit `ace9bee8a73152c91078d23968e5e4dcc11d0c8b`. Its 1,330 original commits are ancestors of
this repository. Their identities, authors, parent relationships and original paths
are unchanged.

History import is incomplete: 1330 of 1486 captured
source commits have been imported. Keep the source repository available until the
remaining history and local-only material are preserved and remotely verified.

Of the 2,171 tracked source files at this revision, 2,170 are
retained verbatim under this directory. The production backlog `TODO.md` remains
recoverable in original history instead of becoming a product backlog.
[SOURCE.json](SOURCE.json) accounts for the source paths, Git blobs, modes and
destinations.

The original manifest labels 1,294 entries complete and 1,706 planned.
These are preserved source claims, not a new assessment of correctness or
publication readiness. The collection remains outside supported-course CI,
qualification inputs and the published catalogue.

## Inspecting original history

Run from the repository root:

```sh
git merge-base --is-ancestor ace9bee8a73152c91078d23968e5e4dcc11d0c8b HEAD
git show ace9bee8a73152c91078d23968e5e4dcc11d0c8b:README.md
git show ace9bee8a73152c91078d23968e5e4dcc11d0c8b:TODO.md
git log ace9bee8a73152c91078d23968e5e4dcc11d0c8b -- manifests/modules.csv
```

Earlier commits use the original paths. A log filtered only by the new directory
may stop at an import boundary; use the original commit and path for older changes.
