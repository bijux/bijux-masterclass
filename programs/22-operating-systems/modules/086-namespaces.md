---
module_id: OS-086
program: Operating Systems
level: 2
module_number: 86
title: Namespaces
status: complete
last_verified: 2026-09-04
---

# Namespaces

## One-Page Review

### Governing question

How does an operating system give groups of processes distinct views and identifiers for shared kernel resources without pretending that view isolation alone is containment?

### Essential definitions

- A **namespace** is a kernel object that scopes a process's view of one resource class.
- A process's **namespace vector** contains one membership for each supported namespace type.
- **clone** creates a process and can create selected new namespaces; **unshare** moves the caller or its future children away from shared contexts; **setns** joins namespaces referenced by file descriptors.
- A **user namespace** scopes user and group identifiers and capabilities.
- A **PID namespace** gives processes hierarchical process identifiers and visibility.
- A **mount namespace** gives processes a mount-tree view with propagation relationships.
- A **network namespace** owns network devices, protocol stacks, routes, filters, sockets and related state.
- A **namespace handle** is an open reference, commonly through `/proc/PID/ns`, that can preserve and later join an otherwise empty namespace.

### Central model, mechanism, or theorem

Namespaces virtualize selected global names and views by making kernel lookups relative to a process's namespace membership. They compose independently: two processes may share a network namespace but have different mount or PID namespaces. Access remains governed by credentials, capabilities in the owning user namespace, object permissions, cgroups, LSM policy, seccomp and non-namespaced resources. A useful isolation claim must name the entire namespace vector and every additional control.

### Critical invariants

- Each namespaced lookup uses the caller's correct namespace object and lifetime reference.
- Capabilities are interpreted in the user namespace that owns the governed namespace or resource.
- UID and GID mappings are explicit, nonoverlapping and bounded.
- PID visibility follows namespace ancestry; namespace PID 1 receives special lifecycle duties.
- Mount propagation cannot unexpectedly export container mounts to the host.
- Namespace destruction occurs only after processes and persistent handles release it.
- Global or shared resources are never described as isolated merely because adjacent state is namespaced.

### Common failures

A launcher creates namespaces in an unsafe order, maps container root to host root, forgets to make a mount subtree private, mounts host `/proc` inside the wrong PID namespace, joins a PID namespace expecting the caller's PID to change, leaves namespace file descriptors open, or assumes a cgroup namespace imposes resource limits.

### Compact example

A user namespace maps inside UIDs 0–999 to outside UIDs 100000–100999. UID 0 inside is unprivileged UID 100000 outside, but can hold capabilities over resources owned by that user namespace. UID 1000 is unmapped and cannot be translated through that range. The mapping changes identity representation; it does not grant host-root authority.

### Connections

Namespaces connect process credentials, mount trees, network stacks, cgroups, capabilities, container runtimes, procfs, checkpoint/restore and least-privilege sandboxing.

## Governing Question

Traditional Unix exposes system-wide process IDs, hostnames, mounts, network interfaces and IPC names. Containers need several mutually inconsistent views of those resources on one kernel. The governing question is how namespace-relative lookup supplies those views while preserving clear ownership, privilege and lifecycle rules.

## Why This Matters

Namespaces are often presented as “containers,” but Linux provides namespace mechanisms rather than one container object. A runtime creates a particular combination, populates filesystems and networking, drops capabilities, applies cgroups and security policy, then launches an init process. Missing one dimension can expose host state or couple tenants.

Subtle semantics matter operationally. PID namespaces are hierarchical; mount propagation is a graph orthogonal to the directory tree; joining a PID namespace affects future children; user namespace capabilities are scoped; open descriptors cross mount and network view changes; and cgroup namespaces change displayed paths without moving processes or enforcing limits. Reliable isolation depends on these details.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain processes, threads, credentials, capabilities and file-descriptor inheritance;
- describe VFS mounts, bind mounts, procfs, sysfs and path lookup;
- reason about PID parentage, signals, reaping and process groups;
- describe interfaces, routes, sockets, firewall rules and network devices;
- distinguish naming isolation, access control, accounting and resource scheduling.

Retrieve the exact kernel and Linux man-pages version, enabled namespace configuration, runtime, helper tools, LSM policy, seccomp profile, cgroup mode, filesystem and network setup. Record the launcher credentials, UID/GID maps, capability sets, mount propagation and persistent namespace handles.

## Learning Objectives

