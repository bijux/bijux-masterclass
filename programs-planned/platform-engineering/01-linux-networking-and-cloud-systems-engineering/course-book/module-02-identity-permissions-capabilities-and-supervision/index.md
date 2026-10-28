# Module 02 — Identity, Permissions, Capabilities, and Service Supervision

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** Which authority should each process possess, and who is responsible for keeping it running?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Give Atlas dedicated service identities, owned directories, restrictive modes, hardened systemd units, and unambiguous restart and shutdown policy.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Reason about users, groups, mode bits, umask, ACLs, set-user-ID, and effective identity.
- Use Linux capabilities only when a narrow kernel privilege is genuinely required.
- Separate code, configuration, mutable state, secrets, logs, and runtime files by ownership and lifecycle.
- Design systemd service dependencies, restart policy, readiness, and sandboxing deliberately.
- Reject root execution, writable code, and credential exposure as convenience shortcuts.
- Verify unit syntax and the effective authority of a running process.

## Capstone increment

Give Atlas dedicated service identities, owned directories, restrictive modes, hardened systemd units, and unambiguous restart and shutdown policy.

## Identity is part of every resource decision

Linux access checks evaluate process credentials against object metadata and policy. A process has real, effective, saved, and filesystem user and group identities, supplementary groups, capabilities, and security-module context. Most host mistakes begin by compressing all of that into “root or not root.”

Atlas uses three long-running service users—`atlas-api`, `atlas-worker`, and `atlas-edge`—plus a bounded `atlas-backup` account. Shared authority is split by purpose: `atlas-spool` for API/worker queue transitions, `atlas-runtime` for heartbeat and port evidence, and `atlas-log` for the local event buffer. The edge never joins the spool group. None has a login shell or home directory. The teaching edge on 8443 requires no low-port capability; an optional drop-in demonstrates the narrower case without granting it by default.

The design question is not “which user makes the command work?” It is “which operations must this process perform, on which objects, and which authority is unnecessary?”

## Mode bits and umask form a default, not a complete policy

A file has owner, group, and other permission sets. Directory read permits listing names; execute permits traversal; write permits creating or removing directory entries subject to other rules. File write permission and directory write permission answer different questions. A process can remove a read-only file if it can modify the containing directory.

The umask clears permission bits at creation. Atlas units set `UMask=0027` or stricter so newly created state is not world-readable. A later `chmod` cannot retroactively prevent data that was already exposed, and a permissive parent directory can still undermine the intended boundary.

ACLs can express additional principals, but they increase the policy surface. Use them when the ownership model truly requires them, not to repair an unclear directory design.

## Separate paths by lifecycle and authority

Atlas uses a conventional split:

```text
/opt/atlas       immutable application release
/etc/atlas       configuration and secret references
/run/atlas       reboot-ephemeral runtime files
/var/lib/atlas   durable mutable state
/var/log/atlas   local operational evidence buffer
```

A service account should not write `/opt/atlas` or its own unit files. If a compromised service can replace the code that the supervisor starts next, restart converts data-plane compromise into persistent code execution. Configuration and secret files are owned by the deployment authority and readable only by the process that needs them.

Do not store a secret in an environment variable merely because systemd can set one. Environment variables can appear in process inspection, crash reports, child processes, and diagnostics. This course uses fixture keys only; later courses introduce managed secret delivery and rotation.

## Root is a bundle of authority

Traditional Unix grants UID 0 broad privilege. Linux capabilities split many kernel privileges into named units such as binding low ports, changing ownership, or administering network configuration. A capability is still powerful, often broader than its name suggests, and may be exploitable through a vulnerable process.

The Atlas edge unit demonstrates a bounded `CAP_NET_BIND_SERVICE` option, but its teaching configuration listens on 8443 and does not require it. Empty `CapabilityBoundingSet` and `AmbientCapabilities` are stronger defaults for API and worker.

`sudo` is an operator delegation tool. It is not a service supervision mechanism and should not appear inside service startup scripts.

