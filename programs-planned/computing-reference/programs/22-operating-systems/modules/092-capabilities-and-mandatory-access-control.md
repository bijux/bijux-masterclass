---
module_id: OS-092
program: Operating Systems
level: 2
module_number: 92
title: Capabilities and Mandatory Access Control
status: complete
last_verified: 2026-09-04
---

# Capabilities and Mandatory Access Control

## One-Page Review

### Governing question

How can an operating system replace all-or-nothing superuser authority with narrowly scoped privilege while enforcing organization-wide rules that subjects cannot waive through ordinary ownership?

### Essential definitions

- A **capability** is a Linux privilege bit checked for a class of operations that would traditionally require UID 0.
- The **permitted set** bounds capabilities a thread may make effective; the **effective set** participates in current kernel checks.
- The **inheritable set** can contribute capabilities across `execve()` when the executed file agrees.
- The **bounding set** limits capabilities gained from a file's permitted set and future inheritable additions.
- The **ambient set** carries selected permitted-and-inheritable capabilities across execution of nonprivileged files.
- **discretionary access control**, or **DAC**, lets owners influence access through identity, modes and ACLs.
- **mandatory access control**, or **MAC**, applies centrally defined policy to labeled subjects and objects independently of owner discretion.
- A **security context** is the LSM-specific label or profile state used for authorization and transitions.

### Central model, mechanism, or theorem

Authorization is an intersection of mechanisms. Credentials and DAC decide whether identity and ownership permit an operation; capability checks gate selected privileged operations in a governing user namespace; LSM hooks apply active MAC and other policies; seccomp, namespaces and mount state constrain other dimensions. Execution transforms credentials and security context. Least privilege therefore proves every transition and every relevant policy layer, not merely a low numeric UID.

### Critical invariants

- Effective capabilities are a subset of permitted capabilities, and ambient capabilities are subsets of both permitted and inheritable sets.
- Capabilities are interpreted in the user namespace governing the resource or operation.
- Bounding-set drops, capability clearing and locked securebits occur before untrusted execution and propagate to descendants.
- File capabilities, set-ID bits, `no_new_privs`, mount flags and LSM transitions are analyzed together for every executable path.
- Active MAC modules, enforcing state, loaded policy, labels and transition rules match the intended deployment.
- A grant in one mechanism cannot bypass a denial imposed by another applicable mechanism.
- Audit evidence distinguishes policy denial, DAC denial, missing capability and absent or permissive enforcement.

### Common failures

A service drops only its effective set, retains `CAP_SYS_ADMIN`, raises ambient privilege for an unexpected helper, assumes container-root capabilities apply to host objects, loses file capability xattrs during image copy, runs an AppArmor task unconfined, boots SELinux permissive, labels a bind mount incorrectly, or treats an audit allow suggestion as reviewed policy.

### Compact example

A web server binds port 443 through `CAP_NET_BIND_SERVICE` but runs as a nonzero UID with no filesystem-administration capability. Its MAC domain may read its immutable application files and TLS key, write only a log directory, and connect only to declared services. The capability answers one privileged network check; MAC, DAC, mounts, seccomp and cgroups still govern the rest.

### Connections

Capabilities and MAC connect credentials, executable metadata, namespaces, containers, service managers, filesystem labels, policy compilers, audit, incident response and least-privilege architecture.

## Governing Question

Unix UID 0 historically bundles unrelated authority, while owner-controlled permissions cannot express every institutional boundary. The governing question is how capability sets and mandatory policy divide this authority without introducing hidden execution transitions, namespace confusion or policy that exists on disk but is not enforced.

## Why This Matters

Compromised services should not inherit the ability to mount filesystems, reconfigure networking, trace peers, load modules or bypass every file permission merely because startup needed one privileged operation. Capabilities make narrower grants possible. MAC can constrain even a process that owns a file or holds a capability when organization policy forbids the requested relationship.

