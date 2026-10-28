# How to read OCI specifications without getting lost

OCI separates the container lifecycle into distinct specifications. This separation is not editorial trivia; it is the architecture of the ecosystem.

```text
Image Specification
    content-addressed image and artifact objects

Distribution Specification
    HTTP protocol for storing and retrieving content

Runtime Specification
    local bundle, configuration, lifecycle, and state
```

A tool may bridge all three, but a standards question must begin in the correct document.

## Start from the object you are holding

Ask what artifact is in front of you:

- `index.json` and `blobs/sha256/*` in a directory: OCI image layout;
- an image manifest or index returned by a registry: Image + Distribution concerns;
- `config.json` beside an unpacked rootfs: runtime bundle;
- a running process: effective runtime/kernel state, not only OCI documents;
- an SBOM/provenance manifest with a `subject`: OCI artifact relationship plus external schema.

This avoids searching the runtime spec for layer whiteouts or the image spec for signal delivery.

## Read normative language precisely

Specifications use terms such as **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY**. Record:

- the actor to whom the requirement applies;
- the preconditions;
- the exact object/field;
- exceptions;
- whether the requirement is syntactic, semantic, or behavioral.

For example, “descriptor digest must match content” is an integrity requirement for the bytes. It does not authorize the publisher or prove the content is safe.

## Follow references as a graph

When reading an image index, write:

```text
index descriptor
→ selected manifest descriptor
→ manifest bytes
→ config descriptor + layer descriptors
→ config bytes + compressed layer bytes
→ DiffIDs over uncompressed layer streams
```

For each edge, note media type, digest, size, and optional platform. The spec is easier when you follow one concrete graph rather than read all sections linearly.

## Keep schema and profile separate

The specification permits many valid objects. A platform release profile narrows them. Atlas, for example, requires:

- linux/amd64 and linux/arm64;
- deterministic gzip/tar profile in the semantic lane;
- numeric non-root identity;
- read-only root expectation;
- subject-bound supply-chain artifacts;
- particular release-policy evidence.

Those are Atlas requirements, not universal OCI requirements. Course documents label local policy so it is not mistaken for the standard.

## Read change history and release notes

Pin the version used by the course. When a current standard changes, determine:

- whether object syntax changed;
- whether existing objects remain compatible;
- whether the course profile depends on new fields;
- whether tools implement the release consistently;
- whether the change is normative or explanatory.

Do not update a version string and claim compatibility without rerunning independent validation.

## Compare specification, implementation, and observation

Use three columns:

| Layer | Example |
|---|---|
| specification | runtime config permits a read-only root |
| implementation | runc/crun/mini-runtime applies mounts and root switch |
| observation | process mountinfo and write attempt show effective behavior |

A configuration that requests a control is not observation that the control was enforced. Conversely, one observed run does not prove the implementation handles every valid config.

## Work through a descriptor example

Given:

```json
{
  "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
  "digest": "sha256:abc...",
  "size": 2048
}
```

A verifier should:

1. retrieve 2048 exact bytes;
2. hash those compressed bytes;
3. compare the digest;
4. interpret them as gzip-compressed tar only after integrity succeeds;
5. decompress under resource limits;
6. hash the uncompressed tar stream for comparison with the corresponding DiffID;
7. apply entries under safe extraction rules.

The descriptor alone does not reveal the DiffID, extraction safety, or merged filesystem.

## Resolve apparent contradictions

When tool behavior seems to contradict the spec:

1. confirm the exact tool and spec versions;
2. capture raw request/object/config;
3. identify whether the tool uses a stricter local profile;
4. distinguish client, registry, runtime, and kernel behavior;
5. look for optional/SHOULD language;
6. test with an independent implementation;
7. document the compatibility conclusion rather than generalizing from one result.

## Build a standards notebook

For each module, keep one page containing:

- normative objects and fields;
- Atlas profile constraints;
- implementation-specific behavior;
- observed evidence;
- unresolved interoperability questions.

By Course 4, this notebook becomes the basis for understanding how Kubernetes consumes image references and creates runtime requests without conflating those layers.
