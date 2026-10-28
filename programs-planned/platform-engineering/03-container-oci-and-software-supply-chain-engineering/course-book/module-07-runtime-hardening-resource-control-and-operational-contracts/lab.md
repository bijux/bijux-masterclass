# Laboratory — Break the approved runtime profile

## Goal

Prove the Atlas runtime profile by observation and show that policy rejects attractive troubleshooting shortcuts.

## Safety boundary

Use the mini-runtime and temporary state. Do not mount the host root, runtime socket, devices, or sensitive paths. Do not use privileged mode.

## Baseline

Run Atlas Probe with the accepted profile and capture identity, PID, hostname, mount writability, process limits, and termination behavior.

## Hypothesis

The profile satisfies the inherited workload contract while rejecting root, writable root, excessive capabilities, unsafe mounts, and unbounded resources.

## Controlled action

Evaluate and, where safe, attempt:

1. UID 0 override;
2. writable root;
3. `CAP_SYS_ADMIN` request;
4. missing memory/PID limit;
5. host `/proc` bind;
6. secret in environment and diagnostic dump;
7. SIGTERM during in-flight work.

## Oracle

Unsafe configurations are rejected before launch. The accepted profile exposes only declared writes and exits within the shutdown contract without losing durable state.

## Evidence

Submit normalized profiles, policy results, observed `/proc` evidence, mount tests, signal timeline, and durable-state reconciliation after restart.

## Interpretation

Identify which controls belong to image, runtime, host, and future Kubernetes admission/scheduling layers.

## Cleanup

Stop all processes, remove temporary state, and scan reports for the synthetic secret value.

## Completion gate

The runtime contract is explicit enough that Course 4 can map it to Pod/workload controls without guessing engine-specific flags.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
