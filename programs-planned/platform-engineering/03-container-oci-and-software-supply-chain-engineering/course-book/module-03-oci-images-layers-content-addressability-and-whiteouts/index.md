# Module 3 — OCI images, layers, content addressability, and whiteouts

A container image is not a tar file and not a filesystem snapshot. It is a directed, content-addressed graph of typed JSON documents and blobs. The graph can identify one platform-specific root filesystem, many platform variants, or an artifact attached to another subject.

This module makes every byte in that graph accountable.

## Learning outcomes

By the end of the module you can:

- navigate descriptors, manifests, configurations, indexes, and image layouts;
- distinguish compressed layer digests from uncompressed DiffIDs;
- apply ordered layer changes including whiteouts and opaque directories;
- explain why file deletion in a later layer does not erase earlier bytes;
- construct deterministic layer archives and canonical JSON objects;
- trace a runtime rootfs back to exact image objects;
- attach a non-image artifact to an image subject;
- diagnose digest, media-type, size, and platform-selection failures.

## Descriptors are typed integrity edges

An OCI descriptor commonly contains:

```json
{
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "digest": "sha256:...",
  "size": 1234,
  "platform": {
    "os": "linux",
    "architecture": "amd64"
  }
}
```

The digest identifies exact bytes. Size helps validation and transfer. Media type tells the consumer how to interpret the bytes. Optional platform data helps select a variant.

A digest without a media type proves byte identity but not meaning. A media type without a verified digest invites substitution. A descriptor is the edge that binds identity, interpretation, and expected length.

The course verifier checks all three before parsing a child object.

## The platform-specific image manifest

An image manifest points to:

- one image configuration descriptor;
- an ordered list of filesystem layer descriptors;
- optional annotations;
- optionally, a subject descriptor when the manifest represents an attached artifact.

For a runnable image, the configuration describes execution defaults and the filesystem history. The layer list describes compressed changesets. Applying the layers in order reconstructs the rootfs view.

The manifest digest is therefore the identity of a specific configuration-and-layer combination. Changing an environment variable in the config changes the config digest, manifest bytes, and manifest digest even if every filesystem layer remains the same.

## Configuration connects distribution to execution

An OCI image configuration contains two important families of data.

### Runtime defaults

- user;
- environment;
- entrypoint;
- command;
- working directory;
- exposed ports;
- stop signal;
- volume hints;
- labels.

These are defaults. A runtime or orchestrator may override them.

### Rootfs and history

- ordered layer DiffIDs;
- history records describing build steps;
- creation metadata and platform information.

The number and order of non-empty filesystem history entries should reconcile with the DiffID list. History is not a secure audit trail: authors can omit or modify descriptive text. Provenance comes later.

## Digest and DiffID are different identities

A layer distributed through a registry is usually a compressed tar archive. Its descriptor digest is calculated over the compressed bytes:

```text
sha256(compressed layer blob)
```

The image configuration stores a DiffID calculated over the uncompressed tar stream:

```text
sha256(uncompressed tar bytes)
```

The same uncompressed tar stream compressed with different gzip metadata or compression levels can have:

- the same DiffID;
- a different blob digest;
- a different size.

This distinction allows a runtime to verify the uncompressed changeset while distribution systems address the transmitted blob. Confusing the two causes cache misses, verification failures, and incorrect content-store records.

## Layers are changesets

A layer describes additions, modifications, and deletions relative to the previous rootfs view. It does not necessarily contain a complete filesystem.

Applying layers:

```text
empty root
  + base layer
  + application layer
  + configuration layer
  = final rootfs view
```

If two layers contain the same path, the later entry wins. Metadata changes such as mode, ownership, links, and xattrs matter alongside file bytes.

The application algorithm must defend against archive path traversal, absolute paths, unsafe links, device nodes, and metadata that escapes the intended root.

## Whiteouts express deletion

A later tar archive cannot literally remove a path from an earlier immutable blob. OCI layer conventions use whiteout entries.

A file named:

```text
path/.wh.secret.txt
```

means that `path/secret.txt` from lower layers should be absent in the final rootfs.

An opaque whiteout:

```text
path/.wh..wh..opq
```

means lower-layer children of `path/` should be hidden before applying new entries in that directory.

Whiteouts change the assembled view. They do not erase historical bytes from lower blobs.

This is why the following build is unsafe:

```dockerfile
COPY production-token /tmp/token
RUN use-token && rm /tmp/token
```

The final rootfs lacks `/tmp/token`, but the earlier layer still contains it. Anyone who can fetch the image blobs can recover it.

Secrets must not enter the build context or committed layer in the first place. Build secret mounts exist precisely to avoid this history leak.

## Determinism requires controlling archive metadata

Two tar archives with identical visible files can differ because of:

- file order;
- timestamps;
- UID/GID and owner names;
- mode bits;
- pax headers;
- extended attributes;
- link encoding;
- gzip timestamp, filename, and compression settings.

