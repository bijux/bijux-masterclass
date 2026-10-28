# Module 02 — Identity, Permissions, Capabilities, and Service Supervision

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.
> **Central question:** Which authority should each process possess, and who is responsible for keeping it running?

---

## Where This Module Fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger security boundary.

The capstone increment for this module is:

> **Give Atlas dedicated service identities, owned directories, restrictive modes, hardened systemd units, and unambiguous restart and shutdown policy.**

This result is required before the next module can build on it honestly.

---

## Learning Outcomes

By the end of this module, you will be able to:

* Reason about users, groups, mode bits, umask, ACLs (Access Control Lists), set-user-ID, and effective identity.
* Use Linux capabilities only when a narrow kernel privilege is genuinely required.
* Separate code, configuration, mutable state, secrets, logs, and runtime files by ownership and lifecycle.
* Design systemd service dependencies, restart policies, readiness checks, and sandboxing deliberately.
* Reject root execution, writable code, and credential exposure as convenience shortcuts.
* Verify unit syntax and the effective authority of a running process.

---

## 1. Identity is Part of Every Resource Decision

> **Concept Refresher: Linux Identities**
> In Linux, every process and file is associated with a specific User ID (UID) and Group ID (GID). Access checks evaluate the process's credentials against the file's metadata to determine if an action (read, write, execute) is allowed.

Most server mistakes begin by compressing all security into a simple question: *"Is this running as root or not root?"* This is dangerous.

Atlas uses dedicated, long-running service users to separate authority by purpose:

* `atlas-api`
* `atlas-worker`
* `atlas-edge`
* `atlas-backup` (a bounded account)

Shared authority is also split by purpose using groups:

* `atlas-spool`: For API/worker queue transitions.
* `atlas-runtime`: For heartbeat and port evidence.
* `atlas-log`: For the local event buffer.

None of these accounts have a login shell or a home directory. The design question is never *"which user makes the command work?"* but rather *"which operations must this process perform, on which objects, and which authority is completely unnecessary?"*

---

## 2. Mode Bits and Umask Form a Default Policy

> **Concept Refresher: Permissions and Umask**
> * **Permissions (Mode Bits):** Files and directories have rules for the Owner, the Group, and Others. *Read* lets you view contents, *Write* lets you modify them, and *Execute* lets you run a file (or enter a directory).
> * **Umask:** A default filter applied when a file or directory is created, stripping away certain permissions automatically.
> 
> 

File write permission and directory write permission answer different questions. A process can actually delete a read-only file if it has write permissions to the *directory* containing that file.

The umask clears permission bits at creation. Atlas systemd units set `UMask=0027` (or stricter) so newly created state files are never world-readable. A permissive parent directory can still undermine your intended boundary, so directory design is critical.

---

## 3. Separate Paths by Lifecycle and Authority

> **Concept Refresher: The Linux File Hierarchy**
> Linux standardizes where certain types of files should live based on their purpose and how often they change.

Atlas uses a conventional, secure split:

| Path | Purpose | Lifecycle |
| --- | --- | --- |
| `/opt/atlas` | Application release | Immutable (Read-only for the service) |
| `/etc/atlas` | Configuration and secrets | Owned by deployment authority, read-only for process |
| `/run/atlas` | Runtime files (PIDs, sockets) | Ephemeral (cleared on reboot) |
| `/var/lib/atlas` | Durable mutable state | Writable by the service, persists across reboots |
| `/var/log/atlas` | Local event buffers | Writable by the service, strictly for logs |

**Crucial Rule:** A service account should *never* be able to write to `/opt/atlas` or its own systemd unit files. If a compromised service can replace its own code, restarting the service converts a temporary breach into persistent code execution.

---

## 4. Root is a Bundle of Authority

> **Concept Refresher: Linux Capabilities**
> Traditionally, the `root` user (UID 0) can do anything. Linux Capabilities break the "root privilege" down into smaller, distinct powers. For example, `CAP_NET_BIND_SERVICE` allows a program to listen on lower-numbered ports (like 80 or 443) without needing full root access.

Capabilities are still powerful and can be exploited. Empty `CapabilityBoundingSet` and `AmbientCapabilities` are strong defaults for the Atlas API and worker. `sudo` is an operator delegation tool; it is not a service supervision mechanism and should never appear inside startup scripts.

