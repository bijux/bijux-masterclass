# Module 2 — OCI runtime bundles, lifecycle, and rootless execution

Module 1 described the Linux mechanisms. The OCI Runtime Specification gives runtimes a portable contract for assembling and starting them. Its central artifact is deliberately plain: a directory containing a root filesystem and a `config.json`.

The runtime spec does not define image layers, registries, SBOMs, or signatures. Keeping that boundary sharp prevents a recurring design error: asking one artifact to prove properties owned by another stage.

## Learning outcomes

By the end of the module you can:

- describe an OCI runtime bundle and distinguish it from an OCI image layout;
- trace the `create`, `start`, `kill`, and `delete` lifecycle;
- read the major sections of `config.json` and connect them to Linux mechanisms;
- explain hook timing and why hooks expand the trusted computing base;
- design a rootless bundle with user mappings and owned writable paths;
- identify lifecycle races, leaked state, and unsafe cleanup;
- evaluate a runtime configuration against the Atlas workload contract.

## The bundle is an execution request

A minimal conceptual bundle is:

```text
bundle/
├── config.json
└── rootfs/
    ├── usr/local/bin/atlas-api
    ├── etc/
    └── ...
```

`config.json` describes the process and the environment in which it should start. The rootfs supplies files. A runtime translates the configuration into namespaces, mounts, credentials, cgroups, limits, devices, and the final `execve`.

The bundle is local, unpacked execution material. An image layout is content-addressed distribution material. A tool may transform an image into a bundle, but the standards keep the forms separate.

## Lifecycle is a state machine, not one command

The OCI lifecycle separates preparation from execution:

```text
absent
  |
create
  v
created
  |
start
  v
running
  |
exit or kill
  v
stopped
  |
delete
  v
absent
```

During `create`, a runtime prepares isolation and invokes the container process in a state where it has not yet executed the configured application. `start` allows the process to continue into the application. This separation enables setup and hook coordination.

State matters. Starting an already running container, deleting a running container without force semantics, or reusing an ID whose old state has not been cleaned are not harmless command errors. They are lifecycle protocol violations.

A production runtime persists enough state to report the container ID, lifecycle status, PID, bundle path, and annotations. The state directory itself becomes operationally sensitive: stale state can prevent recovery, and unauthorized mutation can redirect cleanup or signal operations.

## `config.json` is a collection of authority decisions

A runtime configuration commonly contains:

### Process

- terminal allocation;
- user and additional groups;
- arguments;
- environment;
- working directory;
- capabilities;
- resource limits;
- `noNewPrivileges`;
- AppArmor or SELinux labels where applicable.

### Root

- rootfs path;
- read-only flag.

### Mounts

- destination;
- source;
- filesystem type;
- options and propagation behavior.

### Linux-specific controls

- namespaces;
- UID/GID mappings;
- devices;
- cgroup path and resources;
- seccomp policy;
- masked and read-only paths;
- sysctls;
- rootfs propagation.

### Metadata and hooks

- hostname;
- annotations;
- lifecycle hooks.

Review this file as executable authority. A single bind mount or capability can dominate dozens of hardening settings.

## Mount order and propagation can break isolation

Mounts are not unordered configuration entries. Parent-child relationships, existing mount points, propagation flags, and bind semantics matter.

A bind mount of `/var/lib/atlas` must occur after the rootfs is mounted and before the process starts. A writable submount can exist under a read-only root. A recursive bind may unexpectedly include nested mounts. Shared propagation can cause mounts created in one namespace to appear elsewhere.

The Atlas profile uses:

```text
read-only rootfs
writable /var/lib/atlas
writable tmpfs /tmp
writable tmpfs /run/atlas
masked sensitive kernel interfaces where supported
```

The state directory is not copied into the bundle. It is an independently owned mount with explicit UID/GID mapping.

## Rootless execution is a coordinated design

Rootless does not mean “run the runtime binary as a normal user and hope.” It requires:

- an available user namespace;
- subordinate UID/GID ranges or an explicit mapping;
- rootfs ownership/mapping that allows setup;
- network strategy that does not require host network administration;
- cgroup delegation or service-manager cooperation;
- compatible storage/snapshot behavior;
- restricted devices and mounts.

The checked course mini-runtime maps workload UID/GID 65532 to a subordinate host ID that owns only the state path, while namespace UID 0 maps to host root so the harness can construct mounts in a restricted build environment. That makes it a root-managed teaching harness, not a rootless runtime. The distinction is intentional: the executable proof demonstrates requested-versus-observed process and mount semantics; the native Podman/Buildah lane is where a fully rootless daemon, storage, networking, and cgroup architecture must be demonstrated.

A rootless runtime may use user-space networking or a helper process. That is a trade-off, not a fake network namespace. Document which component can observe or modify traffic and what performance cost it introduces.

## Hooks are powerful because they run across boundaries

Lifecycle hooks can execute before or after selected transitions. They are useful for networking, device setup, policy, or cleanup. They also expand the trusted computing base.

Questions for every hook:

1. Which namespace does it run in?
2. Which credentials does it hold?
3. What state is guaranteed at that point?
4. What happens if it times out or fails?
5. Is it idempotent?
6. Can untrusted bundle content influence its arguments or environment?
7. How is cleanup performed after partial success?

A hook that concatenates an untrusted annotation into a privileged shell command is a host escape mechanism, not an integration feature.

The Atlas reference profile avoids hooks in the mandatory lane. Networking and mounts are configured directly by the bounded runtime. This reduces the proof surface.

## Seccomp and syscall policy

Seccomp filters syscall attempts based on syscall number, architecture, and selected argument values. They are not semantic application policy: filtering `openat` cannot generally decide whether a business file access is authorized.

A default-deny syscall profile is difficult to maintain across language runtimes and libc versions. A practical profile usually begins with a measured allowlist or a maintained baseline, then removes unnecessary calls and tests startup, steady-state, shutdown, and failure paths.

The course stores a profile contract but does not claim that its dependency-light mini-runtime implements a complete production seccomp policy. Native-tool labs use independent runtimes when available.

## Devices, `/proc`, and kernel interfaces

A minimal rootfs still needs carefully chosen virtual filesystems and devices. Typical bundles expose a controlled `/proc`, `/dev`, `/sys`, and shared-memory area. Device nodes such as null, zero, random, urandom, and a terminal may be required.

Mounting the host `/proc` without a private PID namespace can expose host processes. Mounting `/sys` writable can expose extensive kernel control. Passing the container-runtime socket gives the workload authority over other containers or the host runtime.

“Only one volume mount” is not a useful claim until the source, target, flags, and contained interfaces are named.

## Cleanup is part of correctness

Consider a failure sequence:

```text
user namespace created
mount namespace created
rootfs mounted
state mount attached
network created
process fails before start
```

A correct runtime must unwind resources in an order that does not detach another container’s mount, delete a reused network interface, or leave a cgroup accumulating state. Cleanup actions should be keyed by durable container identity and should tolerate already-absent resources.

Force deletion is not permission to ignore evidence. Before removing stale state, confirm that the recorded PID is not alive and not reused, the cgroup is empty, and mount ownership matches the container identity.

## Worked failure: rootless in name only

A team advertises rootless containers because the application process runs as UID 65532. The runtime daemon still runs as host root, mounts a host directory writable, and the container has no user namespace. The application is non-root, but the runtime architecture is not rootless.

Another team runs a rootless daemon but maps the workload’s writable directory to the wrong subordinate UID. They solve the resulting permission error by `chmod 0777`. The workload now functions, but the host-level data boundary is weakened for every local user.

The correct solution follows the identity mapping through:

```text
inner UID/GID
→ user-namespace mapping
→ outer UID/GID
→ host filesystem ownership
→ mount flags
```

## Atlas capstone increment

You will produce and validate three runtime profiles:

- API;
- worker;
- probe.