The machinery is stateful. Capabilities live in multiple sets, file extended attributes and user-namespace scopes. SELinux, AppArmor and other LSMs use distinct policy models and transition rules. Container and service-manager configuration must become correct kernel state. Small misunderstandings around `execve()`, ambient privilege or labels can silently widen the boundary.

## Prerequisites and Retrieval

Before studying this module, be able to:

- explain real, effective, saved and filesystem UIDs and GIDs;
- describe `fork()`, `execve()`, set-ID files and extended attributes;
- reason about user namespaces, mounts, file descriptors and process ancestry;
- distinguish DAC permissions, ACLs, privilege checks and policy hooks;
- interpret deny-by-default policy, audit records and enforcement modes.

Retrieve the exact kernel and highest supported capability, all five capability sets for launcher and workload threads, securebits, `no_new_privs`, IDs and user namespaces, executable file capabilities and mount options, active LSM list, enforcing state, policy build and checksum, process and object contexts, transition rules, bind-mount labels, runtime or unit configuration and relevant audit records.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish permitted, effective, inheritable, bounding and ambient capability sets;
2. reason through ordinary file-capability transformation across `execve()`;
3. scope capability checks to owning user namespaces and controlled resources;
4. design a privilege-dropping launcher whose descendants cannot regain authority;
5. distinguish DAC decisions from MAC subject–object policy and LSM composition;
6. explain SELinux label/type transitions and AppArmor task-profile confinement;
7. translate service and container policy into verifiable running state;
8. test privilege, label, transition, audit and denial behavior adversarially.

## Core Exposition

### Treat credentials as a structured state

A Linux thread carries IDs, supplementary groups, capability sets, securebits, `no_new_privs` and LSM attributes. File descriptors and namespaces add authority not visible in credentials. Capture the entire state at every execution boundary rather than summarizing it as “root” or “nonroot.”

### Use the effective set for present checks

The effective capability set supplies bits used by kernel privilege checks. Clearing a bit there stops current use, but a bit retained in the permitted set may be made effective again by authorized capability-set operations. A durable drop removes unneeded bits from every relevant set and prevents later acquisition paths.

### Use permitted as a hard working ceiling

The permitted set is a superset from which effective bits may be selected and constrains ordinary changes to inheritable state. Dropping a capability from permitted is meaningful, yet a later privileged executable could grant file capabilities within the bounding set unless other mechanisms prevent it.

### Understand inheritable agreement

The process inheritable set alone does not grant an effective privilege. During execution, its intersection with the file's inheritable set contributes to the new permitted set. This two-sided agreement supports controlled propagation but is frequently unnecessary for single-process services and should then be empty.

### Use the bounding set to limit future exec grants

The per-thread bounding set masks capabilities from a file's permitted set during ordinary execution transformation and limits future inheritable additions. Dropping a bit is one-way for the thread and inherited by descendants. Perform required privileged setup first, then drop and verify before untrusted execution.

### Treat ambient capabilities as explicit delegation

An ambient bit must also be permitted and inheritable. It persists across execution of nonprivileged files and contributes to new permitted and effective sets. Executing a privileged file clears ambient state. Ambient privilege is convenient for scripts and helpers, but every executable reachable by the process can receive it.

### Understand file capabilities

The `security.capability` extended attribute stores file permitted and inheritable sets plus an effective flag. It grants privilege during execution under the kernel's transformation rules. Archive, copy, overlay and network filesystems may lose or reject this xattr; verify the deployed inode rather than the build recipe.

### Apply the ordinary exec transformation carefully

For a non-special identity case, the new permitted set combines inherited agreement, file-permitted bits bounded by the process, and surviving ambient bits. The file effective flag controls whether new permitted bits become effective, otherwise surviving ambient bits become effective. Root-specific semantics, set-ID, `no_new_privs`, mount flags and namespace-rooted file capabilities add conditions.

### Avoid capability-dumb partial grants

A binary converted from setuid-root may assume it receives every declared file capability. If bounding removes part of a file-effective grant, the kernel can fail execution rather than run it unpredictably underprivileged. Applications designed for capabilities should check and manage their sets explicitly.

