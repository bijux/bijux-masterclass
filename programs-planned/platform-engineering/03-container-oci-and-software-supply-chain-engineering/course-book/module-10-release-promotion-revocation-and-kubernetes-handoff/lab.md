# Laboratory — Promote one digest and revoke the right thing

## Goal

Evaluate all release candidates, promote the accepted Atlas digest, exercise one revocation scenario, and produce the exact Course 4 handoff.

## Safety boundary

Use the local registry and fixture keys. Do not publish tags or revocation statements to external systems.

## Baseline

Run the complete capstone tour and load every candidate under `capstone/releases/` and `capstone/planted-defects/`.

## Hypothesis

Only the accepted digest satisfies every non-compensable gate. Promotion changes target metadata/tags but not image bytes. Revocation action depends on whether the image, key, evidence, or tag is compromised.

## Controlled action

1. evaluate all candidates in gate order;
2. promote accepted digest from candidate to staging metadata;
3. move a tag and confirm the release subject remains fixed;
4. simulate signing-key compromise;
5. create a new verifier policy and reevaluate the digest using independent evidence;
6. generate the Course 4 handoff and verify its manifest.

## Oracle

Exactly one checked candidate is accepted. Defects fail at their intended gates. Key revocation does not mutate image bytes. The handoff references the same approved digests and contains no secrets.

## Evidence

Submit release-decision report, candidate failure matrix, promotion record, key-compromise timeline, retention decision, and verified handoff manifest.

## Interpretation

Explain why promotion, deployment, rollback, and revocation are related but distinct operations.

## Cleanup

Restore fixture verifier policy, remove temporary tags/reports, and rerun manifest and capstone proofs.

## Completion gate

Another learner can begin Course 4 using only the handoff and identify exact images, runtime obligations, evidence expectations, and unresolved environment-backed proof.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
