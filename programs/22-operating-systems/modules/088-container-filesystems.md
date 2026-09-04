---
module_id: OS-088
program: Operating Systems
level: 2
module_number: 88
title: Container Filesystems
status: complete
last_verified: 2026-09-04
---

# Container Filesystems

## One-Page Review

### Governing question

How does a container runtime turn portable, content-addressed filesystem changesets into an isolated runtime mount tree with efficient sharing, controlled mutation and explicit persistent state?

### Essential definitions

- An **image layer** is an ordered filesystem changeset, not a complete filesystem snapshot by itself.
- A **whiteout** represents removal of a path from lower image layers; an **opaque whiteout** hides all lower children of a directory.
- A **snapshotter** prepares committed parent snapshots and an active writable snapshot for a container.
- An **overlay mount** merges one or more read-only lower directories with an upper directory and work directory into one view.
- **copy-up** creates an upper copy when an operation must modify an object visible from a lower layer.
- A **bind mount** exposes an existing host or namespace path at another location without copying its contents.
- An **idmapped mount** presents ownership through a mount-specific ID mapping without recursively changing stored inode owners.
- A **volume** is storage whose lifecycle and durability contract is intentionally separate from the container's writable layer.

### Central model, mechanism, or theorem

Container filesystem construction is a pipeline: verify content descriptors, apply ordered image changesets to immutable snapshots, create a per-container writable snapshot, assemble additional mounts inside a private mount namespace, make the intended tree the process root, then apply read-only, identity and security attributes. Each stage has distinct identity, lifetime and rollback rules.

### Critical invariants

- Every image blob is verified against its descriptor before use, and layer application cannot escape its target root.
- Layer order, whiteouts, metadata and hard-link semantics reproduce the specified root filesystem.
- Lower snapshots remain immutable while every runtime mutation is attributable to an upper layer or explicit mount.
- Mount propagation cannot export container-created mounts to unintended host peers.
- Bind-mount and volume sources resolve to authorized host objects before the container enters its root.
- Persistent data is never entrusted solely to an ephemeral writable layer.
- Open descriptors, mounts, snapshot leases and content references are released only after workload teardown is fenced.

### Common failures

A runtime extracts tar paths outside the root, treats whiteouts as ordinary files, mutates a shared lower layer, overlooks copy-up latency, bind-mounts a symlink-selected host path, marks only the top mount read-only while writable submounts remain, leaks the old root, misinterprets container UIDs on host storage, or deletes snapshots while references still exist.

### Compact example

A base layer contains `/bin/app`, `/etc/base.conf` and two cache files. An update layer replaces `/bin/app`, whiteouts `/etc/base.conf` and makes `/var/cache` opaque before adding one new index. The merged view contains only the new app and cache state; the base snapshot still contains its original files. A runtime write goes to a separate upper snapshot and does not change image identity.

### Connections

Container filesystems connect VFS path resolution, mount namespaces, overlay filesystems, OCI images, content stores, snapshotters, user namespaces, supply-chain integrity, backup, storage performance and workload lifecycle.

## Governing Question

An image must be portable and shareable, but a running process expects one mutable directory hierarchy. The governing question is how runtimes transform ordered content into that view without losing provenance, allowing one container to mutate another's base, or confusing disposable runtime state with durable storage.

## Why This Matters

Filesystem assembly is both a performance path and a security boundary. Image layers save network and disk space through content reuse, while copy-on-write snapshots make startup cheap. The same indirection creates subtle semantics around deletions, renames, inode identity, page cache, ownership, mount propagation and garbage collection.

The root filesystem also mediates nearly every dependency a process loads. A correct image digest is insufficient if extraction traverses a symlink, a bind source changes during resolution, a writable procfs control remains exposed, or old-root handles survive the pivot. Reliable containers require evidence from content verification through final mount topology and teardown.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain inodes, directory entries, links, permissions, extended attributes and page cache;
- describe mounts, bind mounts, mount namespaces, propagation and process roots;
- distinguish archive representation, filesystem state, content digests and signatures;
- reason about user namespaces, UID/GID translation, capabilities and LSM labels;
- distinguish ephemeral state, persistent volumes, backups and replicated data.

