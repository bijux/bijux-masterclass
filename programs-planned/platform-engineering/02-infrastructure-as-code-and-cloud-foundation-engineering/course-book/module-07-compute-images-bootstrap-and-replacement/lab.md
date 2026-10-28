# Lab — Prove a Host Can Be Replaced

## Goal

Demonstrate that Atlas machine identity is disposable while its declared configuration and durable workload facts survive.

## Safety boundary

The dependency-light path uses the Atlas cloud model and local fixture data. The optional AWS path must run only in the declared sandbox account, use the cost tags, and pass `aws-preflight` before creating an instance or volume.

## Baseline

Use:

```text
capstone/fixtures/compute/image-release-v1.json
capstone/fixtures/compute/launch-template-v1.json
capstone/fixtures/compute/atlas-data-volume.json
```

The baseline has a pinned image, required IMDSv2, a narrow instance role, a separate data volume, and a known readiness contract.

## Hypothesis

A replacement created from the same governed release can assume the correct authority, reconstruct its runtime configuration, recover the durable Atlas result, and become ready without copying the failed host’s root filesystem.

## Controlled action

1. Validate the image and launch contracts.
2. Evaluate `bad-bootstrap-secret.json` and explain every exposure path.
3. Evaluate `mutable-latest-image.json` and identify why the release is not reproducible.
4. Simulate a host loss while preserving the data-volume snapshot.
5. Produce replacement actions for launch-template version 2.
6. Run the bootstrap/readiness simulator.
7. Verify the restored result checksum.
8. Evaluate quota with and without temporary double capacity.
9. Optional AWS lane: create the sandbox instance, submit one Atlas job, snapshot the data volume, replace the instance, restore the volume, and verify the result.

## Oracle

The safe candidate:

- contains no secret in user data;
- pins image and architecture;
- requires IMDSv2;
- uses only the Atlas instance role;
- leaves durable state outside the root filesystem;
- refuses replacement when quota or attachment constraints are unsatisfied;
- does not mark readiness before mount, identity, and application checks pass.

## Evidence

Retain:

```text
reports/module-07/image-contract.json
reports/module-07/replacement-plan.json
reports/module-07/bootstrap-result.json
reports/module-07/readiness-result.json
reports/module-07/quota-preflight.json
reports/module-07/result-checksum.json
```

For the AWS lane, also retain instance, volume, snapshot, launch-template, CloudTrail, and cleanup identifiers. Do not publish credentials or user-data secrets.

## Interpretation

Explain which properties are established by static contracts, which by the local simulator, and which only by a real instance. A successful simulator is not evidence that cloud-init, metadata, block attachment, or provider health checks worked in AWS.

## Cleanup

Terminate created instances, delete temporary volumes and snapshots that are not retained as evidence, remove DNS/target registrations, and verify that no billable resource remains. Keep the evidence files and source release identities.

## Completion gate

Defend the replacement sequence from lost host through restored Atlas result, including the single-zone and singleton limitations that still remain.
