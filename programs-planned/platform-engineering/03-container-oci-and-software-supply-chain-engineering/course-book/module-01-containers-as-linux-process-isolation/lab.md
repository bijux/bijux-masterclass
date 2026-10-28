# Laboratory — Observe the boundary instead of trusting the command

## Goal

Run Atlas Probe in the course mini-runtime and reconcile requested isolation with observed process state.

## Safety boundary

The checked mini-runtime is a **root-managed teaching harness** because it constructs mounts and ID mappings directly. Run it only in the provided disposable laboratory or an isolated VM, never on a shared workstation. It maps the workload UID/GID to subordinate host IDs, but it is not evidence of a fully rootless runtime architecture. Do not add host-sensitive mounts or a container-engine socket to “make it work.”

## Baseline

Run Atlas Probe directly and record:

```text
PID and parent PID
UID/GID
hostname
visible root directory
writability of /etc, /tmp, and /var/lib/atlas
```

## Hypothesis

The same executable, when started by the mini-runtime, will observe PID 1, UID/GID 65532, the configured hostname, a read-only root, and only the declared writable mounts.

## Controlled action

Run the runtime profile from:

```text
capstone/runtime/profiles/api-runtime.json
```

Then repeat after each controlled defect:

1. remove the user-namespace mapping;
2. make the root filesystem writable;
3. remove the `/var/lib/atlas` mount;
4. replace exec-form arguments with a shell wrapper that does not `exec`.

Do not combine defects; isolate them one at a time.

## Oracle

The accepted profile matches every observation. Each defect changes the expected evidence or causes a deliberate failure. A missing feature is reported as unsupported, not treated as success.

## Evidence

Submit a table with requested, observed, and interpreted values; the host kernel/user-namespace prerequisites; and the command output for every defect.

## Interpretation

Explain which observations are properties of the image, which are properties of runtime configuration, and which depend on the host kernel.

## Cleanup

Use the lab cleanup command, verify no probe process remains, and delete temporary rootfs and namespace state.

## Completion gate

You can diagnose every mismatch without using “Docker issue” or “container issue” as a cause category.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