Retrieve the exact image manifest and configuration digests, ordered layer descriptors, runtime and snapshotter versions, backing filesystem and mount options, kernel OverlayFS features, user-namespace mappings, mount namespace and propagation state, final mount information, volume sources, security labels, content-store leases and garbage-collection policy.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish image descriptors and changesets from unpacked snapshots and runtime mounts;
2. apply ordered layers, whiteouts and metadata without corrupting lower state;
3. explain OverlayFS lookup, copy-up, merged directories and rename behavior;
4. assemble a container root using mount namespaces, propagation control and pivoting;
5. configure read-only roots, bind mounts, tmpfs and persistent volumes safely;
6. reason about UID/GID ownership, idmapped mounts, capabilities and LSM labels;
7. compare overlay, native, block and lazy snapshotter trade-offs;
8. validate integrity, isolation, performance, durability and teardown independently.

## Core Exposition

### Separate image, snapshot and runtime representations

An OCI image consists of metadata and content-addressed blobs. Filesystem layers encode changesets. A snapshotter converts those changesets into storage objects useful for execution, and a runtime mounts an active snapshot with other filesystems to form the process root. These representations may share content but have different identities and lifetimes.

### Verify descriptors before interpreting content

An OCI descriptor names a digest, size and media type. Fetch bytes into a content store, verify their digest and size, and only then pass them to decompression or layer application. A signature or policy can authenticate who approved descriptors, while the digest detects byte substitution. Neither alone proves that extracted paths are safe.

### Apply layers in canonical order

The image configuration records an ordered root filesystem history, and the manifest supplies corresponding layer descriptors. Begin from an empty root and apply changesets from base to top. Reversing, sorting or deduplicating layers by filename changes the resulting filesystem even if every blob digest remains valid.

### Treat a layer as a changeset

A layer adds and modifies entries in full and represents removals with whiteouts. It is not a directory tree to union naively and not necessarily a snapshot a process can mount directly. Application must reproduce file type, ownership, mode, timestamps, extended attributes, links and deletion semantics supported by the platform.

### Interpret whiteouts during application

An entry named `.wh.NAME` removes `NAME` from lower state; `.wh..wh..opq` hides lower children of its directory. These markers operate on lower layers and must not appear as ordinary runtime files. Apply opaque semantics before sibling additions so archive entry order cannot expose hidden lower content.

### Harden archive extraction

Reject absolute paths, `..` escapes, malformed whiteouts, device nodes outside policy, and links that redirect later writes beyond the target root. Resolve each operation relative to a trusted directory descriptor with no-follow and beneath-style constraints where available. Limits on entry count, expansion size and nesting protect against resource exhaustion.

### Preserve lower snapshot immutability

Committed image snapshots may be shared by many containers. Never permit runtime writes into them. An active child or upper directory records per-container changes. Immutability enables caching and provenance; it is an implementation invariant enforced through storage and mount permissions, not a property conferred by the word “image.”

### Understand overlay lookup precedence

OverlayFS presents the upper object when a name exists there; otherwise it searches lower layers in order. Directories may merge entries from several layers, while non-directories resolve to one selected object. Whiteouts and opaque directories suppress lower names. The visible namespace is therefore a precedence computation, not a physical directory.

### Account for copy-up on first mutation

When a lower file requires write access or certain metadata changes, OverlayFS copies it to the upper filesystem before completing the operation. The first small write to a large lower file can copy much more data than the application changed. Measure copy-up bytes and latency separately from steady-state upper-file writes.

### Treat metadata changes as potential writes

Changing mode, ownership, timestamps, extended attributes or creating a hard link can require copy-up. Features such as metacopy may defer data copying, but their compatibility and security constraints matter. A workload described as “read-mostly” can still create extensive upper state through metadata scans.

### Understand merged directory behavior

Directory reads combine names from upper and lower directories and cache a merged name list for an open directory. Concurrent mutations can affect seek and enumeration behavior. Applications requiring stable traversal must use their own synchronization or snapshot, rather than assuming a union view gives transactional enumeration.

### Plan for rename and link constraints

Renaming a lower or merged directory can return `EXDEV` unless redirect support is enabled. Tools may respond by recursively copying and deleting, changing performance and atomicity. Hard links, inode numbers, export features and index options also interact with copy-up. Test the exact kernel and mount feature set used in production.

### Keep upper and work directories compatible

