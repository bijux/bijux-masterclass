---
module_id: OS-089
program: Operating Systems
level: 2
module_number: 89
title: System-Call Filtering and Sandboxing
status: complete
last_verified: 2026-09-04
---

# System-Call Filtering and Sandboxing

## One-Page Review

### Governing question

How can a process reduce the kernel and object authority reachable by untrusted code while preserving the exact system-call behavior, resources and recovery paths the workload needs?

### Essential definitions

- **seccomp filter mode** evaluates classic BPF programs over system-call metadata and returns an action such as allow, errno, trap, notify or kill.
- A **system-call ABI** maps an architecture and calling convention to syscall numbers and argument widths.
- **no new privileges** is a one-way thread attribute that prevents `execve()` from granting privilege the caller did not already have.
- An **allowlist** admits enumerated operations and rejects the rest; a **denylist** rejects enumerated operations and admits the rest.
- **seccomp user notification** blocks selected calls and sends metadata to a userspace supervisor that responds or injects a file descriptor.
- **Landlock** is an unprivileged, stackable Linux security module interface for restricting selected object access and scopes.
- A **sandbox** is a composed boundary of syscall, object, identity, namespace, resource and lifecycle controls, not a synonym for one filter.

### Central model, mechanism, or theorem

Seccomp reduces syscall entry paths according to architecture, number and scalar arguments; it does not understand pathname strings, file-descriptor provenance or high-level intent. Filters are inherited, layered monotonically and resolved by action precedence. A defensible sandbox combines that mechanism with least privilege, object-aware policy, isolated views, bounded resources and a trusted supervisor outside the restricted domain.

### Critical invariants

- Every supported syscall ABI is explicitly admitted or rejected before dispatch by number.
- Filters are installed before untrusted threads or code can race ahead, and all intended threads receive them.
- The allowed syscall set includes only required operations and cannot be widened by descendants.
- Pointer arguments are never treated as immutable object-policy evidence.
- Brokers validate notification identity, revalidate raceable state and return only narrowly authorized results.
- Capabilities, descriptors, mounts, namespaces, LSM rules and cgroups bound authority that allowed calls can exercise.
- Failure, logging, debugging, update and supervisor-loss behavior is tested as part of the policy.

### Common failures

A profile checks syscall numbers without the architecture, builds a denylist that misses a new equivalent call, installs after threads start, filters `openat` by pointer value as if it were a path, returns a harmless-looking errno that triggers an unsafe fallback, lets a broker race target memory, retains powerful inherited descriptors, or claims sandboxing from seccomp alone.

### Compact example

A renderer needs `read`, `write`, memory management, signals and exit, but not namespace creation, mounting, kernel-module loading or raw networking. An allowlist makes newly added syscalls fail by default. A read-only mount tree and Landlock constrain which files an allowed `openat` can reach; dropped capabilities and a network namespace constrain allowed `ioctl` and socket operations; cgroups bound denial-of-service impact.

### Connections

System-call filtering connects ABI design, classic BPF, capabilities, namespaces, LSMs, container profiles, brokered authority, resource control, observability, fuzzing and exploit containment.

## Governing Question

Applications need kernel services, but every reachable syscall and object expands the attack surface available after compromise. The governing question is how to make that reachable authority explicit and minimal without breaking legitimate execution, creating broker confused-deputy flaws or mistaking an interface filter for an object-security model.

## Why This Matters

Seccomp can eliminate entire kernel subsystems from a workload's reachable interface. That is valuable defense in depth for services, containers, browsers, language runtimes and build systems. It can turn an exploit primitive into a denied syscall or terminate the compromised process before it reaches a dangerous kernel path.

Yet real programs use surprising calls during startup, error handling, locale loading, threading and shutdown. ABI compatibility adds aliases and multiplexors. Allowed file descriptors can already confer broad authority. Strict profiles therefore require empirical traces, source reasoning, fail-closed defaults and adversarial tests, plus object and resource controls outside seccomp.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain syscall entry, calling conventions, errno, signals and process/thread creation;
- describe classic BPF control flow and scalar comparisons;
- reason about file descriptors, pathname races, capabilities and credentials;
- distinguish namespaces, LSM authorization, cgroups and mount policy;
- identify trusted computing base, confused deputy, TOCTOU and fail-open behavior.