### Account for UID transition fixups

Changing between zero and nonzero UIDs can clear or adjust capabilities. Securebits alter these legacy fixups, and keep-caps can preserve selected permitted state across an ID change while effective state still needs handling. Set and lock a deliberate model; do not depend on accidental UID order.

### Set no_new_privs as a one-way guard

`no_new_privs` prevents `execve()` from granting authority that execution would not otherwise have, suppressing set-ID and file-capability elevation in relevant cases. It persists and cannot be unset. It does not revoke existing capabilities or powerful file descriptors and may affect LSM execution transitions.

### Drop CAP_SYS_ADMIN aggressively

`CAP_SYS_ADMIN` gates a broad and evolving collection of operations. Retaining it weakens claims of fine-grained privilege, even when other capabilities were dropped. Prefer narrower capabilities and move exceptional setup to a short-lived, separately confined helper with a small input contract.

### Scope capabilities through user namespaces

Capabilities are meaningful relative to a user namespace. A process may hold all bits in its container user namespace while holding none in the initial namespace. Operations over resources owned by the initial namespace remain unavailable. Record the owning user namespace for both subject authority and target resource.

### Treat container root as scoped authority

UID 0 inside a mapped user namespace may administer namespaces owned by it and descendants, not the host globally. Without a user namespace, a container process's UID and capability scope can align more closely with the host. Never infer the boundary from the displayed UID inside the container.

### Close descriptor-based authority

A process can use an already-open device, directory, socket or namespace handle even after capabilities are dropped, subject to operation-specific checks. Launchers must close unintended descriptors and constrain deliberate ones. Credential inspection alone cannot prove least privilege.

### Distinguish DAC from MAC

DAC evaluates ownership identities, mode bits and ACLs and lets authorized owners change much policy. MAC attaches centrally administered subject and object semantics that ordinary subjects cannot waive. An operation proceeds only when every applicable check—including capabilities, DAC and LSM policy—permits it.

### Understand the LSM hook model

Linux Security Modules insert additional checks at security-relevant kernel operations and expose security contexts through process attributes and object metadata. Multiple active LSMs may contribute decisions. Inspect the running active-module list and contexts; a compiled policy engine is not necessarily active or enforcing.

### Use SELinux type enforcement as relationships

SELinux associates process domains and object types within richer security contexts. Policy permits specified operations between them, and execution rules can transition a process to another domain. File labels normally travel in security extended attributes, so image, mount and restore workflows must preserve or deliberately relabel them.

### Separate SELinux identity dimensions

SELinux users, roles, types and optional MLS/MCS levels are not Unix IDs, though login mapping connects them. Type enforcement commonly drives service confinement; roles and levels express additional constraints. Diagnose each context component rather than editing a type rule to mask an identity-mapping error.

### Distinguish enforcing and permissive modes

Enforcing mode blocks denied operations and may audit them. Permissive mode records many policy denials but allows them, globally or for configured domains where supported. Permissive testing can discover behavior; it is not equivalent to deployed enforcement and must be clearly visible in evidence.

### Use AppArmor task-centered profiles

AppArmor attaches loaded profiles to tasks and mediates accesses according to its policy model, including path-oriented rules and named transitions. A process with no applied profile can be unconfined. Verify the actual current profile, namespace, mode and loaded policy after execution rather than trusting a filename.

### Treat paths and mount views carefully

Path-oriented policy interacts with bind mounts, aliases, mount namespaces, renamed paths and disconnected objects. Test the exact runtime mount tree. Label-oriented policy also depends on filesystem support, correct xattrs and mount contexts. Neither model excuses incomplete object inventory.

### Design execution transitions explicitly

Launching a helper can inherit a domain/profile, transition to a new one, execute unconfined or fail depending on policy. Combine that with set-ID, file capabilities, ambient bits and `no_new_privs`. Enumerate the complete executable graph, interpreters and dynamic loader rather than only the service's first binary.

