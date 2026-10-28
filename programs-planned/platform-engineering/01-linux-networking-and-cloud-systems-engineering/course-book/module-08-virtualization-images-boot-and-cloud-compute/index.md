# Module 08 — Virtualization, Images, Boot, and Cloud Compute

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** What changes—and what does not—when the Linux host becomes a virtual machine created from an image?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Define the Atlas machine image, boot sequence, cloud-init inputs, ephemeral-disk policy, metadata access, maintenance behavior, and replacement strategy.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Distinguish hardware virtualization, emulation, paravirtual devices, and process isolation.
- Trace firmware, bootloader, kernel, initramfs, system manager, and service startup.
- Separate immutable image content from instance configuration and mutable application data.
- Use cloud-init and instance metadata without placing long-lived secrets in user data.
- Treat instances as replaceable while preserving state according to explicit durability boundaries.
- Model host maintenance, stop/start, reboot, termination, and image replacement as distinct events.

## Capstone increment

Define the Atlas machine image, boot sequence, cloud-init inputs, ephemeral-disk policy, metadata access, maintenance behavior, and replacement strategy.

## A virtual machine emulates a machine boundary, not a process boundary

A hypervisor presents virtual CPUs, memory, interrupt controllers, storage, network devices, firmware, and other machine interfaces to a guest. Hardware-assisted virtualization lets much guest code execute directly while trapping privileged operations. Emulation can reproduce a different architecture at greater cost. Paravirtual devices use guest-aware interfaces for efficient I/O.

The guest still boots a kernel and runs an operating system. That is materially different from a container, which shares the host kernel.

## Trace the boot chain

A simplified Linux VM boot path is:

```text
virtual firmware
→ bootloader
→ kernel and initramfs
→ root filesystem
→ PID 1 / systemd
→ local filesystems and network
→ Atlas units
```

Each stage owns different failure evidence. A cloud console screenshot showing “running” proves that the provider believes the VM is powered, not that the kernel booted, the filesystem mounted, the network configured, or Atlas became ready.

Use serial console, boot logs, `journalctl -b`, `systemd-analyze critical-chain`, and cloud instance status separately.

## Images define initial state

A machine image commonly contains the OS, packages, baseline configuration, and perhaps application release. An image should not contain instance-specific identity, long-lived credentials, stale machine IDs, or mutable application data.

Two strategies are common:

- **baked image:** application and dependencies are included; boot does little work and releases are image replacements;
- **base image plus boot configuration:** a generic image installs or fetches more at launch; boot is slower and depends on external availability.

Atlas chooses a small base image plus a separately versioned application release for Course 1. Course 2 will make the choice reproducible.

## cloud-init is initialization, not a secret manager

cloud-init consumes datasource metadata and user data to configure a new instance. It can create users, install packages, write files, and run commands. User data may be retrievable from the instance metadata service and visible through provider APIs or logs. Do not place long-lived secrets in it.

The course fixture contains a placeholder public SSH key and a statement that application configuration arrives separately. It does not embed a private key, database password, or cloud access key.

Initialization scripts should be idempotent or explicitly one-shot. A partially failed boot must leave diagnosable state rather than silently continuing.

## Instance identity is not hostname

Hostnames, private addresses, and public addresses can change during replacement or stop/start depending on provider configuration. A workload identity should come from a managed identity mechanism with bounded credentials, not from a string chosen by DNS or the instance itself.

Machine identity for inventory may include a provider instance ID and image digest. Application identity and authorization remain separate.

## Root, ephemeral, and persistent disks differ

A root disk may persist across reboot but be deleted at instance termination. An instance-store or local SSD can disappear on stop, maintenance, or replacement. A persistent block disk can survive instance replacement but remains tied to a region or zone and has attachment constraints. Object storage provides a different API and consistency model.

The Atlas storage plan names the required survival boundary instead of assuming `/var/lib` tells the cloud what to preserve.

## Stop, reboot, terminate, and replace are distinct

- **process restart** preserves the host kernel and disks;
- **guest reboot** restarts the OS and clears `/run`;
- **provider stop/start** may move the VM and change ephemeral resources;
- **termination** destroys the instance resource and possibly attached storage according to policy;
- **replacement** creates a new instance from image and configuration;
- **host maintenance** may live-migrate, reboot, stop, or notify depending on provider and VM type.

A runbook must name the event it handles. “Restart the server” is ambiguous.

## Metadata services are privileged local APIs

Cloud providers expose metadata on a link-local or special local endpoint. Metadata can include instance identity, network attributes, maintenance notices, user data, and short-lived workload credentials. Any process able to reach the endpoint may be able to request sensitive material within the instance's identity.

Course profiles require:

- AWS IMDSv2 session-oriented access;
- GCP's required metadata flavor header;
- Azure's required metadata header;
- no arbitrary user-controlled proxying to metadata;
- no long-lived secrets in user data;
- least-privilege workload identity.

The dependency-light metadata module validates only endpoint policy. A real cloud proof must exercise the provider service.

## Worked investigation: new instance is healthy but has no jobs

A replacement VM boots, systemd reports Atlas active, and HTTPS readiness is green. Existing jobs are missing. Investigation shows `/var/lib/atlas` was on the deleted root disk.

The software worked exactly as configured; the architecture made a false durability assumption. Repair requires moving state to a resource with the required replacement boundary or restoring from backup. Changing readiness after the loss cannot recover data.

The outgoing handoff therefore requires durable state independent of the root image and a tested restore route.

## Immutable replacement and mutable repair

