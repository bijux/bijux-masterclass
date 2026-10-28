# Runbook — runtime profile failure

## Trigger

Use when Atlas fails under the approved runtime profile, requires unexpected root/capability/mount authority, does not stop cleanly, violates write-path assumptions, or the observed effective state differs from the request.

## Safety rule

Do not jump to privileged mode, host namespaces, broad host mounts, or engine-socket access. Those changes destroy the diagnostic boundary and can create a larger incident.

## Diagnosis order

1. Confirm exact image digest/platform and entrypoint.
2. Compare Course 2 workload contract, image defaults, requested runtime profile, and observed effective state.
3. Inspect UID/GID/groups, capabilities, no-new-privileges, namespace IDs, mounts, seccomp/LSM, devices, cgroups, sockets, environment, and file ownership.
4. Reproduce with one controlled change at a time.
5. Classify the defect as image content/default, runtime request, host capability, persistent-volume ownership, or application behavior.

## Recovery

Fix the lowest-authority owner. Examples: correct image directory ownership; map volume permissions; add one justified capability; correct a mount destination; update shutdown handling. Rebuild/release when image content changes; version runtime policy when authority changes. Never hide the change in an emergency command.

## Closure

The approved profile runs without unauthorized escalation, shutdown/cleanup pass, durable state reconciles, and a negative test rejects the previous shortcut.
