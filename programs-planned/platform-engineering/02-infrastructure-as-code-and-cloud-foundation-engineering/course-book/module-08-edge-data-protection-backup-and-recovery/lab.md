# Lab — Restore Atlas Through a New Edge Path

## Goal

Prove that a public request reaches only the governed edge and that an acknowledged Atlas result can be restored into an empty destination with its integrity intact.

## Safety boundary

The dependency-light lane uses local TLS/edge and storage fixtures. The AWS lane creates an ALB, certificate/DNS resources only when the learner controls a sandbox zone or uses a documented temporary name, and must pass the cost/cleanup preflight.

## Baseline

Use the safe edge and backup fixtures under:

```text
capstone/fixtures/edge/
capstone/fixtures/recovery/
```

Submit one deterministic Atlas job and record its result hash before backup.

## Hypothesis

Traffic can enter only through the declared edge, and the latest protected backup can reproduce the acknowledged result in a clean destination without relying on the failed host’s root disk.

## Controlled action

1. Validate DNS, listener, target-group, and security-group intent.
2. Evaluate `bad-host-public-ingress.json` and `bad-health-optional-dependency.json`.
3. Start the dependency-light TLS edge and verify correct-host success and wrong-host failure.
4. Submit and complete a deterministic job.
5. Generate a backup manifest and protected copy.
6. Delete the working recovery directory, create an empty destination, and restore.
7. Verify checksums, ownership, and completed-job semantics.
8. Inject a disabled-key or missing-permission fixture and show why the encrypted backup is unusable.
9. Measure the restore sequence and compare it with the declared RTO hypothesis.
10. Optional AWS lane: repeat against the ALB, EBS snapshot, and S3 backup.

## Oracle

The safe result demonstrates:

- only the edge has public ingress;
- TLS authenticates the requested name;
- target health is meaningful but not overcoupled;
- the result was acknowledged before backup;
- restoration starts empty;
- restored bytes match the manifest;
- missing key authority blocks recovery visibly;
- measured recovery is reported without claiming regional resilience.

## Evidence

Retain:

```text
reports/module-08/request-path.json
reports/module-08/tls-check.json
reports/module-08/security-path.json
reports/module-08/backup-manifest.json
reports/module-08/restore-result.json
reports/module-08/rpo-rto-observation.json
```

For AWS, include resource IDs, target-health evidence, snapshot/object IDs, key ID, CloudTrail references, DNS/TLS output, and cleanup inventory.

## Interpretation

Separate what the lab proves about bytes and request routing from what it does not prove about multi-zone availability, regional disaster recovery, long-term durability, or operated response time.

## Cleanup

Stop local processes, remove temporary certificates and restored directories, and destroy optional AWS ALB, target group, records, certificates where appropriate, snapshots, volumes, and backup objects according to the lab retention policy. Verify no target or billable edge resource remains.

## Completion gate

Present one request-path trace and one recovery trace. Every step must identify its owner, evidence, and failure result.