After completing this module, you should be able to:

1. model namespace membership as a per-process vector of independently shareable contexts;
2. use clone, unshare and setns semantics without confusing caller and child effects;
3. reason about user-namespace ownership, identifier maps and scoped capabilities;
4. explain PID hierarchy, namespace init and procfs mounting;
5. control mount-tree cloning, bind mounts and shared-subtree propagation;
6. describe network, IPC, UTS, cgroup and time namespace scope;
7. identify descriptors, global resources and policies that cross namespace boundaries;
8. validate a namespace-based isolation design through state and adversarial tests.

## Core Exposition

### Model membership per namespace type

A task points to namespace objects for user, PID, mount, network, IPC, UTS, cgroup and time views. Threads usually share many contexts, but API and threading constraints differ. Ask “which namespace of which type?” rather than “which container?” Two workloads can intentionally share networking while isolating mounts and PIDs.

### Distinguish names from resources

A namespace often changes lookup and presentation, not the underlying kernel implementation. Multiple network namespaces share one kernel; PID namespaces assign multiple IDs to one task; mount namespaces reference the same filesystem objects through different trees. Isolation is enforced at namespace-specific boundaries plus ordinary access control.

### Create namespaces with clone or clone3

Clone flags can create a child in new selected namespaces while retaining others. The child begins with inherited process state plus new namespace membership according to each type. Namespace creation can fail from privilege, nesting or per-user limits. Treat partial setup as a lifecycle that must be rolled back.

### Use unshare with type-specific effects

`unshare()` separates selected execution contexts for the calling process, but not every flag moves the caller in the same intuitive way. Creating a new PID or time namespace with unshare establishes the namespace for subsequently created children. Existing threads and shared filesystem attributes can impose restrictions. Consult each flag's contract.

### Join by descriptor with setns

`setns()` joins one or more namespaces referenced by descriptors, including descriptors obtained from `/proc/PID/ns` or a PID descriptor. The caller must satisfy type-specific ancestry, threading and capability rules. Joining multiple namespaces one call at a time can leave an intermediate mixed vector; launch a helper or use an atomic supported interface where partial transition is unsafe.

### Treat namespace handles as capabilities

An open namespace file descriptor keeps the object alive and authorizes a later join subject to permission checks. Bind-mounting a namespace handle also persists it. Inventory and close these references on teardown. A namespace with no member processes may remain intentionally or accidentally reachable.

### Inspect identity through procfs carefully

Entries under `/proc/PID/ns` identify namespace objects, and equal device/inode identities indicate shared instances for a type. What PIDs and mount information a process can read depends on its namespaces and procfs mount. Host observers should record both outer task identity and inner IDs to avoid ambiguous incident evidence.

### Make user namespaces the privilege frame

User namespaces isolate UIDs, GIDs and capabilities. A process can appear as UID 0 and hold capabilities inside while mapping to an unprivileged outer UID. Capabilities are meaningful relative to a user namespace and govern resources owned by it or descendant relationships defined by the kernel. “Root in a container” is incomplete without this scope.

### Define UID and GID maps before privilege use

Mapping files describe nonoverlapping ranges from IDs inside a namespace to IDs in the parent view. Only mapped IDs translate. Writes are tightly constrained and generally one-time setup operations. GID mapping interacts with the `setgroups` control to prevent gaining supplementary groups through an unsafe mapping sequence.

### Understand namespace ownership

Each non-user namespace is owned by the user namespace of its creator. Privileged operations over that namespace commonly require the relevant capability in its owning user namespace. Creating a user namespace first can allow an otherwise unprivileged process to create other owned namespaces, but does not confer capabilities in the initial user namespace.

### Reduce user-namespace attack surface consciously

Unprivileged user namespaces expose kernel paths that traditionally required host privilege, while scoping resulting power. They enable rootless containers and sandboxes but can enlarge reachable kernel code. Decide enablement, nesting and workload policy from the threat model and patch posture rather than treating them as universally safe or unsafe.

### Follow PID namespace ancestry

PID namespaces form a hierarchy. A process has one PID in its own namespace and an ID in each ancestor namespace. A process can see tasks in its namespace and descendants, not ancestor-only tasks. Host PID identity therefore differs from the number shown inside a container.

### Respect namespace PID 1

The first process in a PID namespace becomes its init. It reaps orphaned descendants and has special signal behavior. If it terminates, the kernel terminates remaining members and future process creation in that namespace fails. A production container needs an init strategy that forwards signals and reaps children.

