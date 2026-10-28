# OCI runtime configuration map

An OCI runtime bundle contains a root filesystem and a `config.json` execution request. Treat every major field as an authority decision.

## Process

Review:

- `args`: exact executable and arguments; avoid an accidental shell unless required;
- `env`: configuration and credential exposure; environment is visible to the process and often diagnostics;
- `cwd`: must exist in the rootfs;
- `user`: UID, GID, supplemental groups, umask implications;
- `capabilities`: bounding, permitted, effective, inheritable, ambient;
- `noNewPrivileges`: whether exec may gain authority;
- resource limits and terminal behavior.

Image defaults can initialize these fields, but the runtime request is the effective source.

## Root and mounts

`root.path` identifies the prepared rootfs. `root.readonly` protects it only if mount configuration does not reintroduce writable host authority. Review each mount for:

- source ownership;
- destination;
- read/write mode;
- recursive and propagation behavior;
- symlink resolution;
- device and executable permissions;
- expected lifetime.

Atlas requires durable writes only under `/var/lib/atlas`, temporary writes under `/tmp` and `/run/atlas`, configuration under `/etc/atlas`, and a read-only image root.

## Namespaces

A runtime profile may request PID, mount, network, IPC, UTS, cgroup, user, and time namespaces. Presence alone is not sufficient. User namespaces need explicit UID/GID mappings; network namespaces need interfaces/routes; mount namespaces need safe propagation and rootfs assembly.

## Linux resources and devices

Cgroup limits govern resource use, not application capacity. Review CPU quota/weight, memory high/max, PID maximum, and I/O controls. Device rules should begin closed and add only required devices. A resource value inherited from Course 2 is a hypothesis until representative measurement supports it.

## Seccomp, hooks, and LSMs

A seccomp profile governs syscall attempts but does not replace capability, device, filesystem, network, or LSM policy. Hooks can run at lifecycle boundaries with authority outside the workload; every hook needs an owner, idempotency behavior, timeout, failure semantics, and audit trail.

## Lifecycle review

A correct runtime implementation proves:

```text
create → created state
start  → running state
kill   → signal delivery to workload process
wait   → exit status
 delete → resources absent
```

Cleanup is part of correctness. Leftover mounts, namespaces, cgroups, state files, or processes are failed lifecycle evidence even when the application exited successfully.