## systemd owns unit lifecycle, not just process restart

A service unit describes ordering, dependencies, execution, environment, restart policy, shutdown, and sandbox controls. `After=` controls ordering; it does not imply a requirement. `Requires=` creates a stronger relationship but still does not mean the dependency is semantically ready. `Wants=` is weaker. `RequiresMountsFor=` derives mount dependencies for paths.

`Restart=on-failure` is not a substitute for fixing a crash loop. A restart policy needs delay, rate limiting, and an operator-visible failure state. Restarting a command that exits successfully after failing to initialize can create a false green state because the supervisor sees exit code zero.

The Atlas units use foreground processes, explicit `ExecStart`, bounded `TimeoutStopSec`, and no PID files as lifecycle authority. Course-generated JSON PID evidence exists only to make the local tour inspectable. A modern service manager already tracks the cgroup; self-daemonization discards useful ownership.

## Harden the execution environment deliberately

systemd sandbox options express host policy:

- `NoNewPrivileges=yes` prevents privilege gains through exec transitions;
- `ProtectSystem=strict` makes most system paths read-only;
- `ReadWritePaths=` names required mutable paths;
- `PrivateTmp=yes` provides a private temporary namespace;
- `ProtectHome=yes` hides or protects home directories;
- `RestrictSUIDSGID=yes` blocks creating set-ID files;
- `MemoryDenyWriteExecute=yes` narrows writable-executable mappings;
- `RestrictNamespaces=yes` denies new namespaces where not needed;
- `SystemCallArchitectures=native` rejects non-native syscall ABIs.

These options can break legitimate workloads. Apply them from a declared requirement and test the resulting service, not from a copied hardening score alone. A Python process that loads native extensions or JIT code may need different controls.

## Readiness and supervision

A process can be alive but unable to serve. systemd's default `Type=simple` considers the service started after the process is executed, not after the application proves readiness. `Type=notify` can establish a stronger startup handshake when the application calls `sd_notify`, but the notification still only proves what the application checked.

Atlas uses an HTTP readiness endpoint for routing and a process lifecycle for supervision. The readiness check verifies durable storage writability and a fresh worker heartbeat. It does not claim that every future request will succeed.

## Worked investigation: service writes fail after hardening

After adding `ProtectSystem=strict`, Atlas starts but job submission returns an error. The correct investigation is not to remove hardening wholesale.

1. Identify the failing path from logs or `strace`.
2. Classify the path as code, configuration, runtime, durable state, or log.
3. Decide whether the service should write it.
4. Add the narrowest `ReadWritePaths` entry or change ownership.
5. Rerun the operation and inspect effective unit properties.

If the failing path is `/opt/atlas/cache`, the better repair may be moving mutable cache data under `/var/cache/atlas`, not making `/opt/atlas` writable.

## Verifying effective authority

Static unit text is only an input. Verify:

```bash
systemd-analyze verify capstone/systemd/*.service
systemctl show atlas-api.service \
  -p User -p Group -p UMask -p NoNewPrivileges \
  -p CapabilityBoundingSet -p ReadWritePaths -p MemoryMax
namei -l /var/lib/atlas/spool
getfacl -p /var/lib/atlas 2>/dev/null || true
cat /proc/<pid>/status | grep -E '^(Uid|Gid|Groups|Cap|NoNewPrivs):'
```

The decisive evidence combines service-manager policy, filesystem path traversal, and running-process credentials.

## Atlas implementation bridge

Compare `sysusers.d/atlas.conf`, `tmpfiles.d/atlas.conf`, and the three service units. The files express different authorities: identity creation, path creation, and process execution. Verify that no service identity can write the application release or another service's private material.

Use `systemd-analyze verify` as syntax and dependency evidence. On a VM, install the units and inspect effective properties with `systemctl show`; a checked file is not yet an enforced runtime policy.

## Design review prompts

- Which exact path forces the shared `atlas` group?
- Can group write be removed by changing the queue ownership protocol?
- Does the edge truly require a capability on the selected port?
- What happens when initialization exits zero without readiness?
- Which sandbox directive could break a legitimate library and how would you prove it?