Immutable replacement reduces drift by creating a new image or release and replacing instances. It does not remove the need for emergency access, patching, data migration, certificate rotation, or forensic preservation. A platform must define when in-place repair is permitted and how replacement returns the fleet to a known state.

Atlas final defense includes both a controlled service restart and a machine-replacement design. The latter remains environment-backed until exercised in a VM or cloud.

## Atlas implementation bridge

Review the cloud-init fixture and host profile. The image contains no instance credential or durable Atlas state. Initialization creates only baseline packages and an operator placeholder; application release remains separately controlled.

On a VM, record boot stages, reboot behavior, `/run` loss, root-disk persistence, and service ordering. A cloud provider proof additionally records instance ID, image ID, metadata policy, maintenance model, and deletion behavior.

## Design review prompts

- Which bytes belong in the image?
- Which configuration is instance-specific?
- Which state survives termination?
- Which metadata can any local process request?
- How does a failed boot become observable and recoverable?

## Boundary case: image freshness versus reproducibility

An image rebuilt from unpinned package repositories may be fresh but not reproducible. An old pinned image may be reproducible but vulnerable. A mature pipeline records source repositories, package versions, build time, security status, and replacement policy. Course 3 expands this into OCI provenance; Course 2 first makes VM creation reproducible.

## Boundary case: initialization dependency failure

If boot depends on an external package repository, secret service, or artifact registry, a transient outage can leave a half-configured instance. Decide whether boot should fail and be replaced, retry with a bound, or start in a diagnostic state. Never report readiness merely because cloud-init exited.

## VM lifecycle worksheet

```text
image identity and source:
boot configuration source:
instance identity:
workload identity:
root-disk lifecycle:
ephemeral-disk use:
durable-state attachment/restore:
maintenance signal:
replacement trigger:
old-instance decommission proof:
```

The worksheet becomes part of the Course 2 compute module interface.

## Field method: make replacement an engineered operation

A virtual machine is not merely a remote Linux host. Its boot depends on an image, firmware and virtual hardware, block-device mapping, network attachment, instance identity, metadata service, initialization data, and provider control plane. A reproducible replacement requires each dependency to be named.

Classify machine state before designing the image:

```text
image-owned: operating system and immutable Atlas release
boot-supplied: environment-specific configuration and identity references
ephemeral: /run, temporary files, caches safe to lose
durable: queue/results or a documented restore source
evidence: logs and audit records with a retention destination
external: DNS, load balancer, KMS, database, object storage
```

Do not bake long-lived credentials or environment-specific secrets into an image. Do not make boot depend on an unbounded package update from the public internet. Prefer a tested image plus bounded initialization. Record the exact image identity, package provenance, initialization version, and final readiness evidence.

Reboot, stop/start, host migration, termination, and replacement are different events. A reboot usually preserves the instance and root disk; stop/start may change placement or public address; termination can delete ephemeral and root storage according to policy; replacement creates a new identity and must reacquire network, workload identity, configuration, and durable state. Test the failure you claim to survive.

Cloud-init completion is not application readiness. Initialization may succeed while a mount is absent, a certificate name is wrong, or the worker cannot write durable state. The service's readiness oracle remains application-specific.

Images also age. Rebuilding from an unpinned repository is not reproducible; never rebuilding produces known-vulnerable artifacts. A mature image lifecycle separates source definition, resolved package set, build evidence, security review, promotion, deprecation, and replacement. Course 2 encodes the compute resources; Course 3 later turns workload packaging into OCI artifacts.

The module's final evidence is a replacement dossier, not a screenshot of a running VM: old and new instance identities, image identity, boot transcript, mount identity, restored-state hash, verified HTTPS exchange, and deletion of obsolete resources.


## Decision record: rebuild, repair, or replace

A machine incident presents three choices. Repair in place when the state is understood, the change is bounded, and replacement would create more risk. Rebuild the immutable release when code or package identity is uncertain but the machine and durable storage remain trusted. Replace the instance when host integrity, boot state, or configuration convergence is doubtful. The decision must consider recovery time, evidence preservation, state attachment, identity rotation, and rollback. “Pets versus cattle” is too crude: some machines hold recoverable state, and some supposedly replaceable machines depend on undocumented manual changes. Atlas treats replacement as a tested workflow, not a slogan.

A replacement is complete only after the old authority is removed. Detach obsolete identities, revoke temporary access, remove stale DNS or load-balancer membership, apply deletion policy to disks and snapshots, and verify inventory. Running the new instance while leaving the old one reachable is duplication, not recovery.

## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| A VM has a guest kernel and machine boot chain; a container shares the host kernel. | virtualization model | boot and process evidence |
| Long-lived secrets are forbidden in cloud-init user data. | Atlas security profile | configuration scan and provider metadata review |
| Instance replacement must not depend on mutable root-image state. | Atlas host profile | replacement or restore exercise |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Secret user data

Boot metadata and user-data channels are not durable secret stores and may be visible to host processes or provider APIs.

### Hostname identity

A hostname can change or be chosen by configuration; it is not a sufficient workload credential.

### Root-disk durability

A path surviving reboot does not prove it survives instance termination or replacement.


## Module synthesis

Return to the central question: **What changes—and what does not—when the Linux host becomes a virtual machine created from an image?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**A startup script writes a long-lived cloud credential from user data into a world-readable file and assumes the instance hostname is permanent identity.**—fails for the predicted reason.

## Continue

Module 09 maps the VM to cloud identity, network, storage, and failure-domain primitives.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