### Apply least privilege to policy administration

Loading MAC policy, relabeling files and changing enforcement are highly privileged control-plane actions. Separate them from workloads, protect policy artifacts and keys, and audit updates. A confined service should not be able to rewrite the policy that confines it.

### Translate service-manager controls carefully

systemd can set capability bounding and ambient sets, `NoNewPrivileges=`, LSM profiles, syscall filters, identities and filesystem restrictions. Ordering and executable prefixes can create exceptions. Inspect `/proc` credentials, security contexts and mount state for the live process to verify the unit's effect.

### Translate OCI controls carefully

OCI configuration exposes bounding, effective, inheritable, permitted and ambient sets plus AppArmor profile and SELinux process and mount labels. The runtime must establish them during container creation. Compare requested configuration with runtime state and reject unsupported policy rather than silently weakening it.

### Preserve labels through container storage

Image extraction, OverlayFS copy-up, bind mounts and volumes can carry different labels and xattr behavior. Shared host directories require tenant-aware relabeling or mount policy, not blanket writable labels. Test create, rename, copy-up, restore and volume reattachment under enforcement.

### Avoid policy generated blindly from audit

Audit logs reveal observed denials, including attacks, bugs and paths exercised only in permissive mode. Tools that turn them into allow rules can authorize unwanted behavior. Classify the operation, subject, object, transition and business need before changing policy; then rerun negative tests.

### Diagnose the complete denial chain

An `EACCES` may arise from DAC, missing capability, mount flags or an LSM. Collect IDs and groups, capability sets, namespace ownership, object metadata, active contexts, audit record and policy version. Do not disable enforcement to make an ambiguous failure disappear.

### Bound resources separately

Capabilities and MAC govern authority but not fair CPU, memory, I/O or process allocation. Use cgroups, rlimits and quotas. A perfectly confined service can still deny service to neighbors through allowed resource use if those limits are absent.

### Test positive and negative policy

Verify required operations across startup, reload, failure, upgrade and shutdown. Then attempt forbidden files, devices, network peers, process signals, tracing, mounts, namespace changes and policy administration. Test every executable transition and container volume state under enforcing mode.

### Treat policy as versioned code

Review source, compile deterministically where possible, test against representative labeled images and promote with rollback. Record kernel, policy compiler and module versions. Drift in labels, unit files or runtime configuration can change effective authorization without a policy-source diff.

### Recover at the policy boundary

If a capability or MAC escape grants host authority, isolate the host and rotate exposed credentials; restarting one process may be insufficient. Preserve audit and external telemetry, correct policy and root cause, rebuild from known-good artifacts where needed, and verify the negative case before restoration.

## Definitions and Notation

Let thread capability state be

$$
C=(P,E,I,B,A),
$$

for permitted, effective, inheritable, bounding and ambient sets. Required invariants include

$$
E\subseteq P,\qquad A\subseteq P\cap I.
$$

For ordinary nonroot execution without special suppression, let file sets be $F_P,F_I$ and effective flag $F_E$. With a nonprivileged file, the simplified transformation is

$$
A'=A,
$$

$$
P'=(I\cap F_I)\cup(F_P\cap B)\cup A',
$$

$$
E'=\begin{cases}P',&F_E=1,\\A',&F_E=0.\end{cases}
$$

Also $I'=I$ and $B'=B$. Root-ID special handling, privileged files, `no_new_privs`, securebits, namespace-rooted file capabilities and mount flags must be applied before using this model operationally.

For subject $s$, object $o$ and operation $op$, a composed authorization abstraction is

$$
allow(s,o,op)=DAC\land CAP\land LSM_1\land\cdots\land LSM_n\land MOUNT,
$$

where a component denotes its applicable check, not that every operation invokes every mechanism identically.

## Mechanisms, Invariants, or Proof Structure

Review privilege and MAC with these obligations.

