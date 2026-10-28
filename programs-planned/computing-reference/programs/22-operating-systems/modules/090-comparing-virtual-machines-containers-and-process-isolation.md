---
module_id: OS-090
program: Operating Systems
level: 2
module_number: 90
title: Comparing Virtual Machines, Containers, and Process Isolation
status: complete
last_verified: 2026-09-04
---

# Comparing Virtual Machines, Containers, and Process Isolation

## One-Page Review

### Governing question

Which isolation boundary should run a workload when security, compatibility, density, startup, performance and operational ownership pull in different directions?

### Essential definitions

- **Process isolation** uses address spaces, credentials, descriptors and ordinary operating-system policy between processes on one kernel view.
- A **container** packages a process tree with selected namespaces, cgroups, mounts, capabilities, syscall policy and metadata while sharing the host kernel.
- A **virtual machine**, or **VM**, runs a guest operating system against virtual hardware implemented by a hypervisor or virtual-machine monitor.
- A **microVM** retains a hardware-virtualization boundary while minimizing boot path, device model and per-instance overhead.
- An **application-kernel sandbox** intercepts a workload's system API and implements much of it outside the host kernel's normal syscall path.
- The **trusted computing base**, or **TCB**, is the hardware, firmware and software whose correct behavior the isolation claim requires.
- A **trust boundary** is an interface across which hostile input must not gain unauthorized authority.

### Central model, mechanism, or theorem

Isolation is an attack-path argument, not a product category. Compare where workload instructions run, which kernel parses their requests, what interface crosses the boundary, which host helpers and devices remain reachable, and how resources and data are shared. Containers reduce and partition one kernel interface; VMs interpose a guest kernel and virtual hardware; application kernels interpose another system-call implementation. Each still depends on host control-plane, storage, network and hardware policy.

### Critical invariants

- The workload's threat model and required interfaces are explicit before selecting a boundary.
- Every tenant separation claim names the shared kernel, hypervisor, device backends, control plane and hardware in its TCB.
- Direct device, filesystem, network and management paths do not bypass the chosen boundary.
- Resource accounting covers guest or sandbox processes plus host-side helpers and kernel work.
- Images, kernels, firmware, runtimes and policies are independently verified and patched.
- Failure, snapshot, migration, teardown and forensic identity remain attributable across layers.
- Performance or density measurements use equivalent workloads and include steady-state as well as transition costs.

### Common failures

Teams call namespaces a security boundary without hardening the kernel surface, call every VM stronger despite a large device model, count guest memory but omit VMM helpers, pass through a device that bypasses mediation, group hostile tenants inside one sandbox for density, compare warm containers with cold VMs, or let shared volumes and control-plane credentials collapse otherwise sound isolation.

### Compact example

A trusted internal API may run in a hardened container for fast scaling. Untrusted customer code may justify one application-kernel sandbox or microVM per tenant. A legacy appliance needing its own kernel and device assumptions fits a conventional VM. These are threat-model decisions: the same container inside a dedicated VM can combine fleet packaging with a separate guest-kernel boundary.

### Connections

Isolation choice connects CPU virtualization, namespaces, cgroups, seccomp, device emulation, container orchestration, supply-chain integrity, capacity planning, side channels, incident response and platform economics.

## Governing Question

No isolation mechanism simultaneously maximizes compatibility, density, startup speed, performance, simplicity and resistance to escape. The governing question is which boundary makes the workload's likely attack paths narrow enough while leaving an operable system whose cost and failure modes are understood.

## Why This Matters

Architecture diagrams often place “container” and “VM” in separate boxes, then infer security from the boxes. Real deployments nest them, attach host volumes, accelerate I/O, share kernels, run privileged agents and delegate control-plane credentials. Those choices determine the boundary more than the packaging format does.