OverlayFS requires suitable upper and work directories, conventionally on the same supported filesystem, with required d_type and extended-attribute behavior. Network and unusual filesystems may not satisfy these rules. Validate at startup and fail closed rather than silently selecting a storage mode with different isolation or durability.

### Recognize page-cache sharing and divergence

Containers reading the same lower files can benefit from shared cached pages. After copy-up, an upper file has distinct backing and cache behavior. Apparent image sharing therefore changes with mutation. Measure memory and I/O at the backing-object and cgroup layers before attributing savings to layer reuse.

### Use snapshotters as lifecycle managers

A snapshotter prepares active, view and committed snapshots and returns mounts needed to expose them. Its metadata graph tracks parentage independent of image blob storage. Commit an applied layer before using it as the immutable parent of the next; create a fresh active child for runtime mutation.

### Distinguish content-store and snapshot references

Compressed image blobs, uncompressed layer state and runtime snapshots occupy different stores. Garbage collection must know which manifests, leases, snapshots and running containers retain each object. Deleting a tag need not free bytes immediately, and removing content while an unpack or launch is in flight can corrupt lifecycle.

### Choose snapshot technology by workload

OverlayFS offers efficient file-level sharing and copy-up. A native snapshotter copies trees and is simple but space-intensive. Btrfs, ZFS and device-mapper snapshotters use filesystem or block primitives with different prerequisites and failure domains. Remote or lazy snapshotters reduce startup download at the cost of runtime fetch dependence.

### Make lazy loading an availability decision

Fetching file content on first access can shorten cold start and avoid unused bytes. It also places registry, network, cache and verification logic on the page-fault or read path. Define behavior for disconnection, digest failure, eviction and prefetch. “Started” need not mean every executable and library is locally available.

### Create a private mount namespace early

Filesystem assembly should occur in the target mount namespace or a tightly controlled staging namespace. Make the root subtree private or appropriately slave before container mounts. Otherwise new mounts can propagate to host peers, or host mount events can unexpectedly appear in the container.

### Build the root as a mount tree

Mount the active root filesystem, then add procfs, sysfs, tmpfs, device views, secrets, configuration and volumes at defined destinations. Order matters because a later mount hides existing entries below the mount point. Verify that every destination exists in the intended preceding view and that hidden data is not mistaken for deleted data.

### Pivot into the new root safely

`pivot_root()` exchanges the process's root mount with a new root in its mount namespace. Arrange mount relationships, change current directory, pivot, detach the old root and remove its mount point. A root change does not revoke open descriptors; close unintended handles before executing the workload.

### Distinguish pivot_root from chroot

`chroot()` changes pathname resolution for a process but does not replace the mount namespace or prove the old tree is unreachable. A container runtime normally combines a mount namespace, a constructed mount tree, a root transition, descriptor hygiene and capability reduction. No one call supplies the boundary.

### Treat bind sources as host capabilities

A bind mount exposes the source object and its descendants according to recursive and propagation options. Resolve the source against trusted policy before the container can race path components. A host path grants access to the underlying object, not a copy; writes and metadata changes can affect host or other workloads.

### Apply recursive read-only intent explicitly

Making one mount read-only does not necessarily make nested submounts read-only. Modern mount APIs can apply attributes recursively where supported. Inspect the final tree and attempt writes at every sensitive submount. A read-only image root can still contain writable tmpfs, volume and procfs control surfaces.

### Use tmpfs for bounded ephemeral state

Tmpfs suits runtime files, scratch data and secrets that should not persist on disk, but it consumes memory and possibly swap under kernel accounting. Set size, inode, mode and ownership constraints, and account it to the intended cgroup. “Memory-backed” does not mean free, unbounded or immune to swap.

### Separate volumes from the writable layer

The active snapshot is usually disposable with the container. Databases, user uploads and recovery-critical state need an explicitly managed volume, external service or durable log. Define attach, fencing, consistency, backup, restore and deletion semantics independently from image and container removal.

### Do not hide image initialization accidentally

Mounting a fresh volume over a nonempty image directory hides the image's seed files. Some platforms copy initial content; others present an empty volume. Make initialization an explicit, idempotent operation with versioning and ownership checks. Hidden image content still occupies lower storage until image reclamation.

### Map ownership without recursive chown when possible

