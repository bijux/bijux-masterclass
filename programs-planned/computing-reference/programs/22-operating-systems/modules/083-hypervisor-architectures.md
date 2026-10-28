---
module_id: OS-083
program: Operating Systems
level: 2
module_number: 83
title: Hypervisor Architectures
status: complete
last_verified: 2026-09-04
---

# Hypervisor Architectures

## One-Page Review

### Governing question

How should a virtualization system divide mechanisms, policies, devices and management across privileged components so that it remains correct, containable and operable?

### Essential definitions

- A **hypervisor architecture** is the placement of virtualization responsibilities and authority across hardware, privileged software, service domains and host processes.
- A **bare-metal hypervisor** starts beneath general-purpose operating systems and may delegate drivers and management to privileged domains.
- A **hosted architecture** uses a host operating system for scheduling, memory, drivers and process isolation while adding a virtualization mechanism and userspace VMM.
- A **root or control partition** is a privileged VM that creates or services other partitions under a smaller hypervisor.
- A **virtual machine monitor process** implements guest-facing machine state, devices and lifecycle around kernel or hardware execution support.
- A **device backend** converts a virtual device protocol into host storage, networking or accelerator operations.
- The **trusted computing base** (TCB) contains components whose failure can violate a stated security property.
- A **failure domain** is the set of workloads and resources one component failure can impair or expose.

### Central model, mechanism, or theorem

Draw the system as an authority graph, not a stack of product names. Nodes are components; edges are capabilities, calls, shared memory, device access and lifecycle control. Assign each responsibility to the narrowest component that has the required mechanism and context. Then verify data paths, control paths, failure containment, synchronization, upgrade and recovery across every edge. “Type 1” or “Type 2” alone does not determine the TCB, attack surface or blast radius.

### Critical invariants

- Each component holds only the authority required for its durable responsibility.
- Guest execution, device emulation and management input cross explicit validation boundaries.
- vCPU, memory, interrupt and device state have one owner during every lifecycle transition.
- Fast paths cannot bypass resource accounting, isolation or revocation.
- A failed per-VM component cannot silently corrupt another VM's resources.
- Shared services expose tenant identity, quotas, ordering and restart semantics.
- Upgrade and migration preserve one versioned machine and control-plane contract.

### Common failures

The architecture treats the host kernel as outside the TCB despite relying on it for isolation, runs a large device model with ambient root authority, shares a backend without tenant-scoped limits, lets two controllers own VM state, blocks all vCPUs on one global lock, or kills a service domain without defining device and DMA recovery.

### Compact example

A per-VM VMM needs one disk image, one network endpoint and a virtualization descriptor. The launcher opens those resources, passes only their descriptors, installs process restrictions and drops privilege. Compromise of that VMM can affect its VM and granted endpoints, but it cannot name another tenant's disk. A single root VMM with directory-wide access creates a larger authority graph even if both use identical CPU virtualization.

### Connections

Hypervisor architecture connects microkernels, operating-system processes, capability security, device drivers, resource schedulers, storage and network backends, distributed control planes, live migration and incident containment.

## Governing Question

CPU virtualization is only one mechanism inside a production VM system. Something must allocate memory, schedule vCPUs, model devices, route interrupts, open disk images, configure networking, expose management APIs, migrate state and recover failures. The governing question is where each responsibility and its authority should live.

## Why This Matters

Two systems can both be described as hardware-assisted hypervisors while having radically different trust and failure boundaries. A minimal bare-metal core may depend on a highly privileged service domain. A hosted design may keep CPU execution in the kernel and devices in one userspace process. A microVM design may deliberately remove machine features and use one confined process per guest. The labels do not replace a component inventory.

Placement decisions affect performance, portability, attack surface, debugging and upgrades. Moving a device backend out of a VMM can contain parser defects, but introduces interprocess protocols and shared-memory revocation. Reusing a host kernel gains mature drivers and scheduling, but includes that kernel in relevant isolation claims. Architecture work must make such dependencies explicit and test the system as deployed.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain trap-and-emulate, hardware-assisted execution, nested translation and interrupt virtualization;
- distinguish mechanism, policy, authority, identity and resource ownership;
- trace storage and network I/O through guest, frontend, backend and physical device;
- reason about threads, processes, address spaces, service domains, IPC and locks;
- describe VM create, run, pause, snapshot, migrate, reset and destroy transitions.