1. **Credential obligation:** IDs, groups, five capability sets, securebits and `no_new_privs` are recorded per execution stage.
2. **Scope obligation:** each capability check and resource has an explicit governing user namespace.
3. **Execution obligation:** file metadata, interpreters, set-ID, ambient state and LSM transitions produce intended descendants.
4. **Drop obligation:** unneeded privilege leaves permitted, effective, inheritable, bounding and ambient sets irreversibly before untrusted code.
5. **Handle obligation:** retained descriptors cannot bypass the credential design.
6. **Activation obligation:** intended LSMs, enforcement mode, policy and profiles are active on the running kernel.
7. **Label obligation:** process, image, file, mount, volume and network contexts are correct and persistent.
8. **Relationship obligation:** subject–object operations and executable transitions follow reviewed deny-by-default policy.
9. **Control-plane obligation:** policy loading, relabeling and enforcement changes remain outside workload authority.
10. **Translation obligation:** unit and runtime configuration matches observed kernel state without silent fallback.
11. **Evidence obligation:** positive, negative, lifecycle and denial-source tests run under enforcement.
12. **Assurance obligation:** privilege, object authorization, syscall reduction, isolation and resource control remain separate.

The proof traces credentials and context through every process creation, ID change and executable transition. For each requested operation, it checks namespace-relative capability authority, DAC, active LSMs, mount state and retained handles. One empty effective set or one loaded policy file proves only a moment and one layer.

## Alternatives and Trade-Offs

- **setuid root versus file capability:** setuid supplies broad compatibility; file capabilities can grant a narrower executable privilege.
- **Preopened resource versus retained capability:** a handle narrows authority to one object; a capability supports dynamic objects and broader checks.
- **Permitted retention versus permanent drop:** retention supports later elevation; dropping reduces post-compromise authority.
- **Ambient versus file capabilities:** ambient state follows a process execution chain; file capabilities bind privilege to one executable inode.
- **Capability helper versus main-process privilege:** a helper narrows lifetime and interface; integrated privilege avoids IPC and deputy complexity.
- **User namespace versus initial namespace:** scoped root enables rootless workflows; initial-namespace authority reaches host-owned resources.
- **DAC versus MAC:** DAC is familiar and owner-managed; MAC enforces institutional rules owners cannot waive.
- **SELinux type policy versus AppArmor profile:** label relationships suit system-wide object policy; task profiles offer application-centered confinement.
- **Enforcing versus permissive:** enforcing supplies denial; permissive aids observation and supplies no denial for its permissive scope.
- **Inherited versus explicit execution transition:** inheritance simplifies helpers; explicit domains or profiles can narrow each executable stage.
- **Persistent xattr versus mount context:** stored labels travel with supported filesystems; mount labels cover imported storage and can flatten distinctions.
- **Shared volume relabel versus dedicated volume:** sharing saves storage; dedication simplifies tenant-specific labeling and lifecycle.
- **Handwritten versus generated policy:** handwritten intent is reviewable; generated rules accelerate discovery and may encode hostile behavior.
- **Direct denial versus audit-first rollout:** immediate enforcement narrows exposure; staged audit reduces compatibility surprises.
- **Runtime policy versus build-time image labeling:** runtime adapts deployment; prelabeling improves reproducibility and startup.
- **Single versus stacked LSM policy:** one model simplifies diagnosis; stacking composes independent restrictions and evidence.

## Failure Modes and Misconceptions

