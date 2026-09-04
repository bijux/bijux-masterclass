---
module_id: OS-041
program: Operating Systems
level: 1
module_number: 41
title: Files, Directories, and Namespaces
status: complete
last_verified: 2026-09-04
---

# Files, Directories, and Namespaces

## One-Page Review

### Governing question

How should an operating system translate process-relative names into stable filesystem objects while preserving directory topology, permissions, mount views, link semantics, atomic updates, and safe behavior under concurrent namespace change?

### Essential definitions

- A **file** is a filesystem object with identity, type, metadata, content or device behavior, and lifecycle.
- A **directory** maps component names to filesystem objects and participates in a rooted hierarchy.
- A **pathname** is a sequence of components interpreted from a starting directory and namespace view.
- A **directory entry** binds one name in one parent directory to an object; cached entries are often called dentries.
- A **hard link** is another directory entry for the same object; a **symbolic link** stores a pathname to resolve later.
- A **mount namespace** selects the mount topology visible to a process or process group.
- An **open file description** records an opened object and status independently of one descriptor number or current pathname.

### Central model, mechanism, or theorem

Resolve request `R=(N,S,P,O,C,t)`: mount namespace `N`, starting directory `S`, pathname `P`, operation `O`, credentials `C`, and observation time `t`. Walking each component transforms current `(mount,dentry)` state through directory lookup, mount crossing, symbolic-link rules, `.` and `..`, and search permission. The final component is interpreted under operation-specific create, follow, replace, or remove semantics.

Names are references, not object identity. Multiple names can bind one object, one symbolic-link text can resolve differently by context, and an open reference can outlive all names. Correct multi-object mutations establish a linearization point or documented failure while preserving an acyclic directory topology and balanced object references.

### Critical invariants

- Every component is resolved from the caller's actual starting directory, root boundary, and mount namespace.
- Search permission and security policy are checked for each traversed directory using current credentials and mount context.
- Symbolic-link expansion, total path work, component length, and mount traversal are bounded.
- A directory cannot become its own ancestor; `.` and `..` retain root-boundary semantics.
- Rename, link, unlink, create, and remove update directory entries and object link counts atomically under their contracts.
- Open descriptions, mappings, current directories, mounts, and lookup references keep objects alive independently of names.
- Race-resistant callers bind follow-up operations to stable directory or object handles and explicit resolution policy.

### Common failures

Common mistakes are treating a pathname as a permanent object identifier, authorizing a string and reopening it later, confusing hard and symbolic links, assuming unlink destroys open content, using current working directory in concurrent code, following final symlinks unintentionally, allowing `..` or mount traversal to escape a boundary, iterating a mutating directory as a stable snapshot, and assuming rename provides cross-filesystem transactions.

### Compact example

A service opens trusted directory `/srv/jobs` and receives `tenant/output`. It resolves relative to the retained directory handle with policy that forbids symlink and mount escape, creates the final component without replacement, and verifies the returned object. An attacker who renames a parent or swaps in a symlink cannot redirect the operation between a string-based check and use because both resolution and creation occur under one handle-relative contract.

### Connections

[OS-021](021-critical-sections-in-the-kernel.md), [OS-024](024-atomic-operations.md), and [OS-025](025-deadlock-conditions-and-avoidance.md) establish concurrency and atomicity. [OS-042](../ROADMAP.md) through [OS-050](../ROADMAP.md) develop metadata, allocation, directories, links, mounting, consistency, and VFS integration.

## Governing Question

A pathname looks like a string, but resolution is a stateful traversal through directories, mounts, symbolic links, process roots, credentials, and concurrent mutations. The same text can identify different objects for two processes or at two times.

The governing question is how to make this traversal precise enough for ordinary use, atomic namespace mutation, isolation, and security. The answer separates names, objects, open references, and namespace views rather than collapsing them into “the file.”

## Why This Matters

