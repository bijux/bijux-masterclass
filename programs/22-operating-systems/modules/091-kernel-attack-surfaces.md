---
module_id: OS-091
program: Operating Systems
level: 2
module_number: 91
title: Kernel Attack Surfaces
status: complete
last_verified: 2026-09-04
---

# Kernel Attack Surfaces

## One-Page Review

### Governing question

How can operators identify, reduce and monitor the kernel code reachable by each attacker while preserving the devices, protocols and performance the system actually needs?

### Essential definitions

- An **attack surface** is the set of interfaces and implementation paths through which attacker-controlled input reaches a trust boundary.
- A **kernel entry path** begins at a syscall, exception, interrupt, device, packet, filesystem image, virtual device or management interface.
- **reachability** means a principal can cause an implementation path to process controlled input under the deployed configuration.
- A **kernel configuration surface** is code compiled in, loadable or automatically activatable on a system.
- **exploit mitigation** makes a defect harder to convert into useful attacker capability; it does not remove the defect.
- A **security boundary crossing** gives an attacker authority not granted by the correctly configured production system.
- A **reproducer** is a bounded test that triggers a defect on an exact kernel build and configuration.

### Central model, mechanism, or theorem

Kernel risk begins with paths, not package names. Map principals to entry interfaces, interfaces to enabled subsystems, and subsystems to protected assets. Reduce the reachable graph through configuration, least privilege, namespaces, seccomp, LSM policy, device mediation and module control. Then add memory-integrity defenses, fuzzing, telemetry, prompt updates and recovery. No single hardening flag proves that the remaining graph is safe.

### Critical invariants

- Every exposed interface has an owner, required workload and documented trust level.
- Code absent from the build or unreachable by policy is not silently reintroduced through module autoload, compatibility ABIs or privileged helpers.
- Untrusted inputs never gain broader parsing paths merely for diagnostic or compatibility convenience.
- Kernel, firmware and module provenance is verified before execution, and runtime mutation is controlled.
- Mitigation state is measured on the running system rather than inferred from a configuration file.
- Crashes, warnings and sanitizer findings retain exact build, configuration and reproducer evidence.
- Remediation follows supported releases and complete fix dependencies rather than CVE-count shortcuts.

### Common failures

Teams count syscalls but ignore ioctls and devices, disable a userspace tool while leaving its kernel interface reachable, permit unprivileged namespace or BPF creation unintentionally, trust module filenames without enforcing signatures, treat KASLR as memory safety, dismiss a CVE solely from its score, run fuzzers on production hosts, or patch one commit without its prerequisite fixes.

### Compact example

A compute worker needs files, virtual memory and one network protocol but no local users, arbitrary filesystems, USB, Bluetooth, unprivileged BPF or compatibility ABI. A purpose-built kernel and device policy remove unused parsers; seccomp and capabilities narrow each job; signed modules and locked runtime settings prevent reintroduction. Fuzzing and patching then focus on the remaining VFS, memory, networking and driver paths.

### Connections

Kernel attack surfaces connect syscall design, drivers, protocol parsers, virtualization, containers, memory safety, secure boot, fuzzing, incident response, vulnerability management and fleet configuration.

## Governing Question

The kernel must parse hostile input while holding ultimate machine authority. The governing question is how to identify which of its enormous implementation graph each principal can reach, remove unjustified paths and contain defects that remain without breaking the platform's required contract.

## Why This Matters

Kernel bugs can cross process, container and VM-host boundaries, disclose memory, corrupt persistent data or halt a machine. Surface varies dramatically: a storage appliance, phone, build worker and desktop may run related source but expose different syscalls, devices, protocols, modules and privileges. Generic vulnerability counts cannot express that deployment-specific reachability.

Reduction has compounding value. Removing an unused parser eliminates its defect classes, patch urgency and telemetry noise. Yet aggressive configuration can remove recovery paths or force unsafe out-of-tree code. Durable hardening couples minimal functionality with tested operations, supported updates and precise evidence.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain syscall dispatch, interrupts, exceptions, DMA and kernel/user privilege;
- describe modules, drivers, filesystems, network protocols, eBPF and ioctls;
- reason about capabilities, namespaces, seccomp, LSMs and cgroups;
- distinguish defect, exploit primitive, boundary crossing, mitigation and incident;
- interpret kernel versions, configuration, taint, crash traces and stable updates.

