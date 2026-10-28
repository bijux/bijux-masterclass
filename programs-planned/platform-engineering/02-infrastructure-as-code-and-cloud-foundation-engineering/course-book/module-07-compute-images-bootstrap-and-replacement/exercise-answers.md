# Worked Answers — Compute, Images, Bootstrap, and Replacement

## 1. Classify the artifacts

- **Systemd unit:** image content or a versioned configuration package installed by the image pipeline. It should not be improvised by an operator after boot.
- **Subnet ID:** launch definition/environment composition. It determines placement, not filesystem content.
- **Database password:** secret source consumed at runtime. It belongs neither in the image nor in user data.
- **Atlas binary:** image content or a digest-pinned release artifact installed by the image pipeline.
- **Completed result:** durable workload state. Replacement must preserve or restore it independently of the root disk.
- **Log destination:** runtime/environment configuration, unless the organization bakes a stable collector endpoint into the image.

The important distinction is ownership and change cadence, not the file extension used to express the value.

## 2. Backup versus replaceability

A nightly root-volume backup may restore files, but it does not define a reproducible image, launch authority, health gate, or bounded recovery procedure. It may also restore accumulated drift and old credentials. A replaceable design can create a clean machine from governed artifacts and attach or restore only the state that is meant to persist.

## 3. Deterministic bootstrap

Idempotence means repeated execution converges. Determinism additionally requires the same declared inputs to produce the same relevant result. Downloads need immutable versions and digest checks; package repositories and clocks need bounded behavior; failure must stop the bootstrap instead of silently continuing. A script that fetches `latest` may be idempotent today and different tomorrow.

## 4. Secrets in user data

User data can be copied into OpenTofu state, exposed through cloud APIs or instance metadata, printed in cloud-init logs, retained in support evidence, and readable by broader roles than the intended process. Rotation also becomes tied to instance replacement. A secret service with a workload identity gives narrower retrieval and a separate lifecycle.

## 5. IMDSv2 and role authority

IMDSv2 constrains how metadata is requested and reduces some request-forgery and hop-based attacks. The instance profile chooses which IAM role the instance receives. The role policy defines what stolen or legitimate credentials can do. Strong metadata transport cannot compensate for an administrator-equivalent role.

## 6. Desired capacity one

A controller can recreate a missing instance, but there is still no simultaneous healthy target during startup or failure. A zonal data volume, application startup time, exhausted quota, or failed bootstrap can extend the interruption. The design improves reconciliation, not necessarily availability.

## 7. Health layers

Instance status is provider-level compute evidence. Liveness shows that a process can continue running. Readiness shows that it can serve the intended workload now. Load-balancer health is the edge’s routing decision based on one configured request. Each has a different owner and consequence; collapsing them makes replacement and traffic behavior unpredictable.

## 8. Limits of `create_before_destroy`

It may be impossible to allocate a second instance because of quota, to attach a single-attach volume to both hosts, or to create a second resource with a globally unique name. The application may also reject concurrent writers. Lifecycle ordering cannot eliminate architectural constraints.

## 9. Image release identity

Record the source revision, base image, package-lock or package inventory, builder identity, build time, tests, vulnerability disposition, architecture, image ID, and immutable artifact digest where available. The ID alone does not explain how the image was produced or whether it is trusted.

## 10. Emergency in-place patch

It may be defensible when exploitation is active and the image pipeline cannot meet the containment deadline. The action needs an owner, exact commands, affected hosts, evidence, risk approval, and an expiry. A rebuilt image and machine replacement must restore convergence afterward.

## 11. Architecture

An ARM instance cannot run an x86-only kernel or binary. Agents and package sources may also differ. Encoding architecture in image and launch contracts prevents an apparently valid instance-type change from becoming a boot or execution failure.

## 12. Replacement evidence

Retain the old and new image/launch versions, plan and apply digests, quota preflight, bootstrap result, data-volume identity, readiness results, traffic shift, result checksum, old-host termination, and cleanup. State explicitly that a singleton host still permits an interruption and that the exercise does not prove cross-zone service continuity.