Every program depends on namespace operations for executables, configuration, libraries, logs, temporary files, sockets, devices, and persistent data. Containers and service sandboxes rely on process-specific mount views and root boundaries.

Path races are a recurring security problem. Checking ownership or type and later reopening the same string gives an attacker time to replace a component. Symbolic links, bind mounts, renames, and mutable working directories make naive prefix checks especially fragile.

Namespace correctness also underlies recovery. Atomic rename enables publication patterns, hard-link counts govern reclamation, and mount topology determines which filesystem supplies persistence guarantees.

## Prerequisites and Retrieval

Review [OS-021](021-critical-sections-in-the-kernel.md), [OS-024](024-atomic-operations.md), [OS-025](025-deadlock-conditions-and-avoidance.md), and [OS-030](030-designing-an-ipc-mechanism-from-semantics-and-cost.md).

Retrieve these distinctions:

- pathname text, directory entry, inode-like object, open file description, and descriptor are different identities;
- current working directory, process root, directory handle, and mount namespace determine starting context;
- read permission on a directory differs from search or execute permission;
- a hard link adds a name to one object; a symbolic link stores text for a later lookup;
- unlink removes a directory entry, while object reclamation waits for links and live references;
- rename namespace atomicity differs from data durability and multi-filesystem transactions;
- lookup caches accelerate resolution but are not persistent truth;
- directory iteration usually does not promise a transactional snapshot during mutation.

## Learning Objectives

After this module, you should be able to:

1. model absolute, relative, handle-relative, root-constrained, and mount-aware pathname resolution;
2. distinguish object identity, directory entries, hard links, symbolic links, open descriptions, and descriptors;
3. trace create, link, unlink, mkdir, rmdir, and rename through validation, locking, mutation, and references;
4. reason about symlink loops, `..`, mount crossings, chroot-like roots, and namespace propagation;
5. design race-resistant filesystem APIs using directory handles and explicit resolution constraints;
6. diagnose stale lookup caches, directory iteration anomalies, topology races, and cross-filesystem failures;
7. construct concurrency, security, crash, and assurance tests for namespace operations.

## Core Exposition

### Object identity and names

Filesystem objects have identities independent of the strings used to reach them. A directory entry binds one component name in one parent to an object. Several entries can bind the same regular file.

Applications that need stable identity retain an opened handle and inspect object metadata. A pathname can be renamed, replaced, hidden by a mount, or resolve differently later.

### File types

Common object types include regular file, directory, symbolic link, FIFO, socket, block device, and character device. Operations and permissions depend on type.

Opening an untrusted path and then verifying the returned object's type is stronger than assuming a suffix or prefix proves type. Device and special-file opens can have effects unlike reading inert data.

### Directory mappings

A directory maps component names to object references plus filesystem-specific record data. The logical abstraction is not necessarily a flat array; implementations use linear records, hashes, trees, or indexed blocks.

Directory modification updates both namespace and object metadata. Malformed records must not create duplicate live names, invalid references, or traversal outside verified bounds.

### Absolute paths

An absolute pathname begins at the calling process's root directory, not necessarily a machine-global root. Mount namespaces and root-changing mechanisms can give processes different interpretations of `/`.

Walking `..` at the process root does not escape above it under ordinary resolution rules. Bind mounts and namespace topology still require explicit policy.

### Relative paths

A traditional relative path starts at the process's current working directory. Because threads commonly share process filesystem context, changing that directory can affect unrelated resolution.

Library and service code prefers an explicit directory descriptor when location matters. This makes the dependency a handle rather than mutable ambient state.

### Components and separators

Resolution splits a pathname into components separated by slash. Empty runs are handled by platform rules, and a trailing slash generally requires the preceding component to resolve as a directory or eligible directory creation target.

Component and total expanded-path limits are filesystem and system properties. Reject overflow and overlong input without truncating into a different valid name.

### Dot and dot-dot