### Understand PID setns direction

Joining a PID namespace changes the namespace in which future children are created; it does not retroactively change the caller's PID namespace membership. The target must satisfy descendant constraints. Tooling that expects its own PID to become 1 after `setns()` will observe surprising results unless it forks.

### Mount procfs for the intended PID view

Procfs presents process information relative to the PID namespace associated with the mount. Reusing a host procfs mount inside a new mount namespace can expose the wrong task view. After creating the PID namespace and child, mount a suitable procfs instance within the child's mount namespace.

### Treat a mount namespace as a mount tree

Creating a mount namespace clones the caller's mount list, not file contents. Mount, unmount, bind and move operations can then change that view. Processes in different mount namespaces may still access the same inode and backing device through different paths.

### Control shared-subtree propagation

Shared mounts propagate events among peers; slave mounts receive from a master without sending back; private mounts neither send nor receive; unbindable mounts are private and cannot be bind-cloned. Propagation relationships form a graph orthogonal to directory ancestry. Make container roots appropriately private or slave before mounting inside them.

### Distinguish chroot, pivot and mount isolation

Changing a process root affects path resolution but does not itself create a mount namespace or close open descriptors. `pivot_root`, bind mounts and unmounting old roots can construct a filesystem view, while capabilities and open handles determine escapes. Container filesystem isolation is a composition, not one syscall.

### Account for open file descriptors

An open file, directory, socket or device descriptor continues to reference its object after namespace changes, subject to that object's semantics. Joining a mount namespace does not revoke a directory descriptor into the old tree. Launchers must close unintended descriptors before executing the workload.

### Isolate network stacks explicitly

Network namespaces scope interfaces, protocol state, routes, firewall rules, network sysctls, port number space and abstract Unix sockets. A physical device belongs to one network namespace at a time. A new namespace requires explicit loopback and link configuration before applications have expected connectivity.

### Connect network namespaces through devices

A veth pair supplies two linked endpoints that can live in different namespaces. Bridges, routing, NAT or policy attach the container side to wider networks. Crossing the namespace boundary is intentional connectivity, not isolation failure, but its filters and ownership must be explicit.

### Track network namespace lifetime

Sockets and namespace descriptors can keep a network namespace alive after its apparent init exits. Virtual links can be destroyed when the namespace disappears; physical devices return according to kernel rules. Teardown must drain sockets, remove policy and verify device placement rather than keying only on one process.

### Use IPC namespaces for specific facilities

IPC namespaces isolate System V IPC objects and POSIX message queues. They do not automatically isolate file-backed communication, network sockets, shared filesystem paths or inherited descriptors. Enumerate the actual IPC mechanism instead of assuming `CLONE_NEWIPC` covers every interprocess channel.

### Use UTS namespaces for identity views

UTS namespaces isolate hostname and NIS domain name. These values influence discovery and logs but do not secure DNS, network routes, certificates or platform metadata. A container hostname is an application-facing identity hint, not a cryptographic principal.

### Understand cgroup namespace scope

A cgroup namespace virtualizes the cgroup paths shown through proc and mount information relative to namespace roots. It does not create cgroups, move processes, set limits or change controller behavior. Resource governance comes from cgroup membership and configuration, covered separately.

### Understand time namespace scope

Time namespaces apply offsets to specified clocks such as monotonic and boot-time views for member processes. They do not provide arbitrary clock rates or isolate every clock. Correct setup occurs before children depend on time, and applications must still handle wall-clock synchronization and external timestamps.

### Recognize non-namespaced kernel state

Not every sysctl, kernel log, device, filesystem, security key, performance counter or hardware resource is namespaced. Exact scope changes over kernel versions. Deny access or virtualize through other mechanisms where needed. A nearby namespaced `/proc` path does not prove the underlying control is per namespace.

### Compose with capabilities and LSM policy

Drop bounding, permitted, effective, inheritable and ambient capabilities to the workload minimum. Apply SELinux, AppArmor or another LSM to objects and transitions that namespaces do not distinguish. Capability checks and LSM checks are complementary; passing one does not bypass the other.

### Compose with seccomp

Seccomp limits which system calls and argument patterns a process may invoke. It can reduce kernel attack surface after namespace setup. It is not an object authorization system and cannot decide that one otherwise valid path belongs to another tenant. Install it after required setup or delegate setup to a narrow supervisor.

