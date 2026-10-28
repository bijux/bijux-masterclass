---
module_id: PLAT-022
program: Platform Engineering
level: 1
module_number: 22
title: Runtime Isolation and Resource Controls
status: complete
last_verified: 2026-09-02
---

# Runtime Isolation and Resource Controls

## One-Page Review

### Governing question

How should a platform constrain a workload's visibility, authority, resource consumption, and interference according to its trust and consequence without mistaking a collection of Linux controls for an absolute security boundary?

### Essential definitions

- A **security boundary** is a deliberately defended separation across which unauthorized influence, observation, or control must be prevented under a stated threat model.
- A **namespace** gives processes an isolated view of a class of kernel-managed resources such as process IDs, mounts, networks, IPC, hostnames, users, cgroups, or clocks.
- A **control group (cgroup)** accounts for and controls resources used by a hierarchy of processes through controllers such as CPU, memory, I/O, PIDs, and cpusets.
- A **Linux capability** is one element of the kernel's partitioned privileged authority; capability sets and user-namespace scope determine its effect.
- **seccomp** filters system-call entry by number and, in some modes, arguments and action; it does not understand application intent.
- A **Linux security module (LSM)** such as SELinux or AppArmor applies mandatory access policy beyond ordinary discretionary owner/group/mode checks.
- **resource request** is capacity reserved for Kubernetes scheduling and commonly a contention weight; a **limit** is a runtime ceiling or enforcement input.
- **throttling** delays CPU execution after quota use; **out-of-memory termination** kills a selected process when memory policy cannot satisfy allocation.
- A **runtime class** selects an implementation and configuration of workload execution, such as a native shared-kernel runtime or stronger sandbox.
- **no new privileges** is a process property preventing `execve` from granting privileges not already available, reflected by Kubernetes `allowPrivilegeEscalation: false` in applicable Linux cases.

### Central model, mechanism, or theorem

Model a runtime contract as $R=(T,I,A,F,S,M,C,E,O,X)$: threat and trust class $T$, namespace/isolation topology $I$, identity $A$, filesystem and device exposure $F$, syscall and mandatory-access policy $S$, resource model $M$, runtime class $C$, enforcement/evidence $E$, observability and response $O$, and exceptions $X$. For resource $r$, distinguish scheduled request $q_r$, runtime limit $l_r$, observed demand $d_r(t)$, and node availability $a_r(t)$. Placement feasibility does not prove runtime safety; containment does not prove fair capacity; a control is valid only within its kernel, runtime, hardware, and policy assumptions.

### Critical invariants

- Every runtime class states its attacker, protected assets, shared surfaces, escape assumptions, compatibility limits, and residual risk.
- Workloads do not share host PID, network, IPC, user, cgroup, or mount namespaces unless the journey explicitly requires and authorizes that topology.
- Containers run as a known non-host-root identity; user-namespace mappings, volume ownership, image users, and runtime credentials are verified together.
- Default workloads drop all capabilities, prohibit privilege escalation, use an enforced seccomp profile, and run under applicable MAC policy.
- Privileged mode, host paths, host namespaces, unrestricted devices, unsafe sysctls, and broad capabilities are exceptional runtime classes rather than local toggles.
- Requests describe scheduling and contention intent; limits and cgroups describe enforcement. Neither is inferred from current average usage alone.
- CPU throttling, memory pressure/OOM, I/O delay, PID exhaustion, ephemeral-storage pressure, and eviction are observed independently.
- Node, kernel, runtime, firmware, and policy versions are inventory and patch responsibilities because the shared substrate is in the boundary.
- Exceptions are narrow, owned, time-bounded, observable, and tied to a migration or removal trigger.

### Common failures

Calling namespaces a sandbox; running root in the initial user namespace; adding `SYS_ADMIN`; enabling privileged mode to fix permissions; sharing host PID or network casually; mounting the container runtime socket; allowing writable host paths; relying on image `USER` without admission enforcement; using seccomp `Unconfined`; treating AppArmor complain mode as enforcement; setting CPU limits from averages; omitting memory requests; assuming memory limits reserve capacity; ignoring page cache and memory-backed volumes; allowing unlimited PIDs; comparing requested and actual CPU as “efficiency”; and accepting runtime exceptions without expiry.

### Compact example

A platform classifies a public build worker as hostile-input, bursty, and disposable. It selects a sandboxed runtime rather than native shared-kernel execution; creates separate user, PID, mount, network, IPC, and cgroup namespaces; maps container root away from host root; mounts an immutable image with bounded scratch space; drops all capabilities; prohibits privilege escalation; applies enforced syscall and MAC profiles; denies host devices and paths; caps PIDs, memory, CPU, I/O, and ephemeral storage; and restricts egress. Scheduling uses measured requests plus headroom, while limits follow overload and failure policy. A timeout, OOM, throttle, or policy denial yields distinct evidence.

### Connections

Retrieve platform boundaries from [PLAT-001](001-platform-engineering-as-complexity-management.md), external-service and team responsibility from [PLAT-008](008-internal-platforms-and-external-cloud-services.md) and [PLAT-009](009-platform-team-boundaries.md), declarative policy and diagnostics from [PLAT-015](015-apis-and-declarative-resources.md) and [PLAT-018](018-feedback-and-error-diagnostics.md), version/evidence controls from [PLAT-019](019-golden-path-versioning.md) and [PLAT-020](020-measuring-developer-experience-without-vanity-metrics.md), and immutable runtime inputs from [PLAT-021](021-container-images-as-platform-artifacts.md).