Retrieve the exact kernel, enabled seccomp and Landlock features, supported seccomp actions, native and compatibility ABIs, libc and runtime versions, executable and plugin set, existing filters, capability sets, `no_new_privs`, namespaces, mount tree, open descriptors, LSM policy, cgroups, supervisor identity and policy-generation toolchain.

## Learning Objectives

After completing this module, you should be able to:

1. model seccomp evaluation over architecture, syscall number, instruction pointer and six scalar arguments;
2. choose allowlist defaults and return actions appropriate to a workload and failure policy;
3. install and synchronize filters safely across thread creation and execution transitions;
4. reason about filter stacking, action precedence, ABI aliases and argument widths;
5. design user-notification brokers without assuming raceable target memory is stable;
6. apply Landlock and conventional controls for object-aware restrictions;
7. compose capabilities, namespaces, mounts, LSMs and cgroups into a sandbox;
8. validate compatibility, containment, observability and lifecycle under adversarial execution.

## Core Exposition

### Treat seccomp as syscall admission

Filter mode runs a classic BPF program against a read-only `seccomp_data` record before the selected syscall executes. The record supplies syscall number, audit architecture, instruction pointer and six 64-bit argument slots. The filter selects an action. It does not execute arbitrary helper functions or dereference userspace pointers.

### Distinguish strict mode from filter mode

Strict seccomp mode permits only a tiny fixed interface and is useful for narrow computation. Filter mode accepts verified classic BPF and supports practical workload-specific policies. Most production sandbox profiles use filter mode through libseccomp, a service manager or a runtime rather than hand-assembling BPF instructions.

### Check architecture before syscall number

Syscall numbers are meaningful only within an ABI. A kernel may support native and compatibility ABIs simultaneously, and the same number can name different operations. First compare `arch` to explicitly supported audit architectures, then dispatch on number. Kill or otherwise fail closed on an unexpected ABI.

### Account for ABI aliases and multiplexors

Equivalent behavior may be reachable through old and new syscalls, compatibility entry points, multiplexed calls or library fallbacks. Conversely, one syscall name may translate differently across architectures. Generate and test profiles for the deployed ABI set; do not paste a numeric table from another platform.

### Prefer allowlist defaults for strong reduction

With a reject-by-default profile, a new kernel syscall remains unavailable until intentionally admitted. A denylist is easier to deploy but silently admits new or forgotten alternatives. Allowlisting increases compatibility work and should be built from both observed execution and reasoning about rare failure and recovery paths.

### Choose failure actions deliberately

Actions include process or thread kill, trap with `SIGSYS`, errno return, trace, log, user notification and allow. Kill sharply contains unexpected behavior but supplies less graceful recovery. Errno preserves process control flow but applications may retry or select a more dangerous fallback. Logging alone observes; it does not deny.

### Query supported actions at runtime

Kernel action support evolves. Use seccomp operations and `/proc/sys/kernel/seccomp/actions_avail` rather than assuming build headers match the running kernel. Unknown return actions are treated restrictively by the kernel, but a profile compiler or runtime should reject unsupported policy before starting the workload.

### Understand filter stacking and precedence

A thread can add filters but cannot remove earlier ones. On each syscall, all installed filters execute and the highest-precedence action wins; later installation does not simply override an earlier decision. This monotonic restriction supports layered sandboxing but adds evaluation cost and makes profile debugging require the entire filter tree.

### Set no_new_privs for unprivileged installation

An unprivileged thread normally sets `PR_SET_NO_NEW_PRIVS` before installing a filter. The bit persists across fork, clone and exec and cannot be unset. It prevents exec-time set-ID bits and file capabilities from granting new privilege, but does not block every non-exec credential or descriptor transfer.

### Install filters in a safe order

Perform privileged setup, open deliberately retained resources, establish namespaces and object policy, drop excess authority, set `no_new_privs`, then install the final filter before untrusted code runs. If later setup needs forbidden calls, move it to a trusted supervisor instead of temporarily running untrusted code without the profile.