### Compose with cgroups and rlimits

Namespaces do not constrain CPU, memory, I/O or process creation merely by hiding identifiers. Cgroups allocate and account shared resources; rlimits constrain selected per-process or per-user quantities. PID namespace isolation without process limits remains vulnerable to fork-based exhaustion.

### Define container lifecycle as orchestration

A runtime creates namespace objects, mappings, mounts, links, cgroups and policy, then launches the namespace init. Startup needs a parent-child synchronization point so the child cannot execute privileged workload code before mappings and restrictions are ready. Teardown reverses external links and verifies persistent handles.

### Avoid mixed-namespace confusion

Debuggers, sidecars and administrative tools often join only some namespaces. Their `/proc`, paths, sockets and credentials can refer to different worlds. Record the full vector before an action. Enter user and mount contexts in an order consistent with capability and path requirements.

### Preserve namespace identity in checkpoint and restore

Checkpointing must record membership sharing and hierarchy, not just per-process flags. Restore recreates user mappings, PID ancestry, mount propagation, network objects, IPC state and persistent handles in a valid order. External connections and host-global resources need explicit reconciliation.

### Observe from inside and outside

Collect namespace object identifiers, inner and outer PIDs and IDs, mount propagation, device placement, routes, cgroup membership and capability scope. Logs should correlate a durable workload identity rather than only PID or hostname, which can repeat across namespaces.

### Test the negative space

From the workload, attempt to enumerate host PIDs, mounts, interfaces, IPC objects and cgroup paths; exercise prohibited capabilities; inspect leaked descriptors; create mounts and test propagation; exhaust processes; and access non-namespaced sysctls. From the host, verify teardown and ownership. Passing a namespace-list check is not enough.

## Definitions and Notation

Let the namespace vector of process $p$ be

$$
N(p)=(U_p,P_p,M_p,Net_p,I_p,T_p,C_p,Time_p),
$$

for user, PID, mount, network, IPC, UTS, cgroup and time namespaces. Processes can agree on any subset of coordinates.

Let a UID mapping entry be $(i,o,\ell)$: inside start $i$, outside start $o$ and positive length $\ell$. For $x\in[i,i+\ell)$,

$$
map(x)=o+(x-i).
$$

IDs outside every configured interval are unmapped. Valid tables require ranges and translated ranges to satisfy kernel overlap and authorization rules.

Let $P_a$ be a PID namespace that is an ancestor of $P_b$. A task in $P_a$ may receive an ancestor-view PID for a task in $P_b$; the reverse view is not provided merely by hierarchy. Visibility remains subject to procfs and permission checks.

For operation $op$ on resource $r$ owned by user namespace $U_r$, a capability check is modeled as

$$
allowed(p,op,r)\Rightarrow cap_{op}(p,U_r)\land policy(p,op,r),
$$

where policy includes ordinary permissions and applicable security hooks. The implication is a necessary abstraction, not a complete kernel authorization formula.

## Mechanisms, Invariants, or Proof Structure

Review namespace isolation with these obligations.

1. **Vector obligation:** every process and helper has an explicit namespace membership for every relevant type.
2. **Ownership obligation:** each namespace's owning user namespace and capability requirements are known.
3. **Mapping obligation:** UID and GID ranges are authorized, nonoverlapping, bounded and configured before use.
4. **PID obligation:** hierarchy, namespace init, signal, reaping and procfs semantics preserve lifecycle.
5. **Mount obligation:** root construction, propagation and leaked descriptors cannot reach unintended trees.
6. **Network obligation:** devices, routes, filters, sockets, sysctls and teardown have explicit namespace owners.
7. **Scope obligation:** IPC, UTS, cgroup and time views are not credited with controls they do not provide.
8. **Persistence obligation:** process, descriptor and bind-mount references are tracked until deliberate destruction.
9. **Policy obligation:** capabilities, LSM, seccomp, cgroups and rlimits cover non-namespaced authority and resources.
10. **Lifecycle obligation:** creation, child release, checkpoint, restore and teardown use ordered, fenced transitions.
11. **Evidence obligation:** inner and outer identities, namespace objects and resource owners can be correlated.
12. **Assurance obligation:** naming, access, resource, kernel-attack-surface and side-channel claims remain separate.

The isolation argument examines each coordinate of $N(p)$, then every handle and resource that bypasses namespace-relative lookup. It overlays credential and policy checks, resource governance and lifecycle. One new namespace proves only a change in one view.