Retrieve the exact hypervisor, host kernel, VMM, device backend, firmware, management service and orchestration versions. Record process credentials, namespaces, mandatory-access-control policy, file descriptors, service-domain permissions, device assignments and network/storage resources. A logical architecture diagram without deployed authority is insufficient evidence.

## Learning Objectives

After completing this module, you should be able to:

1. decompose a virtualization system into execution, memory, interrupt, device, lifecycle and management responsibilities;
2. compare bare-metal, hosted, partitioned and per-VM-process organizations without relying on one-dimensional labels;
3. construct authority, dependency, data-flow and failure-domain graphs;
4. place fast paths and slow paths while preserving validation and revocation;
5. reason about vCPU scheduling, memory ownership, device backends and shared services;
6. minimize and measure the TCB for a stated threat model;
7. design restart, upgrade, migration and degraded-mode behavior across components;
8. validate an architecture through fault injection, isolation tests and end-to-end observability.

## Core Exposition

### Inventory responsibilities before components

List what the system must do: establish CPU state, map memory, inject events, schedule vCPUs, model or assign devices, connect storage and networking, enforce quotas, authenticate operators, persist configuration, migrate machines and collect evidence. Only then assign responsibilities. Starting from existing daemon names hides duplicated or missing ownership.

### Replace the two-type taxonomy with a map

“Bare metal” describes placement relative to a general-purpose host OS; “hosted” describes reuse of one. Neither says where devices, drivers, policy or management live. Some bare-metal systems delegate major functions to a privileged domain. Some hosted systems move critical execution into a kernel module and isolate each VMM process. Use the label as orientation, then draw actual boundaries.

### Separate mechanism from policy

Low-level mechanisms enter guests, map memory, inject interrupts and mediate privileged operations. Policy decides admission, CPU shares, memory limits, feature profiles, device attachment and migration. Keeping policy outside the smallest privileged core can reduce complexity, provided the mechanism validates every request and never assumes the policy component is benign.

### Understand a minimal bare-metal core

A small hypervisor may own processor scheduling, memory isolation, interrupt routing and hypercalls while omitting most physical device drivers. A control or hardware domain runs a general-purpose OS, toolstack and backend drivers. This can shrink the core, but the privileged domain remains in the TCB for properties affected by its authority.

### Understand a hosted kernel/userspace split

In a KVM-style organization, the host kernel supplies process scheduling, memory management, hardware drivers and the vCPU execution interface. A userspace VMM creates VMs, configures memory and devices, handles selected exits and participates in migration. The kernel and VMM are different failure domains, but both may be in the guest-isolation TCB.

### Understand a root-partition organization

A partitioning hypervisor can retain core processor and memory arbitration while a root partition owns hardware drivers and the management stack. Child partitions consume virtual services over an interpartition channel. This resembles service-domain delegation, with vendor-specific authority, lifecycle and device protocols.

### Understand per-VM VMM processes

One userspace process per VM aligns process lifetime, credentials, address space and resource descriptors with a tenant boundary. A minimal microVM VMM can reduce guest-facing device surface and startup state. Isolation still depends on the host kernel, virtualization interface, launcher and resources granted to the process.

### Decide what belongs in the privileged core

Code belongs in the most privileged layer only when correctness, latency or hardware access demands it. Every additional parser, legacy device and management endpoint increases review burden. Conversely, exporting a mechanism through IPC adds state machines, copies and failure cases. Minimize privilege, not merely line count.

### Trace the vCPU execution path

A vCPU commonly maps to a host thread that enters a kernel or hypervisor run loop. Exits may be handled in the privileged core, returned to a userspace VMM or forwarded to a device process. Cross-vCPU requests must be observed even when a vCPU is running, sleeping or transitioning out of guest mode. Kick, request and acknowledgment protocols are architectural, not incidental.

### Define scheduling ownership

A bare-metal scheduler may directly map virtual to physical CPUs; a hosted design composes a guest scheduler, VMM threads and host scheduler. CPU affinity, quotas, overcommit and NUMA placement belong to policy, while preemption and run state belong to mechanisms. Measure ready time separately at each layer to avoid blaming the wrong scheduler.

### Define memory ownership

