# Practical assessment — repair an inconsistent workload release

You receive a candidate with these defects:

- deployment selects `platform/atlas-api:1.0.0` by tag;
- the arm64 child contains an amd64 executable;
- a fixture secret is hidden by a later whiteout;
- runtime profile requests UID 0 and a writable root;
- SBOM omits Atlas itself;
- provenance is validly signed by an unauthorized builder;
- Course 4 handoff refers to the previous digest.

## Required work

1. Preserve the original candidate and write an evidence inventory.
2. Identify the earliest failing gate for every defect.
3. Repair source/build/runtime/evidence configuration without weakening the Course 2 contract.
4. Rebuild and produce exact OCI graph identities.
5. Verify all platform executables and runtime write paths.
6. Generate subject-bound inventory, vulnerability/VEX, provenance, and signature evidence.
7. Publish through the loopback registry by digest and verify referrers.
8. Produce an accepted or review-required decision with explicit evidence boundary.
9. Regenerate the Course 4 handoff.
10. Demonstrate that every planted defect is rejected by a proof capable of failing.

## Submission

Submit the release record, evidence journal, object-graph diagram, effective runtime profile, policy report, defect-to-proof matrix, exact handoff manifest, and a five-minute recorded or live defense.

A candidate that “runs” but violates identity, platform, secret, runtime, or subject-binding gates cannot pass.
