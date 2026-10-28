# OCI object map

An OCI image is not one archive. It is a directed, content-addressed graph. Debugging and policy become much easier when every edge is named precisely.

```text
image index
  └─ descriptor(platform=linux/amd64) ──> image manifest
       ├─ config descriptor ─────────────> image configuration
       └─ layer descriptors[] ───────────> compressed layer blobs

artifact manifest
  ├─ subject descriptor ────────────────> image index or manifest
  └─ blob descriptors[] ────────────────> SBOM/provenance/signature payloads
```

## Descriptor

A descriptor is a typed integrity edge. Important fields are:

- `mediaType` — how the target bytes should be interpreted;
- `digest` — content identity of the exact stored bytes;
- `size` — byte-length integrity check;
- optional `platform` — selection claim for image-index children;
- optional `annotations` — descriptive metadata, never a replacement for digest identity.

Verification order is: fetch bytes, check size, compute digest, then parse according to media type. Parsing unverified bytes first allows the parser result to influence which object is believed to exist.

## Image index

An index selects one or more manifests. Platform descriptors are claims by the publisher. They must be checked against target content and evidence where platform truth matters. Adding, removing, or reordering descriptors changes index bytes and therefore the index digest even when child manifests remain unchanged.

## Image manifest

A platform-specific manifest references one configuration and an ordered list of compressed layers. Layer order is semantic. A manifest digest does not identify the same thing as its config digest or any child layer digest.

## Image configuration

The configuration records:

- rootfs DiffIDs for uncompressed layer content;
- history entries;
- process defaults such as entrypoint, command, environment, working directory, labels, and declared user;
- architecture and operating-system metadata.

These are defaults and image claims. A runtime or orchestrator may override many of them.

## Layer blobs and DiffIDs

Manifest layer digests identify compressed bytes. Config `rootfs.diff_ids` identify uncompressed tar bytes. Two compression encodings can share a DiffID while having different distribution digests. Chain identity and snapshot behavior commonly use uncompressed identities; registries distribute compressed blobs.

## Artifact and subject

Supply-chain evidence must name an immutable subject. An artifact manifest can point at an image index or platform manifest and carry typed evidence blobs. Discovery through referrers is useful only after the returned artifact’s `subject` is checked against the candidate being authorized.

## Review questions

1. Which object is the release subject: index or one platform manifest?
2. Does every descriptor’s size and digest verify?
3. Are all required child platforms present and independently evidenced?
4. Do config DiffIDs correspond to the uncompressed layer stream?
5. Are evidence artifacts bound to the current subject rather than a prior digest?
6. Is any mutable tag being mistaken for an object identity?