Selection also changes organizational work. Containers concentrate kernel patching in the host fleet and application compatibility around one kernel ABI. VMs add guest kernels, images and virtual devices. MicroVMs minimize some of that surface but retain guest lifecycle. Application-kernel sandboxes add a compatibility implementation that must be tested against workloads. The complete cost includes assurance and operations.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain process address spaces, credentials, namespaces, cgroups and syscall filtering;
- describe trap-and-emulate, hardware-assisted virtualization, VMMs and virtual devices;
- distinguish guest, host, control-plane, data-plane and hardware trust;
- reason about device passthrough, shared storage, networks and side channels;
- compare latency distributions, memory overhead, density, startup and recovery.

Retrieve the exact host and guest kernels, hypervisor or sandbox runtime, firmware and microcode, enabled mitigations, device model and backends, passthrough configuration, namespace and cgroup policy, workload grouping, container and VM images, management agents, storage and network attachments, patch cadence, startup path and representative benchmark method.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish process, container, application-kernel, VM and microVM isolation mechanisms;
2. draw the TCB and attacker-controlled interfaces for each deployed configuration;
3. compare shared-kernel syscall exposure with guest-kernel and virtual-device exposure;
4. reason about compatibility, kernel choice, device access and operational lifecycle;
5. quantify memory, startup, throughput and density with honest denominators;
6. identify boundary bypasses through helpers, passthrough, volumes, networks and control planes;
7. choose nested and tenant-grouping strategies from a stated threat model;
8. validate isolation and performance claims through adversarial and failure testing.

## Core Exposition

### Begin with the attacker and protected assets

Specify whether code is trusted, merely buggy, supply-chain-exposed or actively hostile. Name secrets, tenant data, host availability, control-plane authority and physical confidentiality to protect. A boundary appropriate for mutually trusted services may be inadequate for arbitrary multi-tenant code.

### Use process isolation as the baseline

Separate processes receive virtual address spaces, credentials and descriptor tables, while ordinary permissions and LSMs govern objects. They usually share broader host namespace views and the entire host syscall ABI. This is efficient and often sufficient within one trust domain, but compromise reaches whatever the process's credentials and handles permit.

### Treat a container as a composition

Linux provides no single container kernel object. A runtime composes namespace memberships, cgroup placement, a mount tree, capabilities, seccomp, LSM labels, descriptors and a process lifecycle. OCI supplies configuration and lifecycle conventions. The strength of a container boundary is the exact composition, not image packaging.

### Understand the shared-kernel consequence

Container workload syscalls are serviced by the host kernel. Namespaces change views, cgroups govern resources and filters reduce reachable entry points, but allowed host-kernel code remains in the attack path. Kernel compromise can cross every container boundary on that host unless another layer intervenes.

### Do not undervalue hardened containers

A nonroot container with narrow user mappings, minimal capabilities, read-only mounts, restrictive seccomp and LSM policy, bounded resources and no host handles can expose far less authority than a default privileged container. Fast startup and shared caches enable fine-grained instances. Security comparison must use actual configurations.

### Model a VM as guest kernel plus virtual hardware

A guest application calls its guest kernel. Privileged guest activity encounters hardware virtualization, and I/O reaches virtual devices or passthrough paths handled by the VMM, host kernel and backends. The guest can choose its kernel and userspace independently, but the new kernel, firmware and devices become lifecycle and attack surfaces.

### Locate the VM boundary precisely

Hardware-assisted CPU and memory translation separate guest execution, but exits and device operations cross into KVM, a VMM or host backends. The host management API and storage files sit outside the guest boundary. A VM escape can target hypervisor, device emulation, accelerator or host-kernel code actually exposed by its configuration.

### Treat device models as attack surface

Full machine emulation improves compatibility with operating systems and devices but parses hostile guest inputs. Paravirtual devices reduce overhead and may narrow legacy emulation, yet their host backends remain privileged interfaces. Remove unused devices and sandbox backend processes where supported.

### Evaluate passthrough as a boundary change

Direct device assignment can improve latency and throughput by bypassing emulation. Isolation then depends on IOMMU configuration, device firmware, reset behavior, interrupt routing and peer-to-peer DMA controls. Passthrough is not merely a performance flag; it replaces one mediated interface with another trust chain.