User namespaces can make container UID 0 correspond to an unprivileged host ID. Stored files must still appear with useful ownership. Idmapped mounts apply a mount-specific mapping without rewriting every inode, reducing startup and write amplification, but filesystem and kernel support must be detected.

### Distinguish idmapping from permission bypass

An idmapped mount changes how ownership is interpreted for that mount. Ordinary permission checks, capabilities relative to user namespaces, LSM policy, mount flags and filesystem rules still apply. The mapping neither grants initial-user-namespace privilege nor sanitizes a malicious bind source.

### Preserve extended attributes and security labels

Layer application and copy-up may need to preserve capabilities, ACLs and LSM labels. Some overlay metadata uses trusted or user extended attributes. Define which namespaces are allowed, reject unsupported security-critical metadata, and apply an appropriate mount label. Silent xattr loss can change execution privilege or deny service.

### Restrict special files and kernel interfaces

An image archive can describe device nodes, but creating or using them requires separate policy. Mount controlled `/dev`, mask dangerous procfs paths, make appropriate sysfs and procfs regions read-only, and drop mount-related capabilities. A harmless-looking path can expose a kernel control rather than ordinary storage.

### Pair read-only roots with explicit writable paths

A read-only root reduces persistent mutation and supports drift detection. Applications still need defined writable locations for temporary files, sockets, caches and state. Provide narrowly mounted tmpfs or volumes with size and execution flags, then test failure behavior when accidental writes elsewhere receive `EROFS`.

### Control execution and privilege mount flags

Use `nosuid`, `nodev` and `noexec` where compatible, understanding their exact mount-level scope and exceptions. A bind remount or nested mount can have different attributes. These flags complement file permissions, capabilities, seccomp and LSM policy; they do not validate file content or stop interpretation by another executable.

### Budget inode and metadata pressure

Layer-heavy images, package managers and workloads creating tiny files can exhaust inodes or amplify directory and xattr operations before byte capacity is full. Track upper-directory inode use, workdir health, snapshot counts and backing-filesystem metadata. Disk quotas should include both data and inode-style limits where available.

### Observe the final namespace from both sides

Capture image and snapshot identifiers, `/proc/PID/mountinfo`, propagation tags, filesystem types, mount attributes, source paths, effective IDs, upper/work locations and volume identities. Compare host and container views. A directory listing cannot distinguish overlay origin, bind source or a mount hiding lower entries.

### Teardown in reference-safe order

Stop new operations, terminate or quiesce tasks, close namespace and file descriptors, unmount child mounts deepest first, release active snapshots and leases, then let garbage collection reclaim unreachable content. Lazy unmount can hide a mount from a namespace while references continue using it; it is not proof of completed teardown.

### Test integrity, isolation, durability and performance separately

Recompute content digests, exercise whiteouts and metadata, attempt archive escapes, mutate parallel containers, test propagation, retain old-root descriptors, restart with volumes, fill bytes and inodes, trigger copy-up, and simulate remote-fetch loss. Each test supports one property; passing an image scan does not prove mount isolation or durable recovery.

## Definitions and Notation

Let ordered filesystem states be $F_0,F_1,\ldots,F_n$, with $F_0=\varnothing$. Applying changeset $\Delta_i$ gives

$$
F_i=apply(F_{i-1},\Delta_i).
$$

The operation applies deletions and opaque-directory rules to lower state, then additions and modifications with specified metadata. It is order-sensitive and is not ordinary archive extraction.

For path $p$, let $U(p)$ be an upper entry and $L_1(p),\ldots,L_k(p)$ lower entries in lookup order. Abstract overlay resolution is

$$
view(p)=
\begin{cases}
\varnothing, & \text{if an applicable upper whiteout hides }p,\\
U(p), & \text{if an upper entry exists},\\
L_j(p), & \text{for the first visible lower entry},\\
\varnothing, & \text{otherwise}.
\end{cases}
$$

Directories add merge and opacity semantics; the expression is a lookup model, not a full VFS specification.

Let $B$ be bytes changed logically by an application and $C$ be bytes copied into the upper layer because of first mutation. Define copy-up amplification

$$
A=\frac{C}{\max(B,1)}.
$$

A one-byte edit that copies a 1 GiB lower file has very high $A$ even though later writes target the upper copy directly.