### Synchronize multithreaded processes

Filters are per-thread state inherited by newly created threads. `SECCOMP_FILTER_FLAG_TSYNC` attempts to synchronize the new filter across the process's threads and reports a failing thread when synchronization is impossible. Install before thread creation where feasible and verify every thread, rather than assuming process-wide application.

### Preserve policy through fork and exec

If fork or clone is allowed, children inherit filters; if exec is allowed, filters survive the image change. The new program may need a different syscall set but cannot weaken inherited policy. Design the profile for the entire permitted exec graph or prohibit unexpected execution.

### Compare scalar arguments with exact widths

Seccomp can compare integer, flag, descriptor-number and pointer-value slots. The kernel syscall may later interpret only part of a slot, so account for sign extension and truncation. Masked comparisons are useful for flag sets, but rejecting unknown bits must match the kernel's actual argument contract.

### Do not dereference pointer arguments

A pathname argument appears only as an address. Classic seccomp cannot safely read the string or know what filesystem object it resolves to. Target memory can also change concurrently. Use mounts, permissions, LSMs, Landlock or carefully brokered operations for object-aware decisions.

### Treat file descriptors as existing authority

Allowing `read`, `write`, `ioctl`, `mmap` or `sendmsg` may expose very different powers depending on inherited descriptors. Inventory and close unintended files, directories, devices, sockets, namespace handles, BPF objects and pidfds before sandbox entry. Descriptor provenance matters more than its small integer value.

### Recognize multiplexed kernel interfaces

`ioctl`, `fcntl`, `prctl`, `bpf`, `perf_event_open`, socket operations and asynchronous submission interfaces expose many suboperations. Argument filters can narrow numeric commands, but nested structures and referred objects are not visible to classic seccomp. Apply subsystem-specific permissions and avoid admitting broad multiplexors casually.

### Make errno behavior part of security policy

Returning `EPERM`, `EACCES`, `ENOSYS` or another errno changes application behavior. Libraries may use `ENOSYS` to select a legacy syscall, while applications may retry permission errors or disable a feature. Test the selected errno through all supported versions and error paths; denial is not equivalent across return codes.

### Use SIGSYS traps only with a defined handler

`SECCOMP_RET_TRAP` delivers `SIGSYS` with syscall metadata. A handler can record or emulate limited behavior, but signal safety, register conventions and recursion matter. An absent or unsafe handler terminates or corrupts the process. Do not build a general privileged broker inside the compromised address space.

### Treat ptrace-based decisions cautiously

Trace actions hand decisions to an attached tracer and couple sandbox security to ptrace permissions and kernel-version behavior. A tracer is a powerful part of the TCB. Prefer a more direct mechanism when possible, and never assume the trace action denies a call when no correctly configured tracer exists.

### Understand user-notification flow

A filter installed with a new-listener flag can return `USER_NOTIF`, causing the target to block while a supervisor receives syscall metadata. The supervisor may return an error or value, continue the original call, or for supported operations inject a file descriptor. The listener's custody and supervisor availability become security and liveness dependencies.

### Validate notification identity and lifetime

Notification IDs can become stale if the target exits or the request is interrupted. Use the ID-validity operation at the required points and handle PID reuse and concurrent lifecycle. Size notification structures through the kernel query so userspace and kernel versions agree.

### Eliminate broker TOCTOU assumptions

Arguments that point into target memory can change while the supervisor inspects them. Reading a path, approving it and telling the kernel to continue may authorize different bytes at execution. Prefer performing the sensitive operation in the supervisor using race-resistant resolution and injecting the resulting descriptor rather than continuing the target's path-based call.

### Minimize broker authority

Run the broker with only the namespaces, mounts, descriptors and capabilities needed for the delegated operation. Bind each request to a workload and policy version, validate flags and object types, bound queues and timeouts, and fail closed if the broker dies. A universal root broker turns a sandbox into a confused-deputy interface.

### Negotiate Landlock ABI support

Landlock allows unprivileged processes to restrict themselves with rulesets. Query the supported ABI and handle only rights known to the running kernel. A best-effort compatibility mode must clearly disclose missing protections; high-assurance workloads may need to refuse startup when required rights are unavailable.

