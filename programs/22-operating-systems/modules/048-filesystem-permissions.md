---
module_id: OS-048
program: Operating Systems
level: 1
module_number: 48
title: Filesystem Permissions
status: complete
last_verified: 2026-09-04
---

# Filesystem Permissions

## One-Page Review

### Governing question

How should an operating system authorize filesystem operations using credentials, ownership, mode bits, ACLs, capabilities, mount context, and security policy without path races, confused identity, or unintended privilege?

### Essential definitions

- **Discretionary access control (DAC)** lets object ownership and configured entries govern access.
- A **credential snapshot** contains the identities, groups, capabilities, security context, and namespace mappings used for one decision.
- **Read, write, and execute bits** select basic permissions; execute on a directory means search or traversal.
- An **access ACL** extends owner, named-user, group-class, and other permissions for one object.
- An **ACL mask** limits the effective permissions of named users, owning group, and named groups.
- A **default ACL** on a directory participates in deriving a new child's access ACL.
- A **capability** is a partitioned privilege that can override or add selected checks under its namespace rules.
- An **idmapped mount** changes how caller and filesystem ownership IDs are interpreted for a mount view without rewriting every inode.

### Central model, mechanism, or theorem

Authorize request `A=(op,N,S,P,I,C,M,L,t)`: operation `op`, namespace `N`, starting handle `S`, pathname `P` or stable object `I`, credential snapshot `C`, mount context `M`, security policy `L`, and observation time `t`. Path resolution first requires search permission and policy at every traversed directory. The final decision combines operation-specific parent and target checks, mapped ownership, ACL or mode selection, capabilities, object flags, mount constraints, and mandatory policy.

Permission is neither a property of a pathname string nor one reusable Boolean. A later operation needs either the authority captured by an opened handle or a new decision on the actual current object. Correct mutation of ownership, mode, ACL, labels, and set-ID state is itself an authorized, atomic, recoverable metadata transition.

### Critical invariants

- Authorization and use apply to the same resolved object, parent, credentials, mount, and policy context.
- Every traversed directory grants search through DAC and all additional policy layers; a permissive final inode cannot bypass an inaccessible parent.
- ACL evaluation selects the specified class and applies its mask exactly once; it is not unioned casually with all mode bits.
- Creation derives owner, group, mode, and ACL from credentials, parent inheritance, requested mode, and creation mask under documented rules.
- Ownership and content changes clear or preserve set-ID and file-capability state only as the platform contract permits.
- Open handles retain object identity and granted access under documented use-time checks; pathname changes cannot redirect them.
- Audit evidence identifies decision inputs and policy versions without exposing unnecessary sensitive names or labels.

### Common failures

Common mistakes are calling `access(path)` before `open(path)` as authorization, confusing directory read with search, treating ACL entries as simply additive, ignoring the ACL mask, assuming UID zero bypasses every policy, comparing raw inode IDs under an idmapped mount, preserving set-ID bits or file capabilities after untrusted content changes, interpreting `noexec` as a complete code-execution boundary, and checking only the final component of an attacker-controlled path.

### Compact example

A file's named-user ACL grants Alice `rwx`, but its mask is `r-x`; Alice's effective permission is `r-x`. She can read and execute but not write, even if a tool prints the unmasked entry. Changing the group-class mode bits updates the ACL mask under the ACL contract, so chmod and ACL views remain consistent.

### Connections

[OS-002](002-privilege-levels-and-protection-rings.md), [OS-003](003-system-calls-and-user-kernel-transitions.md), and [OS-041](041-files-directories-and-namespaces.md) establish protection and path resolution. [OS-049](../ROADMAP.md) places permission hooks in VFS layers; later security modules deepen mandatory policy.

## Governing Question

“Can this process access this file?” hides several decisions. The kernel resolves a path through directories, selects an object, interprets ownership through namespaces and mounts, evaluates DAC and ACLs, considers privileges, applies mount and inode flags, and invokes additional security policy.

The governing question is how to make that chain precise, race resistant, and least privileged. The answer treats authorization as a contextual operation over stable identities rather than as a reusable property of a string.

## Why This Matters

Filesystem permissions protect executables, credentials, configuration, devices, logs, sockets, and tenant data. Small misunderstandings can become privilege escalation, disclosure, destructive overwrite, or sandbox escape.

