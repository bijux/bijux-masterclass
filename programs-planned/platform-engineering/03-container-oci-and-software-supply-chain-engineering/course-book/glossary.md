# Glossary

**Artifact manifest** — OCI manifest whose primary purpose is to describe non-runnable content and optionally bind it to a subject.

**Attestation** — signed or otherwise authenticated statement making a typed claim about one or more subjects.

**Base image** — image content used as build material. A tag is discovery; a digest is the controlled material identity.

**Blob** — byte sequence stored and retrieved by digest. Its interpretation comes from a descriptor.

**Build context** — files and metadata made readable to a build frontend; a security and reproducibility boundary.

**Build graph** — dependency graph of sources, operations, mounts, parameters, caches, and exported outputs.

**Capability** — unit of Linux privilege separated from the traditional all-powerful root model.

**Container** — runtime-created process tree and isolated/bounded resources. Not an image.

**Content address** — identity computed from exact bytes, usually an algorithm-qualified digest.

**Descriptor** — typed OCI edge containing media type, digest, size, and optional platform/annotations.

**DiffID** — SHA digest of an uncompressed layer tar stream, stored in image configuration.

**DSSE** — envelope that signs a domain-separated encoding of payload type and bytes.

**Evidence class** — course classification describing whether a claim is documentary, semantic, independently implemented, target-environment, or production-observed.

**Image configuration** — OCI object containing platform, rootfs DiffIDs, history, and runtime defaults.

**Image index** — OCI object selecting one or more manifests, commonly by platform.

**Image manifest** — OCI object referencing one configuration and an ordered layer list.

**Layer** — immutable filesystem changeset archive. Later layers may overwrite or whiteout earlier paths.

**Manifest** — registry-addressable JSON object such as an image manifest, image index, or artifact manifest.

**Namespace** — Linux mechanism giving a process a distinct view/identity for resources such as PIDs, mounts, networks, or users.

**OCI image layout** — local directory with `oci-layout`, `index.json`, and content-addressed blobs.

**OCI runtime bundle** — local rootfs plus `config.json` prepared for an OCI runtime.

**Platform tuple** — operating system, architecture, and optional variant/feature metadata used for image selection.

**Provenance** — claim describing builder, source, materials, parameters, and process used to produce subjects.

**Referrer** — artifact manifest whose subject points to another OCI manifest/index, enabling evidence discovery.

**Release** — immutable authorization record selecting exact subjects for an environment after policy evaluation.

**Registry** — service implementing storage and distribution of repository manifests/blobs and mutable references.

**Rootfs** — filesystem tree visible as `/` to the workload process.

**SBOM** — inventory of components and relationships for a declared subject and scope.

**Signature** — cryptographic authentication of bytes or a statement under an identity/key policy.

**Tag** — mutable repository reference to a manifest; useful for discovery, unsuitable as immutable authority.

**VEX** — scoped vulnerability status and justification for a specific product subject.

**Whiteout** — special layer entry hiding or removing lower-layer filesystem content in the merged view.

**Admission/promotion policy** — rules that decide whether exact subjects and evidence may enter an environment. Separate from signature verification.

**Chain ID** — identity derived from ordered DiffIDs, used by some snapshot/content systems to identify an applied layer chain.

**Cgroup** — Linux hierarchical accounting/control mechanism for resource use such as CPU, memory, PIDs, and I/O.

**Content negotiation** — HTTP selection of representation/media type; important when a registry reference may return an index or manifest format.

**Controlled rebuild** — repeated build under explicitly held inputs/environment to test a bounded reproducibility claim.

**Effective runtime configuration** — image defaults after runtime/orchestrator/operator overrides; the actual execution request.

**Evidence subject** — immutable object whose properties an SBOM, provenance, signature, or policy claim describes.

**Keyless signing** — short-lived signing identity established through an issuer/certificate/transparency system rather than a distributed long-lived private key.

**LSM** — Linux Security Module framework used by systems such as SELinux and AppArmor to enforce additional policy.

**Multi-platform image** — image index selecting platform-specific child manifests. The index itself is not an executable.

**Native evidence** — evidence produced on the intended target architecture/runtime rather than through cross-compilation or emulation.

**No-new-privileges** — process attribute preventing exec from gaining privileges through setuid/setgid or file capabilities.

**Opaque whiteout** — layer entry that hides lower-layer children of a directory.

**Promotion** — authorization/copy/metadata operation moving an existing immutable subject into another lifecycle/environment; not rebuilding.

**Reproducible build** — build for which a defined input/environment procedure can reproduce the output. Scope must be stated.

**Revocation** — decision that a key, identity, evidence object, release, or image subject is no longer authorized. The affected subject must be named.

**Rootless runtime** — runtime architecture whose daemon/monitor/storage/network/user-namespace path operates without host-root authority; different from merely running the workload as non-root.

**Seccomp** — Linux syscall-filtering mechanism. It restricts selected syscall attempts but does not replace capabilities, mounts, devices, network policy, or LSM controls.

**Supply-chain attestation** — authenticated typed statement about a subject, such as provenance or test evidence. Verification and authorization remain separate.

**Target-runtime evidence** — result produced on the intended architecture/kernel/runtime configuration, with environment recorded.