## Governing Question

What may this workload see and do, how much shared capacity may it consume, which substrate failures can it induce or exploit, and what stronger boundary is required when shared-kernel containment is insufficient?

“Run it in a container” is not a threat model. A typical Linux container is a group of ordinary host processes using namespaces, cgroups, credentials, capabilities, seccomp, LSM policy, filesystem mounts, and a runtime. Those controls can sharply reduce exposure, but the processes still depend on a host kernel and hardware. One kernel vulnerability, dangerous device, writable host mount, or excessive privilege can collapse several layers at once.

Resource control is also not merely security. Scheduling must make promises before demand occurs. Runtime enforcement must preserve node and neighbor health during contention. Application owners need useful performance and clear failure evidence. A platform contract must connect all three.

## Why This Matters

Multi-tenant platforms trade dedicated capacity for shared utilization and operational consistency. The trade creates interference paths: CPU competition, memory pressure, I/O queues, PID tables, network bandwidth, filesystem space, kernel objects, device contention, cache side channels, and control-plane overload. It also creates authority paths through syscalls, files, devices, credentials, host APIs, and co-resident workloads.

Defaults determine whether every consumer must become a kernel specialist. A strong platform provides safe native-container defaults, higher-isolation runtime classes for stronger threats, explicit privileged infrastructure classes, and observable resource policies. Escape hatches remain possible, but their consequence is visible.

Kubernetes expresses some intent through pod and container security contexts, requests, limits, runtime classes, and admission policy. The OCI runtime configuration translates lower-level process, namespace, mount, capability, cgroup, seccomp, and LSM settings. The Linux kernel ultimately enforces supported controls. A declarative field is therefore a request in a chain of implementations, not proof that a node applied it correctly.

## Prerequisites and Retrieval

Retrieve container-image identity, runtime contracts, admission, workload journeys, least privilege, scheduling, Linux processes, virtual memory, filesystems, networking, signals, kernel/user boundaries, threat modeling, capacity planning, probability distributions, and incident response.

You should understand UID/GID permissions, set-user-ID execution, capabilities, system calls, namespaces, cgroup hierarchies, page cache, OOM behavior, CPU scheduling, block I/O, process trees, mounts, sockets, devices, virtual machines, hypervisors, and Kubernetes pod scheduling.

## Learning Objectives

After completing this module, you should be able to:

1. define trust classes, protected assets, attackers, shared surfaces, and residual risks;
2. map PID, mount, network, IPC, UTS, user, cgroup, and time namespace topology;
3. constrain identities, capabilities, privilege escalation, syscalls, filesystems, LSM policy, sysctls, and devices;
4. distinguish Kubernetes requests, limits, cgroup controls, QoS, pressure, eviction, and application backpressure;
5. design CPU, memory, I/O, PID, ephemeral-storage, and device policies from workload behavior;
6. select native, user-namespaced, sandboxed, microVM, dedicated-node, or privileged runtime classes;
7. verify effective node enforcement and diagnose throttling, OOM, eviction, policy denial, and interference; and
8. govern exceptions, emergency access, compatibility, versioning, rollout, and retirement.

## Core Exposition

### Start with the threat and consequence

Classify who controls code and input. First-party reviewed code processing trusted data differs from a public build service executing arbitrary repositories. A service parsing internet traffic differs from an internal batch job. A workload holding signing keys differs from a disposable preview. State protected assets: host kernel, node credentials, other tenants' memory and data, control plane, network, devices, service availability, and evidence.

List attacker goals and paths: escape to host, read neighbor data, steal workload identity, alter node state, persist across restart, exhaust resources, exploit a shared device, confuse audit, or induce an unsafe fail-open. Include compromised dependencies and authorized-but-buggy workloads, not only malicious users.

Choose a trust class before controls. A normal native class may accept shared-kernel residual risk. A hostile-code class may require a userspace-kernel sandbox or microVM. A device plugin or node agent may require constrained host integration on dedicated nodes. “Privileged” is not a higher trust guarantee; it is greater authority and consequence.

### Understand namespace topology

Linux namespaces isolate views. A PID namespace changes visible process IDs and process hierarchy. A mount namespace isolates mount tables. A network namespace supplies network devices, routing, ports, and protocol state. IPC isolates System V and POSIX IPC resources. UTS isolates hostname/domain name. A user namespace maps user/group IDs and scopes capabilities. A cgroup namespace changes the visible cgroup root. A time namespace can virtualize selected clocks.

Omitting a namespace from OCI configuration can inherit the runtime namespace of that type. Joining an existing namespace deliberately couples workloads. Kubernetes pod containers normally share some pod-level namespaces, particularly network, while process namespace sharing is optional. Sidecars may need this topology; unrelated tenants do not.

Namespaces do not filter all kernel APIs or allocate resources. They do not prevent a permitted syscall from exploiting a shared kernel bug. They do not automatically isolate files exposed through mounts, devices passed through, hardware caches, or credentials injected into the process.

Document the topology as an edge list: which containers share which namespaces with their pod, runtime sandbox, node, or host. Admission should reject accidental host namespace use and unexpected cross-pod joins.

### Map identities with user namespaces