The details also affect ordinary reliability. Backup, restore, archive extraction, containers, network filesystems, and deployment tools must preserve or deliberately transform ownership, ACLs, labels, and capabilities without creating inaccessible or overprivileged objects.

Permission checks race with namespace and metadata mutation. Correct APIs combine resolution, access mode, creation, and stable handles so an attacker cannot replace the checked object before use.

## Prerequisites and Retrieval

Review [OS-002](002-privilege-levels-and-protection-rings.md), [OS-011](011-processes-and-address-spaces.md), [OS-021](021-critical-sections-in-the-kernel.md), [OS-041](041-files-directories-and-namespaces.md), and [OS-042](042-inodes-and-metadata.md).

Retrieve these distinctions:

- real, effective, saved, filesystem, and namespace-mapped IDs serve different purposes;
- directory read lists names, while directory search traverses and accesses known entries;
- file execute permission, interpreter permission, mount policy, and credential transition are separate checks;
- owner, group class, and other mode bits are mutually selected classes, not permissions always unioned together;
- an ACL named-user or group-class result is constrained by the ACL mask;
- parent directory authority governs creation, removal, and rename more directly than target write bits;
- an opened descriptor identifies an object after its pathname changes;
- DAC, capabilities, mandatory policy, object flags, and mount settings compose rather than replace one another.

## Learning Objectives

After this module, you should be able to:

1. trace path search and final operation authorization using stable credentials and mount context;
2. evaluate owner, group, other, and POSIX ACL permissions including masks and supplementary groups;
3. derive creation ownership, modes, default ACLs, umask effects, setgid inheritance, and sticky-directory behavior;
4. reason about set-user-ID, set-group-ID, file capabilities, execute transitions, and privilege clearing;
5. explain idmapped mounts, user namespaces, remote identity, mandatory controls, and filesystem flags;
6. design race-resistant open, create, mutate, and metadata-management workflows;
7. test authorization matrices, concurrency, failure, audit, and assurance evidence.

## Core Exposition

### Authorization subject

The subject is a credential snapshot, not merely one user number. It can include real and effective IDs, filesystem IDs, supplementary groups, capabilities, user namespace, security label, key state, and audit identity.

The kernel obtains one coherent credential reference for a decision. Concurrent credential replacement cannot mix fields from incompatible snapshots.

### Authorization object

The object includes stable filesystem and inode identity, type, owner, group, mode, ACL, labels, flags, and current mount. Parent directories and namespace topology are additional objects for pathname operations.

A pathname is only a resolution instruction. It can name another object later and must not be cached as an authorization token.

### Operation-specific rights

Read, write, execute, append, search, create, delete, rename, link, metadata change, ownership change, mount, and device use have distinct checks. A single `writable` Boolean loses required context.

For example, unlink usually depends on parent directory write and search plus sticky and policy checks, not target-file write permission.

### Path search

Every nonfinal directory requires search permission or an authorized override. Failure at any component denies traversal even when the final inode would allow the requested data access.

Symbolic links and mount crossings change the objects traversed. Handle-relative constrained resolution limits attacker-controlled substitution and escape.

### Directory read and search

Read permission on a directory permits listing its entries under the interface contract. Search permission permits traversing named components and using entries when other rights allow.

One without the other is meaningful: a caller may access a known name without listing, or list names without successfully inspecting their targets.

### Regular-file read

Reading file data selects owner, group-class, or other permissions after mapping identities and evaluating an ACL if present. Open-time success binds subsequent reads to the open object.

Mandatory policy, encryption keys, leases, or use-time revocation can add checks. DAC success is necessary but not universally sufficient.

### Regular-file write

Write permission allows eligible content modification, but immutable, append-only, read-only mount, seals, mandatory locks, leases, quotas, or security policy can still reject it.

Writing can clear set-user-ID, set-group-ID, or file capability state under platform rules because privileged executable content has changed.

### Execute

Execution requires a regular executable format or interpreter path plus applicable file, directory, mount, credential-transition, and security-policy checks. Scripts add permission and resolution of the interpreter.

Set-ID bits and file capabilities can transform process credentials. `nosuid` and no-new-privileges-like mechanisms constrain elevation but have precise scope.

### Owner class

If the mapped subject identity matches the object's mapped owner, the owner entry supplies the DAC result. The implementation does not then add group or other bits to make access more permissive.

This class-selection rule surprises users who assume group membership can compensate for restrictive owner bits.