### Build Landlock rules by handled rights

A ruleset declares which access rights it handles, making those rights denied by default unless a rule grants them. Rights not declared as handled are outside that layer's restriction. Add path-beneath and supported network rules, then call restrict-self after setting `no_new_privs` as required.

### Use Landlock's monotonic stacking

Enforced Landlock layers compose by requiring all layers and other access-control mechanisms to permit an operation. A child may add restriction but cannot use a new layer to recover access denied by an ancestor. Track the finite layer budget and build coherent rulesets instead of stacking on every helper call.

### Keep object views stable around policy

Landlock rules refer to objects and hierarchies, while mount and rename operations can change reachable topology. Establish the intended mount namespace and mounts before enforcing the policy. Account for bind mounts, OverlayFS and already-open descriptors according to the supported ABI and documented limitations.

### Drop capabilities by all relevant sets

Remove unnecessary bounding, permitted, effective, inheritable and ambient capabilities, considering user-namespace scope. A seccomp-allowed syscall still performs normal capability checks, but retained capabilities can make that call powerful. Seccomp is defense in depth, not a replacement for least privilege.

### Use namespaces to reduce visible targets

Mount, PID, network, IPC, UTS, user, cgroup and time namespaces change which objects and identifiers calls can reach. Build their state before the final profile and close namespace handles. Namespaces do not filter syscalls or guarantee resource limits, so preserve each layer's claim.

### Apply mount and LSM policy for objects

Read-only, `nosuid`, `nodev` and `noexec` mount attributes reduce filesystem authority. SELinux, AppArmor or another LSM can enforce labels and transitions across objects. Landlock enables application-managed additional restrictions. These controls understand context that seccomp's numeric interface does not.

### Bound denial-of-service impact

Allowed calls can consume CPU, memory, I/O, PIDs, file descriptors and kernel objects. Apply cgroups, rlimits, quotas and admission controls. A process that cannot mount or ptrace can still exhaust its host through permitted allocation and creation paths if resources are unbounded.

### Map high-level profiles to generated filters

OCI and systemd profiles describe syscall names, architectures, actions and argument comparisons, then a runtime or libseccomp resolves them into kernel filters. Record tool and syscall-table versions. Inspect generated behavior because names, groups and availability change, and a high-level profile is not itself installed enforcement.

### Design observability without leaking authority

Audit denials with workload identity, architecture, syscall, action and policy version. Rate-limit logs so a hostile loop cannot exhaust I/O. Test kill, trap and broker-loss paths because some actions cannot emit normal application logs. Debug modes that replace deny with log must never be mistaken for production enforcement.

### Test compatibility beyond happy paths

Exercise startup, steady load, signals, DNS, locale, time, entropy, threading, memory pressure, failures, upgrades, shutdown and crash reporting. Test every supported architecture and libc. Run negative probes for equivalent syscalls, forbidden flag combinations, inherited descriptors and broker races.

### Reassess policy when software changes

Compiler, libc, runtime, dependency, kernel and configuration changes can alter syscall use. Version profiles with artifacts and regenerate evidence during release. Avoid automatically widening production policy from traces: traces reveal observed need, not whether an operation is safe.

## Definitions and Notation

Let a syscall event be

$$
x=(a,n,ip,v_0,\ldots,v_5),
$$

where $a$ is the audit architecture, $n$ the syscall number, $ip$ the instruction pointer and $v_i$ the six scalar argument slots. A seccomp filter is a total function $f:x\mapsto r$ returning an action and optional data.

For installed filters $f_1,\ldots,f_k$, let $\prec$ denote kernel action precedence. The effective action is

$$
R(x)=\max_{\prec}\{f_1(x),\ldots,f_k(x)\}.
$$

This models action selection only; query the running kernel for supported ordering and interpret action data under the selected action's contract.

Let $S$ be the set of admitted syscall events and $O$ the objects reachable through credentials, namespaces, mounts and open handles. A useful sandbox authority model is

$$
Authority \subseteq S\cap O\cap C\cap Q,
$$