Retrieve the exact kernel release and commit, distribution patch set, configuration, command line, loaded and loadable modules, firmware and microcode, enabled LSMs, sysctls, capability and namespace policy, syscall ABIs, device inventory, network families, mounted filesystem types, BPF and perf policy, virtualization backends, taint state and supported-update channel.

## Learning Objectives

After completing this module, you should be able to:

1. build a principal-to-entry-path map for a running kernel;
2. distinguish compiled, loadable, exposed, reachable and exercised code;
3. analyze syscall, ioctl, filesystem, network, device and virtualization inputs;
4. reduce surface through kernel configuration and runtime least privilege;
5. explain deterministic and probabilistic exploit mitigations without overclaiming;
6. design safe sanitizer, fuzzing and reproducer workflows;
7. assess vulnerability applicability from exact configuration and reachability;
8. operate patch, rollback, telemetry and incident-response loops for kernel risk.

## Core Exposition

### Start from principals, not features

List remote peers, local unprivileged users, containers, guest VMs, attached devices, administrators and compromised services. Each controls different inputs and credentials. “The kernel exposes BPF” is incomplete until the design states who may create programs, which types and helpers are permitted, and what privileged agent can act for them.

### Model every entry family

Syscalls and exceptions enter from executing tasks. Packets enter network parsers; filesystem images enter block and VFS parsers; USB, PCI and other devices supply descriptors, DMA and interrupts; guests supply exits and virtual-device queues. Management interfaces, debugfs, procfs, sysfs, netlink and modules add control paths.

### Separate presence from reachability

Code may be compiled out, built in, available as a module, loaded, registered, exposed to a namespace or actually callable by one principal. Record each state. An unloaded module can still autoload when an attacker triggers its alias; a loaded driver may be unreachable when no device or node is exposed.

### Treat privilege as a surface multiplier

Root and broad capabilities reach module loading, raw devices, namespaces, BPF, perf, mounts and kernel controls unavailable to ordinary users. Reduce every capability set and privileged helper contract. Root inside a user namespace is scoped, but namespace creation can expose code paths otherwise reserved for host administrators.

### Inventory syscall ABIs

Native, compatibility and special ABIs have separate tables and argument conventions. Disable unused compatibility support where feasible and filter workloads by architecture and call. Count multiplexed interfaces such as `ioctl`, `bpf`, `perf_event_open`, netlink and asynchronous submission by suboperation, not as one uniform entry.

### Narrow file-descriptor authority

An allowed read, write, mmap or ioctl reaches code selected by the descriptor's object type. Close unintended device, directory, socket, namespace, pidfd and BPF handles before executing untrusted code. File permissions, device cgroups, LSM rules and broker design matter as much as the syscall list.

### Minimize filesystem parsers

Filesystem implementations parse complex, sometimes attacker-controlled metadata with deep state and recovery logic. Build or load only required types, restrict unprivileged mounts, validate image provenance and fuzz corrupt media. Network filesystems add protocol and credential paths beyond local block parsing.

### Minimize network protocol families

Listening sockets are only part of network surface. Packet reception can reach link, transport, tunneling, filtering and control parsers before an application accepts data. Disable unused protocol families and modules, constrain raw and packet sockets, and place parsers behind appropriate network and user namespaces.

### Treat devices as hostile input producers

Drivers process register state, descriptors, firmware messages, interrupts and DMA. Physical access, hotplug and compromised firmware change the threat model. Use IOMMU isolation, device authorization and minimal drivers; verify reset and ownership across handoff. An absent device node does not by itself stop DMA or kernel binding.

### Include virtual devices and guests

Guest kernels control virtual-device queues, exits and hypercalls consumed by KVM, VMMs and host backends. Remove unused emulation and sandbox helpers. Device passthrough replaces emulation with IOMMU, firmware and reset assumptions rather than eliminating the boundary.

### Govern eBPF as privileged programmability

eBPF verification, JIT compilation, helpers, maps and attachment points span many subsystems. Determine whether unprivileged use is enabled, which privileged services load programs and how objects are pinned and delegated. Treat a loader API as a security-sensitive compiler and lifecycle, not simply observability.

### Govern perf and tracing interfaces

Performance counters, tracing, kprobes and kernel logs can expose addresses, execution and cross-process data or invoke complex code. Restrict them by principal and namespace, protect tracefs and debugfs, and separate production observability agents from tenants. Debug convenience should not become a permanent universal interface.

