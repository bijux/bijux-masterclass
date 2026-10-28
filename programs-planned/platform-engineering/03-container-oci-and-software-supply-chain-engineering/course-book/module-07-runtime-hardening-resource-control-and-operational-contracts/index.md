# Module 7 — Runtime hardening, resource control, and operational contracts

An image can request a non-root user, advertise a stop signal, and expose a port. None of those defaults is an enforced runtime boundary. The effective workload is produced when image configuration meets runtime policy, host capabilities, mounted state, network topology, and application behavior.

This module turns the Course 2 workload contract into a precise execution profile and then attempts to break it.

## Learning outcomes

By the end of the module you can:

- distinguish image defaults, runtime configuration, host enforcement, and observed process state;
- design a least-authority identity and capability profile;
- reason about read-only roots, writable mounts, secrets, devices, and proc/sys exposure;
- set resource controls without claiming unmeasured capacity guarantees;
- define PID 1, signal, shutdown, health, and logging contracts;
- classify seccomp, AppArmor/SELinux, and no-new-privileges controls;
- debug failures caused by permissions, mounts, cgroups, signals, and health semantics;
- produce a Kubernetes-ready runtime contract without writing Kubernetes YAML prematurely.

## Four layers of runtime truth

A useful review separates:

```text
image configuration      what the publisher suggests
runtime configuration    what this launch requests
enforcement environment  what runtime + kernel can enforce
observation               what the process actually experiences
```

For the runtime user:

```text
image:       USER 65532
runtime:     process.user.uid = 65532
policy:      reject uid 0 and privilege escalation
observation: /proc/self/status shows mapped UID 65532
```

If any layer disagrees, the claim is unresolved. Image-only scanners cannot prove runtime enforcement. Runtime-policy files cannot prove the workload obeys the shutdown contract. Observation without a declared policy can show current behavior but not whether drift will be rejected.

## Identity is more than `USER`

A complete identity profile includes:

- UID and primary GID;
- supplementary groups;
- user-namespace mapping;
- filesystem ownership;
- capability sets;
- `noNewPrivileges`;
- setuid/setgid binaries;
- service/workload identity injected at runtime;
- authorization to network, storage, and secret systems.

Atlas runs as UID/GID 65532, receives no supplementary group by default, has an empty capability set, and uses a short-lived workload identity external to the image. Image metadata never contains cloud credentials.

A group can be as powerful as root for a specific resource. Membership in a group owning the runtime socket, a block device, or sensitive volume must be reviewed as authority, not convenience.

## Capabilities and privilege escalation

Start with all capabilities dropped. Add one only after identifying:

1. the exact syscall/operation that fails;
2. why a less-privileged design cannot satisfy it;
3. the namespace in which the capability is effective;
4. the affected attack surface;
5. the regression test that proves it remains necessary.

`noNewPrivileges` prevents `execve` from granting additional privilege through setuid/setgid bits or file capabilities. It does not remove existing capabilities or stop a process from using already granted authority.

Atlas binds port 8080, so it does not need `CAP_NET_BIND_SERVICE`. It writes only owned mounts and needs no DAC-bypass capability. It does not modify network interfaces, mount filesystems, or change host identity.

## Read-only root and declared write paths

The inherited storage contract separates:

```text
/var/lib/atlas/spool    durable
/var/lib/atlas/results  durable
/run/atlas              ephemeral runtime coordination
/tmp                    bounded ephemeral scratch
```

The image root is read-only. The runtime mounts writable paths independently. The application must fail clearly when durable storage is unavailable or full; it must not fall back to the container writable layer.

Mount review covers:

- source owner;
- destination;
- read/write mode;
- execution, device, and setuid flags;
- propagation;
- symlink handling;
- expected UID/GID;
- capacity and inode policy;
- cleanup and backup ownership.

A secret mount should be read-only, narrowly scoped, and absent from process arguments and logs. Environment variables are easy to inject but can leak through diagnostics and crash reports. The course prefers file-descriptor or file mounts for sensitive material when the consumer supports them.

## Kernel interfaces and device policy

A hardened workload rarely needs arbitrary devices. The runtime should expose only the device nodes required for ordinary process operation.

Sensitive interfaces include:

- container-engine sockets;
- host `/proc` or `/sys`;
- block devices;
- kernel logs;
- BPF and perf interfaces;
- host network namespaces;
- debug or tracing interfaces.

Masking selected paths and mounting `/proc` inside a private PID namespace reduce exposure. The exact policy depends on runtime and host. “No hostPath mounts” later in Kubernetes is a useful default, but Course 3 identifies the lower-level risk first.

## Seccomp, LSMs, and layered controls

### Seccomp

Filters syscall attempts. It reduces kernel attack surface and can enforce “this process never needs mount/ptrace/keyctl” style properties. Profiles must cover startup, steady state, error, and shutdown paths for each architecture.

### AppArmor or SELinux

Linux Security Modules can constrain file, capability, network, signal, and other access according to labels/profiles. They can express controls beyond UID/GID mode bits. Policy availability and semantics depend on the host distribution and configuration.

