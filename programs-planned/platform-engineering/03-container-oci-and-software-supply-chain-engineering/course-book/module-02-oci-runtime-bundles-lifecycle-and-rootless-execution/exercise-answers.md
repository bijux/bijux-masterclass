# Worked answers — OCI runtime bundles and lifecycle

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. Distinguish an OCI image layout from an OCI runtime bundle in purpose, structure, and lifecycle.

An image layout is a content-addressed set of blobs plus an index used for storage, transport, and selection. It may contain multiple platforms and non-image artifacts. A runtime bundle is an unpacked root filesystem plus `config.json` prepared for local execution. Images are immutable distribution graphs; bundles are execution requests whose mounts, namespaces, credentials, and lifecycle are interpreted by a runtime.

## 2. Why does the runtime lifecycle separate `create` from `start`?

Separation allows the runtime to establish isolation, create the initial process, expose stable state, and run lifecycle integration before application code executes. An orchestrator or hook can finish networking or policy setup and then start deterministically. It also defines a clear failure boundary: a created-but-not-started container must be recoverable and deletable without pretending the application ran.

## 3. A state file records PID 4120, but that process exited and the PID was reused. What must a force-delete implementation avoid?

The implementation must not signal or kill PID 4120 solely because stale state records that number. It should verify process identity using a stronger handle—such as start time, pidfd, cgroup membership, or namespace identity—and confirm the container’s cgroup/process set. Otherwise it can kill an unrelated host process that later received the same PID.

## 4. Explain how a read-only root can contain writable submounts without contradiction.

Mount permissions are evaluated per mount. The rootfs mount can be read-only while a tmpfs or persistent volume is mounted at `/tmp` or `/var/lib/atlas` with write permission. The child mount covers that path and provides its own superblock/mount flags. This is the intended way to separate immutable release content from runtime state.

## 5. Design UID/GID mappings so inner UID 65532 owns one host state directory but not the rootfs.

Map a subordinate range, for example inner IDs 1–65536 to outer 100000–165535, so inner 65532 maps to outer 165531. Keep the rootfs owned by a host identity the workload cannot write. Chown only the dedicated state directory to outer UID/GID 165531, mount it at `/var/lib/atlas`, and verify no broader parent path is writable.

## 6. A privileged prestart hook reads a bundle annotation and executes it through a shell. Analyze the trust violation.

Untrusted bundle metadata controls a privileged shell command. The hook crosses from workload-controlled content into host authority without structured validation. Shell metacharacters can turn an annotation into arbitrary host execution. The hook should avoid a shell, accept a constrained schema, pass values as arguments, run with least authority, and reject unexpected input.

## 7. Why can a valid seccomp JSON profile still fail at runtime on another architecture?

Syscall numbers and available calls vary by architecture and kernel. A profile may declare one architecture or omit compatible architectures, so the runtime rejects it or filters the wrong syscall identifiers. Workload code paths can also differ across libc and platform. The profile must be architecture-aware and tested against every released platform.

## 8. What evidence distinguishes a rootless workload from a rootless runtime architecture?

A non-root workload is shown by the process credentials inside and outside its namespace. A rootless runtime architecture additionally shows that the runtime daemon/process, namespace creation, storage, networking helpers, and cgroup operations operate without host-root authority. Record host UIDs, user mappings, daemon credentials, helper binaries, and owned host resources.

## 9. A network namespace exists but has only loopback. Is network isolation working? Is application connectivity working?

Isolation is working in the narrow sense: the process has a separate network stack. Connectivity is not configured beyond loopback. Namespace creation and network provisioning are separate responsibilities. The correct diagnosis is not “network namespace failed,” but “isolated stack lacks interfaces/routes/DNS needed by the application.”

## 10. Give a safe cleanup order after failure between rootfs mount and process start.

Stop or confirm absence of the container process, detach child mounts, unmount the rootfs, remove network resources keyed to the container, remove the cgroup after confirming it is empty, and delete runtime state last. Exact order can vary, but cleanup must reverse ownership dependencies and be idempotent. Do not delete identity records before resources can be attributed safely.

## 11. Explain why mounting a container-engine socket defeats many other restrictions.

The socket often lets a client create privileged containers, mount host paths, join host namespaces, or invoke runtime APIs. That is effectively control over the runtime host. A non-root UID and read-only root inside the current container do not constrain what the socket can ask the daemon to create.

## 12. Review this profile: UID 65532, writable root, `CAP_SYS_ADMIN`, host PID namespace, 256 MiB memory max. Which property dominates the risk review and why?

`CAP_SYS_ADMIN` plus the host PID namespace dominate the review. `CAP_SYS_ADMIN` covers a very broad set of privileged operations, and host PID visibility/interaction exposes host processes. UID 65532 is not meaningful comfort under that authority. Writable root and memory bounds matter, but they do not offset the privilege boundary failure.

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
