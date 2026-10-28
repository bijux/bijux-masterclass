# Computing reference preservation

This collection retains source from `bijux/bijux-courses`, branch `master`, at
commit `54f99514e1953a06f8cebc4dd583354c3a52375d`. Its 1,140 original commits are ancestors of
this repository. Their identities, authors, parent relationships and original paths
are unchanged.

History import is incomplete: 1140 of 1486 captured
source commits have been imported. Keep the source repository available until the
remaining history and local-only material are preserved and remotely verified.

Of the 1,659 tracked source files at this revision, 1,658 are
retained verbatim under this directory. The production backlog `TODO.md` remains
recoverable in original history instead of becoming a product backlog.
[SOURCE.json](SOURCE.json) accounts for the source paths, Git blobs, modes and
destinations.

The original manifest labels 1,114 entries complete and 1,886 planned.
These are preserved source claims, not a new assessment of correctness or
publication readiness. The collection remains outside supported-course CI,
qualification inputs and the published catalogue.

## Inspecting original history

Run from the repository root:

```sh
git merge-base --is-ancestor 54f99514e1953a06f8cebc4dd583354c3a52375d HEAD
git show 54f99514e1953a06f8cebc4dd583354c3a52375d:README.md
git show 54f99514e1953a06f8cebc4dd583354c3a52375d:TODO.md
git log 54f99514e1953a06f8cebc4dd583354c3a52375d -- manifests/modules.csv
```

Earlier commits use the original paths. A log filtered only by the new directory
may stop at an import boundary; use the original commit and path for older changes.