`.` retains the current directory. `..` moves to its logical parent, with special handling at roots and mount boundaries. These meanings are supplied by resolution semantics even if no literal on-disk entry exists.

Confinement cannot safely remove `../` from a string and declare success. Symbolic links, renames, and mounts change the traversal graph.

### Search permission

Each nonfinal directory requires search permission or an authorized override under current credentials. Listing names requires directory read permission, which is a different capability.

The final operation adds checks for the target and parent: creation, removal, execution, opening, and metadata change have distinct rules. Mount flags, ACLs, capabilities, labels, and filesystem policy can add decisions.

### Symbolic links

A symbolic link stores pathname text. When followed, absolute target text restarts at the process root; relative target text is interpreted from the directory containing the link.

Links can form cycles or create excessive expansion. The resolver bounds traversals and work and returns a defined error rather than recursing without limit.

### Final-component policy

Some operations follow a final symlink; others operate on the link itself; still others accept flags that choose behavior. The final component can also be absent when the operation intends to create it.

Callers state whether an existing target may be replaced, must be a directory, must not be a symlink, or must not cross a mount. Implicit defaults are dangerous at trust boundaries.

### Hard links

A hard link creates a new directory entry for an existing object. Both names are peers; neither is the original. Content and object metadata are shared because identity is shared.

Hard links normally cannot cross filesystems and are restricted for directories to preserve topology. Link counts and filesystem limits are checked atomically with insertion.

### Unlink and object lifetime

Unlink removes one name and decrements the object's link count. If other hard links exist, they continue to resolve. If no names remain, open descriptions and mappings can still keep content alive.

Storage is reclaimable only after namespace and live-reference conditions are both satisfied under filesystem recovery rules. Reusing an object number too early risks aliasing stale references.

### Directory removal

Removing a directory requires the target to be eligible and empty under the filesystem's definition. Root, current-working-directory, mount-point, and policy constraints can reject removal.

Parent and victim locks prevent new children from racing the emptiness decision. A directory is never hard-linked into a cycle as a side effect.

### Rename

Rename changes a name or parent while keeping the underlying opened object alive. Within its supported scope, replacement is namespace-atomic: observers do not see the destination absent between old and new bindings.

Atomic visibility does not imply storage durability. Crash-safe publication needs file and directory synchronization under filesystem rules.

### Rename variants

No-replace avoids overwriting an existing destination; exchange atomically swaps two names; overlay filesystems can use whiteout semantics. Feature support and restrictions vary by filesystem.

The source and destination may temporarily both name the source object under ordinary rename visibility rules. Applications rely on the documented contract, not assumed implementation steps.

### Cross-directory rename

Moving across directories changes topology and touches two parents plus source and possible target. Lock ordering must prevent deadlock and ensure a directory never moves below its own descendant.

Linux documents ancestor-first and object-order rules with a per-filesystem rename lock for the hardest cases. Other systems may use different mechanisms with the same topology obligations.

### Cross-filesystem boundaries

A normal rename cannot provide one atomic namespace move across independent filesystems. Applications often copy, synchronize, publish, and remove, but that sequence has partial-failure and concurrency states.

Make the non-atomic migration explicit, preserve metadata deliberately, and design restart and duplicate handling. Do not label it rename-equivalent.

### Open file descriptions

Opening resolves a name and creates or references an open file description containing object, offset, and status. Descriptors are process-table references to that description and can be duplicated or inherited.

Rename and unlink do not redirect or invalidate an existing open description. Authorization at later operations also follows the platform's open-time and use-time rules.

### Directory handles and `*at` APIs

Handle-relative operations interpret a relative path from an opened directory rather than ambient current working directory. The handle pins a directory object even if its name changes.

This supports race-resistant trees: open a trusted parent, resolve children relative to it, and keep returned object handles for subsequent work. It also avoids global process state changes.

### Constrained resolution

