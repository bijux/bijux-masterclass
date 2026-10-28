# Module 1 — Containers as Linux process isolation

A container is not a small virtual machine, and an image is not a running container. The process that handles an Atlas request is an ordinary Linux process. It still executes syscalls against the host kernel, consumes host-scheduled CPU, allocates host-managed memory, opens kernel file descriptions, and can be killed by host policy. What changes is the **view and authority** presented to that process.

This module makes the container boundary concrete before an OCI runtime or image format is introduced.

## Learning outcomes

By the end of the module you can:

- explain a container as a coordinated process-isolation and resource-governance arrangement;
- distinguish namespace isolation, cgroup accounting, capability restriction, filesystem presentation, and syscall filtering;
- compare a container with a virtual machine without reducing the difference to startup speed;
- explain why UID `0` inside a user namespace need not be host root;
- reason about PID 1, signal forwarding, child reaping, and graceful termination;
- identify what a container boundary does not protect;
- derive Atlas runtime obligations from the Course 2 handoff.

## Start with the process, not the image

Run an executable directly:

```text
execve("/usr/local/bin/atlas-api", argv, envp)
```

The kernel creates a process image using the executable, mappings, credentials, file descriptors, current directory, resource limits, and namespaces inherited or configured by the caller. A container runtime eventually performs the same kind of operation. It does not manufacture a second kernel.

A useful model is:

```text
container = process tree
          + namespace membership
          + cgroup membership
          + credentials and capabilities
          + root filesystem and mounts
          + syscall policy
          + lifecycle supervision
```

Every term has an owner. Namespace membership is established by clone/unshare/setns operations. Cgroup membership is controlled through the cgroup filesystem or a service manager. Credentials come from user and group mappings. Mounts shape the filesystem view. Seccomp filters selected syscall attempts. A runtime coordinates these mechanisms and then starts the configured process.

When someone says “the container cannot see the host,” ask which namespace and which resource they mean. A mount namespace can hide most host paths while the process still shares the host kernel, clock behavior, CPU vulnerabilities, and many global kernel subsystems.

## Namespaces isolate views

Linux namespaces do not all isolate the same thing.

| Namespace | Changes the process view of |
|---|---|
| PID | process identifiers and ancestry |
| mount | mount table and propagation |
| network | interfaces, routes, sockets, firewall state |
| UTS | hostname and domain name |
| IPC | System V IPC and POSIX message queues |
| user | user/group IDs and capabilities |
| cgroup | visible cgroup hierarchy |
| time | selected monotonic/boottime offsets |

A PID namespace makes a process appear as PID 1 within that namespace. It does not hide CPU consumption. A network namespace gives a separate network stack. It does not create connectivity; interfaces, routes, veth pairs, bridges, or another transport must still be configured. A mount namespace gives a separate mount table. It does not copy the underlying files.

Isolation claims therefore need predicates:

```text
Bad:  "The process is isolated."
Good: "The process has a private PID, mount, UTS, IPC, and network view;
       a user-namespace mapping; no ambient capabilities; a read-only root;
       and bounded cgroup membership."
```

## User namespaces change the meaning of root

Traditional container deployments often ran a process as UID 0 inside a namespace that mapped directly to UID 0 on the host. Dropping capabilities reduced authority, but a kernel escape could still expose host-root consequences.

A user namespace can map IDs:

```text
container UID 0      -> host UID 100000
container UID 65532  -> host UID 165532
```

Inside the namespace, UID 0 may hold capabilities scoped to that namespace. Outside, it is an unprivileged host identity. This is the foundation of many rootless container modes.

User namespaces are not a universal safety switch. Filesystem ownership must match the mapped IDs. Some operations and filesystem types have restrictions. Networking may require user-space helpers. Kernel attack surface remains. The mapping must be inspected rather than assumed.

Atlas deliberately runs its workload as UID/GID `65532`. The checked course harness maps that workload identity to a subordinate host ID and gives it ownership only of the state directory. The harness itself is launched with host-root authority so it can create mounts in the build environment; it therefore proves the workload mapping and mount behavior, **not** a fully rootless runtime architecture. The optional native lane evaluates that stronger claim separately.