## Alternatives and Trade-Offs

- **New versus shared namespace:** a new view improves separation; sharing simplifies communication and observability.
- **clone versus unshare:** clone creates a child with selected contexts; unshare transforms the caller or future-child context.
- **setns versus fresh creation:** joining reuses existing state; creation starts a separately owned instance.
- **Persistent handle versus process lifetime:** handles enable management; leaked handles prevent teardown.
- **Rootless versus privileged launcher:** rootless user namespaces reduce host identity privilege; privileged launchers support broader setup and increase authority.
- **Broad versus narrow ID maps:** broad maps improve compatibility; narrow maps reduce represented host identities.
- **Private versus slave mounts:** private trees block both directions; slave trees receive host updates without exporting container mounts.
- **Bind mounts versus image assembly:** binds efficiently expose host objects; image assembly narrows accidental host coupling.
- **Host versus namespace procfs:** host proc aids administration; namespace proc presents correct inner PID view.
- **Dedicated versus shared network namespace:** dedication isolates stacks; sharing reduces virtual hops and couples ports and policy.
- **Physical device move versus virtual link:** device moves reduce layers; virtual links retain host mediation and flexibility.
- **Shared versus isolated IPC:** sharing enables low-cost cooperation; isolation reduces unintended object discovery.
- **Cgroup path hiding versus full host paths:** relative views reduce topology leakage; full paths aid host diagnosis.
- **Time offsets versus host time:** offsets support restore and testing; host time simplifies external correlation.
- **Static setup versus dynamic joining:** static vectors are auditable; dynamic setns supports operations and mixed-context risk.
- **Namespace-only versus layered sandbox:** namespace-only is simpler; layered controls address resources and non-namespaced state.

## Failure Modes and Misconceptions

- “A namespace is a container.” A runtime composes several namespaces and controls.
- “A process belongs to one namespace.” It has one membership per namespace type.
- “Different PIDs mean different tasks.” One task has IDs in multiple PID namespaces.
- “clone, unshare and setns have the same effect.” Caller, child and future-child semantics differ.
- “setns into PID changes the caller's PID.” It changes where future children are created.
- “No processes means the namespace is gone.” Open descriptors and bind mounts can retain it.
- “UID 0 inside is host root.” User-namespace ownership and mappings scope its power.
- “Capabilities are global booleans.” They are interpreted relative to a governing user namespace.
- “An unmapped ID becomes nobody by policy.” Translation and syscall behavior are operation-specific.
- “Writing uid_map and gid_map is unrestricted.” Authorization, order and setgroups rules constrain them.
- “PID 1 is an ordinary process.” It has reaping and signal responsibilities.
- “A new PID namespace automatically gives correct `/proc`.” The procfs mount must match the intended view.
- “A mount namespace copies files.” It clones a mount view over shared filesystem objects.
- “Private paths imply private propagation.” Shared-subtree state determines mount-event propagation.
- “chroot closes the old tree.” Open descriptors and privileges can retain access.
- “Joining a mount namespace revokes old descriptors.” Existing handles remain object references.
- “A network namespace is one interface.” It scopes a protocol stack and many related resources.
- “A veth pair is an isolation policy.” It is a link; routing and filtering define reachability.
- “IPC namespace isolates all IPC.” Files, sockets and inherited descriptors use other mechanisms.
- “Hostname isolates identity.” UTS values are not authentication principals.
- “Cgroup namespace applies limits.” It virtualizes path views, not controller policy.
- “Time namespace virtualizes every clock.” Only specified clocks and offsets are covered.
- “Every sysctl is namespaced.” Scope is subsystem- and version-specific.
- “Namespaces stop denial of service.” Cgroups, rlimits and admission govern resources.
- “Listing expected namespaces proves containment.” Leaked handles and global resources need negative tests.

## Worked Examples

### Example 1

Two processes share user and network namespaces but have different PID and mount namespaces. They use the same port space and scoped capabilities, yet see different process trees and filesystem mounts. Labeling them simply “same container” or “different container” loses the relevant facts.

### Example 2

The following executable toy translates IDs through two disjoint mapping ranges. It demonstrates range arithmetic only, not Linux authorization, map-file syntax, GID rules or capability semantics.