## Boundary case: supplementary groups and stale sessions

Adding a user to a group does not alter credentials of already running processes. A shell, service, or daemon must start a new session or restart to receive the new supplementary group set. This is why “I added the group but permission still fails” is not evidence of filesystem inconsistency.

Conversely, removing a user from a group does not revoke authority from existing processes. Revocation requires process termination or a mechanism with dynamic authorization. Account changes and service restart order belong in the change plan.

## Boundary case: path traversal and symlink ownership

A path can cross directories owned by different principals, mount points, and symlinks. Checking only the final file mode can miss a writable parent or symlink substitution. `namei -l` expands each component. Privileged code should use directory descriptors and no-follow operations where attackers can alter path components.

systemd's `ReadWritePaths` controls mount visibility for the unit but does not change Unix ownership. Both layers apply.

## Authority worksheet

For each service operation, record:

```text
operation:
required object/path/socket:
required read/write/execute or kernel capability:
identity performing it:
why another service must not possess it:
positive test:
negative test:
```

A least-privilege claim without a negative test is incomplete.

## Field method: design privilege as a transition graph

Least privilege is not a static list of mode bits. Authority changes during installation, startup, steady operation, maintenance, and recovery. Draw those phases explicitly. A privileged package or image installer may create users and immutable release files; the service manager changes to an unprivileged identity; the running process reads configuration and writes only declared state; an operator may later rotate a certificate or restore a backup. The same process should not silently accumulate the authority of every phase.

For Atlas, use a transition table:

| Phase | Actor | Required authority | Authority that must be absent |
|---|---|---|---|
| install | deployment authority | create users, release files, units | application secrets unrelated to Atlas |
| start | systemd | set identity, namespaces, limits | application business authority |
| serve | `atlas-api` | read config, write queue request | write code, TLS key, unit, firewall |
| process | `atlas-worker` | claim queue item, publish result | bind public listener, read edge key |
| expose | `atlas-edge` | read leaf key, connect to loopback API | write durable job state |
| recover | named operator/runbook | bounded restore or rollback | indefinite root shell without audit |

Stable service users are appropriate when durable files need stable ownership. `DynamicUser=yes` can be excellent for services with manager-owned state directories, but blindly enabling it can make persistent ownership and offline repair confusing. The course uses explicit fixture users so path ownership remains inspectable; the chapter still requires you to compare dynamic and stable identity choices.

Revocation is also a lifecycle operation. Removing group membership does not change credentials already held by a running process. Rotating a file mode does not revoke an already-open descriptor. Removing a capability from a unit does not change the current process until restart. A correct change plan identifies which processes must stop, which descriptors must close, and which cached authorization state must expire.

Finally, distinguish hardening from correctness. A high `systemd-analyze security` score can coexist with writable secrets or a false readiness check. Every hardening directive must map to a requirement, a negative test, and a rollback path. The goal is not to maximize directives; it is to minimize authority while preserving the service's declared work.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| Directory write and traversal permissions are distinct from file write permission. | POSIX access model | `namei -l`, controlled access test |
| Linux capabilities narrow some root privileges but do not make a process harmless. | Linux mechanism | `/proc/<pid>/status` and unit capability properties |
| systemd unit ordering and requirement dependencies are separate concepts. | systemd model | `systemd-analyze verify`, effective unit properties |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Writable release directory

A service that can rewrite its executable or unit content can persist a compromise across restart.

### Broad capability inheritance

Ambient or bounding capabilities copied from a generic hardening guide can grant authority the process never required.

### Restart loop as availability

Repeated restart of a deterministic initialization failure creates churn, not availability.


## Module synthesis

Return to the central question: **Which authority should each process possess, and who is responsible for keeping it running?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**The API runs as root and its executable directory is writable by the service account, allowing configuration compromise to become code execution.**—fails for the predicted reason.

## Continue

Module 03 constrains how much CPU and memory those identities may consume.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