### Understand microVM design

A microVM uses hardware virtualization and a guest kernel but minimizes machine model, devices and boot work for workload isolation and rapid creation. Firecracker, for example, combines KVM with a deliberately small Virtio-oriented device set and a jailed VMM process. “Micro” describes scope and overhead, not a different CPU protection primitive.

### Keep the VMM process sandboxed

The VMM accepts hostile exits and device requests. Run it with least privilege, namespaces, cgroups, syscall filtering and tightly provisioned files and network endpoints. A VM boundary does not justify leaving the host-side monitor or device backend unrestricted.

### Understand application-kernel interposition

An application-kernel sandbox such as gVisor implements much of the Linux system API in a separate Sentry rather than forwarding workload syscalls directly to the host kernel. The Sentry uses a restricted host interface and may use syscall or hardware mechanisms for interception. This changes both attack surface and compatibility.

### Price system-call compatibility explicitly

Containers normally expose the host kernel's Linux ABI, subject to policy. VMs expose whatever the guest kernel implements. Application kernels must reimplement expected semantics, so obscure ioctls, filesystems, networking behavior or newer syscalls may differ or be absent. Run real conformance and application tests rather than equating “Linux-compatible” with identical.

### Recognize nested designs

Containers can run inside VMs or microVMs, and a pod can run inside an application-kernel sandbox. The inner container still supplies packaging, namespaces and resource subdivision; the outer boundary changes which kernel or device interface faces the host. Draw both layers and avoid double-counting one control as two independent protections.

### Choose the unit of isolation

One VM or sandbox may contain a process, container, pod or many services. Sharing amortizes memory and startup, but compromise can reach co-residents inside the same boundary. Align one isolation unit with one mutually trusted principal or document why grouping and internal controls are acceptable.

### Separate root privilege by layer

Root inside a user namespace, guest VM, application kernel and host are different principals. Guest root can fully attack its guest kernel and virtual devices while lacking direct host-root authority. Container root without user mapping can be more dangerous. Always name the governing layer.

### Compare kernel customization

VMs and microVMs can boot a guest kernel with workload-specific configuration, modules and patch timing. Containers inherit the host kernel and cannot require an incompatible kernel ABI. Guest choice improves compatibility or specialization while multiplying kernel inventory and update responsibility.

### Compare memory accounting honestly

Processes and containers can share host kernel, page-cache and library pages. VMs add guest-kernel memory, guest page cache, VMM state and virtual-device buffers; application kernels add their own metadata and caches. Deduplication and ballooning change results. Measure resident and committed host memory for the complete isolation unit.

### Model density as a capacity bound

If host-available memory is $H$ and each isolated workload consumes working-set $w$ plus boundary overhead $o$, a simple packing bound is $\lfloor H/(w+o)\rfloor$. It ignores sharing, fragmentation, overcommit and reservations, but forces comparisons to name overhead rather than cite container count alone.

### Compare startup as a staged path

Container startup may include image fetch, snapshot preparation, namespace construction and process initialization. VM startup adds VMM creation, virtual hardware, guest-kernel boot and guest service startup; snapshots can skip some work. Compare cold, warm and restored paths separately and include readiness, not just process creation.

### Compare steady-state transitions

Containers use ordinary syscalls into the host. VMs can execute many guest-kernel operations without exits but pay for selected exits, emulated I/O and duplicated kernel work. Application kernels intercept syscalls and may translate them into host operations. Workload shape determines which path wins; no mechanism has universal overhead.

### Treat cgroups as host resource governance

Containers, VMM processes and application-kernel sandboxes all need host cgroups. Guest-internal limits do not constrain host-side VMM, backend or kernel resources by themselves. Account for vCPU threads, I/O helpers and kernel work, and coordinate guest scheduling with host quotas and affinity.

### Keep availability separate from escape resistance