Linux `openat2` can request policies such as staying beneath or inside a directory, refusing symlinks, refusing magic links, or refusing mount crossings. Each flag has precise semantics and compatibility costs.

Treat unsupported constraints as failure, not silent downgrade. Recheck feature availability and error policy on the deployed kernel and filesystem.

### Check-then-use races

Calling `stat(path)`, validating it, and later calling `open(path)` performs two resolutions. An attacker can replace any mutable component between them, so the second operation may target another object.

Open with the desired flags and constraints first, then inspect the returned handle. For multi-step traversal, retain directory handles and avoid reconstructing trusted path strings.

### Directory-entry cache

The VFS can cache positive entries mapping names to objects and negative entries recording a recent miss. This accelerates lookup but must respond to local mutation and remote invalidation.

Cache entries are in-memory views, not durable directory records. Generation, revalidation, leases, or filesystem callbacks determine whether a cached answer remains usable.

### Lookup concurrency

Read-side path walking can use optimistic or RCU-like traversal while mutations use stronger locks and sequence checks. If a rename invalidates the observed topology, lookup retries under a stable mode.

Correctness requires the final object and mount path to belong to one permitted traversal history. Combining components from incompatible generations can escape constraints.

### Mount points

A mount attaches a filesystem tree at a directory in a namespace. Walking into the mount switches to its root; walking `..` at that root can return to the covered parent according to namespace rules.

The covered directory still exists but is hidden through that mount path. Unmount reveals it again; open handles into either tree can remain meaningful under lifecycle rules.

### Mount namespaces

A mount namespace contains a process-visible mount list and forms one directory hierarchy. Cloning or unsharing can create a copy whose later mount changes are isolated by default.

The same absolute pathname can therefore resolve to different objects in two namespaces. Diagnostics record namespace and mount IDs rather than assuming `/path` is globally unique.

### Mount propagation

Shared, private, slave, and unbindable mount relationships govern how mount and unmount events propagate among peer trees. Isolation depends on propagation setup, not only creating a namespace.

Container setup makes intended mounts private or otherwise controlled before applying changes. An accidental shared subtree can leak mounts across boundaries.

### Bind mounts and alternate views

A bind mount exposes an existing subtree at another location, creating another namespace path to the same underlying objects. This differs from hard linking a directory and operates at the mount layer.

Policy that forbids filesystem crossing may also reject bind-mount traversal. Prefix comparisons cannot detect every alternate view.

### Root changes and confinement

Changing a process root affects pathname resolution but is not by itself a complete security boundary. Open descriptors, current directories, mount relationships, credentials, and namespace operations can retain escape routes.

Confinement composes root, mount namespace, capabilities, descriptor hygiene, process isolation, and explicit resolution constraints. Test adversarial topology changes.

### Directory iteration

Directory iteration returns records and continuation positions under filesystem-specific ordering. Concurrent insertion, removal, or rename can cause entries to appear, disappear, or be revisited unless a stronger contract is provided.

Treat names as arbitrary byte sequences under platform rules, not newline-delimited safe text. Validate record lengths and use escaping in diagnostics.

### Network and distributed namespaces

Remote filesystems add client caches, server identities, leases, retries, and uncertain outcomes. A request can succeed at the server and lose its reply, so blind retry of non-idempotent mutation can duplicate effects or misreport failure.

Stable file handles and operation identifiers help, but server reboot and export changes require generation validation. POSIX-like local semantics may be approximated within a documented consistency model.

### Crash consistency

After create, link, unlink, or rename returns, namespace change may be visible in memory without surviving a crash. Durable update depends on filesystem journaling, ordering, and explicit synchronization of files and parent directories.

Design recovery for every prefix of persistence. Atomic rename is a powerful publication primitive only when content and directory durability are both handled.

### Observability and experiments

Record operation, start handle and namespace, component count, symlink and mount traversals, cache hit or revalidation, retry, filesystem, latency, outcome, and error. Protect full pathnames as potentially sensitive.