Let $R$ be the set of content blobs, snapshots, mounts, leases and open handles reachable from live roots. Garbage collection may reclaim object $x$ only if $x\notin R$ after a consistent reachability decision. Filesystem deletion alone does not establish this condition.

## Mechanisms, Invariants, or Proof Structure

Review a container filesystem with these obligations.

1. **Descriptor obligation:** manifest, configuration and layer bytes match verified content descriptors and trust policy.
2. **Application obligation:** ordered changesets, whiteouts, metadata and links reproduce the intended root without path escape.
3. **Immutability obligation:** committed parents cannot be mutated by active containers or concurrent unpack operations.
4. **Resolution obligation:** overlay lookup, opacity, copy-up, rename and feature behavior match the deployed kernel and backing store.
5. **Namespace obligation:** root assembly occurs inside the intended mount namespace with controlled propagation.
6. **Root obligation:** pivot, old-root detachment and descriptor closure prevent unintended reachability.
7. **Mount obligation:** bind, tmpfs, procfs, sysfs, device and volume sources and attributes match policy recursively.
8. **Identity obligation:** stored ownership, user-namespace mappings, idmapped mounts, xattrs and LSM labels compose correctly.
9. **Durability obligation:** ephemeral upper data and persistent volume data have explicit, tested lifecycles.
10. **Capacity obligation:** bytes, inodes, metadata, copy-up, page cache and remote fetches fit resource budgets.
11. **Reference obligation:** content, snapshots, mounts, leases and handles remain until fenced teardown, then become reclaimable.
12. **Assurance obligation:** integrity, isolation, privilege, persistence and performance claims remain separate.

The proof traces bytes from a verified descriptor through ordered application and snapshot parentage into the final mount tree. It then traces every mutable path to an upper store or explicit volume, every namespace-visible mount to an authorized source, and every teardown action through the reference graph. Image identity alone proves none of the later stages.

## Alternatives and Trade-Offs

- **Layered image versus monolithic root:** layers enable reuse and incremental distribution; a monolith simplifies lookup and extraction state.
- **Many small versus few large layers:** small layers improve selective reuse; many layers increase metadata and lookup overhead.
- **Overlay versus native copying:** overlay reduces startup and space; full copies avoid union semantics at greater I/O cost.
- **File versus block snapshots:** file snapshots expose per-file copy-up behavior; block snapshots offer different consistency, allocation and device requirements.
- **Eager versus lazy unpack:** eager preparation front-loads bytes and verification; lazy access shortens startup while adding runtime network dependence.
- **Writable versus read-only root:** writable roots maximize compatibility; read-only roots narrow drift and demand explicit state paths.
- **Upper layer versus tmpfs scratch:** disk upper state survives process restart until container deletion; tmpfs avoids disk persistence and consumes memory.
- **Bind mount versus managed volume:** binds offer direct host integration; managed volumes provide stronger lifecycle abstraction.
- **Private versus slave propagation:** private blocks both directions; slave permits selected host-to-container mount events without return propagation.
- **pivot_root versus chroot:** pivoting replaces the mount-root relationship; chroot is simpler but does not provide equivalent mount isolation.
- **Recursive chown versus idmapped mount:** chown is widely understood and permanent; idmapping avoids inode rewrites but requires support.
- **Shared lower cache versus pre-copied tree:** sharing saves memory and disk; copies isolate backing objects and increase duplication.
- **Seeded directory versus explicit initialization:** embedded seed files are convenient; explicit initialization avoids mount-hiding ambiguity.
- **Synchronous delete versus garbage collection:** synchronous deletion offers immediate accounting; reachability-based GC handles sharing and active references safely.
- **Strict mount flags versus application compatibility:** restrictive flags reduce privilege paths; interpreters and legitimate devices may require exceptions.
- **Uniform versus workload-specific snapshotter:** uniformity simplifies operations; workload-specific backends optimize startup, I/O or isolation.

## Failure Modes and Misconceptions

