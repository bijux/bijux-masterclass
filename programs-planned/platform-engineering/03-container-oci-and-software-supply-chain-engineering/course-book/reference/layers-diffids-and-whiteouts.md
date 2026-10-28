# Layers, DiffIDs, and whiteouts

A layer is an immutable filesystem changeset encoded as a tar archive, often compressed for distribution. The merged root filesystem is the result of applying ordered changesets. It is not a proof that earlier content ceased to exist.

## Two identities

```text
compressed layer bytes  ──sha256──> manifest layer digest
        │ decompress
        v
uncompressed tar bytes  ──sha256──> config DiffID
```

The distinction matters when a registry recompresses content, when a builder compares snapshot chains, and when a verifier reconstructs an image. Verify each identity against the bytes it actually names.

## Changeset behavior

A later layer can:

- add a new path;
- replace file content or metadata;
- add directories;
- hide a lower path with a whiteout;
- mark a directory opaque so lower children no longer appear.

Common whiteout forms are:

```text
path/.wh.filename       remove/hide path/filename from lower layers
path/.wh..wh..opq       make path opaque; hide lower children
```

Whiteout entries are merge instructions, not ordinary runtime files. A correct unpacker validates paths, rejects traversal, applies whiteouts in the right directory, and prevents archive entries from escaping the destination through symlinks or absolute names.

## Why deletion is not erasure

Suppose layer 1 contains `root/.npmrc` and layer 2 contains `root/.wh..npmrc`. The final rootfs hides the file, but layer 1’s blob still contains the credential. Anyone with graph access can retrieve it. Remediation requires credential revocation, cache/registry exposure review, and a rebuilt subject whose history never contained the secret.

## Deterministic layer production

For equal filesystem input to produce equal layer bytes, control at least:

- path order;
- uid/gid and user/group names;
- mode bits;
- modification times;
- tar format and extended headers;
- symlink targets;
- compression implementation, parameters, and timestamp/header fields.

A deterministic layer under one controlled implementation does not prove another builder will emit identical bytes. State the experiment boundary.

## Review procedure

1. Verify compressed digest and size.
2. Decompress and verify DiffID.
3. List every path, type, mode, owner, size, and link target.
4. Reject absolute/traversal paths and unsafe devices.
5. Apply changes in manifest order to an empty rootfs.
6. Inspect both each historical layer and the merged result.
7. Compare merged entrypoint and required files with configuration.
8. Scan historical objects for secrets and prohibited content.