A guest that cannot escape may still exhaust assigned and shared host resources through exit storms, dirty-page pressure, I/O queues or control-plane requests. A shared-kernel container can be securely permissioned yet cause contention through allowed operations. Resource limits and admission are distinct evidence tracks.

### Include storage and network paths in the boundary

Host bind mounts, shared volumes, metadata endpoints, virtual block files, network bridges and agents can expose data across otherwise separate compute boundaries. Authenticate workload identity at these services and apply least privilege. Isolation of CPU execution does not isolate a deliberately shared datastore.

### Include the control plane in the TCB

A runtime socket, hypervisor API, orchestration credential or image pipeline may create privileged workloads or attach host resources. Compromise before launch bypasses the runtime boundary entirely. Separate tenant data plane from management authority and audit every boundary-changing operation.

### Consider hardware side channels independently

Containers, application kernels and VMs can share cores, caches, memory controllers and accelerators. Hardware virtualization does not automatically remove timing, speculative-execution or shared-resource channels. Apply current microcode, kernel and scheduler mitigations and decide whether high-risk principals need physical or core separation.

### Understand confidential-VM scope

Memory-encryption and confidential-computing technologies can reduce trust in host software for selected guest state. Their attestation, device, availability, metadata and side-channel scopes are technology-specific. They do not make guest code trustworthy or remove the need for authenticated storage and network services.

### Compare patch responsibility

Container hosts need rapid host-kernel and runtime updates because many workloads share them. VM fleets must patch hypervisor, VMM, host kernel, firmware and each guest kernel. Application-kernel sandboxes add their implementation. Inventory ownership, rollout time and rollback—not only component count.

### Design observability across layers

Container telemetry can use host PIDs, cgroups and namespaces. VM debugging crosses guest agents, virtual consoles, VMM metrics and host events. Application kernels may expose their own procfs and tracing semantics. Correlate one durable workload identity through inner and outer layers without granting tenant access to host diagnostics.

### Plan snapshots and migration by state boundary

VM snapshots may contain CPU, memory and device state but not every external disk or network dependency. Container checkpointing must capture processes, namespaces, mounts and connections. Application-kernel state adds implementation-specific data. Encrypt, authenticate and version snapshot artifacts; restore tests must reconcile external services.

### Test escape paths and boundary bypasses

Fuzz allowed syscalls or virtual devices, probe namespace and capability leaks, stress resources, attack metadata and runtime APIs, vary malformed storage and network input, and test teardown. Use independent security testing appropriate to the mechanism. Absence of a known escape is not a proof of nonexistence.

### Choose with a decision record

Record principals, assets, acceptable shared TCB, required ABI and devices, performance targets, density assumptions, recovery objectives and evidence. State why alternatives were rejected and what change would reopen the decision. Product names and default settings are not durable architectural reasoning.

## Definitions and Notation

Represent a deployed isolation design as

$$
D=(P,B,I,T,R,E),
$$

where $P$ is the protected-principal partition, $B$ boundary mechanism, $I$ exposed interface, $T$ trusted computing base, $R$ resource policy and $E$ evidence. Two deployments using the same runtime can have different $D$ because devices, grouping or host services differ.

Let attack paths from workload $w$ to protected asset $z$ form set $\Pi(w,z)$. A defense claim must show that each path contains an enforced boundary whose assumptions hold:

$$
\forall \pi\in\Pi(w,z),\quad \exists b\in\pi:\ enforced(b)\land assumptions(b).
$$

This is a review obligation, not a proof that all real attack paths have been enumerated.

For available host memory $H$, workload working set $w$ and per-boundary overhead $o$, define the idealized packing bound

$$
N=\left\lfloor\frac{H}{w+o}\right\rfloor.
$$

Real density is lower or occasionally appears higher under sharing and overcommit; reliability constraints determine usable capacity.

For cold-start stages $t_i$, readiness latency is

$$
T_{ready}=\sum_i t_i
$$

only when stages are serial. Parallel fetch, snapshot restore and lazy loading require a dependency graph and may defer cost beyond declared readiness.