Test hot and cold lookup, deep and wide directories, rename storms, symlink chains, negative cache churn, mount propagation, remote invalidation, crashes, and mixed create-remove workloads with raw traces and configuration.

### Security and assurance

Namespace input is attacker-controlled. Bound lengths and expansions, enforce per-component search, constrain symlinks and mounts where required, validate returned objects, and avoid logging raw names unsafely.

Assurance covers topology acyclicity, atomic link-count transitions, reference lifetime, race-resistant authorization, namespace isolation, deadlock freedom, crash recovery, and residual platform limits.

## Definitions and Notation

Let namespace view `N` contain mounts, process root `r`, starting directory `s`, credentials `c`, pathname components `P=(p_1,...,p_k)`, operation `o`, and time-varying namespace generation `g`. Resolution is `L(N,r,s,P,o,c,g)` returning `(mount,dentry,object)` or an error.

Directory relation `D(parent,name)=object` is partial and time-varying. Hard-link count `h(x)` counts eligible directory bindings to object `x`; live reference count `q(x)` includes open descriptions, mappings, current directories, mounts, and transient kernel users under implementation rules.

Object reclamation requires the filesystem's terminal predicate, commonly including `h(x)=0` and no preserving references. Namespace atomicity linearizes a mutation in the visible directory relation but does not imply durable persistence.

## Mechanisms, Invariants, or Proof Structure

A reviewable namespace mechanism follows twelve obligations:

1. Define start directory, process root, mount namespace, credentials, operation, and final-component policy.
2. Parse components without truncation, overflow, or unsafe normalization of arbitrary names.
3. Check search and security policy at every traversed directory and mount transition.
4. Bound symlink, magic-link, mount, `..`, component, and total resolution work.
5. Preserve stable object identity across rename, unlink, descriptor reuse, and cached lookup.
6. Order directory and object locks to prevent cycles, deadlock, and partial multi-object mutation.
7. Update entries, link counts, parents, caches, timestamps, and references atomically under operation semantics.
8. Keep open descriptions, mappings, roots, working directories, and mounts alive until their references end.
9. Revalidate optimistic lookup after concurrent rename, remote change, or namespace generation movement.
10. Define cross-filesystem, distributed retry, mount-propagation, and crash behavior explicitly.
11. Use handle-relative constrained APIs for security decisions and validate returned objects.
12. Test topology, races, failures, durability, isolation, and adversarial names with preserved evidence.

The executable toy separates namespace names, shared object identity, and an open reference that survives unlink.