- “An image layer is a complete filesystem.” It is an ordered changeset.
- “A correct digest makes extraction safe.” It authenticates bytes, not path application.
- “Tar extraction naturally handles whiteouts.” Layer application gives them special deletion semantics.
- “Deleting a file removes it from old layers.” A higher layer hides immutable lower content.
- “Opaque means an empty directory everywhere.” It hides lower children while same-layer children remain visible.
- “Read-only lower directories make the whole container read-only.” The upper layer and additional mounts may be writable.
- “A one-byte edit writes one byte.” First mutation can copy up the whole lower file.
- “Only data writes cause copy-up.” Metadata and hard-link operations can also require it.
- “Overlay rename is identical to one-filesystem rename.” Lower directory rename can return `EXDEV` or use redirect behavior.
- “All backing filesystems support OverlayFS equally.” Required directory and xattr capabilities differ.
- “Shared image layers mean all page cache stays shared.” Upper copies diverge after mutation.
- “Content blobs and snapshots are the same storage.” Compressed blobs, unpacked state and active snapshots have different graphs.
- “Deleting an image tag immediately frees every byte.” Live manifests, snapshots, leases and containers retain objects.
- “A mount namespace copies files.” It supplies a distinct mount view over filesystem objects.
- “pivot_root closes every path to the host.” Open descriptors and other mounts can retain access.
- “chroot is a container filesystem boundary.” It does not build or isolate a mount tree.
- “A bind mount copies the source.” It exposes the same underlying object.
- “Read-only on the root covers nested mounts.” Submount attributes require separate or recursive treatment.
- “tmpfs does not need a quota.” It consumes memory, inodes and potentially swap.
- “The writable layer is a safe database volume.” Its lifecycle is normally tied to the container.
- “Mounting a volume merges it with image files.” The mount hides underlying entries.
- “Container UID 0 must own host files as UID 0.” User and mount ID mappings can translate ownership.
- “Idmapping bypasses permissions.” It changes ownership interpretation within existing permission mechanisms.
- “noexec prevents all use of file contents.” An interpreter can read and execute compatible content.
- “An unmounted filesystem has no users.” Open handles and lazy-detached mounts can retain it.
- “A vulnerability scan proves runtime filesystem isolation.” It evaluates content, not final mount topology and handles.

## Worked Examples

### Example 1

Two containers share three committed image snapshots but each has a distinct active upper snapshot. Container A replaces `/etc/service.conf`; container B and the committed parents remain unchanged. Disk and page-cache sharing persists for untouched lower files.

### Example 2

The following executable toy applies ordered additions, a whiteout-like deletion and an opaque-directory replacement. It demonstrates changeset arithmetic only, not tar safety, OCI encoding, OverlayFS, metadata, links or kernel behavior.

<!-- bijux-verify: {"id":"container-layer-changeset-application","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after_base=4\nafter_update=3\nafter_runtime=4\nbin_app=v2\nbase_conf=absent\ncache_entries=/var/cache/index\nlower_bin_app=v1\n","stderr":""}} -->
```python
def apply(state, additions, deletions=(), opaque_dirs=()):
    result = dict(state)
    for directory in opaque_dirs:
        prefix = directory.rstrip("/") + "/"
        result = {path: value for path, value in result.items()
                  if not path.startswith(prefix)}
    for path in deletions:
        result.pop(path, None)
    result.update(additions)
    return result

base = apply({}, {
    "/bin/app": "v1",
    "/etc/base.conf": "enabled",
    "/var/cache/a": "old-a",
    "/var/cache/b": "old-b",
})
updated = apply(base, {
    "/bin/app": "v2",
    "/etc/new.conf": "enabled",
    "/var/cache/index": "fresh",
}, deletions={"/etc/base.conf"}, opaque_dirs={"/var/cache"})
runtime = apply(updated, {"/tmp/run": "live"})

print(f"after_base={len(base)}")
print(f"after_update={len(updated)}")
print(f"after_runtime={len(runtime)}")
print(f"bin_app={runtime['/bin/app']}")
print(f"base_conf={'present' if '/etc/base.conf' in runtime else 'absent'}")
print("cache_entries=" + ",".join(sorted(
    path for path in runtime if path.startswith("/var/cache/")
)))
print(f"lower_bin_app={base['/bin/app']}")
```

### Example 3

An application opens a 2 GiB lower database template for a one-byte metadata update. Without a relevant optimization, copy-up reads and writes the full file before modification. Startup latency and upper capacity spike even though the logical change is tiny.

### Example 4