## Mechanisms, Invariants, or Proof Structure

Review an isolation choice with these obligations.

1. **Principal obligation:** mutually hostile and mutually trusted workloads are partitioned explicitly.
2. **Boundary obligation:** process, container, application-kernel or VM enforcement is identified without category shortcuts.
3. **Interface obligation:** host syscalls, virtual devices, exits, brokers, files, networks and management APIs are enumerated.
4. **TCB obligation:** hardware, firmware, kernels, VMMs, helpers, runtimes and control planes have owners and patch paths.
5. **Bypass obligation:** passthrough, shared mounts, descriptors, agents and metadata cannot silently cross the boundary.
6. **Identity obligation:** root, tenant and workload identity are scoped at every layer and external service.
7. **Resource obligation:** host and guest accounting includes helpers, kernel work, overcommit and recovery capacity.
8. **Compatibility obligation:** required ABI, kernel, device and observability behavior is tested on the chosen mechanism.
9. **Lifecycle obligation:** create, ready, snapshot, migrate, update, fail and delete preserve isolation.
10. **Performance obligation:** cold, warm and steady measurements use equivalent work and complete denominators.
11. **Evidence obligation:** adversarial tests exercise the actual exposed interface and boundary-changing control plane.
12. **Assurance obligation:** isolation, confidentiality, availability, side-channel and supply-chain claims remain separate.

The proof begins with every attacker-to-asset path, maps each crossing to a concrete mechanism and includes the components enforcing it in the TCB. It overlays resources, external services and lifecycle, then tests both escape resistance and operational behavior. A benchmark or architecture diagram supports only the dimensions it actually measures.

## Alternatives and Trade-Offs

- **Process versus container:** processes minimize machinery; containers add packaged, namespaced and resource-governed lifecycle on the same kernel.
- **Container versus VM:** containers maximize kernel sharing; VMs add guest-kernel and virtual-hardware boundaries with more lifecycle state.
- **Application kernel versus host kernel:** interposition narrows direct host API exposure; reimplementation adds compatibility and its own TCB.
- **MicroVM versus conventional VM:** a minimal device model improves startup and surface; a full model supports broader guests and devices.
- **One tenant per boundary versus grouping:** separation limits blast radius; grouping amortizes overhead and creates shared fate.
- **Nested container in VM versus either alone:** nesting combines packaging and a guest boundary; it increases layers to patch and observe.
- **Emulation versus passthrough:** emulation preserves mediation and portability; passthrough improves performance with device/IOMMU trust.
- **Host kernel versus custom guest kernel:** host sharing simplifies updates; guest choice enables specialized or legacy behavior.
- **Cold boot versus snapshot restore:** boot starts from a simpler provenance path; restore improves latency and adds state integrity/versioning.
- **Eager allocation versus overcommit:** reservation improves predictability; overcommit raises density and contention or OOM risk.
- **Shared cache versus isolated memory:** sharing saves capacity; separation reduces cross-workload coupling and some channels.
- **Guest agent versus agentless operation:** agents improve management; they add privileged software and credentials inside the boundary.
- **Rich observability versus narrow management surface:** deep diagnostics aid response; exposed consoles and agents enlarge TCB.
- **Uniform runtime versus risk tiers:** uniformity simplifies fleets; tiers match boundary cost to workload hostility.
- **Logical versus physical separation:** logical boundaries use hardware efficiently; physical separation narrows shared-hardware channels at high cost.
- **Maximum compatibility versus minimum surface:** broad syscalls and devices run more software; narrow interfaces reduce attack paths.

## Failure Modes and Misconceptions