### Group class

If no owner match exists and an ACL named-user entry does not decide, matching owning or supplementary groups contribute through group-class rules. POSIX ACL evaluation can union matching group entries before applying the mask.

Group membership is captured from the credential snapshot. Remote or dynamic group services do not retroactively change an already constructed kernel credential unless the system refreshes it.

### Other class

If neither owner nor relevant named or group entries match, the other entry supplies the DAC result. It is not a fallback added after an explicit denial in another selected class.

Additional mandatory or mount policy still applies. “World readable” under DAC does not necessarily make encrypted or labeled content accessible.

### Mode representation

Nine basic bits encode owner, group, and other read, write, and execute or search permissions. The inode mode also carries type and special set-ID and sticky bits.

Use masks and standard predicates rather than decimal assumptions or string parsing. Preserve type bits when changing permission fields through the correct API.

### Creation mask

A process supplies a requested mode, and the creation mask removes selected permission bits when no inheritable ACL changes the derivation. The mask never adds requested permissions.

Creation happens atomically relative to publication. Creating permissively and tightening later exposes a race window.

### Default ACL inheritance

A directory default ACL supplies inherited entries for a new child. The requested mode constrains the derived access ACL and corresponding mode classes under the ACL algorithm.

Default ACL inheritance differs from copying the parent's access ACL. File type, requested execute bits, and platform semantics remain relevant.

### Access ACL entries

A minimal ACL contains owner, owning group, and other entries corresponding to mode classes. Extended ACLs add named users, named groups, and a mandatory mask for group-class entries.

Entries are normalized, unique where required, and validated before publication. Unknown or malformed encodings fail safely.

### ACL mask

The mask bounds permissions for named users, the owning group, and named groups. The owner and other entries are not constrained by that mask.

Tools can show both stored and effective permissions. An entry granting `rwx` with mask `r-x` has effective `r-x`.

### ACL evaluation order

Evaluate mapped owner first, then a matching named-user entry, then all matching group-class entries, then other. Apply the mask to named-user and group-class results as specified.

Do not simply union every entry that mentions the subject. Selection and mask order are semantic requirements.

### `chmod` and ACL coherence

When an extended ACL exists, changing mode group-class bits updates or constrains the ACL mask; owner and other bits align with their ACL entries. The two interfaces remain views of one access policy.

An implementation that updates only cached mode while leaving an effective stale ACL creates a privilege discrepancy.

### Ownership changes

Changing owner or group requires appropriate privilege, ownership, group membership, namespace mappings, and filesystem support. It can transfer quota responsibility and update ctime.

`chown` may clear set-user-ID and set-group-ID bits; Linux can also remove file capability extended attributes under relevant changes. Callers reapply privileged metadata only after trusted content is complete.

### Set-user-ID

On eligible executable files, set-user-ID can set an execution credential from file ownership. It does not make every read or open privileged.

Mount policy, interpreter behavior, tracing, no-new-privileges state, user namespaces, and security modules can suppress or constrain the transition.

### Set-group-ID files

Set-group-ID on executable files can transform the effective group. On nonexecutable files its meaning is platform- and filesystem-sensitive, including mandatory-locking history.

Writing or changing ownership can clear it. Programs use documented execution semantics rather than inferring privilege from the bit alone.

### Set-group-ID directories

A setgid directory commonly causes new children to inherit the directory's group. New subdirectories can inherit setgid so the collaborative group tree continues.

Default ACLs and umask still determine permissions. Group inheritance is not an automatic grant of group write.

### Sticky directories

The sticky bit on a directory restricts removal and rename of contained entries even when a caller otherwise has parent write and search permission. Ownership and capability exceptions are precisely defined.

It protects names in shared directories such as temporary areas; it does not prevent reading or modifying file contents through independently granted access.

### File capabilities

Linux file capabilities are encoded in a security extended attribute and can contribute permitted capabilities during execution. Their interpretation includes user-namespace and root-ID rules.

They are privileged metadata. Copy, restore, and archive tools preserve them only with authorization and explicit policy, after content integrity is established.

### Process capabilities

Linux divides traditional superuser privilege into capability sets. `CAP_DAC_OVERRIDE` and `CAP_DAC_READ_SEARCH` bypass selected DAC checks but do not bypass every security mechanism.