Each profile inherits the Course 2 workload contract and declares process arguments, identity, namespaces, writable mounts, resource bounds, and lifecycle. The probe profile is executed by the mini-runtime. API and worker profiles are validated structurally and exercised through native runtimes when available.

You will also create a state-machine report that records accepted and rejected lifecycle transitions. The report must include one interrupted-create case and its cleanup evidence.

## What this module does not prove

A valid `config.json` does not prove:

- that a specific runtime implements every field correctly;
- that the host kernel supports the requested features;
- that the seccomp profile covers every workload path;
- that the cgroup values meet SLOs;
- that the rootfs came from trusted source;
- that the process is free of vulnerabilities.

Those claims belong to runtime conformance, performance, provenance, and security evidence respectively.


## Execution trace — from bundle to process and back to absence

To understand a runtime failure, follow the lifecycle in order rather than treating `run` as an indivisible action.

### 1. Validate input before changing the host

The runtime resolves the bundle directory, parses `config.json`, validates paths and platform-specific fields, checks the container identifier, and decides where runtime state will live. Relative rootfs paths are resolved against the bundle, not the caller’s arbitrary working directory. A robust runtime rejects traversal, malformed mappings, duplicate identifiers, unsupported devices, and impossible mount combinations before partially constructing the container.

### 2. Establish the container process and namespaces

The runtime creates a process that will become the container init. Depending on the design, it creates or joins user, mount, PID, UTS, IPC, network, cgroup, and time namespaces. Ordering matters. User mappings often require coordination with a parent process before operations inside the user namespace can continue. PID namespace semantics mean the first child becomes PID 1 only after the relevant clone/fork boundary.

### 3. Construct the mount tree

The runtime makes mount propagation private where required, binds or mounts the rootfs, creates `/proc` and runtime pseudo-filesystems, applies masked/read-only paths, mounts declared state, and switches the process root with `pivot_root` or an equivalent mechanism. A plain `chroot` changes path resolution but is not a complete mount-isolation strategy. Old-root visibility, propagation to the host, symlink resolution, and mount destination creation are all security-sensitive.

### 4. Apply credentials and restrictions

The runtime sets groups, UID/GID, capability sets, resource limits, `no_new_privs`, seccomp, LSM labels, and other process attributes. Some operations must occur before dropping authority; others must occur after namespace entry. “Drop privilege at the end” is not a sufficient design description because an attacker may exploit an earlier hook or configuration stage.

### 5. Enter the created state

In the OCI lifecycle, `create` prepares the container process without yet allowing the configured application to run. Runtime state should now identify the bundle, PID, status, and annotations. A caller can inspect the state or perform allowed setup. The transition must be atomic enough that a failed create does not leave a container that later looks runnable.

### 6. Start, signal, and observe

`start` releases the init process into the configured executable. Subsequent `kill` requests target the container process according to lifecycle state and signal semantics. The runtime must protect against PID reuse: signalling a raw numeric PID after stale state can affect an unrelated host process. State ownership, namespace-aware signalling, pidfds where available, and cleanup discipline matter.

### 7. Record stop and delete safely

When the process exits, the runtime records stopped state and exit information. `delete` tears down runtime state and owned resources. Cleanup must not remove caller-owned bundle content or shared mounts. Failure during cleanup should remain diagnosable and retryable; silently deleting state while resources remain leaks mounts, namespaces, cgroups, or processes.

## Rootless is a chain of prerequisites

A rootless runtime needs more than a non-zero caller UID:

- subordinate UID/GID ranges and correct mappings;
- user-namespace support enabled by the host;
- filesystems that can represent mapped ownership or idmapped mounts;
- a networking strategy such as user-space forwarding when privileged network setup is unavailable;
- cgroup delegation from a service manager or parent cgroup owner;
- no dependence on privileged devices or host mounts;
- runtime storage that the unprivileged caller owns safely.

When one prerequisite is absent, a tool may fall back to weaker behavior or fail. The correct response is to classify the missing property, not add `sudo` and keep the “rootless” label.