### Capabilities and no-new-privileges

Reduce traditional root authority and prevent privilege acquisition through exec.

These controls are complementary. Passing one does not compensate for a privileged host mount or runtime socket.

## Resource controls are operational safety boundaries

Atlas runtime profiles include memory, CPU, PID, and file-descriptor hypotheses.

Review them carefully:

- `memory.max` is a hard ceiling, not guaranteed capacity;
- `memory.high` can create reclaim pressure before the hard limit;
- CPU quota limits time over a period and can create throttling/tail latency;
- CPU weight controls relative sharing under contention;
- `pids.max` counts threads/tasks;
- `nofile` must cover listeners, client connections, files, pipes, and logs;
- tmpfs consumes memory and needs a size limit;
- volume capacity is independent from memory controls.

The correct failure behavior is part of the profile. Under memory pressure, does the process degrade, receive allocation errors, or get killed? Does a worker retry work that was partially completed? Does the supervisor distinguish an OOM kill from a normal exit?

Course 5 of the API program measured workload behavior; Platform Course 9 will later prove cluster capacity. Here we ensure the process cannot consume without bound.

## PID 1, child processes, and shutdown

Atlas binaries run directly as PID 1. They register SIGTERM/SIGINT handlers, stop accepting new work, finish or checkpoint bounded in-flight work, flush durable state, and exit within thirty seconds.

The runtime should:

- send the configured termination signal;
- wait the grace interval;
- escalate only after the interval;
- report exit reason and signal;
- not restart endlessly on an intentional stop;
- preserve durable state mounts across replacement.

A health check must not keep reporting ready after drain begins. Readiness means “accepting work now,” not “process exists.” Liveness means the process can make progress under the platform’s recovery model; it should not fail merely because a remote dependency is temporarily unavailable if restart will not help.

## Health checks are contracts with side effects

Poor checks cause outages:

- a liveness check that requires the database restarts every replica during a database incident;
- a readiness check that always returns 200 sends traffic during startup or drain;
- an expensive check becomes a self-inflicted load generator;
- a check mutates durable state;
- a check leaks sensitive configuration.

Atlas exposes:

```text
/live   process/event-loop progress only
/ready  local initialization + required durable storage + accepting flag
```

External dependency health is emitted as telemetry and may affect readiness only when the API truly cannot serve any valid request without it.

## Logging and stdout are not durability

Container practice often writes application logs to stdout/stderr so the runtime/platform can collect them. This is an ownership transfer: the process owns emission, while the platform owns buffering, rotation, transport, retention, and access.

The application must:

- write structured bounded records;
- avoid secrets and uncontrolled payloads;
- handle blocked/broken log sinks according to policy;
- preserve audit or business state in the correct durable system rather than relying on log delivery.

A container log file on a node is not a backup, and stdout success is not proof that a central collector received the event.

## Worked case: hardened image, privileged launch

An image passes a static security review:

- non-root user;
- no package manager;
- no shell;
- minimal SBOM;
- read-only intent.

A troubleshooting run launches it with:

```text
host PID namespace
host network
writable host root at /host
runtime socket mounted
all capabilities
```

The effective boundary is privileged. The image is not “secure in production” because the launch profile overrides its defaults.

The release system must publish both:

- image evidence;
- approved runtime-profile evidence.

Course 4 will turn those profiles into Pod security and workload specifications.

## Atlas capstone increment

You will execute Atlas Probe under the accepted runtime profile and verify:

- UID/GID mapping;
- PID 1;
- hostname;
- read-only `/etc`;
- writable bounded `/tmp`;
- writable `/var/lib/atlas`;
- empty capability intent and no-new-privileges;
- resource declarations;
- signal/shutdown behavior.

You will also validate API and worker runtime profiles and reject candidates with root user, writable root, excessive capabilities, missing limits, unsafe mounts, or incompatible stop behavior.

The Course 4 handoff receives a runtime contract rather than opaque engine flags.

## Runtime review questions

1. Which image defaults can the caller override?
2. Which runtime controls are mandatory policy?
3. What identity exists inside and outside user namespaces?
4. Which paths can be written, and who owns their lifecycle?
5. Which kernel interfaces and devices are visible?
6. What happens under memory, PID, disk, and log pressure?
7. How does shutdown propagate and complete?
8. What do liveness and readiness mean?
9. Which properties were observed, and on which host/runtime?
10. What must the orchestrator enforce in Course 4?


## Effective-configuration audit

A production review should reconstruct the running process rather than trust the image or deployment request. Capture:

```text
identity           UID/GID, groups, user mapping
privilege          capability sets, no-new-privileges, LSM label
syscall policy     seccomp mode/filter count and deliberate denied action
namespace set      inode identities and expected sharing
filesystem         mountinfo, root read-only, writable path options
kernel interfaces  devices, proc/sys exposure, engine/control sockets
resources          cgroup limits, events, throttling, pressure, OOM outcome
lifecycle          PID 1, children, stop signal, grace, exit reason
health             startup/live/ready behavior through drain and dependency faults
network            interfaces, routes, listening sockets, egress policy
```