---

## 5. systemd Owns Unit Lifecycle

> **Concept Refresher: systemd Dependencies**
> systemd manages services using unit files.
> * `After=`: Ensures Service A starts only after Service B has attempted to start (determines order, not necessity).
> * `Requires=`: Service A will fail if Service B fails to start.
> * `Wants=`: Service A prefers Service B to be running, but will start anyway if B fails.
> 
> 

`Restart=on-failure` is not a substitute for fixing a crash loop. A valid restart policy needs a delay, rate limiting, and an operator-visible failure state.

Atlas units use foreground processes, explicit `ExecStart` commands, bounded timeouts, and no PID files. Modern service managers track processes via `cgroups` (control groups), making self-daemonizing applications obsolete and difficult to track.

---

## 6. Harden the Execution Environment

systemd offers powerful sandbox options to lock down services:

* `NoNewPrivileges=yes`: Prevents privilege gains through exec transitions.
* `ProtectSystem=strict`: Makes most system paths read-only.
* `ReadWritePaths=`: Explicitly names the specific paths the service *is* allowed to write to.
* `PrivateTmp=yes`: Provides an isolated temporary namespace.
* `ProtectHome=yes`: Hides or protects user home directories.

Apply these options based on declared requirements and test them. Applying a hardening guide blindly can break legitimate workloads (e.g., Python processes loading native extensions).

---

## 7. Readiness and Supervision

A process can be "alive" but unable to serve traffic.

* `Type=simple` (systemd's default) considers a service started the moment the process executes.
* `Type=notify` establishes a stronger handshake, waiting until the application explicitly signals it is ready.

Atlas uses an HTTP readiness endpoint for routing decisions and the process lifecycle for basic supervision.

---

## 8. Worked Investigation: Service Writes Fail After Hardening

Suppose you add `ProtectSystem=strict` and Atlas starts failing to submit jobs. **Do not just remove the hardening directive.**

1. Identify the failing path using logs or `strace`.
2. Classify the path (is it code, config, runtime, or durable state?).
3. Decide if the service *should* legitimately write to it.
4. Add the narrowest possible `ReadWritePaths` entry in systemd, or fix the directory ownership.
5. Rerun the operation and inspect.

*Example:* If the failing path is `/opt/atlas/cache`, the correct fix is to move the cache to `/var/cache/atlas`, not to make `/opt` writable.

---

## 9. Verifying Effective Authority

Static text files are just inputs. You must verify what the system actually enforces. Use these commands:

```bash
# Verify unit syntax
systemd-analyze verify capstone/systemd/*.service

# Check effective unit properties
systemctl show atlas-api.service -p User -p Group -p UMask -p NoNewPrivileges

# Check directory traversal permissions
namei -l /var/lib/atlas/spool

# View process credentials directly from the kernel
cat /proc/<pid>/status | grep -E '^(Uid|Gid|Groups|Cap|NoNewPrivs):'

```

---

## 10. Authority Worksheet

For each service operation, you should be able to clearly document the following:

```text
Operation:
Required object/path/socket:
Required read/write/execute or kernel capability:
Identity performing it:
Why another service must not possess it:
Positive test (Prove it works):
Negative test (Prove unauthorized access fails):

```

A "least-privilege" claim without a negative test is incomplete.

---

## 11. Failure Patterns to Recognize

* **Writable Release Directory:** A service that can rewrite its own executable code can persist a compromise across reboots.
* **Broad Capability Inheritance:** Copying capabilities from generic guides can grant unnecessary authority to your process.
* **Restart Loop as Availability:** Repeatedly restarting a service that is failing deterministically creates useless system churn, not high availability.

---

## Module Synthesis

Return to the central question: **Which authority should each process possess, and who is responsible for keeping it running?**

A complete answer names the owner of the state, the transition that changes it, the failure boundary, and the observation that proves it. The capstone is ready to progress only when your new mechanisms work, and the planted defect—*The API runs as root and its executable directory is writable, allowing configuration compromise to become code execution*—fails for the exact reason you predicted.

### Module Route

1. Complete the exercises before viewing solutions.
2. Compare with the worked answers.
3. Run the controlled lab.
4. Retain the checkpoint evidence.