where $C$ represents object and credential policy and $Q$ resource quotas. The intersection is conceptual because the mechanisms govern different dimensions and stages.

For a broker request observed at times $t_1$ and $t_2$, pointer-backed target memory $m(t)$ is raceable unless the protocol establishes otherwise:

$$
m(t_1)=m(t_2)
$$

cannot be assumed. Performing a validated operation and transferring its resulting descriptor avoids relying on that equality for pathname authorization.

## Mechanisms, Invariants, or Proof Structure

Review a sandbox with these obligations.

1. **ABI obligation:** each allowed architecture and syscall-number table is explicit and tested.
2. **Default obligation:** unknown operations receive the intended fail-closed action and errno semantics.
3. **Installation obligation:** setup order, `no_new_privs`, thread synchronization, fork and exec preserve coverage.
4. **Composition obligation:** all stacked filters and action precedence produce the intended effective result.
5. **Argument obligation:** widths, masks and pointer opacity are honored without inventing object semantics.
6. **Handle obligation:** inherited descriptors and multiplexed interfaces expose only intended authority.
7. **Broker obligation:** notification identity, race resistance, privilege, liveness and result injection are bounded.
8. **Object obligation:** Landlock, LSM, mounts and permissions constrain allowed calls to intended resources.
9. **Identity obligation:** user namespaces and capability sets establish least privilege before untrusted execution.
10. **Resource obligation:** cgroups, rlimits, quotas and admission bound permitted consumption.
11. **Evidence obligation:** denials, compatibility paths, equivalent operations and policy versions are observable and tested.
12. **Assurance obligation:** attack-surface reduction, object isolation, resource control and exploit prevention remain separate claims.

The proof first establishes filter coverage for every execution thread and ABI. It evaluates each reachable syscall through every installed filter, then overlays descriptor, credential, namespace, object and quota authority. Finally it treats brokers and supervisors as principals with their own inputs, races and failure modes. A short allowlist is evidence of neither correct compatibility nor complete containment by itself.

## Alternatives and Trade-Offs

- **Allowlist versus denylist:** allowlists fail closed on new syscalls; denylists ease compatibility and retain unknown attack surface.
- **Kill versus errno:** kill sharply terminates violations; errno supports recovery and can activate surprising fallback paths.
- **Trap versus log:** trap enables in-process handling with signal complexity; log observes without enforcement.
- **Static allow versus user notification:** static rules minimize TCB and latency; notification supports dynamic decisions through a privileged broker.
- **Broker continue versus descriptor injection:** continuing preserves native execution and pathname races; injection lets the broker resolve an authorized object.
- **Install before versus after initialization:** early filters reduce exposure; later filters support setup and create an unfiltered interval.
- **One filter versus stacked filters:** one filter simplifies analysis; layers allow independent components to add monotonic restrictions.
- **Per-thread versus TSYNC installation:** per-thread policy supports specialization; synchronization reduces inconsistent process coverage.
- **Native-only versus compatibility ABIs:** native-only narrows syscall tables; compatibility supports legacy binaries and expands analysis.
- **Argument filtering versus syscall-only rules:** arguments narrow flags and commands; complex or pointer-backed semantics exceed classic seccomp.
- **Landlock versus privileged LSM policy:** Landlock enables self-restriction; administrator LSMs can impose broader system policy.
- **Namespace isolation versus host views:** isolated views reduce reachable objects; shared views simplify integration and enlarge consequences.
- **Preopened descriptors versus broker access:** preopening removes runtime resolution; brokers support dynamic resources with more TCB.
- **Generated groups versus explicit syscall names:** groups improve maintainability; explicit names make reviewed policy boundaries clearer.
- **Fail closed versus compatibility fallback:** refusal preserves stated protection; fallback maintains service with disclosed reduced assurance.
- **Production deny versus learning log:** deny enforces policy; learning mode gathers evidence and must remain operationally distinct.

## Failure Modes and Misconceptions

