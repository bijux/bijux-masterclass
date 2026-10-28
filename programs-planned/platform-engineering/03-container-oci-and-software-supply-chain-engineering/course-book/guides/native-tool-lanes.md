# Native-tool lanes

The dependency-light Atlas implementation makes the standard object model inspectable. Independent tools test interoperability and production-shaped behavior. Keep their evidence separate.

## Build lane

Use BuildKit, Docker Buildx, Podman/Buildah, or another builder to build the checked Containerfiles. Capture tool/frontend versions, lock files, base digests, platform, cache/network/secret mode, and output digest. Compare object semantics with the course builder; do not require byte equality unless the experiment controls both implementations sufficiently.

## Runtime lane

Use runc, crun, containerd/nerdctl, Docker, or Podman to execute a generated bundle/image. Inspect effective UID/GID, capabilities, namespace IDs, mounts, cgroup settings, seccomp/LSM, PID 1, signals, exit, and cleanup. Rootless claims require daemon/runtime/user-namespace/cgroup/storage/network evidence, not merely a non-root workload UID.

## Registry lane

Use a real registry plus ORAS/Skopeo/Crane. Test push/pull by digest, tag mutation, referrers, authorization, retention, garbage collection, mirroring/replication, and recovery. The loopback course registry is not conformance or durability evidence.

## Supply-chain lane

Use Syft/Trivy or equivalent for inventory, a vulnerability scanner with dated database, and Cosign/Sigstore or another attestation system. Verify exact subject, identity constraints, transparency/rekor evidence where relevant, builder/source policy, and revocation behavior.

## Evidence labels

Every report must identify one of:

- dependency-light semantic evidence;
- independent native-tool evidence;
- target-runtime evidence;
- environment-backed but not executed;
- failed or review-required.

Never merge these into one undifferentiated “pipeline passed” status.
