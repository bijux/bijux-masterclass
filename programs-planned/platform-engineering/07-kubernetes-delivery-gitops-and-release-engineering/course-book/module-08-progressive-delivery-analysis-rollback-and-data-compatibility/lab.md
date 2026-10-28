# Laboratory — Reject a reassuring but invalid canary

## Goal

Run a canary whose aggregate error rate passes while one required segment fails and the minimum sample condition is unmet.

## Safety boundary

Use synthetic request and metric fixtures. Do not route real user traffic.

## Baseline

The candidate is initially eligible for 5% exposure and data compatibility gates pass.

## Hypothesis

A sound analysis should reject or mark inconclusive when segment failure or insufficient samples invalidate the aggregate result.

## Controlled action

Execute the canary steps, first with misleading aggregate metrics, then with corrected segment and sample policies. Exercise abort and Git desired-state repair.

## Oracle

The first analysis is rejected as unsound. The corrected analysis aborts the candidate, restores stable traffic, and creates a durable rollback revision without changing protected data.

## Required evidence

Save configured and actual weights, raw counts, metric queries, thresholds, segment results, abort state, Git commit, and rollback-frontier statement.

## Interpretation

A green average is not a valid oracle. Explain which population would have been harmed and why the initial test missed it.

## Cleanup

Reset the semantic router and environment repository to the accepted stable release, then prove no pending canary state remains.

## Completion gate

The learner can distinguish configured exposure, actual exposure, analysis validity, and rollback safety.
