# Lab — Release Atlas Cloud Foundation 1.0

## Goal

Run the complete Course 2 release decision from source through policy, plan, verification evidence, failure handling, and Course 3 handoff.

## Safety boundary

The dependency-light route creates no cloud resource. The optional AWS route requires the declared sandbox account, budget, region, federated/short-lived identity, backend, and explicit `ALLOW_AWS_APPLY=1`. The course never applies automatically from `core-proof`.

## Baseline

Use the final stacks and release candidates:

```text
capstone/stacks/foundation/
capstone/stacks/workload-dev/
capstone/releases/accepted/
capstone/releases/rejected-public-ssh/
capstone/releases/review-nat-cost/
capstone/releases/not-executed-live-cloud/
```

## Hypothesis

Only a candidate whose source, dependencies, target, plan, policies, cost/quota assumptions, data-plane checks, recovery evidence, and handoff are coherent can be called Atlas Cloud Foundation 1.0.

## Controlled action

1. Run formatting/static checks and the complete dependency-light test suite.
2. Verify the Course 1 predecessor manifest.
3. Build the plan model for the accepted candidate.
4. Evaluate all policy outcomes.
5. Confirm that the public-SSH candidate fails and the NAT-cost candidate requires review.
6. Bind the accepted plan to source, lock, state, target, policy, and approval identities.
7. Inject a partial-apply fixture and produce a containment/roll-forward decision.
8. Run the Atlas request, replacement, backup, and restore tours.
9. Generate the Foundation 1.0 release dossier and Course 3 handoff manifest.
10. Optional AWS lane: initialize backend, produce a saved plan, review it, apply with the apply role, run data-plane verification, then destroy or retain under an explicit lease.

## Oracle

The release system:

- never applies an unapproved or regenerated plan;
- uses no long-lived static cloud key in the course path;
- blocks non-compensable safety failures;
- distinguishes review and not-executed from pass;
- records cost and quota assumptions;
- handles partial apply from observed reality;
- verifies user-facing behavior and recovery;
- produces an exact Course 3 handoff;
- leaves no unmanaged sandbox resource.

## Evidence

Retain:

```text
reports/final/source-identity.json
reports/final/dependency-identity.json
reports/final/plan-summary.json
reports/final/policy-result.json
reports/final/cost-quota.json
reports/final/apply-or-not-executed.json
reports/final/data-plane-proof.json
reports/final/recovery-proof.json
reports/final/release-dossier.json
capstone/handoff/MANIFEST.json
```

For AWS, include saved-plan digest, apply transcript, target account/region, role session, CloudTrail references, endpoint checks, resource inventory, and cleanup proof.

## Interpretation

Write a release conclusion that separates:

- dependency-light semantic evidence;
- local Atlas process/data evidence;
- real-cloud control-plane evidence;
- real-cloud data-plane evidence;
- unexecuted multi-account, zone-failure, or regional-recovery claims.

## Cleanup

Run the course clean target. For AWS, destroy in dependency order, inspect state and remote inventory, remove retained snapshots/objects only according to policy, and verify no ALB, NAT gateway, instance, volume, address, hosted-zone record, or log bucket remains unintentionally billable.

## Completion gate

Defend Atlas Cloud Foundation 1.0 using the release dossier. Every claim must identify its evidence class and every missing proof must remain visible.
