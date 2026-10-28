# Orientation laboratory — Trace one release from source to runtime

## Goal

Build a causal map from source files to an executed Atlas process without using the word “container” as an unexplained box.

## Safety boundary

Use only the checked course fixtures and loopback interfaces. Do not push course keys or images to a public registry. The private signing key is an intentionally public laboratory fixture despite its file mode.

## Baseline

Run:

```bash
python capstone/scripts/run_capstone_tour.py
```

Save the report from `capstone/reports/capstone-tour.json`.

## Hypothesis

The accepted release can be reconstructed as a graph in which every edge is justified by an exact digest or an explicit runtime mapping.

## Controlled action

Choose the `linux/amd64` API image. Starting from its image-index descriptor, record:

1. the selected manifest descriptor;
2. the configuration descriptor;
3. every layer descriptor and DiffID;
4. the executable path in the reconstructed root filesystem;
5. the runtime UID/GID, mounts, arguments, environment, and namespace profile;
6. the SBOM and provenance artifact manifests attached to the image subject;
7. the signature envelope and verification key fingerprint.

Then change one byte in a copied layer blob and rerun the relevant digest check.

## Oracle

The unmodified graph resolves completely. The modified blob is rejected before execution because its calculated digest no longer matches its descriptor.

## Evidence

Submit:

- `orientation-release-trace.md`;
- a diagram containing object media types and digests;
- the failing command output for the modified blob;
- one paragraph distinguishing integrity from trust.

## Interpretation

If your trace begins with a tag and ends with “Docker runs it,” it is incomplete. A tag is a mutable lookup name, and Docker is one implementation. The exercise is complete only when the standard objects and runtime obligations are visible.

## Cleanup

Delete the copied and modified blob. Rerun the capstone tour and confirm the checked release remains unchanged.

## Completion gate

You can point to the exact object that proves each transition and name at least three properties the tour still does not prove in a production environment.

## Continue

- [Orientation checkpoint](checkpoint.md)
- [Orientation chapter](index.md)