## cgroups govern use, not view

Namespaces answer “what can the process see?” Cgroups answer “how is resource use accounted for and controlled?”

Cgroup v2 can govern:

- CPU weight and maximum bandwidth;
- memory high/maximum thresholds and OOM behavior;
- number of processes/tasks;
- I/O weight or limits, depending on the device and controller;
- placement in an accounting hierarchy.

A memory limit is not a reservation. A CPU quota is not a latency guarantee. A PID maximum counts tasks and can block thread creation. Resource settings interact with workload shape, page cache, runtime garbage collection, kernel memory, and parent cgroups.

Course 2 handed off resource values as hypotheses. Course 3 turns those values into a runtime profile but does not call them proven capacity. That proof belongs later, under Kubernetes scheduling and performance experiments.

## Capabilities divide traditional root authority

Linux capabilities split many privileged operations into named units such as network administration, changing ownership, or loading kernel modules. A process can have capability sets including permitted, effective, inheritable, bounding, and ambient capabilities.

Container hardening usually begins with an empty capability set and adds only what a measured requirement demands. Running as a non-root UID while retaining broad capabilities is not equivalent to least privilege. Conversely, UID 0 with no capabilities is still not automatically harmless: file ownership, namespace scope, setuid binaries, and kernel interfaces matter.

Atlas needs no elevated capability for its API or worker. The runtime profile therefore starts from an empty bounding and effective set.

## The filesystem is assembled, not magically copied

A container root filesystem is typically assembled from image layers and presented through a mount namespace. Writable changes may be stored in an overlay or another snapshot mechanism. Runtime mounts inject durable state, configuration, secrets, devices, and temporary files.

This produces several distinct lifetimes:

```text
image content             immutable release input
container writable layer  disposable process-instance state
named/host/CSI volume     separately owned persistent state
secret/config mount       runtime-injected configuration
memory-backed tmpfs       ephemeral bounded state
```

Atlas places spool and results under `/var/lib/atlas` because they outlive process replacement. It places runtime coordination under `/run/atlas`. It does not write logs into the image filesystem as a durable strategy.

A read-only root filesystem is effective only when the workload’s legitimate write paths are known and mounted separately. Turning it on without classifying writes produces outages; leaving it off because the application writes everywhere hides a design defect.

## PID 1 is a lifecycle role

The first process in a PID namespace has special responsibilities. Signals sent to the container are delivered according to runtime rules, often to PID 1. Orphaned children are reparented to it. If it never waits for exited children, zombies accumulate.

Shell-form commands can accidentally place a shell at PID 1:

```dockerfile
CMD atlas-api --port 8080
```

The shell may not forward SIGTERM as expected. Exec form avoids the extra shell:

```dockerfile
CMD ["/usr/local/bin/atlas-api", "--port", "8080"]
```

An init shim can be justified when the application launches children but does not reap them correctly. It is not needed as ritual. The better question is whether the process tree and shutdown semantics require one.

The Course 2 contract gives Atlas thirty seconds to stop. Course 3 must prove that SIGTERM reaches the actual workload, new work stops, in-flight work is bounded, and the process exits before escalation.

## Containers and virtual machines solve different boundaries

A virtual machine runs a guest kernel behind a virtualization boundary. A container uses the host kernel. That difference changes:

- kernel version and feature ownership;
- patch and reboot responsibility;
- attack surface;
- device model;
- boot model;
- density and startup characteristics;
- observability and debugging methods.

Neither is universally “more isolated.” The strength depends on the hypervisor, kernel, runtime, configuration, threat model, and workload. Sandboxed runtimes may place container workloads behind a lightweight VM or userspace kernel, intentionally combining models.

Use a VM when a separate kernel boundary, operating-system control, or incompatible kernel is required. Use process isolation when shared-kernel economics and the threat model make it appropriate. Use both when the platform needs container packaging with a stronger workload boundary.

## What the boundary does not provide

A well-configured container does not automatically provide:

- tenant-safe isolation against every kernel vulnerability;
- secret safety if secrets are included in image layers or environment dumps;
- network policy;
- trusted software provenance;
- vulnerability absence;
- correct application authorization;
- data durability;
- backup and restore;
- high availability;
- protection from a compromised privileged runtime daemon.