The lifecycle controller allocates or obtains backing memory; the privileged mechanism enforces guest-physical ownership; the VMM may map memory for emulation; device backends may receive selected shared regions. Every mapping expands authority. Ballooning, dirty logging, confidential memory and migration can change which component may access which page.

### Place interrupt-controller state coherently

Interrupt state may be split between hardware virtualization, kernel acceleration and userspace device models. Assign an authoritative owner for pending, masked, routed and in-service state. Snapshot and restore must reconcile accelerated and software state. Multiple components cannot independently inject the same level or acknowledge one edge.

### Design frontend/backend device paths

A guest frontend places descriptors in shared queues and notifies a backend. The backend validates descriptors, applies tenant identity and performs host I/O. It then publishes completion and signals the guest. The protocol needs bounds, feature negotiation, memory-ordering, reset and revocation semantics across the trust boundary.

### Choose shared or dedicated backends

A dedicated backend limits one process failure to one VM but consumes more resources. A shared backend amortizes caches, connections and threads while making tenant demultiplexing and quotas security-critical. Do not call a backend isolated merely because it is a separate process; inspect all files, devices, memory and peers it can reach.

### Treat device assignment as architectural delegation

Passing a device bypasses much of the software model. The architecture now relies on IOMMU mappings, interrupt remapping, device firmware, reset isolation and lifecycle coordination. The component authorized to attach a device must not retain ambiguous ownership during teardown or migration.

### Keep the control plane off the data path

Management APIs authenticate operators and create desired state. They should not parse every packet or completion. Separate control requests from high-rate guest I/O, but preserve a revocation path: pause, quota change and detach must reach the current resource owner and receive completion evidence.

### Make lifecycle a single-writer state machine

Define legal transitions such as defined, prepared, running, paused, migrating, stopped and destroyed. One controller owns the durable generation. Workers may report observations, but stale workers cannot overwrite newer intent. Idempotency keys and fencing prevent two management instances from acting as simultaneous owners after failover.

### Model IPC as a versioned protocol

Splitting components converts function calls into messages, shared-memory layouts and descriptor passing. Version schemas, validate lengths and identities, bound queues, authenticate peers and specify retry. A local socket is not automatically trustworthy. Shared memory needs publication order and revocation beyond message framing.

### Calculate authority, not process count

For each component, enumerate usable capabilities: guest memory mappings, disk descriptors, network endpoints, device nodes, hypervisor handles, control APIs and credentials. Follow delegation transitively. Ten processes sharing one ambient root credential can have a larger blast radius than one tightly confined process.

### Define the TCB per property

There is no context-free TCB. Guest-to-guest memory confidentiality may depend on CPU, firmware, hypervisor and host kernel. Disk confidentiality also includes storage backends and key services. Availability includes schedulers and control planes. State the property, adversary and deployment before claiming a “small TCB.”

### Apply defense in depth around VMMs

Run VMM and backend processes without ambient root, pass pre-opened resources, restrict system calls, isolate namespaces, apply mandatory access control and remove unused device models. These layers reduce consequence after a guest-facing parser defect. They do not correct a broken kernel isolation mechanism.

### Bound shared-resource contention

Global locks, event loops, work queues, memory allocators and storage connections can couple tenants. Partition hot locks and queues where semantics permit. Apply per-tenant admission and backpressure before shared capacity is exhausted. A shared service must avoid head-of-line blocking and unbounded recovery work.

### Plan component failure and restart

For each process or domain, ask what state is lost, who detects failure, whether a VM can continue, how I/O is fenced and how identity is retained. Restartable device backends need reconstructable queue and feature state or a guest-visible reset protocol. Restarting blindly can duplicate writes or complete stale requests.

### Design observability across boundaries

Correlate VM, vCPU, queue, device, backend, lifecycle generation and host resource identities. Export queue depth, exit reason, ready delay, IPC latency, backend service time, drops and restart counters at their owners. Clock and sampling differences must be recorded before forming end-to-end latency.

### Upgrade by compatibility edge

Rolling upgrades create mixed versions across management, VMM, kernel and backend protocols. Define supported version pairs and downgrade behavior. Machine types and feature profiles preserve guest-visible compatibility; IPC negotiation preserves component compatibility. “Same release train” is not a protocol.

### Treat migration as distributed ownership transfer

Source, destination, storage, network and control plane coordinate a change of owner. Memory and device state must converge while the source remains authoritative, then a fenced switchover transfers authority exactly once. Backend and hardware placement constrain which architectures can migrate a VM without semantic loss.

