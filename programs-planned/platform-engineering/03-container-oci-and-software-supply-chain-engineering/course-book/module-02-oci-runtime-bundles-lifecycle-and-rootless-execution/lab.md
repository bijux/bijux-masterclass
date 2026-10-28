# Laboratory — Build and break an OCI runtime bundle

## Goal

Construct a bundle for Atlas Probe, execute it with the course mini-runtime, and diagnose lifecycle and mapping failures from state rather than trial-and-error.

## Safety boundary

Use the disposable course environment. The checked mini-runtime is deliberately **root-managed** and must not be executed on a shared host. It may bind only its temporary rootfs and state directory. A separate native Podman/Buildah lane examines a genuinely rootless architecture when those tools and subordinate-ID configuration are available. Never use `--privileged`, mount the engine socket, or widen host paths to bypass a failure.

## Baseline

Generate the probe rootfs and `config.json`. Validate the profile and capture its normalized form.

## Hypothesis

The bundle can be created, started, observed, stopped, and deleted without leaving mounts, processes, or state. Inner UID/GID 65532 maps to the expected outer identity and can write only declared paths.

## Controlled action

Execute the normal lifecycle, then repeat with:

1. an invalid transition (`start` before `create`);
2. a missing state-directory ownership mapping;
3. a failure injected after rootfs mount but before start;
4. a stale state record whose PID does not match the container identity;
5. a writable `/sys` request that policy must reject.

## Oracle

Normal execution reaches every lifecycle state exactly once and cleans completely. Invalid transitions fail without changing unrelated state. Partial creation unwinds owned resources. Stale PID evidence is not used to signal an unrelated process.

## Evidence

Submit:

- normalized config;
- lifecycle transition log;
- inner/outer identity map;
- mount inventory before and after cleanup;
- failure records for all five cases.

## Interpretation

Explain which failures belong to the bundle, runtime implementation, host capability, or workload contract.

## Cleanup

Verify the temporary mount tree is empty, no probe process remains, and runtime state contains no live container ID.

## Completion gate

A reviewer can reproduce the lifecycle and determine from evidence—not inference—that cleanup did not affect another process or directory.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