Running UID 0 inside an ordinary container can still mean host UID 0 in the initial user namespace, even if other controls limit it. A user namespace can map container UID 0 to an unprivileged host UID range and scope capabilities to resources governed by that user namespace. It reduces consequence but introduces filesystem ownership, volume, device, runtime, and kernel-feature compatibility constraints.

Set `runAsNonRoot` and an explicit numeric user where the workload does not need container-root semantics. Verify the image can execute under that identity and that mounted volumes have correct ownership without broad recursive changes. Avoid assigning host-sensitive groups. Supplementary groups can grant access unexpectedly, so define and inspect them.

User namespaces are not universal escape prevention. Capabilities within a user namespace can affect resources owned by it and descendants, while host resources, idmapped mounts, file capabilities, and nested namespace operations require careful analysis. The kernel configuration and runtime implementation remain trusted.

### Minimize capabilities and privilege transitions

Linux capabilities divide traditional root authority into sets including permitted, effective, inheritable, bounding, and ambient. Some capabilities remain extremely broad. `CAP_SYS_ADMIN` covers many administrative operations and is often a warning that the workload needs a different runtime boundary or architecture.

Default to dropping `ALL`. Add back one capability only after mapping the exact operation, namespace scope, kernel behavior, alternatives, and tests. Binding a low port can often be avoided through a higher container port and service mapping rather than adding `NET_BIND_SERVICE`. Network administration usually belongs in a dedicated network component, not every application.

Set `allowPrivilegeEscalation: false` so the process cannot gain new privileges through `execve` in applicable Linux configurations. This corresponds to the kernel's no-new-privileges behavior and interacts with set-user-ID binaries and file capabilities. Remove such binaries from the image when unnecessary.

Privileged containers receive extensive authority and override or neutralize seccomp, AppArmor, SELinux, and capability restrictions in common Kubernetes behavior. Treat them as host workloads with node-level blast radius. Isolate them on dedicated pools, minimize mounts and credentials, and replace them where narrower host services can expose a bounded API.

### Filter syscalls with seccomp

Seccomp reduces the host kernel interface reachable from a process. Runtime-default profiles deny or constrain uncommon or dangerous calls while preserving common application behavior. An explicit `RuntimeDefault` policy is better than silently depending on runtime configuration, and `Unconfined` should be exceptional.

Custom allowlists can shrink exposure further for stable workloads. Test every architecture and execution path, including startup, signals, language runtime, DNS, observability, profiling, and upgrades. Syscall names and numbers differ by architecture. A profile can break after a runtime or library change.

Seccomp is not semantic authorization. Allowed calls can contain vulnerabilities; argument filtering has limitations; user notification introduces a privileged decision service and race/availability considerations. Prefer a maintained runtime default unless a threat justifies custom lifecycle cost.

### Apply mandatory access controls

Discretionary file permissions answer what owners and groups permit. SELinux and AppArmor can add mandatory policy over processes and objects. SELinux uses labels and type-enforcement policy; AppArmor commonly uses path-oriented profiles. Node operating systems and runtimes must support and load the intended policy.

Enforcing mode blocks denied operations. Complain or audit mode supplies learning evidence but is not containment. Roll a new profile through observation, test, canary enforcement, and broad enforcement without allowing learning output to become an unreviewed universal allowlist.

Bind policy identity to workload version and runtime class. Observe denials with pod, container, image digest, node, profile, operation, and decision context while protecting sensitive paths. An LSM strengthens depth; it does not repair a privileged container that is unconfined.

### Constrain filesystems, mounts, and devices

Use an immutable image and read-only root filesystem. Mount bounded writable paths for scratch, cache, or state, with size, ownership, lifecycle, backup, and executable/set-user-ID behavior declared. Keep secrets in dedicated read-only mechanisms and avoid environment leakage where process inspection or crash output exposes values.

Mount propagation can make host and container mount events visible across boundaries. Use the narrowest propagation and never expose the host root, runtime socket, kubelet directories, device tree, kernel interfaces, or credential stores to ordinary workloads. A container runtime socket commonly grants host-equivalent control despite appearing as one file.

Restrict `/proc`, `/sys`, sysctls, pseudo-filesystems, and device nodes according to runtime. “Safe” sysctls are namespace-scoped under supported configurations; unsafe host-affecting values require isolated nodes or rejection. Device access bypasses ordinary assumptions: GPUs, accelerators, network devices, FUSE, and raw block devices introduce drivers, firmware, DMA, memory, and cross-tenant surfaces.

### Model resource intent explicitly

For resource $r$, distinguish request $q_r$, limit $l_r$, demand $d_r(t)$, observed use $u_r(t)$, and node allocatable capacity $a_r(t)$. Kubernetes scheduling commonly checks aggregate requests against allocatable capacity:

$$
\sum_{w\in W_n} q_{w,r}\le a_{n,r}.
$$

This is a placement constraint, not a guarantee that every workload can reach its limit simultaneously. If limits exceed requests, the node is overcommitted. Overcommit can improve utilization when peaks do not coincide, but it creates a pressure policy that must be deliberate.

Requests should represent capacity needed for acceptable service under intended load and contention, using distributions, seasonality, startup, failover, and growth. Limits represent a safety or product boundary. Copying observed averages into both produces underprovisioned tails and arbitrary ceilings.

### Control CPU without confusing quota and capacity

CPU is compressible: a constrained process usually waits rather than being killed. A CPU request affects scheduling and normally maps to relative weight during contention. A CPU limit maps to quota over a period; exceeding it causes throttling until quota replenishes.

