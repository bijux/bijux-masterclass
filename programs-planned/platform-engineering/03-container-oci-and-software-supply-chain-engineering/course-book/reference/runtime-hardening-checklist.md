# Runtime hardening checklist

Review the **effective runtime request**, not only image metadata.

## Identity and privilege

- [ ] non-root UID/GID is explicit and present/mapped correctly;
- [ ] supplemental groups are minimal;
- [ ] capability sets begin empty;
- [ ] `noNewPrivileges` is enabled;
- [ ] setuid/setgid files are absent or justified;
- [ ] privileged mode, host namespaces, engine sockets, and broad host mounts are rejected.

## Filesystem and devices

- [ ] rootfs is read-only;
- [ ] each writable mount has an owner, lifetime, quota, and backup/recovery policy;
- [ ] secret/config mounts are separate from image content;
- [ ] mount propagation is controlled;
- [ ] proc/sys/device exposure is bounded;
- [ ] temporary storage exhaustion behavior is known.

## Kernel controls

- [ ] namespace set matches the threat model;
- [ ] user-namespace mappings are inspected rather than assumed;
- [ ] seccomp profile is named/versioned and tested;
- [ ] LSM policy is identified where available;
- [ ] device allowlist and cgroup placement are explicit;
- [ ] stronger isolation is chosen when shared-kernel risk is unacceptable.

## Lifecycle and resources

- [ ] workload process receives termination directly;
- [ ] PID 1 reaps children or a justified init is present;
- [ ] shutdown grace and forced-kill behavior are measured;
- [ ] CPU, memory, PID, I/O, and descriptor limits have failure oracles;
- [ ] health checks do not mutate business state or create overload;
- [ ] logging cannot block the workload indefinitely or masquerade as durable audit.

## Observation

Collect process credentials, capability sets, namespace IDs, mounts, cgroup values/events, open descriptors, sockets, signal/exit evidence, and cleanup state. A declared profile is design evidence; observed effective state is implementation evidence.
