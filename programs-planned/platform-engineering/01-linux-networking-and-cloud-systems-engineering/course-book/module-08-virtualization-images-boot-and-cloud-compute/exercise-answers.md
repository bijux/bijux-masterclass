# Worked Answers — Module 08: Virtualization, Images, Boot, and Cloud Compute

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — VM versus container

A VM runs a guest kernel against virtual hardware presented by a hypervisor. A containerized process normally shares the host kernel while using namespaces, cgroups, mounts, and other controls. This affects isolation, boot, device model, patching, and evidence. Course 3 studies containers after this distinction is established.

## Exercise 2 — Boot stage

Inspect serial or console output for firmware/bootloader/kernel, `journalctl -b` or recovery logs for userspace and systemd, and network/cloud-init status for interface and configuration. Provider power state proves none of these. A failed root mount differs from a failed Atlas unit.

## Exercise 3 — Image content

OS packages and repeatable baseline hardening can belong in the image. Instance private keys and durable spool state must not. The image should be reusable and non-secret; instance identity and mutable data are delivered through controlled runtime mechanisms. Record the image digest and source build.

## Exercise 4 — cloud-init idempotence

Cloud-init or boot scripts can be interrupted after partial changes. Re-running non-idempotent commands can duplicate users, corrupt configuration, or rotate credentials unexpectedly. Design idempotent operations or write durable completion markers with version and validation. Fail visibly when a partial state cannot be reconciled.

## Exercise 5 — User-data secret

User data can be accessible to local processes through metadata, visible through provider APIs or logs, retained in launch templates, and copied during support. Network privacy does not protect those paths. Use workload identity and a managed secret channel with scope and rotation.

## Exercise 6 — Identity source

It may be user-configurable, reused, changed during replacement, resolved through mutable DNS, or duplicated. Use provider-issued workload identity or cryptographic credentials tied to an IAM principal. Hostname remains useful for display or routing, not proof of authority.

## Exercise 7 — Disk lifecycle

Test provider stop/start, instance termination, replacement, zone failure, and deletion policy. Determine whether the disk is detached, deleted, or inaccessible in another zone. Backups and restore are separate. Reboot survival is only one failure boundary.

## Exercise 8 — Ephemeral disk use

Use it for reconstructible caches, staging files whose source remains durable, or temporary processing with recovery. Do not place the only queue or result copy there. The application must tolerate loss at stop, maintenance, or replacement and clean stale data.

## Exercise 9 — Maintenance event

As a bounded signal that may enable draining or checkpointing, not a guaranteed prevention of interruption. Validate the provider mechanism, deadline, and supported VM behavior. Continue to design crash recovery because notices can be absent or too short.

## Exercise 10 — Immutable replacement

Durable application state, secret references, workload identity, DNS/load-balancer registration, configuration source, release manifest, and backup evidence must be independently reconstructible. The new instance should derive them from managed resources, not copy mutable files from the old root disk.

## Exercise 11 — Image drift

Replacement instances start from the old image and lose the patch. The fleet now has unrecorded divergence. Emergency repair may be justified, but it should trigger a new image/release and reconciliation. Record package/version evidence and replacement plan.

## Exercise 12 — Replacement oracle

A new provider instance identity and boot sequence, recreation from the declared image/configuration, restored or reattached durable state, endpoint registration, successful verified request, and termination of the old instance. A new PID or reboot timestamp proves only a process or guest restart.