Capabilities are interpreted in a user namespace and often require relation to the inode's namespace or mapped owner. Minimize bounding, permitted, effective, inheritable, and ambient sets.

### Root is contextual

UID zero in one user namespace is not universally privileged over every filesystem object. Capability possession and namespace ancestry determine many overrides.

Even globally privileged callers remain subject to some mount flags, immutable state, integrity policy, and mandatory access controls unless a specific override applies.

### ID-mapped mounts

An idmapped mount applies a mapping when interpreting filesystem ownership for operations through that mount. The on-disk UID and GID need not change.

Authorization, creation, ownership changes, set-ID behavior, and displayed identity use the applicable mapping. Raw numeric comparison without mount context is incorrect.

### User namespaces

User namespaces map identities and scope capabilities. A process can be privileged inside one namespace while unprivileged relative to the initial namespace and unrelated resources.

Filesystem support, mount ownership, and mapping representability affect operations. Unmappable IDs are handled explicitly rather than truncated or guessed.

### Mount read-only state

A read-only mount blocks filesystem modifications through that mount even if inode DAC grants write. The underlying superblock and per-mount flags can have distinct scope.

Open descriptors and alternate mounts require careful semantics. A policy checks the mount actually used for the operation.

### `noexec`, `nosuid`, and `nodev`

`noexec` restricts direct execution through a mount; `nosuid` suppresses specified set-ID and file-capability effects; `nodev` prevents interpreting special files as devices through that mount.

These are defense layers, not universal sandboxes. An interpreter can read a script from a noexec mount when ordinary read and interpreter policy allow it.

### Inode flags

Immutable and append-only flags can reject writes, truncation, unlink, rename, or metadata changes beyond basic mode decisions. Changing them requires specific authority.

Filesystem support and namespace capability checks vary. Applications report unsupported state rather than silently treating mode bits as equivalent.

### Extended attributes

Extended-attribute namespaces have separate access rules. `user` attributes are generally application data, while `security`, `system`, and `trusted` namespaces can encode kernel or privileged policy.

Names, values, total storage, types, and permissions are bounded. Copying arbitrary privileged attributes from an untrusted archive is unsafe.

### Mandatory access control

Linux security modules can apply labels and policy after or alongside DAC. A DAC grant does not override mandatory denial, and capability overrides need not bypass the module.

Policy version and label transition are part of the authorization evidence. Avoid describing one implementation's hook order as a universal theorem.

### Access checks versus open

`access`-family calls answer a specific question, often using real rather than effective credentials unless flags request otherwise. They are useful when a privileged program asks whether the invoking identity could access a path.

They are not a safe preflight for later `open`: the namespace, metadata, credentials, or policy can change. Attempt the operation with correct flags and handle its result.

### Check-then-use races

Checking ownership or mode by pathname and reopening later performs two resolutions. An attacker can replace a component or final object between them.

Open the desired object relative to a trusted directory with explicit resolution policy, then inspect or operate on that stable handle. Creation uses no-replace and restrictive modes atomically.

### Open-time and use-time authority

An open file description retains object and access mode even after rename or chmod. Many reads and writes rely on permission checked at open, while later operations can still enforce mount, lease, seal, security, or operation-specific checks.

Document revocation semantics. Removing pathname permission does not necessarily revoke existing descriptors or memory mappings.

### Descriptor passing

Passing a descriptor transfers access to the referenced open file description independent of whether the receiver could resolve its path. This is deliberate capability-style delegation.

The sender limits access mode and object type, and the receiver validates protocol context. Close-on-exec controls accidental inheritance.

### Deletion and rename

Removal and rename primarily require rights on involved parent directories plus search, sticky, mount, topology, and policy checks. Target data write permission is not the governing right.

Cross-directory rename checks both parents and possible victim. Authorization and namespace mutation occur under the same locking context.

### Hard links

Creating a hard link requires destination-parent authority and filesystem policy on linking the existing object. Protections can restrict linking files not owned by the caller or writable by others.

Hard links share inode permissions and metadata. They are not independent copies and cannot cross filesystem boundaries.

### Symbolic links

Symlink contents are path text; access is normally governed during resolution of containing directories and the final target or link operation. Symlink ownership matters for some sticky-directory and protected-link policies.

Flags choose whether the final symlink is followed. Ownership change of the link itself uses no-follow operations where supported.

### Network filesystems

