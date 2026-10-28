# Module 10 — Production Host Engineering and Final Defense

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** Can the host be installed, started, observed, upgraded, degraded, recovered, and replaced without making a claim stronger than the evidence?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Release Atlas Host Runtime 1.0, run a bounded failure game day, verify recovery, and export an exact Course 2 cloud-foundation requirements package.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Integrate service identity, resources, storage, network, TLS, firewall, supervision, logging, backup, and recovery into one host release.
- Distinguish liveness, readiness, diagnostics, and business correctness.
- Design patching, configuration change, rollback, certificate rotation, and machine replacement procedures.
- Use structured evidence and runbooks during a multi-fault exercise.
- Classify local, Linux-privileged, VM, and real-cloud evidence honestly.
- Defend every outgoing infrastructure requirement and its failure assumption.

## Capstone increment

Release Atlas Host Runtime 1.0, run a bounded failure game day, verify recovery, and export an exact Course 2 cloud-foundation requirements package.

## Production readiness is an integrated property

A host is not ready because each configuration file looks plausible in isolation. Process lifecycle, identity, resources, storage, network, trust, supervision, recovery, and change procedures interact. A writable state path can be mounted after the service starts; a certificate can be valid while the backend is unreachable; a supervisor can restart a process that deterministically corrupts state.

The final module integrates the Atlas Host Runtime and tests cross-boundary failure.

## Define the release unit

Atlas Host Runtime 1.0 consists of:

- application code and exact version;
- Python interpreter and required OS packages;
- service users and groups;
- directory and permission policy;
- systemd units and resource controls;
- edge, TLS, and firewall configuration;
- host profile and provider-neutral requirements;
- backup and restore procedure;
- tests, manifests, and evidence record.

A configuration edited directly on one host is drift unless it is captured in the release authority. Course 2 will encode more of this desired state.

## Liveness, readiness, diagnostics, and correctness

Atlas exposes:

- **liveness:** the API process can handle the liveness route;
- **readiness:** durable spool is currently writable and worker heartbeat is fresh;
- **diagnostics:** structured events and host evidence;
- **business correctness:** job state and result bytes.

Readiness does not prove a submitted job will complete. It proves the selected routing prerequisites at one time. The final game day includes a read-only or unavailable durable path and verifies that readiness changes before mutating traffic continues.

## Change and rollback are state transitions

For each change define:

1. preconditions and backup;
2. exact release identity;
3. order of configuration, code, and data changes;
4. health and correctness checks;
5. rollback boundary;
6. evidence retention;
7. cleanup and decommission.

A rollback can be unsafe after an irreversible data-format change. Course 1 avoids schema migration, but certificate rotation, unit hardening, and storage relocation still have ordering constraints.

## Patching and machine replacement

Operating-system patching may require service restart or host reboot. A mature plan distinguishes:

- routine package update;
- urgent security patch;
- kernel update requiring reboot;
- immutable image replacement;
- failed boot rollback;
- evidence preservation during suspected compromise.

For a single host, maintenance creates downtime unless another instance or routing path exists. The design must state that rather than hiding it behind a cloud label.

## Structured logs are evidence, not the source of truth

Atlas emits JSON lines with event name, timestamp, PID, and bounded fields. Structured logs improve filtering and correlation. They do not replace durable job state or supervisor exit status. Local logs can be lost with the host and can fill the filesystem; the cloud handoff requires external export in later courses.

Sensitive data should not be logged. Course 1 job payloads are fixtures. Later security and observability courses deepen redaction and retention.

## Backup and restore game

The final defense performs a backup of durable Atlas state, restores it into an independent path, verifies hashes and permissions, and checks that completed job results remain readable. If the course is run in a VM or cloud, the stronger exercise replaces the machine and reattaches or restores state.

Measure observed recovery time and recovered point. Do not turn one measurement into a universal RTO/RPO guarantee.

## Multi-fault game day

A bounded final exercise introduces faults in stages:

1. terminate the worker during or after a claim;
2. make durable storage unwritable or substitute the deterministic fault fixture;
3. stop the API backend while the edge remains up;
4. present an invalid or expired certificate fixture;
5. change a name-resolution entry or query the wrong name;
6. restore the baseline and verify no residual process, route, mount, or temporary file remains.

For each stage record hypothesis, action, first failing oracle, diagnosis, repair, and residual risk. Stop the exercise if cleanup or host access becomes uncertain.

## Runbooks answer decisions, not just commands

A useful runbook states trigger, scope, authority, safety checks, decision points, commands, expected outputs, abort conditions, recovery, and escalation. “Restart service” is a command fragment. “If the worker heartbeat is stale but a processing claim is younger than the lease, stop routing new work, preserve evidence, and wait or terminate according to the grace policy” is an operational decision.

The course includes final runbooks for service failure, storage failure, certificate failure, and instance replacement.

## Manifest and provenance boundaries

The course manifest records exact payload files, sizes, modes, and SHA-256 digests. This proves archive integrity relative to the manifest. It does not prove who authored the files, whether the build host was uncompromised, or whether dependencies are free of vulnerabilities. Later supply-chain courses add stronger provenance.

The Course 2 handoff has its own manifest because it is a contract between courses, not an accidental subset of the repository.

## Final architecture defense

Defend Atlas from the outside inward:

```text
DNS name
→ TLS edge and trust
→ firewall and listener
→ loopback API
→ service identity and resource envelope
→ durable spool and worker
→ backup and recovery
→ VM image and cloud identity
→ region/zone and replacement assumptions
```

For every arrow explain:

- which component owns the transition;
- which identity is used;
- which data crosses;
- which timeout or resource boundary applies;
- what happens on failure;
- which evidence was actually executed.

## Outgoing maturity boundary

After Course 1, the learner can operate and defend one host and specify its cloud requirements. The learner has not yet created reproducible cloud resources, remote infrastructure state, reusable modules, account landing zones, or policy-as-code for infrastructure changes. Those are Course 2 responsibilities.

The handoff is successful when Course 2 can begin without rediscovering what the workload needs or inventing availability claims from provider defaults.

## Atlas implementation bridge

Run `make capstone-tour`, `make linux-proof`, `make systemd-proof`, and the final lab routes available in your environment. Rebuild the handoff manifest only after all requirements are stable. Verify the course manifest after cleanup so generated evidence cannot silently become release content.

The final defense is not a presentation of files. It is a causal walk through one request, one job, one failure, one recovery, and one machine-replacement requirement.

## Design review prompts

- Which claim is strongest, and which evidence class supports it?
- Which cleanup step is most dangerous if a variable is wrong?
- Which rollback becomes unsafe after state change?
- Which local single-host limitation must Course 2 address?
- Can a new engineer reconstruct the host without undocumented knowledge?

## Boundary case: repair creates a second incident

Under pressure, operators may disable TLS verification, open the firewall, run as root, make code writable, or delete state to recover capacity. These actions can restore one symptom while destroying security or durability. Every emergency action needs a time bound, owner, compensating control, and explicit rollback.

The final game day scores preservation of earlier boundaries, not only speed to green.

## Boundary case: clean state after proof

Tests that leave processes, mounts, routes, generated keys, reports, or temporary files make the next run ambiguous and can contaminate release archives. Cleanup is part of correctness. The packaging proof runs from a clean extraction, executes the course, cleans generated outputs, and verifies manifests again.

## Final defense worksheet

```text
promise:
implementation owner:
failure injected:
first oracle:
diagnosis:
repair:
regression:
cleanup:
evidence class:
stronger unexecuted claim:
Course 2 requirement produced:
```

Complete the worksheet for process, storage, network/TLS, and machine replacement. These four paths demonstrate the maturity of the whole course.

## Field method: conduct a production-readiness review from claims

A release review begins with claims, not with a checklist of installed tools. For each Atlas promise, record the owner, mechanism, failure mode, oracle, executed evidence class, and residual risk. A green process list cannot compensate for an unverified restore; a valid certificate cannot compensate for an exposed administrative listener; a successful local tour cannot prove a cloud-zone claim.

Use four end-to-end paths in the final defense:

1. **Normal request:** verified HTTPS reaches the edge, the API durably accepts a job, the worker publishes a result, and the client reads it.
2. **Graceful change:** routing admission stops, in-flight work drains within budget, processes terminate, and restart restores readiness without duplicate effects.
3. **Ungraceful failure:** a worker or machine disappears after a known transition; recovery uses durable evidence and does not invent success.
4. **State recovery:** an empty replacement receives the declared release and configuration, restores durable state from the approved source, and passes the same client oracle.

The game day is bounded. Define blast radius, abort conditions, console access, backup or snapshot, named controller, evidence recorder, and cleanup owner before injecting a fault. Change one variable at a time unless the purpose is explicitly to test correlated failure. Capture the first failed oracle before applying a repair.

Emergency work must preserve earlier guarantees. Opening the firewall to the world, disabling TLS verification, making `/opt/atlas` writable, or running the service as root may make one symptom disappear while creating a more serious incident. If an exceptional action is unavoidable, time-bound it, name an approver, add a compensating control, and prove reversal.

The final output is the Course 2 handoff. It contains requirements rather than cloud resources: compute profile, identity boundaries, network flows, storage classes, DNS/TLS/load-balancer behavior, metadata policy, failure-domain claim, quotas, recovery scenarios, and evidence acceptance criteria. Course 2 may choose AWS resources as its primary lane, but it must preserve these behaviors or record an explicit requirements change.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| Readiness must fail when a declared routing prerequisite fails. | Atlas operational contract | fault injection and edge behavior |
| A restore exercise is required before a recoverability claim. | Atlas recovery policy | restored bytes, permissions, and observed time |
| The outgoing handoff is independently manifested. | program handoff policy | handoff manifest verification |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Readiness as liveness

Keeping a failed writer ready prevents routing from protecting the service.

### Rollback without state analysis

Returning to old code can be unsafe after a configuration or data transition.

### Evidence inflation

A local deterministic tour cannot be reported as proof of provider zone, quota, or managed-service behavior.


## Module synthesis

Return to the central question: **Can the host be installed, started, observed, upgraded, degraded, recovered, and replaced without making a claim stronger than the evidence?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**Readiness reports success while durable storage is read-only, so the proxy continues to send mutating traffic to a process that cannot keep its promise.**—fails for the predicted reason.

## Continue

Course 2 encodes the outgoing requirements as reproducible cloud infrastructure and governed state.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
