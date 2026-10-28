# Computing reference preservation

This collection retains source from `bijux/bijux-courses`, branch `master`, at
commit `dda1bcd49faa48ab8d8e1a9b247d1602ff7cb0b7`. Its 190 original commits are ancestors of
this repository. Their identities, authors, parent relationships and original paths
are unchanged.

History import is incomplete: 190 of 1486 captured
source commits have been imported. Keep the source repository available until the
remaining history and local-only material are preserved and remotely verified.

Of the 258 tracked source files at this revision, 257 are
retained verbatim under this directory. The production backlog `TODO.md` remains
recoverable in original history instead of becoming a product backlog.
[SOURCE.json](SOURCE.json) accounts for the source paths, Git blobs, modes and
destinations.

The original manifest labels 181 entries complete and 2,819 planned.
These are preserved source claims, not a new assessment of correctness or
publication readiness. The collection remains outside supported-course CI,
qualification inputs and the published catalogue.

## Inspecting original history

Run from the repository root:

```sh
git merge-base --is-ancestor dda1bcd49faa48ab8d8e1a9b247d1602ff7cb0b7 HEAD
git show dda1bcd49faa48ab8d8e1a9b247d1602ff7cb0b7:README.md
git show dda1bcd49faa48ab8d8e1a9b247d1602ff7cb0b7:TODO.md
git log dda1bcd49faa48ab8d8e1a9b247d1602ff7cb0b7 -- manifests/modules.csv
```

Earlier commits use the original paths. A log filtered only by the new directory
may stop at an import boundary; use the original commit and path for older changes.