Remote filesystems translate client credentials, server identities, ACL models, exports, and caching. Server-side authorization is authoritative for server resources.

Root squashing, ID mapping, token expiry, lease state, and ACL translation can produce behavior unlike a local inode. Cached permissions require invalidation on policy changes.

### Permission caching

VFS and remote clients can cache ACLs or authorization-relevant metadata. Cache keys include object generation and policy or credential context sufficient for correctness.

Revocation defines invalidation or maximum staleness. A cache optimized for read metadata must not retain privilege past the security contract.

### Creation workflow

A secure service opens a trusted parent, resolves beneath it, creates without replacement using a restrictive initial mode, writes through the returned handle, validates type and ownership, then applies final metadata.

Privileged attributes and set-ID state are applied only after trusted contents are complete. Durability uses the file and directory synchronization protocol separately from authorization.

### Archive extraction

An extractor rejects absolute paths, dot-dot escape, unsafe symlinks, mount crossing, special files, oversized metadata, and unauthorized owners or labels. It treats archive identity numbers as data to map under policy.

Create safely first, then populate, verify, and apply permitted final metadata. Never reproduce file capabilities or devices solely because the archive requests them.

### Audit

Record operation, stable object and parent identifiers, resolution policy, credential and namespace identities, mapped owner class, ACL branch and mask, capability used, mount and inode constraints, mandatory-policy decision, outcome, and error.

Redact sensitive path components, labels, and attribute values. Audit records are integrity protected and state time, policy version, and incomplete visibility.

### Testing

Generate owner, named-user, owning-group, multiple matching-group, other, masked, unmapped, privileged, and mandatory-policy subjects across file types and operations. Vary every path component and mount.

Race rename, symlink replacement, chmod, chown, ACL and label update, credential replacement, descriptor passing, mount changes, remote revocation, and deletion. Verify actual operation results, not just preflight calls.

### Security and assurance

Threat models include malicious local users, compromised containers, hostile archives, confused deputies, stale remote clients, privileged backup tools, and corrupted permission metadata.

Assurance names VFS, filesystem, identity, container, security-module, remote-storage, concurrency, audit, and independent-verification reviewers. A mode-bit matrix alone cannot certify the composed policy.

## Definitions and Notation

Let credential snapshot `C=(ruid,euid,fsuid,rgid,egid,fsgid,G,Cap,U,L_c)`: real, effective, and filesystem IDs, supplementary groups `G`, capability sets `Cap`, user namespace `U`, and subject label `L_c`.

Let object state `O=(I,type,uid,gid,mode,acl,xattr,flags,L_o)`, mount context `M=(idmap,ro,noexec,nosuid,nodev,...)`, and request `A=(op,N,S,P,O,C,M,t)`. Parent state is included for namespace mutation.

Represent permissions as subsets of `{r,w,x}`. If ACL named-user or group-class result is `p` and mask is `m`, effective permission is `p intersection m`. Owner and other ACL entries are not mask-constrained.

Authorization `Allow(A)` is the conjunction or specified composition of successful resolution search, operation-specific DAC or authorized override, mount and object constraints, capability scope, mandatory policy, and current state. Denial in a non-overridden required layer denies the operation.

## Mechanisms, Invariants, or Proof Structure

1. **Capture context.** Retain one credential snapshot, mount and namespace view, security-policy generation, operation, and starting handle.
2. **Resolve safely.** Walk each component from the correct root or directory handle, enforce search and policy, bound indirection, and apply final follow rules.
3. **Bind identities.** Use stable parent and object references and interpret owner and group through the applicable user and mount mappings.
4. **Evaluate DAC exactly.** Select owner, named-user, matching group-class, or other branch and apply the ACL mask under the formal order.
5. **Apply additional policy.** Check capabilities, read-only and other mount flags, immutable or append state, security modules, leases, seals, and operation constraints.
6. **Authorize the actual mutation.** Couple the decision to open, create, delete, rename, chmod, chown, ACL, xattr, or execute without a pathname gap.
7. **Preserve privilege invariants.** Derive creation metadata atomically and clear or revalidate set-ID and file capabilities after ownership or content changes.
8. **Publish recoverably.** Update mode, ACL, owner, labels, quota, timestamps, and directory state as one recoverable transition where required.
9. **Define retained authority.** Specify descriptor, mapping, credential-change, revocation, remote-cache, and use-time behavior.
10. **Fail closed and precisely.** Reject unmappable IDs, unsupported features, malformed ACLs, stale generations, and unavailable enforcement without silent downgrade.
11. **Test the composition.** Cover identities, classes, masks, path components, object types, operations, races, mounts, namespaces, remote state, and recovery.
12. **Preserve evidence.** Retain stable identities, mapped credentials, decision branches, policy versions, outcomes, traces, limitations, and reviewer boundaries.