### Compose nested virtualization explicitly

Nested systems add an L1 guest hypervisor and its device or management components. Identify which exits, translations and virtual devices L0 implements for L1 versus L2. Host resource policy remains with L0 even when L1 presents a complete hypervisor abstraction to its guest.

### Test architecture, not only guest function

Boot tests show little about containment. Crash VMMs, backends, control-plane leaders and service domains during I/O, migration and reset. Saturate shared queues, replay stale generations, revoke descriptors, inject malformed IPC and verify cross-tenant noninterference. Measure recovery-point and recovery-time behavior.

### Record residual coupling

Shared host kernels, last-level caches, memory bandwidth, IOMMUs, firmware, physical devices and control planes remain coupling points even after process separation. Document what can cause confidentiality loss, integrity loss, noisy-neighbor degradation or correlated outage. Architecture is credible when those dependencies are visible.

## Definitions and Notation

Model components as a directed authority graph $G=(C,E)$. Edge $(a,b,r)$ means component $a$ can exercise resource or operation $r$ over $b$. If $R(c)$ is the set reachable from $c$, an approximate compromise blast radius is

$$
B(c)=\bigcup_{x\in R(c)} resources(x).
$$

Reachability is conservative: actual exploitation may require conditions, but missing an authority edge understates risk.

Let a request path traverse components $c_1,\ldots,c_n$. Observed latency is

$$
L=\sum_{i=1}^{n}S_i+\sum_{i=1}^{n-1}Q_i+\sum_{i=1}^{n-1}X_i,
$$

where $S_i$ is service time, $Q_i$ is waiting before the next owner and $X_i$ is boundary-crossing cost. Parallel work and batching require a richer model.

For shared component $j$ with arrival rate $\lambda_j$, mean demand $s_j$ and effective parallelism $m_j$, nominal utilization is

$$
\rho_j=\frac{\lambda_j s_j}{m_j}.
$$

Stability requires capacity beyond mean load; burst, service distribution and downstream backpressure determine the operational margin.

Let lifecycle generation be $g$. A command or completion labeled $g'$ may mutate durable VM state only if $g'=g$ and the sender holds the current fencing authority.

## Mechanisms, Invariants, or Proof Structure

Review a hypervisor architecture with these obligations.

1. **Responsibility obligation:** CPU, memory, interrupt, device, policy and lifecycle responsibilities each have an owner.
2. **Authority obligation:** every component capability is enumerated, justified, bounded and revocable.
3. **Validation obligation:** guest and management inputs are checked at the component that exercises privileged effect.
4. **State obligation:** vCPU, memory, interrupt, device and lifecycle state have one authoritative generation.
5. **Scheduling obligation:** composed schedulers expose admission, accounting, ready delay and progress behavior.
6. **Data-path obligation:** every queue, mapping, copy, backend and physical endpoint preserves tenant identity and bounds.
7. **Containment obligation:** process or domain failure has a tested and documented blast radius.
8. **Recovery obligation:** fencing, restart, reset and degraded-mode behavior prevent replay and ambiguous ownership.
9. **Compatibility obligation:** guest machine, management API and internal protocol versions evolve explicitly.
10. **Migration obligation:** source-to-destination authority transfers exactly once with coherent device and time state.
11. **Observability obligation:** identities, clocks, losses and metrics join across every architectural boundary.
12. **Assurance obligation:** TCB and security claims name the property, adversary, deployment and residual coupling.

The architecture argument starts from a responsibility map, overlays authority and data flow, then proves single ownership and validation at every privileged effect. Failure analysis removes each component and checks containment plus recovery. Performance analysis follows actual crossings and shared capacity. These arguments are related but not interchangeable.

## Alternatives and Trade-Offs