- “A process boundary provides no security.” Address spaces and credentials are foundational but may be too broad for hostile multi-tenancy.
- “A container is one kernel primitive.” It is a runtime composition.
- “Containers have their own kernels.” Standard Linux containers share the host kernel.
- “Image isolation equals runtime isolation.” Packaging does not define the execution boundary.
- “Privileged and rootless containers have the same boundary.” Their reachable host authority differs substantially.
- “Every VM is stronger than every container.” Device model, host helpers, configuration and threat model determine exposure.
- “Guest root is host root.” It is privileged inside the guest and attacks the VM boundary from there.
- “Hardware virtualization removes the host kernel.” KVM and host backends remain involved.
- “Virtio has no attack surface.” Paravirtual queues and backends parse guest-controlled data.
- “Passthrough simply removes overhead.” It introduces IOMMU, firmware and reset assumptions.
- “MicroVM means container without a kernel.” It retains a guest kernel and hardware virtualization.
- “A jailed VMM needs no patching.” It remains in the TCB and processes hostile input.
- “An application kernel forwards every syscall.” Implementations may handle calls independently and use a restricted host API.
- “Linux compatibility is binary.” Syscalls, ioctls, filesystems and timing semantics vary by mechanism and version.
- “Nesting doubles security automatically.” Layers can share assumptions and add bypasses.
- “One pod per sandbox means one tenant per sandbox.” Workload grouping is an orchestration decision.
- “VM memory is only guest RAM.” VMM, guest kernel, caches and backends add host consumption.
- “Container startup is always instant.” Image, storage, network and application readiness can dominate.
- “VMs are always slower.” Workload transition and I/O paths determine overhead.
- “Guest cgroups govern the VMM.” Host resource policy must cover host-side processes and work.
- “Escape resistance implies availability.” Resource exhaustion remains a separate path.
- “Compute isolation protects shared storage.” External services need their own authorization.
- “The control plane is outside the security model.” It can alter every runtime boundary.
- “VMs eliminate hardware side channels.” Physical resources can remain shared.
- “Snapshots are complete backups.” External disks, keys, networks and consistency may be outside them.
- “One successful benchmark selects the boundary.” Workload, risk and lifecycle evidence are multidimensional.

## Worked Examples

### Example 1

A trusted batch job and API share one host kernel but use separate cgroups and hardened containers. Their primary risk is accidental interference, so fast scaling and shared caches dominate. Host-kernel patching and resource tests support the choice.

### Example 2

The following executable toy computes idealized memory packing bounds. It demonstrates integer arithmetic only, not real density, sharing, fragmentation, overcommit, security or performance.