A runtime creates a new mount namespace while its inherited root is shared, then mounts a secret into the container tree. The event propagates to a host peer. Recursively making the staging root private before assembly prevents the export.

### Example 5

A bind source `/srv/tenant/current` is checked, then another process swaps a symlink before mounting. The container receives another tenant's directory. Resolving through trusted directory descriptors and preventing symlink traversal closes the check/use race.

### Example 6

The image contains `/var/lib/app/default.db`, but a fresh empty volume is mounted at `/var/lib/app`. The seed is hidden, not deleted. An explicit initializer copies or creates schema state into the volume and records its version before the service starts.

### Example 7

A rootless container maps inside UID 0 to host UID 200000. An idmapped volume makes files stored under another authorized ownership range appear correctly inside without recursively chowning millions of inodes. LSM and ordinary permission checks still apply.

### Example 8

A root is read-only, but `/proc/sys` is a writable nested mount. The workload changes a namespaced kernel setting despite the root attribute. Inspecting the final mount tree and making sensitive nested interfaces read-only establishes the intended boundary.

### Example 9

A lazy snapshotter starts a workload after fetching its executable but before all locale and model files are local. The registry becomes unavailable; later reads fail. Readiness must include required prefetch or define this dependency as part of service availability.

### Example 10

Container deletion lazily detaches its root while a helper retains a directory descriptor and a snapshot lease. The path disappears from one namespace, but storage remains reachable and cannot be reclaimed. Fencing the helper, closing handles and releasing the lease completes teardown.

## Cross-Program Connections

- **Security engineering:** extraction, path resolution, mount flags, device views, labels and descriptor hygiene define a major containment surface.
- **Platform engineering:** image stores, snapshotters, volumes, runtimes and garbage collection form the node storage plane.
- **Filesystem engineering:** overlay lookup, copy-up, links, xattrs, page cache and mount trees reuse VFS mechanisms.
- **Supply-chain engineering:** descriptors, digests, signatures and provenance connect published images to executed bytes.
- **Reliability engineering:** persistent volumes, fencing, backup, restore and teardown determine data survival.
- **Performance engineering:** layer depth, copy-up, metadata, lazy fetch, page-cache sharing and device behavior affect latency.
- **Distributed systems:** content distribution and remote snapshotters place registries and caches on startup or read paths.
- **Data engineering:** stateful engines require volume consistency and I/O semantics beyond ephemeral container layers.
- **Observability engineering:** mountinfo, snapshot graphs, origin tracking, byte/inode metrics and events explain visible state.
- **Operating systems:** mount namespaces, user namespaces, cgroups and VFS authorization compose the runtime boundary.

## References