<!-- bijux-verify: {"id":"user-namespace-id-mapping","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inside=0 outside=100000\ninside=999 outside=100999\ninside=1000 outside=unmapped\ninside=1999 outside=unmapped\ninside=2000 outside=200000\ninside=2099 outside=200099\ninside=2100 outside=unmapped\n","stderr":""}} -->
```python
mappings = [
    (0, 100000, 1000),
    (2000, 200000, 100),
]

def outside_id(inside):
    for inside_start, outside_start, length in mappings:
        if inside_start <= inside < inside_start + length:
            return outside_start + (inside - inside_start)
    return None

for inside in (0, 999, 1000, 1999, 2000, 2099, 2100):
    outside = outside_id(inside)
    rendered = "unmapped" if outside is None else str(outside)
    print(f"inside={inside} outside={rendered}")
```

### Example 3

A supervisor calls `unshare(CLONE_NEWPID)` and prints its PID, expecting 1. It remains in its current PID namespace. Its first subsequently created child becomes PID 1 in the new namespace and must perform init duties.

### Example 4

A runtime clones a mount namespace from a host tree whose root is shared, then mounts a secret inside the container. The event propagates back to peers. Making the intended subtree recursively private or appropriately slave before container mounts prevents the export.

### Example 5

A debugging tool joins a workload's network namespace but keeps its host mount namespace. `/etc/resolv.conf` and Unix pathname sockets come from the host mount view, while routes and abstract Unix sockets come from the workload network view. Its mixed vector must be recorded.

### Example 6

A new network namespace has a loopback device but the runtime has not brought it up. A service cannot bind its expected localhost endpoint. Namespace creation provides isolated state; setup must establish the desired operational baseline.

### Example 7

The container init exits while an administrative process retains a network namespace descriptor and a socket. Teardown sees no workload processes but the namespace remains. Closing both persistent references permits destruction and device cleanup.

### Example 8

A cgroup namespace displays `/` as the workload's cgroup root, yet the process remains in a host cgroup with no memory limit. The relative path hides topology; only controller membership and settings establish governance.

### Example 9

A rootless launcher creates a user namespace, writes narrow ID maps through an authorized helper, then creates mount, PID and network namespaces owned by it. Container root holds scoped setup capabilities but cannot administer resources owned by the initial user namespace.

### Example 10

Negative testing finds an inherited directory descriptor opened on the host root before namespace setup. Even with a new root and mount namespace, the workload can traverse through the descriptor where permissions allow. Closing all unintended descriptors repairs the boundary.

## Cross-Program Connections

- **Security engineering:** scoped capabilities, LSM policy, seccomp, descriptor hygiene and kernel attack surface define containment.
- **Platform engineering:** runtimes assemble namespace vectors, mounts, networking, identity maps and lifecycle.
- **Network engineering:** isolated stacks, veth links, routing, filters, ports and teardown define connectivity.
- **Filesystem engineering:** mount trees, propagation, bind mounts, roots and open handles define path views.
- **Distributed systems:** durable workload identity must survive repeated inner PIDs and host movement.
- **Reliability engineering:** namespace init, signal forwarding, reaping, ordered teardown and checkpoint restore preserve lifecycle.
- **Resource management:** cgroups, rlimits and admission add governance that namespace views do not provide.
- **API engineering:** clone flags, descriptors and setns form capability-bearing, type-specific interfaces.
- **Observability engineering:** inner and outer identities, full vectors and mount/network context make telemetry interpretable.
- **Systems engineering:** kernel configuration, runtime order, helpers and global resources determine the end-to-end boundary.

## References

