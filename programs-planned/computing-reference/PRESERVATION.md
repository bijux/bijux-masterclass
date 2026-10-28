# Computing reference preservation

This collection retains source from `bijux/bijux-courses`, branch `master`, at
commit `34ff851141a04a7eb58ebea27bd331da30e7cd66`. Its 380 original commits are ancestors of
this repository. Their identities, authors, parent relationships and original paths
are unchanged.

History import is incomplete: 380 of 1486 captured
source commits have been imported. Keep the source repository available until the
remaining history and local-only material are preserved and remotely verified.

Of the 447 tracked source files at this revision, 446 are
retained verbatim under this directory. The production backlog `TODO.md` remains
recoverable in original history instead of becoming a product backlog.
[SOURCE.json](SOURCE.json) accounts for the source paths, Git blobs, modes and
destinations.

The original manifest labels 370 entries complete and 2,630 planned.
These are preserved source claims, not a new assessment of correctness or
publication readiness. The collection remains outside supported-course CI,
qualification inputs and the published catalogue.

## Inspecting original history

Run from the repository root:

```sh
git merge-base --is-ancestor 34ff851141a04a7eb58ebea27bd331da30e7cd66 HEAD
git show 34ff851141a04a7eb58ebea27bd331da30e7cd66:README.md
git show 34ff851141a04a7eb58ebea27bd331da30e7cd66:TODO.md
git log 34ff851141a04a7eb58ebea27bd331da30e7cd66 -- manifests/modules.csv
```

Earlier commits use the original paths. A log filtered only by the new directory
may stop at an import boundary; use the original commit and path for older changes.