- “Capabilities belong to a process.” They are per-thread kernel state, though threading libraries often coordinate them.
- “Nonroot means unprivileged.” Capabilities and handles can grant substantial authority.
- “Clearing effective permanently drops a capability.” Permitted state may allow it to return.
- “Permitted is the only ceiling.” Bounding, file and inheritable state shape execution gains.
- “Inheritable automatically becomes effective.” The executable's metadata and transition rules matter.
- “Ambient capabilities are harmless convenience.” Unexpected helpers inherit them across nonprivileged exec.
- “The bounding set clears current effective bits.” It primarily constrains future acquisition paths and inheritable additions.
- “File capabilities survive every copy.” Extended attributes and filesystem support vary.
- “A signed executable's file capabilities are trustworthy.” Signature and capability-xattr provenance require an explicit chain.
- “no_new_privs clears existing privilege.” It constrains exec-time gains.
- “CAP_SYS_ADMIN is one narrow administration permission.” It covers many unrelated operations.
- “A capability bit is global.” User-namespace ownership scopes many checks.
- “Container UID 0 equals host root.” Mappings and namespace ownership determine authority.
- “Dropping capabilities closes open resources.” Descriptors retain object authority.
- “MAC replaces DAC.” Applicable policies compose; a grant in one does not cancel another's denial.
- “Compiled LSM means enforced policy.” Activation, mode and loaded policy must be verified.
- “SELinux type is the Unix user.” Security-context dimensions are distinct from Unix IDs.
- “Permissive SELinux is enforcing with extra logs.” It allows operations within its permissive scope.
- “AppArmor installed means every task is confined.” Tasks can be unconfined or use an unexpected profile.
- “Path policy is independent of mounts.” Namespace and alias topology affects named objects.
- “A label allow rule grants every operation.” Permissions are class- and operation-specific.
- “Bind mounts preserve the intended container label automatically.” Mount and storage workflows can change contexts.
- “Audit denial always identifies the only failed check.” Multiple authorization layers may reject an operation.
- “audit-to-policy output is safe to accept.” Observed behavior can be unnecessary or hostile.
- “MAC controls resource consumption.” Cgroups and quotas provide that dimension.
- “One successful start proves least privilege.” Rare lifecycle and negative paths remain untested.

## Worked Examples

### Example 1

A daemon clears `CAP_NET_ADMIN` from effective but retains it in permitted. After compromise it calls the capability API and restores the bit. Removing it from permitted and bounding, clearing inheritable and ambient, and controlling executable grants makes the drop durable.

### Example 2

The following executable toy applies the chapter's simplified ordinary file-capability transformation. It demonstrates set arithmetic only, not Linux identity, namespace, file-xattr, securebits, mount, LSM or `execve()` behavior.