Compare the observation with the approved runtime profile. Drift is a policy failure even when the application still serves traffic.

## Authority anti-patterns

### Container-engine socket

Mounting Docker, containerd, CRI-O, or another privileged control socket often grants effective host control. A process can request a privileged workload, host mounts, or host namespaces. Treat the socket as a platform-admin API, not a convenience file.

### Broad host mounts

A read-only host mount can still expose credentials, kernel data, source, or personal information. A writable mount can modify host configuration or binaries. Mount only a specifically owned subtree with explicit mode and propagation.

### Privileged mode

“Privileged” generally widens capabilities, devices, seccomp, LSM, and mount behavior simultaneously. It is not a fix for an unexplained permission error. Reproduce the one denied operation and decide whether the workload should own it.

### Hidden write fallback

Some applications fall back from an unavailable durable path to `/tmp` or the writable image layer. That converts a visible storage failure into silent data loss. Atlas fails readiness and the relevant operation instead.

## Resource experiments need outcome semantics

A limit is useful only when failure behavior is understood. Test:

- memory pressure and OOM kill versus handled allocation failure;
- CPU throttling and request/worker latency;
- PID/thread exhaustion;
- file-descriptor exhaustion;
- tmpfs, inode, and durable-volume exhaustion;
- blocked stdout/log collector;
- graceful shutdown with in-flight durable work.

Record both kernel/controller evidence and application outcome. “The cgroup rejected allocation” is insufficient if the worker leaves an operation in an unrecoverable state.

## Seccomp and LSM evidence

Static profile syntax is E0/E1 evidence. Stronger evidence demonstrates:

1. the target host supports and enables the mechanism;
2. the runtime loaded the intended profile;
3. allowed startup, steady-state, failure, and shutdown paths work;
4. a deliberately forbidden action fails for the expected policy reason;
5. audit records identify the denial without leaking secrets;
6. architecture-specific syscall differences are covered.

The mini-runtime does not claim these properties. Course 4 and Course 8 will introduce platform admission and broader policy, but the workload contract must state what it needs now.

## From container profile to Kubernetes requirements

The handoff should say:

```text
runAsUser/runAsGroup intent       65532
privilege escalation              forbidden
capability requirement            none
root filesystem                   read-only
writable paths                     tmp, spool, results, runtime coordination
host namespaces/devices/sockets   none
termination grace                 30 seconds
health semantics                  explicit startup/live/ready
resource values                   hypotheses with evidence class
```

It should not prescribe a Deployment, Pod, probe interval, or storage class. Those are Course 4 design decisions constrained by this workload truth.

## Controls compose; none is the whole sandbox

A defensible runtime profile layers controls with different failure coverage:

```text
non-root mapped identity
+ empty capabilities
+ no_new_privs
+ read-only root and classified writable mounts
+ private namespaces
+ seccomp syscall policy
+ LSM policy where available
+ bounded cgroup resources
+ device and socket denial
+ lifecycle and health contract
```

Removing one layer changes the residual risk. A read-only root does not stop writes to a broad host bind mount. Seccomp does not prevent reading a mounted secret. A memory limit does not prevent network abuse. Empty capabilities do not neutralize a container-engine socket.

### Resource limits need failure semantics

A useful limit specifies what happens at the boundary. At `memory.max`, allocation pressure can trigger reclaim and cgroup-local OOM selection. At `pids.max`, process or thread creation fails. At CPU quota, runnable work is throttled rather than killed. A full tmpfs returns storage errors. Atlas must surface those failures without corrupting spool transitions.

Course values are hypotheses. Later Kubernetes and performance courses decide scheduling requests, limits, and capacity from representative measurements. Course 3 proves only that the profile is explicit and that selected bounds can be observed.

### Health is part of the runtime contract

Liveness answers whether replacement may help. Readiness answers whether new work should be routed. Startup answers whether initialization deserves more time. A process can be alive but unable to access durable state; it should be unready, not necessarily killed. A repeated liveness failure caused by a shared dependency can create a restart storm.

Atlas API readiness includes local initialization, accepting state, and required durable-store access. Worker readiness includes a fresh heartbeat and queue access. Neither is reduced to “PID exists.”

### Termination must be testable

During termination:

1. stop admitting new work;
2. expose unready status;
3. finish or safely checkpoint bounded in-flight work;
4. flush durable state and telemetry where required;
5. exit before the grace deadline.

Test the actual process tree. An entrypoint shell that fails to `exec` can consume SIGTERM. A child process can survive if PID 1 never forwards or reaps. A hard kill must leave durable spool state recoverable on restart.

The runtime profile becomes a Kubernetes input in Course 4, but the cluster cannot invent these semantics for the application.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-06-registries-distribution-digests-tags-and-referrers/index.md)
- [Next stage](../module-08-sboms-vulnerabilities-licenses-and-vex/index.md)
