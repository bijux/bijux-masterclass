# Capstone — Atlas Host Runtime 1.0

Atlas is a small workload chosen to expose platform responsibilities rather than distract with application complexity. An HTTPS client submits text-processing jobs. The API validates and durably accepts each job. A worker claims work and publishes a deterministic result. The edge terminates TLS and establishes the trusted proxy boundary.

## Logical architecture

```text
client
  |
  | verified TLS, HTTP authority atlas.test
  v
Atlas edge process
  |
  | loopback HTTP, controlled forwarded identity
  v
Atlas API process
  |
  | atomic directory transitions
  v
file spool <---- Atlas worker process
  |
  +---- results and failure records
```

The bundled edge is a dependency-light semantic implementation. A maintained Nginx configuration demonstrates an operational proxy shape. The course does not claim that the standard-library HTTP server is a general production server or that a filesystem queue replaces a durable database or broker. Those deliberate limits make process, file, socket, retry, and recovery transitions observable.

## State model

Atlas separates paths by lifecycle:

```text
/opt/atlas       immutable release
/etc/atlas       configuration and TLS references
/run/atlas       reboot-ephemeral PID, port, and heartbeat evidence
/var/lib/atlas   durable queue and result state
/var/log/atlas   bounded local operational evidence
```

The course-local tour uses temporary equivalents of these paths so it can run without privilege. systemd, sysusers, tmpfiles, Nginx, nftables, and cloud-init fixtures show how the same responsibilities map onto a real host.

The file spool has four states:

```text
queued → processing → results
                  ↘ failed
```

Directory transitions are atomic only within one filesystem. Result publication synchronizes file content and the parent directory. Recovery handles expired processing records and must reconcile an already-published result before requeueing. This is an educational model of durable state transitions, not an exactly-once claim.

## Process ownership

- `atlas-edge` owns the public listener, TLS leaf key, Host policy, and forwarding-header rewrite.
- `atlas-api` owns request parsing, body bounds, health responses, and job acceptance.
- `atlas-worker` owns one claimed job and graceful completion of the current unit of work.
- systemd owns process start, stop, restart, resource limits, and sandbox policy on a managed host.
- the deployment authority owns release files, unit files, firewall policy, configuration, and certificate rotation.

No service account writes its executable release or another service's private material.

## Module evolution

| Module | Atlas change |
|---:|---|
| 1 | explicit processes, descriptors, signals, and exit evidence |
| 2 | service identities, filesystem authority, systemd supervision |
| 3 | cgroup resource envelope and bounded failure |
| 4 | atomic publication, storage classes, backup and restore |
| 5 | listener, route, transport, timeout, and dual-stack policy |
| 6 | local PKI, verified HTTPS, DNS/authority model |
| 7 | firewall, trusted proxy, safe retries, and draining |
| 8 | image, boot, VM replacement, and metadata policy |
| 9 | cloud capability mapping and failure-domain requirements |
| 10 | release, game day, recovery, and Course 2 handoff |

## Proof routes

`make capstone-tour` starts the three processes on loopback with ephemeral ports, performs a verified TLS request, submits a job, checks the durable result, verifies forwarding-header replacement, terminates the worker gracefully, and cleans all processes.

`make systemd-proof` checks unit syntax when systemd tooling is available. `make linux-proof` captures real process, cgroup, mount, and socket evidence. Guarded scripts provide disposable namespace and resource-control labs. Module 8 and 9 define optional VM and cloud evidence; the release report never marks those as passing merely because configuration files exist.

## Final defense

The final defense traces one normal request and three failure paths: worker termination, storage writability loss, and TLS or name failure. The learner must identify the first oracle, repair without weakening another boundary, rerun focused proof, restore clean state, and justify every Course 2 requirement.

The capstone succeeds when it teaches a precise operational model and produces reproducible evidence. It does not succeed by accumulating more components.

## Supporting operational documents

- [Architecture](reference/atlas-architecture.md)
- [Evidence map](reference/atlas-evidence-map.md)
- [Service failure runbook](reference/runbook-service-failure.md)
- [Storage failure runbook](reference/runbook-storage-failure.md)
- [Certificate failure runbook](reference/runbook-certificate-failure.md)
- [Instance replacement runbook](reference/runbook-instance-replacement.md)