## Hook review

Hooks cross lifecycle and privilege boundaries. Review each hook as executable code with:

- exact phase and namespace context;
- host/container credentials;
- inputs and environment;
- timeout and failure semantics;
- idempotency and cleanup;
- path to the binary pinned by digest or package identity;
- audit and upgrade ownership.

A hook that downloads policy or mutates a rootfs during every start destroys release reproducibility. A hook that needs broad host root should be replaced with a narrower platform controller where possible.

## Atlas runtime-bundle evidence

Course 3 generates a runtime profile and an unpacked rootfs from the image graph, then runs the probe through the bounded mini-runtime. The independent identities remain visible:

```text
image/index digest     distribution subject
platform manifest      selected image variant
rootfs tree            unpacked execution material
config.json/profile    execution request
runtime state          one container instance
process observations   effective result
```

A failure can therefore be assigned to the earliest incorrect object instead of blamed on “the container.”

## The runtime lifecycle is a transaction with cleanup obligations

A useful runtime model is not merely `create → start → delete`. Treat creation as a transaction across several kernel objects:

```text
validate bundle
→ allocate container identity
→ create namespaces
→ create cgroup
→ construct mount tree
→ apply credentials and syscall policy
→ create paused process
→ start workload
```

Every step can fail after earlier steps succeeded. The runtime therefore needs compensating cleanup: unmount private trees, remove cgroups, release network resources, delete state, and preserve diagnostics. A leaked mount or cgroup is not cosmetic. It can retain storage, references, resource accounting, or authority after the workload is believed to be gone.

OCI lifecycle state is externally observable. A caller should not infer `running` from the existence of a directory or PID file. PID reuse makes stale records dangerous. State must bind the runtime identifier to the actual process and namespace generation.

### Hooks are authority-bearing code

Runtime hooks execute at sensitive points around namespace and process creation. Their exact context differs by hook phase: some run in the host namespace, some after namespaces exist, and some after the workload exits. A hook that receives bundle paths, process IDs, or annotations can become a privilege bridge.

Review hooks as deployed code:

- Which identity starts the hook?
- Which namespaces and mounts can it see?
- Can untrusted annotations become command arguments?
- Is failure fatal or ignored?
- Can retries repeat a side effect?
- Who updates and signs the hook binary?

Atlas does not use lifecycle hooks in the mandatory profile. This is a deliberate reduction of authority, not a claim that hooks are always wrong.

### Rootless is an end-to-end architecture

A fully rootless claim covers more than the workload UID. Inspect:

```text
runtime launcher identity
runtime daemon identity, if any
user-namespace mappings
storage driver and ownership
network helper and its privileges
cgroup delegation
port-binding mechanism
host paths and device access
```

The checked mini-runtime in this course is root-managed so it can build mounts in the release environment. It proves that Atlas observes the intended PID, UID/GID, hostname, read-only root, and writable mounts. It does not prove a rootless daemon, rootless storage, rootless networking, or safe operation on a shared host. The native Podman/Buildah lane is explicitly separate.

### Failure analysis exercise

When a bundle fails to start, resist changing permissions blindly. Reconstruct the phase:

1. Did JSON/profile validation fail before kernel state changed?
2. Did namespace creation fail because the host disabled a feature?
3. Did an ID mapping fail because subordinate ranges were absent?
4. Did a mount fail because ownership, propagation, or filesystem support differed?
5. Did the workload start and then fail because its executable, ABI, configuration, or writable paths were wrong?

Each phase produces different evidence and demands different cleanup. “The container failed” is not an actionable diagnosis.

## Continue

- [Exercises](exercises.md)
- [Worked answers](exercise-answers.md)
- [Laboratory](lab.md)
- [Checkpoint](checkpoint.md)
- [Previous stage](../module-01-containers-as-linux-process-isolation/index.md)
- [Next stage](../module-03-oci-images-layers-content-addressability-and-whiteouts/index.md)