1. Open Container Initiative, [Image Format Specification](https://github.com/opencontainers/image-spec/blob/main/spec.md), image components, descriptors and translation toward runtime bundles; retrieved 2026-09-04.
2. Open Container Initiative, [Image Filesystem Changesets](https://github.com/opencontainers/image-spec/blob/main/layer.md), layer application, attributes, whiteouts and opaque directories; retrieved 2026-09-04.
3. Open Container Initiative, [Runtime Configuration](https://github.com/opencontainers/runtime-spec/blob/main/config.md), root filesystems, ordered mounts, read-only roots and ID-mapped mount configuration; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Overlay Filesystem](https://docs.kernel.org/filesystems/overlayfs.html), lookup, merged directories, copy-up, whiteouts, rename and feature constraints; retrieved 2026-09-04.
5. Linux man-pages Project, [mount_namespaces(7)](https://man7.org/linux/man-pages/man7/mount_namespaces.7.html), mount views, propagation types and namespace behavior; retrieved 2026-09-04.
6. Linux man-pages Project, [pivot_root(2)](https://man7.org/linux/man-pages/man2/pivot_root.2.html), root-mount transition semantics and container use; retrieved 2026-09-04.
7. Linux man-pages Project, [mount_setattr(2)](https://man7.org/linux/man-pages/man2/mount_setattr.2.html), recursive mount attributes, read-only trees, propagation and ID-mapped mounts; retrieved 2026-09-04.
8. Linux Kernel Documentation, [Idmappings](https://docs.kernel.org/filesystems/idmappings.html), filesystem ownership mappings, permission checks and idmapped mount behavior; retrieved 2026-09-04.
9. containerd, [Content Flow](https://github.com/containerd/containerd/blob/main/docs/content-flow.md), content-store, unpack, committed-layer and snapshot lifecycle; retrieved 2026-09-04.
10. containerd, [Snapshotters](https://github.com/containerd/containerd/blob/main/docs/snapshotters/README.md), overlay, native, block, filesystem and remote snapshotter choices; retrieved 2026-09-04.

## Exercises

### Exercise 1

A base layer has `/a`, `/d/x` and `/d/y`. The next layer whiteouts `/a`, marks `/d` opaque and adds `/d/z`. List the merged paths and state what remains in the base snapshot.

### Exercise 2

An application changes 4 KiB in a 2 GiB lower file and the implementation copies the whole file up. Compute copy-up amplification $A=C/B$ using binary units. Name two ways to avoid repeating the cost.

### Exercise 3

Design the mount sequence for a container with a read-only image root, writable bounded `/tmp`, a persistent `/var/lib/app` volume and no hostward mount propagation.

### Exercise 4

A rootless workload must use a volume containing one million files owned under a different authorized host-ID range. Compare recursive `chown` with an idmapped mount, including one limitation of idmapping.

### Exercise 5

Design a teardown and garbage-collection evidence plan that proves a deleted container no longer retains its active snapshot while shared image layers required by another container remain intact.

## Answers to the Exercises

### Answer 1

The merged view contains `/d/z`. The whiteout hides `/a`, and the opaque marker hides all lower children of `/d` before the same layer adds `z`. Neither `/d/x` nor `/d/y` is visible through the merged directory.

The base snapshot remains unchanged and still contains `/a`, `/d/x` and `/d/y`. Higher-layer removal is a view operation encoded by a changeset, not physical mutation of prior content. Another image whose layer chain stops at the base still sees all three paths.

### Answer 2

Two GiB is $2\times 2^{30}$ bytes and 4 KiB is $4\times 2^{10}$ bytes. Thus

$$
A=\frac{2\times2^{30}}{4\times2^{10}}=2^{19}=524{,}288.
$$

After the first copy-up, later changes to the upper copy avoid repeating a lower-to-upper copy. A design can place known large mutable files on an explicit volume or create them directly in the upper layer rather than baking them into a lower image. Supported metacopy features may help metadata-only changes, but not an actual data edit and must be validated for the deployment.

### Answer 3

Create or enter a dedicated mount namespace and recursively make its staging root private. Mount the image snapshot as the new root, mount a size- and inode-bounded tmpfs at its `/tmp`, and bind or attach the authorized persistent volume at `/var/lib/app`. Apply ownership or idmapping, LSM labels, and restrictive `nosuid`, `nodev` or `noexec` flags where compatible.

Apply read-only attributes to the intended root tree while preserving the explicitly writable tmpfs and volume mounts. Add controlled procfs, sysfs and device views, making sensitive subtrees read-only or masked. Pivot to the new root, detach the old root, close host descriptors, drop setup capabilities and verify final `mountinfo`, propagation and write tests at root and nested mount points.

### Answer 4

Recursive `chown` rewrites ownership on every inode, which is broadly understood but expensive, creates metadata I/O, changes the shared stored view and needs reversal or another rewrite for a different mapping. Interruption can leave mixed ownership. With one million files, this can dominate startup and backup churn.

An idmapped mount attaches an authorized user-namespace mapping to the mount, changing ownership interpretation locally and for the mount lifetime without rewriting those inodes. It reduces startup and preserves other views. The backing filesystem and kernel must support idmapped mounts, mappings must be authorized, and idmapping does not bypass permissions, LSM rules, capabilities or unsafe source selection.

### Answer 5

Fence new exec and filesystem operations, stop or quiesce the target, enumerate its mount namespace and helpers, and record open descriptors, leases and snapshot parentage. Unmount child mounts deepest first, detach the active root, terminate helpers, close namespace and file handles, release the active snapshot and its lease, then run or observe reachability-based garbage collection.

Verify that no mountinfo entry, process working directory, root, file descriptor, lease or snapshot metadata references the deleted active snapshot and that its upper/work storage is reclaimed. Separately trace the surviving container to its committed parent snapshots and content descriptors, re-read representative files and verify digests. The expected result is removal of only the unreachable active child; shared committed layers and content remain reachable and unchanged.
