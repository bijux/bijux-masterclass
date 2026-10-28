# PERF-08 — Planner Cost Release Gate

## Mutation

Version-dependent planner cost is treated as stable latency evidence.

## Why it is tempting

The mutation can make one visible metric look better or make the experiment
simpler. It is therefore realistic enough to survive a superficial review.

## Required rejection

The decisive oracle is `plan-policy-review`. The proof must fail before a latency or
throughput improvement can approve the candidate.
