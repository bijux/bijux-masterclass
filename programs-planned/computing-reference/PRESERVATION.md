# Computing reference preservation

This collection retains the source from `bijux/bijux-courses`, branch `master`, at
commit `71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c`. Its 1,486 original commits are
part of this repository's ancestry. Their commit identities, parent relationships,
authors and original paths are unchanged.

The source tree has 2,962 tracked files. Of these, 2,961 are retained verbatim under
this directory, including 1,442 review records under `artifacts/reviews/`.
The production backlog `TODO.md` is retained in the original history rather than
copied into the product tree. [SOURCE.json](SOURCE.json) accounts for every original
path and records its Git blob, mode and destination.

The local source object database also contained twelve blobs that were not
reachable from a branch or tag. Their original paths are unknown. They are
retained in an ancestor recovery commit, with their object IDs and recovery paths
recorded in `SOURCE.json`; no original filenames or development history are
invented for them.

The original local checkout also contained the untracked chapter SDRE-055,
“Technical Investigation Under Pressure.” Its bytes are retained unchanged. Its
chapter status remains `draft`, and its manifest entry remains `planned`.

These are preservation facts. The original manifest's 1,442 `complete` and 1,558
`planned` labels are not a new assessment of correctness or publication readiness.
The preserved tools remain available for inspection; they are not enrolled in
Masterclass's course CI or published catalogue.

## Inspecting the original history

Run these commands from the repository root:

```sh
git merge-base --is-ancestor 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c HEAD
git show 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c:README.md
git show 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c:TODO.md
git log 71f14e0a9ff959e0dbd5ef87720ce3d0b8e6ee7c -- manifests/modules.csv
```

Earlier commits use the source repository's original paths. A log filtered only
by the new directory may stop at the import boundary; use the original commit and
path when following older changes.

## Local recovery material

The consolidation also captured the complete local working tree, including ignored
outputs, caches and downloaded references, and verified both Git backup bundles
by restoring them. These recovery files live under the repository-root
`artifacts/course-consolidation/` directory. They are local recovery material and
are not tracked or published as curriculum source. The working-tree archive's
checksum is recorded in `SOURCE.json`.

Source-repository deletion requires a separate remote verification: the original
commit graph and retained source files must be present in the accepted Masterclass
history and survive a fresh clone from GitHub. A local import alone is insufficient.