- **Bare-metal versus hosted core:** bare-metal designs control the machine directly; hosted designs reuse mature kernel services and their TCB.
- **Minimal core versus integrated core:** minimality reduces privileged code; integration avoids crossings and duplicated protocols.
- **Service domain versus host process:** domains add a VM boundary; processes reuse host isolation and tooling.
- **One VMM per VM versus shared VMM:** per-VM processes align failure domains; sharing amortizes state and enlarges coupling.
- **In-kernel versus userspace emulation:** kernel paths reduce exits; userspace narrows kernel attack surface and eases tooling.
- **Dedicated versus shared backend:** dedication contains faults; sharing improves utilization and demands tenant-safe multiplexing.
- **Emulation versus assignment:** emulation preserves portability; assignment improves data paths and complicates lifecycle.
- **Synchronous versus asynchronous IPC:** synchronous calls simplify causality; asynchronous queues improve throughput and expand state.
- **Copy versus shared memory:** copies simplify ownership; sharing saves bandwidth and needs careful revocation.
- **Central scheduler versus host scheduling:** central control sees VM policy; host scheduling composes with all system work.
- **Static partitioning versus overcommit:** static allocation improves predictability; overcommit improves utilization and coupling.
- **Rich machine model versus microVM:** richness supports legacy guests; minimal models reduce startup and attack surface.
- **Central control plane versus per-host autonomy:** centralization coordinates policy; local autonomy improves failure tolerance.
- **Restart versus fail-stop VM:** restart preserves service if state reconstructs; fail-stop avoids uncertain replay.
- **Host passthrough versus versioned profile:** passthrough exposes capability; profiles preserve compatibility.
- **Operational convenience versus least authority:** ambient access eases setup; descriptor-based grants reduce compromise impact.

## Failure Modes and Misconceptions

- “Type 1 means small TCB.” Privileged domains, drivers and firmware may dominate the property.
- “Type 2 means weak isolation.” Actual kernel, process and device boundaries decide it.
- “The hypervisor is one binary.” Production systems include kernels, VMMs, backends and control planes.
- “Code outside the core is untrusted and harmless.” Its granted authority may place it in the TCB.
- “More processes always improve security.” Shared credentials can preserve the same blast radius.
- “A small line count proves assurance.” Interfaces, privileges and verification matter.
- “Mechanism can trust policy.” The privileged effect must validate policy requests.
- “One vCPU equals one physical CPU.” Host scheduling and overcommit intervene.
- “A vCPU kick guarantees acknowledgment.” Request visibility and completion need a protocol.
- “Memory belongs only to the VM.” VMMs and backends may map it.
- “Interrupt state is naturally centralized.” Hardware, kernel and userspace can each hold pieces.
- “A separate backend is tenant-isolated.” Inspect all resources it can reach.
- “Shared memory removes IPC cost.” It replaces copies with ordering and revocation work.
- “Device assignment removes the backend.” IOMMU, firmware, reset and lifecycle components remain.
- “The management API is off-path, so it is low risk.” It can grant every resource.
- “Two controllers increase availability.” Without fencing they create split ownership.
- “A local socket authenticates intent.” Peer identity and message authorization still matter.
- “Root is required to open devices.” A launcher can pass narrow descriptors then drop privilege.
- “A global lock is safe because operations are short.” Exit storms and blocking backends amplify it.
- “Restarting a backend is transparent.” Queue state and completed writes may be lost or replayed.
- “Per-component dashboards show end-to-end behavior.” Identities and clocks must join.
- “Rolling upgrades are safe inside one product.” Mixed internal protocols still need compatibility.
- “Migration is a VMM copy.” Storage, network, devices and authority participate.
- “Confidential guests remove the host TCB.” They alter which properties depend on which host components.
- “Boot and benchmark tests validate containment.” Failure and adversarial tests are required.

## Worked Examples

### Example 1

A bare-metal hypervisor schedules vCPUs and protects memory, while a hardware domain owns NIC and storage drivers. For guest-memory isolation the hypervisor is central; for disk confidentiality the hardware domain and backend also enter the TCB. Calling only the hypervisor “trusted” misstates the property.

### Example 2

The following executable toy computes transitive leaf-resource reachability for three components. It demonstrates authority-graph accounting only, not exploitability or a complete TCB analysis.