<!-- bijux-verify: {"id":"capability-exec-set-transformation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"permitted=chown,net_bind_service\neffective=chown,net_bind_service\ninheritable=chown\nbounding=chown,net_bind_service\nambient=none\nsetuid_present=false\n","stderr":""}} -->
```python
permitted_before = {"chown", "net_bind_service", "setuid"}
inheritable = {"chown"}
bounding = {"chown", "net_bind_service"}
ambient = set()
file_permitted = {"net_bind_service", "setuid"}
file_inheritable = {"chown"}
file_effective = True

permitted_after = ((inheritable & file_inheritable)
                   | (file_permitted & bounding)
                   | ambient)
effective_after = permitted_after if file_effective else ambient

def rendered(values):
    return ",".join(sorted(values)) if values else "none"

print(f"permitted={rendered(permitted_after)}")
print(f"effective={rendered(effective_after)}")
print(f"inheritable={rendered(inheritable)}")
print(f"bounding={rendered(bounding)}")
print(f"ambient={rendered(ambient)}")
print(f"setuid_present={str('setuid' in permitted_after).lower()}")
```

### Example 3

A script interpreter is executed while `CAP_NET_BIND_SERVICE` is ambient. The interpreter and arbitrary script code receive the capability. Binding the grant to a narrowly reviewed executable or preopening the listening socket reduces the delegated execution graph.

### Example 4

A rootless container shows every capability in its user namespace. It can configure its owned network namespace but cannot change a host interface owned by the initial user namespace. The bit name is identical; its governing namespace differs.

### Example 5

An SELinux-confined server owns its TLS key by DAC but its domain lacks the required read relation to the key type. Access is denied. Changing mode to world-readable does not override the MAC denial and would weaken DAC unnecessarily.

### Example 6

An AppArmor policy file exists for a worker, but the launched task's current attribute says unconfined because its attachment rule did not match a renamed executable. Inspecting live profile state finds the gap that configuration-file review missed.

### Example 7

An image build assigns a file capability to `/usr/bin/ping`, then an archive export drops `security.capability`. Production execution fails without the bit. Verifying xattrs in the final unpacked snapshot catches the supply-chain transformation.

### Example 8

A host directory is bind-mounted into two tenant containers and broadly relabeled for both. Each domain can now reach the other's files. Dedicated directories with tenant-specific labels or a deliberately shared mediation service preserve separation.

### Example 9

Permissive-mode audit suggests allowing a service to write all of `/etc`. Investigation shows a compromised plugin attempted the write; normal operation needs one state file elsewhere. Blind generation would have encoded attack behavior as policy.

### Example 10

A systemd unit requests a narrow bounding set and `NoNewPrivileges=yes`, but an auxiliary command is configured to bypass selected restrictions. Live credential and transition tests on every unit command reveal the exception before deployment.

## Cross-Program Connections

- **Security engineering:** least privilege, deny-by-default policy, control-plane separation and incident scope define authorization assurance.
- **Platform engineering:** service managers and runtimes translate declared identities, capability sets and labels into kernel state.
- **Container engineering:** user namespaces, mounts, file capabilities and volume labeling determine scoped root authority.
- **Filesystem engineering:** xattrs, ACLs, mount labels, OverlayFS and bind mounts carry authorization metadata.
- **API engineering:** executable and helper interfaces replace broad capabilities with narrower object-specific delegation.
- **Supply-chain engineering:** policy, executable and xattr provenance must survive image and deployment transformations.
- **Observability engineering:** audit, process contexts and capability telemetry distinguish denial sources and drift.
- **Reliability engineering:** policy rollout, permissive staging, rollback and recovery balance enforcement with availability.
- **Formal methods:** set transformations and intersected authorization rules support transition review.
- **Systems engineering:** identities, kernels, policies, storage and operational control planes compose one boundary.

## References

1. Linux man-pages Project, [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html), capability definitions, five sets, file metadata, execution transformation and securebits; retrieved 2026-09-04.
2. Linux man-pages Project, [credentials(7)](https://man7.org/linux/man-pages/man7/credentials.7.html), process IDs, groups, capabilities and filesystem credentials; retrieved 2026-09-04.
3. Linux man-pages Project, [user_namespaces(7)](https://man7.org/linux/man-pages/man7/user_namespaces.7.html), namespace-scoped capabilities, ownership and ID mappings; retrieved 2026-09-04.
4. Linux man-pages Project, [PR_CAP_AMBIENT(2const)](https://man7.org/linux/man-pages/man2/PR_CAP_AMBIENT.2const.html), ambient capability operations and invariants; retrieved 2026-09-04.
5. Linux man-pages Project, [xattr(7)](https://man7.org/linux/man-pages/man7/xattr.7.html), extended-attribute namespaces and filesystem support; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Linux Security Modules](https://docs.kernel.org/userspace-api/lsm.html), active modules and process security-context interfaces; retrieved 2026-09-04.
7. Linux Kernel Documentation, [SELinux](https://docs.kernel.org/admin-guide/LSM/SELinux.html), kernel configuration, policy tooling and filesystem labeling; retrieved 2026-09-04.
8. Linux Kernel Documentation, [AppArmor](https://docs.kernel.org/admin-guide/LSM/apparmor.html), task profiles, activation and unconfined behavior; retrieved 2026-09-04.
9. Linux man-pages Project, [systemd.exec(5)](https://man7.org/linux/man-pages/man5/systemd.exec.5.html), service capability sets, no-new-privileges and LSM profile controls; retrieved 2026-09-04.
10. Open Container Initiative, [Linux Container Configuration](https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md), container capability arrays, AppArmor profile and SELinux process and mount labels; retrieved 2026-09-04.

## Exercises

### Exercise 1

Explain the role of each capability set and state which subset invariants always hold for effective and ambient capabilities.

### Exercise 2

Let $I=\{a,b\}$, $B=\{a,c\}$, $A=\varnothing$, $F_I=\{b,c\}$ and $F_P=\{a,c,d\}$ with the file effective flag set. Compute the simplified post-exec permitted and effective sets.

### Exercise 3

Design a launcher that binds one privileged port, opens one configuration file and then executes an untrusted parser with no reusable privilege.

### Exercise 4

A containerized service can read an expected file in permissive mode but fails in enforcing mode after a volume replacement. Design a diagnosis that distinguishes DAC, capability, mount and MAC causes.

### Exercise 5

Design a minimum verification suite for a systemd- or OCI-launched service that uses a capability and a MAC profile across startup, reload, helper execution and shutdown.

## Answers to the Exercises

### Answer 1

Permitted bounds capabilities that can ordinarily become effective; effective supplies bits for current privilege checks; inheritable can agree with file-inheritable metadata across execution; bounding limits file-permitted gains and future inheritable additions; ambient carries eligible bits across execution of nonprivileged files into permitted and effective state.

The effective set must be a subset of permitted. Ambient must be a subset of both permitted and inheritable. Lowering either supporting set automatically lowers the corresponding ambient bit. Bounding is not simply a superset of every current set, and dropping a bounding bit does not itself clear the same currently effective bit.

### Answer 2

The inherited agreement is $I\cap F_I=\{b\}$. The bounded file-permitted contribution is $F_P\cap B=\{a,c\}$. Ambient contributes nothing. Therefore $P'=\{a,b,c\}$.

Because the file effective flag is set, $E'=P'=\{a,b,c\}$. Capability $d$ is excluded by the bounding set. This uses only the simplified ordinary transformation; identity-zero rules, privileged-file ambient clearing, `no_new_privs`, securebits, namespaces and mount behavior must be evaluated in a real launch.

### Answer 3

Keep a small trusted launcher in a confined domain. Give it only the capability needed to bind the port, or have a service manager preopen the socket. Open the configuration through an authorized path, verify its type and pass only the listening socket and read-only configuration descriptor to the child.

Before releasing untrusted input, close all other descriptors, clear ambient and inheritable, remove every unneeded permitted and effective bit, drop them from bounding, set and lock appropriate securebits, switch to the final nonzero IDs, set `no_new_privs`, enter the parser's MAC domain/profile and install seccomp. Verify live credentials and contexts from a trusted supervisor. The parser uses object handles and retains no capability to bind another port or reopen arbitrary configuration.

### Answer 4

From the live process and a trusted host view, record IDs, groups, all capability sets, user namespace, current security context and enforcement mode. Inspect the target inode rather than only its pathname: ownership, modes, ACLs, xattrs, filesystem, mount flags, bind source and security label. Correlate the denial with audit records and the exact loaded policy version.

Test DAC using the final IDs without disabling MAC; confirm whether any operation-specific capability is required and correctly scoped; inspect read-only or execution mount attributes; then query the MAC relation between the process context, object context, class and permission. Compare the old and replacement volume labels and mount context. Repair the incorrect label or narrowly reviewed policy rule—do not broaden Unix modes or disable enforcement to conceal the source.

### Answer 5

For main process and every helper, record requested and live IDs, groups, all five capability sets, securebits, `no_new_privs`, user namespace, LSM contexts, active modules, enforcement mode, mount tree and open descriptors. Verify executable and image file-capability xattrs and labels after final unpack, copy-up and volume attachment. Confirm the policy and unit/runtime artifact versions.

Run successful startup, privileged operation, steady work, reload, rotation, failure handler and shutdown. Across every exec, assert only the intended capability and domain/profile survives. Negative tests attempt another privileged operation, unauthorized files and volumes, forbidden peer signals, tracing, devices, mounts, namespace creation and policy changes. Repeat under enforcing mode after restart and upgrade, ensure denials are attributable and rate-limited, and prove the supervisor can recover the service without granting the workload broader authority.