Quotas protect neighbors but can harm latency-sensitive, multithreaded, or bursty workloads even when the node has idle CPU. Diagnose throttled periods and time, run-queue delay, latency, request rate, parallelism, and node contention together. High CPU utilization without latency harm may be healthy.

Choose among no CPU limit with strong requests and fair weighting, generous ceilings, or strict quotas based on tenant trust and consequence. Untrusted batch workers need a ceiling. A latency-critical internal service may use a request with headroom and no quota on isolated or well-governed nodes. Document the choice rather than imposing one ratio globally.

Cpuset and CPU-manager policies can provide exclusive CPUs for selected workloads, reducing scheduler interference at the cost of fragmentation. NUMA and topology affect memory/device locality. Qualification must test the actual node policy.

### Control memory and OOM consequence

Memory is incompressible at the point of demand: the kernel cannot simply delay every allocation indefinitely. A Kubernetes memory request informs scheduling and can influence cgroup v2 protection depending on runtime configuration. A memory limit becomes a cgroup boundary; exceeding it can trigger reclaim and OOM termination.

Count anonymous memory, page cache, kernel-accounted memory, shared mappings, and memory-backed `emptyDir` behavior according to the platform. A tmpfs write can consume memory, not ephemeral-storage quota. Language heaps may need container-aware configuration and headroom for native allocations, threads, JIT, buffers, and sidecars.

Observe working set and resident memory, limit, reclaim, pressure stall information where available, `memory.events`, OOM kills, restart loops, and application latency. A memory leak and a legitimate working-set increase require different responses. Restarting after every OOM without evidence can amplify load.

Requests protect placement but do not reserve physical pages exclusively. When node memory is scarce, eviction and OOM selection depend on QoS, usage relative to request, priority, kernel behavior, and kubelet policy. Test node pressure, not only isolated limit exceedance.

### Bound PIDs, I/O, and storage

PID limits contain fork bombs and leaks. Count all processes and threads as enforced by the controller/runtime and include sidecars and startup peaks. Hitting the boundary can prevent health checks, shells, or graceful recovery, so report it distinctly.

Block I/O controls can set weights or bandwidth/IOPS ceilings when the storage stack supports them. Shared filesystem, network volume, and device queues may not align cleanly with container cgroups. Observe service latency and queue pressure, not only bytes.

Ephemeral storage includes writable layers, logs, and disk-backed temporary volumes under Kubernetes accounting rules. Set requests and limits, rotate logs, bound scratch, and observe inode as well as byte exhaustion. Node disk pressure can evict workloads. Stateful data belongs in a storage contract with capacity, durability, backup, and recovery—not an unlimited writable layer.

Network bandwidth, connection tables, sockets, DNS, and control-plane API calls also need protection even when not represented by core compute requests. Use network shaping where supported, application concurrency, rate limits, quotas, and admission to constrain externalities.

### Understand QoS, priority, and eviction

Kubernetes derives QoS classes from CPU and memory request/limit patterns. These classes influence eviction and OOM behavior but do not replace application importance or a capacity plan. `Guaranteed` does not mean immune to node failure, eviction, kernel OOM, or throttling; `BestEffort` is unsuitable for critical latency promises.

Priority affects scheduling order and can preempt lower-priority pods. Uncontrolled high priority shifts harm rather than creating capacity. Reserve it for explicit service consequence and combine it with disruption, quota, and admission governance.

Keep node allocatable below physical capacity to reserve resources for the operating system, kubelet, runtime, networking, storage, security, and eviction thresholds. A fully requested node without system reserve can fail its control agents precisely during workload pressure.

### Validate a resource contract

The following synthetic admission check separates requests, limits, and invalid policy. Millicores and mebibytes are teaching units, not a scheduler implementation.