This course treats those as separate claims with separate evidence.

## Worked failure: the image that was not the container

An operator reviews an image and confirms:

- `USER 65532`;
- no shell package;
- a non-root working directory;
- a health endpoint.

The production runtime starts it with:

- `--user 0`;
- the host root filesystem bind-mounted at `/host`;
- `CAP_SYS_ADMIN`;
- privileged mode;
- no memory limit.

The image review was accurate but irrelevant to the effective runtime boundary. Image configuration supplies defaults. The runtime can override them.

The reverse failure also occurs. A hardening policy demands a read-only root and an empty capability set, but the application has an undocumented write to `/tmp/cache` and binds port `80` using a legacy configuration. The runtime profile is strong; the application contract is incomplete.

The correct artifact is a joined claim:

```text
image configuration
+ runtime configuration
+ host/runtime implementation
+ observed process state
= effective execution boundary
```

## Atlas capstone increment

In this module you produce `container-boundary.md`, which states:

- required namespaces;
- user-ID mappings;
- capability policy;
- cgroup hypotheses;
- immutable and writable paths;
- signal and process-tree expectations;
- unsupported isolation claims.

You also run Atlas Probe inside the course mini-runtime and compare its observed PID, UID, GID, hostname, writable paths, and root filesystem with the profile that requested them.

## Engineering judgment

A mature container review does not ask “Is it containerized?” It asks:

1. Which process tree is being isolated?
2. Which kernel remains shared?
3. Which views are private?
4. Which authorities remain?
5. Which resources are bounded?
6. Which files are immutable, ephemeral, or durable?
7. How does termination propagate?
8. Which properties come from the image, and which come from runtime policy?
9. What evidence came from inspection, and what came from execution?

Those questions remain useful when Course 4 introduces Pods. Kubernetes schedules and reconciles container workloads; it does not erase the Linux process model underneath them.


## Deep review — prove the effective boundary

A useful container review does not begin with the image name or the engine command. It reconstructs the effective process boundary from observations. For Atlas, the minimum evidence set is deliberately redundant:

```text
process identity       /proc/<pid>/status and stat data
namespace membership   /proc/<pid>/ns/* inode identities
capabilities           CapInh, CapPrm, CapEff, CapBnd, CapAmb
privilege escalation   NoNewPrivs
seccomp                 Seccomp and Seccomp_filters
cgroup placement       /proc/<pid>/cgroup plus controller files
mount view              /proc/<pid>/mountinfo
network view            namespace identity, interfaces, routes, listeners
resource outcome        memory.events, cpu.stat, pids.current, pressure data
lifecycle outcome       parentage, PID 1, signals, exit reason, child reaping
```

No individual line proves “the container is secure.” Together they allow a bounded claim about one process tree on one host under one runtime configuration. That phrasing matters. Namespace isolation can be present while the workload still has a writable host mount. A non-root UID can coexist with a dangerous supplemental group. A read-only root can coexist with the container-engine socket. Evidence must cover independent axes rather than search for one green control.

### Trace a compromised Atlas process

Assume an attacker gains arbitrary code execution inside `atlas-api`. Work outward from the process:

1. **Application authority.** The attacker can use every file descriptor, environment variable, token, and socket available to the process. Container boundaries do not revoke application-granted authority.
2. **Filesystem authority.** The attacker can write to declared writable mounts. A read-only image root prevents in-place persistence there but does not protect durable Atlas data from an authorized process.
3. **Network authority.** The attacker can reach every destination allowed by the network namespace, routing, firewall, proxy, and credential policy. A private namespace is not automatically a restricted network.
4. **Kernel authority.** The process can invoke allowed syscalls against the shared host kernel. Capabilities, seccomp, LSM policy, devices, and namespace ownership determine how far those calls reach.
5. **Runtime/control-plane authority.** A mounted engine socket or broad host path can collapse the intended boundary even when every image scanner is green.
6. **Host consequences.** A kernel escape, vulnerable device, or incorrectly mapped user namespace can cross the remaining boundary. A conventional container is therefore inappropriate when the threat model requires a separate kernel.

