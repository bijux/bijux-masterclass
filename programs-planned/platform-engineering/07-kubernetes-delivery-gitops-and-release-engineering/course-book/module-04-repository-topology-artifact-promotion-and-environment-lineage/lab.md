# Laboratory — Promote without rebuilding

## Goal

Move one immutable Atlas candidate through dev, staging, and production while preserving exact artifact identity and environment-specific render identity.

## Safety boundary

Use a temporary local Git repository and synthetic artifact catalogue. Do not push to a real remote.

## Baseline

The candidate exists in dev only. Staging and production reference the predecessor.

## Hypothesis

Promotion should change environment selection and render evidence without changing image or chart bytes.

## Controlled action

Create dev, staging, and production promotion commits. Attempt one prohibited rebuild under the same tag and one force-push rewrite of production history in the semantic model.

## Oracle

All accepted promotions reference the same artifact digests. Render digests differ only where environment configuration differs. Rebuild and rewritten-history candidates are rejected.

## Required evidence

Save Git commit graph, artifact catalogue, promotion records, rendered diffs, rejection reasons, and release lineage.

## Interpretation

If promotion changes an artifact digest, it is a new candidate. If production history can be rewritten without detection, release lineage is not trustworthy.

## Cleanup

Delete the temporary remote only after exporting the evidence bundle. Re-run the lineage verifier against the exported records.

## Completion gate

The learner can prove that production received the tested candidate and identify every environment-specific difference.