<!-- bijux-verify: {"id":"runtime-resource-contract-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"workloads=5\ncpu_request_m=1900\nmemory_request_mib=2432\nvalid=3\ninvalid=2\nburstable=2\nunbounded_memory=1\nnode_request_feasible=true\n","stderr":""}} -->
```python
workloads = [
    {"name": "api", "cpu_request": 500, "cpu_limit": 1000, "memory_request": 512, "memory_limit": 768},
    {"name": "worker", "cpu_request": 800, "cpu_limit": 1600, "memory_request": 1024, "memory_limit": 2048},
    {"name": "cache", "cpu_request": 300, "cpu_limit": 300, "memory_request": 768, "memory_limit": 768},
    {"name": "bad-cpu", "cpu_request": 200, "cpu_limit": 100, "memory_request": 128, "memory_limit": 256},
    {"name": "bad-memory", "cpu_request": 100, "cpu_limit": 200, "memory_request": 0, "memory_limit": None},
]
def valid(workload):
    cpu_ok = workload["cpu_request"] > 0 and workload["cpu_limit"] >= workload["cpu_request"]
    memory_ok = workload["memory_request"] > 0 and workload["memory_limit"] >= workload["memory_request"]
    return cpu_ok and memory_ok

accepted = [workload for workload in workloads if valid(workload)]
print(f"workloads={len(workloads)}")
print(f"cpu_request_m={sum(workload['cpu_request'] for workload in workloads)}")
print(f"memory_request_mib={sum(workload['memory_request'] for workload in workloads)}")
print(f"valid={len(accepted)}")
print(f"invalid={len(workloads) - len(accepted)}")
print(f"burstable={sum(workload['cpu_limit'] > workload['cpu_request'] for workload in accepted)}")
print(f"unbounded_memory={sum(workload['memory_limit'] is None for workload in workloads)}")
print(f"node_request_feasible={str(sum(w['cpu_request'] for w in workloads) <= 2000 and sum(w['memory_request'] for w in workloads) <= 4096).lower()}")
```

The fixture intentionally counts invalid requests in the raw node-feasibility total and uses a local rule requiring both limits. Real Kubernetes permits patterns this policy rejects, has pod-level and init-container semantics, supports more resource types, and schedules only admitted objects. A production validator must use canonical quantity parsing and current API behavior.

### Select the runtime class

Native OCI runtimes offer broad Linux compatibility and low overhead but share the host kernel. User-namespaced native execution reduces host identity consequence with compatibility costs. A userspace-kernel sandbox intercepts or implements much of the guest syscall interface, reducing direct host-kernel exposure but adding performance and compatibility differences. MicroVMs supply a guest kernel and hardware virtualization boundary with startup, memory, device, observability, and operational cost.

Dedicated nodes reduce co-tenancy and can support host-integrated agents or devices, but they remain shared among workloads placed there unless policy says otherwise. A full virtual machine may be appropriate for kernel modules, legacy assumptions, or stronger tenant separation. Confidential-computing features address specific memory/confidentiality threats; they do not substitute for resource and runtime policy.

Benchmark real system-call, networking, filesystem, startup, memory, accelerator, and observability behavior. Select by threat and workload, not by a universal “more secure” label. A sandbox itself depends on host cgroups and network policy for denial-of-service control and cannot eliminate hardware side channels.

### Enforce at admission and verify at runtime

Define allowed combinations rather than checking fields independently. Reject privileged plus supposedly restrictive profiles, host namespace plus tenant class, unrestricted device plus shared node, or custom seccomp profile absent from the selected nodes. Validate runtime class, image platform, node labels, kernel features, and policy versions together.

Pod Security Standards provide a useful baseline: the Restricted profile requires non-root behavior, disallows privilege escalation, applies seccomp, and constrains capabilities, volumes, and host namespaces. A platform-specific contract should extend this baseline for resources, devices, runtime classes, network, identity, and evidence.

After placement, verify effective runtime state from node/runtime evidence: namespace IDs, UID/GID mappings, capability sets, no-new-privileges, seccomp mode, LSM label, mounts and propagation, devices, cgroup path and controller files, runtime implementation, image digest, and policy revision. Declarative acceptance without effective-state sampling leaves implementation drift invisible.

### Observe failure and interference

Separate signals: admission denial, unschedulable request, image/runtime failure, CPU throttling, memory reclaim, cgroup OOM, node OOM, kubelet eviction, PID limit, storage limit, disk pressure, I/O latency, network policy denial, seccomp denial, LSM denial, and sandbox fault. Each has a different owner and remedy.

Correlate application service levels with resource pressure rather than optimizing utilization alone. Use distributions and co-tenant context. Preserve denied-operation details securely and do not suggest unsafe permission escalation as the first fix.

Test contention deliberately: coincident CPU bursts, memory growth, fork bomb, log flood, I/O saturation, network fan-out, slow termination, and failing runtime hooks. Verify neighbors, node agents, control plane, and recovery remain within objectives.

### Govern exceptions and substrate lifecycle

An exception states workload digest, runtime class, exact control relaxed, required authority, reason, protected assets, compensating controls, node scope, monitoring, expiry, and removal trigger. “Needs privileged” is not sufficient. Reproduce the required operation and search for a narrower capability, device broker, node service, or sandbox.

Patch kernels, runtimes, sandbox implementations, hypervisors, firmware, node images, CNI/CSI components, device plugins, and policy engines through versioned node pools and progressive workload evacuation. Runtime compatibility is part of golden-path versioning.

Emergency response can cordon nodes, block admission, revoke runtime class eligibility, isolate networks, replace credentials, capture evidence, terminate affected workloads, and rebuild nodes. The order depends on active exploitation and service consequence. Restore from governed images rather than attempting to “clean” an uncertain host.

## Definitions and Notation

Let workload runtime contract $R=(T,I,A,F,S,M,C,E,O,X)$ have the components defined in the review. Let namespace topology be graph $I=(P,N,J)$ with processes/containers $P$, namespace instances $N$, and membership or join edges $J$. Sharing is explicit in $J$.

For workload $w$, resource $r$, and time $t$, let $q_{w,r}$ be request, $l_{w,r}$ limit when defined, $d_{w,r}(t)$ unconstrained demand, and $u_{w,r}(t)$ observed use after enforcement. Generally $u_{w,r}(t)\ne d_{w,r}(t)$ under throttling, reclaim, blocking, or denial.

Let $a_{n,r}$ be node allocatable capacity and $W_n$ workloads assigned to node $n$. Request feasibility is $\sum_{w\in W_n}q_{w,r}\le a_{n,r}$ for every scheduled resource. It does not imply $\sum l_{w,r}\le a_{n,r}$ or simultaneous satisfaction of unconstrained demand.

Let effective enforcement evidence at time $t$ be $E_t(R,n)$. Desired contract compliance is predicate $E_t(R,n)\models R$ under a named verifier and supported node model. The notation records an evaluated claim, not formal proof against all kernel or hardware attacks.

## Mechanisms, Invariants, or Proof Structure

The mechanism is threat classification $\rightarrow$ runtime class $\rightarrow$ namespace and identity topology $\rightarrow$ authority/syscall/MAC/filesystem/device controls $\rightarrow$ resource request and enforcement $\rightarrow$ admission $\rightarrow$ node/runtime application $\rightarrow$ effective-state evidence $\rightarrow$ pressure and security observation $\rightarrow$ response, exception removal, or substrate update.

Containment has layers. Namespace separation limits views. Credentials and capabilities limit authority. Seccomp limits kernel entry. LSM policy limits subject-object operations. Mount and device policy limits exposed resources. Cgroups limit and account resource use. Sandboxes or guest kernels alter the shared-kernel assumption. Network and workload identity constrain external interaction.

Invariants are explicit sharing, non-host-root identity, minimum authority, enforced syscall/MAC policy, exceptional host integration, separate scheduling and enforcement semantics, multi-resource pressure observation, effective-state verification, versioned substrate, and expiring exceptions.

No composition proves complete isolation. Controls share kernel, runtime, hardware, and operator dependencies. The threat model and residual risk remain part of the contract.

## Alternatives and Trade-Offs

**Non-root versus user-namespaced root:** non-root is simpler and minimizes application authority. User-namespaced root supports software expecting root while remapping host identity, at the cost of filesystem and feature complexity.

**Runtime-default versus custom seccomp:** defaults provide maintained compatibility and broad reduction. Custom allowlists reduce surface further but require architecture, application, and upgrade lifecycle ownership.

**SELinux versus AppArmor:** both add mandatory access control with different object and policy models and operating-system ecosystems. Standardize per node fleet rather than pretending profiles translate mechanically.

**CPU limits versus request-only CPU:** limits contain hostile or runaway workloads but throttle legitimate bursts. Request-only policies improve burst use but require trust, fair weighting, quotas, and node headroom.

**Tight versus generous memory limits:** tight limits bound blast radius but increase OOM risk. Generous limits allow adaptation but expose neighbors. Application backpressure and graceful degradation matter in both.

**Overcommit versus reservation:** overcommit increases utilization when peaks differ but creates pressure and eviction risk. Reservation improves predictability but can strand capacity. Choose by service objective, correlation, and consequence.

**Shared-kernel versus sandbox/microVM:** native execution maximizes compatibility and efficiency. Stronger runtime boundaries reduce selected attack surfaces but add overhead, incompatibility, new trusted code, and operational complexity.

**Shared versus dedicated nodes:** sharing improves utilization and elasticity. Dedicated pools reduce co-tenancy and support special devices/privilege but increase cost and fragmentation; they still require controls.

**Fail closed versus runtime availability:** blocking on unverifiable policy protects trust but can stop urgent service. Use cached time-bounded decisions, redundant verifiers, explicit emergency authority, and auditable recovery rather than a silent fail-open.

## Failure Modes and Misconceptions

- **“Namespaces are virtual machines.”** They partition selected kernel views while relying on a shared kernel.
- **“Root is harmless inside a container.”** Without user mapping and other controls, it may retain consequential host-scoped authority.
- **“One capability is narrow.”** Capabilities such as `SYS_ADMIN` cover broad operations; analyze scope and alternatives.
- **“Seccomp blocks exploits.”** It removes syscall paths; allowed calls and the filter implementation can still be vulnerable.
- **“Complain mode protects us.”** It observes policy violations but does not deny them.
- **“Read-only root means no writes.”** writable volumes, tmpfs, proc/sys interfaces, devices, and external services remain.
- **“A memory limit reserves memory.”** Requests drive placement; limits bound cgroup use and can trigger OOM.
- **“CPU over limit kills the pod.”** CPU quota normally throttles execution rather than terminating it.
- **“Guaranteed QoS guarantees service.”** Node failures, throttling, eviction conditions, and external dependencies still apply.
- **“Average usage is the request.”** Requests must cover acceptable service at relevant demand and contention, including tails.
- **“A sandbox ends the threat model.”** Host resources, network, hardware, implementation bugs, and availability remain.
- **“Privileged is a debugging switch.”** It changes the workload into a node-level authority with a different blast radius.

## Worked Examples

### Example 1

A web service runs as numeric UID 10001, drops all capabilities, uses `RuntimeDefault` seccomp, prohibits privilege escalation, and has a read-only root. A writable cache mount is capped and non-executable. Effective-state sampling confirms the node applied the contract.

### Example 2

A legacy agent requests `SYS_ADMIN` to mount filesystems. The platform replaces it with a node-scoped mount broker exposing one validated operation; application pods remain unprivileged.

### Example 3

A public code runner passes Pod Security Restricted but executes hostile binaries. Its threat class selects a sandboxed runtime, dedicated identity, strict egress, short-lived storage, and hard multi-resource ceilings beyond the baseline.

### Example 4

A latency-sensitive service shows low average CPU yet severe tail latency. Throttling counters reveal quota exhaustion during bursts. The team raises the request, removes the CPU limit on a governed pool, and keeps concurrency protection.

### Example 5

A Java service stays below heap maximum but is OOM-killed. Native buffers, threads, JIT, and memory-backed scratch exceed the cgroup limit. The runtime contract measures total memory and bounds scratch rather than increasing heap blindly.

### Example 6

A fork bomb reaches a PIDs limit. The application cannot start a diagnostic shell, but the node and neighbors remain healthy. Runtime evidence identifies PID exhaustion rather than misreporting a generic crash.

### Example 7

An AppArmor profile is deployed in complain mode and yields new file accesses after an upgrade. The platform reviews and tests them before enforcing; it does not call the learning period protected.

### Example 8

A GPU workload needs a device plugin and driver surface unavailable in a sandbox. It runs on a dedicated patched pool with device-scoped admission, tenant restrictions, resource quotas, and no general privileged flag.

### Example 9

A sidecar intentionally shares the pod network and process namespace for diagnostics. Admission permits that topology only for an approved pair, while tenant-to-tenant namespace joins remain denied and observable.

### Example 10

A runtime escape advisory affects one node-image release. The platform blocks new placement, inventories runtime class and kernel versions, cordons affected pools, preserves evidence, migrates workloads, rotates node credentials, and rebuilds nodes.

## Cross-Program Connections

Operating systems supplies process credentials, namespaces, system calls, virtual memory, page cache, schedulers, cgroups, filesystems, devices, and OOM behavior. Security supplies threat modeling, least privilege, defense in depth, mandatory access, sandboxing, side channels, and incident containment.

Distributed systems supplies multi-tenancy, noisy-neighbor effects, partial failure, admission, backpressure, and recovery. Performance engineering supplies queues, utilization, percentiles, throttling, capacity models, NUMA, and coordinated peaks. Reliability supplies objectives, graceful degradation, load shedding, eviction, and chaos tests.

Kubernetes engineering supplies requests, limits, QoS, priority, runtime classes, pod security contexts, admission, node pools, and status. Image engineering supplies immutable executables, users, entrypoints, architectures, and provenance. Finance contributes utilization and dedicated-capacity cost, while product management contributes safe defaults and exception journeys.

## References

- Open Container Initiative, [*OCI Runtime Specification: Linux Container Configuration*](https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md), current specification retrieved September 2, 2026. Namespaces, cgroups, devices, resources, sysctls, seccomp, rootfs propagation, Intel RDT, and memory policy.
- Open Container Initiative, [*OCI Runtime Configuration*](https://github.com/opencontainers/runtime-spec/blob/main/config.md), current specification retrieved September 2, 2026. Process identity, capabilities, environment, working directory, terminal, resource limits, mounts, hooks, and annotations.
- Linux Kernel, [*Control Group v2*](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html), current kernel documentation retrieved September 2, 2026. Hierarchy and CPU, memory, I/O, PID, cpuset, pressure, delegation, and controller semantics.
- Linux man-pages, [*namespaces(7)*](https://man7.org/linux/man-pages/man7/namespaces.7.html), release 6.18. Namespace types, isolated resources, APIs, lifetime, and `/proc` representation.
- Linux man-pages, [*capabilities(7)*](https://man7.org/linux/man-pages/man7/capabilities.7.html), release 6.18. Capability meanings, process sets, file capabilities, `execve` transformation, bounding and ambient sets, and namespace interaction.
- Linux man-pages, [*user_namespaces(7)*](https://man7.org/linux/man-pages/man7/user_namespaces.7.html), release 6.18. UID/GID maps, namespace ownership, scoped capabilities, nesting, file access, and associated namespace rules.
- Kubernetes Project, [*Linux Kernel Security Constraints for Pods and Containers*](https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/), current documentation retrieved September 2, 2026. Non-root execution, seccomp, AppArmor, SELinux, capabilities, user namespaces, privileged overrides, and sandbox trade-offs.
- Kubernetes Project, [*Pod Security Standards*](https://kubernetes.io/docs/concepts/security/pod-security-standards/), current documentation retrieved September 2, 2026. Privileged, Baseline, and Restricted controls for host namespaces, privilege, capabilities, seccomp, users, volumes, and sysctls.
- Kubernetes Project, [*Resource Management for Pods and Containers*](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/), current documentation retrieved September 2, 2026. Requests, limits, scheduling, cgroup enforcement, CPU throttling, memory OOM, pod resources, huge pages, and ephemeral storage.
- Kubernetes Project, [*Pod Quality of Service Classes*](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/), current documentation retrieved September 2, 2026. Guaranteed, Burstable, and BestEffort classification and eviction/OOM implications.
- Kubernetes Project, [*Runtime Class*](https://kubernetes.io/docs/concepts/containers/runtime-class/), current documentation retrieved September 2, 2026. Runtime handler selection, scheduling constraints, and pod overhead.
- gVisor, [*Security Model*](https://gvisor.dev/docs/architecture_guide/security/), current documentation retrieved September 2, 2026. System API/ABI attack surfaces, side channels, sandbox host interactions, defense in depth, resource dependence, and compatibility/security trade-offs.

## Exercises

### Exercise 1

Define runtime contracts for an internal API, an internet-facing parser, a public build runner, a GPU inference service, and a node monitoring agent. State threat, class, namespace topology, identity, authority, files/devices, resources, evidence, and exceptions.

### Exercise 2

Audit a pod with root user, `SYS_ADMIN`, host PID/network, writable host path, `Unconfined` seccomp, AppArmor complain mode, no requests, 8-GiB memory limit, no PID limit, and a runtime socket. Explain interactions and propose a durable redesign.

### Exercise 3

Design CPU and memory policy for a latency API, bursty worker, in-memory cache, and untrusted compiler on a 16-core, 64-GiB node pool. Address requests, limits, overcommit, system reserve, cgroup evidence, QoS, pressure, and scaling.

### Exercise 4

Diagnose a cluster where latency rises, some pods are throttled, others are OOM-killed, one is evicted for disk pressure, and nodes report low average utilization. Provide an evidence sequence and separate remedies.

### Exercise 5

Transfer the runtime model to a university service that executes untrusted student code. Include assignment isolation, grading integrity, privacy, resource fairness, language compatibility, debugging, network, storage, escape response, and accessibility.

## Answers to the Exercises

### Answer 1

The internal API uses native runtime, separate workload namespaces, explicit non-root UID, all capabilities dropped, no-new-privileges, runtime-default seccomp, enforced fleet MAC, read-only root, bounded scratch, requests based on service tails, and memory/PID limits. The internet parser adds strict egress and may use a sandbox because hostile input reaches complex native code. The public build runner assumes hostile code: sandbox or microVM, user mapping, no host mounts/devices, ephemeral workspace, narrow dependency egress, hard CPU/memory/PID/I/O/storage/time limits, and disposable identity. GPU inference uses a dedicated patched pool and device-scoped plugin because compatibility may preclude the sandbox; it retains non-root, syscall/MAC, network, quotas, and tenant restrictions. The node monitor is a separate host-integrated class with precise read-only host views or bounded node API, dedicated service identity, node pool admission, and replacement plan for every broad permission. Each contract records effective namespace/cgroup/profile evidence, image and substrate versions, pressure/security events, owner, and expiring exceptions.

### Answer 2

The settings collectively erase the claimed container boundary. Host PID/network exposes node processes and network state; root plus `SYS_ADMIN` supplies broad administrative operations; the writable host path and runtime socket provide direct persistence or host workload control; `Unconfined` disables syscall reduction; complain mode audits but does not deny; absent requests permits unsafe placement and weak contention standing; a memory limit is not reservation; absent PID limit permits fork exhaustion. First remove the runtime socket and replace its use with a narrow authenticated service. Move host monitoring into a dedicated node class with read-only, minimal views. Remove host namespaces and path, run non-root or user-mapped, drop all capabilities, prohibit escalation, enforce runtime-default/custom seccomp and MAC, and use a read-only root. Set measured CPU/memory/storage requests, consequence-based limits, PID/I/O controls, and node reserve. If an irreducible host operation remains, isolate dedicated nodes, constrain exact device/path/API, rotate node identity, observe effective state, and issue a time-bounded exception.

### Answer 3

Reserve explicit capacity for OS, kubelet, runtime, networking, storage, and eviction thresholds before offering allocatable resources. The latency API receives a request covering tail-load concurrency plus headroom and may omit CPU quota on a governed pool while retaining concurrency and memory/PID limits. The worker receives a representative request and higher CPU ceiling because delayed work is acceptable; autoscaling uses queue age and throughput. The cache gets a memory request near its intended resident set and a limit including metadata/fragmentation headroom, with admission/load shedding before OOM; CPU is secondary. The compiler is untrusted and receives hard CPU, memory, PID, I/O, storage, and duration ceilings in a sandbox, even if bursting would improve speed. Model correlated peaks before overcommitting memory; CPU can be overcommitted more safely because throttling is compressible. QoS follows the concrete request/limit pattern rather than being selected by name. Validate with cgroup weight/quota, memory protection/limit/events, throttle time, pressure, OOM, queue, and service latency. Scale nodes or workloads from outcome and saturation evidence, not average utilization alone.

### Answer 4

Start with a common timeline of service latency, demand, deployments, node placement, runtime versions, and pressure. For throttled pods, inspect CPU request/limit, cgroup quota periods and throttled time, run queues, burst concurrency, and co-tenants; raise/remove inappropriate quota or reshape concurrency. For OOM, distinguish cgroup OOM from node OOM, inspect total memory including cache/tmpfs/native allocations, `memory.events`, requests, limits, restart timing, and leaks; fix footprint/backpressure or set justified capacity. For disk eviction, inspect writable layers, logs, `emptyDir`, inodes, ephemeral requests/limits, kubelet thresholds, and image garbage collection; bound and relocate data. Low averages can hide per-node placement, short peaks, upper percentiles, quota throttling on idle nodes, and resource-specific saturation. Do not apply one global limit increase. Correct scheduling, node reserve, autoscaling, application behavior, and storage policy separately, then rerun coincident-load tests and verify neighbor objectives.

### Answer 5

Treat every submission as hostile and each run as disposable. Use one sandbox or microVM boundary per student or submission according to the threat, with separate user/PID/mount/network/IPC/cgroup topology, no host mounts or devices, immutable language toolchain, read-only base, bounded ephemeral workspace, non-host-root mapping, no capabilities, no privilege escalation, enforced syscall/MAC policy, and no outbound network except an assignment-specific allowlist. Cap CPU time, wall time, memory, PIDs, output, files/inodes, I/O, and concurrent jobs; schedule fair requests and queues so one student cannot starve others. Keep hidden tests and grading credentials outside the sandbox through a narrow broker. Protect submissions, outputs, and logs by course/role and retention rules. Provide deterministic toolchains, accessible diagnostics, local rehearsal, language-specific profiles, and a bounded debugging mode with no weaker tenant boundary. On suspected escape, stop placement, isolate nodes, preserve evidence, rotate identities, rebuild hosts, regrade affected work transparently, and follow academic and privacy authority rather than inferring misconduct from a runtime alert alone.
