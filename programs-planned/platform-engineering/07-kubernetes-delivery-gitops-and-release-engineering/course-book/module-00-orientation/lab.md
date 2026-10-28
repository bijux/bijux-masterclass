# Laboratory — Establish a trustworthy Course 7 starting point

## Goal

Verify the Course 6 handoff, initialize a local environment repository, and prove that two commits have distinct identities even when they render the same resources.

## Safety boundary

Use only the course working directory. Do not point the exercise at a real cluster, production repository, or credential store.

## Baseline

The predecessor handoff is present. No Git history or orientation report has been created.

## Hypothesis

A delivery system needs both source identity and rendered identity because either one alone loses information needed for review and diagnosis.

## Controlled action

Run `make predecessor-proof`. Initialize a temporary Git repository. Commit the production overlay. Create a second commit that changes only explanatory comments. Use the capstone renderer to compute both rendered-set digests. Record both commit IDs and render digests.

## Oracle

The commit IDs differ. The rendered-set digests are equal. The report explains why promotion records must preserve both identities.

## Required evidence

Save the predecessor proof output, `git log --show-signature --oneline` output where available, both render digests, tool availability, and the selected primary lane.

## Interpretation

If commit identity and render identity are equal in the report, the learner has probably hashed the wrong input. If the rendered digests differ, inspect canonicalization and comment handling.

## Cleanup

Delete only the temporary repository and generated report. Re-run `make predecessor-proof` to prove that cleanup did not alter the immutable handoff.

## Completion gate

The learner can state which facts Git proves, which facts rendering proves, and which facts still require a live controller and cluster.
