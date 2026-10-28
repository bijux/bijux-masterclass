# Worked answers — Runtime hardening

These are worked engineering arguments, not slogans. Compare the conclusion, the mechanism that supports it, the counterexample it excludes, and the evidence that would make the decision reviewable.
## 1. Explain why `USER 65532` is a default rather than an enforcement proof.

Image configuration suggests the user when the runtime does not override it. A caller can request UID 0 or another identity. Enforcement requires runtime/admission policy plus observed process credentials. Review all three: image default, effective runtime config, and runtime observation.

## 2. A non-root process belongs to the group that owns the container-engine socket. Evaluate its authority.

The group can often command a privileged daemon to mount host paths, join host namespaces, or start privileged workloads. That authority is effectively host control even though the current process is numerically non-root. Group membership must be treated as capability-bearing authority.

## 3. Design Atlas writable mounts under a read-only root.

Keep the image root read-only. Mount durable storage at `/var/lib/atlas/spool` and `/var/lib/atlas/results` with owner 65532 and backup/capacity policy. Mount bounded tmpfs at `/run/atlas` and `/tmp` with `nosuid`, `nodev`, and where possible `noexec`. Inject secrets read-only at a narrow path.

## 4. Why does `noNewPrivileges` not make existing capabilities harmless?

`noNewPrivileges` prevents gaining additional privilege through exec transitions. It does not remove capabilities already effective/permitted, revoke open descriptors, unmount host paths, or remove namespace authority. Start with an empty capability set separately.

## 5. A 256 MiB memory maximum is set. What evidence is required before calling it a correct production value?

Measure steady and peak working set, page cache, concurrency, request/worker mix, language-runtime behavior, startup, shutdown, failure paths, and OOM response under representative load. Include headroom and node-level contention. Course 3 records a ceiling hypothesis; later performance/capacity evidence validates it.

## 6. A liveness endpoint fails when PostgreSQL is unavailable. Predict incident behavior and redesign it.

During a database outage, every workload becomes unlive, the orchestrator restarts healthy processes, startup adds load, and recovery is delayed. Liveness should test local ability to progress. Database unavailability belongs in readiness only if no valid service can be offered, and in dependency telemetry/alerts.

## 7. Compare seccomp and SELinux/AppArmor control scopes.

Seccomp filters syscall invocations and selected arguments, reducing kernel call surface. AppArmor/SELinux label and mediate access to files, capabilities, signals, network, and other objects according to policy. They overlap in defense but express different properties and are not substitutes.

## 8. The application spawns children and never waits for them. What does PID 1 need to do?

PID 1 must wait on exited children or delegate to an init shim so zombies are reaped. It must also forward termination and coordinate shutdown. If the application cannot do this correctly, use a small audited init rather than a shell that obscures signals.

## 9. Explain why stdout logging transfers rather than solves durability responsibility.

Writing stdout removes file-rotation ownership from the application, but data can still be buffered, dropped, blocked, exposed, or lost by the runtime/collector. The platform must define collection, retention, backpressure, and access. Business durability cannot depend only on logs.

## 10. A tmpfs has no explicit size limit. Which resource boundary can it consume?

Tmpfs pages consume memory and can contribute to the cgroup/host memory limit. Without a size limit, application scratch growth can cause memory pressure or OOM even when heap use seems normal.

## 11. Design a shutdown proof for the thirty-second Atlas contract.

Start API/worker with known in-flight work, send SIGTERM, record the receiving PID and time, prove readiness becomes false, no new work is accepted, in-flight work reaches a defined terminal/checkpoint state, files are flushed, child processes exit, and the main process exits before thirty seconds without SIGKILL. Verify restart reconciles durable state.

## 12. Write an approved runtime profile claim and list its host/runtime prerequisites.

“Atlas runs as mapped UID/GID 65532, with no supplementary groups/capabilities, no-new-privileges, read-only root, declared writable mounts, private namespaces, bounded CPU/memory/PIDs/tmpfs, and direct signal handling.” Prerequisites include user namespaces, cgroup v2 delegation, compatible mount/runtime features, correct host ownership, and tested kernel/runtime versions.

## Continue

- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