### Reduce module mutability

Build a minimal supported kernel, load required modules early, then disable further loading where operationally viable. If modules remain necessary, enforce signatures from protected keys and control autoload. A signature authenticates an authorized blob; it does not establish that the module is vulnerability-free.

### Verify boot and runtime state

Secure or verified boot can establish provenance for kernel, configuration and early components; measured boot can record evidence. Runtime checks must confirm active LSMs, lockdown, module enforcement, sysctls and mitigations. A signed boot artifact does not prove later policy stayed intact.

### Apply syscall and object least privilege

Use seccomp to remove unneeded entry points, namespaces to reduce visible objects, capabilities to narrow privileged operations and LSM policy to enforce object relationships. These mechanisms compose. Seccomp cannot understand pathname targets; a namespace does not filter calls; an LSM does not bound CPU or memory.

### Control resource-amplification paths

Even non-exploitable kernel operations can allocate memory, spawn work, fill tables, pin pages or trigger expensive parsing. Apply cgroups, rlimits, quotas, queue bounds and admission controls. Include kernel memory and helper work in accounting so a tenant cannot externalize its cost.

### Prefer elimination over exploit mitigation

Compiled-out or unreachable code cannot process an attacker's input. Where functionality must remain, memory permissions, stack protections, hardened allocators, reference-count checks, control-flow defenses and hardware protections can obstruct exploitation. Reduction prevents exposure; mitigations raise exploitation cost.

### Distinguish deterministic and probabilistic defenses

Write-xor-execute style permissions and prevented user-memory execution impose structural constraints. Canaries, address randomization and layout secrets rely partly on hidden values and can be weakened by information disclosure. Record entropy and leak assumptions rather than calling probabilistic defenses absolute.

### Treat KASLR as one layer

Kernel address randomization makes target locations less predictable but does not repair memory corruption. Address leaks can defeat it, and repeated attempts may matter. Preserve leak prevention, strict kernel-pointer exposure and stronger memory-integrity defenses alongside randomization.

### Prevent kernel information exposure

Restrict logs, symbols, debug interfaces and performance data; initialize memory returned to userspace; clear sensitive freed or stack data where supported. Stable opaque identifiers should replace kernel addresses. Information disclosure is often the bridge from a corruption bug to reliable exploitation.

### Use sanitizers in controlled builds

KASAN, KMSAN, UBSAN, lock and concurrency detectors can expose memory, initialization and synchronization defects. They change performance, memory layout and timing, so run them on dedicated test systems and representative configurations. A sanitizer-clean run covers exercised paths only.

### Fuzz stateful interfaces

Coverage-guided fuzzers such as syzkaller generate structured syscall sequences and retain reproducers. Extend campaigns to filesystem images, packets, USB and virtual devices where relevant. Maximize configuration coverage in research, then reproduce against the precise production-relevant surface before assessing applicability.

### Isolate fuzzing infrastructure

Fuzzers intentionally crash, hang and corrupt kernels. Use disposable VMs or dedicated hosts, controlled networks, protected credentials and bounded artifact storage. Preserve console, pstore, kernel image, symbols, config and seed. Never aim hostile campaigns at shared production machines.

### Demand exact reproduction evidence

Record kernel commit, full configuration, compiler, architecture, command line, modules, taint, sanitizer report and minimal reproducer. Confirm on a supported upstream or vendor build as appropriate. A screenshot or CVE label cannot establish root cause, affected versions or boundary crossing.

### Define the crossed boundary

A crash is a reliability defect; a security issue grants capability an attacker should not have on a correctly configured production system. State required access, resulting authority and configuration. Remote denial of service, local privilege escalation, guest-to-host escape and information disclosure are different claims.

### Assess CVE applicability locally

Map a CVE's fixing commits and affected versions to the deployed distribution tree, then check configuration, architecture, module, interface and principal reachability. Large kernel CVE counts include code absent from a given system. Conversely, lack of a CVE does not prove a relevant bug is absent.

### Take coherent supported updates

Kernel fixes often depend on adjacent changes and are tested as release sets. Prefer supported vendor or stable releases over isolated cherry-picks unless expert analysis requires otherwise. Validate boot, drivers, performance, security state and rollback under the exact fleet hardware.

### Shorten exposure windows operationally