<!-- bijux-verify: {"id":"hypervisor-authority-reachability","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"vmm_a=disk_a,guest_a_memory,kvm_fd\nshared_backend=disk_a,disk_b\ncontrol_plane=disk_a,disk_b,guest_a_memory,guest_b_memory,kvm_fd\n","stderr":""}} -->
```python
authority = {
    "vmm_a": {"guest_a_memory", "disk_a", "kvm_fd"},
    "vmm_b": {"guest_b_memory", "disk_b", "kvm_fd"},
    "shared_backend": {"disk_a", "disk_b"},
    "control_plane": {"vmm_a", "vmm_b"},
}

def leaf_resources(component, seen=None):
    seen = set() if seen is None else seen
    if component in seen:
        return set()
    seen.add(component)
    leaves = set()
    for target in authority.get(component, set()):
        if target in authority:
            leaves |= leaf_resources(target, seen)
        else:
            leaves.add(target)
    return leaves

for component in ("vmm_a", "shared_backend", "control_plane"):
    print(f"{component}={','.join(sorted(leaf_resources(component)))}")
```

### Example 3

A hosted VMM handles MMIO in its vCPU thread. A slow disk control operation blocks that thread, preventing guest progress unrelated to disk data. Moving blocking work to an I/O thread preserves vCPU execution but requires ordered completion and reset synchronization.

### Example 4

A control-plane leader fails after destination activation but before recording migration success. The new leader sees fenced source generation 41 and active destination generation 42, so it adopts destination ownership rather than replaying switchover. A boolean `migrating` flag would not settle authority.

### Example 5

A shared network backend accepts descriptors from 500 guests. One guest fills the global completion queue. Per-tenant ingress limits alone do not help; completion capacity, scheduler shares and memory must also preserve tenant identity and backpressure.

### Example 6

A per-VM VMM is compromised through a legacy device parser. Its process has only that VM's memory, disk descriptor, TAP descriptor and virtualization handle under syscall and namespace restrictions. The breach remains serious but lacks ambient access to peer images or management credentials.

### Example 7

A service domain restarts during outstanding block writes. Requests carry durable identifiers and the backend journal records which reached stable storage. The new backend completes or retries by protocol. Without this state, transparent restart risks duplicate or falsely acknowledged writes.

### Example 8

Exit time is low, but p99 I/O latency grows. Correlated tracing shows requests wait in an overloaded userspace backend before host submission. Optimizing the kernel entry path cannot repair shared-backend utilization near one.

### Example 9

A VMM upgrade can read the old machine type but emits a new interrupt-controller state field. Migration to an older destination is therefore not symmetric. The compatibility matrix permits old-to-new movement and blocks the reverse unless state is representable.

### Example 10

A static partitioning deployment gives each safety workload dedicated CPUs and devices, while a management VM owns updates. This removes runtime overcommit but not management authority, firmware coupling or shared memory-controller contention; the residual graph remains documented.

## Cross-Program Connections

- **Software architecture:** responsibility boundaries, interfaces, ownership and dependency direction shape the system.
- **Security engineering:** capabilities, TCBs, least privilege, defense in depth and blast radius define containment.
- **Distributed systems:** fencing, generations, retries, leader failover and migration govern control-plane correctness.
- **Performance engineering:** crossings, queues, utilization, locks, NUMA and batching explain overhead.
- **Network engineering:** frontend/backend queues, virtual switches, TAP endpoints and rate limits form guest connectivity.
- **Storage engineering:** image ownership, caching, stable completion, snapshots and shared backends define durability.
- **Platform engineering:** host pools, launchers, policies, machine profiles, upgrades and observability operate the fleet.
- **Reliability engineering:** fault injection, restart protocols, degraded modes and recovery objectives test architecture.
- **API and service engineering:** versioned IPC, authentication, idempotency and backpressure govern component edges.
- **Systems engineering:** hardware, firmware, kernels, domains, processes and operators contribute to end-to-end claims.

## References

1. Linux Kernel Documentation, [KVM API](https://docs.kernel.org/virt/kvm/api.html), kernel/userspace VM construction, vCPU execution, memory, devices and exit interfaces; retrieved 2026-09-04.
2. Linux Kernel Documentation, [KVM Lock Overview](https://docs.kernel.org/virt/kvm/locking.html), lock ordering, SRCU boundaries and virtualization concurrency; retrieved 2026-09-04.
3. Linux Kernel Documentation, [KVM vCPU Requests](https://docs.kernel.org/virt/kvm/vcpu-requests.html), request publication, guest-mode transitions, kicks and acknowledgments; retrieved 2026-09-04.
4. QEMU Project, [System Emulation Introduction](https://qemu.readthedocs.io/en/master/system/introduction.html), accelerators, machine models, devices, offloaded backends and passthrough; retrieved 2026-09-04.
5. QEMU Project, [Security](https://qemu.readthedocs.io/en/master/system/security.html), guest isolation, least privilege, attack surface and process confinement; retrieved 2026-09-04.
6. QEMU Project, [Multi-process QEMU](https://qemu.readthedocs.io/en/master/system/multi-process.html), orchestrated remote device processes, proxy devices and shared memory; retrieved 2026-09-04.
7. Xen Project, [Introduction](https://xenbits.xenproject.org/docs/latest/admin-guide/introduction.html), bare-metal hypervisor, domains, control and hardware domains, hypercalls and delegated devices; retrieved 2026-09-04.
8. Xen Project, [Hyperlaunch Design](https://xenbits.xenproject.org/docs/unstable/designs/launch/hyperlaunch.html), static and dynamic launch, disaggregation, boot domains and constrained roles; retrieved 2026-09-04.
9. Microsoft, [Hyper-V Architecture](https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-architecture), root and child partitions, VMBus, service providers and virtual devices; retrieved 2026-09-04.
10. Firecracker Project, [Firecracker Design](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md), per-microVM process organization, vCPU and VMM threads, minimal devices and layered containment; retrieved 2026-09-04.

## Exercises

### Exercise 1

Compare the relevant guest-isolation TCB of a hosted kernel/userspace design with a minimal bare-metal hypervisor plus fully privileged hardware domain. Do not rank them by label.

### Exercise 2

A shared block backend can access every tenant image and accepts unauthenticated local IPC from all VMMs. Redesign its authority and request boundary.

### Exercise 3

For a path with service times $3$, $8$ and $12\ \mu s$, queue waits $5$ and $20\ \mu s$, and two crossings of $2\ \mu s$ each, compute observed latency under the serial model and state one limitation.

### Exercise 4

A backend receives $180{,}000$ requests/s, has mean service demand $8\ \mu s$ and two equivalent workers. Compute nominal utilization and interpret the result.

### Exercise 5

Design a fault-injection test for a per-VM device backend crash during live migration, including the invariants and evidence needed.

## Answers to the Exercises

### Answer 1

For the hosted design, relevant components can include CPU and firmware, the host kernel and virtualization module, the per-VM VMM, any device backends, launcher policy and resources involved in the asserted property. Process confinement can narrow what VMM compromise reaches, but the host kernel remains trusted for process and guest memory isolation.

For the bare-metal design, the core hypervisor may contain less code and directly enforce CPU and memory separation. A fully privileged hardware domain still enters the TCB for guest properties affected by its mappings, devices, backends and management rights. Compare actual capabilities, validation and residual shared hardware; neither topology wins from “hosted” or “bare metal” alone.

### Answer 2

Give each request an authenticated VM identity derived from the connection or passed capability, never an untrusted image path. A launcher or storage authority opens the tenant's image and passes a narrow descriptor or issues an unforgeable volume handle. The backend enforces operation, byte, queue and bandwidth limits per tenant and cannot traverse a directory of peer images.

Partition workers or processes where stronger failure containment is required. Version and bound IPC; validate offsets, lengths and ordering; fence stale VM generations; expose per-tenant backpressure; and revoke descriptors only after outstanding I/O reaches a defined completion state.

### Answer 3

Under the serial model,

$$
L=(3+8+12)+(5+20)+(2+2)=52\ \mu s.
$$

The model assumes serial contributions. It does not represent batching, parallel device work, overlap, clock uncertainty or work omitted outside the three components.

### Answer 4

The nominal utilization is

$$
\rho=\frac{(180{,}000)(8\times10^{-6})}{2}=0.72.
$$

Each equivalent worker is 72 percent utilized under balanced mean load. That is not a tail-latency guarantee: burstiness, unequal dispatch, service-time variance, downstream stalls and per-tenant head-of-line blocking determine the needed margin.

### Answer 5

Start migration while the source backend has identified outstanding reads and writes. Crash it before a selected stable write completes, while recording lifecycle generation and storage acknowledgment. Verify that fencing prevents a replacement source backend and destination from both owning the queue, no write is falsely acknowledged or applied twice, and cross-VM backends continue within their objectives.

Exercise both a reconstructable restart path and a fail-stop VM path. Evidence includes request identifiers, stable-storage decisions, queue generations, source/destination fencing, backend process identity, guest completions, disk contents, control-plane decisions, recovery time and peer-tenant metrics. Repeat at pre-submit, submitted, completed and guest-notified boundaries.
