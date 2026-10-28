# Computing reference preservation

This collection retains source from `bijux/bijux-courses`, branch `master`, at
commit `1a585c5ac73272477fb82efc6c08c572285fc880`. Its 570 original commits are ancestors of
this repository. Their identities, authors, parent relationships and original paths
are unchanged.

History import is incomplete: 570 of 1486 captured
source commits have been imported. Keep the source repository available until the
remaining history and local-only material are preserved and remotely verified.

Of the 623 tracked source files at this revision, 622 are
retained verbatim under this directory. The production backlog `TODO.md` remains
recoverable in original history instead of becoming a product backlog.
[SOURCE.json](SOURCE.json) accounts for the source paths, Git blobs, modes and
destinations.

The original manifest labels 545 entries complete and 2,455 planned.
These are preserved source claims, not a new assessment of correctness or
publication readiness. The collection remains outside supported-course CI,
qualification inputs and the published catalogue.

## Inspecting original history

Run from the repository root:

```sh
git merge-base --is-ancestor 1a585c5ac73272477fb82efc6c08c572285fc880 HEAD
git show 1a585c5ac73272477fb82efc6c08c572285fc880:README.md
git show 1a585c5ac73272477fb82efc6c08c572285fc880:TODO.md
git log 1a585c5ac73272477fb82efc6c08c572285fc880 -- manifests/modules.csv
```

Earlier commits use the original paths. A log filtered only by the new directory
may stop at an import boundary; use the original commit and path for older changes.