Inventory kernel build identity continuously, subscribe to relevant advisories, prequalify updates, stage canaries and automate rollback. Live patching can reduce reboot delay for covered changes but has scope and state constraints. It complements rather than eliminates full-kernel update testing.

### Monitor for invariant violations

Collect oopses, warnings, sanitizer-like signals, module changes, taint, failed integrity checks, policy changes and unexpected interface use. Rate-limit without erasing first evidence. A compromised kernel can falsify host telemetry, so high-assurance systems need external logs or attestable state.

### Preserve forensic and recovery boundaries

On suspected kernel compromise, isolate the host, protect volatile evidence, rotate credentials exposed to it and rebuild from known-good artifacts. Restarting one container is insufficient because every host process and secret may be affected. Recovery scope follows the breached kernel boundary.

### Recompute surface after every change

New hardware, kernel configuration, module, observability agent, container privilege, hypervisor backend or workload syscall can add paths. Treat surface inventory as generated evidence tied to release state. Review diffs and require justification for expansion.

## Definitions and Notation

Let principals be $P$, entry interfaces $I$, enabled subsystems $S$ and protected assets $A$. Define edges $p\to i$, $i\to s$ and $s\to a$ when deployed configuration permits the corresponding reachability. The attack-path set is

$$
\Pi=\{(p,i,s,a):p\to i\land i\to s\land s\to a\}.
$$

Removing an edge can eliminate many paths; counting paths alone does not measure exploitability or consequence.

For principal $p$, define its reachable handler set

$$
H(p)=\bigcup_{i\in I(p)} handlers(i,C),
$$

where $C$ is exact build and runtime configuration. The cardinality $|H(p)|$ is a coverage measure only: handlers differ in complexity, privilege and defect density.

Let remediation exposure be approximated by

$$
E=t_{deploy}-t_{applicable},
$$

where applicability is established for the deployed system and deployment completes fleet-wide. This elapsed time says nothing about exploitation probability or preexisting compromise.

A mitigation chain with defenses $d_1,\ldots,d_n$ is not generally assigned independent probabilities: shared assumptions and correlated bypasses make

$$
\Pr(\text{bypass all})\neq\prod_j \Pr(\text{bypass }d_j)
$$

without evidence of independence.

## Mechanisms, Invariants, or Proof Structure

Review kernel exposure with these obligations.

1. **Principal obligation:** remote, local, container, guest, device and administrator attackers are distinguished.
2. **Entry obligation:** syscalls, descriptors, packets, storage, devices, exits and management interfaces are inventoried.
3. **Configuration obligation:** compiled, modular, loaded, registered, exposed and reachable states are separated.
4. **Privilege obligation:** capabilities, namespaces, helpers and open handles grant only intended paths.
5. **Mutation obligation:** boot provenance, module loading, BPF and runtime control changes are authorized.
6. **Reduction obligation:** unused ABIs, parsers, protocols, devices and debug facilities are absent or unreachable.
7. **Mitigation obligation:** memory-integrity and probabilistic defenses retain explicit assumptions.
8. **Resource obligation:** kernel allocation, work queues and helpers are bounded per principal.
9. **Testing obligation:** sanitizer and fuzzing campaigns cover relevant interfaces in isolated environments.
10. **Applicability obligation:** findings map to exact versions, configs, access and crossed boundaries.
11. **Remediation obligation:** coherent supported updates, canaries, rollback and incident scope are proven.
12. **Evidence obligation:** runtime state, crashes, reproducers, telemetry and surface diffs are durable and attributable.

The proof enumerates principal-to-asset paths, removes unnecessary edges and verifies enforcement for those removals. It then reviews remaining implementations for prevention, exploit resistance, detection and recovery. Because path enumeration and testing are incomplete by nature, the result is a maintained assurance case, not a proof that the kernel contains no exploitable defect.

## Alternatives and Trade-Offs