The course layer builder normalizes:

- lexicographic path order;
- fixed modification time;
- numeric UID/GID;
- empty owner/group names;
- controlled modes;
- deterministic gzip metadata.

It then proves both compressed digest and DiffID equality across controlled rebuilds.

Reproducibility claims are scoped. Rebuilding the semantic course model under one toolchain and environment is not proof that every external builder or architecture will emit identical bytes.

## Image indexes select platforms

An image index points to multiple manifests or other indexes. Each descriptor may carry:

- operating system;
- architecture;
- variant;
- OS version/features;
- annotations.

A client chooses a descriptor compatible with the target. The index does not inspect the executable. A publisher can label an amd64 binary as arm64. Selection succeeds; execution fails later.

Course 3 independently parses the ELF header of Atlas binaries and compares the machine type with the descriptor platform. Module 5 deepens this into ABI and multi-platform release truth.

## OCI image layout makes the graph inspectable

An OCI image layout is a directory such as:

```text
layout/
├── oci-layout
├── index.json
└── blobs/
    └── sha256/
        ├── <config>
        ├── <layer>
        ├── <manifest>
        └── ...
```

`oci-layout` declares the layout version. `index.json` is the entry point. Blobs are stored by digest algorithm and encoded hash.

A blob path does not imply a schema. The descriptor that points to it supplies media type and size. Treat blobs as opaque until the descriptor has been verified.

The layout is useful for air-gapped transport, local tests, and direct inspection. A registry exposes the same content-addressed objects through HTTP APIs rather than this exact directory structure.

## Artifact manifests and subject relationships

OCI distribution can store more than runnable images. An artifact manifest may point to evidence blobs and name a subject descriptor:

```text
SBOM manifest
  subject -> atlas-api image index digest
```

The subject relationship is crucial. An excellent SBOM for a different digest does not authorize the candidate in front of you.

The course attaches SBOM and provenance artifacts to the exact Atlas image index. The registry referrers endpoint can discover them by subject.

## Worked case: deletion that preserved a secret

The image history contains:

```text
Layer A: COPY .npmrc /root/.npmrc
Layer B: RUN npm install
Layer C: RUN rm /root/.npmrc
```

The final rootfs inspection reports no `.npmrc`. A security reviewer approves the image.

An attacker downloads Layer A and extracts the token. The review tested the assembled view, not the immutable history.

A correct investigation:

1. enumerate every manifest layer descriptor;
2. verify and unpack each blob independently;
3. inspect history and build context policy;
4. rotate the leaked credential;
5. rebuild from a context that never contains the secret;
6. use a build-time secret mount if access is required;
7. prove no layer contains the token pattern;
8. revoke the compromised digest and dependent caches.

Deleting the tag is insufficient because the digest remains fetchable while retained.

## Atlas capstone increment

You will build deterministic OCI layouts for Atlas API, worker, and probe. For API and worker, the index contains `linux/amd64` and `linux/arm64` manifests. You will:

- trace every descriptor;
- verify media type, digest, and size;
- compare layer digest and DiffID;
- reconstruct the rootfs;
- apply a whiteout fixture;
- attach one artifact manifest;
- corrupt one blob and prove early rejection;
- rebuild under the controlled profile and compare exact index digests.

The output is not yet an authorized release. It is a structurally and cryptographically coherent image graph.

## Review method

When reviewing an OCI image, ask in this order:

1. What exact index or manifest digest is the subject?
2. Which descriptor path selects the target platform?
3. Do media type, size, and digest match every child?
4. Do configuration DiffIDs match uncompressed layers?
5. Does ordered application produce the expected rootfs?
6. Are deleted or overwritten bytes still sensitive in lower layers?
7. Are runtime defaults compatible with the workload contract?
8. Are attached artifacts bound to this exact subject?

This sequence follows the graph instead of trusting a tag or a tool’s summary view.


## Verification algorithm — traverse before trusting

A verifier should treat every descriptor as an untrusted edge. Starting from a known root descriptor:

1. fetch exactly `size` bytes by `digest`;
2. recompute the digest over the received bytes;
3. check that the media type is allowed at this graph position;
4. parse only after integrity succeeds;
5. validate required fields and invariants;
6. recursively traverse referenced descriptors;
7. reject cycles where the profile forbids them;
8. retain the exact bytes used for the decision.

For a platform-specific image manifest, this means verifying the manifest bytes, configuration descriptor, every compressed layer blob, and then the relationship between uncompressed layer streams and configuration DiffIDs. An image can have internally valid JSON while pointing to a layer whose uncompressed content does not match the rootfs history.

### Safe extraction is part of image correctness

Layer archives are untrusted input. Before writing an entry, the unpacker must prevent:

- absolute paths;
- `..` traversal after normalization;
- symlink or hardlink targets that escape the rootfs;
- writes through a previously created symlink;
- device creation unless explicitly authorized;
- setuid/setgid or capability metadata that policy forbids;
- path collisions whose behavior differs across filesystems;
- decompression or inode exhaustion beyond configured bounds.

A common bug validates the textual path `var/lib/atlas/x` and then writes it through `var/lib/atlas`, which a prior layer made a symlink to a host path. Correct extraction resolves each parent under a confined root and handles links according to explicit rules.

### Apply whiteouts in layer order

Suppose layer A contains:

```text
/etc/atlas/config
/opt/secret.txt
/var/cache/atlas/a
/var/cache/atlas/b
```

Layer B contains:

```text
/opt/.wh.secret.txt
/var/cache/atlas/.wh..wh..opq
/var/cache/atlas/c
```

The merged rootfs hides `/opt/secret.txt`, removes lower entries under `/var/cache/atlas`, and exposes only `c` there. The bytes of `secret.txt` remain in layer A and can be recovered by anyone who can pull the graph. This is why secret hygiene belongs to build input and layer history, not merely final-rootfs inspection.

### Deterministic archive construction

Atlas normalizes:

- entry order;
- numeric UID/GID;
- user/group names;
- file mode;
- timestamps;
- PAX metadata;
- gzip timestamp and header fields;
- JSON key order and separators.

That creates stable bytes for the controlled fixture. It does not prove all real builds are reproducible. File contents, compiler behavior, base objects, environment, locale, generated data, and frontend semantics must also be controlled.

## Object-graph debugging

When a pull or unpack fails, identify the first broken edge:

```text
index digest
  └─ platform descriptor
       └─ manifest digest
            ├─ config digest
            └─ layer digest(s)
                 └─ uncompressed DiffID(s)
```

A wrong index platform label is not a layer problem. A corrupted compressed blob is not a runtime configuration problem. A DiffID mismatch means the compressed bytes may be intact while the uncompressed stream is inconsistent with the config. This graph-first method prevents destructive “rebuild until it works” debugging.

## Atlas implementation map

`OciLayout` stores canonical blobs under `blobs/sha256/`. `build_image` emits one configuration and manifest per architecture. `build_index` creates the multi-platform root. `unpack_manifest` verifies and applies layers into a rootfs. Tests intentionally corrupt descriptor size/digest, insert traversal entries, misapply whiteouts, and detach evidence from its subject.

The small model is executable explanation. Native OCI clients remain the independent implementation lane.

## A release is a reachable graph, not a tarball

The top-level index digest commits to child manifest descriptors. Each manifest commits to configuration and compressed layers. The configuration commits to uncompressed layer DiffIDs in order. This gives two related identities:

```text
compressed blob digest  → registry/storage identity
uncompressed DiffID     → rootfs change identity
```

A registry can deduplicate equal compressed blobs. A snapshotter reconstructs a root filesystem from ordered uncompressed changes. Recompressing identical tar content can change the blob digest without changing the DiffID. Reordering layers changes the filesystem history and image identity even when the final visible files appear similar.

### Validate the whole reachable graph

Checking only the top-level index is insufficient. A validator should walk every reachable descriptor and verify:

1. descriptor syntax, media type, digest, and size;
2. blob digest against exact stored bytes;
3. index and manifest schema shape;
4. config and layer references;
5. platform uniqueness within an index;
6. configuration DiffID count and order;
7. safe layer extraction and final required files;
8. subject links for attached artifacts.

The course layout validator now walks the reachable graph rather than stopping at the root descriptor. It remains a strict Atlas profile, not an OCI conformance suite.

### Extraction is security-sensitive

A layer applier is an archive extractor operating on attacker-controlled names. Normalizing `../../etc/passwd` into `etc/passwd` is not safe; it silently changes the attacker’s request. The correct action is rejection. Absolute paths, parent traversal, NUL bytes, links, devices, duplicate members, decompression bombs, and pre-existing symlink ancestors all require explicit policy.

Whiteouts add another trap. An opaque whiteout means “remove lower-layer children from this directory,” not “delete files introduced later by this same layer.” Therefore process whiteout semantics independently of tar-member order before extracting ordinary entries. Course tests deliberately place an ordinary file before an opaque marker to prove this invariant.

### Final filesystem equality is not release equality

Two images can produce the same visible rootfs and still differ in:

- history and layer boundaries;
- environment and entrypoint defaults;
- user and working directory;
- labels and annotations;
- platform metadata;
- compression and media types;
- embedded deleted secrets;
- provenance and build inputs.

Use a final-tree comparison to answer “what files will be visible?” Use descriptor and configuration comparison to answer “is this the same release?” Do not substitute one question for the other.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-02-oci-runtime-bundles-lifecycle-and-rootless-execution/index.md)
- [Next stage](../module-04-build-graphs-cache-reproducibility-and-secret-hygiene/index.md)