<!-- bijux-verify: {"id":"namespace-object-lifetime","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"names=/archive/item,/data/item same-object=True links=2\nafter-unlink names=/archive/item links=1 open-readable=payload\nafter-rename names=/published/item object=inode-1 open-readable=payload\n","stderr":""}} -->
```python
objects = {"inode-1": {"content": "payload", "links": 0}}
namespace = {}

def link(path, object_id):
    if path in namespace:
        raise ValueError("name exists")
    namespace[path] = object_id
    objects[object_id]["links"] += 1

def unlink(path):
    object_id = namespace.pop(path)
    objects[object_id]["links"] -= 1

link("/data/item", "inode-1")
link("/archive/item", "inode-1")
open_object = namespace["/data/item"]
names = ",".join(sorted(namespace))
print(f"names={names} same-object={namespace['/data/item'] == namespace['/archive/item']} links={objects['inode-1']['links']}")
unlink("/data/item")
names = ",".join(sorted(namespace))
print(f"after-unlink names={names} links={objects['inode-1']['links']} open-readable={objects[open_object]['content']}")
namespace["/published/item"] = namespace.pop("/archive/item")
names = ",".join(sorted(namespace))
print(f"after-rename names={names} object={namespace['/published/item']} open-readable={objects[open_object]['content']}")
```

The toy serializes one flat namespace and manual link counts. It omits directories, mounts, permissions, symlinks, descriptors, locks, failures, caches, crash recovery, and actual object reclamation.

## Alternatives and Trade-Offs

- Absolute paths are convenient but depend on process root and mount namespace.
- Current-directory-relative paths are concise but rely on mutable ambient state.
- Directory-handle-relative APIs add handle management but improve race resistance and composability.
- Symbolic links provide flexible indirection but expand traversal and attack surface.
- Hard links preserve object identity but complicate ownership expectations and reclamation.
- Optimistic cached lookup scales reads but requires sequence validation and fallback.
- Coarse namespace locking simplifies consistency but serializes unrelated paths.
- Ordered fine-grained locks improve concurrency but make rename and ancestry proofs harder.
- Private mount propagation improves isolation but requires explicit sharing for desired updates.
- Shared propagation eases system-wide mount distribution but can violate container boundaries.
- Atomic same-filesystem rename simplifies publication but does not cross filesystems or ensure durability.
- Strict no-symlink and no-mount policies protect narrow trust boundaries but can reject legitimate system layouts.

## Failure Modes and Misconceptions

1. **“A pathname is a file identifier.”** resolution depends on namespace, start, credentials, and time.
2. **“The first hard link is the original.”** all hard-link names are peers for one object.
3. **“A symbolic link points directly to an inode.”** it stores text resolved in context.
4. **“Unlink immediately deletes open data.”** live open and mapping references can preserve the object.
5. **“Close after unlink restores the name.”** object lifetime and directory binding are separate.
6. **“Read permission lets a process traverse a directory.”** search permission controls traversal.
7. **“Removing `..` makes a path confined.”** symlinks, mounts, roots, and races defeat string filtering.
8. **“`stat` then `open` validates one object.”** two resolutions can observe different objects.
9. **“Rename is a cross-filesystem transaction.”** ordinary atomic rename is filesystem-scoped.
10. **“Atomic rename means crash durable.”** persistence requires filesystem synchronization rules.
11. **“A new mount namespace is always isolated.”** propagation relationships can transmit events.
12. **“Directory iteration is a snapshot.”** concurrent mutation can change observed entries and positions.
13. **“The dentry cache is filesystem truth.”** cached positives and negatives require invalidation or revalidation.
14. **“Root change alone is a sandbox.”** descriptors, mounts, credentials, and other resources compose confinement.

## Worked Examples

### Example 1

Two hard links `/a/report` and `/b/latest` resolve to one object. Writing through either changes the same content; unlinking one leaves the other and any open descriptions valid.

### Example 2

A relative symlink `next -> ../release/current` is located in `/srv/app`. Its target is interpreted from `/srv/app`, not the caller's current working directory.

### Example 3

A thread changes the process working directory while another library opens `config`. The result depends on timing; an explicit retained directory handle removes that ambient race.

### Example 4

A service checks `/uploads/x` and later opens it. An attacker replaces `uploads` with a symlink between calls. Handle-relative constrained resolution and post-open verification prevent redirection.

### Example 5

A same-directory rename replaces `live` with `candidate`. Concurrent lookup sees either old or new target at `live`, not a required interval with no destination name; durability remains separate.

### Example 6

A cross-directory move attempts to place directory `A` below its descendant `A/B`. Ancestry validation rejects the cycle before namespace mutation.

### Example 7

An open log file is unlinked during rotation. The writer continues through its open description while new opens by the old name fail or reach a new object.

### Example 8

Two containers use different mount namespaces, and `/etc/service.conf` resolves to distinct objects. A diagnostic that records only the pathname cannot explain their differing content.

### Example 9

A mount expected to stay private belongs to a shared peer group. A child namespace mount propagates unexpectedly to the host view, showing why propagation state is part of isolation review.

### Example 10

A remote link operation succeeds at the server but its reply is lost. A blind retry receives “exists”; reconciliation by object identity determines success more reliably than the second return code alone.

## Cross-Program Connections

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects descriptor-relative APIs, path encoding, errors, and resource lifetimes. [Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies race, fault-injection, property, model, and crash testing.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames path traversal, symlink races, capabilities, sandbox escape, audit privacy, and least privilege. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) connects remote namespace consistency, retries, leases, identity, and uncertain outcomes.

Within this program, [OS-021](021-critical-sections-in-the-kernel.md), [OS-024](024-atomic-operations.md), and [OS-025](025-deadlock-conditions-and-avoidance.md) supply concurrency foundations; [OS-042](../ROADMAP.md) through [OS-046](../ROADMAP.md) deepen inode, allocation, directory, link, and mount mechanisms.

## References

- The Open Group, [POSIX.1-2024 General Concepts: Pathname Resolution](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap04.html), current specification checked 2026-09-04. Path components, roots, directory entries, symbolic links, filenames, trailing slashes, limits, and resolution failures.
- Linux man-pages project, [path_resolution(7)](https://man7.org/linux/man-pages/man7/path_resolution.7.html), current page checked 2026-09-04. Process roots, current and descriptor-relative starts, component walk, mount points, dot and dot-dot, symlinks, trailing slashes, limits, and permissions.
- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. VFS abstraction, dentries, inodes, files, directory lookup, positive and negative entries, links, unlink, rename, and mount operations.
- Linux kernel documentation, [Pathname lookup](https://docs.kernel.org/filesystems/path-lookup.html), current page checked 2026-09-04. Cached and filesystem lookup, RCU and reference walks, sequence validation, rename races, symlinks, mount traversal, constrained lookup, and security.
- Linux kernel documentation, [Directory Locking](https://docs.kernel.org/filesystems/directory-locking.html), current page checked 2026-09-04. Read, create, remove, link, same-directory and cross-directory rename locks, ancestry, multi-filesystem ordering, and deadlock argument.
- Linux man-pages project, [openat2(2)](https://man7.org/linux/man-pages/man2/openat2.2.html), current page checked 2026-09-04. Directory-relative opening, extensible arguments, no-symlink and no-magic-link policy, beneath and in-root confinement, mount crossing, errors, and compatibility.
- Linux man-pages project, [mount_namespaces(7)](https://man7.org/linux/man-pages/man7/mount_namespaces.7.html), current page checked 2026-09-04. Per-namespace mount views, clone and unshare, shared subtrees, propagation modes, bind mounts, and lifecycle behavior.
- Linux man-pages project, [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html), current page checked 2026-09-04. Namespace replacement atomicity, open and hard-link stability, descriptor-relative operation, exchange, no-replace, whiteout, and failure behavior.
- Linux man-pages project, [link(2)](https://man7.org/linux/man-pages/man2/link.2.html), current page checked 2026-09-04. Peer names for one object, descriptor-relative linking, final symlink behavior, cross-filesystem limits, errors, and uncertain NFS outcomes.
- Linux man-pages project, [getdents(2)](https://man7.org/linux/man-pages/man2/getdents.2.html), current page checked 2026-09-04. Directory-entry record layout, offsets, record lengths, types, partial buffers, end-of-directory, and errors.

## Exercises

### Exercise 1

Specify a pathname resolver for absolute, current-directory-relative, and directory-handle-relative paths. Cover roots, mounts, symlinks, `..`, permissions, final policy, and bounds.

### Exercise 2

Design create, hard-link, unlink, and object-reclamation transitions. Include entries, link counts, open references, failures, and crash recovery.

### Exercise 3

Specify same-directory and cross-directory rename with replacement and exchange. Prove topology safety, lock ordering, atomic visibility, and limits.

### Exercise 4

Design a secure archive extractor beneath a trusted directory. Cover adversarial names, symlinks, mounts, races, special files, quotas, and evidence.

### Exercise 5

Build a test and assurance plan for mount namespaces and directory operations on local and remote filesystems. Include concurrency, propagation, crashes, retries, and reviewers.

## Answers to the Exercises

### Answer 1

Capture mount namespace, process root, start directory, credentials, operation, flags, and namespace generation. Absolute input starts at the process root; ordinary relative input starts at current working directory; handle-relative input starts at the referenced directory. Parse without truncation, reject invalid empty or overlong cases, and require search authorization at each directory.

For each component, process `.` and root-bounded `..`, consult a validated dentry or filesystem lookup, cross mounts only when policy allows, and expand relative symlink targets from their containing directory or absolute targets from root. Bound total components, links, bytes, mounts, and retries. Apply operation-specific follow, no-follow, create, replace, directory, and absence rules at the final component. Retry optimistic lookup after generation change or fail within the declared policy.

### Answer 2

Create validates an absent final name, authorizes and exclusively stabilizes the parent, allocates initialized object and directory state, then atomically publishes entry and initial link count or unwinds all allocations. Hard link stabilizes source object and destination parent, forbids disallowed types and cross-filesystem relationships, increments link count with entry publication, and handles limits.

Unlink stabilizes parent and victim, verifies current binding and sticky or security policy, atomically removes the entry and decrements link count, then invalidates lookup cache. The object remains while other links, open descriptions, mappings, current directories, mounts, or transient references preserve it. Reclamation begins only at the filesystem's terminal predicate and is crash-recoverable through its journal or recovery design. Every failure leaves either old or new complete state, never a live entry with an unbalanced count.

### Answer 3

For a same-parent rename, lock the parent exclusively, resolve source and target, then lock required non-directory victims in the filesystem's total order. Validate type, emptiness, mount, flags, and ancestry before atomically replacing, exchanging, or moving entries and updating link counts and parent metadata.

For cross-directory rename, take the filesystem topology lock, verify a common tree and stable ancestry, lock parents ancestor-first, reject placing a directory below its descendant, then lock directory children source-before-target and nondirectories in total order. The linearization point changes all affected bindings under lock; failure before it leaves old state. The rank ordering proves no lock cycle if directory ancestry is acyclic. Cross-filesystem moves return the defined boundary error; atomic namespace visibility does not prove crash durability.

### Answer 4

Open the destination root once with minimal rights. Reject absolute paths, empty components as required, dot and dot-dot traversal, overlong names, NUL ambiguity, and unsupported types. Resolve parents relative to retained directory handles with no-symlink, no-magic-link, beneath or in-root, and no-mount-crossing constraints as supported. Treat unavailable security features as failure.

Create final entries without replacement, set restrictive initial permissions, write through returned handles, validate regular-file type and ownership, synchronize content and directory state if durability is required, then publish atomically. Never pre-check and reopen a string. Bound files, total bytes, depth, sparse expansion, links, metadata, CPU, and time. Escape arbitrary names in logs and retain operation IDs, handle-derived identity, outcomes, and policy version without exposing sensitive full paths.

### Answer 5

Create isolated mount namespaces with private, shared, slave, and unbindable propagation topologies. Verify the same absolute path can intentionally resolve differently, intended mount events propagate exactly where specified, open handles remain valid under rename and unmount rules, and root plus descriptor constraints prevent escape.

Stress lookup, create, link, unlink, rmdir, rename replacement and exchange, cross-directory ancestry, directory iteration, negative dentries, symlink loops, bind mounts, concurrent namespace changes, crash points, and remote lost replies or lease invalidation. Preserve namespace and mount IDs, object identities, operation IDs, lock and retry traces, filesystem and server versions, durability calls, raw outcomes, and limitations. Named VFS, filesystem, container-runtime, distributed-storage, security, concurrency, recovery, and independent-verification reviewers assess residual risk; passing local pathname tests alone does not certify isolation or remote consistency.