- “Seccomp is a complete sandbox.” It filters syscall entry and needs complementary controls.
- “Syscall numbers are universal.” They are ABI-specific.
- “Checking the native architecture covers compatibility calls.” Each enabled ABI needs policy.
- “A denylist blocks dangerous behavior.” Equivalent and future syscalls can remain admitted.
- “An allowlist generated from one trace is complete.” Rare error and lifecycle paths may be absent.
- “ERRNO is always safer than kill.” Error handling can retry or fall back dangerously.
- “LOG denies the call.” It records and permits it.
- “The newest filter overrides old filters.” All run and action precedence selects the result.
- “A child can remove an inherited filter.” Seccomp restriction is monotonic.
- “no_new_privs drops all privilege.” It constrains privilege gain through exec, not every authority channel.
- “A filter installed on one thread covers its siblings.” Thread coverage requires ordering or synchronization.
- “exec clears seccomp.” Installed filters persist across permitted exec.
- “A pathname argument can be string-matched by classic seccomp.” The filter sees its pointer value.
- “A file-descriptor number identifies its object class.” The table and provenance define its authority.
- “Allowing ioctl is one operation.” It multiplexes device-specific commands.
- “Argument slots equal kernel parameter widths.” Syscall interpretation may truncate or sign-extend.
- “ENOSYS and EPERM are interchangeable.” Libraries may choose different fallback behavior.
- “A SIGSYS handler is automatically safe.” Signal context, registers and recursion need careful design.
- “USER_NOTIF gives object-aware policy for free.” The broker must defeat pointer races and confused-deputy risks.
- “The notification PID can be trusted forever.” Requests become stale and identities race with lifecycle.
- “Continuing after path inspection executes the inspected path.” Target memory can change before execution.
- “Landlock replaces permissions and LSMs.” Its restrictions stack with other authorization.
- “Unsupported Landlock rights are automatically denied.” Only declared, supported handled rights are governed.
- “Dropping effective capabilities drops every capability path.” Other capability sets and user-namespace scope matter.
- “Namespaces prevent resource exhaustion.” Cgroups and limits govern consumption.
- “No denial logs means the sandbox works.” The filter may be absent, logging suppressed or probes incomplete.

## Worked Examples

### Example 1

An x86-64 process can invoke a compatibility ABI. A filter compares number first and allows a value that means a harmless native call but a different compatibility operation. Checking and rejecting unexpected architecture before number dispatch repairs the confusion.

### Example 2

The following executable toy composes abstract filter results by action precedence. It validates table lookup only, not kernel constants, BPF, syscalls, action data or installed-filter behavior.