<!-- bijux-verify: {"id":"acl-mask-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entry=rwx mask=r-x effective=r-x\nrequest=read allowed=True\nrequest=write allowed=False\nrequest=execute allowed=True\n","stderr":""}} -->
```python
order = "rwx"
entry = set("rwx")
mask = set("rx")
effective = entry & mask


def render(bits: set[str]) -> str:
    return "".join(symbol if symbol in bits else "-" for symbol in order)


print(f"entry={render(entry)} mask={render(mask)} effective={render(effective)}")
for operation, symbol in (("read", "r"), ("write", "w"), ("execute", "x")):
    print(f"request={operation} allowed={symbol in effective}")
```

The executable model demonstrates one named-entry ACL mask intersection. It omits branch selection, IDs, groups, paths, capabilities, mounts, mandatory policy, races, and real kernel behavior.

## Alternatives and Trade-Offs

- Basic mode bits are compact and portable but express only owner, one group class, and other; ACLs add identities and inheritance at policy and tooling cost.
- Path-based APIs are convenient but race-prone across steps; handle-relative operations make identity explicit but require lifecycle discipline.
- Open-time authorization offers stable delegated handles but weakens immediate revocation; use-time rechecks improve revocation and cost latency and complexity.
- Numeric ownership is efficient locally but ambiguous across domains; mapped identities enable isolation and sharing but enlarge context.
- File capabilities grant narrower executable privilege than setuid root but add namespace, xattr, copy, and integrity complexity.
- Default ACLs provide richer inheritance than umask but can surprise tools that display only mode bits.
- `noexec`, `nosuid`, and `nodev` add cheap mount-level defense but have deliberately limited semantics.
- Permission caching reduces remote and ACL lookup cost but creates revocation and generation obligations.
- Fail-closed unsupported-policy behavior protects boundaries but can reduce portability; silent fallback creates privilege risk.
- Rich audit improves investigation but can leak paths, labels, and identities or create denial-of-service pressure.
- Preserving all metadata during restore improves fidelity but can recreate obsolete privilege; policy-filtered restoration is safer and less exact.
- Central mandatory policy supports consistent enforcement but adds operational coupling; distributed policy improves autonomy and complicates coherence.

## Failure Modes and Misconceptions

- **“Permission belongs to a pathname.”** It belongs to resolved objects and context at a decision time.
- **“Directory read permits traversal.”** Search or execute permission governs traversal.
- **“All matching mode classes are unioned.”** Owner, group, or other class is selected under the algorithm.
- **“An ACL entry's printed bits are all effective.”** Named-user and group-class entries are mask constrained.
- **“Umask always directly determines final mode.”** Default ACL inheritance can change the derivation.
- **“Target write permission controls unlink.”** Parent directory rights and sticky policy govern namespace removal.
- **“Root bypasses every restriction.”** Capabilities, namespaces, mounts, flags, and mandatory policy constrain overrides.
- **“Raw UID equality proves ownership.”** ID mappings and namespace context matter.
- **“`access` then `open` is safe.”** Two path resolutions permit substitution.
- **“chmod revokes existing descriptors.”** Open-reference authority follows the documented use-time model.
- **“noexec prevents reading code into an interpreter.”** It restricts mount execution semantics, not every use of file bytes.
- **“Copying xattrs is harmless.”** Security labels and file capabilities can carry authority.
- **“Writing a privileged executable preserves its elevation.”** Set-ID or capabilities can be cleared for safety.
- **“Local DAC tests certify remote policy.”** Server identity mapping, ACLs, exports, caches, and revocation differ.

## Worked Examples

### Example 1

The file owner has mode `040`, while the owning group has read. Because the caller matches owner, owner class is selected and read is denied; group membership is not added.

### Example 2

A named-user ACL grants `rwx`, but mask `r-x` removes write. Effective output and authorization both show `r-x`.

### Example 3

A directory permits read but not search. A caller lists entry names but cannot open a known child through that directory.