1. Linux man-pages Project, [namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html), namespace types, APIs, procfs handles, lifetime and limits; retrieved 2026-09-04.
2. Linux man-pages Project, [user_namespaces(7)](https://man7.org/linux/man-pages/man7/user_namespaces.7.html), scoped IDs, capabilities, mappings, ownership and interactions; retrieved 2026-09-04.
3. Linux man-pages Project, [pid_namespaces(7)](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html), hierarchy, visibility, namespace init, signals and procfs; retrieved 2026-09-04.
4. Linux man-pages Project, [mount_namespaces(7)](https://man7.org/linux/man-pages/man7/mount_namespaces.7.html), isolated mount lists and shared-subtree behavior; retrieved 2026-09-04.
5. Linux Kernel Documentation, [Shared Subtrees](https://docs.kernel.org/filesystems/sharedsubtree.html), shared, slave, private and unbindable propagation semantics; retrieved 2026-09-04.
6. Linux man-pages Project, [network_namespaces(7)](https://man7.org/linux/man-pages/man7/network_namespaces.7.html), network devices, stacks, routes, sockets and namespace lifecycle; retrieved 2026-09-04.
7. Linux man-pages Project, [cgroup_namespaces(7)](https://man7.org/linux/man-pages/man7/cgroup_namespaces.7.html), cgroup-root path virtualization and procfs views; retrieved 2026-09-04.
8. Linux man-pages Project, [time_namespaces(7)](https://man7.org/linux/man-pages/man7/time_namespaces.7.html), clock offsets, membership and setup semantics; retrieved 2026-09-04.
9. Linux man-pages Project, [unshare(2)](https://man7.org/linux/man-pages/man2/unshare.2.html), type-specific creation, caller and future-child behavior and errors; retrieved 2026-09-04.
10. Linux man-pages Project, [setns(2)](https://man7.org/linux/man-pages/man2/setns.2.html), descriptor-based joining, type checks, permissions and restrictions; retrieved 2026-09-04.

## Exercises

### Exercise 1

Processes A and B share user, network and IPC namespaces but differ in PID, mount, UTS, cgroup and time namespaces. State which major views are shared and which remain distinct.

### Exercise 2

Given mapping entries $(0,500000,500)$ and $(1000,700000,50)$, translate inside IDs 0, 499, 500, 1000 and 1049. What can you infer about capabilities from these numbers alone?

### Exercise 3

A tool joins a target PID namespace with `setns()` but still sees its old PID. Design the remaining steps needed to run a command as a process in the target PID view.

### Exercise 4

A container should receive new mounts propagated from `/media` on the host but must not propagate its own mounts back. Select a mount propagation relationship and explain it.

### Exercise 5

Design a minimum containment audit for a rootless workload that uses user, PID, mount and network namespaces but shares the host kernel.

## Answers to the Exercises

### Answer 1

The processes interpret UIDs, GIDs and scoped capabilities in the same user namespace; use the same network devices, routes, port space, filters and abstract Unix sockets; and see the same System V IPC and POSIX message-queue namespace. Those shared coordinates permit intentional interaction subject to ordinary permissions and policy.

They have different PID identities and visibility, mount trees, hostname/domain values, displayed cgroup roots and applicable time offsets. File descriptors, file-backed IPC, cgroup controller settings, global kernel state and other resources are not determined solely from the stated vector.

### Answer 2

The translations are 0 to 500000, 499 to 500499, 500 unmapped, 1000 to 700000 and 1049 to 700049. The intervals leave a gap and stop immediately after their stated lengths.

No capability conclusion follows from ID arithmetic alone. Capability sets, the governing user namespace, namespace ownership, credentials, ordinary object permissions and LSM or other policy determine authority. Even inside UID 0 would not imply initial-user-namespace root.

### Answer 3

After the caller joins the target PID namespace for children, fork or clone a child. That child receives a PID in the target namespace and ancestor namespaces. Ensure it also has the intended mount namespace and a procfs instance mounted for the target PID view, then establish credentials, signal handling and descriptor hygiene before executing the command.

The parent retains its original PID-namespace membership and can supervise the child using an outer identity or PID descriptor. Joining mount, user or other namespaces may have ordering and capability constraints; do not infer them from PID membership.

### Answer 4

Make the container's corresponding subtree a slave of the host's shared `/media` peer group. A slave receives mount and unmount propagation from its master but does not send its local events back. If the container also needs propagation among its own peer mounts, it can be shared-and-slave under carefully constructed relationships.

Verify recursively where submounts exist: changing only one mount may leave shared descendants. Inspect mount information from host and workload, mount test filesystems in both directions and confirm the intended one-way behavior before using sensitive mounts.

### Answer 5

Record the full namespace vector for workload, init and helpers; owning user namespaces; UID/GID maps; capability sets; mount propagation; root construction; open descriptors; procfs; network devices and routes. Verify no initial-user-namespace capabilities, host-root ID mapping, unintended host mount, host network interface, host PID view or persistent namespace handle is reachable.

Then audit the layers namespaces do not supply: seccomp, LSM policy, cgroup CPU/memory/I/O/process limits, rlimits, allowed devices, non-namespaced sysctls, kernel and runtime patch levels, and egress policy. Run negative tests for host PID enumeration, mount propagation, leaked descriptors, privileged syscalls, global resources, fork exhaustion and teardown. The shared kernel remains in the TCB and side-channel or kernel-vulnerability claims require separate evidence.
