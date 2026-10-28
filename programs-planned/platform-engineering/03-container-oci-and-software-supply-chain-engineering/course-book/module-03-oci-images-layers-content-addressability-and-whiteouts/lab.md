# Laboratory — Build, corrupt, and reconstruct an OCI image graph

## Goal

Construct the Atlas Probe OCI layout from deterministic inputs and prove every edge from index to final rootfs.

## Safety boundary

Work in a temporary layout. Do not modify the checked accepted release. Treat arbitrary tar extraction as hostile: use the course safe extractor and never extract unreviewed archives as root.

## Baseline

Build the probe layout twice with the controlled profile. Record index, manifest, config, layer digest, DiffID, and size.

## Hypothesis

Controlled rebuilds produce the same exact index digest, and ordered verified layer application produces the expected rootfs.

## Controlled action

1. Trace every descriptor and reconstruct the rootfs.
2. Recompress one layer with changed gzip metadata and compare blob digest/DiffID.
3. Add a lower-layer secret and a later whiteout; confirm the final rootfs hides it while the lower blob preserves it.
4. Change one byte in a config blob without updating its descriptor.
5. Attach a small artifact manifest to the image subject and discover it through referrer metadata.

## Oracle

The clean rebuilds are byte-identical. Recompression changes only the compressed identity. The secret remains recoverable from history. Config corruption fails descriptor verification. The artifact resolves only through the correct subject relationship.

## Evidence

Submit:

- object graph with media types and digests;
- digest/DiffID comparison table;
- safe rootfs inventory;
- lower-layer secret recovery proof using a synthetic token;
- corruption rejection output;
- artifact subject/referrer trace.

## Interpretation

Explain why each observation belongs to image structure, distribution identity, filesystem history, or release policy.

## Cleanup

Remove synthetic secret fixtures and temporary layouts. Rerun the checked capstone tour.

## Completion gate

You can account for every byte that determines the image digest and demonstrate why final-filesystem inspection alone is insufficient.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