- **General-purpose versus minimal kernel:** broad builds maximize hardware compatibility; minimal builds remove unused implementation paths.
- **Built-in versus module:** built-ins simplify early availability; modules permit lifecycle flexibility and runtime expansion.
- **Disable loading versus signed modules:** disabling freezes surface; signing supports authorized updates while retaining loader paths.
- **Native plus compatibility ABI versus native only:** compatibility runs legacy code; native-only removes alternate syscall tables.
- **Direct access versus broker:** direct interfaces reduce latency; brokers concentrate validation and privileged TCB.
- **Rich drivers versus mediated virtual devices:** native devices maximize features; mediation can narrow host parsers and adds backend code.
- **Unprivileged namespaces versus disabled creation:** enablement supports rootless isolation; restriction removes reachable setup paths.
- **Unprivileged BPF versus privileged loaders:** direct programmability enables tools; controlled loaders narrow verifier and attachment access.
- **Debug visibility versus production surface:** tracing accelerates diagnosis; universal debug interfaces expose data and control paths.
- **Reduction versus mitigation:** removal prevents reachability; mitigation preserves features while assuming defenses resist exploitation.
- **Deterministic versus randomized hardening:** structural controls impose rules; randomization raises cost and depends on secrecy.
- **Sanitizer breadth versus fidelity:** sanitizers detect classes of bugs; instrumentation changes timing, layout and capacity.
- **Broad fuzz configuration versus production match:** broad builds discover more bugs; matched builds establish local applicability.
- **Live patch versus rebooted update:** live patch shortens disruption; full boot applies a coherent image and resets state.
- **Rapid rollout versus staged canary:** rapid deployment shortens exposure; staging reduces regression blast radius.
- **Host recovery versus workload restart:** rebuild addresses kernel compromise; restart is cheaper and cannot restore a breached host boundary.

## Failure Modes and Misconceptions

- “The kernel attack surface is the syscall count.” Devices, packets, filesystems, exits and control interfaces also enter it.
- “Compiled code is exposed code.” Runtime registration, objects and privilege determine reachability.
- “An unloaded module is unreachable.” Autoload can activate it.
- “No device node means no driver risk.” Binding, DMA, packets and sysfs can remain.
- “Root in every namespace is host root.” Authority depends on the owning user namespace.
- “One ioctl is one operation.” Commands and device implementations expose many paths.
- “Disabling a CLI disables the kernel feature.” Other programs can invoke the interface.
- “Containers remove host-kernel exposure.” Their allowed syscalls enter the shared host kernel.
- “VM guests cannot attack host kernel code.” KVM and backends process guest-controlled inputs.
- “Passthrough removes attack surface.” It substitutes IOMMU, firmware and device lifecycle assumptions.
- “BPF is only observability.” It is privileged programmability with verifier, JIT and attachment surfaces.
- “Signed modules are safe modules.” Signatures establish authorization and integrity, not correctness.
- “Secure boot proves runtime hardening.” Later mutable state and policy must also be measured.
- “Seccomp understands paths.” It sees scalar syscall metadata, not pathname objects.
- “KASLR prevents exploitation.” Leaks and corruption remain possible.
- “More mitigations multiply independent protection.” Bypasses can share assumptions and defects.
- “A sanitizer proves memory safety.” It detects exercised violations under instrumentation.
- “Fuzzing proves absence of bugs.” Coverage is finite and oracles incomplete.
- “A kernel crash is automatically a security issue.” The crossed trust boundary and required access must be shown.
- “A CVE affects every Linux system.” Applicability depends on version, configuration and reachability.
- “No CVE means no security-relevant bug.” Assignments and discovery are incomplete.
- “One fix commit is always sufficient.” Dependencies and follow-up fixes may matter.
- “Long-term support means no urgent updates.” Supported trees still receive important fixes.
- “Live patching removes reboot needs forever.” Coverage and accumulated state remain limited.
- “Host logs are trustworthy after kernel compromise.” The compromised kernel can alter local evidence.
- “Restarting a container recovers a host compromise.” The shared kernel boundary remains breached.

## Worked Examples

### Example 1

A web service needs ordinary file and network calls but inherits `/dev/kvm` and a perf descriptor. Its seccomp profile looks narrow, yet the descriptors reach virtualization and tracing paths. Closing them removes more authority than another syscall-name rule.

### Example 2

The following executable toy unions abstract handler sets enabled by interface families. It demonstrates reachability counting only, not code size, defects, exploitability, consequence or risk.