### Example 4

A shared setgid directory gives a new file the directory's group. Its default ACL grants team access, while requested mode limits execute permission.

### Example 5

In a sticky temporary directory, one unprivileged user cannot unlink another user's entry despite parent write and search permission.

### Example 6

A privileged helper checks an attacker-controlled pathname with `access` and then opens it. A rename between calls redirects the open; handle-relative atomic open removes that gap.

### Example 7

A container sees a file as owned by UID 1000 through an idmapped mount although the disk stores another ID. The kernel evaluates the mapped relationship for that mount.

### Example 8

A deployment overwrites an executable carrying file capabilities. The capability attribute is removed under policy, then deliberately reapplied only after content verification.

### Example 9

A script on a `noexec` mount cannot be executed directly through that path, but an allowed interpreter may read it. The sandbox therefore needs broader policy than one mount flag.

### Example 10

A descriptor to a log is passed to a worker that cannot traverse the original directory. The worker writes through delegated handle authority without receiving pathname search access.

## Cross-Program Connections

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects descriptors, credentials, errors, ownership-safe wrappers, and resource lifetime. [Security Engineering](../../25-security-engineering/ROADMAP.md) deepens capabilities, mandatory access control, sandboxing, confused deputies, audit, and threat modeling.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects identity federation, remote ACLs, caching, leases, revocation, and authoritative server decisions. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies layered requirements, hazard analysis, traceability, and assurance.

Within this program, [OS-041](041-files-directories-and-namespaces.md) and [OS-042](042-inodes-and-metadata.md) supply naming and metadata; [OS-049](../ROADMAP.md) explains VFS enforcement hooks, and [OS-050](../ROADMAP.md) integrates secure creation with persistence.

## References