This trace is more useful than a list of hardening flags because it connects each control to a consequence.

### Decide when a container is the wrong isolation unit

Prefer a stronger boundary—such as a microVM, dedicated virtual machine, or dedicated host—when the platform executes mutually hostile tenant code, must run a different kernel, exposes sensitive devices, cannot accept shared-kernel escape risk, or needs a fault domain independent of the host kernel. The trade-off is not merely start time. It includes image/runtime integration, observability, patching, density, device access, and operational complexity.

Conversely, do not select a VM-backed runtime to compensate for an application that receives excessive credentials or a writable production database. Kernel isolation cannot repair an authorization design.

### Atlas implementation map

The capstone’s `atlas-probe` binary reports process-visible facts. `atlas_container.mini_runtime` assembles a private namespace set, user mapping, read-only root, writable temporary and state mounts, and direct PID 1 execution. The implementation is intentionally small enough to inspect. It is not a production runtime: it does not provide complete cgroup delegation, a maintained seccomp profile, LSM integration, device policy, or multi-tenant daemon isolation.

The lab succeeds only when the learner can state both sides:

```text
Observed:
  Atlas ran as mapped UID/GID 65532, PID 1, with the declared mount behavior.

Not proved:
  universal OCI conformance, production sandbox hardness, or safety for hostile code.
```

That distinction becomes the evidence discipline used throughout the rest of the program.

## Design review: describe the boundary as a matrix

A production review should not accept a single boolean named `isolated`. Build a matrix in which each row names a resource and each column names the mechanism, owner, observation, and residual risk.

| Resource | Mechanism | Owner | Decisive observation | Residual risk |
|---|---|---|---|---|
| process IDs | PID namespace | runtime | inner and outer PID pair | shared kernel |
| network stack | network namespace | runtime/CNI | interfaces and route table inside namespace | host bridge and kernel |
| filesystem view | mount namespace plus rootfs | runtime | mount table and write probes | unsafe injected mounts |
| CPU and memory | cgroup v2 | service manager/runtime | `cpu.stat`, `memory.events`, pressure | parent cgroup and host pressure |
| privilege | UID/GID mapping, capabilities, `no_new_privs` | runtime policy | `/proc/self/status`, mappings | kernel bugs and mounted authority |
| syscalls | seccomp and LSM | runtime/platform security | active profile plus denied-call test | incomplete policy and kernel surface |

The table prevents one mechanism from impersonating another. A private PID namespace says nothing about memory pressure. A cgroup memory limit says nothing about which host files are mounted. A non-root UID says nothing about a mounted engine socket. This habit becomes important in Course 4: Kubernetes security contexts are requests to a runtime, not proof that the requested boundary exists.

### Observe from both sides

One-sided observation is often ambiguous. Inside Atlas Probe, record the namespace PID, credentials, mount table, hostname, routes, capabilities, cgroup path, and writable locations. Outside, record the host PID, host UID, cgroup placement, namespace inode identifiers, and open mounts. Join the two records with a generated execution ID.

```text
execution ID: 9c1…
inside:  pid=1 uid=65532 mount-ns=402653…
outside: pid=28491 uid=165531 mount-ns=402653…
```

The pair proves translation. It also reveals when a command was accidentally run on the host or in a different namespace. In later cluster debugging, the same discipline separates evidence from a pod, node, runtime, and control plane.

### Threats choose the required boundary

Do not choose container isolation before describing the threat. Atlas runs reviewed application code owned by one platform team. The course therefore accepts a shared-kernel container boundary with a non-root workload, no capabilities, a read-only root, bounded writable mounts, and resource controls. If Atlas began executing arbitrary customer code, that decision would need review. A VM-backed sandbox, dedicated node pool, stronger syscall mediation, or separate cluster could become necessary.

This is not an argument that containers are weak. It is an argument that a boundary is meaningful only relative to an attacker, protected asset, failure consequence, and operating model.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-00-orientation/index.md)
- [Next stage](../module-02-oci-runtime-bundles-lifecycle-and-rootless-execution/index.md)