<!-- bijux-verify: {"id":"seccomp-action-precedence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"read=ALLOW\nopenat=ERRNO\ngetpid=LOG\nptrace=KILL_PROCESS\n","stderr":""}} -->
```python
precedence = {
    "ALLOW": 0,
    "LOG": 1,
    "TRACE": 2,
    "USER_NOTIF": 3,
    "ERRNO": 4,
    "TRAP": 5,
    "KILL_THREAD": 6,
    "KILL_PROCESS": 7,
}

results = {
    "read": ["ALLOW", "ALLOW"],
    "openat": ["USER_NOTIF", "ERRNO"],
    "getpid": ["ALLOW", "LOG"],
    "ptrace": ["KILL_PROCESS", "ERRNO"],
}

for syscall, actions in results.items():
    effective = max(actions, key=lambda action: precedence[action])
    print(f"{syscall}={effective}")
```

### Example 3

A library receives `ENOSYS` for a modern time syscall and falls back to an older compatibility path that the profile accidentally allows. Returning `EPERM` would fail instead, but the durable fix is to reason about and filter both paths while testing supported library versions.

### Example 4

A process creates four threads, then its main thread installs a filter without TSYNC. One thread remains unrestricted and performs a forbidden mount. Installing before thread creation or successfully synchronizing and checking the result closes the gap.

### Example 5

A broker reads `/tmp/a` from target memory and approves it, but another target thread changes the bytes to `/etc/shadow` before the supervisor tells the kernel to continue. Resolving the approved path inside the broker's restricted view and injecting the opened descriptor avoids this pathname race.

### Example 6

A renderer may call `read` and `ioctl` but inherits a writable GPU device and a host namespace descriptor. The syscall list looks narrow, yet the handles are powerful. Closing the namespace descriptor and applying device-specific policy reduces actual authority.

### Example 7

A service installs a Landlock layer that handles filesystem writes and grants them only beneath `/var/lib/service`. Its mount namespace exposes read-only binaries and a writable data volume. An allowed `openat` still cannot write outside the granted hierarchy under the other checks.

### Example 8

An OCI profile specifies `SCMP_ACT_NOTIFY`, but the runtime cannot deliver its listener descriptor to the configured agent. Starting without notification would weaken policy, so creation fails closed and reports the unsupported broker path.

### Example 9

A service profile permits normal operation but omitted a syscall used only by crash reporting. The first production fault kills the reporter, losing evidence. Failure-injection tests add the narrowly required call without widening unrelated kernel interfaces.

### Example 10

A hostile process loops on a denied syscall with logging enabled. Audit volume saturates storage and obscures other incidents. Rate limiting, cgroup I/O bounds and aggregated counters preserve evidence without turning policy violations into a denial-of-service channel.

## Cross-Program Connections

- **Security engineering:** least privilege, LSM policy, confused deputies and defense in depth define the sandbox argument.
- **Platform engineering:** runtimes and service managers compile portable profiles and enforce lifecycle ordering.
- **API engineering:** syscall ABIs, argument widths, errno and compatibility behavior are security-relevant contracts.
- **Operating systems:** syscall dispatch, credentials, descriptors, namespaces, mounts and resource controllers compose enforcement.
- **Reliability engineering:** broker loss, error fallback, crash reporting and update compatibility determine safe availability.
- **Observability engineering:** denial records, policy versions, rate limits and negative probes make enforcement auditable.
- **Performance engineering:** filter depth, BPF evaluation, notification round trips and audit volume add overhead.
- **Formal methods:** monotonic policy intersections, total decision functions and explicit authority sets support review.
- **Distributed systems:** remote brokers and policy distribution create identity, availability and version-consistency concerns.
- **Supply-chain engineering:** executable and dependency changes must trigger profile compatibility and security review.

## References

1. Linux Kernel Documentation, [Seccomp BPF](https://docs.kernel.org/userspace-api/seccomp_filter.html), filter inputs, installation prerequisites, inheritance, stacking and actions; retrieved 2026-09-04.
2. Linux man-pages Project, [seccomp(2)](https://man7.org/linux/man-pages/man2/seccomp.2.html), operations, flags, filter data, action precedence, architecture and caveats; retrieved 2026-09-04.
3. Linux man-pages Project, [seccomp_unotify(2)](https://man7.org/linux/man-pages/man2/seccomp_unotify.2.html), notification lifecycle, ID validation, responses, descriptor injection and TOCTOU risks; retrieved 2026-09-04.
4. Linux Kernel Documentation, [No New Privileges Flag](https://docs.kernel.org/userspace-api/no_new_privs.html), exec-time privilege constraints, persistence and seccomp relationship; retrieved 2026-09-04.
5. Linux Kernel Documentation, [Landlock: Unprivileged Access Control](https://docs.kernel.org/userspace-api/landlock.html), ABI negotiation, rules, handled access, stacking, scopes and limitations; retrieved 2026-09-04.
6. Linux man-pages Project, [landlock(7)](https://man7.org/linux/man-pages/man7/landlock.7.html), ruleset construction, compatibility and security guidance; retrieved 2026-09-04.
7. Linux man-pages Project, [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html), capability sets, privileged operations and seccomp installation authority; retrieved 2026-09-04.
8. Open Container Initiative, [Linux Container Configuration](https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md), seccomp actions, architectures, comparisons, flags and listener handoff; retrieved 2026-09-04.
9. Linux man-pages Project, [systemd.exec(5)](https://man7.org/linux/man-pages/man5/systemd.exec.5.html), service syscall allowlists, denylists, groups, architectures and error behavior; retrieved 2026-09-04.
10. libseccomp, [seccomp_rule_add(3)](https://man7.org/linux/man-pages/man3/seccomp_rule_add.3.html), rule construction, argument comparisons and architecture handling; retrieved 2026-09-04.

## Exercises

### Exercise 1

Two installed filters return `USER_NOTIF` and `ERRNO` for `openat`; two others return `ALLOW` and `LOG` for `getpid`. Using the chapter's abstract precedence, give each effective action and explain why installation order is irrelevant.

### Exercise 2

A policy allows syscall number 9 without checking architecture. Explain the flaw and design the filter's initial dispatch for a native-only workload.

### Exercise 3

A broker wants to permit opening only files beneath `/srv/input`. Explain why reading the target's pathname and returning continue is unsafe, then design a descriptor-injection flow.

### Exercise 4

Design a sandbox for a document converter that reads one input, writes one output, needs no network and may process hostile formats. Name the role of seccomp, Landlock or LSM, namespaces, descriptors and resource controls.

### Exercise 5

Design a compatibility and negative-test plan for changing a service from a syscall denylist to an allowlist across two architectures and two libc versions.

## Answers to the Exercises

### Answer 1

`ERRNO` has higher precedence than `USER_NOTIF` in the abstract table, so the notification is not the effective result for `openat`. `LOG` has higher precedence than `ALLOW`, so `getpid` is logged and allowed according to log-action semantics.

Every installed filter evaluates the same event, and the kernel selects by action precedence rather than newest-filter wins. Installation order affects which filters exist at a moment in lifecycle, but not precedence among results once all are installed. Production code must query supported actions and follow the running kernel's exact contract.

### Answer 2

The number is ambiguous without an audit architecture: another ABI can assign it to a different operation or interpret arguments differently. A process on a multi-ABI kernel might deliberately switch calling convention and reach behavior the native table did not intend to allow.

The filter first loads and compares `seccomp_data.arch` with the one audited native architecture. On mismatch it returns a fail-closed action such as process kill. Only in the matching branch does it load `nr` and compare it with the generated native syscall table. Test that compatibility binaries and direct compatibility syscall probes receive the expected rejection.

### Answer 3

The pathname is stored in target memory that another target thread can modify after inspection. The target's mount namespace, directory file descriptors, current directory and symlinks also affect resolution. Returning continue asks the target kernel path to resolve state that may differ from what the broker authorized.

Keep the target blocked, validate the notification ID, copy and bound the requested data only as input, then have a minimally privileged broker resolve the path beneath an already-open `/srv/input` directory using race-resistant resolution and restricted flags. Validate the resulting object and inject its descriptor with the notification add-file-descriptor operation. Revalidate the request at documented points, return the injected descriptor result atomically where supported, and fail closed on stale ID, broker loss or unsupported flags.

### Answer 4

The launcher opens the authorized input and newly created output, passes only those descriptors, closes directory, device, socket and namespace handles, constructs isolated mount, PID and network views, and exposes a read-only runtime with bounded scratch space. No network interface or socket handle is available. It drops every unnecessary capability and sets `no_new_privs`.

Landlock or an administrator LSM restricts file access to the runtime, input, output and scratch objects; mount policy makes binaries read-only and blocks devices. Seccomp then allowlists computation, descriptor I/O, memory management, threading, signals, time and exit while rejecting mount, namespace, ptrace, BPF, module and unneeded networking paths. Cgroups and rlimits bound CPU, memory, I/O, PIDs, descriptors and output size. A supervisor outside the sandbox enforces timeout, captures exit and can kill the subtree.

### Answer 5

Inventory native and compatibility ABIs for both architectures, kernel action support, syscall tables, profile compiler versions and the two libc builds. Trace startup, steady load, concurrency, DNS if used, signals, pressure, errors, crash handling, reload, upgrade and shutdown for every binary and plugin combination. Review source and dependency changes to add rare required paths absent from traces.

Run the allowlist first in an isolated learning environment with production-like inputs while keeping logging rate-limited. Negative tests invoke alternate and compatibility syscalls, forbidden flag variants, multiplexed commands, exec transitions, inherited-descriptor attacks and thread races. Verify unknown syscalls fail closed, selected errno does not activate unsafe fallback, every thread is covered, and object/cgroup controls contain allowed calls. Promote a versioned explicit profile only after all four architecture/libc matrices pass; retain rollback to the previous enforced policy rather than an unfiltered mode.