- Linux man-pages project, [path_resolution(7)](https://man7.org/linux/man-pages/man7/path_resolution.7.html), current page checked 2026-09-04. Roots, descriptor-relative paths, per-component search, final-component rules, mode-class selection, supplementary groups, and capability overrides.
- Linux man-pages project, [inode(7)](https://man7.org/linux/man-pages/man7/inode.7.html), current page checked 2026-09-04. Ownership, type, mode, permission and special bits, setgid directories, sticky directories, and metadata.
- Linux man-pages project, [acl(5)](https://man7.org/linux/man-pages/man5/acl.5.html), current page checked 2026-09-04. ACL entries, masks, evaluation order, object creation, default inheritance, correspondence with mode bits, and access checks.
- Linux man-pages project, [access(2)](https://man7.org/linux/man-pages/man2/access.2.html), current page checked 2026-09-04. Real versus effective identity checks, `faccessat2` flags, descriptor-relative operation, ACL handling, and check-use warnings.
- Linux man-pages project, [chmod(2)](https://man7.org/linux/man-pages/man2/chmod.2.html), current page checked 2026-09-04. Permission mutation, special bits, ownership constraints, descriptor-relative behavior, symlinks, errors, and security side effects.
- Linux man-pages project, [chown(2)](https://man7.org/linux/man-pages/man2/chown.2.html), current page checked 2026-09-04. Ownership and group changes, privilege and group requirements, set-ID clearing, file capabilities, symlinks, and errors.
- Linux man-pages project, [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html), current page checked 2026-09-04. Capability sets, DAC overrides, filesystem capabilities, execution transitions, user namespaces, and no-new-privileges interactions.
- Linux man-pages project, [xattr(7)](https://man7.org/linux/man-pages/man7/xattr.7.html), current page checked 2026-09-04. Extended-attribute namespaces, access rules, security and ACL uses, storage limits, and filesystem support.
- Linux kernel documentation, [Idmappings](https://docs.kernel.org/filesystems/idmappings.html), current page checked 2026-09-04. Caller, filesystem, and mount mappings for ownership checks, creation, chown, set-ID, and VFS helpers.
- Linux man-pages project, [mount(2)](https://man7.org/linux/man-pages/man2/mount.2.html), current page checked 2026-09-04. Read-only, noexec, nosuid, nodev, remount, per-mount and filesystem flags, and mount semantics.

## Exercises

### Exercise 1

Specify path and final-object authorization for read, write, execute, create, unlink, and rename. Include credentials, parents, mounts, and mandatory policy.

### Exercise 2

Evaluate a POSIX ACL with owner, named users, multiple matching groups, mask, and other. Explain chmod and default-ACL creation behavior.

### Exercise 3

Design a privileged content-installation workflow that handles ownership, modes, ACLs, set-ID, file capabilities, labels, xattrs, races, and durability.

### Exercise 4

Specify authorization across user namespaces, idmapped mounts, descriptor passing, containers, and a remote filesystem with cached ACLs.

### Exercise 5

Build a test and assurance plan for filesystem permissions. Include operation matrices, races, metadata corruption, audit, recovery, and reviewers.

## Answers to the Exercises

### Answer 1

Capture one credential, user namespace, mount namespace, mount mapping, security context, and policy generation. Resolve from a stable root or directory handle and require search plus mandatory policy on every traversed directory. Bind the final object and parents under operation locks. Read, write, and execute evaluate mapped owner or ACL selection, capability overrides, mount flags, inode flags, type, leases or seals, and mandatory policy.

Create requires parent write and search, derives owner, group, requested mode, umask or default ACL, and restrictive initial metadata atomically. Unlink and rename require appropriate source and destination parent authority, sticky checks, topology, mount, target-victim, and policy checks rather than target write permission. Couple the decision to mutation without reopening a string; failures leave the namespace unchanged.

### Answer 2

If mapped subject equals owner, select owner entry without mask. Otherwise, select an exact named-user entry if present and intersect it with the mask. Otherwise union permissions of all matching owning-group and named-group entries, then intersect that result with the mask. If none match, select other without mask. Do not add permissions from later branches after selection.

For an extended ACL, mode owner and other correspond to their entries, while mode group-class corresponds to the mask; chmod updates these coherently. During creation under a default ACL, inherit the directory's default entries into the child's access ACL and constrain them by requested mode. Without a default ACL, requested mode has umask bits removed. A directory can inherit a default ACL for future descendants; an ordinary file does not use one as a default policy container.

### Answer 3

Open a trusted destination directory, resolve beneath it with explicit no-escape policy, and create a private candidate without replacement using minimal rights. Write through the returned descriptor, reject special-file substitution, enforce size and quota bounds, synchronize content when required, and verify hashes. Map requested archive or package identities through an allowlist rather than trusting raw numbers.

Apply ordinary ownership, mode, and ACL coherently; filter xattr namespaces; set approved security labels through policy-aware APIs. Apply set-ID bits or file capabilities only after trusted content and ownership are final because writes or chown can clear them. Publish with atomic rename and synchronize affected directories for durability. Preserve every error, use handles for cleanup, and audit stable identity and policy decisions without leaking sensitive content.

### Answer 4

Model caller IDs in its user namespace, filesystem IDs, and the idmapped mount transformation explicitly. Check representability and capability scope relative to the owning namespace. A descriptor passed into a container delegates access to one opened object without granting path traversal; constrain its access mode and close-on-exec behavior. Path-based operations through another mount repeat authorization in that mount context.

For a remote filesystem, authenticate the protocol identity, map it to server IDs, evaluate server ACL and export policy authoritatively, and return defined errors. Cache ACLs and permission outcomes only with object generation, credential and policy context, lease or expiry, and invalidation on change. Root squashing and token expiry are tested. A local DAC grant cannot override a remote server denial, and a stale client cache cannot silently extend privilege beyond the declared revocation window.

### Answer 5

Generate subjects for owner, exact named user, owning group, several supplementary and named groups, other, mapped and unmapped IDs, each capability set, user namespaces, labels, and expired remote tokens. Generate file types, every mode and special-bit class, minimal and extended ACLs, masks, default inheritance, xattr namespaces, inode flags, mount flags, and read-only views. Exercise path search, read, write, append, execute, create, link, unlink, rename, chmod, chown, ACL and label update, open descriptors, mappings, and descriptor passing.

Race path replacement, symlink and mount changes, chmod, chown, ACL update, credential replacement, policy reload, remote revocation, and object reuse. Inject malformed ACLs, unmappable IDs, lost labels, metadata I/O errors, and crashes during policy mutation. Verify real operations plus durable recovered metadata, not `access` alone. Preserve identities, mappings, policies, kernels, filesystems, mounts, seeds, traces, audit output, raw results, and limitations. Named VFS, filesystem, identity, container, security-module, network-storage, concurrency, audit, recovery, and independent-verification reviewers assess claims.