<!-- bijux-verify: {"id":"kernel-handler-reachability","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"minimal_handlers=2\nserver_handlers=4\ndevelopment_handlers=8\nremoved_from_development=6\n","stderr":""}} -->
```python
handlers = {
    "core": {"vfs", "memory"},
    "netlink": {"netlink", "network"},
    "userns": {"user_namespace"},
    "bpf": {"bpf_verifier", "bpf_jit"},
    "io_uring": {"io_uring", "vfs"},
}

def reachable(features):
    result = set()
    for feature in features:
        result.update(handlers[feature])
    return result

minimal = reachable({"core"})
server = reachable({"core", "netlink"})
development = reachable(set(handlers))
print(f"minimal_handlers={len(minimal)}")
print(f"server_handlers={len(server)}")
print(f"development_handlers={len(development)}")
print(f"removed_from_development={len(development - minimal)}")
```

### Example 3

A filesystem driver is a module and not currently loaded, but an unprivileged mount request triggers autoload before permission failure. Disabling that module alias or removing the module changes reachability; checking `lsmod` alone did not.

### Example 4

A host disables unprivileged BPF but runs a root observability agent accepting tenant-supplied programs. The broker becomes the reachable verifier path. Its authentication, allowed program types, helpers, maps and attachments define the real policy.

### Example 5

A VM has no emulated USB but passes through a physical accelerator. Guest input no longer reaches USB emulation; it now reaches device firmware, DMA mappings, IOMMU and reset code. The attack graph changed rather than simply shrinking.

### Example 6

KASAN finds a use-after-free on a fuzz kernel with many debug features. The team reproduces it on the exact production configuration, identifies that an unprivileged socket reaches it and records the boundary crossing before prioritizing remediation.

### Example 7

A CVE names a Bluetooth parser. A server fleet has the subsystem compiled as a module but the files remain installed and socket-triggered autoload is possible. “No Bluetooth hardware” is insufficient evidence; policy or build changes must prove unreachability.

### Example 8

A signed out-of-tree module is accepted by enforced module verification. Its key is authorized, but a parsing defect still compromises the kernel. Signing prevented unauthorized replacement, not a trusted publisher's vulnerability.

### Example 9

A live patch covers one vulnerable function, but a related initialization change and new data layout require a full update. Applicability documentation records the partial scope, and the fleet schedules a rebooted coherent kernel rather than claiming complete remediation.

### Example 10

A container exploit gains host-kernel execution. Restarting the pod removes visible symptoms but leaves credentials and every co-resident workload potentially exposed. Incident response isolates and rebuilds the node and rotates secrets whose plaintext crossed it.

## Cross-Program Connections

- **Security engineering:** threat models, least privilege, exploit chains and incident scope turn surface into risk decisions.
- **Platform engineering:** kernel profiles, node pools, workload privilege and update automation define fleet reachability.
- **Network engineering:** packet families, tunnels, filters, netlink and device drivers expose remote and local paths.
- **Filesystem engineering:** image parsers, mount privileges, block devices and network filesystems process hostile state.
- **Virtualization engineering:** exits, virtual devices, KVM, VMM helpers and passthrough define guest-to-host surface.
- **Observability engineering:** BPF, perf, tracing and logs trade operational insight against privileged interfaces.
- **Reliability engineering:** resource amplification, canaries, rollback, live patch and rebuild govern exposure duration.
- **Supply-chain engineering:** kernel, module, firmware and configuration provenance precede runtime assurance.
- **Testing engineering:** sanitizers, coverage-guided fuzzing, fault injection and exact reproducers expose defects.
- **Systems engineering:** hardware, kernel, workloads, policy and response form one maintained assurance case.

## References

1. Linux Kernel Documentation, [The Linux Kernel Threat Model](https://docs.kernel.org/next/process/threat-model.html), boundaries, attacker capabilities and kernel security responsibilities; retrieved 2026-09-04.
2. Linux Kernel Documentation, [Kernel Self-Protection](https://docs.kernel.org/security/self-protection.html), surface reduction, memory integrity, information exposure and probabilistic defenses; retrieved 2026-09-04.
3. Linux man-pages Project, [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html), privileged kernel operations and capability decomposition; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Seccomp BPF](https://docs.kernel.org/userspace-api/seccomp_filter.html), per-process syscall surface reduction; retrieved 2026-09-04.
5. Linux Kernel Documentation, [Linux Security Modules](https://docs.kernel.org/userspace-api/lsm.html), additional access-control hooks and security contexts; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Kernel Module Signing Facility](https://docs.kernel.org/admin-guide/module-signing.html), signature verification, enforcement and key administration; retrieved 2026-09-04.
7. Linux Kernel Documentation, [CVEs](https://docs.kernel.org/process/cve.html), assignment, applicability and coherent-update guidance; retrieved 2026-09-04.
8. Linux Kernel Documentation, [Security Bugs](https://docs.kernel.org/process/security-bugs.html), exact evidence, boundary criteria and reporting process; retrieved 2026-09-04.
9. syzkaller Project, [syzkaller](https://github.com/google/syzkaller), coverage-guided kernel fuzzing, supported targets and documentation; retrieved 2026-09-04.
10. syzkaller Project, [Linux Kernel Fuzzing Setup](https://github.com/google/syzkaller/blob/master/docs/linux/setup.md), instrumented kernels, isolated workers and campaign configuration; retrieved 2026-09-04.

## Exercises

### Exercise 1

For a container host, enumerate one attacker-controlled input path through each of syscalls, filesystems, networking, devices and virtualization. State one reduction control for each.

### Exercise 2

The toy's development configuration reaches eight abstract handlers while the minimal configuration reaches two. Compute the reduction fraction and explain why it is not a risk-reduction percentage.

### Exercise 3

A module is unloaded, signed and present on disk. What evidence is required before claiming an unprivileged tenant cannot reach its parser?

### Exercise 4

Design a safe workflow from a syzkaller crash to a production applicability decision and upstream or vendor report.

### Exercise 5

A container escape is suspected on one node. Design immediate containment, evidence preservation, remediation and recovery without trusting the node kernel to attest to itself.

## Answers to the Exercises

### Answer 1

A process controls syscall numbers and arguments; seccomp and capability reduction remove unnecessary entries. A tenant can supply a filesystem image; restrict mount authority and omit unused parsers. Remote peers supply packets; disable unused families and filter reachability before complex tunnels. A physical or virtual device supplies descriptors and DMA; authorize devices, use IOMMU isolation and remove unused drivers. A guest supplies exits and virtual-device queues; minimize emulation and sandbox the VMM and backends.

For each path also inspect autoload, privileged brokers and inherited descriptors. Reduction is proven only from the principal's effective configuration, not from absence of a familiar userspace command.

### Answer 2

Six of eight abstract handlers are removed, so the count reduction is $6/8=0.75$, or 75%. This is a coverage-set calculation under the toy mapping.

It is not a 75% risk reduction because handlers have unequal complexity, defect likelihood, privilege and consequences. The sets omit paths, interactions and shared code; mitigations and attacker prerequisites differ; and removing low-risk handlers may matter less than retaining one exploitable high-impact path.

### Answer 3

Verify the exact kernel configuration and module, signature-enforcement mode and trusted key, filesystem permissions, module aliases and autoload policy. Identify every syscall, socket family, device, netlink action or privileged helper that can request the module and test from the tenant's actual user, mount, network and device namespaces with its capability and seccomp policy.

A valid signature proves authorized bytes if loading occurs; it does not prevent loading or prove correctness. Strong unreachability evidence is removing the module and alias from the deployed artifact, disabling the feature in the build, or enforcing and testing policy that no tenant-controlled request or broker can load and expose it.

### Answer 4

Preserve the crash, console, exact source commit, config, compiler, architecture, command line, modules, taint, fuzzer revision, corpus seed and reproducer. Reproduce in a disposable isolated worker, minimize the program without losing the report, identify the first faulty subsystem and test a fresh supported upstream kernel. Do not run it on shared production systems.

Map the path to production version and vendor patches, configuration, module state and the principal able to trigger it. State resulting capability and whether a production trust boundary is crossed. Search existing reports, identify maintainers, then follow kernel security or ordinary reporting rules with verifiable facts and appropriately protected reproducer. Test candidate fixes and their dependencies on both fuzz and production-like builds.

### Answer 5

Remove the node from scheduling and network trust using an external control plane; isolate management access without executing more untrusted diagnostics on it. Preserve remote logs, console, crash dump, storage snapshots and orchestration evidence, but label host-reported data untrusted. Identify workloads, credentials, tokens, keys, volumes and peers whose secrets or authority crossed the node.

Rotate exposed credentials, investigate lateral activity from independent telemetry and reproduce the suspected path in an isolated matching environment. Patch with a coherent supported kernel and any runtime or firmware dependencies. Rebuild the node from verified boot artifacts rather than restarting containers, reapply measured configuration, run boundary and regression tests, and return through a canary. Restore workloads from trusted images and data, then verify the vulnerable interface is removed or fixed fleet-wide.