<!-- bijux-verify: {"id":"isolation-memory-packing-bound","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"available_mib=57344\ncontainer_bound=112\napplication_kernel_bound=96\nmicrovm_bound=89\nvm_bound=37\n","stderr":""}} -->
```python
available_mib = 56 * 1024
working_set_mib = 512
overhead_mib = {
    "container": 0,
    "application_kernel": 80,
    "microvm": 128,
    "vm": 1024,
}

print(f"available_mib={available_mib}")
for name, overhead in overhead_mib.items():
    bound = available_mib // (working_set_mib + overhead)
    print(f"{name}_bound={bound}")
```

### Example 3

Untrusted compilation runs in one microVM per customer. Containers inside each guest package build steps. A customer exploit must cross the guest-kernel and virtual-device boundary to reach the host, while inner containers limit accidental interference among that customer's jobs.

### Example 4

A conventional VM exposes an unused emulated USB controller. Removing it reduces guest-controlled parser surface without changing CPU virtualization. The label “VM” did not reveal that avoidable boundary.

### Example 5

A high-throughput appliance receives a passed-through NIC. Performance improves, but review now includes IOMMU groups, device firmware, DMA, reset and network policy. Its boundary differs from the same VM using an emulated or paravirtual NIC.

### Example 6

An application-kernel sandbox rejects an obscure filesystem ioctl required by a vendor tool. A standard container supports it through the host kernel, while a VM supports it through a configured guest kernel and device. Compatibility testing, not category names, reveals the choice.

### Example 7

Two hostile tenants share one application-kernel sandbox because they are separate containers. Compromise of the sandboxed kernel could cross between them. Moving each tenant to a distinct sandbox aligns isolation unit with principal.

### Example 8

A microVM boots in 120 ms, but fetching its root image and establishing network policy takes 800 ms. A container process starts in 25 ms from a warm image but needs 600 ms for the application to become ready. Comparing only VMM and process creation misstates user-visible latency.

### Example 9

A guest agent holds a fleet-wide management credential. Guest compromise steals authority beyond the VM despite intact virtualization. Replacing it with per-instance credentials and a narrow host-mediated channel repairs the cross-boundary path.

### Example 10

A VM snapshot restores memory and device state but its external database lease expired. The process resumes into invalid ownership. A restore protocol must reauthenticate, fence old instances and reconcile external state before declaring readiness.

## Cross-Program Connections

- **Security engineering:** threat models, TCBs, attack paths, side channels and defense in depth drive boundary selection.
- **Platform engineering:** runtimes, orchestration, workload classes and control planes implement the chosen isolation unit.
- **Performance engineering:** transitions, caches, virtual I/O, working sets and startup paths determine cost.
- **Reliability engineering:** snapshots, migration, patching, recovery capacity and shared fate determine availability.
- **Network engineering:** virtual links, passthrough, metadata endpoints and policy create cross-boundary paths.
- **Storage engineering:** shared volumes, virtual disks, snapshots and data fencing remain independent from CPU isolation.
- **Supply-chain engineering:** host, guest, image, VMM, firmware and agent artifacts all require provenance and updates.
- **Distributed systems:** tenant identity and external service authorization must survive nested execution layers.
- **Observability engineering:** inner and outer identities, metrics and event correlation support diagnosis without boundary collapse.
- **Systems engineering:** selecting a boundary is a whole-system trade among risk, compatibility, cost and operational ownership.

## References

1. Linux man-pages Project, [namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html), Linux namespace types, APIs and process isolation views; retrieved 2026-09-04.
2. Linux Kernel Documentation, [Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), unified hierarchical resource accounting and control; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Seccomp BPF](https://docs.kernel.org/userspace-api/seccomp_filter.html), host syscall filtering, inheritance and action model; retrieved 2026-09-04.
4. Open Container Initiative, [Runtime Specification](https://github.com/opencontainers/runtime-spec/blob/main/spec.md), container configuration, execution environment and lifecycle scope; retrieved 2026-09-04.
5. Linux Kernel Documentation, [KVM API](https://docs.kernel.org/virt/kvm/api.html), VM, vCPU and device file-descriptor interfaces; retrieved 2026-09-04.
6. QEMU Project, [System Emulation Introduction](https://qemu.readthedocs.io/en/master/system/introduction.html), virtual machine models, accelerators, device emulation and Virtio; retrieved 2026-09-04.
7. Firecracker, [Design](https://github.com/firecracker-microvm/firecracker/blob/main/docs/design.md), microVM machine model, KVM boundary, jailed VMM, devices and resource controls; retrieved 2026-09-04.
8. gVisor, [Introduction to gVisor Security](https://gvisor.dev/docs/architecture_guide/intro/), application-kernel interposition, restricted host API, platforms and limitations; retrieved 2026-09-04.
9. Kata Containers, [Project Architecture Overview](https://katacontainers.io/), container-runtime integration with lightweight virtual-machine isolation; retrieved 2026-09-04.
10. National Institute of Standards and Technology, [SP 800-190: Application Container Security Guide](https://csrc.nist.gov/pubs/sp/800/190/final), container threat categories and security recommendations; retrieved 2026-09-04.

## Exercises

### Exercise 1

For 56 GiB available memory and 512 MiB workload working sets, compute idealized bounds with per-instance overheads of 0, 128 MiB and 1 GiB. State three reasons production density differs.

### Exercise 2

Compare the attacker-facing path for a syscall that reads a file in a hardened container, an application-kernel sandbox and a VM. Name the primary mediation layers without claiming one is universally strongest.

### Exercise 3

A tenant VM uses a passed-through accelerator and a fleet-wide guest-agent credential. Identify how both choices change the boundary and propose narrower alternatives.

### Exercise 4

Choose an isolation design for a platform running trusted first-party APIs, hostile customer functions and a legacy network appliance. State the isolation unit and dominant reason for each.

### Exercise 5

Design a fair experiment comparing a container, application-kernel sandbox and microVM for one service. Include security, compatibility, startup, steady-state, resource and lifecycle evidence.

## Answers to the Exercises

### Answer 1

Available memory is $56\times1024=57{,}344$ MiB. With zero overhead the bound is $\lfloor57344/512\rfloor=112$. With 128 MiB overhead it is $\lfloor57344/640\rfloor=89$. With 1 GiB overhead it is $\lfloor57344/1536\rfloor=37$.

Production density differs because kernels, VMMs, caches and helpers have nonlinear or shared memory; fragmentation and host reservations consume capacity; and overcommit can admit more instances while reducing reliability. Workload peaks, page-cache sharing, deduplication, ballooning and recovery headroom also change usable capacity. The bound is not a security or performance ranking.

### Answer 2

In a hardened container, the application syscall enters the host kernel after seccomp admission; credentials, namespaces, mounts and LSM policy govern the object. The host kernel's allowed filesystem path is directly exposed to workload input, with the runtime setup and host control plane in the TCB.

In an application-kernel sandbox, the workload call is intercepted and implemented by the sandbox kernel. Its restricted host calls and filesystem helper or proxy then reach host services. Compatibility and the sandbox implementation join the TCB, while direct workload exposure to the host syscall implementation is reduced.

In a VM, the call enters the guest kernel and guest filesystem. I/O reaches a virtual device, VMM or backend and host kernel, or a passthrough path. The guest kernel is attacker-controlled after guest-root compromise, while hardware virtualization and the exposed device path mediate host access. Actual configuration and vulnerabilities—not labels—determine comparative risk.

### Answer 3

Passthrough removes some VMM device mediation and makes isolation depend on IOMMU grouping, DMA remapping, interrupts, firmware, reset and peer-device behavior. The fleet credential creates an application-level escape path: compromising one guest can authorize management actions against assets outside its VM.

Use a mediated virtual device or a dedicated device/IOMMU group when its performance is sufficient; otherwise validate and monitor the complete passthrough trust chain. Replace the shared credential with short-lived per-instance identity scoped to that tenant and operation. Prefer a narrow authenticated host service over a broadly privileged in-guest agent, and rotate or revoke identity during snapshot and restore.

### Answer 4

Run mutually trusted first-party APIs in separately resource-governed, hardened containers, grouping only services that share the same trust domain. This preserves rapid startup and efficient host-kernel sharing while namespaces, capabilities, seccomp, LSM and mounts constrain accidental compromise.

Give each hostile customer's functions a distinct application-kernel sandbox or microVM according to measured compatibility and performance; do not group customers inside one boundary. The dominant reason is reducing direct host-kernel exposure or interposing a hardware-virtualized guest boundary. Run the legacy appliance in a conventional VM with only required virtual devices because it needs its own kernel and machine assumptions. All three still need host cgroups, network/storage policy and protected control-plane identity.

### Answer 5

Pin the same application build, input, host hardware, network and storage service. Record exact kernels, runtimes, policy, device paths and isolation unit. Measure cold image fetch, warm create, snapshot restore and application readiness; steady throughput, tail latency and CPU; full host resident/committed memory, helpers, caches, I/O and density under a reliability headroom target.

Run the complete functional, syscall, filesystem, signal, networking, tracing and failure suite on each mechanism. Draw each TCB and exposed interface; probe forbidden host objects, escape-relevant syscalls or virtual devices, shared-service authorization, resource exhaustion, control-plane operations and cross-tenant grouping. Exercise patch, crash, snapshot, restore and deletion while verifying identity and data fencing. Report unsupported behavior and security evidence separately from benchmark results, then choose against the stated threat model rather than collapsing results into one score.
